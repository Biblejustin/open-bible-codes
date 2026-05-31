from scripts.benchmark_protocol import safe_name, summary_stats, tail


def test_summary_stats_and_name_helpers() -> None:
    stats = summary_stats([1.0, 2.0, 3.0])

    assert stats["median"] == 2.0
    assert stats["count"] == 3
    assert safe_name("a/b c") == "a_b_c"
    assert tail("abcdef", limit=3) == "def"

