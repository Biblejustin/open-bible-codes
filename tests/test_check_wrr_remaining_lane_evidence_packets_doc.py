import csv
import json
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
                        "primary page row visibly contains Maharit/Trani forms",
                        "primary page row visibly contains Rabbi Shalom Sharabi forms",
                        "Page-image near-match rows need page-image review before source edits.",
                        "OCR-matched method rows need method or pair-universe explanation before source edits.",
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                check.validate_remaining_lane_evidence_packets_doc(
                    path,
                    packet=None,
                    summary=None,
                    manifest=None,
                ),
                [],
            )

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Remaining-Lane Evidence Packets\n", encoding="utf-8")

            failures = check.validate_remaining_lane_evidence_packets_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_packet_doc_accepts_matching_csvs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_remaining_lane_evidence_packets_doc(
                    doc,
                    packet=_packet_csv(root),
                    summary=_summary_csv(root),
                ),
                [],
            )

    def test_validate_packet_doc_rejects_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_remaining_lane_evidence_packets_doc(
                doc,
                packet=_packet_csv(root),
                summary=_summary_csv(root, page_terms="2"),
            )

            self.assertTrue(
                any("action_terms='2'" in failure for failure in failures)
            )

    def test_validate_packet_doc_rejects_missing_lane_term(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_remaining_lane_evidence_packets_doc(
                doc,
                packet=_packet_csv(root, omit_term="wrr2_19_app_11"),
                summary=_summary_csv(root),
            )

            self.assertTrue(
                any(
                    "missing terms: wrr2_19_app_11" in failure
                    for failure in failures
                )
            )

    def test_validate_packet_doc_rejects_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "manifest.json"
            payload = json.loads(check.DEFAULT_MANIFEST.read_text(encoding="utf-8"))
            payload["summary_rows"] = 99
            manifest.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            failures = check.validate_remaining_lane_evidence_packets_doc(
                check.DEFAULT_DOC,
                packet=None,
                summary=None,
                manifest=manifest,
            )

            self.assertTrue(
                any("summary_rows drifted" in failure for failure in failures)
            )


def _required_doc(root: Path) -> Path:
    path = root / "packet.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return path


def _summary_csv(root: Path, *, page_terms: str = "3") -> Path:
    path = root / "summary.csv"
    fieldnames = [
        "run_label",
        "action_lane",
        "action_terms",
        "residual_pairs",
        "frontier_pairs",
        "concepts",
        "evidence_required",
        "no_input_boundary",
        "read",
    ]
    rows = [
        {
            "run_label": "all_lanes_cap1000",
            "action_lane": "page_image_near_match_review",
            "action_terms": page_terms,
            "residual_pairs": "3",
            "frontier_pairs": "2",
            "concepts": "2",
            "evidence_required": check.EXPECTED_LANES[
                "page_image_near_match_review"
            ]["evidence_required"],
            "no_input_boundary": check.NO_INPUT_BOUNDARY,
            "read": "near OCR exists",
        },
        {
            "run_label": "all_lanes_cap1000",
            "action_lane": "method_or_pair_universe_review",
            "action_terms": "11",
            "residual_pairs": "11",
            "frontier_pairs": "2",
            "concepts": "8",
            "evidence_required": check.EXPECTED_LANES[
                "method_or_pair_universe_review"
            ]["evidence_required"],
            "no_input_boundary": check.NO_INPUT_BOUNDARY,
            "read": "OCR matched",
        },
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _packet_csv(root: Path, *, omit_term: str | None = None) -> Path:
    path = root / "packet.csv"
    fieldnames = [
        "run_label",
        "evidence_rank",
        "action_rank",
        "action_lane",
        "term_id",
        "term",
        "concept",
        "row_number",
        "residual_pairs",
        "frontier_pairs",
        "review_buckets",
        "row_ocr_status",
        "row_ocr_near_match_distance",
        "row_ocr_near_match_text",
        "row_ocr_text_normalized",
        "visual_review_note",
        "visual_review_action",
        "best_variant_hit_count",
        "best_variant_rule",
        "evidence_required",
        "no_input_boundary",
        "evidence_read",
    ]
    rows: list[dict[str, str]] = []
    rank = 1
    for lane, terms in check.EXPECTED_TERM_IDS_BY_LANE.items():
        for term_id in sorted(terms):
            if term_id == omit_term:
                continue
            rows.append(
                {
                    "run_label": "all_lanes_cap1000",
                    "evidence_rank": str(rank),
                    "action_rank": str(rank + 44),
                    "action_lane": lane,
                    "term_id": term_id,
                    "term": "TERM",
                    "concept": "Concept",
                    "row_number": "02",
                    "residual_pairs": "1",
                    "frontier_pairs": "1",
                    "review_buckets": "ocr_near_match_no_variant_lead",
                    "row_ocr_status": "matched",
                    "row_ocr_near_match_distance": "0",
                    "row_ocr_near_match_text": "",
                    "row_ocr_text_normalized": "",
                    "visual_review_note": "",
                    "visual_review_action": "",
                    "best_variant_hit_count": "0",
                    "best_variant_rule": "none",
                    "evidence_required": check.EXPECTED_LANES[lane][
                        "evidence_required"
                    ],
                    "no_input_boundary": check.NO_INPUT_BOUNDARY,
                    "evidence_read": "review row",
                }
            )
            rank += 1
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


if __name__ == "__main__":
    unittest.main()
