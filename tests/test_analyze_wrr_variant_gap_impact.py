import csv
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_variant_gap_impact as impact


class WrrVariantGapImpactTests(unittest.TestCase):
    def test_build_detail_rows_classifies_blocking_term_variant_coverage(self) -> None:
        blocked = [
            {
                "run_label": "sample",
                "pair_id": "p1",
                "concept": "WRR2 01",
                "reason": "ordinary_missing_both_terms",
                "row_ocr_pair_status": "mixed",
                "appellation_term_id": "app1",
                "appellation_term": "APP",
                "date_term_id": "date1",
                "date_term": "DATE",
            },
            {
                "run_label": "sample",
                "pair_id": "p2",
                "concept": "WRR2 02",
                "reason": "ordinary_missing_appellation_hits",
                "row_ocr_pair_status": "both_matched",
                "appellation_term_id": "app2",
                "appellation_term": "APP2",
                "date_term_id": "date2",
                "date_term": "DATE2",
            },
        ]
        variants = impact.best_variants_by_term(
            [
                {
                    "term_id": "app1",
                    "variant_rule": "delete_one@2",
                    "variant_normalized": "AP",
                    "variant_hit_count": "4",
                },
                {
                    "term_id": "date1",
                    "variant_rule": "none_found",
                    "variant_normalized": "DATE",
                    "variant_hit_count": "0",
                },
                {
                    "term_id": "app2",
                    "variant_rule": "delete_one@1",
                    "variant_normalized": "PP2",
                    "variant_hit_count": "8",
                },
            ]
        )

        rows = impact.build_detail_rows(blocked, variants)
        by_pair = {row["pair_id"]: row for row in rows}

        self.assertEqual(
            by_pair["p1"]["impact_status"],
            "some_blocking_terms_have_variant_hit",
        )
        self.assertEqual(
            by_pair["p2"]["impact_status"],
            "all_blocking_terms_have_variant_hit",
        )
        self.assertEqual(by_pair["p2"]["blocking_term_variant_hits"], "8")

    def test_main_writes_summary_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blocked = root / "blocked.csv"
            variants = root / "variants.csv"
            out = root / "out.csv"
            summary = root / "summary.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(
                blocked,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "pair_id": "p1",
                        "concept": "WRR2 01",
                        "reason": "ordinary_missing_appellation_hits",
                        "row_ocr_pair_status": "both_matched",
                        "appellation_term_id": "app1",
                        "appellation_term": "APP",
                        "date_term_id": "date1",
                        "date_term": "DATE",
                    }
                ],
            )
            write_csv(
                variants,
                [
                    {
                        "term_id": "app1",
                        "variant_rule": "delete_one@2",
                        "variant_normalized": "AP",
                        "variant_hit_count": "4",
                    }
                ],
            )

            rc = impact.main(
                [
                    "--blocked-pairs",
                    str(blocked),
                    "--variants",
                    str(variants),
                    "--out",
                    str(out),
                    "--summary-out",
                    str(summary),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(rows[0]["impact_status"], "all_blocking_terms_have_variant_hit")
            summary_rows = list(csv.DictReader(summary.open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["pairs"], "1")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Variant Gap Impact", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
