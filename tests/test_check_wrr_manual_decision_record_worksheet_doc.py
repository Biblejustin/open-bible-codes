import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_manual_decision_record_worksheet_doc as check


class WrrManualDecisionRecordWorksheetDocTests(unittest.TestCase):
    def test_validate_current_doc_passes(self) -> None:
        if not check.DEFAULT_DOC.exists():
            self.skipTest("generated doc not built yet")
        self.assertEqual(check.validate_worksheet_doc(check.DEFAULT_DOC), [])

    def test_validate_doc_requires_no_input_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "worksheet.md"
            path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")

            self.assertEqual(
                check.validate_worksheet_doc(path, worksheet=None),
                [],
            )

    def test_validate_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "worksheet.md"
            path.write_text("# WRR Manual Decision Record Worksheet\n", encoding="utf-8")

            failures = check.validate_worksheet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_doc_reports_forbidden_decision_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "worksheet.md"
            path.write_text(
                "\n".join(check.REQUIRED_PHRASES) + "\nselected correction\n",
                encoding="utf-8",
            )

            failures = check.validate_worksheet_doc(path)

            self.assertEqual(
                failures,
                [f"{path} contains forbidden phrase: selected correction"],
            )

    def test_validate_doc_accepts_matching_worksheet_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_worksheet_doc(doc, worksheet=_worksheet_csv(root)),
                [],
            )

    def test_validate_doc_rejects_worksheet_row_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_worksheet_doc(
                doc,
                worksheet=_worksheet_csv(root, drop_last=True),
            )

            self.assertTrue(any("has 36 rows" in failure for failure in failures))

    def test_validate_doc_rejects_selected_action_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_worksheet_doc(
                doc,
                worksheet=_worksheet_csv(root, bad_action_rank=1),
            )

            self.assertTrue(any("selected action" in failure for failure in failures))


def _required_doc(root: Path) -> Path:
    path = root / "worksheet.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return path


def _worksheet_csv(
    root: Path,
    *,
    drop_last: bool = False,
    bad_action_rank: int | None = None,
) -> Path:
    path = root / "worksheet.csv"
    fieldnames = [
        "decision_id",
        "register_decision_rank",
        "decision_lane",
        "review_state",
        "decision_target",
        "source_checklist",
        "required_decision_record",
        "evidence_prompt",
        "suggested_decision_status_values",
        "suggested_selected_action_values",
        "allowed_without_input",
        "record_decision_status",
        "record_selected_action",
        "record_locked_by",
        "record_locked_at",
        "record_evidence_citation",
        "record_evidence_summary",
    ]
    rows: list[dict[str, str]] = []
    rank = 1
    for lane, locks in check.LANE_LOCKS.items():
        for offset in range(int(locks["rows"])):
            rows.append(
                {
                    "decision_id": f"wrr_decision_{rank:03d}",
                    "register_decision_rank": str(rank),
                    "decision_lane": lane,
                    "review_state": str(locks["review_state"]),
                    "decision_target": f"{lane} target {offset}",
                    "source_checklist": str(locks["source_checklist"]),
                    "required_decision_record": str(locks["required_decision_record"]),
                    "evidence_prompt": str(locks["evidence_prompt"]),
                    "suggested_decision_status_values": check.SUGGESTED_STATUS_VALUES,
                    "suggested_selected_action_values": str(locks["suggested_actions"]),
                    "allowed_without_input": check.ALLOWED_WITHOUT_INPUT,
                    "record_decision_status": "locked",
                    "record_selected_action": str(locks["record_action"]),
                    "record_locked_by": "Justin Scaggs",
                    "record_locked_at": "2026-05-25",
                    "record_evidence_citation": "citation",
                    "record_evidence_summary": "summary",
                }
            )
            rank += 1
    if drop_last:
        rows = rows[:-1]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if bad_action_rank == int(row["register_decision_rank"]):
                row["record_selected_action"] = "pair_exclusion"
            writer.writerow(row)
    return path


if __name__ == "__main__":
    unittest.main()
