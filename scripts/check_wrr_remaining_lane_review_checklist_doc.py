#!/usr/bin/env python3
"""Validate WRR remaining-lane review checklist stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_remaining_lane_review_checklist as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_CHECKLIST = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES

EXPECTED_TOTALS = {
    "terms": "14",
    "residual_pairs": "14",
    "frontier_pairs": "4",
    "page_image_terms": "3",
    "method_terms": "11",
}

NO_INPUT_BOUNDARY = (
    "No source correction, method change, or pair exclusion is selected by this "
    "checklist."
)
ALLOWED_WITHOUT_INPUT = "organize evidence only"

LANE_LOCKS = {
    "page_image_near_match_review": {
        "terms": 3,
        "residual_pairs": 3,
        "frontier_pairs": 2,
        "review_state": "pending_page_image_lock",
        "row_ocr_status": "not_matched",
        "evidence_required": "page-image inspection against near-match OCR",
        "required_decision_record": (
            "explicit page-image transcription decision with cited image evidence"
        ),
        "next_manual_actions": {"inspect page image before any source correction"},
    },
    "method_or_pair_universe_review": {
        "terms": 11,
        "residual_pairs": 11,
        "frontier_pairs": 2,
        "review_state": "pending_method_pair_universe_lock",
        "row_ocr_status": "matched",
        "evidence_required": (
            "method or pair-universe review for OCR-matched missing ordinary hits"
        ),
        "required_decision_record": (
            "explicit method or pair-universe decision explaining zero ordinary hits"
        ),
        "next_manual_actions": {
            "resolve method or pair universe before frontier pair decision",
            "review after frontier method rows unless scope changes",
        },
    },
}

REQUIRED_PHRASES = (
    "# WRR Remaining-Lane Review Checklist",
    "Status: no-input checklist for page-image and method/pair-universe review.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- Remaining-lane checklist terms: 14.",
    "- Residual pair links: 14.",
    "- Minimum-frontier pair links: 4.",
    "- Page-image terms: 3.",
    "- Method/pair-universe terms: 11.",
    "No source correction, method change, or pair exclusion is selected by this checklist.",
    "| `page_image_near_match_review` | 3 | 3 | 2 | page-image inspection against near-match OCR |",
    "| `method_or_pair_universe_review` | 11 | 11 | 2 | method or pair-universe review for OCR-matched missing ordinary hits |",
    "| 1 | `page_image_near_match_review` | `pending_page_image_lock` | `wrr2_19_app_11` |",
    "| 4 | `method_or_pair_universe_review` | `pending_method_pair_universe_lock` | `wrr2_02_app_03` |",
    "Page-image near-match rows need cited page-image transcription evidence.",
    "Method rows need an explicit method or pair-universe explanation for zero ordinary hits.",
    "Preserve the working source unless a decision record selects a change.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_remaining_lane_review_checklist_doc(
        args.doc,
        args.checklist,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR remaining-lane checklist failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR remaining-lane checklist ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_remaining_lane_review_checklist_doc(
    doc: Path,
    checklist: Path | None = DEFAULT_CHECKLIST,
    manifest: Path | None = DEFAULT_MANIFEST,
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
    if checklist is not None:
        failures.extend(validate_checklist_csv(checklist))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_checklist_csv(checklist: Path) -> list[str]:
    data = _read_csv(checklist)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{checklist} fieldnames drifted")
    expected_rows = int(EXPECTED_TOTALS["terms"])
    if len(rows) != expected_rows:
        failures.append(f"{checklist} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("checklist_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{checklist} checklist_rank sequence drifted")

    checks = {
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
    }
    for metric, actual in checks.items():
        expected = int(EXPECTED_TOTALS[metric])
        if actual != expected:
            failures.append(f"{checklist} {metric}={actual}; expected {expected}")

    lane_counts = {
        "page_image_terms": sum(
            1 for row in rows if row.get("action_lane") == "page_image_near_match_review"
        ),
        "method_terms": sum(
            1
            for row in rows
            if row.get("action_lane") == "method_or_pair_universe_review"
        ),
    }
    for metric, actual in lane_counts.items():
        expected = int(EXPECTED_TOTALS[metric])
        if actual != expected:
            failures.append(f"{checklist} {metric}={actual}; expected {expected}")

    for lane, locks in LANE_LOCKS.items():
        lane_rows = [row for row in rows if row.get("action_lane") == lane]
        lane_failures = _validate_lane_rows(checklist, lane, lane_rows, locks)
        failures.extend(lane_failures)
    known_lanes = set(LANE_LOCKS)
    for row in rows:
        rank = row.get("checklist_rank", "")
        if row.get("action_lane") not in known_lanes:
            failures.append(f"{checklist} rank {rank} unknown lane")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{checklist} rank {rank} no-input boundary drifted")
        if row.get("allowed_without_input") != ALLOWED_WITHOUT_INPUT:
            failures.append(f"{checklist} rank {rank} allowed action drifted")
        if not row.get("term_id") or not row.get("row_number"):
            failures.append(f"{checklist} rank {rank} missing term or row number")
    return failures


def _validate_lane_rows(
    checklist: Path,
    lane: str,
    rows: list[dict[str, str]],
    locks: dict[str, object],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != locks["terms"]:
        failures.append(f"{checklist} {lane} has {len(rows)} rows")
    residual_pairs = sum(_int(row, "residual_pairs") for row in rows)
    frontier_pairs = sum(_int(row, "frontier_pairs") for row in rows)
    if residual_pairs != locks["residual_pairs"]:
        failures.append(f"{checklist} {lane} residual_pairs={residual_pairs}")
    if frontier_pairs != locks["frontier_pairs"]:
        failures.append(f"{checklist} {lane} frontier_pairs={frontier_pairs}")
    for row in rows:
        rank = row.get("checklist_rank", "")
        for key in (
            "review_state",
            "row_ocr_status",
            "evidence_required",
            "required_decision_record",
        ):
            if row.get(key) != locks[key]:
                failures.append(f"{checklist} rank {rank} {key} drifted")
        next_actions = locks["next_manual_actions"]
        if row.get("next_manual_action") not in next_actions:
            failures.append(f"{checklist} rank {rank} manual action drifted")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_remaining_lane_review_checklist",
        "rows": int(EXPECTED_TOTALS["terms"]),
        "summary_rows": 2,
        "residual_pairs": int(EXPECTED_TOTALS["residual_pairs"]),
        "frontier_pairs": int(EXPECTED_TOTALS["frontier_pairs"]),
        "inputs": {
            "packet": str(builder.DEFAULT_PACKET),
            "summary": str(builder.DEFAULT_SUMMARY),
        },
        "outputs": {
            "out": str(DEFAULT_CHECKLIST),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


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
