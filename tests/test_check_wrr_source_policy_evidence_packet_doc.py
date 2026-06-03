import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_source_policy_evidence_packet_doc as check


class WrrSourcePolicyEvidencePacketDocTests(unittest.TestCase):
    def test_validate_packet_doc_requires_diagnostic_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text(
                "\n".join(
                    [
                        "# WRR Source-Policy Evidence Packet",
                        "Status: diagnostic evidence packet for source-policy residual terms.",
                        "It does not choose a source correction, exclude a pair, or lock a replacement.",
                        "- Priority source-policy terms: 1.",
                        "- Related source-review rows: 2.",
                        "- Related scenario-pair rows: 4.",
                        "- WNP context blocks: 3.",
                        "| 1 | `wrr2_32_app_05` | `$LMHMX@LMA` | `WRR2 32` | `wnp_chelm_spelling_context` |",
                        "`wrr2_32_app_04`",
                        "`RBY$LMH`",
                        "`/KA/TMWZ`",
                        "`reports/wrr_1994/wnp_en.html:608-619`",
                        "`review_chelm_spelling_only`",
                        "source/pair-rule review",
                        "No automatic correction or exclusion",
                        "WNP context supports why the Chełm forms are in review scope, not a final pair-rule decision.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                check.validate_source_policy_evidence_packet_doc(
                    path,
                    packet=None,
                    context=None,
                    summary=None,
                    manifest=None,
                ),
                [],
            )

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Source-Policy Evidence Packet\n", encoding="utf-8")

            failures = check.validate_source_policy_evidence_packet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_packet_doc_accepts_matching_csvs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_source_policy_evidence_packet_doc(
                    doc,
                    packet=_packet_csv(root),
                    context=_context_csv(root),
                    summary=_summary_csv(root),
                ),
                [],
            )

    def test_validate_packet_doc_rejects_packet_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_policy_evidence_packet_doc(
                doc,
                packet=_packet_csv(root, bad_term=True),
                context=_context_csv(root),
                summary=_summary_csv(root),
            )

            self.assertTrue(any("term drifted" in failure for failure in failures))

    def test_validate_packet_doc_rejects_context_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_policy_evidence_packet_doc(
                doc,
                packet=_packet_csv(root),
                context=_context_csv(root, bad_ref=True),
                summary=_summary_csv(root),
            )

            self.assertTrue(any("context refs" in failure for failure in failures))

    def test_validate_packet_doc_rejects_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_policy_evidence_packet_doc(
                doc,
                packet=_packet_csv(root),
                context=_context_csv(root),
                summary=_summary_csv(root, bad_count=True),
            )

            self.assertTrue(any("wnp_context_blocks" in failure for failure in failures))

    def test_validate_packet_doc_rejects_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.json"
            payload = json.loads(check.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
            payload["source_context_rows"] = 99
            manifest.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            failures = check.validate_source_policy_evidence_packet_doc(
                check.DEFAULT_DOC,
                packet=None,
                context=None,
                summary=None,
                manifest=manifest,
            )

            self.assertTrue(
                any("source_context_rows drifted" in failure for failure in failures)
            )

    def test_validate_packet_doc_rejects_invalid_manifest_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.json"
            manifest.write_text("{", encoding="utf-8")

            failures = check.validate_source_policy_evidence_packet_doc(
                check.DEFAULT_DOC,
                packet=None,
                context=None,
                summary=None,
                manifest=manifest,
            )

            self.assertTrue(any("is invalid JSON" in failure for failure in failures))

    def test_validate_packet_doc_rejects_manifest_json_array(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.json"
            manifest.write_text("[]", encoding="utf-8")

            failures = check.validate_source_policy_evidence_packet_doc(
                check.DEFAULT_DOC,
                packet=None,
                context=None,
                summary=None,
                manifest=manifest,
            )

            self.assertTrue(
                any("JSON root must be an object" in failure for failure in failures)
            )


def _required_doc(root: Path) -> Path:
    path = root / "packet.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return path


def _packet_csv(root: Path, *, bad_term: bool = False) -> Path:
    path = root / "packet.csv"
    fieldnames = check.PACKET_FIELDNAMES
    row = dict(check.EXPECTED_PACKET_ROW)
    if bad_term:
        row["term"] = "drifted"
    row["scenario_pair_statuses"] = (
        "review_chelm_spelling_only:review_only_no_exclusion:"
        "wrr2_32_app_04__wrr2_32_date_01:needs_primary_source_pair_rule;"
        "review_chelm_spelling_only:review_only_no_exclusion:"
        "wrr2_32_app_05__wrr2_32_date_01:needs_primary_source_pair_rule;"
        "exclude_all_source_review_flags:excluded:"
        "wrr2_32_app_04__wrr2_32_date_01:needs_primary_source_pair_rule;"
        "exclude_all_source_review_flags:excluded:"
        "wrr2_32_app_05__wrr2_32_date_01:needs_primary_source_pair_rule"
    )
    row["evidence_read"] = "wrr2_32_app_05 is a Chełm spelling-context target"
    _write_one_row(path, fieldnames, row)
    return path


def _context_csv(root: Path, *, bad_ref: bool = False) -> Path:
    path = root / "context.csv"
    fieldnames = check.CONTEXT_FIELDNAMES
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for context_id, source_ref in check.EXPECTED_CONTEXT.items():
            writer.writerow(
                {
                    "context_id": context_id,
                    "source_flag": "wnp_chelm_spelling_context",
                    "source_ref": "drifted" if bad_ref else source_ref,
                    "source_terms": "terms",
                    "read": "read",
                    "decision_boundary": check.DECISION_BOUNDARY,
                }
            )
    return path


def _summary_csv(root: Path, *, bad_count: bool = False) -> Path:
    path = root / "summary.csv"
    fieldnames = check.SUMMARY_FIELDNAMES
    row = dict(check.EXPECTED_SUMMARY_ROW)
    if bad_count:
        row["wnp_context_blocks"] = "2"
    row["read"] = "diagnostic packet without changing the working source"
    _write_one_row(path, fieldnames, row)
    return path


def _write_one_row(path: Path, fieldnames: list[str], row: dict[str, str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    unittest.main()
