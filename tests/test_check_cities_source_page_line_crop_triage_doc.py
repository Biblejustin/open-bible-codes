import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_page_line_crop_triage_doc as check


class CitiesSourcePageLineCropTriageDocTests(unittest.TestCase):
    def test_current_doc_passes(self) -> None:
        assert check.validate_cities_source_page_line_crop_triage_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_tracked_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            doc.write_text(doc.read_text(encoding="utf-8") + "\nאבג\n", encoding="utf-8")

            failures = check.validate_cities_source_page_line_crop_triage_doc(
                doc,
                rows_csv=rows,
                summary_csv=summary,
                manifest_json=manifest,
                packet_csv=check.DEFAULT_PACKET,
            )

            self.assertTrue(any("source-script body text" in failure for failure in failures))

    def test_flags_rows_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            fieldnames, data = read_csv(rows)
            data[0]["source_row_import"] = "1"
            write_csv(rows, fieldnames, data)

            failures = check.validate_cities_source_page_line_crop_triage_doc(
                doc,
                rows_csv=rows,
                summary_csv=summary,
                manifest_json=manifest,
                packet_csv=check.DEFAULT_PACKET,
            )

            self.assertTrue(any("row data drifted" in failure for failure in failures))

    def test_flags_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["rows"] = 99
            manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            failures = check.validate_cities_source_page_line_crop_triage_doc(
                doc,
                rows_csv=rows,
                summary_csv=summary,
                manifest_json=manifest,
                packet_csv=check.DEFAULT_PACKET,
            )

            self.assertTrue(any("rows drifted" in failure for failure in failures))


def copy_current_outputs(root: Path) -> tuple[Path, Path, Path, Path]:
    doc = root / "triage.md"
    rows = root / "triage.csv"
    summary = root / "summary.csv"
    manifest = root / "manifest.json"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_ROWS, rows)
    shutil.copyfile(check.DEFAULT_SUMMARY, summary)
    shutil.copyfile(check.DEFAULT_MANIFEST, manifest)
    return doc, rows, summary, manifest


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
