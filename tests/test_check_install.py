#!/usr/bin/env python3

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "check_install.py"
SPEC = importlib.util.spec_from_file_location("your_voice_check_install", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class InstallTargetTests(unittest.TestCase):
    def test_default_targets_cover_codex_and_hermes_without_creating_openclaw(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            self.assertEqual(
                MODULE.expected_targets(user_home),
                [
                    user_home / ".agents/skills/your-voice",
                    user_home / ".hermes/skills/your-voice",
                ],
            )

    def test_existing_openclaw_adds_global_and_agent_targets(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            agent_dir = user_home / ".openclaw/agents/paras/agent"
            agent_dir.mkdir(parents=True)
            self.assertEqual(
                MODULE.expected_targets(user_home)[-2:],
                [
                    user_home / ".openclaw/skills/your-voice",
                    agent_dir / "codex-home/skills/your-voice",
                ],
            )

    def test_legacy_targets_include_old_codex_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            targets = MODULE.legacy_targets(user_home)
            self.assertIn(user_home / ".codex/skills/your-voice", targets)
            self.assertIn(user_home / ".codex/skills/voicelatch", targets)


if __name__ == "__main__":
    unittest.main()
