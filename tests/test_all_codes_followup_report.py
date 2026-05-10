from scripts import build_all_codes_followup_report as report


def selected_rows() -> list[dict[str, str]]:
    return [
        {
            "selection_rank": "1",
            "source_queue": "greek_screening",
            "bucket": "center_word_exact",
            "presence_scope": "all_source",
            "term_id": "amen_g",
            "concept": "Amen",
            "category": "liturgical",
            "normalized_term": "αμην",
            "skip": "2",
            "direction": "forward",
            "center_ref": "1Cor 1:10",
            "center_word": "αμην",
            "center_normalized_word": "αμην",
            "best_context": "exact_center",
            "control_band": "",
            "control_p": "",
            "control_q": "",
            "control_read": "",
        },
        {
            "selection_rank": "2",
            "source_queue": "hebrew_screening",
            "bucket": "hidden_path_only",
            "presence_scope": "all_source",
            "term_id": "messiah_h",
            "concept": "Messiah",
            "category": "theology",
            "normalized_term": "משיח",
            "skip": "3",
            "direction": "forward",
            "center_ref": "Gen 1:1",
            "center_word": "ברא",
            "center_normalized_word": "ברא",
            "best_context": "hidden_path_only",
            "control_band": "",
            "control_p": "",
            "control_q": "",
            "control_read": "",
        },
    ]


def path_rows() -> list[dict[str, str]]:
    return [
        {"selection_rank": "1", "audit_corpus": "TR_NT", "matches_term": "True"},
        {"selection_rank": "1", "audit_corpus": "SBLGNT", "matches_term": "True"},
        {"selection_rank": "2", "audit_corpus": "MT_WLC", "matches_term": "True"},
        {"selection_rank": "2", "audit_corpus": "UHB", "matches_term": "True"},
    ]


def letter_rows() -> list[dict[str, str]]:
    return [
        {"selection_rank": "1"},
        {"selection_rank": "1"},
        {"selection_rank": "2"},
    ]


def extension_rows() -> list[dict[str, str]]:
    return [
        {
            "selection_rank": "1",
            "extension_rows": "2",
            "max_extension_length": "3",
            "best_extension_type": "term_plus_after",
            "best_extended_sequence": "αμηνη",
            "best_match_kind": "word",
            "best_audit_corpus": "TR_NT",
        },
        {
            "selection_rank": "2",
            "extension_rows": "1",
            "max_extension_length": "2",
            "best_extension_type": "after_match",
            "best_extended_sequence": "אב",
            "best_match_kind": "word",
            "best_audit_corpus": "MT_WLC",
        },
    ]


def test_build_summary_rows_classifies_surface_and_hidden_rows() -> None:
    rows = report.build_summary_rows(
        selected_rows(),
        path_rows(),
        letter_rows(),
        extension_rows(),
    )

    assert rows[0]["review_class"] == "same_surface_word_at_center"
    assert rows[0]["review_status"] == "strongest_manual_review"
    assert rows[0]["path_corpora"] == "SBLGNT,TR_NT"
    assert rows[0]["letter_rows"] == "2"
    assert rows[0]["compound_extension"] == "True"
    assert rows[0]["best_extended_sequence"] == "αμηνη"
    assert rows[1]["review_class"] == "hidden_path_only"
    assert rows[1]["review_status"] == "hidden_path_review"
    assert rows[1]["compound_extension"] == "False"


def test_review_status_holds_mismatches() -> None:
    assert report.review_status("center_word_exact", 1) == "audit_hold"


def test_build_report_states_no_claim_and_hidden_rows_retained() -> None:
    summary_rows = report.build_summary_rows(
        selected_rows(),
        path_rows(),
        letter_rows(),
        extension_rows(),
    )

    text = report.build_report(
        summary_rows=summary_rows,
        selection_manifest={"selected_rows": 2},
        path_manifest={"summary_rows": 4, "letter_rows": 3, "mismatches": 0},
        extensions_manifest={
            "selected_rows_with_extensions": 2,
            "selected_rows_with_compound_extensions": 1,
            "extension_rows": 3,
        },
        run_commit="abc123",
    )

    assert "not a claim" in text
    assert "hidden-path-only rows" in text
    assert "`strongest_manual_review`" in text
    assert "`hidden_path_review`" in text
    assert "Rows with compound same-skip extensions" in text
    assert "`αμην` (amen; English: Amen)" in text
    assert "`משיח` (Mashiach; English: Messiah)" in text
    assert "`αμηνη` (amene; English: hidden extension sequence)" in text
