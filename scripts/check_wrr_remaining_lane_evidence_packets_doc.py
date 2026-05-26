#!/usr/bin/env python3
"""Validate WRR remaining-lane evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv")

EXPECTED_LANES = {
    "page_image_near_match_review": {
        "action_terms": "3",
        "residual_pairs": "3",
        "frontier_pairs": "2",
        "evidence_required": "page-image inspection against near-match OCR",
    },
    "method_or_pair_universe_review": {
        "action_terms": "11",
        "residual_pairs": "11",
        "frontier_pairs": "2",
        "evidence_required": "method or pair-universe review for OCR-matched missing ordinary hits",
    },
}

EXPECTED_TERM_IDS_BY_LANE = {
    "page_image_near_match_review": {
        "wrr2_19_app_11",
        "wrr2_19_app_12",
        "wrr2_31_app_07",
    },
    "method_or_pair_universe_review": {
        "wrr2_02_app_03",
        "wrr2_02_app_05",
        "wrr2_07_app_05",
        "wrr2_11_app_05",
        "wrr2_12_app_05",
        "wrr2_19_app_03",
        "wrr2_19_app_10",
        "wrr2_20_app_03",
        "wrr2_20_app_05",
        "wrr2_28_app_05",
        "wrr2_31_app_09",
    },
}

NO_INPUT_BOUNDARY = (
    "No automatic source correction or method change; page-image, method, or "
    "pair-universe evidence must be locked first."
)

REQUIRED_PHRASES = (
    "# WRR Remaining-Lane Evidence Packets",
    "Status: diagnostic evidence packet for page-image and method residual lanes.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- Remaining-lane action terms: 14.",
    "- Residual pair links: 14.",
    "- Minimum-frontier pair links: 4.",
    "| `page_image_near_match_review` | 3 | 3 | 2 |",
    "| `method_or_pair_universe_review` | 11 | 11 | 2 |",
    "`wrr2_19_app_11`",
    "`YWSP+RANY`",
    "`wrr2_02_app_03`",
    "`ZR@ABRHM`",
    "primary page row visibly contains Maharit/Trani forms",
    "primary page row visibly contains Rabbi Shalom Sharabi forms",
    "Page-image near-match rows need page-image review before source edits.",
    "OCR-matched method rows need method or pair-universe explanation before source edits.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_remaining_lane_evidence_packets_doc(
        args.doc,
        args.packet,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR remaining-lane evidence packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR remaining-lane evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_remaining_lane_evidence_packets_doc(
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
    failures: list[str] = []
    by_lane = {row.get("action_lane", ""): row for row in rows}
    if set(by_lane) != set(EXPECTED_LANES):
        failures.append(f"{summary} lanes={sorted(by_lane)}")
    for lane, expected in EXPECTED_LANES.items():
        row = by_lane.get(lane)
        if row is None:
            failures.append(f"{summary} missing lane {lane}")
            continue
        for key, expected_value in expected.items():
            actual = row.get(key)
            if actual != expected_value:
                failures.append(
                    f"{summary} {lane} {key}={actual!r}; expected {expected_value!r}"
                )
        if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
            failures.append(f"{summary} {lane} no-input boundary drifted")
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    rows = _read_csv(packet)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    rows_by_lane: dict[str, list[dict[str, str]]] = {
        lane: [] for lane in EXPECTED_TERM_IDS_BY_LANE
    }
    for row in rows:
        rows_by_lane.setdefault(row.get("action_lane", ""), []).append(row)
    if set(rows_by_lane) != set(EXPECTED_TERM_IDS_BY_LANE):
        failures.append(f"{packet} lanes={sorted(rows_by_lane)}")
    for lane, expected_terms in EXPECTED_TERM_IDS_BY_LANE.items():
        lane_rows = rows_by_lane.get(lane, [])
        actual_terms = {row.get("term_id", "") for row in lane_rows}
        missing = sorted(expected_terms - actual_terms)
        unexpected = sorted(actual_terms - expected_terms)
        if missing:
            failures.append(f"{packet} {lane} missing terms: {', '.join(missing)}")
        if unexpected:
            failures.append(f"{packet} {lane} unexpected terms: {', '.join(unexpected)}")
        if len(lane_rows) != int(EXPECTED_LANES[lane]["action_terms"]):
            failures.append(f"{packet} {lane} has {len(lane_rows)} rows")
        for row in lane_rows:
            term_id = row.get("term_id", "")
            if row.get("no_input_boundary") != NO_INPUT_BOUNDARY:
                failures.append(f"{packet} {term_id} no-input boundary drifted")
            if row.get("evidence_required") != EXPECTED_LANES[lane]["evidence_required"]:
                failures.append(f"{packet} {term_id} evidence requirement drifted")
            if row.get("best_variant_hit_count") != "0":
                failures.append(f"{packet} {term_id} variant lead count is not zero")
    return failures


def _read_csv(path: Path) -> list[dict[str, str]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
