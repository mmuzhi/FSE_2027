from __future__ import annotations

import os
import sys
import json
import re
import time
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import api_defaults, safe_print, load_existing_task_ids, call_api_stream, append_result_to_file

sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)


def parse_txt_sections(txt_content: str) -> dict:
    sections = {}
    m = re.search(r"=== BUGGY CODE ===\n(.*?)\n\n=== REASONING ===", txt_content, re.DOTALL)
    if m:
        sections["buggy_code"] = m.group(1).strip()
    m = re.search(r"=== REASONING ===\n<think>\n(.*?)\n</think>", txt_content, re.DOTALL)
    if m:
        sections["cot"] = m.group(1).strip()
    m = re.search(r"=== RAW ANSWER ===\n(.*?)\n\n=== FIXED CODE ===", txt_content, re.DOTALL)
    if m:
        sections["raw_answer_full"] = m.group(1).strip()
    m = re.search(r"=== FIXED CODE ===\n(.*)", txt_content, re.DOTALL)
    if m:
        sections["fixed_code"] = m.group(1).strip()
    return sections


def recover_result_from_txt(task_id: str, output_dir: Path, save_path: Path) -> bool:
    """If txt exists but JSONL missing, parse txt and append reconstructed result."""
    txt_path = output_dir / f"{task_id}.txt"
    if not txt_path.exists():
        return False

    try:
        content = txt_path.read_text(encoding="utf-8")
    except Exception:
        return False

    sections = parse_txt_sections(content)
    fixed_code = extract_code_from_text(sections.get("raw_answer_full", ""))

    result = {
        "task_id": task_id,
        "buggy_code": sections.get("buggy_code", ""),
        "cot": sections.get("cot", ""),
        "fixed_code": fixed_code or sections.get("fixed_code", ""),
        "raw_answer": sections.get("raw_answer_full", ""),
    }

    return append_result_to_file(result, str(save_path))


def build_prompt(buggy_code: str) -> str:
    return (
        "Observe the following faulty python code. It contains one or more bugs. "
        "Fix the code and output only the fixed code.\n\n"
        f"```python\n{buggy_code}\n```"
    )


