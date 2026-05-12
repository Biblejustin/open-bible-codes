from pathlib import Path

from scripts.summarize_word_edge_patterns import main, summarize_rows


def test_summarize_rows_groups_word_edge_hits() -> None:
    rows = [
        {
            "pattern_type": "acrostic",
            "corpus_label": "MT_WLC",
            "corpus": "OSHB",
            "term_id": "yhwh",
            "concept": "YHWH",
            "category": "word_edge",
            "normalized_term": "יהוה",
            "direction": "forward",
            "word_skip": "1",
            "center_ref": "Esth 5:4",
        },
        {
            "pattern_type": "acrostic",
            "corpus_label": "MT_WLC",
            "corpus": "OSHB",
            "term_id": "yhwh",
            "concept": "YHWH",
            "category": "word_edge",
            "normalized_term": "יהוה",
            "direction": "backward",
            "word_skip": "3",
            "center_ref": "Esth 7:5",
        },
    ]

    output = summarize_rows(rows, cap_threshold=1)

    assert len(output) == 1
    assert output[0]["hits"] == 2
    assert output[0]["forward_hits"] == 1
    assert output[0]["backward_hits"] == 1
    assert output[0]["min_word_skip"] == 1
    assert output[0]["max_word_skip"] == 3
    assert output[0]["capped_at_step_limit"] == "yes"
    assert output[0]["center_refs_sample"] == "Esth 5:4;Esth 7:5"


def test_main_writes_word_edge_summary(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    hits.write_text(
        "pattern_type,corpus_label,corpus,term_id,concept,category,normalized_term,direction,word_skip,center_ref\n"
        "acrostic,MT_WLC,OSHB,yhwh,YHWH,word_edge,יהוה,forward,1,Esth 5:4\n",
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
                "--cap-threshold",
                "1",
            ]
        )
        == 0
    )

    assert "yhwh" in summary.read_text(encoding="utf-8")
    assert "capped_at_step_limit" in summary.read_text(encoding="utf-8")
    assert "Acrostic means first letters" in markdown.read_text(encoding="utf-8")
    assert "Word skip is the interval" in markdown.read_text(encoding="utf-8")
    assert manifest.exists()


def test_main_writes_word_skip_token_summary_text(tmp_path: Path) -> None:
    hits = tmp_path / "hits.csv"
    hits.write_text(
        "pattern_type,corpus_label,corpus,term_id,concept,category,normalized_term,direction,word_skip,center_ref\n"
        "word_skip_ELS,MT_WLC,OSHB,children_israel,Children Israel,word_skip,בני ישראל,forward,2,Exod 1:1\n",
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
                "--title",
                "Word-Skip Term Audit",
            ]
        )
        == 0
    )

    markdown_text = markdown.read_text(encoding="utf-8")
    assert "full normalized surface-word tokens" in markdown_text
    assert "`word_skip_ELS` means full normalized surface-word tokens" in markdown_text
