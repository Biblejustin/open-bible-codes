from collections import Counter

from scripts import build_hebrew_concordance_prospective_terms as builder


def test_build_terms_keeps_first_normalized_headword_with_step_counts() -> None:
    entries = [
        builder.StrongEntry("H9", "alpha", "alpha", "first", "n", "alpha", "heb"),
        builder.StrongEntry("H10", "alpha", "alpha", "duplicate", "n", "alpha", "heb"),
        builder.StrongEntry("H11", "beta", "beta", "second", "n", "beta", "heb"),
    ]

    rows = builder.build_terms(
        entries,
        step_counts=Counter({"H9": 2, "H10": 3, "H11": 0}),
        min_normalized_length=4,
        require_step_count=True,
    )

    assert [row.term_id for row in rows] == ["hcon_h0009"]
    assert "strong_ids=H9,H10" in rows[0].notes
    assert "step_tahot_count=5" in rows[0].notes

