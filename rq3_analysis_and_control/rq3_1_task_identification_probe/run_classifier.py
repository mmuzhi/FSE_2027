"""Run the RQ3.1 four-class task classifier."""
from pathlib import Path

from data_infrastructure import load_all_tasks
from task_classifier import train_and_evaluate

ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = ROOT / "data" / "derived_cot" / "rq1_segmented"


def main() -> None:
    for index, (model, label) in enumerate((("r1", "R1"), ("qwen", "Qwen"))):
        if index:
            print(f"\n{'=' * 60}\n")
        print(f"=== {label} (4-class) ===")
        output_dir = ROOT / "data" / "derived_cot" / "rq3_task_identification" / model / "classifier_analysis_4class"
        all_samples = load_all_tasks(BASE_DIR, model=model)
        print(f"Tasks: {list(all_samples.keys())}")
        train_and_evaluate(all_samples, output_dir)


if __name__ == "__main__":
    main()
