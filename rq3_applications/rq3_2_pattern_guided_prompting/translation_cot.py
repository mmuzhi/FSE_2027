from __future__ import annotations

import argparse
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


def build_prompt(source_code: str, source_lang: str, target_lang: str, args) -> tuple[str, dict]:
    return render_prompt(
        task="translation",
        model_name=args.model,
        prompt_method=args.prompt_method,
        prompt_variant=args.prompt_variant,
        templates_path=args.templates_path,
        source_lang=source_lang,
        target_lang=target_lang,
        source_code=source_code,
    )


def get_code_extension(lang: str) -> str:
    return {
        "java": ".java",
        "cpp": ".cpp",
        "py": ".py",
        "python": ".py",
    }.get(lang, f".{lang}")


def extract_code_from_text(answer_text: str, target_lang: str) -> str | None:
    if not answer_text:
        return None
    lang_patterns = {
        "cpp": r"```(?:cpp|c\+\+)\s*\n([\s\S]*?)\n```",
        "java": r"```java\s*\n([\s\S]*?)\n```",
        "py": r"```(?:python|py)\s*\n([\s\S]*?)\n```",
        "python": r"```(?:python|py)\s*\n([\s\S]*?)\n```",
    }
    pattern = lang_patterns.get(target_lang)
    if pattern:
        match = re.search(pattern, answer_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    match = re.search(r"```\w*\s*\n([\s\S]*?)\n```", answer_text)
    if match:
        return match.group(1).strip()
    return None


def load_source_files(data_dir: Path, source_lang: str) -> list[dict]:
    solution_dir = data_dir / source_lang / "solutuon"
    if not solution_dir.exists():
        solution_dir = data_dir / source_lang / "solution"
    if not solution_dir.exists():
        raise FileNotFoundError(f"Solution directory not found: {solution_dir}")

    ext = get_code_extension(source_lang)
    samples = []
    for file_path in sorted(solution_dir.glob(f"*{ext}")):
        source_code = file_path.read_text(encoding="utf-8")
        samples.append({
            "task_id": file_path.stem,
            "source_code": source_code,
            "source_file": str(file_path),
        })
    return samples


def process_single_task(task_data: dict, args, output_dir: Path, code_output_dir: Path) -> dict:
    task_id = task_data["task_id"]
    source_code = task_data["source_code"]
    safe_print(f"[{task_id}] Start translation...")

    prompt, prompt_meta = build_prompt(source_code, args.source_lang, args.target_lang, args)
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

    translated_code = extract_code_from_text(answer_text, args.target_lang) or ""
    estimated_tokens = (len(reasoning_content) + len(answer_text)) // 4
    result = {
        "task_id": f"{args.source_lang}_to_{args.target_lang}_{task_id}",
        "original_task_id": task_id,
        "source_lang": args.source_lang,
        "target_lang": args.target_lang,
        "source_code": source_code,
        "prompt_method": prompt_meta["method"],
        "prompt_variant": prompt_meta["variant"],
        "prompt_task": prompt_meta["task"],
        "prompt": prompt,
        "cot": reasoning_content,
        "translated_code": translated_code,
        "raw_answer": answer_text,
    }

    full_text = (
        f"=== PROMPT VARIANT ===\n{prompt_meta['variant']}\n\n"
        f"=== SOURCE CODE ({args.source_lang}) ===\n{source_code}\n\n"
        f"=== PROMPT ===\n{prompt}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== RAW ANSWER ===\n{answer_text}\n\n"
        f"=== TRANSLATED CODE ({args.target_lang}) ===\n{translated_code}\n"
    )
    (output_dir / f"{task_id}.txt").write_text(full_text, encoding="utf-8")
    if translated_code:
        (code_output_dir / f"{task_id}{get_code_extension(args.target_lang)}").write_text(translated_code, encoding="utf-8")

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

    parser = argparse.ArgumentParser(description="RQ3.2 translation CoT collection")
    parser.add_argument("--base_url", type=str, default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", type=str, default=api["api_key"], help="API key")
    parser.add_argument("--model", type=str, default=api["model"], help="Model name")
    parser.add_argument("--data_dir", type=str, default=str(project_root / "data" / "ClassEval_T"))
    parser.add_argument("--source_lang", type=str, default="cpp")
    parser.add_argument("--target_lang", type=str, default="py")
    parser.add_argument("--lang_pairs", type=str, default="cpp-py,java-py,java-cpp,py-cpp")
    parser.add_argument(
        "--prompt_method",
        type=str,
        default="pattern_and_anti",
        choices=PROMPT_METHODS,
    )
    parser.add_argument("--prompt_variant", type=str, default="auto")
    parser.add_argument("--templates_path", type=str, default=str(script_dir / "prompt_templates.json"))
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--code_output_dir", type=str, default=None)
    parser.add_argument("--save_path", type=str, default=None)
    parser.add_argument("--max_tokens", type=int, default=16384)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--num_samples", type=int, default=10)
    parser.add_argument("--num_workers", type=int, default=10)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--max_retries", type=int, default=2)
    args = parser.parse_args()

    lang_pairs = [
        tuple(part.strip() for part in pair.strip().split("-", 1))
        for pair in args.lang_pairs.split(",")
        if pair.strip()
    ] or [(args.source_lang, args.target_lang)]

    resolved_variant = infer_prompt_variant(args.model, args.prompt_variant)
    base_results_dir = results_dir(
        project_root,
        "translation",
        args.model,
        args.prompt_method,
        resolved_variant,
    )
    save_path = Path(args.save_path) if args.save_path else base_results_dir / "results.jsonl"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    all_stats = []
    for source_lang, target_lang in lang_pairs:
        args.source_lang = source_lang
        args.target_lang = target_lang

        pair_dir = base_results_dir / f"{source_lang}_to_{target_lang}"
        output_dir = Path(args.output_dir) if args.output_dir else pair_dir / "txt_output"
        code_output_dir = Path(args.code_output_dir) if args.code_output_dir else pair_dir / "code_output"
        output_dir.mkdir(parents=True, exist_ok=True)
        code_output_dir.mkdir(parents=True, exist_ok=True)

        samples = load_source_files(Path(args.data_dir), source_lang)
        saved_task_ids = load_existing_task_ids(str(save_path))
        prefix = f"{source_lang}_to_{target_lang}_"
        pair_saved_ids = {tid[len(prefix):] for tid in saved_task_ids if tid.startswith(prefix)}
        pending_samples = [s for s in samples if s["task_id"] not in pair_saved_ids]
        if args.num_samples > 0:
            pending_samples = pending_samples[: args.num_samples]
        if not pending_samples:
            safe_print(f"No pending tasks for {source_lang}->{target_lang}.")
            continue

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

        all_stats.append({
            "pair": f"{source_lang}->{target_lang}",
            "total": len(pending_samples),
            "success": success_count,
            "failed": failed_count,
            "tokens": total_tokens,
        })

    safe_print(f"Results saved to: {save_path}")
    for stat in all_stats:
        safe_print(f"{stat['pair']}: {stat['success']}/{stat['total']} success, {stat['tokens']} tokens")


if __name__ == "__main__":
    main()
