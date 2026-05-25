#!/usr/bin/env python3
"""Validate the manual-review queue stays evidence-linked and non-claiming."""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


DEFAULT_DOC = Path("docs/MANUAL_REVIEW_QUEUE.md")
DEFAULT_REVIEW_SUMMARY = Path("reports/all_codes_followup_review/review_summary.csv")
DEFAULT_PATH_SUMMARY = Path("reports/all_codes_followup_letter_paths/path_summary.csv")
DEFAULT_LETTER_PATHS = Path("reports/all_codes_followup_letter_paths/letter_paths.csv")

REQUIRED_PHRASES = (
    "Status: navigation aid, not a claim report.",
    "Rows stay in review status unless a future locked",
    "Review candidates are not public claims.",
    "Any upgrade requires a new locked prospective design",
)

REQUIRED_EVIDENCE_PATHS = (
    Path("docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md"),
    Path("docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md"),
    Path("docs/CENTERED_OCCURRENCE_INDEX.md"),
    Path("docs/CRD_CENTER_WORD_SELF_VS_CONCEPT_FINDINGS.md"),
    Path("docs/ALL_CODES_FOLLOWUP_REVIEW.md"),
)

REQUIRED_ROW_FAMILIES = (
    "four-source follow-up",
    "compound extension",
    "centered on open Gog",
    "referent discipline",
    "background-pressure cautions",
)


@dataclass(frozen=True)
class ReviewPacketPaths:
    review_summary: Path = DEFAULT_REVIEW_SUMMARY
    path_summary: Path = DEFAULT_PATH_SUMMARY
    letter_paths: Path = DEFAULT_LETTER_PATHS


@dataclass(frozen=True)
class ReviewPacketShape:
    selected_review_rows: int
    path_summary_rows: int
    letter_rows: int
    path_mismatch_rows: int
    same_skip_extension_rows: int
    compound_same_skip_extension_rows: int

    def expected_doc_lines(self) -> tuple[str, ...]:
        return (
            f"{self.selected_review_rows:,} selected review rows.",
            f"{self.path_summary_rows:,} path-summary rows.",
            f"{self.letter_rows:,} letter rows.",
            f"{self.path_mismatch_rows:,} path mismatches.",
            f"{self.same_skip_extension_rows:,} rows with same-skip extensions.",
            (
                f"{self.compound_same_skip_extension_rows:,} rows with compound "
                "same-skip extensions."
            ),
        )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_manual_review_queue(args.doc)
    if failures:
        for failure in failures:
            print(f"manual review queue failure: {failure}", file=sys.stderr)
        return 1
    print(f"manual review queue ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_manual_review_queue(doc: Path) -> list[str]:
    if not doc.exists():
        return [f"{doc} is missing"]
    text = doc.read_text(encoding="utf-8")
    failures: list[str] = []
    for phrase in REQUIRED_PHRASES:
        if phrase not in text:
            failures.append(f"{doc} missing guard phrase: {phrase}")
    for family in REQUIRED_ROW_FAMILIES:
        if family not in text:
            failures.append(f"{doc} missing row family: {family}")
    for evidence_path in REQUIRED_EVIDENCE_PATHS:
        if not evidence_path.exists():
            failures.append(f"evidence path missing: {evidence_path}")
        if f"`{evidence_path}`" not in text:
            failures.append(f"{doc} missing evidence link: {evidence_path}")
    shape, shape_failures = load_review_packet_shape(ReviewPacketPaths())
    failures.extend(shape_failures)
    if shape is not None:
        for expected_line in shape.expected_doc_lines():
            if expected_line not in text:
                failures.append(f"{doc} missing packet-shape line: {expected_line}")
    return failures


def load_review_packet_shape(
    paths: ReviewPacketPaths,
) -> tuple[ReviewPacketShape | None, list[str]]:
    failures = _missing_packet_paths(paths)
    if failures:
        return None, failures

    review_rows = _read_csv_rows(paths.review_summary)
    path_rows = _read_csv_rows(paths.path_summary)
    letter_rows = _read_csv_rows(paths.letter_paths)

    try:
        review_path_total = _sum_int_field(review_rows, "path_rows", paths.review_summary)
        review_letter_total = _sum_int_field(
            review_rows, "letter_rows", paths.review_summary
        )
        review_mismatch_total = _sum_int_field(
            review_rows, "path_mismatch_rows", paths.review_summary
        )
        review_extension_rows = sum(
            1
            for row in review_rows
            if _int_field(row, "extension_rows", paths.review_summary) > 0
        )
    except ValueError as exc:
        failures.append(str(exc))
        return None, failures
    review_compound_rows = sum(
        1 for row in review_rows if row.get("compound_extension", "").casefold() == "true"
    )

    if review_path_total != len(path_rows):
        failures.append(
            "review_summary path_rows total "
            f"{review_path_total} != path_summary rows {len(path_rows)}"
        )
    if review_letter_total != len(letter_rows):
        failures.append(
            "review_summary letter_rows total "
            f"{review_letter_total} != letter_paths rows {len(letter_rows)}"
        )

    return (
        ReviewPacketShape(
            selected_review_rows=len(review_rows),
            path_summary_rows=len(path_rows),
            letter_rows=len(letter_rows),
            path_mismatch_rows=review_mismatch_total,
            same_skip_extension_rows=review_extension_rows,
            compound_same_skip_extension_rows=review_compound_rows,
        ),
        failures,
    )


def _missing_packet_paths(paths: ReviewPacketPaths) -> list[str]:
    return [
        f"review packet source missing: {path}"
        for path in (paths.review_summary, paths.path_summary, paths.letter_paths)
        if not path.exists()
    ]


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _sum_int_field(rows: list[dict[str, str]], field: str, path: Path) -> int:
    return sum(_int_field(row, field, path) for row in rows)


def _int_field(row: dict[str, str], field: str, path: Path) -> int:
    value = row.get(field)
    if value is None:
        raise ValueError(f"{path} missing required field {field}")
    return int(value)


if __name__ == "__main__":
    raise SystemExit(main())
