from scripts import analyze_kjva_gutenberg_book_coverage_probe as probe


def test_build_book_rows_detects_book_heading_markers_only() -> None:
    raw = b"""
Book 01 Genesis
Book 40 Matthew
Book 66 Revelation
Baruch the son of Neriah is a body-text name, not a book heading.
"""

    rows = probe.build_book_rows(raw)
    by_book = {row["expected_book"]: row for row in rows}

    assert by_book["Genesis"]["status"] == "found"
    assert by_book["Genesis"]["found_book_number"] == "01"
    assert by_book["Matthew"]["status"] == "found"
    assert by_book["Revelation"]["status"] == "found"
    assert by_book["Baruch"]["status"] == "missing"


def test_build_book_rows_matches_apocrypha_heading_alias() -> None:
    raw = b"""
Book 67 First Esdras
Book 68 Prayer of Manasses
"""

    rows = probe.build_book_rows(raw)
    by_book = {row["expected_book"]: row for row in rows}

    assert by_book["1 Esdras"]["status"] == "found"
    assert by_book["Prayer of Manasseh"]["status"] == "found"


def test_build_summary_keeps_probe_non_result_bearing() -> None:
    fetched = probe.FetchedText(
        raw=b"Book 01 Genesis\nBook 40 Matthew\n",
        final_url=probe.TXT_URL,
        fetch_status="fetched",
    )
    rows = probe.build_book_rows(fetched.raw)

    summary = probe.build_summary(rows, fetched)

    assert summary["expected_kjv_books"] == 66
    assert summary["expected_apocrypha_books"] == 14
    assert summary["book_order_lock_ready"] is False
    assert summary["verse_import_ready"] is False
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "coverage_probe_only_not_result_bearing"
