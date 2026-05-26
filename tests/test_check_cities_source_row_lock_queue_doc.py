import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_row_lock_queue_doc as check


class CitiesSourceRowLockQueueDocTests(unittest.TestCase):
    def test_current_cities_source_row_lock_queue_doc_passes(self) -> None:
        assert check.validate_cities_source_row_lock_queue_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "queue.md"
            rows = root / "rows.csv"
            summary = root / "summary.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            row = valid_row("cities_pdf_dp365a_p5_11", "4", "source_table_page")
            row["next_action"] = "Hebrew source: אבג"
            write_csv(rows, [row])
            write_csv(summary, valid_summary("1"))

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
            )

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_source_row_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "queue.md"
            rows = root / "rows.csv"
            summary = root / "summary.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            row = valid_row("cities_pdf_dp365a_p5_11", "4", "source_table_page")
            row["current_decision"] = "source_row_import"
            write_csv(rows, [row])
            write_csv(summary, valid_summary("1"))

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
            )

            self.assertTrue(any("imports source row" in failure for failure in failures))


def valid_doc_text() -> str:
    return """# Cities Source Row Lock Queue

Status: source-row lock planning record.
This does not import source rows. No OCR body text or source-script body text appears.

- Queue rows: 1.
- Unique labels: 1.
- Table-bearing candidate pages: 1.
- Source-list candidate pages: 0.
- Exception-note candidate pages: 0.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.

cities_pdf_dp365a_p5_11 source_table_page table_candidate_page
needs_citable_source_row_lock
This queue names page locations only.
"""


def valid_row(label: str, page: str, role: str) -> dict[str, str]:
    return {
        "lock_rank": "1",
        "label": label,
        "page_number": page,
        "family": "aumann_committee",
        "lane": "encoding_or_ocr_candidate",
        "visual_page_role": role,
        "page_class": "table_candidate_page",
        "packet_ocr_status": "page_ocr_text_detected",
        "packet_ocr_text_signal_chars": "900",
        "page_image_path": "reports/pages/page.png",
        "source_row_use": "no_source_row_use",
        "current_decision": "no_source_row_import",
        "lock_status": "needs_citable_source_row_lock",
        "next_action": "needs citable source-row lock",
        "claim_boundary": "source-row lock planning only",
    }


def valid_summary(queue_rows: str) -> list[dict[str, str]]:
    return [
        {"metric": "queue_rows", "value": queue_rows},
        {"metric": "unique_labels", "value": "1"},
        {"metric": "table_candidate_pages", "value": "1"},
        {"metric": "source_list_candidate_pages", "value": "0"},
        {"metric": "exception_note_candidate_pages", "value": "0"},
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


if __name__ == "__main__":
    unittest.main()
