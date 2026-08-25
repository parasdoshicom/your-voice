#!/usr/bin/env python3
"""Find candidate public writing skills through GitHub's public API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from urllib.error import HTTPError
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

TRACKED_UPSTREAMS = (
    ("blader/humanizer", "v2.11.1"),
    ("conorbronsdon/avoid-ai-writing", "v3.26.0"),
    ("petergyang/no-ai-slop", "v1.0.6"),
    ("hardikpandya/stop-slop", "8da1f030185b"),
    ("cosmos-makers/writer-persona", "5eee0fd5b0c2"),
    ("AshwinSathian/humanize-writing-skill", "0c3f05bc4f37"),
    ("ai-evals-course/evals-skills", "b91c188388ef"),
)


def github_api(path: str) -> object:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "your-voice-discovery"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/{path.lstrip('/')}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def github_search(query: str, per_page: int) -> list[dict[str, object]]:
    path = "search/repositories?" + urllib.parse.urlencode(
        {"q": query, "sort": "updated", "order": "desc", "per_page": per_page}
    )
    payload = github_api(path)
    return payload.get("items", []) if isinstance(payload, dict) else []


def upstream_status(repo: str) -> dict[str, str]:
    metadata = github_api(f"repos/{repo}")
    if not isinstance(metadata, dict):
        raise ValueError(f"unexpected metadata for {repo}")
    default_branch = str(metadata.get("default_branch") or "main")
    head = github_api(f"repos/{repo}/commits/{default_branch}")
    if not isinstance(head, dict):
        raise ValueError(f"unexpected head commit for {repo}")
    try:
        release = github_api(f"repos/{repo}/releases/latest")
    except HTTPError as exc:
        if exc.code != 404:
            raise
        release = {}
    return {
        "head": str(head.get("sha") or "unknown")[:12],
        "pushed": str(metadata.get("pushed_at") or "unknown"),
        "release": str(release.get("tag_name") or "none") if isinstance(release, dict) else "none",
    }


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

    lines.extend(["", "## Tracked upstreams", ""])
    upstream_errors: list[str] = []
    for repo, reviewed in TRACKED_UPSTREAMS:
        try:
            status = upstream_status(repo)
            lines.extend(
                [
                    f"- [{repo}](https://github.com/{repo})",
                    f"  - reviewed: `{reviewed}`",
                    f"  - latest release: `{status['release']}`",
                    f"  - head: `{status['head']}`",
                    f"  - pushed: `{status['pushed']}`",
                ]
            )
        except Exception as exc:  # keep candidate discovery useful if one upstream probe fails
            upstream_errors.append(f"- `{repo}`: {type(exc).__name__}")
    if upstream_errors:
        lines.extend(["", "### Upstream scan errors", "", *upstream_errors])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
