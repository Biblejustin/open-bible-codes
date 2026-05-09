import argparse

from els.corpus import Corpus, VerseSpan, WordSpan
from els.extensions import build_extension_lexicon
from scripts import analyze_all_codes_extensions as ext


def sample_corpus() -> Corpus:
    text = "αγεζη"
    verses = (
        VerseSpan("test", "Test 1:1", "Test", "1", "1", "αγε ζη", 0, 4, 5),
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αγε", "αγε", 0, 2, 3),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "ζη", "ζη", 3, 4, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=verses,
        position_to_verse=(0, 0, 0, 0, 0),
        words=words,
        position_to_word=(0, 0, 0, 1, 1),
    )


def path_row() -> dict[str, str]:
    return {
        "selection_rank": "1",
        "source_queue": "greek_screening",
        "selection_reason": "test",
        "bucket": "hidden_path_review",
        "presence_scope": "source_only",
        "present_corpora": "TEST",
        "corpus_count": "1",
        "corpus_row_count": "1",
        "term_id": "term",
        "concept": "Term",
        "category": "test",
        "term": "γε",
        "normalized_term": "γε",
        "normalized_length": "2",
        "skip": "1",
        "direction": "forward",
        "span_letters": "2",
        "offsets_by_corpus": "TEST:1/1/2",
        "start_ref": "Test 1:1",
        "center_ref": "Test 1:1",
        "end_ref": "Test 1:1",
        "center_word": "αγε",
        "center_normalized_word": "αγε",
        "audit_corpus": "TEST",
        "sequence": "γε",
        "matches_term": "True",
        "audit_start_ref": "Test 1:1",
        "audit_center_ref": "Test 1:1",
        "audit_end_ref": "Test 1:1",
        "path_refs": "Test 1:1",
        "audit_center_word": "αγε",
        "audit_center_normalized_word": "αγε",
        "audit_start_offset": "1",
        "audit_center_offset": "1",
        "audit_end_offset": "2",
        "path_offsets": "1/2",
    }


def args() -> argparse.Namespace:
    return argparse.Namespace(
        max_before=1,
        max_after=2,
        include_both_sided=True,
        max_extensions_per_path=20,
    )


def test_hit_from_path_row_reconstructs_hit_metadata() -> None:
    hit = ext.hit_from_path_row(sample_corpus(), path_row())

    assert hit.normalized_term == "γε"
    assert hit.start_offset == 1
    assert hit.end_offset == 2
    assert hit.center_word == "αγε"
    assert hit.direction == "forward"


def test_build_extension_rows_finds_same_skip_compound_extension() -> None:
    corpus = sample_corpus()
    rows = ext.build_extension_rows(
        [path_row()],
        {"TEST": corpus},
        {"TEST": build_extension_lexicon(corpus, max_phrase_words=2)},
        args(),
    )

    extended = {row["extended_sequence"]: row for row in rows}
    assert "αγε" in extended
    assert "αγεζη" in extended
    assert extended["αγεζη"]["extension_type"] == "before_plus_term_plus_after"
    assert extended["αγεζη"]["match_kind"] == "phrase_2"


def test_build_summary_rows_promotes_best_extension() -> None:
    corpus = sample_corpus()
    extension_rows = ext.build_extension_rows(
        [path_row()],
        {"TEST": corpus},
        {"TEST": build_extension_lexicon(corpus, max_phrase_words=2)},
        args(),
    )
    summary = ext.build_summary_rows([path_row()], extension_rows)

    assert summary[0]["extension_rows"] == str(len(extension_rows))
    assert summary[0]["best_extended_sequence"] == "αγεζη"
    assert summary[0]["best_extension_type"] == "before_plus_term_plus_after"


def test_is_compound_extension_distinguishes_adjacent_only_rows() -> None:
    assert ext.is_compound_extension({"extension_type": "term_plus_after"})
    assert not ext.is_compound_extension({"extension_type": "after_match"})


def test_markdown_cell_escapes_pipes() -> None:
    assert ext.md_cell("a|b\nc") == "a\\|b c"
