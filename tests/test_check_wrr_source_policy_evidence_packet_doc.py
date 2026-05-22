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

            self.assertEqual(check.validate_source_policy_evidence_packet_doc(path), [])

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Source-Policy Evidence Packet\n", encoding="utf-8")

            failures = check.validate_source_policy_evidence_packet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])


if __name__ == "__main__":
    unittest.main()
