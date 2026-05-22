import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_remaining_lane_evidence_packets_doc as check


class WrrRemainingLaneEvidencePacketDocTests(unittest.TestCase):
    def test_validate_packet_doc_requires_diagnostic_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text(
                "\n".join(
                    [
                        "# WRR Remaining-Lane Evidence Packets",
                        "Status: diagnostic evidence packet for page-image and method residual lanes.",
                        "It does not choose source corrections, method changes, or pair exclusions.",
                        "- Remaining-lane action terms: 14.",
                        "- Residual pair links: 14.",
                        "- Minimum-frontier pair links: 4.",
                        "| `page_image_near_match_review` | 3 | 3 | 2 |",
                        "| `method_or_pair_universe_review` | 11 | 11 | 2 |",
                        "`wrr2_19_app_11`",
                        "`YWSP+RANY`",
                        "`wrr2_02_app_03`",
                        "`ZR@ABRHM`",
                        "Page-image near-match rows need page-image review before source edits.",
                        "OCR-matched method rows need method or pair-universe explanation before source edits.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(check.validate_remaining_lane_evidence_packets_doc(path), [])

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Remaining-Lane Evidence Packets\n", encoding="utf-8")

            failures = check.validate_remaining_lane_evidence_packets_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])


if __name__ == "__main__":
    unittest.main()
