#!/usr/bin/env python3
"""Validate WRR source-policy review checklist stays no-input."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md")
DEFAULT_CHECKLIST = Path("reports/wrr_1994/wrr_source_policy_review_checklist.csv")

EXPECTED_ROW = {
    "run_label": "all_lanes_cap1000",
    "checklist_rank": "1",
    "review_state": "pending_source_policy_pair_rule_lock",
    "term_id": "wrr2_32_app_05",
    "term": "$LMHMX@LMA",
    "concept": "WRR2 32",
    "source_flags": "wnp_chelm_spelling_context",
    "residual_pairs": "1",
    "frontier_pairs": "1",
    "related_source_term_ids": "wrr2_32_app_04;wrr2_32_app_05",
    "wnp_evidence_refs": (
        "reports/wrr_1994/wnp_en.html:608-619;"
        "reports/wrr_1994/wnp_en.html:931-935;"
        "reports/wrr_1994/wnp_en.html:1052-1054"
    ),
    "required_decision_record": (
        "cited source/pair-rule decision for Chełm forms before changing source lock"
    ),
    "no_input_boundary": (
        "No source correction, pair exclusion, or replacement lock is selected by "
        "this checklist."
    ),
    "allowed_without_input": "organize evidence only",
    "next_manual_action": (
        "cite primary source/pair-rule evidence before changing working source"
    ),
}

REQUIRED_PHRASES = (
    "# WRR Source-Policy Review Checklist",
    "Status: no-input checklist for Chełm source-policy/pair-rule review.",
    "It does not choose a source correction, exclude a pair, or lock a replacement.",
    "- Source-policy checklist terms: 1.",
    "- Residual pair links: 1.",
    "- Minimum-frontier pair links: 1.",
    "- Related source-review rows: 2.",
    "- Related scenario-pair rows: 4.",
    "- WNP context blocks: 3.",
    "No source correction, pair exclusion, or replacement lock is selected by this checklist.",
    "| 1 | `pending_source_policy_pair_rule_lock` | `wrr2_32_app_05` | `$LMHMX@LMA` |",
    "`reports/wrr_1994/wnp_en.html:608-619`",
    "Citable primary source/pair-rule evidence is required before changing the working source.",
    "The record must say whether Chełm forms belong in the Hebrew source cell, a source-policy note, or neither.",
    "Preserve the working source unless a decision record selects a change.",
)

FORBIDDEN_PHRASES = (
    "selected correction",
    "selected exclusion",
    "source corrected to",
    "pair excluded",
    "replacement locked",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_policy_review_checklist_doc(args.doc, args.checklist)
    if failures:
        for failure in failures:
            print(f"WRR source-policy checklist failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-policy checklist ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--checklist", type=Path, default=DEFAULT_CHECKLIST)
    return parser


def validate_source_policy_review_checklist_doc(
    doc: Path,
    checklist: Path | None = DEFAULT_CHECKLIST,
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
    return failures


def validate_checklist_csv(checklist: Path) -> list[str]:
    rows = _read_csv(checklist)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != 1:
        failures.append(f"{checklist} has {len(rows)} rows; expected 1")
    if not rows:
        return failures
    row = rows[0]
    for key, expected in EXPECTED_ROW.items():
        if row.get(key) != expected:
            failures.append(f"{checklist} {key} drifted")
    related_terms = [term for term in row.get("related_source_term_ids", "").split(";") if term]
    if len(related_terms) != 2:
        failures.append(f"{checklist} related source term count drifted")
    wnp_refs = [ref for ref in row.get("wnp_evidence_refs", "").split(";") if ref]
    if len(wnp_refs) != 3:
        failures.append(f"{checklist} WNP evidence ref count drifted")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
