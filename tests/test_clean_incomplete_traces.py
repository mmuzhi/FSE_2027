import unittest

from rq1_general_patterns.clean_incomplete_traces import TASKS, incomplete_reasons


class CleanIncompleteTracesTest(unittest.TestCase):
    def test_execution_keeps_empty_parsed_answer_when_final_answer_exists(self):
        row = {
            "cot": "reasoning trace",
            "answer": "",
            "raw_answer": "",
            "raw_answer_full": "<ans></ans>",
        }

        self.assertEqual(incomplete_reasons(row, TASKS["execution"]["required_fields"]), [])

    def test_execution_deletes_missing_final_answer(self):
        row = {
            "cot": "reasoning trace",
            "answer": "",
            "raw_answer": "",
            "raw_answer_full": "",
        }

        self.assertEqual(
            incomplete_reasons(row, TASKS["execution"]["required_fields"]),
            ["empty_raw_answer_full"],
        )

    def test_debug_keeps_empty_extracted_code_when_final_answer_exists(self):
        row = {
            "cot": "reasoning trace",
            "raw_answer": "I cannot produce a patch, but here is the explanation.",
            "fixed_code": "",
        }

        self.assertEqual(incomplete_reasons(row, TASKS["debug"]["required_fields"]), [])

    def test_translation_keeps_empty_extracted_code_when_final_answer_exists(self):
        row = {
            "cot": "reasoning trace",
            "raw_answer": "No translation is needed for this snippet.",
            "translated_code": "",
        }

        self.assertEqual(incomplete_reasons(row, TASKS["translation"]["required_fields"]), [])

    def test_generation_deletes_missing_answer(self):
        row = {
            "cot": "reasoning trace",
            "answer": "",
        }

        self.assertEqual(
            incomplete_reasons(row, TASKS["generation"]["required_fields"]),
            ["empty_answer"],
        )


if __name__ == "__main__":
    unittest.main()
