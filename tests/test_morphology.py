import tempfile
import unittest
from collections import Counter
from pathlib import Path

from els.morphology import (
    count_morph_tokens,
    format_multiples,
    hebrew_pos,
    lexical_oshb_lemma,
    lexical_oshb_morph,
    preferred_display,
    preferred_word,
    read_morphgnt_tokens,
    read_oshb_tokens,
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
        # the bundle also keeps display examples and back-references
        self.assertEqual(bundle.display_lemmas["βιβλοσ"].most_common(1)[0][0], "βίβλος")
        self.assertIn("Matt 1:1", bundle.verse_refs[("noun", "βιβλοσ")])
        self.assertIn("Matt", bundle.book_refs[("verb", "γενναω")])

    def test_read_oshb_tokens_parses_osis_words(self) -> None:
        osis = (
            '<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace">'
            '<verse osisID="Gen.1.1">'
            '<w lemma="b/7225" morph="HR/Ncfsa">בְּרֵאשִׁית</w>'
            '<w lemma="1254 a" morph="HVqp3ms">בָּרָא</w>'
            "</verse>"
            '<verse osisID="Gen.1"/>'
            "</osis>"
        )
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Gen.xml").write_text(osis, encoding="utf-8")
            tokens = read_oshb_tokens(root)

        # the malformed two-part osisID contributes nothing
        self.assertEqual(len(tokens), 2)
        first, second = tokens
        self.assertEqual(first.ref, "Gen 1:1")
        self.assertEqual(first.lemma, "7225")        # prefix segment dropped
        self.assertEqual(first.pos, "noun")           # lexical morph Ncfsa
        self.assertEqual(second.lemma, "1254")        # homograph letter dropped
        self.assertEqual(second.pos, "verb")          # HVqp3ms -> V
        self.assertEqual(second.normalized_word, "ברא")  # points stripped

    def test_hebrew_pos_codes(self) -> None:
        self.assertEqual(hebrew_pos("HNcmsa"), "noun")     # H prefix: second char
        self.assertEqual(hebrew_pos("Vqp3ms"), "verb")     # bare: first char
        self.assertEqual(hebrew_pos("HC"), "conjunction")
        self.assertEqual(hebrew_pos(""), "")
        self.assertEqual(hebrew_pos("Z"), "Z")             # unknown code passes through

    def test_preferred_display_and_word_pick_most_common(self) -> None:
        displays = {"βιβλοσ": Counter({"βίβλος": 3, "Βίβλος": 1})}
        self.assertEqual(preferred_display(displays, "βιβλοσ"), "βίβλος")
        self.assertEqual(preferred_display(displays, "missing"), "")
        words = {("noun", "βιβλοσ"): Counter({"Βίβλος": 2})}
        self.assertEqual(preferred_word(words, "noun", "βιβλοσ"), "Βίβλος")
        self.assertEqual(preferred_word(words, "verb", "βιβλοσ"), "")

    def test_format_multiples_renders_matching_divisors(self) -> None:
        self.assertEqual(format_multiples(14), "7")      # of (3, 7, 12, 40, 70)
        self.assertEqual(format_multiples(21), "3;7")
        self.assertEqual(format_multiples(13), "")
        self.assertEqual(format_multiples(0), "")


if __name__ == "__main__":
    unittest.main()
