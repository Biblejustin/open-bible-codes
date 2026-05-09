import csv
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from els.cli import FIELDNAMES, main
from els.corpus import Corpus, VerseSpan, WordSpan
from els.extensions import build_extension_lexicon, extension_score, extensions_for_hit
from els.search import find_els


def sample_corpus() -> Corpus:
    verse = VerseSpan(
        "test",
        "Test 1:1",
        "Test",
        "1",
        "1",
        "αβ γδ εζ",
        0,
        5,
        6,
    )
    words = (
        WordSpan("test", "Test 1:1", "Test", "1", "1", 1, "αβ", "αβ", 0, 1, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 2, "γδ", "γδ", 2, 3, 2),
        WordSpan("test", "Test 1:1", "Test", "1", "1", 3, "εζ", "εζ", 4, 5, 2),
    )
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text="αβγδεζ",
        verses=(verse,),
        position_to_verse=tuple(0 for _ in range(6)),
        words=words,
        position_to_word=(0, 0, 1, 1, 2, 2),
    )


class ExtensionTests(unittest.TestCase):
    def test_extension_score_supports_standard_and_all_codes_scales(self) -> None:
        self.assertEqual(
            extension_score("before_plus_term_plus_after", 3, "phrase_3", 4),
            3314,
        )
        self.assertEqual(
            extension_score(
                "before_plus_term",
                2,
                "phrase_2+word",
                6,
                high_priority_scale=True,
            ),
            302016,
        )

    def test_extensions_find_words_and_phrases_on_same_skip_lane(self) -> None:
        corpus = sample_corpus()
        hit = list(
            find_els(
                corpus,
                "γδ",
                min_skip=1,
                max_skip=1,
                direction="forward",
            )
        )[0]
        lexicon = build_extension_lexicon(corpus, max_phrase_words=3)

        matches = extensions_for_hit(
            corpus,
            hit,
            lexicon,
            max_before=2,
            max_after=2,
            include_both_sided=True,
        )
        by_type = {match.extension_type: match for match in matches}

        self.assertEqual(by_type["before_match"].extended_sequence, "αβ")
        self.assertEqual(by_type["before_match"].match_kind, "word")
        self.assertEqual(by_type["after_match"].extended_sequence, "εζ")
        self.assertEqual(by_type["before_plus_term"].extended_sequence, "αβγδ")
        self.assertEqual(by_type["before_plus_term"].match_kind, "phrase_2")
        self.assertEqual(by_type["term_plus_after"].extended_sequence, "γδεζ")
        self.assertEqual(
            by_type["before_plus_term_plus_after"].extended_sequence,
            "αβγδεζ",
        )
        self.assertEqual(by_type["before_plus_term_plus_after"].match_kind, "phrase_3")

    def test_extensions_can_be_capped_per_hit(self) -> None:
        corpus = sample_corpus()
        hit = list(find_els(corpus, "γδ", min_skip=1, max_skip=1))[0]
        lexicon = build_extension_lexicon(corpus, max_phrase_words=3)

        matches = extensions_for_hit(
            corpus,
            hit,
            lexicon,
            max_before=2,
            max_after=2,
            include_both_sided=True,
            max_extensions=2,
        )

        self.assertEqual(len(matches), 2)

    def test_extensions_cli_writes_matches(self) -> None:
        corpus = sample_corpus()
        hit = list(find_els(corpus, "γδ", min_skip=1, max_skip=1))[0]

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_path = root / "greek.csv"
            config_path = root / "config.toml"
            hits_path = root / "hits.csv"
            out_path = root / "extensions.csv"
            summary_path = root / "extension_summary.csv"
            top_path = root / "extension_top.csv"
            manifest_path = root / "extension_summary.manifest.json"
            filtered_summary_path = root / "extension_summary_filtered.csv"
            filtered_top_path = root / "extension_top_filtered.csv"
            filtered_manifest_path = root / "extension_summary_filtered.manifest.json"
            excluded_summary_path = root / "extension_summary_excluded.csv"
            excluded_top_path = root / "extension_top_excluded.csv"
            excluded_manifest_path = root / "extension_summary_excluded.manifest.json"

            data_path.write_text(
                "ref,book,chapter,verse,text\n"
                "Test 1:1,Test,1,1,αβ γδ εζ\n",
                encoding="utf-8",
            )
            config_path.write_text(
                "\n".join(
                    [
                        'name = "Test"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "Test"',
                        'format = "csv"',
                        f'path = "{data_path}"',
                        'text_column = "text"',
                        'ref_column = "ref"',
                        'book_column = "book"',
                        'chapter_column = "chapter"',
                        'verse_column = "verse"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            with hits_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
                writer.writeheader()
                writer.writerow(hit.as_row())

            with mock.patch.dict(os.environ, {"EDLS_NO_CORPUS_CACHE": "1"}):
                self.assertEqual(
                    main(
                        [
                            "extensions",
                            "--config",
                            str(config_path),
                            "--hits",
                            str(hits_path),
                            "--max-before",
                            "2",
                            "--max-after",
                            "2",
                            "--include-both-sided",
                            "--out",
                            str(out_path),
                        ]
                    ),
                    0,
                )

            with out_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(
                main(
                    [
                        "extension-summary",
                        "--extensions",
                        str(out_path),
                        "--top",
                        "10",
                        "--out",
                        str(summary_path),
                        "--top-out",
                        str(top_path),
                        "--manifest-out",
                        str(manifest_path),
                    ]
                ),
                0,
            )
            with summary_path.open("r", encoding="utf-8", newline="") as handle:
                summary_rows = list(csv.DictReader(handle))
            with top_path.open("r", encoding="utf-8", newline="") as handle:
                top_rows = list(csv.DictReader(handle))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(
                main(
                    [
                        "extension-summary",
                        "--extensions",
                        str(out_path),
                        "--min-term-length",
                        "2",
                        "--match-kind-prefix",
                        "phrase_",
                        "--exclude-term",
                        "missing",
                        "--out",
                        str(filtered_summary_path),
                        "--top-out",
                        str(filtered_top_path),
                        "--manifest-out",
                        str(filtered_manifest_path),
                    ]
                ),
                0,
            )
            with filtered_top_path.open("r", encoding="utf-8", newline="") as handle:
                filtered_top_rows = list(csv.DictReader(handle))
            filtered_manifest = json.loads(
                filtered_manifest_path.read_text(encoding="utf-8")
            )
            self.assertEqual(
                main(
                    [
                        "extension-summary",
                        "--extensions",
                        str(out_path),
                        "--exclude-term",
                        "γδ",
                        "--out",
                        str(excluded_summary_path),
                        "--top-out",
                        str(excluded_top_path),
                        "--manifest-out",
                        str(excluded_manifest_path),
                    ]
                ),
                0,
            )
            excluded_manifest = json.loads(
                excluded_manifest_path.read_text(encoding="utf-8")
            )

        self.assertGreaterEqual(len(rows), 5)
        self.assertIn(
            "before_plus_term_plus_after",
            {row["extension_type"] for row in rows},
        )
        self.assertGreaterEqual(len(summary_rows), 1)
        self.assertGreaterEqual(len(top_rows), 1)
        self.assertIn(
            "before_plus_term_plus_after",
            {row["extension_type"] for row in top_rows},
        )
        self.assertEqual(manifest["input_rows"], len(rows))
        self.assertEqual(manifest["kept_rows"], len(rows))
        self.assertTrue(filtered_top_rows)
        self.assertTrue(
            all(row["match_kind"].startswith("phrase_") for row in filtered_top_rows)
        )
        self.assertGreater(filtered_manifest["filtered_match_kind_rows"], 0)
        self.assertEqual(excluded_manifest["kept_rows"], 0)
        self.assertEqual(excluded_manifest["filtered_excluded_term_rows"], len(rows))

    def test_extensions_cli_filters_labeled_hit_rows(self) -> None:
        hit = list(find_els(sample_corpus(), "γδ", min_skip=1, max_skip=1))[0]

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_path = root / "greek.csv"
            config_path = root / "config.toml"
            hits_path = root / "hits.csv"
            out_path = root / "extensions.csv"
            manifest_path = root / "extensions.manifest.json"

            data_path.write_text(
                "ref,book,chapter,verse,text\n"
                "Test 1:1,Test,1,1,αβ γδ εζ\n",
                encoding="utf-8",
            )
            config_path.write_text(
                "\n".join(
                    [
                        'name = "Test"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "Test"',
                        'format = "csv"',
                        f'path = "{data_path}"',
                        'text_column = "text"',
                        'ref_column = "ref"',
                        'book_column = "book"',
                        'chapter_column = "chapter"',
                        'verse_column = "verse"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            with hits_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["corpus", *FIELDNAMES])
                writer.writeheader()
                for corpus_label in ("A", "B"):
                    row = {"corpus": corpus_label}
                    row.update(hit.as_row())
                    writer.writerow(row)

            with mock.patch.dict(os.environ, {"EDLS_NO_CORPUS_CACHE": "1"}):
                self.assertEqual(
                    main(
                        [
                            "extensions",
                            "--config",
                            str(config_path),
                            "--hits",
                            str(hits_path),
                            "--corpus-label",
                            "A",
                            "--max-before",
                            "2",
                            "--max-after",
                            "2",
                            "--out",
                            str(out_path),
                            "--manifest-out",
                            str(manifest_path),
                        ]
                    ),
                    0,
                )

            with out_path.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

        self.assertTrue(rows)
        self.assertEqual({row["corpus"] for row in rows}, {"A"})
        self.assertEqual(manifest["input_hit_count"], 2)
        self.assertEqual(manifest["hit_count"], 1)
        self.assertEqual(manifest["skipped_hit_count"], 1)


if __name__ == "__main__":
    unittest.main()
