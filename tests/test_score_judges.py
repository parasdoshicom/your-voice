#!/usr/bin/env python3

import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "score_judges.py"
SPEC = importlib.util.spec_from_file_location("your_voice_judge_scorer", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def row(row_id, human, judge, mode="voice_fit", split="test", evidence="quoted text"):
    return {
        "id": row_id,
        "failure_mode": mode,
        "split": split,
        "human_label": human,
        "judge_label": judge,
        "evidence": evidence,
    }


class JudgeScoreTests(unittest.TestCase):
    def test_scores_tpr_and_tnr_separately(self):
        rows = [
            row("1", "Pass", "Pass"),
            row("2", "Pass", "Fail"),
            row("3", "Fail", "Fail"),
            row("4", "Fail", "Pass"),
        ]
        result = MODULE.score_rows(rows)["voice_fit"]
        self.assertEqual(result["tpr"], 0.5)
        self.assertEqual(result["tnr"], 0.5)
        self.assertEqual(result["false_pass"], 1)
        self.assertEqual(result["false_fail"], 1)

    def test_filters_to_requested_split(self):
        rows = [
            row("dev-pass", "Pass", "Fail", split="dev"),
            row("test-pass", "Pass", "Pass"),
            row("test-fail", "Fail", "Fail"),
        ]
        result = MODULE.score_rows(rows, split="test")["voice_fit"]
        self.assertEqual(result["rows"], 2)
        self.assertEqual(result["tpr"], 1.0)
        self.assertEqual(result["tnr"], 1.0)

    def test_requires_evidence_and_binary_labels(self):
        rows = [row("1", "Maybe", "Pass", evidence="")]
        errors = MODULE.validate_rows(rows)
        self.assertTrue(any("human_label" in error for error in errors))
        self.assertTrue(any("evidence" in error for error in errors))

    def test_production_threshold_catches_small_or_weak_sets(self):
        rows = [row("1", "Pass", "Pass"), row("2", "Fail", "Pass")]
        results = MODULE.score_rows(rows)
        failures = MODULE.threshold_failures(results, min_per_label=2, min_rate=0.9)
        self.assertTrue(any("human Pass" in failure for failure in failures))
        self.assertTrue(any("TNR" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
