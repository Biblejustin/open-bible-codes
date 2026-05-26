import csv
import json
import shutil
from pathlib import Path

from scripts import check_cities_unreadable_pdf_ocr_feasibility_doc as check


def test_current_cities_unreadable_pdf_ocr_feasibility_doc_passes() -> None:
    assert check.validate_cities_unreadable_pdf_ocr_feasibility_doc(check.DEFAULT_DOC) == []


def test_detects_missing_boundary_phrase(tmp_path: Path) -> None:
    paths = copy_current_outputs(tmp_path)
    paths["doc"].write_text(
        "# Cities Unreadable PDF OCR Feasibility\n",
        encoding="utf-8",
    )

    failures = validate_tmp(paths)

    assert any("missing phrase" in failure for failure in failures)


def test_detects_source_script_text_in_rows(tmp_path: Path) -> None:
    paths = copy_current_outputs(tmp_path)
    fieldnames, rows = read_csv(paths["rows"])
    rows[0]["ocr_note"] = "Hebrew source: אבג"
    write_csv(paths["rows"], fieldnames, rows)

    failures = validate_tmp(paths)

    assert any("source-script body text" in failure for failure in failures)


def test_detects_rows_fieldname_drift(tmp_path: Path) -> None:
    paths = copy_current_outputs(tmp_path)
    fieldnames, rows = read_csv(paths["rows"])
    fieldnames.remove("claim_boundary")
    write_csv(paths["rows"], fieldnames, rows)

    failures = validate_tmp(paths)

    assert any("fieldnames drifted" in failure for failure in failures)


def test_detects_summary_row_drift(tmp_path: Path) -> None:
    paths = copy_current_outputs(tmp_path)
    fieldnames, rows = read_csv(paths["summary"])
    rows[0]["value"] = "99"
    write_csv(paths["summary"], fieldnames, rows)

    failures = validate_tmp(paths)

    assert any("summary rows drifted" in failure for failure in failures)


def test_detects_manifest_drift(tmp_path: Path) -> None:
    paths = copy_current_outputs(tmp_path)
    manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
    manifest["rows"] = 99
    paths["manifest"].write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    failures = validate_tmp(paths)

    assert any("rows drifted" in failure for failure in failures)


def copy_current_outputs(root: Path) -> dict[str, Path]:
    paths = {
        "doc": root / "feasibility.md",
        "rows": root / "rows.csv",
        "summary": root / "summary.csv",
        "manifest": root / "manifest.json",
    }
    shutil.copy2(check.DEFAULT_DOC, paths["doc"])
    shutil.copy2(check.DEFAULT_ROWS, paths["rows"])
    shutil.copy2(check.DEFAULT_SUMMARY, paths["summary"])
    shutil.copy2(check.DEFAULT_MANIFEST, paths["manifest"])
    return paths


def validate_tmp(paths: dict[str, Path]) -> list[str]:
    return check.validate_cities_unreadable_pdf_ocr_feasibility_doc(
        paths["doc"],
        paths["rows"],
        paths["summary"],
        paths["manifest"],
    )


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
