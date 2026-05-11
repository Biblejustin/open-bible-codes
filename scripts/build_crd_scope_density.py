#!/usr/bin/env python3
"""Build CRD density summaries for one surface-match scope."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path

from els.report_db import fetch_dicts, quote_identifier, report_table_name_for_path, sanitize_table_name, verify_table_current


MATRIX_FIELDNAMES = [
    "classifier_mode",
    "term_id",
    "term",
    "concept",
    "category",
    "language",
    "corpus",
    "corpus_class",
    "surface_match_scope",
    "total_centered_hits",
    "scope_relevant_hits",
    "corpus_normalized_letters",
    "scope_density_per_million",
    "scope_relevance_rate",
]

SUMMARY_FIELDNAMES = [
    "classifier_mode",
    "term_id",
    "term",
    "language",
    "surface_match_scope",
    "bible_max_density",
    "bible_max_corpus",
    "secular_max_density",
    "secular_max_corpus",
    "ratio",
    "exceeds_secular_max",
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    table_name = args.table or report_table_name_for_path(args.classified_hits)
    if args.db is not None:
        verify_table_current(
            db_path=args.db,
            table_name=table_name,
            source_path=args.classified_hits,
        )
        counts = count_scope_hits_db(
            db=args.db,
            table=table_name,
            surface_match_scope=args.surface_match_scope,
        )
    else:
        counts = count_scope_hits(args.classified_hits, args.surface_match_scope)
    matrix_rows = build_matrix_rows(
        base_density_matrix=args.base_density_matrix,
        counts=counts,
        surface_match_scope=args.surface_match_scope,
    )
    summary_rows = build_summary_rows(matrix_rows)
    write_rows(args.matrix_out, MATRIX_FIELDNAMES, matrix_rows)
    write_rows(args.summary_out, SUMMARY_FIELDNAMES, summary_rows)
    print(args.matrix_out)
    print(args.summary_out)
    print(f"matrix_rows={len(matrix_rows)}")
    print(f"summary_rows={len(summary_rows)}")
    print(f"scope_hits={sum(counts.values())}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-density-matrix", type=Path, required=True)
    parser.add_argument("--classified-hits", type=Path, required=True)
    parser.add_argument("--surface-match-scope", required=True)
    parser.add_argument("--matrix-out", type=Path, required=True)
    parser.add_argument("--summary-out", type=Path, required=True)
    parser.add_argument("--db", type=Path, help="Read classified-hit counts from a DuckDB report database.")
    parser.add_argument("--table", help="DuckDB classified-hit table name. Defaults to a name derived from --classified-hits.")
    return parser


def count_scope_hits(classified_hits: Path, surface_match_scope: str) -> Counter[tuple[str, str, str]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    with classified_hits.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("is_relevant") != "true":
                continue
            if row.get("surface_match_scope") != surface_match_scope:
                continue
            key = (row["classifier_mode"], row["term_id"], row["corpus"])
            counts[key] += 1
    return counts


def count_scope_hits_db(
    *,
    db: Path,
    table: str,
    surface_match_scope: str,
) -> Counter[tuple[str, str, str]]:
    qtable = quote_identifier(sanitize_table_name(table))
    qscope = surface_match_scope.replace("'", "''")
    rows = fetch_dicts(
        db_path=db,
        query=f"""
            SELECT classifier_mode, term_id, corpus, count(*) AS scope_hits
            FROM {qtable}
            WHERE is_relevant = 'true'
              AND surface_match_scope = '{qscope}'
            GROUP BY classifier_mode, term_id, corpus
        """,
    )
    counts: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        counts[(row["classifier_mode"], row["term_id"], row["corpus"])] = int(row["scope_hits"])
    return counts


def build_matrix_rows(
    *,
    base_density_matrix: Path,
    counts: Counter[tuple[str, str, str]],
    surface_match_scope: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    with base_density_matrix.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            key = (row["classifier_mode"], row["term_id"], row["corpus"])
            scope_hits = counts[key]
            letters = int(row["corpus_normalized_letters"])
            total_hits = int(row["total_centered_hits"])
            rows.append(
                {
                    "classifier_mode": row["classifier_mode"],
                    "term_id": row["term_id"],
                    "term": row["term"],
                    "concept": row["concept"],
                    "category": row["category"],
                    "language": row["language"],
                    "corpus": row["corpus"],
                    "corpus_class": row["corpus_class"],
                    "surface_match_scope": surface_match_scope,
                    "total_centered_hits": row["total_centered_hits"],
                    "scope_relevant_hits": str(scope_hits),
                    "corpus_normalized_letters": row["corpus_normalized_letters"],
                    "scope_density_per_million": format_float(scope_hits * 1_000_000 / letters),
                    "scope_relevance_rate": format_float(scope_hits / total_hits if total_hits else 0.0),
                }
            )
    return rows


def build_summary_rows(matrix_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in matrix_rows:
        groups.setdefault((row["classifier_mode"], row["term_id"]), []).append(row)
    summaries: list[dict[str, str]] = []
    for (_mode, _term_id), rows in sorted(groups.items()):
        bible_rows = [row for row in rows if row["corpus_class"] == "bible"]
        secular_rows = [row for row in rows if row["corpus_class"] == "secular_control"]
        if not bible_rows or not secular_rows:
            continue
        bible_max = max(bible_rows, key=lambda row: float(row["scope_density_per_million"]))
        secular_max = max(secular_rows, key=lambda row: float(row["scope_density_per_million"]))
        bible_density = float(bible_max["scope_density_per_million"])
        secular_density = float(secular_max["scope_density_per_million"])
        ratio = "" if secular_density == 0.0 else format_float(bible_density / secular_density)
        summaries.append(
            {
                "classifier_mode": bible_max["classifier_mode"],
                "term_id": bible_max["term_id"],
                "term": bible_max["term"],
                "language": bible_max["language"],
                "surface_match_scope": bible_max["surface_match_scope"],
                "bible_max_density": bible_max["scope_density_per_million"],
                "bible_max_corpus": bible_max["corpus"],
                "secular_max_density": secular_max["scope_density_per_million"],
                "secular_max_corpus": secular_max["corpus"],
                "ratio": ratio,
                "exceeds_secular_max": str(bible_density > secular_density).lower(),
            }
        )
    return summaries


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def format_float(value: float) -> str:
    return f"{value:.9g}"


if __name__ == "__main__":
    raise SystemExit(main())
