#!/usr/bin/env python3
"""Validate Cities source-review queue doc stays source-triage only."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/CITIES_SOURCE_REVIEW_QUEUE.md")
DEFAULT_QUEUE = Path("reports/cities_pdf_recovery_probe/cities_source_review_queue.csv")
DEFAULT_SUMMARY = Path("reports/cities_pdf_recovery_probe/cities_source_review_queue_summary.csv")

REQUIRED_PHRASES = (
    "# Cities Source Review Queue",
    "Status: source-review triage only.",
    "does not run OCR",
    "normalize city names",
    "ELS searches",
    "compute compactness",
    "verify p-levels",
    "Rows queued: 35.",
    "does not decide source admissibility",
    "does not create city-name rows",
    "does not make any result-bearing claim",
    "CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md",
    "records visual page-role decisions for all 41 OCR-packet pages",
    "source-row imports at zero",
    "CITIES_SOURCE_ROW_LOCK_QUEUE.md",
    "14 table/list/exception-note",
    "separate citable source-row locks",
)

EXPECTED_LANES = (
    "review_extractable_text",
    "ocr_image_only_pdf",
    "encoding_or_ocr_candidate",
    "recover_missing_pdf",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_review_queue_doc(
        args.doc,
        args.queue,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-review queue doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-review queue doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_cities_source_review_queue_doc(
    doc: Path,
    queue_csv: Path = DEFAULT_QUEUE,
    summary_csv: Path = DEFAULT_SUMMARY,
) -> list[str]:
    missing = [str(path) for path in (doc, queue_csv, summary_csv) if not path.exists()]
    if missing:
        return ["missing required files: " + ", ".join(missing)]
    text = doc.read_text(encoding="utf-8")
    normalized = normalize_space(text)
    queue_rows = read_csv(queue_csv)
    summary_rows = read_csv(summary_csv)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized
    ]
    failures.extend(validate_lanes(doc, normalized, queue_rows, summary_rows))
    return failures


def validate_lanes(
    doc: Path,
    normalized_doc: str,
    queue_rows: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    queue_lanes = {row.get("lane", "") for row in queue_rows}
    summary_by_lane = {row.get("lane", ""): row for row in summary_rows}
    for lane in EXPECTED_LANES:
        if lane not in queue_lanes:
            failures.append(f"queue CSV missing lane: {lane}")
        if lane not in summary_by_lane:
            failures.append(f"summary CSV missing lane: {lane}")
            continue
        expected = normalize_space(f"| `{lane}` | {summary_by_lane[lane]['rows']} |")
        if expected not in normalized_doc:
            failures.append(
                f"{doc} missing lane summary count: {lane}={summary_by_lane[lane]['rows']}"
            )
    queued_phrase = normalize_space(f"- Rows queued: {len(queue_rows)}.")
    if queued_phrase not in normalized_doc:
        failures.append(f"{doc} missing queue total: {len(queue_rows)}")
    return failures


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
