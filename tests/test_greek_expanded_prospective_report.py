from scripts import build_greek_expanded_prospective_report as report


def test_surface_counts_sums_by_corpus() -> None:
    rows = [
        {
            "corpus": "TR_NT",
            "hit_count": "2",
            "context_hit_count": "1",
            "exact_center_hits": "1",
            "exact_span_hits": "0",
        },
        {
            "corpus": "TR_NT",
            "hit_count": "3",
            "context_hit_count": "2",
            "exact_center_hits": "0",
            "exact_span_hits": "1",
        },
    ]

    counts = report.surface_counts(rows)

    assert counts["TR_NT"]["hit_count"] == 5
    assert counts["TR_NT"]["context_hit_count"] == 3
    assert counts["TR_NT"]["exact_center_hits"] == 1
    assert counts["TR_NT"]["exact_span_hits"] == 1


def test_pattern_counts_handles_empty_matrix() -> None:
    counts = report.pattern_counts([])

    assert counts["scope_counts"] == {}


def test_top_exact_center_rows_limits_per_corpus() -> None:
    rows = [
        {
            "corpus": "TR_NT",
            "term_id": "b",
            "normalized_term": "βητα",
            "concept": "Beta",
            "exact_center_hits": "2",
        },
        {
            "corpus": "TR_NT",
            "term_id": "a",
            "normalized_term": "αλφα",
            "concept": "Alpha",
            "exact_center_hits": "5",
        },
        {
            "corpus": "TR_NT",
            "term_id": "c",
            "normalized_term": "γαμμα",
            "concept": "Gamma",
            "exact_center_hits": "0",
        },
    ]

    top = report.top_exact_center_rows(rows, limit_per_corpus=1)

    assert [row["term_id"] for row in top] == ["a"]


def test_display_report_term_adds_transliteration_and_english() -> None:
    text = report.display_report_term(
        {
            "normalized_term": "αμην",
            "concept": "Amen",
        }
    )

    assert text == "`αμην` (amen; English: Amen)"
