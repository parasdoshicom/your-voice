#!/usr/bin/env python3
"""Verify that one Your Voice checkout serves the supported host skill roots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def expected_targets(user_home: Path) -> list[Path]:
    targets = [
        user_home / ".agents/skills/your-voice",
        user_home / ".hermes/skills/your-voice",
    ]
    openclaw = user_home / ".openclaw"
    agents = openclaw / "agents"
    if openclaw.exists():
        targets.append(openclaw / "skills/your-voice")
        targets.extend(
            agent_dir / "codex-home/skills/your-voice"
            for agent_dir in sorted(agents.glob("*/agent"))
            if agent_dir.is_dir()
        )
    return targets


def legacy_targets(user_home: Path) -> list[Path]:
    targets = [
        user_home / ".agents/skills/voicelatch",
        user_home / ".codex/skills/your-voice",
        user_home / ".codex/skills/voicelatch",
        user_home / ".hermes/skills/voicelatch",
    ]
    openclaw = user_home / ".openclaw"
    agents = openclaw / "agents"
    if openclaw.exists():
        targets.append(openclaw / "skills/voicelatch")
        targets.extend(
            agent_dir / "codex-home/skills/voicelatch"
            for agent_dir in sorted(agents.glob("*/agent"))
            if agent_dir.is_dir()
        )
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", default=str(Path.home()))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    user_home = Path(args.home)
    rows = []
    for target in expected_targets(user_home):
        resolved = target.resolve() if target.exists() else None
        rows.append(
            {
                "target": str(target),
                "exists": target.exists(),
                "is_symlink": target.is_symlink(),
                "resolved": str(resolved) if resolved else None,
                "has_skill": bool(resolved and (resolved / "SKILL.md").is_file()),
            }
        )
    duplicates = [str(target) for target in legacy_targets(user_home) if target.exists() or target.is_symlink()]
    healthy = bool(rows) and all(row["has_skill"] for row in rows) and not duplicates
    payload = {
        "skill": "your-voice",
        "status": "healthy" if healthy else "needs_repair",
        "targets": rows,
        "duplicate_targets": duplicates,
    }
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload["status"])
        for row in rows:
            print(f"- {row['target']}: {'ok' if row['has_skill'] else 'missing'}")
        for target in duplicates:
            print(f"- duplicate: {target}")
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
