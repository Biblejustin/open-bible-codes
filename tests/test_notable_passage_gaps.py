from array import array
from types import SimpleNamespace

from els.corpus import Corpus, VerseSpan, WordSpan
from scripts.analyze_notable_passage_gaps import (
    Passage,
    classify_gap,
    parse_ref,
    passage_span,
    ref_number,
    verse_key_or_none,
    write_markdown,
)


def tiny_corpus() -> Corpus:
    text = "abcdefghijkl"
    verses = (
        VerseSpan("test", "Lev 24:1", "Lev", "24", "1", "abc def", 0, 6, 6),
        VerseSpan("test", "Lev 24:2", "Lev", "24", "2", "ghi jkl", 6, 12, 6),
    )
    words = (
        WordSpan("test", "Lev 24:1", "Lev", "24", "1", 1, "abc", "abc", 0, 3, 3),
        WordSpan("test", "Lev 24:1", "Lev", "24", "1", 2, "def", "def", 3, 6, 3),
        WordSpan("test", "Lev 24:2", "Lev", "24", "2", 1, "ghi", "ghi", 6, 9, 3),
        WordSpan("test", "Lev 24:2", "Lev", "24", "2", 2, "jkl", "jkl", 9, 12, 3),
    )
    return Corpus(
        name="tiny",
        language="english",
        keep_hebrew_final_forms=False,
        text=text,
        verses=verses,
        position_to_verse=array("i", [0] * 6 + [1] * 6),
        words=words,
        position_to_word=array("i", [0] * 3 + [1] * 3 + [2] * 3 + [3] * 3),
    )


def test_parse_ref_normalizes_book_alias() -> None:
    parsed = parse_ref("Leviticus 24:23")
    assert parsed.book == "Lev"
    assert parsed.chapter == 24
    assert parsed.verse == 23


def test_ref_number_accepts_lxx_suffixes() -> None:
    assert ref_number("14α") == 14


def test_verse_key_or_none_skips_unmapped_apocrypha_book() -> None:
    verse = VerseSpan("test", "TOB 1:1", "TOB", "1", "1", "text", 0, 4, 4)
    assert verse_key_or_none(verse) is None


def test_passage_span_finds_requested_verses() -> None:
    passage = Passage(
        passage_id="lev24",
        concept="Leviticus 24",
        category="test",
        language="english",
        corpus_group="test",
        start_ref="Lev 24:2",
        end_ref="Lev 24:2",
        notes="",
    )
    span = passage_span(tiny_corpus(), passage)
    assert span.norm_start == 6
    assert span.norm_end == 12
    assert span.norm_length == 6


def test_classify_gap_absent_common_elsewhere() -> None:
    assert (
        classify_gap(
            total_hits=25,
            centered_in_passage=0,
            expected_in_passage=2.5,
            common_elsewhere=True,
        )
        == "absent_in_passage_common_elsewhere"
    )


def test_classify_gap_low_vs_uniform() -> None:
    assert (
        classify_gap(
            total_hits=100,
            centered_in_passage=1,
            expected_in_passage=8.0,
            common_elsewhere=True,
        )
        == "low_in_passage_vs_uniform"
    )


def test_write_markdown_includes_declared_gap_target_section(tmp_path) -> None:
    out = tmp_path / "gaps.md"
    args = SimpleNamespace(
        passages="passages.csv",
        terms="terms.csv",
        min_skip=2,
        max_skip=100,
        direction="both",
        jobs=1,
        min_term_length=3,
        common_elsewhere_threshold=10,
        detail_out="detail.csv",
        summary_out="summary.csv",
        manifest_out="manifest.json",
    )
    summary_row = {
        "passage_id": "lev24",
        "passage_concept": "Leviticus 24 Blasphemy Law",
        "passage_category": "notable_passage_gap",
        "corpus_label": "MT_WLC",
        "passage_letters": "1037",
        "eligible_terms": "1",
        "terms_present_in_passage": "0",
        "terms_absent_in_passage_present_elsewhere": "1",
        "terms_absent_in_passage_common_elsewhere": "1",
        "terms_low_vs_uniform": "0",
        "observed_centered_hits_in_passage": "0",
        "expected_centered_hits_in_passage_uniform": "3.000",
    }
    detail_row = {
        "passage_id": "lev24",
        "passage_concept": "Leviticus 24 Blasphemy Law",
        "passage_category": "notable_passage_gap",
        "corpus_label": "MT_WLC",
        "term_id": "npg_yhwh_h",
        "normalized_term": "יהוה",
        "concept": "YHWH",
        "gap_class": "absent_in_passage_common_elsewhere",
        "centered_elsewhere": "25",
        "centered_in_passage": "0",
        "expected_in_passage_uniform": "3.000",
        "uniform_zero_probability": "0.049787",
        "sample_center_refs": "",
    }

    write_markdown(out, detail_rows=[detail_row], summary_rows=[summary_row], args=args)

    text = out.read_text(encoding="utf-8")
    assert "## Declared Gap-Target Passages" in text
    assert "## Declared Gap-Target Detail" in text
    assert "Leviticus 24 Blasphemy Law" in text
    assert "Uniform Zero P" in text
    assert "0.049787" in text
