import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_cities_source_row_lock_evidence_packet as packet


class CitiesSourceRowLockEvidencePacketTests(unittest.TestCase):
    def test_build_packet_rows_joins_source_metadata(self) -> None:
        rows = packet.build_packet_rows(
            [
                worksheet_row("1", "cities_pdf_dp365a_p5_11", "table_candidate_page"),
                worksheet_row(
                    "2",
                    "cities_pdf_dp365a_appendix_7",
                    "source_list_candidate_page",
                ),
            ],
            [
                source_row("cities_pdf_dp365a_p5_11", "abc123"),
                source_row("cities_pdf_dp365a_appendix_7", "def456"),
            ],
        )

        self.assertEqual([row["evidence_rank"] for row in rows], ["1", "2"])
        self.assertEqual(rows[0]["source_sha256"], "abc123")
        self.assertIn("cities_source_row_lock_001", rows[0]["evidence_required"])
        self.assertEqual(rows[0]["source_row_use"], "no_source_row_use")

    def test_build_packet_rows_rejects_source_row_import(self) -> None:
        imported = worksheet_row("1", "cities_pdf_dp365a_p5_11", "table_candidate_page")
        imported["current_decision"] = "source_row_import"

        with self.assertRaisesRegex(ValueError, "imports source rows"):
            packet.build_packet_rows([imported], [source_row("cities_pdf_dp365a_p5_11", "abc")])

    def test_summary_counts_zero_imports(self) -> None:
        rows = packet.build_packet_rows(
            [
                worksheet_row("1", "cities_pdf_dp365a_p5_11", "table_candidate_page"),
                worksheet_row(
                    "2",
                    "cities_pdf_dp365a_p12_17",
                    "exception_note_candidate_page",
                ),
            ],
            [
                source_row("cities_pdf_dp365a_p5_11", "abc123"),
                source_row("cities_pdf_dp365a_p12_17", "def456"),
            ],
        )

        summary = {row["metric"]: row["value"] for row in packet.build_summary_rows(rows)}
        self.assertEqual(summary["evidence_rows"], "2")
        self.assertEqual(summary["source_row_imports"], "0")
        self.assertEqual(summary["els_runs"], "0")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            worksheet = root / "worksheet.csv"
            source_queue = root / "source_queue.csv"
            out = root / "packet.csv"
            summary = root / "summary.csv"
            markdown = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(
                worksheet,
                [worksheet_row("1", "cities_pdf_dp365a_p5_11", "table_candidate_page")],
            )
            write_csv(source_queue, [source_row("cities_pdf_dp365a_p5_11", "abc123")])

            rc = packet.main(
                [
                    "--worksheet",
                    str(worksheet),
                    "--source-queue",
                    str(source_queue),
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
            self.assertIn("Cities Source Row Lock Evidence Packet", markdown.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["source_row_imports"], 0)


def worksheet_row(rank: str, label: str, page_class: str) -> dict[str, str]:
    return {
        "worksheet_rank": rank,
        "decision_id": f"cities_source_row_lock_{int(rank):03d}",
        "queue_lock_rank": rank,
        "label": label,
        "page_number": rank,
        "family": "aumann_committee",
        "page_class": page_class,
        "visual_page_role": "source_table_page",
        "page_image_path": f"reports/pages/{label}_p{rank}.png",
        "required_decision_record": "cite evidence",
        "evidence_prompt": "cite page evidence",
        "suggested_decision_status_values": "unrecorded;locked;deferred_no_lock",
        "suggested_selected_action_values": "no_source_row_import;source_row_lock_ready",
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


def source_row(label: str, sha: str) -> dict[str, str]:
    return {
        "label": label,
        "url": f"https://example.test/{label}.pdf",
        "selected_source": "archive",
        "selected_path": f"reports/snapshots/{label}.pdf",
        "sha256": sha,
        "pdf_pages": "7",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
