import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json

from scripts import check_cities_pdf_recovery_probe_doc as check


def test_current_cities_pdf_recovery_probe_doc_passes() -> None:
    assert check.validate_cities_pdf_recovery_probe_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path) -> None:
    doc = tmp_path / "probe.md"
    doc.write_text("# Cities PDF Recovery Probe\n", encoding="utf-8")

    failures = check.validate_cities_pdf_recovery_probe_doc(doc)

    assert any("missing phrase" in failure for failure in failures)


def test_validate_cities_pdf_recovery_accepts_matching_data(tmp_path) -> None:
    failures = check.validate_cities_pdf_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert failures == []


def test_validate_cities_pdf_recovery_rejects_row_drift(tmp_path) -> None:
    failures = check.validate_cities_pdf_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path, bad_label="cities_pdf_wrr"),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path),
    )

    assert any("cities_pdf_wrr pdf_pages drifted" in failure for failure in failures)


def test_validate_cities_pdf_recovery_rejects_summary_drift(tmp_path) -> None:
    failures = check.validate_cities_pdf_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path, bad_key="usable_pdf_rows"),
        manifest=_manifest(tmp_path),
    )

    assert any("usable_pdf_rows drifted" in failure for failure in failures)


def test_validate_cities_pdf_recovery_rejects_manifest_drift(tmp_path) -> None:
    failures = check.validate_cities_pdf_recovery_probe_doc(
        _doc(tmp_path),
        rows=_rows_csv(tmp_path),
        summary=_summary_csv(tmp_path),
        manifest=_manifest(tmp_path, bad_claim=True),
    )

    assert any("claim_boundary drifted" in failure for failure in failures)


def _doc(tmp_path):
    doc = tmp_path / "CITIES_PDF_RECOVERY_PROBE.md"
    lines = list(check.REQUIRED_PHRASES)
    for label in check.EXPECTED_LABELS:
        lines.append(f"| {label} | source | html | no_archived_snapshot | 0 | url |")
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return doc


def _rows_csv(tmp_path, *, bad_label=None):
    path = tmp_path / "cities_pdf_recovery_probe.csv"
    rows = []
    for label, (pages, text_chars, sha_prefix) in check.EXPECTED_USABLE_ROWS.items():
        rows.append(_row(label, usable=True, pages=pages, text_chars=text_chars, sha=sha_prefix))
    for label in check.EXPECTED_KEY_UNRECOVERED:
        rows.append(_row(label, usable=False))
    filler_needed = int(check.EXPECTED_SUMMARY["pdf_urls_probed"]) - len(rows)
    for index in range(filler_needed):
        rows.append(_row(f"cities_pdf_filler_{index:02d}", usable=False))
    if bad_label is not None:
        for row in rows:
            if row["label"] == bad_label:
                row["pdf_pages"] = "99"
    return _write_csv(path, check.EXPECTED_ROW_FIELDNAMES, rows)


def _row(label, *, usable, pages="", text_chars="", sha=""):
    return {
        "label": label,
        "source_pages": "source",
        "url": f"https://www.torah-code.org/{label}.pdf",
        "live_final_url": "https://www.torah-code.org/",
        "live_http_status": "200",
        "live_status": "html",
        "live_kind": "html",
        "live_bytes": "629155",
        "live_sha256": "d60a59519b55bcff",
        "archive_probe_url": f"https://www.torah-code.org/{label}.pdf",
        "archive_status": "archive_downloaded" if usable else "no_archived_snapshot",
        "archive_snapshot_source": "availability_closest" if usable else "",
        "archive_timestamp": "20000101000000" if usable else "",
        "archive_cdx_checked": "False",
        "archive_cdx_candidate_count": "0",
        "archive_raw_url": "https://web.archive.org/example" if usable else "",
        "archive_kind": "pdf" if usable else "",
        "archive_bytes": "1" if usable else "0",
        "archive_sha256": sha + "x" if usable else "",
        "selected_source": "archive" if usable else "",
        "selected_path": (
            f"reports/cities_pdf_recovery_probe/snapshots/archive/{label}.pdf"
            if usable
            else ""
        ),
        "pdf_pages": pages if usable else "",
        "pdf_text_chars": text_chars if usable else "",
        "usable_status": "usable_archived_pdf" if usable else "no_pdf_recovered",
    }


def _summary_csv(tmp_path, *, bad_key=None):
    path = tmp_path / "cities_pdf_recovery_probe_summary.csv"
    row = dict(check.EXPECTED_SUMMARY)
    if bad_key is not None:
        row[bad_key] = "99"
    return _write_csv(path, list(check.EXPECTED_SUMMARY), [row])


def _manifest(tmp_path, *, bad_claim=False):
    path = tmp_path / "cities_pdf_recovery_probe.manifest.json"
    path.write_text(
        json.dumps(
            {
                "tool": "build_cities_pdf_recovery_probe.py",
                "source_globs": ["reports/wrr_1994/torah_code_experiment_cities*.html"],
                "rows": int(check.EXPECTED_SUMMARY["pdf_urls_probed"]),
                "summary": {
                    key: int(value) if value.isdigit() else value
                    for key, value in check.EXPECTED_SUMMARY.items()
                },
                "outputs": {
                    "csv": str(check.DEFAULT_ROWS),
                    "summary": str(check.DEFAULT_SUMMARY),
                    "markdown": str(check.DEFAULT_DOC),
                    "manifest": str(check.DEFAULT_MANIFEST),
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


def _write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path
