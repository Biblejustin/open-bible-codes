from scripts.build_english_version_context_review import first_hit_by_corpus_term, int_value


def test_first_hit_by_corpus_term_keeps_first_row() -> None:
    rows = [
        {"corpus": "KJV", "term_id": "alpha", "skip": "2"},
        {"corpus": "KJV", "term_id": "alpha", "skip": "3"},
    ]

    first = first_hit_by_corpus_term(rows)

    assert first[("KJV", "alpha")]["skip"] == "2"
    assert int_value("bad") == 0
    assert int_value("5") == 5

