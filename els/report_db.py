"""DuckDB helpers for large report artifacts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


class DuckDBUnavailable(RuntimeError):
    """Raised when a DuckDB-backed path is requested without duckdb installed."""


class ReportDBStale(RuntimeError):
    """Raised when a report DB table is missing or stale relative to its source CSV."""


@dataclass(frozen=True)
class TableImportResult:
    table_name: str
    source_path: Path
    source_size_bytes: int
    row_count: int


def require_duckdb() -> Any:
    try:
        import duckdb
    except ImportError as exc:
        raise DuckDBUnavailable(
            "DuckDB support requires the optional analytics dependency. "
            "Install with `python3 -m pip install --user --break-system-packages duckdb` "
            "or `python3 -m pip install '.[analytics]'` inside a virtual environment."
        ) from exc
    return duckdb


def connect(db_path: Path, *, read_only: bool = False) -> Any:
    duckdb = require_duckdb()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path), read_only=read_only)


def default_table_name(path: Path) -> str:
    parts = list(path.with_suffix("").parts)
    if "reports" in parts:
        parts = parts[parts.index("reports") + 1 :]
    name = "_".join(parts)
    return sanitize_table_name(name)


DEFAULT_REPORT_TABLE_NAMES = {
    "reports/crd_self_surface/classified_hits.csv": "crd_self_surface_classified_hits",
    "reports/crd_self_surface/density_matrix.csv": "crd_self_surface_density_matrix",
    "reports/crd_concept_surface/classified_hits.csv": "crd_concept_surface_classified_hits",
    "reports/crd_concept_surface/density_matrix.csv": "crd_concept_surface_density_matrix",
    "reports/crd/classified_hits.csv": "crd_classified_hits",
    "reports/crd/density_matrix.csv": "crd_density_matrix",
    "reports/hebrew_screening_all_codes/surface_all_codes.csv": "hebrew_screening_surface_all_codes",
    "reports/hebrew_screening_all_codes/surface_all_codes_summary.csv": "hebrew_screening_surface_all_codes_summary",
    "reports/english_screening_all_codes/surface_all_codes.csv": "english_screening_surface_all_codes",
    "reports/english_screening_all_codes/surface_all_codes_summary.csv": "english_screening_surface_all_codes_summary",
    "reports/greek_screening_all_codes/surface_all_codes.csv": "greek_screening_surface_all_codes",
    "reports/greek_screening_all_codes/surface_all_codes_summary.csv": "greek_screening_surface_all_codes_summary",
    "reports/hebrew_theology_all_codes/surface_all_codes.csv": "hebrew_theology_surface_all_codes",
    "reports/hebrew_theology_all_codes/surface_all_codes_summary.csv": "hebrew_theology_surface_all_codes_summary",
    "reports/external_claim_source_all_codes/surface_all_codes.csv": "external_claim_source_surface_all_codes",
    "reports/external_claim_source_all_codes/surface_all_codes_summary.csv": (
        "external_claim_source_surface_all_codes_summary"
    ),
    "reports/dynamic_skip_focus/full_span_exported_hits.csv": "dynamic_skip_focus_full_span_exported_hits",
    "reports/word_counts_by_word.csv": "word_counts_by_word",
    "reports/word_counts_by_book.csv": "word_counts_by_book",
    "reports/word_counts_by_chapter.csv": "word_counts_by_chapter",
    "reports/word_counts_by_verse.csv": "word_counts_by_verse",
    "reports/word_count_multiples.csv": "word_count_multiples",
    "reports/morph_counts_by_lemma.csv": "morph_counts_by_lemma",
    "reports/morph_counts_by_book.csv": "morph_counts_by_book",
    "reports/morph_counts_by_chapter.csv": "morph_counts_by_chapter",
    "reports/morph_counts_by_verse.csv": "morph_counts_by_verse",
    "reports/morph_count_multiples.csv": "morph_count_multiples",
}


def report_table_name_for_path(path: Path) -> str:
    candidates = [path.as_posix()]
    try:
        candidates.append(path.resolve().relative_to(Path.cwd().resolve()).as_posix())
    except ValueError:
        pass
    for candidate in candidates:
        if candidate in DEFAULT_REPORT_TABLE_NAMES:
            return DEFAULT_REPORT_TABLE_NAMES[candidate]
    return default_table_name(path)


def sanitize_table_name(value: str) -> str:
    name = re.sub(r"[^0-9A-Za-z_]+", "_", value).strip("_").lower()
    if not name:
        raise ValueError("table name cannot be empty")
    if name[0].isdigit():
        name = f"t_{name}"
    return name


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def sql_literal(value: str | Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def import_csv_table(
    *,
    db_path: Path,
    csv_path: Path,
    table_name: str | None = None,
    replace: bool = True,
) -> TableImportResult:
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)
    table = sanitize_table_name(table_name or report_table_name_for_path(csv_path))
    qtable = quote_identifier(table)
    create_mode = "OR REPLACE " if replace else ""
    source = sql_literal(csv_path)
    with connect(db_path) as con:
        con.execute(
            f"""
            CREATE {create_mode}TABLE {qtable} AS
            SELECT *
            FROM read_csv_auto(
                {source},
                header = true,
                delim = ',',
                quote = '"',
                escape = '"',
                all_varchar = true,
                sample_size = 20480
            )
            """
        )
        con.execute(f"ANALYZE {qtable}")
        row_count = int(con.execute(f"SELECT count(*) FROM {qtable}").fetchone()[0])
        record_table_import(con, table, csv_path, row_count)
    return TableImportResult(
        table_name=table,
        source_path=csv_path,
        source_size_bytes=csv_path.stat().st_size,
        row_count=row_count,
    )


def record_table_import(con: Any, table_name: str, source_path: Path, row_count: int) -> None:
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS report_table_imports (
            table_name VARCHAR,
            source_path VARCHAR,
            source_size_bytes BIGINT,
            source_mtime_ns BIGINT,
            imported_at_utc VARCHAR,
            row_count BIGINT
        )
        """
    )
    con.execute("DELETE FROM report_table_imports WHERE table_name = ?", [table_name])
    stat = source_path.stat()
    con.execute(
        """
        INSERT INTO report_table_imports
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            table_name,
            str(source_path),
            stat.st_size,
            stat.st_mtime_ns,
            datetime.now(UTC).isoformat(),
            row_count,
        ],
    )


def table_exists(db_path: Path, table_name: str) -> bool:
    table = sanitize_table_name(table_name)
    with connect(db_path, read_only=True) as con:
        rows = con.execute(
            "SELECT count(*) FROM information_schema.tables WHERE table_name = ?",
            [table],
        ).fetchone()
    return bool(rows and rows[0])


def verify_table_current(*, db_path: Path, table_name: str, source_path: Path) -> None:
    table = sanitize_table_name(table_name)
    if not source_path.exists():
        raise FileNotFoundError(source_path)
    if not db_path.exists():
        raise ReportDBStale(f"DuckDB database {db_path} does not exist; rebuild with `make report-db`")
    with connect(db_path, read_only=True) as con:
        metadata_table = con.execute(
            "SELECT count(*) FROM information_schema.tables WHERE table_name = 'report_table_imports'"
        ).fetchone()
        if not metadata_table or not metadata_table[0]:
            raise ReportDBStale("DuckDB import metadata table is missing; rebuild with `make report-db`")
        rows = con.execute(
            """
            SELECT source_size_bytes, source_mtime_ns
            FROM report_table_imports
            WHERE table_name = ?
            """,
            [table],
        ).fetchall()
    if not rows:
        raise ReportDBStale(f"DuckDB table {table!r} has no import metadata; rebuild with `make report-db`")
    source_size, source_mtime_ns = rows[0]
    stat = source_path.stat()
    if int(source_size) != stat.st_size or int(source_mtime_ns) != stat.st_mtime_ns:
        raise ReportDBStale(
            f"DuckDB table {table!r} is stale for {source_path}; rebuild with `make report-db`"
        )


def export_query_to_csv(*, db_path: Path, query: str, output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    with connect(db_path, read_only=True) as con:
        count = int(con.execute(f"SELECT count(*) FROM ({query}) AS export_count").fetchone()[0])
        con.execute(
            f"""
            COPY ({query})
            TO {sql_literal(output)}
            (HEADER, DELIMITER ',')
            """
        )
    return count


def fetch_dicts(*, db_path: Path, query: str) -> list[dict[str, str]]:
    with connect(db_path, read_only=True) as con:
        cursor = con.execute(query)
        columns = [description[0] for description in cursor.description]
        return [
            {column: "" if value is None else str(value) for column, value in zip(columns, row, strict=True)}
            for row in cursor.fetchall()
        ]


def where_clause(filters: Iterable[tuple[str, str]]) -> str:
    clauses = [f"{quote_identifier(column)} = {sql_literal(value)}" for column, value in filters if value]
    return " WHERE " + " AND ".join(clauses) if clauses else ""
