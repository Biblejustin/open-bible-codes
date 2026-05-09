import tempfile
import unittest
from pathlib import Path

from scripts.download_wrr_sources import (
    DEFAULT_SOURCES,
    REQUIRED_MANIFEST_LABELS,
    sha256_file,
    source_filename,
)


class DownloadWrrSourcesTests(unittest.TestCase):
    def test_source_filename_uses_stable_famous_rabbi_names(self) -> None:
        self.assertEqual(
            source_filename("wrr_1994_paper", "https://example.test/source.pdf"),
            "wrr_1994_paper.pdf",
        )
        self.assertEqual(source_filename("wrr1", "https://example.test/source.txt"), "WRR1.txt")
        self.assertEqual(source_filename("wrr2", "https://example.test/source.txt"), "WRR2.txt")
        self.assertEqual(source_filename("se2a", "https://example.test/source.txt"), "SE2a.txt")
        self.assertEqual(source_filename("se2b", "https://example.test/source.txt"), "SE2b.txt")
        self.assertEqual(source_filename("se3", "https://example.test/source.txt"), "SE3.txt")
        self.assertEqual(
            source_filename("wrr_nations_mc", "https://example.test/main_mc.html"),
            "wrr_nations_main_mc.html",
        )
        self.assertEqual(
            source_filename("wrr_nations_gir", "https://example.test/main_gir.html"),
            "wrr_nations_main_gir.html",
        )
        self.assertEqual(source_filename("mc_key", "https://example.test/MC.html"), "mc_key.html")
        self.assertEqual(source_filename("wnp_mc", "https://example.test/main_mc.html"), "wnp_mc.html")
        self.assertEqual(source_filename("wnp_en", "https://example.test/main_en.html"), "wnp_en.html")

    def test_sha256_file_hashes_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_text("abc", encoding="utf-8")

            digest = sha256_file(path)

        self.assertEqual(digest, "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")

    def test_required_manifest_labels_track_default_sources(self) -> None:
        self.assertEqual(REQUIRED_MANIFEST_LABELS, tuple(DEFAULT_SOURCES))
        self.assertIn("wrr_nations_mc", REQUIRED_MANIFEST_LABELS)
        self.assertIn("wrr_nations_gir", REQUIRED_MANIFEST_LABELS)


if __name__ == "__main__":
    unittest.main()
