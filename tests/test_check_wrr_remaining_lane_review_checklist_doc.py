import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_remaining_lane_review_checklist_doc as check


class WrrRemainingLaneReviewChecklistDocTests(unittest.TestCase):
    def test_validate_current_doc_passes(self) -> None:
        if not check.DEFAULT_DOC.exists():
            self.skipTest("generated doc not built yet")
        self.assertEqual(
            check.validate_remaining_lane_review_checklist_doc(check.DEFAULT_DOC),
            [],
        )

    def test_validate_doc_requires_no_input_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")

            self.assertEqual(
                check.validate_remaining_lane_review_checklist_doc(
                    path,
                    checklist=None,
                    manifest=None,
                ),
                [],
            )

    def test_validate_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text(
                "# WRR Remaining-Lane Review Checklist\n",
                encoding="utf-8",
            )

            failures = check.validate_remaining_lane_review_checklist_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_doc_reports_forbidden_decision_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text(
                "\n".join(check.REQUIRED_PHRASES) + "\nselected correction\n",
                encoding="utf-8",
            )

            failures = check.validate_remaining_lane_review_checklist_doc(path)

            self.assertEqual(
                failures,
                [f"{path} contains forbidden phrase: selected correction"],
            )

    def test_validate_doc_accepts_matching_checklist_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_remaining_lane_review_checklist_doc(
                    doc,
                    checklist=_checklist_csv(root),
                    manifest=None,
                ),
                [],
            )

    def test_validate_doc_rejects_lane_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_remaining_lane_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root, drop_last=True),
                manifest=None,
            )

            self.assertTrue(any("has 13 rows" in failure for failure in failures))

    def test_validate_doc_rejects_review_state_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_remaining_lane_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root, bad_state_rank=1),
                manifest=None,
            )

            self.assertTrue(any("review_state" in failure for failure in failures))

    def test_validate_doc_rejects_manifest_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)
            manifest = root / "manifest.json"
            manifest.write_text(
                """
{
  "frontier_pairs": 4,
  "inputs": {
    "packet": "reports/wrr_1994/wrr_remaining_lane_evidence_packet.csv",
    "summary": "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv"
  },
  "outputs": {
    "manifest_out": "reports/wrr_1994/wrr_remaining_lane_review_checklist.manifest.json",
    "markdown_out": "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
    "out": "reports/wrr_1994/wrr_remaining_lane_review_checklist.csv"
  },
  "residual_pairs": 13,
  "rows": 14,
  "summary_rows": 2,
  "tool": "build_wrr_remaining_lane_review_checklist"
}
""".lstrip(),
                encoding="utf-8",
            )

            failures = check.validate_remaining_lane_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root),
                manifest=manifest,
            )

            self.assertTrue(any("residual_pairs drifted" in failure for failure in failures))


def _required_doc(root: Path) -> Path:
    path = root / "checklist.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return path


def _checklist_csv(
    root: Path,
    *,
    drop_last: bool = False,
    bad_state_rank: int | None = None,
) -> Path:
    path = root / "checklist.csv"
    fieldnames = check.FIELDNAMES
    rows = [
        _checklist_row(
            index,
            lane="page_image_near_match_review",
            frontier_pairs="1" if index <= 2 else "0",
        )
        for index in range(1, 4)
    ] + [
        _checklist_row(
            index,
            lane="method_or_pair_universe_review",
            frontier_pairs="1" if index <= 5 else "0",
        )
        for index in range(4, 15)
    ]
    if drop_last:
        rows = rows[:-1]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            if bad_state_rank == int(row["checklist_rank"]):
                row["review_state"] = "locked"
            writer.writerow(row)
    return path


def _checklist_row(index: int, *, lane: str, frontier_pairs: str) -> dict[str, str]:
    locks = check.LANE_LOCKS[lane]
    next_action = sorted(locks["next_manual_actions"])[0]
    return {
        "run_label": "all_lanes_cap1000",
        "checklist_rank": str(index),
        "action_lane": lane,
        "review_state": str(locks["review_state"]),
        "term_id": f"wrr2_{index:02d}_app_01",
        "term": "TERM",
        "concept": f"WRR2 {index:02d}",
        "row_number": f"{index:02d}",
        "residual_pairs": "1",
        "frontier_pairs": frontier_pairs,
        "row_ocr_status": str(locks["row_ocr_status"]),
        "near_match": "d=0 term",
        "visual_review_note": "note",
        "evidence_required": str(locks["evidence_required"]),
        "required_decision_record": str(locks["required_decision_record"]),
        "no_input_boundary": check.NO_INPUT_BOUNDARY,
        "allowed_without_input": check.ALLOWED_WITHOUT_INPUT,
        "next_manual_action": next_action,
    }


if __name__ == "__main__":
    unittest.main()
