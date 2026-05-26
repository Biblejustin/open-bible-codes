#!/usr/bin/env python3
"""Validate WRR source row crop packet stays scoped to review aids."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_CROP_PACKET.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_source_row_crop_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_source_row_crop_packet_summary.csv")

EXPECTED_SUMMARY = {
    "source_rows": "22",
    "auto_crops_available": "22",
    "contact_sheet_available": "true",
    "contact_sheet_rows": "22",
    "existing_manual_crop_rows_in_checklist": "4",
    "action_terms": "43",
    "frontier_pairs": "35",
    "detected_row_markers": "31",
    "crop_boundary": (
        "Crops are review aids only; no row transcription, source correction, "
        "pair exclusion, or method change is selected by this packet."
    ),
}

NO_INPUT_BOUNDARY = EXPECTED_SUMMARY["crop_boundary"]
CROP_STATUS = "written_review_aid_only"

REQUIRED_PHRASES = (
    "# WRR Source Row Crop Packet",
    "Status: no-input row-crop packet for WRR source-row review.",
    "It writes local review crops only; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "Auto row crops available: 22.",
    "Existing manual crop rows in checklist: 4.",
    "Crop availability is not transcription verification.",
    "Manual visual notes remain triage notes unless a separate decision record cites source evidence.",
    "No row here changes the working WRR source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_crop_packet_doc(
        args.doc,
        args.packet,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row crop packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row crop packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_source_row_crop_packet_doc(
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

    action_terms = sum(_int(row, "action_terms") for row in rows)
    frontier_pairs = sum(_int(row, "frontier_pairs") for row in rows)
    auto_crops = sum(1 for row in rows if row.get("crop_exists") == "true")
    manual_crop_rows = sum(1 for row in rows if _int(row, "manual_crop_count") > 0)
    if action_terms != int(EXPECTED_SUMMARY["action_terms"]):
        failures.append(f"{packet} action_terms sum={action_terms}")
    if frontier_pairs != int(EXPECTED_SUMMARY["frontier_pairs"]):
        failures.append(f"{packet} frontier_pairs sum={frontier_pairs}")
    if auto_crops != int(EXPECTED_SUMMARY["auto_crops_available"]):
        failures.append(f"{packet} auto crops available={auto_crops}")
    expected_manual_rows = int(
        EXPECTED_SUMMARY["existing_manual_crop_rows_in_checklist"]
    )
    if manual_crop_rows != expected_manual_rows:
        failures.append(f"{packet} manual crop rows={manual_crop_rows}")

    for row in rows:
        row_rank = row.get("row_rank", "")
        if row.get("crop_status") != CROP_STATUS:
            failures.append(f"{packet} rank {row_rank} crop status drifted")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{packet} rank {row_rank} no-input boundary drifted")
        if not row.get("crop_path", "").startswith(
            "reports/wrr_1994/source_review_crops_auto/"
        ):
            failures.append(f"{packet} rank {row_rank} crop path drifted")
        if _int(row, "crop_width") <= 0 or _int(row, "crop_height") <= 0:
            failures.append(f"{packet} rank {row_rank} crop dimensions invalid")
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
