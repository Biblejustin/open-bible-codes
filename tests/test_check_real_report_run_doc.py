from pathlib import Path
import shutil

from scripts import check_real_report_run_doc as check


def test_current_real_report_run_doc_passes() -> None:
    assert check.validate_real_report_run_doc() == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    doc = tmp_path / "missing.md"

    failures = check.validate_real_report_run_doc(doc)

    assert failures == [f"missing required files: {doc}"]


def test_missing_required_phrase_fails(tmp_path: Path) -> None:
    protocol = tmp_path / "real_report_run.toml"
    makefile = tmp_path / "Makefile"
    doc = tmp_path / "REAL_REPORT_RUN.md"
    shutil.copyfile(check.DEFAULT_PROTOCOL, protocol)
    shutil.copyfile(check.DEFAULT_MAKEFILE, makefile)
    doc.write_text("incomplete", encoding="utf-8")

    failures = check.validate_real_report_run_doc(doc, protocol, makefile)

    assert f"{doc} missing phrase: {check.REQUIRED_PHRASES[0]}" in failures


def test_matching_structural_inputs_pass(tmp_path: Path) -> None:
    doc, protocol, makefile = copy_current_inputs(tmp_path)

    assert check.validate_real_report_run_doc(doc, protocol, makefile) == []


def test_protocol_preflight_output_drift_fails(tmp_path: Path) -> None:
    doc, protocol, makefile = copy_current_inputs(tmp_path)
    protocol.write_text(
        protocol.read_text(encoding="utf-8").replace(
            '"reports/real_report_run/preflight.json"',
            '"reports/real_report_run/renamed_preflight.json"',
            1,
        ),
        encoding="utf-8",
    )

    failures = check.validate_real_report_run_doc(doc, protocol, makefile)

    assert any("preflight outputs drifted" in failure for failure in failures)


def test_protocol_summary_output_drift_fails(tmp_path: Path) -> None:
    doc, protocol, makefile = copy_current_inputs(tmp_path)
    protocol.write_text(
        protocol.read_text(encoding="utf-8").replace(
            '"reports/real_report_run/summary.md"',
            '"reports/real_report_run/renamed_summary.md"',
            1,
        ),
        encoding="utf-8",
    )

    failures = check.validate_real_report_run_doc(doc, protocol, makefile)

    assert any("real_report_summary outputs drifted" in failure for failure in failures)


def test_protocol_summary_kjva_handoff_input_drift_fails(tmp_path: Path) -> None:
    doc, protocol, makefile = copy_current_inputs(tmp_path)
    protocol_text = protocol.read_text(encoding="utf-8")
    before, separator, after = protocol_text.rpartition(
        '"reports/kjva_no_input_handoff_status/summary.csv"'
    )
    assert separator
    protocol.write_text(
        before
        + '"reports/kjva_no_input_handoff_status/renamed_summary.csv"'
        + after,
        encoding="utf-8",
    )

    failures = check.validate_real_report_run_doc(doc, protocol, makefile)

    assert any(
        "real_report_summary inputs missing: "
        "reports/kjva_no_input_handoff_status/summary.csv" in failure
        for failure in failures
    )


def test_make_target_drift_fails(tmp_path: Path) -> None:
    doc, protocol, makefile = copy_current_inputs(tmp_path)
    makefile.write_text(
        makefile.read_text(encoding="utf-8").replace(check.RUN_COMMAND, "echo stale", 1),
        encoding="utf-8",
    )

    failures = check.validate_real_report_run_doc(doc, protocol, makefile)

    assert any("real-report target drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    code = check.main(["--doc", str(tmp_path / "missing.md")])

    assert code == 1
    assert "real-report run doc failure" in capsys.readouterr().err


def copy_current_inputs(tmp_path: Path) -> tuple[Path, Path, Path]:
    doc = tmp_path / "REAL_REPORT_RUN.md"
    protocol = tmp_path / "real_report_run.toml"
    makefile = tmp_path / "Makefile"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_PROTOCOL, protocol)
    shutil.copyfile(check.DEFAULT_MAKEFILE, makefile)
    return doc, protocol, makefile
