"""Interpretable RQ3.3 replay policy."""

from __future__ import annotations

import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_POLICY_CONFIG = {
    "policy_name": "global_default",
    "loop_risk_threshold": 0.82,
    "closure_score_threshold": 0.85,
    "closure_low_threshold": 0.55,
    "closure_score_threshold_no_answer": 0.92,
    "require_wrap_evidence_no_answer": True,
    "debounce_windows": 2,
    "min_decision_segments": 4,
    "low_novelty_threshold": 0.65,
    "min_explore_ratio_for_loop_trigger": 0.0,
    "min_prefix_segment_ratio_for_loop_trigger": 0.0,
    "min_segment_index_for_loop_trigger": 0,
    "min_reasoning_chars_for_loop_trigger": 0,
    "min_token_progress_for_loop_trigger": 0.0,
    "min_reasoning_chars_for_closure_no_answer": 0,
    "require_build_or_verify_for_closure_no_answer": False,
    "require_fail_motif_for_loop_trigger": False,
    "require_recent_fail_motif_for_loop_trigger": False,
    "max_fail_motif_age_for_loop_trigger": 999,
    "block_loop_on_recent_healthy_motif": False,
    "max_healthy_motif_age_for_loop_block": 1,
    "require_current_explore_for_loop_trigger": False,
    "distance_norm": 6,
    "loop_weights": {
        "w_explore": 2.0,
        "w_no_build": 1.5,
        "w_no_verify": 1.0,
        "w_novelty": 1.0,
        "w_motif": 2.5,
        "w_healthy": 2.0,
        "w_answer": 3.0,
    },
    "closure_weights": {
        "w_bv_path": 2.0,
        "w_bvw_path": 3.0,
        "w_answer": 2.5,
        "w_wrap_lang": 1.5,
        "w_explore": 1.5,
    },
}


def sigmoid(value: float) -> float:
    return 1.0 / (1.0 + math.exp(-value))


def load_policy_config(path: str | None = None, task: str | None = None) -> dict[str, Any]:
    config = deepcopy(DEFAULT_POLICY_CONFIG)
    if not path:
        return config
    cfg_path = Path(path)
    if not cfg_path.exists():
        return config
    user_config = json.loads(cfg_path.read_text(encoding="utf-8"))
    _deep_update(config, user_config)
    tasks = user_config.get("tasks", {})
    if task and isinstance(tasks, dict) and task in tasks and isinstance(tasks[task], dict):
        _deep_update(config, tasks[task])
    return config


def _deep_update(base: dict[str, Any], incoming: dict[str, Any]) -> None:
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_update(base[key], value)
        else:
            base[key] = value


def _path_contains(path: list[dict[str, Any]], pattern: tuple[str, ...]) -> bool:
    states = [item["state"] for item in path]
    width = len(pattern)
    return any(tuple(states[start : start + width]) == pattern for start in range(len(states) - width + 1))


def _recent_motif_bonus(
    motif_result: dict[str, Any],
    key: str,
    path_len: int,
    max_age: int,
) -> float:
    hits = motif_result.get(key, [])
    if not isinstance(hits, list) or path_len <= 0:
        return 0.0
    return max(
        (
            float(hit.get("bonus", 0.0))
            for hit in hits
            if path_len - 1 - int(hit.get("end", -path_len)) <= max_age
        ),
        default=0.0,
    )


def has_closure_evidence_without_answer(window_state: dict[str, Any], config: dict[str, Any]) -> bool:
    if not bool(config.get("require_wrap_evidence_no_answer", True)):
        return True
    recent = window_state.get("recent_segments", [])
    if not recent:
        return False
    latest = recent[-1]
    latest_coarse = latest.get("coarse_state")
    latest_fine = latest.get("fine_state")
    wrap_lang = bool(window_state.get("wrap_language_indicator", 0))
    return latest_fine not in {"MR", "PU", "SD", "KR"} and (
        latest_coarse == "Wrap"
        or latest_fine == "AUX"
        or (latest_coarse == "Verify" and latest_fine == "VV" and wrap_lang)
    )


