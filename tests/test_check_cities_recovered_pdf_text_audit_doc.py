import csv
import json
import shutil
from pathlib import Path

from scripts import check_cities_recovered_pdf_text_audit_doc as check


def test_current_cities_recovered_pdf_text_audit_doc_passes() -> None:
    assert check.validate_cities_recovered_pdf_text_audit_doc(check.DEFAULT_DOC) == []


def test_matching_locked_outputs_pass(tmp_path: Path) -> None:
    doc, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert failures == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    _, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)
    doc = tmp_path / "audit.md"
    doc.write_text("# Cities Recovered PDF Text Audit\n", encoding="utf-8")

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert any("missing phrase" in failure for failure in failures)


def test_detects_summary_count_mismatch(tmp_path: Path) -> None:
    doc, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)
    fieldnames, summary_rows = read_csv(summary)
    summary_rows[0]["recovered_pdf_rows"] = "99"
    write_csv(summary, fieldnames, summary_rows)

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert any("summary row drifted" in failure for failure in failures)


def test_detects_row_data_drift(tmp_path: Path) -> None:
    doc, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)
    fieldnames, row_data = read_csv(rows)
    row_data[0]["sha256"] = "bad"
    write_csv(rows, fieldnames, row_data)

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert any("row data drifted" in failure for failure in failures)


def test_detects_row_fieldname_drift(tmp_path: Path) -> None:
    doc, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)
    fieldnames, row_data = read_csv(rows)
    write_csv(rows, fieldnames[:-1], [{k: v for k, v in row.items() if k != "title_guess"} for row in row_data])

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert any("fieldnames drifted" in failure for failure in failures)


def test_detects_anchor_drift(tmp_path: Path) -> None:
    doc, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)
    fieldnames, anchor_rows = read_csv(anchors)
    anchor_rows[0]["status"] = "missing"
    write_csv(anchors, fieldnames, anchor_rows)

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert any("anchor rows drifted" in failure for failure in failures)


def test_detects_manifest_drift(tmp_path: Path) -> None:
    doc, rows, summary, anchors, manifest = copy_current_outputs(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["rows"] = 99
    manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    failures = check.validate_cities_recovered_pdf_text_audit_doc(
        doc,
        rows,
        summary,
        anchors,
        manifest,
    )

    assert any("rows drifted" in failure for failure in failures)


def copy_current_outputs(tmp_path: Path) -> tuple[Path, Path, Path, Path, Path]:
    doc = tmp_path / "audit.md"
    rows = tmp_path / "rows.csv"
    summary = tmp_path / "summary.csv"
    anchors = tmp_path / "anchors.csv"
    manifest = tmp_path / "manifest.json"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_ROWS, rows)
    shutil.copyfile(check.DEFAULT_SUMMARY, summary)
    shutil.copyfile(check.DEFAULT_ANCHORS, anchors)
    shutil.copyfile(check.DEFAULT_MANIFEST, manifest)
    return doc, rows, summary, anchors, manifest


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
