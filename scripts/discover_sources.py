#!/usr/bin/env python3
"""Find candidate public writing skills through GitHub's public API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path


QUERIES = (
    'humanizer topic:agent-skills',
    '"no-ai-slop" in:name,description,readme',
    '"stop-slop" in:name,description,readme',
    '"voice calibration" "SKILL.md" in:readme',
)

SIGNALS = (
    "ai writing",
    "agent skill",
    "humanizer",
    "no ai slop",
    "no-ai-slop",
    "stop slop",
    "stop-slop",
    "voice calibration",
    "writing voice",
)


def github_search(query: str, per_page: int) -> list[dict[str, object]]:
    url = "https://api.github.com/search/repositories?" + urllib.parse.urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": per_page}
    )
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "your-voice-discovery"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response).get("items", [])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="reports/candidates.md")
    parser.add_argument("--per-query", type=int, default=5)
    args = parser.parse_args()

    seen: dict[str, dict[str, object]] = {}
    errors: list[str] = []
    for query in QUERIES:
        try:
            for item in github_search(query, args.per_query):
                haystack = " ".join(
                    [str(item.get("name") or ""), str(item.get("description") or "")]
                ).lower()
                if any(signal in haystack for signal in SIGNALS):
                    seen[str(item["full_name"])] = item
        except Exception as exc:  # report a bounded discovery failure without hiding it
            errors.append(f"- `{query}`: {type(exc).__name__}")

    lines = [
        "# Your Voice discovery candidates",
        "",
        f"Generated: {dt.date.today().isoformat()}",
        "",
        "Discovery does not imply endorsement or adoption. Check provenance, license, code, privacy, and eval impact.",
        "",
    ]
    for name, item in sorted(seen.items(), key=lambda pair: str(pair[1].get("updated_at", "")), reverse=True):
        description = str(item.get("description") or "No description").replace("\n", " ")
        lines.extend(
            [
                f"- [{name}]({item['html_url']})",
                f"  - updated: `{item.get('updated_at', 'unknown')}`",
                f"  - license: `{(item.get('license') or {}).get('spdx_id', 'unknown')}`",
                f"  - description: {description}",
            ]
        )
    if not seen:
        lines.append("No new candidates matched the review filter.")
    if errors:
        lines.extend(["", "## Discovery errors", "", *errors])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
