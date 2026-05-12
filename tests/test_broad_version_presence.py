import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.analyze_broad_version_presence import (
    read_count_rows,
    version_presence_rows,
    write_markdown,
)


class BroadVersionPresenceTests(unittest.TestCase):
    def test_presence_rows_group_term_by_corpus_hits(self) -> None:
        rows = version_presence_rows(
            [
                row("modern", "trump_g", "TR_NT", "38"),
                row("modern", "trump_g", "SBLGNT", "0"),
                row("modern", "trump_g", "BYZ_NT", "41"),
            ]
        )

        self.assertEqual(rows[0]["term_id"], "trump_g")
        self.assertEqual(rows[0]["present_corpora"], "BYZ_NT,TR_NT")
        self.assertEqual(rows[0]["absent_corpora"], "SBLGNT")
        self.assertEqual(rows[0]["observed_corpus_count"], 3)
        self.assertEqual(rows[0]["presence_scope"], "present_multiple_sources")
        self.assertEqual(rows[0]["total_hits"], 79)

    def test_absent_all_observed_sources_is_explicit(self) -> None:
        rows = version_presence_rows(
            [
                row("modern", "catering_g", "TR_NT", "0", length="9"),
                row("modern", "catering_g", "SBLGNT", "0", length="9"),
            ]
        )

        self.assertEqual(rows[0]["presence_scope"], "absent_all_observed_sources")
        self.assertEqual(rows[0]["read"], "absent at this range")

    def test_single_compatible_corpus_read_is_explicit(self) -> None:
        rows = version_presence_rows(
            [row("modern", "trump_h", "MT_WLC", "4", length="5")]
        )

        self.assertEqual(rows[0]["presence_scope"], "present_all_observed_sources")
        self.assertEqual(rows[0]["read"], "present in only compatible corpus")

    def test_read_count_rows_ignores_generated_top_counts(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_count_csv(root / "modern_names_dates_counts.csv", "trump_h")
            (root / "modern_names_dates_counts.manifest.json").write_text("{}", encoding="utf-8")
            write_count_csv(root / "wide_focus_top_counts.csv", "noise")

            rows = read_count_rows(root)

        self.assertEqual([row["term_id"] for row in rows], ["trump_h"])

    def test_markdown_displays_transliteration_and_english_gloss(self) -> None:
        with TemporaryDirectory() as tmp:
            rows = version_presence_rows(
                [row("modern", "trump_h", "MT_WLC", "4", term_language="hebrew", term="טראמפ")]
            )
            path = Path(tmp) / "presence.md"

            write_markdown(path, rows, object())

            text = path.read_text(encoding="utf-8")
        self.assertIn("`טראמפ` (trmp; English: Trump)", text)


def row(
    term_set: str,
    term_id: str,
    corpus: str,
    hits: str,
    *,
    length: str = "5",
    term_language: str = "greek",
    term: str = "τραμπ",
) -> dict[str, str]:
    return {
        "term_set": term_set,
        "term_id": term_id,
        "concept": "Trump",
        "category": "modern_names",
        "term_language": term_language,
        "normalized_term": term,
        "normalized_length": length,
        "corpus": corpus,
        "hit_count": hits,
    }


def write_count_csv(path: Path, term_id: str) -> None:
    path.write_text(
        "corpus,term_id,concept,category,term_language,normalized_term,normalized_length,hit_count,status\n"
        f"MT_WLC,{term_id},Trump,modern,hebrew,טראמפ,5,1,counted\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
