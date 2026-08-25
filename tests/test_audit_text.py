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

    def test_does_not_join_markdown_blocks_into_fake_fragments(self):
        text = "## Non-negotiables\n\n1. Preserve meaning.\n2. Preserve voice."
        rules = {finding.rule for finding in MODULE.audit(text)}
        self.assertNotIn("stacked_short_fragments", rules)

    def test_does_not_match_tail_of_long_sentence_as_fragment(self):
        text = "Fix any line a smart person would not say naturally. Keep intentional roughness."
        rules = {finding.rule for finding in MODULE.audit(text)}
        self.assertNotIn("stacked_short_fragments", rules)

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
            "The key point is that three users still cannot sign in.": "interpretive_metadiscourse",
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

    def test_spoken_mode_flags_written_syntax_and_long_breath_groups(self):
        text = (
            "Furthermore, in order to build a system that people can trust, we need to "
            "review every definition, trace each answer to its source, record the failures, "
            "and make sure the next run can reuse the correction."
        )
        voice_rules = {finding.rule for finding in MODULE.audit(text)}
        spoken_rules = {finding.rule for finding in MODULE.audit(text, mode="spoken")}
        self.assertNotIn("written_only_spoken_phrase", voice_rules)
        self.assertNotIn("long_spoken_sentence", voice_rules)
        self.assertIn("written_only_spoken_phrase", spoken_rules)
        self.assertIn("long_spoken_sentence", spoken_rules)

    def test_spoken_mode_preserves_plain_spoken_answer(self):
        text = (
            "Yes, I would start with the weekly growth question. We already trust the funnel "
            "data, and the answer changes what the team works on next."
        )
        self.assertEqual(MODULE.audit(text, mode="spoken"), [])

    def test_protects_fenced_code_inline_code_urls_and_tables(self):
        text = (
            "Keep the exact examples below.\n"
            "```text\nGreat question. Here's the thing.\n```\n"
            "Run `great question` at https://example.com/let-me-be-clear.\n"
            "| phrase | result |\n|---|---|\n| Great question | keep |\n"
        )
        self.assertEqual(MODULE.audit(text), [])

    def test_patterns_outside_protected_spans_still_fire(self):
        text = "Great question. Run `great question` after the check."
        findings = MODULE.audit(text)
        self.assertEqual([finding.rule for finding in findings], ["chatbot_artifact"])


if __name__ == "__main__":
    unittest.main()
