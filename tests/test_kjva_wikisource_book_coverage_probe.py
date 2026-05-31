from scripts import analyze_kjva_wikisource_book_coverage_probe as probe


def test_build_book_rows_records_existing_and_redlink_statuses() -> None:
    html = b"""
    <a href="/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha/Volume_1/Genesis">Genesis</a>
    <a href="/w/index.php?title=The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha/Volume_3/Romans&action=edit&redlink=1">Romans</a>
    <a href="/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha/Volume_4/Tobit">Tobit</a>
    """

    rows = probe.build_book_rows(html)
    by_book = {row["expected_book"]: row for row in rows}

    assert by_book["Genesis"]["link_status"] == "existing"
    assert by_book["Genesis"]["volume"] == "1"
    assert by_book["Romans"]["link_status"] == "redlink"
    assert by_book["Romans"]["volume"] == "3"
    assert by_book["Tobit"]["link_status"] == "existing"
    assert by_book["Judith"]["link_status"] == "missing"


def test_build_summary_keeps_probe_non_result_bearing() -> None:
    rows = probe.build_book_rows(b"")
    summary = probe.build_summary(rows, fetch_status="fetched")

    assert summary["expected_kjv_books"] == 66
    assert summary["expected_apocrypha_books"] == 14
    assert summary["missing_apocrypha_book_links"] == 14
    assert summary["book_order_lock_ready"] is False
    assert summary["verse_import_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "coverage_probe_only_not_result_bearing"


def test_roman_book_aliases_match_expected_books() -> None:
    html = b"""
    <a href="/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha/Volume_1/I._Samuel">I. Samuel</a>
    <a href="/wiki/The_Holy_Bible,_containing_the_Old_%26_New_Testament_%26_the_Apocrypha/Volume_1/II._Kings">II. Kings</a>
    """

    rows = probe.build_book_rows(html)
    by_book = {row["expected_book"]: row for row in rows}

    assert by_book["1 Samuel"]["link_status"] == "existing"
    assert by_book["2 Kings"]["link_status"] == "existing"
