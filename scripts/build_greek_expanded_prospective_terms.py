#!/usr/bin/env python3
"""Build a frozen expanded Greek exact-center prospective term list."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from els.normalization import normalize_text


TERMS_DIR = Path("terms")
EXISTING_COHORT = TERMS_DIR / "greek_exact_center_cohort_terms.csv"
OUTPUT = TERMS_DIR / "greek_expanded_prospective_terms.csv"
SOURCE_FILES = (
    "theological_terms.csv",
    "greek_nt_claim_terms.csv",
    "prophetic_terms.csv",
    "biblical_festivals.csv",
    "biblical_tribes.csv",
    "table_of_nations.csv",
)
FIELDNAMES = ["term_id", "concept", "category", "language", "term", "notes"]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    rows = build_rows(args.terms_dir, min_length=args.min_length)
    write_rows(args.out, rows)
    print(args.out)
    print(f"rows={len(rows)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms-dir", type=Path, default=TERMS_DIR)
    parser.add_argument("--out", type=Path, default=OUTPUT)
    parser.add_argument("--min-length", type=int, default=4)
    return parser


def build_rows(terms_dir: Path, *, min_length: int) -> list[dict[str, str]]:
    existing = existing_normalized_terms(terms_dir / EXISTING_COHORT.name)
    seen_normalized = set(existing)
    used_ids: set[str] = set()
    output: list[dict[str, str]] = []
    for source_name in SOURCE_FILES:
        source_path = terms_dir / source_name
        for row in read_rows(source_path):
            if row.get("language") != "greek":
                continue
            normalized = normalize_text(row["term"], "greek")
            if len(normalized) < min_length:
                continue
            if normalized in seen_normalized:
                continue
            seen_normalized.add(normalized)
            term_id = unique_term_id("gpx_" + row["term_id"], used_ids)
            output.append(
                {
                    "term_id": term_id,
                    "concept": row["concept"],
                    "category": row["category"],
                    "language": "greek",
                    "term": row["term"],
                    "notes": notes_for_row(source_name, row),
                }
            )
    return output


def existing_normalized_terms(path: Path) -> set[str]:
    return {
        normalize_text(row["term"], row["language"])
        for row in read_rows(path)
        if row.get("language") == "greek"
    }


def unique_term_id(base: str, used: set[str]) -> str:
    candidate = base
    counter = 2
    while candidate in used:
        candidate = f"{base}_{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def notes_for_row(source_name: str, row: dict[str, str]) -> str:
    parts = [
        "prospective expanded Greek exact-center cohort",
        f"source={source_name}",
        f"original_id={row['term_id']}",
    ]
    original_notes = row.get("notes", "").strip()
    if original_notes:
        parts.append(original_notes)
    return "; ".join(parts)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    raise SystemExit(main())
