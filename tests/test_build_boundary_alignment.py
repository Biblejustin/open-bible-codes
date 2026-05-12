import csv
import json
from pathlib import Path

from scripts.build_boundary_alignment import main, summarize_boundary_alignment


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
        "boundary_strata": strata,
    }


def test_summarize_boundary_alignment_counts_boundary_buckets() -> None:
    summary = summarize_boundary_alignment(
        [
            row(term_id="a", strata="boundary_start_verse;boundary_start_chapter"),
            row(term_id="b", strata="boundary_end_verse;boundary_both_endpoints"),
            row(term_id="a", strata=""),
        ]
    )
    keyed = {(item["bucket"], item["corpus"]): item for item in summary}

    assert keyed[("boundary_start_verse", "MT")]["rows"] == 1
    assert keyed[("boundary_start_chapter", "MT")]["rows"] == 1
    assert keyed[("boundary_end_verse", "MT")]["rows"] == 1
    assert keyed[("boundary_both_endpoints", "MT")]["rows"] == 1
    assert keyed[("no_boundary_data", "MT")]["share_of_group"] == "0.333333"


def test_main_writes_outputs(tmp_path: Path) -> None:
    strata = tmp_path / "strata.csv"
    out = tmp_path / "summary.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"
    rows = [row(term_id="a", strata="boundary_start_book"), row(term_id="b")]
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
    assert "boundary_start_book" in out.read_text(encoding="utf-8")
    assert "Boundary Alignment" in markdown.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["input_rows"] == 2
