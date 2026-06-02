#!/usr/bin/env python3
"""Validate WRR no-input handoff status boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import build_wrr_no_input_handoff_status as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_STATUS = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

REQUIRED_STATUS_IDS = {
    "local_claim_readiness",
    "exact_published_reproduction_gap",
    "residual_review_lanes",
    "source_policy_pair_rule",
    "source_transcription_rows",
    "page_image_near_match",
    "method_pair_universe",
    "method_wide_skip_probe",
    "manual_decision_records",
}
REQUIRED_PHRASES = (
    "# WRR No-Input Handoff Status",
    "Status: consolidated no-input handoff.",
    "not a new WRR result",
    "not an exact published WRR reproduction",
    "not a source correction",
    "not a pair exclusion",
    "not a replacement spelling lock",
    "not a method change",
    "Status rows: 9.",
    "Handoff-ready rows: 9.",
    "Manual-input-needed rows: 8.",
    "Local claim-readiness rows: 4/4 ready.",
    "Claim-blocker rows: 0.",
    "Source-cited defined distances: 163.",
    "Current defined distances: 72.",
    "Remaining gap: 91.",
    "Review lanes: 4.",
    "Residual action terms: 58.",
    "Residual pairs: 59.",
    "Frontier pairs: 40.",
    "Manual decision rows: 37.",
    "Source-transcription row clusters: 22.",
    "Page-image near-match terms: 3.",
    "Method/pair-universe terms: 11.",
    "Wide-skip total hits through skip 5000: 0.",
    "New WRR result allowed: 0.",
    "Exact published reproduction ready: 0.",
    "`local_locked_method_ready_exact_published_open`",
    "`local_claim_readiness`",
    "`exact_published_reproduction_gap`",
    "`residual_review_lanes`",
    "`source_policy_pair_rule`",
    "`source_transcription_rows`",
    "`page_image_near_match`",
    "`method_pair_universe`",
    "`method_wide_skip_probe`",
    "`manual_decision_records`",
    "The next result-bearing WRR claim remains blocked",
    "Local locked-method evidence remains separate from exact published WRR reproduction.",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"(?:exact published WRR reproduced|new WRR result allowed:\s*1|"
    r"exact published reproduction ready:\s*1|source correction selected|"
    r"pair exclusion selected|replacement spelling lock selected|method change selected)",
    re.IGNORECASE,
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_no_input_handoff_status_doc(
        args.doc,
        status=args.status,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR no-input handoff status failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR no-input handoff status ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_no_input_handoff_status_doc(
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
        "claim_readiness_rows": "4",
        "claim_readiness_ready_rows": "4",
        "claim_blocker_rows": "0",
        "source_cited_defined_distances": "163",
        "current_defined_distances": "72",
        "remaining_gap": "91",
        "review_lanes": "4",
        "residual_action_terms": "58",
        "residual_pairs": "59",
        "frontier_pairs": "40",
        "manual_decision_rows": "37",
        "manual_action_terms": "58",
        "manual_residual_pairs": "59",
        "manual_frontier_pairs": "40",
        "source_transcription_row_clusters": "22",
        "source_transcription_action_terms": "43",
        "page_image_terms": "3",
        "method_pair_universe_terms": "11",
        "wide_skip_max": "5000",
        "wide_skip_total_hits": "0",
        "new_result_allowed": "False",
        "exact_reproduction_ready": "False",
        "claim_boundary": builder.CLAIM_BOUNDARY,
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
    if not isinstance(payload, dict):
        return [f"{path} JSON root must be an object"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "WRR no-input handoff only; no new result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    if payload.get("summary", {}).get("new_result_allowed") is not False:
        failures.append(f"{path} summary.new_result_allowed drifted")
    if payload.get("summary", {}).get("exact_reproduction_ready") is not False:
        failures.append(f"{path} summary.exact_reproduction_ready drifted")
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
