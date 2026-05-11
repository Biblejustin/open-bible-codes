import json
import tempfile
import unittest
from pathlib import Path

from els.protocol_runner import load_protocol
from scripts import build_real_report_run_summary as summary
from scripts import preflight_real_report_run as preflight


class RealReportRunTests(unittest.TestCase):
    def test_forbidden_hits_detects_forbidden_account_text(self) -> None:
        account_part = "sp" + "lunk"
        account = "justin-" + account_part
        self.assertEqual(
            preflight.forbidden_hits(f"git@github.com:{account}/repo"),
            {account, account_part},
        )

    def test_preflight_scan_skips_reports_and_data(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "reports").mkdir()
            (root / "reports" / "old.md").write_text("justin-" + ("sp" + "lunk"), encoding="utf-8")
            (root / "ok.md").write_text("Biblejustin only", encoding="utf-8")
            self.assertEqual(preflight.scan_forbidden_terms(root), [])

    def test_real_report_preflight_and_summary_are_not_resume_cached(self) -> None:
        protocol = load_protocol("protocols/real_report_run.toml")
        steps_by_id = {step["id"]: step for step in protocol["steps"]}

        self.assertTrue(steps_by_id["preflight"]["always_run"])
        self.assertTrue(steps_by_id["real_report_summary"]["always_run"])
        self.assertIn("wrr_audit_counts", steps_by_id)
        self.assertIn("scripts/release_hygiene.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_public_release_hygiene.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_REPLICATION_PLAN.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("claims/claim_catalog.csv", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/CLAIM_CATALOG.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("configs/prospective_study_lanes.json", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_prospective_study_lanes.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/FINAL_REPORT_OUTLINE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/FINAL_REPORT_DRAFT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/FINAL_REPORT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/PROSPECTIVE_STUDY_NEXT_LOCK.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/hebrew_modern_geopolitical_prospective.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("hebrew_modern_geopolitical_prospective", steps_by_id)
        self.assertIn(
            "protocols/gog_magog_pair_prospective.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/APOCRYPHA_ONLY_COUNTS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/APOCRYPHA_BRIDGE_CONTEXT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("all_codes_followup_letter_paths", steps_by_id)
        self.assertIn("all_codes_followup_context", steps_by_id)
        self.assertIn("all_codes_followup_extensions", steps_by_id)
        self.assertIn("all_codes_compound_extension_controls", steps_by_id)
        self.assertIn("all_codes_followup_review", steps_by_id)
        self.assertIn("external_claim_source_counts", steps_by_id)
        self.assertIn("external_claim_source_all_codes_collection", steps_by_id)
        for step_id in [
            "greek_expanded_surface_queue",
            "greek_expanded_surface_triage",
            "greek_expanded_surface_control_pool",
            "greek_expanded_surface_control_evaluation",
            "greek_expanded_surface_available_control_evaluation",
            "greek_expanded_surface_followup",
            "greek_surface_length4_followup",
            "greek_surface_length4_vocabulary_controls",
        ]:
            self.assertIn("els/term_display.py", steps_by_id[step_id]["inputs"])
        self.assertIn(
            "reports/centered_occurrence_index/presence_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/apocrypha_bridge_context/context.csv",
            steps_by_id["centered_occurrence_index"]["inputs"],
        )
        self.assertIn(
            "reports/kjv_apocrypha_bridge_context/context.csv",
            steps_by_id["centered_occurrence_index"]["inputs"],
        )
        self.assertIn("final_report_highlights", steps_by_id)
        self.assertIn(
            "reports/final_report_highlights/highlights.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/external_claim_source_counts/summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/external_claim_source_all_codes/triage_queue.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/ALL_CODES_FOLLOWUP_REVIEW.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/ALL_CODES_FOLLOWUP_CONTEXT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/WRR_REPLICATION_PLAN.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/release_hygiene.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_public_release_hygiene.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("claims/claim_catalog.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/CLAIM_CATALOG.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/prospective_study_lanes.json", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_prospective_study_lanes.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/FINAL_REPORT_OUTLINE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/FINAL_REPORT_DRAFT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/FINAL_REPORT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/PROSPECTIVE_STUDY_NEXT_LOCK.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/GOG_MAGOG_PAIR_PROSPECTIVE_REPORT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/gog_magog_pair_prospective.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("terms/gog_magog_pair_prospective_terms.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/hebrew_modern_geopolitical_prospective.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "terms/hebrew_modern_geopolitical_prospective_terms.csv",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/APOCRYPHA_BRIDGE_STUDY.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/APOCRYPHA_SOURCE_COVERAGE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/APOCRYPHA_BRIDGE_CANDIDATES.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/APOCRYPHA_BRIDGE_CONTEXT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/APOCRYPHA_BRIDGE_CONTROLS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/APOCRYPHA_ONLY_COUNTS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/KJV_APOCRYPHA_ONLY_COUNTS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/KJV_APOCRYPHA_BRIDGE_CANDIDATES.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/KJV_APOCRYPHA_BRIDGE_CONTEXT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/KJV_APOCRYPHA_BRIDGE_CONTROLS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/KJV_APOCRYPHA_BRIDGE_SHUFFLED_CONTROLS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/EXTERNAL_CLAIM_SOURCE_COUNTS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_COLLECTION.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/external_claim_source_counts.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("configs/example_ebible_engkjv_apocrypha.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/apocrypha_bridge_study.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/ALL_CODES_FOLLOWUP_REVIEW.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/ALL_CODES_FOLLOWUP_CONTEXT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/FINAL_REPORT_HIGHLIGHTS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/build_final_report_highlights.py", preflight.DEFAULT_REQUIRED_PATHS)

    def test_preflight_required_paths_match_protocol_inputs(self) -> None:
        protocol = load_protocol("protocols/real_report_run.toml")
        preflight_step = next(step for step in protocol["steps"] if step["id"] == "preflight")

        self.assertEqual(
            set(preflight.DEFAULT_REQUIRED_PATHS),
            set(preflight_step["inputs"]),
        )

    def test_preflight_payload_records_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "preflight.json"

            code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 0)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["output_path"], str(out))
            self.assertIn("git_commit", payload)
            self.assertIn("risky_tracked_paths", payload)
            self.assertIn("secret_pattern_hits", payload)

    def test_summary_percent_formats_rates(self) -> None:
        self.assertEqual(summary.percent(0.0244863), "2.449%")
        self.assertEqual(summary.percent("bad"), "0.000%")

    def test_int_value_handles_missing_or_bad_values(self) -> None:
        self.assertEqual(summary.int_value({"x": 12.9}, "x"), 12)
        self.assertEqual(summary.int_value({"x": "bad"}, "x"), 0)

    def test_doxa_q_range_formats_report_range(self) -> None:
        rows = [{"combined_min_q": "0.0008"}, {"combined_min_q": "0.0016"}]
        self.assertEqual(summary.q_range(rows), "0.0008..0.0016")

    def test_surface_queue_section_counts_scopes(self) -> None:
        lines = summary.surface_queue_section(
            [
                {
                    "term_id": "amen_g",
                    "concept": "Amen",
                    "normalized_term": "αμην",
                    "total_exact_center_hits": "101",
                    "unique_patterns": "44",
                    "all_source_patterns": "11",
                    "multi_source_patterns": "14",
                }
            ],
            [
                {"presence_scope": "all_sources"},
                {"presence_scope": "multi_source"},
                {"presence_scope": "source_only"},
            ],
            {"status": "completed", "duration_seconds": 1.23},
        )
        text = "\n".join(lines)
        self.assertIn("| All-source | 1 |", text)
        self.assertIn("`αμην`", text)

    def test_surface_triage_section_lists_selected_rows(self) -> None:
        lines = summary.surface_triage_section(
            [
                {
                    "term_id": "gpx_lawlessness_g",
                    "concept": "Lawlessness",
                    "normalized_term": "ανομια",
                    "center_ref": "Matt 7:23",
                    "skip": "20",
                    "direction": "forward",
                    "length_cohort_all_source_rank": "1",
                }
            ],
            [
                {
                    "read": "all-source but below length threshold",
                    "all_source_patterns": "24",
                }
            ],
            {"status": "completed", "duration_seconds": 0.05},
        )
        text = "\n".join(lines)
        self.assertIn("Selected patterns: 1", text)
        self.assertIn("`ανομια`", text)
        self.assertIn("all-source patterns below length threshold: 24", text)

    def test_surface_letter_paths_section_lists_sequences(self) -> None:
        lines = summary.surface_letter_paths_section(
            [
                {
                    "normalized_term": "ανομια",
                    "corpus": "TR_NT",
                    "sequence": "ανομια",
                    "skip": "20",
                    "center_ref": "MAT 7:23",
                    "center_word": "Οὐδέποτε",
                }
            ],
            {"status": "completed", "duration_seconds": 0.7},
        )
        text = "\n".join(lines)
        self.assertIn("## Expanded Greek Surface Letter Paths", text)
        self.assertIn("`ανομια`", text)
        self.assertIn("Οὐδέποτε", text)

    def test_surface_control_pool_section_lists_closest_controls(self) -> None:
        lines = summary.surface_control_pool_section(
            [
                {
                    "term_id": "gpx_lawlessness_g",
                    "normalized_term": "ανομια",
                    "selected_target": "True",
                    "all_source_surface_present": "True",
                    "surface_verses_tr_nt": "12",
                    "surface_verses_byz_nt": "12",
                    "surface_verses_tcg_nt": "12",
                    "surface_verses_sblgnt": "13",
                    "surface_verse_sum": "49",
                },
                {
                    "term_id": "gpx_darkness_g",
                    "selected_target": "False",
                    "all_source_surface_present": "True",
                },
            ],
            [
                {
                    "target_term_id": "gpx_lawlessness_g",
                    "control_normalized_term": "σκοτοσ",
                    "surface_vector_l1_delta": "3",
                }
            ],
            {"status": "completed", "duration_seconds": 1.2},
        )
        text = "\n".join(lines)
        self.assertIn("Terms measured: 2", text)
        self.assertIn("`σκοτοσ` (skotos) (3)", text)

    def test_surface_control_evaluation_section_lists_p_values(self) -> None:
        lines = summary.surface_control_evaluation_section(
            [
                {
                    "target_normalized_term": "ανομια",
                    "observed_all_source_patterns": "1",
                    "controls_ge_observed_all_source": "0",
                    "all_source_p_ge": "0.090909",
                    "all_source_q_value": "0.090909",
                }
            ],
            {"status": "completed", "duration_seconds": 0.04},
        )
        text = "\n".join(lines)
        self.assertIn("`ανομια`", text)
        self.assertIn("0.090909", text)

    def test_surface_control_evaluation_section_accepts_custom_title_and_lead(self) -> None:
        lines = summary.surface_control_evaluation_section(
            [
                {
                    "target_normalized_term": "ανομια",
                    "observed_all_source_patterns": "1",
                    "controls_ge_observed_all_source": "0",
                    "all_source_p_ge": "0.032258",
                    "all_source_q_value": "0.058824",
                }
            ],
            {"status": "completed", "duration_seconds": 0.04},
            title="Expanded Greek Surface All-Available Control Evaluation",
            lead="All available controls narrow the remaining signal.",
            read="Current read: strongest remaining row, still post-screen.",
        )
        text = "\n".join(lines)
        self.assertIn("## Expanded Greek Surface All-Available Control Evaluation", text)
        self.assertIn("All available controls narrow the remaining signal.", text)
        self.assertIn("Current read: strongest remaining row, still post-screen.", text)
        self.assertIn("0.032258", text)

    def test_surface_followup_section_lists_status_and_counts(self) -> None:
        lines = summary.surface_followup_section(
            {
                "status": "post_screen_surface_followup_review_candidate",
                "selected_rows": 3,
                "path_rows": 12,
                "control_rows": 3,
            },
            {"status": "completed", "duration_seconds": 0.08},
        )
        text = "\n".join(lines)
        self.assertIn("## Expanded Greek Surface Follow-Up Report", text)
        self.assertIn("post_screen_surface_followup_review_candidate", text)
        self.assertIn("| Letter-path audit rows | 12 |", text)

    def test_length4_vocabulary_controls_section_lists_overlap_read(self) -> None:
        lines = summary.surface_length4_vocabulary_controls_section(
            {"target_rows": 7, "control_rows": 572},
            [
                {
                    "target_normalized_term": "αμην",
                    "observed_all_source_patterns": "11",
                    "controls_ge_observed_all_source": "69",
                    "all_source_p_ge": "0.348259",
                    "all_source_q_value": "0.441127",
                    "matched_controls": "200",
                }
            ],
            {"status": "success", "duration_seconds": 40.9},
        )
        text = "\n".join(lines)
        self.assertIn("Generated vocabulary controls | 572", text)
        self.assertIn("`αμην`", text)
        self.assertIn("overlaps every length-4", text)

    def test_wrr_audit_section_keeps_under_specified_read(self) -> None:
        lines = summary.wrr_audit_section(
            {"status": "success", "duration_seconds": 12.3},
            {
                "downloads": [
                    {"label": "wrr_1994_paper", "sha256": "paperhash"},
                    {"label": "wrr1", "sha256": "wrr1hash"},
                    {"label": "wrr2", "sha256": "abc"},
                    {"label": "se2a", "sha256": "se2ahash"},
                    {"label": "se2b", "sha256": "se2bhash"},
                    {"label": "se3", "sha256": "se3hash"},
                    {"label": "mc_key", "sha256": "def"},
                    {"label": "wrr_nations_mc", "sha256": "nationsmc"},
                    {"label": "wrr_nations_gir", "sha256": "nationsgir"},
                    {"label": "wnp_mc", "sha256": "wnpmc"},
                    {"label": "wnp_en", "sha256": "wnpen"},
                ]
            },
            [
                {
                    "source_raw_sha256": "rawhash",
                    "source_text_sha256": "texthash",
                    "normalized_text_sha256": "normhash",
                    "normalized_letters": "78064",
                    "verse_count": "2075",
                }
            ],
            [
                {
                    "parsed_files": "5",
                    "files_matching_expected_pairs": "0",
                    "max_same_record_pairs": "193",
                }
            ],
            [
                {
                    "concept": "WRR2 01",
                    "appellation_rows": "2",
                    "date_rows": "1",
                    "appellation_hits": "12",
                    "date_hits": "3",
                }
            ],
            [
                {
                    "concept": "WRR2 01",
                    "pair_rows": "2",
                    "all_pairs_within_gap": "5",
                    "all_overlap_pairs": "3",
                    "strict_pairs_within_gap": "0",
                    "best_wrr_alpha": "1.2",
                }
            ],
            [
                {
                    "band": "not_unusual",
                    "combined_min_q": "0.40",
                }
            ],
            [
                {
                    "cap_le_observed_max_skip": "1",
                    "target_unreached_rows": "4",
                }
            ],
            [
                {
                    "imported_same_record_pairs": "182",
                    "appellation_min_length_same_record_pairs": "165",
                    "length_filtered_same_record_pairs": "86",
                    "imported_pair_gap_to_expected": "-19",
                    "appellation_min_length_gap_to_expected": "-2",
                    "length_filtered_gap_to_expected": "77",
                    "wnp_disputed_zacut_appellation_rows": "4",
                    "wnp_disputed_zacut_appellation_min_length_pair_delta": "8",
                    "appellation_min_length_pairs_after_one_zacut_appellation_excluded": "163",
                    "appellation_min_length_gap_after_one_zacut_appellation_excluded": "0",
                }
            ],
            [
                {
                    "rows": "120",
                    "rows_with_hits": "64",
                    "rows_with_sample_under_10_valid": "0",
                    "ordinary_in_bounds_failures": "0",
                }
            ],
        )
        text = "\n".join(lines)

        self.assertIn("## WRR 1994 Source Audit", text)
        self.assertIn("WRR remains `under_specified`", text)
        self.assertIn("| WRR 1994 paper PDF | `paperhash` |", text)
        self.assertIn("| WRR/Nations MC page | `nationsmc` |", text)
        self.assertIn("| WRR/Nations Hebrew page | `nationsgir` |", text)
        self.assertIn("| WNP source critique MC page | `wnpmc` |", text)
        self.assertIn("| Normalized text SHA-256 | `normhash` |", text)
        self.assertIn("| Length 5..8 adjusted control-signal rows | 0 |", text)
        self.assertIn("| Length 5..8 best diagnostic WRR alpha | 1.2 |", text)
        self.assertIn("| WRR paper second-list candidate word pairs | 298 |", text)
        self.assertIn("| WRR/Nations cited second-list defined distances | 163 |", text)
        self.assertIn("| ANU source files matching 163 raw pairs | 0 |", text)
        self.assertIn("| Appellation length >= 5 source-record pairs | 165 |", text)
        self.assertIn("| Gap after one Zacut appellation exclusion | 0 |", text)
        self.assertIn("| Gap to source-cited 163 distances after length filter | 77 |", text)
        self.assertIn("| Perturbation diagnostic rows | 120 |", text)

    def test_wrr_audit_section_requires_all_source_hashes(self) -> None:
        with self.assertRaisesRegex(ValueError, "wrr_nations_mc"):
            summary.wrr_audit_section(
                {"status": "success", "duration_seconds": 12.3},
                {"downloads": [{"label": "wrr_1994_paper", "sha256": "paperhash"}]},
                [],
                [],
                [],
                [],
                [],
                [],
                [],
                [],
            )

    def test_all_codes_triage_section_lists_letter_path_audit(self) -> None:
        lines = summary.all_codes_triage_section(
            {"scanned_rows": 10, "queue_rows": 3, "selected_keys": 2, "bucket_counts": {}},
            {"scanned_rows": 20, "queue_rows": 4, "selected_keys": 3, "bucket_counts": {}},
            {"scanned_rows": 30, "queue_rows": 5, "selected_keys": 4, "bucket_counts": {}},
            {"selected_rows": 2, "queue_rows": 12, "selected_by_queue": {"greek": 1}},
            [{"audit_corpus": "TR_NT"}, {"audit_corpus": "SBLGNT"}],
            {"letter_rows": 8, "mismatches": 0, "summary_by_corpus": {"TR_NT": 1}},
            [{"audit_corpus": "TR_NT"}],
            {
                "excerpt_rows": 1,
                "center_contains_normalized_term_rows": 1,
                "span_contains_normalized_term_rows": 1,
            },
            [{"extension_rows": "2"}],
            {
                "selected_rows_with_extensions": 1,
                "extension_rows": 2,
                "max_extension_length": 4,
                "extension_rows_by_type": {"before_plus_term": 2},
            },
            [
                {
                    "extension_band": "extension_q_le_0.05",
                    "all_controls_band": "all_controls_q_le_0.10",
                }
            ],
            {
                "targets": 1,
                "term_control_samples": 25,
                "random_control_samples": 25,
            },
            [
                {
                    "all_controls_band": "all_controls_q_le_0.01",
                    "all_controls_max_q": "0.003599",
                }
            ],
            {
                "targets": 1,
                "term_control_samples": 5000,
                "random_control_samples": 5000,
            },
            {"status": "success"},
            [{"review_status": "strongest_manual_review"}],
            {
                "summary_rows": 1,
                "review_status_counts": {
                    "strongest_manual_review": 1,
                    "hidden_path_review": 0,
                },
            },
        )
        text = "\n".join(lines)

        self.assertIn("Letter-path audit", text)
        self.assertIn("path summary rows: 2", text)
        self.assertIn("sequence mismatches: 0", text)
        self.assertIn("Manual-review packet", text)
        self.assertIn("Context excerpts", text)
        self.assertIn("Same-skip extension audit", text)
        self.assertIn("selected rows with extensions: 1", text)
        self.assertIn("Compound-extension paired controls", text)
        self.assertIn("all-control q band counts", text)
        self.assertIn("post-screen flags only", text)
        self.assertIn("Compound-extension confirmatory controls", text)
        self.assertIn("term controls per target: 5,000", text)
        self.assertIn("conservative all-control q range: 0.003599..0.003599", text)
        self.assertIn("locked post-discovery confirmatory review candidate", text)
        self.assertIn("strongest same-surface-word rows: 1", text)
        self.assertIn("work queues", text)

    def test_centered_occurrence_section_summarizes_presence_rows(self) -> None:
        lines = summary.centered_occurrence_section(
            [
                {
                    "summary_rank": "1",
                    "occurrence_type": "centered_self_exact_word",
                    "source_family": "gog_source_review",
                    "corpus_class": "bible",
                    "normalized_term": "γωγ",
                    "center_ref": "REV 20:8",
                    "center_word": "Gog",
                    "corpora": "BYZ_NT;SBLGNT;TCG_NT;TR_NT",
                    "occurrence_rows": "4",
                    "total_paths": "14",
                    "frequency_reads": "short-form caution",
                },
                {
                    "summary_rank": "2",
                    "occurrence_type": "centered_self_exact_word",
                    "source_family": "control",
                    "corpus_class": "control",
                    "normalized_term": "abc",
                    "center_ref": "X 1:1",
                    "center_word": "abc",
                    "corpora": "CONTROL",
                    "occurrence_rows": "1",
                    "total_paths": "1",
                    "frequency_reads": "control",
                },
            ],
            {"rows": 5},
        )
        text = "\n".join(lines)

        self.assertIn("## Centered Occurrence Index", text)
        self.assertIn("| Bible presence rows | 1 |", text)
        self.assertIn("| Control presence rows | 1 |", text)
        self.assertIn("`γωγ`", text)
        self.assertIn("REV 20:8", text)
        self.assertIn("short length still", text)

    def test_external_claim_source_section_summarizes_counts_and_triage(self) -> None:
        lines = summary.external_claim_source_section(
            [
                {
                    "term_set": "bible_code_digest_claim_terms",
                    "corpus": "MT_WLC",
                    "counted_rows": "3",
                    "zero_rows": "1",
                    "total_hits": "42",
                    "max_term_id": "bcd_yhwh_h",
                    "max_normalized_term": "יהוה",
                    "max_concept": "YHWH",
                    "max_hit_count": "25",
                }
            ],
            {"rows": 3},
            [{"term_id": "bcd_yhwh_h"}],
            {
                "aggregates": {
                    "hit_rows": 100,
                    "context_hits": 80,
                    "center_word_exact_hits": 3,
                    "center_word_related_hits": 5,
                    "context_counts": {"exact_center": 40, "hidden_path_only": 20},
                }
            },
            [
                {
                    "overall_rank": "1",
                    "bucket_rank": "1",
                    "bucket": "center_word_exact",
                    "presence_scope": "multi_source",
                    "term_id": "bcd_yhwh_h",
                    "normalized_term": "יהוה",
                    "concept": "YHWH",
                    "center_ref": "1Kgs 10:5",
                    "center_normalized_word": "יהוה",
                    "best_context": "exact_center",
                }
            ],
            {"bucket_counts": {"center_word_exact": 1}},
        )
        text = "\n".join(lines)

        self.assertIn("## External Claim Source Runs", text)
        self.assertIn("| Hidden-path rows retained | 100 |", text)
        self.assertIn("`יהוה` (YHWH; English: YHWH)", text)
        self.assertIn("center_word_exact", text)
        self.assertIn("source's original geometry", text)


if __name__ == "__main__":
    unittest.main()
