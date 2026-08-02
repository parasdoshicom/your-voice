#!/usr/bin/env python3
"""Verify that one VoiceLatch checkout serves the supported host skill roots."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def expected_targets(user_home: Path) -> list[Path]:
    targets = [
        user_home / ".codex/skills/voicelatch",
        user_home / ".openclaw/skills/voicelatch",
    ]
    agents = user_home / ".openclaw/agents"
    if agents.exists():
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

    rows = []
    for target in expected_targets(Path(args.home)):
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
    healthy = bool(rows) and all(row["has_skill"] for row in rows)
    payload = {"status": "healthy" if healthy else "needs_repair", "targets": rows}
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(payload["status"])
        for row in rows:
            print(f"- {row['target']}: {'ok' if row['has_skill'] else 'missing'}")
    return 0 if healthy else 1


if __name__ == "__main__":
    raise SystemExit(main())
