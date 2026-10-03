"""Micro-unit splitting and semantic segment tracking for RQ3.3."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any

from schema import append_compressed
from state_model import RuleStateModel, tokenize


BOUNDARY_RE = re.compile(
    r"(?<=[.!?。！？])\s+|(?=\n\s*(?:[-*]|\d+[.)])\s+)|\n{2,}"
)
COMPLETE_MICRO_UNIT_END_RE = re.compile(r"(?:[.!?;:]\s*|\n\s*)$")
TRANSITION_CUES = (
    "however",
    "but",
    "now",
    "therefore",
    "finally",
    "let's code",
    "let me check",
    "check",
    "verify",
    "so,",
)


def split_micro_units(text: str) -> list[str]:
    if not text:
        return []
    rough_parts = BOUNDARY_RE.split(text.replace("\r\n", "\n"))
    units: list[str] = []
    for part in rough_parts:
        cleaned = part.strip()
        if not cleaned:
            continue
        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        if len(lines) > 1:
            units.extend(lines)
        else:
            units.append(cleaned)
    return units


def split_complete_micro_units(text: str, force: bool = False) -> tuple[list[str], str]:
    if not text:
        return [], ""
    units = split_micro_units(text)
    if not units:
        return [], text
    if force or COMPLETE_MICRO_UNIT_END_RE.search(text):
        return units, ""
    if len(units) == 1:
        return [], text
    return units[:-1], units[-1]


def token_set(text: str) -> set[str]:
    return {token for token in tokenize(text) if len(token) > 1}


def novelty_against(tokens_new: set[str], tokens_existing: set[str]) -> float:
    if not tokens_new or not tokens_existing:
        return 1.0
    union = tokens_new | tokens_existing
    return 1.0 - (len(tokens_new & tokens_existing) / len(union))


def _dominant(values: list[str], default: str) -> str:
    if not values:
        return default
    return Counter(values).most_common(1)[0][0]


class StateTracker:
    def __init__(self, novelty_threshold: float = 0.7, model: RuleStateModel | None = None) -> None:
        self.novelty_threshold = novelty_threshold
        self.model = model or RuleStateModel()
        self.pending_micro_unit = ""
        self.active_units: list[dict[str, Any]] = []
        self.active_tokens: set[str] = set()
        self.closed_segments: list[dict[str, Any]] = []
        self.coarse_compressed_path: list[dict[str, Any]] = []
        self.fine_compressed_path: list[dict[str, Any]] = []
        self.has_answer_started = False
        self.distance_since_last_build = 0
        self.distance_since_last_verify = 0

    def _add_units(self, units: list[str]) -> list[dict[str, Any]]:
        closed: list[dict[str, Any]] = []
        for unit in units:
            closed_segment = self.add_unit(unit)
            if closed_segment:
                closed.append(closed_segment)
        return closed

    def feed_text(self, text: str) -> list[dict[str, Any]]:
        return self._add_units(split_micro_units(text))

    def feed_delta(self, text: str) -> list[dict[str, Any]]:
        self.pending_micro_unit += text
        units, remainder = split_complete_micro_units(self.pending_micro_unit)
        self.pending_micro_unit = remainder
        return self._add_units(units)

    def flush_pending(self) -> list[dict[str, Any]]:
        units, _ = split_complete_micro_units(self.pending_micro_unit, force=True)
        self.pending_micro_unit = ""
        closed = self._add_units(units)
        final_segment = self.close_active_segment()
        if final_segment:
            closed.append(final_segment)
        return closed

    def add_unit(self, text: str, scores: dict[str, Any] | None = None) -> dict[str, Any] | None:
        scores = scores or self.model.score(text)
        unit_tokens = token_set(text)
        novelty = novelty_against(unit_tokens, self.active_tokens)
        unit = {
            "unit_id": len(self.active_units),
            "unit_text": text,
            "coarse_state": scores["predicted_coarse"],
            "fine_state": scores["predicted_fine"],
            "coarse_scores": scores["coarse_scores"],
            "fine_scores": scores["fine_scores"],
            "novelty": novelty,
        }

        closed_segment = None
        if self._should_start_new_segment(unit):
            closed_segment = self.close_active_segment()

        self.active_units.append(unit)
        self.active_tokens |= unit_tokens
        return closed_segment

    def _should_start_new_segment(self, unit: dict[str, Any]) -> bool:
        if not self.active_units:
            return False
        active_coarse = _dominant([item["coarse_state"] for item in self.active_units], "Explore")
        active_fine = _dominant([item["fine_state"] for item in self.active_units], "PU")
        text = unit["unit_text"].lower()
        has_transition = any(cue in text for cue in TRANSITION_CUES)
        coarse_switch = unit["coarse_state"] != active_coarse
        fine_switch = unit["fine_state"] != active_fine
        novelty_switch = unit["novelty"] > self.novelty_threshold and len(self.active_units) >= 2
        if coarse_switch:
            return True
        if fine_switch and (has_transition or len(self.active_units) >= 3):
            return True
        if novelty_switch and has_transition:
            return True
        return False

    def close_active_segment(self) -> dict[str, Any] | None:
        if not self.active_units:
            return None
        segment_id = len(self.closed_segments)
        coarse = _dominant([item["coarse_state"] for item in self.active_units], "Explore")
        fine = _dominant([item["fine_state"] for item in self.active_units], "PU")
        text = "\n".join(item["unit_text"] for item in self.active_units)
        avg_novelty = sum(item["novelty"] for item in self.active_units) / max(len(self.active_units), 1)
        segment = {
            "segment_id": segment_id,
            "segment_text": text,
            "units": self.active_units,
            "coarse_state": coarse,
            "fine_state": fine,
            "avg_novelty": avg_novelty,
            "num_units": len(self.active_units),
        }
        self.closed_segments.append(segment)
        append_compressed(self.coarse_compressed_path, coarse)
        append_compressed(self.fine_compressed_path, fine)
        if coarse == "Build":
            self.distance_since_last_build = 0
        else:
            self.distance_since_last_build += 1
        if coarse == "Verify":
            self.distance_since_last_verify = 0
        else:
            self.distance_since_last_verify += 1
        self.active_units = []
        self.active_tokens = set()
        return segment

    def finalize(self) -> dict[str, Any] | None:
        return self.close_active_segment()

    def get_window_state(self, window_size: int = 3) -> dict[str, Any]:
        recent = self.closed_segments[-window_size:]
        recent_novelty = [seg["avg_novelty"] for seg in self.closed_segments[-2:]]
        avg_novelty_recent_2 = sum(recent_novelty) / len(recent_novelty) if recent_novelty else 1.0
        explore_count = sum(1 for seg in recent if seg["coarse_state"] == "Explore")
        return {
            "segments": self.closed_segments,
            "active_segment_units": self.active_units,
            "recent_segments": recent,
            "has_answer_started": self.has_answer_started,
            "distance_since_last_build": self.distance_since_last_build,
            "distance_since_last_verify": self.distance_since_last_verify,
            "coarse_compressed_path": list(self.coarse_compressed_path),
            "fine_compressed_path": list(self.fine_compressed_path),
            "avg_novelty_recent_2": avg_novelty_recent_2,
            "explore_segment_ratio": explore_count / max(len(recent), 1),
            "wrap_language_indicator": self._wrap_language_indicator(recent),
        }

    @staticmethod
    def _wrap_language_indicator(segments: list[dict[str, Any]]) -> int:
        if not segments:
            return 0
        text = segments[-1]["segment_text"].lower()
        cues = ("therefore", "finally", "answer", "output", "print", "result is", "final")
        return int(any(cue in text for cue in cues))
