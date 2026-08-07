# Prompt Ablation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add four isolated prompt-ablation conditions: `default`, `pattern_only`, `anti_pattern_only`, and `pattern_and_anti`.

**Architecture:** Keep complete prompt templates in `prompt_templates.json`. Extend the shared prompt utility with the canonical method list and method-aware result paths, then update all four task runners to use the same CLI choices and isolated output directories.

**Tech Stack:** Python 3, `argparse`, JSON, `unittest`.

---

### Task 1: Define prompt-ablation behavior with tests

**Files:**
- Create: `tests/test_prompt_ablation.py`
- Test: `tests/test_prompt_ablation.py`

- [ ] **Step 1: Write failing tests**

Test that:

```python
PROMPT_METHODS == (
    "default",
    "pattern_only",
    "anti_pattern_only",
    "pattern_and_anti",
)
```

For every task and `r1`/`qwen` variant, assert that `pattern_only` contains the positive guidance marker only, `anti_pattern_only` contains `Try to avoid` only, `pattern_and_anti` contains both, and `default` contains neither.

Test that:

```python
results_dir(root, "generation", "model-x", "pattern_only", "r1")
```

ends with:

```text
data/derived_cot/rq3_prompting/results/generation/model-x/pattern_only/r1
```

- [ ] **Step 2: Verify RED**

Run:

```bash
python3 -m unittest tests.test_prompt_ablation -v
```

Expected: failure because `PROMPT_METHODS` and the method-aware `results_dir` interface do not exist.

### Task 2: Add four prompt methods

**Files:**
- Modify: `rq3_applications/rq3_2_pattern_guided_prompting/prompt_templates.json`
- Modify: `rq3_applications/rq3_2_pattern_guided_prompting/prompt_utils.py`
- Test: `tests/test_prompt_ablation.py`

- [ ] **Step 1: Replace prompt methods**

For each task and model variant:

```text
default
pattern_only
anti_pattern_only
pattern_and_anti
```

Remove `concise` and `pattern_guided`. Preserve the existing positive and negative wording exactly when splitting the current combined prompt.

- [ ] **Step 2: Add canonical method and path helpers**

Add:

```python
PROMPT_METHODS = (
    "default",
    "pattern_only",
    "anti_pattern_only",
    "pattern_and_anti",
)
```

Change `results_dir` to include the selected method and resolved variant.

- [ ] **Step 3: Verify GREEN**

Run:

```bash
python3 -m unittest tests.test_prompt_ablation -v
```

Expected: all prompt-ablation tests pass.

### Task 3: Adapt all task runners

**Files:**
- Modify: `rq3_applications/rq3_2_pattern_guided_prompting/generation_cot.py`
- Modify: `rq3_applications/rq3_2_pattern_guided_prompting/execution_cot.py`
- Modify: `rq3_applications/rq3_2_pattern_guided_prompting/debug_cot.py`
- Modify: `rq3_applications/rq3_2_pattern_guided_prompting/translation_cot.py`
- Test: `tests/test_prompt_ablation.py`

- [ ] **Step 1: Use the canonical choices**

Each runner must define:

```python
parser.add_argument(
    "--prompt_method",
    default="pattern_and_anti",
    choices=PROMPT_METHODS,
)
```

- [ ] **Step 2: Isolate outputs**

Resolve the variant and build the default output directory with:

```python
results_dir(project_root, task, args.model, args.prompt_method, resolved_variant)
```

- [ ] **Step 3: Run focused and full verification**

Run:

```bash
python3 -m unittest tests.test_prompt_ablation -v
python3 -m unittest discover -s tests -v
python3 -m compileall -q rq3_applications tests
```

Expected: all tests pass and compilation exits with status 0.
