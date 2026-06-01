from __future__ import annotations

from pathlib import Path

from els.protocol_runner import path_fingerprint
from scripts.audit_study_lock_manifest_drift import (
    classify_manifest,
    render_markdown,
    summarize_rows,
)


def _manifest(path: Path, *, dirty: bool = False) -> dict[str, object]:
    return {
        "tool": "build_study_lock_manifest",
        "created_utc": "2026-06-01T00:00:00+00:00",
        "name": "test_lock",
        "status": "locked",
        "git": {"commit": "abc1234", "dirty": dirty},
        "missing_paths": [],
        "settings": {"skip_range": "2..50"},
        "locked_paths": [path_fingerprint(str(path))],
    }


def test_classify_manifest_current(tmp_path: Path) -> None:
    locked = tmp_path / "terms.csv"
    locked.write_text("term_id,term\nx,abc\n", encoding="utf-8")

    row = classify_manifest(tmp_path / "study.manifest.json", _manifest(locked))

    assert row["audit_status"] == "current"
    assert row["structural_failures"] == ""
    assert row["fingerprint_failures"] == ""


def test_classify_manifest_fingerprint_drift(tmp_path: Path) -> None:
    locked = tmp_path / "terms.csv"
    locked.write_text("term_id,term\nx,abc\n", encoding="utf-8")
    manifest = _manifest(locked)
    locked.write_text("term_id,term\nx,changed\n", encoding="utf-8")

    row = classify_manifest(tmp_path / "study.manifest.json", manifest)

    assert row["audit_status"] == "fingerprint_drift"
    assert row["structural_failures"] == ""
    assert "locked path changed" in row["fingerprint_failures"]


def test_classify_manifest_structural_failure(tmp_path: Path) -> None:
    locked = tmp_path / "terms.csv"
    locked.write_text("term_id,term\nx,abc\n", encoding="utf-8")

    row = classify_manifest(
        tmp_path / "study.manifest.json",
        _manifest(locked, dirty=True),
    )

    assert row["audit_status"] == "structural_fail"
    assert "git dirty-state is true" in row["structural_failures"]


def test_summarize_rows_counts_statuses() -> None:
    rows = [
        {"audit_status": "current"},
        {"audit_status": "fingerprint_drift"},
        {"audit_status": "fingerprint_drift"},
        {"audit_status": "structural_fail"},
    ]

    assert summarize_rows(rows) == {
        "total_manifests": 4,
        "current": 1,
        "fingerprint_drift": 2,
        "structural_fail": 1,
    }


def test_render_markdown_explains_historical_boundary() -> None:
    rows = [
        {
            "manifest_path": "reports/study_locks/example.manifest.json",
            "name": "example",
            "status": "locked",
            "audit_status": "current",
            "structural_failures": "",
            "fingerprint_failures": "",
        }
    ]
    summary = summarize_rows(rows)

    text = render_markdown(
        rows,
        summary,
        Path("reports/study_locks"),
        Path("reports/audit.csv"),
        Path("reports/summary.csv"),
    )

    assert "Status: historical audit, not a prospective approval." in text
    assert "A drifted historical manifest is not a failed result." in text
    assert "- current: 1" in text
    assert "`reports/study_locks/example.manifest.json`" in text
