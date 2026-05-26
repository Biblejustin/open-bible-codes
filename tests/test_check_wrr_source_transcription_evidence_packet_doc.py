import csv
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
                check.validate_source_transcription_evidence_packet_doc(
                    path,
                    packet=None,
                    row_summary=None,
                ),
                [],
            )

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Source-Transcription Evidence Packet\n", encoding="utf-8")

            failures = check.validate_source_transcription_evidence_packet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_packet_doc_accepts_matching_csvs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_source_transcription_evidence_packet_doc(
                    doc,
                    packet=_packet_csv(root),
                    row_summary=_row_summary_csv(root),
                ),
                [],
            )

    def test_validate_packet_doc_rejects_packet_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_transcription_evidence_packet_doc(
                doc,
                packet=_packet_csv(root, variant_rank=1),
                row_summary=_row_summary_csv(root),
            )

            self.assertTrue(any("variant lead count" in failure for failure in failures))

    def test_validate_packet_doc_rejects_row_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_source_transcription_evidence_packet_doc(
                doc,
                packet=_packet_csv(root),
                row_summary=_row_summary_csv(root, bad_boundary_rank=1),
            )

            self.assertTrue(any("no-input boundary" in failure for failure in failures))


def _required_doc(root: Path) -> Path:
    path = root / "packet.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return path


def _packet_csv(root: Path, *, variant_rank: int | None = None) -> Path:
    path = root / "packet.csv"
    fieldnames = [
        "run_label",
        "evidence_rank",
        "action_rank",
        "term_id",
        "term",
        "concept",
        "row_number",
        "residual_pairs",
        "frontier_pairs",
        "review_buckets",
        "row_ocr_status",
        "row_ocr_text_normalized",
        "best_variant_hit_count",
        "best_variant_rule",
        "row_matched_terms",
        "row_action_not_matched_terms",
        "table2_bridge_read",
        "evidence_required",
        "no_input_boundary",
        "evidence_read",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index in range(1, 44):
            writer.writerow(
                {
                    "run_label": "all_lanes_cap1000",
                    "evidence_rank": str(index),
                    "action_rank": str(index + 1),
                    "term_id": f"wrr2_{index:02d}_app_01",
                    "term": "TERM",
                    "concept": "WRR2",
                    "row_number": f"{index:02d}",
                    "residual_pairs": "2" if index == 1 else "1",
                    "frontier_pairs": "1" if index <= 35 else "0",
                    "review_buckets": "ocr_not_matched_no_variant_lead",
                    "row_ocr_status": "not_matched",
                    "row_ocr_text_normalized": "ocr",
                    "best_variant_hit_count": "1" if variant_rank == index else "0",
                    "best_variant_rule": "none",
                    "row_matched_terms": "matched",
                    "row_action_not_matched_terms": "not_matched",
                    "table2_bridge_read": "Hebrew cells are not verified.",
                    "evidence_required": check.EVIDENCE_REQUIRED,
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                    "evidence_read": "needs evidence",
                }
            )
    return path


def _row_summary_csv(root: Path, *, bad_boundary_rank: int | None = None) -> Path:
    path = root / "row_summary.csv"
    fieldnames = [
        "run_label",
        "row_rank",
        "row_number",
        "concept",
        "action_terms",
        "residual_pairs",
        "frontier_pairs",
        "action_term_ids",
        "action_terms_display",
        "row_matched_terms",
        "row_action_not_matched_terms",
        "row_ocr_name_texts",
        "row_ocr_date_texts",
        "table2_bridge_read",
        "evidence_required",
        "no_input_boundary",
        "read",
    ]
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
                    "action_terms": str(action_terms),
                    "residual_pairs": str(residual_counts[index - 1]),
                    "frontier_pairs": str(frontier_counts[index - 1]),
                    "action_term_ids": ";".join(
                        f"term_{index}_{offset}" for offset in range(action_terms)
                    ),
                    "action_terms_display": "display",
                    "row_matched_terms": "matched",
                    "row_action_not_matched_terms": "not matched",
                    "row_ocr_name_texts": "name",
                    "row_ocr_date_texts": "date",
                    "table2_bridge_read": "Hebrew cells are not verified.",
                    "evidence_required": check.EVIDENCE_REQUIRED,
                    "no_input_boundary": (
                        "bad"
                        if bad_boundary_rank == index
                        else check.NO_INPUT_BOUNDARY
                    ),
                    "read": "review row once",
                }
            )
    return path


if __name__ == "__main__":
    unittest.main()
