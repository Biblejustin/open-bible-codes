import csv
import json
from pathlib import Path

from scripts import check_wrr_source_recovery_probe_doc as check


def test_current_wrr_source_recovery_probe_doc_passes() -> None:
    assert check.validate_source_recovery_probe_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_source_recovery_probe_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_probe_only_status_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_RECOVERY_PROBE.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[2:]) + "\n", encoding="utf-8")

    failures = check.validate_source_recovery_probe_doc(doc)

    assert any("live-source recovery probe only" in failure for failure in failures)


def test_missing_probe_label_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_SOURCE_RECOVERY_PROBE.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "| torah_code_research_program_1_shtml |",
        "| missing_program_1_shtml |",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_source_recovery_probe_doc(doc)

    assert any("torah_code_research_program_1_shtml" in failure for failure in failures)


def test_validate_source_recovery_probe_accepts_matching_data(tmp_path: Path) -> None:
    failures = check.validate_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        source_manifest=_source_manifest(tmp_path),
        report_manifest=_report_manifest(tmp_path),
    )

    assert failures == []


def test_validate_source_recovery_probe_rejects_row_drift(tmp_path: Path) -> None:
    failures = check.validate_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path, bad_label="torah_code_research_program_1"),
        summary=_summary_csv(tmp_path),
        source_manifest=_source_manifest(tmp_path),
        report_manifest=_report_manifest(tmp_path),
    )

    assert any("torah_code_research_program_1 bytes drifted" in failure for failure in failures)


def test_validate_source_recovery_probe_rejects_summary_drift(tmp_path: Path) -> None:
    failures = check.validate_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_key="usable_current_source_rows"),
        source_manifest=_source_manifest(tmp_path),
        report_manifest=_report_manifest(tmp_path),
    )

    assert any("usable_current_source_rows drifted" in failure for failure in failures)


def test_validate_source_recovery_probe_rejects_source_manifest_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        source_manifest=_source_manifest(tmp_path, bad_label="torah_code_research_program_1"),
        report_manifest=_report_manifest(tmp_path),
    )

    assert any("torah_code_research_program_1 http_status drifted" in failure for failure in failures)


def test_validate_source_recovery_probe_rejects_report_manifest_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        source_manifest=_source_manifest(tmp_path),
        report_manifest=_report_manifest(tmp_path, bad_claim=True),
    )

    assert any("claim_boundary drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "WRR source-recovery probe doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    path = tmp_path / "WRR_SOURCE_RECOVERY_PROBE.md"
    lines = list(check.REQUIRED_PHRASES)
    lines.extend(
        "| "
        + " | ".join(
            [
                label,
                "200",
                "True",
                "True",
                "False",
                "True",
                check.EXPECTED_BYTES,
                f"`{check.EXPECTED_SHA256[:16]}`",
                "unusable_current_download",
            ]
        )
        + " |"
        for label in check.EXPECTED_PROBE_LABELS
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _rows_csv(tmp_path: Path, *, bad_label: str | None = None) -> Path:
    path = tmp_path / "source_recovery_probe.csv"
    rows = []
    for label in check.EXPECTED_PROBE_LABELS:
        rows.append(
            {
                "label": label,
                "requested_url": f"https://www.torah-code.org/{label}.html",
                "final_url": check.ROOT_URL,
                "redirected": "True",
                "http_status": "200",
                "download_status": "downloaded",
                "path": f"reports/wrr_source_recovery_probe/{label}.html",
                "bytes": "1" if label == bad_label else check.EXPECTED_BYTES,
                "sha256": check.EXPECTED_SHA256,
                "title": "root",
                "canonical": check.ROOT_URL,
                "expected_label": check.EXPECTED_LABEL_TEXT[label],
                "expected_label_present": "False",
                "canonical_is_root": "True",
                "final_url_is_root": "True",
                "spam_marker_present": "True",
                "usable_status": "unusable_current_download",
            }
        )
    return _write_csv(path, check.EXPECTED_ROW_FIELDNAMES, rows)


def _summary_csv(tmp_path: Path, *, bad_key: str | None = None) -> Path:
    path = tmp_path / "source_recovery_probe_summary.csv"
    row = dict(check.EXPECTED_SUMMARY)
    if bad_key is not None:
        row[bad_key] = "1"
    return _write_csv(path, check.EXPECTED_SUMMARY_FIELDNAMES, [row])


def _source_manifest(tmp_path: Path, *, bad_label: str | None = None) -> Path:
    path = tmp_path / "sources.manifest.json"
    downloads = []
    for label in check.EXPECTED_PROBE_LABELS:
        downloads.append(
            {
                "label": label,
                "url": f"https://www.torah-code.org/{label}.html",
                "final_url": check.ROOT_URL,
                "redirected": True,
                "http_status": 500 if label == bad_label else 200,
                "path": f"reports/wrr_source_recovery_probe/{label}.html",
                "status": "downloaded",
                "bytes": int(check.EXPECTED_BYTES),
                "sha256": check.EXPECTED_SHA256,
            }
        )
    path.write_text(json.dumps({"downloads": downloads}) + "\n", encoding="utf-8")
    return path


def _report_manifest(tmp_path: Path, *, bad_claim: bool = False) -> Path:
    path = tmp_path / "source_recovery_probe.manifest.json"
    path.write_text(
        json.dumps(
            {
                "rows": len(check.EXPECTED_PROBE_LABELS),
                "summary": {
                    key: int(value) if value.isdigit() else value
                    for key, value in check.EXPECTED_SUMMARY.items()
                },
                "claim_boundary": (
                    "changed" if bad_claim else check.EXPECTED_REPORT_CLAIM_BOUNDARY
                ),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def _write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> Path:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