class PolicyEngine:
    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config or load_policy_config()
        self.consecutive_loop_windows = 0

    def evaluate(self, window_state: dict[str, Any], motif_result: dict[str, Any]) -> dict[str, Any]:
        config = self.config
        loop_features = compute_loop_features(window_state, motif_result, config)
        closure_features = compute_closure_features(window_state, config)
        loop_score = sigmoid(loop_features["raw"])
        closure_score = sigmoid(closure_features["raw"])
        action = "continue"
        trigger_type = "none"
        trigger_reason = "scores below trigger thresholds"
        num_segments = len(window_state.get("segments", []))
        has_low_novelty = (
            float(window_state.get("avg_novelty_recent_2", 1.0))
            <= float(config.get("low_novelty_threshold", 0.65))
        )
        fine_path_len = len(window_state.get("fine_compressed_path", []))
        recent_fail_motif_bonus = _recent_motif_bonus(
            motif_result,
            "matched_fail_motifs",
            fine_path_len,
            int(config.get("max_fail_motif_age_for_loop_trigger", 999)),
        )
        recent_healthy_motif_bonus = _recent_motif_bonus(
            motif_result,
            "matched_healthy_motifs",
            fine_path_len,
            int(config.get("max_healthy_motif_age_for_loop_block", 1)),
        )
        require_recent_fail_motif = bool(config.get("require_recent_fail_motif_for_loop_trigger", False))
        has_motif = (
            recent_fail_motif_bonus > 0.0
            if require_recent_fail_motif
            else float(motif_result.get("motif_risk_bonus", 0.0)) > 0.0
        )
        recent_healthy_motif = recent_healthy_motif_bonus > 0.0
        explore_ratio = float(window_state.get("explore_segment_ratio", 0.0))
        prefix_segment_ratio = float(window_state.get("prefix_segment_ratio", 0.0))
        segment_id = int(window_state.get("segment_id", 0))
        recent = window_state.get("recent_segments", [])
        current_coarse_state = recent[-1].get("coarse_state") if recent else ""
        require_fail_motif = bool(config.get("require_fail_motif_for_loop_trigger", False))
        passes_guardrails = (
            explore_ratio >= float(config.get("min_explore_ratio_for_loop_trigger", 0.0))
            and prefix_segment_ratio >= float(config.get("min_prefix_segment_ratio_for_loop_trigger", 0.0))
            and segment_id >= int(config.get("min_segment_index_for_loop_trigger", 0))
            and ((not require_fail_motif) or has_motif)
            and (
                not bool(config.get("require_current_explore_for_loop_trigger", False))
                or current_coarse_state == "Explore"
            )
            and (
                not bool(config.get("block_loop_on_recent_healthy_motif", False))
                or not recent_healthy_motif
            )
        )
        has_no_answer_closure_evidence = has_closure_evidence_without_answer(window_state, config)
        prefix_reasoning_chars = int(window_state.get("prefix_reasoning_chars", 0) or 0)
        token_progress = float(window_state.get("token_progress", 1.0))
        has_build_or_verify = any(
            item.get("state") in {"Build", "Verify"}
            for item in window_state.get("coarse_compressed_path", [])
        )
        passes_loop_budget_guard = (
            prefix_reasoning_chars >= int(config.get("min_reasoning_chars_for_loop_trigger", 0))
            and token_progress >= float(config.get("min_token_progress_for_loop_trigger", 0.0))
        )
        passes_no_answer_closure_guard = (
            prefix_reasoning_chars >= int(config.get("min_reasoning_chars_for_closure_no_answer", 0))
            and (
                not bool(config.get("require_build_or_verify_for_closure_no_answer", False))
                or has_build_or_verify
            )
        )

        if (
            num_segments >= int(config.get("min_decision_segments", 1))
            and loop_score >= config["loop_risk_threshold"]
            and closure_score <= config["closure_low_threshold"]
            and (has_low_novelty or has_motif)
            and passes_guardrails
            and passes_loop_budget_guard
        ):
            self.consecutive_loop_windows += 1
        else:
            self.consecutive_loop_windows = 0

        min_segments_for_closure = int(config.get("min_decision_segments", 1))
        if (
            num_segments >= min_segments_for_closure
            and closure_score >= config["closure_score_threshold"]
            and window_state.get("has_answer_started")
        ):
            action = "stop"
            trigger_type = "closure"
            trigger_reason = "high closure score with answer started"
        elif (
            num_segments >= min_segments_for_closure
            and closure_score >= float(config.get("closure_score_threshold_no_answer", 0.92))
            and not window_state.get("has_answer_started")
            and has_no_answer_closure_evidence
            and passes_no_answer_closure_guard
        ):
            action = "stop-and-finalize"
            trigger_type = "closure"
            trigger_reason = "high closure score with wrap evidence before answer, finalization needed"
        elif self.consecutive_loop_windows >= config["debounce_windows"]:
            action = "stop-and-finalize"
            trigger_type = "loop"
            trigger_reason = "confirmed high loop risk and low closure score"

        return {
            "policy_name": config.get("policy_name", "global_default"),
            "loop_score": loop_score,
            "closure_score": closure_score,
            "healthy_loop_bonus": motif_result.get("healthy_loop_bonus", 0.0),
            "recent_fail_motif_bonus": recent_fail_motif_bonus,
            "recent_healthy_motif_bonus": recent_healthy_motif_bonus,
            "loop_features": loop_features,
            "closure_features": closure_features,
            "has_no_answer_closure_evidence": has_no_answer_closure_evidence,
            "trigger_type": trigger_type,
            "trigger_reason": trigger_reason,
            "action": action,
            "would_trigger": action != "continue",
            "consecutive_loop_windows": self.consecutive_loop_windows,
        }


