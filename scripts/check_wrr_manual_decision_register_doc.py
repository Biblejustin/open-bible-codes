#!/usr/bin/env python3
"""Validate WRR manual-decision register remains a lane inventory."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_MANUAL_DECISION_REGISTER.md")
DEFAULT_REGISTER = Path("reports/wrr_1994/wrr_manual_decision_register.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_manual_decision_register_summary.csv")

NO_INPUT_BOUNDARY = (
    "No source correction, row transcription, pair exclusion, replacement lock, "
    "or method change is selected by this register."
)
ALLOWED_WITHOUT_INPUT = "organize evidence only"

LANE_LOCKS = {
    "source_policy_pair_rule": {
        "decision_rows": 1,
        "action_terms": 1,
        "residual_pairs": 1,
        "frontier_pairs": 1,
        "review_state": "pending_source_policy_pair_rule_lock",
        "required_decision_record": (
            "cited source/pair-rule decision for Chełm forms before changing source lock"
        ),
        "source_checklist": "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md",
    },
    "source_transcription_row_cluster": {
        "decision_rows": 22,
        "action_terms": 43,
        "residual_pairs": 44,
        "frontier_pairs": 35,
        "review_state": "pending_manual_source_lock",
        "required_decision_record": (
            "explicit keep, correct, exclude, or method/pair-universe decision "
            "recorded outside this checklist"
        ),
        "source_checklist": "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
    },
    "page_image_near_match": {
        "decision_rows": 3,
        "action_terms": 3,
        "residual_pairs": 3,
        "frontier_pairs": 2,
        "review_state": "pending_page_image_lock",
        "required_decision_record": (
            "explicit page-image transcription decision with cited image evidence"
        ),
        "source_checklist": "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
    },
    "method_pair_universe": {
        "decision_rows": 11,
        "action_terms": 11,
        "residual_pairs": 11,
        "frontier_pairs": 2,
        "review_state": "pending_method_pair_universe_lock",
        "required_decision_record": (
            "explicit method or pair-universe decision explaining zero ordinary hits"
        ),
        "source_checklist": "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
    },
}

EXPECTED_TOTALS = {
    "decision_rows": 37,
    "action_terms": 58,
    "residual_pairs": 59,
    "frontier_pairs": 40,
}

REQUIRED_PHRASES = (
    "# WRR Manual Decision Register",
    "Status: consolidated lane register for WRR manual-decision records.",
    "It defines decision ranks, lanes, targets, and evidence requirements; current lock status lives in `data/study/mappings/wrr_manual_decision_records.csv`.",
    "It does not choose source corrections, row transcriptions, pair exclusions, replacement locks, or method changes.",
    "- Manual decision rows: 37.",
    "- Action terms represented: 58.",
    "- Residual pair links represented: 59.",
    "- Minimum-frontier pair links represented: 40.",
    "- Source-policy/pair-rule decision rows: 1.",
    "- Source-transcription row-cluster decision rows: 22.",
    "- Page-image decision rows: 3.",
    "- Method/pair-universe decision rows: 11.",
    "No source correction, row transcription, pair exclusion, replacement lock, or method change is selected by this register.",
    "| `source_policy_pair_rule` | 1 | 1 | 1 | 1 |",
    "| `source_transcription_row_cluster` | 22 | 43 | 44 | 35 |",
    "| `page_image_near_match` | 3 | 3 | 3 | 2 |",
    "| `method_pair_universe` | 11 | 11 | 11 | 2 |",
    "| 1 | `source_policy_pair_rule` | `pending_source_policy_pair_rule_lock` |",
    "| 2 | `source_transcription_row_cluster` | `pending_manual_source_lock` |",
    "| 24 | `page_image_near_match` | `pending_page_image_lock` |",
    "| 27 | `method_pair_universe` | `pending_method_pair_universe_lock` |",
    "Source-policy/pair-rule rows need citable source and pair-rule evidence.",
    "Source-transcription row clusters need cited row image or source-list transcription plus row/column alignment evidence.",
    "Page-image rows need cited page-image transcription evidence.",
    "Method/pair-universe rows need an explicit explanation for zero ordinary hits.",
    "Use `data/study/mappings/wrr_manual_decision_records.csv` for current lock status.",
    "This register remains the rank/lane/target inventory for those records.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
    "replacement locked",
    "method changed to",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_manual_decision_register_doc(
        args.doc,
        args.register,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR manual decision register failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR manual decision register ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--register", type=Path, default=DEFAULT_REGISTER)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_manual_decision_register_doc(
    doc: Path,
    register: Path | None = DEFAULT_REGISTER,
    summary: Path | None = DEFAULT_SUMMARY,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    failures.extend(
        f"{doc} contains forbidden phrase: {phrase}"
        for phrase in FORBIDDEN_PHRASES
        if phrase in normalized_text
    )
    if register is not None:
        failures.extend(validate_register_csv(register))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    return failures


def validate_register_csv(register: Path) -> list[str]:
    rows = _read_csv(register)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    expected_rows = EXPECTED_TOTALS["decision_rows"]
    if len(rows) != expected_rows:
        failures.append(f"{register} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("decision_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{register} decision_rank sequence drifted")

    checks = {
        "action_terms": sum(_int(row, "action_terms") for row in rows),
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
    }
    for metric, actual in checks.items():
        expected = EXPECTED_TOTALS[metric]
        if actual != expected:
            failures.append(f"{register} {metric}={actual}; expected {expected}")

    for lane, locks in LANE_LOCKS.items():
        lane_rows = [row for row in rows if row.get("decision_lane") == lane]
        failures.extend(_validate_lane_rows(register, lane, lane_rows, locks))
    known_lanes = set(LANE_LOCKS)
    for row in rows:
        rank = row.get("decision_rank", "")
        if row.get("decision_lane") not in known_lanes:
            failures.append(f"{register} rank {rank} unknown lane")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{register} rank {rank} no-input boundary drifted")
        if row.get("allowed_without_input") != ALLOWED_WITHOUT_INPUT:
            failures.append(f"{register} rank {rank} allowed action drifted")
        if not row.get("decision_target") or not row.get("concept"):
            failures.append(f"{register} rank {rank} missing target or concept")
    return failures


def _validate_lane_rows(
    register: Path,
    lane: str,
    rows: list[dict[str, str]],
    locks: dict[str, object],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != locks["decision_rows"]:
        failures.append(f"{register} {lane} has {len(rows)} rows")
    for metric in ("action_terms", "residual_pairs", "frontier_pairs"):
        actual = sum(_int(row, metric) for row in rows)
        if actual != locks[metric]:
            failures.append(f"{register} {lane} {metric}={actual}")
    for row in rows:
        rank = row.get("decision_rank", "")
        for key in ("review_state", "required_decision_record", "source_checklist"):
            if row.get(key) != locks[key]:
                failures.append(f"{register} rank {rank} {key} drifted")
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    rows = _read_csv(summary)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != len(LANE_LOCKS):
        failures.append(f"{summary} has {len(rows)} rows; expected {len(LANE_LOCKS)}")
    lanes = {row.get("decision_lane", ""): row for row in rows}
    if set(lanes) != set(LANE_LOCKS):
        failures.append(f"{summary} lane set drifted")
    for lane, locks in LANE_LOCKS.items():
        row = lanes.get(lane)
        if row is None:
            continue
        for key in (
            "decision_rows",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
            "review_state",
        ):
            expected = str(locks[key])
            if row.get(key) != expected:
                failures.append(f"{summary} {lane} {key} drifted")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "0")
    try:
        return int(value)
    except ValueError:
        return 0


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
