#!/usr/bin/env python3
"""Convert a reviewed CRD CSV queue into a relevance dictionary TOML file."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        rows = read_review_rows(args.queue)
        if args.require_reviewer:
            validate_reviewers(rows)
        write_dictionary(
            args.out,
            rows,
            locked_by=args.locked_by,
            reviewer=args.reviewer,
            drafted_with=args.drafted_with,
        )
    except ValueError as exc:
        print(f"CRD review apply failed: {exc}", file=sys.stderr)
        return 1
    print(args.out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=Path("reports/crd/relevance_review_queue.csv"))
    parser.add_argument("--out", type=Path, default=Path("reports/crd/relevance_dictionary_reviewed.toml"))
    parser.add_argument("--locked-by", default="TEMPLATE")
    parser.add_argument("--reviewer", default="TEMPLATE")
    parser.add_argument("--drafted-with", default="human")
    parser.add_argument("--require-reviewer", action="store_true")
    return parser


def read_review_rows(path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            term_id = row.get("term_id", "").strip()
            if not term_id:
                continue
            if term_id in seen:
                raise ValueError(f"duplicate term_id in review queue: {term_id}")
            seen.add(term_id)
            rows.append(
                {
                    "term_id": term_id,
                    "surface_keywords": split_review_values(row.get("surface_keywords_reviewed", "")),
                    "concept_codes": split_review_values(row.get("concept_codes_reviewed", "")),
                    "verse_refs": split_review_values(row.get("verse_refs_reviewed", "")),
                    "book_scope": split_review_values(row.get("book_scope_reviewed", "")),
                    "source_file": row.get("source_file", "").strip(),
                    "reviewer": row.get("reviewer", "").strip(),
                    "review_notes": row.get("review_notes", "").strip(),
                    "concept": row.get("concept", "").strip(),
                    "category": row.get("category", "").strip(),
                    "language": row.get("language", "").strip(),
                    "term": row.get("term", "").strip(),
                }
            )
    return rows


def split_review_values(value: str) -> list[str]:
    normalized = value.replace("\n", ";").replace("|", ";")
    return [part.strip() for part in normalized.split(";") if part.strip()]


def validate_reviewers(rows: list[dict[str, object]]) -> None:
    missing = [str(row["term_id"]) for row in rows if not str(row.get("reviewer", "")).strip()]
    if missing:
        raise ValueError(f"reviewer missing for term_ids: {', '.join(missing[:20])}")


def write_dictionary(
    path: Path,
    rows: list[dict[str, object]],
    *,
    locked_by: str,
    reviewer: str,
    drafted_with: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(UTC).date().isoformat()
    lines = [
        "[metadata]",
        'schema_version = "1"',
        f'locked_by = "{toml_escape(locked_by)}"',
        f'locked_at = "{today}"',
        'sha256 = "computed-after-generation"',
        f'drafted_with = "{toml_escape(drafted_with)}"',
        "",
    ]
    for row in rows:
        entry_reviewer = str(row.get("reviewer") or reviewer)
        notes = review_note(row)
        lines.extend(
            [
                "[[entries]]",
                f'term_id = "{toml_escape(str(row["term_id"]))}"',
                f"surface_keywords = {toml_list(row['surface_keywords'])}",
                f"concept_codes = {toml_list(row['concept_codes'])}",
                f"verse_refs = {toml_list(row['verse_refs'])}",
                f"book_scope = {toml_list(row['book_scope'])}",
                "",
                "[entries.provenance]",
                f'author = "{toml_escape(locked_by)}"',
                f'lock_date = "{today}"',
                f'reviewer = "{toml_escape(entry_reviewer)}"',
                f'notes = "{toml_escape(notes)}"',
                "",
            ]
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def review_note(row: dict[str, object]) -> str:
    pieces = [
        f"source={row.get('source_file', '')}",
        f"concept={row.get('concept', '')}",
        f"category={row.get('category', '')}",
        f"language={row.get('language', '')}",
        f"term={row.get('term', '')}",
    ]
    notes = str(row.get("review_notes", "")).strip()
    if notes:
        pieces.append(f"review_notes={notes}")
    return "; ".join(pieces)


def toml_list(values: object) -> str:
    if not isinstance(values, list):
        return "[]"
    return "[" + ", ".join(f'"{toml_escape(str(value))}"' for value in values) + "]"


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    raise SystemExit(main())
