#!/usr/bin/env python3
"""Validate study-mapping CSV schemas without interpreting content."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


MAPPINGS_DIR = Path("data/study/mappings")
LANGUAGES = {"hebrew", "greek", "english", "michigan"}
REF_RE = re.compile(r"^(?P<book>[1-3]?[A-Za-z]+) (?P<chapter>[0-9]+):(?P<verse>[0-9]+)$")


@dataclass(frozen=True)
class MappingSchema:
    filename: str
    required_columns: tuple[str, ...]
    required_values: tuple[str, ...]
    unique_column: str = "mapping_id"


SCHEMAS: tuple[MappingSchema, ...] = (
    MappingSchema(
        filename="thematic_chapters.csv",
        required_columns=(
            "mapping_id",
            "term_id",
            "concept",
            "language",
            "book",
            "chapter_start",
            "chapter_end",
            "notes",
            "locked_by",
            "locked_at",
        ),
        required_values=(
            "mapping_id",
            "term_id",
            "concept",
            "language",
            "book",
            "chapter_start",
            "chapter_end",
            "locked_by",
            "locked_at",
        ),
    ),
    MappingSchema(
        filename="author_book_mapping.csv",
        required_columns=(
            "mapping_id",
            "author_term_id",
            "author_name",
            "language",
            "book",
            "scope_start_ref",
            "scope_end_ref",
            "tradition",
            "notes",
            "locked_by",
            "locked_at",
        ),
        required_values=(
            "mapping_id",
            "author_term_id",
            "author_name",
            "language",
            "book",
            "scope_start_ref",
            "scope_end_ref",
            "tradition",
            "locked_by",
            "locked_at",
        ),
    ),
    MappingSchema(
        filename="protagonist_narrative_mapping.csv",
        required_columns=(
            "mapping_id",
            "protagonist_term_id",
            "protagonist_name",
            "language",
            "book",
            "scope_start_ref",
            "scope_end_ref",
            "notes",
            "locked_by",
            "locked_at",
        ),
        required_values=(
            "mapping_id",
            "protagonist_term_id",
            "protagonist_name",
            "language",
            "book",
            "scope_start_ref",
            "scope_end_ref",
            "locked_by",
            "locked_at",
        ),
    ),
    MappingSchema(
        filename="ot_in_nt_quotations.csv",
        required_columns=(
            "mapping_id",
            "ot_corpus",
            "ot_ref_start",
            "ot_ref_end",
            "nt_ref_start",
            "nt_ref_end",
            "anchor_text",
            "anchor_normalized",
            "relationship",
            "source",
            "notes",
            "locked_by",
            "locked_at",
        ),
        required_values=(
            "mapping_id",
            "ot_corpus",
            "ot_ref_start",
            "ot_ref_end",
            "nt_ref_start",
            "nt_ref_end",
            "anchor_text",
            "anchor_normalized",
            "relationship",
            "source",
            "locked_by",
            "locked_at",
        ),
    ),
    MappingSchema(
        filename="mt_lxx_semantic_divergence.csv",
        required_columns=(
            "mapping_id",
            "mt_ref",
            "lxx_ref",
            "mt_anchor_text",
            "lxx_anchor_text",
            "divergence_type",
            "source",
            "notes",
            "locked_by",
            "locked_at",
        ),
        required_values=(
            "mapping_id",
            "mt_ref",
            "lxx_ref",
            "mt_anchor_text",
            "lxx_anchor_text",
            "divergence_type",
            "source",
            "locked_by",
            "locked_at",
        ),
    ),
    MappingSchema(
        filename="hebrew_root_policy.csv",
        required_columns=(
            "mapping_id",
            "term_id",
            "concept",
            "language",
            "surface_form",
            "normalized_surface_form",
            "root",
            "root_scheme",
            "analyzer",
            "source",
            "notes",
            "locked_by",
            "locked_at",
        ),
        required_values=(
            "mapping_id",
            "term_id",
            "concept",
            "language",
            "surface_form",
            "normalized_surface_form",
            "root",
            "root_scheme",
            "analyzer",
            "source",
            "locked_by",
            "locked_at",
        ),
    ),
    MappingSchema(
        filename="wrr_manual_decision_records.csv",
        required_columns=(
            "decision_id",
            "register_decision_rank",
            "decision_lane",
            "review_state",
            "decision_target",
            "source_checklist",
            "decision_status",
            "selected_action",
            "evidence_citation",
            "evidence_summary",
            "locked_by",
            "locked_at",
            "notes",
        ),
        required_values=(
            "decision_id",
            "register_decision_rank",
            "decision_lane",
            "review_state",
            "decision_target",
            "source_checklist",
            "decision_status",
            "selected_action",
            "evidence_citation",
            "evidence_summary",
            "locked_by",
            "locked_at",
        ),
        unique_column="decision_id",
    ),
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_mapping_dir(args.mappings_dir, require_nonempty=args.require_nonempty)
    if failures:
        for failure in failures:
            print(f"study mapping schema failure: {failure}", file=sys.stderr)
        return 1
    print(f"study mapping schemas ok: {args.mappings_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mappings-dir", type=Path, default=MAPPINGS_DIR)
    parser.add_argument(
        "--require-nonempty",
        action="store_true",
        help="Require every mapping file to contain at least one declared row.",
    )
    return parser


def validate_mapping_dir(mappings_dir: Path, *, require_nonempty: bool = False) -> list[str]:
    failures: list[str] = []
    for schema in SCHEMAS:
        failures.extend(
            validate_mapping_file(
                mappings_dir / schema.filename,
                schema,
                require_nonempty=require_nonempty,
            )
        )
    return failures


def validate_mapping_file(
    path: Path,
    schema: MappingSchema,
    *,
    require_nonempty: bool = False,
) -> list[str]:
    failures: list[str] = []
    if not path.exists():
        return [f"{path} is missing"]

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = tuple(reader.fieldnames or ())
        missing = sorted(set(schema.required_columns) - set(fieldnames))
        if missing:
            return [f"{path} missing required columns: {', '.join(missing)}"]
        extra = [field for field in fieldnames if field not in schema.required_columns]
        if extra:
            return [f"{path} has unexpected columns: {', '.join(extra)}"]
        rows = list(reader)

    if require_nonempty and not rows:
        failures.append(f"{path} has no rows")
    seen_ids: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        failures.extend(validate_row(path, row_number, row, schema, seen_ids))
    return failures


def validate_row(
    path: Path,
    row_number: int,
    row: dict[str, str | None],
    schema: MappingSchema,
    seen_ids: set[str],
) -> list[str]:
    failures: list[str] = []
    if None in row:
        failures.append(f"{path}:{row_number} has extra unheadered columns")

    mapping_id = clean(row.get(schema.unique_column))
    if mapping_id:
        if mapping_id in seen_ids:
            failures.append(f"{path}:{row_number} duplicate {schema.unique_column}: {mapping_id}")
        seen_ids.add(mapping_id)

    for column in schema.required_values:
        if not clean(row.get(column)):
            failures.append(f"{path}:{row_number} missing value for {column}")

    language = clean(row.get("language"))
    if language and language not in LANGUAGES:
        failures.append(f"{path}:{row_number} unsupported language: {language}")

    chapter_start = clean(row.get("chapter_start"))
    chapter_end = clean(row.get("chapter_end"))
    if chapter_start or chapter_end:
        failures.extend(validate_chapter_range(path, row_number, chapter_start, chapter_end))
    book = clean(row.get("book"))
    scope_start_ref = clean(row.get("scope_start_ref"))
    scope_end_ref = clean(row.get("scope_end_ref"))
    if book and (scope_start_ref or scope_end_ref):
        failures.extend(
            validate_scope_ref_range(
                path,
                row_number,
                book,
                scope_start_ref,
                scope_end_ref,
            )
        )
    locked_at = clean(row.get("locked_at"))
    if locked_at:
        failures.extend(validate_iso_date(path, row_number, "locked_at", locked_at))
    return failures


def validate_chapter_range(
    path: Path,
    row_number: int,
    chapter_start: str,
    chapter_end: str,
) -> list[str]:
    try:
        start = int(chapter_start)
        end = int(chapter_end)
    except ValueError:
        return [f"{path}:{row_number} chapter_start/chapter_end must be integers"]
    if start < 1 or end < 1:
        return [f"{path}:{row_number} chapter_start/chapter_end must be positive"]
    if start > end:
        return [f"{path}:{row_number} chapter_start must be <= chapter_end"]
    return []


def clean(value: str | None) -> str:
    return (value or "").strip()


def validate_iso_date(path: Path, row_number: int, column: str, value: str) -> list[str]:
    try:
        date.fromisoformat(value)
    except ValueError:
        return [f"{path}:{row_number} {column} must be an ISO date"]
    return []


def validate_scope_ref_range(
    path: Path,
    row_number: int,
    book: str,
    scope_start_ref: str,
    scope_end_ref: str,
) -> list[str]:
    start = parse_ref(scope_start_ref)
    end = parse_ref(scope_end_ref)
    failures: list[str] = []
    if start is None:
        failures.append(f"{path}:{row_number} scope_start_ref must look like '<Book> <chapter>:<verse>'")
    if end is None:
        failures.append(f"{path}:{row_number} scope_end_ref must look like '<Book> <chapter>:<verse>'")
    if start is None or end is None:
        return failures
    start_book, start_chapter, start_verse = start
    end_book, end_chapter, end_verse = end
    if start_book != book:
        failures.append(f"{path}:{row_number} scope_start_ref book must match book: {book}")
    if end_book != book:
        failures.append(f"{path}:{row_number} scope_end_ref book must match book: {book}")
    if start_book == end_book and (start_chapter, start_verse) > (end_chapter, end_verse):
        failures.append(f"{path}:{row_number} scope_start_ref must be <= scope_end_ref")
    return failures


def parse_ref(value: str) -> tuple[str, int, int] | None:
    match = REF_RE.match(value)
    if not match:
        return None
    chapter = int(match.group("chapter"))
    verse = int(match.group("verse"))
    if chapter < 1 or verse < 1:
        return None
    return match.group("book"), chapter, verse


if __name__ == "__main__":
    raise SystemExit(main())
