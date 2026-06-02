from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.audit_study_lock_manifest_drift import AUDIT_STATUSES, FIELDNAMES, SUMMARY_FIELDNAMES
from scripts.check_study_lock_manifest_drift_audit_doc import validate_doc


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_validate_doc_accepts_synced_artifacts(tmp_path: Path) -> None:
    rows_path = tmp_path / "rows.csv"
    summary_path = tmp_path / "summary.csv"
    doc = tmp_path / "doc.md"
    manifest_path = tmp_path / "manifest.json"
    rows = [
        {
            "manifest_path": "reports/study_locks/example.manifest.json",
            "name": "example",
            "created_utc": "2026-06-01T00:00:00+00:00",
            "git_commit": "abc1234",
            "git_dirty": "False",
            "status": "locked",
            "locked_path_count": "1",
            "missing_path_count": "0",
            "audit_status": "current",
            "structural_failures": "",
            "fingerprint_failures": "",
        }
    ]
    _write_csv(rows_path, FIELDNAMES, rows)
    _write_csv(
        summary_path,
        SUMMARY_FIELDNAMES,
        [
            {"metric": "total_manifests", "value": "1"},
            {"metric": "current", "value": "1"},
            {"metric": "fingerprint_drift", "value": "0"},
            {"metric": "structural_fail", "value": "0"},
        ],
    )
    doc.write_text(
        "\n".join(
            [
                "# Study Lock Manifest Drift Audit",
                "",
                "Status: historical audit, not a prospective approval.",
                "",
                "A drifted historical manifest is not a failed result.",
                "Use `scripts.check_study_lock_manifest` for one fresh, study-specific",
                "",
                "- total_manifests: 1",
                "- current: 1",
                "- fingerprint_drift: 0",
                "- structural_fail: 0",
                "",
                "`reports/study_locks/example.manifest.json`",
            ]
        ),
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(
            {
                "tool": "audit_study_lock_manifest_drift",
                "outputs": [
                    {"path": rows_path.as_posix()},
                    {"path": summary_path.as_posix()},
                    {"path": doc.as_posix()},
                ],
            }
        ),
        encoding="utf-8",
    )

    assert validate_doc(doc, rows_path, summary_path, manifest_path) == []


def test_validate_doc_rejects_non_object_manifest(tmp_path: Path) -> None:
    rows_path = tmp_path / "rows.csv"
    summary_path = tmp_path / "summary.csv"
    doc = tmp_path / "doc.md"
    manifest_path = tmp_path / "manifest.json"
    _write_csv(rows_path, FIELDNAMES, [])
    summary_rows = [{"metric": "total_manifests", "value": "0"}]
    summary_rows.extend({"metric": status, "value": "0"} for status in AUDIT_STATUSES)
    _write_csv(summary_path, SUMMARY_FIELDNAMES, summary_rows)
    doc.write_text(
        "\n".join(
            [
                "Status: historical audit, not a prospective approval.",
                "A drifted historical manifest is not a failed result.",
                "Use `scripts.check_study_lock_manifest` for one fresh, study-specific",
                "- total_manifests: 0",
                *[f"- {status}: 0" for status in AUDIT_STATUSES],
            ]
        ),
        encoding="utf-8",
    )
    manifest_path.write_text("[]\n", encoding="utf-8")

    failures = validate_doc(doc, rows_path, summary_path, manifest_path)

    assert f"{manifest_path} JSON root must be an object" in failures


def test_validate_doc_rejects_summary_drift(tmp_path: Path) -> None:
    rows_path = tmp_path / "rows.csv"
    summary_path = tmp_path / "summary.csv"
    doc = tmp_path / "doc.md"
    manifest_path = tmp_path / "manifest.json"
    _write_csv(rows_path, FIELDNAMES, [])
    _write_csv(
        summary_path,
        SUMMARY_FIELDNAMES,
        [{"metric": "total_manifests", "value": "99"}],
    )
    doc.write_text(
        "Status: historical audit, not a prospective approval.\n"
        "A drifted historical manifest is not a failed result.\n"
        "Use `scripts.check_study_lock_manifest` for one fresh, study-specific\n",
        encoding="utf-8",
    )
    manifest_path.write_text(
        json.dumps(
            {
                "tool": "audit_study_lock_manifest_drift",
                "outputs": [
                    {"path": rows_path.as_posix()},
                    {"path": summary_path.as_posix()},
                    {"path": doc.as_posix()},
                ],
            }
        ),
        encoding="utf-8",
    )

    failures = validate_doc(doc, rows_path, summary_path, manifest_path)

    assert any("does not match rows" in failure for failure in failures)
