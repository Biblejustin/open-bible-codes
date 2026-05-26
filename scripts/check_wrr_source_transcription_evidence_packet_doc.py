#!/usr/bin/env python3
"""Validate WRR source-transcription evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_source_transcription_evidence_packet.csv")
DEFAULT_ROW_SUMMARY = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)

EXPECTED_TOTALS = {
    "action_terms": "43",
    "residual_pairs": "44",
    "frontier_pairs": "35",
    "row_clusters": "22",
}

EVIDENCE_REQUIRED = "primary Table 2 row transcription or row-alignment evidence"
NO_INPUT_BOUNDARY = (
    "No automatic source correction; primary row transcription or row-alignment "
    "evidence must be locked before changing imported terms."
)

REQUIRED_PHRASES = (
    "# WRR Source-Transcription Evidence Packet",
    "Status: diagnostic evidence packet for source-transcription residual terms.",
    "It does not choose source corrections, row edits, or pair exclusions.",
    "- Source-transcription action terms: 43.",
    "- Residual pair links: 44.",
    "- Minimum-frontier pair links: 35.",
    "- Row clusters: 22.",
    "| 1 | `06` | `WRR2 06` | 4 | 4 | 4 |",
    "`wrr2_27_app_13`",
    "`B@LQWLHRMZ`",
    "primary Table 2 row transcription or row-alignment evidence",
    "No automatic source correction",
    "Rows with multiple unresolved terms should be reviewed once by row",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_transcription_evidence_packet_doc(
        args.doc,
        args.packet,
        args.row_summary,
    )
    if failures:
        for failure in failures:
            print(
                f"WRR source-transcription evidence packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR source-transcription evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--row-summary", type=Path, default=DEFAULT_ROW_SUMMARY)
    return parser


def validate_source_transcription_evidence_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
    row_summary: Path | None = DEFAULT_ROW_SUMMARY,
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
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if row_summary is not None:
        failures.extend(validate_row_summary_csv(row_summary))
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    rows = _read_csv(packet)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    expected_rows = int(EXPECTED_TOTALS["action_terms"])
    if len(rows) != expected_rows:
        failures.append(f"{packet} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("evidence_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{packet} evidence_rank sequence drifted")

    residual_pairs = sum(_int(row, "residual_pairs") for row in rows)
    frontier_pairs = sum(_int(row, "frontier_pairs") for row in rows)
    if residual_pairs != int(EXPECTED_TOTALS["residual_pairs"]):
        failures.append(f"{packet} residual_pairs sum={residual_pairs}")
    if frontier_pairs != int(EXPECTED_TOTALS["frontier_pairs"]):
        failures.append(f"{packet} frontier_pairs sum={frontier_pairs}")

    for row in rows:
        rank = row.get("evidence_rank", "")
        if row.get("row_ocr_status") != "not_matched":
            failures.append(f"{packet} rank {rank} row OCR status drifted")
        if row.get("best_variant_hit_count") != "0":
            failures.append(f"{packet} rank {rank} variant lead count drifted")
        if row.get("evidence_required") != EVIDENCE_REQUIRED:
            failures.append(f"{packet} rank {rank} evidence requirement drifted")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{packet} rank {rank} no-input boundary drifted")
        if not row.get("term_id") or not row.get("row_number"):
            failures.append(f"{packet} rank {rank} missing term or row number")
    return failures


def validate_row_summary_csv(row_summary: Path) -> list[str]:
    rows = _read_csv(row_summary)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    expected_rows = int(EXPECTED_TOTALS["row_clusters"])
    if len(rows) != expected_rows:
        failures.append(f"{row_summary} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("row_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{row_summary} row_rank sequence drifted")

    checks = {
        "action_terms": sum(_int(row, "action_terms") for row in rows),
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
    }
    for metric, actual in checks.items():
        expected = int(EXPECTED_TOTALS[metric])
        if actual != expected:
            failures.append(f"{row_summary} {metric}={actual}; expected {expected}")
    for row in rows:
        rank = row.get("row_rank", "")
        if row.get("evidence_required") != EVIDENCE_REQUIRED:
            failures.append(f"{row_summary} rank {rank} evidence requirement drifted")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{row_summary} rank {rank} no-input boundary drifted")
        term_count = len([term for term in row.get("action_term_ids", "").split(";") if term])
        if term_count != _int(row, "action_terms"):
            failures.append(f"{row_summary} rank {rank} action term count mismatch")
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
