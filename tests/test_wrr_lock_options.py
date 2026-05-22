import csv
import tempfile
import unittest
from pathlib import Path

from scripts import build_wrr_lock_options as lock_options


class WrrLockOptionsTests(unittest.TestCase):
    def test_build_option_rows_marks_diagnostics_not_claim_ready(self) -> None:
        rows = lock_options.build_option_rows(
            pair_row={
                "imported_same_record_pairs": "182",
                "appellation_min_length_same_record_pairs": "165",
                "appellation_min_length_pairs_after_one_zacut_appellation_excluded": "163",
                "expected_published_pairs": "163",
                "length_filtered_same_record_pairs": "86",
                "wnp_disputed_zacut_appellation_min_length_pair_delta": "8",
            },
            skip_row={
                "rows": "120",
                "target_unreached_rows": "55",
                "program_cap_lt_printed": "13",
                "program_cap_eq_printed": "107",
            },
            variant_rows=[
                {"variant": "term_printed", "defined_corrected_distances": "28"},
                {"variant": "term_program", "defined_corrected_distances": "28"},
                {"variant": "fixed_250", "defined_corrected_distances": "28"},
            ],
            permutation_row={
                "permutations": "999999",
                "observed_rows": "174",
                "observed_defined_corrected_distances": "48",
                "rho0_bonferroni": "0.00086",
            },
        )

        by_option = {row["option"]: row for row in rows}
        self.assertEqual(
            by_option["defined-distance output interpretation"]["status"],
            "recommended_working_interpretation",
        )
        self.assertIn(
            "not a raw table count",
            by_option["defined-distance output interpretation"]["evidence"],
        )
        self.assertEqual(by_option["single Zacut appellation exclusion"]["status"], "diagnostic_only")
        self.assertEqual(
            by_option["repo-defined WNP-excluded 999,999 date-label diagnostic"]["claim_boundary"],
            "diagnostic only",
        )
        self.assertIn(
            "printed/program/fixed250 = 28/28/28",
            by_option["reported WRR-program formula"]["evidence"],
        )

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pair = root / "pair.csv"
            skip = root / "skip.csv"
            variants = root / "variants.csv"
            permutation = root / "perm.csv"
            out = root / "out.csv"
            markdown = root / "out.md"
            manifest = root / "manifest.json"
            write_csv(
                pair,
                [
                    {
                        "imported_same_record_pairs": "182",
                        "appellation_min_length_same_record_pairs": "165",
                        "appellation_min_length_pairs_after_one_zacut_appellation_excluded": "163",
                        "expected_published_pairs": "163",
                        "length_filtered_same_record_pairs": "86",
                        "wnp_disputed_zacut_appellation_min_length_pair_delta": "8",
                    }
                ],
            )
            write_csv(
                skip,
                [
                    {
                        "rows": "120",
                        "target_unreached_rows": "55",
                        "program_cap_lt_printed": "13",
                        "program_cap_eq_printed": "107",
                    }
                ],
            )
            write_csv(
                variants,
                [
                    {"variant": "term_printed", "defined_corrected_distances": "28"},
                    {"variant": "term_program", "defined_corrected_distances": "28"},
                    {"variant": "fixed_250", "defined_corrected_distances": "28"},
                ],
            )
            write_csv(
                permutation,
                [
                    {
                        "permutations": "999999",
                        "observed_rows": "174",
                        "observed_defined_corrected_distances": "48",
                        "rho0_bonferroni": "0.00086",
                    }
                ],
            )

            rc = lock_options.main(
                [
                    "--pair-summary",
                    str(pair),
                    "--skip-summary",
                    str(skip),
                    "--variants",
                    str(variants),
                    "--recommended-permutation",
                    str(permutation),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 7)
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("Status: decision aid, not a WRR reproduction.", text)
            self.assertIn("Current No-Input Path", text)
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
