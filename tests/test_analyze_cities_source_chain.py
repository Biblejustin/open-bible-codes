import csv
import json
import tempfile
import unittest
from pathlib import Path

from scripts import analyze_cities_source_chain as cities


MAIN_HTML = """<!doctype html><html><head><title>Cities</title></head><body>
The original Gans cities experiment reported a p-level of 6/1,000,000.
<a href="gans_original_report.pdf">Gans report</a>
</body></html>"""

GANS_HTML = """<html><body>
The revised Gans communities experiment reported a p-level of 4/1,000,000.
</body></html>"""

AUMANN_HTML = """<html><body>
The Aumann committee reported that the cities experiments were non-significant.
</body></html>"""

SIMON_HTML = """<html><body>
Margolioth city names found: 330. Used city names found in Margolioth: 197.
The protocol restricts city names to between 5 and 8 letters.
</body></html>"""

WRAPPER_HTML = """<!doctype html><html><head><title>Wayback</title></head><body>
Archived wrapper page, not the underlying PDF.
</body></html>"""


class CitiesSourceChainTests(unittest.TestCase):
    def test_detect_kind_separates_pdf_header_from_html_wrapper(self) -> None:
        self.assertEqual(cities.detect_kind(b"%PDF-1.4\n"), "pdf")
        self.assertEqual(cities.detect_kind(WRAPPER_HTML.encode("utf-8")), "html")
        self.assertEqual(cities.detect_kind(b"plain text"), "other")

    def test_analyze_file_flags_pdf_named_html_wrapper(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "wrapped.pdf"
            path.write_text(WRAPPER_HTML, encoding="utf-8")

            row = cities.analyze_file(path)

            self.assertEqual(row["extension"], "pdf")
            self.assertEqual(row["detected_kind"], "html")
            self.assertEqual(row["status"], "html_wrapper_saved_as_pdf")
            self.assertEqual(row["title"], "Wayback")

    def test_protocol_anchors_find_declared_source_chain_claims(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            html_paths = [
                root / "cities.html",
                root / "gans.html",
                root / "aumann.html",
                root / "simon.html",
            ]
            for path, text in zip(
                html_paths,
                [MAIN_HTML, GANS_HTML, AUMANN_HTML, SIMON_HTML],
                strict=True,
            ):
                path.write_text(text, encoding="utf-8")
            wrapper = root / "appendix.pdf"
            wrapper.write_text(WRAPPER_HTML, encoding="utf-8")

            rows = [cities.analyze_file(path) for path in [*html_paths, wrapper]]
            anchors = cities.protocol_anchors(rows)

            self.assertEqual({row["status"] for row in anchors}, {"found"})

    def test_main_writes_source_chain_outputs_without_default_glob_leak(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "inputs"
            input_dir.mkdir()
            for name, text in {
                "cities.html": MAIN_HTML,
                "gans.html": GANS_HTML,
                "aumann.html": AUMANN_HTML,
                "simon.html": SIMON_HTML,
                "wrapped.pdf": WRAPPER_HTML,
            }.items():
                (input_dir / name).write_text(text, encoding="utf-8")

            rc = cities.main(
                [
                    "--source-glob",
                    str(input_dir / "*"),
                    "--out",
                    str(root / "files.csv"),
                    "--summary-out",
                    str(root / "summary.csv"),
                    "--anchors-out",
                    str(root / "anchors.csv"),
                    "--markdown-out",
                    str(root / "audit.md"),
                    "--manifest-out",
                    str(root / "manifest.json"),
                ]
            )

            self.assertEqual(rc, 0)
            summary_rows = list(csv.DictReader((root / "summary.csv").open(encoding="utf-8")))
            self.assertEqual(summary_rows[0]["source_files"], "5")
            self.assertEqual(summary_rows[0]["html_wrapper_pdf_files"], "1")
            markdown = (root / "audit.md").read_text(encoding="utf-8")
            self.assertIn("source-shape audit only", markdown)
            self.assertIn("Found anchors: 7 of 7", markdown)
            manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["source_globs"], [str(input_dir / "*")])


if __name__ == "__main__":
    unittest.main()
