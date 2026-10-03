#!/usr/bin/env python3
"""Remove incomplete RQ1 trace records so collection scripts can retry them."""

from __future__ import annotations

import argparse
import glob
import json
import shutil
from pathlib import Path
from typing import Any


TASKS = {
    "generation": {
        "results": Path("generation") / "{model}" / "v4_v6" / "results.jsonl",
        "artifact_dirs": [
            Path("generation") / "{model}" / "v4_v6" / "v4_output",
            Path("generation") / "{model}" / "v4_v6" / "txt_output",
        ],
        "required_fields": ["cot", "answer"],
    },
    "execution": {
        "results": Path("execution") / "{model}" / "results.jsonl",
        "artifact_dirs": [Path("execution") / "{model}" / "txt_output"],
        "required_fields": ["cot", "raw_answer_full"],
    },
    "debug": {
        "results": Path("debug") / "{model}" / "results.jsonl",
        "artifact_dirs": [
            Path("debug") / "{model}" / "txt_output",
            Path("debug") / "{model}" / "code_output",
        ],
        "required_fields": ["cot", "raw_answer"],
    },
    "translation": {
        "results": Path("translation") / "{model}" / "results.jsonl",
        "artifact_dirs": [
            Path("translation") / "{model}" / "*" / "txt_output",
            Path("translation") / "{model}" / "*" / "code_output",
        ],
        "required_fields": ["cot", "raw_answer"],
    },
}


def resolve_template(base: Path, template: Path, model: str) -> Path:
    return base / Path(str(template).format(model=model))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {path}:{line_no}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"JSON object expected at {path}:{line_no}")
            rows.append(row)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def task_id(row: dict[str, Any]) -> str:
    return str(row.get("task_id", "")).strip()


def is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return value.strip() == ""
    return False


def incomplete_reasons(row: dict[str, Any], required_fields: list[str]) -> list[str]:
    reasons = []
    for field in required_fields:
        if is_empty(row.get(field)):
            reasons.append(f"empty_{field}")
    return reasons


def artifact_candidates(trace_root: Path, task: str, model: str, row: dict[str, Any]) -> list[Path]:
    config = TASKS[task]
    tid = task_id(row)
    if not tid:
        return []
    candidates: list[Path] = []
    for template in config["artifact_dirs"]:
        pattern = resolve_template(trace_root, template, model)
        for directory_name in glob.glob(str(pattern)):
            directory = Path(directory_name)
            if not directory.exists():
                continue
            for suffix in (".txt", ".py", ".cpp", ".java"):
                candidates.append(directory / f"{tid}{suffix}")
            if task == "translation":
                original_task_id = str(row.get("original_task_id", "")).strip()
                if original_task_id:
                    for suffix in (".txt", ".py", ".cpp", ".java"):
                        candidates.append(directory / f"{original_task_id}{suffix}")
    return [path for path in candidates if path.exists()]


def clean_task(repo_root: Path, task: str, model: str, apply: bool) -> dict[str, Any]:
    trace_root = repo_root / "data" / "derived_cot" / "rq1_traces"
    config = TASKS[task]
    results_path = resolve_template(trace_root, config["results"], model)
    rows = read_jsonl(results_path)

    invalid: list[dict[str, Any]] = []
    kept: list[dict[str, Any]] = []
    reason_counts: dict[str, int] = {}
    for row in rows:
        reasons = incomplete_reasons(row, config["required_fields"])
        if reasons:
            invalid.append(row)
            for reason in reasons:
                reason_counts[reason] = reason_counts.get(reason, 0) + 1
        else:
            kept.append(row)

    moved = 0
    if apply and invalid:
        backup_path = results_path.with_suffix(results_path.suffix + ".incomplete.bak")
        shutil.copy2(results_path, backup_path)
        trash_root = results_path.parent / "_incomplete_samples"
        trash_root.mkdir(parents=True, exist_ok=True)
        for row in invalid:
            tid = task_id(row) or "unknown"
            for artifact in artifact_candidates(trace_root, task, model, row):
                target_dir = trash_root / tid
                target_dir.mkdir(parents=True, exist_ok=True)
                target = target_dir / artifact.name
                if target.exists():
                    target = target_dir / f"{artifact.stem}_{moved}{artifact.suffix}"
                shutil.move(str(artifact), str(target))
                moved += 1
        write_jsonl(results_path, kept)
    else:
        backup_path = None

    return {
        "task": task,
        "results_path": results_path,
        "rows": len(rows),
        "kept": len(kept),
        "invalid": len(invalid),
        "invalid_task_ids": [task_id(row) for row in invalid if task_id(row)],
        "reason_counts": reason_counts,
        "moved_artifacts": moved,
        "backup_path": backup_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean incomplete RQ1 trace records for retry.")
    parser.add_argument("--model", default="glm5.1", help="Trace-source model directory.")
    parser.add_argument("--task", choices=["all", *TASKS.keys()], default="all")
    parser.add_argument("--apply", action="store_true", help="Rewrite results.jsonl files in place.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    tasks = list(TASKS) if args.task == "all" else [args.task]
    for task in tasks:
        summary = clean_task(repo_root, task, args.model, args.apply)
        print(
            f"[{task}] rows={summary['rows']} kept={summary['kept']} "
            f"incomplete={summary['invalid']} moved_artifacts={summary['moved_artifacts']}"
        )
        print(f"  results: {summary['results_path']}")
        if summary["reason_counts"]:
            print(f"  reasons: {summary['reason_counts']}")
        preview = summary["invalid_task_ids"][:10]
        if preview:
            print(f"  incomplete preview: {preview}")
        if summary["backup_path"]:
            print(f"  backup: {summary['backup_path']}")
        elif not args.apply:
            print("  dry run only; pass --apply to clean incomplete rows.")


if __name__ == "__main__":
    main()
