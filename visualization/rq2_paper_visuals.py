"""Generate the paper-ready RQ2 figure.

This script reads the paper-level RQ pattern catalog and writes a diverging
(butterfly) chart of positive/anti-pattern support, used by
``_ICSE_2027__COT_Analysis/main.tex`` as Fig.~\\ref{fig:rq2-patterns}.

Usage:
    python3 visualization/rq2_paper_visuals.py
"""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


MODEL_LABELS = {
    "r1": "R1-0528",
    "qwen": "R1-Qwen3-8B",
}

VALID_COLOR = "#4477AA"
INVALID_COLOR = "#CC6677"

TASK_LABELS = {
    "generation": "Generation",
    "execution": "Execution",
    "summarization": "Summarization",
    "debug": "Debugging",
    "translation": "Translation",
}


@dataclass(frozen=True)
class PatternCatalogRow:
    task: str
    model: str
    kind: str
    pattern: str
    main_pct: float
    contrast_pct: float
    code: str


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def parse_pct(value: str) -> float:
    return float(value.strip().rstrip("%"))


def extract_code(pattern: str) -> str:
    matches = re.findall(r"\(([^()]*)\)", pattern)
    return matches[-1].strip() if matches else pattern.strip()


def format_code_for_label(code: str) -> str:
    return code.replace("<->", "↔").replace("=>", "⇒").replace("->", "→")


def figure_label(row: PatternCatalogRow) -> str:
    task = TASK_LABELS.get(row.task, row.task.title())
    return f"{task}: {format_code_for_label(row.code)}"


def format_code_for_latex(code: str) -> str:
    formatted = code
    formatted = formatted.replace("<->", r"$\leftrightarrow$")
    formatted = formatted.replace("=>", r"$\Rightarrow$")
    formatted = formatted.replace("->", r"$\rightarrow$")
    formatted = formatted.replace("_", r"\_")
    formatted = formatted.replace("%", r"\%")
    return formatted


def load_pattern_catalog(path: Path) -> list[PatternCatalogRow]:
    rows: list[PatternCatalogRow] = []
    for row in read_csv(path):
        pattern = row["pattern"]
        rows.append(
            PatternCatalogRow(
                task=row["task"],
                model=row["model"],
                kind=row["type"],
                pattern=pattern,
                main_pct=parse_pct(row["main_pct"]),
                contrast_pct=parse_pct(row["contrast_pct"]),
                code=extract_code(pattern),
            )
        )
    return rows


TASK_ORDER = ("generation", "execution", "debug", "translation")


def select_butterfly_entries(
    rows: list[PatternCatalogRow],
    model: str,
) -> list[PatternCatalogRow]:
    """For one model, pick the strongest positive and anti-pattern per task.

    This keeps the figure balanced across the four oracle-backed tasks instead
    of letting one task dominate. A (task, kind) cell with no mined pattern
    (e.g. translation positive on R1-Qwen3-8B) is simply skipped.
    """
    model_rows = [row for row in rows if row.model == model and row.kind in {"positive", "anti-pattern"}]
    selected: list[PatternCatalogRow] = []
    for kind in ("positive", "anti-pattern"):
        for task in TASK_ORDER:
            candidates = [row for row in model_rows if row.kind == kind and row.task == task]
            if candidates:
                selected.append(max(candidates, key=lambda row: row.main_pct))
    return selected


def write_pattern_catalog_table(rows: list[PatternCatalogRow], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    selected = [row for row in rows if row.kind in {"positive", "anti-pattern"}]
    selected.sort(key=lambda row: (row.task, row.model, row.kind, -row.main_pct))

    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Unified RQ2 pattern catalog. Main support reports the support of a pattern in its target group, while contrast support reports its support in the corresponding comparison group.}",
        r"\label{tab:rq2-pattern-catalog}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{5pt}",
        r"\renewcommand{\arraystretch}{1.15}",
        r"\begin{tabular}{llllrr}",
        r"\toprule",
        r"Task & Model & Type & Signature & Main (\%) & Contrast (\%) \\",
        r"\midrule",
    ]
    for row in selected:
        task = TASK_LABELS.get(row.task, row.task.title())
        model = MODEL_LABELS.get(row.model, row.model)
        kind = row.kind
        code = format_code_for_latex(row.code)
        lines.append(f"{task} & {model} & {kind} & {code} & {row.main_pct:.1f} & {row.contrast_pct:.1f} \\\\")
    lines.extend([r"\bottomrule", r"\end{tabular}", r"\end{table*}", ""])
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def catalog_path(paper_dir: Path) -> Path:
    return paper_dir / "patterns/rq_task_pattern_summary.csv"


