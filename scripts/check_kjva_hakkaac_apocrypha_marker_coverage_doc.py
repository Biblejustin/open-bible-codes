#!/usr/bin/env python3
"""Validate Hakkaac KJVA Apocrypha marker-coverage audit."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_marker_coverage as audit


DEFAULT_DOC = audit.DEFAULT_MD
DEFAULT_ROWS = audit.DEFAULT_ROWS
DEFAULT_CHAPTER_ROWS = audit.DEFAULT_CHAPTER_ROWS
DEFAULT_SUMMARY = audit.DEFAULT_SUMMARY
DEFAULT_MANIFEST = audit.DEFAULT_MANIFEST

REQUIRED_PHRASES = (
    "# KJVA Hakkaac Apocrypha Marker Coverage",
    "Status: marker-coverage audit only.",
    "not an ELS result",
    "not a corpus import",
    "not a source lock",
    "not a result-bearing replication",
    "does not commit Bible text, normalize Bible text, create a local corpus",
    "Pages scanned: 14.",
    "Exact book marker matches: 14/14.",
    "Count-drift books: 0.",
    "Source markers: 5720.",
    "Local markers: 5720.",
    "Chapter rows: 173.",
    "Chapter drift rows: 0.",
    "Pages with public-domain note: 14.",
    "Source-lock ready: 0.",
    "Result-ready sources: 0.",
    "Claim status: `marker_coverage_audit_only_not_result_bearing`.",
    "`SIR`",
    "`MAN`",
    "`exact_marker_match`",
    "No Bible text is written to tracked outputs.",
    "does not change KJVA bridge result status",
)
FORBIDDEN_OVERCLAIM_RE = re.compile(
    r"\b(?:source-lock ready|result-bearing replication is ready|claim report|"
    r"claim-level|proved|proves|proof|conclusive evidence|significant finding)\b",
    re.IGNORECASE,
)
ALLOWED_FORBIDDEN_CONTEXTS = (
    "Source-lock ready: 0.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_kjva_hakkaac_apocrypha_marker_coverage_doc(
        args.doc,
        rows=args.rows,
        chapter_rows=args.chapter_rows,
        summary=args.summary,
        manifest=args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"KJVA Hakkaac marker coverage failure: {failure}", file=sys.stderr)
        return 1
    print(f"KJVA Hakkaac marker coverage ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--chapter-rows", type=Path, default=DEFAULT_CHAPTER_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_kjva_hakkaac_apocrypha_marker_coverage_doc(
    doc: Path = DEFAULT_DOC,
    *,
    rows: Path | None = DEFAULT_ROWS,
    chapter_rows: Path | None = DEFAULT_CHAPTER_ROWS,
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
    failures.extend(validate_no_overclaim(doc, text))
    if rows is not None:
        failures.extend(validate_rows_csv(rows))
    if chapter_rows is not None:
        failures.extend(validate_chapter_rows_csv(chapter_rows))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest, doc=doc))
    return failures


def validate_rows_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.BOOK_ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 14:
        failures.append(f"{path} expected 14 book rows, found {len(rows)}")
        return failures
    if sum(int(row["source_total_markers"]) for row in rows) != 5720:
        failures.append(f"{path} source marker total drifted")
    if sum(int(row["local_total_markers"]) for row in rows) != 5720:
        failures.append(f"{path} local marker total drifted")
    if any(row["status"] != "exact_marker_match" for row in rows):
        failures.append(f"{path} expected all book rows exact_marker_match")
    if any(row["license_note_present"] != "True" for row in rows):
        failures.append(f"{path} expected all book pages to retain public-domain note")
    by_book = {row["book"]: row for row in rows}
    for book, total in {"SIR": "1393", "MAN": "15", "TOB": "244", "2ES": "874"}.items():
        row = by_book.get(book)
        if row is None:
            failures.append(f"{path} missing book row {book}")
        elif row["source_total_markers"] != total or row["local_total_markers"] != total:
            failures.append(f"{path} {book} marker total drifted")
    return failures


def validate_chapter_rows_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.CHAPTER_ROW_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 173:
        failures.append(f"{path} expected 173 chapter rows, found {len(rows)}")
        return failures
    drift_rows = [row for row in rows if row["status"] != "exact_marker_match"]
    if drift_rows:
        failures.append(f"{path} expected 0 drift rows, found {len(drift_rows)}")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    data = read_csv(path)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != audit.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{path} expected 1 summary row, found {len(rows)}")
        return failures
    expected = {
        "pages_scanned": "14",
        "local_books_compared": "14",
        "exact_book_marker_matches": "14",
        "count_drift_books": "0",
        "source_total_markers": "5720",
        "local_total_markers": "5720",
        "chapter_rows": "173",
        "chapter_drift_rows": "0",
        "license_note_pages": "14",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "marker_coverage_audit_only_not_result_bearing",
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
    if payload.get("claim_boundary") != "marker-coverage audit only; no ELS result":
        failures.append(f"{path} claim_boundary drifted")
    if payload.get("text_retention") != "no Bible text written to tracked outputs":
        failures.append(f"{path} text_retention drifted")
    if payload.get("row_count") != 14:
        failures.append(f"{path} row_count drifted")
    if payload.get("chapter_row_count") != 173:
        failures.append(f"{path} chapter_row_count drifted")
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
