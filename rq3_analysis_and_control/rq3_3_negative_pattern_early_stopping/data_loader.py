"""Data adapters for RQ3.3 offline replay."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Iterable

from schema import ReplaySample, normalize_difficulty, normalize_model_name, normalize_task_name


ROOT = Path(__file__).resolve().parents[2]


def iter_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                yield json.loads(line)


def normalize_answer(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    text = str(value).strip()
    text = re.sub(r"^<ans>|</ans>$", "", text, flags=re.IGNORECASE).strip()
    text = text.strip("` \n\r\t")
    return text


def expected_value(record: dict[str, Any]) -> str:
    expected = record.get("expected_output")
    if isinstance(expected, list) and expected:
        first = expected[0]
        if isinstance(first, dict):
            return normalize_answer(first.get("value"))
        return normalize_answer(first)
    return ""


def infer_passed_from_expected(record: dict[str, Any]) -> bool | None:
    expected = expected_value(record)
    if not expected:
        return None
    candidates = [
        record.get("answer"),
        record.get("raw_answer"),
        record.get("raw_answer_full"),
        record.get("translated_code"),
    ]
    norm_expected = normalize_answer(expected)
    for candidate in candidates:
        norm_candidate = normalize_answer(candidate)
        if not norm_candidate:
            continue
        if norm_candidate == norm_expected or norm_expected in norm_candidate:
            return True
    return False


def load_eval_pass_map(path: Path) -> dict[str, bool]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    results = payload.get("results", payload if isinstance(payload, list) else [])
    pass_map: dict[str, bool] = {}
    for item in results:
        if not isinstance(item, dict) or "task_id" not in item:
            continue
        total = int(item.get("total", 0) or 0)
        failed = int(item.get("failed", 0) or 0)
        passed = item.get("passed")
        if isinstance(passed, bool):
            ok = passed
        elif total:
            ok = failed == 0 or int(item.get("passed", 0) or 0) == total
        else:
            ok = failed == 0
        task_id = str(item["task_id"])
        pass_map[task_id] = ok
        pass_map[task_id.replace("/", "_")] = ok
    return pass_map


def default_eval_path(task: str, model: str) -> Path | None:
    task = normalize_task_name(task)
    model = normalize_model_name(model)
    candidates: list[Path] = []
    if task == "execution":
        candidates.extend(
            [
                ROOT / "data" / "CodeSense" / "test" / task / model / "result_rechecked.json",
                ROOT / "data" / "CodeSense" / "test" / task / model / "result.json",
                ROOT / "rq2_positive_negative_patterns" / "test" / task / model / "result.json",
            ]
        )
    else:
        candidates.append(ROOT / "rq2_positive_negative_patterns" / "test" / task / model / "results.json")
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_rq41_jsonl(
    path: Path,
    task: str | None = None,
    model: str | None = None,
    eval_path: Path | None = None,
    limit: int | None = None,
) -> list[ReplaySample]:
    task = normalize_task_name(task or path.parent.parent.name)
    model = normalize_model_name(model or path.parent.name)
    pass_map = load_eval_pass_map(eval_path) if eval_path else {}
    samples: list[ReplaySample] = []
    for idx, record in enumerate(iter_jsonl(path)):
        if limit is not None and idx >= limit:
            break
        task_id = str(record.get("task_id", f"sample_{idx}"))
        passed = pass_map.get(task_id)
        if passed is None:
            passed = infer_passed_from_expected(record)
        difficulty = normalize_difficulty(
            record.get("difficulty")
            or record.get("category")
            or record.get("level")
            or record.get("metadata", {}).get("difficulty", None)
        )
        samples.append(
            ReplaySample(
                task_id=task_id,
                task=task,
                model=model,
                difficulty=difficulty,
                prompt=record.get("prompt", ""),
                cot=record.get("cot") or record.get("reasoning_content") or record.get("original_cot") or "",
                answer=record.get("answer") or record.get("raw_answer") or record.get("translated_code") or "",
                passed=passed,
                score=1.0 if passed else (0.0 if passed is False else None),
                source_path=str(path),
                metadata={key: value for key, value in record.items() if key not in {"prompt", "cot", "answer"}},
            )
        )
    return samples


def load_segmentation_map(path: Path) -> dict[str, dict[str, Any]]:
    mapping: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return mapping
    for record in iter_jsonl(path):
        task_id = str(record.get("task_id", ""))
        if task_id:
            mapping[task_id] = record
    return mapping


def resolve_default_results(task: str, model: str) -> Path:
    task = normalize_task_name(task)
    model = normalize_model_name(model)
    candidates: list[Path]
    if task == "generation":
        candidates = [
            ROOT / "data" / "derived_cot" / "rq1_traces" / "generation" / model / "v4_v6" / "results.jsonl",
            ROOT / "data" / "derived_cot" / "rq1_traces" / "generation" / model / "v1_v3" / "results.jsonl",
        ]
    elif task in {"execution", "debug", "translation"}:
        candidates = [
            ROOT / "data" / "derived_cot" / "rq1_traces" / task / model / "results.jsonl",
        ]
    else:
        candidates = []
    for path in candidates:
        if path.exists():
            return path
    attempted = "\n".join(str(path) for path in candidates) if candidates else f"<no candidates for task={task}>"
    raise FileNotFoundError(f"Cannot find default results path. Tried:\n{attempted}")


def resolve_default_segmentation(task: str, model: str) -> Path | None:
    task = normalize_task_name(task)
    model = normalize_model_name(model)
    folder = {
        "generation": "Generate_COT",
        "execution": "Execution_COT",
        "debug": "Debug_COT",
        "translation": "Translation_COT",
    }.get(task, task)
    path = ROOT / "data" / "derived_cot" / "rq1_segmented" / folder / model / "segmented_results.jsonl"
    return path if path.exists() else None


def main() -> None:
    parser = argparse.ArgumentParser(description="Load and summarize RQ3.3 replay samples.")
    parser.add_argument("--task", default="execution")
    parser.add_argument("--model", default="qwen")
    parser.add_argument("--results", default="")
    parser.add_argument("--eval", default="")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    results_path = Path(args.results) if args.results else resolve_default_results(args.task, args.model)
    eval_path = Path(args.eval) if args.eval else default_eval_path(args.task, args.model)
    samples = load_rq41_jsonl(results_path, args.task, args.model, eval_path, args.limit)
    print(json.dumps([sample.to_dict() for sample in samples], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
