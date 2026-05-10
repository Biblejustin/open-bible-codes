import unittest
from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_apocrypha_bridge_controls import position_classes, repeated_prefix, write_markdown


class ApocryphaBridgeControlsTests(unittest.TestCase):
    def test_position_classes_split_on_boundary(self) -> None:
        self.assertEqual(
            position_classes([0, 9, 10, 11], 10),
            ["canonical", "canonical", "apocrypha", "apocrypha"],
        )

    def test_repeated_prefix_fills_requested_length(self) -> None:
        self.assertEqual(repeated_prefix("abc", 8), "abcabcab")
        self.assertEqual(repeated_prefix("abc", 0), "")

    def test_write_markdown_displays_original_language_terms(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "controls.md"
            args = Namespace(
                canonical_label="LXX",
                canonical_config=Path("configs/example.toml"),
                control=["ODYSSEY=configs/odyssey.toml"],
                terms=[Path("terms/example.csv")],
                observed=Path("reports/observed.csv"),
                min_skip=2,
                max_skip=250,
                direction="both",
                min_term_length=4,
                jobs=1,
                out=root / "summary.csv",
                term_out=root / "terms.csv",
                markdown_out=out,
                manifest_out=root / "manifest.json",
            )

            write_markdown(
                out,
                [{"control_label": "ODYSSEY", "bridge_rows": 1, "terms_with_bridge_rows": 1, "canonical_to_apocrypha": 1, "apocrypha_to_canonical": 0, "multi_segment_bridge": 0}],
                [{"control_label": "ODYSSEY", "normalized_term": "ναοσ", "bridge_rows": 1, "canonical_to_apocrypha": 1, "apocrypha_to_canonical": 0, "multi_segment_bridge": 0}],
                [{"normalized_term": "ναοσ", "bridge_type": "canonical_to_apocrypha"}],
                args,
            )
            text = out.read_text(encoding="utf-8")

        self.assertIn("`ναοσ` (naos; English: temple)", text)
