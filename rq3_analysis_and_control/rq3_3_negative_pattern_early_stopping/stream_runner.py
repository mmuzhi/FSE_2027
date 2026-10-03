from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from utils import api_alias, api_defaults
from intervention_prompts import build_prefill_transition, build_user_finalizer_prompt
from code_postprocess import extract_code_answer
from motif_detector import detect_motifs
from policy import PolicyEngine, load_policy_config
from schema import normalize_task_name
from state_model import RuleStateModel
from state_tracker import StateTracker


DEFAULT_EXTRA_BODY = '{"chat_template_kwargs":{"thinking":true}}'
TASK_FINAL_MAX_TOKENS = {
    "execution": 128,
    "generation": 1024,
    "debug": 1024,
    "translation": 1536,
}


def sanitize_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())
    return slug.strip("._-") or "unknown"


def resolve_model_runtime(args: argparse.Namespace) -> None:
    model_from_cli = bool(args.model)
    runtime = api_defaults()
    if not args.model:
        args.model = runtime["model"]
    if not args.base_url:
        args.base_url = runtime["base_url"]
    if not args.api_key:
        args.api_key = runtime["api_key"]
    args.model_alias = sanitize_slug(api_alias() if not model_from_cli else (args.model or "model"))


def iter_json_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Input data not found: {path}")
    if path.suffix.lower() == ".json":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            payload = payload["data"]
        if not isinstance(payload, list):
            raise ValueError(f"JSON data must be a list or contain a data list: {path}")
        return [item for item in payload if isinstance(item, dict)]

    records: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON at {path}:{line_no}") from exc
        if isinstance(item, dict):
            records.append(item)
    return records


