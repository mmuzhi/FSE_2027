import json
from pathlib import Path
from dataclasses import dataclass
from collections import Counter
from itertools import groupby

CATEGORIES = ["PU", "SD", "IP", "CC", "VV", "KR", "MR", "AUX"]

@dataclass
class COTSample:
    task_id: str
    task_type: str
    raw_sequence: list[str]
    compressed_sequence: list[str]
    effort_counts: list[int]
    category_distribution: dict[str, float]

def load_segmented_data(jsonl_path: Path) -> list[dict]:
    with jsonl_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def extract_raw_sequence(sample: dict) -> list[str]:
    result = sample.get("segmentation_result", {})
    if not result.get("success"):
        return []
    return [
        step["category"]
        for step in result.get("steps", [])
        if step.get("category") in CATEGORIES
    ]

def compress_sequence(raw_seq: list[str]) -> tuple[list[str], list[int]]:
    groups = [(cat, sum(1 for _ in items)) for cat, items in groupby(raw_seq)]
    return [cat for cat, _ in groups], [count for _, count in groups]

def compute_distribution(raw_seq: list[str]) -> dict[str, float]:
    counter = Counter(raw_seq)
    total = len(raw_seq)
    return {cat: counter[cat] / total for cat in CATEGORIES} if total else {cat: 0.0 for cat in CATEGORIES}

def process_samples(data: list[dict], task_type: str, min_steps: int = 2) -> list[COTSample]:
    samples = []
    for item in data:
        raw_seq = extract_raw_sequence(item)
        if len(raw_seq) < min_steps:
            continue
        compressed, counts = compress_sequence(raw_seq)
        samples.append(COTSample(
            task_id=item.get("task_id", "unknown"),
            task_type=task_type,
            raw_sequence=raw_seq,
            compressed_sequence=compressed,
            effort_counts=counts,
            category_distribution=compute_distribution(raw_seq)
        ))
    return samples

def load_all_tasks(base_dir: Path, model: str = "r1") -> dict[str, list[COTSample]]:
    task_dirs = {
        "Generate": "Generate_COT",
        "Execute": "Execution_COT",
        "Debug": "Debug_COT",
        "Translate": "Translation_COT",
    }
    all_samples = {}
    for task_type, task_dir in task_dirs.items():
        path = base_dir / task_dir / model / "segmented_results.jsonl"
        if not path.exists():
            all_samples[task_type] = []
            print(f"[{task_type}] File not found: {path}")
            continue
        all_samples[task_type] = process_samples(load_segmented_data(path), task_type)
        print(f"[{task_type}] Loaded {len(all_samples[task_type])} samples from {path.name}")
    return all_samples

def get_all_samples_flat(all_samples: dict[str, list[COTSample]]) -> list[COTSample]:
    return [sample for samples in all_samples.values() for sample in samples]

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2] / "data" / "derived_cot" / "rq1_segmented"
    all_samples = load_all_tasks(base_dir)
    print(f"\nTotal samples: {sum(len(s) for s in all_samples.values())}")
