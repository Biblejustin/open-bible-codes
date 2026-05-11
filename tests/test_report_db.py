from __future__ import annotations

import csv
from pathlib import Path

import pytest

from els.report_db import (
    ReportDBStale,
    default_table_name,
    fetch_dicts,
    import_csv_table,
    report_table_name_for_path,
    sanitize_table_name,
    verify_table_current,
)


duckdb = pytest.importorskip("duckdb")


def test_import_csv_table_and_query(tmp_path: Path) -> None:
    csv_path = tmp_path / "reports" / "crd" / "classified_hits.csv"
    csv_path.parent.mkdir(parents=True)
    write_rows(
        csv_path,
        [
            {"hit_id": "1", "term_id": "term", "is_relevant": "true"},
            {"hit_id": "2", "term_id": "term", "is_relevant": "false"},
        ],
    )
    db = tmp_path / "reports" / "db" / "open_bible_codes.duckdb"

    result = import_csv_table(db_path=db, csv_path=csv_path, table_name="hits")
    rows = fetch_dicts(db_path=db, query="SELECT hit_id FROM hits WHERE is_relevant = 'true'")

    assert result.row_count == 2
    assert rows == [{"hit_id": "1"}]
    verify_table_current(db_path=db, table_name="hits", source_path=csv_path)


def test_verify_table_current_rejects_stale_source(tmp_path: Path) -> None:
    csv_path = tmp_path / "hits.csv"
    write_rows(csv_path, [{"hit_id": "1", "term_id": "term"}])
    db = tmp_path / "reports" / "db" / "open_bible_codes.duckdb"
    import_csv_table(db_path=db, csv_path=csv_path, table_name="hits")
    write_rows(csv_path, [{"hit_id": "1", "term_id": "term"}, {"hit_id": "2", "term_id": "term"}])

    with pytest.raises(ReportDBStale):
        verify_table_current(db_path=db, table_name="hits", source_path=csv_path)


def test_default_table_name_uses_report_path() -> None:
    assert default_table_name(Path("reports/crd_self_surface/classified_hits.csv")) == "crd_self_surface_classified_hits"


def test_report_table_name_for_count_paths() -> None:
    assert report_table_name_for_path(Path("reports/word_counts_by_verse.csv")) == "word_counts_by_verse"
    assert report_table_name_for_path(Path("reports/morph_counts_by_lemma.csv")) == "morph_counts_by_lemma"


def test_report_table_name_for_mapped_all_codes_path() -> None:
    assert (
        report_table_name_for_path(Path("reports/hebrew_screening_all_codes/surface_all_codes.csv"))
        == "hebrew_screening_surface_all_codes"
    )


def test_import_csv_table_uses_report_table_mapping_by_default(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    csv_path = tmp_path / "reports" / "hebrew_screening_all_codes" / "surface_all_codes.csv"
    csv_path.parent.mkdir(parents=True)
    write_rows(csv_path, [{"term_id": "yhwh", "hit_id": "1"}])
    db = tmp_path / "reports" / "db" / "open_bible_codes.duckdb"

    monkeypatch.chdir(tmp_path)
    result = import_csv_table(db_path=db, csv_path=Path("reports/hebrew_screening_all_codes/surface_all_codes.csv"))

    assert result.table_name == "hebrew_screening_surface_all_codes"
    assert fetch_dicts(db_path=db, query="SELECT hit_id FROM hebrew_screening_surface_all_codes") == [{"hit_id": "1"}]


def test_sanitize_table_name_prefixes_digit() -> None:
    assert sanitize_table_name("123 hits!") == "t_123_hits"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
