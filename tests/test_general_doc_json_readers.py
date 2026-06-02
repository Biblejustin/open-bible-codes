import importlib
from collections.abc import Callable
from pathlib import Path

from scripts import check_critical_omission_followup_docs
from scripts import check_wrr_no_input_handoff_status_doc
from scripts import check_wrr_post_lock_reporting_boundary_doc


GENERAL_DOC_JSON_READER_MODULES = (
    "scripts.check_final_report_highlights_doc",
    "scripts.check_hypothesis_testing_source_audit_doc",
    "scripts.check_israeli_prime_ministers_detail_recovery_probe_doc",
    "scripts.check_research_missing_model_pages_audit_doc",
    "scripts.check_strongest_candidate_deep_dive_doc",
)


def test_general_doc_json_checks_reject_invalid_json(tmp_path: Path) -> None:
    for name, check in _checks():
        path = tmp_path / f"{name}.json"
        path.write_text("{", encoding="utf-8")

        failures = check(path)

        assert any("is invalid JSON" in failure for failure in failures), name


def test_general_doc_json_checks_reject_non_object_json(tmp_path: Path) -> None:
    for name, check in _checks():
        path = tmp_path / f"{name}.json"
        path.write_text("[]", encoding="utf-8")

        failures = check(path)

        assert any("JSON root must be an object" in failure for failure in failures), name


def _checks() -> tuple[tuple[str, Callable[[Path], list[str]]], ...]:
    module_checks = tuple(
        (module_name.rsplit(".", 1)[-1], _module_json_reader(module_name))
        for module_name in GENERAL_DOC_JSON_READER_MODULES
    )
    return module_checks + (
        ("critical_omission_followup", _critical_omission_reader),
        ("wrr_post_lock_reporting_boundary", _wrr_post_lock_manifest),
        ("wrr_no_input_handoff_status", _wrr_no_input_manifest),
    )


def _module_json_reader(module_name: str) -> Callable[[Path], list[str]]:
    module = importlib.import_module(module_name)
    reader = getattr(module, "_read_json", None)
    assert reader is not None, module_name

    def check(path: Path) -> list[str]:
        result = reader(path)
        return [result] if isinstance(result, str) else []

    return check


def _critical_omission_reader(path: Path) -> list[str]:
    failures: list[str] = []
    check_critical_omission_followup_docs.read_json_object(
        path.parent,
        Path(path.name),
        failures,
    )
    return failures


def _wrr_post_lock_manifest(path: Path) -> list[str]:
    return check_wrr_post_lock_reporting_boundary_doc.validate_manifest(path, [])


def _wrr_no_input_manifest(path: Path) -> list[str]:
    return check_wrr_no_input_handoff_status_doc.validate_manifest(
        path,
        doc=path.parent / "doc.md",
    )
