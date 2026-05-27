#!/usr/bin/env python3
"""Validate WRR source-transcription row checklist stays no-input."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_source_transcription_row_review_checklist as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_CHECKLIST = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES

EXPECTED_TOTALS = {
    "row_clusters": "22",
    "action_terms": "43",
    "residual_pairs": "44",
    "frontier_pairs": "35",
}

REVIEW_STATE = "pending_manual_source_lock"
SOURCE_EVIDENCE = (
    "citable primary Table 2 row image or source-list row transcription for this row"
)
ALIGNMENT_EVIDENCE = (
    "row-number and column alignment evidence tying the cited transcription to the "
    "imported WRR2 terms"
)
DECISION_RECORD = (
    "explicit keep, correct, exclude, or method/pair-universe decision recorded "
    "outside this checklist"
)
NO_INPUT_BOUNDARY = (
    "No row transcription, source correction, pair exclusion, or method change is "
    "selected by this checklist."
)
ALLOWED_WITHOUT_INPUT = "organize evidence only"
ALLOWED_NEXT_ACTIONS = {
    "review row image once before individual term decisions",
    "review row image before any frontier pair decision",
    "review after frontier rows unless policy scope changes",
}

REQUIRED_PHRASES = (
    "# WRR Source-Transcription Row Review Checklist",
    "Status: no-input checklist for row-level source-transcription review.",
    "It does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "- Row review clusters: 22.",
    "- Source-transcription action terms: 43.",
    "- Residual pair links: 44.",
    "- Minimum-frontier pair links: 35.",
    "- Review state: `pending_manual_source_lock`.",
    "No row transcription, source correction, pair exclusion, or method change is selected by this checklist.",
    "| 1 | `06` | `WRR2 06` | `pending_manual_source_lock` | 4 | 4 | 4 |",
    "`wrr2_06_app_03 B@LM@$YH$M",
    "review row image once before individual term decisions",
    "Cite the primary row image or source-list row transcription used.",
    "Record keep, correct, exclude, or method/pair-universe decision outside this checklist.",
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
    failures = validate_row_review_checklist_doc(
        args.doc,
        args.checklist,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(
                f"WRR source-transcription row checklist failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR source-transcription row checklist ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_row_review_checklist_doc(
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
    expected_rows = int(EXPECTED_TOTALS["row_clusters"])
    if len(rows) != expected_rows:
        failures.append(f"{checklist} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("row_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{checklist} row_rank sequence drifted")

    checks = {
        "action_terms": sum(_int(row, "action_terms") for row in rows),
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
    }
    for metric, actual in checks.items():
        expected = int(EXPECTED_TOTALS[metric])
        if actual != expected:
            failures.append(f"{checklist} {metric}={actual}; expected {expected}")

    for row in rows:
        rank = row.get("row_rank", "")
        if row.get("review_state") != REVIEW_STATE:
            failures.append(f"{checklist} rank {rank} review state drifted")
        if row.get("required_source_evidence") != SOURCE_EVIDENCE:
            failures.append(f"{checklist} rank {rank} source evidence drifted")
        if row.get("required_alignment_evidence") != ALIGNMENT_EVIDENCE:
            failures.append(f"{checklist} rank {rank} alignment evidence drifted")
        if row.get("required_decision_record") != DECISION_RECORD:
            failures.append(f"{checklist} rank {rank} decision record drifted")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{checklist} rank {rank} no-input boundary drifted")
        if row.get("allowed_without_input") != ALLOWED_WITHOUT_INPUT:
            failures.append(f"{checklist} rank {rank} allowed action drifted")
        if row.get("next_manual_action") not in ALLOWED_NEXT_ACTIONS:
            failures.append(f"{checklist} rank {rank} manual action drifted")
        if "Hebrew cells are not verified." not in row.get("table2_bridge_read", ""):
            failures.append(f"{checklist} rank {rank} bridge boundary drifted")
        if not row.get("row_number") or not row.get("concept"):
            failures.append(f"{checklist} rank {rank} missing row id")
        terms = [term for term in row.get("terms_to_verify", "").split(";") if term]
        if len(terms) != _int(row, "action_terms"):
            failures.append(f"{checklist} rank {rank} term count mismatch")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_source_transcription_row_review_checklist",
        "rows": int(EXPECTED_TOTALS["row_clusters"]),
        "action_terms": int(EXPECTED_TOTALS["action_terms"]),
        "residual_pairs": int(EXPECTED_TOTALS["residual_pairs"]),
        "frontier_pairs": int(EXPECTED_TOTALS["frontier_pairs"]),
        "inputs": {"row_summary": str(builder.DEFAULT_ROW_SUMMARY)},
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
