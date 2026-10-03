import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from data_infrastructure import load_all_tasks
from macro_topology import analyze_topology
from markov_advanced import run_markov_advanced_analysis
from discriminative_patterns import analyze_discriminative_patterns


def run_full_analysis(base_dir: Path, output_base: Path, model: str = "r1"):
    print("=" * 70)
    print(" RQ1: Cross-Task Reasoning Workflow Analysis")
    print(" Tasks: Generate, Execute, Debug, Translate")
    print("=" * 70)

    print("\n[Step 1] Loading segmented data...")
    all_samples = load_all_tasks(base_dir, model)

    total = sum(map(len, all_samples.values()))
    if total == 0:
        print("No data found. Please run segmentation first.")
        return

    print(f"\nTotal: {total} samples")
    for task, samples in all_samples.items():
        print(f"  {task}: {len(samples)}")

    print("\n" + "=" * 70)
    print("[Step 2] Macro Topology Analysis")
    analyze_topology(all_samples, output_base / "topology_analysis")

    print("\n" + "=" * 70)
    print("[Step 3] Markov Chain Advanced Analysis")
    run_markov_advanced_analysis(all_samples, output_base / "markov_analysis")

    print("\n" + "=" * 70)
    print("[Step 4] Discriminative Pattern Analysis")
    analyze_discriminative_patterns(all_samples, output_base / "discriminative_analysis")

    print("\n" + "=" * 70)
    print(" Analysis Complete!")
    print("=" * 70)
    print(f"\nOutput: {output_base}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run CoT Analysis Pipeline")
    parser.add_argument("--model", default="qwen", help="Model name (e.g., r1, qwen)")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    base_dir = repo_root / "data" / "derived_cot" / "rq1_segmented"
    output_dir = repo_root / "data" / "derived_cot" / "rq1_analysis" / "analysis_results" / args.model
    
    run_full_analysis(base_dir, output_dir, model=args.model)
