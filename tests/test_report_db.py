from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import pytest

from scripts.build_report_db import main as build_report_db_main
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
    assert (
        report_table_name_for_path(Path("reports/external_claim_source_all_codes/surface_all_codes.csv"))
        == "external_claim_source_surface_all_codes"
    )


def test_report_table_name_for_matrix_and_gap_paths() -> None:
    assert report_table_name_for_path(Path("reports/matrix_clusters/candidates.csv")) == "matrix_cluster_candidates"
    assert (
        report_table_name_for_path(Path("reports/matrix_clusters/relation_control_summary.csv"))
        == "matrix_cluster_relation_control_summary"
    )
    assert (
        report_table_name_for_path(Path("reports/notable_passage_gaps/cross_source_gap_summary.csv"))
        == "notable_passage_gap_cross_source_summary"
    )
    assert (
        report_table_name_for_path(Path("reports/thematic_chapter_absence/cross_source_gap_summary.csv"))
        == "thematic_chapter_absence_cross_source_summary"
    )


def test_report_table_name_for_expanded_strata_paths() -> None:
    assert (
        report_table_name_for_path(Path("reports/match_strata_index/occurrence_strata.csv"))
        == "match_strata_occurrence_strata"
    )
    assert report_table_name_for_path(Path("reports/match_strata_index/strata_summary.csv")) == "match_strata_summary"
    assert report_table_name_for_path(Path("reports/boundary_alignment/summary.csv")) == "boundary_alignment_summary"
    assert (
        report_table_name_for_path(Path("reports/chapter_position_bias/summary.csv"))
        == "chapter_position_bias_summary"
    )
    assert report_table_name_for_path(Path("reports/direction_asymmetry/summary.csv")) == "direction_asymmetry_summary"
    assert (
        report_table_name_for_path(Path("reports/direction_asymmetry/term_summary.csv"))
        == "direction_asymmetry_term_summary"
    )
    assert report_table_name_for_path(Path("reports/canonical_first_summary/summary.csv")) == "canonical_first_summary"
    assert (
        report_table_name_for_path(Path("reports/canonical_first_summary/first_occurrences.csv"))
        == "canonical_first_occurrences"
    )
    assert report_table_name_for_path(Path("reports/cross_skip_summary/summary.csv")) == "cross_skip_summary"
    assert report_table_name_for_path(Path("reports/cross_skip_summary/candidate_rows.csv")) == "cross_skip_candidate_rows"
    assert report_table_name_for_path(Path("reports/review_flag_summary/summary.csv")) == "review_flag_summary"
    assert report_table_name_for_path(Path("reports/review_flag_summary/flag_rows.csv")) == "review_flag_rows"
    assert (
        report_table_name_for_path(Path("reports/cohort_cluster_density/windows.csv"))
        == "cohort_cluster_density_windows"
    )
    assert (
        report_table_name_for_path(Path("reports/cohort_cluster_density/summary.csv"))
        == "cohort_cluster_density_summary"
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


def test_build_report_db_writes_stable_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    csv_path = tmp_path / "reports" / "english_screening_all_codes" / "surface_all_codes.csv"
    csv_path.parent.mkdir(parents=True)
    write_rows(csv_path, [{"term_id": "tree", "hit_id": "1"}])
    db = tmp_path / "reports" / "db" / "open_bible_codes.duckdb"
    manifest = tmp_path / "reports" / "db" / "open_bible_codes.manifest.json"
    monkeypatch.chdir(tmp_path)

    args = [
        "--db",
        str(db),
        "--no-defaults",
        "--table",
        "reports/english_screening_all_codes/surface_all_codes.csv",
        "--manifest-out",
        str(manifest),
    ]
    assert build_report_db_main(args) == 0
    first_payload = json.loads(manifest.read_text(encoding="utf-8"))
    first_mtime_ns = manifest.stat().st_mtime_ns

    time.sleep(0.01)
    assert build_report_db_main(args) == 0
    second_payload = json.loads(manifest.read_text(encoding="utf-8"))

    assert first_payload == second_payload
    assert manifest.stat().st_mtime_ns == first_mtime_ns
    assert first_payload["table_count"] == 1
    assert first_payload["tables"][0]["table_name"] == "english_screening_surface_all_codes"
    assert first_payload["tables"][0]["row_count"] == 1


def test_sanitize_table_name_prefixes_digit() -> None:
    assert sanitize_table_name("123 hits!") == "t_123_hits"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
