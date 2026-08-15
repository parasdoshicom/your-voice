#!/usr/bin/env python3
"""Flag reviewable writing patterns without guessing authorship."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


VERSION = "1.2.0"
DEFAULT_FORBIDDEN_PATH = Path("~/.config/your-voice/forbidden.md").expanduser()


@dataclass(frozen=True)
class Finding:
    rule: str
    line: int
    excerpt: str
    advice: str


@dataclass(frozen=True)
class AuditRule:
    name: str
    pattern: re.Pattern[str]
    advice: str


def _rule(name: str, pattern: str, advice: str) -> AuditRule:
    return AuditRule(name, re.compile(pattern, re.IGNORECASE), advice)


LINE_RULES = (
    _rule(
        "throat_clearing",
        r"\b(here(?:'s| is) the (?:thing|truth)|let me be clear|the truth is|"
        r"it(?:'s| is) worth noting|let(?:'s| us) (?:dive in|break this down|explore))\b",
        "Start with the next sentence or the concrete point.",
    ),
    _rule(
        "binary_contrast",
        r"\b(?:it|that|this)(?:'s| is) not\b.{0,120}(?:\bbut\b|[,.!?]\s*(?:it|that|this)(?:'s| is))",
        "State the useful half directly unless the contrast carries evidence.",
    ),
    _rule(
        "empty_comparison",
        r"\bless (?:of )?a\b.{1,80}\bmore (?:of )?a\b",
        "Replace the paired image with the action or decision it implies.",
    ),
    _rule(
        "self_applause",
        r"\b(and that matters|that(?:'s| is) the part (?:everyone|most people) misses|"
        r"which is exactly the point|and that(?:'s| is) the point|i promise)\b",
        "Delete the applause. Let the preceding detail carry the weight.",
    ),
    _rule(
        "unexplained_analogy",
        r"\b(?:it|this|that)(?:'s| is) the [^.!?\n]{1,60} of [^.!?\n]{1,60}[.!?]?\s*$",
        "Explain the shared mechanism or use a direct description.",
    ),
    _rule(
        "faux_insight",
        r"\b(what (?:most people|everyone|nobody) (?:misses|gets wrong|tells you)|the uncomfortable truth)\b",
        "Remove the setup and state the supported observation.",
    ),
    _rule(
        "importance_puffery",
        r"\b(pivotal moment|stands as a testament|plays a (?:vital|crucial) role|underscores (?:the|its) significance)\b",
        "Name the consequence instead of asserting importance.",
    ),
    _rule(
        "chatbot_artifact",
        r"\b(great question|i hope this helps|let me know if you(?:'d| would) like)\b",
        "Remove assistant-to-user residue from the draft.",
    ),
    _rule(
        "ai_vocabulary",
        r"\b(delve|tapestry|multifaceted|paramount|supercharge|ever-evolving|game[ -]?changer)\b",
        "Use the ordinary word the writer would say, or add a concrete fact.",
    ),
    _rule(
        "imprecise_time_range",
        r"\b\d+(?:\.\d+)?\s*(?:to|[-–—])\s*\d+(?:\.\d+)?\s*(?:minutes?|hours?|days?|weeks?)\b",
        "Use the observed duration when one exists. Keep the range if it is measured or genuinely variable.",
    ),
)

# Preserve the v1.1 import surface for callers that inspect the built-in regexes.
RULES = {rule.name: rule.pattern for rule in LINE_RULES}

DOCUMENT_RULES = (
    _rule(
        "binary_contrast",
        r"\b(?:it|that|this)(?:'s| is) not\b[^\n]{0,120}[.!?]\s*\n+\s*"
        r"(?:it|that|this)(?:'s| is)\b",
        "State the useful half directly unless the contrast carries evidence.",
    ),
    _rule(
        "stacked_short_fragments",
        r"(?<![\w'-])([A-Z][\w'-]*(?:\s+[\w'-]+){0,2})[.!]\s+"
        r"([A-Z][\w'-]*(?:\s+[\w'-]+){0,2})[.!](?![\w'-])",
        "Keep the stronger fragment, or join them if both carry information.",
    ),
    _rule(
        "forced_triad",
        r"(?:^|[.!?;:]\s+)([A-Z][\w'-]*(?:\s+[\w'-]+)?),\s+"
        r"([\w'-]+(?:\s+[\w'-]+)?),\s+(?:and\s+)?"
        r"([\w'-]+(?:\s+[\w'-]+)?)(?=[.!?])",
        "Check whether the three-part list is real. Keep the natural number of reasons.",
    ),
)

RECAP_RULE = _rule(
    "recap_ending",
    r"^(?:in short|in summary|to sum up|in conclusion|at the end of the day)\b",
    "End on the last concrete point, implication, or next action.",
)

PASSIVE_PATTERN = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en)\b",
    re.IGNORECASE,
)


def load_forbidden_patterns(path: Path) -> list[AuditRule]:
    """Load literal and regex rules from a small, private Markdown file."""

    rules: list[AuditRule] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            line = line[2:].lstrip()

        kind, separator, value = line.partition(":")
        if not separator or kind.lower() not in {"literal", "regex"} or not value.strip():
            raise ValueError(
                f"{path}:{line_number}: expected 'literal: text' or 'regex: expression'"
            )

        value = value.strip()
        try:
            pattern = re.compile(re.escape(value) if kind.lower() == "literal" else value, re.IGNORECASE)
        except re.error as exc:
            raise ValueError(f"{path}:{line_number}: invalid regex: {exc}") from exc

        rules.append(
            AuditRule(
                f"forbidden_{kind.lower()}_{len(rules) + 1}",
                pattern,
                f"Revise this pattern using the preference recorded in {path.name}.",
            )
        )
    return rules


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _excerpt(value: str) -> str:
    return " ".join(value.strip().split())[:240]


def _technical_findings(text: str) -> Iterable[Finding]:
    sentence_pattern = re.compile(r"[^.!?\n]+(?:[.!?]+|$)")
    for match in sentence_pattern.finditer(text):
        sentence = match.group(0).strip()
        if not sentence or sentence.startswith("#"):
            continue
        line = _line_number(text, match.start())
        word_count = len(re.findall(r"\b[\w'-]+\b", sentence))
        if word_count > 25:
            yield Finding(
                "long_technical_sentence",
                line,
                _excerpt(sentence),
                "Split the sentence so each sentence carries one main instruction or fact.",
            )
        if PASSIVE_PATTERN.search(sentence):
            yield Finding(
                "passive_technical_sentence",
                line,
                _excerpt(sentence),
                "Name the actor and use active voice when the actor is known.",
            )


def audit(
    text: str,
    forbidden_patterns: Iterable[AuditRule] = (),
    mode: str = "voice",
) -> list[Finding]:
    if mode not in {"voice", "technical"}:
        raise ValueError("mode must be 'voice' or 'technical'")

    findings: list[Finding] = []
    seen: set[tuple[str, int, str]] = set()

    def add(finding: Finding) -> None:
        key = (finding.rule, finding.line, finding.excerpt)
        if key not in seen:
            seen.add(key)
            findings.append(finding)

    all_line_rules = (*LINE_RULES, *tuple(forbidden_patterns))
    for line_number, line in enumerate(text.splitlines(), start=1):
        for rule in all_line_rules:
            if rule.pattern.search(line):
                add(Finding(rule.name, line_number, _excerpt(line), rule.advice))
        if "—" in line:
            add(
                Finding(
                    "em_dash",
                    line_number,
                    _excerpt(line),
                    "Keep the dash only if it matches the writer's normal rhythm.",
                )
            )

    for rule in DOCUMENT_RULES:
        for match in rule.pattern.finditer(text):
            add(Finding(rule.name, _line_number(text, match.start()), _excerpt(match.group(0)), rule.advice))

    nonempty_lines = [(number, line.strip()) for number, line in enumerate(text.splitlines(), 1) if line.strip()]
    if nonempty_lines:
        line_number, last_line = nonempty_lines[-1]
        if RECAP_RULE.pattern.search(last_line):
            add(Finding(RECAP_RULE.name, line_number, _excerpt(last_line), RECAP_RULE.advice))

    if mode == "technical":
        for finding in _technical_findings(text):
            add(finding)

    return sorted(findings, key=lambda item: (item.line, item.rule))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", help="UTF-8 text file; stdin when omitted")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--forbidden",
        action="append",
        default=[],
        metavar="PATH",
        help="load a private forbidden-pattern file; repeatable",
    )
    parser.add_argument(
        "--no-default-forbidden",
        action="store_true",
        help="do not load ~/.config/your-voice/forbidden.md when it exists",
    )
    parser.add_argument(
        "--mode",
        choices=("voice", "technical"),
        default="voice",
        help="add technical clarity checks without claiming ASD-STE100 compliance",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    try:
        text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
        forbidden_paths = [Path(value).expanduser() for value in args.forbidden]
        if (
            not args.no_default_forbidden
            and DEFAULT_FORBIDDEN_PATH.is_file()
            and DEFAULT_FORBIDDEN_PATH not in forbidden_paths
        ):
            forbidden_paths.insert(0, DEFAULT_FORBIDDEN_PATH)
        custom_rules = [
            rule
            for forbidden_path in forbidden_paths
            for rule in load_forbidden_patterns(forbidden_path)
        ]
        findings = audit(text, forbidden_patterns=custom_rules, mode=args.mode)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"audit_text.py: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps([asdict(item) for item in findings], indent=2))
    else:
        for item in findings:
            print(f"{item.line}: {item.rule}: {item.excerpt}")
            print(f"  Fix: {item.advice}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
