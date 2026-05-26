#!/usr/bin/env python3
"""Validate WRR method/pair-universe evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_method_pair_universe_evidence_packet.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv")

EXPECTED_SUMMARY = {
    "action_terms": "11",
    "residual_pairs": "11",
    "frontier_pairs": "1",
    "ocr_matched_terms": "11",
    "zero_base_skip_250_terms": "11",
    "zero_highcap_appellation_terms": "11",
    "both_sides_zero_highcap_pairs": "2",
    "no_variant_lead_terms": "11",
}

EXPECTED_TERM_IDS = {
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
}

REQUIRED_PHRASES = (
    "# WRR Method/Pair-Universe Evidence Packet",
    "Status: diagnostic packet for OCR-matched WRR residual terms.",
    "It does not choose source corrections, method changes, or pair exclusions.",
    "- Method/pair-universe action terms: 11.",
    "- OCR-matched terms: 11.",
    "- Zero skip-250 appellation counts: 11.",
    "- Zero high-cap appellation ordinary hits: 11.",
    "`wrr2_02_app_03`",
    "`ZR@ABRHM`",
    "`wrr2_31_app_09`",
    "`$LWMMZRXY`",
    "OCR match is not enough to define a WRR corrected distance.",
    "Zero ordinary hits keep these rows in method or pair-universe review.",
    "No row here changes the working source or excludes a pair automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_method_pair_universe_evidence_packet_doc(
        args.doc,
        args.packet,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"WRR method/pair-universe evidence packet failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR method/pair-universe evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_method_pair_universe_evidence_packet_doc(
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
    if len(rows) != 1:
        return [f"{summary} has {len(rows)} rows; expected 1"]
    row = rows[0]
    failures: list[str] = []
    for key, expected in EXPECTED_SUMMARY.items():
        actual = row.get(key)
        if actual != expected:
            failures.append(f"{summary} {key}={actual!r}; expected {expected!r}")
    if row.get("run_label") != "all_lanes_cap1000":
        failures.append(f"{summary} run_label={row.get('run_label')!r}")
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    rows = _read_csv(packet)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != int(EXPECTED_SUMMARY["action_terms"]):
        failures.append(f"{packet} has {len(rows)} rows; expected 11")
    actual_term_ids = {row.get("term_id", "") for row in rows}
    missing = sorted(EXPECTED_TERM_IDS - actual_term_ids)
    unexpected = sorted(actual_term_ids - EXPECTED_TERM_IDS)
    if missing:
        failures.append(f"{packet} missing method terms: {', '.join(missing)}")
    if unexpected:
        failures.append(f"{packet} unexpected method terms: {', '.join(unexpected)}")
    for row in rows:
        term_id = row.get("term_id", "")
        if row.get("row_ocr_status") != "matched":
            failures.append(f"{packet} {term_id} row_ocr_status is not matched")
        if row.get("base_skip_250_hit_count") != "0":
            failures.append(f"{packet} {term_id} base skip-250 count is not zero")
        if row.get("highcap_appellation_ordinary_hits") != "0":
            failures.append(f"{packet} {term_id} high-cap appellation hits not zero")
        if row.get("best_variant_hit_count") != "0":
            failures.append(f"{packet} {term_id} variant lead count is not zero")
        if "No source correction or method change is selected" not in row.get(
            "no_input_boundary", ""
        ):
            failures.append(f"{packet} {term_id} missing no-input boundary")
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
