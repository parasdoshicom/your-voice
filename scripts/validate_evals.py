#!/usr/bin/env python3
"""Validate the model-agnostic Your Voice behavioral benchmark."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


VALID_MODES = {"preserve", "condense", "generate", "spoken", "technical"}
VALID_CRITERIA_ORIGINS = {"top_down", "bottom_up"}
VALID_DIMENSIONS = {
    "meaning",
    "human_move",
    "relationship",
    "point_of_view",
    "recognition",
    "specificity",
    "rhythm_and_restraint",
    "speakability",
}
REQUIRED_STRESS_IDS = {
    "prompt-style-robustness",
    "long-context-retention",
    "output-variation",
    "blind-human-review",
}
REQUIRED_CASE_FIELDS = {
    "id",
    "mode",
    "request",
    "context",
    "source_facts",
    "must_preserve",
    "must_not_add",
    "success_criteria",
    "criteria_origin",
    "failure_modes",
    "rubric_focus",
}


def _nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and item.strip() for item in value
    )


def _validate_rubric(payload: dict[str, Any], errors: list[str]) -> None:
    rubric = payload.get("rubric")
    if not _nonempty_strings(rubric):
        errors.append("rubric must be a non-empty list of strings")
    elif set(rubric) != VALID_DIMENSIONS or len(rubric) != len(VALID_DIMENSIONS):
        errors.append("rubric must contain each supported dimension exactly once")


def _validate_judge_contract(payload: dict[str, Any], errors: list[str]) -> None:
    contract = payload.get("judge_contract")
    if not isinstance(contract, dict):
        errors.append("judge_contract must be an object")
        return
    if contract.get("labels") != ["Pass", "Fail"]:
        errors.append("judge_contract labels must be Pass and Fail")
    for field in (
        "one_failure_mode_per_judge",
        "evidence_required",
        "human_rubric_is_not_judge_score",
    ):
        if contract.get(field) is not True:
            errors.append(f"judge_contract {field} must be true")


def _validate_stress_test(
    stress: Any,
    index: int,
    stress_ids: set[str],
    errors: list[str],
) -> None:
    label = f"stress test {index}"
    if not isinstance(stress, dict):
        errors.append(f"{label} must be an object")
        return
    stress_id = stress.get("id")
    if not isinstance(stress_id, str) or not stress_id.strip():
        errors.append(f"{label} id must be a non-empty string")
    elif stress_id in stress_ids:
        errors.append(f"duplicate stress test id: {stress_id}")
    else:
        stress_ids.add(stress_id)
        label = stress_id
    if not isinstance(stress.get("procedure"), str) or not stress["procedure"].strip():
        errors.append(f"{label} procedure must be a non-empty string")
    if not _nonempty_strings(stress.get("pass_criteria")):
        errors.append(f"{label} pass_criteria must be a non-empty list of strings")


def _validate_stress_tests(payload: dict[str, Any], errors: list[str]) -> None:
    stress_tests = payload.get("stress_tests")
    if not isinstance(stress_tests, list) or not stress_tests:
        errors.append("stress_tests must be a non-empty list")
        return
    stress_ids: set[str] = set()
    for index, stress in enumerate(stress_tests, start=1):
        _validate_stress_test(stress, index, stress_ids, errors)
    missing_stress = sorted(REQUIRED_STRESS_IDS - stress_ids)
    if missing_stress:
        errors.append(f"stress_tests missing required ids: {', '.join(missing_stress)}")


def _validate_case(
    case: Any,
    index: int,
    case_ids: set[str],
    errors: list[str],
) -> str | None:
    label = f"case {index}"
    if not isinstance(case, dict):
        errors.append(f"{label} must be an object")
        return None
    missing = sorted(REQUIRED_CASE_FIELDS - set(case))
    if missing:
        errors.append(f"{label} missing fields: {', '.join(missing)}")

    case_id = case.get("id")
    if not isinstance(case_id, str) or not case_id.strip():
        errors.append(f"{label} id must be a non-empty string")
    elif case_id in case_ids:
        errors.append(f"duplicate case id: {case_id}")
    else:
        case_ids.add(case_id)
        label = case_id

    mode = case.get("mode")
    if mode not in VALID_MODES:
        errors.append(f"{label} has unsupported mode: {mode}")
        mode = None

    for field in ("request", "context"):
        if not isinstance(case.get(field), str) or not case[field].strip():
            errors.append(f"{label} {field} must be a non-empty string")
    for field in ("source_facts", "must_preserve", "must_not_add", "success_criteria"):
        if not _nonempty_strings(case.get(field)):
            errors.append(f"{label} {field} must be a non-empty list of strings")

    origin = case.get("criteria_origin")
    if origin not in VALID_CRITERIA_ORIGINS:
        errors.append(f"{label} criteria_origin must be top_down or bottom_up")
    if not _nonempty_strings(case.get("failure_modes")):
        errors.append(f"{label} failure_modes must be a non-empty list of strings")

    focus = case.get("rubric_focus")
    if not _nonempty_strings(focus):
        errors.append(f"{label} rubric_focus must be a non-empty list of strings")
    elif not set(focus).issubset(VALID_DIMENSIONS):
        errors.append(f"{label} rubric_focus contains an unsupported dimension")
    if mode == "spoken" and isinstance(focus, list) and "speakability" not in focus:
        errors.append(f"{label} spoken cases must focus on speakability")
    return mode


def validate(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["benchmark must be a JSON object"]
    if payload.get("version") != 3:
        errors.append("version must be 3")

    _validate_rubric(payload, errors)
    _validate_judge_contract(payload, errors)
    _validate_stress_tests(payload, errors)

    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        errors.append("cases must be a non-empty list")
        return errors

    case_ids: set[str] = set()
    represented_modes: set[str] = set()
    represented_origins: set[str] = set()
    for index, case in enumerate(cases, start=1):
        mode = _validate_case(case, index, case_ids, errors)
        if mode:
            represented_modes.add(mode)
        if isinstance(case, dict) and case.get("criteria_origin") in VALID_CRITERIA_ORIGINS:
            represented_origins.add(case["criteria_origin"])

    if not {"preserve", "condense", "generate", "spoken", "technical"}.issubset(
        represented_modes
    ):
        errors.append("benchmark must represent every transformation mode")
    if represented_origins != VALID_CRITERIA_ORIGINS:
        errors.append("benchmark must represent top_down and bottom_up criteria")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="evals/benchmark.json")
    args = parser.parse_args()
    path = Path(args.path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"validate_evals.py: {exc}", file=sys.stderr)
        return 2

    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(payload['cases'])} behavioral eval cases in {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
