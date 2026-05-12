import csv
from pathlib import Path

from scripts.summarize_matrix_cluster_controls import (
    main,
    summarize_by_relation,
    summarize_by_term_pair,
)


def candidate_row(
    *,
    relation: str = "same_cell",
    corpus_label: str = "MT_WLC",
    corpus_class: str = "bible",
    left_term_id: str = "gog_h",
    right_term_id: str = "magog_h",
) -> dict[str, str]:
    return {
        "row_width": "50",
        "max_cell_distance": "1",
        "cell_distance": "0" if relation == "same_cell" else "1",
        "cell_relation": relation,
        "left_cell": "1:1",
        "right_cell": "1:1",
        "corpus_label": corpus_label,
        "corpus_class": corpus_class,
        "left_hit_index": "1",
        "right_hit_index": "2",
        "left_term_id": left_term_id,
        "right_term_id": right_term_id,
        "left_concept": "Gog",
        "right_concept": "Magog",
        "left_normalized_term": "גוג",
        "right_normalized_term": "מגוג",
        "left_skip": "7",
        "right_skip": "11",
        "left_direction": "forward",
        "right_direction": "backward",
        "left_center_ref": "Ezek 38:2",
        "right_center_ref": "Ezek 38:2",
        "left_center_word": "גוג",
        "right_center_word": "מגוג",
    }


def test_summarize_by_relation_compares_bible_and_controls() -> None:
    rows = [
        candidate_row(corpus_label="MT_WLC", corpus_class="bible"),
        candidate_row(corpus_label="UHB", corpus_class="bible"),
        candidate_row(corpus_label="UHB", corpus_class="bible"),
        candidate_row(corpus_label="HEB_CONTROL", corpus_class="secular_control"),
    ]

    summary = summarize_by_relation(rows)
    same_cell = next(row for row in summary if row["cell_relation"] == "same_cell")

    assert same_cell["bible_pairs"] == 3
    assert same_cell["secular_control_pairs"] == 1
    assert same_cell["bible_corpora"] == 2
    assert same_cell["secular_control_corpora"] == 1
    assert same_cell["bible_pairs_per_corpus"] == "1.500000"
    assert same_cell["secular_control_pairs_per_corpus"] == "1.000000"
    assert same_cell["bible_to_control_rate_ratio"] == "1.500000"
    assert same_cell["exceeds_secular_max"] == "yes"


def test_summarize_by_term_pair_canonicalizes_term_order() -> None:
    reversed_row = candidate_row(left_term_id="magog_h", right_term_id="gog_h")
    reversed_row["left_concept"] = "Magog"
    reversed_row["right_concept"] = "Gog"
    reversed_row["left_normalized_term"] = "מגוג"
    reversed_row["right_normalized_term"] = "גוג"
    rows = [candidate_row(), reversed_row]

    summary = summarize_by_term_pair(rows)

    assert len(summary) == 1
    assert summary[0]["term_a_id"] == "gog_h"
    assert summary[0]["term_b_id"] == "magog_h"
    assert summary[0]["bible_pairs"] == 2


def test_main_writes_control_summaries(tmp_path: Path) -> None:
    candidates = tmp_path / "candidates.csv"
    relation_out = tmp_path / "relation.csv"
    term_pair_out = tmp_path / "term_pair.csv"
    markdown_out = tmp_path / "matrix_control.md"
    manifest_out = tmp_path / "manifest.json"
    rows = [
        candidate_row(corpus_label="MT_WLC", corpus_class="bible"),
        candidate_row(corpus_label="HEB_CONTROL", corpus_class="secular_control"),
    ]
    with candidates.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    assert (
        main(
            [
                "--candidates",
                str(candidates),
                "--relation-out",
                str(relation_out),
                "--term-pair-out",
                str(term_pair_out),
                "--markdown-out",
                str(markdown_out),
                "--manifest-out",
                str(manifest_out),
            ]
        )
        == 0
    )

    assert "same_cell" in relation_out.read_text(encoding="utf-8")
    assert "gog_h" in term_pair_out.read_text(encoding="utf-8")
    assert "Matrix Cluster Control Summary" in markdown_out.read_text(encoding="utf-8")
    assert '"candidate_rows": 2' in manifest_out.read_text(encoding="utf-8")
