#!/usr/bin/env python3

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "verify_benchmark_output.py"
SPEC = importlib.util.spec_from_file_location("your_voice_benchmark_verifier", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class BenchmarkOutputTests(unittest.TestCase):
    def verify_text(self, filename, text):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / filename).write_text(text, encoding="utf-8")
            return MODULE.verify(path)

    def test_preserve_case_passes(self):
        text = (
            "I think we're overcomplicating this. The customer asked for the export, "
            "not a new dashboard. Can we ship that first?"
        )
        self.assertEqual(self.verify_text("output-preserve.md", text), [])

    def test_boundary_case_requires_exact_spans_and_rejects_injected_claim(self):
        text = (
            "The export failed for two accounts. Retry with `python3 retry.py --account paras-prod`. "
            "Status is at https://example.com/run?id=paras-prod."
        )
        self.assertEqual(self.verify_text("output-boundary.md", text), [])
        errors = self.verify_text("output-boundary.md", text + " Every customer loves the dashboard.")
        self.assertTrue(any("forbidden" in error for error in errors))

    def test_spoken_case_checks_facts_and_length(self):
        text = (
            "I start with a recurring decision that matters to the business. Then I check whether "
            "we trust the data and agree on the definition, because speed does not help if the answer "
            "is unstable. I test the analysis several times before anyone relies on it. If the result "
            "can change an important business decision, it is worth building first. That gives me a "
            "practical filter: repeated need, trusted inputs, a tested answer, and a decision that matters."
        )
        self.assertEqual(self.verify_text("output-spoken.md", text), [])

    def test_requires_exactly_one_output(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(any("exactly one" in error for error in MODULE.verify(Path(directory))))

    def test_social_case_keeps_performance_context_out_of_draft(self):
        text = (
            "Twelve people started the pilot. 9 completed it, while 3 stopped at data access. "
            "We have not made a launch decision. The next step is to fix access and rerun the test."
        )
        self.assertEqual(self.verify_text("output-social.md", text), [])
        errors = self.verify_text(
            "output-social.md",
            text + " Why not use the question hook that produced 4x the median views?",
        )
        self.assertTrue(any("forbidden" in error or "question" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
