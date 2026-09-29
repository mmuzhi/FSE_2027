"""Replay local RQ3.3 monitor work without making model/API requests.

Run from the repository root:
    python rq3_applications/rq3_3_pattern_aware_early_stopping/benchmark_monitor.py

The fixed sample is the first ten records with nonempty ``cot`` in each Qwen
early-stopping JSONL file. Each trace is replayed in 25-character chunks. This
benchmarks only the local monitor; it excludes model generation, network I/O,
answer finalization, and JSONL loading.
"""

from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from pathlib import Path

from policy import PolicyEngine, load_policy_config
from state_model import RuleStateModel
from state_tracker import StateTracker
from stream_runner import detect_repetition_trigger, evaluate_latest_segment


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TASKS = ("generation", "execution", "debug", "translation")
SAMPLES_PER_TASK = 10
CHUNK_CHARS = 25
MAX_TOKENS = 51200
EXPECTED_SEGMENTS = 0
MIN_MEASURED_CPU_NS = 125_000_000  # Amortize the coarse CPU clock on Windows.
MAX_REPEATS = 4096
POLICY_PATH = HERE / "configs" / "task_aware_policy.json"
DATA_ROOT = ROOT / "data" / "derived_cot" / "rq3_early_stopping" / "output" / "qwen"


def first_nonempty_traces(path: Path) -> list[tuple[str, str]]:
    traces: list[tuple[str, str]] = []
    with path.open("r", encoding="utf-8") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON in {path}:{line_number}") from exc
            cot = record.get("cot")
            if isinstance(cot, str) and cot.strip():
                traces.append((str(record.get("task_id", line_number)), cot))
                if len(traces) == SAMPLES_PER_TASK:
                    break
    if len(traces) < SAMPLES_PER_TASK:
        raise ValueError(f"Expected {SAMPLES_PER_TASK} nonempty CoTs in {path}; found {len(traces)}")
    return traces


def percentile(values: list[float], fraction: float) -> float:
    """Linearly interpolate at the zero-based (n - 1) * fraction position."""
    if not values:
        raise ValueError("Cannot calculate a percentile of an empty sample")
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def replay_trace(task: str, task_id: str, cot: str, config: dict) -> tuple[dict, list[float]]:
    tracker = StateTracker(model=RuleStateModel())
    policy = PolicyEngine(config)
    reasoning_parts: list[str] = []
    chunk_wall_ms: list[float] = []
    trigger_type = "none"
    processed_chars = 0

    for offset in range(0, len(cot), CHUNK_CHARS):
        delta = cot[offset : offset + CHUNK_CHARS]
        start_wall = time.perf_counter_ns()

        # Match the reasoning_delta branch of stream_runner.stream_with_policy.
        reasoning_parts.append(delta)
        repetition_event = detect_repetition_trigger(
            "".join(reasoning_parts), config, len(tracker.closed_segments)
        )
        if repetition_event:
            trigger_type = repetition_event["trigger_type"]
        else:
            for segment in tracker.feed_delta(delta):
                event = evaluate_latest_segment(
                    tracker=tracker,
                    segment=segment,
                    task=task,
                    policy_engine=policy,
                    expected_segments=EXPECTED_SEGMENTS,
                    max_tokens=MAX_TOKENS,
                )
                if event["would_trigger"]:
                    trigger_type = event["trigger_type"]
                    break

        chunk_wall_ms.append((time.perf_counter_ns() - start_wall) / 1_000_000)
        processed_chars += len(delta)
        if trigger_type != "none":
            break

    if trigger_type == "none":
        tracker.flush_pending()  # The runner flushes, but does not evaluate, at normal EOF.

    result = {
        "task": task,
        "task_id": task_id,
        "input_chars": len(cot),
        "processed_chars": processed_chars,
        "chunks": len(chunk_wall_ms),
        "closed_segments": len(tracker.closed_segments),
        "trigger": trigger_type,
    }
    return result, chunk_wall_ms


def average_trace_cpu_ms(task: str, task_id: str, cot: str, config: dict) -> tuple[float, int]:
    """Amortize a complete local replay over enough CPU ticks to be measurable."""
    repeats = 0
    start_cpu = time.process_time_ns()
    elapsed_cpu = 0
    while elapsed_cpu < MIN_MEASURED_CPU_NS and repeats < MAX_REPEATS:
        replay_trace(task, task_id, cot, config)
        repeats += 1
        elapsed_cpu = time.process_time_ns() - start_cpu
    return elapsed_cpu / repeats / 1_000_000, repeats


def main() -> None:
    results: list[dict] = []
    all_chunk_wall_ms: list[float] = []
    for task in TASKS:
        source_path = DATA_ROOT / task / "results.jsonl"
        config = load_policy_config(str(POLICY_PATH), task=task)
        for task_id, cot in first_nonempty_traces(source_path):
            result, chunk_times = replay_trace(task, task_id, cot, config)
            result["cpu_ms_per_replay"], result["cpu_repeats"] = average_trace_cpu_ms(
                task, task_id, cot, config
            )
            results.append(result)
            all_chunk_wall_ms.extend(chunk_times)

    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    print(f"Platform: {platform.platform()}")
    print(f"Processor: {platform.processor() or 'unreported by platform'}")
    print(f"CPU clock: {time.get_clock_info('process_time').implementation}")
    print(f"Policy: {POLICY_PATH.relative_to(ROOT)}")
    print(f"Sample: first {SAMPLES_PER_TASK} nonempty Qwen CoTs per task; {CHUNK_CHARS} characters/chunk")
    print(f"Traces: {len(results)}; processed chunks: {len(all_chunk_wall_ms)}")
    print(
        "Per-chunk local wall latency (ms): "
        f"median={statistics.median(all_chunk_wall_ms):.4f}, "
        f"p95={percentile(all_chunk_wall_ms, 0.95):.4f}, "
        f"p99={percentile(all_chunk_wall_ms, 0.99):.4f}"
    )
    print(
        "Per-trace cumulative local CPU (ms, mean of repeated full replays; "
        "includes initialization and final flush):"
    )
    trace_cpu_ms = [item["cpu_ms_per_replay"] for item in results]
    print(
        f"Summary: median={statistics.median(trace_cpu_ms):.3f}, "
        f"p95={percentile(trace_cpu_ms, 0.95):.3f}, max={max(trace_cpu_ms):.3f}"
    )
    print("task\ttask_id\tchunks\ttrigger\trepeats\tcpu_ms")
    for result in results:
        print(
            f"{result['task']}\t{result['task_id']}\t{result['chunks']}\t"
            f"{result['trigger']}\t{result['cpu_repeats']}\t{result['cpu_ms_per_replay']:.3f}"
        )


if __name__ == "__main__":
    main()
