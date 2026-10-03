"""Rule-based coarse/fine state scoring for RQ3.3 micro-units."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from schema import COARSE_STATES, FINE_STATES, FINE_TO_COARSE, fine_to_coarse


COARSE_KEYWORDS = {
    "Explore": [
        "maybe",
        "perhaps",
        "consider",
        "constraint",
        "constraints",
        "alternative",
        "however",
        "note",
        "assume",
        "recall",
        "think",
        "possibility",
        "need to understand",
    ],
    "Build": [
        "implement",
        "code",
        "function",
        "class",
        "loop",
        "array",
        "dict",
        "return",
        "assign",
        "initialize",
        "update",
        "construct",
    ],
    "Verify": [
        "check",
        "verify",
        "test",
        "sample",
        "edge case",
        "simulate",
        "trace",
        "confirm",
        "validate",
        "example",
    ],
    "Wrap": [
        "therefore",
        "finally",
        "final",
        "answer",
        "output",
        "so the",
        "thus",
        "print",
        "result is",
        "expected output",
    ],
}

FINE_KEYWORDS = {
    "PU": [
        "given",
        "input",
        "problem",
        "method",
        "function",
        "we need",
        "need to",
        "understand",
        "task",
    ],
    "SD": [
        "design",
        "approach",
        "strategy",
        "algorithm",
        "plan",
        "use",
        "data structure",
        "idea",
        "complexity",
    ],
    "IP": [
        "implement",
        "code",
        "write",
        "loop",
        "if ",
        "else",
        "return",
        "variable",
        "initialize",
        "append",
    ],
    "CC": [
        "change",
        "fix",
        "modify",
        "adjust",
        "replace",
        "patch",
        "correct",
        "update",
    ],
    "VV": [
        "check",
        "verify",
        "test",
        "sample",
        "edge",
        "trace",
        "simulate",
        "confirm",
        "works",
    ],
    "KR": [
        "recall",
        "known",
        "theorem",
        "property",
        "in java",
        "in python",
        "built-in",
        "library",
        "rule",
    ],
    "MR": [
        "maybe",
        "however",
        "but",
        "wait",
        "on second thought",
        "not sure",
        "could",
        "might",
        "possibility",
        "reconsider",
    ],
    "AUX": [
        "therefore",
        "finally",
        "answer",
        "output",
        "print",
        "result",
        "so,",
        "let's write",
        "final code",
    ],
}

TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+|[^\s]")


def _softmax(scores: dict[str, float]) -> dict[str, float]:
    if not scores:
        return {}
    max_score = max(scores.values())
    exps = {key: math.exp(value - max_score) for key, value in scores.items()}
    total = sum(exps.values()) or 1.0
    return {key: value / total for key, value in exps.items()}


def _keyword_hits(text: str, keywords: list[str]) -> int:
    lowered = text.lower()
    return sum(1 for keyword in keywords if keyword in lowered)


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text or "") if token.strip()]


class RuleStateModel:
    def __init__(self, label_confidence: float = 3.0) -> None:
        self.label_confidence = label_confidence

    def score(self, text: str, weak_fine_label: str | None = None) -> dict:
        fine_raw = {
            state: 0.25 + _keyword_hits(text, FINE_KEYWORDS[state])
            for state in FINE_STATES
        }
        if weak_fine_label in FINE_STATES:
            fine_raw[weak_fine_label] += self.label_confidence

        coarse_raw = {
            state: 0.25 + _keyword_hits(text, COARSE_KEYWORDS[state])
            for state in COARSE_STATES
        }
        if weak_fine_label in FINE_TO_COARSE:
            coarse_raw[FINE_TO_COARSE[weak_fine_label]] += self.label_confidence

        fine_scores = _softmax(fine_raw)
        coarse_scores = _softmax(coarse_raw)
        predicted_fine = max(fine_scores, key=fine_scores.get)
        predicted_coarse = max(coarse_scores, key=coarse_scores.get)

        mapped_coarse = fine_to_coarse(predicted_fine)
        if coarse_scores[mapped_coarse] >= coarse_scores[predicted_coarse] * 0.75:
            predicted_coarse = mapped_coarse

        return {
            "unit_text": text,
            "coarse_scores": coarse_scores,
            "fine_scores": fine_scores,
            "predicted_coarse": predicted_coarse,
            "predicted_fine": predicted_fine,
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="Score RQ3.3 micro-units with rule states.")
    parser.add_argument("--text", default="")
    parser.add_argument("--input", default="")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    model = RuleStateModel()
    if args.text:
        print(json.dumps(model.score(args.text), ensure_ascii=False, indent=2))
        return

    if not args.input:
        raise SystemExit("Provide --text or --input.")

    output_path = Path(args.output) if args.output else None
    out_fh = output_path.open("w", encoding="utf-8") if output_path else None
    try:
        for line in Path(args.input).read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            item = json.loads(line)
            scored = model.score(
                item.get("unit_text", ""),
                weak_fine_label=item.get("fine_state_corrected") or item.get("fine_state"),
            )
            item.update(scored)
            text = json.dumps(item, ensure_ascii=False)
            if out_fh:
                out_fh.write(text + "\n")
            else:
                print(text)
    finally:
        if out_fh:
            out_fh.close()


if __name__ == "__main__":
    main()
