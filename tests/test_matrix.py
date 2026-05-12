import csv
import tempfile
import unittest
from pathlib import Path

from els.cli import hit_from_row, hit_with_corpus_center, main
from els.corpus import Corpus, VerseSpan
from els.matrix import (
    cell_relation,
    chebyshev_cell_distance,
    closest_cell_pair,
    hit_matrix_cells,
    hit_offsets,
    matrix_cell,
    matrix_letters,
    matrix_summary,
)
from els.search import ELSHit


def sample_hit(skip: int = 5) -> ELSHit:
    if skip > 0:
        start, end = 2, 12
    else:
        start, end = 12, 2
    return ELSHit(
        term="abc",
        normalized_term="abc",
        skip=skip,
        start_offset=start,
        end_offset=end,
        span_letters=11,
        sequence="abc",
        start_ref="Test 1:1",
        end_ref="Test 1:1",
        start_source="test",
        end_source="test",
        center_offset=7,
        center_ref="Test 1:1",
        center_source="test",
        center_word_index="",
        center_word="",
        center_normalized_word="",
    )


def sample_corpus() -> Corpus:
    text = "abcdefghijklmnop"
    return Corpus(
        name="test",
        language="greek",
        keep_hebrew_final_forms=False,
        text=text,
        verses=(
            VerseSpan("test", "Test 1:1", "Test", "1", "1", text, 0, len(text) - 1, len(text)),
        ),
        position_to_verse=tuple(0 for _char in text),
    )


class MatrixTests(unittest.TestCase):
    def test_hit_offsets_follow_reading_order(self) -> None:
        self.assertEqual(hit_offsets(sample_hit(5)), (2, 7, 12))
        self.assertEqual(hit_offsets(sample_hit(-5)), (12, 7, 2))

    def test_matrix_letters_default_to_skip_width(self) -> None:
        hit = sample_hit(5)
        letters = matrix_letters(sample_corpus(), hit, hit_index=1)
        summary = matrix_summary(hit, letters)

        self.assertEqual([(letter.row, letter.col) for letter in letters], [(0, 2), (1, 2), (2, 2)])
        self.assertEqual([letter.letter for letter in letters], ["a", "b", "c"])
        self.assertEqual(summary.row_width, 5)
        self.assertEqual(summary.rows_spanned, 3)
        self.assertEqual(summary.cols_spanned, 1)

    def test_matrix_cell_helpers_compute_distance(self) -> None:
        hit = sample_hit(5)

        self.assertEqual(matrix_cell(12, 5), (2, 2))
        self.assertEqual(hit_matrix_cells(hit), ((0, 2), (1, 2), (2, 2)))
        self.assertEqual(chebyshev_cell_distance((1, 2), (3, 4)), 2)
        self.assertEqual(cell_relation((1, 2), (1, 2)), "same_cell")
        self.assertEqual(cell_relation((1, 2), (1, 4)), "orthogonal")
        self.assertEqual(cell_relation((1, 2), (3, 4)), "diagonal")
        self.assertEqual(cell_relation((1, 2), (2, 4)), "neighborhood")
        self.assertEqual(
            closest_cell_pair(((0, 0), (5, 5)), ((2, 1), (6, 6))),
            (1, (5, 5), (6, 6)),
        )

    def test_cli_matrix_exports_letter_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.csv"
            config = root / "corpus.toml"
            hits = root / "hits.csv"
            matrix = root / "matrix.csv"
            summary = root / "summary.csv"
            source.write_text(
                "ref,book,chapter,verse,text\n"
                "Test 1:1,Test,1,1,αβγδεζηθικλ\n",
                encoding="utf-8",
            )
            config.write_text(
                "\n".join(
                    [
                        'name = "test"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'format = "csv"',
                        f'path = "{source}"',
                        'text_column = "text"',
                        'ref_column = "ref"',
                        'book_column = "book"',
                        'chapter_column = "chapter"',
                        'verse_column = "verse"',
                    ]
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                main(
                    [
                        "search",
                        "--config",
                        str(config),
                        "--term",
                        "αζλ",
                        "--min-skip",
                        "5",
                        "--max-skip",
                        "5",
                        "--direction",
                        "forward",
                        "--out",
                        str(hits),
                    ]
                ),
                0,
            )
            self.assertEqual(
                main(
                    [
                        "matrix",
                        "--config",
                        str(config),
                        "--hits",
                        str(hits),
                        "--out",
                        str(matrix),
                        "--summary-out",
                        str(summary),
                    ]
                ),
                0,
            )

            with matrix.open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            with summary.open("r", encoding="utf-8", newline="") as handle:
                summary_rows = list(csv.DictReader(handle))

        self.assertEqual([row["letter"] for row in rows], ["α", "ζ", "λ"])
        self.assertEqual([row["col"] for row in rows], ["0", "0", "0"])
        self.assertEqual(summary_rows[0]["rows_spanned"], "3")
        self.assertEqual(summary_rows[0]["cols_spanned"], "1")

    def test_legacy_hit_rows_compute_center_offset(self) -> None:
        hit = hit_from_row(
            {
                "term": "abc",
                "normalized_term": "abc",
                "skip": "5",
                "start_offset": "2",
                "end_offset": "12",
                "span_letters": "11",
                "sequence": "abc",
                "start_ref": "Test 1:1",
                "end_ref": "Test 1:1",
                "start_source": "test",
                "end_source": "test",
            }
        )

        self.assertEqual(hit.center_offset, 7)
        self.assertEqual(hit.center_ref, "")

        enriched = hit_with_corpus_center(sample_corpus(), hit)
        self.assertEqual(enriched.center_ref, "Test 1:1")


if __name__ == "__main__":
    unittest.main()
