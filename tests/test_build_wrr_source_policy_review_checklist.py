import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_source_policy_review_checklist as checklist


class WrrSourcePolicyReviewChecklistTests(unittest.TestCase):
    def test_build_checklist_rows_assigns_no_input_state(self) -> None:
        rows = checklist.build_checklist_rows([packet_row()])

        self.assertEqual(rows[0]["review_state"], "pending_source_policy_pair_rule_lock")
        self.assertEqual(rows[0]["allowed_without_input"], "organize evidence only")
        self.assertIn("No source correction", rows[0]["no_input_boundary"])
        self.assertIn("source/pair-rule", rows[0]["required_decision_record"])

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            packet = root / "packet.csv"
            context = root / "context.csv"
            summary = root / "summary.csv"
            out = root / "checklist.csv"
            md = root / "checklist.md"
            manifest = root / "manifest.json"
            write_csv(packet, [packet_row()])
            write_csv(context, [context_row()])
            write_csv(summary, [summary_row()])

            rc = checklist.main(
                [
                    "--packet",
                    str(packet),
                    "--context",
                    str(context),
                    "--summary",
                    str(summary),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(md),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 1)
            self.assertIn(
                "WRR Source-Policy Review Checklist",
                md.read_text(encoding="utf-8"),
            )
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(payload["rows"], 1)
            self.assertEqual(payload["context_rows"], 1)
            self.assertEqual(payload["frontier_pairs"], 1)


def packet_row() -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "evidence_rank": "1",
        "term_id": "wrr2_32_app_05",
        "term": "$LMHMX@LMA",
        "concept": "WRR2 32",
        "source_flags": "wnp_chelm_spelling_context",
        "residual_pairs": "1",
        "frontier_pairs": "1",
        "related_source_term_ids": "wrr2_32_app_04;wrr2_32_app_05",
        "wnp_evidence_refs": "reports/wrr_1994/wnp_en.html:608-619",
    }


def context_row() -> dict[str, str]:
    return {
        "context_id": "wnp_chelm_spelling_argument",
        "source_flag": "wnp_chelm_spelling_context",
        "source_ref": "reports/wrr_1994/wnp_en.html:608-619",
        "source_terms": "clma; cilma; wlmh clma; wlmh cilma",
        "read": "WNP discusses Chelma spellings.",
        "decision_boundary": "No automatic correction.",
    }


def summary_row() -> dict[str, str]:
    return {
        "run_label": "all_lanes_cap1000",
        "priority_source_policy_terms": "1",
        "related_source_review_rows": "2",
        "related_scenario_pair_rows": "4",
        "wnp_context_blocks": "3",
        "decision_boundary": "No automatic correction.",
        "read": "diagnostic",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
