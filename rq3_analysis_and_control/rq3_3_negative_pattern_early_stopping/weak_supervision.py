"""Build micro-unit weak supervision from RQ1 step-level segmentation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from schema import fine_to_coarse, normalize_model_name, normalize_task_name
from state_model import FINE_KEYWORDS
from state_tracker import split_micro_units


ROOT = Path(__file__).resolve().parents[2]


def keyword_best_label(text: str) -> tuple[str | None, int]:
    lowered = text.lower()
    scores = {
        label: sum(1 for keyword in keywords if keyword in lowered)
        for label, keywords in FINE_KEYWORDS.items()
    }
    label = max(scores, key=scores.get)
    score = scores[label]
    return (label, score) if score > 0 else (None, 0)


def iter_segmented_records(paths: list[Path]):
    for path in paths:
        parts = path.parts
        task_name = "unknown"
        model_name = "unknown"
        if "rq1_segmented" in parts:
            idx = parts.index("rq1_segmented")
            task_name = normalize_task_name(parts[idx + 1])
            model_name = normalize_model_name(parts[idx + 2])
        elif "segmentation_results" in parts:
            idx = parts.index("segmentation_results")
            task_name = normalize_task_name(parts[idx + 1])
            model_name = normalize_model_name(parts[idx + 2])
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                yield path, task_name, model_name, json.loads(line)


def build_micro_units(paths: list[Path], limit: int | None = None) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen = 0
    for source_path, task, model, record in iter_segmented_records(paths):
        if limit is not None and seen >= limit:
            break
        seen += 1
        task_id = str(record.get("task_id", ""))
        result = record.get("segmentation_result") or {}
        steps = result.get("steps") or []
        for step_index, step in enumerate(steps):
            fine = step.get("category") or step.get("fine_state") or "PU"
            content = step.get("content") or ""
            units = split_micro_units(content)
            prev_fine = steps[step_index - 1].get("category") if step_index > 0 else None
            next_fine = steps[step_index + 1].get("category") if step_index + 1 < len(steps) else None
            for unit_index, unit_text in enumerate(units):
                corrected = fine
                correction_type = "inherit"
                keyword_label, keyword_score = keyword_best_label(unit_text)
                if unit_index == 0 and prev_fine and keyword_label == prev_fine:
                    corrected = prev_fine
                    correction_type = "boundary"
                elif unit_index == len(units) - 1 and next_fine and keyword_label == next_fine:
                    corrected = next_fine
                    correction_type = "boundary"
                elif keyword_label and keyword_label != fine and keyword_score >= 2:
                    corrected = keyword_label
                    correction_type = "keyword"
                output.append(
                    {
                        "task_id": task_id,
                        "task": task,
                        "model": model,
                        "difficulty": "unknown",
                        "step_id": step.get("step_id", str(step_index + 1)),
                        "unit_id": unit_index,
                        "unit_text": unit_text,
                        "fine_state": fine,
                        "coarse_state": fine_to_coarse(fine),
                        "fine_state_corrected": corrected,
                        "coarse_state_corrected": fine_to_coarse(corrected),
                        "correction_type": correction_type,
                        "source_path": str(source_path),
                    }
                )
    return output


def default_paths(task: str = "", model: str = "") -> list[Path]:
    base = ROOT / "data" / "derived_cot" / "rq1_segmented"
    patterns = []
    if task:
        folder = {
            "generation": "Generate_COT",
            "execution": "Execution_COT",
            "debug": "Debug_COT",
            "translation": "Translation_COT",
        }.get(normalize_task_name(task), task)
        if model:
            patterns.append(base / folder / normalize_model_name(model) / "segmented_results.jsonl")
        else:
            patterns.extend((base / folder).glob("*/segmented_results.jsonl"))
    else:
        patterns.extend(base.glob("*/*/segmented_results.jsonl"))
    return [path for path in patterns if path.exists()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build RQ3.3 micro-unit weak supervision.")
    parser.add_argument("--task", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--output", default=str(ROOT / "data" / "derived_cot" / "rq3_negative_pattern_early_stopping" / "weak_supervision" / "micro_units.jsonl"))
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    paths = [Path(item) for item in args.input] if args.input else default_paths(args.task, args.model)
    if not paths:
        raise SystemExit("No segmentation files found.")
    units = build_micro_units(paths, limit=args.limit or None)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(json.dumps(item, ensure_ascii=False) + "\n" for item in units), encoding="utf-8")
    print(f"Wrote {len(units)} micro-units to {output_path}")


if __name__ == "__main__":
    main()
