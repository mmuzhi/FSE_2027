"""Code extraction and cleanup helpers for generated RQ3.3 answers."""

from __future__ import annotations

import ast
import re


PYTHON_START_RE = re.compile(
    r"(?m)^(?:from\s+\w[\w.]*\s+import\s+.+|import\s+\w[\w.]*.*|class\s+\w+\s*[:(]|def\s+\w+\s*\(|@\w)"
)


def strip_think_blocks(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
    # Some broken outputs contain a stray closing tag. If it appears before the
    # first code-looking line, drop the prefix; otherwise keep the code and only
    # remove the marker itself.
    close_match = re.search(r"</think>", text, flags=re.IGNORECASE)
    if close_match:
        first_code = PYTHON_START_RE.search(text)
        if first_code and first_code.start() > close_match.end():
            text = text[close_match.end() :]
        else:
            text = re.sub(r"</think>", "", text, flags=re.IGNORECASE)
    return re.sub(r"<think>", "", text, flags=re.IGNORECASE)


def strip_fence_markers(text: str) -> str:
    if not text:
        return ""
    lines = text.strip().splitlines()
    while lines and re.fullmatch(r"\s*```(?:\w+|\w[+\w-]*)?\s*", lines[0]):
        lines.pop(0)
    while lines and re.fullmatch(r"\s*```\s*", lines[-1]):
        lines.pop()
    return "\n".join(lines).strip()


def leading_code_before_fence(text: str) -> str | None:
    if not text:
        return None
    stripped = text.lstrip()
    if not PYTHON_START_RE.match(stripped):
        return None
    match = re.search(r"(?m)^\s*```\s*$", stripped)
    if not match:
        return None
    candidate = stripped[: match.start()].strip()
    return candidate or None


def extract_fenced_code(answer_text: str, languages: str = r"\w+") -> str | None:
    if not answer_text:
        return None
    pattern = re.compile(rf"```(?:{languages})?\s*\n([\s\S]*?)(?:\n```|```\s*\Z)", re.IGNORECASE)
    matches = [match.group(1).strip() for match in pattern.finditer(answer_text)]
    if matches:
        return max(matches, key=lambda item: (looks_like_python_code(item), len(item)))
    open_fence = re.search(rf"```(?:{languages})?\s*\n([\s\S]*)\Z", answer_text, re.IGNORECASE)
    if open_fence:
        return open_fence.group(1).strip()
    return None


def looks_like_python_code(text: str) -> bool:
    clean = strip_fence_markers(strip_think_blocks(text or "").lstrip("\ufeff"))
    return bool(PYTHON_START_RE.search(clean))


def _parses_python(text: str) -> bool:
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


def trim_to_python_start(text: str) -> str:
    if not text:
        return ""
    matches = list(PYTHON_START_RE.finditer(text))
    if not matches:
        return text.strip()
    stripped = text.lstrip()
    leading_offset = len(text) - len(stripped)
    if matches[0].start() == leading_offset:
        return text[matches[0].start() :].strip()
    return text[matches[-1].start() :].strip()


def trim_after_python_code(text: str) -> str:
    candidate = text.rstrip().strip()
    if not candidate:
        return ""
    original = candidate
    if _parses_python(candidate):
        return candidate

    lines = candidate.splitlines()
    while lines:
        tail = lines[-1].strip()
        lines.pop()
        candidate = "\n".join(lines).strip()
        if not candidate:
            return "" if not tail or tail == "```" or tail.startswith("===") else original
        if _parses_python(candidate):
            return candidate
    return original


def strip_full_line_python_comments(code: str) -> str:
    if not code:
        return ""
    lines = [
        line
        for line in code.splitlines()
        if not line.lstrip().startswith("#")
    ]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def repair_python_answer(code: str) -> str:
    if not code:
        return code
    code = strip_fence_markers(strip_think_blocks(code))
    code = trim_to_python_start(code)
    code = strip_fence_markers(code)
    code = trim_after_python_code(code)
    code = strip_full_line_python_comments(code)
    lines = code.rstrip().splitlines()
    if not lines:
        return ""
    last = lines[-1].strip()
    if re.fullmatch(r"if\s+__name__\s*==\s*['\"]__main__['\"]\s*:", last):
        indent = re.match(r"\s*", lines[-1]).group(0)
        lines.append(f"{indent}    main()")
    return "\n".join(lines).strip()


def extract_python_answer(answer_text: str) -> str:
    if not answer_text:
        return ""
    cleaned = strip_think_blocks(answer_text)
    leading = leading_code_before_fence(cleaned)
    if leading is not None:
        return repair_python_answer(leading)
    code = extract_fenced_code(cleaned, r"python|py")
    if code is None:
        code = extract_fenced_code(cleaned)
    if code is None:
        code = cleaned.strip()
    repaired = repair_python_answer(code)
    return repaired if looks_like_python_code(repaired) else ""


def extract_code_answer(answer_text: str, target_lang: str = "py") -> str:
    if not answer_text:
        return ""
    if target_lang.lower() in {"py", "python"}:
        return extract_python_answer(answer_text)
    cleaned = strip_think_blocks(answer_text)
    lang_patterns = {
        "cpp": r"cpp|c\+\+",
        "c++": r"cpp|c\+\+",
        "java": r"java",
    }
    code = extract_fenced_code(cleaned, lang_patterns.get(target_lang.lower(), r"\w+"))
    if code is None:
        code = extract_fenced_code(cleaned)
    return strip_fence_markers(code if code is not None else cleaned.strip())
