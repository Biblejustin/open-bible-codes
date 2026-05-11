from array import array

from els.corpus import Corpus, VerseSpan, WordSpan
from scripts.analyze_notable_passage_gaps import (
    Passage,
    classify_gap,
    parse_ref,
    passage_span,
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
