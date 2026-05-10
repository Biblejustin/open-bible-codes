from scripts.analyze_targeted_terms import display_target_term


def test_display_target_term_adds_transliteration_and_english() -> None:
    row = {"normalized_term": "ιραν", "concept": "Iran"}

    assert display_target_term(row) == "`ιραν` (iran; English: Iran)"


def test_display_target_term_keeps_english_terms_plain() -> None:
    row = {"normalized_term": "gog", "concept": "Gog"}

    assert display_target_term(row) == "`gog`"
