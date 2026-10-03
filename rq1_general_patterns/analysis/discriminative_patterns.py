import json
from pathlib import Path
from collections import defaultdict
from itertools import combinations

import numpy as np
import matplotlib.pyplot as plt

from data_infrastructure import COTSample, CATEGORIES, load_all_tasks


def extract_ngrams(sequence: list[str], n: int) -> list[tuple]:
    return [tuple(sequence[i:i+n]) for i in range(len(sequence) - n + 1)]


def compute_ngram_support(samples: list[COTSample], n_range: tuple = (2, 3)) -> dict[tuple, float]:
    if not samples:
        return {}
    
    ngram_presence = defaultdict(int)
    for sample in samples:
        for ngram in {
            ngram
            for n in range(n_range[0], n_range[1] + 1)
            for ngram in extract_ngrams(sample.compressed_sequence, n)
        }:
            ngram_presence[ngram] += 1
    
    return {ngram: count / len(samples) for ngram, count in ngram_presence.items()}


def statistical_test(count_a: int, total_a: int, count_b: int, total_b: int) -> float:
    from scipy.stats import chi2_contingency, fisher_exact

    table = np.array([[count_a, count_b], 
                      [total_a - count_a, total_b - count_b]])
    try:
        _, p, *_ = (fisher_exact if min(table.ravel()) < 5 else chi2_contingency)(table)
        return p
    except ValueError:
        return 1.0


def find_discriminative_patterns(samples_a: list[COTSample], samples_b: list[COTSample],
                                  task_a: str, task_b: str,
                                  n_range: tuple = (2, 5), min_support: float = 0.03,
                                  p_threshold: float = 0.01) -> list[dict]:
    support_a = compute_ngram_support(samples_a, n_range)
    support_b = compute_ngram_support(samples_b, n_range)
    
    discriminative = []
    for pattern in support_a.keys() | support_b.keys():
        sup_a, sup_b = support_a.get(pattern, 0), support_b.get(pattern, 0)
        if max(sup_a, sup_b) < min_support:
            continue
        
        count_a, count_b = int(sup_a * len(samples_a)), int(sup_b * len(samples_b))
        p_value = statistical_test(count_a, len(samples_a), count_b, len(samples_b))
        
        if p_value < p_threshold:
            if sup_a > sup_b:
                favored, ratio = task_a, sup_a / max(sup_b, 1e-10)
            else:
                favored, ratio = task_b, sup_b / max(sup_a, 1e-10)
            
            discriminative.append({
                "pattern": "->".join(pattern),
                f"support_{task_a}": round(sup_a, 4),
                f"support_{task_b}": round(sup_b, 4),
                "favored_task": favored,
                "ratio": round(ratio, 2),
                "p_value": round(p_value, 6)
            })
    
    return sorted(discriminative, key=lambda x: x["p_value"])


def find_task_signatures(all_samples: dict[str, list[COTSample]], top_k: int = 15, 
                         n_range: tuple = (2, 5), min_support: float = 0.05, 
                         min_ratio: float = 2.0) -> dict:
    signatures = {}
    task_supports = {
        task: compute_ngram_support(samples, n_range)
        for task, samples in all_samples.items()
        if samples
    }
    tasks = list(task_supports)
    
    for task in tasks:
        candidates = []
        my_supports = task_supports[task]
        
        for pattern, support in my_supports.items():
            if support < min_support:
                continue
            
            runner_up_task, max_other_support = max(
                (
                    (other_task, task_supports[other_task].get(pattern, 0.0))
                    for other_task in tasks
                    if other_task != task
                ),
                key=lambda item: item[1],
                default=(None, 0.0),
            )
            
            current_ratio = support / max(max_other_support, 0.001)
            
            if current_ratio >= min_ratio:
                score = current_ratio * (np.log(support * 100) + 1)
                
                candidates.append({
                    "pattern": "->".join(pattern),
                    f"support_{task}": round(support, 4),
                    "support_others_max": round(max_other_support, 4),
                    "runner_up": runner_up_task,
                    "favored_task": task,
                    "ratio": round(current_ratio, 2),
                    "p_value": 0.0,
                    "score": score
                })
        
        candidates.sort(key=lambda x: x["score"], reverse=True)
        signatures[task] = candidates[:top_k]
    
    return signatures


