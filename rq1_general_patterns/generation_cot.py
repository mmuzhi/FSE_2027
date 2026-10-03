import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import api_defaults, append_result_to_file, call_api_stream, load_existing_task_ids, safe_print

sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)


def build_prompt(example: dict) -> str:
    question_content = example["question_content"]
    starter_code = example.get("starter_code", "")
    return (
        "You will be given a competitive programming problem.\n"
        f"{question_content}\n\n"
        "You will use the following starter code to write the solution to the problem and enclose your code within delimiters.\n"
        f"```python\n{starter_code}\n```"
    )


def extract_code_from_text(text: str) -> str:
    if not text:
        return ""
    code_block = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if code_block:
        return code_block[0].strip()
    return text.strip()


def load_examples(path: Path) -> list[dict]:
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        return [item for item in data if isinstance(item, dict)]
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def process_single_task(example, args, output_dir):
    task_id = example.get("question_id", example.get("task_id", "unknown"))
    output_file = output_dir / f"{task_id}.txt"

    safe_print(f"[{task_id}] Start...")
    prompt = build_prompt(example)
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

    generation_time = time.time() - start_time
    if not success:
        safe_print(f"[{task_id}] Failed ({generation_time:.2f}s): {error_msg}")
        return {
            "status": "failed",
            "task_id": task_id,
            "result": None,
            "tokens": 0,
            "time": generation_time,
        }

    code = extract_code_from_text(final_answer)
    estimated_tokens = (len(reasoning_content) + len(final_answer)) // 4
    result = {
        "task_id": task_id,
        "prompt": prompt,
        "cot": reasoning_content,
        "answer": code,
    }

    full_text = (
        f"=== PROMPT ===\n{prompt}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== ANSWER ===\n{final_answer}"
    )
    output_file.write_text(full_text, encoding="utf-8")
    safe_print(f"[{task_id}] Done ({generation_time:.2f}s, ~{estimated_tokens} tokens)")

    return {
        "status": "success",
        "task_id": task_id,
        "result": result,
        "tokens": estimated_tokens,
        "time": generation_time,
    }


def generate_main(args) -> None:
    print("\n" + "=" * 80)
    print(" API Code Generation (Parallel Stream Mode - OpenAI SDK)")
    print("=" * 80)
    print(f" Base URL: {args.base_url}")
    print(f" Model: {args.model}")
    print(f" Data: {args.data}")
    print(f" Max Tokens: {args.max_tokens}")
    print(f" Temperature: {args.temperature}")
    print(f" Parallel Workers: {args.num_workers}")
    print(f" Delay: {args.delay}s between requests")
    print("=" * 80 + "\n")

    all_examples = load_examples(Path(args.data))
    print(f" Total examples in dataset: {len(all_examples)}")

    print("Loading existing task_ids from results file...")
    save_path = Path(args.save_path)
    saved_task_ids = load_existing_task_ids(str(save_path))
    print(f" Found {len(saved_task_ids)} existing task_ids")

    print("Filtering out completed tasks...")
    pending_examples = [
        example
        for example in all_examples
        if example.get("question_id", example.get("task_id", "unknown")) not in saved_task_ids
    ]
    print(f" Pending tasks: {len(pending_examples)}")

    if args.num_samples > 0:
        examples = pending_examples[: args.num_samples]
        print(f" Selected {len(examples)} tasks to generate (limited by num_samples)")
    else:
        examples = pending_examples
        print(f" Will generate all {len(examples)} pending tasks")

    if not examples:
        print("All tasks already completed!")
        return

    output_dir = Path(args.output_dir)
    print(f" Save results in {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    print("Start parallel generation process\n")

    total_time_start = time.time()
    total_tokens = 0
    total_count = 0
    failed_count = 0

    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for example in examples:
            futures.append(executor.submit(process_single_task, example, args, output_dir))
            if args.delay > 0:
                time.sleep(args.delay / max(args.num_workers, 1))

        for future in as_completed(futures):
            try:
                result_data = future.result()
                if result_data["status"] == "success":
                    total_count += 1
                    total_tokens += result_data["tokens"]
                    append_result_to_file(result_data["result"], str(save_path))
                else:
                    failed_count += 1
            except Exception as exc:
                safe_print(f"Task execution error: {exc}")
                failed_count += 1

    total_time = time.time() - total_time_start

    print(f"\n\n{'=' * 80}")
    print(" Generation Statistics")
    print(f"{'=' * 80}")
    print(f" Total time: {total_time:.2f}s")
    print(f" Successful count: {total_count}")
    print(f" Failed count: {failed_count}")
    if total_count + failed_count > 0:
        print(f" Avg time per task: {total_time / (total_count + failed_count):.2f}s")
    else:
        print(" Avg time per task: N/A")
    print(f" Total tokens (estimated): {total_tokens}")
    if total_count > 0:
        print(f" Avg tokens (estimated): {total_tokens / total_count:.2f}")
    else:
        print(" Avg tokens (estimated): N/A")
    print(f" Speedup: ~{len(examples) / total_time * 60:.1f} tasks/minute")
    print(f"{'=' * 80}\n")

    print(f" Results saved to {save_path}")
    print(" Generation completed!")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    api = api_defaults()

    parser = argparse.ArgumentParser(description="Generate code solutions using API (OpenAI SDK)")
    parser.add_argument("--base_url", default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", default=api["api_key"], help="API key")
    parser.add_argument("--model", default=api["model"], help="Model name")
    parser.add_argument(
        "--data",
        default=str(project_root / "data" / "LCB" / "v4_v6.jsonl"),
        help="Data path",
    )
    parser.add_argument(
        "--output_dir",
        default=str(project_root / "data" / "derived_cot" / "rq1_traces" / "generation" / "glm5.1" / "v4_v6" / "txt_output"),
        help="Output directory for saving results",
    )
    parser.add_argument(
        "--save_path",
        default=str(project_root / "data" / "derived_cot" / "rq1_traces" / "generation" / "glm5.1" / "v4_v6" / "results.jsonl"),
        help="Path to save final results",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=51200,
        help="Maximum number of tokens to generate",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.6,
        help="Temperature for sampling",
    )
    parser.add_argument(
        "--top_p",
        type=float,
        default=0.95,
        help="Top-p for sampling",
    )
    parser.add_argument(
        "--num_samples",
        type=int,
        default=-1,
        help="Number of samples to process from pending tasks (-1 for all)",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=30,
        help="Number of parallel workers",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between API calls in seconds (to avoid rate limits)",
    )

    args = parser.parse_args()
    generate_main(args)
