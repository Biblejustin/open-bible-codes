from array import array
from pathlib import Path

from els.corpus import Corpus, VerseSpan, WordSpan
from scripts.search_word_skip_terms import (
    main,
    matching_word_starts,
    normalize_term_tokens,
    search_word_skip_terms,
)


def tiny_word_corpus() -> Corpus:
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "alpha", "alpha", 0, 4, 5),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "beta", "beta", 5, 8, 4),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "gamma", "gamma", 9, 13, 5),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 4, "delta", "delta", 14, 18, 5),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 5, "epsilon", "epsilon", 19, 25, 7),
    )
    return Corpus(
        name="tiny",
        language="english",
        keep_hebrew_final_forms=False,
        text="alphabetagammadeltaepsilon",
        verses=(VerseSpan("test", "Test 1:1", "Test", "1", "1", "alpha beta gamma delta epsilon", 0, 25, 26),),
        position_to_verse=array("i", [0] * 26),
        words=words,
        position_to_word=array("i", [0] * 5 + [1] * 4 + [2] * 5 + [3] * 5 + [4] * 7),
    )


def test_normalize_term_tokens_keeps_word_boundaries() -> None:
    assert normalize_term_tokens("Alpha, Beta!", "english") == ("alpha", "beta")


def test_matching_word_starts_supports_word_skip_lanes() -> None:
    corpus = tiny_word_corpus()

    assert matching_word_starts(corpus.words, ("beta", "delta"), word_skip=2) == [1]


def test_search_word_skip_terms_finds_forward_phrase() -> None:
    rows = search_word_skip_terms(
        tiny_word_corpus(),
        [{"term_id": "beta_gamma", "concept": "Beta Gamma", "category": "test", "language": "english", "term": "beta gamma"}],
        corpus_label="TINY",
        direction="forward",
        min_word_skip=1,
        max_word_skip=1,
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["pattern_type"] == "word_skip_ELS"
    assert rows[0]["corpus_label"] == "TINY"
    assert rows[0]["normalized_tokens"] == "beta gamma"
    assert rows[0]["sequence"] == "beta gamma"
    assert rows[0]["word_skip"] == 1
    assert rows[0]["word_span"] == 2
    assert rows[0]["center_word"] == "beta"


def test_search_word_skip_terms_finds_skipped_phrase() -> None:
    rows = search_word_skip_terms(
        tiny_word_corpus(),
        [{"term_id": "beta_delta", "concept": "Beta Delta", "category": "test", "language": "english", "term": "beta delta"}],
        direction="forward",
        min_word_skip=2,
        max_word_skip=2,
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["word_skip"] == 2
    assert rows[0]["word_span"] == 3
    assert rows[0]["start_word"] == "beta"
    assert rows[0]["end_word"] == "delta"


def test_search_word_skip_terms_finds_backward_phrase() -> None:
    rows = search_word_skip_terms(
        tiny_word_corpus(),
        [{"term_id": "delta_beta", "concept": "Delta Beta", "category": "test", "language": "english", "term": "delta beta"}],
        direction="backward",
        min_word_skip=2,
        max_word_skip=2,
        max_hits_per_term=10,
    )

    assert len(rows) == 1
    assert rows[0]["direction"] == "backward"
    assert rows[0]["sequence"] == "beta delta"
    assert rows[0]["start_word"] == "beta"


def test_search_word_skip_terms_filters_mismatched_language() -> None:
    rows = search_word_skip_terms(
        tiny_word_corpus(),
        [{"term_id": "hebrew", "concept": "Hebrew", "category": "test", "language": "hebrew", "term": "אבג"}],
    )

    assert rows == []


def test_main_writes_word_skip_hits(tmp_path: Path, monkeypatch) -> None:
    terms = tmp_path / "terms.csv"
    terms.write_text(
        "term_id,concept,category,language,term,notes\n"
        "beta_gamma,Beta Gamma,test,english,beta gamma,\n",
        encoding="utf-8",
    )
    out = tmp_path / "hits.csv"

    monkeypatch.setattr("scripts.search_word_skip_terms.load_corpus", lambda _config: tiny_word_corpus())

    assert (
        main(
            [
                "--config",
                "unused.toml",
                "--terms",
                str(terms),
                "--direction",
                "forward",
                "--out",
                str(out),
            ]
        )
        == 0
    )

    assert "word_skip_ELS" in out.read_text(encoding="utf-8")
