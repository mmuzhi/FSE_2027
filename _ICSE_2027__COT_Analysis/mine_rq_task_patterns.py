from __future__ import annotations

import argparse
import csv
import json
import math
from importlib import import_module
from pathlib import Path
from typing import Any


CATEGORIES = {"PU", "SD", "IP", "CC", "VV", "KR", "MR", "AUX"}
MODELS = ["r1", "qwen"]
TASKS = {
  "generation": ("generation", "Generate_COT"),
  "execution": ("execution", "Execution_COT"),
  "summarization": ("summarization", "Summarization_COT"),
  "debug": ("debug", "Debug_COT"),
  "translation": ("translation", "Translation_COT"),
}
RQ2_TASKS = ["generation", "execution", "debug", "translation"]
TRANSLATION_DIRECTIONS = ("cpp_to_py", "java_to_py", "py_to_cpp", "java_to_cpp")
ORDERED_PATHS = [
  ("PU", "AUX"),
  ("PU", "SD", "IP", "CC"),
  ("PU", "SD", "IP", "CC", "VV"),
  ("PU", "VV", "MR", "VV"),
  ("SD", "IP", "CC", "VV"),
  ("VV", "IP", "CC", "VV"),
  ("IP", "VV", "IP", "VV"),
  ("PU", "SD", "KR", "SD"),
  ("PU", "SD", "MR", "SD"),
  ("PU", "MR", "PU", "MR"),
  ("SD", "MR", "SD", "MR"),
]
CLOSURE_PATHS = [
  ("IP", "VV", "AUX"),
  ("CC", "VV", "AUX"),
  ("VV", "MR", "VV", "AUX"),
  ("IP", "CC", "VV", "AUX"),
  ("SD", "IP", "CC", "VV"),
]
LOOP_PAIRS = [
  ("PU", "MR"),
  ("PU", "SD"),
  ("SD", "MR"),
  ("SD", "KR"),
  ("SD", "VV"),
  ("VV", "MR"),
  ("VV", "IP"),
  ("IP", "CC"),
]


def read_json(path: Path) -> dict[str, Any]:
  with path.open(encoding="utf-8") as f:
    return json.load(f)


