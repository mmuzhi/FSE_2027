#!/usr/bin/env python3
"""Remove failed RQ1 segmentation records so they can be retried."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


TASKS = {
    "generation": {
        "trace": Path("generation") / "{model}" / "v4_v6" / "results.jsonl",
        "segmented": Path("Generate_COT") / "{model}" / "segmented_results.jsonl",
    },
    "execution": {
        "trace": Path("execution") / "{model}" / "results.jsonl",
        "segmented": Path("Execution_COT") / "{model}" / "segmented_results.jsonl",
    },
    "debug": {
        "trace": Path("debug") / "{model}" / "results.jsonl",
        "segmented": Path("Debug_COT") / "{model}" / "segmented_results.jsonl",
    },
    "translation": {
        "trace": Path("translation") / "{model}" / "results.jsonl",
        "segmented": Path("Translation_COT") / "{model}" / "segmented_results.jsonl",
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


def is_segmentation_success(row: dict[str, Any]) -> bool:
    result = row.get("segmentation_result")
    return isinstance(result, dict) and bool(result.get("success"))


def summarize_task(repo_root: Path, task: str, model: str) -> dict[str, Any]:
    trace_root = repo_root / "data" / "derived_cot" / "rq1_traces"
    segmented_root = repo_root / "data" / "derived_cot" / "rq1_segmented"
    config = TASKS[task]
    trace_path = resolve_template(trace_root, config["trace"], model)
    segmented_path = resolve_template(segmented_root, config["segmented"], model)

    trace_rows = read_jsonl(trace_path)
    segmented_rows = read_jsonl(segmented_path)
    trace_ids = [task_id(row) for row in trace_rows if task_id(row)]
    segmented_ids = {task_id(row) for row in segmented_rows if task_id(row)}
    success_ids = {task_id(row) for row in segmented_rows if task_id(row) and is_segmentation_success(row)}
    failed_rows = [row for row in segmented_rows if not is_segmentation_success(row)]

    return {
        "task": task,
        "trace_path": trace_path,
        "segmented_path": segmented_path,
        "trace_rows": len(trace_rows),
        "segmented_rows": len(segmented_rows),
        "success_rows": len(success_ids),
        "failed_rows": len(failed_rows),
        "missing_rows": sum(1 for item in trace_ids if item not in segmented_ids),
        "pending_after_cleanup": sum(1 for item in trace_ids if item not in success_ids),
        "failed_task_ids": [task_id(row) for row in failed_rows if task_id(row)],
    }


def clean_task(repo_root: Path, task: str, model: str, apply: bool, remove_task_ids: set[str]) -> dict[str, Any]:
    summary = summarize_task(repo_root, task, model)
    segmented_path: Path = summary["segmented_path"]
    if not segmented_path.exists():
        summary["changed"] = False
        return summary

    rows = read_jsonl(segmented_path)
    forced_rows = [row for row in rows if task_id(row) in remove_task_ids]
    kept = [
        row for row in rows
        if is_segmentation_success(row) and task_id(row) not in remove_task_ids
    ]
    if summary["failed_rows"] == 0 and not forced_rows:
        summary["changed"] = False
        summary["forced_rows"] = 0
        return summary

    summary["kept_rows"] = len(kept)
    summary["forced_rows"] = len(forced_rows)
    summary["changed"] = apply
    if apply:
        backup_path = segmented_path.with_suffix(segmented_path.suffix + ".bak")
        shutil.copy2(segmented_path, backup_path)
        write_jsonl(segmented_path, kept)
        summary["backup_path"] = backup_path
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean failed RQ1 segmentation records for retry.")
    parser.add_argument("--model", default="glm5.1", help="Trace-source model directory, e.g., glm5.1")
    parser.add_argument("--task", choices=["all", *TASKS.keys()], default="all")
    parser.add_argument("--task-id", action="append", default=[], help="Force-remove a task_id from segmented results.")
    parser.add_argument("--task-id-file", default=None, help="Text file containing task_ids to force-remove, one per line.")
    parser.add_argument("--apply", action="store_true", help="Rewrite segmented_results.jsonl files in place.")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    remove_task_ids = {item.strip() for item in args.task_id if item.strip()}
    if args.task_id_file:
        path = Path(args.task_id_file)
        remove_task_ids.update(
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        )
    tasks = list(TASKS) if args.task == "all" else [args.task]
    for task in tasks:
        summary = clean_task(repo_root, task, args.model, args.apply, remove_task_ids)
        print(
            f"[{task}] trace={summary['trace_rows']} segmented={summary['segmented_rows']} "
            f"success={summary['success_rows']} failed={summary['failed_rows']} "
            f"forced={summary.get('forced_rows', 0)} "
            f"missing={summary['missing_rows']} pending_after_cleanup={summary['pending_after_cleanup']}"
        )
        print(f"  trace:     {summary['trace_path']}")
        print(f"  segmented: {summary['segmented_path']}")
        failed_preview = summary["failed_task_ids"][:10]
        if failed_preview:
            print(f"  failed preview: {failed_preview}")
        if summary.get("backup_path"):
            print(f"  backup: {summary['backup_path']}")
        elif not args.apply:
            print("  dry run only; pass --apply to clean failed rows.")


if __name__ == "__main__":
    main()
