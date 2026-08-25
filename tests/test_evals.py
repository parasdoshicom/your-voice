#!/usr/bin/env python3

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_evals.py"
SPEC = importlib.util.spec_from_file_location("your_voice_eval_validator", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class EvalBenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "evals" / "benchmark.json").read_text(encoding="utf-8"))

    def test_repository_benchmark_is_valid(self):
        self.assertEqual(MODULE.validate(self.payload), [])

    def test_duplicate_case_ids_fail(self):
        payload = copy.deepcopy(self.payload)
        payload["cases"][1]["id"] = payload["cases"][0]["id"]
        self.assertTrue(any("duplicate case id" in error for error in MODULE.validate(payload)))

    def test_duplicate_rubric_dimension_fails(self):
        payload = copy.deepcopy(self.payload)
        payload["rubric"].append(payload["rubric"][0])
        self.assertTrue(any("exactly once" in error for error in MODULE.validate(payload)))

    def test_spoken_case_requires_speakability(self):
        payload = copy.deepcopy(self.payload)
        spoken = next(case for case in payload["cases"] if case["mode"] == "spoken")
        spoken["rubric_focus"].remove("speakability")
        self.assertTrue(any("spoken cases must focus" in error for error in MODULE.validate(payload)))

    def test_case_requires_criteria_origin_and_failure_modes(self):
        payload = copy.deepcopy(self.payload)
        del payload["cases"][0]["criteria_origin"]
        payload["cases"][1]["failure_modes"] = []
        errors = MODULE.validate(payload)
        self.assertTrue(any("criteria_origin" in error for error in errors))
        self.assertTrue(any("failure_modes" in error for error in errors))

    def test_judge_contract_stays_binary_and_atomic(self):
        payload = copy.deepcopy(self.payload)
        payload["judge_contract"]["labels"] = ["0", "1", "2"]
        payload["judge_contract"]["one_failure_mode_per_judge"] = False
        errors = MODULE.validate(payload)
        self.assertTrue(any("labels" in error for error in errors))
        self.assertTrue(any("one_failure_mode" in error for error in errors))

    def test_required_stress_test_cannot_disappear(self):
        payload = copy.deepcopy(self.payload)
        payload["stress_tests"] = [
            stress for stress in payload["stress_tests"] if stress["id"] != "long-context-retention"
        ]
        self.assertTrue(any("missing required ids" in error for error in MODULE.validate(payload)))

    def test_stress_test_requires_pass_criteria(self):
        payload = copy.deepcopy(self.payload)
        payload["stress_tests"][0]["pass_criteria"] = []
        self.assertTrue(any("pass_criteria" in error for error in MODULE.validate(payload)))


if __name__ == "__main__":
    unittest.main()
