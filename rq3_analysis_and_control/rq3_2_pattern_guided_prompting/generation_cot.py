import argparse
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from utils import api_defaults, append_result_to_file, call_api_stream, load_existing_task_ids, safe_print

from prompt_utils import (
    PROMPT_METHODS,
    infer_prompt_variant,
    load_json_records,
    render_prompt,
    results_dir,
)

sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)


def extract_code_from_text(text: str) -> str:
    if not text:
        return ""
    code_block = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if code_block:
        return code_block[0].strip()
    return text.strip()


def build_prompt(example: dict, args) -> tuple[str, dict]:
    return render_prompt(
        task="generation",
        model_name=args.model,
        prompt_method=args.prompt_method,
        prompt_variant=args.prompt_variant,
        templates_path=args.templates_path,
        question_content=example["question_content"],
        starter_code=example.get("starter_code", ""),
    )


def process_single_task(task_data):
    example, args, output_dir = task_data
    task_id = example.get("question_id", example.get("task_id", "unknown"))
    output_file = output_dir / f"{task_id}.txt"

    safe_print(f"[{task_id}] Start...")
    prompt, prompt_meta = build_prompt(example, args)
    start_time = time.time()

    reasoning_content, final_answer, success, error_msg = call_api_stream(
        prompt=prompt,
        api_key=args.api_key,
        base_url=args.base_url,
        model_name=args.model,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_p=args.top_p,
        task_id=task_id,
    )

    elapsed = time.time() - start_time
    if not success:
        safe_print(f"[{task_id}] Failed ({elapsed:.2f}s): {error_msg}")
        return {"status": "failed", "task_id": task_id, "time": elapsed}

    code = extract_code_from_text(final_answer)
    estimated_tokens = (len(reasoning_content) + len(final_answer)) // 4
    result = {
        "task_id": task_id,
        "prompt_method": prompt_meta["method"],
        "prompt_variant": prompt_meta["variant"],
        "prompt_task": prompt_meta["task"],
        "prompt": prompt,
        "cot": reasoning_content,
        "answer": code,
    }

    full_text = (
        f"=== PROMPT VARIANT ===\n{prompt_meta['variant']}\n\n"
        f"=== PROMPT ===\n{prompt}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== ANSWER ===\n{final_answer}"
    )
    output_file.write_text(full_text, encoding="utf-8")
    safe_print(f"[{task_id}] Done ({elapsed:.2f}s, ~{estimated_tokens} tokens)")

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

    parser = argparse.ArgumentParser(description="RQ3.2 generation CoT collection")
    parser.add_argument("--base_url", type=str, default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", type=str, default=api["api_key"], help="API key")
    parser.add_argument("--model", type=str, default=api["model"], help="Model name")
    parser.add_argument("--data", type=str, default=str(project_root / "data" / "LCB" / "v4_v6.jsonl"))
    parser.add_argument(
        "--prompt_method",
        type=str,
        default="anti_pattern_only",
        choices=PROMPT_METHODS,
    )
    parser.add_argument("--prompt_variant", type=str, default="r1")
    parser.add_argument("--templates_path", type=str, default=str(script_dir / "prompt_templates.json"))
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--save_path", type=str, default=None)
    parser.add_argument("--max_tokens", type=int, default=51200)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--num_samples", type=int, default=-1)
    parser.add_argument("--num_workers", type=int, default=20)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    resolved_variant = infer_prompt_variant(args.model, args.prompt_variant)
    base_results_dir = results_dir(
        project_root,
        "generation",
        args.model,
        args.prompt_method,
        resolved_variant,
    )
    if args.output_dir is None:
        args.output_dir = str(base_results_dir / "txt_output")
    if args.save_path is None:
        args.save_path = str(base_results_dir / "results.jsonl")

    all_examples = load_json_records(args.data)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = Path(args.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    saved_task_ids = load_existing_task_ids(str(save_path))
    pending_examples = [
        example
        for example in all_examples
        if example.get("question_id", example.get("task_id", "unknown")) not in saved_task_ids
    ]
    if args.num_samples > 0:
        pending_examples = pending_examples[: args.num_samples]
    if not pending_examples:
        safe_print("No pending tasks. Exit.")
        return

    total_tokens = 0
    success_count = 0
    failed_count = 0
    tasks = [(example, args, output_dir) for example in pending_examples]

    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for task in tasks:
            futures.append(executor.submit(process_single_task, task))
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
