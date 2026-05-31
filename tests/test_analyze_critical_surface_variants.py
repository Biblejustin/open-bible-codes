from collections import Counter

from scripts.analyze_critical_surface_variants import count_delta_rows, format_counter


def test_count_delta_rows_reports_created_and_broken_counts() -> None:
    rows = count_delta_rows(Counter({"alpha": 2}), Counter({"alpha": 3, "beta": 1}))

    by_word = {row["normalized_word"]: row for row in rows}
    assert by_word["alpha"]["delta_sbl_minus_tr"] == 1
    assert by_word["beta"]["tr_count"] == 0
    assert format_counter(Counter({"alpha": 2, "beta": 1})) == "alpha:2;beta:1"
