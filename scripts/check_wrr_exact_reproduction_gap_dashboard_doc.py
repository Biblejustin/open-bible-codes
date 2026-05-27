#!/usr/bin/env python3
"""Validate the WRR exact-reproduction gap dashboard keeps boundaries visible."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_exact_reproduction_gap_dashboard as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_DASHBOARD = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES
EXPECTED_GAP_REASON_ROWS = 3
EXPECTED_REVIEW_LANE_ROWS = 4

EXPECTED_ROWS = {
    "exact_published_reproduction": (
        "status",
        "not_reproduced",
        "open",
    ),
    "local_locked_report": (
        "status",
        "locked local WRR method report; not an exact published WRR reproduction",
        "locked_local",
    ),
    "source_cited_defined_distances": (
        "gap",
        "163",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "current_defined_distances": (
        "gap",
        "72",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "remaining_gap": (
        "gap",
        "91",
        "diagnostic_only_not_wrr_reproduction",
    ),
    "residual_after_simple_variants": (
        "variant_upper_bound",
        "40",
        "diagnostic_upper_bound_not_source_correction",
    ),
    "manual_decision_inventory": (
        "manual_locks",
        "37 rows; 58 action terms; 40 frontier pair links",
        "locked_no_source_change_or_method_lock",
    ),
    "manual_decision_records": (
        "manual_locks",
        "37 locked; 0 unlocked; method_lock=11; no_source_change=26",
        "all_current_manual_reviews_locked",
    ),
    "source_policy_pair_rule_lock": (
        "manual_locks",
        "wrr_decision_001 no_source_change",
        "locked",
    ),
    "ordinary_missing_appellation_hits": ("gap_reason", "83", "diagnostic"),
    "ordinary_missing_date_hits": ("gap_reason", "12", "diagnostic"),
    "ordinary_missing_both_terms": ("gap_reason", "15", "diagnostic"),
    "source_policy_or_pair_rule_review": (
        "review_lane",
        "1 terms; 1 residual pairs; 1 frontier pairs",
        "pending_review",
    ),
    "source_transcription_or_row_alignment": (
        "review_lane",
        "43 terms; 44 residual pairs; 35 frontier pairs",
        "pending_review",
    ),
    "page_image_near_match_review": (
        "review_lane",
        "3 terms; 3 residual pairs; 2 frontier pairs",
        "pending_review",
    ),
    "method_or_pair_universe_review": (
        "review_lane",
        "11 terms; 11 residual pairs; 2 frontier pairs",
        "pending_review",
    ),
    "post-lock reporting boundary": (
        "recommended_next",
        "organize_evidence_only",
        "no_source_change",
    ),
    "exact-published gap language": (
        "recommended_next",
        "organize_evidence_only",
        "no_source_change",
    ),
}

REQUIRED_PHRASES = (
    "# WRR Exact Reproduction Gap Dashboard",
    "Status: exact published WRR reproduction is not closed.",
    "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
    "Source-cited defined distances | 163",
    "Current defined distances | 72",
    "Remaining 163-distance gap | 91",
    "Residual gap after simple-variant upper bound | 40",
    "Manual decision rows | 37",
    "Locked manual decision records | 37",
    "Unlocked manual decision records | 0",
    "Recorded selected actions | method_lock=11; no_source_change=26",
    "| `source_policy_or_pair_rule_review` | 1 | 1 | 1 |",
    "| `source_transcription_or_row_alignment` | 43 | 44 | 35 |",
    "Chelm source-policy/pair-rule target | locked | no_source_change",
    "post-lock reporting boundary",
    "all current manual review rows are locked",
    "Do not describe the local result as exact published WRR reproduction.",
    "This dashboard is a review map, not a reproduction result.",
)

FORBIDDEN_PHRASES = (
    "exact published WRR reproduced",
    "source correction selected",
    "pair exclusion selected",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_gap_dashboard_doc(args.doc, args.dashboard, args.manifest)
    if failures:
        for failure in failures:
            print(f"WRR exact gap dashboard failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR exact gap dashboard ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--dashboard", type=Path, default=DEFAULT_DASHBOARD)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_gap_dashboard_doc(
    doc: Path,
    dashboard: Path | None = DEFAULT_DASHBOARD,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text and f"- {phrase}" not in text:
            failures.append(f"{doc} forbidden phrase outside boundary list: {phrase}")
    if dashboard is not None:
        failures.extend(validate_dashboard_csv(dashboard))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_dashboard_csv(dashboard: Path) -> list[str]:
    data = _read_csv(dashboard)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{dashboard} fieldnames drifted")
    if len(rows) != len(EXPECTED_ROWS):
        failures.append(f"{dashboard} has {len(rows)} rows; expected {len(EXPECTED_ROWS)}")
    by_item = {row.get("item", ""): row for row in rows}
    if set(by_item) != set(EXPECTED_ROWS):
        failures.append(f"{dashboard} item set drifted")
    for item, (section, value, status) in EXPECTED_ROWS.items():
        row = by_item.get(item)
        if row is None:
            continue
        if row.get("section") != section:
            failures.append(f"{dashboard} {item} section drifted")
        if row.get("value") != value:
            failures.append(f"{dashboard} {item} value drifted")
        if row.get("status") != status:
            failures.append(f"{dashboard} {item} status drifted")
        if not row.get("evidence") or not row.get("source"):
            failures.append(f"{dashboard} {item} missing evidence/source")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_exact_reproduction_gap_dashboard",
        "dashboard_rows": len(EXPECTED_ROWS),
        "gap_reason_rows": EXPECTED_GAP_REASON_ROWS,
        "review_lane_rows": EXPECTED_REVIEW_LANE_ROWS,
        "inputs": {
            "locked_report": str(builder.DEFAULT_LOCKED_REPORT),
            "defined_pair_summary": str(builder.DEFAULT_DEFINED_PAIR_SUMMARY),
            "gap_reasons": str(builder.DEFAULT_GAP_REASONS),
            "variant_upper_bound": str(builder.DEFAULT_VARIANT_UPPER_BOUND),
            "action_summary": str(builder.DEFAULT_ACTION_SUMMARY),
            "manual_register_summary": str(builder.DEFAULT_MANUAL_REGISTER_SUMMARY),
            "manual_decision_records": str(builder.DEFAULT_MANUAL_DECISION_RECORDS),
            "source_policy_checklist": str(builder.DEFAULT_SOURCE_POLICY_CHECKLIST),
            "row_checklist": str(builder.DEFAULT_ROW_CHECKLIST),
            "remaining_checklist": str(builder.DEFAULT_REMAINING_CHECKLIST),
        },
        "outputs": {
            "out": str(DEFAULT_DASHBOARD),
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


if __name__ == "__main__":
    raise SystemExit(main())
