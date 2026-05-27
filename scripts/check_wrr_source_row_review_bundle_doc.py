#!/usr/bin/env python3
"""Validate WRR source row review bundle stays scoped to review aids."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_source_row_review_bundle as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_PACKET = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

PACKET_FIELDNAMES = builder.FIELDNAMES
SUMMARY_FIELDNAMES = builder.SUMMARY_FIELDNAMES

EXPECTED_SUMMARY = {
    "row_review_clusters": "22",
    "frontier_rows": "19",
    "action_terms": "43",
    "residual_pairs": "44",
    "frontier_pairs": "35",
    "rows_with_generated_crops": "22",
    "rows_with_ocr_words": "22",
    "total_ocr_words": "337",
    "low_confidence_ocr_words": "78",
}

NO_INPUT_BOUNDARY = (
    "No row transcription, source correction, pair exclusion, or method change "
    "is selected by this bundle."
)
REVIEW_STATE = "pending_manual_source_lock"
ALLOWED_WITHOUT_INPUT = "organize crop and OCR evidence only"

REQUIRED_PHRASES = (
    "# WRR Source Row Review Bundle",
    "Status: no-input row-review bundle for WRR source-row review.",
    "It combines row-checklist, crop-path, and OCR-word evidence; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "Row review clusters: 22.",
    "Rows with generated crops: 22.",
    "Rows with OCR words: 22.",
    "Low-confidence OCR words: 78.",
    "Crop and OCR availability is not transcription verification.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_review_bundle_doc(
        args.doc,
        args.packet,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row review bundle failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row review bundle ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_source_row_review_bundle_doc(
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
        if phrase not in text and normalize_space(phrase) not in normalized_text
    ]
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    by_metric = {row.get("metric", ""): row for row in rows}
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
        failures.append(f"{summary} fieldnames drifted")
    for metric, expected in EXPECTED_SUMMARY.items():
        actual = by_metric.get(metric, {}).get("value")
        if actual != expected:
            failures.append(f"{summary} metric {metric}={actual!r}; expected {expected!r}")
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    data = _read_csv(packet)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != PACKET_FIELDNAMES:
        failures.append(f"{packet} fieldnames drifted")
    expected_rows = int(EXPECTED_SUMMARY["row_review_clusters"])
    if len(rows) != expected_rows:
        failures.append(f"{packet} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("row_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{packet} row_rank sequence drifted")

    checks = {
        "frontier_rows": sum(1 for row in rows if _int(row, "frontier_pairs") > 0),
        "action_terms": sum(_int(row, "action_terms") for row in rows),
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
        "rows_with_generated_crops": sum(
            1 for row in rows if row.get("crop_exists") == "true"
        ),
        "rows_with_ocr_words": sum(1 for row in rows if _int(row, "word_count") > 0),
        "total_ocr_words": sum(_int(row, "word_count") for row in rows),
        "low_confidence_ocr_words": sum(
            _int(row, "low_conf_word_count") for row in rows
        ),
    }
    for metric, actual in checks.items():
        expected = int(EXPECTED_SUMMARY[metric])
        if actual != expected:
            failures.append(f"{packet} {metric}={actual}; expected {expected}")

    for row in rows:
        row_rank = row.get("row_rank", "")
        if row.get("review_state") != REVIEW_STATE:
            failures.append(f"{packet} rank {row_rank} review state drifted")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{packet} rank {row_rank} no-input boundary drifted")
        if row.get("allowed_without_input") != ALLOWED_WITHOUT_INPUT:
            failures.append(f"{packet} rank {row_rank} allowed action drifted")
        if not row.get("crop_path", "").startswith(
            "reports/wrr_1994/source_review_crops_auto/"
        ):
            failures.append(f"{packet} rank {row_rank} crop path drifted")
        terms_to_verify = [
            term for term in row.get("terms_to_verify", "").split(";") if term
        ]
        if len(terms_to_verify) != _int(row, "action_terms"):
            failures.append(f"{packet} rank {row_rank} term count mismatch")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_source_row_review_bundle",
        "rows": int(EXPECTED_SUMMARY["row_review_clusters"]),
        "summary": {key: int(value) for key, value in EXPECTED_SUMMARY.items()},
        "inputs": {
            "row_checklist": str(builder.DEFAULT_ROW_CHECKLIST),
            "crop_packet": str(builder.DEFAULT_CROP_PACKET),
            "ocr_word_packet": str(builder.DEFAULT_OCR_WORD_PACKET),
        },
        "outputs": {
            "out": str(DEFAULT_PACKET),
            "summary_out": str(DEFAULT_SUMMARY),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
    }
    failures: list[str] = []
    for key, value in expected.items():
        if data.get(key) != value:
            failures.append(f"{manifest} {key} drifted")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


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
