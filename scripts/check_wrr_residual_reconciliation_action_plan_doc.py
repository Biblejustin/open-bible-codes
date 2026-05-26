#!/usr/bin/env python3
"""Validate WRR residual reconciliation action plan keeps limits explicit."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md")
DEFAULT_PLAN = Path("reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv")

LANE_LOCKS = {
    "source_policy_or_pair_rule_review": {
        "terms": 1,
        "residual_pairs": 1,
        "frontier_pairs": 1,
        "evidence_required": (
            "citable source-policy or pair-rule evidence for whether the flagged "
            "appellation belongs in the selected pair universe"
        ),
        "no_input_boundary": (
            "keep term in working source; no automatic correction or exclusion "
            "without citable rule"
        ),
    },
    "source_transcription_or_row_alignment": {
        "terms": 43,
        "residual_pairs": 44,
        "frontier_pairs": 35,
        "evidence_required": (
            "primary table row transcription or row-alignment evidence for the "
            "imported term; current queue has no simple variant lead"
        ),
        "no_input_boundary": (
            "keep imported term; do not correct transcription until primary row "
            "evidence is locked"
        ),
    },
    "page_image_near_match_review": {
        "terms": 3,
        "residual_pairs": 3,
        "frontier_pairs": 2,
        "evidence_required": (
            "page-image inspection against near-match OCR before treating the "
            "term as source text or method blocker"
        ),
        "no_input_boundary": (
            "keep imported term; do not treat near OCR as correction without "
            "page-image review"
        ),
    },
    "method_or_pair_universe_review": {
        "terms": 11,
        "residual_pairs": 11,
        "frontier_pairs": 2,
        "evidence_required": (
            "method and pair-universe review because OCR already matched but "
            "ordinary hits remain absent"
        ),
        "no_input_boundary": (
            "keep source row; investigate ordinary-hit method or pair universe "
            "before source edits"
        ),
    },
}

EXPECTED_TOTALS = {"terms": 58, "residual_pairs": 59, "frontier_pairs": 40}

REQUIRED_PHRASES = (
    "# WRR Residual Reconciliation Action Plan",
    "Status: diagnostic action plan from the residual unique-term queue.",
    "does not select source corrections, exclude pairs, or reproduce WRR",
    "- Action terms: 58.",
    "- Residual pair links: 59.",
    "- Minimum-frontier pair links: 40.",
    "| `source_policy_or_pair_rule_review` | 1 | 1 | 1 |",
    "| `source_transcription_or_row_alignment` | 43 | 44 | 35 |",
    "| 1 | `source_policy_or_pair_rule_review` | `wrr2_32_app_05` | `$LMHMX@LMA` |",
    "keep term in working source; no automatic correction or exclusion without citable rule",
    "method or pair-universe review before source edits",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_residual_reconciliation_action_plan_doc(
        args.doc,
        args.plan,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"WRR residual reconciliation action-plan failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR residual reconciliation action plan ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_residual_reconciliation_action_plan_doc(
    doc: Path,
    plan: Path | None = DEFAULT_PLAN,
    summary: Path | None = DEFAULT_SUMMARY,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    if plan is not None:
        failures.extend(validate_plan_csv(plan))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    return failures


def validate_plan_csv(plan: Path) -> list[str]:
    rows = _read_csv(plan)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    expected_rows = EXPECTED_TOTALS["terms"]
    if len(rows) != expected_rows:
        failures.append(f"{plan} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("action_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, expected_rows + 1)]
    if ranks != expected_ranks:
        failures.append(f"{plan} action_rank sequence drifted")
    for lane, locks in LANE_LOCKS.items():
        lane_rows = [row for row in rows if row.get("action_lane") == lane]
        failures.extend(_validate_lane_rows(plan, lane, lane_rows, locks))
    known_lanes = set(LANE_LOCKS)
    for row in rows:
        rank = row.get("action_rank", "")
        if row.get("action_lane") not in known_lanes:
            failures.append(f"{plan} rank {rank} unknown lane")
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{plan} rank {rank} run label drifted")
        if row.get("term_side") != "appellation":
            failures.append(f"{plan} rank {rank} term side drifted")
        if row.get("source_queue_best_variant_hits") != "0":
            failures.append(f"{plan} rank {rank} variant count drifted")
        if row.get("source_queue_best_variant_rule") != "none":
            failures.append(f"{plan} rank {rank} variant rule drifted")
        if not row.get("term_id") or not row.get("pair_ids"):
            failures.append(f"{plan} rank {rank} missing term or pair ids")
    return failures


def _validate_lane_rows(
    path: Path,
    lane: str,
    rows: list[dict[str, str]],
    locks: dict[str, object],
) -> list[str]:
    failures: list[str] = []
    if len(rows) != locks["terms"]:
        failures.append(f"{path} {lane} has {len(rows)} rows")
    for metric in ("residual_pairs", "frontier_pairs"):
        actual = sum(_int(row, metric) for row in rows)
        if actual != locks[metric]:
            failures.append(f"{path} {lane} {metric}={actual}")
    for row in rows:
        rank = row.get("action_rank", row.get("action_lane", ""))
        for key in ("evidence_required", "no_input_boundary"):
            if row.get(key) != locks[key]:
                failures.append(f"{path} rank {rank} {key} drifted")
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    rows = _read_csv(summary)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != len(LANE_LOCKS):
        failures.append(f"{summary} has {len(rows)} rows; expected {len(LANE_LOCKS)}")
    lanes = {row.get("action_lane", ""): row for row in rows}
    if set(lanes) != set(LANE_LOCKS):
        failures.append(f"{summary} lane set drifted")
    for lane, locks in LANE_LOCKS.items():
        row = lanes.get(lane)
        if row is None:
            continue
        for key in (
            "terms",
            "residual_pairs",
            "frontier_pairs",
            "evidence_required",
            "no_input_boundary",
        ):
            expected = str(locks[key])
            if row.get(key) != expected:
                failures.append(f"{summary} {lane} {key} drifted")
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


if __name__ == "__main__":
    raise SystemExit(main())
