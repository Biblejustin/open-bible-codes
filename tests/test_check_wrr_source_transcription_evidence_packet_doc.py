import tempfile
import unittest
from pathlib import Path

from scripts import check_wrr_source_transcription_evidence_packet_doc as check


class WrrSourceTranscriptionEvidencePacketDocTests(unittest.TestCase):
    def test_validate_packet_doc_requires_diagnostic_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text(
                "\n".join(
                    [
                        "# WRR Source-Transcription Evidence Packet",
                        "Status: diagnostic evidence packet for source-transcription residual terms.",
                        "It does not choose source corrections, row edits, or pair exclusions.",
                        "- Source-transcription action terms: 43.",
                        "- Residual pair links: 44.",
                        "- Minimum-frontier pair links: 35.",
                        "- Row clusters: 22.",
                        "| 1 | `06` | `WRR2 06` | 4 | 4 | 4 |",
                        "`wrr2_27_app_13`",
                        "`B@LQWLHRMZ`",
                        "primary Table 2 row transcription or row-alignment evidence",
                        "No automatic source correction",
                        "Rows with multiple unresolved terms should be reviewed once by row",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                check.validate_source_transcription_evidence_packet_doc(path), []
            )

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Source-Transcription Evidence Packet\n", encoding="utf-8")

            failures = check.validate_source_transcription_evidence_packet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])


if __name__ == "__main__":
    unittest.main()
