import csv
import json
from pathlib import Path

from scripts import check_hypothesis_testing_source_audit_doc as check


def test_current_hypothesis_testing_source_audit_doc_passes() -> None:
    assert check.validate_hypothesis_testing_source_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_hypothesis_testing_source_audit_doc(tmp_path / "missing.md")

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_no_usable_pages_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "HYPOTHESIS_TESTING_SOURCE_AUDIT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:9]) + "\n", encoding="utf-8")

    failures = check.validate_hypothesis_testing_source_audit_doc(doc)

    assert any("usable hypothesis-testing source pages" in failure for failure in failures)


def test_validate_hypothesis_testing_source_accepts_matching_data(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_hypothesis_testing_source_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"]),
        anchors=_anchors_csv(paths["anchors"]),
        manifest=_manifest(paths),
        source_manifest=_source_manifest(paths["source_manifest"]),
    )

    assert failures == []


def test_validate_hypothesis_testing_source_rejects_row_drift(tmp_path: Path) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_hypothesis_testing_source_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"], bad_page="overview"),
        summary=_summary_csv(paths["summary"]),
        anchors=_anchors_csv(paths["anchors"]),
        manifest=_manifest(paths),
        source_manifest=_source_manifest(paths["source_manifest"]),
    )

    assert any("overview expected_label_present drifted" in failure for failure in failures)


def test_validate_hypothesis_testing_source_rejects_summary_drift(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_hypothesis_testing_source_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"], bad_key="usable_method_pages"),
        anchors=_anchors_csv(paths["anchors"]),
        manifest=_manifest(paths),
        source_manifest=_source_manifest(paths["source_manifest"]),
    )

    assert any("usable_method_pages drifted" in failure for failure in failures)


def test_validate_hypothesis_testing_source_rejects_anchor_drift(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_hypothesis_testing_source_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"]),
        anchors=_anchors_csv(paths["anchors"], bad=True),
        manifest=_manifest(paths),
        source_manifest=_source_manifest(paths["source_manifest"]),
    )

    assert any("anchor rows drifted" in failure for failure in failures)


def test_validate_hypothesis_testing_source_rejects_manifest_drift(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_hypothesis_testing_source_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"]),
        anchors=_anchors_csv(paths["anchors"]),
        manifest=_manifest(paths, bad_claim=True),
        source_manifest=_source_manifest(paths["source_manifest"]),
    )

    assert any("claim_boundary drifted" in failure for failure in failures)


def test_validate_hypothesis_testing_source_rejects_source_manifest_drift(
    tmp_path: Path,
) -> None:
    paths = _paths(tmp_path)
    failures = check.validate_hypothesis_testing_source_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(paths["rows"]),
        summary=_summary_csv(paths["summary"]),
        anchors=_anchors_csv(paths["anchors"]),
        manifest=_manifest(paths),
        source_manifest=_source_manifest(paths["source_manifest"], bad_label="overview"),
    )

    assert any("torah_code_hypothesis_testing_overview bytes drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "hypothesis-testing source audit doc failure" in capsys.readouterr().err


def _paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "doc": tmp_path / "HYPOTHESIS_TESTING_SOURCE_AUDIT.md",
        "rows": tmp_path / "hypothesis_testing_source_pages.csv",
        "summary": tmp_path / "hypothesis_testing_source_summary.csv",
        "anchors": tmp_path / "hypothesis_testing_source_anchors.csv",
        "manifest": tmp_path / "hypothesis_testing_source_audit.manifest.json",
        "source_manifest": tmp_path / "hypothesis_testing_sources.manifest.json",
    }


def _doc(tmp_path: Path) -> Path:
    path = tmp_path / "HYPOTHESIS_TESTING_SOURCE_AUDIT.md"
    path.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return path


def _rows_csv(path: Path, *, bad_page: str | None = None) -> Path:
    rows = []
    for page, (source_path, label, _download_label, _url) in check.EXPECTED_ROWS.items():
        rows.append(
            {
                "page": page,
                "path": source_path,
                "bytes": check.EXPECTED_BYTES,
                "sha256": check.EXPECTED_SHA256,
                "title": check.EXPECTED_TITLE,
                "canonical": check.EXPECTED_CANONICAL,
                "link_count": check.EXPECTED_LINK_COUNT,
                "expected_label": label,
                "expected_label_present": "True" if page == bad_page else "False",
                "spam_marker_present": "True",
                "canonical_is_root": "True",
                "method_anchor_count": "0",
                "usable_status": "unusable_current_download",
            }
        )
    return _write_csv(path, check.analyzer.ROW_FIELDNAMES, rows)


def _summary_csv(path: Path, *, bad_key: str | None = None) -> Path:
    row = dict(check.EXPECTED_SUMMARY)
    if bad_key is not None:
        row[bad_key] = "99"
    return _write_csv(path, check.analyzer.SUMMARY_FIELDNAMES, [row])


def _anchors_csv(path: Path, *, bad: bool = False) -> Path:
    rows = [dict(row) for row in check.EXPECTED_ANCHORS]
    if bad:
        rows[0]["status"] = "found"
    return _write_csv(path, check.analyzer.ANCHOR_FIELDNAMES, rows)


def _manifest(paths: dict[str, Path], *, bad_claim: bool = False) -> Path:
    paths["manifest"].write_text(
        json.dumps(
            {
                "rows": len(check.EXPECTED_ROWS),
                "summary": {
                    key: int(value) if value.isdigit() else value
                    for key, value in check.EXPECTED_SUMMARY.items()
                },
                "anchors": check.EXPECTED_ANCHORS,
                "sources": [row[0] for row in check.EXPECTED_ROWS.values()],
                "outputs": {
                    "csv": str(paths["rows"]),
                    "summary": str(paths["summary"]),
                    "anchors": str(paths["anchors"]),
                    "markdown": str(paths["doc"]),
                    "manifest": str(paths["manifest"]),
                },
                "claim_boundary": (
                    "changed" if bad_claim else check.EXPECTED_CLAIM_BOUNDARY
                ),
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return paths["manifest"]


def _source_manifest(
    path: Path,
    *,
    bad_label: str | None = None,
) -> Path:
    downloads = []
    for page, (source_path, _label, download_label, url) in check.EXPECTED_ROWS.items():
        downloads.append(
            {
                "label": download_label,
                "path": source_path,
                "url": url,
                "bytes": 1 if page == bad_label else int(check.EXPECTED_BYTES),
                "sha256": check.EXPECTED_SHA256,
                "final_url": check.EXPECTED_CANONICAL,
                "http_status": 200,
                "status": "downloaded",
                "redirected": True,
            }
        )
    path.write_text(json.dumps({"downloads": downloads}) + "\n", encoding="utf-8")
    return path


def _write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
