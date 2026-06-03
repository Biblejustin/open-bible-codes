import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_row_lock_evidence_packet_doc as check


class CitiesSourceRowLockEvidencePacketDocTests(unittest.TestCase):
    def test_current_cities_source_row_lock_evidence_packet_doc_passes(self) -> None:
        assert check.validate_cities_source_row_lock_evidence_packet_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = copy_current_outputs(root)
            fieldnames, rows = read_csv(paths["rows"])
            rows[0]["evidence_required"] = "Hebrew source: אבג"
            write_csv(paths["rows"], fieldnames, rows)

            failures = validate_tmp(paths)

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_source_row_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = copy_current_outputs(root)
            fieldnames, rows = read_csv(paths["rows"])
            rows[0]["current_decision"] = "source_row_import"
            write_csv(paths["rows"], fieldnames, rows)

            failures = validate_tmp(paths)

            self.assertTrue(any("imports source row" in failure for failure in failures))

    def test_flags_rows_fieldname_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = copy_current_outputs(root)
            fieldnames, rows = read_csv(paths["rows"])
            fieldnames.remove("claim_boundary")
            write_csv(paths["rows"], fieldnames, rows)

            failures = validate_tmp(paths)

            self.assertTrue(any("fieldnames drifted" in failure for failure in failures))

    def test_flags_summary_row_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = copy_current_outputs(root)
            fieldnames, rows = read_csv(paths["summary"])
            rows[0]["value"] = "99"
            write_csv(paths["summary"], fieldnames, rows)

            failures = validate_tmp(paths)

            self.assertTrue(any("summary rows drifted" in failure for failure in failures))

    def test_flags_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = copy_current_outputs(root)
            manifest = json.loads(paths["manifest"].read_text(encoding="utf-8"))
            manifest["rows"] = 99
            paths["manifest"].write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            failures = validate_tmp(paths)

            self.assertTrue(any("rows drifted" in failure for failure in failures))

    def test_flags_missing_page_image_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            paths = copy_current_outputs(root)
            fieldnames, rows = read_csv(paths["rows"])
            rows[0]["page_image_path"] = str(root / "missing_page.png")
            write_csv(paths["rows"], fieldnames, rows)

            failures = validate_tmp(paths)

            self.assertTrue(
                any("page_image_path not found" in failure for failure in failures)
            )


def copy_current_outputs(root: Path) -> dict[str, Path]:
    paths = {
        "doc": root / "packet.md",
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
    return check.validate_cities_source_row_lock_evidence_packet_doc(
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


if __name__ == "__main__":
    unittest.main()
