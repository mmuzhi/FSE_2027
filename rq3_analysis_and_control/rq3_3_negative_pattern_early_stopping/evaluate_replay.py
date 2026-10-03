"""Summarize RQ3.3 replay logs."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


def iter_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def safe_div(num: float, den: float) -> float:
    return num / den if den else 0.0


def binary_auc(y_true: list[int], scores: list[float]) -> float:
    pairs = [(score, label) for score, label in zip(scores, y_true) if score is not None]
    if not pairs:
        return 0.0
    positives = sum(label for _, label in pairs)
    negatives = len(pairs) - positives
    if positives == 0 or negatives == 0:
        return 0.0
    pairs.sort(key=lambda item: item[0])
    rank_sum = 0.0
    idx = 0
    rank = 1
    while idx < len(pairs):
        j = idx
        while j < len(pairs) and pairs[j][0] == pairs[idx][0]:
            j += 1
        avg_rank = (rank + (rank + (j - idx) - 1)) / 2.0
        rank_sum += avg_rank * sum(label for _, label in pairs[idx:j])
        rank += j - idx
        idx = j
    return (rank_sum - positives * (positives + 1) / 2.0) / (positives * negatives)


def ablation_scores(loop_features: dict[str, Any]) -> dict[str, float]:
    return {
        "full": float(loop_features.get("raw", 0.0)),
        "-explore": float(loop_features.get("raw", 0.0)) - 2.0 * float(loop_features.get("explore_segment_ratio", 0.0)),
        "-no_build": float(loop_features.get("raw", 0.0)) - 1.5 * float(loop_features.get("distance_since_last_build_norm", 0.0)),
        "-no_verify": float(loop_features.get("raw", 0.0)) - 1.0 * float(loop_features.get("distance_since_last_verify_norm", 0.0)),
        "-novelty": float(loop_features.get("raw", 0.0)) - 1.0 * float(loop_features.get("low_novelty", 0.0)),
        "-motif": float(loop_features.get("raw", 0.0)) - 2.5 * float(loop_features.get("motif_risk_bonus", 0.0)),
        "-healthy": float(loop_features.get("raw", 0.0)) + 2.0 * float(loop_features.get("healthy_loop_bonus", 0.0)),
    }


def summarize(events: list[dict[str, Any]]) -> dict[str, Any]:
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_sample: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        by_task[event.get("task", "unknown")].append(event)
        by_sample[event["task_id"]].append(event)

    sample_trigger = {}
    for task_id, rows in by_sample.items():
        triggered = [row for row in rows if row.get("would_trigger")]
        first = min(triggered, key=lambda row: row["segment_id"]) if triggered else None
        sample_trigger[task_id] = first

    pass_samples = {
        task_id for task_id, rows in by_sample.items() if rows and rows[0].get("passed") is True
    }
    fail_samples = {
        task_id for task_id, rows in by_sample.items() if rows and rows[0].get("passed") is False
    }
    triggered_samples = {task_id for task_id, row in sample_trigger.items() if row}
    false_positive = {
        task_id for task_id, row in sample_trigger.items() if row and row.get("is_false_positive")
    }
    fail_triggered = {
        task_id for task_id, row in sample_trigger.items() if row and task_id in fail_samples
    }
    oracle_useful = {
        task_id
        for task_id, row in sample_trigger.items()
        if row and row.get("oracle_action") == "stop-and-finalize"
    }

    savings = []
    for task_id, row in sample_trigger.items():
        if not row:
            continue
        total = max(int(row.get("num_segments_total", 0)), 1)
        saved = max(total - int(row.get("segment_id", 0)) - 1, 0)
        savings.append(saved / total)

    motif_counter = Counter()
    oracle_counter = Counter()
    oracle_labels = []
    full_scores = []
    single_signal_scores = defaultdict(list)
    ablation_buckets = defaultdict(list)
    for event in events:
        oracle_counter[event.get("oracle_action", "unknown")] += 1
        label = int(event.get("oracle_action") == "stop-and-finalize")
        oracle_labels.append(label)
        loop_features = event.get("loop_features", {})
        full_scores.append(float(loop_features.get("raw", 0.0)))
        for key in (
            "explore_segment_ratio",
            "distance_since_last_build_norm",
            "distance_since_last_verify_norm",
            "low_novelty",
            "motif_risk_bonus",
            "healthy_loop_bonus",
        ):
            value = float(loop_features.get(key, 0.0))
            if key == "healthy_loop_bonus":
                value = -value
            single_signal_scores[key].append(value)
        for name, score in ablation_scores(loop_features).items():
            ablation_buckets[name].append(score)
        for hit in event.get("motif_hits", []):
            motif_counter["->".join(hit.get("motif", []))] += 1

    ablation_auc = {name: binary_auc(oracle_labels, scores) for name, scores in ablation_buckets.items()}
    single_signal_auc = {name: binary_auc(oracle_labels, scores) for name, scores in single_signal_scores.items()}

    return {
        "num_events": len(events),
        "num_samples": len(by_sample),
        "num_pass_samples": len(pass_samples),
        "num_fail_samples": len(fail_samples),
        "triggered_samples": len(triggered_samples),
        "sample_trigger_rate": safe_div(len(triggered_samples), len(by_sample)),
        "pass_false_trigger_rate": safe_div(len(false_positive & pass_samples), len(pass_samples)),
        "fail_trigger_rate": safe_div(len(fail_triggered), len(fail_samples)),
        "fail_oracle_useful_trigger_rate": safe_div(len(oracle_useful & fail_samples), len(fail_samples)),
        "oracle_useful_trigger_rate": safe_div(len(oracle_useful), len(triggered_samples)),
        "fail_useful_trigger_rate": safe_div(len(oracle_useful & fail_samples), len(fail_samples)),
        "useful_trigger_rate": safe_div(len(oracle_useful), len(triggered_samples)),
        "avg_segment_saving_ratio": sum(savings) / len(savings) if savings else 0.0,
        "action_counts": Counter(event.get("action", "unknown") for event in events),
        "trigger_type_counts": Counter(event.get("trigger_type", "unknown") for event in events),
        "oracle_action_counts": oracle_counter,
        "oracle_stop_auc_full": binary_auc(oracle_labels, full_scores),
        "ablation_auc": ablation_auc,
        "single_signal_auc": single_signal_auc,
        "motif_counts": motif_counter,
        "by_task": {
            task: {
                "num_events": len(rows),
                "trigger_events": sum(1 for row in rows if row.get("would_trigger")),
                "avg_loop_score": sum(float(row.get("loop_score", 0.0)) for row in rows) / max(len(rows), 1),
                "avg_closure_score": sum(float(row.get("closure_score", 0.0)) for row in rows) / max(len(rows), 1),
            }
            for task, rows in by_task.items()
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RQ3.3 replay logs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    input_path = Path(args.input)
    events = list(iter_jsonl(input_path))
    summary = summarize(events)
    output_path = Path(args.output) if args.output else (
        ROOT / "data" / "derived_cot" / "rq3_negative_pattern_early_stopping" / "replay_metrics" / f"{input_path.stem}.json"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"Wrote metrics to {output_path}")


if __name__ == "__main__":
    main()
