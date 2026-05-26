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
                check.validate_method_pair_universe_evidence_packet_doc(
                    path,
                    packet=None,
                    summary=None,
                ),
                [],
            )

    def test_validate_packet_doc_reports_missing_required_phrase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "packet.md"
            path.write_text("# WRR Method/Pair-Universe Evidence Packet\n", encoding="utf-8")

            failures = check.validate_method_pair_universe_evidence_packet_doc(path)

            self.assertTrue(failures)
            self.assertIn("missing phrase", failures[0])

    def test_validate_packet_doc_accepts_matching_csvs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            self.assertEqual(
                check.validate_method_pair_universe_evidence_packet_doc(
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

            failures = check.validate_method_pair_universe_evidence_packet_doc(
                doc,
                packet=_packet_csv(root),
                summary=_summary_csv(root, action_terms="10"),
            )

            self.assertTrue(any("action_terms" in failure for failure in failures))

    def test_validate_packet_doc_rejects_missing_method_term(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc = _required_doc(root)

            failures = check.validate_method_pair_universe_evidence_packet_doc(
                doc,
                packet=_packet_csv(root, omit_term="wrr2_02_app_03"),
                summary=_summary_csv(root),
            )

            self.assertTrue(
                any(
                    "missing method terms: wrr2_02_app_03" in failure
                    for failure in failures
                )
            )


def _required_doc(root: Path) -> Path:
    path = root / "packet.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    return path


def _summary_csv(root: Path, *, action_terms: str = "11") -> Path:
    path = root / "summary.csv"
    path.write_text(
        "\n".join(
            [
                (
                    "run_label,action_terms,residual_pairs,frontier_pairs,"
                    "ocr_matched_terms,zero_base_skip_250_terms,"
                    "zero_highcap_appellation_terms,both_sides_zero_highcap_pairs,"
                    "no_variant_lead_terms,read"
                ),
                (
                    f"all_lanes_cap1000,{action_terms},11,1,11,11,11,2,11,"
                    "OCR matched all method-lane terms."
                ),
            ]
        ),
        encoding="utf-8",
    )
    return path


def _packet_csv(root: Path, *, omit_term: str | None = None) -> Path:
    rows = [
        (
            "run_label,evidence_rank,action_rank,term_id,term,concept,row_number,"
            "pair_id,date_term_id,review_bucket,blocking_reasons,row_ocr_status,"
            "base_skip_250_hit_count,highcap_appellation_ordinary_hits,"
            "highcap_date_ordinary_hits,pair_valid_perturbations,"
            "corrected_distance_status,best_variant_hit_count,best_variant_rule,"
            "diagnostic_read,no_input_boundary"
        )
    ]
    for rank, term_id in enumerate(sorted(check.EXPECTED_TERM_IDS), start=1):
        if term_id == omit_term:
            continue
        rows.append(
            ",".join(
                [
                    "all_lanes_cap1000",
                    str(rank),
                    str(rank + 47),
                    term_id,
                    "TERM",
                    "Concept",
                    "02",
                    f"{term_id}__date",
                    "date",
                    "ocr_matched_no_variant_lead",
                    "1 ordinary_missing_appellation_hits",
                    "matched",
                    "0",
                    "0",
                    "1",
                    "0",
                    "ordinary_not_valid",
                    "0",
                    "none",
                    "diagnostic read",
                    (
                        "No source correction or method change is selected; "
                        "OCR-matched zero-hit terms remain diagnostic."
                    ),
                ]
            )
        )
    path = root / "packet.csv"
    path.write_text("\n".join(rows), encoding="utf-8")
    return path


if __name__ == "__main__":
    unittest.main()