def write_butterfly_figure(paper_dir: Path) -> list[Path]:
    """Diverging chart of catalog positive/anti-pattern support by model."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ModuleNotFoundError as exc:
        raise SystemExit("matplotlib and numpy are required to generate the RQ2 figure.") from exc

    rows = load_pattern_catalog(catalog_path(paper_dir))

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.5,
            "axes.titlesize": 7.5,
            "axes.labelsize": 7.2,
            "xtick.labelsize": 6.8,
            "ytick.labelsize": 6.4,
            "legend.fontsize": 6.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, axes = plt.subplots(2, 1, figsize=(7.4, 6.2))
    fig.subplots_adjust(left=0.22, right=0.995, top=0.95, bottom=0.08, hspace=0.25)

    for ax, model, panel_label in zip(axes, ("r1", "qwen"), ("a", "b")):
        entries = select_butterfly_entries(rows, model)
        labels = [figure_label(row) for row in entries]
        positive_main = np.array([row.main_pct if row.kind == "positive" else 0.0 for row in entries])
        anti_main = np.array([row.main_pct if row.kind == "anti-pattern" else 0.0 for row in entries])
        positive_contrast = np.array([row.contrast_pct if row.kind == "positive" else 0.0 for row in entries])
        anti_contrast = np.array([row.contrast_pct if row.kind == "anti-pattern" else 0.0 for row in entries])
        y = np.arange(len(entries))[::-1]  # first entry on top

        bar_h = 0.62
        ax.barh(y, positive_main, height=bar_h, color=VALID_COLOR, edgecolor="white", linewidth=0.4)
        ax.barh(y, -anti_main, height=bar_h, color=INVALID_COLOR, edgecolor="white", linewidth=0.4)
        # Light contrast bars keep main-vs-contrast support visible without adding another table.
        ax.barh(y, -positive_contrast, height=bar_h, color=INVALID_COLOR, alpha=0.22, edgecolor="none")
        ax.barh(y, anti_contrast, height=bar_h, color=VALID_COLOR, alpha=0.22, edgecolor="none")
        ax.axvline(0, color="#444444", linewidth=0.7)

        for yi, row in zip(y, entries):
            if row.kind == "positive":
                ax.text(row.main_pct + 1.0, yi, f"{row.main_pct:.1f}", va="center", ha="left", fontsize=6.5)
            else:
                ax.text(-row.main_pct + 1.0, yi, f"{row.main_pct:.1f}", va="center", ha="left", fontsize=6.5)

        ax.set_yticks(y)
        ax.set_yticklabels(labels)
        ax.set_ylim(y.min() - 0.7, y.max() + 0.7)
        max_value = max([row.main_pct for row in entries] + [row.contrast_pct for row in entries])
        limit = max(25, int((max_value + 9) // 10) * 10)
        ax.set_xlim(-limit, limit)
        ticks = list(range(-limit, limit + 1, 20))
        ax.set_xticks(ticks)
        ax.set_xticklabels([str(abs(tick)) for tick in ticks])
        ax.set_xlabel("Support (%)", labelpad=1)
        ax.set_title(f"({panel_label}) {MODEL_LABELS[model]}", pad=3)
        ax.grid(axis="x", color="#dddddd", linewidth=0.5, alpha=0.7)
        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    from matplotlib.patches import Patch

    handles = [
        Patch(facecolor=INVALID_COLOR, label="Negative pattern main support"),
        Patch(facecolor=VALID_COLOR, label="Positive pattern main support"),
        Patch(facecolor="#bbbbbb", alpha=0.45, label="Contrast support (opposite side)"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.03))

    fig_dir = paper_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = fig_dir / "rq2_valid_invalid_patterns.pdf"
    png_path = fig_dir / "rq2_valid_invalid_patterns.png"
    fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.02)
    fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    return [pdf_path, png_path]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the RQ2 paper figure.")
    parser.add_argument(
        "--paper-dir",
        type=Path,
        default=repo_root() / "_ICSE_2027__COT_Analysis",
        help="Path to the paper directory.",
    )
    args = parser.parse_args()
    rows = load_pattern_catalog(catalog_path(args.paper_dir))
    table_path = write_pattern_catalog_table(rows, args.paper_dir / "tables/rq2_pattern_catalog.tex")
    print(table_path)
    for path in write_butterfly_figure(args.paper_dir):
        print(path)


if __name__ == "__main__":
    main()
