#!/usr/bin/env python3
"""Validate Project Gutenberg KJVA candidate source audit boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_gutenberg_candidate_source as analyzer


DEFAULT_DOC = analyzer.DEFAULT_MD
DEFAULT_ROWS = analyzer.DEFAULT_ROWS
DEFAULT_SUMMARY = analyzer.DEFAULT_SUMMARY
DEFAULT_ANCHORS = analyzer.DEFAULT_ANCHORS
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Candidate Source Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "does not download, retain, normalize, or commit Bible text",
    "Public-domain-USA pages: 2.",
    "KJV-complete metadata candidates: 1.",
    "Apocrypha/deuterocanon metadata candidates: 1.",
    "Split KJV+Apocrypha metadata candidates: 1.",
    "Apocrypha marker pages in RDF: 1.",
    "Plain-text UTF-8 format pages: 2.",
    "Source-use ready pages: 0.",
    "Source-lock ready pages: 0.",
    "Verse-numbered import ready pages: 0.",
    "Result-ready pages: 0.",
    "eBook 124 as `Deuterocanonical Books of the Bible Apocrypha`",
    "Baruch/Epistle handling",
    "It does not change any KJVA bridge result status.",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:result-bearing replication is ready|source-lock ready|corpus import ready|"
    r"claim report|claim-level|proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready pages: 0.",
    "does not declare source-lock readiness",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_gutenberg_candidate_source_audit_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        anchors=args.anchors,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Gutenberg source audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Gutenberg source audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_candidate_source_audit_doc(
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
    if len(rows) != 2:
        failures.append(f"{path} expected 2 source rows, found {len(rows)}")
        return failures
    by_source = {row.get("source_id", ""): row for row in rows}
    expected_by_source = {
        "gutenberg_ebook_30_kjv_complete": {
            "title": "The Bible, King James Version, Complete",
            "rights": "Public domain in the USA.",
            "plain_text_utf8_url_present": "True",
            "public_domain_usa_marker_present": "True",
            "apocrypha_marker_present": "False",
            "source_audit_status": "public_domain_kjv_complete_metadata_component",
            "source_use_status": "needs_source_use_policy_lock",
            "verse_numbered_import_ready": "False",
            "source_lock_ready_status": "not_source_lock_ready",
            "result_ready_status": "not_result_ready",
        },
        "gutenberg_ebook_124_deuterocanonical": {
            "title": "Deuterocanonical Books of the Bible Apocrypha",
            "rights": "Public domain in the USA.",
            "plain_text_utf8_url_present": "True",
            "public_domain_usa_marker_present": "True",
            "apocrypha_marker_present": "True",
            "source_audit_status": "public_domain_apocrypha_metadata_component",
            "source_use_status": "needs_source_use_policy_lock",
            "verse_numbered_import_ready": "False",
            "source_lock_ready_status": "not_source_lock_ready",
            "result_ready_status": "not_result_ready",
        },
    }
    for source_id, expected in expected_by_source.items():
        row = by_source.get(source_id)
        if row is None:
            failures.append(f"{path} missing source row: {source_id}")
            continue
        for key, value in expected.items():
            if row.get(key) != value:
                failures.append(f"{path} {source_id} {key} drifted: {row.get(key)!r}")
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
        "source_pages": "2",
        "metadata_fetches_ok": "2",
        "public_domain_usa_pages": "2",
        "kjv_complete_metadata_candidates": "1",
        "apocrypha_metadata_candidates": "1",
        "split_kjv_apocrypha_metadata_candidates": "1",
        "apocrypha_marker_pages": "1",
        "plain_text_utf8_pages": "2",
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
        "public_domain_usa_recorded",
        "plain_text_format_recorded",
        "apocrypha_metadata_recorded",
        "split_metadata_components_recorded",
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
