from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from els.report_db import import_csv_table
from scripts.build_crd_comparison import build_crd_comparison
from scripts.run_crd_density import CLASSIFIED_HIT_FIELDNAMES, DENSITY_FIELDNAMES


def test_build_crd_comparison_can_read_classified_hits_from_duckdb(tmp_path: Path) -> None:
    pytest.importorskip("duckdb")
    density = tmp_path / "density_matrix.csv"
    hits = tmp_path / "classified_hits.csv"
    manifest = tmp_path / "manifest.json"
    out_dir = tmp_path / "out"
    db = tmp_path / "reports" / "db.duckdb"
    write_rows(
        density,
        DENSITY_FIELDNAMES,
        [
            density_row("deterministic", "term", "BIBLE", "bible", "10", "2"),
            density_row("llm", "term", "BIBLE", "bible", "10", "2"),
            density_row("deterministic", "term", "CTRL", "secular_control", "10", "0"),
            density_row("llm", "term", "CTRL", "secular_control", "10", "0"),
        ],
    )
    write_rows(
        hits,
        CLASSIFIED_HIT_FIELDNAMES,
        [
            hit_row("h1", "deterministic", "term", "BIBLE", "true"),
            hit_row("h1", "llm", "term", "BIBLE", "true"),
            hit_row("h2", "deterministic", "term", "BIBLE", "false"),
            hit_row("h2", "llm", "term", "BIBLE", "true"),
        ],
    )
    manifest.write_text(json.dumps({"status": "completed"}), encoding="utf-8")
    import_csv_table(db_path=db, csv_path=hits, table_name="classified_hits")

    build_crd_comparison(
        density_matrix=density,
        classified_hits=hits,
        manifest=manifest,
        out_dir=out_dir,
        markdown_out=out_dir / "CRD_REPORT.md",
        db=db,
        classified_table="classified_hits",
    )

    agreement = read_rows(out_dir / "classifier_agreement_summary.csv")
    report = (out_dir / "CRD_REPORT.md").read_text(encoding="utf-8")
    assert agreement[0]["scope"] == "overall"
    assert agreement[0]["agreement_rate"] == "0.5"
    assert "Representative Relevant Centers" in report


def test_build_crd_comparison_displays_script_terms_with_glosses(tmp_path: Path) -> None:
    density = tmp_path / "density_matrix.csv"
    hits = tmp_path / "classified_hits.csv"
    manifest = tmp_path / "manifest.json"
    out_dir = tmp_path / "out"
    write_rows(
        density,
        DENSITY_FIELDNAMES,
        [
            density_row("deterministic", "cyrus_h", "BIBLE", "bible", "10", "2", term="כורש", concept="Cyrus"),
            density_row(
                "deterministic",
                "cyrus_h",
                "CTRL",
                "secular_control",
                "10",
                "0",
                term="כורש",
                concept="Cyrus",
            ),
        ],
    )
    write_rows(
        hits,
        CLASSIFIED_HIT_FIELDNAMES,
        [
            hit_row(
                "h1",
                "deterministic",
                "cyrus_h",
                "BIBLE",
                "true",
                term="כורש",
                concept="Cyrus",
                center_word="מלך",
                matched_surface_keyword="כורש",
            ),
        ],
    )
    manifest.write_text(json.dumps({"status": "completed"}), encoding="utf-8")

    build_crd_comparison(
        density_matrix=density,
        classified_hits=hits,
        manifest=manifest,
        out_dir=out_dir,
        markdown_out=out_dir / "CRD_REPORT.md",
    )

    report = (out_dir / "CRD_REPORT.md").read_text(encoding="utf-8")
    assert "`כורש`" in report
    assert "English: Cyrus" in report
    assert "<br>`cyrus_h`" in report
    assert "`מלך`" in report
    assert "English: king" in report


def density_row(
    classifier_mode: str,
    term_id: str,
    corpus: str,
    corpus_class: str,
    total_hits: str,
    relevant_hits: str,
    *,
    term: str = "term",
    concept: str = "Term",
    language: str = "english",
) -> dict[str, str]:
    return {
        "term_id": term_id,
        "term": term,
        "concept": concept,
        "category": "category",
        "language": language,
        "corpus": corpus,
        "corpus_class": corpus_class,
        "classifier_mode": classifier_mode,
        "total_centered_hits": total_hits,
        "relevant_centered_hits": relevant_hits,
        "corpus_normalized_letters": "100",
        "density_per_million": str(int(relevant_hits) * 10000),
        "relevance_rate": "0.2",
        "agreement_rate": "0.5",
        "agreement_kappa": "",
        "deterministic_only_relevant_count": "0",
        "llm_only_relevant_count": "1",
    }


def hit_row(
    hit_id: str,
    classifier_mode: str,
    term_id: str,
    corpus: str,
    is_relevant: str,
    *,
    term: str = "term",
    concept: str = "Term",
    language: str = "english",
    center_word: str = "term",
    matched_surface_keyword: str = "term",
) -> dict[str, str]:
    return {
        "hit_id": hit_id,
        "term_id": term_id,
        "term": term,
        "concept": concept,
        "category": "category",
        "language": language,
        "corpus": corpus,
        "corpus_class": "bible",
        "classifier_mode": classifier_mode,
        "is_relevant": is_relevant,
        "relevance_type": "surface_keyword_match" if is_relevant == "true" else "none",
        "surface_match_scope": "center_word" if is_relevant == "true" else "",
        "matched_surface_keyword": matched_surface_keyword if is_relevant == "true" else "",
        "matched_normalized_surface_keyword": matched_surface_keyword if is_relevant == "true" else "",
        "confidence": "",
        "skip": "2",
        "direction": "forward",
        "start_ref": "A 1:1",
        "center_ref": "A 1:1",
        "end_ref": "A 1:1",
        "center_word": center_word,
        "center_normalized_word": center_word,
        "center_verse_text": "term appears",
        "span_text": "term appears",
    }


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