def iter_jsonl(path: Path):
  with path.open(encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if line:
        yield json.loads(line)


def compress_sequence(seq: list[str]) -> list[str]:
  out: list[str] = []
  for item in seq:
    if not out or item != out[-1]:
      out.append(item)
  return out


def extract_sequence(record: dict[str, Any]) -> list[str]:
  seg = record.get("segmentation_result", {})
  if not isinstance(seg, dict) or not seg.get("success"):
    return []
  seq = []
  for step in seg.get("steps", []):
    cat = step.get("category") if isinstance(step, dict) else None
    if cat in CATEGORIES:
      seq.append(cat)
  return seq


def normalize_translation_id(task_id: str) -> str:
  if "/" in task_id:
    return task_id
  for direction in TRANSLATION_DIRECTIONS:
    prefix = f"{direction}_"
    if task_id.startswith(prefix):
      return f"{direction}/{task_id[len(prefix):]}"
  return task_id


def normalize_task_id(task: str, task_id: str) -> str:
  if task == "translation":
    return normalize_translation_id(task_id)
  return task_id


def load_segmented(repo_root: Path) -> dict[str, dict[str, list[dict[str, Any]]]]:
  data: dict[str, dict[str, list[dict[str, Any]]]] = {model: {} for model in MODELS}
  seg_root = repo_root / "RQ1" / "segmentation_results"
  for model in MODELS:
    for task, (_, seg_dir) in TASKS.items():
      path = seg_root / seg_dir / model / "segmented_results.jsonl"
      samples = []
      if not path.exists():
        data[model][task] = samples
        continue
      for record in iter_jsonl(path):
        task_id = record.get("task_id")
        seq = extract_sequence(record)
        if task_id is None or not seq:
          continue
        samples.append({
          "task_id": normalize_task_id(task, str(task_id)),
          "seq": compress_sequence(seq),
        })
      data[model][task] = samples
  return data


def has_ordered_path(seq: list[str], path: tuple[str, ...]) -> bool:
  pos = 0
  for item in seq:
    if item == path[pos]:
      pos += 1
      if pos == len(path):
        return True
  return False


def has_transition(seq: list[str], src: str, dst: str) -> bool:
  return any(a == src and b == dst for a, b in zip(seq, seq[1:]))


def has_alternating_loop(seq: list[str], a: str, b: str) -> bool:
  targets = [(a, b, a), (b, a, b), (a, b, a, b), (b, a, b, a)]
  for size in (3, 4):
    if len(seq) < size:
      continue
    for idx in range(len(seq) - size + 1):
      if tuple(seq[idx:idx + size]) in targets:
        return True
  return False


def add_pattern(found: dict[str, str], kind: str, pattern: str) -> None:
  found[f"{kind}:{pattern}"] = kind


def pattern_set(seq: list[str], ngram_sizes: list[int]) -> dict[str, str]:
  found: dict[str, str] = {}
  for size in ngram_sizes:
    if size <= 0 or len(seq) < size:
      continue
    for idx in range(len(seq) - size + 1):
      add_pattern(found, "连续片段", "->".join(seq[idx:idx + size]))

  for path in ORDERED_PATHS:
    if has_ordered_path(seq, path):
      add_pattern(found, "有序路径", "=>".join(path))

  for path in CLOSURE_PATHS:
    if has_ordered_path(seq, path):
      add_pattern(found, "闭合模式", "=>".join(path))

  for a, b in LOOP_PAIRS:
    if has_transition(seq, a, b) and has_transition(seq, b, a):
      add_pattern(found, "双向回退", f"{a}<->{b}")
    if has_alternating_loop(seq, a, b):
      add_pattern(found, "交替循环", f"{a}<->{b}")
  return found


def split_pattern_key(pattern_key: str) -> tuple[str, str]:
  kind, pattern = pattern_key.split(":", 1)
  return kind, pattern


def fisher_p_value(a: int, b: int, c: int, d: int) -> float:
  try:
    fisher_exact = import_module("scipy.stats").fisher_exact
    return float(fisher_exact([[a, b], [c, d]], alternative="two-sided")[1])
  except Exception:
    return fisher_p_value_fallback(a, b, c, d)


def fisher_p_value_fallback(a: int, b: int, c: int, d: int) -> float:
  row_a = a + b
  row_c = c + d
  col_a = a + c
  col_b = b + d
  total = row_a + row_c
  lo = max(0, col_a - row_c)
  hi = min(row_a, col_a)

  def log_comb(n: int, k: int) -> float:
    if k < 0 or k > n:
      return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)

  def prob(x: int) -> float:
    y = row_a - x
    if y < 0 or y > col_b:
      return 0.0
    return math.exp(log_comb(col_a, x) + log_comb(col_b, y) - log_comb(total, row_a))

  observed = prob(a)
  return min(1.0, sum(prob(x) for x in range(lo, hi + 1) if prob(x) <= observed + 1e-12))


def add_bh_q_value(rows: list[dict[str, Any]]) -> None:
  if not rows:
    return
  order = sorted(range(len(rows)), key=lambda idx: rows[idx]["p值"])
  raw_q = [1.0] * len(rows)
  for rank, idx in enumerate(order, start=1):
    raw_q[idx] = rows[idx]["p值"] * len(rows) / rank
  running = 1.0
  for idx in reversed(order):
    running = min(running, raw_q[idx])
    rows[idx]["q值"] = min(1.0, running)


def compare_groups(
  target: list[dict[str, Any]],
  baseline: list[dict[str, Any]],
  ngram_sizes: list[int],
  min_support: float,
  min_delta: float,
) -> list[dict[str, Any]]:
  target_sets = [pattern_set(item["seq"], ngram_sizes) for item in target]
  baseline_sets = [pattern_set(item["seq"], ngram_sizes) for item in baseline]
  target_total = len(target_sets)
  baseline_total = len(baseline_sets)
  all_patterns = set().union(*(item.keys() for item in target_sets + baseline_sets)) if target_sets or baseline_sets else set()
  rows = []
  for pattern in all_patterns:
    target_count = sum(pattern in item for item in target_sets)
    baseline_count = sum(pattern in item for item in baseline_sets)
    target_support = target_count / target_total if target_total else 0.0
    baseline_support = baseline_count / baseline_total if baseline_total else 0.0
    delta = target_support - baseline_support
    if target_support < min_support or delta < min_delta:
      continue
    pattern_kind, pattern_text = split_pattern_key(pattern)
    rows.append({
      "pattern": pattern_text,
      "pattern类型": pattern_kind,
      "目标组支持度": target_support,
      "对照组支持度": baseline_support,
      "支持度差": delta,
      "目标组样本数": target_total,
      "对照组样本数": baseline_total,
      "p值": fisher_p_value(
        target_count,
        target_total - target_count,
        baseline_count,
        baseline_total - baseline_count,
      ),
    })
  add_bh_q_value(rows)
  return rows


