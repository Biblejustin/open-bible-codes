import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_transcription_review_worksheet as worksheet


class CitiesSourceTranscriptionReviewWorksheetTests(unittest.TestCase):
    def test_build_worksheet_rows_uses_locked_rows_only(self) -> None:
        rows = worksheet.build_worksheet_rows(
            [
                evidence_row("1", "table_candidate_page", "locked", "source_row_lock_ready"),
                evidence_row("2", "source_list_candidate_page", "unrecorded", ""),
            ]
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(
            rows[0]["transcription_decision_id"],
            "cities_source_transcription_001",
        )
        self.assertEqual(rows[0]["source_lock_decision_id"], "cities_source_row_lock_001")
        self.assertEqual(rows[0]["review_state"], worksheet.REVIEW_STATE)
        self.assertEqual(rows[0]["source_row_import"], "0")

    def test_build_worksheet_rows_reflects_existing_record(self) -> None:
        rows = worksheet.build_worksheet_rows(
            [evidence_row("1", "table_candidate_page", "locked", "source_row_lock_ready")],
            {
                "cities_source_transcription_001": record_row(
                    "cities_source_transcription_001",
                    "deferred_no_transcription",
                    "deferred_no_transcription",
                )
            },
        )

        self.assertEqual(rows[0]["current_transcription_status"], "deferred_no_transcription")
        self.assertEqual(rows[0]["current_selected_action"], "deferred_no_transcription")

    def test_rejects_source_row_import(self) -> None:
        row = evidence_row("1", "table_candidate_page", "locked", "source_row_lock_ready")
        row["current_decision"] = "source_row_import"

        with self.assertRaisesRegex(ValueError, "imports source rows"):
            worksheet.build_worksheet_rows([row])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.csv"
            records = root / "records.csv"
            out = root / "worksheet.csv"
            markdown = root / "worksheet.md"
            manifest = root / "manifest.json"
            write_csv(
                evidence,
                [
                    evidence_row(
                        "1",
                        "table_candidate_page",
                        "locked",
                        "source_row_lock_ready",
                    )
                ],
                worksheet_input_fieldnames(),
            )
            write_csv(records, [], worksheet.RECORD_FIELDS)

            rc = worksheet.main(
                [
                    "--evidence-packet",
                    str(evidence),
                    "--records-template",
                    str(records),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(len(rows), 1)
            self.assertIn(
                "Cities Source Transcription Review Worksheet",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["locked_source_pages"], 1)
            self.assertEqual(payload["source_row_imports"], 0)
            self.assertEqual(payload["p_levels"], 0)


def evidence_row(
    rank: str,
    page_class: str,
    status: str,
    action: str,
) -> dict[str, str]:
    return {
        "evidence_rank": rank,
        "decision_id": f"cities_source_row_lock_{int(rank):03d}",
        "queue_lock_rank": rank,
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": rank,
        "family": "aumann_committee",
        "page_class": page_class,
        "visual_page_role": "source_table_page",
        "source_url": "https://example.test/source.pdf",
        "selected_source": "archive",
        "selected_path": "reports/snapshots/source.pdf",
        "source_sha256": "abc123",
        "pdf_pages": "7",
        "page_image_path": "reports/pages/source.png",
        "record_decision_status": status,
        "record_selected_action": action,
        "evidence_prompt": "cite evidence",
        "evidence_required": "verify evidence",
        "source_row_use": "no_source_row_use",
        "current_decision": "no_source_row_import",
        "claim_boundary": "diagnostic only",
    }


def record_row(decision_id: str, status: str, action: str) -> dict[str, str]:
    return {
        "transcription_decision_id": decision_id,
        "source_lock_decision_id": "cities_source_row_lock_001",
        "source_label": "cities_pdf_dp365a_p5_11",
        "page_number": "1",
        "page_class": "table_candidate_page",
        "decision_status": status,
        "selected_action": action,
        "evidence_citation": "reports/example.csv:2",
        "evidence_summary": "test record",
        "locked_by": "tester",
        "locked_at": "2026-05-28",
        "notes": "test",
    }


def worksheet_input_fieldnames() -> list[str]:
    return [
        "evidence_rank",
        "decision_id",
        "queue_lock_rank",
        "label",
        "page_number",
        "family",
        "page_class",
        "visual_page_role",
        "source_url",
        "selected_source",
        "selected_path",
        "source_sha256",
        "pdf_pages",
        "page_image_path",
        "record_decision_status",
        "record_selected_action",
        "evidence_prompt",
        "evidence_required",
        "source_row_use",
        "current_decision",
        "claim_boundary",
    ]


def write_csv(
    path: Path,
    rows: list[dict[str, str]],
    fieldnames: list[str],
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
