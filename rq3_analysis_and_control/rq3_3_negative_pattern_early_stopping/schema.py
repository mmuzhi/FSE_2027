"""Shared schema and constants for RQ3.3 replay experiments."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


FINE_STATES = ["PU", "SD", "IP", "CC", "VV", "KR", "MR", "AUX"]
COARSE_STATES = ["Explore", "Build", "Verify", "Wrap"]

FINE_TO_COARSE = {
    "PU": "Explore",
    "SD": "Explore",
    "KR": "Explore",
    "MR": "Explore",
    "IP": "Build",
    "CC": "Build",
    "VV": "Verify",
    "AUX": "Wrap",
}

DEFAULT_DIFFICULTY = "unknown"


@dataclass
class ReplaySample:
    task_id: str
    task: str
    model: str
    prompt: str = ""
    cot: str = ""
    answer: str = ""
    passed: bool | None = None
    difficulty: str = DEFAULT_DIFFICULTY
    score: float | None = None
    source_path: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task": self.task,
            "model": self.model,
            "difficulty": self.difficulty,
            "prompt": self.prompt,
            "cot": self.cot,
            "answer": self.answer,
            "passed": self.passed,
            "score": self.score,
            "source_path": self.source_path,
            "metadata": self.metadata,
        }


def normalize_task_name(task: str | None) -> str:
    if not task:
        return "unknown"
    text = task.strip().lower()
    return {
        "generate_cot": "generation",
        "generation_cot": "generation",
        "execution_cot": "execution",
        "debug_cot": "debug",
        "translation_cot": "translation",
    }.get(text, text)


def normalize_model_name(model: str | None) -> str:
    if not model:
        return "unknown"
    text = model.strip().lower()
    return "r1" if text == "deepseek-r1" else text


def normalize_difficulty(value: Any) -> str:
    if value is None:
        return DEFAULT_DIFFICULTY
    text = str(value).strip()
    return text.lower() if text else DEFAULT_DIFFICULTY


def fine_to_coarse(fine_state: str | None) -> str:
    if not fine_state:
        return "Explore"
    return FINE_TO_COARSE.get(fine_state, "Explore")


def append_compressed(path: list[dict[str, Any]], state: str) -> None:
    if not state:
        return
    if path and path[-1]["state"] == state:
        path[-1]["count"] += 1
    else:
        path.append({"state": state, "count": 1})
