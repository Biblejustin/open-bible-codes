import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_row_lock_evidence_packet_doc as check


class CitiesSourceRowLockEvidencePacketDocTests(unittest.TestCase):
    def test_current_cities_source_row_lock_evidence_packet_doc_passes(self) -> None:
        assert check.validate_cities_source_row_lock_evidence_packet_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = root / "packet.md"
            rows = root / "rows.csv"
            summary = root / "summary.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            row = valid_row("cities_source_row_lock_001")
            row["evidence_required"] = "Hebrew source: אבג"
            write_csv(rows, [row])
            write_csv(summary, valid_summary("1"))

            failures = check.validate_cities_source_row_lock_evidence_packet_doc(
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
            doc = root / "packet.md"
            rows = root / "rows.csv"
            summary = root / "summary.csv"
            doc.write_text(valid_doc_text(), encoding="utf-8")
            row = valid_row("cities_source_row_lock_001")
            row["current_decision"] = "source_row_import"
            write_csv(rows, [row])
            write_csv(summary, valid_summary("1"))

            failures = check.validate_cities_source_row_lock_evidence_packet_doc(
                doc,
                rows,
                summary,
            )

            self.assertTrue(any("imports source row" in failure for failure in failures))


def valid_doc_text() -> str:
    return """# Cities Source Row Lock Evidence Packet

Status: diagnostic evidence packet for Cities source-row lock candidates.
It joins decision ids to PDF/source metadata and page-image paths.
It does not transcribe rows. No OCR body text or source-script body text appears.

- Evidence rows: 1.
- Unique labels: 1.
- Table-bearing candidate pages: 1.
- Source-list candidate pages: 0.
- Exception-note candidate pages: 0.
- Recorded decision rows: 0.
- Source-row imports: 0.
- ELS runs: 0.
- Compactness runs: 0.

cities_source_row_lock_001 cities_source_row_lock_014
This packet collects evidence locations only.
does not copy their body text
"""


def valid_row(decision_id: str) -> dict[str, str]:
    return {
        "evidence_rank": "1",
        "decision_id": decision_id,
        "queue_lock_rank": "1",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "1",
        "family": "aumann_committee",
        "page_class": "table_candidate_page",
        "visual_page_role": "source_table_page",
        "source_url": "https://example.test/source.pdf",
        "selected_source": "archive",
        "selected_path": "reports/source.pdf",
        "source_sha256": "abc123",
        "pdf_pages": "7",
        "page_image_path": "reports/page.png",
        "record_decision_status": "unrecorded",
        "record_selected_action": "",
        "evidence_prompt": "cite page evidence",
        "evidence_required": "verify page evidence",
        "source_row_use": "no_source_row_use",
        "current_decision": "no_source_row_import",
        "claim_boundary": "diagnostic evidence packet only",
    }


def valid_summary(rows: str) -> list[dict[str, str]]:
    return [
        {"metric": "evidence_rows", "value": rows},
        {"metric": "unique_labels", "value": "1"},
        {"metric": "table_candidate_pages", "value": "1"},
        {"metric": "source_list_candidate_pages", "value": "0"},
        {"metric": "exception_note_candidate_pages", "value": "0"},
        {"metric": "recorded_decision_rows", "value": "0"},
        {"metric": "source_row_imports", "value": "0"},
        {"metric": "els_runs", "value": "0"},
        {"metric": "compactness_runs", "value": "0"},
    ]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
