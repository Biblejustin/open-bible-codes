#!/usr/bin/env python3
"""Validate WRR residual term reconciliation queue doc keeps limits explicit."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md")
DEFAULT_QUEUE = Path("reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv")
DEFAULT_SUMMARY = Path("reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv")

EXPECTED_TOTALS = {"terms": 58, "residual_pairs": 59, "frontier_pairs": 40}
EXPECTED_SUMMARY = {
    ("residual_terms", "unique_unresolved_terms"): (58, 59, 40),
    ("term_side", "appellation"): (58, 59, 40),
    ("review_bucket", "ocr_matched_no_variant_lead"): (11, 11, 2),
    ("review_bucket", "ocr_near_match_no_variant_lead"): (3, 3, 2),
    ("review_bucket", "ocr_not_matched_no_variant_lead"): (44, 45, 36),
    ("term_ocr_status", "matched"): (11, 11, 2),
    ("term_ocr_status", "not_matched"): (47, 48, 38),
    ("source_flag", "wnp_chelm_spelling_context"): (1, 1, 1),
    ("reconciliation_need", "method_or_pair_universe_review"): (11, 11, 2),
    ("reconciliation_need", "page_image_near_match_review"): (3, 3, 2),
    ("reconciliation_need", "source_policy_or_pair_rule_review"): (1, 1, 1),
    ("reconciliation_need", "source_transcription_or_row_alignment"): (43, 44, 35),
}
EXPECTED_NEEDS = {
    "source_policy_or_pair_rule_review": {
        "terms": 1,
        "residual_pairs": 1,
        "frontier_pairs": 1,
    },
    "source_transcription_or_row_alignment": {
        "terms": 43,
        "residual_pairs": 44,
        "frontier_pairs": 35,
    },
    "page_image_near_match_review": {
        "terms": 3,
        "residual_pairs": 3,
        "frontier_pairs": 2,
    },
    "method_or_pair_universe_review": {
        "terms": 11,
        "residual_pairs": 11,
        "frontier_pairs": 2,
    },
}
EXPECTED_PRIORITY_ONE = {
    "term_id": "wrr2_32_app_05",
    "term": "$LMHMX@LMA",
    "term_side": "appellation",
    "residual_pairs": "1",
    "frontier_pairs": "1",
    "review_buckets": "ocr_not_matched_no_variant_lead",
    "term_ocr_statuses": "not_matched",
    "source_flags": "wnp_chelm_spelling_context",
    "reconciliation_need": "source_policy_or_pair_rule_review",
    "source_queue_best_variant_hits": "0",
    "source_queue_best_variant_rule": "none",
    "pair_ids": "wrr2_32_app_05__wrr2_32_date_01",
}

REQUIRED_PHRASES = (
    "# WRR Residual Term Reconciliation Queue",
    "Status: diagnostic-only unique-term queue from the residual pair packet.",
    "does not select source corrections, exclude pairs, or reproduce WRR",
    "- Unique unresolved terms: 58.",
    "- Residual pair links represented: 59.",
    "- Minimum-frontier pair links represented: 40.",
    "| `term_side` | `appellation` | 58 | 59 | 40 |",
    "| `source_flag` | `wnp_chelm_spelling_context` | 1 | 1 | 1 |",
    "| `reconciliation_need` | `source_transcription_or_row_alignment` | 43 | 44 | 35 |",
    "| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `source_policy_or_pair_rule_review` |",
    "Source-Policy Context",
    "pair-rule evidence before any source-lock change",
    "method or pair-universe blockers",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_residual_term_reconciliation_queue_doc(
        args.doc,
        args.queue,
        args.summary,
    )
    if failures:
        for failure in failures:
            print(
                f"WRR residual term reconciliation doc failure: {failure}",
                file=sys.stderr,
            )
        return 1
    print(f"WRR residual term reconciliation doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    return parser


def validate_residual_term_reconciliation_queue_doc(
    doc: Path,
    queue: Path | None = DEFAULT_QUEUE,
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
    if queue is not None:
        failures.extend(validate_queue_csv(queue))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    return failures


def validate_queue_csv(queue: Path) -> list[str]:
    rows = _read_csv(queue)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    expected_rows = EXPECTED_TOTALS["terms"]
    if len(rows) != expected_rows:
        failures.append(f"{queue} has {len(rows)} rows; expected {expected_rows}")
    ranks = [row.get("priority_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, len(rows) + 1)]
    if ranks != expected_ranks:
        failures.append(f"{queue} priority_rank sequence drifted")
    totals = {
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
    }
    for key, expected in EXPECTED_TOTALS.items():
        actual = len(rows) if key == "terms" else totals[key]
        if actual != expected:
            failures.append(f"{queue} {key}={actual}; expected {expected}")
    priority_one = next((row for row in rows if row.get("priority_rank") == "1"), None)
    if priority_one is None:
        failures.append(f"{queue} missing priority rank 1")
    else:
        for key, expected in EXPECTED_PRIORITY_ONE.items():
            if priority_one.get(key, "") != expected:
                failures.append(f"{queue} priority 1 {key} drifted")
    failures.extend(_validate_need_rows(queue, rows))
    for row in rows:
        rank = row.get("priority_rank", "")
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{queue} rank {rank} run label drifted")
        if row.get("term_side") != "appellation":
            failures.append(f"{queue} rank {rank} term side drifted")
        if not row.get("term_id") or not row.get("term") or not row.get("pair_ids"):
            failures.append(f"{queue} rank {rank} missing term or pair ids")
        if row.get("reconciliation_need") not in EXPECTED_NEEDS:
            failures.append(f"{queue} rank {rank} unknown reconciliation need")
        if row.get("source_queue_best_variant_hits") not in {"", "0"}:
            failures.append(f"{queue} rank {rank} variant count drifted")
        if row.get("source_queue_best_variant_rule") not in {"", "none"}:
            failures.append(f"{queue} rank {rank} variant rule drifted")
    return failures


def _validate_need_rows(
    path: Path,
    rows: list[dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    for need, expected in EXPECTED_NEEDS.items():
        need_rows = [row for row in rows if row.get("reconciliation_need") == need]
        if len(need_rows) != expected["terms"]:
            failures.append(f"{path} {need} has {len(need_rows)} rows")
        for metric in ("residual_pairs", "frontier_pairs"):
            actual = sum(_int(row, metric) for row in need_rows)
            if actual != expected[metric]:
                failures.append(f"{path} {need} {metric}={actual}")
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    rows = _read_csv(summary)
    if isinstance(rows, str):
        return [rows]
    failures: list[str] = []
    if len(rows) != len(EXPECTED_SUMMARY):
        failures.append(
            f"{summary} has {len(rows)} rows; expected {len(EXPECTED_SUMMARY)}"
        )
    by_key = {(row.get("group", ""), row.get("value", "")): row for row in rows}
    if set(by_key) != set(EXPECTED_SUMMARY):
        failures.append(f"{summary} summary key set drifted")
    for key, expected_values in EXPECTED_SUMMARY.items():
        row = by_key.get(key)
        if row is None:
            continue
        for field, expected in zip(
            ("terms", "residual_pairs", "frontier_pairs"),
            expected_values,
            strict=True,
        ):
            if row.get(field) != str(expected):
                failures.append(f"{summary} {key[0]} {key[1]} {field} drifted")
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{summary} {key[0]} {key[1]} run label drifted")
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
