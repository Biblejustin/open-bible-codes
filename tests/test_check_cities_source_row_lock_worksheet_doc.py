import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_row_lock_worksheet_doc as check


class CitiesSourceRowLockWorksheetDocTests(unittest.TestCase):
    def test_current_cities_source_row_lock_worksheet_doc_passes(self) -> None:
        assert check.validate_cities_source_row_lock_worksheet_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "worksheet.md"
            rows = root / "rows.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            row = valid_row("cities_source_row_lock_001")
            row["evidence_prompt"] = "Hebrew source: אבג"
            write_csv(rows, [row])

            failures = check.validate_cities_source_row_lock_worksheet_doc(doc, rows)

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_recorded_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "worksheet.md"
            rows = root / "rows.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            row = valid_row("cities_source_row_lock_001")
            row["record_selected_action"] = "source_row_lock_ready"
            write_csv(rows, [row])

            failures = check.validate_cities_source_row_lock_worksheet_doc(doc, rows)

            self.assertTrue(any("selected action" in failure for failure in failures))


def valid_doc_text() -> str:
    return """# Cities Source Row Lock Worksheet

Status: worksheet plus current Cities source-row lock decision-record status.
This does not update either file. No OCR body text or source-script body text appears.

- Worksheet rows: 1.
- Table-bearing candidate pages: 1.
- Source-list candidate pages: 0.
- Exception-note candidate pages: 0.
- Recorded decision rows: 0.
- Locked decision rows: 0.
- Unrecorded decision rows: 1.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.
- Recorded selected actions: none.

source_row_lock_ready cities_source_row_lock_001 cities_source_row_lock_014
never imports or transcribes source rows
"""


def valid_row(decision_id: str) -> dict[str, str]:
    return {
        "worksheet_rank": "1",
        "decision_id": decision_id,
        "queue_lock_rank": "1",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "4",
        "family": "aumann_committee",
        "page_class": "table_candidate_page",
        "visual_page_role": "source_table_page",
        "page_image_path": "reports/pages/page.png",
        "required_decision_record": "cite evidence",
        "evidence_prompt": "cite page evidence",
        "suggested_decision_status_values": "unrecorded;locked;deferred_no_lock",
        "suggested_selected_action_values": (
            "no_source_row_import;source_row_lock_ready;"
            "exclude_page_from_source_rows;deferred_no_lock"
        ),
        "current_lock_status": "needs_citable_source_row_lock",
        "source_row_use": "no_source_row_use",
        "current_decision": "no_source_row_import",
        "record_decision_status": "unrecorded",
        "record_selected_action": "",
        "record_locked_by": "",
        "record_locked_at": "",
        "record_evidence_citation": "",
        "record_evidence_summary": "",
        "claim_boundary": "worksheet only",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
