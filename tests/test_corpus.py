import os
import tempfile
import unittest
from array import array
from pathlib import Path

from els.corpus import (
    Corpus,
    VerseSpan,
    _normalize_ref_number,
    _split_osis_ref,
    load_corpus,
    source_files_for_cache,
    splice_verses_into_corpus,
)


class CorpusTests(unittest.TestCase):
    def test_michigan_ref_numbers_are_rtl_encoded(self) -> None:
        self.assertEqual(_normalize_ref_number("61"), "16")
        self.assertEqual(_normalize_ref_number("03"), "30")
        self.assertEqual(_normalize_ref_number("7"), "7")

    def test_osis_ref_split(self) -> None:
        self.assertEqual(_split_osis_ref("Gen.1.1"), ("Gen", "1", "1"))

    def test_loader_maps_positions_to_words(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.txt").write_text("Ἰησοῦς Χριστός.", encoding="utf-8")
            (root / "sample.toml").write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "sample.txt"',
                        'ref = "Sample 1:1"',
                        'book = "Sample"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            corpus = load_corpus(root / "sample.toml")

        self.assertEqual(corpus.text, "ιησουσχριστοσ")
        self.assertIsInstance(corpus.position_to_verse, array)
        self.assertIsInstance(corpus.position_to_word, array)
        self.assertEqual(len(corpus.words), 2)
        self.assertEqual(corpus.word_at(0).raw_word, "Ἰησοῦς")
        self.assertEqual(corpus.word_at(6).raw_word, "Χριστός.")
        self.assertEqual(corpus.word_at(6).normalized_word, "χριστοσ")

    def test_loader_cache_invalidates_when_source_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cache_dir = root / "cache"
            source = root / "sample.txt"
            config = root / "sample.toml"
            source.write_text("Ἰησοῦς", encoding="utf-8")
            config.write_text(
                "\n".join(
                    [
                        'name = "sample"',
                        'language = "greek"',
                        "",
                        "[[sources]]",
                        'name = "sample"',
                        'format = "text"',
                        'path = "sample.txt"',
                        'ref = "Sample 1:1"',
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            prior_cache_dir = os.environ.get("EDLS_CORPUS_CACHE_DIR")
            os.environ["EDLS_CORPUS_CACHE_DIR"] = str(cache_dir)
            try:
                first = load_corpus(config)
                source.write_text("Χριστός", encoding="utf-8")
                next_mtime = source.stat().st_mtime_ns + 1_000_000_000
                os.utime(source, ns=(next_mtime, next_mtime))
                second = load_corpus(config)
            finally:
                if prior_cache_dir is None:
                    os.environ.pop("EDLS_CORPUS_CACHE_DIR", None)
                else:
                    os.environ["EDLS_CORPUS_CACHE_DIR"] = prior_cache_dir

            self.assertEqual(first.text, "ιησουσ")
            self.assertEqual(second.text, "χριστοσ")
            self.assertEqual(len(list(cache_dir.glob("*.pickle"))), 2)

    def test_splice_verses_inserts_donor_refs_in_donor_order(self) -> None:
        base = _toy_corpus(
            "base",
            [
                ("B", "MAT 1:1", "MAT", "1", "1", "αα"),
                ("B", "MAT 1:3", "MAT", "1", "3", "γγ"),
            ],
        )
        donor = _toy_corpus(
            "donor",
            [
                ("D", "MAT 1:1", "MAT", "1", "1", "xx"),
                ("D", "MAT 1:2", "MAT", "1", "2", "ββ"),
                ("D", "MAT 1:3", "MAT", "1", "3", "yy"),
            ],
        )

        spliced = splice_verses_into_corpus(base, donor, ["MAT 1:2"])

        self.assertEqual(spliced.text, "ααββγγ")
        self.assertEqual([verse.ref for verse in spliced.verses], ["MAT 1:1", "MAT 1:2", "MAT 1:3"])
        self.assertEqual([verse.source for verse in spliced.verses], ["B", "D", "B"])
        self.assertEqual(
            [spliced.ref_at(i) for i in range(len(spliced.text))],
            ["MAT 1:1"] * 2 + ["MAT 1:2"] * 2 + ["MAT 1:3"] * 2,
        )

    def test_splice_verses_maps_sbl_book_codes_to_ebible_donor_order(self) -> None:
        base = _toy_corpus(
            "sbl",
            [
                ("B", "Matt 1:1", "Matt", "1", "1", "αα"),
                ("B", "Matt 1:3", "Matt", "1", "3", "γγ"),
            ],
        )
        donor = _toy_corpus(
            "tr",
            [
                ("D", "MAT 1:1", "MAT", "1", "1", "xx"),
                ("D", "MAT 1:2", "MAT", "1", "2", "ββ"),
                ("D", "MAT 1:3", "MAT", "1", "3", "yy"),
            ],
        )

        spliced = splice_verses_into_corpus(base, donor, ["MAT 1:2"])

        self.assertEqual(spliced.text, "ααββγγ")
        self.assertEqual([verse.ref for verse in spliced.verses], ["Matt 1:1", "MAT 1:2", "Matt 1:3"])

    def test_uxlc_loader_uses_ketiv_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            books = root / "books"
            books.mkdir()
            (books / "Genesis.xml").write_text(
                """<?xml version="1.0" encoding="UTF-8"?>
<Tanach>
  <tanach>
    <book>
      <names><name>Genesis</name><abbrev>Gen</abbrev></names>
      <c n="8">
        <v n="17">
          <w>הָאָ֖רֶץ</w>
          <k>הוצא</k>
          <q>הַיְצֵ֣א</q>
        </v>
      </c>
    </book>
  </tanach>
</Tanach>
""",
                encoding="utf-8",
            )
            (root / "uxlc.toml").write_text(
                "\n".join(
                    [
                        'name = "UXLC sample"',
                        'language = "hebrew"',
                        "",
                        "[[sources]]",
                        'name = "UXLC"',
                        'format = "uxlc_dir"',
                        'path = "books"',
                    ]
                ),
                encoding="utf-8",
            )

            corpus = load_corpus(root / "uxlc.toml")

        self.assertEqual(corpus.verses[0].ref, "Gen 8:17")
        self.assertEqual(corpus.verses[0].book, "Genesis")
        self.assertIn("הוצא", corpus.verses[0].raw_text)
        self.assertNotIn("הַיְצֵ֣א", corpus.verses[0].raw_text)
        self.assertEqual(corpus.text, "הארצהוצא")

    def test_uxlc_loader_can_use_qere(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            books = root / "books"
            books.mkdir()
            (books / "Genesis.xml").write_text(
                """<?xml version="1.0" encoding="UTF-8"?>
<Tanach>
  <tanach>
    <book>
      <names><name>Genesis</name><abbrev>Gen</abbrev></names>
      <c n="8"><v n="17"><w>ארץ</w><k>הוצא</k><q>היצא</q></v></c>
    </book>
  </tanach>
</Tanach>
""",
                encoding="utf-8",
            )
            (root / "uxlc.toml").write_text(
                "\n".join(
                    [
                        'name = "UXLC sample"',
                        'language = "hebrew"',
                        "",
                        "[[sources]]",
                        'name = "UXLC"',
                        'format = "uxlc_dir"',
                        'path = "books"',
                        'qere_mode = "qere"',
                    ]
                ),
                encoding="utf-8",
            )

            corpus = load_corpus(root / "uxlc.toml")

        self.assertEqual(corpus.text, "ארצהיצא")

    def test_oshb_loader_ignores_notes_and_qere_readings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            books = root / "wlc"
            books.mkdir()
            (books / "Gen.xml").write_text(
                """<?xml version="1.0" encoding="UTF-8"?>
<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace">
  <osisText>
    <div>
      <chapter osisID="Gen.1">
        <verse osisID="Gen.1.1">
          <w lemma="7225">בְּרֵאשִׁ֖ית</w>
          <note type="alternative"><rdg type="x-accent">בְּרֵאשִׁ֜ית</rdg></note>
          <w type="x-ketiv">הוצא</w>
          <note type="variant"><rdg type="x-qere"><w>הַיְצֵ֣א</w></rdg></note>
        </verse>
      </chapter>
    </div>
  </osisText>
</osis>
""",
                encoding="utf-8",
            )
            (root / "oshb.toml").write_text(
                "\n".join(
                    [
                        'name = "OSHB sample"',
                        'language = "hebrew"',
                        "",
                        "[[sources]]",
                        'name = "OSHB"',
                        'format = "oshb_wlc_dir"',
                        'path = "wlc"',
                    ]
                ),
                encoding="utf-8",
            )

            corpus = load_corpus(root / "oshb.toml")

        self.assertEqual(corpus.text, "בראשיתהוצא")
        self.assertNotIn("הַיְצֵ֣א", corpus.verses[0].raw_text)

    def test_mam_loader_reads_only_verse_text_column(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            books = root / "mam"
            books.mkdir()
            (books / "A1-Genesis.html").write_text(
                """<!doctype html>
<html>
<head><title>MAM with doc: Genesis</title></head>
<body>
<table>
<tr>
<td id="c1v1">א:</td>
<td><span>בְּרֵאשִׁ֖ית</span> בָּרָ֣א אֱלֹהִ֑ים<wbr>׃</td>
<td><span>דוקומנטציה</span> הערת מסורה</td>
</tr>
</table>
</body>
</html>
""",
                encoding="utf-8",
            )
            (root / "mam.toml").write_text(
                "\n".join(
                    [
                        'name = "MAM sample"',
                        'language = "hebrew"',
                        "",
                        "[[sources]]",
                        'name = "MAM"',
                        'format = "mam_html_dir"',
                        'path = "mam"',
                    ]
                ),
                encoding="utf-8",
            )

            corpus = load_corpus(root / "mam.toml")

        self.assertEqual(corpus.verses[0].ref, "Gen 1:1")
        self.assertEqual(corpus.verses[0].book, "Genesis")
        self.assertEqual(corpus.text, "בראשיתבראאלהימ")
        self.assertNotIn("דוקומנטציה", corpus.verses[0].raw_text)

    def test_mam_loader_keeps_canonical_book_name_for_short_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            books = root / "mam"
            books.mkdir()
            (books / "A3-Levit.html").write_text(
                """<!doctype html>
<html>
<head><title>MAM with doc: Levit</title></head>
<body>
<table>
<tr><td id="c1v1">א:</td><td>וַיִּקְרָ֖א</td><td>doc note</td></tr>
</table>
</body>
</html>
""",
                encoding="utf-8",
            )
            (root / "mam.toml").write_text(
                "\n".join(
                    [
                        'name = "MAM sample"',
                        'language = "hebrew"',
                        "",
                        "[[sources]]",
                        'name = "MAM"',
                        'format = "mam_html_dir"',
                        'path = "mam"',
                    ]
                ),
                encoding="utf-8",
            )

            corpus = load_corpus(root / "mam.toml")

        self.assertEqual(corpus.verses[0].ref, "Lev 1:1")
        self.assertEqual(corpus.verses[0].book, "Leviticus")

    def test_directory_source_cache_files_track_source_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Genesis.xml").write_text("<xml />", encoding="utf-8")
            (root / "Exodus.xml").write_text("<xml />", encoding="utf-8")
            (root / "notes.txt").write_text("ignore", encoding="utf-8")

            self.assertEqual(
                [path.name for path in source_files_for_cache(root, "uxlc_dir")],
                ["Exodus.xml", "Genesis.xml"],
            )

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "A1-Genesis.html").write_text("<html></html>", encoding="utf-8")
            (root / "sigil-decoding.html").write_text("<html></html>", encoding="utf-8")

            self.assertEqual(
                [path.name for path in source_files_for_cache(root, "mam_html_dir")],
                ["A1-Genesis.html"],
            )


def _toy_corpus(name: str, rows: list[tuple[str, str, str, str, str, str]]) -> Corpus:
    verses: list[VerseSpan] = []
    letters: list[str] = []
    position_to_verse: list[int] = []
    for source, ref, book, chapter, verse_num, text in rows:
        start = len(letters)
        verse_index = len(verses)
        letters.extend(text)
        position_to_verse.extend([verse_index] * len(text))
        verses.append(
            VerseSpan(
                source,
                ref,
                book,
                chapter,
                verse_num,
                text,
                start,
                len(letters) - 1,
                len(text),
            )
        )
    return Corpus(
        name=name,
        language="greek",
        keep_hebrew_final_forms=False,
        text="".join(letters),
        verses=tuple(verses),
        position_to_verse=array("i", position_to_verse),
    )


if __name__ == "__main__":
    unittest.main()
