import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts import check_cities_source_page_line_crop_packet_doc as check


class CitiesSourcePageLineCropPacketDocTests(unittest.TestCase):
    def test_current_doc_passes(self) -> None:
        assert check.validate_cities_source_page_line_crop_packet_doc(check.DEFAULT_DOC) == []

    def test_flags_source_script_text_in_doc(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, packet, summary, manifest = copy_current_outputs(root)
            doc.write_text(doc.read_text(encoding="utf-8") + "\nאבג\n", encoding="utf-8")

            failures = check.validate_cities_source_page_line_crop_packet_doc(
                doc,
                packet=packet,
                summary=summary,
                manifest=manifest,
            )

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_source_script_text_in_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, packet, summary, manifest = copy_current_outputs(root)
            fieldnames, rows = read_csv(packet)
            rows[0]["next_manual_action"] = "אבג"
            write_csv(packet, fieldnames, rows)

            failures = check.validate_cities_source_page_line_crop_packet_doc(
                doc,
                packet=packet,
                summary=summary,
                manifest=manifest,
            )

            self.assertTrue(
                any("source-script body text" in failure for failure in failures)
            )

    def test_flags_summary_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, packet, summary, manifest = copy_current_outputs(root)
            fieldnames, rows = read_csv(summary)
            rows[0]["value"] = "99"
            write_csv(summary, fieldnames, rows)

            failures = check.validate_cities_source_page_line_crop_packet_doc(
                doc,
                packet=packet,
                summary=summary,
                manifest=manifest,
            )

            self.assertTrue(any("table_candidate_pages" in failure for failure in failures))

    def test_flags_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, packet, summary, manifest = copy_current_outputs(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["rows"] = 99
            manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

            failures = check.validate_cities_source_page_line_crop_packet_doc(
                doc,
                packet=packet,
                summary=summary,
                manifest=manifest,
            )

            self.assertTrue(any("rows drifted" in failure for failure in failures))

    def test_rejects_non_object_manifest_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            doc, packet, summary, manifest = copy_current_outputs(root)
            manifest.write_text("[]\n", encoding="utf-8")

            failures = check.validate_cities_source_page_line_crop_packet_doc(
                doc,
                packet=packet,
                summary=summary,
                manifest=manifest,
            )

            self.assertTrue(any("JSON root must be an object" in failure for failure in failures))


def copy_current_outputs(root: Path) -> tuple[Path, Path, Path, Path]:
    doc = root / "line_crops.md"
    packet = root / "line_crops.csv"
    summary = root / "summary.csv"
    manifest = root / "manifest.json"
    shutil.copyfile(check.DEFAULT_DOC, doc)
    shutil.copyfile(check.DEFAULT_PACKET, packet)
    shutil.copyfile(check.DEFAULT_SUMMARY, summary)
    shutil.copyfile(check.DEFAULT_MANIFEST, manifest)
    return doc, packet, summary, manifest


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
