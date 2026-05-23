import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_manual_decision_record_worksheet as worksheet


class WrrManualDecisionRecordWorksheetTests(unittest.TestCase):
    def test_build_worksheet_rows_adds_record_ids_and_prompts(self) -> None:
        rows = worksheet.build_worksheet_rows([register_row("2", "source_transcription_row_cluster")])

        self.assertEqual(rows[0]["decision_id"], "wrr_decision_002")
        self.assertEqual(rows[0]["register_decision_rank"], "2")
        self.assertIn("row image", rows[0]["evidence_prompt"])
        self.assertIn("row_transcription_update", rows[0]["suggested_selected_action_values"])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            register_path = root / "register.csv"
            out = root / "worksheet.csv"
            md = root / "worksheet.md"
            manifest = root / "manifest.json"
            write_csv(
                register_path,
                [
                    register_row("1", "source_policy_pair_rule"),
                    register_row("2", "source_transcription_row_cluster"),
                    register_row("24", "page_image_near_match"),
                    register_row("27", "method_pair_universe"),
                ],
            )

            rc = worksheet.main(
                [
                    "--register",
                    str(register_path),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 4)
            text = md.read_text(encoding="utf-8")
            self.assertIn("WRR Manual Decision Record Worksheet", text)
            self.assertIn("wrr_decision_027", text)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 4)
            self.assertEqual(payload["lane_counts"]["method_pair_universe"], 1)


def register_row(rank: str, lane: str) -> dict[str, str]:
    return {
        "decision_rank": rank,
        "decision_lane": lane,
        "review_state": "pending_manual_source_lock",
        "decision_target": "row 06",
        "concept": "WRR2 06",
        "row_number": "06",
        "term_id": "wrr2_06_app_03",
        "term": "B@LM@$YH$M",
        "action_terms": "1",
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "required_decision_record": "explicit keep, correct, exclude decision",
        "source_checklist": "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
        "no_input_boundary": "No source correction selected.",
        "allowed_without_input": "organize evidence only",
        "next_manual_action": "review row image",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
