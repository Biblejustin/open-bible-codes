import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
from pathlib import Path

from scripts import check_kjva_gutenberg_source_lock_prep_doc as check


def test_current_kjva_gutenberg_source_lock_prep_doc_passes() -> None:
    assert check.validate_kjva_gutenberg_source_lock_prep_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    missing = tmp_path / "missing.md"

    failures = check.validate_kjva_gutenberg_source_lock_prep_doc(missing)

    assert failures == [f"{missing} is missing"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "KJV exact count matches: 66.",
        "KJV exact count matches: unknown.",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_kjva_gutenberg_source_lock_prep_doc(
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
        "plain_text_pages_scanned": "2",
        "raw_text_retained": "False",
        "kjv_plain_text_bytes": "10",
        "kjv_plain_text_sha256": "abc",
        "apocrypha_plain_text_bytes": "10",
        "apocrypha_plain_text_sha256": "def",
        "local_kjva_books": "80",
        "local_kjva_verses": "36822",
        "local_kjva_kjv_verses": "31102",
        "local_kjva_apocrypha_verses": "5720",
        "book_shape_rows": "81",
        "local_book_rows_compared": "80",
        "kjv_books_compared": "66",
        "kjv_books_exact_count_matches": "65",
        "kjv_books_count_drift": "1",
        "apocrypha_books_compared": "14",
        "apocrypha_books_exact_count_matches": "11",
        "apocrypha_books_count_drift": "3",
        "extra_source_sections": "1",
        "gutenberg_kjv_verse_markers": "31102",
        "gutenberg_apocrypha_chapter_verse_markers": "5636",
        "gutenberg_apocrypha_number_only_markers": "68",
        "gutenberg_apocrypha_total_verse_like_markers": "5704",
        "baruch_epistle_split_detected": "True",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "source_lock_prep_only_not_result_bearing",
    }
    with summary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.prep.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(summary)

    assert any("kjv_books_exact_count_matches drifted" in failure for failure in failures)
    assert any(
        "apocrypha_books_exact_count_matches drifted" in failure
        for failure in failures
    )
