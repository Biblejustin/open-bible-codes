import csv
import json
from pathlib import Path

from scripts import analyze_kjva_hakkaac_apocrypha_marker_coverage as audit
from scripts import check_kjva_hakkaac_apocrypha_marker_coverage_doc as check


def test_current_marker_coverage_doc_passes() -> None:
    failures = check.validate_kjva_hakkaac_apocrypha_marker_coverage_doc()

    assert failures == []


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "doc.md"
    doc.write_text("# KJVA Hakkaac Apocrypha Marker Coverage\n", encoding="utf-8")

    failures = check.validate_kjva_hakkaac_apocrypha_marker_coverage_doc(
        doc,
        rows=None,
        chapter_rows=None,
        summary=None,
        manifest=None,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_book_row_drift_fails(tmp_path: Path) -> None:
    path = tmp_path / "rows.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit.BOOK_ROW_FIELDNAMES)
        writer.writeheader()
        for book in audit.BOOKS:
            writer.writerow(
                {
                    "book": book.book,
                    "title": book.title,
                    "chapter_prefix": book.chapter_prefix,
                    "source_url": "https://example.test",
                    "source_status": "http_200",
                    "bytes": "1",
                    "sha256": "x",
                    "license_note_present": "True",
                    "source_chapters": "1",
                    "local_chapters": "1",
                    "source_total_markers": "1",
                    "local_total_markers": "1",
                    "chapter_drift_rows": "0",
                    "status": "exact_marker_match",
                    "candidate_status": "hakkaac_exact_marker_match_candidate_not_source_lock",
                    "notes": "x",
                }
            )

    failures = check.validate_rows_csv(path)

    assert any("source marker total drifted" in failure for failure in failures)


def test_summary_drift_fails(tmp_path: Path) -> None:
    path = tmp_path / "summary.csv"
    row = {
        "pages_scanned": "14",
        "local_books_compared": "14",
        "exact_book_marker_matches": "13",
        "count_drift_books": "1",
        "source_total_markers": "5719",
        "local_total_markers": "5720",
        "chapter_rows": "173",
        "chapter_drift_rows": "1",
        "license_note_pages": "14",
        "source_lock_ready": "False",
        "result_ready": "False",
        "claim_status": "marker_coverage_audit_only_not_result_bearing",
    }
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=audit.SUMMARY_FIELDNAMES)
        writer.writeheader()
        writer.writerow(row)

    failures = check.validate_summary_csv(path)

    assert any("exact_book_marker_matches drifted" in failure for failure in failures)
    assert any("source_total_markers drifted" in failure for failure in failures)


def test_manifest_boundary_drift_fails(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "claim_boundary": "bad",
                "text_retention": "no Bible text written to tracked outputs",
                "row_count": 14,
                "chapter_row_count": 173,
                "outputs": {"markdown": "doc.md"},
            }
        ),
        encoding="utf-8",
    )

    failures = check.validate_manifest(manifest, doc=Path("doc.md"))

    assert any("claim_boundary drifted" in failure for failure in failures)