def analyze_discriminative_patterns(all_samples: dict[str, list[COTSample]], 
                                     output_dir: Path) -> dict:
    import seaborn as sns

    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "=" * 70)
    print(" Discriminative Pattern Analysis")
    print("=" * 70)
    
    results = {}
    tasks = [t for t in all_samples.keys() if all_samples[t]]
    
    print("\n[1] Task Signature Patterns (p<0.01)")
    signatures = find_task_signatures(all_samples, top_k=15)
    results["signatures"] = {}
    
    for task, patterns in signatures.items():
        print(f"\n  [{task}]")
        results["signatures"][task] = []
        for p in patterns[:5]:
            print(f"    {p['pattern']}: support={p.get(f'support_{task}', 0):.3f}, "
                  f"ratio={p['ratio']:.1f}x")
            results["signatures"][task].append({
                "pattern": p["pattern"],
                "support": p.get(f"support_{task}", 0),
                "support_others_max": p.get("support_others_max", 0),
                "ratio": p["ratio"],
                "p_value": p["p_value"]
            })
    
    print("\n[2] Pairwise Task Comparison")
    results["pairwise"] = {}
    
    for task_a, task_b in combinations(tasks, 2):
        patterns = find_discriminative_patterns(
            all_samples[task_a], all_samples[task_b], task_a, task_b)
        
        key = f"{task_a}_vs_{task_b}"
        results["pairwise"][key] = {
            "total": len(patterns),
            f"favored_{task_a}": sum(p["favored_task"] == task_a for p in patterns),
            f"favored_{task_b}": sum(p["favored_task"] == task_b for p in patterns),
            "top_patterns": [{"pattern": p["pattern"], "favored": p["favored_task"], 
                             "ratio": p["ratio"]} for p in patterns[:5]]
        }
        print(f"  {task_a} vs {task_b}: {len(patterns)} discriminative patterns")
    
    print("\n[3] Generating visualizations...")
    
    patterns_per_task = 4
    
    all_patterns = [
        (p["pattern"], task)
        for task in tasks
        for p in signatures.get(task, [])[:patterns_per_task]
    ]
    owner_counts = {task: sum(owner == task for _, owner in all_patterns) for task in tasks}
    
    pattern_support = {}
    for pattern_str, owner in all_patterns:
        pattern_tuple = tuple(pattern_str.split("->"))
        n = len(pattern_tuple)
        pattern_support[pattern_str] = {"owner": owner}
        for t in tasks:
            if all_samples[t]:
                support_dict = compute_ngram_support(all_samples[t], (n, n))
                pattern_support[pattern_str][t] = support_dict.get(pattern_tuple, 0)
    
    _, ax = plt.subplots(figsize=(20, 10))
    
    pattern_names = [p[0] for p in all_patterns]
    n_patterns = len(pattern_names)
    n_tasks = len(tasks)
    
    bar_width = 0.15
    x = np.arange(n_patterns)
    colors_map = {
        task: plt.cm.Set2(i / n_tasks) for i, task in enumerate(tasks)
    }
    
    max_y = 0
    for i, task in enumerate(tasks):
        supports = [pattern_support[p].get(task, 0) for p in pattern_names]
        max_y = max(max_y, max(supports) if supports else 0)
        offset = (i - n_tasks/2 + 0.5) * bar_width
        ax.bar(x + offset, supports, bar_width, label=task, color=colors_map[task], alpha=0.9, edgecolor='white', linewidth=0.5)
    
    current_idx = 0
    bg_colors = ['#f8f9fa', '#e9ecef']
    for i, task in enumerate(tasks):
        count = owner_counts[task]
        
        start_x = current_idx - 0.5
        end_x = current_idx + count - 0.5
        ax.axvspan(start_x, end_x, color=bg_colors[i % 2], alpha=0.3, zorder=-1)
        
        if current_idx + count < n_patterns:
            ax.axvline(x=current_idx + count - 0.5, color='gray', linestyle=':', alpha=0.5, linewidth=1.0)
            
        current_idx += count
    
    current_idx = 0
    label_y = max_y * 1.05
    for task in tasks:
        count = owner_counts[task]
        start_x = current_idx - 0.4
        ax.text(start_x, label_y, task, ha='left', va='bottom', fontsize=14, 
               fontweight='bold', color=colors_map[task],
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.8))
        current_idx += count
    
    ax.set_xlabel('Signature Reasoning Patterns', fontsize=14, fontweight='bold', labelpad=15)
    ax.set_ylabel('Frequency (Support)', fontsize=14, fontweight='bold')
    ax.set_title('Cross-Task Comparison of Signature Patterns', fontsize=18, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    formatted_labels = [p.replace("->", "→") for p in pattern_names]
    ax.set_xticklabels(formatted_labels, rotation=35, ha='right', fontsize=10, fontfamily='monospace')
    
    ax.tick_params(axis='y', labelsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.3, zorder=0)
    
    ax.legend(title='Task Frequency', loc='upper right', fontsize=11, title_fontsize=12, 
              framealpha=0.95, edgecolor='gray', shadow=True)
    
    ax.set_ylim(bottom=0, top=max_y * 1.2)
    ax.set_xlim(left=-0.5)
    plt.subplots_adjust(bottom=0.2)
    
    plt.savefig(output_dir / "signature_patterns.png", dpi=200, bbox_inches='tight')
    plt.close()
    
    n = len(tasks)
    diff_matrix = np.zeros((n, n))
    for i, t_a in enumerate(tasks):
        for j, t_b in enumerate(tasks):
            if i != j:
                key = f"{t_a}_vs_{t_b}" if f"{t_a}_vs_{t_b}" in results["pairwise"] else f"{t_b}_vs_{t_a}"
                if key in results["pairwise"]:
                    diff_matrix[i, j] = results["pairwise"][key]["total"]
    
    _, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(diff_matrix, annot=True, fmt='.0f', cmap='YlOrRd',
                xticklabels=tasks, yticklabels=tasks, ax=ax)
    ax.set_title('Discriminative Patterns Between Tasks (p<0.01)')
    plt.tight_layout()
    plt.savefig(output_dir / "pairwise_discrimination.png", dpi=150)
    plt.close()
    
    _, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(CATEGORIES), endpoint=False).tolist() + [0]
    colors = plt.cm.Set2(np.linspace(0, 1, len(tasks)))
    
    for idx, task in enumerate(tasks):
        samples = all_samples[task]
        if not samples:
            continue
        avg = np.array([
            [s.category_distribution.get(cat, 0) for cat in CATEGORIES]
            for s in samples
        ]).mean(axis=0)
        values = list(avg) + [avg[0]]
        ax.plot(angles, values, 'o-', linewidth=2, label=task, color=colors[idx])
        ax.fill(angles, values, alpha=0.1, color=colors[idx])
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(CATEGORIES)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
    ax.set_title('Category Distribution by Task', y=1.08)
    plt.tight_layout()
    plt.savefig(output_dir / "category_radar.png", dpi=150, bbox_inches='tight')
    plt.close()
    
    (output_dir / "discriminative_results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    
    print(f"\n[Saved] {output_dir}")
    return results


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[2]
    base_dir = repo_root / "data" / "derived_cot" / "rq1_segmented"
    output_dir = repo_root / "data" / "derived_cot" / "rq1_analysis" / "discriminative_analysis"
    all_samples = load_all_tasks(base_dir)
    analyze_discriminative_patterns(all_samples, output_dir)
