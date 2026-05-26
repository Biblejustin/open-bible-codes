import csv
from pathlib import Path

from scripts import check_wrr_lock_options_doc as check


def test_current_wrr_lock_options_doc_passes() -> None:
    assert check.validate_lock_options_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_lock_options_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_decision_aid_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_lock_options_doc(doc)

    assert any("decision aid" in failure for failure in failures)


def test_missing_no_input_posture_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    text = "\n".join(
        phrase
        for phrase in check.REQUIRED_PHRASES
        if phrase != "No source-review flag or visual-review note excludes a pair automatically."
    )
    doc.write_text(text + "\n", encoding="utf-8")

    failures = check.validate_lock_options_doc(doc)

    assert any("visual-review note excludes" in failure for failure in failures)


def test_validate_lock_options_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_lock_options_doc(doc, options=_options_csv(tmp_path))

    assert failures == []


def test_validate_lock_options_rejects_status_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCK_OPTIONS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_lock_options_doc(
        doc,
        options=_options_csv(tmp_path, bad_option="printed WRR formula"),
    )

    assert any("printed WRR formula status drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR lock-options doc failure" in capsys.readouterr().err


def _options_csv(tmp_path: Path, *, bad_option: str | None = None) -> Path:
    path = tmp_path / "options.csv"
    fieldnames = [
        "area",
        "option",
        "status",
        "evidence",
        "recommendation",
        "claim_boundary",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for option, (area, status, claim_boundary) in check.EXPECTED_OPTIONS.items():
            writer.writerow(
                {
                    "area": area,
                    "option": option,
                    "status": "drifted" if option == bad_option else status,
                    "evidence": "evidence",
                    "recommendation": "recommendation",
                    "claim_boundary": claim_boundary,
                }
            )
    return path
