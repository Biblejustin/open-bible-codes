#!/usr/bin/env python3
"""Validate WRR source row OCR word packet stays scoped to review aids."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_source_row_ocr_word_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_source_row_ocr_word_summary.csv")

EXPECTED_SUMMARY = {
    "source_rows": "22",
    "rows_with_tokens": "22",
    "frontier_rows": "19",
    "total_ocr_words": "337",
    "total_hebrew_letters": "972",
    "low_conf_threshold": "50",
    "low_conf_words": "78",
    "ocr_boundary": (
        "OCR words are review aids only; no row transcription, source "
        "correction, pair exclusion, or method change is selected by this packet."
    ),
}

NO_INPUT_BOUNDARY = EXPECTED_SUMMARY["ocr_boundary"]

REQUIRED_PHRASES = (
    "# WRR Source Row OCR Word Packet",
    "Status: no-input OCR word packet for WRR source-row review.",
    "it is not transcription verification and does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "OCR words are review aids only; no row transcription, source correction, pair exclusion, or method change is selected by this packet.",
    "OCR word availability is not transcription verification.",
    "Low confidence counts are review triage only.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_ocr_word_packet_doc(
        args.doc,
        args.packet,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row OCR word packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row OCR word packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_source_row_ocr_word_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
    summary: Path | None = DEFAULT_SUMMARY,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    rows = _read_csv(summary)
    if isinstance(rows, str):
        return [rows]
    by_metric = {row.get("metric", ""): row for row in rows}
    failures: list[str] = []
    for metric, expected in EXPECTED_SUMMARY.items():
        actual = by_metric.get(metric, {}).get("value")
        if actual != expected:
            failures.append(f"{summary} metric {metric}={actual!r}; expected {expected!r}")
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    rows = _read_csv(packet)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    expected_rows = int(EXPECTED_SUMMARY["source_rows"])
    if len(rows) != expected_rows:
        failures.append(f"{packet} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("row_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{packet} row_rank sequence drifted")

    rows_with_tokens = sum(1 for row in rows if _int(row, "word_count") > 0)
    frontier_rows = sum(1 for row in rows if _int(row, "frontier_pairs") > 0)
    total_words = sum(_int(row, "word_count") for row in rows)
    total_letters = sum(_int(row, "hebrew_letter_count") for row in rows)
    low_conf_words = sum(_int(row, "low_conf_word_count") for row in rows)
    checks = {
        "rows_with_tokens": rows_with_tokens,
        "frontier_rows": frontier_rows,
        "total_ocr_words": total_words,
        "total_hebrew_letters": total_letters,
        "low_conf_words": low_conf_words,
    }
    for metric, actual in checks.items():
        expected = int(EXPECTED_SUMMARY[metric])
        if actual != expected:
            failures.append(f"{packet} {metric}={actual}; expected {expected}")

    for row in rows:
        row_rank = row.get("row_rank", "")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{packet} rank {row_rank} no-input boundary drifted")
        if not row.get("crop_path", "").startswith(
            "reports/wrr_1994/source_review_crops_auto/"
        ):
            failures.append(f"{packet} rank {row_rank} crop path drifted")
        if _int(row, "word_count") <= 0:
            failures.append(f"{packet} rank {row_rank} has no OCR words")
        if _int(row, "hebrew_letter_count") <= 0:
            failures.append(f"{packet} rank {row_rank} has no Hebrew OCR letters")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "0")
    try:
        return int(value)
    except ValueError:
        return 0


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
