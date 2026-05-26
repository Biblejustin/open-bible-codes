#!/usr/bin/env python3
"""Validate WRR blocker packet keeps no-input claim blockers visible."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path


DEFAULT_DOC = Path("docs/WRR_CLAIM_BLOCKER_PACKET.md")
DEFAULT_PACKET = Path("reports/wrr_1994/wrr_claim_blocker_packet.csv")
DEFAULT_READINESS = Path("reports/wrr_1994/wrr_claim_readiness.csv")
DEFAULT_SOURCE_QUEUE = Path("reports/wrr_1994/wrr_source_review_queue.csv")
DEFAULT_VARIANT_RESIDUAL_SUMMARY = Path(
    "reports/wrr_1994/wrr_variant_residual_review_summary.csv"
)
DEFAULT_RESIDUAL_TERM_SUMMARY = Path(
    "reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv"
)
DEFAULT_SOURCE_TRANSCRIPTION_ROW_SUMMARY = Path(
    "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
)
DEFAULT_REMAINING_LANE_SUMMARY = Path(
    "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv"
)

PACKET_FIELDNAMES = [
    "decision_area",
    "current_status",
    "ready",
    "blocker",
    "current_read",
    "available_options",
    "source_review_flags",
    "no_input_next",
    "input_needed",
]
EXPECTED_READINESS = {
    "Pair universe": "source_locked",
    "D(w) skip-cap formula": "source_locked",
    "Corrected distance c(w,w')": "defined_full_run",
    "Aggregate statistic and permutation": "permutation_locked",
}
EXPECTED_SOURCE_FLAGS = {
    "wnp_book_title_appellation_dispute": 1,
    "wnp_chelm_spelling_context": 2,
    "wnp_disputed_zacut_appellation": 2,
}
EXPECTED_FLAGGED_TERMS = {
    "2": ("wrr2_30_app_05", "wnp_book_title_appellation_dispute"),
    "5": ("wrr2_32_app_04", "wnp_chelm_spelling_context"),
    "7": ("wrr2_27_app_06", "wnp_disputed_zacut_appellation"),
    "12": ("wrr2_27_app_05", "wnp_disputed_zacut_appellation"),
    "83": ("wrr2_32_app_05", "wnp_chelm_spelling_context"),
}
EXPECTED_VISUAL_TERMS = {
    "1": ("wrr2_23_app_04", "treat as visual OCR miss until a locked transcription says otherwise"),
    "2": ("wrr2_30_app_05", "review title-prefix/appellation rule before any source correction"),
    "3": ("wrr2_23_app_05", "treat as visual OCR miss until a locked transcription says otherwise"),
    "4": ("wrr2_28_app_04", "review title-prefix/appellation rule before any source correction"),
    "5": ("wrr2_32_app_04", "review source/pair rule before using this as a Hebrew-cell match"),
    "6": ("wrr2_27_date_01", "check page image before treating as source difference"),
    "7": ("wrr2_27_app_06", "check WNP Zacut dispute and page image before treating as source difference"),
    "84": (
        "wrr2_19_app_11",
        "keep as page-image near-match until a locked transcription resolves the aleph spelling",
    ),
    "85": (
        "wrr2_19_app_12",
        "keep as page-image near-match until a locked transcription resolves the aleph spelling",
    ),
    "86": (
        "wrr2_31_app_07",
        "keep as page-image or pair-rule review before any source correction",
    ),
}
EXPECTED_VARIANT_RESIDUAL = {
    ("residual_pool", "candidate_pairs_not_closed_by_all-blocker_simple_variants"): "59",
    ("review_frontier", "minimum_residual_frontier"): "40",
    ("impact_status", "no_blocking_term_variant_hit"): "50",
    ("impact_status", "some_blocking_terms_have_variant_hit"): "9",
    ("row_ocr_pair_status", "both_matched"): "11",
    ("row_ocr_pair_status", "both_not_matched"): "3",
    ("row_ocr_pair_status", "mixed"): "45",
    ("frontier_impact_status", "no_blocking_term_variant_hit"): "31",
    ("frontier_impact_status", "some_blocking_terms_have_variant_hit"): "9",
    ("frontier_row_ocr_pair_status", "both_matched"): "2",
    ("frontier_row_ocr_pair_status", "both_not_matched"): "3",
    ("frontier_row_ocr_pair_status", "mixed"): "35",
    ("unresolved_term_side", "appellation"): "59",
    ("unresolved_term_bucket", "ocr_matched_no_variant_lead"): "11",
    ("unresolved_term_bucket", "ocr_near_match_no_variant_lead"): "3",
    ("unresolved_term_bucket", "ocr_not_matched_no_variant_lead"): "45",
    ("unresolved_source_flag", "wnp_chelm_spelling_context"): "1",
}
EXPECTED_RESIDUAL_TERM_SUMMARY = {
    ("residual_terms", "unique_unresolved_terms"): ("58", "59", "40"),
    ("term_side", "appellation"): ("58", "59", "40"),
    ("review_bucket", "ocr_matched_no_variant_lead"): ("11", "11", "2"),
    ("review_bucket", "ocr_near_match_no_variant_lead"): ("3", "3", "2"),
    ("review_bucket", "ocr_not_matched_no_variant_lead"): ("44", "45", "36"),
    ("term_ocr_status", "matched"): ("11", "11", "2"),
    ("term_ocr_status", "not_matched"): ("47", "48", "38"),
    ("source_flag", "wnp_chelm_spelling_context"): ("1", "1", "1"),
    ("reconciliation_need", "method_or_pair_universe_review"): ("11", "11", "2"),
    ("reconciliation_need", "page_image_near_match_review"): ("3", "3", "2"),
    ("reconciliation_need", "source_policy_or_pair_rule_review"): ("1", "1", "1"),
    ("reconciliation_need", "source_transcription_or_row_alignment"): ("43", "44", "35"),
}
SOURCE_TRANSCRIPTION_TOTALS = {
    "rows": 22,
    "action_terms": 43,
    "residual_pairs": 44,
    "frontier_pairs": 35,
}
EXPECTED_REMAINING_LANES = {
    "page_image_near_match_review": ("3", "3", "2"),
    "method_or_pair_universe_review": ("11", "11", "2"),
}

REQUIRED_PHRASES = (
    "# WRR Claim Blocker Packet",
    "Status: no current claim-readiness blockers under selected local WRR lock policy.",
    "| None | `ready` | Current method-status rows satisfy the claim-readiness gate. | none |",
    "Aggregate/permutation lock: keep-all cap1000 999,999 date-label permutation over the full selected-universe corrected-distance output.",
    "source/title-prefix rule review; visual notes show title text without visible B@L prefix",
    "source/pair-rule review; visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "## Exact-WRR Residual Caveat",
    "Residual Frontier Sample",
    "Residual Term Queue",
    "Top Residual Term Targets",
    "Source-Transcription Row Evidence Summary",
    "Source-Transcription Priority Rows",
    "review multi-term rows once by row before term edits",
    "Page-Image Near-Match Evidence Summary",
    "Page-Image Near-Match Terms",
    "near OCR exists, but page image must decide whether it is source evidence",
    "Method/Pair-Universe Evidence Summary",
    "OCR matched all method-lane terms",
    "unique_unresolved_terms",
    "source_policy_or_pair_rule_review",
    "wnp_chelm_spelling_context",
    "Residual term priority is a review order, not a correction set or pair-exclusion list.",
    "residual source/method gap after the simple-variant upper bound",
    "## Visual Triage Highlights",
    "primary page row visibly contains Yaakov Ha-Levi wording; row OCR missed it",
    "treat as visual OCR miss until a locked transcription says otherwise",
    "This is a decision packet, not a reproduction result.",
    "Pair universe lock: keep_all_working_source",
    "D(w) lock: printed WRR formula main",
    "No visual-review note excludes a pair automatically; pair exclusion would require an explicit source-policy change.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_blocker_packet_doc(
        args.doc,
        args.packet,
        args.readiness,
        args.source_queue,
        args.variant_residual_summary,
        args.residual_term_summary,
        args.source_transcription_row_summary,
        args.remaining_lane_summary,
    )
    if failures:
        for failure in failures:
            print(f"WRR claim-blocker packet failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR claim-blocker packet ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--source-queue", type=Path, default=DEFAULT_SOURCE_QUEUE)
    parser.add_argument(
        "--variant-residual-summary",
        type=Path,
        default=DEFAULT_VARIANT_RESIDUAL_SUMMARY,
    )
    parser.add_argument(
        "--residual-term-summary",
        type=Path,
        default=DEFAULT_RESIDUAL_TERM_SUMMARY,
    )
    parser.add_argument(
        "--source-transcription-row-summary",
        type=Path,
        default=DEFAULT_SOURCE_TRANSCRIPTION_ROW_SUMMARY,
    )
    parser.add_argument(
        "--remaining-lane-summary",
        type=Path,
        default=DEFAULT_REMAINING_LANE_SUMMARY,
    )
    return parser


def validate_blocker_packet_doc(
    doc: Path,
    packet: Path | None = DEFAULT_PACKET,
    readiness: Path | None = DEFAULT_READINESS,
    source_queue: Path | None = DEFAULT_SOURCE_QUEUE,
    variant_residual_summary: Path | None = DEFAULT_VARIANT_RESIDUAL_SUMMARY,
    residual_term_summary: Path | None = DEFAULT_RESIDUAL_TERM_SUMMARY,
    source_transcription_row_summary: Path | None = DEFAULT_SOURCE_TRANSCRIPTION_ROW_SUMMARY,
    remaining_lane_summary: Path | None = DEFAULT_REMAINING_LANE_SUMMARY,
) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures = [
        f"{doc} missing phrase: {phrase}"
        for phrase in REQUIRED_PHRASES
        if phrase not in text
    ]
    if packet is not None:
        failures.extend(validate_packet_csv(packet))
    if readiness is not None:
        failures.extend(validate_readiness_csv(readiness))
    if source_queue is not None:
        failures.extend(validate_source_queue_csv(source_queue))
    if variant_residual_summary is not None:
        failures.extend(validate_variant_residual_summary_csv(variant_residual_summary))
    if residual_term_summary is not None:
        failures.extend(validate_residual_term_summary_csv(residual_term_summary))
    if source_transcription_row_summary is not None:
        failures.extend(validate_source_transcription_row_summary_csv(source_transcription_row_summary))
    if remaining_lane_summary is not None:
        failures.extend(validate_remaining_lane_summary_csv(remaining_lane_summary))
    return failures


def validate_packet_csv(packet: Path) -> list[str]:
    data = _read_csv(packet)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != PACKET_FIELDNAMES:
        failures.append(f"{packet} fieldnames drifted")
    if rows:
        failures.append(f"{packet} has {len(rows)} rows; expected 0 ready-state blockers")
    return failures


def validate_readiness_csv(readiness: Path) -> list[str]:
    data = _read_csv(readiness)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    by_area = {row.get("decision_area", ""): row for row in rows}
    if set(by_area) != set(EXPECTED_READINESS):
        failures.append(f"{readiness} decision area set drifted")
    for area, expected_status in EXPECTED_READINESS.items():
        row = by_area.get(area)
        if row is None:
            continue
        if row.get("status") != expected_status:
            failures.append(f"{readiness} {area} status drifted")
        if row.get("ready") != "true":
            failures.append(f"{readiness} {area} no longer ready")
        if row.get("blocker"):
            failures.append(f"{readiness} {area} blocker field is populated")
        if not row.get("current_read") or not row.get("evidence"):
            failures.append(f"{readiness} {area} missing read/evidence")
    return failures


def validate_source_queue_csv(source_queue: Path) -> list[str]:
    data = _read_csv(source_queue)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    flag_counts = Counter(
        flag
        for row in rows
        for flag in row.get("source_review_flags", "").split(";")
        if flag
    )
    if dict(flag_counts) != EXPECTED_SOURCE_FLAGS:
        failures.append(f"{source_queue} source review flag counts drifted")
    by_rank = {row.get("priority_rank", ""): row for row in rows}
    for rank, (term_id, flag) in EXPECTED_FLAGGED_TERMS.items():
        row = by_rank.get(rank)
        if row is None:
            failures.append(f"{source_queue} missing flagged rank {rank}")
            continue
        if row.get("term_id") != term_id or row.get("source_review_flags") != flag:
            failures.append(f"{source_queue} flagged rank {rank} drifted")
        if not row.get("source_review_action"):
            failures.append(f"{source_queue} flagged rank {rank} missing action")
    visual_rows = [row for row in rows if row.get("visual_review_note")]
    if len(visual_rows) != len(EXPECTED_VISUAL_TERMS):
        failures.append(f"{source_queue} visual highlight count drifted")
    for rank, (term_id, action) in EXPECTED_VISUAL_TERMS.items():
        row = by_rank.get(rank)
        if row is None:
            failures.append(f"{source_queue} missing visual rank {rank}")
            continue
        if row.get("term_id") != term_id or row.get("visual_review_action") != action:
            failures.append(f"{source_queue} visual rank {rank} drifted")
        if not row.get("visual_review_note"):
            failures.append(f"{source_queue} visual rank {rank} missing note")
    return failures


def validate_variant_residual_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    by_key = {(row.get("group", ""), row.get("value", "")): row for row in rows}
    for key, expected_pairs in EXPECTED_VARIANT_RESIDUAL.items():
        row = by_key.get(key)
        if row is None:
            failures.append(f"{summary} missing {key[0]} {key[1]}")
            continue
        if row.get("pairs") != expected_pairs:
            failures.append(f"{summary} {key[0]} {key[1]} pairs drifted")
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{summary} {key[0]} {key[1]} run label drifted")
    residual_pool = by_key.get(
        ("residual_pool", "candidate_pairs_not_closed_by_all-blocker_simple_variants")
    )
    if residual_pool and (
        residual_pool.get("residual_needed") != "40"
        or residual_pool.get("residual_slack_pairs") != "19"
    ):
        failures.append(f"{summary} residual pool frontier arithmetic drifted")
    return failures


def validate_residual_term_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    by_key = {(row.get("group", ""), row.get("value", "")): row for row in rows}
    if set(by_key) != set(EXPECTED_RESIDUAL_TERM_SUMMARY):
        failures.append(f"{summary} residual term summary key set drifted")
    for key, expected_values in EXPECTED_RESIDUAL_TERM_SUMMARY.items():
        row = by_key.get(key)
        if row is None:
            continue
        for field, expected in zip(
            ("terms", "residual_pairs", "frontier_pairs"),
            expected_values,
            strict=True,
        ):
            if row.get(field) != expected:
                failures.append(f"{summary} {key[0]} {key[1]} {field} drifted")
    return failures


def validate_source_transcription_row_summary_csv(row_summary: Path) -> list[str]:
    data = _read_csv(row_summary)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    if len(rows) != SOURCE_TRANSCRIPTION_TOTALS["rows"]:
        failures.append(f"{row_summary} has {len(rows)} rows")
    sums = {
        "action_terms": sum(_int(row, "action_terms") for row in rows),
        "residual_pairs": sum(_int(row, "residual_pairs") for row in rows),
        "frontier_pairs": sum(_int(row, "frontier_pairs") for row in rows),
    }
    for metric, actual in sums.items():
        if actual != SOURCE_TRANSCRIPTION_TOTALS[metric]:
            failures.append(f"{row_summary} {metric}={actual}")
    top = next((row for row in rows if row.get("row_rank") == "1"), None)
    if top is None:
        failures.append(f"{row_summary} missing row rank 1")
    elif (
        top.get("row_number") != "06"
        or top.get("action_terms") != "4"
        or top.get("residual_pairs") != "4"
        or top.get("frontier_pairs") != "4"
    ):
        failures.append(f"{row_summary} top row drifted")
    return failures


def validate_remaining_lane_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    _, rows = data
    failures: list[str] = []
    by_lane = {row.get("action_lane", ""): row for row in rows}
    if set(by_lane) != set(EXPECTED_REMAINING_LANES):
        failures.append(f"{summary} remaining-lane set drifted")
    for lane, expected_values in EXPECTED_REMAINING_LANES.items():
        row = by_lane.get(lane)
        if row is None:
            continue
        for field, expected in zip(
            ("action_terms", "residual_pairs", "frontier_pairs"),
            expected_values,
            strict=True,
        ):
            if row.get(field) != expected:
                failures.append(f"{summary} {lane} {field} drifted")
        if not row.get("evidence_required") or not row.get("no_input_boundary"):
            failures.append(f"{summary} {lane} missing boundary fields")
    return failures


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]] | str:
    if not path.exists():
        return f"{path} is missing"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def _int(row: dict[str, str], key: str) -> int:
    value = row.get(key, "0")
    try:
        return int(value)
    except ValueError:
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
