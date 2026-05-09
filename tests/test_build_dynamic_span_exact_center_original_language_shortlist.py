from scripts.build_dynamic_span_exact_center_original_language_shortlist import build_shortlist


def row(
    *,
    rank: str,
    corpus_class: str = "bible",
    corpus: str = "UHB",
    priority: str = "bible_exact_center",
    paths: str = "1",
    strong: str = "0",
) -> dict[str, str]:
    return {
        "rank": rank,
        "priority": priority,
        "corpus_class": corpus_class,
        "corpus": corpus,
        "term_id": "term",
        "normalized_term": "ישוע",
        "center_ref": "EZR 2:2",
        "center_word": "יֵשׁ֡וּעַ",
        "exact_center_paths": paths,
        "min_abs_skip": "2",
        "max_abs_skip": "20",
        "strong_extension_rows": strong,
        "best_extension": "",
        "best_extension_type": "",
        "best_extension_match_kind": "",
        "best_extension_examples": "",
        "matrix_paths": paths,
        "matrix_min_rows_spanned": "5",
        "matrix_max_rows_spanned": "5",
        "center_word_context": "context",
        "center_verse_excerpt": "verse",
    }


def test_shortlist_keeps_original_language_bible_rows_only() -> None:
    rows = [
        row(rank="1", corpus="UHB"),
        row(rank="2", corpus="KJV"),
        row(rank="3", corpus_class="control", corpus="HEB_PBY_BIALIK"),
        row(rank="4", corpus="LXX"),
    ]

    shortlist = build_shortlist(rows, limit=0)

    assert [item["corpus"] for item in shortlist] == ["UHB", "LXX"]


def test_shortlist_prefers_strong_extensions_then_path_count() -> None:
    rows = [
        row(rank="3", corpus="LXX", paths="50"),
        row(
            rank="2",
            corpus="UHB",
            priority="bible_exact_center_with_strong_extension",
            paths="2",
            strong="1",
        ),
        row(rank="1", corpus="SBLGNT", paths="100"),
    ]

    shortlist = build_shortlist(rows, limit=0)

    assert [item["corpus"] for item in shortlist] == ["UHB", "SBLGNT", "LXX"]
    assert [item["shortlist_rank"] for item in shortlist] == [1, 2, 3]
