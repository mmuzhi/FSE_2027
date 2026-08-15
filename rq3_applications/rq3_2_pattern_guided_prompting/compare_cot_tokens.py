#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


_TIKTOKEN_ENC = None
DEFAULT_FILE_A = Path(r"/Users/bytedance/XLLM_COT/data/CodeSense/Execution_COT/qwen/results.jsonl")
DEFAULT_FILE_B = Path(r"/Users/bytedance/XLLM_COT/RQ4.1/results/concise/execution/qwen/results.jsonl")


def _get_tiktoken_encoder():
    global _TIKTOKEN_ENC
    if _TIKTOKEN_ENC is None:
        try:
            import tiktoken  # type: ignore

            _TIKTOKEN_ENC = tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None
    return _TIKTOKEN_ENC


def count_tokens(text: str) -> int:
    if not text:
        return 0
    enc = _get_tiktoken_encoder()
    if enc is not None:
        return len(enc.encode(text))
    return len(text.split())


def tokenizer_label() -> str:
    return "tiktoken/cl100k_base" if _get_tiktoken_encoder() is not None else "whitespace"


def total_cot_tokens(path: Path) -> tuple[int, int]:
    total_tokens = 0
    record_count = 0
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON at {path}:{line_no}") from exc
            if not isinstance(obj, dict):
                continue
            cot_text = obj.get("cot", "")
            if not isinstance(cot_text, str):
                cot_text = json.dumps(cot_text, ensure_ascii=False)
            total_tokens += count_tokens(cot_text)
            record_count += 1
    return total_tokens, record_count


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare total token counts of the 'cot' field in two result JSONL files.")
    parser.add_argument(
        "file_a",
        nargs="?",
        default=str(DEFAULT_FILE_A),
        help=f"Path of file A. Default: {DEFAULT_FILE_A}",
    )
    parser.add_argument(
        "file_b",
        nargs="?",
        default=str(DEFAULT_FILE_B),
        help=f"Path of file B. Default: {DEFAULT_FILE_B}",
    )
    args = parser.parse_args()

    file_a = Path(args.file_a)
    file_b = Path(args.file_b)
    if not file_a.is_file():
        raise FileNotFoundError(f"File not found: {file_a}")
    if not file_b.is_file():
        raise FileNotFoundError(f"File not found: {file_b}")

    total_a, count_a = total_cot_tokens(file_a)
    total_b, count_b = total_cot_tokens(file_b)
    avg_a = total_a / count_a if count_a else 0.0
    avg_b = total_b / count_b if count_b else 0.0

    print(f"Tokenizer: {tokenizer_label()}")
    print(f"File A: {file_a}")
    print(f"Records A: {count_a}")
    print(f"CoT tokens A: {total_a}")
    print(f"Average tokens A: {avg_a:.2f}")
    print()
    print(f"File B: {file_b}")
    print(f"Records B: {count_b}")
    print(f"CoT tokens B: {total_b}")
    print(f"Average tokens B: {avg_b:.2f}")
    print()
    print(f"Delta (A - B): {total_a - total_b}")


if __name__ == "__main__":
    main()