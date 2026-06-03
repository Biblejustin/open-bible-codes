import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_source_policy_review_checklist_doc as check


class WrrSourcePolicyReviewChecklistDocTests(unittest.TestCase):
    def test_validate_current_doc_passes(self) -> None:
        if not check.DEFAULT_DOC.exists():
            self.skipTest("generated doc not built yet")
        self.assertEqual(
            check.validate_source_policy_review_checklist_doc(check.DEFAULT_DOC),
            [],
        )

    def test_validate_doc_requires_no_input_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")

            self.assertEqual(
                check.validate_source_policy_review_checklist_doc(
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
                "# WRR Source-Policy Review Checklist\n",
                encoding="utf-8",
            )

            failures = check.validate_source_policy_review_checklist_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_doc_reports_forbidden_decision_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "checklist.md"
            path.write_text(
                "\n".join(check.REQUIRED_PHRASES) + "\nselected correction\n",
                encoding="utf-8",
            )

            failures = check.validate_source_policy_review_checklist_doc(path)

            self.assertEqual(
                failures,
                [f"{path} contains forbidden phrase: selected correction"],
            )

    def test_validate_doc_accepts_matching_checklist_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_source_policy_review_checklist_doc(
                    doc,
                    checklist=_checklist_csv(root),
                    manifest=None,
                ),
                [],
            )

    def test_validate_doc_rejects_checklist_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_policy_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root, bad_term=True),
                manifest=None,
            )

            self.assertTrue(any("term drifted" in failure for failure in failures))

    def test_validate_doc_rejects_wnp_ref_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_policy_review_checklist_doc(
                doc,
                checklist=_checklist_csv(root, drop_ref=True),
                manifest=None,
            )

            self.assertTrue(any("WNP evidence ref count" in failure for failure in failures))

    def test_validate_doc_rejects_manifest_count_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)
            manifest = root / "manifest.json"
            manifest.write_text(
                """
{
  "context_rows": 3,
  "frontier_pairs": 1,
  "inputs": {
    "context": "reports/wrr_1994/wrr_source_policy_evidence_context.csv",
    "packet": "reports/wrr_1994/wrr_source_policy_evidence_packet.csv",
    "summary": "reports/wrr_1994/wrr_source_policy_evidence_summary.csv"
  },
  "outputs": {
    "manifest_out": "reports/wrr_1994/wrr_source_policy_review_checklist.manifest.json",
    "markdown_out": "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md",
    "out": "reports/wrr_1994/wrr_source_policy_review_checklist.csv"
  },
  "residual_pairs": 0,
  "rows": 1,
  "summary_rows": 1,
  "tool": "build_wrr_source_policy_review_checklist"
}
""".lstrip(),
                encoding="utf-8",
            )

            failures = check.validate_source_policy_review_checklist_doc(
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
    bad_term: bool = False,
    drop_ref: bool = False,
) -> Path:
    path = root / "checklist.csv"
    fieldnames = check.FIELDNAMES
    row = dict(check.EXPECTED_ROW)
    if bad_term:
        row["term"] = "drifted"
    if drop_ref:
        row["wnp_evidence_refs"] = "reports/wrr_1994/wnp_en.html:608-619"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)
    return path


if __name__ == "__main__":
    unittest.main()
