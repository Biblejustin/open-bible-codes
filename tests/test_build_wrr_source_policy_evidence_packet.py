import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_policy_evidence_packet as packet


class WrrSourcePolicyEvidencePacketTests(unittest.TestCase):
    def test_build_evidence_rows_joins_chelm_context(self) -> None:
        action_rows = [
            {
                "run_label": "all_lanes_cap1000",
                "action_lane": "source_policy_or_pair_rule_review",
                "term_id": "wrr2_32_app_05",
                "term": "$LMHMX@LMA",
                "source_flags": "wnp_chelm_spelling_context",
                "residual_pairs": "1",
                "frontier_pairs": "1",
                "pair_ids": "wrr2_32_app_05__wrr2_32_date_01",
            }
        ]
        source_rows = [
            source_row("wrr2_32_app_04", "$LMHMXLMA", "1", "delete_one@1"),
            source_row("wrr2_32_app_05", "$LMHMX@LMA", "0", "none"),
            {
                **source_row("wrr2_30_app_05", "B@LY$RLBB", "2", "delete_one@8"),
                "concepts": "WRR2 30",
            },
        ]
        ocr_rows = [
            row_ocr("wrr2_32_app_01", "RBY$LMH", "wrr_appellation", "matched"),
            row_ocr("wrr2_32_app_04", "$LMHMXLMA", "wrr_appellation", "not_matched"),
            row_ocr("wrr2_32_app_05", "$LMHMX@LMA", "wrr_appellation", "not_matched"),
            row_ocr("wrr2_32_date_01", "/KA/TMWZ", "wrr_date", "matched"),
        ]
        scenario_rows = [
            scenario_row("review_chelm_spelling_only", "wrr2_32_app_04"),
            scenario_row("review_chelm_spelling_only", "wrr2_32_app_05"),
        ]
        table_rows = [
            {
                "row_number": "32",
                "current_read": "Primary English row label and secondary WRR2 record align.",
            }
        ]
        context_rows = [
            {
                "context_id": "wnp_chelm_spelling_argument",
                "source_flag": "wnp_chelm_spelling_context",
                "source_ref": "reports/wrr_1994/wnp_en.html:608-619",
                "source_terms": "clma; cilma",
                "read": "WNP discusses Chelma spellings.",
                "decision_boundary": packet.DIAGNOSTIC_BOUNDARY,
            }
        ]

        rows = packet.build_evidence_rows(
            action_rows,
            source_rows,
            ocr_rows,
            scenario_rows,
            table_rows,
            context_rows,
        )

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["term_id"], "wrr2_32_app_05")
        self.assertIn("wrr2_32_app_04", rows[0]["related_source_term_ids"])
        self.assertIn("RBY$LMH", rows[0]["row_ocr_matched_terms"])
        self.assertIn("$LMHMX@LMA", rows[0]["row_ocr_not_matched_related_terms"])
        self.assertIn("review_chelm_spelling_only", rows[0]["scenario_pair_statuses"])
        self.assertIn("wnp_en.html:608-619", rows[0]["wnp_evidence_refs"])
        self.assertIn("No automatic correction", rows[0]["decision_boundary"])

    def test_main_writes_packet_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            action = root / "action.csv"
            source = root / "source.csv"
            ocr = root / "ocr.csv"
            scenarios = root / "scenarios.csv"
            table = root / "table.csv"
            wnp = root / "wnp_en.html"
            out = root / "packet.csv"
            context = root / "context.csv"
            summary = root / "summary.csv"
            md = root / "packet.md"
            manifest = root / "manifest.json"
            write_csv(
                action,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "action_lane": "source_policy_or_pair_rule_review",
                        "term_id": "wrr2_32_app_05",
                        "term": "$LMHMX@LMA",
                        "source_flags": "wnp_chelm_spelling_context",
                        "residual_pairs": "1",
                        "frontier_pairs": "1",
                        "pair_ids": "wrr2_32_app_05__wrr2_32_date_01",
                    }
                ],
            )
            write_csv(
                source,
                [
                    source_row("wrr2_32_app_04", "$LMHMXLMA", "1", "delete_one@1"),
                    source_row("wrr2_32_app_05", "$LMHMX@LMA", "0", "none"),
                ],
            )
            write_csv(
                ocr,
                [
                    row_ocr("wrr2_32_app_01", "RBY$LMH", "wrr_appellation", "matched"),
                    row_ocr("wrr2_32_app_04", "$LMHMXLMA", "wrr_appellation", "not_matched"),
                    row_ocr("wrr2_32_app_05", "$LMHMX@LMA", "wrr_appellation", "not_matched"),
                    row_ocr("wrr2_32_date_01", "/KA/TMWZ", "wrr_date", "matched"),
                ],
            )
            write_csv(
                scenarios,
                [
                    scenario_row("review_chelm_spelling_only", "wrr2_32_app_04"),
                    scenario_row("review_chelm_spelling_only", "wrr2_32_app_05"),
                ],
            )
            write_csv(
                table,
                [
                    {
                        "row_number": "32",
                        "current_read": "Primary English row label and secondary WRR2 record align.",
                    }
                ],
            )
            wnp.write_text("\n".join(f"line {index}" for index in range(1, 1055)), encoding="utf-8")

            rc = packet.main(
                [
                    "--action-plan",
                    str(action),
                    "--source-queue",
                    str(source),
                    "--row-ocr",
                    str(ocr),
                    "--scenario-pairs",
                    str(scenarios),
                    "--table2-bridge",
                    str(table),
                    "--wnp-html",
                    str(wnp),
                    "--out",
                    str(out),
                    "--source-context-out",
                    str(context),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertEqual(len(list(csv.DictReader(context.open(encoding="utf-8")))), 3)
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["priority_source_policy_terms"], "1")
            self.assertIn("WRR Source-Policy Evidence Packet", md.read_text(encoding="utf-8"))
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["evidence_rows"], 1)


def source_row(term_id: str, term: str, hits: str, rule: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "term": term,
        "concepts": "WRR2 32",
        "source_review_flags": "wnp_chelm_spelling_context",
        "row_ocr_status": "not_matched",
        "best_variant_hit_count": hits,
        "best_variant_rule": rule,
        "source_review_action": "source/pair-rule review",
        "visual_review_action": "review source/pair rule",
    }


def row_ocr(term_id: str, term: str, category: str, status: str) -> dict[str, str]:
    return {
        "term_id": term_id,
        "concept": "WRR2 32",
        "category": category,
        "michigan_term": term,
        "row_ocr_status": status,
        "row_ocr_text_normalized": "רבישלמהה",
    }


def scenario_row(scenario: str, term_id: str) -> dict[str, str]:
    return {
        "scenario": scenario,
        "scenario_action": "review_only_no_exclusion",
        "pair_id": f"{term_id}__wrr2_32_date_01",
        "concept": "WRR2 32",
        "appellation_term_id": term_id,
        "source_review_flags": "wnp_chelm_spelling_context",
        "pair_review_status": "needs_primary_source_pair_rule",
        "candidate_lane": "appellation_min_length_candidate",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
