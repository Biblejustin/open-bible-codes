from els.corpus import Corpus, VerseSpan, WordSpan
from scripts import analyze_all_codes_letter_paths as paths


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
        "selection_rank": "1",
        "source_queue": "greek_screening",
        "selection_reason": "test",
        "bucket": "center_word_exact",
        "presence_scope": "all_source",
        "present_corpora": "TEST",
        "term_id": "term",
        "concept": "Term",
        "category": "test",
        "term": "αγε",
        "normalized_term": "αγε",
        "skip": "2",
        "direction": "forward",
        "offsets_by_corpus": "TEST:0/2/4",
    }


def test_parse_offsets_by_corpus() -> None:
    assert paths.parse_offsets_by_corpus("TR_NT:1/3/5; SBLGNT:2/4/6") == {
        "TR_NT": (1, 3, 5),
        "SBLGNT": (2, 4, 6),
    }


def test_audit_row_reconstructs_sequence_and_selected_metadata() -> None:
    audit = paths.audit_row(selected_row(), "TEST", sample_corpus(), 0, 2, 4)

    assert audit.summary["sequence"] == "αγε"
    assert audit.summary["matches_term"] == "True"
    assert audit.summary["source_queue"] == "greek_screening"
    assert audit.summary["audit_corpus"] == "TEST"
    assert audit.summary["path_refs"] == "Test 1:1"
    assert audit.summary["audit_center_word"] == "γδ"
    assert [row["letter"] for row in audit.letters] == ["α", "γ", "ε"]
    assert [row["word"] for row in audit.letters] == ["αβ", "γδ", "εζ"]


def test_audit_row_handles_backward_skip() -> None:
    row = {**selected_row(), "normalized_term": "εγα", "skip": "-2"}

    audit = paths.audit_row(row, "TEST", sample_corpus(), 4, 2, 0)

    assert audit.summary["sequence"] == "εγα"
    assert audit.summary["matches_term"] == "True"
    assert audit.summary["path_offsets"] == "4/2/0"


def test_build_audits_uses_present_corpora_and_offsets() -> None:
    audits = paths.build_audits([selected_row()], {"TEST": sample_corpus()})

    assert len(audits) == 1
    assert audits[0].summary["audit_corpus"] == "TEST"
    assert audits[0].summary["path_offsets"] == "0/2/4"


def test_letter_path_read_lines_distinguishes_center_word_from_requirement() -> None:
    lines = paths.letter_path_read_lines([{"matches_term": "True"}], [])

    text = "\n".join(lines)
    assert "not a requirement" in text
    assert "hidden-path-only" in text


def test_markdown_displays_original_language_terms_with_gloss(tmp_path) -> None:
    markdown = tmp_path / "paths.md"
    args = type(
        "Args",
        (),
        {
            "title": "Letter Paths",
            "status": "test",
            "selected": "selected.csv",
            "markdown_row_limit": 10,
        },
    )()
    summary = {
        **selected_row(),
        "audit_corpus": "TEST",
        "sequence": "αγε",
        "matches_term": "True",
        "audit_center_ref": "Test 1:1",
        "audit_center_word": "γδ",
        "path_refs": "Test 1:1",
    }

    paths.write_markdown(markdown, [selected_row()], [summary], [], args)

    text = markdown.read_text(encoding="utf-8")
    assert "`αγε` (age; English: Term)" in text
    assert "`γδ` (gd)" in text