def load_judge_labels(repo_root: Path, model: str, task: str) -> dict[str, bool]:
  path = repo_root / "RQ2" / "results" / model / f"aggregated_{task}.json"
  if not path.exists():
    return {}
  labels = {}
  for item in read_json(path).get("results", []):
    task_id = item.get("task_id")
    if task_id is None:
      continue
    labels[normalize_task_id(task, str(task_id))] = bool(item.get("is_valid"))
  return labels


def append_rows(
  output: list[dict[str, Any]],
  rows: list[dict[str, Any]],
  task_name: str,
  model: str,
  rq: str,
  pattern_group: str,
  contrast: str,
  top_k: int,
  max_q: float,
) -> None:
  rows = [row for row in rows if row.get("q值", 1.0) <= max_q]
  rows.sort(key=lambda row: (row["q值"], -row["支持度差"], row["pattern类型"], row["pattern"]))
  for row in rows[:top_k]:
    output.append({
      "任务": task_name,
      "模型": model,
      "研究问题": rq,
      "模式分类": pattern_group,
      "pattern类型": row["pattern类型"],
      "对比对象": contrast,
      "pattern": row["pattern"],
      "目标组支持度": round(row["目标组支持度"], 6),
      "对照组支持度": round(row["对照组支持度"], 6),
      "支持度差": round(row["支持度差"], 6),
      "目标组样本数": row["目标组样本数"],
      "对照组样本数": row["对照组样本数"],
      "FDR_q": round(row.get("q值", 1.0), 12),
    })


def mine_rq1_patterns(segmented: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
  output = []
  for model in MODELS:
    for task, (task_name, _) in TASKS.items():
      target = segmented[model].get(task, [])
      baseline = [
        item
        for other_task, samples in segmented[model].items()
        if other_task != task
        for item in samples
      ]
      rows = compare_groups(target, baseline, [4, 5], 0.05, 0.03)
      append_rows(
        output,
        rows,
        task_name,
        model,
        "RQ1",
        "task_specific",
        "task vs others",
        top_k=10,
        max_q=0.05,
      )
  return output


def mine_rq2_patterns(repo_root: Path, segmented: dict[str, dict[str, list[dict[str, Any]]]]) -> list[dict[str, Any]]:
  output = []
  for model in MODELS:
    for task in RQ2_TASKS:
      task_name = TASKS[task][0]
      samples = {item["task_id"]: item for item in segmented[model].get(task, [])}
      judge = load_judge_labels(repo_root, model, task)
      valid = [samples[key] for key, is_valid in judge.items() if is_valid and key in samples]
      invalid = [samples[key] for key, is_valid in judge.items() if not is_valid and key in samples]

      for target, baseline, pattern_group, contrast in [
        (valid, invalid, "validity_positive", "valid vs invalid"),
        (invalid, valid, "validity_negative", "invalid vs valid"),
      ]:
        rows = compare_groups(target, baseline, [4, 5], 0.08, 0.06)
        append_rows(
          output,
          rows,
          task_name,
          model,
          "RQ2",
          pattern_group,
          contrast,
          top_k=8,
          max_q=0.05,
        )
  return output


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
  fieldnames = [
    "任务",
    "模型",
    "研究问题",
    "模式分类",
    "pattern类型",
    "对比对象",
    "pattern",
    "目标组支持度",
    "对照组支持度",
    "支持度差",
    "目标组样本数",
    "对照组样本数",
    "FDR_q",
  ]
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def parse_args() -> argparse.Namespace:
  parser = argparse.ArgumentParser()
  parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
  parser.add_argument("--output", default=str(Path(__file__).resolve().parent / "tables" / "rq_task_pattern_summary.csv"))
  return parser.parse_args()


def main() -> None:
  args = parse_args()
  repo_root = Path(args.repo_root).resolve()
  segmented = load_segmented(repo_root)
  rows = mine_rq1_patterns(segmented)
  rows.extend(mine_rq2_patterns(repo_root, segmented))
  rows.sort(key=lambda row: (row["任务"], row["研究问题"], row["模式分类"], row["模型"], row["FDR_q"]))
  write_csv(Path(args.output), rows)
  print(f"写入 {len(rows)} 行: {args.output}")


if __name__ == "__main__":
  main()
