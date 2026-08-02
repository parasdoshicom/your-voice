#!/usr/bin/env python3
"""Flag surface-level writing patterns without guessing authorship."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    rule: str
    line: int
    excerpt: str


RULES = {
    "throat_clearing": re.compile(
        r"\b(here(?:'s| is) the (?:thing|truth)|let me be clear|it(?:'s| is) worth noting|let(?:'s| us) dive in)\b",
        re.IGNORECASE,
    ),
    "binary_contrast": re.compile(
        r"\b(?:it(?:'s| is)|this is|the question is) not\b.{0,100}\b(?:it(?:'s| is)|but)\b",
        re.IGNORECASE,
    ),
    "faux_insight": re.compile(
        r"\b(what (?:most people|everyone|nobody) (?:misses|gets wrong|tells you)|the uncomfortable truth)\b",
        re.IGNORECASE,
    ),
    "importance_puffery": re.compile(
        r"\b(pivotal moment|stands as a testament|plays a (?:vital|crucial) role|underscores (?:the|its) significance)\b",
        re.IGNORECASE,
    ),
    "chatbot_artifact": re.compile(
        r"\b(great question|i hope this helps|let me know if you(?:'d| would) like)\b",
        re.IGNORECASE,
    ),
    "ai_vocabulary": re.compile(
        r"\b(delve|tapestry|multifaceted|paramount|supercharge|ever-evolving|game[ -]?changer)\b",
        re.IGNORECASE,
    ),
}


def audit(text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule, pattern in RULES.items():
            if pattern.search(line):
                findings.append(Finding(rule, line_number, line.strip()[:240]))
        if "—" in line:
            findings.append(Finding("em_dash", line_number, line.strip()[:240]))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="UTF-8 text file; stdin when omitted")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()

    text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
    findings = audit(text)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    else:
        for item in findings:
            print(f"{item.line}: {item.rule}: {item.excerpt}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())

