import tempfile
import unittest
from pathlib import Path

from els.corpus import load_corpus
from els.critical import classify_missing_verses


class CriticalTests(unittest.TestCase):
    def test_ebible_book_codes_map_to_sbl_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "tr.csv").write_text(
                "\n".join(
                    [
                        "ref,book,chapter,verse,text",
                        "MAT 1:1,MAT,1,1,Βίβλος γενέσεως",
                        "MRK 16:9,MRK,16,9,Ἀναστὰς δὲ",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "sbl.csv").write_text(
                "\n".join(
                    [
                        "ref,book,chapter,verse,text",
                        "Matt 1:1,Matt,1,1,Βίβλος γενέσεως",
                    ]
                ),
                encoding="utf-8",
            )
            tr_config = _write_config(root, "tr", "tr.csv")
            sbl_config = _write_config(root, "sbl", "sbl.csv")
            tr = load_corpus(tr_config)
            sbl = load_corpus(sbl_config)

        omitted = classify_missing_verses(tr, sbl)

        self.assertEqual([block.ref for block in omitted], ["MRK 16:9"])


def _write_config(root: Path, name: str, csv_name: str) -> Path:
    path = root / f"{name}.toml"
    path.write_text(
        "\n".join(
            [
                f'name = "{name}"',
                'language = "greek"',
                "",
                "[[sources]]",
                f'name = "{name}"',
                'format = "csv"',
                f'path = "{csv_name}"',
                'text_column = "text"',
                'ref_column = "ref"',
                'book_column = "book"',
                'chapter_column = "chapter"',
                'verse_column = "verse"',
            ]
        ),
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    unittest.main()
