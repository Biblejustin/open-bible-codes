from scripts.build_dynamic_span_exact_center_original_language_review_packet import build_packet


def bundle_row(
    *,
    corpus: str = "UHB",
    corpus_class: str = "bible",
    term_id: str = "dyn_yeshua_h",
    normalized_term: str = "ישוע",
    center_ref: str = "EZR 2:2",
    center_word_index: str = "4",
    center_word: str = "יֵשׁ֡וּעַ",
) -> dict[str, str]:
    return {
        "rank": "1",
        "priority": "bible_exact_center",
        "corpus_class": corpus_class,
        "corpus": corpus,
        "term_id": term_id,
        "normalized_term": normalized_term,
        "center_ref": center_ref,
        "center_word_index": center_word_index,
        "center_word": center_word,
        "exact_center_paths": "1",
        "min_abs_skip": "7",
        "max_abs_skip": "7",
        "strong_extension_rows": "0",
        "best_extension": "",
        "best_extension_type": "",
        "best_extension_match_kind": "",
        "best_extension_examples": "",
        "center_word_context": "sons of [Yeshua] and brothers",
        "center_verse_excerpt": "demo verse excerpt",
    }


def exact_row(
    *,
    corpus: str = "UHB",
    term_id: str = "dyn_yeshua_h",
    normalized_term: str = "ישוע",
    center_ref: str = "EZR 2:2",
    center_word_index: str = "4",
    center_word: str = "יֵשׁ֡וּעַ",
    skip: str = "7",
    direction: str = "forward",
    start_ref: str = "EZR 1:1",
    end_ref: str = "EZR 3:3",
) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "term": normalized_term,
        "normalized_term": normalized_term,
        "skip": skip,
        "direction": direction,
        "span_letters": "21",
        "start_ref": start_ref,
        "center_ref": center_ref,
        "end_ref": end_ref,
        "center_word_index": center_word_index,
        "center_word": center_word,
        "start_offset": "10",
        "center_offset": "17",
        "end_offset": "31",
    }


def matrix_summary_row() -> dict[str, str]:
    return {
        "corpus": "UHB",
        "term": "ישוע",
        "normalized_term": "ישוע",
        "skip": "7",
        "direction": "forward",
        "row_width": "7",
        "min_row": "1",
        "max_row": "4",
        "min_col": "3",
        "max_col": "3",
        "rows_spanned": "4",
        "cols_spanned": "1",
        "start_ref": "EZR 1:1",
        "center_ref": "EZR 2:2",
        "end_ref": "EZR 3:3",
    }


def letter_rows() -> list[dict[str, str]]:
    letters = ["י", "ש", "ו", "ע"]
    return [
        {
            "corpus": "UHB",
            "term": "ישוע",
            "normalized_term": "ישוע",
            "skip": "7",
            "direction": "forward",
            "letter_index": str(index),
            "letter": letter,
            "row_width": "7",
            "row": str(index + 1),
            "col": "3",
            "ref": f"EZR {index + 1}:1",
            "word": f"word{index}",
            "start_ref": "EZR 1:1",
            "center_ref": "EZR 2:2",
            "end_ref": "EZR 3:3",
        }
        for index, letter in enumerate(letters)
    ]


def test_build_packet_filters_to_original_language_bible_and_joins_paths() -> None:
    bundle_rows = [
        bundle_row(),
        bundle_row(corpus="KJV", term_id="dyn_jesus_e", normalized_term="jesus", center_word="Jesus"),
        bundle_row(corpus="HEB_PBY_BIALIK", corpus_class="control"),
    ]
    exact_rows = [
        exact_row(),
        exact_row(corpus="KJV", term_id="dyn_jesus_e", normalized_term="jesus", center_word="Jesus"),
    ]
    exact_summary_rows = [
        {
            "corpus": "HEB_PBY_BIALIK",
            "normalized_term": "ישוע",
            "exact_center_rows": "1151",
            "exact_center_rows_per_million_hits": "5.56",
            "top_center_words": "ישוע:10",
        }
    ]

    review_rows, path_rows = build_packet(
        bundle_rows,
        exact_rows,
        [],
        [matrix_summary_row()],
        letter_rows(),
        exact_summary_rows,
        limit=0,
    )

    assert len(review_rows) == 1
    assert len(path_rows) == 1
    assert review_rows[0]["corpus"] == "UHB"
    assert review_rows[0]["path_rows_joined"] == 1
    assert review_rows[0]["example_rows_spanned"] == 4
    assert "background-rate warning" in str(review_rows[0]["control_read"])
    assert "HEB_PBY_BIALIK:1151 exact-center rows" in str(review_rows[0]["control_comparison"])
    assert "י@EZR 1:1:word0[r1,c3]" in str(path_rows[0]["letter_path"])


def test_build_packet_reports_zero_control_summary() -> None:
    bundle_rows = [
        bundle_row(
            corpus="TCG_NT",
            term_id="dyn_gog_g",
            normalized_term="γωγ",
            center_ref="REV 20:8",
            center_word_index="6",
            center_word="Γώγ",
        )
    ]
    exact_rows = [
        exact_row(
            corpus="TCG_NT",
            term_id="dyn_gog_g",
            normalized_term="γωγ",
            center_ref="REV 20:8",
            center_word_index="6",
            center_word="Γώγ",
            start_ref="REV 19:1",
            end_ref="REV 21:1",
        )
    ]
    exact_summary_rows = [
        {
            "corpus": "GRC_PERSEUS_HERODOTUS",
            "normalized_term": "γωγ",
            "exact_center_rows": "0",
            "exact_center_rows_per_million_hits": "0.0",
            "top_center_words": "",
        }
    ]

    review_rows, path_rows = build_packet(
        bundle_rows,
        exact_rows,
        [],
        [],
        [],
        exact_summary_rows,
        limit=0,
    )

    assert len(review_rows) == 1
    assert len(path_rows) == 1
    assert "zero exact-center rows" in str(review_rows[0]["control_read"])
    assert "GRC_PERSEUS_HERODOTUS:0 exact-center rows" in str(review_rows[0]["control_comparison"])
