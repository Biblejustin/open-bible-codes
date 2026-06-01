import csv
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_marker_coverage as audit
from scripts.analyze_kjva_hakkaac_apocrypha_boundary_candidate import TextPayload


def test_parse_index_links_resolves_hakkaac_relative_urls() -> None:
    links = audit.parse_index_links(
        '<a href="KJV_Tobit.html">Tobit</a>'
        '<a href="KJV_Prayer-of-Manasses.html">Prayer of Manasses</a>'
    )

    assert links["Tobit"].endswith("/KJV_Tobit.html")
    assert links["Prayer of Manasses"].endswith("/KJV_Prayer-of-Manasses.html")


def test_load_local_chapter_counts_reads_selected_books(tmp_path: Path) -> None:
    path = tmp_path / "kjva.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["ref", "book", "chapter", "verse", "text"])
        writer.writeheader()
        writer.writerow({"ref": "TOB 1:1", "book": "TOB", "chapter": "1", "verse": "1", "text": "x"})
        writer.writerow({"ref": "TOB 1:2", "book": "TOB", "chapter": "1", "verse": "2", "text": "x"})
        writer.writerow({"ref": "TOB 2:1", "book": "TOB", "chapter": "2", "verse": "1", "text": "x"})
        writer.writerow({"ref": "GEN 1:1", "book": "GEN", "chapter": "1", "verse": "1", "text": "x"})

    counts = audit.load_local_chapter_counts(path, books=(audit.BOOKS[0],))

    assert counts == {"TOB": {1: 2, 2: 1}}


def test_analyze_book_chapters_and_book_row_exact_match() -> None:
    book = audit.HakkaacBook("TOB", "Tobit", "Tobit", "Tobit")
    html = """
    <html><body>
    <p>Public domain outside the United Kingdom King James Bible</p>
    <h3>Tobit 1</h3><span>▽</span><sup>1</sup><p>one</p><sup>2</sup><p>two</p>
    <span>◁</span>
    <h3>Tobit 2</h3><span>▽</span><sup>1</sup><p>one</p>
    </body></html>
    """
    payload = TextPayload(html.encode(), "https://example.test/KJV_Tobit.html", "http_200")
    local = {1: 2, 2: 1}

    chapter_rows = audit.analyze_book_chapters(book, payload, local)
    book_row = audit.build_book_row(book, payload, chapter_rows, local)

    assert [row["source_marker_count"] for row in chapter_rows] == [2, 1]
    assert all(row["status"] == "exact_marker_match" for row in chapter_rows)
    assert book_row["source_total_markers"] == 3
    assert book_row["local_total_markers"] == 3
    assert book_row["status"] == "exact_marker_match"
    assert book_row["license_note_present"] is True


def test_build_summary_keeps_marker_audit_non_result_bearing() -> None:
    book_rows = [
        {
            "status": "exact_marker_match",
            "source_total_markers": 2,
            "local_total_markers": 2,
            "license_note_present": True,
        },
        {
            "status": "count_drift",
            "source_total_markers": 1,
            "local_total_markers": 2,
            "license_note_present": False,
        },
    ]
    chapter_rows = [
        {"status": "exact_marker_match"},
        {"status": "count_drift"},
    ]

    summary = audit.build_summary(book_rows, chapter_rows)

    assert summary["pages_scanned"] == 2
    assert summary["exact_book_marker_matches"] == 1
    assert summary["count_drift_books"] == 1
    assert summary["source_lock_ready"] is False
    assert summary["result_ready"] is False
    assert summary["claim_status"] == "marker_coverage_audit_only_not_result_bearing"
