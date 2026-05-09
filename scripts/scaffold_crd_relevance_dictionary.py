#!/usr/bin/env python3
"""Scaffold blank CRD relevance dictionary entries from term CSV files."""

from __future__ import annotations

import argparse
import csv
from datetime import UTC, datetime
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = read_terms(args.term_file)
    concept_surface_keywords = surface_keywords_by_concept(rows) if args.seed_concept_terms else {}
    write_dictionary(
        args.out,
        rows,
        locked_by=args.locked_by,
        reviewer=args.reviewer,
        drafted_with=args.drafted_with,
        seed_surface_term=args.seed_surface_term,
        concept_surface_keywords=concept_surface_keywords,
    )
    write_queue(
        args.queue_out,
        rows,
        seed_surface_term=args.seed_surface_term,
        concept_surface_keywords=concept_surface_keywords,
    )
    print(args.out)
    print(args.queue_out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--term-file", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, default=Path("reports/crd/relevance_dictionary_draft.toml"))
    parser.add_argument("--queue-out", type=Path, default=Path("reports/crd/relevance_review_queue.csv"))
    parser.add_argument("--locked-by", default="TEMPLATE")
    parser.add_argument("--reviewer", default="TEMPLATE")
    parser.add_argument("--drafted-with", default="human")
    parser.add_argument(
        "--seed-surface-term",
        action="store_true",
        help="Seed each entry's surface keyword review field with the term's own surface form.",
    )
    parser.add_argument(
        "--seed-concept-terms",
        action="store_true",
        help="Seed each entry with all surface forms sharing the same normalized language+concept.",
    )
    return parser


def read_terms(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in paths:
        with path.open("r", encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                term_id = row.get("term_id", "").strip()
                if not term_id or term_id in seen:
                    continue
                seen.add(term_id)
                rows.append(
                    {
                        "source_file": str(path),
                        "term_id": term_id,
                        "concept": row.get("concept", "").strip(),
                        "category": row.get("category", "").strip(),
                        "language": row.get("language", "").strip(),
                        "term": row.get("term", "").strip(),
                        "notes": row.get("notes", "").strip(),
                    }
                )
    return rows


def write_dictionary(
    path: Path,
    rows: list[dict[str, str]],
    *,
    locked_by: str,
    reviewer: str,
    drafted_with: str,
    seed_surface_term: bool = False,
    concept_surface_keywords: dict[tuple[str, str], list[str]] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    today = datetime.now(UTC).date().isoformat()
    lines = [
        "[metadata]",
        'schema_version = "1"',
        f'locked_by = "{toml_escape(locked_by)}"',
        f'locked_at = "{today}"',
        'sha256 = "TEMPLATE_REPLACE_WITH_FILE_SHA256_AFTER_LOCK"',
        f'drafted_with = "{toml_escape(drafted_with)}"',
        "",
    ]
    for row in rows:
        surface_keywords = seeded_keywords(row, seed_surface_term, concept_surface_keywords)
        lines.extend(
            [
                "[[entries]]",
                f'term_id = "{toml_escape(row["term_id"])}"',
                f"surface_keywords = {toml_list(surface_keywords)}",
                "concept_codes = []",
                "verse_refs = []",
                "book_scope = []",
                "",
                "[entries.provenance]",
                f'author = "{toml_escape(locked_by)}"',
                f'lock_date = "{today}"',
                f'reviewer = "{toml_escape(reviewer)}"',
                (
                    'notes = "Blank scaffold from '
                    f'{toml_escape(row["source_file"])}; reviewer or locked drafting process must populate or explicitly leave empty."'
                ),
                "",
            ]
        )
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_queue(
    path: Path,
    rows: list[dict[str, str]],
    *,
    seed_surface_term: bool = False,
    concept_surface_keywords: dict[tuple[str, str], list[str]] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "review_rank",
        "source_file",
        "term_id",
        "concept",
        "category",
        "language",
        "term",
        "notes",
        "surface_keywords_reviewed",
        "concept_codes_reviewed",
        "verse_refs_reviewed",
        "book_scope_reviewed",
        "reviewer",
        "review_notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(rows, start=1):
            surface_keywords = seeded_keywords(row, seed_surface_term, concept_surface_keywords)
            writer.writerow(
                {
                    **row,
                    "review_rank": index,
                    "surface_keywords_reviewed": ";".join(surface_keywords),
                    "concept_codes_reviewed": "",
                    "verse_refs_reviewed": "",
                    "book_scope_reviewed": "",
                    "reviewer": "",
                    "review_notes": "",
                }
            )


def seeded_keywords(
    row: dict[str, str],
    seed_surface_term: bool,
    concept_surface_keywords: dict[tuple[str, str], list[str]] | None,
) -> list[str]:
    values: list[str] = []
    if seed_surface_term:
        values.extend(seed_surface_keywords(row))
    if concept_surface_keywords:
        values.extend(concept_surface_keywords.get(concept_key(row), []))
    return unique_values(values)


def seed_surface_keywords(row: dict[str, str]) -> list[str]:
    term = row.get("term", "").strip()
    if not term:
        return []
    values: list[str] = []
    for part in term.replace("|", "/").replace(";", "/").split("/"):
        value = part.strip()
        values.append(value)
    return unique_values(values)


def surface_keywords_by_concept(rows: list[dict[str, str]]) -> dict[tuple[str, str], list[str]]:
    grouped: dict[tuple[str, str], list[str]] = {}
    for row in rows:
        key = concept_key(row)
        if not all(key):
            continue
        grouped.setdefault(key, []).extend(seed_surface_keywords(row))
    return {key: unique_values(values) for key, values in grouped.items()}


def concept_key(row: dict[str, str]) -> tuple[str, str]:
    return (row.get("language", "").strip().lower(), row.get("concept", "").strip().casefold())


def unique_values(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        if value and value not in out:
            out.append(value)
    return out


def toml_list(values: list[str]) -> str:
    return "[" + ", ".join(f'"{toml_escape(value)}"' for value in values) + "]"


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


if __name__ == "__main__":
    raise SystemExit(main())
