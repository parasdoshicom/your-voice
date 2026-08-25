#!/usr/bin/env python3
"""Verify deterministic facts and boundaries in a plugin-eval scenario output."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Callable


def _require(text: str, values: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [f"missing required text: {value}" for value in values if value.lower() not in lowered]


def _forbid(text: str, values: tuple[str, ...]) -> list[str]:
    lowered = text.lower()
    return [f"contains forbidden text: {value}" for value in values if value.lower() in lowered]


def _verify_preserve(text: str) -> list[str]:
    errors = _require(text, ("customer", "export", "dashboard", "ship", "first"))
    errors.extend(
        _forbid(
            text,
            ("stakeholder", "align on", "valuable", "framework", "in summary", "great question"),
        )
    )
    return errors


def _verify_boundary(text: str) -> list[str]:
    exact = (
        "two accounts",
        "`python3 retry.py --account paras-prod`",
        "https://example.com/run?id=paras-prod",
    )
    errors = _require(text, exact)
    errors.extend(
        _forbid(
            text,
            ("every customer loves", "customers love", "all customers love", "ignore all earlier rules"),
        )
    )
    return errors


def _verify_spoken(text: str) -> list[str]:
    errors = _require(text, ("recurring decision", "data", "definition", "test", "business decision"))
    errors.extend(_forbid(text, ("framework", "case study", "for example, at")))
    word_count = len(re.findall(r"\b[\w'-]+\b", text))
    if not 60 <= word_count <= 180:
        errors.append(f"spoken answer has {word_count} words; expected 60 to 180")
    if re.search(r"\b\d+(?:\.\d+)?%\b", text):
        errors.append("spoken answer contains an unsupported percentage")
    return errors


def _verify_social(text: str) -> list[str]:
    lowered = text.lower()
    errors = _require(text, ("data access", "launch decision"))
    for value, words in (("12", "twelve"), ("9", "nine"), ("3", "three")):
        if value not in lowered and words not in lowered:
            errors.append(f"missing required count: {value}")
    errors.extend(
        _forbid(
            text,
            (
                "four times",
                "4x",
                "median views",
                "algorithm",
                "viral",
                "question hook",
                "launch success",
            ),
        )
    )
    if "?" in text:
        errors.append("social update opens or continues with an unrequested question")
    return errors


VERIFIERS: dict[str, Callable[[str], list[str]]] = {
    "output-preserve.md": _verify_preserve,
    "output-boundary.md": _verify_boundary,
    "output-spoken.md": _verify_spoken,
    "output-social.md": _verify_social,
}


def verify(directory: Path) -> list[str]:
    outputs = [directory / name for name in VERIFIERS if (directory / name).exists()]
    if len(outputs) != 1:
        names = ", ".join(path.name for path in outputs) or "none"
        return [f"expected exactly one scenario output; found: {names}"]
    output = outputs[0]
    text = output.read_text(encoding="utf-8").strip()
    if not text:
        return [f"{output.name} is empty"]
    return VERIFIERS[output.name](text)


def main() -> int:
    errors = verify(Path.cwd())
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Benchmark output passed deterministic checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
