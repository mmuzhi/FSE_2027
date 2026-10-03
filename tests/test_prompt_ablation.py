import unittest
import inspect
from pathlib import Path

from rq3_analysis_and_control.rq3_2_pattern_guided_prompting import prompt_utils


TASK_ARGUMENTS = {
    "generation": {
        "question_content": "Add two integers.",
        "starter_code": "def solve(): pass",
    },
    "execution": {
        "language": "python",
        "code": "print(1 + 1)",
        "input_text": "",
    },
    "debug": {
        "buggy_code": "print(1 / 0)",
    },
    "translation": {
        "source_lang": "java",
        "target_lang": "python",
        "source_code": "class Main {}",
    },
}

POSITIVE_MARKERS = {
    "generation": ("A productive rhythm",),
    "execution": ("A productive pattern",),
    "debug": ("A practical pattern", "A useful pattern"),
    "translation": ("Keep the reasoning compact",),
}


class PromptAblationTest(unittest.TestCase):
    def test_exposes_exactly_four_ablation_methods(self):
        self.assertEqual(
            getattr(prompt_utils, "PROMPT_METHODS", ()),
            (
                "default",
                "pattern_only",
                "anti_pattern_only",
                "pattern_and_anti",
            ),
        )

    def test_each_ablation_method_contains_only_its_intended_guidance(self):
        methods = getattr(prompt_utils, "PROMPT_METHODS", ())
        self.assertEqual(len(methods), 4)
        for task, task_args in TASK_ARGUMENTS.items():
            for variant in ("r1", "qwen"):
                prompts = {
                    method: prompt_utils.render_prompt(
                        task=task,
                        model_name=variant,
                        prompt_method=method,
                        prompt_variant=variant,
                        **task_args,
                    )[0]
                    for method in methods
                }
                markers = POSITIVE_MARKERS[task]

                with self.subTest(task=task, variant=variant, method="default"):
                    self.assertFalse(any(marker in prompts["default"] for marker in markers))
                    self.assertNotIn("Try to avoid", prompts["default"])

                with self.subTest(task=task, variant=variant, method="pattern_only"):
                    self.assertTrue(any(marker in prompts["pattern_only"] for marker in markers))
                    self.assertNotIn("Try to avoid", prompts["pattern_only"])

                with self.subTest(task=task, variant=variant, method="anti_pattern_only"):
                    self.assertFalse(any(marker in prompts["anti_pattern_only"] for marker in markers))
                    self.assertIn("Try to avoid", prompts["anti_pattern_only"])

                with self.subTest(task=task, variant=variant, method="pattern_and_anti"):
                    self.assertTrue(any(marker in prompts["pattern_and_anti"] for marker in markers))
                    self.assertIn("Try to avoid", prompts["pattern_and_anti"])

    def test_results_directory_isolated_by_method_and_variant(self):
        parameters = tuple(inspect.signature(prompt_utils.results_dir).parameters)
        self.assertEqual(
            parameters,
            ("root", "task", "model", "prompt_method", "prompt_variant"),
        )
        path = prompt_utils.results_dir(
            Path("/repo"),
            "generation",
            "model-x",
            "pattern_only",
            "r1",
        )
        self.assertEqual(
            path,
            Path(
                "/repo/data/derived_cot/rq3_prompting/results/"
                "generation/model-x/pattern_only/r1"
            ),
        )


if __name__ == "__main__":
    unittest.main()
