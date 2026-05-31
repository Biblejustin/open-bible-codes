from scripts.analyze_morphology_counts import chapter_sort_key


def test_chapter_sort_key_sorts_numeric_before_text() -> None:
    assert sorted(["10", "2", "intro"], key=chapter_sort_key) == ["2", "10", "intro"]

