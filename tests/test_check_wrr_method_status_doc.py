import csv
from pathlib import Path

from scripts import check_wrr_method_status_doc as check


def test_current_wrr_method_status_doc_passes() -> None:
    assert check.validate_method_status_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_method_status_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_exact_published_reproduction_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_method_status_doc(doc)

    assert any("not an exact published WRR reproduction" in failure for failure in failures)


def test_validate_method_status_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_method_status_doc(doc, status=_status_csv(tmp_path))

    assert failures == []


def test_validate_method_status_rejects_status_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_METHOD_STATUS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_method_status_doc(
        doc,
        status=_status_csv(tmp_path, bad_area="Pair universe"),
    )

    assert any("Pair universe status drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR method-status doc failure" in capsys.readouterr().err


def _status_csv(tmp_path: Path, *, bad_area: str | None = None) -> Path:
    path = tmp_path / "status.csv"
    fieldnames = ["decision_area", "status", "current_read", "evidence", "next_action"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for area, status in check.EXPECTED_STATUS.items():
            writer.writerow(
                {
                    "decision_area": area,
                    "status": "drifted" if area == bad_area else status,
                    "current_read": "read",
                    "evidence": "evidence",
                    "next_action": "next",
                }
            )
    return path