def compute_loop_features(
    window_state: dict[str, Any],
    motif_result: dict[str, Any],
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = config or DEFAULT_POLICY_CONFIG
    weights = config["loop_weights"]
    norm = float(config.get("distance_norm", 6))
    features = {
        "explore_segment_ratio": float(window_state.get("explore_segment_ratio", 0.0)),
        "distance_since_last_build_norm": min(float(window_state.get("distance_since_last_build", norm)) / norm, 1.0),
        "distance_since_last_verify_norm": min(float(window_state.get("distance_since_last_verify", norm)) / norm, 1.0),
        "low_novelty": 1.0 - float(window_state.get("avg_novelty_recent_2", 1.0)),
        "motif_risk_bonus": float(motif_result.get("motif_risk_bonus", 0.0)),
        "healthy_loop_bonus": float(motif_result.get("healthy_loop_bonus", 0.0)),
        "answer_started": float(bool(window_state.get("has_answer_started", False))),
    }
    raw = (
        weights["w_explore"] * features["explore_segment_ratio"]
        + weights["w_no_build"] * features["distance_since_last_build_norm"]
        + weights["w_no_verify"] * features["distance_since_last_verify_norm"]
        + weights["w_novelty"] * features["low_novelty"]
        + weights["w_motif"] * features["motif_risk_bonus"]
        - weights["w_healthy"] * features["healthy_loop_bonus"]
        - weights["w_answer"] * features["answer_started"]
    )
    features["raw"] = raw
    return features


def compute_closure_features(
    window_state: dict[str, Any], config: dict[str, Any] | None = None
) -> dict[str, Any]:
    config = config or DEFAULT_POLICY_CONFIG
    weights = config["closure_weights"]
    coarse_path = window_state.get("coarse_compressed_path", [])
    bv_path = _path_contains(coarse_path, ("Build", "Verify"))
    bvw_path = int(
        _path_contains(coarse_path, ("Build", "Verify", "Wrap"))
        or _path_contains(coarse_path, ("Verify", "Build", "Wrap"))
    )
    path_length = sum(item.get("count", 1) for item in coarse_path)
    bvw_discount = min(path_length / 10.0, 1.0) if bvw_path else 0.0
    if bvw_discount > 0 and coarse_path and coarse_path[-1]["state"] == "Explore":
        bvw_discount *= 0.4
    features = {
        "bv_path_indicator": float(bv_path),
        "bvw_path_indicator": bvw_discount,
        "answer_started": float(bool(window_state.get("has_answer_started", False))),
        "wrap_language_indicator": float(window_state.get("wrap_language_indicator", 0)),
        "explore_segment_ratio": float(window_state.get("explore_segment_ratio", 0.0)),
    }
    raw = (
        weights["w_bv_path"] * features["bv_path_indicator"]
        + weights["w_bvw_path"] * features["bvw_path_indicator"]
        + weights["w_answer"] * features["answer_started"]
        + weights["w_wrap_lang"] * features["wrap_language_indicator"]
        - weights["w_explore"] * features["explore_segment_ratio"]
    )
    features["raw"] = raw
    return features
