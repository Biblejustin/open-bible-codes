#!/usr/bin/env python3
"""Validate WRR manual-decision record worksheet stays no-input."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md")

REQUIRED_PHRASES = (
    "# WRR Manual Decision Record Worksheet",
    "Status: no-input worksheet for future WRR manual decision records.",
    "It does not populate `data/study/mappings/wrr_manual_decision_records.csv`.",
    "Header-only current status means no correction, transcription, method change, replacement lock, or pair exclusion has been selected.",
    "- Worksheet rows: 37.",
    "- Source-policy/pair-rule rows: 1.",
    "- Source-transcription row-cluster rows: 22.",
    "- Page-image rows: 3.",
    "- Method/pair-universe rows: 11.",
    "- Target records file: `data/study/mappings/wrr_manual_decision_records.csv`.",
    "The worksheet gives exact `decision_id` and register fields. Evidence, selected action, reviewer, and lock date still require manual input.",
    "`decision_id,register_decision_rank,decision_lane,review_state,decision_target,source_checklist,decision_status,selected_action,evidence_citation,evidence_summary,locked_by,locked_at,notes`",
    "`wrr_decision_001`",
    "`wrr_decision_037`",
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
    failures = validate_worksheet_doc(args.doc)
    if failures:
        for failure in failures:
            print(f"WRR manual decision record worksheet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR manual decision record worksheet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_worksheet_doc(doc: Path) -> list[str]:
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
    return failures


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
