import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from data_infrastructure import COTSample, CATEGORIES, load_all_tasks


def compute_stationary_distribution(transition_matrix: np.ndarray) -> np.ndarray:
    n = transition_matrix.shape[0]
    A = transition_matrix.T - np.eye(n)
    A = np.vstack([A, np.ones(n)])
    b = np.zeros(n + 1)
    b[-1] = 1
    try:
        pi, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        pi = np.maximum(pi, 0)
        return pi / pi.sum()
    except np.linalg.LinAlgError:
        return np.ones(n) / n


def compute_mean_first_passage_time(transition_matrix: np.ndarray) -> np.ndarray:
    n = transition_matrix.shape[0]
    M = np.zeros((n, n))
    for j in range(n):
        A = np.eye(n) - transition_matrix.copy()
        A[j, :] = 0
        A[j, j] = 1
        b = np.ones(n)
        b[j] = 0
        try:
            M[:, j] = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            M[:, j] = np.inf
    return M


def compute_transition_entropy(transition_matrix: np.ndarray) -> tuple[float, np.ndarray]:
    row_entropies = -np.sum(
        np.where(transition_matrix > 0, transition_matrix * np.log2(transition_matrix + 1e-10), 0),
        axis=1,
    )
    pi = compute_stationary_distribution(transition_matrix)
    return np.sum(pi * row_entropies), row_entropies


def compute_coupling_strength(transition_matrix: np.ndarray) -> np.ndarray:
    coupling = transition_matrix * transition_matrix.T
    np.fill_diagonal(coupling, 0)
    return coupling


