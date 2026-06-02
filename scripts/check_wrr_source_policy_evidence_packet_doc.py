#!/usr/bin/env python3
"""Validate WRR source-policy evidence packet stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_source_policy_evidence_packet as builder


DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_PACKET = builder.DEFAULT_OUT
DEFAULT_CONTEXT = builder.DEFAULT_SOURCE_CONTEXT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

PACKET_FIELDNAMES = builder.EVIDENCE_FIELDNAMES
CONTEXT_FIELDNAMES = builder.SOURCE_CONTEXT_FIELDNAMES
SUMMARY_FIELDNAMES = builder.SUMMARY_FIELDNAMES

DECISION_BOUNDARY = (
    "No automatic correction or exclusion; source-policy targets need citable "
    "pair-rule evidence before changing the working source."
)

EXPECTED_PACKET_ROW = {
    "run_label": "all_lanes_cap1000",
    "evidence_rank": "1",
    "term_id": "wrr2_32_app_05",
    "term": "$LMHMX@LMA",
    "concept": "WRR2 32",
    "source_flags": "wnp_chelm_spelling_context",
    "residual_pairs": "1",
    "frontier_pairs": "1",
    "related_source_term_ids": "wrr2_32_app_04;wrr2_32_app_05",
    "related_source_terms": "wrr2_32_app_04 $LMHMXLMA;wrr2_32_app_05 $LMHMX@LMA",
    "row_ocr_matched_terms": "wrr2_32_app_01 RBY$LMH;wrr2_32_date_01 /KA/TMWZ",
    "row_ocr_not_matched_related_terms": (
        "wrr2_32_app_04 $LMHMXLMA;wrr2_32_app_05 $LMHMX@LMA"
    ),
    "wnp_evidence_refs": (
        "reports/wrr_1994/wnp_en.html:608-619;"
        "reports/wrr_1994/wnp_en.html:931-935;"
        "reports/wrr_1994/wnp_en.html:1052-1054"
    ),
    "table2_bridge_read": (
        "Primary English row label and secondary WRR2 record align by row number; "
        "secondary record has 5 appellations, 1 dates, and 5 same-record pairs. "
        "Hebrew cells are not verified."
    ),
    "decision_boundary": DECISION_BOUNDARY,
}

EXPECTED_SUMMARY_ROW = {
    "run_label": "all_lanes_cap1000",
    "priority_source_policy_terms": "1",
    "related_source_review_rows": "2",
    "related_scenario_pair_rows": "4",
    "wnp_context_blocks": "3",
    "decision_boundary": DECISION_BOUNDARY,
}

EXPECTED_CONTEXT = {
    "wnp_chelm_spelling_argument": "reports/wrr_1994/wnp_en.html:608-619",
    "wnp_chelm_appellation_table": "reports/wrr_1994/wnp_en.html:931-935",
    "wnp_chelm_bibliography_context": "reports/wrr_1994/wnp_en.html:1052-1054",
}

REQUIRED_PHRASES = (
    "# WRR Source-Policy Evidence Packet",
    "Status: diagnostic evidence packet for source-policy residual terms.",
    "It does not choose a source correction, exclude a pair, or lock a replacement.",
    "- Priority source-policy terms: 1.",
    "- Related source-review rows: 2.",
    "- Related scenario-pair rows: 4.",
    "- WNP context blocks: 3.",
    "| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `WRR2 32` | `wnp_chelm_spelling_context` |",
    "`wrr2_32_app_04`",
    "`RBY$LMH`",
    "`/KA/TMWZ`",
    "`reports/wrr_1994/wnp_en.html:608-619`",
    "`review_chelm_spelling_only`",
    "source/pair-rule review",
    "No automatic correction or exclusion",
    "WNP context supports why the Chełm forms are in review scope, not a final pair-rule decision.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_policy_evidence_packet_doc(
        args.doc,
        args.packet,
        args.context,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source-policy evidence packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-policy evidence packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_source_policy_evidence_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
    context: Path | None = DEFAULT_CONTEXT,
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
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if context is not None:
        failures.extend(validate_context_csv(context))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    data = _read_csv(packet)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != PACKET_FIELDNAMES:
        failures.append(f"{packet} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{packet} has {len(rows)} rows; expected 1")
    if not rows:
        return failures
    row = rows[0]
    for key, expected in EXPECTED_PACKET_ROW.items():
        if row.get(key) != expected:
            failures.append(f"{packet} {key} drifted")
    scenario_statuses = [
        status for status in row.get("scenario_pair_statuses", "").split(";") if status
    ]
    if len(scenario_statuses) != 4:
        failures.append(f"{packet} scenario pair status count drifted")
    if "Chełm spelling-context target" not in row.get("evidence_read", ""):
        failures.append(f"{packet} evidence read drifted")
    return failures


def validate_context_csv(context: Path) -> list[str]:
    data = _read_csv(context)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != CONTEXT_FIELDNAMES:
        failures.append(f"{context} fieldnames drifted")
    if len(rows) != len(EXPECTED_CONTEXT):
        failures.append(f"{context} has {len(rows)} rows; expected {len(EXPECTED_CONTEXT)}")
    actual_refs = {row.get("context_id", ""): row.get("source_ref", "") for row in rows}
    if actual_refs != EXPECTED_CONTEXT:
        failures.append(f"{context} context refs drifted")
    for row in rows:
        context_id = row.get("context_id", "")
        if row.get("source_flag") != "wnp_chelm_spelling_context":
            failures.append(f"{context} {context_id} source flag drifted")
        if row.get("decision_boundary") != DECISION_BOUNDARY:
            failures.append(f"{context} {context_id} decision boundary drifted")
        if not row.get("source_terms") or not row.get("read"):
            failures.append(f"{context} {context_id} missing context read")
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
        failures.append(f"{summary} fieldnames drifted")
    if len(rows) != 1:
        failures.append(f"{summary} has {len(rows)} rows; expected 1")
    if not rows:
        return failures
    row = rows[0]
    for key, expected in EXPECTED_SUMMARY_ROW.items():
        if row.get(key) != expected:
            failures.append(f"{summary} {key} drifted")
    if "without changing the working source" not in row.get("read", ""):
        failures.append(f"{summary} read drifted")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_source_policy_evidence_packet",
        "evidence_rows": 1,
        "source_context_rows": len(EXPECTED_CONTEXT),
        "summary_rows": 1,
        "inputs": {
            "action_plan": str(builder.DEFAULT_ACTION_PLAN),
            "source_queue": str(builder.DEFAULT_SOURCE_QUEUE),
            "row_ocr": str(builder.DEFAULT_ROW_OCR),
            "scenario_pairs": str(builder.DEFAULT_SCENARIO_PAIRS),
            "table2_bridge": str(builder.DEFAULT_TABLE2_BRIDGE),
            "wnp_html": str(builder.DEFAULT_WNP_HTML),
        },
        "outputs": {
            "out": str(DEFAULT_PACKET),
            "source_context_out": str(DEFAULT_CONTEXT),
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
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return f"{path} is invalid JSON: {exc}"
    if not isinstance(data, dict):
        return f"{path} JSON root must be an object"
    return data


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
