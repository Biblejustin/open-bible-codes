#!/usr/bin/env python3
"""Validate Cities source-row lock evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md")
DEFAULT_ROWS = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_packet.csv"
)
DEFAULT_SUMMARY = Path(
    "reports/cities_pdf_recovery_probe/cities_source_row_lock_evidence_summary.csv"
)

REQUIRED_PHRASES = (
    "# Cities Source Row Lock Evidence Packet",
    "Status: diagnostic evidence packet for Cities source-row lock candidates.",
    "joins decision ids to PDF/source metadata and page-image paths",
    "does not transcribe rows",
    "No OCR body text or source-script body text appears",
    "Evidence rows: 14.",
    "Unique labels: 3.",
    "Table-bearing candidate pages: 4.",
    "Source-list candidate pages: 5.",
    "Exception-note candidate pages: 5.",
    "Recorded decision rows: 0.",
    "Source-row imports: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "`cities_source_row_lock_001`",
    "`cities_source_row_lock_014`",
    "This packet collects evidence locations only.",
    "does not copy their body text",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_row_lock_evidence_packet_doc(
        args.doc,
        args.rows,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"Cities source-row lock evidence packet doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"Cities source-row lock evidence packet doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--rows", type=Path, default=DEFAULT_ROWS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_source_row_lock_evidence_packet_doc(
    doc: Path,
    rows_csv: Path = DEFAULT_ROWS,
    summary_csv: Path = DEFAULT_SUMMARY,
) -> list[str]:
    missing = [str(path) for path in (doc, rows_csv, summary_csv) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    rows_text = rows_csv.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    rows = read_csv(rows_csv)
    summary = {row["metric"]: row["value"] for row in read_csv(summary_csv)}
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_no_source_text(doc, text, rows_csv, rows_text))
    failures.extend(validate_rows(doc, normalized, rows))
    failures.extend(validate_summary(doc, normalized, rows, summary))
    return failures


def validate_no_source_text(
    doc: Path,
    doc_text: str,
    rows_csv: Path,
    rows_text: str,
) -> list[str]:
    failures: list[str] = []
    if contains_hebrew_or_greek(doc_text):
        failures.append(f"{doc} appears to contain source-script body text")
    if contains_hebrew_or_greek(rows_text):
        failures.append(f"{rows_csv} appears to contain source-script body text")
    return failures


def validate_rows(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != 14:
        failures.append(f"rows CSV has {len(rows)} rows, expected 14")
    for index, row in enumerate(rows, start=1):
        expected = f"cities_source_row_lock_{index:03d}"
        if row.get("decision_id") != expected:
            failures.append(
                f"rows CSV rank {index} decision_id={row.get('decision_id')} expected {expected}"
            )
        if row.get("source_row_use") != "no_source_row_use":
            failures.append(f"rows CSV {expected} allows source-row use")
        if row.get("current_decision") != "no_source_row_import":
            failures.append(f"rows CSV {expected} imports source row")
        if row.get("record_decision_status") != "unrecorded":
            failures.append(f"rows CSV {expected} unexpectedly has decision record")
        if expected not in normalized_doc:
            failures.append(f"{doc} missing decision id: {expected}")
    return failures


def validate_summary(
    doc: Path,
    normalized_doc: str,
    rows: list[dict[str, str]],
    summary: dict[str, str],
) -> list[str]:
    failures: list[str] = []
    if summary.get("evidence_rows") != str(len(rows)):
        failures.append(
            f"summary CSV evidence_rows={summary.get('evidence_rows')} does not match rows={len(rows)}"
        )
    for label, metric in (
        ("Evidence rows", "evidence_rows"),
        ("Source-row imports", "source_row_imports"),
        ("ELS runs", "els_runs"),
        ("Compactness runs", "compactness_runs"),
    ):
        value = summary.get(metric, "")
        if not value:
            failures.append(f"summary CSV missing metric: {metric}")
            continue
        needle = normalize_space(f"- {label}: {value}.")
        if needle not in normalized_doc:
            failures.append(f"{doc} missing summary value: {label}={value}")
    return failures


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
