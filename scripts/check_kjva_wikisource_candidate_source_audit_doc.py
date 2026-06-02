#!/usr/bin/env python3
"""Validate KJVA Wikisource candidate source audit boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_wikisource_candidate_source as analyzer


DEFAULT_DOC = analyzer.DEFAULT_MD
DEFAULT_ROWS = analyzer.DEFAULT_ROWS
DEFAULT_SUMMARY = analyzer.DEFAULT_SUMMARY
DEFAULT_ANCHORS = analyzer.DEFAULT_ANCHORS
DEFAULT_MANIFEST = analyzer.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Wikisource Candidate Source Audit",
    "Status: source-status audit only.",
    "not an ELS result",
    "not a corpus import",
    "does not retain or commit Bible text",
    "Verse-numbered import ready pages: 0.",
    "Result-ready pages: 0.",
    "lawful text import, verse mapping, book-order lock",
    "metadata-level candidate for future source work",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:result-bearing replication is ready|corpus import ready|claim report|"
    r"claim-level|proved|proves|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "and study-lock sidecar before any ELS run.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_wikisource_candidate_source_audit_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        anchors=args.anchors,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Wikisource source audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Wikisource source audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_wikisource_candidate_source_audit_doc(
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
    checks = {
        "source_id": "wikisource_ballantyne_1911_kjva",
        "url": analyzer.WIKISOURCE_URL,
        "verse_numbered_import_ready": "False",
        "result_ready_status": "not_result_ready",
    }
    for key, expected in checks.items():
        if row.get(key) != expected:
            failures.append(f"{path} {key} drifted: {row.get(key)!r}")
    if row.get("source_audit_status") not in {
        "source_candidate_needs_import",
        "source_candidate_not_confirmed",
    }:
        failures.append(f"{path} source_audit_status is not recognized")
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
        "page_fetch_status_recorded",
        "apocrypha_marker_recorded",
        "verse_import_not_ready",
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
    allowed = {normalize_space(context) for context in ALLOWED_FORBIDDEN_CONTEXTS}
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not FORBIDDEN_OVERCLAIM_RE.search(line):
            continue
        normalized_line = normalize_space(line).lstrip("- ")
        if normalized_line in allowed:
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
