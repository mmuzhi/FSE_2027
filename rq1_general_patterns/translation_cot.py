#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
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
    m = re.search(r"=== SOURCE CODE(?: \([^)]+\))? ===\n(.*?)\n\n=== REASONING ===", txt_content, re.DOTALL)
    if m:
        sections["source_code"] = m.group(1).strip()
    m = re.search(r"=== REASONING ===\n<think>\n(.*?)\n</think>", txt_content, re.DOTALL)
    if m:
        sections["cot"] = m.group(1).strip()
    m = re.search(r"=== RAW ANSWER ===\n(.*?)\n\n=== TRANSLATED CODE(?: \([^)]+\))? ===", txt_content, re.DOTALL)
    if m:
        sections["raw_answer_full"] = m.group(1).strip()
    m = re.search(r"=== TRANSLATED CODE(?: \([^)]+\))? ===\n(.*)", txt_content, re.DOTALL)
    if m:
        sections["translated_code"] = m.group(1).strip()
    return sections


def recover_result_from_txt(task_id: str, source_lang: str, target_lang: str, 
                            output_dir: Path, save_path: Path) -> bool:
    """If txt exists but JSONL missing, parse txt and append reconstructed result."""
    txt_path = output_dir / f"{task_id}.txt"
    if not txt_path.exists():
        return False

    try:
        content = txt_path.read_text(encoding="utf-8")
    except Exception:
        return False

    sections = parse_txt_sections(content)
    translated_code = extract_code_from_text(sections.get("raw_answer_full", ""), target_lang)

    result = {
        "task_id": f"{source_lang}_to_{target_lang}_{task_id}",
        "original_task_id": task_id,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source_code": sections.get("source_code", ""),
        "cot": sections.get("cot", ""),
        "translated_code": translated_code or sections.get("translated_code", ""),
        "raw_answer": sections.get("raw_answer_full", ""),
    }

    return append_result_to_file(result, str(save_path))


