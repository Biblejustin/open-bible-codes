import csv
import json
import struct
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_page_review_bundle as bundle


class CitiesSourcePageReviewBundleTests(unittest.TestCase):
    def test_build_bundle_rows_records_image_dimensions_without_imports(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "page.png"
            write_png_header(image, 640, 480)
            rows = bundle.build_bundle_rows([worksheet_row(image)])

        self.assertEqual(rows[0]["page_image_exists"], "true")
        self.assertEqual(rows[0]["page_image_width"], "640")
        self.assertEqual(rows[0]["page_image_height"], "480")
        self.assertEqual(rows[0]["source_row_import"], "0")
        self.assertEqual(rows[0]["p_levels"], "0")

    def test_summary_counts_pages_and_zero_result_work(self) -> None:
        rows = [
            {
                **worksheet_row(Path("missing.png")),
                "page_class": "table_candidate_page",
            },
            {
                **worksheet_row(Path("missing2.png")),
                "page_class": "source_list_candidate_page",
            },
        ]
        bundle_rows = bundle.build_bundle_rows(rows)
        summary = {row["metric"]: row["value"] for row in bundle.build_summary_rows(bundle_rows)}

        self.assertEqual(summary["bundle_rows"], "2")
        self.assertEqual(summary["page_images_missing"], "2")
        self.assertEqual(summary["source_row_imports"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "page.png"
            write_png_header(image, 320, 200)
            worksheet = root / "worksheet.csv"
            out = root / "bundle.csv"
            summary = root / "summary.csv"
            markdown = root / "bundle.md"
            manifest = root / "manifest.json"
            write_csv(worksheet, [worksheet_row(image)], worksheet_fieldnames())

            rc = bundle.main(
                [
                    "--worksheet",
                    str(worksheet),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertIn(
                "Cities Source Page Review Bundle",
                markdown.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["summary"]["page_images_found"], "1")


def worksheet_row(image: Path) -> dict[str, str]:
    return {
        "transcription_rank": "1",
        "transcription_decision_id": "cities_source_transcription_001",
        "source_lock_decision_id": "cities_source_row_lock_001",
        "queue_lock_rank": "1",
        "label": "cities_pdf_dp365a_p5_11",
        "page_number": "3",
        "family": "aumann_committee",
        "page_class": "table_candidate_page",
        "visual_page_role": "source_table_page",
        "source_url": "https://example.test/source.pdf",
        "selected_source": "archive",
        "selected_path": "reports/source.pdf",
        "source_sha256": "abc123",
        "pdf_pages": "7",
        "page_image_path": str(image),
        "lock_record_decision_status": "locked",
        "lock_record_selected_action": "source_row_lock_ready",
        "review_state": "pending_readable_transcription",
        "required_source_evidence": "cite evidence",
        "required_alignment_evidence": "readable transcription",
        "required_decision_record": "record decision",
        "allowed_without_input": "organize transcription review only",
        "next_manual_action": "prepare row/column transcription plan",
        "source_row_import": "0",
        "city_name_normalization": "0",
        "els_runs": "0",
        "compactness_runs": "0",
        "p_levels": "0",
        "current_transcription_status": "unrecorded",
        "current_selected_action": "",
        "current_evidence_citation": "",
        "current_evidence_summary": "",
        "claim_boundary": "worksheet only",
    }


def worksheet_fieldnames() -> list[str]:
    return list(worksheet_row(Path("page.png")).keys())


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_png_header(path: Path, width: int, height: int) -> None:
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + struct.pack(">I", 13)
        + b"IHDR"
        + struct.pack(">II", width, height)
        + b"\x08\x02\x00\x00\x00"
        + b"\x00\x00\x00\x00"
    )


if __name__ == "__main__":
    unittest.main()
