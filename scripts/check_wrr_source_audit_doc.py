#!/usr/bin/env python3
"""Validate WRR source-audit doc keeps current local-lock boundary."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_SOURCE_AUDIT.md")
DEFAULT_LOCKED_METHOD_REPORT = Path("reports/wrr_1994/wrr_locked_method_report.csv")
DEFAULT_METHOD_STATUS = Path("reports/wrr_1994/wrr_method_status.csv")
DEFAULT_MANUAL_SUMMARY = Path("reports/wrr_1994/wrr_manual_decision_register_summary.csv")

EXPECTED_LOCKED_METHOD_ROWS = {
    ("status", "report_status"): (
        "locked local WRR method report; not an exact published WRR reproduction",
        "locked_local_not_exact_reproduction",
    ),
    ("lock", "Pair universe"): ("keep_all_working_source", "source_locked"),
    ("lock", "D(w)"): (
        "printed WRR formula main; reported-program formula sensitivity",
        "source_locked",
    ),
    ("lock", "corrected_distance"): (
        "full selected universe cap1000; undefined ordinary-not-valid",
        "defined_full_run",
    ),
    ("lock", "Permutation"): ("999,999 date-label shuffles", "permutation_locked"),
    ("lock", "Manual decisions"): (
        "37 locked rows: 26 no_source_change; 11 method_lock",
        "locked",
    ),
    ("local_result", "observed_rows"): (
        "182",
        "diagnostic_only_not_wrr_reproduction",
    ),
    ("local_result", "defined_c_values"): (
        "72",
        "diagnostic_only_not_wrr_reproduction",
    ),
    ("local_result", "ordinary_not_valid"): (
        "110",
        "diagnostic_only_not_wrr_reproduction",
    ),
    ("boundary", "source_defined_gap"): (
        "defined 72 of 163; gap 91",
        "diagnostic_only_not_wrr_reproduction",
    ),
}
EXPECTED_METHOD_STATUS = {
    "Genesis text stream": "locally_locked",
    "WRR2 term source": "working_source_locked",
    "Pair universe": "source_locked",
    "D(w) skip-cap formula": "source_locked",
    "Corrected distance c(w,w')": "defined_full_run",
    "Aggregate statistic and permutation": "permutation_locked",
}
EXPECTED_METHOD_EVIDENCE_SNIPPETS = {
    "Pair universe": (
        "source policy selected: keep_all_working_source",
        "Visual triage notes do not exclude pairs automatically",
    ),
    "D(w) skip-cap formula": (
        "D(w) sensitivity: all-lane cap1000 printed/program defined 72/72",
        "printed formula selected as main",
    ),
    "Corrected distance c(w,w')": (
        "full all-lane cap 1000 run: 72 defined over 182 selected pairs",
        "110 ordinary-not-valid",
    ),
    "Aggregate statistic and permutation": (
        "locked keep-all cap1000 999999 date-label permutation",
        "rho0=0.000404",
    ),
}
EXPECTED_MANUAL_SUMMARY = {
    "source_policy_pair_rule": (
        "1",
        "1",
        "1",
        "1",
        "pending_source_policy_pair_rule_lock",
    ),
    "source_transcription_row_cluster": (
        "22",
        "43",
        "44",
        "35",
        "pending_manual_source_lock",
    ),
    "page_image_near_match": (
        "3",
        "3",
        "3",
        "2",
        "pending_page_image_lock",
    ),
    "method_pair_universe": (
        "11",
        "11",
        "11",
        "2",
        "pending_method_pair_universe_lock",
    ),
}

REQUIRED_PHRASES = (
    "# WRR Source Audit",
    "Status: source audit trail for WRR; local locked-method evidence exists",
    "exact published WRR reproduction remains caveated",
    "Visual triage",
    "do not exclude pairs automatically",
    "The repo now has a locked local reporting path: keep_all_working_source",
    "printed `D(w)` as the main rule",
    "reported-program `D(w)` as sensitivity output",
    "full selected-universe cap-1000 corrected-distance output",
    "keep-all cap-1000 999,999 date-label permutation",
    "source-cited 163 defined distances still do not match the current 72 defined",
    "current manual decision records keep the working source unchanged",
    "locking method-lane rows",
    "Do not describe that local run as exact published WRR reproduction.",
)

FORBIDDEN_PHRASES = (
    "corrected-distance smoke driver built",
    "future corrected-distance implementation",
    "missing corrected-distance layer",
    "the WRR distance metric is implemented and tested against toy fixtures",
    "the permutation procedure is implemented with saved seeds and manifests",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_audit_doc(
        args.doc,
        locked_method_report=args.locked_method_report,
        method_status=args.method_status,
        manual_summary=args.manual_summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR source-audit doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-audit doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument(
        "--locked-method-report",
        type=Path,
        default=DEFAULT_LOCKED_METHOD_REPORT,
    )
    parser.add_argument("--method-status", type=Path, default=DEFAULT_METHOD_STATUS)
    parser.add_argument("--manual-summary", type=Path, default=DEFAULT_MANUAL_SUMMARY)
    return parser


def validate_source_audit_doc(
    doc: Path = DEFAULT_DOC,
    *,
    locked_method_report: Path | None = DEFAULT_LOCKED_METHOD_REPORT,
    method_status: Path | None = DEFAULT_METHOD_STATUS,
    manual_summary: Path | None = DEFAULT_MANUAL_SUMMARY,
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
    for phrase in FORBIDDEN_PHRASES:
        if normalize_space(phrase) in normalized_text:
            failures.append(f"{doc} contains stale phrase: {phrase}")
    if locked_method_report is not None:
        failures.extend(validate_locked_method_report(locked_method_report))
    if method_status is not None:
        failures.extend(validate_method_status(method_status))
    if manual_summary is not None:
        failures.extend(validate_manual_summary(manual_summary))
    return failures


def validate_locked_method_report(path: Path) -> list[str]:
    rows = _read_csv(path)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    by_key = {(row.get("section", ""), row.get("item", "")): row for row in rows}
    for key, (value, status) in EXPECTED_LOCKED_METHOD_ROWS.items():
        row = by_key.get(key)
        if row is None:
            failures.append(f"{path} missing row {key}")
            continue
        if row.get("value") != value:
            failures.append(f"{path} {key} value drifted")
        if row.get("status") != status:
            failures.append(f"{path} {key} status drifted")
        if not row.get("evidence") or not row.get("source"):
            failures.append(f"{path} {key} missing evidence/source")
    return failures


def validate_method_status(path: Path) -> list[str]:
    rows = _read_csv(path)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    by_area = {row.get("decision_area", ""): row for row in rows}
    if set(by_area) != set(EXPECTED_METHOD_STATUS):
        failures.append(f"{path} decision-area set drifted")
    for area, status in EXPECTED_METHOD_STATUS.items():
        row = by_area.get(area)
        if row is None:
            continue
        if row.get("status") != status:
            failures.append(f"{path} {area} status drifted")
        if not row.get("current_read") or not row.get("next_action"):
            failures.append(f"{path} {area} current_read/next_action drifted")
        for snippet in EXPECTED_METHOD_EVIDENCE_SNIPPETS.get(area, ()):
            if snippet not in row.get("evidence", ""):
                failures.append(f"{path} {area} evidence missing: {snippet}")
    return failures


def validate_manual_summary(path: Path) -> list[str]:
    rows = _read_csv(path)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    by_lane = {row.get("decision_lane", ""): row for row in rows}
    if set(by_lane) != set(EXPECTED_MANUAL_SUMMARY):
        failures.append(f"{path} decision-lane set drifted")
    for lane, expected in EXPECTED_MANUAL_SUMMARY.items():
        row = by_lane.get(lane)
        if row is None:
            continue
        keys = [
            "decision_rows",
            "action_terms",
            "residual_pairs",
            "frontier_pairs",
            "review_state",
        ]
        for key, value in zip(keys, expected, strict=True):
            if row.get(key) != value:
                failures.append(f"{path} {lane} {key} drifted")
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
