import csv
import json
import shutil
import tempfile
from pathlib import Path

from scripts import check_wrr_post_lock_reporting_boundary_doc as check


def test_current_doc_passes() -> None:
    assert check.validate_post_lock_reporting_boundary_doc(check.DEFAULT_DOC) == []


def test_missing_required_phrase_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        doc, csv_path, manifest = copy_current_outputs(root)
        text = doc.read_text(encoding="utf-8").replace(
            "Status: post-lock reporting boundary locked.",
            "Status: drifted.",
        )
        doc.write_text(text, encoding="utf-8")

        failures = check.validate_post_lock_reporting_boundary_doc(
            doc,
            csv_path=csv_path,
            manifest=manifest,
        )

        assert any("missing phrase" in failure for failure in failures)


def test_csv_drift_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        doc, csv_path, manifest = copy_current_outputs(root)
        fieldnames, rows = read_csv(csv_path)
        rows[0]["status"] = "drifted"
        write_csv(csv_path, fieldnames, rows)

        failures = check.validate_post_lock_reporting_boundary_doc(
            doc,
            csv_path=csv_path,
            manifest=manifest,
        )

        assert any("boundary rows drifted" in failure for failure in failures)


def test_manifest_drift_fails() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        doc, csv_path, manifest = copy_current_outputs(root)
        payload = json.loads(manifest.read_text(encoding="utf-8"))
        payload["rows"] = 99
        manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

        failures = check.validate_post_lock_reporting_boundary_doc(
            doc,
            csv_path=csv_path,
            manifest=manifest,
        )

        assert any("rows drifted" in failure for failure in failures)


def copy_current_outputs(root: Path) -> tuple[Path, Path, Path]:
    doc = root / "boundary.md"
    csv_path = root / "boundary.csv"
    manifest = root / "manifest.json"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_CSV, csv_path)
    shutil.copyfile(check.DEFAULT_MANIFEST, manifest)
    return doc, csv_path, manifest


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
