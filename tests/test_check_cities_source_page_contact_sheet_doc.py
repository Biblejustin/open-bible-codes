import pytest

# Reads generated reports/; auto-skips when corpora/reports are absent.
pytestmark = pytest.mark.requires_corpus

import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_page_contact_sheet_doc as check


class CitiesSourcePageContactSheetDocTests(unittest.TestCase):
    def test_current_doc_passes(self) -> None:
        assert check.validate_cities_source_page_contact_sheet_doc(check.DEFAULT_DOC) == []

    def test_missing_image_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.png"

            failures = check.validate_cities_source_page_contact_sheet_doc(
                check.DEFAULT_DOC,
                image=missing,
                summary=None,
                manifest=None,
                bundle=None,
            )

            self.assertEqual(failures, [f"{missing} is missing"])

    def test_flags_source_script_text_in_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, summary, manifest = copy_current_outputs(root)
            doc.write_text(doc.read_text(encoding="utf-8") + "\nאבג\n", encoding="utf-8")

            failures = check.validate_cities_source_page_contact_sheet_doc(
                doc,
                image=check.DEFAULT_IMAGE,
                summary=summary,
                manifest=manifest,
                bundle=check.DEFAULT_BUNDLE,
            )

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, summary, manifest = copy_current_outputs(root)
            fieldnames, rows = read_csv(summary)
            rows[0]["value"] = "99"
            write_csv(summary, fieldnames, rows)

            failures = check.validate_cities_source_page_contact_sheet_doc(
                doc,
                image=check.DEFAULT_IMAGE,
                summary=summary,
                manifest=manifest,
                bundle=check.DEFAULT_BUNDLE,
            )

            self.assertTrue(any("contact_sheet_pages" in failure for failure in failures))

    def test_flags_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, summary, manifest = copy_current_outputs(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["rows"] = 99
            manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            failures = check.validate_cities_source_page_contact_sheet_doc(
                doc,
                image=check.DEFAULT_IMAGE,
                summary=summary,
                manifest=manifest,
                bundle=check.DEFAULT_BUNDLE,
            )

            self.assertTrue(any("rows drifted" in failure for failure in failures))


def copy_current_outputs(root: Path) -> tuple[Path, Path, Path]:
    doc = root / "contact.md"
    summary = root / "summary.csv"
    manifest = root / "manifest.json"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_SUMMARY, summary)
    shutil.copyfile(check.DEFAULT_MANIFEST, manifest)
    return doc, summary, manifest


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    unittest.main()
