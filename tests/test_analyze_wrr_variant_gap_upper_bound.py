import csv
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_wrr_variant_gap_upper_bound as upper


class WrrVariantGapUpperBoundTests(unittest.TestCase):
    def test_build_rows_bounds_simple_variant_gap_closure(self) -> None:
        rows = upper.build_rows(
            [
                {
                    "run_label": "all_lanes_cap1000",
                    "defined": "72",
                    "source_cited_defined_distances": "163",
                    "defined_gap_to_source_cited": "91",
                }
            ],
            [
                {
                    "run_label": "all_lanes_cap1000",
                    "impact_status": "all_blocking_terms_have_variant_hit",
                    "pairs": "51",
                },
                {
                    "run_label": "all_lanes_cap1000",
                    "impact_status": "some_blocking_terms_have_variant_hit",
                    "pairs": "9",
                },
                {
                    "run_label": "all_lanes_cap1000",
                    "impact_status": "no_blocking_term_variant_hit",
                    "pairs": "50",
                },
            ],
        )

        self.assertEqual(rows[0]["upper_bound_defined_distances"], "123")
        self.assertEqual(rows[0]["residual_gap_after_simple_variant_upper_bound"], "40")
        self.assertEqual(rows[0]["gap_coverage_percent"], "56.04")

    def test_main_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            defined = root / "defined.csv"
            variants = root / "variants.csv"
            out = root / "out.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(
                defined,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "defined": "72",
                        "source_cited_defined_distances": "163",
                        "defined_gap_to_source_cited": "91",
                    }
                ],
            )
            write_csv(
                variants,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "impact_status": "all_blocking_terms_have_variant_hit",
                        "pairs": "51",
                    }
                ],
            )

            rc = upper.main(
                [
                    "--defined-pair-summary",
                    str(defined),
                    "--variant-gap-summary",
                    str(variants),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            rows = list(csv.DictReader(out.open(encoding="utf-8")))
            self.assertEqual(rows[0]["current_gap_to_source_cited"], "91")
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("WRR Variant Gap Upper Bound", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
