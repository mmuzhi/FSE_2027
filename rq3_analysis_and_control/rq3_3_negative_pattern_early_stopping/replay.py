"""Offline replay engine for RQ3.3 structure-aware stopping."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from data_loader import (
    default_eval_path,
    load_rq41_jsonl,
    load_segmentation_map,
    resolve_default_results,
    resolve_default_segmentation,
)
from motif_detector import detect_motifs
from policy import PolicyEngine, load_policy_config
from schema import append_compressed, normalize_model_name, normalize_task_name
from state_model import RuleStateModel
from state_tracker import StateTracker, split_micro_units


ROOT = Path(__file__).resolve().parents[2]


def score_suffix(segments: list[dict[str, Any]], start_index: int) -> dict[str, Any]:
    suffix = segments[start_index + 1 :]
    suffix_coarse = [seg["coarse_state"] for seg in suffix]
    build_or_verify = any(state in {"Build", "Verify", "Wrap"} for state in suffix_coarse)
    explore_ratio = (
        sum(1 for state in suffix_coarse if state == "Explore") / len(suffix_coarse)
        if suffix_coarse
        else 0.0
    )
    avg_novelty = (
        sum(float(seg.get("avg_novelty", 1.0)) for seg in suffix) / len(suffix)
        if suffix
        else 1.0
    )
    return {
        "suffix_len": len(suffix),
        "suffix_has_build_verify_wrap": build_or_verify,
        "suffix_explore_ratio": explore_ratio,
        "suffix_avg_novelty": avg_novelty,
    }


def oracle_action(
    sample_passed: bool | None,
    task: str,
    segments: list[dict[str, Any]],
    segment_id: int,
    motif_result: dict[str, Any],
    window_state: dict[str, Any],
) -> tuple[str, str]:
    suffix = score_suffix(segments, segment_id)
    prefix = segments[: segment_id + 1]
    prefix_has_productive = any(seg["coarse_state"] in {"Build", "Verify", "Wrap"} for seg in prefix)
    prefix_ratio = float(window_state.get("prefix_segment_ratio", 0.0))
    current_has_fail_motif = float(motif_result.get("motif_risk_bonus", 0.0)) > 0.0
    current_has_healthy = float(motif_result.get("healthy_loop_bonus", 0.0)) > 0.0
    suffix_fine_path: list[dict[str, Any]] = []
    for segment in segments[segment_id + 1 :]:
        append_compressed(suffix_fine_path, segment["fine_state"])
    suffix_motif_result = detect_motifs(suffix_fine_path, task)
    suffix_has_fail_motif = float(suffix_motif_result.get("motif_risk_bonus", 0.0)) > 0.0
    suffix_has_healthy = float(suffix_motif_result.get("healthy_loop_bonus", 0.0)) > 0.0

    if suffix["suffix_has_build_verify_wrap"] and sample_passed is True:
        return "continue", "suffix adds productive Build/Verify/Wrap and full sample passes"
    if (
        sample_passed is False
        and current_has_fail_motif
        and not current_has_healthy
        and prefix_ratio >= 0.15
        and (
            suffix_has_fail_motif
            or suffix["suffix_explore_ratio"] >= 0.5
            or not suffix["suffix_has_build_verify_wrap"]
        )
        and not suffix_has_healthy
    ):
        return "stop-and-finalize", "fail-rich anti-pattern already identified and suffix shows no healthy recovery"
    if (
        prefix_has_productive
        and suffix["suffix_explore_ratio"] >= 0.66
        and suffix["suffix_avg_novelty"] <= 0.55
        and not suffix["suffix_has_build_verify_wrap"]
    ):
        return "stop-and-finalize", "prefix has productive state and suffix is low-novelty Explore-heavy"
    if sample_passed is False and not suffix["suffix_has_build_verify_wrap"]:
        return "stop-and-finalize", "full sample fails and suffix shows no productive progress"
    return "continue", "insufficient evidence that stopping is safe"


def build_segments(sample: dict[str, Any], segmentation_record: dict[str, Any] | None = None) -> StateTracker:
    tracker = StateTracker(model=RuleStateModel())
    steps = segmentation_record.get("segmentation_result", {}).get("steps") if segmentation_record else None
    if steps:
        for step in steps:
            text = step.get("content", "")
            weak_label = step.get("category")
            for unit_text in split_micro_units(text):
                scores = tracker.model.score(unit_text, weak_fine_label=weak_label)
                tracker.add_unit(unit_text, scores=scores)
        tracker.finalize()
        return tracker
    tracker.feed_text(sample.get("cot", ""))
    tracker.finalize()
    return tracker


def replay_samples(
    samples: list,
    segmentation_map: dict[str, dict[str, Any]],
    task: str,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for sample_obj in samples:
        sample = sample_obj.to_dict() if hasattr(sample_obj, "to_dict") else dict(sample_obj)
        tracker = build_segments(sample, segmentation_map.get(sample["task_id"]))
        policy_engine = PolicyEngine(config)
        segments = tracker.closed_segments
        if not segments:
            continue
        coarse_path: list[dict[str, Any]] = []
        fine_path: list[dict[str, Any]] = []
        distance_since_last_build = 0
        distance_since_last_verify = 0
        prefix_segments: list[dict[str, Any]] = []

        for segment in segments:
            prefix_segments.append(segment)
            append_compressed(coarse_path, segment["coarse_state"])
            append_compressed(fine_path, segment["fine_state"])
            if segment["coarse_state"] == "Build":
                distance_since_last_build = 0
            else:
                distance_since_last_build += 1
            if segment["coarse_state"] == "Verify":
                distance_since_last_verify = 0
            else:
                distance_since_last_verify += 1

            recent = prefix_segments[-3:]
            recent_novelty = [seg["avg_novelty"] for seg in prefix_segments[-2:]]
            explore_ratio = sum(1 for seg in recent if seg["coarse_state"] == "Explore") / max(len(recent), 1)
            latest_text = segment["segment_text"].lower()
            wrap_language_indicator = int(
                any(cue in latest_text for cue in ("therefore", "finally", "answer", "output", "print", "result is", "final"))
            )
            window_state = {
                "segments": list(prefix_segments),
                "recent_segments": recent,
                "has_answer_started": False,
                "segment_id": segment["segment_id"],
                "prefix_segment_ratio": (segment["segment_id"] + 1) / max(len(segments), 1),
                "distance_since_last_build": distance_since_last_build,
                "distance_since_last_verify": distance_since_last_verify,
                "coarse_compressed_path": [dict(item) for item in coarse_path],
                "fine_compressed_path": [dict(item) for item in fine_path],
                "avg_novelty_recent_2": sum(recent_novelty) / len(recent_novelty) if recent_novelty else 1.0,
                "explore_segment_ratio": explore_ratio,
                "wrap_language_indicator": wrap_language_indicator,
            }
            motif_result = detect_motifs(window_state["fine_compressed_path"], task)
            decision = policy_engine.evaluate(window_state, motif_result)
            oracle, oracle_reason = oracle_action(
                sample.get("passed"),
                task,
                segments,
                segment["segment_id"],
                motif_result,
                window_state,
            )
            suffix = score_suffix(segments, segment["segment_id"])
            is_false_positive = bool(
                decision["would_trigger"]
                and sample.get("passed") is True
                and oracle == "continue"
            )
            is_useful_trigger = bool(
                decision["would_trigger"]
                and (sample.get("passed") is False or oracle == "stop-and-finalize")
            )
            events.append(
                {
                    "task_id": sample["task_id"],
                    "task": task,
                    "difficulty": sample.get("difficulty", "unknown"),
                    "model": sample.get("model", "unknown"),
                    "passed": sample.get("passed"),
                    "policy_name": decision["policy_name"],
                    "segment_id": segment["segment_id"],
                    "num_segments_total": len(segments),
                    "segment_text": segment["segment_text"],
                    "coarse_state": segment["coarse_state"],
                    "fine_state": segment["fine_state"],
                    "coarse_compressed_path": window_state["coarse_compressed_path"],
                    "fine_compressed_path": window_state["fine_compressed_path"],
                    "loop_score": decision["loop_score"],
                    "closure_score": decision["closure_score"],
                    "healthy_loop_bonus": decision["healthy_loop_bonus"],
                    "recent_fail_motif_bonus": decision.get("recent_fail_motif_bonus", 0.0),
                    "recent_healthy_motif_bonus": decision.get("recent_healthy_motif_bonus", 0.0),
                    "loop_features": decision.get("loop_features", {}),
                    "closure_features": decision.get("closure_features", {}),
                    "avg_novelty_recent_2": window_state["avg_novelty_recent_2"],
                    "action": decision["action"],
                    "would_trigger": decision["would_trigger"],
                    "trigger_type": decision["trigger_type"],
                    "trigger_reason": decision["trigger_reason"],
                    "oracle_action": oracle,
                    "oracle_reason": oracle_reason,
                    "is_false_positive": is_false_positive,
                    "is_useful_trigger": is_useful_trigger,
                    "motif_hits": motif_result["motif_hits"],
                    "suffix_summary": suffix,
                    "prefix_segment_ratio": window_state["prefix_segment_ratio"],
                }
            )
    return events


def main() -> None:
    parser = argparse.ArgumentParser(description="Run RQ3.3 offline replay.")
    parser.add_argument("--task", default="execution")
    parser.add_argument("--model", default="qwen")
    parser.add_argument("--results", default="")
    parser.add_argument("--eval", default="")
    parser.add_argument("--segmentation", default="")
    parser.add_argument("--config", default="")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    task = normalize_task_name(args.task)
    model = normalize_model_name(args.model)
    results_path = Path(args.results) if args.results else resolve_default_results(task, model)
    eval_path = Path(args.eval) if args.eval else default_eval_path(task, model)
    segmentation_path = Path(args.segmentation) if args.segmentation else resolve_default_segmentation(task, model)
    samples = load_rq41_jsonl(results_path, task, model, eval_path, limit=args.limit if args.limit > 0 else None)
    segmentation_map = load_segmentation_map(segmentation_path) if segmentation_path else {}
    config = load_policy_config(args.config or None, task=task)
    events = replay_samples(samples, segmentation_map, task, config)

    output = Path(args.output) if args.output else (
        ROOT / "data" / "derived_cot" / "rq3_negative_pattern_early_stopping" / "replay_logs" / f"{task}_{model}_{config.get('policy_name', 'global')}.jsonl"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in events), encoding="utf-8")
    print(f"Wrote {len(events)} replay events to {output}")


if __name__ == "__main__":
    main()
