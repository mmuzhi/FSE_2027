#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import threading
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import api_defaults, append_result_to_file, load_existing_task_ids, safe_print

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

TASK_OUTPUT_DIRS = {
    "generation": "Generate_COT",
    "execution": "Execution_COT",
    "debug": "Debug_COT",
    "translation": "Translation_COT",
}
EXTRA_BODY = {"chat_template_kwargs": {"enable_thinking": True, "clear_thinking": False}}


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
                    safe_print(f"Rate limit reached ({len(self.request_times)}/{self.limit_count} in {self.window_minutes}m), waiting {wait_seconds:.1f}s...")
                    time.sleep(wait_seconds + 0.1)

                    now = datetime.now()
                    threshold_time = now - self.window_delta
                    while self.request_times and self.request_times[0] < threshold_time:
                        self.request_times.popleft()
            
            self.request_times.append(now)
            safe_print(f"ending request (window usage: {len(self.request_times)}/{self.limit_count})")



def load_prompt(prompt_file: Path) -> str:
    return prompt_file.read_text(encoding="utf-8").strip()

def clean_json_response(response_text: str) -> str:
    text = response_text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    start_idx = text.find('[')
    end_idx = text.rfind(']')
    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"No valid JSON array found. Text starts with: {text[:200]}")
    if start_idx >= end_idx:
        raise ValueError(f"Invalid JSON array boundaries: start={start_idx}, end={end_idx}")
    return text[start_idx:end_idx+1]

def validate_steps(steps: list) -> None:
    if not isinstance(steps, list) or len(steps) == 0:
        raise ValueError("Response is not a valid JSON array")

    valid_categories = {"PU", "SD", "IP", "CC", "VV", "KR", "MR", "AUX"}
    for i, step in enumerate(steps):
        if not isinstance(step, dict):
            raise ValueError(f"Step {i} is not an object")
        for field in ["step_id", "category", "content"]:
            if field not in step:
                raise ValueError(f"Step {i} missing required field: {field}")
        
        if step["category"] not in valid_categories:
            raise ValueError(f"Step {i} has invalid category: {step['category']}")
        if not isinstance(step["content"], str):
            raise ValueError(f"Step {i} 'content' must be string")

class COTSegmenter:
    def __init__(self, base_url: str, api_key: str, model: str, prompt_template: str,
                 temperature: float = 0.01, max_tokens: int = 8192,
                 top_p: float = 0.95, max_retries: int = 3,
                 use_stream: bool = True,
                 watched_task_id: str | None = None,
                 watch_enabled: bool = True,
                 rate_limiter: SlidingWindowLimiter | None = None):
        from openai import OpenAI

        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.prompt_template = prompt_template
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.max_retries = max_retries
        self.use_stream = use_stream
        self.watched_task_id = watched_task_id
        self.watch_enabled = watch_enabled
        self.rate_limiter = rate_limiter

    def _read_stream_safely(self, stream, is_watched: bool) -> str:
        parts = []
        if is_watched:
            safe_print(f"\n===== [WATCH:{self.watched_task_id}] Streaming begin =====")

        for chunk in stream:
            if not getattr(chunk, "choices", None):
                continue
            delta = getattr(chunk.choices[0], "delta", None)
            if delta is None:
                continue

            reasoning = getattr(delta, "reasoning_content", None)
            if reasoning and is_watched:
                safe_print(reasoning, end="", flush=True)

            content = getattr(delta, "content", None)
            if content:
                parts.append(content)
                if is_watched:
                    safe_print(content, end="", flush=True)

        full_content = ''.join(parts).strip()
        if is_watched:
            safe_print(f"\n===== [WATCH:{self.watched_task_id}] Streaming end =====\n")
        return full_content

    def segment_cot(self, cot_content: str, task_id: str = "unknown") -> dict[str, object]:
        prompt = self.prompt_template.format(cot_content=cot_content)
        
        for attempt in range(self.max_retries):
            try:
                if self.rate_limiter:
                    self.rate_limiter.wait_if_needed()
                
                if self.use_stream:
                    stream = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{'role': 'user', 'content': prompt}],
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        top_p=self.top_p,
                        extra_body=EXTRA_BODY,
                        stream=True
                    )
                    is_watched = self.watch_enabled and (self.watched_task_id is not None) and (task_id == self.watched_task_id)
                    full_content = self._read_stream_safely(stream, is_watched)
                else:
                    resp = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{'role': 'user', 'content': prompt}],
                        temperature=self.temperature,
                        max_tokens=self.max_tokens,
                        top_p=self.top_p,
                        extra_body=EXTRA_BODY,
                        stream=False
                    )
                    full_content = resp.choices[0].message.content if resp and resp.choices else ""

                if not full_content:
                    raise RuntimeError("Empty response from API")
                    
                cleaned_text = clean_json_response(full_content)
                steps = json.loads(cleaned_text)
                validate_steps(steps)

                return {
                    "success": True,
                    "steps": steps,
                    "num_steps": len(steps)
                }

            except Exception as e:
                msg = str(e)
                if "list index out of range" in msg or "choices" in msg:
                    safe_print(f"[{task_id}] Non-fatal streaming quirk, continuing… ({msg})")
                    continue

                if attempt < self.max_retries - 1:
                    safe_print(f"[{task_id}] Attempt {attempt + 1} failed: {e}")
                    time.sleep(2 ** attempt)
                    continue

                return {"success": False, "error": msg}

        return {"success": False, "error": "Max retries exceeded"}

