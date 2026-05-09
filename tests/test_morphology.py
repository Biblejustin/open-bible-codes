import tempfile
import unittest
from pathlib import Path

from els.morphology import (
    count_morph_tokens,
    lexical_oshb_lemma,
    lexical_oshb_morph,
    read_morphgnt_tokens,
)


class MorphologyTests(unittest.TestCase):
    def test_oshb_lexical_segment(self) -> None:
        self.assertEqual(lexical_oshb_lemma("b/7225"), "7225")
        self.assertEqual(lexical_oshb_morph("HTd/Ncmpa"), "Ncmpa")

    def test_read_morphgnt_tokens_and_count_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "61-Mt-morphgnt.txt").write_text(
                "\n".join(
                    [
                        "010101 N- ----NSF- Βίβλος Βίβλος βίβλος βίβλος",
                        "010101 RA ----GSN- τοῦ τοῦ τοῦ ὁ",
                        "010101 V- 3AAI-S-- ἐγέννησεν ἐγέννησεν ἐγέννησε(ν) γεννάω",
                    ]
                ),
                encoding="utf-8",
            )
            tokens = read_morphgnt_tokens(root)
        self.assertEqual(tokens[0].ref, "Matt 1:1")
        self.assertEqual(tokens[0].pos, "noun")
        self.assertEqual(tokens[2].pos, "verb")

        bundle = count_morph_tokens(tokens)

        self.assertEqual(bundle.by_lemma[("noun", "βιβλοσ")], 1)
        self.assertEqual(bundle.by_lemma[("verb", "γενναω")], 1)
        self.assertNotIn(("article", "ο"), bundle.by_lemma)


if __name__ == "__main__":
    unittest.main()
