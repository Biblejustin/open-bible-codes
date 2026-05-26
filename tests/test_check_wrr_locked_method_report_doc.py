import csv
from pathlib import Path

from scripts import check_wrr_locked_method_report_doc as check


def test_current_wrr_locked_method_report_doc_passes() -> None:
    assert check.validate_locked_method_report_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_locked_method_report_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text(
        "\n".join(
            phrase
            for phrase in check.REQUIRED_PHRASES
            if "Status: locked local WRR method report" not in phrase
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_locked_method_report_doc(doc)

    assert any("locked local WRR method report" in failure for failure in failures)


def test_forbidden_phrase_outside_list_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    text = "\n".join(check.REQUIRED_PHRASES)
    doc.write_text(text + "\nThis proves WRR now.\n", encoding="utf-8")

    failures = check.validate_locked_method_report_doc(doc)

    assert any("forbidden phrase outside forbidden-language list" in failure for failure in failures)


def test_validate_locked_method_report_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_locked_method_report_doc(
        doc,
        report=_report_csv(tmp_path),
    )

    assert failures == []


def test_validate_locked_method_report_rejects_value_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_LOCKED_METHOD_REPORT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_locked_method_report_doc(
        doc,
        report=_report_csv(tmp_path, bad_item="defined_c_values"),
    )

    assert any("defined_c_values value drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR locked-method report failure" in capsys.readouterr().err


def _report_csv(tmp_path: Path, *, bad_item: str | None = None) -> Path:
    path = tmp_path / "report.csv"
    fieldnames = ["section", "item", "value", "status", "evidence", "source"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for item, (section, value, status) in check.EXPECTED_ROWS.items():
            writer.writerow(
                {
                    "section": section,
                    "item": item,
                    "value": "drifted" if item == bad_item else value,
                    "status": status,
                    "evidence": "evidence",
                    "source": "source.csv",
                }
            )
        for (section, item), (value, status) in check.EXPECTED_DUPLICATE_ITEMS.items():
            writer.writerow(
                {
                    "section": section,
                    "item": item,
                    "value": "drifted" if item == bad_item else value,
                    "status": status,
                    "evidence": "evidence",
                    "source": "source.csv",
                }
            )
    return path
