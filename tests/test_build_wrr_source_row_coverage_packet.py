import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_row_coverage_packet as packet


class WrrSourceRowCoveragePacketTests(unittest.TestCase):
    def test_build_packet_rows_keeps_related_visual_notes_separate(self) -> None:
        rows = packet.build_packet_rows(
            [
                row_checklist(
                    row_rank="1",
                    row_number="06",
                    action_terms="2",
                    terms_to_verify="wrr2_06_app_03 AAA;wrr2_06_app_04 BBB",
                )
            ],
            [
                source_queue(
                    row_numbers="06",
                    term_id="wrr2_06_app_01",
                    visual_review_note="same row note",
                )
            ],
        )

        self.assertEqual(rows[0]["direct_visual_terms"], "")
        self.assertEqual(rows[0]["related_visual_terms"], "wrr2_06_app_01")
        self.assertEqual(rows[0]["coverage_state"], "related_row_visual_triage_only")
        self.assertIn("do not transfer", rows[0]["next_manual_action"])
        self.assertIn("No row transcription", rows[0]["no_input_boundary"])

    def test_build_summary_rows_counts_direct_and_outside_rows(self) -> None:
        checklist = [
            row_checklist(
                row_rank="1",
                row_number="06",
                action_terms="1",
                terms_to_verify="wrr2_06_app_03 AAA",
            )
        ]
        queue = [
            source_queue("06", "wrr2_06_app_03", "direct note"),
            source_queue("07", "wrr2_07_app_01", "outside note"),
        ]
        packet_rows = packet.build_packet_rows(checklist, queue)
        summary = {row["metric"]: row for row in packet.build_summary_rows(packet_rows, checklist, queue)}

        self.assertEqual(summary["direct_visual_action_terms"]["value"], 1)
        self.assertEqual(
            summary["rows_with_direct_visual_action_term_coverage"]["value"], 1
        )
        self.assertEqual(
            summary["visual_triage_rows_outside_source_transcription_checklist"]["read"],
            "07",
        )

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row_checklist_path = root / "rows.csv"
            source_queue_path = root / "queue.csv"
            out = root / "packet.csv"
            summary_out = root / "summary.csv"
            md = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(
                row_checklist_path,
                [
                    row_checklist(
                        row_rank="1",
                        row_number="06",
                        action_terms="1",
                        terms_to_verify="wrr2_06_app_03 AAA",
                    )
                ],
            )
            write_csv(
                source_queue_path,
                [source_queue("06", "wrr2_06_app_04", "related note")],
            )

            rc = packet.main(
                [
                    "--row-checklist",
                    str(row_checklist_path),
                    "--source-queue",
                    str(source_queue_path),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary_out),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn("WRR Source Row Coverage Packet", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["summary"]["source_rows"], 1)


def row_checklist(
    *,
    row_rank: str,
    row_number: str,
    action_terms: str,
    terms_to_verify: str,
) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "row_rank": row_rank,
        "row_number": row_number,
        "concept": f"WRR2 {row_number}",
        "action_terms": action_terms,
        "residual_pairs": action_terms,
        "frontier_pairs": action_terms,
        "terms_to_verify": terms_to_verify,
    }


def source_queue(
    row_numbers: str,
    term_id: str,
    visual_review_note: str,
) -> dict[str, str]:
    return {
        "row_numbers": row_numbers,
        "term_id": term_id,
        "visual_review_note": visual_review_note,
        "visual_review_action": "review only",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
