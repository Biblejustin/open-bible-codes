import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_method_pair_universe_evidence_packet_doc as check


class WrrMethodPairUniverseEvidencePacketDocTests(unittest.TestCase):
    def test_validate_packet_doc_requires_diagnostic_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

            self.assertEqual(
                check.validate_method_pair_universe_evidence_packet_doc(path), []
            )

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Method/Pair-Universe Evidence Packet\n", encoding="utf-8")

            failures = check.validate_method_pair_universe_evidence_packet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])


if __name__ == "__main__":
    unittest.main()
