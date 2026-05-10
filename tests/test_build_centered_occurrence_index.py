from pathlib import Path

from scripts.build_centered_occurrence_index import (
    all_codes_occurrences,
    apocrypha_bridge_occurrences,
    build_presence_summary,
    classify_occurrence,
    gog_source_occurrences,
    summary_markdown_row,
)


def test_classify_occurrence_separates_exact_word_from_surface_form() -> None:
    assert (
        classify_occurrence(
            {
                "normalized_term": "αιμα",
                "center_normalized_word": "αιμα",
                "bucket": "center_word_exact",
            }
        )
        == "centered_self_exact_word"
    )
    assert (
        classify_occurrence(
            {
                "normalized_term": "αιμα",
                "center_normalized_word": "αιματι",
                "bucket": "center_word_exact",
            }
        )
        == "centered_self_surface_form"
    )
    assert (
        classify_occurrence(
            {
                "normalized_term": "γωγ",
                "center_normalized_word": "Γὼγ",
            }
        )
        == "centered_self_exact_word"
    )


def test_classify_occurrence_keeps_relevant_center_buckets() -> None:
    assert (
        classify_occurrence(
            {
                "normalized_term": "edom",
                "center_normalized_word": "ammon",
                "bucket": "center_word_same_category",
            }
        )
        == "relevant_center_same_category"
    )
    assert (
        classify_occurrence(
            {
                "normalized_term": "messiah",
                "center_normalized_word": "savior",
                "bucket": "center_word_same_concept",
            }
        )
        == "relevant_center_same_concept"
    )
    assert (
        classify_occurrence(
            {
                "normalized_term": "messiah",
                "center_normalized_word": "savior",
                "context_bucket": "center_verse_exact",
            }
        )
        == "center_verse_relevant"
    )


def test_all_codes_occurrences_add_context_and_frequency_read() -> None:
    rows = all_codes_occurrences(
        [
            {
                "selection_rank": "1",
                "source_queue": "greek_screening",
                "bucket": "center_word_exact",
                "presence_scope": "all_source",
                "term_id": "blood_g",
                "concept": "Blood",
                "category": "worship",
                "normalized_term": "αιμα",
                "center_ref": "REV 19:13",
                "center_word": "αἵματι",
                "center_normalized_word": "αιματι",
                "skip": "-10",
                "direction": "backward",
                "path_rows": "4",
                "path_corpora": "TR_NT,BYZ_NT,TCG_NT,SBLGNT",
                "control_p": "0.05",
                "control_q": "0.10",
                "best_context": "exact_center",
                "review_note": "hidden term centered on same normalized surface word",
            }
        ],
        [
            {
                "selection_rank": "1",
                "center_verse_text": "and his garment was dipped in blood",
            }
        ],
    )

    assert len(rows) == 1
    assert rows[0]["occurrence_type"] == "centered_self_surface_form"
    assert rows[0]["frequency_read"] == "control q=0.10; control p=0.05"
    assert rows[0]["context_excerpt"] == "and his garment was dipped in blood"


def test_gog_source_occurrences_attach_frequency_caution() -> None:
    rows = gog_source_occurrences(
        [
            {
                "corpus": "TCG_NT",
                "normalized_term": "γωγ",
                "exact_center_paths": "4",
                "center_refs": "REV 20:8=4",
                "skip_values": "-17;17",
                "read": "promoted source retains exact-center hidden paths",
            }
        ],
        "length-3 matched-control rank desc 25/asc 1; controls above target 24; not frequency-promoted",
    )

    assert rows[0]["occurrence_type"] == "centered_self_exact_word"
    assert rows[0]["context_read"] == "hidden Gog centers on open Gog in Rev 20:8"
    assert "not frequency-promoted" in str(rows[0]["frequency_read"])


def test_apocrypha_bridge_occurrences_skip_hidden_path_only() -> None:
    rows = apocrypha_bridge_occurrences(
        [
            {
                "context_rank": "1",
                "corpus": "KJVA",
                "context_bucket": "span_exact",
                "bridge_type": "canonical_to_apocrypha",
                "term_ids": "eng_life",
                "concepts": "Life",
                "categories": "theology",
                "normalized_term": "life",
                "center_ref": "TOB 1:2",
                "center_word": "the",
                "center_normalized_word": "the",
                "skip": "-234",
                "direction": "backward",
                "center_verse_text": "the life of Tobit",
            },
            {
                "context_rank": "2",
                "corpus": "KJVA",
                "context_bucket": "hidden_path_only",
                "normalized_term": "nato",
            },
        ],
        source_family="kjv_apocrypha_bridge_context",
    )

    assert len(rows) == 1
    assert rows[0]["occurrence_type"] == "span_relevant"
    assert rows[0]["source_family"] == "kjv_apocrypha_bridge_context"
    assert rows[0]["context_excerpt"] == "the life of Tobit"


def test_presence_summary_collapses_same_term_center_across_corpora() -> None:
    rows = gog_source_occurrences(
        [
            {
                "corpus": "TCG_NT",
                "normalized_term": "γωγ",
                "exact_center_paths": "4",
                "center_refs": "REV 20:8=4",
                "skip_values": "-17;17",
                "read": "promoted source retains exact-center hidden paths",
            },
            {
                "corpus": "SBLGNT",
                "normalized_term": "γωγ",
                "exact_center_paths": "4",
                "center_refs": "Rev 20:8=4",
                "skip_values": "-7;7",
                "read": "comparison source also has exact-center hidden paths",
            },
        ],
        "not frequency-promoted",
    )

    summary = build_presence_summary(rows)

    assert len(summary) == 1
    assert summary[0]["corpora"] == "TCG_NT;SBLGNT"
    assert summary[0]["occurrence_rows"] == 2
    assert summary[0]["total_paths"] == 8
    assert summary[0]["center_ref"] == "REV 20:8"
    assert "English: Gog" in summary_markdown_row(summary[0])


def test_module_default_paths_are_relative() -> None:
    # Keeps the CLI portable across machines and external-drive layouts.
    from scripts import build_centered_occurrence_index as module

    assert isinstance(module.DEFAULT_OUT, Path)
    assert not module.DEFAULT_OUT.is_absolute()
