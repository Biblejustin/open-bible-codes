import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_manual_decision_records as check


class WrrManualDecisionRecordsTests(unittest.TestCase):
    def test_current_header_only_records_pass(self) -> None:
        self.assertEqual(
            check.validate_decision_records(
                check.DEFAULT_RECORDS,
                check.DEFAULT_REGISTER_DOC,
            ),
            [],
        )

    def test_populated_record_must_match_register(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.csv"
            write_records(
                path,
                [
                    {
                        "decision_id": "wrr_decision_002",
                        "register_decision_rank": "2",
                        "decision_lane": "source_transcription_row_cluster",
                        "review_state": "pending_manual_source_lock",
                        "decision_target": "row 06",
                        "source_checklist": (
                            "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md"
                        ),
                        "decision_status": "accepted_keep",
                        "selected_action": "no_source_change",
                        "evidence_citation": "source scan page 6 row image",
                        "evidence_summary": (
                            "Reviewed row image and kept working-source row unchanged."
                        ),
                        "locked_by": "reviewer",
                        "locked_at": "2026-05-22",
                        "notes": "test row",
                    }
                ],
            )

            self.assertEqual(
                check.validate_decision_records(path, check.DEFAULT_REGISTER_DOC),
                [],
            )

    def test_populated_record_rejects_mismatch_and_placeholder_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.csv"
            write_records(
                path,
                [
                    {
                        "decision_id": "wrr_decision_002",
                        "register_decision_rank": "2",
                        "decision_lane": "source_transcription_row_cluster",
                        "review_state": "pending_manual_source_lock",
                        "decision_target": "row 99",
                        "source_checklist": (
                            "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md"
                        ),
                        "decision_status": "accepted_keep",
                        "selected_action": "no_source_change",
                        "evidence_citation": "todo",
                        "evidence_summary": "short",
                        "locked_by": "reviewer",
                        "locked_at": "2026/05/22",
                        "notes": "test row",
                    }
                ],
            )

            failures = check.validate_decision_records(path, check.DEFAULT_REGISTER_DOC)

            self.assertIn(
                f"{path}:2 decision_target must match register: row 06",
                failures,
            )
            self.assertIn(
                f"{path}:2 placeholder value for evidence_citation",
                failures,
            )
            self.assertIn(f"{path}:2 evidence_summary is too short", failures)
            self.assertIn(f"{path}:2 locked_at must be ISO date", failures)

    def test_populated_record_rejects_missing_checklist_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "records.csv"
            write_records(
                path,
                [
                    {
                        "decision_id": "wrr_decision_002",
                        "register_decision_rank": "2",
                        "decision_lane": "source_transcription_row_cluster",
                        "review_state": "pending_manual_source_lock",
                        "decision_target": "row 06",
                        "source_checklist": "docs/MISSING_WRR_CHECKLIST.md",
                        "decision_status": "accepted_keep",
                        "selected_action": "no_source_change",
                        "evidence_citation": "source scan page 6 row image",
                        "evidence_summary": (
                            "Reviewed row image and kept working-source row unchanged."
                        ),
                        "locked_by": "reviewer",
                        "locked_at": "2026-05-22",
                        "notes": "test row",
                    }
                ],
            )

            failures = check.validate_decision_records(path, check.DEFAULT_REGISTER_DOC)

            self.assertIn(
                f"{path}:2 source_checklist must match register: "
                "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
                failures,
            )
            self.assertIn(
                f"{path}:2 source_checklist is missing: docs/MISSING_WRR_CHECKLIST.md",
                failures,
            )


def write_records(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=check.REQUIRED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