def build_prompt(source_code: str, source_lang: str, target_lang: str) -> str:
    lang_names = {
        "java": "Java",
        "cpp": "C++",
        "py": "Python",
        "python": "Python",
    }
    source_name = lang_names.get(source_lang, source_lang)
    target_name = lang_names.get(target_lang, target_lang)
    
    return (
        f"You are an expert programmer. Translate the following {source_name} code to {target_name}.\n"
        f"- Keep behavior identical (inputs/outputs, side effects, edge cases, exceptions).\n"
        f"- Use idiomatic {target_name} only when it doesn't change behavior.\n\n"
        f"```{source_lang}\n{source_code}\n```"
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
    return match.group(1).strip() if match else None


def process_single_task(
    task_data: dict, 
    args, 
    output_dir: Path, 
    code_output_dir: Path
) -> dict:
    task_id = task_data["task_id"]
    source_code = task_data["source_code"]
    source_lang = args.source_lang
    target_lang = args.target_lang

    safe_print(f"[{task_id}] Start translation ({source_lang} -> {target_lang})...")

    prompt = build_prompt(source_code, source_lang, target_lang)
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

    translated_code = extract_code_from_text(answer_text, target_lang) or ""
    total_chars = len(reasoning_content) + len(answer_text)
    estimated_tokens = total_chars // 4

    result = {
        "task_id": f"{source_lang}_to_{target_lang}_{task_id}",
        "original_task_id": task_id,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "source_code": source_code,
        "cot": reasoning_content,
        "translated_code": translated_code,
        "raw_answer": answer_text,
    }

    full_text = (
        f"=== SOURCE CODE ({source_lang}) ===\n{source_code}\n\n"
        f"=== REASONING ===\n<think>\n{reasoning_content}\n</think>\n\n"
        f"=== RAW ANSWER ===\n{answer_text}\n\n"
        f"=== TRANSLATED CODE ({target_lang}) ===\n{translated_code}\n"
    )

    output_file = output_dir / f"{task_id}.txt"
    output_file.write_text(full_text, encoding="utf-8")

    if translated_code:
        (code_output_dir / f"{task_id}{get_code_extension(target_lang)}").write_text(translated_code, encoding="utf-8")

    safe_print(f"[{task_id}] Done ({elapsed:.2f}s, ~{estimated_tokens} tokens)")

    return {
        "status": "success",
        "task_id": task_id,
        "result": result,
        "tokens": estimated_tokens,
        "time": elapsed,
    }


def load_source_files(data_dir: Path, source_lang: str) -> list[dict]:
    solution_dir = data_dir / source_lang / "solutuon"
    if not solution_dir.exists():
        solution_dir = data_dir / source_lang / "solution"
    
    if not solution_dir.exists():
        raise FileNotFoundError(f"Solution directory not found: {solution_dir}")
    
    ext = get_code_extension(source_lang)
    samples = []
    
    for file_path in sorted(solution_dir.glob(f"*{ext}")):
        try:
            samples.append({
                "task_id": file_path.stem,
                "source_code": file_path.read_text(encoding="utf-8"),
                "source_file": str(file_path),
            })
        except Exception as e:
            safe_print(f"Failed to load {file_path}: {e}")
    
    return samples


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    api = api_defaults()

    parser = argparse.ArgumentParser(description="Code Translation using LLM API (OpenAI SDK)")
    parser.add_argument("--base_url", default=api["base_url"], help="API base URL")
    parser.add_argument("--api_key", default=api["api_key"], help="API key")
    parser.add_argument("--model", default=api["model"], help="Model name")
    parser.add_argument(
        "--data_dir", 
        default=str(project_root / "data" / "ClassEval_T"), 
        help="ClassEval_T data directory"
    )
    parser.add_argument("--source_lang", default="cpp", help="Source language (java, py, cpp)")
    parser.add_argument("--target_lang", default="py", help="Target language (java, py, cpp)")
    parser.add_argument("--lang_pairs", default="py-cpp,java-cpp,cpp-py,java-py", help="Language pairs to translate, comma-separated (e.g., 'java-py,cpp-py,java-cpp')")
    parser.add_argument(
        "--output_dir",
        default=None,
        help="Output directory for saving per-task text (auto-generated if not specified)",
    )
    parser.add_argument(
        "--code_output_dir",
        default=None,
        help="Output directory for saving translated code files (auto-generated if not specified)",
    )
    parser.add_argument(
        "--save_path",
        default=None,
        help="Path to save final JSONL results (auto-generated if not specified)",
    )
    parser.add_argument("--max_tokens", type=int, default=16384, help="Maximum number of tokens to generate")
    parser.add_argument("--temperature", type=float, default=0.6, help="Temperature for sampling")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p for sampling")
    parser.add_argument("--num_samples", type=int, default=-1, help="Number of samples to process (-1 for all)")
    parser.add_argument("--num_workers", type=int, default=20, help="Number of parallel workers")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between API calls in seconds")
    parser.add_argument("--max_retries", type=int, default=2, help="Max retries on failure")
    args = parser.parse_args()

    os.environ["TOKENIZERS_PARALLELISM"] = "false"

    lang_pairs = [
        tuple(part.strip() for part in pair.strip().split("-", 1))
        for pair in args.lang_pairs.split(",")
        if pair.strip()
    ] or [(args.source_lang, args.target_lang)]

    data_dir = Path(args.data_dir)
    base_output_dir = Path(args.output_dir) if args.output_dir else project_root / "data" / "derived_cot" / "rq1_traces" / "translation" / "glm5.1"
    base_code_output_dir = Path(args.code_output_dir) if args.code_output_dir else None

    unified_save_path = Path(args.save_path) if args.save_path else base_output_dir / "results.jsonl"
    unified_save_path.parent.mkdir(parents=True, exist_ok=True)
    unified_save_path.touch(exist_ok=True)

    safe_print("\n" + "=" * 80)
    safe_print(f" Code Translation - Multiple Language Pairs")
    safe_print("=" * 80)
    safe_print(f" Base URL: {args.base_url}")
    safe_print(f" Model: {args.model}")
    safe_print(f" Language Pairs: {', '.join([f'{s}->{t}' for s, t in lang_pairs])}")
    safe_print(f" Max Tokens: {args.max_tokens}")
    safe_print(f" Temperature: {args.temperature}")
    safe_print(f" Parallel Workers: {args.num_workers}")
    safe_print(f" Delay: {args.delay}s between requests")
    safe_print(f" Unified Results: {unified_save_path}")
    safe_print("=" * 80 + "\n")

    all_stats = []

    for source_lang, target_lang in lang_pairs:
        safe_print(f"\n{'=' * 80}")
        safe_print(f" Processing: {source_lang} -> {target_lang}")
        safe_print(f"{'=' * 80}")

        pair_dir = base_output_dir / f"{source_lang}_to_{target_lang}"
        output_dir = pair_dir / "txt_output"
        if base_code_output_dir is None:
            code_output_dir = pair_dir / "code_output"
        else:
            code_output_dir = base_code_output_dir / f"{source_lang}_to_{target_lang}"

        output_dir.mkdir(parents=True, exist_ok=True)
        code_output_dir.mkdir(parents=True, exist_ok=True)

        samples = load_source_files(data_dir, source_lang)
        safe_print(f" Loaded {len(samples)} source files")

        saved_task_ids = load_existing_task_ids(str(unified_save_path))
        pair_saved_ids = {tid.replace(f"{source_lang}_to_{target_lang}_", "")
                          for tid in saved_task_ids if tid.startswith(f"{source_lang}_to_{target_lang}_")}
        safe_print(f" Found {len(pair_saved_ids)} already processed")

        recovered = 0
        for sample in samples:
            tid = sample["task_id"]
            if tid not in pair_saved_ids:
                if recover_result_from_txt(tid, source_lang, target_lang, output_dir, unified_save_path):
                    recovered += 1
                    pair_saved_ids.add(tid)
        if recovered:
            safe_print(f"Recovered {recovered} from txt")

        pending_samples = [s for s in samples if s["task_id"] not in pair_saved_ids]
        if args.num_samples > 0:
            pending_samples = pending_samples[:args.num_samples]

        if not pending_samples:
            safe_print(" No pending tasks for this pair\n")
            continue

        safe_print(f" Processing {len(pending_samples)} tasks\n")

        args.source_lang = source_lang
        args.target_lang = target_lang

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
                    append_result_to_file(result_data["result"], str(unified_save_path))
                else:
                    failed_count += 1

        all_stats.append({
            "pair": f"{source_lang}->{target_lang}",
            "total": len(pending_samples),
            "success": success_count,
            "failed": failed_count,
            "tokens": total_tokens,
        })

    safe_print(f"\n{'=' * 80}")
    safe_print(" Overall Translation Stats")
    safe_print(f"{'=' * 80}")
    for stat in all_stats:
        safe_print(f" {stat['pair']}: {stat['success']}/{stat['total']} success, {stat['tokens']} tokens")
    safe_print(f" Unified Results: {unified_save_path}")
    safe_print(f"{'=' * 80}")


if __name__ == "__main__":
    main()
