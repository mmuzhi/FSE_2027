"""Mine RQ2 reasoning-pattern differences from segmented CoTs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from dataclasses import dataclass
from itertools import groupby
from pathlib import Path
from typing import Any, Iterable, Optional


CATEGORIES = ["PU", "SD", "IP", "CC", "VV", "KR", "MR", "AUX"]
CAT_TO_IDX = {c: i for i, c in enumerate(CATEGORIES)}
TRANSLATION_DIRECTIONS = ("cpp_to_py", "java_to_py", "py_to_cpp", "java_to_cpp")

_TIKTOKEN_ENC = None


def _get_tiktoken_encoder():
    global _TIKTOKEN_ENC
    if _TIKTOKEN_ENC is None:
        try:
            import tiktoken
            _TIKTOKEN_ENC = tiktoken.get_encoding("cl100k_base")
        except ImportError:
            return None
    return _TIKTOKEN_ENC


def count_tokens(text: str) -> int:
    if not text:
        return 0
    enc = _get_tiktoken_encoder()
    return len(enc.encode(text)) if enc is not None else len(text.split())


def _safe_read_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse JSON file {path}: {e}")
        return None


def _iter_jsonl(path: Path) -> Iterable[dict]:
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def compress_sequence(seq: list[str]) -> list[str]:
    return [cat for cat, _ in groupby(seq)]


def extract_categories(segmented_record: dict) -> list[str]:
    seg = segmented_record.get("segmentation_result")
    if not isinstance(seg, dict) or not seg.get("success", False):
        return []
    steps = seg.get("steps", [])
    if not isinstance(steps, list):
        return []
    seq: list[str] = []
    for step in steps:
        if not isinstance(step, dict):
            continue
        cat = step.get("category")
        if cat in CATEGORIES:
            seq.append(cat)
    return seq


def ngrams(seq: list[str], n: int) -> set[tuple[str, ...]]:
    if n <= 0:
        return set()
    return {tuple(seq[i : i + n]) for i in range(len(seq) - n + 1)}


def try_fisher_exact_p(table_2x2: list[list[int]]) -> float:
    """
    Two-sided Fisher exact p-value for 2x2 table.
    Uses SciPy if available; otherwise returns 1.0 (still ranks by support/ratio).
    """
    try:
        from scipy.stats import fisher_exact  # type: ignore

        _, p = fisher_exact(table_2x2, alternative="two-sided")
        return float(p)
    except Exception:
        # Fallback: exact two-sided Fisher p-value via hypergeometric probabilities.
        # Table:
        #   [a b]
        #   [c d]
        try:
            a = int(table_2x2[0][0])
            b = int(table_2x2[0][1])
            c = int(table_2x2[1][0])
            d = int(table_2x2[1][1])
        except Exception:
            return 1.0

        r1 = a + b
        r2 = c + d
        c1 = a + c
        c2 = b + d
        n = r1 + r2
        if n <= 0:
            return 1.0

        lo = max(0, c1 - r2)
        hi = min(r1, c1)
        if lo > hi:
            return 1.0

        def log_comb(nn: int, kk: int) -> float:
            if kk < 0 or kk > nn:
                return float("-inf")
            return math.lgamma(nn + 1) - math.lgamma(kk + 1) - math.lgamma(nn - kk + 1)

        def hypergeom_prob(aa: int) -> float:
            # P(A=aa) where A is the top-left cell given fixed margins.
            bb = r1 - aa
            if bb < 0 or bb > c2:
                return 0.0
            logp = log_comb(c1, aa) + log_comb(c2, bb) - log_comb(n, r1)
            if not math.isfinite(logp):
                return 0.0
            return float(math.exp(logp))

        p_obs = hypergeom_prob(a)
        if p_obs <= 0.0:
            return 1.0

        p_two_sided = 0.0
        # Two-sided p-value: sum probs <= observed probability.
        tol = 1e-12
        for aa in range(lo, hi + 1):
            p_i = hypergeom_prob(aa)
            if p_i <= p_obs + tol:
                p_two_sided += p_i

        return float(min(max(p_two_sided, 0.0), 1.0))


def load_test_results(path: Path) -> dict[str, bool]:
    """
    Load test results JSON:
      - generation/debug: results.json
      - execution: result.json
    Returns: {task_id: passed_bool}
    """
    data = _safe_read_json(path)
    if not data:
        return {}
    results: dict[str, bool] = {}
    items = data.get("results", [])
    if not isinstance(items, list):
        return {}
    for item in items:
        if not isinstance(item, dict):
            continue
        task_id = item.get("task_id")
        if task_id is None:
            continue
        failed = item.get("failed", 0)
        try:
            results[str(task_id)] = int(failed) == 0
        except Exception:
            continue
    return results


def normalize_translation_task_id(task_id: str) -> str:
    """
    Normalize translation task IDs to:
      <direction>/<task_name>

    Supports both:
      - cpp_to_py/Foo
      - cpp_to_py_Foo
    """
    if not task_id:
        return task_id
    if "/" in task_id:
        direction, rest = task_id.split("/", 1)
        if direction in TRANSLATION_DIRECTIONS:
            return f"{direction}/{rest}"
        return task_id

    for direction in TRANSLATION_DIRECTIONS:
        prefix = f"{direction}_"
        if task_id.startswith(prefix):
            return f"{direction}/{task_id[len(prefix):]}"
    return task_id


def normalize_task_id_for_task(task_key: str, task_id: str) -> str:
    if task_key == "translation":
        return normalize_translation_task_id(task_id)
    return task_id


def normalize_result_map_keys(task_key: str, data: dict[str, Any]) -> dict[str, Any]:
    if task_key != "translation":
        return data
    out: dict[str, Any] = {}
    for k, v in data.items():
        out[normalize_translation_task_id(str(k))] = v
    return out


def load_aggregated_judge(path: Path) -> dict[str, dict]:
    """
    Load RQ2 aggregated results JSON and key by task_id.
    """
    data = _safe_read_json(path)
    if not data:
        return {}
    out: dict[str, dict] = {}
    items = data.get("results", [])
    if not isinstance(items, list):
        return {}
    for item in items:
        if not isinstance(item, dict):
            continue
        task_id = item.get("task_id")
        if task_id is None:
            continue
        out[str(task_id)] = item
    return out


def compute_transition_matrix(seqs: list[list[str]]) -> list[list[float]]:
    """
    Compute row-normalized transition matrix (8x8).
    """
    n = len(CATEGORIES)
    counts = [[0.0 for _ in range(n)] for _ in range(n)]
    for seq in seqs:
        if len(seq) < 2:
            continue
        for a, b in zip(seq[:-1], seq[1:]):
            ia = CAT_TO_IDX.get(a)
            ib = CAT_TO_IDX.get(b)
            if ia is None or ib is None:
                continue
            counts[ia][ib] += 1.0

    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        row_sum = sum(counts[i]) or 1.0
        for j in range(n):
            matrix[i][j] = counts[i][j] / row_sum
    return matrix


def stationary_distribution_power_iteration(matrix: list[list[float]], max_iters: int = 2000, tol: float = 1e-10) -> list[float]:
    """
    Approximate stationary distribution π for row-stochastic matrix using power iteration.
    """
    n = len(matrix)
    if n == 0:
        return []
    pi = [1.0 / n for _ in range(n)]
    for _ in range(max_iters):
        nxt = [0.0 for _ in range(n)]
        for i in range(n):
            for j in range(n):
                nxt[j] += pi[i] * matrix[i][j]
        s = sum(nxt)
        if s > 0:
            nxt = [x / s for x in nxt]
        diff = sum(abs(nxt[i] - pi[i]) for i in range(n))
        pi = nxt
        if diff < tol:
            break
    return pi


def transition_entropy_bits(row: list[float]) -> float:
    return -sum(p * math.log2(p) for p in row if p > 0.0)


def markov_metrics(matrix: list[list[float]], coupling_topk: int = 10) -> dict[str, Any]:
    """
    Compute minimal Markov metrics:
      - stationary distribution
      - row entropies + global entropy
      - coupling strengths (top pairs): P(i->j)*P(j->i)
    """
    n = len(matrix)
    pi = stationary_distribution_power_iteration(matrix)
    row_ent = [transition_entropy_bits(matrix[i]) for i in range(n)]
    global_ent = sum((pi[i] if i < len(pi) else 0.0) * row_ent[i] for i in range(n))

    couplings: list[dict[str, Any]] = []
    for i in range(n):
        for j in range(i + 1, n):
            c = matrix[i][j] * matrix[j][i]
            if c <= 0.0:
                continue
            couplings.append({"pair": f"{CATEGORIES[i]}-{CATEGORIES[j]}", "strength": c})
    couplings.sort(key=lambda x: -x["strength"])

    return {
        "stationary": {CATEGORIES[i]: round(float(pi[i]), 6) for i in range(n)} if len(pi) == n else {},
        "row_entropy_bits": {CATEGORIES[i]: round(float(row_ent[i]), 6) for i in range(n)},
        "global_entropy_bits": round(float(global_ent), 6),
        "top_couplings": [
            {"pair": c["pair"], "strength": round(float(c["strength"]), 8)} for c in couplings[:coupling_topk]
        ],
    }


def diff_matrix(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    n = min(len(a), len(b))
    out: list[list[float]] = []
    for i in range(n):
        row = []
        for j in range(min(len(a[i]), len(b[i]))):
            row.append(a[i][j] - b[i][j])
        out.append(row)
    return out


@dataclass(frozen=True)
class TaskConfig:
    seg_task_dir: str
    rq2_task_key: str
    has_test: bool


TASKS: dict[str, TaskConfig] = {
    "generation": TaskConfig(seg_task_dir="Generate_COT", rq2_task_key="generation", has_test=True),
    "execution": TaskConfig(seg_task_dir="Execution_COT", rq2_task_key="execution", has_test=True),
    "debug": TaskConfig(seg_task_dir="Debug_COT", rq2_task_key="debug", has_test=True),
    "translation": TaskConfig(seg_task_dir="Translation_COT", rq2_task_key="translation", has_test=True),
}


def resolve_tasks(task_args: list[str]) -> list[str]:
    if not task_args:
        return ["generation", "execution", "debug", "translation"]
    tasks: list[str] = []
    for t in task_args:
        t = t.strip()
        if not t:
            continue
        if t not in TASKS:
            raise ValueError(f"Unknown task '{t}'. Available: {sorted(TASKS.keys())}")
        tasks.append(t)
    # De-dup while preserving order
    seen = set()
    out = []
    for t in tasks:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def find_seg_file(seg_root: Path, seg_task_dir: str, cot_model: str) -> Optional[Path]:
    expected = seg_root / seg_task_dir / cot_model / "segmented_results.jsonl"
    if expected.exists():
        return expected
    candidates = list(seg_root.glob(f"**/{seg_task_dir}/{cot_model}/segmented_results.jsonl"))
    if candidates:
        return sorted(candidates)[0]
    return None


def load_segmented_samples(seg_path: Path, task_name: str, min_steps: int) -> list[dict[str, Any]]:
    samples: list[dict[str, Any]] = []
    for rec in _iter_jsonl(seg_path):
        task_id = rec.get("task_id")
        if task_id is None:
            continue
        raw_seq = extract_categories(rec)
        if len(raw_seq) < min_steps:
            continue
        # Extract original COT text for token counting
        original_cot = rec.get("original_cot", "")
        if not isinstance(original_cot, str):
            original_cot = ""
        samples.append(
            {
                "task_id": str(task_id),
                "task": task_name,
                "raw_seq": raw_seq,
                "compressed_seq": compress_sequence(raw_seq),
                "original_cot": original_cot,
            }
        )
    return samples


def calc_category_distribution(seq: list[str]) -> dict[str, float]:
    total = len(seq) or 1
    counts = {cat: 0 for cat in CATEGORIES}
    for c in seq:
        if c in counts:
            counts[c] += 1
    return {cat: counts[cat] / total for cat in CATEGORIES}


def compute_basic_features(sample: dict[str, Any]) -> dict[str, Any]:
    raw = sample["raw_seq"]
    comp = sample["compressed_seq"]
    original_cot = sample.get("original_cot", "")
    token_count = count_tokens(original_cot)
    char_count = len(original_cot)
    return {
        "len_raw": len(raw),
        "len_compressed": len(comp),
        "compress_ratio": (len(comp) / len(raw)) if len(raw) else 0.0,
        "first": raw[0] if raw else None,
        "last": raw[-1] if raw else None,
        "dist": calc_category_distribution(raw),
        "token_count": token_count,
        "char_count": char_count,
    }


def quadrant_label(judge_is_valid: bool, test_pass: bool) -> str:
    if judge_is_valid and test_pass:
        return "TP"
    if judge_is_valid and not test_pass:
        return "FP"
    if (not judge_is_valid) and test_pass:
        return "FN"
    return "TN"


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k) for k in fieldnames})


def add_bh_fdr(rows: list[dict[str, Any]], p_key: str = "p_value", q_key: str = "q_value") -> None:
    m = len(rows)
    if m == 0:
        return

    order = sorted(range(m), key=lambda i: float(rows[i].get(p_key, 1.0)))
    raw_q = [1.0 for _ in range(m)]

    for rank, idx in enumerate(order, start=1):
        p = float(rows[idx].get(p_key, 1.0))
        p = min(max(p, 0.0), 1.0)
        raw_q[idx] = (p * m) / rank

    running_min = 1.0
    for idx in reversed(order):
        running_min = min(running_min, raw_q[idx])
        rows[idx][q_key] = round(min(max(running_min, 0.0), 1.0), 12)


def mine_discriminative_patterns(
    records: list[dict[str, Any]],
    group_key: str,
    group_a: str,
    group_b: str,
    n_sizes: list[int],
    min_support: float,
    min_count: int,
    min_delta: float,
    topk: int,
    task_filter: Optional[str] = None,
    examples_per_group: int = 0,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """
    Presence-based n-gram comparison between group_a and group_b.
    Returns (rows, meta).
    """
    filtered = [
        r
        for r in records
        if r.get(group_key) in (group_a, group_b) and (task_filter is None or r.get("task") == task_filter)
    ]
    group_a_recs = [r for r in filtered if r.get(group_key) == group_a]
    group_b_recs = [r for r in filtered if r.get(group_key) == group_b]
    total_a = len(group_a_recs)
    total_b = len(group_b_recs)
    if total_a == 0 or total_b == 0:
        return [], {"total_a": total_a, "total_b": total_b}

    presence_a: dict[tuple[str, ...], int] = {}
    presence_b: dict[tuple[str, ...], int] = {}
    examples_a: dict[tuple[str, ...], list[str]] = {}
    examples_b: dict[tuple[str, ...], list[str]] = {}

    def add_presence(
        presence: dict[tuple[str, ...], int],
        examples: dict[tuple[str, ...], list[str]],
        recs: list[dict[str, Any]],
    ):
        for r in recs:
            seq = r.get("compressed_seq", [])
            if not isinstance(seq, list):
                continue
            task_id = str(r.get("task_id", ""))
            pats: set[tuple[str, ...]] = set()
            for n in n_sizes:
                pats |= ngrams(seq, n)
            for p in pats:
                presence[p] = presence.get(p, 0) + 1
                if examples_per_group > 0:
                    lst = examples.get(p)
                    if lst is None:
                        lst = []
                        examples[p] = lst
                    if len(lst) < examples_per_group:
                        lst.append(task_id)

    add_presence(presence_a, examples_a, group_a_recs)
    add_presence(presence_b, examples_b, group_b_recs)

    all_patterns = set(presence_a.keys()) | set(presence_b.keys())
    rows: list[dict[str, Any]] = []
    eps = 1e-12

    for p in all_patterns:
        count_a = presence_a.get(p, 0)
        count_b = presence_b.get(p, 0)
        support_a = count_a / total_a
        support_b = count_b / total_b
        if max(support_a, support_b) < min_support:
            continue
        if max(count_a, count_b) < min_count:
            continue
        if abs(support_a - support_b) < min_delta:
            continue

        table = [[count_a, count_b], [total_a - count_a, total_b - count_b]]
        p_value = try_fisher_exact_p(table)

        ratio = (support_a + eps) / (support_b + eps)
        enriched_in = group_a if support_a >= support_b else group_b
        rows.append(
            {
                "task": task_filter or "ALL",
                "group_key": group_key,
                "group_a": group_a,
                "group_b": group_b,
                "pattern": "->".join(p),
                "n": len(p),
                "count_a": count_a,
                "total_a": total_a,
                "support_a": round(support_a, 6),
                "count_b": count_b,
                "total_b": total_b,
                "support_b": round(support_b, 6),
                "delta_support": round(support_a - support_b, 6),
                "ratio_a_over_b": round(ratio, 6),
                "p_value": round(p_value, 12),
                "enriched_in": enriched_in,
                "examples_a": ";".join(examples_a.get(p, [])[:examples_per_group]) if examples_per_group > 0 else "",
                "examples_b": ";".join(examples_b.get(p, [])[:examples_per_group]) if examples_per_group > 0 else "",
            }
        )

    add_bh_fdr(rows, p_key="p_value", q_key="q_value")
    rows.sort(key=lambda r: (r["q_value"], r["p_value"], -abs(r["delta_support"]), -r["ratio_a_over_b"]))
    return rows[:topk], {"total_a": total_a, "total_b": total_b, "num_patterns": len(rows)}


def group_basic_stats(records: list[dict[str, Any]], group_key: str, group_value: str, task: Optional[str]) -> dict[str, Any]:
    subset = [r for r in records if r.get(group_key) == group_value and (task is None or r.get("task") == task)]
    if not subset:
        return {"count": 0}
    lens_raw = [r["len_raw"] for r in subset if isinstance(r.get("len_raw"), int)]
    lens_comp = [r["len_compressed"] for r in subset if isinstance(r.get("len_compressed"), int)]
    ratios = [r["compress_ratio"] for r in subset if isinstance(r.get("compress_ratio"), float)]
    token_counts = [r["token_count"] for r in subset if isinstance(r.get("token_count"), int)]
    char_counts = [r["char_count"] for r in subset if isinstance(r.get("char_count"), int)]
    
    def _mean(xs: list[float]) -> float:
        return float(sum(xs) / len(xs)) if xs else 0.0
    
    def _std(xs: list[float]) -> float:
        if len(xs) < 2:
            return 0.0
        m = _mean(xs)
        return float(math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs)))
    
    def _median(xs: list[float]) -> float:
        if not xs:
            return 0.0
        s = sorted(xs)
        n = len(s)
        if n % 2 == 1:
            return float(s[n // 2])
        return float((s[n // 2 - 1] + s[n // 2]) / 2)
    
    dist_avg = {cat: 0.0 for cat in CATEGORIES}
    for r in subset:
        d = r.get("dist", {})
        if not isinstance(d, dict):
            continue
        for cat in CATEGORIES:
            dist_avg[cat] += float(d.get(cat, 0.0))
    for cat in CATEGORIES:
        dist_avg[cat] = dist_avg[cat] / len(subset)
    
    return {
        "count": len(subset),
        "mean_len_raw": round(_mean([float(x) for x in lens_raw]), 4),
        "mean_len_compressed": round(_mean([float(x) for x in lens_comp]), 4),
        "mean_compress_ratio": round(_mean(ratios), 6),
        "avg_category_dist": {k: round(v, 6) for k, v in dist_avg.items()},
        "mean_token_count": round(_mean([float(x) for x in token_counts]), 2),
        "std_token_count": round(_std([float(x) for x in token_counts]), 2),
        "median_token_count": round(_median([float(x) for x in token_counts]), 2),
        "min_token_count": min(token_counts) if token_counts else 0,
        "max_token_count": max(token_counts) if token_counts else 0,
        "mean_char_count": round(_mean([float(x) for x in char_counts]), 2),
    }


def safe_div(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else 0.0


def build_efficiency_metrics(stats: dict[str, Any]) -> dict[str, Any]:
    count = int(stats.get("count", 0) or 0)
    if count <= 0:
        return {"count": 0}

    dist = stats.get("avg_category_dist", {})
    if not isinstance(dist, dict):
        dist = {}

    pu = float(dist.get("PU", 0.0))
    sd = float(dist.get("SD", 0.0))
    ip = float(dist.get("IP", 0.0))
    cc = float(dist.get("CC", 0.0))
    vv = float(dist.get("VV", 0.0))
    kr = float(dist.get("KR", 0.0))
    mr = float(dist.get("MR", 0.0))
    aux = float(dist.get("AUX", 0.0))

    mean_len_raw = float(stats.get("mean_len_raw", 0.0) or 0.0)
    mean_len_compressed = float(stats.get("mean_len_compressed", 0.0) or 0.0)
    mean_token_count = float(stats.get("mean_token_count", 0.0) or 0.0)
    mean_char_count = float(stats.get("mean_char_count", 0.0) or 0.0)
    mean_compress_ratio = float(stats.get("mean_compress_ratio", 0.0) or 0.0)

    closure_share = vv + cc + aux
    drift_share = sd + mr + kr
    implementation_share = ip + vv + aux
    planning_share = pu + sd + kr

    return {
        "count": count,
        "token_per_raw_step": round(safe_div(mean_token_count, mean_len_raw), 4),
        "token_per_compressed_step": round(safe_div(mean_token_count, mean_len_compressed), 4),
        "char_per_token": round(safe_div(mean_char_count, mean_token_count), 4),
        "compress_ratio": round(mean_compress_ratio, 6),
        "verification_share": round(vv, 6),
        "closure_share": round(closure_share, 6),
        "drift_share": round(drift_share, 6),
        "implementation_share": round(implementation_share, 6),
        "planning_share": round(planning_share, 6),
        "closure_minus_drift": round(closure_share - drift_share, 6),
    }


def _taxonomy_entry(
    profile: dict[str, Any],
    *,
    metric_type: str,
    key: str,
    focus_title: str,
    contrast_title: str,
    evidence_label: str,
    focus_medium: float,
    focus_strong: float,
    favor_lower: bool = False,
) -> Optional[dict[str, Any]]:
    favor: Optional[str] = None
    strength: Optional[str] = None
    title = ""
    if metric_type == "ratio":
        value = float(profile.get("ratios", {}).get(key, 0.0) or 0.0)
        if value <= 0.0:
            return None
        if value <= focus_strong:
            favor, strength, title = "focus", "strong", focus_title
        elif value <= focus_medium:
            favor, strength, title = "focus", "medium", focus_title
        elif (contrast_strong := safe_div(1.0, focus_strong)) and value >= contrast_strong:
            favor, strength, title = "contrast", "strong", contrast_title
        elif (contrast_medium := safe_div(1.0, focus_medium)) and value >= contrast_medium:
            favor, strength, title = "contrast", "medium", contrast_title
        evidence = f"{evidence_label} {value:.3f}"
    else:
        value = float(profile.get("deltas", {}).get(key, 0.0) or 0.0)
        signed = -value if favor_lower else value
        if signed >= focus_strong:
            favor, strength, title = "focus", "strong", focus_title
        elif signed >= focus_medium:
            favor, strength, title = "focus", "medium", focus_title
        elif signed <= -focus_strong:
            favor, strength, title = "contrast", "strong", contrast_title
        elif signed <= -focus_medium:
            favor, strength, title = "contrast", "medium", contrast_title
        evidence = f"{evidence_label} {value:+.3f}"

    if not favor or not strength:
        return None

    return {
        "id": key,
        "title": title,
        "favor": favor,
        "strength": strength,
        "metric_type": metric_type,
        "metric_key": key,
        "value": round(value, 6),
        "evidence": evidence,
    }


def build_pattern_taxonomy(profile: dict[str, Any]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []

    specs = [
        {
            "metric_type": "ratio",
            "key": "mean_token_count",
            "focus_title": "精简 Token",
            "contrast_title": "Token 膨胀",
            "evidence_label": "token ratio",
            "focus_medium": 0.85,
            "focus_strong": 0.70,
        },
        {
            "metric_type": "ratio",
            "key": "mean_len_raw",
            "focus_title": "步骤更紧凑",
            "contrast_title": "步骤拖长",
            "evidence_label": "raw-step ratio",
            "focus_medium": 0.90,
            "focus_strong": 0.75,
        },
        {
            "metric_type": "ratio",
            "key": "token_per_raw_step",
            "focus_title": "单位步骤更省 Token",
            "contrast_title": "单位步骤更啰嗦",
            "evidence_label": "token/raw-step ratio",
            "focus_medium": 0.92,
            "focus_strong": 0.82,
        },
        {
            "metric_type": "delta",
            "key": "mean_compress_ratio",
            "focus_title": "压缩率更高",
            "contrast_title": "压缩率走弱",
            "evidence_label": "compress-ratio delta",
            "focus_medium": 0.03,
            "focus_strong": 0.06,
        },
        {
            "metric_type": "delta",
            "key": "verification_share",
            "focus_title": "验证驱动增强",
            "contrast_title": "验证驱动减弱",
            "evidence_label": "verification delta",
            "focus_medium": 0.03,
            "focus_strong": 0.08,
        },
        {
            "metric_type": "delta",
            "key": "closure_share",
            "focus_title": "收敛更强",
            "contrast_title": "收敛走弱",
            "evidence_label": "closure delta",
            "focus_medium": 0.04,
            "focus_strong": 0.10,
        },
        {
            "metric_type": "delta",
            "key": "drift_share",
            "focus_title": "漂移受控",
            "contrast_title": "漂移加重",
            "evidence_label": "drift delta",
            "focus_medium": 0.05,
            "focus_strong": 0.12,
            "favor_lower": True,
        },
        {
            "metric_type": "delta",
            "key": "implementation_share",
            "focus_title": "实现推进更强",
            "contrast_title": "实现推进不足",
            "evidence_label": "implementation delta",
            "focus_medium": 0.04,
            "focus_strong": 0.10,
        },
        {
            "metric_type": "delta",
            "key": "planning_share",
            "focus_title": "规划开销更低",
            "contrast_title": "规划负担更高",
            "evidence_label": "planning delta",
            "focus_medium": 0.04,
            "focus_strong": 0.10,
            "favor_lower": True,
        },
        {
            "metric_type": "delta",
            "key": "closure_minus_drift",
            "focus_title": "闭环平衡更强",
            "contrast_title": "闭环平衡更弱",
            "evidence_label": "closure-minus-drift delta",
            "focus_medium": 0.08,
            "focus_strong": 0.18,
        },
    ]

    for spec in specs:
        entry = _taxonomy_entry(profile, **spec)
        if entry:
            entries.append(entry)

    focus_entries = sorted(
        [e for e in entries if e["favor"] == "focus"],
        key=lambda x: (x["strength"] != "strong", x["title"]),
    )
    contrast_entries = sorted(
        [e for e in entries if e["favor"] == "contrast"],
        key=lambda x: (x["strength"] != "strong", x["title"]),
    )
    return {
        "focus_patterns": focus_entries,
        "contrast_patterns": contrast_entries,
        "focus_titles": [e["title"] for e in focus_entries],
        "contrast_titles": [e["title"] for e in contrast_entries],
    }


def build_efficiency_profile(
    focus_stats: dict[str, Any],
    contrast_stats: dict[str, Any],
    *,
    focus_label: str,
    contrast_label: str,
) -> dict[str, Any]:
    focus_metrics = build_efficiency_metrics(focus_stats)
    contrast_metrics = build_efficiency_metrics(contrast_stats)
    if focus_metrics.get("count", 0) <= 0 or contrast_metrics.get("count", 0) <= 0:
        return {
            "focus_label": focus_label,
            "contrast_label": contrast_label,
            "focus_metrics": focus_metrics,
            "contrast_metrics": contrast_metrics,
            "deltas": {},
            "ratios": {},
            "tags": [],
        }

    def _delta(key: str, digits: int = 6) -> float:
        return round(float(focus_metrics.get(key, 0.0)) - float(contrast_metrics.get(key, 0.0)), digits)

    def _ratio_from_stats(key: str, digits: int = 6) -> float:
        return round(
            safe_div(float(focus_stats.get(key, 0.0) or 0.0), float(contrast_stats.get(key, 0.0) or 0.0)),
            digits,
        )

    def _ratio_from_metrics(key: str, digits: int = 6) -> float:
        return round(
            safe_div(float(focus_metrics.get(key, 0.0) or 0.0), float(contrast_metrics.get(key, 0.0) or 0.0)),
            digits,
        )

    deltas = {
        "mean_token_count": round(
            float(focus_stats.get("mean_token_count", 0.0) or 0.0) - float(contrast_stats.get("mean_token_count", 0.0) or 0.0),
            2,
        ),
        "mean_len_raw": round(
            float(focus_stats.get("mean_len_raw", 0.0) or 0.0) - float(contrast_stats.get("mean_len_raw", 0.0) or 0.0),
            4,
        ),
        "mean_len_compressed": round(
            float(focus_stats.get("mean_len_compressed", 0.0) or 0.0) - float(contrast_stats.get("mean_len_compressed", 0.0) or 0.0),
            4,
        ),
        "mean_compress_ratio": round(
            float(focus_stats.get("mean_compress_ratio", 0.0) or 0.0) - float(contrast_stats.get("mean_compress_ratio", 0.0) or 0.0),
            6,
        ),
        "token_per_raw_step": _delta("token_per_raw_step", 4),
        "token_per_compressed_step": _delta("token_per_compressed_step", 4),
        "verification_share": _delta("verification_share"),
        "closure_share": _delta("closure_share"),
        "drift_share": _delta("drift_share"),
        "implementation_share": _delta("implementation_share"),
        "planning_share": _delta("planning_share"),
        "closure_minus_drift": _delta("closure_minus_drift"),
    }

    ratios = {
        "mean_token_count": _ratio_from_stats("mean_token_count"),
        "mean_len_raw": _ratio_from_stats("mean_len_raw"),
        "mean_len_compressed": _ratio_from_stats("mean_len_compressed"),
        "mean_compress_ratio": _ratio_from_stats("mean_compress_ratio"),
        "token_per_raw_step": _ratio_from_metrics("token_per_raw_step"),
        "token_per_compressed_step": _ratio_from_metrics("token_per_compressed_step"),
    }

    tags: list[str] = []
    if ratios["mean_token_count"] and ratios["mean_token_count"] <= 0.85:
        tags.append("leaner_tokens")
    if ratios["mean_len_raw"] and ratios["mean_len_raw"] <= 0.90:
        tags.append("fewer_steps")
    if deltas["mean_compress_ratio"] >= 0.03:
        tags.append("higher_compression")
    if deltas["verification_share"] >= 0.03:
        tags.append("verification_forward")
    if deltas["closure_share"] >= 0.04:
        tags.append("closure_heavier")
    if deltas["drift_share"] <= -0.05:
        tags.append("drift_suppressed")
    if deltas["implementation_share"] >= 0.04:
        tags.append("implementation_oriented")
    if deltas["planning_share"] <= -0.04:
        tags.append("less_planning_overhead")
    if deltas["closure_minus_drift"] >= 0.08:
        tags.append("stronger_closure_balance")
    if not tags:
        tags.append("mixed_profile")

    return {
        "focus_label": focus_label,
        "contrast_label": contrast_label,
        "focus_metrics": focus_metrics,
        "contrast_metrics": contrast_metrics,
        "deltas": deltas,
        "ratios": ratios,
        "tags": tags,
        "taxonomy": build_pattern_taxonomy(
            {
                "focus_label": focus_label,
                "contrast_label": contrast_label,
                "deltas": deltas,
                "ratios": ratios,
            }
        ),
    }


def build_efficiency_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def _append_row(scope: str, task_name: str, comparison: str, profile: dict[str, Any]) -> None:
        if not profile or not profile.get("focus_metrics", {}).get("count"):
            return
        rows.append(
            {
                "scope": scope,
                "task": task_name,
                "comparison": comparison,
                "focus_label": profile.get("focus_label", ""),
                "contrast_label": profile.get("contrast_label", ""),
                "focus_count": profile.get("focus_metrics", {}).get("count", 0),
                "contrast_count": profile.get("contrast_metrics", {}).get("count", 0),
                "token_ratio": profile.get("ratios", {}).get("mean_token_count", 0.0),
                "raw_step_ratio": profile.get("ratios", {}).get("mean_len_raw", 0.0),
                "compress_ratio_delta": profile.get("deltas", {}).get("mean_compress_ratio", 0.0),
                "token_per_raw_step_delta": profile.get("deltas", {}).get("token_per_raw_step", 0.0),
                "verification_share_delta": profile.get("deltas", {}).get("verification_share", 0.0),
                "closure_share_delta": profile.get("deltas", {}).get("closure_share", 0.0),
                "drift_share_delta": profile.get("deltas", {}).get("drift_share", 0.0),
                "implementation_share_delta": profile.get("deltas", {}).get("implementation_share", 0.0),
                "closure_minus_drift_delta": profile.get("deltas", {}).get("closure_minus_drift", 0.0),
                "tags": ",".join(profile.get("tags", [])),
                "focus_patterns": ",".join(profile.get("taxonomy", {}).get("focus_titles", [])),
                "contrast_patterns": ",".join(profile.get("taxonomy", {}).get("contrast_titles", [])),
            }
        )

    global_profiles = summary.get("global", {}).get("profiles", {})
    for comparison, profile in global_profiles.items():
        _append_row("global", "ALL", comparison, profile)

    for task_name, task_block in summary.get("by_task", {}).items():
        for comparison, profile in task_block.get("profiles", {}).items():
            _append_row("task", task_name, comparison, profile)

    return rows


def parse_int_list(csv_text: str) -> list[int]:
    return [int(part.strip()) for part in csv_text.split(",") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Mine patterns on segmented CoTs with RQ2 correctness labels")
    parser.add_argument("--cot-model", type=str, default="r1", help="CoT model (default: qwen)")
    parser.add_argument(
        "--tasks",
        type=str,
        default="generation,execution,debug,translation",
        help="Comma-separated tasks (default: generation,execution,debug,translation)",
    )
    parser.add_argument("--seg-root", type=str, default="data/derived_cot/rq1_segmented")
    parser.add_argument("--rq2-results-root", type=str, default="data/derived_cot/rq2_judging")
    parser.add_argument("--rq2-test-root", type=str, default="data/derived_cot/rq2_eval")
    parser.add_argument("--output-dir", type=str, default=None, help="Output dir (default: data/derived_cot/rq2_patterns/<cot_model>/)")
    parser.add_argument("--ngram-sizes", type=str, default="3,4,5", help="Comma-separated n-gram sizes (default: 2,3,4)")
    parser.add_argument("--min-support", type=float, default=0.03, help="Min support threshold (default: 0.03)")
    parser.add_argument("--min-count", type=int, default=5, help="Min count in enriched group (default: 5)")
    parser.add_argument("--min-delta", type=float, default=0.05, help="Min |delta_support| (default: 0.05)")
    parser.add_argument("--topk", type=int, default=50, help="Top-K patterns to save per comparison (default: 50)")
    parser.add_argument("--examples-per-pattern", type=int, default=5, help="How many task_id examples to attach per pattern per group (default: 5)")
    parser.add_argument("--min-steps", type=int, default=2, help="Minimum raw steps to keep a sample (default: 2)")
    parser.add_argument("--include-judge-patterns", action="store_true", help="Also output judge invalid vs valid patterns")
    parser.add_argument(
        "--topology-seq",
        type=str,
        default="compressed",
        choices=["compressed", "raw"],
        help="Which sequence to use for topology/Markov metrics (default: compressed)",
    )
    args = parser.parse_args()

    cot_model = args.cot_model
    tasks = resolve_tasks([t.strip() for t in args.tasks.split(",") if t.strip()])
    n_sizes = parse_int_list(args.ngram_sizes)

    seg_root = Path(args.seg_root)
    rq2_results_root = Path(args.rq2_results_root) / cot_model
    rq2_test_root = Path(args.rq2_test_root)
    out_dir = Path(args.output_dir) if args.output_dir else Path("data/derived_cot/rq2_patterns") / cot_model
    out_dir.mkdir(parents=True, exist_ok=True)

    seg_samples: list[dict[str, Any]] = []
    seg_coverage: dict[str, Any] = {}
    for t in tasks:
        cfg = TASKS[t]
        seg_file = find_seg_file(seg_root, cfg.seg_task_dir, cot_model)
        if not seg_file:
            seg_coverage[t] = {"seg_file": None, "seg_count": 0}
            continue
        samples = load_segmented_samples(seg_file, cfg.rq2_task_key, args.min_steps)
        seg_samples.extend(samples)
        seg_coverage[t] = {"seg_file": str(seg_file), "seg_count": len(samples)}

    judge_maps: dict[str, dict[str, dict]] = {}
    for t in tasks:
        cfg = TASKS[t]
        agg_file = rq2_results_root / f"aggregated_{cfg.rq2_task_key}.json"
        judge_maps[cfg.rq2_task_key] = normalize_result_map_keys(cfg.rq2_task_key, load_aggregated_judge(agg_file))

    test_maps: dict[str, dict[str, bool]] = {}
    test_task_keys = sorted({TASKS[t].rq2_task_key for t in tasks if TASKS[t].has_test})
    for task_key in test_task_keys:
        test_file: Optional[Path] = None
        if task_key == "execution":
            candidate = rq2_test_root / "execution" / cot_model / "result.json"
            if candidate.exists():
                test_file = candidate
        elif task_key in {"generation", "debug"}:
            candidate = rq2_test_root / task_key / cot_model / "results.json"
            if candidate.exists():
                test_file = candidate
        elif task_key == "translation":
            c1 = rq2_test_root / "translation" / cot_model / "result.json"
            c2 = rq2_test_root / "translation" / cot_model / "results.json"
            if c1.exists():
                test_file = c1
            elif c2.exists():
                test_file = c2

        if test_file and test_file.exists():
            test_map = load_test_results(test_file)
            test_maps[task_key] = normalize_result_map_keys(task_key, test_map)
        else:
            test_maps[task_key] = {}

    records: list[dict[str, Any]] = []
    for s in seg_samples:
        task_key = s["task"]
        lookup_task_id = normalize_task_id_for_task(task_key, str(s["task_id"]))
        judge = judge_maps.get(task_key, {}).get(lookup_task_id)
        if not judge:
            continue
        judge_is_valid = bool(judge.get("is_valid", False))
        judge_conf = float(judge.get("confidence", 0.0))

        rec = {
            **s,
            **compute_basic_features(s),
            "judge_is_valid": judge_is_valid,
            "judge_confidence": judge_conf,
            "judge_group": "valid" if judge_is_valid else "invalid",
            "test_pass": None,
            "result_group": None,
            "quad": None,
        }

        if task_key in test_maps:
            passed = test_maps[task_key].get(lookup_task_id)
            if passed is not None:
                rec["test_pass"] = bool(passed)
                rec["result_group"] = "pass" if passed else "fail"
                rec["quad"] = quadrant_label(judge_is_valid, bool(passed))

        records.append(rec)

    coverage = {
        "cot_model": cot_model,
        "tasks": tasks,
        "segmentation": seg_coverage,
        "joined_records": len(records),
        "joined_by_task": {},
        "with_test_by_task": {},
    }
    for task_key in sorted({r["task"] for r in records}):
        coverage["joined_by_task"][task_key] = sum(1 for r in records if r["task"] == task_key)
        coverage["with_test_by_task"][task_key] = sum(1 for r in records if r["task"] == task_key and r.get("quad") is not None)

    (out_dir / "coverage.json").write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")

    summary: dict[str, Any] = {"cot_model": cot_model, "by_task": {}, "global": {}}
    summary["global"]["valid"] = group_basic_stats(records, "judge_group", "valid", task=None)
    summary["global"]["invalid"] = group_basic_stats(records, "judge_group", "invalid", task=None)
    summary["global"]["pass"] = group_basic_stats(records, "result_group", "pass", task=None)
    summary["global"]["fail"] = group_basic_stats(records, "result_group", "fail", task=None)
    summary["global"]["profiles"] = {
        "pass_vs_fail": build_efficiency_profile(
            summary["global"]["pass"],
            summary["global"]["fail"],
            focus_label="pass",
            contrast_label="fail",
        ),
        "valid_vs_invalid": build_efficiency_profile(
            summary["global"]["valid"],
            summary["global"]["invalid"],
            focus_label="valid",
            contrast_label="invalid",
        ),
    }
    for task_key in sorted({r["task"] for r in records}):
        summary["by_task"].setdefault(task_key, {})
        summary["by_task"][task_key]["valid"] = group_basic_stats(records, "judge_group", "valid", task=task_key)
        summary["by_task"][task_key]["invalid"] = group_basic_stats(records, "judge_group", "invalid", task=task_key)
        summary["by_task"][task_key]["pass"] = group_basic_stats(records, "result_group", "pass", task=task_key)
        summary["by_task"][task_key]["fail"] = group_basic_stats(records, "result_group", "fail", task=task_key)
        summary["by_task"][task_key]["profiles"] = {
            "pass_vs_fail": build_efficiency_profile(
                summary["by_task"][task_key]["pass"],
                summary["by_task"][task_key]["fail"],
                focus_label="pass",
                contrast_label="fail",
            ),
            "valid_vs_invalid": build_efficiency_profile(
                summary["by_task"][task_key]["valid"],
                summary["by_task"][task_key]["invalid"],
                focus_label="valid",
                contrast_label="invalid",
            ),
        }

        for quad in ["TP", "FP", "FN", "TN"]:
            summary["by_task"][task_key][quad] = group_basic_stats(records, "quad", quad, task=task_key)

    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    efficiency_rows = build_efficiency_rows(summary)
    if efficiency_rows:
        write_csv_rows(out_dir / "efficiency_profiles.csv", efficiency_rows, list(efficiency_rows[0].keys()))

    result_records = [r for r in records if r.get("result_group") in ("pass", "fail")]
    rows_global, _ = mine_discriminative_patterns(
        result_records,
        group_key="result_group",
        group_a="fail",
        group_b="pass",
        n_sizes=n_sizes,
        min_support=args.min_support,
        min_count=args.min_count,
        min_delta=args.min_delta,
        topk=args.topk,
        task_filter=None,
        examples_per_group=args.examples_per_pattern,
    )
    if rows_global:
        write_csv_rows(
            out_dir / "patterns_fail_vs_pass_global.csv",
            rows_global,
            fieldnames=list(rows_global[0].keys()),
        )

    rows_by_task: list[dict[str, Any]] = []
    for task_key in sorted({r["task"] for r in result_records}):
        rows, _ = mine_discriminative_patterns(
            result_records,
            group_key="result_group",
            group_a="fail",
            group_b="pass",
            n_sizes=n_sizes,
            min_support=args.min_support,
            min_count=args.min_count,
            min_delta=args.min_delta,
            topk=args.topk,
            task_filter=task_key,
            examples_per_group=args.examples_per_pattern,
        )
        rows_by_task.extend(rows)
    if rows_by_task:
        write_csv_rows(
            out_dir / "patterns_fail_vs_pass_by_task.csv",
            rows_by_task,
            fieldnames=list(rows_by_task[0].keys()),
        )

    if args.include_judge_patterns:
        rows_global, _ = mine_discriminative_patterns(
            records,
            group_key="judge_group",
            group_a="invalid",
            group_b="valid",
            n_sizes=n_sizes,
            min_support=args.min_support,
            min_count=args.min_count,
            min_delta=args.min_delta,
            topk=args.topk,
            task_filter=None,
            examples_per_group=args.examples_per_pattern,
        )
        if rows_global:
            write_csv_rows(
                out_dir / "patterns_invalid_vs_valid_global.csv",
                rows_global,
                fieldnames=list(rows_global[0].keys()),
            )

        rows_by_task = []
        for task_key in sorted({r["task"] for r in records}):
            rows, _ = mine_discriminative_patterns(
                records,
                group_key="judge_group",
                group_a="invalid",
                group_b="valid",
                n_sizes=n_sizes,
                min_support=args.min_support,
                min_count=args.min_count,
                min_delta=args.min_delta,
                topk=args.topk,
                task_filter=task_key,
                examples_per_group=args.examples_per_pattern,
            )
            rows_by_task.extend(rows)
        if rows_by_task:
            write_csv_rows(
                out_dir / "patterns_invalid_vs_valid_by_task.csv",
                rows_by_task,
                fieldnames=list(rows_by_task[0].keys()),
            )

    # 6) Quadrant patterns (only when test labels exist)
    quad_records = [r for r in records if r.get("quad") in ("TP", "FP", "FN", "TN")]
    if quad_records:
        fp_tp_global, _ = mine_discriminative_patterns(
            quad_records,
            group_key="quad",
            group_a="FP",
            group_b="TP",
            n_sizes=n_sizes,
            min_support=args.min_support,
            min_count=args.min_count,
            min_delta=args.min_delta,
            topk=args.topk,
            task_filter=None,
            examples_per_group=args.examples_per_pattern,
        )
        if fp_tp_global:
            write_csv_rows(out_dir / "patterns_fp_vs_tp_global.csv", fp_tp_global, list(fp_tp_global[0].keys()))

        fn_tn_global, _ = mine_discriminative_patterns(
            quad_records,
            group_key="quad",
            group_a="FN",
            group_b="TN",
            n_sizes=n_sizes,
            min_support=args.min_support,
            min_count=args.min_count,
            min_delta=args.min_delta,
            topk=args.topk,
            task_filter=None,
            examples_per_group=args.examples_per_pattern,
        )
        if fn_tn_global:
            write_csv_rows(out_dir / "patterns_fn_vs_tn_global.csv", fn_tn_global, list(fn_tn_global[0].keys()))

        tp_tn_global, _ = mine_discriminative_patterns(
            quad_records,
            group_key="quad",
            group_a="TN",
            group_b="TP",
            n_sizes=n_sizes,
            min_support=args.min_support,
            min_count=args.min_count,
            min_delta=args.min_delta,
            topk=args.topk,
            task_filter=None,
            examples_per_group=args.examples_per_pattern,
        )
        if tp_tn_global:
            write_csv_rows(out_dir / "patterns_tn_vs_tp_global.csv", tp_tn_global, list(tp_tn_global[0].keys()))

        fp_tp_by_task: list[dict[str, Any]] = []
        fn_tn_by_task: list[dict[str, Any]] = []
        tn_tp_by_task: list[dict[str, Any]] = []
        for task_key in sorted({r["task"] for r in quad_records}):
            r1, _ = mine_discriminative_patterns(
                quad_records,
                group_key="quad",
                group_a="FP",
                group_b="TP",
                n_sizes=n_sizes,
                min_support=args.min_support,
                min_count=args.min_count,
                min_delta=args.min_delta,
                topk=args.topk,
                task_filter=task_key,
                examples_per_group=args.examples_per_pattern,
            )
            fp_tp_by_task.extend(r1)

            r2, _ = mine_discriminative_patterns(
                quad_records,
                group_key="quad",
                group_a="FN",
                group_b="TN",
                n_sizes=n_sizes,
                min_support=args.min_support,
                min_count=args.min_count,
                min_delta=args.min_delta,
                topk=args.topk,
                task_filter=task_key,
                examples_per_group=args.examples_per_pattern,
            )
            fn_tn_by_task.extend(r2)

            r3, _ = mine_discriminative_patterns(
                quad_records,
                group_key="quad",
                group_a="TN",
                group_b="TP",
                n_sizes=n_sizes,
                min_support=args.min_support,
                min_count=args.min_count,
                min_delta=args.min_delta,
                topk=args.topk,
                task_filter=task_key,
                examples_per_group=args.examples_per_pattern,
            )
            tn_tp_by_task.extend(r3)

        if fp_tp_by_task:
            write_csv_rows(out_dir / "patterns_fp_vs_tp_by_task.csv", fp_tp_by_task, list(fp_tp_by_task[0].keys()))
        if fn_tn_by_task:
            write_csv_rows(out_dir / "patterns_fn_vs_tn_by_task.csv", fn_tn_by_task, list(fn_tn_by_task[0].keys()))
        if tn_tp_by_task:
            write_csv_rows(out_dir / "patterns_tn_vs_tp_by_task.csv", tn_tp_by_task, list(tn_tp_by_task[0].keys()))

    seq_key = "compressed_seq" if args.topology_seq == "compressed" else "raw_seq"
    topology: dict[str, Any] = {"cot_model": cot_model, "sequence": args.topology_seq, "global": {}, "by_task": {}}

    def collect_seqs(subset: list[dict[str, Any]]) -> list[list[str]]:
        seqs: list[list[str]] = []
        for r in subset:
            s = r.get(seq_key, [])
            if isinstance(s, list) and len(s) >= 2:
                seqs.append([x for x in s if x in CAT_TO_IDX])
        return seqs

    pass_recs = [r for r in records if r.get("result_group") == "pass"]
    fail_recs = [r for r in records if r.get("result_group") == "fail"]
    if pass_recs or fail_recs:
        mat_pass = compute_transition_matrix(collect_seqs(pass_recs))
        mat_fail = compute_transition_matrix(collect_seqs(fail_recs))
        topology["global"]["result_group"] = {
            "pass": {"matrix": mat_pass, **markov_metrics(mat_pass)},
            "fail": {"matrix": mat_fail, **markov_metrics(mat_fail)},
            "diff_fail_minus_pass": diff_matrix(mat_fail, mat_pass),
        }

    valid_recs = [r for r in records if r.get("judge_group") == "valid"]
    invalid_recs = [r for r in records if r.get("judge_group") == "invalid"]
    mat_valid = compute_transition_matrix(collect_seqs(valid_recs))
    mat_invalid = compute_transition_matrix(collect_seqs(invalid_recs))
    topology["global"]["judge_group"] = {
        "valid": {"matrix": mat_valid, **markov_metrics(mat_valid)},
        "invalid": {"matrix": mat_invalid, **markov_metrics(mat_invalid)},
        "diff_invalid_minus_valid": diff_matrix(mat_invalid, mat_valid),
    }

    if quad_records:
        mats = {}
        for q in ["TP", "FP", "FN", "TN"]:
            subset = [r for r in quad_records if r.get("quad") == q]
            m = compute_transition_matrix(collect_seqs(subset))
            mats[q] = {"matrix": m, **markov_metrics(m)}
        topology["global"]["quad"] = mats
        topology["global"]["quad"]["diff_fp_minus_tp"] = diff_matrix(mats["FP"]["matrix"], mats["TP"]["matrix"])
        topology["global"]["quad"]["diff_fn_minus_tn"] = diff_matrix(mats["FN"]["matrix"], mats["TN"]["matrix"])
        topology["global"]["quad"]["diff_tn_minus_tp"] = diff_matrix(mats["TN"]["matrix"], mats["TP"]["matrix"])

    for task_key in sorted({r["task"] for r in records}):
        subset_task = [r for r in records if r.get("task") == task_key]
        p_task = [r for r in subset_task if r.get("result_group") == "pass"]
        f_task = [r for r in subset_task if r.get("result_group") == "fail"]
        v_task = [r for r in subset_task if r.get("judge_group") == "valid"]
        i_task = [r for r in subset_task if r.get("judge_group") == "invalid"]
        mp = compute_transition_matrix(collect_seqs(p_task))
        mf = compute_transition_matrix(collect_seqs(f_task))
        mv = compute_transition_matrix(collect_seqs(v_task))
        mi = compute_transition_matrix(collect_seqs(i_task))
        topology["by_task"][task_key] = {
            "result_group": {
                "pass": {"matrix": mp, **markov_metrics(mp)},
                "fail": {"matrix": mf, **markov_metrics(mf)},
                "diff_fail_minus_pass": diff_matrix(mf, mp),
            },
            "judge_group": {
                "valid": {"matrix": mv, **markov_metrics(mv)},
                "invalid": {"matrix": mi, **markov_metrics(mi)},
                "diff_invalid_minus_valid": diff_matrix(mi, mv),
            }
        }
        subset_quad = [r for r in subset_task if r.get("quad") in ("TP", "FP", "FN", "TN")]
        if subset_quad:
            mats_t = {}
            for q in ["TP", "FP", "FN", "TN"]:
                ss = [r for r in subset_quad if r.get("quad") == q]
                m = compute_transition_matrix(collect_seqs(ss))
                mats_t[q] = {"matrix": m, **markov_metrics(m)}
            mats_t["diff_fp_minus_tp"] = diff_matrix(mats_t["FP"]["matrix"], mats_t["TP"]["matrix"])
            mats_t["diff_fn_minus_tn"] = diff_matrix(mats_t["FN"]["matrix"], mats_t["TN"]["matrix"])
            mats_t["diff_tn_minus_tp"] = diff_matrix(mats_t["TN"]["matrix"], mats_t["TP"]["matrix"])
            topology["by_task"][task_key]["quad"] = mats_t

    (out_dir / "topology.json").write_text(json.dumps(topology, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[done] records={len(records)} output={out_dir}")


if __name__ == "__main__":
    main()
