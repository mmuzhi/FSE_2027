"""Grid-search policy thresholds on existing replay logs."""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path
from typing import Any


DEFAULT_OBJECTIVE_WEIGHTS = {
    "fail_oracle_useful": 1.4,
    "pass_false_penalty": 1.4,
    "oracle_useful": 0.8,
    "fail_trigger": 0.3,
    "segment_saving": 0.2,
}

POLICY_PARAM_KEYS = (
    "loop_risk_threshold",
    "closure_low_threshold",
    "debounce_windows",
    "min_decision_segments",
    "low_novelty_threshold",
    "min_explore_ratio_for_loop_trigger",
    "min_prefix_segment_ratio_for_loop_trigger",
    "min_segment_index_for_loop_trigger",
    "min_reasoning_chars_for_loop_trigger",
    "min_token_progress_for_loop_trigger",
    "min_reasoning_chars_for_closure_no_answer",
    "require_build_or_verify_for_closure_no_answer",
    "require_fail_motif_for_loop_trigger",
    "require_recent_fail_motif_for_loop_trigger",
    "max_fail_motif_age_for_loop_trigger",
    "block_loop_on_recent_healthy_motif",
    "max_healthy_motif_age_for_loop_block",
    "require_current_explore_for_loop_trigger",
    "repetition_trigger_enabled",
    "repetition_min_segment_id",
    "repetition_min_chars",
    "repetition_window_chars",
    "repetition_ngram_ratio_threshold",
    "repetition_tail_min_repeats",
    "repetition_tail_chars_threshold",
)

GROUP_BY_FIELDS = {
    "all": (),
    "task": ("task",),
    "difficulty": ("difficulty",),
    "model": ("model",),
    "task+difficulty": ("task", "difficulty"),
    "task+model": ("task", "model"),
    "task+difficulty+model": ("task", "difficulty", "model"),
}

DELTA_KEYS = (
    "objective",
    "pass_false_trigger_rate",
    "fail_trigger_rate",
    "fail_oracle_useful_trigger_rate",
    "oracle_useful_trigger_rate",
    "avg_segment_saving_ratio",
)


def rank_key(item: dict[str, Any]) -> tuple[float, float, float, float, float]:
    return (
        item["objective"],
        item["fail_oracle_useful_trigger_rate"],
        item["oracle_useful_trigger_rate"],
        -item["pass_false_trigger_rate"],
        item["avg_segment_saving_ratio"],
    )


