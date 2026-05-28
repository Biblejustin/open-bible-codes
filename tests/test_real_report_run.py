import ast
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

    def test_real_report_summary_uses_completed_kjva_status(self) -> None:
        source = Path("scripts/build_real_report_run_summary.py").read_text(
            encoding="utf-8"
        )

        self.assertIn("completed KJVA prospective", source)
        self.assertNotIn("fresh KJVA prospective", source)

    def test_real_report_tracks_clean_lock_closeout_docs(self) -> None:
        protocol = load_protocol("protocols/real_report_run.toml")
        steps_by_id = {step["id"]: step for step in protocol["steps"]}
        real_report = Path("docs/REAL_REPORT_RUN.md").read_text(encoding="utf-8")
        summary_source = Path("scripts/build_real_report_run_summary.py").read_text(
            encoding="utf-8"
        )
        paths = [
            "docs/CLEAN_LOCK_RESULTS_SUMMARY.md",
            "docs/STRICT_FOLLOWUP_GATE_SUMMARY.md",
            "docs/GREEK_LEXICON_EXTENSION_PROSPECTIVE_REPORT.md",
        ]

        self.assertIn("clean-lock close-out", real_report)
        for path in paths:
            self.assertIn(path, steps_by_id["preflight"]["inputs"])
            self.assertIn(path, steps_by_id["real_report_summary"]["inputs"])
            self.assertIn(path, preflight.DEFAULT_REQUIRED_PATHS)
            self.assertIn(path, summary_source)

    def test_preflight_required_paths_include_imported_check_scripts(self) -> None:
        source_path = Path("scripts/preflight_real_report_run.py")
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imported_check_scripts = {
            f"scripts/{alias.name}.py"
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "scripts"
            for alias in node.names
            if alias.name.startswith("check_")
        }

        self.assertGreater(len(imported_check_scripts), 0)
        self.assertEqual(
            sorted(imported_check_scripts - set(preflight.DEFAULT_REQUIRED_PATHS)),
            [],
        )

    def test_final_report_doc_refs_are_preflight_required(self) -> None:
        failures = preflight.find_unrequired_doc_references(
            Path("."),
            set(preflight.DEFAULT_REQUIRED_PATHS),
        )

        self.assertEqual(failures, [])

    def test_final_report_doc_ref_guard_reports_unrequired_existing_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "FINAL_REPORT.md").write_text(
                "`docs/UNTRACKED_SUPPORT_DOC.md`\n",
                encoding="utf-8",
            )
            (root / "docs" / "UNTRACKED_SUPPORT_DOC.md").write_text(
                "support\n",
                encoding="utf-8",
            )

            failures = preflight.find_unrequired_doc_references(
                root,
                {"docs/FINAL_REPORT.md"},
            )

        self.assertEqual(
            failures,
            [
                "docs/FINAL_REPORT.md references docs/UNTRACKED_SUPPORT_DOC.md "
                "but it is not in required paths"
            ],
        )

    def test_real_report_preflight_and_summary_are_not_resume_cached(self) -> None:
        protocol = load_protocol("protocols/real_report_run.toml")
        steps_by_id = {step["id"]: step for step in protocol["steps"]}

        self.assertTrue(steps_by_id["preflight"]["always_run"])
        self.assertTrue(steps_by_id["real_report_summary"]["always_run"])
        self.assertIn("wrr_audit_counts", steps_by_id)
        self.assertIn("wrr_method_lane_wide_skip_probe", steps_by_id)
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
        self.assertIn("scripts/check_public_claim_language.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_doc_command_references.py", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "scripts/check_project_findings_overview_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("els/project_index.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("README.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/START_HERE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/REAL_REPORT_RUN.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/REMAINING_WORK_REGISTER.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("protocols/README.md", steps_by_id["preflight"]["inputs"])
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
        self.assertIn("docs/WRR_LOCKED_METHOD_REPORT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_EXACT_GAP_PRIORITY_PACKET.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("docs/WRR_ZERO_HIT_VARIANT_PROBE.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_VARIANT_GAP_IMPACT.md", steps_by_id["preflight"]["inputs"])
        self.assertIn("docs/WRR_VARIANT_GAP_UPPER_BOUND.md", steps_by_id["preflight"]["inputs"])
        self.assertIn(
            "docs/WRR_VARIANT_RESIDUAL_REVIEW_PACKET.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_MANUAL_DECISION_REGISTER.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md",
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
            "scripts/build_wrr_residual_term_reconciliation_queue.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_residual_reconciliation_action_plan.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_policy_evidence_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_policy_review_checklist.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_transcription_evidence_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_transcription_row_review_checklist.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_row_coverage_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_row_crop_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_row_ocr_word_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_source_row_review_bundle.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_remaining_lane_evidence_packets.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_remaining_lane_review_checklist.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_manual_decision_register.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_manual_decision_record_worksheet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_method_pair_universe_evidence_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/analyze_wrr_method_lane_wide_skip.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_claim_blocker_packet.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_locked_method_report.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_exact_reproduction_gap_dashboard.py",
            steps_by_id["wrr_audit_counts"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_exact_gap_priority_packet.py",
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
            "reports/wrr_1994/wrr_residual_term_reconciliation_queue.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_residual_term_reconciliation_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_residual_reconciliation_action_plan.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_residual_reconciliation_action_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_locked_method_report.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_LOCKED_METHOD_REPORT.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_EXACT_GAP_PRIORITY_PACKET.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_evidence_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_review_checklist.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_row_coverage_packet_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_CROP_PACKET.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_row_review_bundle_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_remaining_lane_review_checklist.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_manual_decision_register_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_manual_decision_record_worksheet.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md",
            steps_by_id["wrr_audit_counts"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv",
            steps_by_id["wrr_method_lane_wide_skip_probe"]["outputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_policy_evidence_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_transcription_evidence_row_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_source_row_review_bundle_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_remaining_lane_evidence_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_manual_decision_register_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_method_pair_universe_evidence_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_locked_method_report.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_exact_reproduction_gap_dashboard.csv",
            steps_by_id["real_report_summary"]["inputs"],
        )
        self.assertIn(
            "reports/wrr_1994/wrr_exact_gap_priority_packet_summary.csv",
            steps_by_id["real_report_summary"]["inputs"],
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
            "reports/wrr_1994/wrr_method_lane_wide_skip_probe_summary.csv",
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
            "scripts/check_wrr_source_policy_evidence_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_policy_review_checklist_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_transcription_evidence_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_transcription_row_review_checklist_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_row_coverage_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_row_crop_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_row_crop_contact_sheet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_row_ocr_word_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_row_review_bundle_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_remaining_lane_evidence_packets_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_remaining_lane_review_checklist_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_manual_decision_register_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_manual_decision_record_worksheet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_manual_decision_record_worksheet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_manual_decision_records.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_method_pair_universe_evidence_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_public_handoff_docs.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_public_handoff_docs.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_claim_catalog_boundary.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_source_audit_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_support_docs_local_lock.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_dw_formula_sensitivity_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_locked_method_report_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_exact_reproduction_gap_dashboard.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_exact_reproduction_gap_dashboard_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_exact_gap_priority_packet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_exact_gap_priority_packet_doc.py",
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
            "docs/CITIES_PDF_RECOVERY_PROBE.md",
            "docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md",
            "docs/CITIES_SOURCE_REVIEW_QUEUE.md",
            "docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md",
            "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
            "docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md",
            "docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md",
            "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
            "docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md",
            "docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md",
            "docs/EVENT_OBJECT_EXPERIMENT_SOURCE_AUDIT.md",
            "docs/UNDER_CONSTRUCTION_EXPERIMENT_SOURCE_AUDIT.md",
            "docs/HYPOTHESIS_TESTING_SOURCE_AUDIT.md",
            "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md",
            "docs/WRR_SOURCE_RECOVERY_PROBE.md",
            "docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md",
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
            "protocols/wrr_wayback_source_recovery_probe.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_wrr_wayback_source_recovery_probe.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_wayback_source_recovery_probe_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_pdf_recovery_probe.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_pdf_recovery_probe.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_pdf_recovery_probe_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_recovered_pdf_text_audit.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/analyze_cities_recovered_pdf_text.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_recovered_pdf_text_audit_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_review_queue.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_review_queue.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_review_queue_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_review.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_review.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_review_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_feasibility.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_feasibility.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_feasibility_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_review_packet.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_review_packet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_review_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_review_checklist.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_page_review.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_row_lock_queue.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_row_lock_worksheet.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_row_lock_evidence_packet.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_transcription_review_worksheet.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_page_review_bundle.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_source_page_contact_sheet.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "data/study/mappings/cities_source_row_lock_decisions.csv",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "data/study/mappings/cities_source_transcription_decisions.csv",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "data/study/mappings/cities_ocr_page_review_decisions.csv",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_review_checklist.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_review_checklist_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_page_review.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_page_review_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_row_lock_queue.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_queue_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_decision_records.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_row_lock_evidence_packet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_evidence_packet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_row_lock_worksheet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_worksheet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_transcription_review_worksheet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_transcription_review_worksheet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_page_review_bundle.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_page_review_bundle_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_source_page_contact_sheet.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_source_page_contact_sheet_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "protocols/cities_extractable_text_review.toml",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/build_cities_extractable_text_review.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_cities_extractable_text_review_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_hypothesis_testing_source_audit_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_israeli_prime_ministers_detail_recovery_probe_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_research_missing_model_pages_audit_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_adjacent_source_audit_docs.py",
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
        self.assertIn(
            "docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_greek_surface_second_cohort_readiness_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_consolidated_findings_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_prospective_lane_status_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_final_report_assembly_docs.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_final_report_highlights_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_study_lock_manifests_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_prospective_study_next_lock_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_prospective_study_readiness_doc.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn("scripts/check_prospective_study_lanes.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_english_corpus_policy_docs.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_source_basis_audit_queue.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_expanded_strata_tooling.py", steps_by_id["preflight"]["inputs"])
        self.assertIn("scripts/check_public_claim_language.py", steps_by_id["preflight"]["inputs"])
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
            "scripts/build_wrr_locked_method_report.py",
            steps_by_id["preflight"]["inputs"],
        )
        self.assertIn(
            "scripts/check_wrr_locked_method_report_doc.py",
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
        self.assertIn(
            "data/study/mappings/wrr_manual_decision_records.csv",
            steps_by_id["preflight"]["inputs"],
        )
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
        self.assertIn("docs/WRR_LOCKED_METHOD_REPORT.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_EXACT_GAP_PRIORITY_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_CROP_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
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
        self.assertIn("docs/WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "protocols/wrr_wayback_source_recovery_probe.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_wayback_source_recovery_probe.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_wayback_source_recovery_probe_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("docs/CITIES_PDF_RECOVERY_PROBE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_SOURCE_REVIEW_QUEUE.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_UNREADABLE_PDF_REVIEW.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_pdf_recovery_probe.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_recovered_pdf_text_audit.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_review_queue.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_review.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_feasibility.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_review_packet.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_review_checklist.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_unreadable_pdf_ocr_page_review.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_row_lock_queue.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_row_lock_worksheet.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_row_lock_evidence_packet.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_transcription_review_worksheet.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_page_review_bundle.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_source_page_contact_sheet.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "data/study/mappings/cities_source_row_lock_decisions.csv",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "data/study/mappings/cities_source_transcription_decisions.csv",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "data/study/mappings/cities_ocr_page_review_decisions.csv",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/cities_extractable_text_review.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_pdf_recovery_probe.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_pdf_recovery_probe_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/analyze_cities_recovered_pdf_text.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_recovered_pdf_text_audit_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_review_queue.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_review_queue_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_review.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_review_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_feasibility.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_feasibility_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_review_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_review_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_review_checklist.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_review_checklist_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_unreadable_pdf_ocr_page_review.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_unreadable_pdf_ocr_page_review_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_row_lock_queue.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_queue_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_decision_records.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_row_lock_evidence_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_evidence_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_row_lock_worksheet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_row_lock_worksheet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_transcription_review_worksheet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_transcription_review_worksheet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_page_review_bundle.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_page_review_bundle_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_source_page_contact_sheet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_source_page_contact_sheet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_cities_extractable_text_review.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_cities_extractable_text_review_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_hypothesis_testing_source_audit_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_israeli_prime_ministers_detail_recovery_probe_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md",
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
            "docs/WRR_RESIDUAL_TERM_RECONCILIATION_QUEUE.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_residual_term_reconciliation_queue.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_residual_reconciliation_action_plan.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_residual_term_reconciliation_queue_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_residual_reconciliation_action_plan_doc.py",
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
            "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_source_policy_review_checklist.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_policy_review_checklist_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_remaining_lane_evidence_packets.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_remaining_lane_evidence_packets_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_remaining_lane_review_checklist.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_remaining_lane_review_checklist_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_MANUAL_DECISION_REGISTER.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_manual_decision_register.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_manual_decision_register_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_method_pair_universe_evidence_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_source_transcription_row_review_checklist.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_transcription_row_review_checklist_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_source_row_coverage_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_row_coverage_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_source_row_crop_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_row_crop_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_row_crop_contact_sheet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_source_row_ocr_word_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_row_ocr_word_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_source_row_review_bundle.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_row_review_bundle_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_method_pair_universe_evidence_packet_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/analyze_wrr_method_lane_wide_skip.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_method_lane_wide_skip_probe_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "protocols/wrr_method_lane_wide_skip_probe.toml",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_public_handoff_docs.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_source_audit_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_support_docs_local_lock.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_dw_formula_sensitivity_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn("scripts/release_hygiene.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_public_release_hygiene.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_public_claim_language.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("scripts/check_doc_command_references.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("els/project_index.py", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("README.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/START_HERE.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/REAL_REPORT_RUN.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/REMAINING_WORK_REGISTER.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/README.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/INDEX.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/INDEX.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("claims/claim_catalog.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("docs/CLAIM_CATALOG.md", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/prospective_study_lanes.json", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn(
            "docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_greek_surface_second_cohort_readiness_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_consolidated_findings_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_prospective_lane_status_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_final_report_assembly_docs.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_final_report_highlights_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_study_lock_manifests_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_prospective_study_next_lock_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_prospective_study_readiness_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
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
            "scripts/build_wrr_locked_method_report.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_locked_method_report_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_exact_reproduction_gap_dashboard.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_exact_reproduction_gap_dashboard_doc.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_exact_gap_priority_packet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_exact_gap_priority_packet_doc.py",
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
        self.assertIn(
            "scripts/check_wrr_manual_decision_records.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/build_wrr_manual_decision_record_worksheet.py",
            preflight.DEFAULT_REQUIRED_PATHS,
        )
        self.assertIn(
            "scripts/check_wrr_manual_decision_record_worksheet_doc.py",
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
        self.assertIn("configs/door43_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/oet_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/otb_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/openbible_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/odr_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("configs/supplemental_english_controls.csv", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/biblegateway_english_versions.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/ebible_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/door43_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/oet_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/otb_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/openbible_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/odr_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
        self.assertIn("protocols/supplemental_english_controls.toml", preflight.DEFAULT_REQUIRED_PATHS)
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
        self.assertIn(
            "data/study/mappings/wrr_manual_decision_records.csv",
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
        self.assertEqual(preflight.find_preflight_protocol_input_failures(Path(".")), [])

    def test_preflight_protocol_input_guard_reports_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "protocols").mkdir()
            (root / "protocols" / "real_report_run.toml").write_text(
                """
name = "real_report_run"

[[steps]]
id = "preflight"
inputs = ["docs/A.md", "docs/C.md"]
""",
                encoding="utf-8",
            )

            with patch.object(preflight, "DEFAULT_REQUIRED_PATHS", ["docs/A.md", "docs/B.md"]):
                failures = preflight.find_preflight_protocol_input_failures(root)

        self.assertEqual(
            failures,
            [
                "protocol preflight inputs missing required paths: docs/B.md",
                "protocol preflight inputs not in DEFAULT_REQUIRED_PATHS: docs/C.md",
            ],
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
            self.assertIn("english_corpus_policy_failures", payload)
            self.assertIn("expanded_strata_tooling_failures", payload)
            self.assertIn("public_claim_language_failures", payload)
            self.assertIn("doc_command_reference_failures", payload)
            self.assertIn("preflight_protocol_input_failures", payload)
            self.assertIn("real_report_doc_reference_failures", payload)
            self.assertIn("prospective_next_lock_doc_failures", payload)
            self.assertIn("prospective_readiness_doc_failures", payload)
            self.assertIn("study_lock_manifests_doc_failures", payload)
            self.assertIn("greek_second_cohort_readiness_doc_failures", payload)
            self.assertIn("consolidated_findings_doc_failures", payload)
            self.assertIn("prospective_lane_status_doc_failures", payload)
            self.assertIn("final_report_assembly_doc_failures", payload)
            self.assertIn("final_report_highlights_doc_failures", payload)
            self.assertIn("study_mapping_schema_failures", payload)
            self.assertIn("preregistration_placeholder_paths", payload)
            self.assertIn("preregistration_placeholder_failures", payload)
            self.assertIn("crd_relevance_dictionary_failures", payload)
            self.assertIn("manual_review_queue_failures", payload)
            self.assertIn("wrr_claim_readiness_doc_failures", payload)
            self.assertIn("wrr_claim_blocker_packet_doc_failures", payload)
            self.assertIn("wrr_locked_method_report_doc_failures", payload)
            self.assertIn(
                "wrr_exact_reproduction_gap_dashboard_doc_failures",
                payload,
            )
            self.assertIn("wrr_exact_gap_priority_packet_doc_failures", payload)
            self.assertIn("research_missing_model_pages_audit_doc_failures", payload)
            self.assertIn("wrr_adjacent_source_audit_doc_failures", payload)
            self.assertIn("wrr_public_handoff_doc_failures", payload)
            self.assertIn(
                "wrr_source_transcription_row_review_checklist_doc_failures",
                payload,
            )
            self.assertIn("wrr_source_row_coverage_packet_doc_failures", payload)
            self.assertIn("wrr_source_row_crop_packet_doc_failures", payload)
            self.assertIn("wrr_source_row_crop_contact_sheet_doc_failures", payload)
            self.assertIn("wrr_source_row_ocr_word_packet_doc_failures", payload)
            self.assertIn("wrr_source_row_review_bundle_doc_failures", payload)
            self.assertIn("wrr_source_policy_review_checklist_doc_failures", payload)
            self.assertIn("wrr_remaining_lane_review_checklist_doc_failures", payload)
            self.assertIn("wrr_manual_decision_register_doc_failures", payload)
            self.assertIn("wrr_manual_decision_record_worksheet_doc_failures", payload)
            self.assertIn("wrr_manual_decision_record_failures", payload)
            self.assertIn("wrr_method_lane_wide_skip_probe_doc_failures", payload)
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

    def test_preflight_fails_on_english_corpus_policy_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_english_corpus_policy_docs,
                "validate_policy_docs",
                return_value=["README.md missing deferred policy"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["english_corpus_policy_failures"],
                ["README.md missing deferred policy"],
            )
            self.assertIn(
                "English corpus policy failures: README.md missing deferred policy",
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

    def test_preflight_fails_on_public_claim_language_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_public_claim_language,
                "validate_public_claim_language",
                return_value=["docs/FINAL_REPORT.md:10: unsupported claim language `proves`"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["public_claim_language_failures"],
                ["docs/FINAL_REPORT.md:10: unsupported claim language `proves`"],
            )
            self.assertIn(
                "public claim-language failures: "
                "docs/FINAL_REPORT.md:10: unsupported claim language `proves`",
                payload["failures"],
            )

    def test_preflight_fails_on_doc_command_reference_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_doc_command_references,
                "validate_doc_command_references",
                return_value=[
                    "docs/REAL_REPORT_RUN.md:10: missing script module scripts.demo"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["doc_command_reference_failures"],
                ["docs/REAL_REPORT_RUN.md:10: missing script module scripts.demo"],
            )
            self.assertIn(
                "doc command-reference failures: "
                "docs/REAL_REPORT_RUN.md:10: missing script module scripts.demo",
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

    def test_preregistration_failures_include_stale_template_phrases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            prereg = Path(tmp) / "STUDY_PREREGISTRATION.md"
            prereg.write_text(
                "Status: template; copy before use.\n",
                encoding="utf-8",
            )

            failures = preflight.find_preregistration_placeholder_failures([prereg])

            self.assertEqual(len(failures), 2)
            self.assertTrue(
                any("stale template phrase Status: template" in failure for failure in failures)
            )
            self.assertTrue(
                any("stale template phrase copy before use" in failure for failure in failures)
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

    def test_preflight_fails_on_prospective_readiness_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_prospective_study_readiness_doc,
                "validate_readiness_doc",
                return_value=["docs/PROSPECTIVE_STUDY_READINESS.md says no ready lanes"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["prospective_readiness_doc_failures"],
                ["docs/PROSPECTIVE_STUDY_READINESS.md says no ready lanes"],
            )
            self.assertIn(
                "prospective readiness doc failures: "
                "docs/PROSPECTIVE_STUDY_READINESS.md says no ready lanes",
                payload["failures"],
            )

    def test_preflight_fails_on_prospective_next_lock_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_prospective_study_next_lock_doc,
                "validate_next_lock_doc",
                return_value=["docs/PROSPECTIVE_STUDY_NEXT_LOCK.md says no ready lanes"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["prospective_next_lock_doc_failures"],
                ["docs/PROSPECTIVE_STUDY_NEXT_LOCK.md says no ready lanes"],
            )
            self.assertIn(
                "prospective next-lock doc failures: "
                "docs/PROSPECTIVE_STUDY_NEXT_LOCK.md says no ready lanes",
                payload["failures"],
            )

    def test_preflight_fails_on_study_lock_manifests_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_study_lock_manifests_doc,
                "validate_study_lock_doc",
                return_value=["docs/STUDY_LOCK_MANIFESTS.md missing guard"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["study_lock_manifests_doc_failures"],
                ["docs/STUDY_LOCK_MANIFESTS.md missing guard"],
            )
            self.assertIn(
                "study-lock manifests doc failures: "
                "docs/STUDY_LOCK_MANIFESTS.md missing guard",
                payload["failures"],
            )

    def test_preflight_fails_on_greek_second_cohort_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_greek_surface_second_cohort_readiness_doc,
                "validate_second_cohort_doc",
                return_value=["docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md stale"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["greek_second_cohort_readiness_doc_failures"],
                ["docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md stale"],
            )
            self.assertIn(
                "Greek second-cohort readiness doc failures: "
                "docs/GREEK_SURFACE_SECOND_COHORT_READINESS.md stale",
                payload["failures"],
            )

    def test_preflight_fails_on_consolidated_findings_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_consolidated_findings_doc,
                "validate_consolidated_findings_doc",
                return_value=["docs/CONSOLIDATED_FINDINGS.md stale"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["consolidated_findings_doc_failures"],
                ["docs/CONSOLIDATED_FINDINGS.md stale"],
            )
            self.assertIn(
                "consolidated findings doc failures: "
                "docs/CONSOLIDATED_FINDINGS.md stale",
                payload["failures"],
            )

    def test_preflight_fails_on_prospective_lane_status_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_prospective_lane_status_doc,
                "validate_lane_status_doc",
                return_value=["docs/PROSPECTIVE_LANE_STATUS.md stale"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["prospective_lane_status_doc_failures"],
                ["docs/PROSPECTIVE_LANE_STATUS.md stale"],
            )
            self.assertIn(
                "prospective lane-status doc failures: "
                "docs/PROSPECTIVE_LANE_STATUS.md stale",
                payload["failures"],
            )

    def test_preflight_fails_on_final_report_assembly_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_final_report_assembly_docs,
                "validate_final_report_assembly_docs",
                return_value=["docs/FINAL_REPORT.md stale"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["final_report_assembly_doc_failures"],
                ["docs/FINAL_REPORT.md stale"],
            )
            self.assertIn(
                "final-report assembly doc failures: docs/FINAL_REPORT.md stale",
                payload["failures"],
            )

    def test_preflight_fails_on_final_report_highlights_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_final_report_highlights_doc,
                "validate_highlights_doc",
                return_value=["docs/FINAL_REPORT_HIGHLIGHTS.md stale"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["final_report_highlights_doc_failures"],
                ["docs/FINAL_REPORT_HIGHLIGHTS.md stale"],
            )
            self.assertIn(
                "final-report highlights doc failures: "
                "docs/FINAL_REPORT_HIGHLIGHTS.md stale",
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

    def test_preflight_fails_on_wrr_locked_method_report_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_locked_method_report_doc,
                "validate_locked_method_report_doc",
                return_value=["docs/WRR_LOCKED_METHOD_REPORT.md missing caveat"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_locked_method_report_doc_failures"],
                ["docs/WRR_LOCKED_METHOD_REPORT.md missing caveat"],
            )
            self.assertIn(
                "WRR locked-method report failures: "
                "docs/WRR_LOCKED_METHOD_REPORT.md missing caveat",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_exact_gap_dashboard_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_exact_reproduction_gap_dashboard_doc,
                "validate_gap_dashboard_doc",
                return_value=["docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md missing caveat"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_exact_reproduction_gap_dashboard_doc_failures"],
                ["docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md missing caveat"],
            )
            self.assertIn(
                "WRR exact-reproduction gap dashboard failures: "
                "docs/WRR_EXACT_REPRODUCTION_GAP_DASHBOARD.md missing caveat",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_exact_gap_priority_packet_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_exact_gap_priority_packet_doc,
                "validate_priority_packet_doc",
                return_value=["docs/WRR_EXACT_GAP_PRIORITY_PACKET.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_exact_gap_priority_packet_doc_failures"],
                ["docs/WRR_EXACT_GAP_PRIORITY_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR exact-gap priority packet failures: "
                "docs/WRR_EXACT_GAP_PRIORITY_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_public_handoff_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_public_handoff_docs,
                "validate_public_handoff_docs",
                return_value=["README.md missing phrase: WRR claim-blocker packet:"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_public_handoff_doc_failures"],
                ["README.md missing phrase: WRR claim-blocker packet:"],
            )
            self.assertIn(
                "WRR public handoff doc failures: "
                "README.md missing phrase: WRR claim-blocker packet:",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_public_handoff_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_public_handoff_docs,
                "validate_public_handoff_docs",
                return_value=[
                    "README.md missing phrase: Cities source-row lock handoff:"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_public_handoff_doc_failures"],
                ["README.md missing phrase: Cities source-row lock handoff:"],
            )
            self.assertIn(
                "Cities public handoff doc failures: "
                "README.md missing phrase: Cities source-row lock handoff:",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_claim_catalog_boundary_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_claim_catalog_boundary,
                "validate_cities_claim_catalog_boundary",
                return_value=[
                    "claims/claim_catalog.csv cities row promoted"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_claim_catalog_boundary_failures"],
                ["claims/claim_catalog.csv cities row promoted"],
            )
            self.assertIn(
                "Cities claim-catalog boundary failures: "
                "claims/claim_catalog.csv cities row promoted",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_audit_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_audit_doc,
                "validate_source_audit_doc",
                return_value=["docs/WRR_SOURCE_AUDIT.md missing local lock"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_audit_doc_failures"],
                ["docs/WRR_SOURCE_AUDIT.md missing local lock"],
            )
            self.assertIn(
                "WRR source-audit doc failures: "
                "docs/WRR_SOURCE_AUDIT.md missing local lock",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_support_docs_local_lock_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_support_docs_local_lock,
                "validate_support_docs",
                return_value=["docs/WRR_REPLICATION_PLAN.md missing local lock"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_support_docs_local_lock_failures"],
                ["docs/WRR_REPLICATION_PLAN.md missing local lock"],
            )
            self.assertIn(
                "WRR support-doc local-lock failures: "
                "docs/WRR_REPLICATION_PLAN.md missing local lock",
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

    def test_preflight_fails_on_wrr_residual_action_plan_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_residual_reconciliation_action_plan_doc,
                "validate_residual_reconciliation_action_plan_doc",
                return_value=["docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_residual_reconciliation_action_plan_doc_failures"],
                ["docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md missing boundary"],
            )
            self.assertIn(
                "WRR residual reconciliation action-plan failures: "
                "docs/WRR_RESIDUAL_RECONCILIATION_ACTION_PLAN.md missing boundary",
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

    def test_preflight_fails_on_wrr_source_policy_evidence_packet_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_policy_evidence_packet_doc,
                "validate_source_policy_evidence_packet_doc",
                return_value=["docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_policy_evidence_packet_doc_failures"],
                ["docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR source-policy evidence packet failures: "
                "docs/WRR_SOURCE_POLICY_EVIDENCE_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_policy_checklist_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_policy_review_checklist_doc,
                "validate_source_policy_review_checklist_doc",
                return_value=["docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_policy_review_checklist_doc_failures"],
                ["docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md missing boundary"],
            )
            self.assertIn(
                "WRR source-policy checklist failures: "
                "docs/WRR_SOURCE_POLICY_REVIEW_CHECKLIST.md missing boundary",
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

    def test_preflight_fails_on_wrr_source_transcription_evidence_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_transcription_evidence_packet_doc,
                "validate_source_transcription_evidence_packet_doc",
                return_value=[
                    "docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_transcription_evidence_packet_doc_failures"],
                ["docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR source-transcription evidence packet failures: "
                "docs/WRR_SOURCE_TRANSCRIPTION_EVIDENCE_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_transcription_row_checklist_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_transcription_row_review_checklist_doc,
                "validate_row_review_checklist_doc",
                return_value=[
                    "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_transcription_row_review_checklist_doc_failures"],
                ["docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md missing boundary"],
            )
            self.assertIn(
                "WRR source-transcription row checklist failures: "
                "docs/WRR_SOURCE_TRANSCRIPTION_ROW_REVIEW_CHECKLIST.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_row_coverage_packet_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_row_coverage_packet_doc,
                "validate_source_row_coverage_packet_doc",
                return_value=[
                    "docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_row_coverage_packet_doc_failures"],
                ["docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR source row coverage packet failures: "
                "docs/WRR_SOURCE_ROW_COVERAGE_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_row_crop_packet_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_row_crop_packet_doc,
                "validate_source_row_crop_packet_doc",
                return_value=["docs/WRR_SOURCE_ROW_CROP_PACKET.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_row_crop_packet_doc_failures"],
                ["docs/WRR_SOURCE_ROW_CROP_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR source row crop packet failures: "
                "docs/WRR_SOURCE_ROW_CROP_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_row_crop_contact_sheet_failure(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_row_crop_contact_sheet_doc,
                "validate_source_row_crop_contact_sheet_doc",
                return_value=[
                    "docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_row_crop_contact_sheet_doc_failures"],
                ["docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md missing boundary"],
            )
            self.assertIn(
                "WRR source row crop contact sheet failures: "
                "docs/WRR_SOURCE_ROW_CROP_CONTACT_SHEET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_row_ocr_word_packet_failure(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_row_ocr_word_packet_doc,
                "validate_source_row_ocr_word_packet_doc",
                return_value=[
                    "docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_row_ocr_word_packet_doc_failures"],
                ["docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR source row OCR word packet failures: "
                "docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_source_row_review_bundle_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_source_row_review_bundle_doc,
                "validate_source_row_review_bundle_doc",
                return_value=[
                    "docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_source_row_review_bundle_doc_failures"],
                ["docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md missing boundary"],
            )
            self.assertIn(
                "WRR source row review bundle failures: "
                "docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_remaining_lane_evidence_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_remaining_lane_evidence_packets_doc,
                "validate_remaining_lane_evidence_packets_doc",
                return_value=[
                    "docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_remaining_lane_evidence_packets_doc_failures"],
                ["docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md missing boundary"],
            )
            self.assertIn(
                "WRR remaining-lane evidence packet failures: "
                "docs/WRR_REMAINING_LANE_EVIDENCE_PACKETS.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_remaining_lane_checklist_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_remaining_lane_review_checklist_doc,
                "validate_remaining_lane_review_checklist_doc",
                return_value=["docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_remaining_lane_review_checklist_doc_failures"],
                ["docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md missing boundary"],
            )
            self.assertIn(
                "WRR remaining-lane checklist failures: "
                "docs/WRR_REMAINING_LANE_REVIEW_CHECKLIST.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_manual_decision_register_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_manual_decision_register_doc,
                "validate_manual_decision_register_doc",
                return_value=["docs/WRR_MANUAL_DECISION_REGISTER.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_manual_decision_register_doc_failures"],
                ["docs/WRR_MANUAL_DECISION_REGISTER.md missing boundary"],
            )
            self.assertIn(
                "WRR manual decision register failures: "
                "docs/WRR_MANUAL_DECISION_REGISTER.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_manual_decision_record_worksheet_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_manual_decision_record_worksheet_doc,
                "validate_worksheet_doc",
                return_value=["docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_manual_decision_record_worksheet_doc_failures"],
                ["docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md missing boundary"],
            )
            self.assertIn(
                "WRR manual decision record worksheet failures: "
                "docs/WRR_MANUAL_DECISION_RECORD_WORKSHEET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_manual_decision_record_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_manual_decision_records,
                "validate_decision_records",
                return_value=["data/study/mappings/wrr_manual_decision_records.csv bad row"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_manual_decision_record_failures"],
                ["data/study/mappings/wrr_manual_decision_records.csv bad row"],
            )
            self.assertIn(
                "WRR manual decision record failures: "
                "data/study/mappings/wrr_manual_decision_records.csv bad row",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_method_pair_universe_evidence_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_method_pair_universe_evidence_packet_doc,
                "validate_method_pair_universe_evidence_packet_doc",
                return_value=[
                    "docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_method_pair_universe_evidence_packet_doc_failures"],
                ["docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md missing boundary"],
            )
            self.assertIn(
                "WRR method/pair-universe evidence packet failures: "
                "docs/WRR_METHOD_PAIR_UNIVERSE_EVIDENCE_PACKET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_method_lane_wide_skip_probe_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_method_lane_wide_skip_probe_doc,
                "validate_wide_skip_probe_doc",
                return_value=["docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_method_lane_wide_skip_probe_doc_failures"],
                ["docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md missing boundary"],
            )
            self.assertIn(
                "WRR method-lane wide-skip probe failures: "
                "docs/WRR_METHOD_LANE_WIDE_SKIP_PROBE.md missing boundary",
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

    def test_preflight_fails_on_israeli_pm_detail_recovery_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_israeli_prime_ministers_detail_recovery_probe_doc,
                "validate_detail_recovery_doc",
                return_value=[
                    "docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md "
                    "missing recovery boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["israeli_prime_ministers_detail_recovery_doc_failures"],
                [
                    "docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md "
                    "missing recovery boundary"
                ],
            )
            self.assertIn(
                "Israeli PM detail recovery doc failures: "
                "docs/ISRAELI_PRIME_MINISTERS_DETAIL_RECOVERY_PROBE.md "
                "missing recovery boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_pdf_recovery_probe_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_pdf_recovery_probe_doc,
                "validate_cities_pdf_recovery_probe_doc",
                return_value=[
                    "docs/CITIES_PDF_RECOVERY_PROBE.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_pdf_recovery_probe_doc_failures"],
                [
                    "docs/CITIES_PDF_RECOVERY_PROBE.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities PDF recovery probe doc failures: "
                "docs/CITIES_PDF_RECOVERY_PROBE.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_recovered_pdf_text_audit_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_recovered_pdf_text_audit_doc,
                "validate_cities_recovered_pdf_text_audit_doc",
                return_value=[
                    "docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_recovered_pdf_text_audit_doc_failures"],
                [
                    "docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities recovered-PDF text audit doc failures: "
                "docs/CITIES_RECOVERED_PDF_TEXT_AUDIT.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_review_queue_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_review_queue_doc,
                "validate_cities_source_review_queue_doc",
                return_value=[
                    "docs/CITIES_SOURCE_REVIEW_QUEUE.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_review_queue_doc_failures"],
                [
                    "docs/CITIES_SOURCE_REVIEW_QUEUE.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities source-review queue doc failures: "
                "docs/CITIES_SOURCE_REVIEW_QUEUE.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_unreadable_pdf_review_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_unreadable_pdf_review_doc,
                "validate_cities_unreadable_pdf_review_doc",
                return_value=[
                    "docs/CITIES_UNREADABLE_PDF_REVIEW.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_unreadable_pdf_review_doc_failures"],
                [
                    "docs/CITIES_UNREADABLE_PDF_REVIEW.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities unreadable-PDF review doc failures: "
                "docs/CITIES_UNREADABLE_PDF_REVIEW.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_unreadable_pdf_ocr_feasibility_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_unreadable_pdf_ocr_feasibility_doc,
                "validate_cities_unreadable_pdf_ocr_feasibility_doc",
                return_value=[
                    "docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_unreadable_pdf_ocr_feasibility_doc_failures"],
                [
                    "docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities unreadable-PDF OCR feasibility doc failures: "
                "docs/CITIES_UNREADABLE_PDF_OCR_FEASIBILITY.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_unreadable_pdf_ocr_review_packet_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_unreadable_pdf_ocr_review_packet_doc,
                "validate_cities_unreadable_pdf_ocr_review_packet_doc",
                return_value=[
                    "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_unreadable_pdf_ocr_review_packet_doc_failures"],
                [
                    "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities unreadable-PDF OCR review packet doc failures: "
                "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_PACKET.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_unreadable_pdf_ocr_review_checklist_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_unreadable_pdf_ocr_review_checklist_doc,
                "validate_cities_unreadable_pdf_ocr_review_checklist_doc",
                return_value=[
                    "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_unreadable_pdf_ocr_review_checklist_doc_failures"],
                [
                    "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities unreadable-PDF OCR review checklist doc failures: "
                "docs/CITIES_UNREADABLE_PDF_OCR_REVIEW_CHECKLIST.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_unreadable_pdf_ocr_page_review_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_unreadable_pdf_ocr_page_review_doc,
                "validate_cities_unreadable_pdf_ocr_page_review_doc",
                return_value=[
                    "docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_unreadable_pdf_ocr_page_review_doc_failures"],
                [
                    "docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities unreadable-PDF OCR page-review doc failures: "
                "docs/CITIES_UNREADABLE_PDF_OCR_PAGE_REVIEW.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_row_lock_queue_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_row_lock_queue_doc,
                "validate_cities_source_row_lock_queue_doc",
                return_value=[
                    "docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_row_lock_queue_doc_failures"],
                [
                    "docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities source-row lock queue doc failures: "
                "docs/CITIES_SOURCE_ROW_LOCK_QUEUE.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_row_lock_evidence_packet_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_row_lock_evidence_packet_doc,
                "validate_cities_source_row_lock_evidence_packet_doc",
                return_value=[
                    "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_row_lock_evidence_packet_doc_failures"],
                [
                    "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities source-row lock evidence packet doc failures: "
                "docs/CITIES_SOURCE_ROW_LOCK_EVIDENCE_PACKET.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_row_lock_decision_record_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_row_lock_decision_records,
                "validate_decision_records",
                return_value=[
                    "data/study/mappings/cities_source_row_lock_decisions.csv bad row"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_row_lock_decision_record_failures"],
                [
                    "data/study/mappings/cities_source_row_lock_decisions.csv bad row"
                ],
            )
            self.assertIn(
                "Cities source-row lock decision record failures: "
                "data/study/mappings/cities_source_row_lock_decisions.csv bad row",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_row_lock_worksheet_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_row_lock_worksheet_doc,
                "validate_cities_source_row_lock_worksheet_doc",
                return_value=[
                    "docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_row_lock_worksheet_doc_failures"],
                [
                    "docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities source-row lock worksheet doc failures: "
                "docs/CITIES_SOURCE_ROW_LOCK_WORKSHEET.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_transcription_review_worksheet_doc_failure(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_transcription_review_worksheet_doc,
                "validate_cities_source_transcription_review_worksheet_doc",
                return_value=[
                    "docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload[
                    "cities_source_transcription_review_worksheet_doc_failures"
                ],
                [
                    "docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md missing boundary"
                ],
            )
            self.assertIn(
                "Cities source-transcription review worksheet doc failures: "
                "docs/CITIES_SOURCE_TRANSCRIPTION_REVIEW_WORKSHEET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_page_review_bundle_doc_failure(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_page_review_bundle_doc,
                "validate_cities_source_page_review_bundle_doc",
                return_value=[
                    "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_page_review_bundle_doc_failures"],
                ["docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md missing boundary"],
            )
            self.assertIn(
                "Cities source-page review bundle doc failures: "
                "docs/CITIES_SOURCE_PAGE_REVIEW_BUNDLE.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_source_page_contact_sheet_doc_failure(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_source_page_contact_sheet_doc,
                "validate_cities_source_page_contact_sheet_doc",
                return_value=[
                    "docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md missing boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_source_page_contact_sheet_doc_failures"],
                ["docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md missing boundary"],
            )
            self.assertIn(
                "Cities source-page contact sheet doc failures: "
                "docs/CITIES_SOURCE_PAGE_CONTACT_SHEET.md missing boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_cities_extractable_text_review_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_cities_extractable_text_review_doc,
                "validate_cities_extractable_text_review_doc",
                return_value=[
                    "docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["cities_extractable_text_review_doc_failures"],
                [
                    "docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md missing source boundary"
                ],
            )
            self.assertIn(
                "Cities extractable-text review doc failures: "
                "docs/CITIES_EXTRACTABLE_TEXT_REVIEW.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_critical_omission_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_critical_omission_followup_docs,
                "validate_critical_omission_docs",
                return_value=[
                    "docs/CRITICAL_OMISSION_BREAKS_NULL.md missing Cautions"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["critical_omission_doc_failures"],
                ["docs/CRITICAL_OMISSION_BREAKS_NULL.md missing Cautions"],
            )
            self.assertIn(
                "critical-omission doc failures: "
                "docs/CRITICAL_OMISSION_BREAKS_NULL.md missing Cautions",
                payload["failures"],
            )

    def test_preflight_fails_on_research_missing_model_pages_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_research_missing_model_pages_audit_doc,
                "validate_research_missing_model_pages_audit_doc",
                return_value=[
                    "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md missing source boundary"
                ],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["research_missing_model_pages_audit_doc_failures"],
                [
                    "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md missing source boundary"
                ],
            )
            self.assertIn(
                "research missing model pages audit doc failures: "
                "docs/RESEARCH_MISSING_MODEL_PAGES_AUDIT.md missing source boundary",
                payload["failures"],
            )

    def test_preflight_fails_on_wrr_adjacent_source_audit_doc_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "preflight.json"
            with patch.object(
                preflight.check_wrr_adjacent_source_audit_docs,
                "validate_adjacent_source_audit_docs",
                return_value=["docs/CITIES_SOURCE_CHAIN_AUDIT.md missing boundary"],
            ):
                code = preflight.main(["--allow-dirty", "--out", str(out)])

            self.assertEqual(code, 1)
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["wrr_adjacent_source_audit_doc_failures"],
                ["docs/CITIES_SOURCE_CHAIN_AUDIT.md missing boundary"],
            )
            self.assertIn(
                "WRR adjacent source audit doc failures: "
                "docs/CITIES_SOURCE_CHAIN_AUDIT.md missing boundary",
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
                    "priority_source_policy_terms": "1",
                    "related_source_review_rows": "2",
                    "related_scenario_pair_rows": "4",
                    "wnp_context_blocks": "3",
                    "read": "source-policy residual is now tied to local WNP context",
                }
            ],
            [
                {
                    "row_number": "06",
                    "concept": "WRR2 06",
                    "action_terms": "4",
                    "residual_pairs": "4",
                    "frontier_pairs": "4",
                    "read": "multi-term row cluster",
                }
            ],
            [
                {
                    "metric": "row_review_clusters",
                    "value": "22",
                    "read": "source-row review bundle rows",
                },
                {
                    "metric": "frontier_rows",
                    "value": "19",
                    "read": "rows with minimum-frontier pair links",
                },
                {
                    "metric": "rows_with_generated_crops",
                    "value": "22",
                    "read": "rows with generated crop paths",
                },
                {
                    "metric": "rows_with_ocr_words",
                    "value": "22",
                    "read": "rows with OCR words in the row band",
                },
                {
                    "metric": "total_ocr_words",
                    "value": "337",
                    "read": "OCR words in bundled rows",
                },
                {
                    "metric": "low_confidence_ocr_words",
                    "value": "78",
                    "read": "OCR words below the packet confidence threshold",
                },
            ],
            [
                {
                    "action_lane": "page_image_near_match_review",
                    "action_terms": "3",
                    "residual_pairs": "3",
                    "frontier_pairs": "2",
                    "read": "near OCR exists",
                },
                {
                    "action_lane": "method_or_pair_universe_review",
                    "action_terms": "11",
                    "residual_pairs": "11",
                    "frontier_pairs": "2",
                    "read": "OCR matched imported term",
                },
            ],
            [
                {
                    "action_terms": "11",
                    "residual_pairs": "11",
                    "ocr_matched_terms": "11",
                    "zero_base_skip_250_terms": "11",
                    "zero_highcap_appellation_terms": "11",
                    "both_sides_zero_highcap_pairs": "2",
                    "read": "OCR matched all method-lane terms",
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
        self.assertIn("Source-policy evidence packet status", text)
        self.assertIn("| 1 | 2 | 4 | 3 | source-policy residual", text)
        self.assertIn("Source-transcription evidence packet status", text)
        self.assertIn("- Source-transcription action terms: 4.", text)
        self.assertIn("| 06 | WRR2 06 | 4 | 4 | 4 | multi-term row cluster |", text)
        self.assertIn("Source-row review bundle status", text)
        self.assertIn("| rows_with_generated_crops | 22 | rows with generated crop paths |", text)
        self.assertIn("| low_confidence_ocr_words | 78 | OCR words below the packet confidence threshold |", text)
        self.assertIn("without selecting", text)
        self.assertIn("Remaining-lane evidence packet status", text)
        self.assertIn(
            "| page_image_near_match_review | 3 | 3 | 2 | near OCR exists |",
            text,
        )
        self.assertIn(
            "| method_or_pair_universe_review | 11 | 11 | 2 | OCR matched imported term |",
            text,
        )
        self.assertIn("Method/pair-universe evidence packet status", text)
        self.assertIn(
            "| 11 | 11 | 11 | 11 | 11 | 2 | OCR matched all method-lane terms |",
            text,
        )
        self.assertIn(
            "| wrr2_27_app_02 | ZKWTA | wnp_disputed_zacut_appellation | 2 | 163 | 0 | single-term exclusion closes >=5 count gap |",
            text,
        )
        self.assertIn("| all_lanes_cap1000 | 182 | 72 | 72 | 0 |", text)
        self.assertIn("visual triage notes, and the source-row review bundle", text)
        self.assertIn("coverage, row crops, the contact sheet, and OCR row words", text)

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
