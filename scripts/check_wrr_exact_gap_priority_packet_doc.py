#!/usr/bin/env python3
"""Validate the WRR exact-gap priority packet keeps boundaries visible."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_exact_gap_priority_packet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_PACKET = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

EXPECTED_SUMMARY = {
    "source_cited_defined_distances": "163",
    "current_defined_distances": "72",
    "remaining_163_distance_gap": "91",
    "review_lanes": "4",
    "source_row_clusters": "22",
}

EXPECTED_REVIEW_LANES = {
    "source_policy_or_pair_rule_review": {
        "priority": "1",
        "value": "1 terms; 1 residual pairs; 1 frontier pairs",
        "status": "evidence_needed_no_source_change_selected",
    },
    "source_transcription_or_row_alignment": {
        "priority": "2",
        "value": "43 terms; 44 residual pairs; 35 frontier pairs",
        "status": "evidence_needed_no_source_change_selected",
    },
    "page_image_near_match_review": {
        "priority": "3",
        "value": "3 terms; 3 residual pairs; 2 frontier pairs",
        "status": "evidence_needed_no_source_change_selected",
    },
    "method_or_pair_universe_review": {
        "priority": "4",
        "value": "11 terms; 11 residual pairs; 2 frontier pairs",
        "status": "evidence_needed_no_source_change_selected",
    },
}

EXPECTED_GAP_ROW = {
    "section": "gap",
    "item": "remaining_163_distance_gap",
    "value": "72 current defined distances vs 163 source-cited; gap 91",
    "status": "exact_published_reproduction_open",
}

REQUIRED_PHRASES = (
    "# WRR Exact Gap Priority Packet",
    "Status: no-input priority packet for the exact-published WRR reproduction gap.",
    "It does not select source corrections, pair exclusions, replacement spellings, or method changes.",
    "Source-cited defined distances | 163",
    "Current defined distances | 72",
    "Remaining 163-distance gap | 91",
    "| 2 | `source_transcription_or_row_alignment` | 43 terms; 44 residual pairs; 35 frontier pairs |",
    "Full CSV includes 22 row clusters.",
    "| remaining_lane | `method_or_pair_universe_review` | 11 terms; 11 residual pairs; 2 frontier pairs |",
    "| method_pair_universe | `ocr_matched_zero_ordinary_hits` | 11 OCR-matched terms;",
    "wide-skip probe: 0 total hits through skip 5000",
    "11/11 terms remain zero through skip 5000",
    "This is an evidence-priority packet, not an exact published WRR reproduction result.",
    "Do not describe the local locked-method result as exact published reproduction.",
)

FORBIDDEN_PHRASES = (
    "source correction selected",
    "pair exclusion selected",
    "replacement spelling selected",
    "exact published WRR reproduced",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_priority_packet_doc(
        args.doc,
        args.packet,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR exact-gap priority packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR exact-gap priority packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_priority_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
    summary: Path | None = DEFAULT_SUMMARY,
    manifest: Path | None = DEFAULT_MANIFEST,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    for phrase in FORBIDDEN_PHRASES:
        if phrase in text and f"- {phrase}" not in text:
            failures.append(f"{doc} forbidden phrase outside caution list: {phrase}")
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
    if fieldnames != builder.SUMMARY_FIELDNAMES:
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
    if fieldnames != builder.FIELDNAMES:
        failures.append(f"{packet} fieldnames drifted")
    gap_rows = [row for row in rows if row.get("section") == "gap"]
    if not any(_row_matches(row, EXPECTED_GAP_ROW) for row in gap_rows):
        failures.append(f"{packet} missing exact reproduction gap boundary row")

    review_lanes = [row for row in rows if row.get("section") == "review_lane"]
    if len(review_lanes) != int(EXPECTED_SUMMARY["review_lanes"]):
        failures.append(f"{packet} has {len(review_lanes)} review lanes")
    lanes_by_item = {row.get("item", ""): row for row in review_lanes}
    for item, expected in EXPECTED_REVIEW_LANES.items():
        row = lanes_by_item.get(item)
        if row is None:
            failures.append(f"{packet} missing review lane {item}")
            continue
        if not _row_matches(row, expected):
            failures.append(f"{packet} review lane {item} no longer matches lock")
        boundary = row.get("no_input_boundary", "")
        if not boundary or not any(
            phrase in boundary for phrase in ("automatic", "do not", "source row")
        ):
            failures.append(f"{packet} review lane {item} missing no-input boundary")

    cluster_count = sum(1 for row in rows if row.get("section") == "source_row_cluster")
    if cluster_count != int(EXPECTED_SUMMARY["source_row_clusters"]):
        failures.append(f"{packet} has {cluster_count} source-row clusters")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_exact_gap_priority_packet",
        "inputs": {
            "dashboard": str(builder.DEFAULT_DASHBOARD),
            "action_summary": str(builder.DEFAULT_ACTION_SUMMARY),
            "row_summary": str(builder.DEFAULT_ROW_SUMMARY),
            "remaining_summary": str(builder.DEFAULT_REMAINING_SUMMARY),
            "method_summary": str(builder.DEFAULT_METHOD_SUMMARY),
            "method_wide_skip_summary": str(builder.DEFAULT_METHOD_WIDE_SKIP_SUMMARY),
            "gap_reasons": str(builder.DEFAULT_GAP_REASONS),
        },
        "outputs": {
            "csv": str(DEFAULT_PACKET),
            "summary_csv": str(DEFAULT_SUMMARY),
            "markdown": str(DEFAULT_DOC),
        },
        "rows": 33,
        "summary_rows": len(EXPECTED_SUMMARY),
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
        return list(reader.fieldnames or []), list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


def _row_matches(row: dict[str, str], expected: dict[str, str]) -> bool:
    return all(row.get(key) == value for key, value in expected.items())


if __name__ == "__main__":
    raise SystemExit(main())
