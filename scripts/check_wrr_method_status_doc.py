#!/usr/bin/env python3
"""Validate WRR method-status doc keeps reproduction blockers explicit."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

from scripts import build_wrr_method_status as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_STATUS = builder.DEFAULT_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

FIELDNAMES = builder.FIELDNAMES

EXPECTED_STATUS = {
    "Genesis text stream": "locally_locked",
    "WRR2 term source": "working_source_locked",
    "Pair universe": "source_locked",
    "D(w) skip-cap formula": "source_locked",
    "Corrected distance c(w,w')": "defined_full_run",
    "Aggregate statistic and permutation": "permutation_locked",
}

REQUIRED_PHRASES = (
    "# WRR Method Status",
    "Status: current audit matrix; not an exact published WRR reproduction.",
    "still has a 163-distance gap; current manual records do not authorize source edits",
    "| Genesis text stream | `locally_locked` |",
    "| WRR2 term source | `working_source_locked` |",
    "| Pair universe | `source_locked` |",
    "| D(w) skip-cap formula | `source_locked` |",
    "| Corrected distance c(w,w') | `defined_full_run` |",
    "| Aggregate statistic and permutation | `permutation_locked` |",
    "variant-gap impact best run",
    "variant residual review best run",
    "manual no-source-change locks visible",
    "Source Anchors",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_method_status_doc(args.doc, args.status, args.manifest)
    if failures:
        for failure in failures:
            print(f"WRR method-status doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR method-status doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--status", type=Path, default=DEFAULT_STATUS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_method_status_doc(
    doc: Path,
    status: Path | None = DEFAULT_STATUS,
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
    if status is not None:
        failures.extend(validate_status_csv(status))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_status_csv(status: Path) -> list[str]:
    data = _read_csv(status)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != FIELDNAMES:
        failures.append(f"{status} fieldnames drifted")
    if len(rows) != len(EXPECTED_STATUS):
        failures.append(f"{status} has {len(rows)} rows; expected {len(EXPECTED_STATUS)}")
    by_area = {row.get("decision_area", ""): row for row in rows}
    if set(by_area) != set(EXPECTED_STATUS):
        failures.append(f"{status} decision area set drifted")
    for area, expected_status in EXPECTED_STATUS.items():
        row = by_area.get(area)
        if row is None:
            continue
        if row.get("status") != expected_status:
            failures.append(f"{status} {area} status drifted")
        if not row.get("current_read") or not row.get("evidence") or not row.get("next_action"):
            failures.append(f"{status} {area} missing read/evidence/action")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_method_status.py",
        "inputs": {
            "text_source": str(builder.DEFAULT_TEXT_SOURCE),
            "pair_summary": str(builder.DEFAULT_PAIR_SUMMARY),
            "defined_pair_summary": str(builder.DEFAULT_DEFINED_PAIR_SUMMARY),
            "defined_gap_reasons": str(builder.DEFAULT_DEFINED_GAP_REASONS),
            "zero_hit_variant_summary": str(builder.DEFAULT_ZERO_HIT_VARIANT_SUMMARY),
            "variant_gap_summary": str(builder.DEFAULT_VARIANT_GAP_SUMMARY),
            "variant_residual_summary": str(builder.DEFAULT_VARIANT_RESIDUAL_SUMMARY),
            "table2_bridge_summary": str(builder.DEFAULT_TABLE2_BRIDGE_SUMMARY),
            "table2_ocr_summary": str(builder.DEFAULT_TABLE2_OCR_SUMMARY),
            "table2_row_ocr_summary": str(builder.DEFAULT_TABLE2_ROW_OCR_SUMMARY),
            "skip_summary": str(builder.DEFAULT_SKIP_SUMMARY),
            "corrected_distance_variants": str(builder.DEFAULT_VARIANTS),
            "source_policy_scenarios": str(builder.DEFAULT_SOURCE_POLICY_SCENARIOS),
            "source_policy_term_impacts": str(builder.DEFAULT_SOURCE_POLICY_TERM_IMPACTS),
            "dw_formula_sensitivity": str(builder.DEFAULT_DW_FORMULA_SENSITIVITY),
            "corrected_distance_aggregate": str(builder.DEFAULT_AGGREGATE),
            "cross_pair_permutation_summary": str(
                builder.DEFAULT_CROSS_PAIR_PERMUTATION_SUMMARY
            ),
            "cross_pair_recommended_permutation_summary": str(
                builder.DEFAULT_CROSS_PAIR_RECOMMENDED_PERMUTATION_SUMMARY
            ),
            "highcap_corrected_distance_summary": str(
                builder.DEFAULT_HIGHCAP_CORRECTED_DISTANCE_SUMMARY
            ),
            "highcap_perturbation_summary": str(
                builder.DEFAULT_HIGHCAP_PERTURBATION_SUMMARY
            ),
            "highcap_pair_readiness_summary": str(
                builder.DEFAULT_HIGHCAP_PAIR_READINESS_SUMMARY
            ),
            "primary_result_table": str(builder.DEFAULT_PRIMARY_RESULT_TABLE),
        },
        "outputs": {
            "csv": str(DEFAULT_STATUS),
            "markdown": str(DEFAULT_DOC),
            "manifest": str(DEFAULT_MANIFEST),
        },
        "rows": len(EXPECTED_STATUS),
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


if __name__ == "__main__":
    raise SystemExit(main())
