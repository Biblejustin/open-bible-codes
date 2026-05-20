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
        self.assertEqual(
            source_filename("mmbbk_1999_paper", "https://example.test/source.pdf"),
            "mmbbk_1999_paper.pdf",
        )
        self.assertEqual(
            source_filename("mmbbk_data_page", "https://example.test/data.html"),
            "mmbbk_data_page.html",
        )
        self.assertEqual(
            source_filename("chance_article", "https://example.test/Chance.pdf"),
            "chance_torah_codes_puzzle_solution.pdf",
        )
        self.assertEqual(
            source_filename("torah_code_papers_page", "https://example.test/papers.html"),
            "torah_code_papers.html",
        )
        self.assertEqual(
            source_filename("torah_code_colinear_paper", "https://example.test/bombach.pdf"),
            "torah_code_colinear_paper.pdf",
        )
        self.assertEqual(
            source_filename("torah_code_colinear_attachments", "https://example.test/attachments.html"),
            "torah_code_colinear_attachments.html",
        )
        self.assertEqual(
            source_filename("gans_communities_paper", "https://example.test/gans.pdf"),
            "gans_communities_paper.pdf",
        )
        self.assertEqual(
            source_filename("gans_communities_data", "https://example.test/communities_data.pdf"),
            "gans_communities_data.pdf",
        )
        self.assertEqual(
            source_filename("haralick_new_protocols", "https://example.test/sspr98.pdf"),
            "haralick_new_protocols.pdf",
        )
        self.assertEqual(
            source_filename("haralick_controversy", "https://example.test/icpr98.pdf"),
            "haralick_controversy.pdf",
        )
        self.assertEqual(
            source_filename("haralick_skeptical_response", "https://example.test/response.pdf"),
            "haralick_skeptical_response.pdf",
        )
        self.assertEqual(
            source_filename("haralick_basic_concepts", "https://example.test/wdp.pdf"),
            "haralick_basic_concepts.pdf",
        )
        self.assertEqual(
            source_filename("haralick_experimental_protocol", "https://example.test/wdp2.pdf"),
            "haralick_experimental_protocol.pdf",
        )
        self.assertEqual(
            source_filename("levitt_component_analysis", "https://example.test/levitt.pdf"),
            "levitt_component_analysis.pdf",
        )
        self.assertEqual(
            source_filename("levitt_component_data", "https://example.test/caweb.pdf"),
            "levitt_component_data.pdf",
        )
        self.assertEqual(
            source_filename("levitt_long_phrases", "https://example.test/belgpdf.pdf"),
            "levitt_long_phrases.pdf",
        )
        self.assertEqual(
            source_filename("levitt_linguistic_connections", "https://example.test/belj.pdf"),
            "levitt_linguistic_connections.pdf",
        )
        self.assertEqual(
            source_filename("rips_twin_towers", "https://example.test/rips.pdf"),
            "rips_twin_towers.pdf",
        )
        self.assertEqual(
            source_filename("schwartzman_dialog_mode", "https://example.test/mode_1.pdf"),
            "schwartzman_dialog_mode.pdf",
        )
        self.assertEqual(
            source_filename("witztum_birth_dates", "https://example.test/witztum.pdf"),
            "witztum_birth_dates.pdf",
        )
        self.assertEqual(
            source_filename("witztum_birth_dates_data", "https://example.test/personaldata.pdf"),
            "witztum_birth_dates_data.pdf",
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
        self.assertIn("mmbbk_1999_paper", REQUIRED_MANIFEST_LABELS)
        self.assertIn("mmbbk_data_page", REQUIRED_MANIFEST_LABELS)
        self.assertIn("chance_article", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_papers_page", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_colinear_paper", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_colinear_attachments", REQUIRED_MANIFEST_LABELS)
        self.assertIn("gans_communities_paper", REQUIRED_MANIFEST_LABELS)
        self.assertIn("gans_communities_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("haralick_new_protocols", REQUIRED_MANIFEST_LABELS)
        self.assertIn("haralick_experimental_protocol", REQUIRED_MANIFEST_LABELS)
        self.assertIn("witztum_birth_dates_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("wrr_nations_mc", REQUIRED_MANIFEST_LABELS)
        self.assertIn("wrr_nations_gir", REQUIRED_MANIFEST_LABELS)


if __name__ == "__main__":
    unittest.main()
