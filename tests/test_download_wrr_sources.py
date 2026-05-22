import tempfile
import unittest
import json
from pathlib import Path
from unittest.mock import patch

from scripts.download_wrr_sources import (
    DEFAULT_SOURCES,
    FetchResult,
    REQUIRED_MANIFEST_LABELS,
    fetch_url,
    main,
    selected_sources,
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
        colinear_attachment_names = {
            "torah_code_colinear_attachment_pls": "torah_code_colinear_attachment_pls.pdf",
            "torah_code_colinear_attachment_roots": "torah_code_colinear_attachment_roots.pdf",
            "torah_code_colinear_attachment_all_1698": "torah_code_colinear_attachment_all_1698.pdf",
            "torah_code_colinear_attachment_res_113": "torah_code_colinear_attachment_res_113.pdf",
            "torah_code_colinear_attachment_consul_138": "torah_code_colinear_attachment_consul_138.pdf",
            "torah_code_colinear_attachment_intersec_108": "torah_code_colinear_attachment_intersec_108.pdf",
            "torah_code_colinear_attachment_comb_143": "torah_code_colinear_attachment_comb_143.pdf",
            "torah_code_colinear_attachment_att_heb": "torah_code_colinear_attachment_att_heb.pdf",
        }
        for label, expected in colinear_attachment_names.items():
            with self.subTest(label=label):
                self.assertEqual(source_filename(label, "https://example.test/source.bin"), expected)
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
        experiment_names = {
            "torah_code_experiments_page": "torah_code_experiments.html",
            "torah_code_experiment_personal_statement": "torah_code_experiment_personal_statement.html",
            "torah_code_experiment_american_presidents_page": "torah_code_experiment_american_presidents.html",
            "torah_code_experiment_american_presidents_paper": "torah_code_experiment_american_presidents.pdf",
            "torah_code_experiment_american_presidents_data": "torah_code_experiment_american_presidents_data.pdf",
            "torah_code_experiment_english_hebrew_transliteration_rules": "torah_code_experiment_english_hebrew_transliteration_rules.pdf",
            "torah_code_experiment_israeli_prime_ministers_page": "torah_code_experiment_israeli_prime_ministers.html",
            "torah_code_experiment_israeli_prime_ministers_paper": "torah_code_experiment_israeli_prime_ministers.pdf",
            "torah_code_experiment_israeli_prime_ministers_1": "torah_code_experiment_israeli_prime_ministers_1.html",
            "torah_code_experiment_israeli_prime_ministers_8": "torah_code_experiment_israeli_prime_ministers_8.html",
            "torah_code_experiment_cities_page": "torah_code_experiment_cities.html",
            "torah_code_experiment_cities_gans_original_report": "torah_code_experiment_cities_gans_original_report.pdf",
            "torah_code_experiment_cities_aumann_report": "torah_code_experiment_cities_aumann_report.pdf",
            "torah_code_experiment_cities_simon_mckay_page": "torah_code_experiment_cities_simon_mckay.html",
            "torah_code_experiment_cities_margolioth_data": "torah_code_experiment_cities_margolioth_data.pdf",
            "torah_code_experiment_sons_of_haman_data": "torah_code_experiment_sons_of_haman_data.html",
            "torah_code_experiment_pumbedita_data": "torah_code_experiment_pumbedita_data.pdf",
            "torah_code_experiment_auschwitz_data": "torah_code_experiment_auschwitz_data.pdf",
            "torah_code_experiment_ark_code": "torah_code_experiment_ark_code.pdf",
            "torah_code_hypothesis_testing_overview": "torah_code_hypothesis_testing_overview.html",
            "torah_code_hypothesis_testing_errors": "torah_code_hypothesis_testing_errors.html",
            "torah_code_hypothesis_testing_hypotheses": "torah_code_hypothesis_testing_hypotheses.html",
            "torah_code_hypothesis_testing_simulated_experiments": "torah_code_hypothesis_testing_simulated_experiments.html",
        }
        for label, expected in experiment_names.items():
            with self.subTest(label=label):
                self.assertEqual(source_filename(label, "https://example.test/source.bin"), expected)
        research_names = {
            "torah_code_research_program_1": "torah_code_research_program_1.html",
            "torah_code_research_program_2": "torah_code_research_program_2.html",
            "torah_code_research_model_overview": "torah_code_research_model_overview.html",
            "torah_code_research_model_overview_shtml": "torah_code_research_model_overview_shtml.html",
            "torah_code_research_geometric_model_level_1": "torah_code_research_geometric_model_level_1.html",
            "torah_code_research_geometric_model_level_2": "torah_code_research_geometric_model_level_2.html",
            "torah_code_research_geometric_model_level_2_shtml": "torah_code_research_geometric_model_level_2_shtml.html",
            "torah_code_research_geometric_model_level_3": "torah_code_research_geometric_model_level_3.html",
            "torah_code_research_geometric_model_level_3_shtml": "torah_code_research_geometric_model_level_3_shtml.html",
            "torah_code_research_els_model_level_1": "torah_code_research_els_model_level_1.html",
            "torah_code_research_els_model_level_1_shtml": "torah_code_research_els_model_level_1_shtml.html",
            "torah_code_research_els_model_level_2": "torah_code_research_els_model_level_2.html",
            "torah_code_research_els_model_level_2_shtml": "torah_code_research_els_model_level_2_shtml.html",
            "torah_code_research_els_model_level_3": "torah_code_research_els_model_level_3.html",
            "torah_code_research_els_model_level_3_shtml": "torah_code_research_els_model_level_3_shtml.html",
        }
        for label, expected in research_names.items():
            with self.subTest(label=label):
                self.assertEqual(source_filename(label, "https://example.test/source.bin"), expected)
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
        self.assertIn("torah_code_colinear_attachment_pls", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_colinear_attachment_att_heb", REQUIRED_MANIFEST_LABELS)
        self.assertIn("gans_communities_paper", REQUIRED_MANIFEST_LABELS)
        self.assertIn("gans_communities_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("haralick_new_protocols", REQUIRED_MANIFEST_LABELS)
        self.assertIn("haralick_experimental_protocol", REQUIRED_MANIFEST_LABELS)
        self.assertIn("witztum_birth_dates_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiments_page", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiment_american_presidents_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiment_israeli_prime_ministers_8", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiment_cities_aumann_report", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiment_cities_margolioth_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiment_sons_of_haman_data", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_experiment_ark_code", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_program_1", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_model_overview", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_model_overview_shtml", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_els_model_level_1", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_geometric_model_level_2", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_geometric_model_level_2_shtml", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_els_model_level_3", REQUIRED_MANIFEST_LABELS)
        self.assertIn("torah_code_research_els_model_level_3_shtml", REQUIRED_MANIFEST_LABELS)
        self.assertIn("wrr_nations_mc", REQUIRED_MANIFEST_LABELS)
        self.assertIn("wrr_nations_gir", REQUIRED_MANIFEST_LABELS)

    def test_selected_sources_filters_requested_labels(self) -> None:
        selected = selected_sources(
            ["torah_code_research_program_1", "torah_code_research_model_overview"]
        )

        self.assertEqual(
            selected,
            [
                (
                    "torah_code_research_program_1",
                    DEFAULT_SOURCES["torah_code_research_program_1"],
                ),
                (
                    "torah_code_research_model_overview",
                    DEFAULT_SOURCES["torah_code_research_model_overview"],
                ),
            ],
        )

    def test_selected_sources_rejects_unknown_label(self) -> None:
        with self.assertRaises(SystemExit):
            selected_sources(["missing"])

    def test_fetch_url_records_final_url_and_status(self) -> None:
        class FakeResponse:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb) -> None:
                return None

            def read(self) -> bytes:
                return b"payload"

            def geturl(self) -> str:
                return "https://example.test/final.html"

        with patch("scripts.download_wrr_sources.urlopen", return_value=FakeResponse()):
            result = fetch_url("https://example.test/start.html")

        self.assertEqual(result.data, b"payload")
        self.assertEqual(result.final_url, "https://example.test/final.html")
        self.assertEqual(result.http_status, 200)

    def test_main_can_refresh_selected_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = root / "manifest.json"
            with patch(
                "scripts.download_wrr_sources.fetch_url",
                return_value=FetchResult(
                    data=b"payload",
                    final_url="https://example.test/final.html",
                    http_status=200,
                ),
            ):
                code = main(
                    [
                        "--out-dir",
                        str(root),
                        "--manifest-out",
                        str(manifest),
                        "--refresh",
                        "--label",
                        "torah_code_research_model_overview",
                    ]
                )

            self.assertEqual(code, 0)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["downloads"]), 1)
            download = payload["downloads"][0]
            self.assertEqual(download["label"], "torah_code_research_model_overview")
            self.assertEqual(download["final_url"], "https://example.test/final.html")
            self.assertTrue(download["redirected"])
            self.assertEqual(download["http_status"], 200)


if __name__ == "__main__":
    unittest.main()
