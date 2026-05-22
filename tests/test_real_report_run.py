import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from els.protocol_runner import load_protocol
from scripts import build_real_report_run_summary as summary
from scripts import preflight_real_report_run as preflight
from scripts.download_wrr_sources import REQUIRED_MANIFEST_LABELS


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
        self.assertIn("wrr_cross_pair_grid", steps_by_id)
        self.assertIn(
            "scripts/analyze_wrr_source_policy_scenarios.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/analyze_wrr_dw_formula_sensitivity.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_term_impacts.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn("scripts/release_hygiene.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_public_release_hygiene.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("els/project_index.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/INDEX.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("protocols/INDEX.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_REPLICATION_PLAN.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_METHOD_STATUS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_LOCK_OPTIONS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_CROSS_PAIR_GRID.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/WRR_CLAIM_READINESS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_CLAIM_BLOCKER_PACKET.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_ZERO_HIT_VARIANT_PROBE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_VARIANT_GAP_IMPACT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_VARIANT_GAP_UPPER_BOUND.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/WRR_SOURCE_REVIEW_QUEUE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/WRR_SOURCE_POLICY_SCENARIOS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_DW_FORMULA_SENSITIVITY.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "scripts/check_wrr_source_review_queue_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/analyze_wrr_variant_gap_upper_bound.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_variant_residual_review_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_claim_blocker_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_gap_upper_bound.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_residual_review_packet.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_residual_review_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_residual_review_summary.csv",
            steps_by_id["wrr_cross_pair_grid"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_variant_residual_review_packet.csv",
            steps_by_id["wrr_cross_pair_grid"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_visual_review_notes_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_cross_pair_grid_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_direct_all_lanes_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_policy_scenarios_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_dw_formula_sensitivity_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        for source_audit_doc in [
            "docs/TORAH_CODE_RESEARCH_MODEL_SIMULATION.md",
            "docs/TORAH_CODE_RESEARCH_ELS_MODEL_SIMULATION.md",
            "docs/GANS_COMMUNITIES_SOURCE_AUDIT.md",
            "docs/AMERICAN_PRESIDENTS_SOURCE_AUDIT.md",
            "docs/WITZTUM_BIRTH_DATES_SOURCE_AUDIT.md",
            "docs/ISRAELI_PRIME_MINISTERS_SOURCE_AUDIT.md",
            "docs/COLINEAR_ELS_SOURCE_AUDIT.md",
            "docs/CITIES_SOURCE_CHAIN_AUDIT.md",
            "docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md",
            "docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md",
            "docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md",
            "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md",
            "docs/WRR_SOURCE_RECOVERY_PROBE.md",
        ]:
            self.assertIn(source_audit_doc, steps_by_id["preflight"]["inputs"])
            self.assertIn(source_audit_doc, preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "protocols/wrr_source_recovery_probe.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_recovery_probe.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_recovery_probe_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_hypothesis_testing_source_audit_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_variant_gap_docs.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/analyze_wrr_source_policy_scenarios.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/analyze_wrr_dw_formula_sensitivity.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("claims/claim_catalog.csv", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/CLAIM_CATALOG.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("configs/prospective_study_lanes.json", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_prospective_study_lanes.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_source_basis_audit_queue.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_expanded_strata_tooling.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/validate_study_mapping_schemas.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_crd_relevance_dictionary.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/classify_centered_relevance.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_manual_review_queue.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_wrr_claim_readiness_doc.py", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "scripts/check_wrr_claim_blocker_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_defined_diagnostic_docs.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_lock_options_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_method_status_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/EXPANDED_STRATA_TOOLING.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/STUDY_MAPPING_SCHEMAS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/CRD_PREREGISTRATION.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("terms/relevance_dictionary.toml", steps_by_id["preflight"]["inputs"])
        self.assertIn("protocols/centered_relevance_density.toml", steps_by_id["preflight"]["inputs"])
        self.assertIn("Makefile", steps_by_id["preflight"]["inputs"])
        self.assertIn("data/study/mappings/thematic_chapters.csv", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/FINAL_REPORT_OUTLINE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/FINAL_REPORT_DRAFT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/FINAL_REPORT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/PROSPECTIVE_STUDY_NEXT_LOCK.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/PROSPECTIVE_LANE_STATUS.md", steps_by_id["preflight"]["inputs"])
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
        self.assertIn(
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("kjv_apocrypha_bridge_prospective_controls", steps_by_id)
        self.assertIn("kjv_apocrypha_bridge_prospective_nonbible_controls", steps_by_id)
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
            "reports/wrr_1994/cross_pair_grid/highcap_1000/wrr2_cross_pair_permutations_999999_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_scenarios.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_term_impacts.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_dw_formula_sensitivity.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        for step_id in [
            "boundary_alignment",
            "chapter_position_bias",
            "direction_asymmetry",
            "canonical_first_summary",
            "cross_skip_summary",
            "review_flag_summary",
            "cohort_cluster_density_audit",
        ]:
            self.assertIn(step_id, steps_by_id)
            self.assertIn(
                f"protocols/{step_id}.toml",
                steps_by_id[step_id]["inputs"],
            )
        self.assertIn(
            "reports/boundary_alignment/summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/cohort_cluster_density/summary.csv",
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
            "reports/kjv_apocrypha_bridge_prospective/term_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/kjv_apocrypha_bridge_prospective_nonbible_controls/control_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/ALL_CODES_FOLLOWUP_REVIEW.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/MANUAL_REVIEW_QUEUE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/ALL_CODES_FOLLOWUP_CONTEXT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/ALL_CODES_FOLLOWUP_EXTENSIONS.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/ALL_CODES_COMPOUND_EXTENSION_CONTROLS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/WRR_REPLICATION_PLAN.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_METHOD_STATUS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_LOCK_OPTIONS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_CROSS_PAIR_GRID.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/WRR_CLAIM_READINESS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_CLAIM_BLOCKER_PACKET.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_ZERO_HIT_VARIANT_PROBE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_VARIANT_GAP_IMPACT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_VARIANT_GAP_UPPER_BOUND.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/WRR_SOURCE_REVIEW_QUEUE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/WRR_SOURCE_POLICY_SCENARIOS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/WRR_DW_FORMULA_SENSITIVITY.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/wrr_source_recovery_probe.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/build_wrr_source_recovery_probe.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_wrr_source_recovery_probe_doc.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "scripts/check_hypothesis_testing_source_audit_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_variant_gap_docs.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_variant_residual_review_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_review_queue_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_visual_review_notes_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/analyze_wrr_source_policy_scenarios.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/analyze_wrr_dw_formula_sensitivity.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_cross_pair_grid_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_direct_all_lanes_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_policy_scenarios_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_dw_formula_sensitivity_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("scripts/release_hygiene.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_public_release_hygiene.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("els/project_index.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/INDEX.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/INDEX.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("claims/claim_catalog.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/CLAIM_CATALOG.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/prospective_study_lanes.json", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_prospective_study_lanes.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_source_basis_audit_queue.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_expanded_strata_tooling.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/validate_study_mapping_schemas.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_crd_relevance_dictionary.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/classify_centered_relevance.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_manual_review_queue.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_wrr_claim_readiness_doc.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "scripts/check_wrr_claim_blocker_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_defined_diagnostic_docs.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_lock_options_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_method_status_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/EXPANDED_STRATA_TOOLING.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/STUDY_MAPPING_SCHEMAS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/CRD_PREREGISTRATION.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("terms/relevance_dictionary.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/centered_relevance_density.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("Makefile", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("data/study/mappings/thematic_chapters.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/FINAL_REPORT_OUTLINE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/FINAL_REPORT_DRAFT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/FINAL_REPORT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/PROSPECTIVE_STUDY_NEXT_LOCK.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/PROSPECTIVE_LANE_STATUS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/build_prospective_lane_status.py", preflight.DEFAULT_REQUIRED_PATHS)
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
        self.assertIn(
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/kjv_apocrypha_bridge_prospective_nonbible_controls.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "terms/kjv_apocrypha_bridge_prospective_terms.csv",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/EXTERNAL_CLAIM_SOURCE_COUNTS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/EXTERNAL_CLAIM_SOURCE_ALL_CODES_COLLECTION.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/MATRIX_CLUSTER_CONTROL_SUMMARY.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/NOTABLE_PASSAGE_GAPS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/THEMATIC_CHAPTER_ABSENCE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/MATCH_STRATA_INDEX.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/BOUNDARY_ALIGNMENT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/DIRECTION_ASYMMETRY.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/CROSS_SKIP_SUMMARY.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/COHORT_CLUSTER_DENSITY_AUDIT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "protocols/external_claim_source_counts.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("protocols/matrix_cluster_control_summary.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/notable_passage_gaps.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/thematic_chapter_absence.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/boundary_alignment.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/direction_asymmetry.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/cross_skip_summary.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/cohort_cluster_density_audit.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/PRIVATE_ENGLISH_VERSIONS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/SOURCE_BASIS_AUDIT_QUEUE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/biblegateway_english_versions.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/ebible_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/biblegateway_english_versions.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/ebible_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/example_ebible_engkjv_apocrypha.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/apocrypha_bridge_study.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/ALL_CODES_FOLLOWUP_LETTER_PATHS.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/ALL_CODES_FOLLOWUP_REVIEW.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/MANUAL_REVIEW_QUEUE.md", preflight.DEFAULT_REQUIRED_PATHS)
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
            self.assertIn("prospective_lane_failures", payload)
            self.assertIn("source_basis_failures", payload)
            self.assertIn("expanded_strata_tooling_failures", payload)
            self.assertIn("study_mapping_schema_failures", payload)
            self.assertIn("preregistration_placeholder_paths", payload)
            self.assertIn("preregistration_placeholder_failures", payload)
            self.assertIn("crd_relevance_dictionary_failures", payload)
            self.assertIn("manual_review_queue_failures", payload)
            self.assertIn("wrr_claim_readiness_doc_failures", payload)
            self.assertIn("wrr_claim_blocker_packet_doc_failures", payload)
            self.assertIn("wrr_lock_options_doc_failures", payload)
            self.assertIn("wrr_method_status_doc_failures", payload)
            self.assertIn("stale_generated_indexes", payload)

    def test_preflight_fails_on_prospective_lane_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_prospective_study_lanes,
                "validate_profiles",
                return_value=["demo_lane: unknown status: ready"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["prospective_lane_failures"],
                ["demo_lane: unknown status: ready"],
            )
            self.assertIn(
                "prospective lane validation failures: demo_lane: unknown status: ready",
                payload["failures"],
            )

    def test_preflight_fails_on_source_basis_validation_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_source_basis_audit_queue,
                "validate_source_basis_queue",
                return_value=["needs_audit rows remain: BibleGateway English versions:DEMO"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["source_basis_failures"],
                ["needs_audit rows remain: BibleGateway English versions:DEMO"],
            )
            self.assertIn(
                "source-basis validation failures: needs_audit rows remain: "
                "BibleGateway English versions:DEMO",
                payload["failures"],
            )

    def test_preflight_fails_on_expanded_strata_tooling_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_expanded_strata_tooling,
                "check_tooling",
                return_value={"ok": False, "missing": ["docs/EXPANDED_STRATA_TOOLING.md:make demo"]},
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["expanded_strata_tooling_failures"],
                ["docs/EXPANDED_STRATA_TOOLING.md:make demo"],
            )
            self.assertIn(
                "expanded-strata tooling failures: docs/EXPANDED_STRATA_TOOLING.md:make demo",
                payload["failures"],
            )

    def test_preflight_fails_on_study_mapping_schema_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.validate_study_mapping_schemas,
                "validate_mapping_dir",
                return_value=["data/study/mappings/demo.csv missing required columns: locked_at"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["study_mapping_schema_failures"],
                ["data/study/mappings/demo.csv missing required columns: locked_at"],
            )
            self.assertIn(
                "study mapping schema failures: "
                "data/study/mappings/demo.csv missing required columns: locked_at",
                payload["failures"],
            )

    def test_preflight_fails_on_preregistration_placeholder_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight,
                "find_preregistration_placeholder_failures",
                return_value=["docs/STUDY_PREREGISTRATION.md:12:5: [name]"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["preregistration_placeholder_failures"],
                ["docs/STUDY_PREREGISTRATION.md:12:5: [name]"],
            )
            self.assertIn(
                "preregistration placeholder failures: "
                "docs/STUDY_PREREGISTRATION.md:12:5: [name]",
                payload["failures"],
            )

    def test_concrete_preregistration_paths_skip_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "ALPHA_PREREGISTRATION.md").write_text("# Alpha\n", encoding="utf-8")
            (docs / "PROSPECTIVE_STUDY_PREREGISTRATION_TEMPLATE.md").write_text(
                "# Template\n",
                encoding="utf-8",
            )

            self.assertEqual(
                preflight.concrete_preregistration_paths(root),
                [Path("docs/ALPHA_PREREGISTRATION.md")],
            )

    def test_preflight_fails_on_crd_relevance_dictionary_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight,
                "check_crd_relevance_dictionary_lock",
                return_value=["dictionary sha256 mismatch"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["crd_relevance_dictionary_failures"],
                ["dictionary sha256 mismatch"],
            )
            self.assertIn(
                "CRD relevance dictionary failures: dictionary sha256 mismatch",
                payload["failures"],
            )

    def test_preflight_fails_on_manual_review_queue_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_manual_review_queue,
                "validate_manual_review_queue",
                return_value=["docs/MANUAL_REVIEW_QUEUE.md missing guard phrase"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["manual_review_queue_failures"],
                ["docs/MANUAL_REVIEW_QUEUE.md missing guard phrase"],
            )
            self.assertIn(
                "manual review queue failures: "
                "docs/MANUAL_REVIEW_QUEUE.md missing guard phrase",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_claim_readiness_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_claim_readiness_doc,
                "validate_readiness_doc",
                return_value=["docs/WRR_CLAIM_READINESS.md missing blocked status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_claim_readiness_doc_failures"],
                ["docs/WRR_CLAIM_READINESS.md missing blocked status"],
            )
            self.assertIn(
                "WRR claim-readiness doc failures: "
                "docs/WRR_CLAIM_READINESS.md missing blocked status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_claim_blocker_packet_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_claim_blocker_packet_doc,
                "validate_blocker_packet_doc",
                return_value=["docs/WRR_CLAIM_BLOCKER_PACKET.md missing no-input status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_claim_blocker_packet_doc_failures"],
                ["docs/WRR_CLAIM_BLOCKER_PACKET.md missing no-input status"],
            )
            self.assertIn(
                "WRR claim-blocker packet failures: "
                "docs/WRR_CLAIM_BLOCKER_PACKET.md missing no-input status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_defined_diagnostic_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_defined_diagnostic_docs,
                "validate_defined_diagnostic_docs",
                return_value=["docs/WRR_DEFINED_PAIR_SET_AUDIT.md missing 72 of 163"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_defined_diagnostic_doc_failures"],
                ["docs/WRR_DEFINED_PAIR_SET_AUDIT.md missing 72 of 163"],
            )
            self.assertIn(
                "WRR defined diagnostic doc failures: "
                "docs/WRR_DEFINED_PAIR_SET_AUDIT.md missing 72 of 163",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_variant_gap_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_variant_gap_docs,
                "validate_variant_gap_docs",
                return_value=["docs/WRR_VARIANT_GAP_IMPACT.md missing diagnostic status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_variant_gap_doc_failures"],
                ["docs/WRR_VARIANT_GAP_IMPACT.md missing diagnostic status"],
            )
            self.assertIn(
                "WRR variant-gap doc failures: "
                "docs/WRR_VARIANT_GAP_IMPACT.md missing diagnostic status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_lock_options_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_lock_options_doc,
                "validate_lock_options_doc",
                return_value=["docs/WRR_LOCK_OPTIONS.md missing decision aid status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_lock_options_doc_failures"],
                ["docs/WRR_LOCK_OPTIONS.md missing decision aid status"],
            )
            self.assertIn(
                "WRR lock-options doc failures: "
                "docs/WRR_LOCK_OPTIONS.md missing decision aid status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_review_queue_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_review_queue_doc,
                "validate_source_review_queue_doc",
                return_value=["docs/WRR_SOURCE_REVIEW_QUEUE.md missing diagnostic status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_review_queue_doc_failures"],
                ["docs/WRR_SOURCE_REVIEW_QUEUE.md missing diagnostic status"],
            )
            self.assertIn(
                "WRR source-review queue doc failures: "
                "docs/WRR_SOURCE_REVIEW_QUEUE.md missing diagnostic status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_dw_formula_sensitivity_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_dw_formula_sensitivity_doc,
                "validate_dw_formula_sensitivity_doc",
                return_value=["docs/WRR_DW_FORMULA_SENSITIVITY.md missing unlocked status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_dw_formula_sensitivity_doc_failures"],
                ["docs/WRR_DW_FORMULA_SENSITIVITY.md missing unlocked status"],
            )
            self.assertIn(
                "WRR D(w) formula sensitivity doc failures: "
                "docs/WRR_DW_FORMULA_SENSITIVITY.md missing unlocked status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_policy_scenarios_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_policy_scenarios_doc,
                "validate_source_policy_scenarios_doc",
                return_value=["docs/WRR_SOURCE_POLICY_SCENARIOS.md missing diagnostic status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_policy_scenarios_doc_failures"],
                ["docs/WRR_SOURCE_POLICY_SCENARIOS.md missing diagnostic status"],
            )
            self.assertIn(
                "WRR source-policy scenarios doc failures: "
                "docs/WRR_SOURCE_POLICY_SCENARIOS.md missing diagnostic status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_cross_pair_grid_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_cross_pair_grid_doc,
                "validate_cross_pair_grid_doc",
                return_value=["docs/WRR_CROSS_PAIR_GRID.md missing diagnostic status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_cross_pair_grid_doc_failures"],
                ["docs/WRR_CROSS_PAIR_GRID.md missing diagnostic status"],
            )
            self.assertIn(
                "WRR cross-pair grid doc failures: "
                "docs/WRR_CROSS_PAIR_GRID.md missing diagnostic status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_direct_all_lanes_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_direct_all_lanes_doc,
                "validate_direct_all_lanes_doc",
                return_value=[
                    "docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md missing diagnostic status"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_direct_all_lanes_doc_failures"],
                ["docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md missing diagnostic status"],
            )
            self.assertIn(
                "WRR direct all-lane doc failures: "
                "docs/WRR_DIRECT_ALL_LANES_DIAGNOSTIC.md missing diagnostic status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_visual_review_notes_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_visual_review_notes_doc,
                "validate_source_visual_review_notes_doc",
                return_value=[
                    "docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md missing triage status"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_visual_review_notes_doc_failures"],
                ["docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md missing triage status"],
            )
            self.assertIn(
                "WRR source visual-review notes doc failures: "
                "docs/WRR_SOURCE_VISUAL_REVIEW_NOTES.md missing triage status",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_method_status_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_method_status_doc,
                "validate_method_status_doc",
                return_value=["docs/WRR_METHOD_STATUS.md missing blocked status"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_method_status_doc_failures"],
                ["docs/WRR_METHOD_STATUS.md missing blocked status"],
            )
            self.assertIn(
                "WRR method-status doc failures: "
                "docs/WRR_METHOD_STATUS.md missing blocked status",
                payload["failures"],
            )

    def test_preflight_fails_on_hypothesis_testing_source_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_hypothesis_testing_source_audit_doc,
                "validate_hypothesis_testing_source_audit_doc",
                return_value=[
                    "docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md missing usable method pages"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["hypothesis_testing_source_audit_doc_failures"],
                [
                    "docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md missing usable method pages"
                ],
            )
            self.assertIn(
                "hypothesis-testing source audit doc failures: "
                "docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md missing usable method pages",
                payload["failures"],
            )

    def test_preflight_detects_stale_generated_indexes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            protocols = root / "protocols"
            docs.mkdir()
            protocols.mkdir()
            (docs / "INDEX.md").write_text("# stale\n", encoding="utf-8")
            (docs / "ALPHA_REPORT.md").write_text("# Alpha Report\n", encoding="utf-8")
            (protocols / "INDEX.md").write_text("# stale\n", encoding="utf-8")
            (protocols / "sample.toml").write_text(
                'name = "sample"\ndescription = "Demo."\n',
                encoding="utf-8",
            )

            self.assertEqual(
                preflight.stale_generated_indexes(root),
                ["docs/INDEX.md", "protocols/INDEX.md"],
            )

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
        source_hashes = {label: f"{label}hash" for label in REQUIRED_MANIFEST_LABELS}
        source_hashes.update(
            {
                "wrr_1994_paper": "paperhash",
                "wrr1": "wrr1hash",
                "wrr2": "abc",
                "se2a": "se2ahash",
                "se2b": "se2bhash",
                "se3": "se3hash",
                "mc_key": "def",
                "wrr_nations_mc": "nationsmc",
                "wrr_nations_gir": "nationsgir",
                "wnp_mc": "wnpmc",
                "wnp_en": "wnpen",
            }
        )
        lines = summary.wrr_audit_section(
            {"status": "success", "duration_seconds": 12.3},
            {
                "downloads": [
                    {"label": label, "sha256": digest}
                    for label, digest in source_hashes.items()
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
                    "rows_with_checked_under_10_valid": "0",
                    "ordinary_in_bounds_failures": "0",
                }
            ],
            [
                {
                    "permutations": "999999",
                    "observed_rows": "182",
                    "observed_defined_corrected_distances": "72",
                    "rho_p1": "0.019722",
                    "rho_p2": "0.000101",
                    "rho_p3": "0.0506065",
                    "rho_p4": "0.000535",
                    "rho0_bonferroni": "0.000404",
                }
            ],
            [
                {
                    "scenario": "exclude_wnp_zacut_only",
                    "excluded_pairs": "8",
                    "remaining_appellation_min_length_pairs": "157",
                    "gap_to_source_cited_163_after_appellation_min_length": "6",
                    "remaining_length_filtered_pairs": "78",
                }
            ],
            [
                {
                    "term_id": "wrr2_27_app_02",
                    "term": "ZKWTA",
                    "flags": "wnp_disputed_zacut_appellation",
                    "affected_appellation_min_length_pairs": "2",
                    "remaining_appellation_min_length_pairs_if_excluded": "163",
                    "gap_to_source_cited_163_after_appellation_min_length_if_excluded": "0",
                    "closes_appellation_min_length_gap_to_163": "true",
                    "diagnostic_read": "single-term exclusion closes >=5 count gap",
                }
            ],
            [
                {
                    "scope": "all_lanes_cap1000",
                    "row_count": "182",
                    "printed_defined_corrected_distances": "72",
                    "program_defined_corrected_distances": "72",
                    "changed_pairs": "0",
                }
            ],
        )
        text = "\n".join(lines)

        self.assertIn("## WRR 1994 Source Audit", text)
        self.assertIn("locked repo-defined local evidence", text)
        self.assertIn("Exact published WRR", text)
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
        self.assertIn("| Repo-defined date-label permutations | 999,999 |", text)
        self.assertIn("| Repo-defined Bonferroni rho0 | 0.000404 |", text)
        self.assertIn("| exclude_wnp_zacut_only | 8 | 157 | 6 | 78 |", text)
        self.assertIn("Single-term source-policy impacts", text)
        self.assertIn(
            "| wrr2_27_app_02 | ZKWTA | wnp_disputed_zacut_appellation | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |",
            text,
        )
        self.assertIn("| all_lanes_cap1000 | 182 | 72 | 72 | 0 |", text)
        self.assertIn("and visual triage notes.", text)

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

    def test_matrix_cluster_control_section_lists_opportunity_ratio(self) -> None:
        lines = summary.matrix_cluster_control_section(
            [
                {
                    "cell_relation": "orthogonal",
                    "bible_pairs": "20",
                    "secular_control_pairs": "4",
                    "bible_to_control_rate_ratio": "5.000000",
                    "bible_to_control_opportunity_ratio": "4.500000",
                    "exceeds_secular_max": "yes",
                }
            ],
            [
                {
                    "cell_relation": "orthogonal",
                    "term_a_id": "gog_h",
                    "term_b_id": "magog_h",
                    "term_a_concept": "Gog",
                    "term_b_concept": "Magog",
                    "term_a_normalized": "גוג",
                    "term_b_normalized": "מגוג",
                    "bible_pairs": "10",
                    "secular_control_pairs": "1",
                    "bible_to_control_rate_ratio": "10.000000",
                    "bible_to_control_opportunity_ratio": "9.000000",
                }
            ],
        )
        text = "\n".join(lines)

        self.assertIn("## Matrix Cluster Control Summary", text)
        self.assertIn("4.500000", text)
        self.assertIn("`גוג` (Gog; English: Gog)", text)
        self.assertIn("not a", text)

    def test_expanded_strata_summary_section_lists_post_search_counts(self) -> None:
        lines = summary.expanded_strata_summary_section(
            [{"stratum": "cross_skip_pair_at_word", "rows": "12"}],
            [{"bucket": "boundary_start_verse", "rows": "2"}],
            [{"bucket": "center_verse_first_in_chapter", "rows": "3"}],
            [{"bucket": "forward_only", "term_groups": "4"}],
            [{"bucket": "canonical_first_centered_occurrence", "rows": "5"}],
            [{"bucket": "cross_skip_pair_at_letter", "rows": "6"}],
            [{"flag_type": "skip_equals_meaningful_constant", "flag_rows": "7"}],
            [{"bucket": "all", "windows": "0", "max_distinct_term_count": "0"}],
        )
        text = "\n".join(lines)

        self.assertIn("## Expanded Post-Search Strata", text)
        self.assertIn("`cross_skip_pair_at_word`", text)
        self.assertIn("boundary_start_verse", text)
        self.assertIn("forward_only", text)
        self.assertIn("no cohort windows", text)

    def test_gap_sections_list_cross_source_rows(self) -> None:
        notable_lines = summary.notable_passage_gap_section(
            [
                {
                    "passage_id": "lev24_blasphemy_law",
                    "terms_present_in_passage": "45",
                    "terms_absent_in_passage_common_elsewhere": "7",
                    "terms_low_vs_uniform": "1",
                }
            ],
            [
                {
                    "passage_id": "lev24_blasphemy_law",
                    "passage_concept": "Leviticus 24 Blasphemy Law",
                    "normalized_term": "גוג",
                    "concept": "Gog",
                    "strongest_gap_class": "absent_in_passage_common_elsewhere",
                    "gap_corpus_count": "5",
                    "present_corpus_count": "0",
                }
            ],
        )
        thematic_lines = summary.thematic_chapter_absence_section(
            [],
            [
                {
                    "passage_concept": "Wound Thematic Chapter",
                    "normalized_term": "חבורה",
                    "concept": "Wound",
                    "strongest_gap_class": "absent_in_passage_common_elsewhere",
                    "gap_corpus_count": "5",
                    "present_corpus_count": "0",
                },
                {
                    "passage_concept": "Gog Thematic Chapter",
                    "normalized_term": "גוג",
                    "concept": "Gog",
                    "strongest_gap_class": "present_in_passage",
                    "gap_corpus_count": "0",
                    "present_corpus_count": "5",
                },
            ],
        )
        notable_text = "\n".join(notable_lines)
        thematic_text = "\n".join(thematic_lines)

        self.assertIn("## Notable Passage Gap Ledger", notable_text)
        self.assertIn("45", notable_text)
        self.assertIn("`גוג` (Gog; English: Gog)", notable_text)
        self.assertIn("## Thematic Chapter Absence Ledger", thematic_text)
        self.assertIn("`חבורה` (chabburah; English: Wound)", thematic_text)
        self.assertIn("`גוג` (Gog; English: Gog)", thematic_text)


if __name__ == "__main__":
    unittest.main()
