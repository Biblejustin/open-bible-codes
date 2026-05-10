from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_crd_review_queue import build_review_queue, select_terms


def test_select_terms_keeps_top_finite_and_zero(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    write_rows(
        summary,
        [
            {
                "term_id": "high",
                "bible_max_corpus": "BIBLE",
                "bible_max_density": "10",
                "secular_max_corpus": "CTRL",
                "secular_max_density": "2",
                "ratio": "5",
                "exceeds_secular_max": "true",
            },
            {
                "term_id": "zero",
                "bible_max_corpus": "BIBLE",
                "bible_max_density": "4",
                "secular_max_corpus": "CTRL",
                "secular_max_density": "0",
                "ratio": "",
                "exceeds_secular_max": "true",
            },
            {
                "term_id": "low",
                "bible_max_corpus": "BIBLE",
                "bible_max_density": "1",
                "secular_max_corpus": "CTRL",
                "secular_max_density": "3",
                "ratio": "0.333",
                "exceeds_secular_max": "false",
            },
        ],
    )

    selected = select_terms(summary, top_finite=1, top_zero=1)

    assert selected["high"].reason == "top_finite_ratio"
    assert selected["zero"].reason == "bible_positive_secular_zero"
    assert "low" not in selected


def test_build_review_queue_filters_relevant_bible_rows(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    hits = tmp_path / "hits.csv"
    output = tmp_path / "queue.csv"
    write_rows(
        summary,
        [
            {
                "term_id": "high",
                "bible_max_corpus": "BIBLE",
                "bible_max_density": "10",
                "secular_max_corpus": "CTRL",
                "secular_max_density": "2",
                "ratio": "5",
                "exceeds_secular_max": "true",
            }
        ],
    )
    write_rows(
        hits,
        [
            hit_row("high", "BIBLE", "bible", "true", "1"),
            hit_row("high", "BIBLE", "bible", "true", "2"),
            hit_row("high", "OTHER_BIBLE", "bible", "true", "3"),
            hit_row("high", "CTRL", "secular_control", "true", "4"),
            hit_row("high", "BIBLE", "bible", "false", "5"),
        ],
    )

    selected = select_terms(summary, top_finite=1, top_zero=0)
    written = build_review_queue(
        classified_hits=hits,
        output=output,
        selected_terms=selected,
        examples_per_term=1,
        all_bible_corpora=False,
    )

    rows = read_rows(output)
    assert written == 1
    assert rows[0]["hit_id"] == "1"
    assert rows[0]["selection_reason"] == "top_finite_ratio"
    assert rows[0]["bible_max_corpus"] == "BIBLE"


def hit_row(term_id: str, corpus: str, corpus_class: str, is_relevant: str, hit_id: str) -> dict[str, str]:
    return {
        "hit_id": hit_id,
        "term_id": term_id,
        "term": "term",
        "concept": "Concept",
        "category": "category",
        "language": "english",
        "corpus": corpus,
        "corpus_class": corpus_class,
        "classifier_mode": "deterministic",
        "is_relevant": is_relevant,
        "relevance_type": "surface_keyword_match" if is_relevant == "true" else "none",
        "confidence": "",
        "skip": "2",
        "direction": "forward",
        "start_ref": "A 1:1",
        "center_ref": "A 1:1",
        "end_ref": "A 1:1",
        "center_word": "word",
        "center_normalized_word": "word",
        "center_verse_text": "center text",
        "span_text": "span text",
    }


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
