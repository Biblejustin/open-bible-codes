import csv
import json
from pathlib import Path

from scripts import check_research_missing_model_pages_audit_doc as check


def test_current_research_missing_model_pages_audit_doc_passes() -> None:
    assert check.validate_research_missing_model_pages_audit_doc(check.DEFAULT_DOC) == []


def test_missing_doc_fails(tmp_path: Path) -> None:
    failures = check.validate_research_missing_model_pages_audit_doc(
        tmp_path / "missing.md"
    )

    assert failures == [f"{tmp_path / 'missing.md'} is missing"]


def test_missing_no_usable_pages_phrase_fails(tmp_path: Path) -> None:
    doc = tmp_path / "RESEARCH_MISSING_MODEL_PAGES_AUDIT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES[:10]) + "\n", encoding="utf-8")

    failures = check.validate_research_missing_model_pages_audit_doc(doc)

    assert any("missing source material" in failure for failure in failures)


def test_validate_research_missing_model_pages_accepts_matching_data(
    tmp_path: Path,
) -> None:
    failures = check.validate_research_missing_model_pages_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert failures == []


def test_validate_research_missing_model_pages_rejects_row_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_research_missing_model_pages_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path, bad_model="els_model_level_2"),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert any("els_model_level_2 requested_url drifted" in failure for failure in failures)


def test_validate_research_missing_model_pages_rejects_summary_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_research_missing_model_pages_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_key="usable_model_pages"),
        manifest=_manifest(tmp_path),
    )

    assert any("usable_model_pages drifted" in failure for failure in failures)


def test_validate_research_missing_model_pages_rejects_manifest_drift(
    tmp_path: Path,
) -> None:
    failures = check.validate_research_missing_model_pages_audit_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path, bad_claim=True),
    )

    assert any("claim_boundary drifted" in failure for failure in failures)


def test_main_reports_failure(tmp_path: Path, capsys) -> None:
    missing = tmp_path / "missing.md"

    code = check.main(["--doc", str(missing)])

    assert code == 1
    assert "research missing model pages audit doc failure" in capsys.readouterr().err


def _doc(tmp_path: Path) -> Path:
    doc = tmp_path / "RESEARCH_MISSING_MODEL_PAGES_AUDIT.md"
    doc.write_text("\n".join(check.REQUIRED_PHRASES) + "\n", encoding="utf-8")
    return doc


def _rows_csv(tmp_path: Path, *, bad_model: str | None = None) -> Path:
    path = tmp_path / "research_missing_model_pages.csv"
    rows = []
    for model_page, (url, label, expected_path) in check.EXPECTED_MODEL_ROWS.items():
        rows.append(
            {
                "model_page": model_page,
                "path": expected_path,
                "requested_url": "changed" if model_page == bad_model else url,
                "bytes": check.EXPECTED_BYTES,
                "sha256": check.EXPECTED_SHA256,
                "title": check.EXPECTED_TITLE,
                "canonical": check.EXPECTED_CANONICAL,
                "expected_label": label,
                "expected_label_present": "False",
                "canonical_is_root": "True",
                "spam_marker_present": "True",
                "usable_status": check.EXPECTED_USABLE_STATUS,
            }
        )
    return _write_csv(path, check.EXPECTED_ROW_FIELDNAMES, rows)


def _summary_csv(tmp_path: Path, *, bad_key: str | None = None) -> Path:
    path = tmp_path / "research_missing_model_pages_summary.csv"
    row = dict(check.EXPECTED_SUMMARY)
    if bad_key is not None:
        row[bad_key] = "99"
    return _write_csv(path, list(check.EXPECTED_SUMMARY), [row])


def _manifest(tmp_path: Path, *, bad_claim: bool = False) -> Path:
    path = tmp_path / "research_missing_model_pages.manifest.json"
    path.write_text(
        json.dumps(
            {
                "rows": len(check.EXPECTED_MODEL_ROWS),
                "adjacent_rows": 2,
                "anchor_status_counts": check.EXPECTED_ANCHOR_STATUS_COUNTS,
                "claim_boundary": (
                    "changed" if bad_claim else check.EXPECTED_CLAIM_BOUNDARY
                ),
                "summary": {
                    key: int(value) if value.isdigit() else value
                    for key, value in check.EXPECTED_SUMMARY.items()
                },
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
