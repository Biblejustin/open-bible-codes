import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_row_lock_worksheet as worksheet


class CitiesSourceRowLockWorksheetTests(unittest.TestCase):
    def test_build_worksheet_rows_adds_ids_and_prompts(self) -> None:
        rows = worksheet.build_worksheet_rows(
            [
                queue_row("1", "cities_pdf_dp365a_p5_11", "4", "table_candidate_page"),
                queue_row(
                    "2",
                    "cities_pdf_dp365a_appendix_7",
                    "1",
                    "source_list_candidate_page",
                ),
            ]
        )

        self.assertEqual(rows[0]["decision_id"], "cities_source_row_lock_001")
        self.assertEqual(rows[1]["decision_id"], "cities_source_row_lock_002")
        self.assertIn("row/column boundary", rows[0]["evidence_prompt"])
        self.assertIn("list scope", rows[1]["evidence_prompt"])
        self.assertEqual(rows[0]["record_decision_status"], "unrecorded")

    def test_existing_record_is_reflected_without_importing_source_rows(self) -> None:
        rows = worksheet.build_worksheet_rows(
            [queue_row("1", "cities_pdf_dp365a_p5_11", "4", "table_candidate_page")],
            {
                "cities_source_row_lock_001": record_row(
                    "cities_source_row_lock_001",
                    "locked",
                    "source_row_lock_ready",
                )
            },
        )

        self.assertEqual(rows[0]["record_decision_status"], "locked")
        self.assertEqual(rows[0]["record_selected_action"], "source_row_lock_ready")
        self.assertEqual(rows[0]["source_row_use"], "no_source_row_use")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            queue_path = root / "queue.csv"
            records_path = root / "records.csv"
            out = root / "worksheet.csv"
            md = root / "worksheet.md"
            manifest = root / "manifest.json"
            write_csv(
                queue_path,
                [
                    queue_row("1", "cities_pdf_dp365a_p5_11", "4", "table_candidate_page"),
                    queue_row(
                        "2",
                        "cities_pdf_dp365a_p12_17",
                        "2",
                        "exception_note_candidate_page",
                    ),
                ],
            )
            write_csv(records_path, [], fieldnames=worksheet.RECORD_FIELDS)

            rc = worksheet.main(
                [
                    "--queue",
                    str(queue_path),
                    "--records-template",
                    str(records_path),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(len(rows), 2)
            self.assertIn("Cities Source Row Lock Worksheet", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 2)
            self.assertEqual(payload["recorded_rows"], 0)
            self.assertEqual(payload["source_row_imports"], 0)


def queue_row(
    rank: str,
    label: str,
    page: str,
    page_class: str,
) -> dict[str, str]:
    return {
        "lock_rank": rank,
        "label": label,
        "page_number": page,
        "family": "aumann_committee",
        "lane": "encoding_or_ocr_candidate",
        "visual_page_role": "source_table_page",
        "page_class": page_class,
        "packet_ocr_status": "page_ocr_text_detected",
        "packet_ocr_text_signal_chars": "900",
        "page_image_path": f"reports/pages/{label}_p{page}.png",
        "source_row_use": "no_source_row_use",
        "current_decision": "no_source_row_import",
        "lock_status": "needs_citable_source_row_lock",
        "next_action": "needs citable source-row lock",
        "claim_boundary": "source-row lock planning only",
    }


def record_row(decision_id: str, status: str, action: str) -> dict[str, str]:
    return {
        "decision_id": decision_id,
        "queue_lock_rank": "1",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "4",
        "page_class": "table_candidate_page",
        "decision_status": status,
        "selected_action": action,
        "evidence_citation": "reports/example.csv:2",
        "evidence_summary": "test lock",
        "locked_by": "tester",
        "locked_at": "2026-05-26",
        "notes": "test",
    }


def write_csv(
    path: Path,
    rows: list[dict[str, str]],
    fieldnames: list[str] | None = None,
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
