"""Data loading helpers for the RQ3.1 task-identification probe."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rq1_general_patterns.analysis.data_infrastructure import (  # noqa: E402
    CATEGORIES,
    COTSample,
    compress_sequence,
    compute_distribution,
    extract_raw_sequence,
    get_all_samples_flat,
    load_all_tasks,
    load_segmented_data,
    process_samples,
)

__all__ = [
    "CATEGORIES",
    "COTSample",
    "compress_sequence",
    "compute_distribution",
    "extract_raw_sequence",
    "get_all_samples_flat",
    "load_all_tasks",
    "load_segmented_data",
    "process_samples",
]


if __name__ == "__main__":
    all_samples = load_all_tasks(ROOT / "data" / "derived_cot" / "rq1_segmented")
    total = sum(len(samples) for samples in all_samples.values())
    print(f"\nTotal samples: {total}")
