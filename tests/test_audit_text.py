#!/usr/bin/env python3

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "audit_text.py"
SPEC = importlib.util.spec_from_file_location("your_voice_audit", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class AuditTests(unittest.TestCase):
    def test_flags_named_patterns(self):
        text = "Great question! Here's the thing: this is not a tool, it is a game changer—full stop."
        rules = {finding.rule for finding in MODULE.audit(text)}
        self.assertEqual(
            rules,
            {"chatbot_artifact", "throat_clearing", "binary_contrast", "ai_vocabulary", "em_dash"},
        )

    def test_preserves_plain_specific_prose(self):
        text = "The team cut review time from 40 minutes to 12 after it cached the approved metric definitions."
        self.assertEqual(MODULE.audit(text), [])

    def test_flags_new_pattern_set(self):
        cases = {
            "That's not compliance. That's stalling.": "binary_contrast",
            "That's not compliance.\nThat's stalling.": "binary_contrast",
            "Fast. Simple.": "stacked_short_fragments",
            "Use less of a hammer, more of a scalpel.": "empty_comparison",
            "And that matters.": "self_applause",
            "It's the Excel of AI agents.": "unexplained_analogy",
            "Faster, cheaper, smarter.": "forced_triad",
            "Setup takes 5 to 10 minutes.": "imprecise_time_range",
            "In short, use the smaller model.": "recap_ending",
        }
        for text, expected_rule in cases.items():
            with self.subTest(text=text):
                rules = {finding.rule for finding in MODULE.audit(text)}
                self.assertIn(expected_rule, rules)

    def test_loads_private_forbidden_patterns(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "forbidden.md"
            path.write_text(
                "# personal rules\n- literal: move the needle\nregex: \\bsynerg(?:y|ize)\\b\n",
                encoding="utf-8",
            )
            custom_rules = MODULE.load_forbidden_patterns(path)
            findings = MODULE.audit(
                "This will move the needle without asking us to synergize.",
                forbidden_patterns=custom_rules,
            )
            self.assertEqual(
                {finding.rule for finding in findings},
                {"forbidden_literal_1", "forbidden_regex_2"},
            )

    def test_rejects_invalid_forbidden_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "forbidden.md"
            path.write_text("write better\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "expected 'literal: text'"):
                MODULE.load_forbidden_patterns(path)

    def test_technical_mode_adds_clarity_checks(self):
        text = (
            "The configuration file was created by the installer after the operator opened "
            "the package and selected the target directory that contains every shared agent "
            "skill used by the local runtime."
        )
        voice_rules = {finding.rule for finding in MODULE.audit(text)}
        technical_rules = {finding.rule for finding in MODULE.audit(text, mode="technical")}
        self.assertNotIn("long_technical_sentence", voice_rules)
        self.assertIn("long_technical_sentence", technical_rules)
        self.assertIn("passive_technical_sentence", technical_rules)


if __name__ == "__main__":
    unittest.main()
