"""Task-specific fail-rich and healthy motif detection for RQ3.3."""

from __future__ import annotations

from typing import Any


FAIL_MOTIFS = {
    "generation": [
        ("SD", "KR", "SD"),
        ("SD", "MR", "SD"),
        ("MR", "SD", "MR"),
        ("MR", "SD", "KR"),
        ("KR", "SD", "MR"),
        ("KR", "SD", "KR"),
        ("SD", "KR", "SD", "KR"),
        ("KR", "SD", "MR", "SD"),
        ("VV", "MR", "SD"),
        ("VV", "SD", "VV", "SD"),
    ],
    "execution": [("PU", "MR", "PU"), ("MR", "PU", "MR"), ("PU", "MR", "SD")],
    "debug": [("IP", "VV", "MR"), ("MR", "IP", "VV"), ("SD", "MR", "SD")],
    "translation": [("SD", "IP", "SD"), ("IP", "SD", "IP")],
}

HEALTHY_MOTIFS = [
    ("VV", "IP", "VV"),
    ("VV", "CC", "VV"),
    ("IP", "VV", "AUX"),
    ("CC", "VV", "AUX"),
]


def _window_bonus(window: list[dict[str, Any]]) -> float:
    repeated = sum(max(int(item.get("count", 1)) - 1, 0) for item in window)
    if repeated >= 2:
        return 1.5
    if repeated == 1:
        return 1.2
    return 1.0


def _match(path: list[dict[str, Any]], motifs: list[tuple[str, ...]], kind: str) -> list[dict[str, Any]]:
    states = [item["state"] for item in path]
    hits: list[dict[str, Any]] = []
    for motif in motifs:
        width = len(motif)
        for start in range(0, max(len(states) - width + 1, 0)):
            if tuple(states[start : start + width]) == motif:
                window = path[start : start + width]
                hits.append(
                    {
                        "kind": kind,
                        "motif": list(motif),
                        "start": start,
                        "end": start + width - 1,
                        "bonus": _window_bonus(window),
                        "counts": [item.get("count", 1) for item in window],
                    }
                )
    return hits


def detect_motifs(fine_compressed_path: list[dict[str, Any]], task: str) -> dict[str, Any]:
    task_motifs = FAIL_MOTIFS.get(task, [])
    fail_hits = _match(fine_compressed_path, task_motifs, "fail")
    healthy_hits = _match(fine_compressed_path, HEALTHY_MOTIFS, "healthy")
    motif_risk_bonus = max((hit["bonus"] for hit in fail_hits), default=0.0)
    healthy_loop_bonus = max((hit["bonus"] for hit in healthy_hits), default=0.0)
    return {
        "matched_fail_motifs": fail_hits,
        "matched_healthy_motifs": healthy_hits,
        "motif_risk_bonus": motif_risk_bonus,
        "healthy_loop_bonus": healthy_loop_bonus,
        "motif_hits": fail_hits + healthy_hits,
    }