def run_markov_advanced_analysis(all_samples: dict[str, list[COTSample]], output_dir: Path):
    import seaborn as sns

    from macro_topology import compute_transition_matrix
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 70)
    print(" Markov Chain Advanced Analysis")
    print("=" * 70)
    
    results = {"stationary_distribution": {}, "hitting_times": {}, "entropy": {}, "coupling": {}}
    cat_to_idx = {cat: i for i, cat in enumerate(CATEGORIES)}
    
    key_paths = [
        ("PU", "CC"), ("PU", "VV"), ("SD", "VV"),
        ("SD", "CC"), ("VV", "CC"), ("CC", "VV"),
    ]
    
    stationary_dists = {}
    hitting_times = {}
    entropies = {}
    couplings = {}
    
    for task_type, samples in all_samples.items():
        if not samples:
            continue
        
        matrix = compute_transition_matrix(samples, use_compressed=True)
        
        pi = compute_stationary_distribution(matrix)
        stationary_dists[task_type] = pi
        results["stationary_distribution"][task_type] = {
            cat: round(float(pi[i]), 4) for i, cat in enumerate(CATEGORIES)
        }
        
        mfpt = compute_mean_first_passage_time(matrix)
        task_ht = {}
        for from_cat, to_cat in key_paths:
            i, j = cat_to_idx[from_cat], cat_to_idx[to_cat]
            if mfpt[i, j] < 100:
                task_ht[f"{from_cat}->{to_cat}"] = round(float(mfpt[i, j]), 2)
        hitting_times[task_type] = task_ht
        results["hitting_times"][task_type] = task_ht
        
        global_ent, row_ent = compute_transition_entropy(matrix)
        entropies[task_type] = {"global": global_ent, "rows": row_ent}
        results["entropy"][task_type] = {
            "global_entropy": round(float(global_ent), 4),
            "row_entropies": {cat: round(float(row_ent[i]), 4) for i, cat in enumerate(CATEGORIES)}
        }
        
        coupling = compute_coupling_strength(matrix)
        couplings[task_type] = coupling
        pairs = sorted(
            (
                {"pair": f"{CATEGORIES[i]}-{CATEGORIES[j]}", "strength": round(float(coupling[i, j]), 4)}
                for i in range(len(CATEGORIES))
                for j in range(i + 1, len(CATEGORIES))
                if coupling[i, j] > 0.01
            ),
            key=lambda x: -x["strength"],
        )
        results["coupling"][task_type] = pairs[:5]
        
        print(f"\n[{task_type}]")
        print(f"  Top stationary: {CATEGORIES[np.argmax(pi)]}={pi.max():.3f}")
        print(f"  Global entropy: {global_ent:.3f} bits")
        print(f"  PU->CC steps: {task_ht.get('PU->CC', 'N/A')}")
    
    tasks = list(all_samples.keys())
    n_tasks = len(stationary_dists)
    
    _, ax = plt.subplots(figsize=(12, 6))
    x = np.arange(len(CATEGORIES))
    width = 0.8 / n_tasks
    for i, (task_type, pi) in enumerate(stationary_dists.items()):
        ax.bar(x + i * width, pi, width, label=task_type, alpha=0.8)
    ax.set_xlabel('Category')
    ax.set_ylabel('Stationary Probability')
    ax.set_title('Stationary Distribution Comparison')
    ax.set_xticks(x + width * (n_tasks - 1) / 2)
    ax.set_xticklabels(CATEGORIES)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_dir / "stationary_distribution.png", dpi=150)
    plt.close()
    
    _, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    for idx, (from_cat, to_cat) in enumerate(key_paths):
        times, task_names = [], []
        for task_type in tasks:
            key = f"{from_cat}->{to_cat}"
            if task_type in hitting_times and key in hitting_times[task_type]:
                times.append(hitting_times[task_type][key])
                task_names.append(task_type)
        if times:
            colors = plt.cm.Set2(np.linspace(0, 1, len(task_names)))
            axes[idx].bar(task_names, times, color=colors)
            axes[idx].set_title(f'{from_cat} -> {to_cat}')
            axes[idx].set_ylabel('Avg Steps')
            axes[idx].tick_params(axis='x', rotation=15)
    plt.tight_layout()
    plt.savefig(output_dir / "hitting_times.png", dpi=150)
    plt.close()
    
    _, axes = plt.subplots(1, 2, figsize=(14, 5))
    task_names = list(entropies.keys())
    global_ents = [entropies[t]["global"] for t in task_names]
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(task_names)))
    axes[0].bar(task_names, global_ents, color=colors)
    axes[0].set_title('Global Transition Entropy')
    axes[0].set_ylabel('Entropy (bits)')
    axes[0].set_xlabel('Task Type')
    
    entropy_matrix = np.array([entropies[t]["rows"] for t in task_names])
    sns.heatmap(entropy_matrix, annot=True, fmt='.2f', cmap='YlOrRd',
                xticklabels=CATEGORIES, yticklabels=task_names, ax=axes[1])
    axes[1].set_title('Row Entropy by Category')
    plt.tight_layout()
    plt.savefig(output_dir / "entropy_analysis.png", dpi=150)
    plt.close()
    
    n_tasks_valid = len(couplings)
    _, axes = plt.subplots(1, n_tasks_valid, figsize=(5 * n_tasks_valid, 5))
    if n_tasks_valid == 1:
        axes = [axes]
    for idx, (task_type, coupling) in enumerate(couplings.items()):
        sns.heatmap(coupling, annot=True, fmt='.3f', cmap='Reds',
                    xticklabels=CATEGORIES, yticklabels=CATEGORIES,
                    ax=axes[idx], vmin=0, vmax=0.15)
        axes[idx].set_title(f'{task_type} Coupling')
    plt.tight_layout()
    plt.savefig(output_dir / "coupling_analysis.png", dpi=150)
    plt.close()
    
    (output_dir / "markov_advanced_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    
    print(f"\n[Saved] {output_dir}")
    return results


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    base_dir = repo_root / "data" / "derived_cot" / "rq1_segmented"
    output_dir = repo_root / "data" / "derived_cot" / "rq1_analysis" / "markov_analysis"
    all_samples = load_all_tasks(base_dir)
    run_markov_advanced_analysis(all_samples, output_dir)