def load_existing_task_ids(path: Path) -> set[str]:
    task_ids: set[str] = set()
    if not path.exists():
        return task_ids
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            item = json.loads(raw)
        except json.JSONDecodeError:
            continue
        task_id = item.get("task_id")
        if task_id:
            task_ids.add(str(task_id))
    return task_ids


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def stringify_field(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def get_code_extension(lang: str) -> str:
    return {
        "java": ".java",
        "cpp": ".cpp",
        "c++": ".cpp",
        "py": ".py",
        "python": ".py",
    }.get(lang.lower(), f".{lang}")


def default_data_path(task: str) -> Path:
    if task == "generation":
        candidates = [
            ROOT / "data" / "LCB" / "v4_v6.jsonl",
            ROOT / "data" / "derived_cot" / "rq1_traces" / "generation" / "qwen" / "v4_v6" / "results.jsonl",
            ROOT / "data" / "derived_cot" / "rq1_traces" / "generation" / "qwen" / "v1_v3" / "results.jsonl",
            ROOT / "data" / "derived_cot" / "rq1_traces" / "generation" / "r1" / "v4_v6" / "results.jsonl",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return candidates[0]
    return {
        "execution": ROOT / "data" / "CodeSense" / "input_output_dataset.jsonl",
        "debug": ROOT / "data" / "DebugBench" / "python_samples.json",
    }.get(task, ROOT / "data" / "ClassEval_T")


def load_translation_samples(data_dir: Path, source_lang: str) -> list[dict[str, Any]]:
    solution_dir = data_dir / source_lang / "solutuon"
    if not solution_dir.exists():
        solution_dir = data_dir / source_lang / "solution"
    if not solution_dir.exists():
        raise FileNotFoundError(f"Translation source directory not found: {solution_dir}")
    ext = get_code_extension(source_lang)
    return [
        {
            "task_id": file_path.stem,
            "source_code": file_path.read_text(encoding="utf-8"),
            "source_file": str(file_path),
        }
        for file_path in sorted(solution_dir.glob(f"*{ext}"))
    ]


def normalize_loaded_sample(sample: dict[str, Any], task: str, idx: int, args: argparse.Namespace) -> dict[str, Any]:
    item = dict(sample)
    if task == "generation":
        item.setdefault("task_id", item.get("question_id", f"sample-{idx}"))
    elif task == "execution":
        item.setdefault("task_id", f"sample-{idx}")
    elif task == "debug":
        item.setdefault("task_id", item.get("sample_id", f"sample-{idx}"))
        item.setdefault("buggy_code", item.get("code", ""))
    elif task == "translation":
        item.setdefault("task_id", f"sample-{idx}")
        item.setdefault("source_lang", args.source_lang)
        item.setdefault("target_lang", args.target_lang)
    item["task_id"] = str(item.get("task_id"))
    return item


def load_task_samples(args: argparse.Namespace) -> list[dict[str, Any]]:
    task = normalize_task_name(args.task)
    data_path = Path(args.data) if args.data else default_data_path(task)
    if task == "translation" and data_path.is_dir():
        raw_samples = load_translation_samples(data_path, args.source_lang)
    else:
        raw_samples = iter_json_records(data_path)
    samples = [normalize_loaded_sample(sample, task, idx, args) for idx, sample in enumerate(raw_samples)]
    if task == "translation":
        prefix = f"{args.source_lang}_to_{args.target_lang}_"
        for sample in samples:
            if not str(sample["task_id"]).startswith(prefix):
                sample["original_task_id"] = sample["task_id"]
                sample["task_id"] = f"{prefix}{sample['task_id']}"
    return samples


def parse_lang_pairs(raw: str, source_lang: str, target_lang: str) -> list[tuple[str, str]]:
    if not raw:
        return [(source_lang, target_lang)]
    pairs: list[tuple[str, str]] = []
    for text in (item.strip() for item in raw.split(",") if item.strip()):
        src, sep, tgt = text.partition("-")
        if not sep:
            raise ValueError(f"Invalid language pair '{text}'. Expected format like cpp-py.")
        pairs.append((src.strip(), tgt.strip()))
    return pairs or [(source_lang, target_lang)]


def language_display_name(lang: str) -> str:
    return {
        "java": "Java",
        "cpp": "C++",
        "c++": "C++",
        "py": "Python",
        "python": "Python",
    }.get(lang.lower(), lang)


def build_rq1_generation_prompt(question_content: str, starter_code: str = "") -> str:
    return (
        "You will be given a competitive programming problem.\n"
        f"{question_content}\n\n"
        "You will use the following starter code to write the solution to the problem and enclose your code within delimiters.\n"
        f"```python\n{starter_code}\n```"
    )


def parse_generation_fields_from_prompt(prompt: str) -> tuple[str, str]:
    if not prompt:
        return "", ""
    text = prompt.strip()
    starter_code = ""
    code_match = re.search(r"```python\s*\n([\s\S]*?)```", text, re.IGNORECASE)
    if code_match:
        starter_code = code_match.group(1).strip()
        text = text[: code_match.start()].rstrip()
    marker = "You will use the following starter code to write the solution to the problem and enclose your code within delimiters."
    if marker in text:
        text = text.split(marker, 1)[0].rstrip()
    prefix = "You will be given a competitive programming problem."
    if text.startswith(prefix):
        text = text[len(prefix) :].strip()
    return text, starter_code


def build_prompt_for_sample(sample: dict[str, Any], args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    task = normalize_task_name(args.task)
    meta = {
        "task": task,
        "prompt_source": "rq1_default",
        "source_script": f"rq1_general_patterns/{task}_cot.py",
    }
    if task == "generation":
        question_content = sample.get("question_content", "")
        starter_code = sample.get("starter_code", "")
        if not question_content and sample.get("prompt"):
            question_content, starter_code = parse_generation_fields_from_prompt(str(sample["prompt"]))
            meta["prompt_source"] = "rq1_default_rebuilt_from_sample_prompt"
        return build_rq1_generation_prompt(str(question_content), str(starter_code)), meta
    if task == "execution":
        language = str(sample.get("language", "python"))
        code = str(sample.get("code", ""))
        input_text = stringify_field(sample.get("input", ""))
        return (
            f"Here's some {language} code and the inputs passed into it.\n"
            "What output do you expect from it?\n"
            f"Code: {language}\n{code}\n"
            f"Inputs: {input_text}\n"
            "Answer using <ans></ans> tags",
            meta,
        )
    if task == "debug":
        return (
            "Observe the following faulty python code. It contains one or more bugs. "
            "Fix the code and output only the fixed code.\n\n"
            f"```python\n{str(sample.get('buggy_code', ''))}\n```",
            meta,
        )
    if task == "translation":
        source_lang = str(sample.get("source_lang", args.source_lang))
        target_lang = str(sample.get("target_lang", args.target_lang))
        source_name = language_display_name(source_lang)
        target_name = language_display_name(target_lang)
        source_code = str(sample.get("source_code", ""))
        return (
            f"You are an expert programmer. Translate the following {source_name} code to {target_name}.\n"
            f"- Keep behavior identical (inputs/outputs, side effects, edge cases, exceptions).\n"
            f"- Use idiomatic {target_name} only when it doesn't change behavior.\n\n"
            f"```{source_lang}\n{source_code}\n```",
            meta,
        )
    raise ValueError(f"Unsupported task: {task}")


def answer_repair_metadata(answer_text: str, parsed_answer: str, task: str) -> dict[str, bool]:
    raw = answer_text or ""
    open_code_fence = "```" in raw and raw.count("```") % 2 == 1
    missing_main_call = bool(
        task in {"generation", "debug"}
        and re.search(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:\s*\Z", raw.strip())
        and parsed_answer.rstrip().endswith("main()")
    )
    return {
        "answer_postprocessed": bool(open_code_fence or missing_main_call),
        "answer_open_fence_repaired": open_code_fence,
        "answer_main_guard_repaired": missing_main_call,
    }


REASONING_MARKER_RE = re.compile(
    r"\b("
    r"but wait|let me|let's|we need|i need|the idea|the approach|"
    r"first,|now,|however,|actually,|alternatively|observe that|"
    r"we can|we should|we will|proof|complexity"
    r")\b",
    re.IGNORECASE,
)


def answer_reasoning_metadata(parsed_answer: str, task: str) -> dict[str, bool]:
    if task not in {"generation", "debug", "translation"}:
        return {"answer_contains_reasoning_markers": False}
    return {"answer_contains_reasoning_markers": bool(REASONING_MARKER_RE.search(parsed_answer or ""))}


def extract_answer(answer_text: str, task: str, target_lang: str = "py") -> str:
    if not answer_text:
        return ""
    if task == "execution":
        match = re.search(r"<ans>(.*?)</ans>", answer_text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else answer_text.strip()
    if task in {"generation", "debug"}:
        return extract_code_answer(answer_text, "py")
    if task == "translation":
        return extract_code_answer(answer_text, target_lang)
    return answer_text.strip()


def parse_extra_body(raw: str) -> dict[str, Any] | None:
    if not raw or raw.strip().lower() in {"none", "null", "{}"}:
        return None
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("--extra-body-json must decode to a JSON object")
    return payload


def chat_kwargs(args: argparse.Namespace, *, messages: list[dict[str, Any]], stream: bool, max_tokens: int, temperature: float) -> dict[str, Any]:
    kwargs: dict[str, Any] = {
        "model": args.model,
        "messages": messages,
        "stream": stream,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": args.top_p,
    }
    extra_body = parse_extra_body(args.extra_body_json)
    if extra_body:
        kwargs["extra_body"] = extra_body
    if args.request_timeout > 0:
        kwargs["timeout"] = args.request_timeout
    return kwargs


def is_deepseek_runtime(args: argparse.Namespace) -> bool:
    model_name = (getattr(args, "model", "") or "").lower()
    alias = (getattr(args, "model_alias", "") or "").lower()
    base_url = (getattr(args, "base_url", "") or "").lower()
    return alias == "deepseek" or "deepseek" in model_name or "api.deepseek.com" in base_url


def deepseek_beta_base_url(base_url: str) -> str:
    clean = (base_url or "https://api.siliconflow.cn/v1").rstrip("/")
    if "siliconflow" in clean:
        return clean
    if clean.endswith("/beta"):
        return clean
    if clean.endswith("/v1"):
        clean = clean[:-3]
    return clean + "/beta"


def build_deepseek_prefill_content(task: str) -> str:
    return {"execution": "<ans>", "generation": "```python\n", "debug": "```python\n", "translation": "```\n"}.get(task, "")


def merge_deepseek_prefill_answer(prefix: str, answer_text: str) -> str:
    if not prefix:
        return answer_text
    if not answer_text:
        return prefix
    return answer_text if answer_text.startswith(prefix) else prefix + answer_text


def finalizer_no_thinking_extra_body(args: argparse.Namespace) -> dict[str, Any]:
    """Ask chat-template based APIs to disable thinking during answer completion."""
    extra_body = parse_extra_body(args.extra_body_json) or {}
    chat_template_kwargs = dict(extra_body.get("chat_template_kwargs") or {})
    chat_template_kwargs["thinking"] = False
    chat_template_kwargs["enable_thinking"] = False
    extra_body["chat_template_kwargs"] = chat_template_kwargs
    return extra_body


def provider_rejects_assistant_prefill(args: argparse.Namespace) -> bool:
    """DeepSeek reasoner/thinking endpoints reject assistant content without reasoning metadata."""
    model_name = (getattr(args, "model", "") or "").lower()
    alias = (getattr(args, "model_alias", "") or "").lower()
    return "deepseek-reasoner" in model_name or (alias == "deepseek" and "reasoner" in model_name)


def use_user_finalizer_mode(args: argparse.Namespace) -> bool:
    mode = getattr(args, "finalizer_mode", "auto")
    if mode == "user":
        return True
    if mode == "assistant":
        return False
    return provider_rejects_assistant_prefill(args)


def close_stream(stream: Any) -> None:
    close = getattr(stream, "close", None)
    if callable(close):
        try:
            close()
        except Exception:
            pass


def estimate_token_progress(tracker: StateTracker, max_tokens: int) -> float:
    """Estimate stream progress ratio from accumulated text vs max_tokens."""
    if max_tokens <= 0:
        return 1.0
    estimated_tokens = estimate_reasoning_chars(tracker) // 4
    return min(estimated_tokens / max(max_tokens, 1), 1.0)


def estimate_reasoning_chars(tracker: StateTracker) -> int:
    total_chars = sum(len(seg.get("segment_text", "")) for seg in tracker.closed_segments)
    for unit in tracker.active_units:
        total_chars += len(unit.get("unit_text", ""))
    return total_chars


def _tail_repetition_metrics(text: str, max_unit_chars: int) -> dict[str, Any]:
    best = {"unit": "", "count": 0, "chars": 0}
    tail = text[-max(max_unit_chars * 80, 1) :]
    for unit_len in range(1, max(max_unit_chars, 1) + 1):
        if len(tail) < unit_len * 2:
            continue
        unit = tail[-unit_len:]
        count = 0
        pos = len(tail)
        while pos >= unit_len and tail[pos - unit_len : pos] == unit:
            count += 1
            pos -= unit_len
        chars = count * unit_len
        if chars > best["chars"]:
            best = {"unit": unit, "count": count, "chars": chars}
    return best


def detect_repetition_trigger(text: str, config: dict[str, Any], segment_id: int) -> dict[str, Any] | None:
    if not bool(config.get("repetition_trigger_enabled", True)):
        return None
    if segment_id < int(config.get("repetition_min_segment_id", 0)):
        return None

    min_chars = int(config.get("repetition_min_chars", 600))
    window_chars = int(config.get("repetition_window_chars", 1200))
    if len(text) < min_chars:
        return None

    window = re.sub(r"\s+", " ", text[-window_chars:]).strip()
    ngram_size = int(config.get("repetition_ngram_size", 6))
    if len(window) < max(min_chars, ngram_size * 4):
        return None

    ngrams = [window[i : i + ngram_size] for i in range(0, len(window) - ngram_size + 1)]
    unique_ratio = len(set(ngrams)) / max(len(ngrams), 1)
    repeated_ngram_ratio = 1.0 - unique_ratio
    ngram_threshold = float(config.get("repetition_ngram_ratio_threshold", 0.72))

    tail_metrics = _tail_repetition_metrics(
        window,
        int(config.get("repetition_tail_unit_max_chars", 24)),
    )
    tail_repeats = int(tail_metrics["count"])
    tail_chars = int(tail_metrics["chars"])
    tail_repeat_threshold = int(config.get("repetition_tail_min_repeats", 24))
    tail_chars_threshold = int(config.get("repetition_tail_chars_threshold", 160))

    if repeated_ngram_ratio < ngram_threshold and not (
        tail_repeats >= tail_repeat_threshold and tail_chars >= tail_chars_threshold
    ):
        return None

    return {
        "segment_id": segment_id,
        "coarse_state": "Degenerate",
        "fine_state": "REP",
        "avg_novelty": 0.0,
        "num_units": 0,
        "prefix_segment_ratio": 1.0,
        "loop_score": 1.0,
        "closure_score": 0.0,
        "healthy_loop_bonus": 0.0,
        "has_no_answer_closure_evidence": False,
        "action": "stop-and-finalize",
        "would_trigger": True,
        "trigger_type": "repetition",
        "trigger_reason": "degenerate repeated text detected in streaming reasoning",
        "consecutive_loop_windows": 0,
        "repetition_metrics": {
            "window_chars": len(window),
            "ngram_size": ngram_size,
            "repeated_ngram_ratio": repeated_ngram_ratio,
            "tail_unit": tail_metrics["unit"][:80],
            "tail_repeat_count": tail_repeats,
            "tail_repeated_chars": tail_chars,
        },
    }


def evaluate_latest_segment(
    *,
    tracker: StateTracker,
    segment: dict[str, Any],
    task: str,
    policy_engine: PolicyEngine,
    expected_segments: int,
    max_tokens: int = 0,
) -> dict[str, Any]:
    window_state = tracker.get_window_state()
    segment_id = int(segment["segment_id"])
    prefix_ratio = 1.0
    if expected_segments > 0:
        prefix_ratio = min((segment_id + 1) / expected_segments, 1.0)
    window_state.update(
        {
            "segment_id": segment_id,
            "prefix_segment_ratio": prefix_ratio,
            "prefix_reasoning_chars": estimate_reasoning_chars(tracker),
            "token_progress": estimate_token_progress(tracker, max_tokens),
        }
    )
    motif_result = detect_motifs(window_state["fine_compressed_path"], task)
    decision = policy_engine.evaluate(window_state, motif_result)
    return {
        "segment_id": segment_id,
        "coarse_state": segment["coarse_state"],
        "fine_state": segment["fine_state"],
        "avg_novelty": segment.get("avg_novelty", 1.0),
        "num_units": segment.get("num_units", 0),
        "prefix_segment_ratio": prefix_ratio,
        "prefix_reasoning_chars": window_state["prefix_reasoning_chars"],
        "token_progress": window_state["token_progress"],
        "loop_score": decision["loop_score"],
        "closure_score": decision["closure_score"],
        "healthy_loop_bonus": decision["healthy_loop_bonus"],
        "recent_fail_motif_bonus": decision.get("recent_fail_motif_bonus", 0.0),
        "recent_healthy_motif_bonus": decision.get("recent_healthy_motif_bonus", 0.0),
        "has_no_answer_closure_evidence": decision.get("has_no_answer_closure_evidence", False),
        "action": decision["action"],
        "would_trigger": decision["would_trigger"],
        "trigger_type": decision["trigger_type"],
        "trigger_reason": decision["trigger_reason"],
        "consecutive_loop_windows": decision.get("consecutive_loop_windows", 0),
    }


def stream_with_policy(
    *,
    prompt: str,
    task: str,
    policy_config: dict[str, Any],
    args: argparse.Namespace,
) -> dict[str, Any]:
    from openai import OpenAI

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)
    last_error: str | None = None
    for attempt in range(args.max_retries):
        tracker = StateTracker(model=RuleStateModel())
        policy_engine = PolicyEngine(policy_config)
        reasoning_parts: list[str] = []
        answer_parts: list[str] = []
        segment_events: list[dict[str, Any]] = []
        trigger_event: dict[str, Any] | None = None
        start_time = time.time()
        stream = None
        try:
            stream = client.chat.completions.create(
                **chat_kwargs(
                    args,
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                    max_tokens=args.max_tokens,
                    temperature=args.temperature,
                )
            )
            for chunk in stream:
                choices = getattr(chunk, "choices", None) or []
                if not choices:
                    continue
                delta = choices[0].delta
                reasoning_delta = getattr(delta, "reasoning_content", None) or ""
                content_delta = getattr(delta, "content", None) or ""

                if reasoning_delta:
                    reasoning_parts.append(reasoning_delta)
                    repetition_event = detect_repetition_trigger(
                        "".join(reasoning_parts),
                        policy_config,
                        len(tracker.closed_segments),
                    )
                    if repetition_event:
                        trigger_event = repetition_event
                        segment_events.append(repetition_event)
                        close_stream(stream)
                        break
                    closed_segments = tracker.feed_delta(reasoning_delta)
                    for segment in closed_segments:
                        event = evaluate_latest_segment(
                            tracker=tracker,
                            segment=segment,
                            task=task,
                            policy_engine=policy_engine,
                            expected_segments=args.expected_segments,
                            max_tokens=args.max_tokens,
                        )
                        segment_events.append(event)
                        if event["would_trigger"]:
                            trigger_event = event
                            break

                if content_delta:
                    answer_parts.append(content_delta)
                    tracker.has_answer_started = True
                    if args.track_content:
                        closed_segments = tracker.feed_delta(content_delta)
                        for segment in closed_segments:
                            event = evaluate_latest_segment(
                                tracker=tracker,
                                segment=segment,
                                task=task,
                                policy_engine=policy_engine,
                                expected_segments=args.expected_segments,
                                max_tokens=args.max_tokens,
                            )
                            segment_events.append(event)
                            if event["would_trigger"]:
                                trigger_event = event
                                break

                if trigger_event:
                    close_stream(stream)
                    break

            if not trigger_event:
                tracker.flush_pending()

            elapsed = time.time() - start_time
            return {
                "success": True,
                "error": None,
                "reasoning_prefix": "".join(reasoning_parts),
                "answer_prefix": "".join(answer_parts),
                "segment_events": segment_events,
                "trigger_event": trigger_event,
                "online_stopped": trigger_event is not None,
                "stream_elapsed": elapsed,
                "attempt": attempt + 1,
            }
        except Exception as exc:
            close_stream(stream)
            last_error = f"Request exception: {exc}"
            if attempt < args.max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                break
    return {
        "success": False,
        "error": last_error or "Max retries exceeded",
        "reasoning_prefix": "",
        "answer_prefix": "",
        "segment_events": [],
        "trigger_event": None,
        "online_stopped": False,
        "stream_elapsed": 0.0,
        "attempt": args.max_retries,
    }


def call_answer_from_stopped_cot(
    *,
    original_prompt: str,
    reasoning_prefix: str,
    task: str,
    task_id: str,
    args: argparse.Namespace,
) -> dict[str, Any]:
    """Continue from the stopped CoT and emit only the final answer."""
    from openai import OpenAI

    transition = build_prefill_transition(task)
    deepseek_answer_prefix = build_deepseek_prefill_content(task)

    use_user_finalizer = use_user_finalizer_mode(args)
    use_deepseek_prefill = (not use_user_finalizer) and is_deepseek_runtime(args)
    finalizer_mode = (
        "user-finalizer"
        if use_user_finalizer
        else ("deepseek-prefix" if use_deepseek_prefill else "assistant-prefill")
    )
    finalizer_base_url = deepseek_beta_base_url(args.base_url) if use_deepseek_prefill else args.base_url
    client = OpenAI(base_url=finalizer_base_url, api_key=args.api_key)
    system_message = {
        "role": "system",
        "content": (
            "You are an answer-only finalizer. Do not write analysis, reasoning, "
            "planning, explanations, self-corrections, or comments. "
            "For code tasks, output runnable code only. If the stopped reasoning is incomplete, "
            "make the best direct implementation choice and still output code only. "
            "Never place reasoning inside code comments."
        ),
    }
    if use_user_finalizer:
        messages = [
            system_message,
            {
                "role": "user",
                "content": build_user_finalizer_prompt(
                    original_prompt=original_prompt,
                    reasoning_prefix=reasoning_prefix,
                    task=task,
                ),
            }
        ]
    else:
        messages = [
            system_message,
            {"role": "user", "content": original_prompt},
        ]
        if use_deepseek_prefill:
            messages.append(
                {
                    "role": "assistant",
                    "content": deepseek_answer_prefix,
                    "reasoning_content": reasoning_prefix + transition,
                    "prefix": True,
                }
            )
        else:
            messages.append({"role": "assistant", "content": reasoning_prefix + transition})

    last_error: str | None = None
    for attempt in range(args.max_retries):
        start_time = time.time()
        stream = None
        try:
            kwargs = chat_kwargs(
                args,
                messages=messages,
                stream=True,
                max_tokens=args.final_max_tokens,
                temperature=args.final_temperature,
            )
            if not use_deepseek_prefill:
                kwargs["extra_body"] = finalizer_no_thinking_extra_body(args)
            stream = client.chat.completions.create(**kwargs)
            reasoning_parts: list[str] = []
            answer_parts: list[str] = []
            for chunk in stream:
                if not getattr(chunk, "choices", None):
                    continue
                delta = chunk.choices[0].delta
                reasoning_delta = getattr(delta, "reasoning_content", None) or ""
                answer_delta = getattr(delta, "content", None) or ""
                if reasoning_delta:
                    reasoning_parts.append(reasoning_delta)
                if answer_delta:
                    answer_parts.append(answer_delta)
            reasoning_text = "".join(reasoning_parts)
            answer_text = "".join(answer_parts)
            if use_deepseek_prefill:
                answer_text = merge_deepseek_prefill_answer(deepseek_answer_prefix, answer_text)
            return {
                "success": True,
                "error": None,
                "reasoning": reasoning_text,
                "answer": answer_text,
                "mode": finalizer_mode,
                "elapsed": time.time() - start_time,
                "attempt": attempt + 1,
            }
        except Exception as exc:
            last_error = f"Answer completion exception for {task_id}: {exc}"
            if attempt < args.max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                break
        finally:
            if stream is not None:
                close_stream(stream)
    return {
        "success": False,
        "error": last_error or "Max retries exceeded",
        "reasoning": "",
        "answer": "",
        "mode": finalizer_mode,
        "elapsed": 0.0,
        "attempt": args.max_retries,
    }


def process_sample(
    sample: dict[str, Any],
    args: argparse.Namespace,
    policy_config: dict[str, Any],
    output_base_dir: Path,
    code_base_dir: Path | None,
) -> dict[str, Any]:
    task = normalize_task_name(args.task)
    task_id = str(sample["task_id"])
    source_lang = str(sample.get("source_lang", args.source_lang))
    target_lang = str(sample.get("target_lang", args.target_lang))
    if task == "translation":
        pair_dir_name = f"{source_lang}_to_{target_lang}"
        output_dir = output_base_dir / pair_dir_name / "txt_output"
        code_output_dir = code_base_dir / pair_dir_name / "code_output" if code_base_dir else None
    else:
        output_dir = output_base_dir
        code_output_dir = code_base_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    if code_output_dir:
        code_output_dir.mkdir(parents=True, exist_ok=True)
    prompt, prompt_meta = build_prompt_for_sample(sample, args)
    start_time = time.time()

    stream_result = stream_with_policy(
        prompt=prompt,
        task=task,
        policy_config=policy_config,
        args=args,
    )
    if not stream_result["success"]:
        return {
            "status": "failed",
            "task_id": task_id,
            "error": stream_result["error"],
            "time": time.time() - start_time,
        }

    trigger_event = stream_result["trigger_event"]
    intervention_action = None
    finalizer_result: dict[str, Any] | None = None
    raw_answer_full = stream_result["answer_prefix"]
    final_reasoning = ""

    if trigger_event:
        intervention_action = "answer-from-stopped-cot"
        finalizer_prefix = stream_result["reasoning_prefix"]
        finalizer_result = call_answer_from_stopped_cot(
            original_prompt=prompt,
            reasoning_prefix=finalizer_prefix,
            task=task,
            task_id=task_id,
            args=args,
        )
        if finalizer_result["success"]:
            raw_answer_full = finalizer_result["answer"]
            final_reasoning = finalizer_result["reasoning"]
    else:
        finalizer_result = None

    parsed_answer = extract_answer(raw_answer_full, task, target_lang=target_lang)
    repair_meta = answer_repair_metadata(raw_answer_full, parsed_answer, task)
    reasoning_answer_meta = answer_reasoning_metadata(parsed_answer, task)
    elapsed = time.time() - start_time
    estimated_stream_tokens = (len(stream_result["reasoning_prefix"]) + len(stream_result["answer_prefix"])) // 4
    finalizer_success = bool(finalizer_result and finalizer_result.get("success"))
    estimated_final_tokens = (
        (len(final_reasoning) + len(raw_answer_full)) // 4
        if finalizer_success
        else 0
    )
    estimated_total_tokens = estimated_stream_tokens + estimated_final_tokens
    cot_text = stream_result["reasoning_prefix"]

    result: dict[str, Any] = {
        "task_id": task_id,
        "prompt_source": prompt_meta["prompt_source"],
        "prompt_task": prompt_meta["task"],
        "prompt": prompt,
        "cot": cot_text,
        "finalizer_reasoning": final_reasoning,
        "answer": parsed_answer,
        "online_stopped": stream_result["online_stopped"],
        "intervention_action": intervention_action,
        "trigger_event": trigger_event,
        "segment_events_count": len(stream_result["segment_events"]),
        "stream_reasoning_chars": len(stream_result["reasoning_prefix"]),
        "stream_answer_chars": len(stream_result["answer_prefix"]),
        "final_reasoning_chars": len(final_reasoning),
        "final_answer_chars": len(raw_answer_full) if finalizer_success else 0,
        "estimated_stream_tokens": estimated_stream_tokens,
        "estimated_final_tokens": estimated_final_tokens,
        "estimated_total_tokens": estimated_total_tokens,
        "finalizer_success": finalizer_success,
        "finalizer_error": finalizer_result.get("error") if finalizer_result else None,
        "finalizer_mode": finalizer_result.get("mode") if finalizer_result else None,
        **repair_meta,
        **reasoning_answer_meta,
    }
    if task == "execution":
        result.update(
            {
                "language": str(sample.get("language", "")),
                "category": str(sample.get("category", "")),
                "code": sample.get("code", ""),
                "input": sample.get("input", ""),
                "expected_output": sample.get("output", ""),
                "raw_answer": parsed_answer,
                "raw_answer_full": raw_answer_full,
            }
        )
    elif task == "debug":
        result.pop("answer", None)
        result.update({"buggy_code": sample.get("buggy_code", ""), "fixed_code": parsed_answer, "raw_answer": raw_answer_full})
    elif task == "translation":
        result.pop("answer", None)
        result.update(
            {
                "original_task_id": sample.get("original_task_id", task_id),
                "source_lang": source_lang,
                "target_lang": target_lang,
                "source_code": sample.get("source_code", ""),
                "translated_code": parsed_answer,
                "raw_answer": raw_answer_full,
            }
        )

    write_text_artifact(output_dir / f"{sanitize_slug(task_id)}.txt", task, result, raw_answer_full)
    if code_output_dir and parsed_answer and task in {"generation", "debug", "translation"}:
        ext = get_code_extension(target_lang) if task == "translation" else ".py"
        (code_output_dir / f"{sanitize_slug(task_id)}{ext}").write_text(parsed_answer, encoding="utf-8")

    return {
        "status": "success",
        "task_id": task_id,
        "result": result,
        "tokens": estimated_total_tokens,
        "time": elapsed,
        "stopped": stream_result["online_stopped"],
    }


def write_text_artifact(path: Path, task: str, result: dict[str, Any], raw_answer_full: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if task == "generation":
        text = (
            f"=== PROMPT ===\n{result['prompt']}\n\n"
            f"=== REASONING ===\n<think>\n{result['cot']}\n</think>\n\n"
            f"=== ANSWER ===\n{raw_answer_full}"
        )
    elif task == "execution":
        text = (
            f"=== PROMPT ===\n{result['prompt']}\n\n"
            f"=== REASONING ===\n<think>\n{result['cot']}\n</think>\n\n"
            f"=== RAW ANSWER ===\n{raw_answer_full}\n\n"
            f"=== PARSED ANSWER ===\n{result['answer']}\n"
        )
    elif task == "debug":
        text = (
            f"=== BUGGY CODE ===\n{result['buggy_code']}\n\n"
            f"=== REASONING ===\n<think>\n{result['cot']}\n</think>\n\n"
            f"=== RAW ANSWER ===\n{raw_answer_full}\n\n"
            f"=== FIXED CODE ===\n{result['fixed_code']}\n"
        )
    elif task == "translation":
        text = (
            f"=== SOURCE CODE ({result['source_lang']}) ===\n{result['source_code']}\n\n"
            f"=== REASONING ===\n<think>\n{result['cot']}\n</think>\n\n"
            f"=== RAW ANSWER ===\n{raw_answer_full}\n\n"
            f"=== TRANSLATED CODE ({result['target_lang']}) ===\n{result['translated_code']}\n"
        )
    else:
        text = json.dumps(result, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")


def run(args: argparse.Namespace) -> None:
    resolve_model_runtime(args)
    task = normalize_task_name(args.task)
    args.task = task
    if args.final_max_tokens <= 0:
        args.final_max_tokens = TASK_FINAL_MAX_TOKENS.get(task, 1024)
    policy_config = load_policy_config(args.config or None, task=task)
    if task == "translation":
        original_source_lang = args.source_lang
        original_target_lang = args.target_lang
        samples = []
        for source_lang, target_lang in parse_lang_pairs(args.lang_pairs, args.source_lang, args.target_lang):
            args.source_lang = source_lang
            args.target_lang = target_lang
            pair_samples = load_task_samples(args)
            if args.num_samples > 0:
                pair_samples = pair_samples[: args.num_samples]
            samples.extend(pair_samples)
        args.source_lang = original_source_lang
        args.target_lang = original_target_lang
    else:
        samples = load_task_samples(args)
        if args.num_samples > 0:
            samples = samples[: args.num_samples]

    model_slug = sanitize_slug(args.model_alias)
    if args.output_dir:
        base_output_dir = Path(args.output_dir)
    elif task == "translation":
        base_output_dir = ROOT / "data" / "derived_cot" / "rq3_negative_pattern_early_stopping" / "output" / model_slug / "translation"
    else:
        base_output_dir = ROOT / "data" / "derived_cot" / "rq3_negative_pattern_early_stopping" / "output" / model_slug / task

    if task == "translation":
        txt_output_dir = base_output_dir
        code_output_dir = Path(args.code_output_dir) if args.code_output_dir else base_output_dir
    else:
        txt_output_dir = base_output_dir / "txt_output"
        code_output_dir = Path(args.code_output_dir) if args.code_output_dir else (
            base_output_dir / "code_output" if task in {"generation", "debug"} else None
        )
    save_path = Path(args.save_path) if args.save_path else base_output_dir / "results.jsonl"
    txt_output_dir.mkdir(parents=True, exist_ok=True)
    if code_output_dir:
        code_output_dir.mkdir(parents=True, exist_ok=True)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.touch(exist_ok=True)

    if args.dry_run:
        first_prompt, first_meta = build_prompt_for_sample(samples[0], args)
        print(json.dumps({"prompt_meta": first_meta, "prompt": first_prompt}, ensure_ascii=False, indent=2))
        return

    if not args.api_key:
        raise ValueError("Missing API key. Provide --api_key or set API_KEY / <ALIAS>_API_KEY in .env.")

    completed = load_existing_task_ids(save_path) if args.skip_existing else set()
    pending_samples = [sample for sample in samples if str(sample["task_id"]) not in completed]
    if not pending_samples:
        print("No pending samples. Exit.")
        return

    print(f"Task: {task}")
    print(f"Model: {args.model_alias} ({args.model})")
    print(f"Policy: {policy_config.get('policy_name', 'unknown')}")
    print(f"Samples: {len(pending_samples)}")
    print(f"Final max tokens: {args.final_max_tokens}")
    print(f"Save path: {save_path}")

    success_count = 0
    failed_count = 0
    stopped_count = 0
    total_tokens = 0
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max(args.num_workers, 1)) as executor:
        futures = []
        for sample in pending_samples:
            futures.append(executor.submit(process_sample, sample, args, policy_config, txt_output_dir, code_output_dir))
            if args.delay > 0:
                time.sleep(args.delay / max(args.num_workers, 1))

        for index, future in enumerate(as_completed(futures), 1):
            try:
                payload = future.result()
            except Exception as exc:
                failed_count += 1
                print(f"[{index}/{len(futures)}] task error: {exc}")
                continue

            if payload.get("status") == "success":
                success_count += 1
                stopped_count += int(bool(payload.get("stopped")))
                total_tokens += int(payload.get("tokens", 0))
                append_jsonl(save_path, payload["result"])
                print(
                    f"[{index}/{len(futures)}] {payload['task_id']} ok "
                    f"stopped={payload.get('stopped')} tokens~{payload.get('tokens', 0)}"
                )
            else:
                failed_count += 1
                print(f"[{index}/{len(futures)}] {payload.get('task_id', 'unknown')} failed: {payload.get('error')}")

    elapsed = time.time() - start_time
    print(f"Done in {elapsed:.2f}s")
    print(f"Success: {success_count}, Failed: {failed_count}, Early-stopped: {stopped_count}, Tokens~{total_tokens}")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run RQ3.3 online streaming early stopping.")
    parser.add_argument("--task", choices=["generation", "execution", "debug", "translation"], default="generation")
    parser.add_argument("--data", default="", help="JSON/JSONL data file, or ClassEval_T root for translation.")
    parser.add_argument("--source_lang", default="cpp")
    parser.add_argument("--target_lang", default="py")
    parser.add_argument("--lang_pairs", default="cpp-py,java-py,java-cpp,py-cpp")
    parser.add_argument("--base_url", default="", help="Override the provider base URL. Empty means use the selected model env.")
    parser.add_argument("--api_key", default="", help="Override the provider API key. Empty means use the selected model env.")
    parser.add_argument(
        "--model",
        default="",
        help="Model id. Empty means .env DEFAULT_MODEL_ALIAS.",
    )
    parser.add_argument(
        "--config",
        default=str(Path(__file__).resolve().parent / "configs" / "task_aware_policy.json"),
        help="Policy config JSON. Use tuned configs from outputs/replay_metrics when available.",
    )
    parser.add_argument("--output_dir", default="")
    parser.add_argument("--code_output_dir", default="")
    parser.add_argument("--save_path", default="")
    parser.add_argument("--max_tokens", type=int, default=51200)
    parser.add_argument(
        "--final_max_tokens",
        type=int,
        default=0,
        help=(
            "Max tokens for the final answer completion. 0 uses task defaults: "
            "execution=128, generation=1024, debug=1024, translation=1536."
        ),
    )
    parser.add_argument("--temperature", type=float, default=0.6)
    parser.add_argument("--final_temperature", type=float, default=0.2)
    parser.add_argument(
        "--finalizer_mode",
        choices=["auto", "user", "assistant"],
        default="auto",
        help=(
            "How to complete after an early stop. auto uses assistant-prefill unless "
            "the provider rejects it; user forces a separate user-message finalizer "
            "for ablations."
        ),
    )
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--request_timeout", type=float, default=180.0)
    parser.add_argument("--max_retries", type=int, default=2)
    parser.add_argument("--num_samples", type=int, default=-1)
    parser.add_argument("--num_workers", type=int, default=20)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument(
        "--expected_segments",
        type=int,
        default=0,
        help="Optional online proxy for prefix_segment_ratio. If 0, ratio guard is treated as satisfied.",
    )
    parser.add_argument(
        "--track_content",
        action="store_true",
        help="Also feed answer content deltas into the state tracker when reasoning_content is unavailable.",
    )
    parser.add_argument("--extra_body_json", default=DEFAULT_EXTRA_BODY)
    parser.add_argument("--skip_existing", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry_run", action="store_true")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
