#!/usr/bin/env python3
"""Filter CRD classified-hit rows into a smaller review artifact."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from els.report_db import (
    export_query_to_csv,
    quote_identifier,
    report_table_name_for_path,
    sanitize_table_name,
    verify_table_current,
    where_clause,
)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    count = filter_rows(
        classified_hits=args.classified_hits,
        output=args.output,
        corpus_class=args.corpus_class,
        is_relevant=args.is_relevant,
        surface_match_scope=args.surface_match_scope,
        db=args.db,
        table=args.table,
    )
    print(args.output)
    print(f"rows={count}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--classified-hits", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--corpus-class", default="")
    parser.add_argument("--is-relevant", choices=["true", "false", ""], default="")
    parser.add_argument("--surface-match-scope", default="")
    parser.add_argument("--db", type=Path, help="Read classified hits from a DuckDB report database.")
    parser.add_argument("--table", help="DuckDB table name. Defaults to a name derived from --classified-hits.")
    return parser


def filter_rows(
    *,
    classified_hits: Path,
    output: Path,
    corpus_class: str = "",
    is_relevant: str = "",
    surface_match_scope: str = "",
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
        return filter_rows_db(
            db=db,
            table=table_name,
            output=output,
            corpus_class=corpus_class,
            is_relevant=is_relevant,
            surface_match_scope=surface_match_scope,
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with classified_hits.open(newline="", encoding="utf-8") as input_file, output.open(
        "w", newline="", encoding="utf-8"
    ) as output_file:
        reader = csv.DictReader(input_file)
        if reader.fieldnames is None:
            raise ValueError("classified hits file is missing a header")
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if corpus_class and row.get("corpus_class") != corpus_class:
                continue
            if is_relevant and row.get("is_relevant") != is_relevant:
                continue
            if surface_match_scope and row.get("surface_match_scope") != surface_match_scope:
                continue
            writer.writerow(row)
            count += 1
    return count


def filter_rows_db(
    *,
    db: Path,
    table: str,
    output: Path,
    corpus_class: str = "",
    is_relevant: str = "",
    surface_match_scope: str = "",
) -> int:
    qtable = quote_identifier(sanitize_table_name(table))
    query = (
        f"SELECT * FROM {qtable}"
        + where_clause(
            [
                ("corpus_class", corpus_class),
                ("is_relevant", is_relevant),
                ("surface_match_scope", surface_match_scope),
            ]
        )
    )
    return export_query_to_csv(db_path=db, query=query, output=output)


if __name__ == "__main__":
    raise SystemExit(main())
