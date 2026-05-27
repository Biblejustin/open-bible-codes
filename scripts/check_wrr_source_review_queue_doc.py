#!/usr/bin/env python3
"""Validate WRR source-review queue doc stays diagnostic."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts import build_wrr_source_review_queue as builder

DEFAULT_DOC = builder.DEFAULT_MD
DEFAULT_QUEUE = builder.DEFAULT_OUT
DEFAULT_SUMMARY = builder.DEFAULT_SUMMARY_OUT
DEFAULT_MANIFEST = builder.DEFAULT_MANIFEST

QUEUE_FIELDNAMES = builder.QUEUE_FIELDNAMES
SUMMARY_FIELDNAMES = builder.SUMMARY_FIELDNAMES

EXPECTED_SUMMARY = {
    "ocr_not_matched_with_variant_lead": ("5", "5", "7", "5 not_matched"),
    "ocr_near_match_with_variant_lead": ("2", "16", "13", "2 not_matched"),
    "ocr_matched_with_variant_lead": ("32", "45", "948", "32 matched"),
    "ocr_not_matched_no_variant_lead": ("44", "45", "0", "44 not_matched"),
    "ocr_near_match_no_variant_lead": ("3", "3", "0", "3 not_matched"),
    "ocr_matched_no_variant_lead": ("11", "11", "0", "11 matched"),
}
EXPECTED_TOP_RANKS = {
    "1": ("wrr2_23_app_04", "ocr_not_matched_with_variant_lead", "not_matched", "2"),
    "2": ("wrr2_30_app_05", "ocr_not_matched_with_variant_lead", "not_matched", "2"),
    "3": ("wrr2_23_app_05", "ocr_not_matched_with_variant_lead", "not_matched", "1"),
    "4": ("wrr2_28_app_04", "ocr_not_matched_with_variant_lead", "not_matched", "1"),
    "5": ("wrr2_32_app_04", "ocr_not_matched_with_variant_lead", "not_matched", "1"),
    "6": ("wrr2_27_date_01", "ocr_near_match_with_variant_lead", "not_matched", "12"),
    "7": ("wrr2_27_app_06", "ocr_near_match_with_variant_lead", "not_matched", "1"),
}
EXPECTED_SOURCE_FLAGS = {
    "wnp_book_title_appellation_dispute": 1,
    "wnp_chelm_spelling_context": 2,
    "wnp_disputed_zacut_appellation": 2,
}
EXPECTED_FLAGGED_RANKS = {
    "2": ("wrr2_30_app_05", "wnp_book_title_appellation_dispute"),
    "5": ("wrr2_32_app_04", "wnp_chelm_spelling_context"),
    "7": ("wrr2_27_app_06", "wnp_disputed_zacut_appellation"),
    "12": ("wrr2_27_app_05", "wnp_disputed_zacut_appellation"),
    "83": ("wrr2_32_app_05", "wnp_chelm_spelling_context"),
}
EXPECTED_VISUAL_RANKS = {
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

REQUIRED_PHRASES = (
    "# WRR Source Review Queue",
    "Status: diagnostic-only source-review triage",
    "not a source correction",
    "not a term replacement",
    "not a WRR reproduction",
    "- Terms queued: 97.",
    "| `ocr_not_matched_with_variant_lead` | 5 | 5 | 7 |",
    "| `ocr_matched_with_variant_lead` | 32 | 45 | 948 |",
    "| `ocr_not_matched_no_variant_lead` | 44 | 45 | 0 |",
    "Visual Triage Notes For Queued Terms",
    "treat as visual OCR miss until a locked transcription says otherwise",
    "review title-prefix/appellation rule before any source correction",
    "English label says of-Chelm; visible primary Hebrew cell supports Rabbi Shelomo only in this pass",
    "WNP Context For Queued Terms",
    "visual notes show title text without visible B@L prefix",
    "visual notes show English of-Chelm label but primary Hebrew cell only supports RBY$LMH in this pass",
    "Variant leads do not validate the original blocked pairs.",
    "Locked source rows and pair rules are still required before reproduction language.",
    "Visual-review notes do not exclude pairs automatically.",
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_source_review_queue_doc(
        args.doc,
        args.queue,
        args.summary,
        args.manifest,
    )
    if failures:
        for failure in failures:
            print(f"WRR source-review queue doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"WRR source-review queue doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser


def validate_source_review_queue_doc(
    doc: Path,
    queue: Path | None = DEFAULT_QUEUE,
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
    if queue is not None:
        failures.extend(validate_queue_csv(queue))
    if summary is not None:
        failures.extend(validate_summary_csv(summary))
    if manifest is not None:
        failures.extend(validate_manifest(manifest))
    return failures


def validate_queue_csv(queue: Path) -> list[str]:
    data = _read_csv(queue)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != QUEUE_FIELDNAMES:
        failures.append(f"{queue} fieldnames drifted")
    if len(rows) != 97:
        failures.append(f"{queue} has {len(rows)} rows; expected 97")
    ranks = [row.get("priority_rank", "") for row in rows]
    expected_ranks = [str(index) for index in range(1, len(rows) + 1)]
    if ranks != expected_ranks:
        failures.append(f"{queue} priority_rank sequence drifted")
    for row in rows:
        rank = row.get("priority_rank", "")
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{queue} rank {rank} run label drifted")
        if not row.get("term_id") or not row.get("pair_ids") or not row.get("read"):
            failures.append(f"{queue} rank {rank} missing term/pairs/read")
    by_rank = {row.get("priority_rank", ""): row for row in rows}
    for rank, (term_id, bucket, ocr_status, variant_hits) in EXPECTED_TOP_RANKS.items():
        row = by_rank.get(rank)
        if row is None:
            failures.append(f"{queue} missing top rank {rank}")
            continue
        checks = {
            "term_id": term_id,
            "review_bucket": bucket,
            "row_ocr_status": ocr_status,
            "best_variant_hit_count": variant_hits,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{queue} top rank {rank} {key} drifted")
    failures.extend(_validate_source_flags(queue, rows, by_rank))
    failures.extend(_validate_visual_rows(queue, rows, by_rank))
    return failures


def _validate_source_flags(
    queue: Path,
    rows: list[dict[str, str]],
    by_rank: dict[str, dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    flag_counts = Counter(
        flag
        for row in rows
        for flag in row.get("source_review_flags", "").split(";")
        if flag
    )
    if dict(flag_counts) != EXPECTED_SOURCE_FLAGS:
        failures.append(f"{queue} source review flag counts drifted")
    for rank, (term_id, flag) in EXPECTED_FLAGGED_RANKS.items():
        row = by_rank.get(rank)
        if row is None:
            failures.append(f"{queue} missing flagged rank {rank}")
            continue
        if row.get("term_id") != term_id or row.get("source_review_flags") != flag:
            failures.append(f"{queue} flagged rank {rank} drifted")
        if not row.get("source_review_note") or not row.get("source_review_action"):
            failures.append(f"{queue} flagged rank {rank} missing source context")
    return failures


def _validate_visual_rows(
    queue: Path,
    rows: list[dict[str, str]],
    by_rank: dict[str, dict[str, str]],
) -> list[str]:
    failures: list[str] = []
    visual_rows = [row for row in rows if row.get("visual_review_note")]
    if len(visual_rows) != len(EXPECTED_VISUAL_RANKS):
        failures.append(f"{queue} visual note count drifted")
    for rank, (term_id, action) in EXPECTED_VISUAL_RANKS.items():
        row = by_rank.get(rank)
        if row is None:
            failures.append(f"{queue} missing visual rank {rank}")
            continue
        if row.get("term_id") != term_id or row.get("visual_review_action") != action:
            failures.append(f"{queue} visual rank {rank} drifted")
        if not row.get("visual_review_note"):
            failures.append(f"{queue} visual rank {rank} missing note")
    return failures


def validate_summary_csv(summary: Path) -> list[str]:
    data = _read_csv(summary)
    if isinstance(data, str):
        return [data]
    fieldnames, rows = data
    failures: list[str] = []
    if fieldnames != SUMMARY_FIELDNAMES:
        failures.append(f"{summary} fieldnames drifted")
    by_bucket = {row.get("review_bucket", ""): row for row in rows}
    if set(by_bucket) != set(EXPECTED_SUMMARY):
        failures.append(f"{summary} bucket set drifted")
    for bucket, expected in EXPECTED_SUMMARY.items():
        row = by_bucket.get(bucket)
        if row is None:
            continue
        terms, blocking_pairs, variant_hit_total, row_ocr_statuses = expected
        checks = {
            "terms": terms,
            "blocking_pairs": blocking_pairs,
            "variant_hit_total": variant_hit_total,
            "row_ocr_statuses": row_ocr_statuses,
        }
        for key, value in checks.items():
            if row.get(key) != value:
                failures.append(f"{summary} {bucket} {key} drifted")
        if row.get("run_label") != "all_lanes_cap1000":
            failures.append(f"{summary} {bucket} run label drifted")
    return failures


def validate_manifest(manifest: Path) -> list[str]:
    data = _read_json(manifest)
    if isinstance(data, str):
        return [data]
    expected = {
        "tool": "build_wrr_source_review_queue",
        "run_label": "all_lanes_cap1000",
        "inputs": {
            "blocked_pairs": str(builder.DEFAULT_BLOCKED_PAIRS),
            "variants": str(builder.DEFAULT_VARIANTS),
            "row_ocr": str(builder.DEFAULT_ROW_OCR),
        },
        "outputs": {
            "out": str(DEFAULT_QUEUE),
            "summary_out": str(DEFAULT_SUMMARY),
            "markdown_out": str(DEFAULT_DOC),
            "manifest_out": str(DEFAULT_MANIFEST),
        },
        "queue_rows": 97,
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
        return reader.fieldnames or [], list(reader)


def _read_json(path: Path) -> dict[str, Any] | str:
    if not path.exists():
        return f"{path} is missing"
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(text: str) -> str:
    return " ".join(text.split())


if __name__ == "__main__":
    raise SystemExit(main())
