from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from utils import api_defaults, append_result_to_file, call_api_stream, load_existing_task_ids, safe_print

from prompt_utils import PROMPT_METHODS, infer_prompt_variant, render_prompt, results_dir

sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)


def build_prompt(buggy_code: str, args) -> tuple[str, dict]:
    return render_prompt(
        task="debug",
        model_name=args.model,
        prompt_method=args.prompt_method,
        prompt_variant=args.prompt_variant,
        templates_path=args.templates_path,
        buggy_code=buggy_code,
    )


def extract_code_from_text(answer_text: str) -> str | None:
    if not answer_text:
        return None
    pattern = r"```(?:python|py)?\s*\n([\s\S]*?)\n```"
    match = re.search(pattern, answer_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\w*\s*\n([\s\S]*?)\n```", answer_text)
    if match:
        return match.group(1).strip()
    return None


def load_source_files(data_path: Path) -> list[dict]:
    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("DebugBench dataset must be a list.")
    samples = []
    for item in data:
        task_id = str(item.get("sample_id", "")).strip()
        if not task_id:
            raise ValueError("Missing sample_id in DebugBench dataset record.")
        samples.append({
            "task_id": task_id,
            "buggy_code": str(item.get("buggy_code", "")).strip(),
            "level": item.get("level", ""),
        })
    return samples


def process_single_task(task_data: dict, args, output_dir: Path, code_output_dir: Path) -> dict:
    task_id = task_data["task_id"]
    buggy_code = task_data["buggy_code"]
    safe_print(f"[{task_id}] Start bug fixing...")

    prompt, prompt_meta = build_prompt(buggy_code, args)
    start_time = time.time()
    reasoning_content, answer_text, success, error_msg = call_api_stream(
        prompt=prompt,
        api_key=args.api_key,
        base_url=args.base_url,
        model_name=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        max_retries=args.max_retries,
        task_id=task_id,
    )
    elapsed = time.time() - start_time

    if not success:
        safe_print(f"[{task_id}] Failed ({elapsed:.2f}s): {error_msg}")
        return {"status": "failed", "task_id": task_id, "time": elapsed}

    fixed_code = extract_code_from_text(answer_text) or ""
    estimated_tokens = (len(reasoning_content) + len(answer_text)) // 4
    result = {
        "task_id": task_id,
        "buggy_code": buggy_code,
        "prompt_method": prompt_meta["method"],
        "prompt_variant": prompt_meta["variant"],
        "prompt_task": prompt_meta["task"],
        "prompt": prompt,
        "cot": reasoning_content,
        "fixed_code": fixed_code,
        "raw_answer": answer_text,
    }

    full_text = (
        f"=== PROMPT VARIANT ===\n{prompt_meta['variant']}\n\n"
        f"=== BUGGY CODE ===\n{buggy_code}\n\n"
        f"=== PROMPT ===\n{prompt}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== RAW ANSWER ===\n{answer_text}\n\n"
        f"=== FIXED CODE ===\n{fixed_code}\n"
    )
    (output_dir / f"{task_id}.txt").write_text(full_text, encoding="utf-8")
    if fixed_code:
        (code_output_dir / f"{task_id}.py").write_text(fixed_code, encoding="utf-8")

    return {
        "status": "success",
        "task_id": task_id,
        "result": result,
        "tokens": estimated_tokens,
        "time": elapsed,
    }


def main() -> None:
    script_dir = Path(__file__).parent
    project_root = Path(__file__).resolve().parents[2]
    api = api_defaults()

    parser = argparse.ArgumentParser(description="RQ3.2 bug fixing with CoT")
    parser.add_argument("--base_url", type=str, default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", type=str, default=api["api_key"], help="API key")
    parser.add_argument("--model", type=str, default=api["model"], help="Model name")
    parser.add_argument("--data_path", type=str, default=str(project_root / "data" / "DebugBench" / "python_samples.json"))
    parser.add_argument(
        "--prompt_method",
        type=str,
        default="pattern_only",
        choices=PROMPT_METHODS,
    )
    parser.add_argument("--prompt_variant", type=str, default="r1")
    parser.add_argument("--templates_path", type=str, default=str(script_dir / "prompt_templates.json"))
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--code_output_dir", type=str, default=None)
    parser.add_argument("--save_path", type=str, default=None)
    parser.add_argument("--max_tokens", type=int, default=51200)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--num_samples", type=int, default=-1)
    parser.add_argument("--num_workers", type=int, default=20)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument("--max_retries", type=int, default=2)
    args = parser.parse_args()

    resolved_variant = infer_prompt_variant(args.model, args.prompt_variant)
    base_results_dir = results_dir(
        project_root,
        "debug",
        args.model,
        args.prompt_method,
        resolved_variant,
    )
    if args.output_dir is None:
        args.output_dir = str(base_results_dir / "txt_output")
    if args.code_output_dir is None:
        args.code_output_dir = str(base_results_dir / "code_output")
    if args.save_path is None:
        args.save_path = str(base_results_dir / "results.jsonl")

    samples = load_source_files(Path(args.data_path))

    output_dir = Path(args.output_dir)
    code_output_dir = Path(args.code_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    code_output_dir.mkdir(parents=True, exist_ok=True)
    save_path = Path(args.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    saved_task_ids = load_existing_task_ids(str(save_path))
    pending_samples = [s for s in samples if s["task_id"] not in saved_task_ids]
    if args.num_samples > 0:
        pending_samples = pending_samples[: args.num_samples]
    if not pending_samples:
        safe_print("No pending tasks. Exit.")
        return

    total_tokens = 0
    success_count = 0
    failed_count = 0
    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for sample in pending_samples:
            futures.append(executor.submit(process_single_task, sample, args, output_dir, code_output_dir))
            if args.delay > 0:
                time.sleep(args.delay / max(args.num_workers, 1))

        for future in as_completed(futures):
            try:
                result_data = future.result()
            except Exception as exc:
                safe_print(f"Task execution error: {exc}")
                failed_count += 1
                continue

            if result_data.get("status") == "success":
                success_count += 1
                total_tokens += int(result_data.get("tokens", 0))
                append_result_to_file(result_data["result"], str(save_path))
            else:
                failed_count += 1

    safe_print(f"Results saved to: {save_path}")
    safe_print(f"Success: {success_count}, Failed: {failed_count}, Tokens: {total_tokens}")


if __name__ == "__main__":
    main()
