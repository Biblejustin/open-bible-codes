import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_transcription_row_review_checklist as checklist


class WrrSourceTranscriptionRowReviewChecklistTests(unittest.TestCase):
    def test_build_checklist_rows_preserves_no_input_boundary(self) -> None:
        rows = checklist.build_checklist_rows(
            [
                row_summary(
                    row_rank="1",
                    row_number="06",
                    concept="WRR2 06",
                    action_terms="4",
                    residual_pairs="4",
                    frontier_pairs="4",
                )
            ]
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["review_state"], "pending_manual_source_lock")
        self.assertEqual(rows[0]["allowed_without_input"], "organize evidence only")
        self.assertIn("No row transcription", rows[0]["no_input_boundary"])
        self.assertIn("review row image once", rows[0]["next_manual_action"])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row_summary_path = root / "rows.csv"
            out = root / "checklist.csv"
            md = root / "checklist.md"
            manifest = root / "manifest.json"
            write_csv(
                row_summary_path,
                [
                    row_summary(
                        row_rank="1",
                        row_number="06",
                        concept="WRR2 06",
                        action_terms="4",
                        residual_pairs="4",
                        frontier_pairs="4",
                    )
                ],
            )

            rc = checklist.main(
                [
                    "--row-summary",
                    str(row_summary_path),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn(
                "WRR Source-Transcription Row Review Checklist",
                md.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["action_terms"], 4)


def row_summary(
    *,
    row_rank: str,
    row_number: str,
    concept: str,
    action_terms: str,
    residual_pairs: str,
    frontier_pairs: str,
) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "row_rank": row_rank,
        "row_number": row_number,
        "concept": concept,
        "action_terms": action_terms,
        "residual_pairs": residual_pairs,
        "frontier_pairs": frontier_pairs,
        "action_terms_display": "wrr2_06_app_03 B@LM@$YH$M",
        "row_matched_terms": "wrr2_06_app_01 M@$YH$M",
        "row_ocr_name_texts": "מעשיהשממעשייהוה",
        "row_ocr_date_texts": "כבכסלובכבכסלוכבבכסלו",
        "table2_bridge_read": "Primary English row label and secondary WRR2 record align.",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
