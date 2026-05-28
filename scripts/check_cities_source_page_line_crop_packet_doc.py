#!/usr/bin/env python3
"""Validate Cities source-page line crop packet stays review-only."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_cities_source_page_line_crop_packet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_PACKET = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

EXPECTED_SUMMARY = {
    "table_candidate_pages": "4",
    "line_crop_rows": "203",
    "line_crops_available": "203",
    "tsv_sidecars": "4",
    "ocr_words": "1511",
    "ocr_hebrew_letters": "4934",
    "language": "heb",
    "psm": "4",
    "tessdata_dir": "reports/wrr_1994/tessdata",
    "source_row_imports": "0",
    "city_name_normalization": "0",
    "els_runs": "0",
    "compactness_runs": "0",
    "p_levels": "0",
    "no_input_boundary": builder.NO_INPUT_BOUNDARY,
}

EXPECTED_PAGE_COUNTS = {
    "cities_source_transcription_001": 44,
    "cities_source_transcription_002": 55,
    "cities_source_transcription_003": 54,
    "cities_source_transcription_004": 50,
}

REQUIRED_PHRASES = (
    "# Cities Source Page Line Crop Packet",
    "Status: local line-crop review packet for Cities table candidate pages.",
    "Tracked files contain no OCR body text or source-script body text.",
    "Table candidate pages: 4.",
    "Line crop rows: 203.",
    "Line crops available: 203.",
    "TSV sidecars: 4.",
    "OCR words represented by line boxes: 1511.",
    "OCR Hebrew letters represented by line boxes: 4934.",
    "Source-row imports: 0.",
    "City-name normalization: 0.",
    "ELS runs: 0.",
    "Compactness runs: 0.",
    "p-levels: 0.",
    "`cities_source_transcription_001`",
    "`cities_source_transcription_004`",
    "Line crops are local review aids, not verified row transcriptions.",
    "TSV sidecars may contain OCR text locally; tracked files do not.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_cities_source_page_line_crop_packet_doc(
        args.doc,
        args.packet,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"Cities source-page line crop failure: {failure}", file=sys.stderr)
        return 1
    print(f"Cities source-page line crop ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_cities_source_page_line_crop_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    normalized_text = normalize_space(text)
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if normalize_space(phrase) not in normalized_text
    ]
    failures.extend(validate_no_source_text({doc: text}))
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_packet_csv(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    expected_rows = int(EXPECTED_SUMMARY["line_crop_rows"])
    if len(rows) != expected_rows:
        failures.append(f"{path} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("line_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{path} line_rank sequence drifted")
    page_counts: dict[str, int] = {}
    for row in rows:
        page_counts[row.get("transcription_decision_id", "")] = (
            page_counts.get(row.get("transcription_decision_id", ""), 0) + 1
        )
        rank = row.get("line_rank", "")
        for field in (
            "source_row_import",
            "city_name_normalization",
            "els_runs",
            "compactness_runs",
            "p_levels",
        ):
            if row.get(field) != "0":
                failures.append(f"{path} rank {rank} {field} must be 0")
        if row.get("no_input_boundary") != builder.NO_INPUT_BOUNDARY:
            failures.append(f"{path} rank {rank} no-input boundary drifted")
        if row.get("crop_exists") != "true":
            failures.append(f"{path} rank {rank} crop missing")
        if row.get("tsv_exists") != "true":
            failures.append(f"{path} rank {rank} TSV missing")
        if not row.get("crop_path", "").startswith(
            "reports/cities_pdf_recovery_probe/source_page_line_crops/crops/"
        ):
            failures.append(f"{path} rank {rank} crop path drifted")
    if page_counts != EXPECTED_PAGE_COUNTS:
        failures.append(f"{path} page counts drifted: {page_counts}")
    if sum_int(rows, "ocr_word_count") != int(EXPECTED_SUMMARY["ocr_words"]):
        failures.append(f"{path} OCR word total drifted")
    if sum_int(rows, "ocr_hebrew_letters") != int(EXPECTED_SUMMARY["ocr_hebrew_letters"]):
        failures.append(f"{path} OCR Hebrew letter total drifted")
    return failures


def validate_summary_csv(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    fieldnames, rows = read_csv(path)
    if fieldnames != builder.SUMMARY_FIELDNAMES:
        failures.append(f"{path} fieldnames drifted")
    summary = {row["metric"]: row["value"] for row in rows}
    for key, value in EXPECTED_SUMMARY.items():
        if summary.get(key) != value:
            failures.append(f"{path} {key}={summary.get(key)!r}; expected {value!r}")
    return failures


def validate_manifest(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path} is missing"]
    raw_text = path.read_text(encoding="utf-8")
    failures = validate_no_source_text({path: raw_text})
    data = json.loads(raw_text)
    expected: dict[str, Any] = {
        "tool": "build_cities_source_page_line_crop_packet.py",
        "inputs": {
            "packet": str(builder.DEFAULT_OCR_PACKET),
            "tessdata_dir": str(builder.DEFAULT_TESSDATA_DIR),
            "language": "heb",
            "psm": "4",
        },
        "outputs": {
            "base_dir": str(builder.DEFAULT_BASE_DIR),
            "csv": str(DEFAULT_PACKET),
            "summary": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "table_pages": 4,
        "rows": int(EXPECTED_SUMMARY["line_crop_rows"]),
        "summary": EXPECTED_SUMMARY,
        "no_input_boundary": builder.NO_INPUT_BOUNDARY,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{path} {key} drifted")
    return failures


def validate_no_source_text(texts_by_path: dict[Path, str]) -> list[str]:
    failures: list[str] = []
    for path, text in texts_by_path.items():
        if contains_hebrew_or_greek(text):
            failures.append(f"{path} appears to contain source-script body text")
    return failures


def contains_hebrew_or_greek(text: str) -> bool:
    for char in text:
        code = ord(char)
        if 0x0590 <= code <= 0x05FF or 0x0370 <= code <= 0x03FF:
            return True
    return False


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def sum_int(rows: list[dict[str, str]], key: str) -> int:
    total = 0
    for row in rows:
        try:
            total += int(row.get(key, "0"))
        except ValueError:
            continue
    return total


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
