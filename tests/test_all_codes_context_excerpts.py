from els.corpus import Corpus, VerseSpan, WordSpan
from scripts import build_all_codes_context_excerpts as context


def sample_corpus() -> Corpus:
    text = "αβγδεζηθ"
    verses = (
        VerseSpan("test", "Test 1:1", "Test", "1", "1", "αβ γδ", 0, 3, 4),
        VerseSpan("test", "Test 1:2", "Test", "1", "2", "εζ ηθ", 4, 7, 4),
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 1, "εζ", "εζ", 4, 5, 2),
        WordSpan("test", "Test 1:2", "Test", "1", "2", 2, "ηθ", "ηθ", 6, 7, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=verses,
        position_to_verse=(0, 0, 0, 0, 1, 1, 1, 1),
        words=words,
        position_to_word=(0, 0, 1, 1, 2, 2, 3, 3),
    )


def selected_row() -> dict[str, str]:
    return {
        "selection_rank": "1",
        "source_queue": "greek_screening",
        "bucket": "span_exact",
        "presence_scope": "all_source",
        "present_corpora": "TEST",
        "term_id": "term",
        "concept": "Term",
        "category": "test",
        "normalized_term": "εζ",
        "skip": "2",
        "direction": "forward",
        "offsets_by_corpus": "TEST:0/2/4",
        "center_word": "γδ",
        "center_normalized_word": "γδ",
    }


def test_excerpt_row_exports_center_and_span_text() -> None:
    row = context.excerpt_row(selected_row(), "TEST", sample_corpus(), 0, 2, 4)

    assert row["center_ref"] == "Test 1:1"
    assert row["span_refs"] == "Test 1:1; Test 1:2"
    assert row["center_verse_contains_normalized_term"] == "False"
    assert row["span_contains_normalized_term"] == "True"
    assert row["center_verse_text"] == "αβ γδ"
    assert "Test 1:2: εζ ηθ" in row["span_verse_text"]


def test_build_excerpt_rows_uses_present_corpora() -> None:
    rows = context.build_excerpt_rows([selected_row()], {"TEST": sample_corpus()})

    assert len(rows) == 1
    assert rows[0]["audit_corpus"] == "TEST"


def test_markdown_cell_escapes_pipes() -> None:
    assert context.md_cell("a|b\nc") == "a\\|b c"


def test_write_markdown_displays_original_language_term(tmp_path) -> None:
    row = context.excerpt_row(selected_row(), "TEST", sample_corpus(), 0, 2, 4)
    out = tmp_path / "context.md"

    context.write_markdown(
        out,
        [row],
        args=type("Args", (), {"markdown_row_limit": 10})(),
    )

    text = out.read_text(encoding="utf-8")
    assert "`εζ` (ez; English: Term)" in text
