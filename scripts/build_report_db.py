#!/usr/bin/env python3
"""Import large report CSV artifacts into a DuckDB report database."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from els.report_db import default_table_name, import_csv_table, sanitize_table_name


DEFAULT_DB = Path("reports/db/open_bible_codes.duckdb")


@dataclass(frozen=True)
class DefaultReportTable:
    path: Path
    table_name: str


DEFAULT_REPORT_TABLES = [
    DefaultReportTable(Path("reports/crd_self_surface/classified_hits.csv"), "crd_self_surface_classified_hits"),
    DefaultReportTable(Path("reports/crd_self_surface/density_matrix.csv"), "crd_self_surface_density_matrix"),
    DefaultReportTable(Path("reports/crd_concept_surface/classified_hits.csv"), "crd_concept_surface_classified_hits"),
    DefaultReportTable(Path("reports/crd_concept_surface/density_matrix.csv"), "crd_concept_surface_density_matrix"),
    DefaultReportTable(Path("reports/crd/classified_hits.csv"), "crd_classified_hits"),
    DefaultReportTable(Path("reports/crd/density_matrix.csv"), "crd_density_matrix"),
    DefaultReportTable(Path("reports/hebrew_screening_all_codes/surface_all_codes.csv"), "hebrew_screening_surface_all_codes"),
    DefaultReportTable(
        Path("reports/hebrew_screening_all_codes/surface_all_codes_summary.csv"),
        "hebrew_screening_surface_all_codes_summary",
    ),
    DefaultReportTable(Path("reports/english_screening_all_codes/surface_all_codes.csv"), "english_screening_surface_all_codes"),
    DefaultReportTable(
        Path("reports/english_screening_all_codes/surface_all_codes_summary.csv"),
        "english_screening_surface_all_codes_summary",
    ),
    DefaultReportTable(Path("reports/greek_screening_all_codes/surface_all_codes.csv"), "greek_screening_surface_all_codes"),
    DefaultReportTable(
        Path("reports/greek_screening_all_codes/surface_all_codes_summary.csv"),
        "greek_screening_surface_all_codes_summary",
    ),
    DefaultReportTable(Path("reports/hebrew_theology_all_codes/surface_all_codes.csv"), "hebrew_theology_surface_all_codes"),
    DefaultReportTable(
        Path("reports/hebrew_theology_all_codes/surface_all_codes_summary.csv"),
        "hebrew_theology_surface_all_codes_summary",
    ),
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    specs = list(DEFAULT_REPORT_TABLES) if not args.no_defaults else []
    specs.extend(parse_table_specs(args.table))
    imported = 0
    skipped = 0
    for spec in specs:
        if not spec.path.exists():
            if args.skip_missing:
                skipped += 1
                print(f"skip missing {spec.path}")
                continue
            raise FileNotFoundError(spec.path)
        result = import_csv_table(
            db_path=args.db,
            csv_path=spec.path,
            table_name=spec.table_name,
            replace=not args.no_replace,
        )
        imported += 1
        print(f"{result.table_name}\trows={result.row_count}\tsize={result.source_size_bytes}\tsource={result.source_path}")
    print(f"db={args.db}")
    print(f"imported={imported}")
    print(f"skipped={skipped}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument(
        "--table",
        action="append",
        default=[],
        metavar="CSV_PATH[:TABLE_NAME]",
        help="Additional CSV to import. If TABLE_NAME is omitted, a report-derived name is used.",
    )
    parser.add_argument("--no-defaults", action="store_true", help="Only import explicitly provided --table entries.")
    parser.add_argument("--no-replace", action="store_true", help="Fail if a target table already exists.")
    parser.add_argument("--skip-missing", action="store_true")
    return parser


def parse_table_specs(values: list[str]) -> list[DefaultReportTable]:
    specs: list[DefaultReportTable] = []
    for value in values:
        if ":" in value:
            path_text, table_text = value.rsplit(":", 1)
            table_name = sanitize_table_name(table_text)
        else:
            path_text = value
            table_name = default_table_name(Path(path_text))
        specs.append(DefaultReportTable(Path(path_text), table_name))
    return specs


if __name__ == "__main__":
    raise SystemExit(main())
