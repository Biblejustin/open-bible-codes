from scripts.select_control_target_pilot import select_pilot_rows


def test_select_pilot_rows_keeps_top_rows_and_skips_absent_terms() -> None:
    rows = [
        _row("MT_WLC", "top", 100),
        _row("MT_WLC", "second", 50),
        _row("MT_WLC", "absent", 0),
        _row("UHB", "utop", 80),
    ]

    selected = select_pilot_rows(rows, per_corpus=2, top_per_corpus=1)

    keys = {(row["corpus"], row["term_id"]) for row in selected}
    assert ("MT_WLC", "top") in keys
    assert ("MT_WLC", "absent") not in keys
    assert ("UHB", "utop") in keys


def _row(corpus: str, term_id: str, hits: int) -> dict[str, str]:
    return {
        "concept": term_id.title(),
        "corpus": corpus,
        "term_set": "demo",
        "term_id": term_id,
        "category": "demo",
        "term_language": "hebrew",
        "term": term_id,
        "normalized_term": term_id,
        "normalized_length": "4",
        "hit_count": str(hits),
        "status": "counted" if hits else "absent",
    }

