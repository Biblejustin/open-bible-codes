import unittest
from argparse import Namespace
from array import array
from pathlib import Path
from tempfile import TemporaryDirectory

from els.corpus import Corpus, VerseSpan
from scripts.analyze_apocrypha_only_counts import write_markdown, text_for_class


class ApocryphaOnlyCountsTests(unittest.TestCase):
    def test_text_for_class_splits_apocrypha_books(self) -> None:
        corpus = Corpus(
            name="demo",
            language="greek",
            keep_hebrew_final_forms=False,
            text="abcdef",
            verses=(
                VerseSpan("demo", "MAL 1:1", "MAL", "1", "1", "", 0, 2, 3),
                VerseSpan("demo", "TOB 1:1", "TOB", "1", "1", "", 3, 5, 3),
            ),
            position_to_verse=array("i", [0, 0, 0, 1, 1, 1]),
        )

        self.assertEqual(text_for_class(corpus, apocrypha=False), "abc")
        self.assertEqual(text_for_class(corpus, apocrypha=True), "def")

    def test_write_markdown_displays_original_language_terms(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            out = root / "counts.md"
            args = Namespace(
                corpus_label="LXX",
                config=Path("configs/example.toml"),
                control=["ODYSSEY=configs/odyssey.toml"],
                terms=[Path("terms/example.csv")],
                min_skip=2,
                max_skip=250,
                direction="both",
                min_term_length=4,
                jobs=1,
                out=root / "counts.csv",
                summary_out=root / "summary.csv",
                markdown_out=out,
                manifest_out=root / "manifest.json",
            )
            rows = [
                row("bible_apocrypha", "LXX", "ναοσ", "Temple", 10, "71.0"),
                row("bible_canonical", "LXX", "ναοσ", "Temple", 5, "61.0"),
                row("nonbible_control", "ODYSSEY", "ναοσ", "Temple", 4, "63.0"),
            ]

            write_markdown(out, rows, [{"metric": "queries_tested", "value": 1}], args)
            text = out.read_text(encoding="utf-8")

        self.assertIn("`ναοσ` (naos; English: temple)", text)


def row(
    segment: str,
    label: str,
    term: str,
    concept: str,
    hits: int,
    hits_per_million: str,
) -> dict[str, object]:
    return {
        "segment": segment,
        "segment_label": label,
        "normalized_term": term,
        "concepts": concept,
        "hit_count": hits,
        "hits_per_million": hits_per_million,
    }
