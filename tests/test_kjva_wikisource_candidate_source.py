from scripts import analyze_kjva_wikisource_candidate_source as analyzer


def test_analyze_candidate_marks_metadata_candidate() -> None:
    raw = (
        "<html><title>Ballantyne</title>"
        "King James standard version of 1769 Apocrypha public domain"
        "</html>"
    ).encode()

    row = analyzer.analyze_candidate(
        analyzer.SourceCandidate("wikisource_ballantyne_1911_kjva", analyzer.WIKISOURCE_URL),
        analyzer.FetchedPage(raw=raw, final_url=analyzer.WIKISOURCE_URL, fetch_status="fetched"),
    )

    assert row["source_audit_status"] == "source_candidate_needs_import"
    assert row["verse_numbered_import_ready"] is False
    assert row["result_ready_status"] == "not_result_ready"


def test_analyze_candidate_records_fetch_failure_without_ready_status() -> None:
    row = analyzer.analyze_candidate(
        analyzer.SourceCandidate("wikisource_ballantyne_1911_kjva", analyzer.WIKISOURCE_URL),
        analyzer.FetchedPage(
            raw=b"",
            final_url=analyzer.WIKISOURCE_URL,
            fetch_status="fetch_error",
            error="offline",
        ),
    )

    assert row["source_audit_status"] == "source_candidate_not_confirmed"
    assert row["bytes"] == 0
    assert row["sha256"] == ""
    assert row["verse_numbered_import_ready"] is False


def test_build_summary_keeps_non_result_boundary() -> None:
    row = analyzer.analyze_candidate(
        analyzer.SourceCandidate("wikisource_ballantyne_1911_kjva", analyzer.WIKISOURCE_URL),
        analyzer.FetchedPage(
            raw=b"King James standard version of 1769 Apocrypha Ballantyne public domain",
            final_url=analyzer.WIKISOURCE_URL,
            fetch_status="fetched",
        ),
    )

    summary = analyzer.build_summary([row])

    assert summary["source_pages"] == 1
    assert summary["source_candidate_pages"] == 1
    assert summary["verse_import_ready_pages"] == 0
    assert summary["result_ready_pages"] == 0
    assert summary["claim_status"] == "source_status_only_not_result_bearing"
