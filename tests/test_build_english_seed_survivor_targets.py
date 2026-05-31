from scripts.build_english_seed_survivor_targets import build_rows


def test_build_rows_dedupes_by_corpus_and_term() -> None:
    audit_rows = [
        _row("KJV", "alpha", "2"),
        _row("KJV", "alpha", "9"),
        _row("BSB", "beta", "1"),
    ]

    rows = build_rows(audit_rows)

    assert [(row["corpus"], row["term_id"], row["hit_count"]) for row in rows] == [
        ("BSB", "beta", "1"),
        ("KJV", "alpha", "2"),
    ]


def _row(corpus: str, term_id: str, observed: str) -> dict[str, str]:
    return {
        "corpus": corpus,
        "term_id": term_id,
        "concept": term_id.title(),
        "category": "demo",
        "term": term_id,
        "normalized_term": term_id,
        "term_shuffle_observed": observed,
    }

