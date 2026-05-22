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
            source_review_summary=[
                {"source_review_flags": "2 wnp_disputed_zacut_appellation"},
                {"source_review_flags": "1 wnp_book_title_appellation_dispute"},
            ],
            source_policy_scenarios=[
                {
                    "scenario": "keep_all_working_source",
                    "remaining_appellation_min_length_pairs": "165",
                    "gap_to_source_cited_163_after_appellation_min_length": "-2",
                    "remaining_length_filtered_pairs": "86",
                },
                {
                    "scenario": "exclude_wnp_zacut_only",
                    "remaining_appellation_min_length_pairs": "157",
                    "gap_to_source_cited_163_after_appellation_min_length": "6",
                    "remaining_length_filtered_pairs": "78",
                },
                {
                    "scenario": "exclude_all_source_review_flags",
                    "remaining_appellation_min_length_pairs": "154",
                    "gap_to_source_cited_163_after_appellation_min_length": "9",
                    "remaining_length_filtered_pairs": "78",
                },
            ],
            source_policy_term_impacts=[
                {
                    "term": "ZKWTA",
                    "remaining_appellation_min_length_pairs_if_excluded": "163",
                    "gap_to_source_cited_163_after_appellation_min_length_if_excluded": "0",
                    "closes_appellation_min_length_gap_to_163": "true",
                }
            ],
            direct_all_lanes_250={"defined_corrected_distances": "50"},
            direct_all_lanes_1000={"defined_corrected_distances": "72"},
            direct_all_lanes_1000_program={"defined_corrected_distances": "72"},
            direct_all_lanes_program_changed_pairs=0,
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
        self.assertIn(
            "50 distances at cap 250 and 72 at cap 1000",
            by_option["defined-distance output interpretation"]["evidence"],
        )
        self.assertEqual(by_option["single Zacut appellation exclusion"]["status"], "diagnostic_only")
        self.assertEqual(
            by_option["repo-defined WNP-excluded 999,999 date-label diagnostic"]["claim_boundary"],
            "diagnostic only",
        )
        self.assertIn(
            "3 WNP/context queued terms",
            by_option["WNP/context flagged source-review queue"]["evidence"],
        )
        self.assertEqual(
            by_option["source-policy scenario impact"]["status"],
            "diagnostic_scenario_only",
        )
        self.assertIn(
            "exclude WNP Zacut: 157 >=5 pairs",
            by_option["source-policy scenario impact"]["evidence"],
        )
        self.assertIn(
            "Single-term impact",
            by_option["source-policy scenario impact"]["evidence"],
        )
        self.assertIn("ZKWTA", by_option["source-policy scenario impact"]["evidence"])
        self.assertIn(
            "printed/program/fixed250 = 28/28/28",
            by_option["reported WRR-program formula"]["evidence"],
        )
        self.assertIn(
            "changes 0 pair rows versus printed",
            by_option["reported WRR-program formula"]["evidence"],
        )

    def test_compare_corrected_distance_changes_counts_pair_differences(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            left = root / "left.csv"
            right = root / "right.csv"
            write_csv(
                left,
                [
                    {
                        "pair_id": "a",
                        "corrected_distance": "0.1",
                        "corrected_distance_status": "defined",
                        "pair_valid_perturbations": "10",
                    },
                    {
                        "pair_id": "b",
                        "corrected_distance": "",
                        "corrected_distance_status": "ordinary_not_valid",
                        "pair_valid_perturbations": "0",
                    },
                ],
            )
            write_csv(
                right,
                [
                    {
                        "pair_id": "a",
                        "corrected_distance": "0.1",
                        "corrected_distance_status": "defined",
                        "pair_valid_perturbations": "10",
                    },
                    {
                        "pair_id": "b",
                        "corrected_distance": "0.2",
                        "corrected_distance_status": "defined",
                        "pair_valid_perturbations": "11",
                    },
                ],
            )

            self.assertEqual(lock_options.compare_corrected_distance_changes(left, right), 1)

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pair = root / "pair.csv"
            skip = root / "skip.csv"
            variants = root / "variants.csv"
            permutation = root / "perm.csv"
            source_review_summary = root / "source_review_summary.csv"
            source_policy_scenarios = root / "source_policy_scenarios.csv"
            source_policy_term_impacts = root / "source_policy_term_impacts.csv"
            direct_250 = root / "direct_250.csv"
            direct_1000 = root / "direct_1000.csv"
            direct_1000_program = root / "direct_1000_program.csv"
            direct_rows = root / "direct_rows.csv"
            direct_program_rows = root / "direct_program_rows.csv"
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
            write_csv(
                source_review_summary,
                [
                    {"source_review_flags": "2 wnp_disputed_zacut_appellation"},
                    {"source_review_flags": "1 wnp_book_title_appellation_dispute"},
                ],
            )
            write_csv(
                source_policy_scenarios,
                [
                    {
                        "scenario": "exclude_wnp_zacut_only",
                        "remaining_appellation_min_length_pairs": "157",
                        "gap_to_source_cited_163_after_appellation_min_length": "6",
                        "remaining_length_filtered_pairs": "78",
                    }
                ],
            )
            write_csv(
                source_policy_term_impacts,
                [
                    {
                        "term": "ZKWTA",
                        "remaining_appellation_min_length_pairs_if_excluded": "163",
                        "gap_to_source_cited_163_after_appellation_min_length_if_excluded": "0",
                        "closes_appellation_min_length_gap_to_163": "true",
                    }
                ],
            )
            write_csv(direct_250, [{"defined_corrected_distances": "50"}])
            write_csv(direct_1000, [{"defined_corrected_distances": "72"}])
            write_csv(direct_1000_program, [{"defined_corrected_distances": "72"}])
            direct_row_payload = [
                {
                    "pair_id": "a",
                    "corrected_distance": "0.1",
                    "corrected_distance_status": "defined",
                    "pair_valid_perturbations": "10",
                }
            ]
            write_csv(direct_rows, direct_row_payload)
            write_csv(direct_program_rows, direct_row_payload)

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
                    "--source-review-summary",
                    str(source_review_summary),
                    "--source-policy-scenarios",
                    str(source_policy_scenarios),
                    "--source-policy-term-impacts",
                    str(source_policy_term_impacts),
                    "--direct-all-lanes-250-summary",
                    str(direct_250),
                    "--direct-all-lanes-1000-summary",
                    str(direct_1000),
                    "--direct-all-lanes-1000-program-summary",
                    str(direct_1000_program),
                    "--direct-all-lanes-1000",
                    str(direct_rows),
                    "--direct-all-lanes-1000-program",
                    str(direct_program_rows),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            self.assertEqual(rc, 0)
            self.assertEqual(len(list(csv.DictReader(out.open(encoding="utf-8")))), 9)
            text = markdown.read_text(encoding="utf-8")
            self.assertIn("Status: decision aid, not a WRR reproduction.", text)
            self.assertIn("Current No-Input Path", text)
            self.assertIn("WNP/context queued terms", text)
            self.assertIn("source-policy scenario impact", text)
            self.assertIn("Single-term impact", text)
            self.assertIn("changes 0 pair rows", text)
            self.assertIn("Recommended no-input working posture:", text)
            self.assertIn(
                "No source-review flag or visual-review note excludes a pair automatically.",
                text,
            )
            self.assertTrue(manifest.exists())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
