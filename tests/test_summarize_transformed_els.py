from pathlib import Path

from scripts.summarize_transformed_els import main, summarize_rows


def test_summarize_rows_groups_hits_by_transform_corpus_and_term() -> None:
    rows = [
        {
            "transform": "hebrew_atbash",
            "base_corpus": "MT_WLC",
            "term_id": "babylon",
            "concept": "Babylon",
            "category": "cryptogram",
            "normalized_term": "בבל",
            "direction": "forward",
            "skip": "5",
            "center_ref": "Jer 25:26",
        },
        {
            "transform": "hebrew_atbash",
            "base_corpus": "MT_WLC",
            "term_id": "babylon",
            "concept": "Babylon",
            "category": "cryptogram",
            "normalized_term": "בבל",
            "direction": "backward",
            "skip": "-7",
            "center_ref": "Jer 51:41",
        },
    ]

    output = summarize_rows(rows)

    assert len(output) == 1
    assert output[0]["hits"] == 2
    assert output[0]["forward_hits"] == 1
    assert output[0]["backward_hits"] == 1
    assert output[0]["min_abs_skip"] == 5
    assert output[0]["max_abs_skip"] == 7
    assert output[0]["center_refs_sample"] == "Jer 25:26;Jer 51:41"


def test_main_writes_summary_markdown_and_manifest(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    hits.write_text(
        "transform,base_corpus,term_id,concept,category,normalized_term,direction,skip,center_ref\n"
        "hebrew_atbash,MT_WLC,babylon,Babylon,cryptogram,בבל,forward,5,Jer 25:26\n",
        encoding="utf-8",
    )
    summary = tmp_path / "summary.csv"
    markdown = tmp_path / "summary.md"
    manifest = tmp_path / "manifest.json"

    assert (
        main(
            [
                "--hits",
                str(hits),
                "--summary-out",
                str(summary),
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )

    assert "babylon" in summary.read_text(encoding="utf-8")
    assert "opt-in transformed-text audit" in markdown.read_text(encoding="utf-8")
    assert manifest.exists()
