from array import array
from pathlib import Path

from els.corpus import Corpus, VerseSpan, WordSpan
from scripts.search_word_edge_patterns import (
    main,
    matching_starts,
    search_word_edge_patterns,
    word_edge_letters,
)


def tiny_word_corpus() -> Corpus:
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "alpha", "alpha", 0, 4, 5),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "beta", "beta", 5, 8, 4),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "gamma", "gamma", 9, 13, 5),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 4, "delta", "delta", 14, 18, 5),
    )
    return Corpus(
        name="tiny",
        language="english",
        keep_hebrew_final_forms=False,
        text="alphabetagammadelta",
        verses=(VerseSpan("test", "Test 1:1", "Test", "1", "1", "alpha beta gamma delta", 0, 18, 19),),
        position_to_verse=array("i", [0] * 19),
        words=words,
        position_to_word=array("i", [0] * 5 + [1] * 4 + [2] * 5 + [3] * 5),
    )


def test_word_edge_letters_extract_acrostic_and_telestic() -> None:
    corpus = tiny_word_corpus()

    assert word_edge_letters(corpus.words, "acrostic") == "abgd"
    assert word_edge_letters(corpus.words, "telestic") == "aaaa"


def test_search_word_edge_patterns_finds_forward_acrostic() -> None:
    rows = search_word_edge_patterns(
        tiny_word_corpus(),
        [{"term_id": "abg", "concept": "ABG", "category": "test", "term": "abg"}],
        corpus_label="TINY",
        pattern="acrostic",
        direction="forward",
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["pattern_type"] == "acrostic"
    assert rows[0]["corpus_label"] == "TINY"
    assert rows[0]["center_word"] == "beta"
    assert rows[0]["sequence"] == "abg"
    assert rows[0]["word_skip"] == 1
    assert rows[0]["word_span"] == 3


def test_matching_starts_supports_word_skip_lanes() -> None:
    assert matching_starts("abgd", "bd", word_skip=2) == [1]


def test_search_word_edge_patterns_finds_word_skip_acrostic() -> None:
    rows = search_word_edge_patterns(
        tiny_word_corpus(),
        [{"term_id": "bd", "concept": "BD", "category": "test", "term": "bd"}],
        pattern="acrostic",
        direction="forward",
        min_word_skip=2,
        max_word_skip=2,
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["sequence"] == "bd"
    assert rows[0]["word_skip"] == 2
    assert rows[0]["word_span"] == 3
    assert rows[0]["start_word"] == "beta"
    assert rows[0]["end_word"] == "delta"


def test_search_word_edge_patterns_finds_backward_telestic() -> None:
    rows = search_word_edge_patterns(
        tiny_word_corpus(),
        [{"term_id": "aaa", "concept": "AAA", "category": "test", "term": "aaa"}],
        pattern="telestic",
        direction="backward",
        max_hits_per_term=1,
    )

    assert len(rows) == 1
    assert rows[0]["pattern_type"] == "telestic"
    assert rows[0]["direction"] == "backward"


def test_main_writes_word_edge_hits(tmp_path: Path, monkeypatch) -> None:
    terms = tmp_path / "terms.csv"
    terms.write_text(
        "term_id,concept,category,language,term,notes\n"
        "abg,ABG,test,english,abg,\n",
        encoding="utf-8",
    )
    out = tmp_path / "hits.csv"

    monkeypatch.setattr("scripts.search_word_edge_patterns.load_corpus", lambda _config: tiny_word_corpus())

    assert (
        main(
            [
                "--config",
                "unused.toml",
                "--terms",
                str(terms),
                "--pattern",
                "acrostic",
                "--direction",
                "forward",
                "--out",
                str(out),
            ]
        )
        == 0
    )

    assert "abg" in out.read_text(encoding="utf-8")
