from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_crd_scope_density import build_matrix_rows, build_summary_rows, count_scope_hits


def test_scope_density_counts_and_compares_bible_controls(tmp_path: Path) -> None:
    classified_hits = tmp_path / "classified_hits.csv"
    density = tmp_path / "density.csv"
    write_rows(
        classified_hits,
        [
            hit("term", "BIBLE", "bible", "center_word"),
            hit("term", "BIBLE", "bible", "center_word"),
            hit("term", "BIBLE", "bible", "center_verse"),
            hit("term", "CTRL", "secular_control", "center_word"),
        ],
    )
    write_rows(
        density,
        [
            density_row("term", "BIBLE", "bible", letters="100", total_hits="4"),
            density_row("term", "CTRL", "secular_control", letters="200", total_hits="4"),
        ],
    )

    counts = count_scope_hits(classified_hits, "center_word")
    matrix_rows = build_matrix_rows(
        base_density_matrix=density,
        counts=counts,
        surface_match_scope="center_word",
    )
    summary_rows = build_summary_rows(matrix_rows)

    assert matrix_rows[0]["scope_relevant_hits"] == "2"
    assert matrix_rows[0]["scope_density_per_million"] == "20000"
    assert matrix_rows[0]["scope_relevance_rate"] == "0.5"
    assert summary_rows[0]["bible_max_density"] == "20000"
    assert summary_rows[0]["secular_max_density"] == "5000"
    assert summary_rows[0]["ratio"] == "4"
    assert summary_rows[0]["exceeds_secular_max"] == "true"


def hit(term_id: str, corpus: str, corpus_class: str, scope: str) -> dict[str, str]:
    return {
        "classifier_mode": "deterministic",
        "term_id": term_id,
        "corpus": corpus,
        "corpus_class": corpus_class,
        "is_relevant": "true",
        "surface_match_scope": scope,
    }


def density_row(term_id: str, corpus: str, corpus_class: str, *, letters: str, total_hits: str) -> dict[str, str]:
    return {
        "classifier_mode": "deterministic",
        "term_id": term_id,
        "term": "term",
        "concept": "Term",
        "category": "category",
        "language": "english",
        "corpus": corpus,
        "corpus_class": corpus_class,
        "total_centered_hits": total_hits,
        "corpus_normalized_letters": letters,
    }


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
