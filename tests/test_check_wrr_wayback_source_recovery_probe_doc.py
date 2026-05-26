import csv
import json
from pathlib import Path

from scripts import check_wrr_wayback_source_recovery_probe_doc as check


def test_current_wrr_wayback_source_recovery_probe_doc_passes() -> None:
    assert check.validate_wayback_source_recovery_probe_doc(check.DEFAULT_DOC) == []


def test_missing_wrr_wayback_source_recovery_probe_doc_fails(tmp_path) -> None:
    failures = check.validate_wayback_source_recovery_probe_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_incomplete_wrr_wayback_source_recovery_probe_doc_fails(tmp_path) -> None:
    doc = tmp_path / "WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md"
    doc.write_text("# WRR Wayback Source Recovery Probe\n", encoding="utf-8")

    failures = check.validate_wayback_source_recovery_probe_doc(doc)

    assert failures
    assert any("Status: archived-source recovery probe only." in failure for failure in failures)


def test_missing_wayback_probe_label_fails(tmp_path: Path) -> None:
    doc = tmp_path / "WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md"
    text = check.DEFAULT_DOC.read_text(encoding="utf-8").replace(
        "| torah_code_research_program_1_shtml |",
        "| missing_program_1_shtml |",
    )
    doc.write_text(text, encoding="utf-8")

    failures = check.validate_wayback_source_recovery_probe_doc(doc)

    assert any("torah_code_research_program_1_shtml" in failure for failure in failures)


def test_validate_wayback_source_recovery_probe_accepts_matching_data(
    tmp_path: Path,
) -> None:
    failures = check.validate_wayback_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert failures == []


def test_validate_wayback_source_recovery_probe_rejects_row_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_wayback_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path, bad_label="torah_code_research_program_1_shtml"),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert any("torah_code_research_program_1_shtml bytes drifted" in failure for failure in failures)


def test_validate_wayback_source_recovery_probe_rejects_summary_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_wayback_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_key="usable_archived_source_rows"),
        manifest=_manifest(tmp_path),
    )

    assert any("usable_archived_source_rows drifted" in failure for failure in failures)


def test_validate_wayback_source_recovery_probe_rejects_manifest_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_wayback_source_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path, bad_claim=True),
    )

    assert any("claim_boundary drifted" in failure for failure in failures)


def _doc(tmp_path: Path) -> Path:
    path = tmp_path / "WRR_WAYBACK_SOURCE_RECOVERY_PROBE.md"
    lines = list(check.REQUIRED_PHRASES)
    for label in check.EXPECTED_PROBE_LABELS:
        expected = check.EXPECTED_ROW_OBSERVED[label]
        lines.append(
            "| "
            + " | ".join(
                [
                    label,
                    expected["closest_available"],
                    expected["snapshot_source"],
                    expected["closest_timestamp"],
                    expected["cdx_candidate_count"],
                    expected["expected_label_present"],
                    expected["spam_marker_present"],
                    expected["bytes"],
                    f"`{expected['sha256'][:16]}`" if expected["sha256"] else "",
                    expected["usable_status"],
                ]
            )
            + " |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _rows_csv(tmp_path: Path, *, bad_label: str | None = None) -> Path:
    path = tmp_path / "wayback_source_recovery_probe.csv"
    rows = []
    for label in check.EXPECTED_PROBE_LABELS:
        source = check.SOURCE_BY_LABEL[label]
        expected = dict(check.EXPECTED_ROW_OBSERVED[label])
        if label == bad_label:
            expected["bytes"] = "1"
        usable = expected["usable_status"] == "usable_archived_source"
        rows.append(
            {
                "label": label,
                "concept": source.concept,
                "family": source.family,
                "original_url": source.url,
                "expected_label": source.expected_label,
                "availability_status": "availability_checked",
                "closest_available": expected["closest_available"],
                "closest_status": "200" if expected["closest_available"] == "True" else "",
                "closest_timestamp": expected["closest_timestamp"],
                "closest_url": "https://web.archive.org/web/example" if usable else "",
                "snapshot_source": expected["snapshot_source"],
                "cdx_status": "cdx_checked",
                "cdx_candidate_count": expected["cdx_candidate_count"],
                "archive_raw_url": "https://web.archive.org/web/exampleid_" if usable else "",
                "archive_fetch_status": "downloaded" if usable else "not_available",
                "path": (
                    f"reports/wrr_wayback_source_recovery_probe/snapshots/{label}.html"
                    if usable
                    else ""
                ),
                "bytes": expected["bytes"],
                "sha256": expected["sha256"],
                "title": expected["title"],
                "expected_label_present": expected["expected_label_present"],
                "spam_marker_present": expected["spam_marker_present"],
                "usable_status": expected["usable_status"],
            }
        )
    return _write_csv(path, check.ROW_FIELDNAMES, rows)


def _summary_csv(tmp_path: Path, *, bad_key: str | None = None) -> Path:
    path = tmp_path / "wayback_source_recovery_probe_summary.csv"
    row = dict(check.EXPECTED_SUMMARY)
    if bad_key is not None:
        row[bad_key] = "1"
    return _write_csv(path, check.SUMMARY_FIELDNAMES, [row])


def _manifest(tmp_path: Path, *, bad_claim: bool = False) -> Path:
    path = tmp_path / "wayback_source_recovery_probe.manifest.json"
    path.write_text(
        json.dumps(
            {
                "rows": len(check.EXPECTED_PROBE_LABELS),
                "summary": {
                    key: int(value) if value.isdigit() else value
                    for key, value in check.EXPECTED_SUMMARY.items()
                },
                "claim_boundary": (
                    "changed" if bad_claim else check.EXPECTED_CLAIM_BOUNDARY
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
