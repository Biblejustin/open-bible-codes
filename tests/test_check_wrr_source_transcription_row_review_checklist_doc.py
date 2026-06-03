import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_source_transcription_row_review_checklist_doc as check


class WrrSourceTranscriptionRowReviewChecklistDocTests(unittest.TestCase):
    def test_validate_current_doc_passes(self) -> None:
        if not check.DEFAULT_DOC.exists():
            self.skipTest("generated doc not built yet")
        self.assertEqual(check.validate_row_review_checklist_doc(check.DEFAULT_DOC), [])

    def test_validate_doc_requires_no_input_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")

            self.assertEqual(
                check.validate_row_review_checklist_doc(
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
                "# WRR Source-Transcription Row Review Checklist\n",
                encoding="utf-8",
            )

            failures = check.validate_row_review_checklist_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_doc_reports_forbidden_decision_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text(
                "\n".join(check.REQUIRED_PHRASES) + "\nselected correction\n",
                encoding="utf-8",
            )

            failures = check.validate_row_review_checklist_doc(path)

            self.assertEqual(
                failures,
                [f"{path} contains forbidden phrase: selected correction"],
            )

    def test_validate_doc_accepts_matching_checklist_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_row_review_checklist_doc(
                    doc,
                    checklist=_checklist_csv(root),
                    manifest=None,
                ),
                [],
            )

    def test_validate_doc_rejects_checklist_review_state_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_row_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root, review_state_rank=1),
                manifest=None,
            )

            self.assertTrue(any("review state" in failure for failure in failures))

    def test_validate_doc_rejects_checklist_boundary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_row_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root, bad_boundary_rank=1),
                manifest=None,
            )

            self.assertTrue(any("no-input boundary" in failure for failure in failures))

    def test_validate_doc_rejects_manifest_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)
            manifest = root / "manifest.json"
            manifest.write_text(
                """
{
  "action_terms": 42,
  "frontier_pairs": 35,
  "inputs": {
    "row_summary": "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv"
  },
  "outputs": {
    "manifest_out": "reports/wrr_1994/wrr_source_transcription_row_review_checklist.manifest.json",
    "markdown_out": "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
    "out": "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv"
  },
  "residual_pairs": 44,
  "rows": 22,
  "tool": "build_wrr_source_transcription_row_review_checklist"
}
""".lstrip(),
                encoding="utf-8",
            )

            failures = check.validate_row_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root),
                manifest=manifest,
            )

            self.assertTrue(any("action_terms drifted" in failure for failure in failures))


def _required_doc(root: Path) -> Path:
    path = root / "checklist.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return path


def _checklist_csv(
    root: Path,
    *,
    review_state_rank: int | None = None,
    bad_boundary_rank: int | None = None,
) -> Path:
    path = root / "checklist.csv"
    fieldnames = check.FIELDNAMES
    action_counts = [4, 3, 3] + [2] * 10 + [1] * 6 + [4, 2, 1]
    residual_counts = action_counts.copy()
    residual_counts[13] = 2
    frontier_counts = [4, 3, 3] + [2] * 9 + [1] * 7 + [0, 0, 0]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 23):
            action_terms = action_counts[index - 1]
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "row_rank": str(index),
                    "row_number": f"{index:02d}",
                    "concept": f"WRR2 {index:02d}",
                    "review_state": (
                        "manual_source_locked"
                        if review_state_rank == index
                        else check.REVIEW_STATE
                    ),
                    "action_terms": str(action_terms),
                    "residual_pairs": str(residual_counts[index - 1]),
                    "frontier_pairs": str(frontier_counts[index - 1]),
                    "terms_to_verify": ";".join(
                        f"term_{index}_{offset}" for offset in range(action_terms)
                    ),
                    "matched_row_terms": "matched",
                    "row_ocr_name_texts": "name",
                    "row_ocr_date_texts": "date",
                    "table2_bridge_read": "Hebrew cells are not verified.",
                    "required_source_evidence": check.SOURCE_EVIDENCE,
                    "required_alignment_evidence": check.ALIGNMENT_EVIDENCE,
                    "required_decision_record": check.DECISION_RECORD,
                    "no_input_boundary": (
                        "bad"
                        if bad_boundary_rank == index
                        else check.NO_INPUT_BOUNDARY
                    ),
                    "allowed_without_input": check.ALLOWED_WITHOUT_INPUT,
                    "next_manual_action": "review row image once before individual term decisions",
                }
            )
    return path


if __name__ == "__main__":
    unittest.main()
