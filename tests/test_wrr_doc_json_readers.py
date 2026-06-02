import importlib
from pathlib import Path
from typing import Callable


WRR_DOC_JSON_READER_MODULES = (
    "scripts.check_wrr_claim_blocker_packet_doc",
    "scripts.check_wrr_claim_readiness_doc",
    "scripts.check_wrr_cross_pair_grid_doc",
    "scripts.check_wrr_direct_all_lanes_doc",
    "scripts.check_wrr_dw_formula_sensitivity_doc",
    "scripts.check_wrr_exact_gap_priority_packet_doc",
    "scripts.check_wrr_exact_reproduction_gap_dashboard_doc",
    "scripts.check_wrr_lock_options_doc",
    "scripts.check_wrr_locked_method_report_doc",
    "scripts.check_wrr_manual_decision_record_worksheet_doc",
    "scripts.check_wrr_manual_decision_register_doc",
    "scripts.check_wrr_method_lane_wide_skip_probe_doc",
    "scripts.check_wrr_method_pair_universe_evidence_packet_doc",
    "scripts.check_wrr_method_status_doc",
    "scripts.check_wrr_remaining_lane_evidence_packets_doc",
    "scripts.check_wrr_remaining_lane_review_checklist_doc",
    "scripts.check_wrr_residual_reconciliation_action_plan_doc",
    "scripts.check_wrr_residual_term_reconciliation_queue_doc",
    "scripts.check_wrr_source_audit_doc",
    "scripts.check_wrr_source_policy_evidence_packet_doc",
    "scripts.check_wrr_source_policy_review_checklist_doc",
    "scripts.check_wrr_source_policy_scenarios_doc",
    "scripts.check_wrr_source_recovery_probe_doc",
    "scripts.check_wrr_source_review_queue_doc",
    "scripts.check_wrr_source_row_coverage_packet_doc",
    "scripts.check_wrr_source_row_crop_contact_sheet_doc",
    "scripts.check_wrr_source_row_crop_packet_doc",
    "scripts.check_wrr_source_row_ocr_word_packet_doc",
    "scripts.check_wrr_source_row_review_bundle_doc",
    "scripts.check_wrr_source_transcription_evidence_packet_doc",
    "scripts.check_wrr_source_transcription_row_review_checklist_doc",
    "scripts.check_wrr_source_visual_review_notes_doc",
    "scripts.check_wrr_wayback_source_recovery_probe_doc",
)


def test_wrr_doc_json_readers_reject_invalid_json(tmp_path: Path) -> None:
    for module_name in WRR_DOC_JSON_READER_MODULES:
        path = tmp_path / f"{module_name.rsplit('.', 1)[-1]}.json"
        path.write_text("{", encoding="utf-8")

        failure = _reader(module_name)(path)

        assert isinstance(failure, str), module_name
        assert "is invalid JSON" in failure, module_name


def test_wrr_doc_json_readers_reject_non_object_json(tmp_path: Path) -> None:
    for module_name in WRR_DOC_JSON_READER_MODULES:
        path = tmp_path / f"{module_name.rsplit('.', 1)[-1]}.json"
        path.write_text("[]", encoding="utf-8")

        failure = _reader(module_name)(path)

        assert isinstance(failure, str), module_name
        assert "JSON root must be an object" in failure, module_name


def _reader(module_name: str) -> Callable[[Path], object]:
    module = importlib.import_module(module_name)
    reader = getattr(module, "_read_json", None) or getattr(module, "read_json", None)
    assert reader is not None, module_name
    return reader
