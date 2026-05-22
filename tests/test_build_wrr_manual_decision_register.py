import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_manual_decision_register as register


class WrrManualDecisionRegisterTests(unittest.TestCase):
    def test_build_register_rows_consolidates_lanes(self) -> None:
        rows = register.build_register_rows(
            [source_policy_row()],
            [row_checklist_row()],
            [remaining_row("page_image_near_match_review")],
        )

        self.assertEqual([row["decision_rank"] for row in rows], [1, 2, 3])
        self.assertEqual(rows[0]["decision_lane"], "source_policy_pair_rule")
        self.assertEqual(rows[1]["decision_lane"], "source_transcription_row_cluster")
        self.assertEqual(rows[2]["decision_lane"], "page_image_near_match")
        self.assertIn("No source correction", rows[0]["no_input_boundary"])

    def test_build_summary_rows_counts_terms_and_pairs(self) -> None:
        rows = register.build_register_rows(
            [source_policy_row()],
            [row_checklist_row()],
            [remaining_row("method_or_pair_universe_review")],
        )

        summary = register.build_summary_rows(rows)
        by_lane = {row["decision_lane"]: row for row in summary}

        self.assertEqual(by_lane["source_policy_pair_rule"]["action_terms"], 1)
        self.assertEqual(by_lane["source_transcription_row_cluster"]["action_terms"], 4)
        self.assertEqual(by_lane["method_pair_universe"]["frontier_pairs"], 1)

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_policy = root / "source_policy.csv"
            row_checklist = root / "row_checklist.csv"
            remaining = root / "remaining.csv"
            out = root / "register.csv"
            summary = root / "summary.csv"
            md = root / "register.md"
            manifest = root / "manifest.json"
            write_csv(source_policy, [source_policy_row()])
            write_csv(row_checklist, [row_checklist_row()])
            write_csv(remaining, [remaining_row("page_image_near_match_review")])

            rc = register.main(
                [
                    "--source-policy",
                    str(source_policy),
                    "--row-checklist",
                    str(row_checklist),
                    "--remaining",
                    str(remaining),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 3)
            self.assertIn("WRR Manual Decision Register", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 3)
            self.assertEqual(payload["action_terms"], 6)


def source_policy_row() -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "checklist_rank": "1",
        "review_state": "pending_source_policy_pair_rule_lock",
        "term_id": "wrr2_32_app_05",
        "term": "$LMHMX@LMA",
        "concept": "WRR2 32",
        "source_flags": "wnp_chelm_spelling_context",
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "required_decision_record": "cited source/pair-rule decision",
        "next_manual_action": "cite primary source/pair-rule evidence",
    }


def row_checklist_row() -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "row_rank": "1",
        "row_number": "06",
        "concept": "WRR2 06",
        "review_state": "pending_manual_source_lock",
        "action_terms": "4",
        "residual_pairs": "4",
        "frontier_pairs": "4",
        "terms_to_verify": "wrr2_06_app_03 B@LM@$YH$M",
        "required_decision_record": "explicit keep, correct, exclude decision",
        "next_manual_action": "review row image once before individual term decisions",
    }


def remaining_row(lane: str) -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "checklist_rank": "1",
        "action_lane": lane,
        "review_state": "pending_page_image_lock"
        if lane == "page_image_near_match_review"
        else "pending_method_pair_universe_lock",
        "term_id": "wrr2_19_app_11",
        "term": "YWSP+RANY",
        "concept": "WRR2 19",
        "row_number": "19",
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "required_decision_record": "explicit decision",
        "next_manual_action": "inspect page image",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
