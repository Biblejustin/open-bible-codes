from els.corpus import Corpus, VerseSpan, WordSpan
from scripts import analyze_greek_surface_letter_paths as paths


def sample_corpus() -> Corpus:
    text = "αβγδεζηθικ"
    verses = (
        VerseSpan("test", "Test 1:1", "Test", "1", "1", "αβ γδ εζ", 0, 5, 6),
        VerseSpan("test", "Test 1:2", "Test", "1", "2", "ηθ ικ", 6, 9, 4),
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "εζ", "εζ", 4, 5, 2),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 1, "ηθ", "ηθ", 6, 7, 2),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 2, "ικ", "ικ", 8, 9, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=verses,
        position_to_verse=(0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
        words=words,
        position_to_word=(0, 0, 1, 1, 2, 2, 3, 3, 4, 4),
    )


def selected_row() -> dict[str, str]:
    return {
        "term_id": "term",
        "concept": "Term",
        "normalized_term": "αγε",
        "skip": "2",
        "direction": "forward",
        "present_corpora": "TEST",
        "offsets_by_corpus": "TEST:0/2/4",
    }


def test_parse_offsets_by_corpus() -> None:
    assert paths.parse_offsets_by_corpus("TR_NT:1/3/5; SBLGNT:2/4/6") == {
        "TR_NT": (1, 3, 5),
        "SBLGNT": (2, 4, 6),
    }


def test_audit_row_reconstructs_sequence_and_words() -> None:
    audit = paths.audit_row(selected_row(), "TEST", sample_corpus(), 0, 2, 4)

    assert audit.summary["sequence"] == "αγε"
    assert audit.summary["matches_term"] == "True"
    assert audit.summary["path_refs"] == "Test 1:1"
    assert audit.summary["center_word"] == "γδ"
    assert [row["letter"] for row in audit.letters] == ["α", "γ", "ε"]
    assert [row["word"] for row in audit.letters] == ["αβ", "γδ", "εζ"]


def test_build_audits_uses_present_corpora_and_offsets() -> None:
    audits = paths.build_audits([selected_row()], {"TEST": sample_corpus()})

    assert len(audits) == 1
    assert audits[0].summary["corpus"] == "TEST"
    assert audits[0].summary["path_offsets"] == "0/2/4"
