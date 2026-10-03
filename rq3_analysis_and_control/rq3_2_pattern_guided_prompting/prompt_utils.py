from __future__ import annotations

import json
import re
from pathlib import Path
from string import Formatter


DEFAULT_TEMPLATES_PATH = Path(__file__).parent / "prompt_templates.json"
PROMPT_METHODS = (
    "default",
    "pattern_only",
    "anti_pattern_only",
    "pattern_and_anti",
)
DEFAULT_PROMPT_METHOD = "pattern_and_anti"


def load_prompt_templates(path: str | Path | None = None) -> dict:
    template_path = Path(path) if path else DEFAULT_TEMPLATES_PATH
    with template_path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_json_records(path: str | Path) -> list[dict]:
    data_path = Path(path)
    if data_path.suffix.lower() == ".json":
        payload = json.loads(data_path.read_text(encoding="utf-8"))
        return [item for item in payload if isinstance(item, dict)]
    with data_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def sanitize_slug(text: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "_", text.strip())
    return slug.strip("._-") or "unknown"


def results_dir(
    root: Path,
    task: str,
    model: str,
    prompt_method: str,
    prompt_variant: str,
) -> Path:
    return (
        root
        / "data"
        / "derived_cot"
        / "rq3_prompting"
        / "results"
        / task
        / sanitize_slug(model)
        / sanitize_slug(prompt_method)
        / sanitize_slug(prompt_variant)
    )


def infer_prompt_variant(model_name: str, requested: str = "auto") -> str:
    if requested and requested != "auto":
        return requested

    name = model_name.lower()
    if "qwen" in name:
        return "qwen"
    if "r1" in name:
        return "r1"
    return "qwen"


def get_prompt_template(
    task: str,
    model_name: str,
    prompt_method: str = DEFAULT_PROMPT_METHOD,
    prompt_variant: str = "auto",
    templates_path: str | Path | None = None,
) -> tuple[str, dict]:
    templates = load_prompt_templates(templates_path)
    task_cfg = templates["tasks"][task]
    resolved_variant = infer_prompt_variant(model_name, prompt_variant)
    requested_method = prompt_method or DEFAULT_PROMPT_METHOD
    method_cfg = task_cfg
    resolved_method = DEFAULT_PROMPT_METHOD
    if "methods" in task_cfg:
        resolved_method = requested_method
        try:
            method_cfg = task_cfg["methods"][resolved_method]
        except KeyError as exc:
            raise KeyError(f"Unknown prompt method '{resolved_method}' for task '{task}'") from exc
    try:
        template = method_cfg["variants"][resolved_variant]["template"]
    except KeyError as exc:
        raise KeyError(
            f"Unknown prompt variant '{resolved_variant}' for task '{task}' and method '{resolved_method}'"
        ) from exc
    return template, {
        "task": task,
        "method": resolved_method,
        "requested_method": prompt_method,
        "requested_variant": prompt_variant,
        "variant": resolved_variant,
        "placeholders": task_cfg.get("placeholders", []),
        "output_mode": task_cfg.get("output_mode", ""),
        "source_script": task_cfg.get("source_script", ""),
    }


def render_prompt(
    task: str,
    model_name: str,
    prompt_method: str = DEFAULT_PROMPT_METHOD,
    prompt_variant: str = "auto",
    templates_path: str | Path | None = None,
    **kwargs,
) -> tuple[str, dict]:
    template, meta = get_prompt_template(task, model_name, prompt_method, prompt_variant, templates_path)
    required = {
        field_name
        for _, field_name, _, _ in Formatter().parse(template)
        if field_name
    }
    missing = [name for name in sorted(required) if name not in kwargs]
    if missing:
        raise KeyError(f"Missing prompt placeholders for task '{task}': {missing}")
    return template.format(**kwargs), meta
