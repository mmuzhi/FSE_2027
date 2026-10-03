import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import api_defaults, append_result_to_file, call_api_stream, load_existing_task_ids, safe_print

sys.stdout = os.fdopen(sys.stdout.fileno(), "w", buffering=1)


def stringify_field(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def sanitize_filename(text: str) -> str:
    return re.sub(r"[\\/:*?\"<>|]+", "_", text)


def build_prompt(language: str, code: str, input_text: str) -> str:
    return (
        f"Here's some {language} code and the inputs passed into it.\n"
        "What output do you expect from it?\n"
        f"Code: {language}\n{code}\n"
        f"Inputs: {input_text}\n"
        "Answer using <ans></ans> tags"
    )


def extract_answer(answer_text: str) -> str:
    if not answer_text:
        return ""
    match = re.search(r"<ans>(.*?)</ans>", answer_text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return answer_text.strip()


def parse_txt_sections(txt_content: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    prompt_match = re.search(r"=== PROMPT ===\n(.*?)\n\n=== REASONING ===", txt_content, re.DOTALL)
    if prompt_match:
        sections["prompt"] = prompt_match.group(1).strip()

    cot_match = re.search(r"=== REASONING ===\n<think>\n(.*?)\n</think>", txt_content, re.DOTALL)
    if cot_match:
        sections["cot"] = cot_match.group(1).strip()

    raw_match = re.search(r"=== RAW ANSWER ===\n(.*?)\n\n=== PARSED ANSWER ===", txt_content, re.DOTALL)
    if raw_match:
        sections["raw_answer_full"] = raw_match.group(1).strip()

    parsed_match = re.search(r"=== PARSED ANSWER ===\n(.*)", txt_content, re.DOTALL)
    if parsed_match:
        sections["parsed_answer"] = parsed_match.group(1).strip()

    return sections


def recover_result_from_txt(sample: dict[str, Any], output_dir: Path, save_path: Path) -> bool:
    task_id = str(sample.get("task_id") or "unknown")
    txt_path = output_dir / f"{sanitize_filename(task_id)}.txt"
    if not txt_path.exists():
        return False

    try:
        content = txt_path.read_text(encoding="utf-8")
    except Exception:
        return False

    sections = parse_txt_sections(content)
    raw_answer_full = sections.get("raw_answer_full", "")
    parsed_answer = extract_answer(raw_answer_full) or sections.get("parsed_answer", "")

    result = {
        "task_id": task_id,
        "language": str(sample.get("language", "")),
        "category": str(sample.get("category", "")),
        "code": sample.get("code", ""),
        "input": sample.get("input", ""),
        "expected_output": sample.get("output", ""),
        "prompt": sections.get("prompt", ""),
        "cot": sections.get("cot", ""),
        "answer": parsed_answer,
        "raw_answer": parsed_answer,
        "raw_answer_full": raw_answer_full,
    }
    return append_result_to_file(result, str(save_path))


def process_single_task(sample: dict[str, Any], args, output_dir: Path) -> dict[str, Any]:
    task_id = str(sample.get("task_id") or "unknown")
    language = str(sample.get("language", "python"))
    code = str(sample.get("code", ""))
    input_text = stringify_field(sample.get("input", ""))

    prompt = build_prompt(language=language, code=code, input_text=input_text)
    safe_print(f"[{task_id}] Start...")

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
        return {"status": "failed", "task_id": task_id, "error": error_msg, "time": elapsed}

    parsed_answer = extract_answer(answer_text)
    estimated_tokens = (len(reasoning_content) + len(answer_text)) // 4

    result = {
        "task_id": task_id,
        "language": language,
        "category": str(sample.get("category", "")),
        "code": code,
        "input": sample.get("input", ""),
        "expected_output": sample.get("output", ""),
        "prompt": prompt,
        "cot": reasoning_content,
        "answer": parsed_answer,
        "raw_answer": parsed_answer,
        "raw_answer_full": answer_text,
    }

    full_text = (
        f"=== PROMPT ===\n{prompt}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== RAW ANSWER ===\n{answer_text}\n\n"
        f"=== PARSED ANSWER ===\n{parsed_answer}\n"
    )
    txt_path = output_dir / f"{sanitize_filename(task_id)}.txt"
    txt_path.write_text(full_text, encoding="utf-8")
    safe_print(f"[{task_id}] Done ({elapsed:.2f}s, ~{estimated_tokens} tokens)")

    return {
        "status": "success",
        "task_id": task_id,
        "result": result,
        "tokens": estimated_tokens,
        "time": elapsed,
    }


def load_dataset(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("JSON dataset must be a list.")
        return [x for x in data if isinstance(x, dict)]

    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at {path}:{line_no}") from exc
        if isinstance(obj, dict):
            records.append(obj)
    return records


def main() -> None:
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    api = api_defaults()

    parser = argparse.ArgumentParser(description="Execution CoT for CodeSense dataset")
    parser.add_argument("--base_url", default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", default=api["api_key"], help="API key")
    parser.add_argument("--model", default=api["model"], help="Model name")
    parser.add_argument(
        "--data",
        default=str(project_root / "data" / "CodeSense" / "input_output_dataset.jsonl"),
        help="CodeSense optimized dataset path (jsonl/json)",
    )
    parser.add_argument(
        "--output_dir",
        default=str(project_root / "data" / "derived_cot" / "rq1_traces" / "execution" / "glm5.1" / "txt_output"),
        help="Directory for per-task text outputs",
    )
    parser.add_argument(
        "--save_path",
        default=str(project_root / "data" / "derived_cot" / "rq1_traces" / "execution" / "glm5.1" / "results.jsonl"),
        help="Path to save JSONL results",
    )
    parser.add_argument("--max_tokens", type=int, default=51200, help="Max tokens for generation")
    parser.add_argument("--temperature", type=float, default=0.6, help="Sampling temperature")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p sampling")
    parser.add_argument("--num_samples", type=int, default=-1, help="Number of pending samples to process")
    parser.add_argument("--num_workers", type=int, default=20, help="Parallel worker count")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between submissions in seconds")
    parser.add_argument("--max_retries", type=int, default=2, help="Max retries for API request")
    args = parser.parse_args()

    if not args.api_key:
        raise ValueError("Missing API key. Set --api_key or API_KEY / <ALIAS>_API_KEY in .env.")

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    data_path = Path(args.data)
    samples = load_dataset(data_path)

    for i, sample in enumerate(samples):
        sample.setdefault("task_id", f"sample-{i}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = Path(args.save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    safe_print("\n" + "=" * 80)
    safe_print(" Execution CoT For CodeSense")
    safe_print("=" * 80)
    safe_print(f" Base URL: {args.base_url}")
    safe_print(f" Model: {args.model}")
    safe_print(f" Data: {data_path} ({len(samples)} records)")
    safe_print(f" Save Path: {save_path}")
    safe_print(f" Output Dir: {output_dir}")
    safe_print(f" Max Tokens: {args.max_tokens}")
    safe_print(f" Temperature: {args.temperature}")
    safe_print(f" Top-p: {args.top_p}")
    safe_print(f" Parallel Workers: {args.num_workers}")
    safe_print(f" Delay: {args.delay}s")
    safe_print("=" * 80 + "\n")

    saved_task_ids = load_existing_task_ids(str(save_path))
    safe_print(f"Found {len(saved_task_ids)} task_ids in JSONL; skip enabled.")

    recovered = 0
    for sample in samples:
        tid = str(sample.get("task_id"))
        if tid in saved_task_ids:
            continue
        if recover_result_from_txt(sample, output_dir, save_path):
            recovered += 1
            saved_task_ids.add(tid)
    if recovered:
        safe_print(f"Recovered {recovered} tasks from existing txt outputs.")

    pending_samples = [s for s in samples if str(s.get("task_id")) not in saved_task_ids]
    if args.num_samples > 0:
        pending_samples = pending_samples[: args.num_samples]

    if not pending_samples:
        safe_print("No pending tasks. Exit.")
        return

    total_tokens = 0
    success_count = 0
    failed_count = 0
    total_time_start = time.time()

    safe_print(f"Start processing {len(pending_samples)} tasks\n")
    with ThreadPoolExecutor(max_workers=args.num_workers) as executor:
        futures = []
        for sample in pending_samples:
            futures.append(executor.submit(process_single_task, sample, args, output_dir))
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

    total_time = time.time() - total_time_start
    safe_print("\n" + "=" * 80)
    safe_print(" Execution Stats")
    safe_print(f" Total tasks processed: {len(pending_samples)}")
    safe_print(f" Success: {success_count}, Failed: {failed_count}")
    safe_print(f" Total time: {total_time:.2f}s")
    if success_count + failed_count > 0:
        safe_print(f" Avg time per task: {total_time / (success_count + failed_count):.2f}s")
    safe_print(f" Estimated tokens: {total_tokens}")
    safe_print(f" Avg tokens (success only): {total_tokens / success_count:.2f}" if success_count else "N/A")
    safe_print(f" Results saved to: {save_path}")
    safe_print("=" * 80)


if __name__ == "__main__":
    main()
