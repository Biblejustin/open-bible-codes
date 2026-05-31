#!/usr/bin/env python3
"""Validate Project Gutenberg KJVA book coverage probe boundaries."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_gutenberg_book_coverage_probe as probe


DEFAULT_DOC = probe.DEFAULT_MD
DEFAULT_ROWS = probe.DEFAULT_ROWS
DEFAULT_SUMMARY = probe.DEFAULT_SUMMARY
DEFAULT_ANCHORS = probe.DEFAULT_ANCHORS
DEFAULT_MANIFEST = probe.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Gutenberg Book Coverage Probe",
    "Status: source-coverage probe only.",
    "not an ELS result",
    "not a corpus import",
    "not a verse import",
    "not a source lock",
    "does not commit Bible text, normalize Bible text, or create a local corpus",
    "Expected KJV books checked: 66.",
    "KJV book headings found: 66.",
    "Missing KJV book headings: 0.",
    "Expected apocrypha/deuterocanon books checked: 14.",
    "Apocrypha/deuterocanon book headings found: 0.",
    "Missing apocrypha/deuterocanon book headings: 14.",
    "Book-order lock ready: 0.",
    "Verse-numbered import ready: 0.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Project Gutenberg eBook 30 heading markers show all 66 KJV book headings and no Apocrypha/deuterocanon book headings.",
    "public-domain KJV-only control candidate",
    "does not change any KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:book-order lock ready|verse import ready|source-lock ready|"
    r"result-bearing replication is ready|claim report|claim-level|proved|"
    r"proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Book-order lock ready: 0.",
    "Verse-numbered import ready: 0.",
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_gutenberg_book_coverage_probe_doc(
        args.doc,
        rows=args.rows,
        summary=args.summary,
        anchors=args.anchors,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Gutenberg book coverage probe failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Gutenberg book coverage probe ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHORS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_gutenberg_book_coverage_probe_doc(
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
    if fieldnames != probe.ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 80:
        failures.append(f"{path} expected 80 rows, found {len(rows)}")
    kjv_rows = [row for row in rows if row.get("section") == "kjv"]
    apocrypha_rows = [row for row in rows if row.get("section") == "apocrypha"]
    if len(kjv_rows) != 66:
        failures.append(f"{path} expected 66 KJV rows, found {len(kjv_rows)}")
    if len(apocrypha_rows) != 14:
        failures.append(f"{path} expected 14 apocrypha rows, found {len(apocrypha_rows)}")
    if any(row.get("status") != "found" for row in kjv_rows):
        failures.append(f"{path} expected current KJV rows to be found")
    if any(row.get("status") != "missing" for row in apocrypha_rows):
        failures.append(f"{path} expected current apocrypha rows to remain missing")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != probe.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "fetched_plain_text_pages": "1",
        "expected_kjv_books": "66",
        "found_kjv_book_headings": "66",
        "missing_kjv_book_headings": "0",
        "expected_apocrypha_books": "14",
        "found_apocrypha_book_headings": "0",
        "missing_apocrypha_book_headings": "14",
        "book_order_lock_ready": "False",
        "verse_import_ready": "False",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "coverage_probe_only_not_result_bearing",
    }
    row = rows[0]
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
    if fieldnames != probe.ANCHOR_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 5:
        failures.append(f"{path} expected 5 anchors, found {len(rows)}")
    missing = [row["anchor"] for row in rows if row.get("status") != "found"]
    if missing:
        failures.append(f"{path} missing anchors: {', '.join(missing)}")
    return failures


def validate_manifest(path: Path, *, doc: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path} is invalid JSON: {exc}"]
    failures: list[str] = []
    if payload.get("claim_boundary") != "source-coverage probe only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "plain text scanned in memory; Bible text not committed":
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


def validate_no_overclaim(path: Path, text: str) -> list[str]:
    failures: list[str] = []
    for match in FORBIDDEN_OVERCLAIM_RE.finditer(text):
        line = text.count("\n", 0, match.start()) + 1
        line_text = text.splitlines()[line - 1].strip()
        if any(context in line_text for context in ALLOWED_FORBIDDEN_CONTEXTS):
            continue
        failures.append(f"{path}:{line} overclaim phrase: {match.group(0)!r}")
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