def iter_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def group_by_sample(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        row["_loop_score"] = float(row.get("loop_score", 0.0))
        row["_closure_score"] = float(row.get("closure_score", 1.0))
        row["_avg_novelty_recent_2"] = float(row.get("avg_novelty_recent_2", 1.0))
        row["_motif_bonus"] = float(row.get("loop_features", {}).get("motif_risk_bonus", 0.0))
        row["_explore_ratio"] = float(row.get("loop_features", {}).get("explore_segment_ratio", 0.0))
        row["_prefix_ratio"] = float(row.get("prefix_segment_ratio", 0.0))
        row["_prefix_reasoning_chars"] = int(row.get("prefix_reasoning_chars", 0) or 0)
        row["_token_progress"] = float(row.get("token_progress", 1.0))
        row["_segment_id"] = int(row.get("segment_id", 0))
        row["_prefix_segments"] = row["_segment_id"] + 1
        row["_oracle_stop"] = row.get("oracle_action") == "stop-and-finalize"
        grouped.setdefault(row["task_id"], []).append(row)
    for task_id in grouped:
        grouped[task_id].sort(key=lambda item: item["segment_id"])
    return grouped


def split_sample_labels(grouped: dict[str, list[dict[str, Any]]]) -> tuple[set[str], set[str], set[str]]:
    pass_samples: set[str] = set()
    fail_samples: set[str] = set()
    unknown_samples: set[str] = set()
    for task_id, items in grouped.items():
        if not items:
            continue
        passed = items[0].get("passed")
        if passed is True:
            pass_samples.add(task_id)
        elif passed is False:
            fail_samples.add(task_id)
        else:
            unknown_samples.add(task_id)
    return pass_samples, fail_samples, unknown_samples


def sample_group_identity(rows: list[dict[str, Any]], group_by: str) -> tuple[str, dict[str, str]]:
    fields = GROUP_BY_FIELDS[group_by]
    if not fields:
        return "all", {}
    first = rows[0]
    values = {
        field: str(first.get(field, "unknown") or "unknown")
        for field in fields
    }
    key = "|".join(f"{field}={value}" for field, value in values.items())
    return key, values


def build_group_slices(
    grouped: dict[str, list[dict[str, Any]]],
    group_by: str,
    include_unknown: bool,
    min_labeled_samples: int,
) -> dict[str, dict[str, Any]]:
    slices: dict[str, dict[str, Any]] = {}
    for task_id, rows in grouped.items():
        if not rows:
            continue
        if rows[0].get("passed") is None and not include_unknown:
            continue
        group_key, group_values = sample_group_identity(rows, group_by)
        payload = slices.setdefault(
            group_key,
            {
                "group_key": group_key,
                "group_values": group_values,
                "samples": {},
            },
        )
        payload["samples"][task_id] = rows

    filtered: dict[str, dict[str, Any]] = {}
    for group_key, payload in slices.items():
        pass_samples, fail_samples, _ = split_sample_labels(payload["samples"])
        if len(pass_samples) + len(fail_samples) < min_labeled_samples:
            continue
        filtered[group_key] = payload
    return filtered


def recent_motif_bonus(row: dict[str, Any], kind: str, max_age: int) -> float:
    hits = row.get("motif_hits", [])
    fine_path_len = len(row.get("fine_compressed_path", []))
    if not isinstance(hits, list) or fine_path_len <= 0:
        return 0.0
    return max(
        (
            float(hit.get("bonus", 0.0))
            for hit in hits
            if hit.get("kind") == kind
            and fine_path_len - 1 - int(hit.get("end", -fine_path_len)) <= max_age
        ),
        default=0.0,
    )


def should_trigger(row: dict[str, Any], params: dict[str, Any], consecutive_hits: int) -> tuple[bool, int]:
    loop_score = row["_loop_score"]
    closure_score = row["_closure_score"]
    avg_novelty_recent_2 = row["_avg_novelty_recent_2"]
    motif_bonus = row["_motif_bonus"]
    recent_fail_motif_bonus = recent_motif_bonus(
        row,
        "fail",
        int(params.get("max_fail_motif_age_for_loop_trigger", 999)),
    )
    recent_healthy_motif_bonus = recent_motif_bonus(
        row,
        "healthy",
        int(params.get("max_healthy_motif_age_for_loop_block", 1)),
    )
    explore_ratio = row["_explore_ratio"]
    prefix_ratio = row["_prefix_ratio"]
    prefix_segments = row["_prefix_segments"]
    has_low_novelty = avg_novelty_recent_2 <= float(params.get("low_novelty_threshold", 1.0))
    has_motif = (
        recent_fail_motif_bonus > 0.0
        if bool(params.get("require_recent_fail_motif_for_loop_trigger", False))
        else motif_bonus > 0.0
    )
    has_recent_healthy_motif = recent_healthy_motif_bonus > 0.0
    required_prefix_segments = max(
        int(params["min_decision_segments"]),
        int(params["min_segment_index_for_loop_trigger"]) + 1,
    )
    passes = (
        prefix_segments >= required_prefix_segments
        and loop_score >= float(params["loop_risk_threshold"])
        and closure_score <= float(params["closure_low_threshold"])
        and (has_low_novelty or has_motif)
        and explore_ratio >= float(params["min_explore_ratio_for_loop_trigger"])
        and prefix_ratio >= float(params["min_prefix_segment_ratio_for_loop_trigger"])
        and row["_prefix_reasoning_chars"] >= int(params.get("min_reasoning_chars_for_loop_trigger", 0))
        and row["_token_progress"] >= float(params.get("min_token_progress_for_loop_trigger", 0.0))
        and ((not params["require_fail_motif_for_loop_trigger"]) or has_motif)
        and (
            not bool(params.get("require_current_explore_for_loop_trigger", False))
            or row.get("coarse_state") == "Explore"
        )
        and (
            not bool(params.get("block_loop_on_recent_healthy_motif", False))
            or not has_recent_healthy_motif
        )
    )
    if passes:
        consecutive_hits += 1
    else:
        consecutive_hits = 0
    return consecutive_hits >= int(params["debounce_windows"]), consecutive_hits


def summarize_first_trigger(
    first_trigger: dict[str, dict[str, Any]],
    pass_samples: set[str],
    fail_samples: set[str],
    unknown_samples: set[str],
) -> dict[str, Any]:
    labeled_samples = pass_samples | fail_samples
    labeled_first_trigger = {
        task_id: row
        for task_id, row in first_trigger.items()
        if task_id in labeled_samples
    }
    false_triggers = sum(
        1
        for task_id, row in labeled_first_trigger.items()
        if task_id in pass_samples and row.get("oracle_action") == "continue"
    )
    fail_triggered = sum(
        1
        for task_id in labeled_first_trigger
        if task_id in fail_samples
    )
    oracle_useful_fail = sum(
        1
        for task_id, row in labeled_first_trigger.items()
        if task_id in fail_samples and row["_oracle_stop"]
    )
    oracle_useful_triggered = sum(
        1
        for row in labeled_first_trigger.values()
        if row["_oracle_stop"]
    )
    savings = [
        max(row.get("num_segments_total", 0) - row.get("segment_id", 0) - 1, 0) / max(row.get("num_segments_total", 1), 1)
        for row in labeled_first_trigger.values()
    ]

    pass_false_trigger_rate = false_triggers / len(pass_samples) if pass_samples else 0.0
    fail_trigger_rate = fail_triggered / len(fail_samples) if fail_samples else 0.0
    fail_oracle_useful_trigger_rate = oracle_useful_fail / len(fail_samples) if fail_samples else 0.0
    oracle_useful_trigger_rate = (
        oracle_useful_triggered / len(labeled_first_trigger)
        if labeled_first_trigger
        else 0.0
    )
    avg_segment_saving_ratio = sum(savings) / len(savings) if savings else 0.0

    return {
        "num_pass_samples": len(pass_samples),
        "num_fail_samples": len(fail_samples),
        "num_unknown_samples": len(unknown_samples),
        "triggered_samples": len(first_trigger),
        "triggered_labeled_samples": len(labeled_first_trigger),
        "triggered_unknown_samples": sum(1 for task_id in first_trigger if task_id in unknown_samples),
        "pass_false_trigger_rate": pass_false_trigger_rate,
        "fail_trigger_rate": fail_trigger_rate,
        "fail_oracle_useful_trigger_rate": fail_oracle_useful_trigger_rate,
        "oracle_useful_trigger_rate": oracle_useful_trigger_rate,
        "avg_segment_saving_ratio": avg_segment_saving_ratio,
    }


def compute_objective(metrics: dict[str, Any], weights: dict[str, float]) -> float:
    return (
        weights["fail_oracle_useful"] * float(metrics["fail_oracle_useful_trigger_rate"])
        - weights["pass_false_penalty"] * float(metrics["pass_false_trigger_rate"])
        + weights["oracle_useful"] * float(metrics["oracle_useful_trigger_rate"])
        + weights["fail_trigger"] * float(metrics["fail_trigger_rate"])
        + weights["segment_saving"] * float(metrics["avg_segment_saving_ratio"])
    )


def metric_deltas(current: dict[str, Any], reference: dict[str, Any]) -> dict[str, float]:
    return {
        key: float(current.get(key, 0.0)) - float(reference.get(key, 0.0))
        for key in DELTA_KEYS
    }


def build_baseline_metrics(
    grouped: dict[str, list[dict[str, Any]]],
    pass_samples: set[str],
    fail_samples: set[str],
    unknown_samples: set[str],
    weights: dict[str, float],
) -> dict[str, Any]:
    first_trigger: dict[str, dict[str, Any]] = {}
    for task_id, items in grouped.items():
        for row in items:
            if row.get("would_trigger"):
                first_trigger[task_id] = row
                break
    metrics = summarize_first_trigger(first_trigger, pass_samples, fail_samples, unknown_samples)
    metrics["objective"] = compute_objective(metrics, weights)
    return metrics


def default_fixed_budget_values(task_hint: str | None) -> tuple[list[int], list[float]]:
    return {
        "execution": ([3, 4, 6, 8], [0.25, 0.50, 0.75]),
        "generation": ([4, 8, 12, 16], [0.25, 0.50, 0.75]),
    }.get(task_hint or "", ([4, 8, 12], [0.25, 0.50, 0.75]))


def evaluate_fixed_budget(
    grouped: dict[str, list[dict[str, Any]]],
    pass_samples: set[str],
    fail_samples: set[str],
    unknown_samples: set[str],
    weights: dict[str, float],
    *,
    label: str,
    strategy: str,
    threshold: float,
) -> dict[str, Any]:
    first_trigger: dict[str, dict[str, Any]] = {}
    for task_id, items in grouped.items():
        for row in items:
            if strategy == "segments":
                should_fire = int(row.get("_prefix_segments", 0)) >= int(threshold)
            else:
                should_fire = float(row.get("_prefix_ratio", 0.0)) >= float(threshold)
            if should_fire:
                first_trigger[task_id] = row
                break
    metrics = summarize_first_trigger(first_trigger, pass_samples, fail_samples, unknown_samples)
    metrics["objective"] = compute_objective(metrics, weights)
    metrics["label"] = label
    metrics["strategy"] = strategy
    metrics["threshold"] = threshold
    return metrics


def build_fixed_budget_baselines(
    grouped: dict[str, list[dict[str, Any]]],
    pass_samples: set[str],
    fail_samples: set[str],
    unknown_samples: set[str],
    weights: dict[str, float],
    task_hint: str | None,
    segment_values: list[int],
    ratio_values: list[float],
    max_pass_false_trigger_rate: float,
    min_fail_oracle_useful_trigger_rate: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    default_segments, default_ratios = default_fixed_budget_values(task_hint)
    segment_thresholds = sorted({int(value) for value in (segment_values or default_segments) if int(value) > 0})
    ratio_thresholds = sorted({float(value) for value in (ratio_values or default_ratios) if 0.0 < float(value) <= 1.0})
    baseline_specs = (
        [(f"fixed_segments_{threshold}", "segments", threshold) for threshold in segment_thresholds]
        + [(f"fixed_ratio_{threshold:.2f}", "ratio", threshold) for threshold in ratio_thresholds]
    )
    baselines = [
        evaluate_fixed_budget(
            grouped,
            pass_samples,
            fail_samples,
            unknown_samples,
            weights,
            label=label,
            strategy=strategy,
            threshold=threshold,
        )
        for label, strategy, threshold in baseline_specs
    ]
    for item in baselines:
        item["meets_constraints"] = bool(
            item["pass_false_trigger_rate"] <= max_pass_false_trigger_rate
            and item["fail_oracle_useful_trigger_rate"] >= min_fail_oracle_useful_trigger_rate
        )
    constrained = [item for item in baselines if item["meets_constraints"]]
    ranked = constrained or list(baselines)
    ranked.sort(key=rank_key, reverse=True)
    best = dict(ranked[0]) if ranked else {}
    if best:
        best["selection_source"] = "constrained" if constrained else "overall"
    return baselines, best


def evaluate_params(
    grouped: dict[str, list[dict[str, Any]]],
    pass_samples: set[str],
    fail_samples: set[str],
    unknown_samples: set[str],
    params: dict[str, Any],
    group_key: str,
    group_values: dict[str, str],
    weights: dict[str, float],
    baseline_metrics: dict[str, Any],
    best_fixed_budget: dict[str, Any],
) -> dict[str, Any]:
    first_trigger: dict[str, dict[str, Any]] = {}
    for task_id, items in grouped.items():
        consecutive_hits = 0
        for row in items:
            triggered, consecutive_hits = should_trigger(row, params, consecutive_hits)
            if triggered:
                first_trigger[task_id] = row
                break

    metrics = summarize_first_trigger(first_trigger, pass_samples, fail_samples, unknown_samples)
    objective = compute_objective(metrics, weights)
    metrics["objective"] = objective
    deltas = metric_deltas(metrics, baseline_metrics)
    vs_best_fixed_budget = metric_deltas(metrics, best_fixed_budget) if best_fixed_budget else {}

    return {
        "group_key": group_key,
        "group_values": group_values,
        "params": params,
        **metrics,
        "fail_useful_trigger_rate": metrics["fail_oracle_useful_trigger_rate"],
        "useful_trigger_rate": metrics["oracle_useful_trigger_rate"],
        "baseline": baseline_metrics,
        "deltas": deltas,
        "best_fixed_budget": best_fixed_budget,
        "vs_best_fixed_budget": vs_best_fixed_budget,
    }


def simplify_search_space(search_space: dict[str, list[Any]]) -> dict[str, list[Any]]:
    simplified = {key: list(values) for key, values in search_space.items()}
    require_values = simplified.get("require_fail_motif_for_loop_trigger", [])
    if require_values and all(bool(value) for value in require_values):
        simplified["low_novelty_threshold"] = [simplified["low_novelty_threshold"][0]]
    return simplified


def equivalent_param_key(params: dict[str, Any]) -> tuple[tuple[str, Any], ...]:
    normalized = dict(params)
    normalized["effective_min_prefix_segments"] = max(
        int(normalized["min_decision_segments"]),
        int(normalized["min_segment_index_for_loop_trigger"]) + 1,
    )
    if normalized["require_fail_motif_for_loop_trigger"]:
        normalized["low_novelty_threshold"] = 1.0
    normalized.pop("min_decision_segments", None)
    return tuple(sorted(normalized.items()))


def infer_task_hint(grouped: dict[str, list[dict[str, Any]]]) -> str | None:
    tasks = {
        str(items[0].get("task", "unknown"))
        for items in grouped.values()
        if items
    }
    return next(iter(tasks)) if len(tasks) == 1 else None


def build_search_space(mode: str, task_hint: str | None = None) -> dict[str, list[Any]]:
    if task_hint == "generation":
        if mode == "narrow":
            return {
                "loop_risk_threshold": [0.82, 0.86, 0.90],
                "closure_low_threshold": [0.50, 0.55],
                "debounce_windows": [3, 4],
                "min_decision_segments": [8, 10, 12],
                "low_novelty_threshold": [0.65, 0.70],
                "min_explore_ratio_for_loop_trigger": [0.85, 0.90],
                "min_prefix_segment_ratio_for_loop_trigger": [0.30, 0.35, 0.40],
                "min_segment_index_for_loop_trigger": [40, 60, 80],
                "min_reasoning_chars_for_loop_trigger": [8000, 10000, 12000],
                "min_token_progress_for_loop_trigger": [0.0],
                "require_fail_motif_for_loop_trigger": [True],
                "require_recent_fail_motif_for_loop_trigger": [True],
                "max_fail_motif_age_for_loop_trigger": [1, 2],
                "block_loop_on_recent_healthy_motif": [True],
                "max_healthy_motif_age_for_loop_block": [1, 2],
                "require_current_explore_for_loop_trigger": [True],
            }
        return {
            "loop_risk_threshold": [0.82, 0.86, 0.90, 0.94, 0.97],
            "closure_low_threshold": [0.45, 0.50, 0.55],
            "debounce_windows": [2, 3, 4],
            "min_decision_segments": [6, 8, 10, 12],
            "low_novelty_threshold": [0.60, 0.65, 0.70],
            "min_explore_ratio_for_loop_trigger": [0.75, 0.85, 0.90, 0.95],
            "min_prefix_segment_ratio_for_loop_trigger": [0.20, 0.30, 0.40, 0.50],
            "min_segment_index_for_loop_trigger": [20, 40, 60, 80, 100],
            "min_reasoning_chars_for_loop_trigger": [0, 8000, 12000],
            "min_token_progress_for_loop_trigger": [0.0],
            "require_fail_motif_for_loop_trigger": [False, True],
            "require_recent_fail_motif_for_loop_trigger": [False, True],
            "max_fail_motif_age_for_loop_trigger": [1, 2],
            "block_loop_on_recent_healthy_motif": [False, True],
            "max_healthy_motif_age_for_loop_block": [1, 2],
            "require_current_explore_for_loop_trigger": [False, True],
        }
    if task_hint == "execution":
        if mode == "narrow":
            return {
                "loop_risk_threshold": [0.78, 0.82, 0.86],
                "closure_low_threshold": [0.45, 0.50, 0.55],
                "debounce_windows": [2, 3],
                "min_decision_segments": [4, 6, 8],
                "low_novelty_threshold": [0.65, 0.75, 0.85],
                "min_explore_ratio_for_loop_trigger": [0.34, 0.50, 0.67],
                "min_prefix_segment_ratio_for_loop_trigger": [0.0, 0.05, 0.10],
                "min_segment_index_for_loop_trigger": [2, 4, 6, 8],
                "require_fail_motif_for_loop_trigger": [False, True],
            }
        return {
            "loop_risk_threshold": [0.78, 0.82, 0.86, 0.90, 0.94],
            "closure_low_threshold": [0.40, 0.45, 0.50, 0.55],
            "debounce_windows": [1, 2, 3, 4],
            "min_decision_segments": [3, 4, 6, 8, 10],
            "low_novelty_threshold": [0.45, 0.55, 0.65, 0.75],
            "min_explore_ratio_for_loop_trigger": [0.34, 0.50, 0.67, 0.75, 0.85],
            "min_prefix_segment_ratio_for_loop_trigger": [0.0, 0.05, 0.10, 0.15, 0.20],
            "min_segment_index_for_loop_trigger": [2, 4, 8, 12, 20, 30],
            "require_fail_motif_for_loop_trigger": [False, True],
        }
    if mode == "narrow":
        return {
            "loop_risk_threshold": [0.82, 0.86, 0.90],
            "closure_low_threshold": [0.50, 0.55],
            "debounce_windows": [2, 3, 4],
            "min_decision_segments": [6, 8, 10],
            "low_novelty_threshold": [0.60, 0.65, 0.70],
            "min_explore_ratio_for_loop_trigger": [0.75, 0.85, 0.90],
            "min_prefix_segment_ratio_for_loop_trigger": [0.20, 0.30, 0.40],
            "min_segment_index_for_loop_trigger": [20, 40, 60, 80],
            "require_fail_motif_for_loop_trigger": [False, True],
        }
    return {
        "loop_risk_threshold": [0.78, 0.82, 0.86, 0.90, 0.94],
        "closure_low_threshold": [0.40, 0.45, 0.50, 0.55],
        "debounce_windows": [1, 2, 3, 4],
        "min_decision_segments": [3, 4, 6, 8, 10, 12],
        "low_novelty_threshold": [0.45, 0.55, 0.65, 0.75],
        "min_explore_ratio_for_loop_trigger": [0.34, 0.50, 0.67, 0.75, 0.85, 0.95],
        "min_prefix_segment_ratio_for_loop_trigger": [0.05, 0.10, 0.20, 0.30, 0.40, 0.50],
        "min_segment_index_for_loop_trigger": [4, 8, 20, 40, 60, 80, 100],
        "require_fail_motif_for_loop_trigger": [False, True],
    }


def extract_policy_params(params: dict[str, Any]) -> dict[str, Any]:
    return {key: params[key] for key in POLICY_PARAM_KEYS if key in params}


def build_config_payload(grouped_payloads: list[dict[str, Any]], group_by: str, policy_name: str) -> dict[str, Any]:
    if not grouped_payloads:
        return {"policy_name": policy_name}
    if group_by == "all":
        first = grouped_payloads[0]
        best_params = extract_policy_params(first["top_candidates"][0]["params"]) if first["top_candidates"] else {}
        return {"policy_name": policy_name, **best_params}
    if group_by == "task":
        tasks: dict[str, Any] = {}
        for item in grouped_payloads:
            if not item["top_candidates"]:
                continue
            task_name = item["group_values"].get("task", item["group_key"])
            tasks[task_name] = extract_policy_params(item["top_candidates"][0]["params"])
        return {"policy_name": policy_name, "tasks": tasks}
    slices: list[dict[str, Any]] = []
    for item in grouped_payloads:
        if not item["top_candidates"]:
            continue
        slices.append(
            {
                "match": item["group_values"],
                **extract_policy_params(item["top_candidates"][0]["params"]),
            }
        )
    return {"policy_name": policy_name, "slices": slices}


def main() -> None:
    parser = argparse.ArgumentParser(description="Tune replay policy thresholds from existing logs.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--top-k", type=int, default=10)
    parser.add_argument("--output", default="")
    parser.add_argument("--config-output", default="")
    parser.add_argument("--policy-name", default="tuned_policy")
    parser.add_argument("--mode", choices=["narrow", "broad"], default="narrow")
    parser.add_argument(
        "--group-by",
        choices=sorted(GROUP_BY_FIELDS),
        default="all",
        help="Tune one global threshold set or one set per task/difficulty/model slice.",
    )
    parser.add_argument(
        "--include-unknown",
        action="store_true",
        help="Keep samples without pass/fail labels inside slice construction. They are still excluded from objective denominators.",
    )
    parser.add_argument(
        "--min-labeled-samples",
        type=int,
        default=20,
        help="Skip slices with too few labeled samples for stable tuning.",
    )
    parser.add_argument("--max-pass-false-trigger-rate", type=float, default=0.22)
    parser.add_argument("--min-fail-oracle-useful-trigger-rate", type=float, default=0.10)
    parser.add_argument(
        "--fixed-budget-segments",
        type=int,
        nargs="*",
        default=[],
        help="Optional fixed segment budgets for naive stop-and-finalize baselines.",
    )
    parser.add_argument(
        "--fixed-budget-ratios",
        type=float,
        nargs="*",
        default=[],
        help="Optional fixed prefix-ratio budgets for naive stop-and-finalize baselines.",
    )
    parser.add_argument("--weight-fail-oracle-useful", type=float, default=DEFAULT_OBJECTIVE_WEIGHTS["fail_oracle_useful"])
    parser.add_argument("--weight-pass-false-penalty", type=float, default=DEFAULT_OBJECTIVE_WEIGHTS["pass_false_penalty"])
    parser.add_argument("--weight-oracle-useful", type=float, default=DEFAULT_OBJECTIVE_WEIGHTS["oracle_useful"])
    parser.add_argument("--weight-fail-trigger", type=float, default=DEFAULT_OBJECTIVE_WEIGHTS["fail_trigger"])
    parser.add_argument("--weight-segment-saving", type=float, default=DEFAULT_OBJECTIVE_WEIGHTS["segment_saving"])
    args = parser.parse_args()

    rows = iter_jsonl(Path(args.input))
    grouped = group_by_sample(rows)
    grouped_slices = build_group_slices(
        grouped,
        group_by=args.group_by,
        include_unknown=args.include_unknown,
        min_labeled_samples=args.min_labeled_samples,
    )
    if not grouped_slices:
        raise SystemExit("No slices matched the current filters. Try lowering --min-labeled-samples or enabling --include-unknown.")

    weights = {
        "fail_oracle_useful": args.weight_fail_oracle_useful,
        "pass_false_penalty": args.weight_pass_false_penalty,
        "oracle_useful": args.weight_oracle_useful,
        "fail_trigger": args.weight_fail_trigger,
        "segment_saving": args.weight_segment_saving,
    }

    grouped_payloads: list[dict[str, Any]] = []
    for slice_payload in grouped_slices.values():
        slice_grouped = slice_payload["samples"]
        pass_samples, fail_samples, unknown_samples = split_sample_labels(slice_grouped)
        task_hint = infer_task_hint(slice_grouped)
        search_space = simplify_search_space(build_search_space(args.mode, task_hint=task_hint))
        keys = list(search_space)
        baseline_metrics = build_baseline_metrics(
            slice_grouped,
            pass_samples,
            fail_samples,
            unknown_samples,
            weights,
        )
        fixed_budget_baselines, best_fixed_budget = build_fixed_budget_baselines(
            slice_grouped,
            pass_samples,
            fail_samples,
            unknown_samples,
            weights,
            task_hint,
            args.fixed_budget_segments,
            args.fixed_budget_ratios,
            args.max_pass_false_trigger_rate,
            args.min_fail_oracle_useful_trigger_rate,
        )
        results: list[dict[str, Any]] = []
        all_results: list[dict[str, Any]] = []
        seen_param_keys: set[tuple[tuple[str, Any], ...]] = set()
        for values in itertools.product(*(search_space[key] for key in keys)):
            params = dict(zip(keys, values))
            cache_key = equivalent_param_key(params)
            if cache_key in seen_param_keys:
                continue
            seen_param_keys.add(cache_key)
            result = evaluate_params(
                slice_grouped,
                pass_samples,
                fail_samples,
                unknown_samples,
                params,
                group_key=slice_payload["group_key"],
                group_values=slice_payload["group_values"],
                weights=weights,
                baseline_metrics=baseline_metrics,
                best_fixed_budget=best_fixed_budget,
            )
            all_results.append(result)
            if (
                result["pass_false_trigger_rate"] <= args.max_pass_false_trigger_rate
                and result["fail_oracle_useful_trigger_rate"] >= args.min_fail_oracle_useful_trigger_rate
            ):
                results.append(result)

        if not results:
            results = all_results

        results.sort(key=rank_key, reverse=True)
        grouped_payloads.append(
            {
                "group_key": slice_payload["group_key"],
                "group_values": slice_payload["group_values"],
                "task_hint": task_hint or "mixed",
                "baseline": baseline_metrics,
                "best_fixed_budget": best_fixed_budget,
                "fixed_budget_baselines": fixed_budget_baselines,
                "num_candidates_considered": len(all_results),
                "top_candidates": results[: args.top_k],
            }
        )

    payload: Any
    if args.group_by == "all" and len(grouped_payloads) == 1:
        payload = grouped_payloads[0]["top_candidates"]
    else:
        payload = grouped_payloads

    payload_text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(payload_text)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(payload_text, encoding="utf-8")
    if args.config_output:
        config_payload = build_config_payload(grouped_payloads, args.group_by, args.policy_name)
        config_output_path = Path(args.config_output)
        config_output_path.parent.mkdir(parents=True, exist_ok=True)
        config_output_path.write_text(json.dumps(config_payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
