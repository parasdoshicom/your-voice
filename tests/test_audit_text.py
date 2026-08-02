#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "audit_text.py"
SPEC = importlib.util.spec_from_file_location("voicelatch_audit", MODULE_PATH)
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


if __name__ == "__main__":
    unittest.main()

