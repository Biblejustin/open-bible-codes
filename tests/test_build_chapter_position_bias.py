import csv
import json
from pathlib import Path

from scripts.build_chapter_position_bias import main, summarize_position_bias


def row(
    *,
    term_id: str = "term",
    strata: str = "",
    source_family: str = "demo",
    corpus: str = "MT",
) -> dict[str, str]:
    return {
        "source_family": source_family,
        "corpus_class": "bible",
        "corpus": corpus,
        "term_id": term_id,
        "center_position_strata": strata,
    }


def test_summarize_position_bias_counts_position_buckets() -> None:
    summary = summarize_position_bias(
        [
            row(term_id="a", strata="center_verse_first_in_chapter"),
            row(term_id="b", strata="center_verse_last_in_chapter;center_verse_last_in_book"),
            row(term_id="a", strata=""),
        ]
    )
    keyed = {(item["bucket"], item["corpus"]): item for item in summary}

    assert keyed[("center_verse_first_in_chapter", "MT")]["rows"] == 1
    assert keyed[("center_verse_last_in_chapter", "MT")]["rows"] == 1
    assert keyed[("center_verse_last_in_book", "MT")]["rows"] == 1
    assert keyed[("interior_or_unmapped", "MT")]["rows"] == 1
    assert keyed[("interior_or_unmapped", "MT")]["share_of_group"] == "0.333333"


def test_main_writes_outputs(tmp_path: Path) -> None:
    strata = tmp_path / "strata.csv"
    out = tmp_path / "summary.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"
    rows = [row(term_id="a", strata="center_verse_first_in_book"), row(term_id="b")]
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
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )
    assert "center_verse_first_in_book" in out.read_text(encoding="utf-8")
    assert "Chapter Position Bias" in markdown.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["input_rows"] == 2
