#!/usr/bin/env python3
"""Build a compact CRD review queue from density and classified-hit outputs."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from els.report_db import fetch_dicts, quote_identifier, report_table_name_for_path, sanitize_table_name, verify_table_current


OUTPUT_FIELDNAMES = [
    "selection_reason",
    "selection_rank",
    "term_id",
    "term",
    "concept",
    "language",
    "category",
    "corpus",
    "bible_max_corpus",
    "bible_max_density",
    "secular_max_corpus",
    "secular_max_density",
    "ratio",
    "hit_id",
    "relevance_type",
    "surface_match_scope",
    "matched_surface_keyword",
    "matched_normalized_surface_keyword",
    "skip",
    "direction",
    "start_ref",
    "center_ref",
    "end_ref",
    "center_word",
    "center_normalized_word",
    "center_verse_text",
    "span_text",
]


@dataclass(frozen=True)
class SelectedTerm:
    term_id: str
    reason: str
    rank: int
    bible_max_corpus: str
    bible_max_density: str
    secular_max_corpus: str
    secular_max_density: str
    ratio: str


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    selected_terms = select_terms(
        args.summary,
        top_finite=args.top_finite,
        top_zero=args.top_zero,
    )
    written = build_review_queue(
        classified_hits=args.classified_hits,
        output=args.output,
        selected_terms=selected_terms,
        examples_per_term=args.examples_per_term,
        all_bible_corpora=args.all_bible_corpora,
        db=args.db,
        table=args.table,
    )
    print(args.output)
    print(f"selected_terms={len(selected_terms)}")
    print(f"review_rows={written}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--classified-hits", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--top-finite", type=int, default=25)
    parser.add_argument("--top-zero", type=int, default=25)
    parser.add_argument("--examples-per-term", type=int, default=10)
    parser.add_argument(
        "--all-bible-corpora",
        action="store_true",
        help="Keep examples from all Bible corpora instead of only the term's max-density Bible corpus.",
    )
    parser.add_argument("--db", type=Path, help="Read classified hits from a DuckDB report database.")
    parser.add_argument("--table", help="DuckDB table name. Defaults to a name derived from --classified-hits.")
    return parser


def select_terms(summary_path: Path, *, top_finite: int, top_zero: int) -> dict[str, SelectedTerm]:
    rows = read_dicts(summary_path)
    finite_rows = [
        row
        for row in rows
        if row.get("exceeds_secular_max") == "true" and parse_float(row.get("ratio")) is not None
    ]
    finite_rows.sort(key=lambda row: parse_float(row.get("ratio")) or 0.0, reverse=True)

    zero_rows = [
        row
        for row in rows
        if parse_float(row.get("secular_max_density")) == 0.0
        and (parse_float(row.get("bible_max_density")) or 0.0) > 0.0
    ]
    zero_rows.sort(key=lambda row: parse_float(row.get("bible_max_density")) or 0.0, reverse=True)

    selected: dict[str, SelectedTerm] = {}
    add_selected(selected, finite_rows[:top_finite], reason="top_finite_ratio")
    add_selected(selected, zero_rows[:top_zero], reason="bible_positive_secular_zero")
    return selected


def add_selected(selected: dict[str, SelectedTerm], rows: list[dict[str, str]], *, reason: str) -> None:
    for index, row in enumerate(rows, start=1):
        term_id = row["term_id"]
        if term_id in selected:
            continue
        selected[term_id] = SelectedTerm(
            term_id=term_id,
            reason=reason,
            rank=index,
            bible_max_corpus=row["bible_max_corpus"],
            bible_max_density=row["bible_max_density"],
            secular_max_corpus=row["secular_max_corpus"],
            secular_max_density=row["secular_max_density"],
            ratio=row.get("ratio", ""),
        )


def build_review_queue(
    *,
    classified_hits: Path,
    output: Path,
    selected_terms: dict[str, SelectedTerm],
    examples_per_term: int,
    all_bible_corpora: bool,
    db: Path | None = None,
    table: str = "",
) -> int:
    table_name = table or report_table_name_for_path(classified_hits)
    if db is not None:
        verify_table_current(
            db_path=db,
            table_name=table_name,
            source_path=classified_hits,
        )
        return build_review_queue_db(
            db=db,
            table=table_name,
            output=output,
            selected_terms=selected_terms,
            examples_per_term=examples_per_term,
            all_bible_corpora=all_bible_corpora,
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    written_by_term: dict[str, int] = defaultdict(int)
    written = 0
    with classified_hits.open(newline="", encoding="utf-8") as input_file, output.open(
        "w", newline="", encoding="utf-8"
    ) as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDNAMES)
        writer.writeheader()
        for row in reader:
            selected = selected_terms.get(row.get("term_id", ""))
            if selected is None:
                continue
            if row.get("is_relevant") != "true" or row.get("corpus_class") != "bible":
                continue
            if not all_bible_corpora and row.get("corpus") != selected.bible_max_corpus:
                continue
            if written_by_term[selected.term_id] >= examples_per_term:
                continue
            writer.writerow(output_row(row, selected))
            written_by_term[selected.term_id] += 1
            written += 1
    return written


def build_review_queue_db(
    *,
    db: Path,
    table: str,
    output: Path,
    selected_terms: dict[str, SelectedTerm],
    examples_per_term: int,
    all_bible_corpora: bool,
) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    qtable = quote_identifier(sanitize_table_name(table))
    for selected in selected_terms.values():
        corpus_filter = "" if all_bible_corpora else f"AND corpus = '{sql_escape(selected.bible_max_corpus)}'"
        query = f"""
            SELECT *
            FROM {qtable}
            WHERE term_id = '{sql_escape(selected.term_id)}'
              AND is_relevant = 'true'
              AND corpus_class = 'bible'
              {corpus_filter}
            ORDER BY corpus, center_ref, abs(try_cast(skip AS INTEGER)), hit_id
            LIMIT {int(examples_per_term)}
        """
        for row in fetch_dicts(db_path=db, query=query):
            rows.append(output_row(row, selected))
    with output.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=OUTPUT_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def output_row(row: dict[str, str], selected: SelectedTerm) -> dict[str, str]:
    return {
        "selection_reason": selected.reason,
        "selection_rank": str(selected.rank),
        "term_id": selected.term_id,
        "term": row.get("term", ""),
        "concept": row.get("concept", ""),
        "language": row.get("language", ""),
        "category": row.get("category", ""),
        "corpus": row.get("corpus", ""),
        "bible_max_corpus": selected.bible_max_corpus,
        "bible_max_density": selected.bible_max_density,
        "secular_max_corpus": selected.secular_max_corpus,
        "secular_max_density": selected.secular_max_density,
        "ratio": selected.ratio,
        "hit_id": row.get("hit_id", ""),
        "relevance_type": row.get("relevance_type", ""),
        "surface_match_scope": row.get("surface_match_scope", ""),
        "matched_surface_keyword": row.get("matched_surface_keyword", ""),
        "matched_normalized_surface_keyword": row.get("matched_normalized_surface_keyword", ""),
        "skip": row.get("skip", ""),
        "direction": row.get("direction", ""),
        "start_ref": row.get("start_ref", ""),
        "center_ref": row.get("center_ref", ""),
        "end_ref": row.get("end_ref", ""),
        "center_word": row.get("center_word", ""),
        "center_normalized_word": row.get("center_normalized_word", ""),
        "center_verse_text": row.get("center_verse_text", ""),
        "span_text": row.get("span_text", ""),
    }


def read_dicts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_float(value: str | None) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def sql_escape(value: str) -> str:
    return value.replace("'", "''")


if __name__ == "__main__":
    raise SystemExit(main())
