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

            self.assertEqual(check.validate_worksheet_doc(path), [])

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


if __name__ == "__main__":
    unittest.main()
