import csv
import json
from pathlib import Path

from scripts.build_cross_skip_summary import cross_skip_candidate_rows, main, summarize_cross_skip


def row(
    *,
    term_id: str = "term",
    at_word: str = "no",
    at_letter: str = "no",
    within: str = "no",
    source_family: str = "demo",
    corpus: str = "MT",
) -> dict[str, str]:
    return {
        "source_family": source_family,
        "source_queue": source_family,
        "corpus_class": "bible",
        "corpus": corpus,
        "term_id": term_id,
        "concept": term_id.title(),
        "category": "demo",
        "normalized_term": term_id,
        "center_ref": "Gen 1:1",
        "center_word": term_id,
        "skip": "7",
        "direction": "forward",
        "cross_skip_pair_at_word": at_word,
        "cross_skip_pair_count": "1" if at_word == "yes" else "0",
        "cross_skip_pair_terms": "other" if at_word == "yes" else "",
        "cross_skip_pair_skips": "11" if at_word == "yes" else "",
        "cross_skip_pair_at_letter": at_letter,
        "cross_skip_pair_at_letter_count": "1" if at_letter == "yes" else "0",
        "cross_skip_pair_at_letter_terms": "letter_other" if at_letter == "yes" else "",
        "cross_skip_pair_within_N_letters": within,
        "cross_skip_pair_within_letter_distance": "10" if within == "yes" else "",
        "cross_skip_pair_within_letter_min_distance": "2" if within == "yes" else "",
        "cross_skip_pair_within_letter_count": "1" if within == "yes" else "0",
        "cross_skip_pair_within_letter_terms": "near_other" if within == "yes" else "",
    }


def test_summarize_cross_skip_counts_overlapping_buckets() -> None:
    summary = summarize_cross_skip(
        [
            row(term_id="a", at_word="yes", at_letter="yes"),
            row(term_id="b", within="yes"),
            row(term_id="c"),
        ]
    )
    keyed = {(item["bucket"], item["corpus"]): item for item in summary}

    assert keyed[("cross_skip_pair_at_word", "MT")]["rows"] == 1
    assert keyed[("cross_skip_pair_at_letter", "MT")]["rows"] == 1
    assert keyed[("cross_skip_pair_within_N_letters", "MT")]["rows"] == 1
    assert keyed[("no_cross_skip_pair_data", "MT")]["rows"] == 1
    assert keyed[("cross_skip_pair_at_word", "MT")]["share_of_group"] == "0.333333"


def test_cross_skip_candidate_rows_keep_only_rows_with_any_pair() -> None:
    rows = cross_skip_candidate_rows([row(term_id="a", at_word="yes"), row(term_id="b")])

    assert len(rows) == 1
    assert rows[0]["term_id"] == "a"
    assert rows[0]["cross_skip_pair_terms"] == "other"


def test_main_writes_outputs(tmp_path: Path) -> None:
    strata = tmp_path / "strata.csv"
    out = tmp_path / "summary.csv"
    candidate_out = tmp_path / "candidates.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"
    rows = [row(term_id="a", at_word="yes"), row(term_id="b")]
    with strata.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    assert (
        main(
            [
                "--strata",
                str(strata),
                "--out",
                str(out),
                "--candidate-out",
                str(candidate_out),
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )
    assert "cross_skip_pair_at_word" in out.read_text(encoding="utf-8")
    assert "Gen 1:1" in candidate_out.read_text(encoding="utf-8")
    assert "Cross-Skip Summary" in markdown.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["candidate_rows"] == 1
