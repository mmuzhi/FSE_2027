"""Prompt text for completing an answer from a stopped CoT prefix."""

from __future__ import annotations


PREFILL_TRANSITIONS = {
    "generation": "\n\nFinal Python code only. No explanations. No comments.\n```python\n",
    "execution": "\n\nBased on the reasoning above, answer using <ans></ans> tags only.\n\n",
    "debug": "\n\nFinal fixed Python code only. No explanations. No comments.\n```python\n",
    "translation": "\n\nFinal translated code only. No explanations. No comments.\n```\n",
}


def build_prefill_transition(task: str) -> str:
    return PREFILL_TRANSITIONS.get(
        task,
        "\n\nBased on the reasoning above, output only the final answer.\n\n",
    )


def build_user_finalizer_prompt(*, original_prompt: str, reasoning_prefix: str, task: str) -> str:
    """Build a user-message finalizer for APIs that reject assistant prefill."""
    transition = build_prefill_transition(task).strip()
    if task == "generation":
        return (
            "You previously started solving the following competitive programming task.\n\n"
            "=== ORIGINAL TASK ===\n"
            f"{original_prompt}\n\n"
            "=== STOPPED REASONING PREFIX ===\n"
            f"{reasoning_prefix.strip()}\n\n"
            "The stopped reasoning is only background context. Do not continue it, "
            "do not explain it, and do not put reasoning into comments. "
            "Make one direct implementation choice now and output only runnable Python code. "
            "No Markdown fences, no analysis, no comments."
        )
    return (
        "You previously started solving the following task.\n\n"
        "=== ORIGINAL TASK ===\n"
        f"{original_prompt}\n\n"
        "=== STOPPED REASONING PREFIX ===\n"
        f"{reasoning_prefix.strip()}\n\n"
        "Do not continue the reasoning. Use only the stopped reasoning prefix above, "
        f"and {transition[0].lower() + transition[1:] if transition else 'output only the final answer.'}"
    )
