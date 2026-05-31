from array import array
from pathlib import Path
from types import SimpleNamespace

from els.corpus import Corpus, VerseSpan, WordSpan
from scripts.analyze_notable_passage_gaps import (
    Passage,
    TermRow,
    add_uniform_zero_q_values,
    merge_terms,
    classify_gap,
    cross_source_gap_rows,
    parse_ref,
    passage_span,
    restricted_term_ids_for_passages,
    read_thematic_chapter_targets,
    ref_number,
    term_allowed_for_passage,
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


def test_term_allowed_for_passage_uses_optional_term_filter() -> None:
    filtered = Passage(
        passage_id="thematic",
        concept="Thematic",
        category="test",
        language="hebrew",
        corpus_group="test",
        start_ref="Isa 53:1",
        end_ref="Isa 53:999",
        notes="",
        term_ids="servant_h; lamb_h",
    )
    open_passage = Passage(
        passage_id="open",
        concept="Open",
        category="test",
        language="hebrew",
        corpus_group="test",
        start_ref="Isa 53:1",
        end_ref="Isa 53:999",
        notes="",
    )
    servant = TermRow("servant_h", "Servant", "test", "hebrew", "עבד", "")
    gog = TermRow("gog_h", "Gog", "test", "hebrew", "גוג", "")

    assert term_allowed_for_passage(servant, filtered)
    assert not term_allowed_for_passage(gog, filtered)
    assert term_allowed_for_passage(gog, open_passage)


def test_restricted_term_ids_for_passages_returns_none_when_any_open_passage() -> None:
    filtered = Passage("filtered", "Filtered", "test", "hebrew", "test", "Isa 53:1", "Isa 53:999", "", "servant_h")
    open_passage = Passage("open", "Open", "test", "hebrew", "test", "Isa 53:1", "Isa 53:999", "")

    assert restricted_term_ids_for_passages([filtered]) == {"servant_h"}
    assert restricted_term_ids_for_passages([filtered, open_passage]) is None


def test_read_thematic_chapter_targets_uses_term_lookup(tmp_path: Path) -> None:
    terms_dir = tmp_path / "terms"
    terms_dir.mkdir()
    (terms_dir / "terms.csv").write_text(
        "term_id,concept,category,language,term,notes\n"
        "servant_h,Servant,servant_song,hebrew,עבד,\n",
        encoding="utf-8",
    )
    mappings = tmp_path / "thematic.csv"
    mappings.write_text(
        "mapping_id,term_id,concept,language,book,chapter_start,chapter_end,notes,locked_by,locked_at\n"
        "isa53_servant,servant_h,Servant,hebrew,Isa,53,53,Isaiah 53,test,2026-05-12\n",
        encoding="utf-8",
    )

    passages, terms = read_thematic_chapter_targets(mappings, terms_dir=terms_dir)

    assert len(passages) == 1
    assert passages[0].passage_id == "thematic_absence_isa53_servant"
    assert passages[0].start_ref == "Isa 53:1"
    assert passages[0].end_ref == "Isa 53:999"
    assert passages[0].term_ids == "servant_h"
    assert terms == [TermRow("servant_h", "Servant", "servant_song", "hebrew", "עבד", "")]


def test_merge_terms_keeps_primary_rows() -> None:
    primary = [TermRow("term", "Primary", "cat", "hebrew", "אמת", "primary")]
    extra = [TermRow("term", "Extra", "cat", "hebrew", "שקר", "extra")]

    assert merge_terms(primary, extra) == primary


def test_add_uniform_zero_q_values_only_scores_gap_rows() -> None:
    rows = [
        {
            "gap_class": "absent_in_passage_common_elsewhere",
            "uniform_zero_probability": "0.010000",
        },
        {
            "gap_class": "present_in_passage",
            "uniform_zero_probability": "0.001000",
        },
        {
            "gap_class": "low_in_passage_vs_uniform",
            "uniform_zero_probability": "0.020000",
        },
    ]

    add_uniform_zero_q_values(rows)

    assert rows[0]["uniform_zero_bh_q"] == "0.020000"
    assert rows[1]["uniform_zero_bh_q"] == ""
    assert rows[2]["uniform_zero_bh_q"] == "0.020000"


def test_cross_source_gap_rows_groups_passage_term_across_corpora() -> None:
    rows = [
        {
            "passage_id": "lev24",
            "passage_concept": "Leviticus 24",
            "passage_category": "notable_passage_gap",
            "language": "hebrew",
            "term_id": "gog_h",
            "concept": "Gog",
            "category": "prophetic",
            "normalized_term": "גוג",
            "corpus_label": "MT_WLC",
            "status": "eligible",
            "gap_class": "absent_in_passage_common_elsewhere",
        },
        {
            "passage_id": "lev24",
            "passage_concept": "Leviticus 24",
            "passage_category": "notable_passage_gap",
            "language": "hebrew",
            "term_id": "gog_h",
            "concept": "Gog",
            "category": "prophetic",
            "normalized_term": "גוג",
            "corpus_label": "UHB",
            "status": "eligible",
            "gap_class": "present_in_passage",
        },
        {
            "passage_id": "lev24",
            "passage_concept": "Leviticus 24",
            "passage_category": "notable_passage_gap",
            "language": "hebrew",
            "term_id": "gog_h",
            "concept": "Gog",
            "category": "prophetic",
            "normalized_term": "גוג",
            "corpus_label": "MAM",
            "status": "eligible",
            "gap_class": "low_in_passage_vs_uniform",
        },
    ]

    summary = cross_source_gap_rows(rows)

    assert len(summary) == 1
    assert summary[0]["gap_corpora"] == "MAM;MT_WLC"
    assert summary[0]["present_corpora"] == "UHB"
    assert summary[0]["gap_corpus_count"] == 2
    assert summary[0]["strongest_gap_class"] == "absent_in_passage_common_elsewhere"


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
        cross_source_out="cross.csv",
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
    cross_source_row = {
        "passage_id": "lev24",
        "passage_concept": "Leviticus 24 Blasphemy Law",
        "passage_category": "notable_passage_gap",
        "term_id": "npg_yhwh_h",
        "normalized_term": "יהוה",
        "concept": "YHWH",
        "gap_corpora": "MT_WLC",
        "present_corpora": "",
        "gap_corpus_count": 1,
        "strongest_gap_class": "absent_in_passage_common_elsewhere",
    }

    write_markdown(
        out,
        detail_rows=[detail_row],
        summary_rows=[summary_row],
        cross_source_rows=[cross_source_row],
        args=args,
    )

    text = out.read_text(encoding="utf-8")
    assert "## Declared Gap-Target Passages" in text
    assert "## Declared Gap-Target Detail" in text
    assert "Leviticus 24 Blasphemy Law" in text
    assert "Uniform Zero P" in text
    assert "Uniform Zero Q" in text
    assert "0.049787" in text
    assert "## Declared Gap-Target Cross-Source Summary" in text
    assert "Cross-source gap summary CSV" in text
