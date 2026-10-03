"""RQ2 LLM-as-a-Judge runner."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
from utils import (  # noqa: E402
    append_result_to_file,
    api_defaults,
    call_api_stream,
    consolidate_jsonl,
    load_existing_results,
    safe_print,
)

PROMPT_TEMPLATE_PATH = Path(__file__).parent / "judge_prompt.txt"
TASK_DEFAULTS = {
    "generation": ("r1", PROJECT_ROOT / "data" / "derived_cot" / "rq1_traces" / "generation" / "r1" / "v4_v6" / "results.jsonl", 2),
    "execution": ("r1", PROJECT_ROOT / "data" / "derived_cot" / "rq1_traces" / "execution" / "r1" / "results.jsonl", 2),
    "debug": ("qwen", PROJECT_ROOT / "data" / "derived_cot" / "rq1_traces" / "debug" / "qwen" / "results.jsonl", 2),
    "translation": ("r1", PROJECT_ROOT / "data" / "derived_cot" / "rq1_traces" / "translation" / "r1" / "results.jsonl", 10),
}

_rpm_limiter = None
def judge_model_slug(model_name: str) -> str:
    name = (model_name or "model").split("/")[-1].lower()
    if "glm" in name:
        return name.replace("-", "")
    if "deepseek" in name and "v3" in name:
        return "deepseekv3.2"
    return re.sub(r"[^a-z0-9._-]+", "-", name).strip("-") or "model"





class SlidingWindowLimiter:
    def __init__(self, limit_count: int, window_minutes: int = 1):
        self.limit_count = limit_count
        self.window_minutes = window_minutes
        self.window_delta = timedelta(minutes=window_minutes)
        self.request_times = deque()
        self.lock = threading.Lock()
    
    def wait_if_needed(self):
        with self.lock:
            now = datetime.now()
            threshold_time = now - self.window_delta
            
            while self.request_times and self.request_times[0] < threshold_time:
                self.request_times.popleft()
            
            if len(self.request_times) >= self.limit_count:
                oldest_request = self.request_times[0]
                wait_until = oldest_request + self.window_delta
                wait_seconds = (wait_until - now).total_seconds()
                
                if wait_seconds > 0:
                    safe_print(f"RPM limit reached ({len(self.request_times)}/{self.limit_count}), waiting {wait_seconds:.1f}s...")
                    time.sleep(wait_seconds + 0.1)
                    
                    now = datetime.now()
                    threshold_time = now - self.window_delta
                    while self.request_times and self.request_times[0] < threshold_time:
                        self.request_times.popleft()
            
            self.request_times.append(now)


def set_rpm_limit(rpm: int, window_minutes: int = 1):
    global _rpm_limiter
    _rpm_limiter = SlidingWindowLimiter(rpm, window_minutes) if rpm > 0 else None


def load_prompt_template() -> str:
    if PROMPT_TEMPLATE_PATH.exists():
        return PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Prompt template not found: {PROMPT_TEMPLATE_PATH}")


def build_judge_prompt(
    task_description: str,
    cot_content: str,
) -> str:
    template = load_prompt_template()
    return template.replace("{task_description}", task_description).replace("{cot_content}", cot_content)


def parse_judge_response(response_text: str) -> dict:
    text = response_text.strip()

    start_idx = text.find('{')
    end_idx = text.rfind('}')
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = text[start_idx:end_idx + 1]
        try:
            result = json.loads(json_str)
            label = result.get("label", "").strip()
            confidence = abs(float(result.get("confidence", 0.5)))
            reason = result.get("reason", "").strip()

            if label.lower() in ["valid", "correct"]:
                label = "Valid"
            elif label.lower() in ["invalid", "incorrect"]:
                label = "Invalid"
            else:
                label = "Invalid"

            return {
                "label": label,
                "confidence": min(max(confidence, 0.0), 1.0),
                "reason": reason,
                "parse_success": True,
            }
        except (json.JSONDecodeError, ValueError):
            pass

    text_lower = text.lower()
    if "valid" in text_lower and "invalid" not in text_lower:
        return {"label": "Valid", "confidence": 0.5, "reason": "", "parse_success": False}
    if "invalid" in text_lower:
        return {"label": "Invalid", "confidence": 0.5, "reason": "", "parse_success": False}

    return {"label": "Invalid", "confidence": 0.0, "reason": "", "parse_success": False}


def judge_single_cot(
    task_description: str,
    cot_content: str,
    api_key: str,
    base_url: str,
    model_name: str,
    max_tokens: int = 512,
    temperature: float = 0.5,
    task_id: str = "unknown",
) -> dict:
    prompt = build_judge_prompt(task_description, cot_content)
    
    reasoning_content, answer_text, success, error_msg = call_api_stream(
        prompt=prompt,
        api_key=api_key,
        base_url=base_url,
        model_name=model_name,
        max_tokens=max_tokens,
        temperature=temperature,
        task_id=task_id,
        before_request=_rpm_limiter.wait_if_needed if _rpm_limiter else None,
    )
    
    if not success:
        return {
            "label": "Invalid",
            "confidence": 0.0,
            "raw_response": "",
            "parse_success": False,
            "task_id": task_id,
            "success": False,
            "error": error_msg,
            "prompt": prompt,
            "reasoning": "",
        }
    
    raw_response = answer_text or reasoning_content
    result = parse_judge_response(raw_response)
    result["raw_response"] = raw_response
    result["task_id"] = task_id
    result["success"] = True
    result["prompt"] = prompt
    result["reasoning"] = reasoning_content
    return result


def aggregate_votes(results: list[dict]) -> dict:
    vote_counts = {"Valid": 0, "Invalid": 0}
    total_confidence = 0.0
    
    for r in results:
        label = r.get("label", "Invalid")
        vote_counts[label] = vote_counts.get(label, 0) + 1
        total_confidence += r.get("confidence", 0.0)
    
    final_label = max(vote_counts, key=vote_counts.get)
    consensus = vote_counts[final_label] / len(results) if results else 0.0
    avg_confidence = total_confidence / len(results) if results else 0.0
    
    return {
        "final_label": final_label,
        "vote_counts": vote_counts,
        "consensus": consensus,
        "avg_confidence": avg_confidence,
    }


def run_judge_batch(
    cot_results: dict,
    existing_results: dict,
    build_task_description_fn,
    get_cot_content_fn,
    api_key: str,
    base_url: str,
    model_name: str,
    num_samples: int = 3,
    max_tokens: int = 512,
    temperature: float = 0.5,
    rpm: int = 20,
    num_tasks: int = -1,
    save_callback=None,
    debug_dir: str = None,
    debug_count: int = 3,
) -> dict:
    debug_saved_count = 0
    if debug_dir:
        debug_path = Path(debug_dir)
        debug_path.mkdir(parents=True, exist_ok=True)
        safe_print(f"Debug output enabled: will save first {debug_count} samples to {debug_dir}")
    
    jobs = []
    task_existing_samples = {}
    task_expected_samples = {}
    
    for task_id, cot_data in cot_results.items():
        cot_content = get_cot_content_fn(cot_data)
        if not cot_content:
            continue
            
        existing_samples = []
        if task_id in existing_results:
            prev_result = existing_results[task_id]
            existing_samples = [
                s for s in prev_result.get('samples', []) 
                if s.get('parse_success', False)
            ]
        
        task_existing_samples[task_id] = existing_samples
        current_count = len(existing_samples)
        needed = num_samples - current_count
        
        if needed > 0:
            task_expected_samples[task_id] = needed
            for sample_idx in range(current_count + 1, num_samples + 1):
                jobs.append((task_id, sample_idx, cot_data))
    
    safe_print(f"Total API calls needed: {len(jobs)}")
    
    if num_tasks > 0:
        limited_task_ids = set()
        limited_jobs = []
        for job in jobs:
            if len(limited_task_ids) >= num_tasks and job[0] not in limited_task_ids:
                continue
            limited_task_ids.add(job[0])
            limited_jobs.append(job)
        jobs = limited_jobs
        task_expected_samples = {k: v for k, v in task_expected_samples.items() if k in limited_task_ids}
        safe_print(f"Limited to {len(limited_task_ids)} tasks, {len(jobs)} API calls")
    
    if not jobs:
        safe_print("No jobs to process")
        return {}
    
    def run_single_sample(job):
        task_id, sample_idx, cot_data = job
        task_description = build_task_description_fn(cot_data)
        cot_content = get_cot_content_fn(cot_data)
        
        result = judge_single_cot(
            task_description=task_description,
            cot_content=cot_content,
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            max_tokens=max_tokens,
            temperature=temperature,
            task_id=f"{task_id}_s{sample_idx}",
        )
        result["sample_idx"] = sample_idx
        return (task_id, result)
    
    task_new_samples = {}
    final_results = {}
    completed_tasks = set()
    results_lock = threading.Lock()
    
    with ThreadPoolExecutor(max_workers=rpm) as executor:
        futures = {executor.submit(run_single_sample, job): job for job in jobs}
        for future in as_completed(futures):
            try:
                task_id, sample_result = future.result()

                with results_lock:
                    task_new_samples.setdefault(task_id, []).append(sample_result)

                    if debug_dir and debug_saved_count < debug_count:
                        debug_saved_count += 1
                        sample_idx = sample_result.get("sample_idx", 1)
                        debug_file = debug_path / f"{task_id}_s{sample_idx}.txt"
                        try:
                            debug_file.write_text(
                                "=== PROMPT ===\n{prompt}\n\n"
                                "=== REASONING ===\n<think>\n{reasoning}\n</think>\n\n"
                                "=== RAW RESPONSE ===\n{raw_response}\n\n"
                                "=== PARSED RESULT ===\n"
                                "Label: {label}\n"
                                "Confidence: {confidence}\n"
                                "Reason: {reason}\n".format(
                                    prompt=sample_result.get("prompt", ""),
                                    reasoning=sample_result.get("reasoning", ""),
                                    raw_response=sample_result.get("raw_response", ""),
                                    label=sample_result.get("label", ""),
                                    confidence=sample_result.get("confidence", 0),
                                    reason=sample_result.get("reason", ""),
                                ),
                                encoding="utf-8",
                            )
                            safe_print(f"[Debug] Saved {debug_file}")
                        except Exception as e:
                            safe_print(f"[Debug] Failed to save {debug_file}: {e}")

                    expected = task_expected_samples.get(task_id, 0)
                    if len(task_new_samples[task_id]) >= expected and task_id not in completed_tasks:
                        completed_tasks.add(task_id)

                        all_samples = task_existing_samples.get(task_id, []) + task_new_samples[task_id]
                        aggregated = aggregate_votes(all_samples)
                        task_result = {
                            'task_id': task_id,
                            'samples': [{k: v for k, v in sample.items() if k != 'prompt'} for sample in all_samples],
                            'final_label': aggregated['final_label'],
                            'vote_counts': aggregated['vote_counts'],
                            'consensus': aggregated['consensus'],
                        }
                        final_results[task_id] = task_result

                        if save_callback:
                            save_callback(task_result)

            except Exception as e:
                job = futures[future]
                safe_print(f"[{job[0]}_s{job[1]}] Error: {e}")
    
    return final_results


def load_cot_results(path: Path) -> dict:
    results = {}
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            if not raw.strip():
                continue
            data = json.loads(raw)
            task_id = data.get("task_id")
            if task_id:
                results[task_id] = data
    return results


def get_cot_content(cot_data: dict) -> str:
    return cot_data.get("cot", "")


def build_task_description(task: str, cot_data: dict, args: argparse.Namespace) -> str:
    if task == "debug":
        return f"Fix the following buggy code:\n{cot_data.get('buggy_code', '')}"
    if task == "translation":
        source_lang = cot_data.get("source_lang", args.source_lang)
        target_lang = cot_data.get("target_lang", args.target_lang)
        return f"Translate the following {source_lang} code to {target_lang}:\n{cot_data.get('source_code', '')}"
    return cot_data.get("prompt", "")


def default_cot_path(task: str, cot_model: str | None = None) -> Path:
    default_model, path, _ = TASK_DEFAULTS[task]
    if not cot_model or cot_model == default_model:
        return path
    return Path(str(path).replace(f"/{default_model}/", f"/{cot_model}/"))


def main() -> None:
    api = api_defaults()
    parser = argparse.ArgumentParser(description="Judge RQ2 CoT validity.")
    parser.add_argument("--task", choices=sorted(TASK_DEFAULTS), default="generation")
    parser.add_argument("--cot_path", default="")
    parser.add_argument("--output_dir", default="")
    parser.add_argument("--cot_model", default="")
    parser.add_argument("--source_lang", default="java")
    parser.add_argument("--target_lang", default="py")
    parser.add_argument("--base_url", default=api["base_url"])
    parser.add_argument("--api_key", default=api["api_key"])
    parser.add_argument("--model", default=api["model"])
    parser.add_argument("--num_samples", type=int, default=3)
    parser.add_argument("--max_tokens", type=int, default=51200)
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--num_tasks", type=int, default=-1)
    parser.add_argument("--rpm", type=int, default=0)
    parser.add_argument("--debug_dir", default="")
    parser.add_argument("--debug_count", type=int, default=50)
    args = parser.parse_args()

    default_model, _, default_rpm = TASK_DEFAULTS[args.task]
    args.cot_model = args.cot_model or default_model
    args.rpm = args.rpm or default_rpm
    if not args.api_key:
        raise ValueError("Missing API key. Set --api_key or API_KEY / <ALIAS>_API_KEY in .env.")
    set_rpm_limit(args.rpm)

    cot_path = Path(args.cot_path) if args.cot_path else default_cot_path(args.task, args.cot_model)
    judge_model = judge_model_slug(args.model)
    output_dir = Path(args.output_dir) if args.output_dir else PROJECT_ROOT / "data" / "derived_cot" / "rq2_judging" / args.cot_model / judge_model
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / f"{args.task}_judge_results.jsonl"
    debug_dir = Path(args.debug_dir) if args.debug_dir else output_dir / "_debug"

    print(f"Loading COT results from: {cot_path}")
    cot_results = load_cot_results(cot_path)
    print(f"Loaded {len(cot_results)} COT results")
    consolidate_jsonl(str(save_path))
    existing_results = load_existing_results(str(save_path))
    print(f"Found {len(existing_results)} existing tasks")

    results = run_judge_batch(
        cot_results=cot_results,
        existing_results=existing_results,
        build_task_description_fn=lambda item: build_task_description(args.task, item, args),
        get_cot_content_fn=get_cot_content,
        api_key=args.api_key,
        base_url=args.base_url,
        model_name=args.model,
        num_samples=args.num_samples,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        rpm=args.rpm,
        num_tasks=args.num_tasks,
        save_callback=lambda result: append_result_to_file(result, str(save_path)),
        debug_dir=str(debug_dir),
        debug_count=args.debug_count,
    )
    print(f"\nSaved {len(results)} task results to: {save_path}")
    consolidate_jsonl(str(save_path))


if __name__ == "__main__":
    main()
