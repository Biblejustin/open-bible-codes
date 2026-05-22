import csv
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_claim_blocker_packet as packet


class WrrClaimBlockerPacketTests(unittest.TestCase):
    def test_build_packet_rows_combines_readiness_options_and_source_flags(self) -> None:
        rows = packet.build_packet_rows(
            readiness_rows=[
                {
                    "decision_area": "Pair universe",
                    "status": "open",
                    "ready": "false",
                    "blocker": "Pair universe blocked",
                },
                {
                    "decision_area": "D(w) skip-cap formula",
                    "status": "open",
                    "ready": "false",
                    "blocker": "D blocked",
                },
                {
                    "decision_area": "Aggregate statistic and permutation",
                    "status": "claim_grade_ready",
                    "ready": "true",
                    "blocker": "",
                },
            ],
            lock_rows=[
                {
                    "area": "Pair universe",
                    "option": "working input",
                    "status": "diagnostic_only",
                },
                {
                    "area": "D(w) skip-cap formula",
                    "option": "printed",
                    "status": "primary_text_default",
                },
            ],
            source_rows=[
                {"source_review_flags": "wnp_disputed_zacut_appellation"},
                {"source_review_flags": "wnp_chelm_spelling_context"},
            ],
            method_rows=[
                {
                    "decision_area": "Pair universe",
                    "current_read": "pair read",
                },
                {
                    "decision_area": "D(w) skip-cap formula",
                    "current_read": "formula read",
                },
            ],
        )

        self.assertEqual(len(rows), 2)
        by_area = {row["decision_area"]: row for row in rows}
        self.assertIn("working input [diagnostic_only]", by_area["Pair universe"]["available_options"])
        self.assertIn("2 flagged queued terms", by_area["Pair universe"]["source_review_flags"])
        self.assertEqual(by_area["Pair universe"]["current_read"], "pair read")
        self.assertIn("printed", by_area["D(w) skip-cap formula"]["available_options"])
        self.assertEqual(by_area["D(w) skip-cap formula"]["source_review_flags"], "")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            readiness = root / "readiness.csv"
            lock_options = root / "lock_options.csv"
            source_queue = root / "source_queue.csv"
            method_status = root / "method_status.csv"
            source_policy_scenarios = root / "source_policy_scenarios.csv"
            out = root / "packet.csv"
            markdown = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(
                readiness,
                [
                    {
                        "decision_area": "Pair universe",
                        "status": "open",
                        "required_statuses": "locked,source_locked",
                        "ready": "false",
                        "blocker": "Pair universe blocked",
                    }
                ],
            )
            write_csv(
                lock_options,
                [
                    {
                        "area": "Pair universe",
                        "option": "working input",
                        "status": "diagnostic_only",
                    }
                ],
            )
            write_csv(
                source_queue,
                [
                    {
                        "priority_rank": "7",
                        "term_id": "wrr2_27_app_06",
                        "term": "M$HZKWTW",
                        "review_bucket": "ocr_near_match_with_variant_lead",
                        "source_review_flags": "wnp_disputed_zacut_appellation",
                        "source_review_action": "diagnostic flag only",
                    }
                ],
            )
            write_csv(
                method_status,
                [
                    {
                        "decision_area": "Pair universe",
                        "status": "open",
                        "current_read": "pair read",
                    }
                ],
            )
            write_csv(
                source_policy_scenarios,
                [
                    {
                        "scenario": "exclude_wnp_zacut_only",
                        "policy_type": "diagnostic_exclusion",
                        "excluded_pairs": "8",
                        "remaining_appellation_min_length_pairs": "157",
                        "gap_to_source_cited_163_after_appellation_min_length": "6",
                        "remaining_length_filtered_pairs": "78",
                    }
                ],
            )

            rc = packet.main(
                [
                    "--readiness",
                    str(readiness),
                    "--lock-options",
                    str(lock_options),
                    "--source-queue",
                    str(source_queue),
                    "--method-status",
                    str(method_status),
                    "--source-policy-scenarios",
                    str(source_policy_scenarios),
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
            self.assertEqual(rows[0]["decision_area"], "Pair universe")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Claim Blocker Packet", text)
            self.assertIn("Flagged Source-Review Rows", text)
            self.assertIn("Source Policy Scenario Impact", text)
            self.assertIn("exclude_wnp_zacut_only", text)
            self.assertIn("No pair exclusion or D(w) formula is chosen here", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
