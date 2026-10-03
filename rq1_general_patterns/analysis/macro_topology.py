import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from data_infrastructure import COTSample, CATEGORIES, load_all_tasks


def compute_transition_matrix(samples: list[COTSample], use_compressed: bool = False) -> np.ndarray:
    n = len(CATEGORIES)
    cat_to_idx = {cat: i for i, cat in enumerate(CATEGORIES)}
    counts = np.zeros((n, n), dtype=float)

    for sample in samples:
        seq = sample.compressed_sequence if use_compressed else sample.raw_sequence
        for current, next_cat in zip(seq, seq[1:]):
            counts[cat_to_idx[current], cat_to_idx[next_cat]] += 1

    row_sums = counts.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    return counts / row_sums


def compute_dependency_edges(matrix: np.ndarray, threshold: float = 0.15) -> list[tuple]:
    return sorted(
        (
            (from_cat, to_cat, matrix[i, j])
            for i, from_cat in enumerate(CATEGORIES)
            for j, to_cat in enumerate(CATEGORIES)
            if matrix[i, j] > threshold
        ),
        key=lambda x: -x[2],
    )


def extract_backbone(all_samples: dict[str, list[COTSample]], threshold: float = 0.1) -> list[tuple]:
    edge_sets = [
        {(edge[0], edge[1]) for edge in compute_dependency_edges(compute_transition_matrix(samples), threshold)}
        for samples in all_samples.values()
        if samples
    ]
    if not edge_sets:
        return []
    return list(set.intersection(*edge_sets))


def analyze_topology(all_samples: dict[str, list[COTSample]], output_dir: Path):
    import seaborn as sns

    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 60)
    print(" Macro Topology Analysis")
    print("=" * 60)

    _, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()

    for idx, (task_type, samples) in enumerate(all_samples.items()):
        if not samples or idx >= 4:
            continue
        matrix = compute_transition_matrix(samples)
        sns.heatmap(matrix, annot=True, fmt=".2f", cmap="Blues",
                    xticklabels=CATEGORIES, yticklabels=CATEGORIES,
                    ax=axes[idx], vmin=0, vmax=0.5)
        axes[idx].set_title(f"{task_type} Transition Matrix")
        axes[idx].set_xlabel("To")
        axes[idx].set_ylabel("From")

    plt.tight_layout()
    plt.savefig(output_dir / "transition_heatmaps.png", dpi=150)
    plt.close()

    print("\n[Strong Dependency Edges (p > 0.15)]")
    for task_type, samples in all_samples.items():
        if not samples:
            continue
        matrix = compute_transition_matrix(samples)
        edges = compute_dependency_edges(matrix, 0.15)
        print(f"\n  [{task_type}]")
        for from_cat, to_cat, prob in edges[:5]:
            print(f"    {from_cat} -> {to_cat}: {prob:.3f}")

    backbone = extract_backbone(all_samples)
    print(f"\n[Common Backbone (all tasks)]")
    for from_cat, to_cat in backbone:
        print(f"  {from_cat} -> {to_cat}")

    matrices = {
        task_type: compute_transition_matrix(samples).tolist()
        for task_type, samples in all_samples.items()
        if samples
    }
    (output_dir / "transition_matrices.json").write_text(json.dumps(matrices, indent=2))
    
    print(f"\n[Saved] {output_dir}")


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    base_dir = repo_root / "data" / "derived_cot" / "rq1_segmented"
    output_dir = repo_root / "data" / "derived_cot" / "rq1_analysis" / "topology_analysis"
    all_samples = load_all_tasks(base_dir)
    analyze_topology(all_samples, output_dir)