def extract_code_from_text(answer_text: str) -> str | None:
    if not answer_text:
        return None

    match = re.search(r"```(?:python|py)?\s*\n([\s\S]*?)\n```", answer_text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\w*\s*\n([\s\S]*?)\n```", answer_text)
    return match.group(1).strip() if match else None


def process_single_task(
    task_data: dict,
    args,
    output_dir: Path,
    code_output_dir: Path
) -> dict:
    task_id = task_data["task_id"]
    buggy_code = task_data["buggy_code"]

    safe_print(f"[{task_id}] Start bug fixing...")

    prompt = build_prompt(buggy_code)
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
        return {
            "status": "failed",
            "task_id": task_id,
            "error": error_msg,
            "time": elapsed,
        }

    fixed_code = extract_code_from_text(answer_text)
    if not fixed_code:
        fixed_code = ""

    total_chars = len(reasoning_content) + len(answer_text)
    estimated_tokens = total_chars // 4

    result = {
        "task_id": task_id,
        "buggy_code": buggy_code,
        "cot": reasoning_content,
        "fixed_code": fixed_code,
        "raw_answer": answer_text,
    }

    full_text = (
        f"=== BUGGY CODE ===\n{buggy_code}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== RAW ANSWER ===\n{answer_text}\n\n"
        f"=== FIXED CODE ===\n{fixed_code}\n"
    )

    output_file = output_dir / f"{task_id}.txt"
    try:
        output_file.write_text(full_text, encoding="utf-8")
    except Exception as e:
        safe_print(f"[{task_id}] Failed to save text file: {e}")

    if fixed_code:
        (code_output_dir / f"{task_id}.py").write_text(fixed_code, encoding="utf-8")
    return {
        "status": "success",
        "task_id": task_id,
        "result": result,
        "tokens": estimated_tokens,
        "time": elapsed,
    }


def load_source_files(data_path: Path) -> list[dict]:
    data = json.loads(data_path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("DebugBench dataset must be a list.")

    samples = []
    seen_task_ids = set()
    for item in data:
        task_id = str(item.get("sample_id", "")).strip()
        if not task_id:
            raise ValueError("Missing sample_id in DebugBench dataset record.")
        if task_id in seen_task_ids:
            raise ValueError(f"Duplicate sample_id found: {task_id}")
        seen_task_ids.add(task_id)

        buggy_code = item.get("buggy_code", "").strip()
        samples.append({
            "task_id": task_id,
            "buggy_code": buggy_code,
            "level": item.get("level", ""),
        })

    return samples


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    api = api_defaults()

    parser = argparse.ArgumentParser(description="Bug Fixing using LLM API (OpenAI SDK)")
    parser.add_argument("--base_url", default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", default=api["api_key"], help="API key")
    parser.add_argument("--model", default=api["model"], help="Model name")
    parser.add_argument(
        "--data_path",
        default=str(project_root / "data" / "DebugBench" / "python_samples.json"),
        help="DebugBench data path"
    )
    parser.add_argument(
        "--output_dir",
        default=None,
        help="Output directory for saving per-task text (auto-generated if not specified)",
    )
    parser.add_argument(
        "--code_output_dir",
        default=None,
        help="Output directory for saving fixed code files (auto-generated if not specified)",
    )
    parser.add_argument(
        "--save_path",
        default=None,
        help="Path to save final JSONL results (auto-generated if not specified)",
    )
    parser.add_argument("--max_tokens", type=int, default=51200, help="Maximum number of tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.6, help="Temperature for sampling")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p for sampling")
    parser.add_argument("--num_samples", type=int, default=-1, help="Number of samples to process (-1 for all)")
    parser.add_argument("--num_workers", type=int, default=20, help="Number of parallel workers")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between API calls in seconds")
    parser.add_argument("--max_retries", type=int, default=2, help="Max retries on failure")
    args = parser.parse_args()

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    base_output_dir = project_root / "data" / "derived_cot" / "rq1_traces" / "debug" / "glm5.1"

    if args.output_dir is None:
        args.output_dir = str(base_output_dir / "txt_output")
    if args.code_output_dir is None:
        args.code_output_dir = str(base_output_dir / "code_output")
    if args.save_path is None:
        args.save_path = str(base_output_dir / "results.jsonl")

    data_path = Path(args.data_path)
    samples = load_source_files(data_path)

    safe_print("\n" + "=" * 80)
    safe_print(" Bug Fixing with CoT")
    safe_print("=" * 80)
    safe_print(f" Base URL: {args.base_url}")
    safe_print(f" Model: {args.model}")
    safe_print(f" Data Path: {data_path} ({len(samples)} samples)")
    safe_print(f" Max Tokens: {args.max_tokens}")
    safe_print(f" Temperature: {args.temperature}")
    safe_print(f" Parallel Workers: {args.num_workers}")
    safe_print(f" Delay: {args.delay}s between requests")
    safe_print(f" Output Dir: {args.output_dir}")
    safe_print(f" Code Output Dir: {args.code_output_dir}")
    safe_print(f" Results JSONL: {args.save_path}")
    safe_print("=" * 80 + "\n")

    output_dir = Path(args.output_dir)
    code_output_dir = Path(args.code_output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    code_output_dir.mkdir(parents=True, exist_ok=True)

    save_path = Path(args.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    saved_task_ids = load_existing_task_ids(str(save_path))
    safe_print(f"Found {len(saved_task_ids)} task_ids in JSONL; will skip them.")

    recovered = 0
    for sample in samples:
        tid = sample["task_id"]
        if tid in saved_task_ids:
            continue
        if recover_result_from_txt(tid, output_dir, save_path):
            recovered += 1
            saved_task_ids.add(tid)

    if recovered:
        safe_print(f"Recovered {recovered} tasks from existing txt outputs.")

    pending_samples = [s for s in samples if s["task_id"] not in saved_task_ids]
    if args.num_samples > 0:
        pending_samples = pending_samples[:args.num_samples]

    if not pending_samples:
        safe_print("No pending tasks. Exit.")
        return

    safe_print(f"Start processing {len(pending_samples)} tasks\n")

    total_tokens = 0
    success_count = 0
    failed_count = 0

    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for sample in pending_samples:
            futures.append(
                executor.submit(process_single_task, sample, args, output_dir, code_output_dir)
            )
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
                total_tokens += result_data.get("tokens", 0)
                append_result_to_file(result_data["result"], str(save_path))
            else:
                failed_count += 1

    safe_print(f"\n{'=' * 80}")
    safe_print(" Bug Fixing Stats")
    safe_print(f" Total tasks processed: {len(pending_samples)}")
    safe_print(f" Success: {success_count}, Failed: {failed_count}")
    safe_print(f" Estimated tokens: {total_tokens}")
    safe_print(f" Avg tokens (success only): {total_tokens / success_count:.2f}" if success_count else "N/A")
    safe_print(f" Results saved to: {save_path}")
    safe_print(f" Fixed code files saved to: {code_output_dir}")
    safe_print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
