import csv
from pathlib import Path

from scripts import check_kjva_gutenberg_book_coverage_probe_doc as check


def test_current_kjva_gutenberg_book_coverage_probe_doc_passes() -> None:
    assert check.validate_kjva_gutenberg_book_coverage_probe_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_gutenberg_book_coverage_probe_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "KJV book headings found: 66.",
        "KJV book headings found: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_gutenberg_book_coverage_probe_doc(
        doc,
        rows=None,
        summary=None,
        anchors=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_summary_status_drift_fails(tmp_path: Path) -> None:
    summary = tmp_path / "summary.csv"
    row = {
        "source_pages": "2",
        "fetched_plain_text_pages": "2",
        "kjv_plain_text_bytes": "10",
        "kjv_plain_text_sha256": "abc",
        "apocrypha_plain_text_bytes": "10",
        "apocrypha_plain_text_sha256": "def",
        "expected_kjv_books": "66",
        "found_kjv_book_headings": "65",
        "missing_kjv_book_headings": "1",
        "expected_apocrypha_books": "14",
        "found_apocrypha_book_headings": "13",
        "missing_apocrypha_book_headings": "1",
        "extra_apocrypha_source_headings": "1",
        "kjv_verse_markers": "31102",
        "apocrypha_chapter_verse_markers": "5636",
        "apocrypha_number_only_markers": "68",
        "apocrypha_total_verse_markers": "5704",
        "book_order_lock_ready": "False",
        "verse_import_ready": "False",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "coverage_probe_only_not_result_bearing",
    }
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.probe.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(summary)

    assert any("found_kjv_book_headings drifted" in failure for failure in failures)
    assert any("found_apocrypha_book_headings drifted" in failure for failure in failures)
