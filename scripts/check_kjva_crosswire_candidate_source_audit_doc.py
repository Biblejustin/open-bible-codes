#!/usr/bin/env python3
"""Validate CrossWire KJVA candidate source audit boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_crosswire_candidate_source as analyzer


DEFAULT_DOC = analyzer.DEFAULT_MD
DEFAULT_ROWS = analyzer.DEFAULT_ROWS
DEFAULT_SUMMARY = analyzer.DEFAULT_SUMMARY
DEFAULT_ANCHORS = analyzer.DEFAULT_ANCHORS
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA CrossWire Candidate Source Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "does not download, retain, normalize, or commit Bible text",
    "Possible independent KJVA metadata candidates: 1.",
    "KJVA OSIS paths: 1.",
    "KJVDC XML paths: 1.",
    "Source-use ready pages: 0.",
    "Source-lock ready pages: 0.",
    "Verse-numbered import ready pages: 0.",
    "Result-ready pages: 0.",
    "It does not change any KJVA bridge result status.",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:result-bearing replication is ready|source-lock ready|corpus import ready|"
    r"claim report|claim-level|proved|proves|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready pages: 0.",
    "not source-lock ready",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_crosswire_candidate_source_audit_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        anchors=args.anchors,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA CrossWire source audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA CrossWire source audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_crosswire_candidate_source_audit_doc(
    doc: Path = DEFAULT_DOC,
    *,
    rows: Path | None = DEFAULT_ROWS,
    summary: Path | None = DEFAULT_SUMMARY,
    anchors: Path | None = DEFAULT_ANCHORS,
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
    failures.extend(validate_no_overclaim(doc, text))
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if anchors is not None:
        failures.extend(validate_anchors_csv(anchors))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_rows_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 source row, found {len(rows)}")
        return failures
    row = rows[0]
    expected = {
        "source_id": "crosswire_gitlab_kjva_osis",
        "kjv_osis_path_present": "True",
        "kjva_osis_path_present": "True",
        "kjvdc_xml_path_present": "True",
        "kjva_distribution_license": "GPL",
        "kjvdc_distribution_license": "General public license for distribution for any purpose",
        "kjva_crown_rights_marker_present": "True",
        "kjvdc_crown_rights_marker_present": "True",
        "source_audit_status": "possible_independent_kjva_candidate_needs_text_audit",
        "source_use_status": "needs_rights_review",
        "verse_numbered_import_ready": "False",
        "source_lock_ready_status": "not_source_lock_ready",
        "result_ready_status": "not_result_ready",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    row = rows[0]
    expected = {
        "source_pages": "1",
        "possible_independent_kjva_candidates": "1",
        "kjva_osis_paths": "1",
        "kjvdc_paths": "1",
        "source_use_ready_pages": "0",
        "source_lock_ready_pages": "0",
        "verse_import_ready_pages": "0",
        "result_ready_pages": "0",
        "claim_status": "source_status_only_not_result_bearing",
    }
    for key, value in expected.items():
        if row.get(key) != value:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    return failures


def validate_anchors_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != analyzer.ANCHOR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    anchors = {row.get("anchor", ""): row.get("status", "") for row in rows}
    for anchor in [
        "metadata_fetch_status_recorded",
        "kjva_osis_path_recorded",
        "kjvdc_xml_path_recorded",
        "source_use_not_ready",
        "source_lock_not_ready",
        "result_not_ready",
    ]:
        if anchors.get(anchor) != "found":
            failures.append(f"{path} anchor {anchor} is not found")
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
    if payload.get("claim_boundary") != "source-status audit only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "metadata only; no Bible text retained":
        failures.append(f"{path} text_retention drifted")
    outputs = payload.get("outputs", {})
    markdown = outputs.get("markdown") if isinstance(outputs, dict) else None
    allowed_markdown_paths = {str(doc)}
    try:
        allowed_markdown_paths.add(str(doc.relative_to(Path.cwd())))
    except ValueError:
        pass
    if markdown not in allowed_markdown_paths:
        failures.append(f"{path} markdown output drifted")
    return failures


def validate_no_overclaim(doc: Path, text: str) -> list[str]:
    failures: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not FORBIDDEN_OVERCLAIM_RE.search(line):
            continue
        if any(context in line for context in ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        failures.append(f"{doc}:{line_number} possible overclaim wording: {line.strip()}")
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
