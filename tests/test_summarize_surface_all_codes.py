import csv
import json
from pathlib import Path

import pytest

from els.report_db import import_csv_table
from scripts import summarize_surface_all_codes as summarize


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def test_aggregate_counts_center_word_surface_flags() -> None:
    summary_rows = [
        {
            "corpus": "MT",
            "term_id": "t1",
            "concept": "Term",
            "category": "cat",
            "term": "אבגד",
            "normalized_term": "אבגד",
            "hit_count": "10",
            "context_hit_count": "4",
            "exact_center_word_hits": "1",
            "same_concept_center_word_hits": "2",
            "same_category_center_word_hits": "3",
            "exact_center_hits": "4",
            "same_concept_center_hits": "5",
            "same_category_center_hits": "6",
            "exact_span_hits": "7",
            "same_concept_span_hits": "8",
            "same_category_span_hits": "9",
        }
    ]
    hit_rows = [
        {"best_context": "exact_center"},
        {"best_context": ""},
    ]

    aggregates = summarize.aggregate(summary_rows, hit_rows)

    assert aggregates["total_hits"] == 10
    assert aggregates["center_word_exact_hits"] == 1
    assert aggregates["center_word_related_hits"] == 5
    assert aggregates["center_verse_related_hits"] == 11
    assert aggregates["span_context_hits"] == 24
    assert aggregates["context_counts"]["hidden_path_only"] == 1


def test_main_writes_markdown_and_manifest(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    summary = tmp_path / "summary.csv"
    md = tmp_path / "summary.md"
    manifest = tmp_path / "manifest.json"
    write_csv(
        hits,
        [
            {
                "best_context": "exact_center",
            }
        ],
    )
    write_csv(
        summary,
        [
            {
                "corpus": "MT",
                "term_id": "t1",
                "concept": "Term",
                "category": "cat",
                "term": "אבגד",
                "normalized_term": "אבגד",
                "hit_count": "10",
                "context_hit_count": "4",
                "exact_center_word_hits": "1",
                "same_concept_center_word_hits": "2",
                "same_category_center_word_hits": "0",
                "exact_center_hits": "3",
                "same_concept_center_hits": "0",
                "same_category_center_hits": "0",
                "exact_span_hits": "4",
                "same_concept_span_hits": "0",
                "same_category_span_hits": "0",
            }
        ],
    )

    code = summarize.main(
        [
            "--hits",
            str(hits),
            "--summary",
            str(summary),
            "--markdown-out",
            str(md),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    assert "Center word contains same term" in md.read_text(encoding="utf-8")
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["aggregates"]["center_word_exact_hits"] == 1


def test_main_can_read_from_duckdb(tmp_path: Path) -> None:
    pytest.importorskip("duckdb")
    hits = tmp_path / "hits.csv"
    summary = tmp_path / "summary.csv"
    md = tmp_path / "summary.md"
    manifest = tmp_path / "manifest.json"
    db = tmp_path / "reports" / "db.duckdb"
    write_csv(
        hits,
        [
            {"best_context": "exact_center"},
            {"best_context": ""},
        ],
    )
    write_csv(
        summary,
        [
            {
                "corpus": "MT",
                "term_id": "t1",
                "concept": "Term",
                "category": "cat",
                "term": "אבגד",
                "normalized_term": "אבגד",
                "hit_count": "10",
                "context_hit_count": "4",
                "exact_center_word_hits": "1",
                "same_concept_center_word_hits": "2",
                "same_category_center_word_hits": "0",
                "exact_center_hits": "3",
                "same_concept_center_hits": "0",
                "same_category_center_hits": "0",
                "exact_span_hits": "4",
                "same_concept_span_hits": "0",
                "same_category_span_hits": "0",
            }
        ],
    )
    import_csv_table(db_path=db, csv_path=hits, table_name="hits")
    import_csv_table(db_path=db, csv_path=summary, table_name="summary")

    code = summarize.main(
        [
            "--hits",
            str(hits),
            "--summary",
            str(summary),
            "--db",
            str(db),
            "--hits-table",
            "hits",
            "--summary-table",
            "summary",
            "--markdown-out",
            str(md),
            "--manifest-out",
            str(manifest),
        ]
    )

    assert code == 0
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    assert payload["aggregates"]["hit_rows"] == 2
    assert payload["aggregates"]["context_counts"]["hidden_path_only"] == 1
    assert payload["aggregates"]["center_word_exact_hits"] == 1
