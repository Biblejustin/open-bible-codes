import csv
import tempfile
import unittest
from pathlib import Path

from scripts.build_wrr_method_status import FIELDNAMES, build_status_rows, main, markdown_cell, write_markdown


class WrrMethodStatusTests(unittest.TestCase):
    def test_build_status_rows_summarizes_open_method_decisions(self) -> None:
        rows = build_status_rows(
            text_row={
                "normalized_letters": "78064",
                "verse_count": "2075",
                "normalized_text_sha256": "abc123",
            },
            pair_row={
                "source_records": "32",
                "source_appellations": "174",
                "source_dates": "31",
                "source_undated_records": "2",
                "source_same_record_pairs": "182",
                "appellation_min_length_same_record_pairs": "165",
                "appellation_min_length": "5",
                "length_filtered_same_record_pairs": "86",
                "length_filter_min": "5",
                "length_filter_max": "8",
                "expected_published_pairs": "163",
            },
            defined_pair_rows=[
                {
                    "run_label": "all_lanes_cap1000",
                    "defined": "72",
                    "source_cited_defined_distances": "163",
                    "defined_gap_to_source_cited": "91",
                    "ordinary_not_valid": "110",
                }
            ],
            defined_gap_reason_rows=[
                {
                    "run_label": "all_lanes_cap1000",
                    "reason": "defined",
                    "pairs": "72",
                    "run_defined": "72",
                },
                {
                    "run_label": "all_lanes_cap1000",
                    "reason": "ordinary_missing_appellation_hits",
                    "pairs": "83",
                    "run_defined": "72",
                },
                {
                    "run_label": "all_lanes_cap1000",
                    "reason": "ordinary_missing_date_hits",
                    "pairs": "12",
                    "run_defined": "72",
                },
                {
                    "run_label": "all_lanes_cap1000",
                    "reason": "ordinary_missing_both_terms",
                    "pairs": "15",
                    "run_defined": "72",
                },
            ],
            zero_hit_variant_rows=[
                {
                    "category": "wrr_appellation",
                    "zero_terms": "105",
                    "terms_with_variant_hit": "48",
                    "terms_without_variant_hit": "57",
                    "best_variant_total_hits": "2981",
                },
                {
                    "category": "wrr_date",
                    "zero_terms": "7",
                    "terms_with_variant_hit": "7",
                    "terms_without_variant_hit": "0",
                    "best_variant_total_hits": "1358",
                },
            ],
            variant_gap_rows=[
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
            variant_residual_rows=[
                {
                    "run_label": "all_lanes_cap1000",
                    "group": "residual_pool",
                    "value": "candidate_pairs_not_closed_by_all-blocker_simple_variants",
                    "pairs": "59",
                    "residual_needed": "40",
                    "candidate_pool_pairs": "59",
                    "residual_slack_pairs": "19",
                },
                {
                    "run_label": "all_lanes_cap1000",
                    "group": "review_frontier",
                    "value": "minimum_residual_frontier",
                    "pairs": "40",
                    "residual_needed": "40",
                    "candidate_pool_pairs": "59",
                    "residual_slack_pairs": "19",
                },
            ],
            skip_row={
                "rows": "120",
                "program_cap_lt_printed": "13",
                "program_cap_eq_printed": "107",
                "target_unreached_rows": "55",
            },
            variant_rows=[
                {"variant": "term_printed", "defined_corrected_distances": "0", "max_pair_valid_perturbations": "3"},
                {"variant": "fixed_250", "defined_corrected_distances": "0", "max_pair_valid_perturbations": "4"},
            ],
            source_policy_rows=[
                {
                    "scenario": "keep_all_working_source",
                    "remaining_appellation_min_length_pairs": "165",
                    "gap_to_source_cited_163_after_appellation_min_length": "-2",
                },
                {
                    "scenario": "exclude_wnp_zacut_only",
                    "remaining_appellation_min_length_pairs": "157",
                    "gap_to_source_cited_163_after_appellation_min_length": "6",
                },
                {
                    "scenario": "exclude_all_source_review_flags",
                    "remaining_appellation_min_length_pairs": "154",
                    "gap_to_source_cited_163_after_appellation_min_length": "9",
                },
            ],
            source_policy_term_impact_rows=[
                {
                    "term": "ZKWTA",
                    "remaining_appellation_min_length_pairs_if_excluded": "163",
                    "gap_to_source_cited_163_after_appellation_min_length_if_excluded": "0",
                    "closes_appellation_min_length_gap_to_163": "true",
                }
            ],
            dw_formula_rows=[
                {
                    "scope": "smoke_length_5_8_cap250",
                    "printed_defined_corrected_distances": "28",
                    "program_defined_corrected_distances": "28",
                    "fixed_250_defined_corrected_distances": "28",
                },
                {
                    "scope": "all_lanes_cap1000",
                    "printed_defined_corrected_distances": "72",
                    "program_defined_corrected_distances": "72",
                    "changed_pairs": "0",
                },
            ],
            primary_result_rows=[
                {
                    "label": "G",
                    "status": "found",
                    "min_statistic": "P4",
                    "min_rank": "4",
                    "bonferroni_p0": "0.000016",
                },
                {"label": "V", "status": "found", "bonferroni_p0": "0.847108"},
            ],
            table2_bridge_row={
                "primary_rows": "32",
                "primary_rows_found": "32",
                "secondary_records": "32",
                "primary_hebrew_cells_verified": "0",
            },
            table2_ocr_row={
                "total_terms": "205",
                "matched_terms": "135",
                "appellation_terms": "174",
                "matched_appellation_terms": "106",
                "date_terms": "31",
                "matched_date_terms": "29",
                "status": "ocr_probe_not_verification",
            },
            table2_row_ocr_row={
                "total_terms": "205",
                "matched_terms": "132",
                "appellation_terms": "174",
                "matched_appellation_terms": "103",
                "date_terms": "31",
                "matched_date_terms": "29",
                "detected_row_markers": "31",
                "inferred_row_markers": "1",
                "status": "row_ocr_probe_not_verification",
            },
            corrected_distance_aggregate_row={
                "rows": "182",
                "defined_corrected_distances": "72",
                "p1": "0.00252257011468",
                "p2": "1.16472976875e-05",
                "p3": "0.0184584022574",
                "p4": "0.000274264355592",
            },
            cross_pair_permutation_row={
                "permutations": "1000",
                "seed": "1994",
                "source": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                "observed_defined_corrected_distances": "72",
                "observed_rows": "182",
                "rho_p1": "0.013986013986",
                "rho_p2": "0.000999000999001",
                "rho_p3": "0.0474525474525",
                "rho_p4": "0.000999000999001",
                "rho0_bonferroni": "0.003996003996",
            },
            cross_pair_recommended_permutation_row={
                "permutations": "999999",
                "seed": "1994",
                "source": "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_corrected_distance_1000.csv",
                "observed_defined_corrected_distances": "72",
                "observed_rows": "182",
                "rho_p1": "0.019722",
                "rho_p2": "0.000101",
                "rho_p3": "0.0506065",
                "rho_p4": "0.000535",
                "rho0_bonferroni": "0.000404",
            },
            highcap_corrected_distance_row={
                "selected_pairs": "182",
                "candidate_lane": "all",
                "search_max_skip": "1000",
                "skip_cap_formula": "printed",
                "pairs": "182",
                "defined_corrected_distances": "72",
                "ordinary_not_valid_pairs": "110",
                "under_minimum_valid_pairs": "0",
                "max_pair_valid_perturbations": "125",
                "status": "diagnostic_only_not_wrr_reproduction",
            },
            highcap_perturbation_row={
                "rows": "120",
                "rows_with_hits": "80",
                "max_exact_perturbation_matches": "12",
                "rows_with_checked_under_10_exact_matches": "80",
            },
            highcap_pair_readiness_row={
                "pairs_ready": "0",
                "pairs_missing_checked_hits": "40",
                "pairs_under_10_exact_matches": "46",
            },
        )

        by_area = {row["decision_area"]: row for row in rows}
        self.assertIn("32/32 primary Table 2", by_area["WRR2 term source"]["evidence"])
        self.assertIn("0 primary Hebrew cells verified", by_area["WRR2 term source"]["evidence"])
        self.assertIn("OCR probe matched 135/205", by_area["WRR2 term source"]["evidence"])
        self.assertIn("row OCR probe matched 132/205", by_area["WRR2 term source"]["evidence"])
        self.assertIn("31 detected row markers", by_area["WRR2 term source"]["evidence"])
        self.assertIn("55/112 zero-hit terms", by_area["WRR2 term source"]["evidence"])
        self.assertIn("diagnostic_only_not_source_correction", by_area["WRR2 term source"]["evidence"])
        self.assertEqual(by_area["WRR2 term source"]["status"], "working_source_locked")
        self.assertIn("User authorized ANU/McKay WRR2", by_area["WRR2 term source"]["current_read"])
        self.assertIn("working corrected-distance runs", by_area["WRR2 term source"]["next_action"])
        self.assertEqual(by_area["Pair universe"]["status"], "source_locked")
        self.assertIn("keep_all_working_source", by_area["Pair universe"]["current_read"])
        self.assertIn("182 raw same-record pairs", by_area["Pair universe"]["evidence"])
        self.assertIn("163 cited second-list distances", by_area["Pair universe"]["evidence"])
        self.assertIn("defined pair-set audit best run all_lanes_cap1000", by_area["Pair universe"]["evidence"])
        self.assertIn("gap 91", by_area["Pair universe"]["evidence"])
        self.assertIn("83 no-appellation ordinary hits", by_area["Pair universe"]["evidence"])
        self.assertIn("source-policy scenarios", by_area["Pair universe"]["evidence"])
        self.assertIn("exclude WNP Zacut >=5 157", by_area["Pair universe"]["evidence"])
        self.assertIn(
            "Visual triage notes do not exclude pairs automatically",
            by_area["Pair universe"]["evidence"],
        )
        self.assertIn(
            "source policy selected: keep_all_working_source",
            by_area["Pair universe"]["evidence"],
        )
        self.assertIn("single-term source-policy impacts", by_area["Pair universe"]["evidence"])
        self.assertIn("ZKWTA", by_area["Pair universe"]["evidence"])
        self.assertIn("variant-gap impact best run all_lanes_cap1000", by_area["Pair universe"]["evidence"])
        self.assertIn("51 blocked pairs have all blocking terms with variant leads", by_area["Pair universe"]["evidence"])
        self.assertIn("variant residual review best run all_lanes_cap1000", by_area["Pair universe"]["evidence"])
        self.assertIn("59 residual candidate pairs", by_area["Pair universe"]["evidence"])
        self.assertIn("40 needed after the simple-variant upper bound", by_area["Pair universe"]["evidence"])
        self.assertEqual(by_area["D(w) skip-cap formula"]["status"], "source_locked")
        self.assertIn("printed WRR formula", by_area["D(w) skip-cap formula"]["current_read"])
        self.assertIn("13 program caps below printed", by_area["D(w) skip-cap formula"]["evidence"])
        self.assertIn("all-lane cap1000 printed/program defined 72/72", by_area["D(w) skip-cap formula"]["evidence"])
        self.assertIn("0 changed pairs", by_area["D(w) skip-cap formula"]["evidence"])
        self.assertIn("printed formula selected as main", by_area["D(w) skip-cap formula"]["evidence"])
        self.assertEqual(by_area["Corrected distance c(w,w')"]["status"], "defined_full_run")
        self.assertIn("maximum valid perturbation count 4", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertIn("full all-lane cap 1000 run: 72 defined over 182 selected pairs", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertIn("max valid 125", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertIn("110 ordinary-not-valid", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertIn("legacy ordinary-hit perturbation diagnostic: 80/120 rows with hits", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertIn("max row-min exact 12", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertIn("legacy ordinary-hit pair readiness: 0 ready, 40 missing hits, 46 under exact", by_area["Corrected distance c(w,w')"]["evidence"])
        self.assertEqual(by_area["Aggregate statistic and permutation"]["status"], "permutation_locked")
        self.assertIn("G min P4 rank 4", by_area["Aggregate statistic and permutation"]["evidence"])
        self.assertIn("72 defined c-values from 182 rows", by_area["Aggregate statistic and permutation"]["evidence"])
        self.assertIn("cap1000 1000-sample date-label diagnostic", by_area["Aggregate statistic and permutation"]["evidence"])
        self.assertIn("rho0=0.003996003996", by_area["Aggregate statistic and permutation"]["evidence"])
        self.assertIn("locked keep-all cap1000 999999", by_area["Aggregate statistic and permutation"]["evidence"])
        self.assertIn("rho0=0.000404", by_area["Aggregate statistic and permutation"]["evidence"])

    def test_corrected_distance_status_summarizes_defined_smoke_rows(self) -> None:
        rows = build_status_rows(
            text_row={
                "normalized_letters": "78064",
                "verse_count": "2075",
                "normalized_text_sha256": "abc123",
            },
            pair_row={
                "source_records": "32",
                "source_appellations": "174",
                "source_dates": "31",
                "source_undated_records": "2",
                "source_same_record_pairs": "182",
                "appellation_min_length_same_record_pairs": "165",
                "appellation_min_length": "5",
                "length_filtered_same_record_pairs": "86",
                "length_filter_min": "5",
                "length_filter_max": "8",
                "expected_published_pairs": "163",
            },
            defined_pair_rows=[],
            defined_gap_reason_rows=[],
            zero_hit_variant_rows=[],
            variant_gap_rows=[],
            variant_residual_rows=[],
            skip_row={
                "rows": "120",
                "program_cap_lt_printed": "13",
                "program_cap_eq_printed": "107",
                "target_unreached_rows": "55",
            },
            variant_rows=[
                {"variant": "term_printed", "defined_corrected_distances": "28", "max_pair_valid_perturbations": "125"},
                {"variant": "fixed_250", "defined_corrected_distances": "28", "max_pair_valid_perturbations": "125"},
            ],
        )

        corrected = {row["decision_area"]: row for row in rows}["Corrected distance c(w,w')"]

        self.assertEqual(corrected["status"], "smoke_only")
        self.assertIn("produces defined corrected distances", corrected["current_read"])
        self.assertIn("keep_all_working_source universe", corrected["current_read"])
        self.assertIn("total defined 56", corrected["evidence"])
        self.assertIn("printed D(w) as main", corrected["next_action"])

    def test_markdown_cell_escapes_pipes(self) -> None:
        self.assertEqual(markdown_cell("a|b\nc"), "a\\|b c")

    def test_write_markdown_emits_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "status.md"
            args = type(
                "Args",
                (),
                {
                    "text_source": Path("text.csv"),
                    "pair_summary": Path("pairs.csv"),
                    "defined_pair_summary": Path("defined_pairs.csv"),
                    "defined_gap_reasons": Path("gap_reasons.csv"),
                    "zero_hit_variant_summary": Path("zero_hit_variants.csv"),
                    "variant_gap_summary": Path("variant_gap.csv"),
                    "variant_residual_summary": Path("variant_residual.csv"),
                    "table2_bridge_summary": Path("bridge_summary.csv"),
                    "table2_ocr_summary": Path("ocr_summary.csv"),
                    "skip_summary": Path("skip.csv"),
                    "corrected_distance_variants": Path("variants.csv"),
                    "source_policy_scenarios": Path("source_policy.csv"),
                    "source_policy_term_impacts": Path("source_policy_terms.csv"),
                    "dw_formula_sensitivity": Path("dw_formula.csv"),
                    "corrected_distance_aggregate": Path("aggregate.csv"),
                    "cross_pair_permutation_summary": Path("missing_permutations.csv"),
                    "cross_pair_recommended_permutation_summary": Path("missing_recommended_permutations.csv"),
                    "highcap_corrected_distance_summary": Path("highcap_corrected.csv"),
                    "highcap_perturbation_summary": Path("highcap_perturbation.csv"),
                    "highcap_pair_readiness_summary": Path("highcap_pair_readiness.csv"),
                    "primary_result_table": Path("primary.csv"),
                    "out": Path("out.csv"),
                    "markdown_out": path,
                    "manifest_out": Path("manifest.json"),
                },
            )()
            write_markdown(
                path,
                [
                    {
                        "decision_area": "Pair universe",
                        "status": "open",
                        "current_read": "current",
                        "evidence": "evidence",
                        "next_action": "next",
                    }
                ],
                args,
            )

            text = path.read_text(encoding="utf-8")

        self.assertIn("# WRR Method Status", text)
        self.assertIn("| Pair universe | `open` | current | evidence | next |", text)
        self.assertIn("## Source Anchors", text)
        self.assertIn("WRR printed D(w) formula", text)

    def test_main_writes_csv_markdown_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            text_source = root / "text.csv"
            pair_summary = root / "pairs.csv"
            defined_pair_summary = root / "defined_pairs.csv"
            defined_gap_reasons = root / "defined_gap_reasons.csv"
            zero_hit_variants = root / "zero_hit_variants.csv"
            variant_gap = root / "variant_gap.csv"
            variant_residual = root / "missing_variant_residual.csv"
            bridge_summary = root / "bridge_summary.csv"
            ocr_summary = root / "ocr_summary.csv"
            row_ocr_summary = root / "row_ocr_summary.csv"
            skip_summary = root / "skip.csv"
            variants = root / "variants.csv"
            source_policy = root / "missing_source_policy.csv"
            source_policy_term_impacts = root / "missing_source_policy_term_impacts.csv"
            dw_formula = root / "missing_dw_formula.csv"
            aggregate = root / "aggregate.csv"
            highcap_corrected = root / "missing_highcap_corrected.csv"
            highcap_perturbation = root / "missing_highcap_perturbation.csv"
            highcap_pair_readiness = root / "missing_highcap_pair_readiness.csv"
            cross_pair_permutations = root / "missing_cross_pair_permutations.csv"
            cross_pair_recommended_permutations = root / "missing_cross_pair_recommended_permutations.csv"
            primary_results = root / "primary.csv"
            out = root / "status.csv"
            markdown = root / "status.md"
            manifest = root / "manifest.json"
            write_dict_rows(
                text_source,
                [
                    {
                        "normalized_letters": "78064",
                        "verse_count": "2075",
                        "normalized_text_sha256": "abc123",
                    }
                ],
            )
            write_dict_rows(
                pair_summary,
                [
                    {
                        "source_records": "32",
                        "source_appellations": "174",
                        "source_dates": "31",
                        "source_undated_records": "2",
                        "source_same_record_pairs": "182",
                        "appellation_min_length_same_record_pairs": "165",
                        "appellation_min_length": "5",
                        "length_filtered_same_record_pairs": "86",
                        "length_filter_min": "5",
                        "length_filter_max": "8",
                        "expected_published_pairs": "163",
                    }
                ],
            )
            write_dict_rows(
                defined_pair_summary,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "defined": "72",
                        "source_cited_defined_distances": "163",
                        "defined_gap_to_source_cited": "91",
                        "ordinary_not_valid": "110",
                    }
                ],
            )
            write_dict_rows(
                defined_gap_reasons,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "reason": "ordinary_missing_appellation_hits",
                        "pairs": "83",
                        "run_defined": "72",
                    }
                ],
            )
            write_dict_rows(
                zero_hit_variants,
                [
                    {
                        "category": "wrr_appellation",
                        "zero_terms": "105",
                        "terms_with_variant_hit": "48",
                        "terms_without_variant_hit": "57",
                        "best_variant_total_hits": "2981",
                    }
                ],
            )
            write_dict_rows(
                variant_gap,
                [
                    {
                        "run_label": "all_lanes_cap1000",
                        "impact_status": "all_blocking_terms_have_variant_hit",
                        "pairs": "51",
                    }
                ],
            )
            write_dict_rows(
                bridge_summary,
                [
                    {
                        "primary_rows": "32",
                        "primary_rows_found": "32",
                        "secondary_records": "32",
                        "primary_hebrew_cells_verified": "0",
                    }
                ],
            )
            write_dict_rows(
                ocr_summary,
                [
                    {
                        "total_terms": "205",
                        "matched_terms": "132",
                        "appellation_terms": "174",
                        "matched_appellation_terms": "103",
                        "date_terms": "31",
                        "matched_date_terms": "29",
                        "status": "ocr_probe_not_verification",
                    }
                ],
            )
            write_dict_rows(
                row_ocr_summary,
                [
                    {
                        "total_terms": "205",
                        "matched_terms": "128",
                        "appellation_terms": "174",
                        "matched_appellation_terms": "99",
                        "date_terms": "31",
                        "matched_date_terms": "29",
                        "detected_row_markers": "31",
                        "inferred_row_markers": "1",
                        "status": "row_ocr_probe_not_verification",
                    }
                ],
            )
            write_dict_rows(
                skip_summary,
                [
                    {
                        "rows": "120",
                        "program_cap_lt_printed": "13",
                        "program_cap_eq_printed": "107",
                        "target_unreached_rows": "55",
                    }
                ],
            )
            write_dict_rows(
                variants,
                [
                    {
                        "variant": "term_printed",
                        "defined_corrected_distances": "0",
                        "max_pair_valid_perturbations": "3",
                    }
                ],
            )
            write_dict_rows(
                aggregate,
                [
                    {
                        "rows": "86",
                        "defined_corrected_distances": "0",
                        "p1": "",
                        "p2": "",
                    }
                ],
            )
            write_dict_rows(
                primary_results,
                [
                    {
                        "label": "G",
                        "status": "found",
                        "min_statistic": "P4",
                        "min_rank": "4",
                        "bonferroni_p0": "0.000016",
                    }
                ],
            )

            rc = main(
                [
                    "--text-source",
                    str(text_source),
                    "--pair-summary",
                    str(pair_summary),
                    "--defined-pair-summary",
                    str(defined_pair_summary),
                    "--defined-gap-reasons",
                    str(defined_gap_reasons),
                    "--zero-hit-variant-summary",
                    str(zero_hit_variants),
                    "--variant-gap-summary",
                    str(variant_gap),
                    "--variant-residual-summary",
                    str(variant_residual),
                    "--table2-bridge-summary",
                    str(bridge_summary),
                    "--table2-ocr-summary",
                    str(ocr_summary),
                    "--table2-row-ocr-summary",
                    str(row_ocr_summary),
                    "--skip-summary",
                    str(skip_summary),
                    "--corrected-distance-variants",
                    str(variants),
                    "--source-policy-scenarios",
                    str(source_policy),
                    "--source-policy-term-impacts",
                    str(source_policy_term_impacts),
                    "--dw-formula-sensitivity",
                    str(dw_formula),
                    "--corrected-distance-aggregate",
                    str(aggregate),
                    "--cross-pair-permutation-summary",
                    str(cross_pair_permutations),
                    "--cross-pair-recommended-permutation-summary",
                    str(cross_pair_recommended_permutations),
                    "--highcap-corrected-distance-summary",
                    str(highcap_corrected),
                    "--highcap-perturbation-summary",
                    str(highcap_perturbation),
                    "--highcap-pair-readiness-summary",
                    str(highcap_pair_readiness),
                    "--primary-result-table",
                    str(primary_results),
                    "--out",
                    str(out),
                    "--markdown-out",
                    str(markdown),
                    "--manifest-out",
                    str(manifest),
                ]
            )

            with out.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(rc, 0)
            self.assertEqual(rows[0]["decision_area"], "Genesis text stream")
            self.assertTrue(markdown.exists())
            self.assertTrue(manifest.exists())


def write_dict_rows(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = sorted({field for row in rows for field in row}) if rows else FIELDNAMES
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
