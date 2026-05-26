import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_row_lock_queue_doc as check


class CitiesSourceRowLockQueueDocTests(unittest.TestCase):
    def test_current_cities_source_row_lock_queue_doc_passes(self) -> None:
        assert check.validate_cities_source_row_lock_queue_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            fieldnames, row_data = read_csv(rows)
            row_data[0]["next_action"] = "Hebrew source: אבג"
            write_csv(rows, fieldnames, row_data)

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
                manifest,
            )

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_source_row_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            fieldnames, row_data = read_csv(rows)
            row_data[0]["current_decision"] = "source_row_import"
            write_csv(rows, fieldnames, row_data)

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
                manifest,
            )

            self.assertTrue(any("imports source row" in failure for failure in failures))

    def test_flags_fieldname_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            fieldnames, row_data = read_csv(rows)
            write_csv(
                rows,
                fieldnames[:-1],
                [{k: v for k, v in row.items() if k != "claim_boundary"} for row in row_data],
            )

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
                manifest,
            )

            self.assertTrue(any("fieldnames drifted" in failure for failure in failures))

    def test_flags_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            fieldnames, summary_rows = read_csv(summary)
            summary_rows[0]["value"] = "99"
            write_csv(summary, fieldnames, summary_rows)

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
                manifest,
            )

            self.assertTrue(any("summary rows drifted" in failure for failure in failures))

    def test_flags_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, rows, summary, manifest = copy_current_outputs(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["rows"] = 99
            manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            failures = check.validate_cities_source_row_lock_queue_doc(
                doc,
                rows,
                summary,
                manifest,
            )

            self.assertTrue(any("rows drifted" in failure for failure in failures))


def copy_current_outputs(root: Path) -> tuple[Path, Path, Path, Path]:
    doc = root / "queue.md"
    rows = root / "rows.csv"
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
