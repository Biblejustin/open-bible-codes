import unittest
from pathlib import Path

from scripts.download_nonbible_controls import (
    SOURCES,
    strip_gutenberg_boilerplate,
    tei_xml_to_text,
)


class NonBibleControlTests(unittest.TestCase):
    def test_three_sources_per_language_are_registered(self) -> None:
        by_language: dict[str, list[str]] = {}
        for source_id, source in SOURCES.items():
            by_language.setdefault(source.language, []).append(source_id)

        self.assertEqual(sorted(by_language), ["english", "greek", "hebrew"])
        self.assertEqual(len(by_language["hebrew"]), 3)
        self.assertEqual(len(by_language["greek"]), 3)
        self.assertEqual(len(by_language["english"]), 3)

    def test_registered_sources_have_matching_configs(self) -> None:
        expected_configs = {
            "english_pg_moby_dick": "configs/nonbible_english_pg_moby_dick.toml",
            "english_pg_shakespeare": "configs/nonbible_english_pg_shakespeare.toml",
            "english_pg_war_and_peace": "configs/nonbible_english_pg_war_and_peace.toml",
            "greek_perseus_herodotus": "configs/nonbible_greek_perseus_herodotus.toml",
            "greek_perseus_iliad": "configs/nonbible_greek_perseus_iliad.toml",
            "greek_perseus_odyssey": "configs/nonbible_greek_perseus_odyssey.toml",
            "hebrew_pby_ahad_haam": "configs/nonbible_hebrew_pby_ahad_haam.toml",
            "hebrew_pby_bialik": "configs/nonbible_hebrew_pby_bialik.toml",
            "hebrew_pby_brenner": "configs/nonbible_hebrew_pby_brenner.toml",
        }

        self.assertEqual(set(SOURCES), set(expected_configs))
        for source_id, config_path in expected_configs.items():
            text = Path(config_path).read_text(encoding="utf-8")
            self.assertIn(str(SOURCES[source_id].out_text), text)

    def test_tei_xml_to_text_uses_text_body(self) -> None:
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader><fileDesc><titleStmt><title>Metadata</title></titleStmt></fileDesc></teiHeader>
  <text><body><p>\xce\xbb\xcf\x8c\xce\xb3\xce\xbf\xcf\x82 <hi>\xce\xb8\xce\xb5\xcf\x8c\xcf\x82</hi>.</p></body></text>
</TEI>
"""

        text = tei_xml_to_text(xml)

        self.assertIn("λόγος", text)
        self.assertIn("θεός", text)
        self.assertNotIn("Metadata", text)

    def test_gutenberg_boilerplate_is_stripped(self) -> None:
        text = "\n".join(
            [
                "header",
                "*** START OF THE PROJECT GUTENBERG EBOOK SAMPLE ***",
                "Real text",
                "*** END OF THE PROJECT GUTENBERG EBOOK SAMPLE ***",
                "license",
            ]
        )

        self.assertEqual(strip_gutenberg_boilerplate(text), "Real text")


if __name__ == "__main__":
    unittest.main()
