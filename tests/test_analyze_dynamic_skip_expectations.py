from scripts.analyze_dynamic_skip_expectations import recommendation


def test_recommendation_orders_runtime_risk_reasons() -> None:
    assert recommendation(100_001, 0, 1) == "requires_long_run_or_large_span_counter"
    assert recommendation(50, 0, 1_000_000_001) == "targeted_large_span_count_candidate"
    assert recommendation(50, 100_001, 1) == "count_but_expect_many_hits"
    assert recommendation(50, 1, 1) == "good_targeted_count_candidate"
    assert recommendation(50, 0.5, 1) == "rare_expected_target"

