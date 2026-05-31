from collections import Counter

from scripts.build_crd_broad_screening_findings import (
    format_distribution,
    top_bible_positive_secular_zero,
    top_finite_ratios,
)


def test_broad_screening_helpers_rank_ratios_and_zero_controls() -> None:
    rows = [
        {"ratio": "2", "bible_max_density": "5", "secular_max_density": "0"},
        {"ratio": "4", "bible_max_density": "3", "secular_max_density": "1"},
    ]

    assert top_finite_ratios(rows, limit=1)[0]["ratio"] == "4"
    assert top_bible_positive_secular_zero(rows, limit=1)[0]["bible_max_density"] == "5"
    assert format_distribution(Counter({2: 3, 1: 1})) == "3 terms in 2 corpus labels, 1 term in 1 corpus label"

