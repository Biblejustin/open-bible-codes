import importlib
from pathlib import Path
from typing import Callable


KJVA_DOC_JSON_CHECK_MODULES = (
    "scripts.check_kjva_crosswire_candidate_source_audit_doc",
    "scripts.check_kjva_current_source_lock_sidecar_doc",
    "scripts.check_kjva_gutenberg_book_coverage_probe_doc",
    "scripts.check_kjva_gutenberg_candidate_checksum_sidecar_doc",
    "scripts.check_kjva_gutenberg_candidate_source_audit_doc",
    "scripts.check_kjva_gutenberg_hakkaac_split_source_role_sidecar_doc",
    "scripts.check_kjva_gutenberg_source_lock_blocker_packet_doc",
    "scripts.check_kjva_gutenberg_source_lock_decision_packet_doc",
    "scripts.check_kjva_gutenberg_source_lock_prep_doc",
    "scripts.check_kjva_hakkaac_apocrypha_boundary_candidate_doc",
    "scripts.check_kjva_hakkaac_apocrypha_collation_doc",
    "scripts.check_kjva_hakkaac_apocrypha_marker_coverage_doc",
    "scripts.check_kjva_hakkaac_source_lock_decision_packet_doc",
    "scripts.check_kjva_next_result_gate_doc",
    "scripts.check_kjva_no_input_handoff_status_doc",
    "scripts.check_kjva_open_bibles_candidate_source_audit_doc",
    "scripts.check_kjva_source_policy_blocker_packet_doc",
    "scripts.check_kjva_wikisource_candidate_source_audit_doc",
)


def test_kjva_doc_manifest_checks_reject_invalid_json(tmp_path: Path) -> None:
    for module_name in KJVA_DOC_JSON_CHECK_MODULES:
        manifest = tmp_path / f"{module_name.rsplit('.', 1)[-1]}.json"
        manifest.write_text("{", encoding="utf-8")

        failures = _manifest_checker(module_name)(manifest, doc=tmp_path / "doc.md")

        assert any("is invalid JSON" in failure for failure in failures), module_name


def test_kjva_doc_manifest_checks_reject_non_object_json(tmp_path: Path) -> None:
    for module_name in KJVA_DOC_JSON_CHECK_MODULES:
        manifest = tmp_path / f"{module_name.rsplit('.', 1)[-1]}.json"
        manifest.write_text("[]", encoding="utf-8")

        failures = _manifest_checker(module_name)(manifest, doc=tmp_path / "doc.md")

        assert any(
            "JSON root must be an object" in failure for failure in failures
        ), module_name


def _manifest_checker(module_name: str) -> Callable[..., list[str]]:
    module = importlib.import_module(module_name)
    checker = getattr(module, "validate_manifest", None)
    assert checker is not None, module_name
    return checker
