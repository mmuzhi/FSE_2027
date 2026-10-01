"""Generate the paper-ready RQ3.1 task-classification figure.

This script regenerates the RQ3.1 task classification figure used by
``_ICSE_2027__COT_Analysis/main.tex``. It reads the figure data from
``visualization/rq3_1_plot_data.json`` and writes outputs to the paper directory.
The RQ1 pattern table (``tables/rq1_pattern_families.tex``) is maintained
directly as LaTeX and is no longer generated here.

Usage:
    python3 visualization/paper_pattern_assets.py
    python3 visualization/paper_pattern_assets.py --paper-dir _ICSE_2027__COT_Analysis
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def get_repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def write_rq3_classifier_figure(repo_root: Path, paper_dir: Path) -> list[Path]:
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError as exc:
        raise SystemExit("matplotlib and numpy are required to generate the RQ3.1 figure.") from exc

    data_path = repo_root / "visualization" / "rq3_1_plot_data.json"
    plot_data = json.loads(data_path.read_text(encoding="utf-8"))
    models = plot_data["models"]
    model_labels = [model["label"] for model in models]
    logistic_acc = np.array([model["logistic_regression"]["mean"] for model in models])
    forest_acc = np.array([model["random_forest"]["mean"] for model in models])
    logistic_err = np.array([model["logistic_regression"]["std"] for model in models])
    forest_err = np.array([model["random_forest"]["std"] for model in models])
    chance = float(plot_data.get("chance", 0.25))

    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 6.8,
            "axes.titlesize": 7.1,
            "axes.labelsize": 6.9,
            "xtick.labelsize": 6.6,
            "ytick.labelsize": 6.6,
            "legend.fontsize": 6.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    colors = {
        "logistic": "#4477AA",
        "forest": "#CC6677",
    }
    output_dir = paper_dir / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig, ax_acc = plt.subplots(figsize=(4.8, 2.0))
    fig.patch.set_facecolor("white")
    x_acc = np.arange(len(models), dtype=float) * 0.92
    width = 0.27
    bar_gap = 0.01

    c1 = colors["logistic"]
    c2 = colors["forest"]

    b1 = ax_acc.bar(
        x_acc - width / 2 - bar_gap,
        logistic_acc,
        width,
        yerr=logistic_err,
        label="Logistic Regression",
        color=c1,
        alpha=0.9,
        edgecolor="black",
        linewidth=0.3,
        capsize=2.0,
        error_kw=dict(lw=0.65, capthick=0.65, ecolor="black"),
        zorder=3
    )
    b2 = ax_acc.bar(
        x_acc + width / 2 + bar_gap,
        forest_acc,
        width,
        yerr=forest_err,
        label="Random Forest",
        color=c2,
        alpha=0.9,
        edgecolor="black",
        linewidth=0.3,
        capsize=2.0,
        error_kw=dict(lw=0.65, capthick=0.65, ecolor="black"),
        zorder=3
    )

    ax_acc.axhline(chance, color="gray", linestyle=(0, (5, 4)), linewidth=0.65, zorder=0)
    ax_acc.text(
        x_acc[-1] + 0.42,
        chance + 0.025,
        f"Chance ({chance:.0%})",
        ha="left",
        va="bottom",
        fontsize=6.2,
        color="0.3",
        style="italic",
        zorder=5,
    )

    for bars, errors in zip([b1, b2], [logistic_err, forest_err]):
        for bar, err in zip(bars, errors):
            yval = bar.get_height()
            ax_acc.text(
                bar.get_x() + bar.get_width() / 2,
                yval + err + 0.015,
                f"{yval:.3f}",
                ha="center",
                va="bottom",
                fontsize=6.2,
                color="black",
            )

    ax_acc.set_xlim(-0.38, x_acc[-1] + 1.22)
    ax_acc.set_ylim(0, 1.05)
    ax_acc.set_xticks(x_acc)
    ax_acc.set_xticklabels(model_labels)
    ax_acc.set_ylabel("Accuracy")
    ax_acc.grid(axis="y", linestyle="-", alpha=0.15, color="black", linewidth=0.5, zorder=0)
    
    ax_acc.spines["top"].set_visible(False)
    ax_acc.spines["right"].set_visible(False)
    ax_acc.spines["left"].set_linewidth(0.65)
    ax_acc.spines["bottom"].set_linewidth(0.65)
    ax_acc.tick_params(axis="both", width=0.65, length=2.5)

    ax_acc.legend(
        loc="lower center",
        bbox_to_anchor=(0.5, 1.02),
        ncol=2,
        frameon=False,
        handlelength=1.2,
        handletextpad=0.5,
        columnspacing=1.5
    )

    fig.subplots_adjust(left=0.15, right=0.98, top=0.82, bottom=0.15)
    pdf_path = output_dir / "rq3_task_classification.pdf"
    png_path = output_dir / "rq3_task_classification.png"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.02, facecolor="white", transparent=False)
    fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.02, facecolor="white", transparent=False)
    plt.close(fig)
    return [pdf_path, png_path]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the RQ3.1 paper-ready figure.")
    parser.add_argument("--repo-root", type=Path, default=get_repo_root(), help="Repository root directory.")
    parser.add_argument(
        "--paper-dir",
        type=Path,
        default=Path("_ICSE_2027__COT_Analysis"),
        help="Paper directory, relative to repo root unless absolute.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    paper_dir = args.paper_dir if args.paper_dir.is_absolute() else repo_root / args.paper_dir

    outputs = write_rq3_classifier_figure(repo_root, paper_dir)

    print("Generated paper assets:")
    for output in outputs:
        print(f"  - {output}")


if __name__ == "__main__":
    main()
