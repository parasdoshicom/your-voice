#!/usr/bin/env python3

import importlib.util
import json
import subprocess
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

    def check_home(self, user_home):
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), "--home", str(user_home), "--json"],
            text=True, capture_output=True, check=False,
        )
        return result.returncode, json.loads(result.stdout)

    def test_canonical_links_are_healthy(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            for target in MODULE.expected_targets(user_home):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(MODULE_PATH.parents[1], target_is_directory=True)
            code, payload = self.check_home(user_home)
            self.assertEqual(code, 0)
            self.assertEqual(payload["status"], "healthy")

    def test_separate_copies_are_not_one_canonical_install(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            for target in MODULE.expected_targets(user_home):
                target.mkdir(parents=True)
                (target / "SKILL.md").write_text("stale copy", encoding="utf-8")
            code, payload = self.check_home(user_home)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "needs_repair")
            self.assertTrue(all(row["has_skill"] for row in payload["targets"]))
            self.assertFalse(any(row["is_canonical"] for row in payload["targets"]))

    def test_links_to_a_different_checkout_need_repair(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            other = user_home / "other-checkout"
            other.mkdir()
            (other / "SKILL.md").write_text("other version", encoding="utf-8")
            for target in MODULE.expected_targets(user_home):
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(other, target_is_directory=True)
            code, payload = self.check_home(user_home)
            self.assertEqual(code, 1)
            self.assertEqual(payload["status"], "needs_repair")

    def test_legacy_targets_include_old_codex_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            user_home = Path(directory)
            targets = MODULE.legacy_targets(user_home)
            self.assertIn(user_home / ".codex/skills/your-voice", targets)
            self.assertIn(user_home / ".codex/skills/voicelatch", targets)


if __name__ == "__main__":
    unittest.main()
