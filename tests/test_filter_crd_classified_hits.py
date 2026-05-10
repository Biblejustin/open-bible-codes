from __future__ import annotations

import csv
from pathlib import Path

from scripts.filter_crd_classified_hits import filter_rows


def test_filter_rows_by_relevance_corpus_class_and_scope(tmp_path: Path) -> None:
    hits = tmp_path / "classified_hits.csv"
    output = tmp_path / "center_word.csv"
    rows = [
        row("1", "bible", "true", "center_word"),
        row("2", "bible", "true", "center_verse"),
        row("3", "secular_control", "true", "center_word"),
        row("4", "bible", "false", "center_word"),
    ]
    write_rows(hits, rows)

    count = filter_rows(
        classified_hits=hits,
        output=output,
        corpus_class="bible",
        is_relevant="true",
        surface_match_scope="center_word",
    )

    filtered = read_rows(output)
    assert count == 1
    assert filtered[0]["hit_id"] == "1"


def row(hit_id: str, corpus_class: str, is_relevant: str, scope: str) -> dict[str, str]:
    return {
        "hit_id": hit_id,
        "term_id": "term",
        "corpus_class": corpus_class,
        "is_relevant": is_relevant,
        "surface_match_scope": scope,
    }


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
