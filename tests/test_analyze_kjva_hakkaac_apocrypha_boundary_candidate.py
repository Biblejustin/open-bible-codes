from scripts import analyze_kjva_hakkaac_apocrypha_boundary_candidate as audit


def test_extract_chapter_markers_reads_until_navigation_boundary() -> None:
    items = [
        "Other",
        "Sirach 44",
        "▷",
        "KJV",
        "△",
        "44",
        "▽",
        "1",
        "text",
        "2",
        "text",
        "23",
        "text",
        "◁",
        "Sirach 45",
        "1",
    ]

    assert audit.extract_chapter_markers(items, "Sirach 44") == [1, 2, 23]


def test_compact_markers_formats_single_range_and_sparse_values() -> None:
    assert audit.compact_markers([23]) == "23"
    assert audit.compact_markers([1, 2, 3]) == "1..3"
    assert audit.compact_markers([1, 3, 5]) == "1;3;5"


def test_classify_candidate_records_sirach_and_prayer_candidates() -> None:
    sirach = audit.CANDIDATES[0]
    prayer = audit.CANDIDATES[1]

    assert (
        audit.classify_candidate(sirach, "all_target_markers_present")
        == "sirach_marker_gap_candidate_not_source_lock"
    )
    assert (
        audit.classify_candidate(prayer, "all_target_markers_present")
        == "prayer_boundary_candidate_not_source_lock"
    )


def test_build_summary_keeps_candidate_non_result_bearing() -> None:
    rows = [
        {
            "page_id": "hakkaac_sirach_44",
            "license_note_present": True,
            "marker_count": 23,
            "markers_present": "1..23",
            "target_status": "all_target_markers_present",
        },
        {
            "page_id": "hakkaac_manasseh_1",
            "license_note_present": True,
            "marker_count": 15,
            "markers_present": "1..15",
            "target_status": "all_target_markers_present",
        },
    ]

    summary = audit.build_summary(rows)

    assert summary["pages_scanned"] == 2
    assert summary["license_note_pages"] == 2
    assert summary["candidate_resolves_sirach"] is True
    assert summary["candidate_resolves_prayer"] is True
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
