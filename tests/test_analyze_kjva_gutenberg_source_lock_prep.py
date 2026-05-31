from collections import OrderedDict

from scripts import analyze_kjva_gutenberg_source_lock_prep as prep


def test_parse_kjv_verse_marker_counts_by_book_number() -> None:
    text = """
Book 01 Genesis
01:001:001 sample
01:001:002 sample
02:001:001 sample
"""

    counts = prep.parse_kjv_verse_marker_counts(text)

    assert counts["01"]["count"] == 2
    assert counts["02"]["count"] == 1


def test_parse_apocrypha_sections_handles_split_heading_and_number_only() -> None:
    text = """
The Book of Baruch
1:1 sample
The Epistle [or Letter] of Jeremiah [Jeremy]
1:1 sample
The Song of the Three Holy Children
1 sample
The History of the Destruction of
Bel and the Dragon
1:1 sample
"""

    counts = prep.parse_apocrypha_source_sections(text)

    assert counts["BAR"]["count"] == 1
    assert counts["LJE_SOURCE"]["count"] == 1
    assert counts["S3Y"]["number_only"] == 1
    assert counts["BEL"]["count"] == 1


def test_build_book_shape_rows_rolls_epistle_into_baruch() -> None:
    local_counts = OrderedDict((book.code, 0) for book in prep.KJV_BOOKS)
    local_counts.update(
        OrderedDict(
            [
                ("TOB", 0),
                ("JDT", 0),
                ("ESG", 0),
                ("WIS", 0),
                ("SIR", 0),
                ("BAR", 2),
                ("S3Y", 1),
                ("SUS", 0),
                ("BEL", 1),
                ("1MA", 0),
                ("2MA", 0),
                ("1ES", 0),
                ("MAN", 1),
                ("2ES", 0),
            ]
        )
    )
    apocrypha = b"""
The Book of Baruch
1:1 sample
The Epistle [or Letter] of Jeremiah [Jeremy]
1:1 sample
The Song of the Three Holy Children
1 sample
The History of the Destruction of
Bel and the Dragon
1:1 sample
The Prayer of Manasses
"""

    rows = prep.build_book_shape_rows(b"", apocrypha, local_counts)
    by_book = {row["book"]: row for row in rows}

    assert by_book["BAR"]["gutenberg_marker_count"] == 2
    assert by_book["BAR"]["status"] == "exact_count_match"
    assert by_book["S3Y"]["gutenberg_marker_count"] == 1
    assert by_book["BEL"]["gutenberg_marker_count"] == 1
    assert by_book["MAN"]["status"] == "source_markers_missing"
    assert by_book["LJE_SOURCE"]["status"] == "extra_source_component_rolls_into_BAR"


def test_build_summary_keeps_source_lock_prep_non_result_bearing() -> None:
    local_counts = OrderedDict((book.code, 1) for book in prep.KJV_BOOKS)
    local_counts.update(OrderedDict((book.code, 1) for book in prep.APOCRYPHA_BOOKS))
    rows = [
        {
            "section": "kjv",
            "book": "GEN",
            "status": "exact_count_match",
            "gutenberg_marker_count": 1,
            "marker_shape": "book:chapter:verse",
        },
        {
            "section": "apocrypha",
            "book": "SIR",
            "status": "count_drift",
            "gutenberg_marker_count": 1,
            "marker_shape": "chapter:verse",
        },
        {
            "section": "apocrypha_extra_source_section",
            "book": "LJE_SOURCE",
            "status": "extra_source_component_rolls_into_BAR",
            "gutenberg_marker_count": 1,
            "marker_shape": "chapter:verse",
        },
    ]
    kjv = prep.TextPayload(b"abc", "kjv", "read_local", "ignored_local_path")
    apocrypha = prep.TextPayload(b"def", "apocrypha", "read_local", "ignored_local_path")

    summary = prep.build_summary(rows, kjv, apocrypha, local_counts)

    assert summary["plain_text_pages_scanned"] == 2
    assert summary["raw_text_retained"] is False
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "source_lock_prep_only_not_result_bearing"
