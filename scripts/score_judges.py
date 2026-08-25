#!/usr/bin/env python3
"""Validate human/judge labels and report TPR and TNR by failure mode."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


LABELS = {"Pass", "Fail"}
SPLITS = {"train", "dev", "test"}
REQUIRED_FIELDS = {
    "id",
    "failure_mode",
    "split",
    "human_label",
    "judge_label",
    "evidence",
}


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as exc:
        return [], [str(exc)]
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_number}: row must be an object")
            continue
        row["_line"] = line_number
        rows.append(row)
    return rows, errors


def validate_rows(rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, row in enumerate(rows, start=1):
        line = row.get("_line", index)
        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            errors.append(f"line {line}: missing fields: {', '.join(missing)}")
            continue
        row_id = row["id"]
        if not isinstance(row_id, str) or not row_id.strip():
            errors.append(f"line {line}: id must be a non-empty string")
        elif row_id in seen_ids:
            errors.append(f"line {line}: duplicate id: {row_id}")
        else:
            seen_ids.add(row_id)
        if not isinstance(row["failure_mode"], str) or not row["failure_mode"].strip():
            errors.append(f"line {line}: failure_mode must be a non-empty string")
        if row["split"] not in SPLITS:
            errors.append(f"line {line}: split must be train, dev, or test")
        for field in ("human_label", "judge_label"):
            if row[field] not in LABELS:
                errors.append(f"line {line}: {field} must be Pass or Fail")
        if not isinstance(row["evidence"], str) or not row["evidence"].strip():
            errors.append(f"line {line}: evidence must cite the draft text or decision")
    if not rows:
        errors.append("label file contains no rows")
    return errors


def score_rows(rows: list[dict[str, Any]], split: str = "test") -> dict[str, dict[str, Any]]:
    selected = [row for row in rows if row.get("split") == split]
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in selected:
        grouped[row["failure_mode"]].append(row)

    results: dict[str, dict[str, Any]] = {}
    for failure_mode, mode_rows in sorted(grouped.items()):
        tp = sum(
            row["human_label"] == "Pass" and row["judge_label"] == "Pass"
            for row in mode_rows
        )
        fn = sum(
            row["human_label"] == "Pass" and row["judge_label"] == "Fail"
            for row in mode_rows
        )
        tn = sum(
            row["human_label"] == "Fail" and row["judge_label"] == "Fail"
            for row in mode_rows
        )
        fp = sum(
            row["human_label"] == "Fail" and row["judge_label"] == "Pass"
            for row in mode_rows
        )
        pass_count = tp + fn
        fail_count = tn + fp
        results[failure_mode] = {
            "rows": len(mode_rows),
            "human_pass": pass_count,
            "human_fail": fail_count,
            "true_pass": tp,
            "false_fail": fn,
            "true_fail": tn,
            "false_pass": fp,
            "tpr": tp / pass_count if pass_count else None,
            "tnr": tn / fail_count if fail_count else None,
        }
    return results


def threshold_failures(
    results: dict[str, dict[str, Any]],
    min_per_label: int,
    min_rate: float,
) -> list[str]:
    failures: list[str] = []
    if not results:
        return ["no rows matched the requested split"]
    for failure_mode, result in results.items():
        if result["human_pass"] < min_per_label:
            failures.append(
                f"{failure_mode}: only {result['human_pass']} human Pass labels; "
                f"need {min_per_label}"
            )
        if result["human_fail"] < min_per_label:
            failures.append(
                f"{failure_mode}: only {result['human_fail']} human Fail labels; "
                f"need {min_per_label}"
            )
        for metric in ("tpr", "tnr"):
            value = result[metric]
            if value is None or value < min_rate:
                rendered = "undefined" if value is None else f"{value:.3f}"
                failures.append(
                    f"{failure_mode}: {metric.upper()} {rendered} is below {min_rate:.3f}"
                )
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--split", choices=sorted(SPLITS), default="test")
    parser.add_argument("--min-per-label", type=int, default=1)
    parser.add_argument("--min-rate", type=float, default=0.0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.min_per_label < 1:
        parser.error("--min-per-label must be at least 1")
    if not 0.0 <= args.min_rate <= 1.0:
        parser.error("--min-rate must be between 0 and 1")

    rows, errors = load_jsonl(args.path)
    errors.extend(validate_rows(rows))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    results = score_rows(rows, split=args.split)
    failures = threshold_failures(results, args.min_per_label, args.min_rate)
    if args.json:
        print(json.dumps({"split": args.split, "results": results, "failures": failures}, indent=2))
    else:
        for failure_mode, result in results.items():
            tpr = "undefined" if result["tpr"] is None else f"{result['tpr']:.3f}"
            tnr = "undefined" if result["tnr"] is None else f"{result['tnr']:.3f}"
            print(
                f"{failure_mode}: n={result['rows']} "
                f"TPR={tpr} TNR={tnr}"
            )
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
