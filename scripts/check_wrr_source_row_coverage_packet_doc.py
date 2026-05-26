#!/usr/bin/env python3
"""Validate WRR source row coverage packet stays scoped to triage."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_source_row_coverage_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_source_row_coverage_packet_summary.csv")

EXPECTED_SUMMARY = {
    "source_rows": "22",
    "action_terms": "43",
    "frontier_pairs": "35",
    "direct_visual_action_terms": "0",
    "rows_with_direct_visual_action_term_coverage": "0",
    "rows_with_related_visual_triage_only": "4",
    "rows_with_no_related_visual_triage": "18",
    "visual_triage_rows_outside_source_transcription_checklist": "3",
}

EXPECTED_ROW_STATES = {
    "related_row_visual_triage_only": 4,
    "no_related_visual_triage": 18,
}

NO_INPUT_BOUNDARY = (
    "No row transcription, source correction, pair exclusion, or method change "
    "is selected by this coverage packet."
)

REQUIRED_PHRASES = (
    "# WRR Source Row Coverage Packet",
    "Status: no-input visual-triage coverage packet for WRR source-row review.",
    "It does not choose row transcriptions, source corrections, method changes, or pair exclusions.",
    "Direct action-term visual coverage: 0 terms.",
    "Related row visual triage only: 4 rows.",
    "No related visual triage: 18 rows.",
    "Do not transfer related visual notes to action terms.",
    "Visual notes can identify rows worth reviewing, but they are not locked primary transcriptions.",
    "No row here changes the working WRR source or excludes a pair automatically.",
    "Preserve the working source unless a separate decision record selects a source or method change.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_row_coverage_packet_doc(
        args.doc,
        args.packet,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR source row coverage packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source row coverage packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_source_row_coverage_packet_doc(
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
    direct_terms = _semicolon_count(
        row.get("direct_visual_terms", "") for row in rows
    )
    state_counts = {
        state: sum(1 for row in rows if row.get("coverage_state") == state)
        for state in EXPECTED_ROW_STATES
    }
    if action_terms != int(EXPECTED_SUMMARY["action_terms"]):
        failures.append(f"{packet} action_terms sum={action_terms}")
    if frontier_pairs != int(EXPECTED_SUMMARY["frontier_pairs"]):
        failures.append(f"{packet} frontier_pairs sum={frontier_pairs}")
    if direct_terms != int(EXPECTED_SUMMARY["direct_visual_action_terms"]):
        failures.append(f"{packet} direct visual action terms={direct_terms}")
    for state, expected in EXPECTED_ROW_STATES.items():
        if state_counts[state] != expected:
            failures.append(f"{packet} {state} rows={state_counts[state]}")

    for row in rows:
        row_rank = row.get("row_rank", "")
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{packet} rank {row_rank} no-input boundary drifted")
        action_term_count = _semicolon_count([row.get("action_term_ids", "")])
        if action_term_count != _int(row, "action_terms"):
            failures.append(f"{packet} rank {row_rank} action term ids mismatch")
        if row.get("direct_visual_terms", ""):
            failures.append(f"{packet} rank {row_rank} has direct visual term")
        if row.get("coverage_state") not in EXPECTED_ROW_STATES:
            failures.append(f"{packet} rank {row_rank} unknown coverage state")
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


def _semicolon_count(values: object) -> int:
    total = 0
    for value in values:
        total += len([item for item in str(value).split(";") if item])
    return total


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
