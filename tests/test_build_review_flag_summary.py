import csv
import json
from pathlib import Path

from scripts.build_review_flag_summary import build_flag_rows, main, summarize_flags


def row(
    *,
    term_id: str = "term",
    constant: str = "no",
    bigram: str = "",
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
        "skip_equals_meaningful_constant": constant,
        "meaningful_constant_skips": "7" if constant == "yes" else "",
        "meaningful_constant_labels": "Sabbath" if constant == "yes" else "",
        "skip_equals_term_gematria": "no",
        "term_gematria_matching_skips": "",
        "term_gematria_value": "",
        "skip_equals_center_word_gematria": "no",
        "center_word_gematria_matching_skips": "",
        "center_word_gematria_value": "",
        "bigram_surprise_stratum": bigram,
        "bigram_surprise_evidence": "ab:1" if bigram else "",
        "bigram_min_count": "1" if bigram else "",
        "bigram_max_count": "9" if bigram else "",
        "letter_frequency_stratum": "",
        "letter_frequency_evidence": "",
        "letter_frequency_min_count": "",
        "letter_frequency_max_count": "",
    }


def test_build_flag_rows_unpivots_review_flags() -> None:
    flags = build_flag_rows([row(term_id="a", constant="yes", bigram="high_bigram_surprise"), row(term_id="b")])

    assert [flag["flag_type"] for flag in flags] == ["skip_equals_meaningful_constant", "bigram_surprise"]
    assert flags[0]["flag_value"] == "7"
    assert flags[1]["evidence"] == "ab:1"


def test_summarize_flags_counts_by_source_and_type() -> None:
    rows = [row(term_id="a", constant="yes"), row(term_id="b", bigram="low_bigram_surprise"), row(term_id="c")]
    flags = build_flag_rows(rows)
    summary = summarize_flags(rows, flags)
    keyed = {(item["flag_type"], item["corpus"]): item for item in summary}

    assert keyed[("skip_equals_meaningful_constant", "MT")]["flag_rows"] == 1
    assert keyed[("bigram_surprise", "MT")]["flag_rows"] == 1
    assert keyed[("bigram_surprise", "MT")]["share_of_input_rows"] == "0.333333"


def test_main_writes_outputs(tmp_path: Path) -> None:
    strata = tmp_path / "strata.csv"
    out = tmp_path / "summary.csv"
    flag_out = tmp_path / "flags.csv"
    markdown = tmp_path / "report.md"
    manifest = tmp_path / "manifest.json"
    rows = [row(term_id="a", constant="yes"), row(term_id="b")]
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
                "--flag-out",
                str(flag_out),
                "--markdown-out",
                str(markdown),
                "--manifest-out",
                str(manifest),
            ]
        )
        == 0
    )
    assert "skip_equals_meaningful_constant" in out.read_text(encoding="utf-8")
    assert "Sabbath" in flag_out.read_text(encoding="utf-8")
    assert "Review Flag Summary" in markdown.read_text(encoding="utf-8")
    assert json.loads(manifest.read_text(encoding="utf-8"))["flag_rows"] == 1
