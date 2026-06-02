import csv
import json
from pathlib import Path

from scripts import check_wrr_claim_readiness_doc as check


def test_current_wrr_claim_readiness_doc_passes() -> None:
    assert check.validate_readiness_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_readiness_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_ready_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[1:]) + "\n", encoding="utf-8")

    failures = check.validate_readiness_doc(doc)

    assert any("Status: ready" in failure for failure in failures)


def test_validate_readiness_accepts_matching_csv(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_readiness_doc(
        doc,
        readiness=_readiness_csv(tmp_path),
        manifest=None,
    )

    assert failures == []


def test_validate_readiness_rejects_status_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")

    failures = check.validate_readiness_doc(
        doc,
        readiness=_readiness_csv(tmp_path, bad_area="Pair universe"),
        manifest=None,
    )

    assert any("Pair universe status drifted" in failure for failure in failures)


def test_validate_readiness_rejects_manifest_drift(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "tool": "check_wrr_claim_readiness.py",
                "status": "blocked",
                "input": "reports/wrr_1994/wrr_method_status.csv",
                "outputs": {
                    "csv": "reports/wrr_1994/wrr_claim_readiness.csv",
                    "markdown": "docs/WRR_CLAIM_READINESS.md",
                    "manifest": "reports/wrr_1994/wrr_claim_readiness.manifest.json",
                },
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    failures = check.validate_readiness_doc(
        doc,
        readiness=_readiness_csv(tmp_path),
        manifest=manifest,
    )

    assert any("status drifted" in failure for failure in failures)


def test_validate_readiness_rejects_invalid_manifest_json(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{", encoding="utf-8")

    failures = check.validate_readiness_doc(
        doc,
        readiness=_readiness_csv(tmp_path),
        manifest=manifest,
    )

    assert any("is invalid JSON" in failure for failure in failures)


def test_validate_readiness_rejects_manifest_json_array(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_CLAIM_READINESS.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES), encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    manifest.write_text("[]", encoding="utf-8")

    failures = check.validate_readiness_doc(
        doc,
        readiness=_readiness_csv(tmp_path),
        manifest=manifest,
    )

    assert any("JSON root must be an object" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR claim-readiness doc failure" in capsys.readouterr().err


def _readiness_csv(tmp_path: Path, *, bad_area: str | None = None) -> Path:
    path = tmp_path / "readiness.csv"
    fieldnames = check.FIELDNAMES
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for area, (status, required_statuses) in check.EXPECTED_ROWS.items():
            writer.writerow(
                {
                    "decision_area": area,
                    "status": "drifted" if area == bad_area else status,
                    "required_statuses": required_statuses,
                    "ready": "true",
                    "current_read": "read",
                    "evidence": "evidence",
                    "blocker": "",
                }
            )
    return path
