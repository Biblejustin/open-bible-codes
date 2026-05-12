import csv
import json
from pathlib import Path

from scripts.build_canonical_first_summary import canonical_first_rows, main, summarize_canonical_first


def row(
    *,
    term_id: str = "term",
    first: str = "yes",
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
        "canonical_first_centered_occurrence": first,
        "canonical_first_group": f"{source_family}|{corpus}|{term_id}",
    }


def test_summarize_canonical_first_counts_buckets() -> None:
    summary = summarize_canonical_first([row(term_id="a", first="yes"), row(term_id="a", first="no"), row(term_id="b", first="")])
    keyed = {(item["bucket"], item["corpus"]): item for item in summary}

    assert keyed[("canonical_first_centered_occurrence", "MT")]["rows"] == 1
    assert keyed[("later_centered_occurrence", "MT")]["rows"] == 1
    assert keyed[("no_canonical_first_data", "MT")]["rows"] == 1
    assert keyed[("canonical_first_centered_occurrence", "MT")]["share_of_group"] == "0.333333"


def test_canonical_first_rows_preserve_review_fields() -> None:
    rows = canonical_first_rows([row(term_id="a", first="yes"), row(term_id="b", first="no")])

    assert len(rows) == 1
    assert rows[0]["term_id"] == "a"
    assert rows[0]["center_ref"] == "Gen 1:1"


def test_main_writes_outputs(tmp_path: Path) -> None:
    strata = tmp_path / "strata.csv"
    out = tmp_path / "summary.csv"
    first_out = tmp_path / "first.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"
    rows = [row(term_id="a", first="yes"), row(term_id="b", first="no")]
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
                "--first-out",
                str(first_out),
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )
    assert "canonical_first_centered_occurrence" in out.read_text(encoding="utf-8")
    assert "Gen 1:1" in first_out.read_text(encoding="utf-8")
    assert "Canonical First Summary" in markdown.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["canonical_first_rows"] == 1
