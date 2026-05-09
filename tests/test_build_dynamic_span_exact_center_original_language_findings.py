from collections import Counter

from scripts.build_dynamic_span_exact_center_original_language_findings import (
    build_findings,
    classify_recommendation,
    finding_sort_key,
)


def review_row(
    *,
    review_rank: str,
    corpus: str,
    term: str,
    center_ref: str,
    center_word: str,
    paths: str = "1",
    control_read: str = "available language-matched control summary has zero exact-center rows for this normalized term",
) -> dict[str, str]:
    return {
        "review_rank": review_rank,
        "corpus": corpus,
        "term_id": f"term_{review_rank}",
        "normalized_term": term,
        "center_ref": center_ref,
        "center_word": center_word,
        "exact_center_paths": paths,
        "path_rows_joined": paths,
        "min_abs_skip": "2",
        "max_abs_skip": "100",
        "example_skip": "10",
        "example_direction": "forward",
        "example_start_ref": "START 1:1",
        "example_end_ref": "END 1:1",
        "example_rows_spanned": "4",
        "example_row_width": "10",
        "center_word_context": "before [center] after",
        "center_verse_excerpt": "verse",
        "control_read": control_read,
        "control_comparison": "control:0 exact-center rows",
    }


def test_classify_promotes_gog_centered_on_revelation_with_zero_control() -> None:
    row = review_row(
        review_rank="1",
        corpus="TCG_NT",
        term="γωγ",
        center_ref="REV 20:8",
        center_word="Γὼγ",
    )

    assert classify_recommendation(row) == "promote"


def test_classify_background_when_language_control_has_exact_center_rows() -> None:
    row = review_row(
        review_rank="2",
        corpus="UHB",
        term="ישוע",
        center_ref="NEH 8:17",
        center_word="יֵשׁ֨וּעַ",
        control_read="language-matched controls also produce exact-center rows; treat as background-rate warning",
    )

    assert classify_recommendation(row) == "background"


def test_classify_holds_daniel_messiah_despite_background_control() -> None:
    row = review_row(
        review_rank="3",
        corpus="EBIBLE_WLC",
        term="משיח",
        center_ref="DAN 9:26",
        center_word="מָשִׁ֖יחַ",
        control_read="language-matched controls also produce exact-center rows; treat as background-rate warning",
    )

    assert classify_recommendation(row) == "hold"


def test_build_findings_sorts_promote_then_hold_then_background() -> None:
    rows = [
        review_row(
            review_rank="2",
            corpus="UHB",
            term="ישוע",
            center_ref="NEH 8:17",
            center_word="יֵשׁ֨וּעַ",
            paths="85",
            control_read="language-matched controls also produce exact-center rows; treat as background-rate warning",
        ),
        review_row(
            review_rank="3",
            corpus="EBIBLE_WLC",
            term="משיח",
            center_ref="DAN 9:26",
            center_word="מָשִׁ֖יחַ",
            paths="1",
            control_read="language-matched controls also produce exact-center rows; treat as background-rate warning",
        ),
        review_row(
            review_rank="1",
            corpus="TCG_NT",
            term="γωγ",
            center_ref="REV 20:8",
            center_word="Γὼγ",
            paths="4",
        ),
    ]
    path_rows = [
        {"review_rank": "1"},
        {"review_rank": "1"},
        {"review_rank": "2"},
        {"review_rank": "3"},
    ]

    findings = build_findings(rows, path_rows, limit=0)

    assert [row["recommendation"] for row in findings] == ["promote", "hold", "background"]
    assert findings[0]["normalized_term"] == "γωγ"
    assert "clearest current centered-self/contextual occurrence" in str(
        findings[0]["manual_review_note"]
    )
    assert findings[1]["center_ref"] == "DAN 9:26"
    assert findings[2]["path_rows_joined"] == 1


def test_findings_sort_key_treats_lxx_zero_control_above_background() -> None:
    lxx = review_row(
        review_rank="4",
        corpus="LXX",
        term="ιησουσ",
        center_ref="JOS 8:3",
        center_word="Ἰησοῦς",
        paths="2",
    )
    background = review_row(
        review_rank="5",
        corpus="UHB",
        term="ישוע",
        center_ref="NEH 8:17",
        center_word="יֵשׁ֨וּעַ",
        paths="85",
        control_read="language-matched controls also produce exact-center rows; treat as background-rate warning",
    )

    path_counts: Counter[str] = Counter({"4": 2, "5": 85})

    assert finding_sort_key(lxx, path_counts) < finding_sort_key(background, path_counts)
