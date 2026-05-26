import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_unreadable_pdf_ocr_page_review_doc as check


class CitiesUnreadablePdfOcrPageReviewDocTests(unittest.TestCase):
    def test_current_cities_unreadable_pdf_ocr_page_review_doc_passes(self) -> None:
        assert check.validate_cities_unreadable_pdf_ocr_page_review_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "review.md"
            rows = root / "rows.csv"
            summary = root / "summary.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            write_csv(
                rows,
                [
                    valid_row(
                        "cities_pdf_dp365a_p1_4",
                        "3",
                        "appendix_toc_or_index_page",
                        notes="Hebrew source: אבג",
                    ),
                    valid_row("cities_pdf_dp365a_p1_4", "4", "blank_or_separator_page"),
                    valid_row("cities_pdf_dp365a_p5_11", "1", "title_page"),
                ],
            )
            write_csv(summary, valid_summary())

            failures = check.validate_cities_unreadable_pdf_ocr_page_review_doc(
                doc,
                rows,
                summary,
            )

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_source_row_use(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "review.md"
            rows = root / "rows.csv"
            summary = root / "summary.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            source_row = valid_row(
                "cities_pdf_dp365a_p1_4",
                "3",
                "appendix_toc_or_index_page",
            )
            source_row["source_row_use"] = "source_row_candidate"
            write_csv(
                rows,
                [
                    source_row,
                    valid_row("cities_pdf_dp365a_p1_4", "4", "blank_or_separator_page"),
                    valid_row("cities_pdf_dp365a_p5_11", "1", "title_page"),
                ],
            )
            write_csv(summary, valid_summary())

            failures = check.validate_cities_unreadable_pdf_ocr_page_review_doc(
                doc,
                rows,
                summary,
            )

            self.assertTrue(any("allows source-row use" in failure for failure in failures))


def valid_doc_text() -> str:
    return """# Cities Unreadable PDF OCR Page Review

Status: manual page-image review record.
This does not track OCR body text. No OCR body text appears.

- Review rows: 3.
- Reviewed pages: 3.
- OCR-empty pages reviewed: 2.
- Low-signal pages reviewed: 3.
- Visual-text-present pages: 2.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.

cities_pdf_dp365a_p1_4 appendix_toc_or_index_page blank_or_separator_page
cities_pdf_dp365a_p5_11 title_page
Source-row decisions require separate citable decision records.
"""


def valid_row(label: str, page: str, role: str, *, notes: str = "") -> dict[str, str]:
    return {
        "review_rank": "1",
        "decision_id": f"{label}_{page}",
        "label": label,
        "page_number": page,
        "family": "aumann_committee",
        "lane": "encoding_or_ocr_candidate",
        "packet_ocr_status": "page_ocr_empty",
        "packet_ocr_text_signal_chars": "0",
        "page_image_path": "reports/pages/page.png",
        "visual_review_status": "reviewed",
        "visual_page_role": role,
        "visual_text_signal": "text_present",
        "ocr_read_status": "reviewed",
        "source_row_use": "no_source_row_use",
        "decision": "no_source_row_import",
        "reviewed_by": "tester",
        "reviewed_at": "2026-05-26",
        "notes": notes,
        "claim_boundary": "manual page-image review only",
    }


def valid_summary() -> list[dict[str, str]]:
    return [
        {"metric": "review_rows", "value": "3"},
        {"metric": "reviewed_pages", "value": "3"},
        {"metric": "ocr_empty_pages_reviewed", "value": "2"},
        {"metric": "low_signal_pages_reviewed", "value": "3"},
        {"metric": "visual_text_present_pages", "value": "2"},
        {"metric": "source_row_imports", "value": "0"},
        {"metric": "els_runs", "value": "0"},
        {"metric": "compactness_runs", "value": "0"},
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
