#!/usr/bin/env python3
"""Validate KJVA no-input handoff status boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_kjva_no_input_handoff_status as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_STATUS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

REQUIRED_STATUS_IDS = {
    "current_rerun_baseline",
    "completed_prospective_lane",
    "source_policy_lock",
    "source_text_lock",
    "verse_map_collation_lock",
    "drift_boundary_lock",
    "fresh_terms_leakage_controls",
    "study_lock_manifest",
    "result_permission",
}
REQUIRED_PHRASES = (
    "# KJVA No-Input Handoff Status",
    "Status: consolidated KJVA no-input handoff.",
    "not an ELS result",
    "not a corpus import",
    "not a source-use approval",
    "not a source lock",
    "not a term lock",
    "not a study lock",
    "not a new KJVA result",
    "Status rows: 9.",
    "Handoff-ready rows: 9.",
    "Manual-input-needed rows: 8.",
    "Gate rows: 11.",
    "Rerun-only ready rows: 1.",
    "Blocked gate rows: 10.",
    "Source-policy blocker rows: 7.",
    "Policy options: 5.",
    "Policy-ready options: 2.",
    "Blocked options: 3.",
    "Checksum records ready: 2.",
    "Current rerun locked: 1.",
    "Source-use ready pages: 0.",
    "Source-lock ready: 0.",
    "Result allowed: 0.",
    "Completed lane terms: 7.",
    "Completed lane observed bridge rows: 1.",
    "Completed lane significant terms: 0.",
    "Non-Bible controls at or above observed: 1.",
    "Gutenberg Sirach gap refs: `SIR 44:23`.",
    "Gutenberg Prayer of Manasseh markers: 0/15.",
    "Hakkaac exact normalized verse matches: 5719/5720.",
    "Hakkaac length-drift verses: 1.",
    "Split-source role rows: 7.",
    "Split-source blocker rows: 6.",
    "Fresh terms ready: 0.",
    "Leakage audit ready: 0.",
    "Fixed controls ready: 0.",
    "Study-lock ready: 0.",
    "`kjva_no_input_handoff_blocks_new_result`",
    "`current_rerun_baseline`",
    "`completed_prospective_lane`",
    "`source_policy_lock`",
    "`source_text_lock`",
    "`verse_map_collation_lock`",
    "`drift_boundary_lock`",
    "`fresh_terms_leakage_controls`",
    "`study_lock_manifest`",
    "`result_permission`",
    "The next result-bearing KJVA run remains blocked",
    "Current eBible KJVA remains a rerun baseline only",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"(?:new KJVA result allowed:\s*1|Result allowed:\s*1|"
    r"source-lock ready:\s*1|Study-lock ready:\s*1|"
    r"source-use approved|source lock selected|fresh terms ready:\s*1|"
    r"independent KJVA replication ready|result-bearing KJVA run is ready)",
    re.IGNORECASE,
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_no_input_handoff_status_doc(
        args.doc,
        status=args.status,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA no-input handoff status failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA no-input handoff status ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_no_input_handoff_status_doc(
    doc: Path = DEFAULT_DOC,
    *,
    status: Path | None = DEFAULT_STATUS,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if normalize_space(phrase) not in normalized:
            failures.append(f"{doc} missing phrase: {phrase}")
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        failures.append(f"{doc}:{line} overclaim phrase: {match.group(0)!r}")
    if status is not None:
        failures.extend(validate_status_csv(status))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_status_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.STATUS_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 9:
        failures.append(f"{path} expected 9 status rows, found {len(rows)}")
    ids = {row.get("status_id") for row in rows}
    for status_id in REQUIRED_STATUS_IDS:
        if status_id not in ids:
            failures.append(f"{path} missing status row {status_id}")
    if sum(1 for row in rows if row.get("handoff_ready") == "yes") != 9:
        failures.append(f"{path} expected 9 handoff-ready rows")
    if sum(1 for row in rows if row.get("manual_input_needed") == "yes") != 8:
        failures.append(f"{path} expected 8 manual-input-needed rows")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "status_rows": "9",
        "handoff_ready_rows": "9",
        "manual_input_needed_rows": "8",
        "gate_rows": "11",
        "rerun_only_ready_rows": "1",
        "blocked_gate_rows": "10",
        "source_policy_blocker_rows": "7",
        "policy_option_rows": "5",
        "policy_ready_options": "2",
        "blocked_options": "3",
        "checksum_records_ready": "2",
        "current_rerun_locked": "True",
        "source_use_ready_pages": "0",
        "source_lock_ready": "False",
        "result_allowed": "False",
        "completed_lane_terms": "7",
        "completed_lane_observed_bridge_rows": "1",
        "completed_lane_significant_terms": "0",
        "nonbible_controls_at_or_above_observed": "1",
        "gutenberg_sirach_gap_refs": "SIR 44:23",
        "gutenberg_manasseh_source_markers": "0",
        "gutenberg_manasseh_local_markers": "15",
        "hakkaac_exact_normalized_verse_matches": "5719",
        "hakkaac_total_verses": "5720",
        "hakkaac_length_drift_verses": "1",
        "split_source_role_rows": "7",
        "split_source_blocker_rows": "6",
        "fresh_terms_ready": "False",
        "leakage_audit_ready": "False",
        "fixed_controls_ready": "False",
        "study_lock_ready": "False",
        "claim_status": builder.CLAIM_BOUNDARY,
    }
    row = rows[0]
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "KJVA no-input handoff only; no new result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    if payload.get("summary", {}).get("result_allowed") is not False:
        failures.append(f"{path} summary.result_allowed drifted")
    if payload.get("summary", {}).get("source_lock_ready") is not False:
        failures.append(f"{path} summary.source_lock_ready drifted")
    outputs = payload.get("outputs", {})
    markdown = outputs.get("markdown") if isinstance(outputs, dict) else None
    allowed_markdown = {str(doc)}
    try:
        allowed_markdown.add(str(doc.relative_to(Path.cwd())))
    except ValueError:
        pass
    if markdown not in allowed_markdown:
        failures.append(f"{path} markdown output drifted")
    return failures


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