def load_dataset(dataset_path: Path) -> list[dict]:
    return [json.loads(line) for line in dataset_path.read_text(encoding="utf-8").splitlines()]

def process_single_sample(segmenter: COTSegmenter, sample: dict, idx: int, processed_ids: set[str]) -> dict:
    task_id = sample.get("task_id", f"unknown_{idx}")
    if task_id in processed_ids:
        return {"status": "skipped", "task_id": task_id, "reason": "already_processed"}
    cot_content = sample.get("cot", "")
    if not cot_content.strip():
        return {"status": "skipped", "task_id": task_id, "reason": "empty_cot"}
    result = segmenter.segment_cot(cot_content, task_id=task_id)
    output_record = {
        "task_id": task_id,
        "original_cot": cot_content,
        "segmentation_result": result
    }
    status = "success" if result.get("success") else "failed"
    return {"status": status, "task_id": task_id, "result": output_record}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="COT segmentation runner with Rate Limiting")
    parser.add_argument("--task", choices=sorted(TASK_OUTPUT_DIRS), default="debug", help="RQ1 task to segment")
    parser.add_argument("--trace-model", default="glm5.1", help="Trace-source model directory, e.g., r1, qwen, glm5.1")
    parser.add_argument("--dataset-path", default=None, help="Override input results.jsonl path")
    parser.add_argument("--output-dir", default=None, help="Override output directory")
    parser.add_argument("--output-file", default=None, help="Override output segmented_results.jsonl path")
    parser.add_argument("--num", type=int, default=-1, help="Limit number of new COT tasks to process")
    parser.add_argument("--rpm", type=int, default=30, help="Requests Count Limit (in the window)")
    parser.add_argument("--window", type=int, default=1, help="Time window in minutes (e.g. 5 means limit applies to 5 mins)")
    parser.add_argument("--prompt-file", default="segmentation_prompt.txt", help="Path to prompt file")
    parser.add_argument("--max-tokens", type=int, default=51200, help="Response max_tokens")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming")
    parser.add_argument("--no-watch", action="store_true", help="Do not live-print the first task's output")
    return parser.parse_args()


def default_dataset_path(project_root: Path, task: str, trace_model: str) -> Path:
    base = project_root / "data" / "derived_cot" / "rq1_traces" / task / trace_model
    direct_path = base / "results.jsonl"
    if direct_path.exists() or task != "generation":
        return direct_path
    return base / "v4_v6" / "results.jsonl"


def main():
    args = parse_args()

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    prompt_file = script_dir / args.prompt_file
    prompt_template = load_prompt(prompt_file)

    api = api_defaults()
    base_url = api["base_url"]
    api_key = api["api_key"]
    model = api["model"]
    if not api_key:
        raise ValueError("Missing API key. Set API_KEY / <ALIAS>_API_KEY in .env.")

    dataset_path = Path(args.dataset_path) if args.dataset_path else default_dataset_path(
        project_root, args.task, args.trace_model
    )
    output_dir = Path(args.output_dir) if args.output_dir else (
        project_root / "data" / "derived_cot" / "rq1_segmented" / TASK_OUTPUT_DIRS[args.task] / args.trace_model
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = Path(args.output_file) if args.output_file else output_dir / "segmented_results.jsonl"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Input results.jsonl not found: {dataset_path}")

    processed_ids = load_existing_task_ids(str(output_file))
    dataset = load_dataset(dataset_path)
    dataset = [s for i, s in enumerate(dataset) if s.get("task_id", f"unknown_{i}") not in processed_ids]
    if args.num:
        dataset = dataset[:args.num]
    if not dataset:
        print("No pending samples. Exit.")
        return
    watched_task_id = dataset[0].get("task_id", "unknown_0")

    limiter = SlidingWindowLimiter(limit_count=args.rpm, window_minutes=args.window)
    print(f"Input: {dataset_path}")
    print(f"Output: {output_file}")
    print(f"Trace model: {args.trace_model}")
    print(f"Segmentation API model: {model}")
    print(f"Rate Limiter initialized: {args.rpm} requests / {args.window} minutes")

    segmenter = COTSegmenter(
        base_url=base_url,
        api_key=api_key,
        model=model,
        prompt_template=prompt_template,
        temperature=0.01,
        max_tokens=args.max_tokens,
        top_p=0.95,
        max_retries=1,
        use_stream=not args.no_stream,
        watched_task_id=watched_task_id,
        watch_enabled=not args.no_watch,
        rate_limiter=limiter
    )

    success_count = failed_count = 0

    max_workers = min(args.rpm, 50) 
    print(f"Thread pool size: {max_workers}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_single_sample, segmenter, sample, idx, processed_ids)
            for idx, sample in enumerate(dataset)
        ]

        for future in as_completed(futures):
            result_data = future.result()

            if 'result' in result_data:
                append_result_to_file(result_data['result'], str(output_file))

            if result_data['status'] == 'success':
                success_count += 1
            elif result_data['status'] == 'failed':
                failed_count += 1

    print(f"\nDone. Success: {success_count}, Failed: {failed_count}")

if __name__ == "__main__":
    main()
