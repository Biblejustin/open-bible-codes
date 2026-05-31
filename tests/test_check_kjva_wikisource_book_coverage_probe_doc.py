import csv
import tempfile
from pathlib import Path

from scripts import check_kjva_wikisource_book_coverage_probe_doc as checker


def test_current_doc_passes() -> None:
    assert checker.validate_kjva_wikisource_book_coverage_probe_doc() == []


def test_missing_required_phrase_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        doc = Path(tmp) / "probe.md"
        text = checker.DEFAULT_DOC.read_text(encoding="utf-8").replace(
            "Expected apocrypha/deuterocanon books checked: 14.",
            "Expected apocrypha/deuterocanon books checked: unknown.",
        )
        doc.write_text(text, encoding="utf-8")

        failures = checker.validate_kjva_wikisource_book_coverage_probe_doc(
            doc,
            rows=None,
            summary=None,
            anchors=None,
            manifest=None,
        )

    assert any("Expected apocrypha/deuterocanon books checked: 14." in failure for failure in failures)


def test_summary_drift_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        summary = Path(tmp) / "summary.csv"
        with summary.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=checker.probe.SUMMARY_FIELDNAMES,
            )
            writer.writeheader()
            writer.writerow(
                {
                    "source_pages": "1",
                    "fetched_pages": "1",
                    "expected_kjv_books": "66",
                    "existing_kjv_book_links": "36",
                    "redlinked_kjv_book_links": "30",
                    "missing_kjv_book_links": "0",
                    "expected_apocrypha_books": "14",
                    "existing_apocrypha_book_links": "1",
                    "redlinked_apocrypha_book_links": "0",
                    "missing_apocrypha_book_links": "13",
                    "book_order_lock_ready": "False",
                    "verse_import_ready": "False",
                    "result_ready": "False",
                    "claim_status": "coverage_probe_only_not_result_bearing",
                }
            )

        failures = checker.validate_kjva_wikisource_book_coverage_probe_doc(
            checker.DEFAULT_DOC,
            rows=None,
            summary=summary,
            anchors=None,
            manifest=None,
        )

    assert any("existing_apocrypha_book_links drifted" in failure for failure in failures)
