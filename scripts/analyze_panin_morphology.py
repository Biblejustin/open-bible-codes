#!/usr/bin/env python3
"""Panin's claims under real published morphology: does his counting hold?

The earlier studies tested Panin's Matthew 1:1-11 numbers at the surface-form
level and could not reach his vocabulary (lemma) and part-of-speech features
without a Greek lemmatizer and tagger. The repository already carries one:
MorphGNT, the SBLGNT tagged with lemma and part of speech for every word
(data/raw/morphgnt). This script uses it, so the test is against a published
morphological analysis, not against any hand-classification of ours.

The result is a vindication of Panin's counting. On the SBLGNT every one of his
Matthew 1:1-11 features reproduces exactly: 49 vocabulary words, 28 vowel-initial
and 21 consonant-initial, 266 letters with 140 vowels and 126 consonants, 35
recurring and 14 once, 7 in more than one form and 42 in one, 42 nouns and 7 not,
and 28 male ancestors of the Christ (he even excludes Zerah, named in the line
but not of it). The only seam is proper versus common nouns, 36 to 6 here against
his 35 to 7, which is just whether Christos is a name or a title. His other
passage vocabularies land within one. So Panin counted accurately; he was not
fudging arithmetic.

What this does NOT rescue is the inference. The accuracy of a chosen basket of
counts is not evidence of design once you see (see analyze_panin_claims and
analyze_panin_passages) that the features are selected from an inexhaustible set,
that a neutral panel finds no excess of sevens, and that the structure is not
load-bearing. And one figure is text-bound: the genealogy's vocabulary gematria
is 42,364 on Panin's Westcott-Hort text, a multiple of seven, but 42,452 on the
SBLGNT, which is not. Accurate counting of selected, text-specific features still
does not prove inspiration.

Outputs under reports/panin_morphology/.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els.morphology import read_morphgnt_tokens
from els.normalization import normalize_greek
from els.textstats import GREEK_VOWELS, GRK_ISOPSEPHY, gematria, is_heptad

MORPHGNT_DIR = Path("data/raw/morphgnt/sblgnt")
OUT_DIR = Path("reports/panin_morphology")

# Proper names in Matthew 1:1-11 that are not male ancestors of the Christ:
# three women (Tamar, Rahab, Ruth), Uriah (Bathsheba's husband, not in the line),
# Zerah (Perez's brother, named but not an ancestor), the place Babylon, and the
# two names of the subject himself (Jesus, Christ). Documented, not derived.
NON_ANCESTOR_PROPER = {
    "Ἰησοῦς", "Χριστός", "Θαμάρ", "Ῥαχάβ", "Ῥούθ", "Οὐρίας", "Βαβυλών", "Ζάρα",
}

# Panin's published Matthew 1:1-11 features (his 1899 pamphlet), each a multiple
# of seven. The two-name proper/common split follows his "Christ is a title" count.
PANIN_1_1_11 = {
    "vocabulary": 49, "vowel_initial": 28, "consonant_initial": 21,
    "letters": 266, "vowels": 140, "consonants": 126,
    "more_than_once": 35, "once": 14, "more_than_one_form": 7, "one_form": 42,
    "nouns": 42, "not_nouns": 7, "proper": 35, "common": 7, "male_ancestors": 28,
}


def passage(tokens, book: str, chapter: int, verses) -> list:
    want = {str(v) for v in verses}
    return [t for t in tokens if t.book == book and t.chapter == str(chapter) and t.verse in want]


def vocab_features(entries: list[tuple[str, str, str]]) -> dict[str, int]:
    """All of Panin's countable features over (lemma, pos, normalized_word) triples.

    The lemma is the dictionary word (capitalized for proper nouns in MorphGNT);
    pos is the part of speech; normalized_word is the inflected surface form.
    """
    forms: dict[str, set[str]] = defaultdict(set)
    freq: dict[str, int] = defaultdict(int)
    pos: dict[str, str] = {}
    for lemma, p, nword in entries:
        forms[lemma].add(nword)
        freq[lemma] += 1
        pos[lemma] = p
    lemmas = list(forms)
    nlem = {l: normalize_greek(l) for l in lemmas}
    letters = sum(len(nlem[l]) for l in lemmas)
    vowels = sum(1 for l in lemmas for c in nlem[l] if c in GREEK_VOWELS)
    nouns = [l for l in lemmas if pos[l] == "noun"]
    proper = [l for l in nouns if l[:1].isupper()]
    vinit = sum(1 for l in lemmas if nlem[l] and nlem[l][0] in GREEK_VOWELS)
    return {
        "vocabulary": len(lemmas),
        "vowel_initial": vinit, "consonant_initial": len(lemmas) - vinit,
        "letters": letters, "vowels": vowels, "consonants": letters - vowels,
        "more_than_once": sum(1 for l in lemmas if freq[l] > 1),
        "once": sum(1 for l in lemmas if freq[l] == 1),
        "more_than_one_form": sum(1 for l in lemmas if len(forms[l]) > 1),
        "one_form": sum(1 for l in lemmas if len(forms[l]) == 1),
        "nouns": len(nouns), "not_nouns": len(lemmas) - len(nouns),
        "proper": len(proper), "common": len(nouns) - len(proper),
        "male_ancestors": len(set(proper) - NON_ANCESTOR_PROPER),
        "gematria": sum(gematria(nlem[l], GRK_ISOPSEPHY) for l in lemmas),
    }


def entries(tokens) -> list[tuple[str, str, str]]:
    return [(t.lemma, t.pos, t.normalized_word) for t in tokens]


def main() -> int:
    toks = read_morphgnt_tokens(MORPHGNT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Matthew 1:1-11, the full feature ledger ----
    feat = vocab_features(entries(passage(toks, "Matt", 1, range(1, 12))))
    ledger = []
    for key, claim in PANIN_1_1_11.items():
        got = feat[key]
        ledger.append({"feature": key, "panin": claim, "morphology": got,
                       "exact": got == claim, "delta": got - claim})
    exact = sum(1 for r in ledger if r["exact"])

    # ---- other passages, vocabulary (lemma) counts ----
    passages = [
        ("Matthew 1:1-17 genealogy", passage(toks, "Matt", 1, range(1, 18)), 72),
        ("Matthew 1:18-25 birth", passage(toks, "Matt", 1, range(18, 26)), 77),
        ("Matthew 2 childhood", passage(toks, "Matt", 2, range(1, 24)), 161),
        ("Matthew 2:1-6", passage(toks, "Matt", 2, range(1, 7)), 56),
        ("Mark 16:9-20 Long Ending", passage(toks, "Mark", 16, range(9, 21)), 98),
    ]
    vocab_rows = []
    for label, tk, panin_vocab in passages:
        vf = vocab_features(entries(tk))
        vocab_rows.append({"passage": label, "panin_vocabulary": panin_vocab,
                           "morphology_vocabulary": vf["vocabulary"],
                           "delta": vf["vocabulary"] - panin_vocab})

    # ---- the one text-bound figure: the genealogy vocabulary gematria ----
    gen17 = vocab_features(entries(passage(toks, "Matt", 1, range(1, 18))))
    gematria_note = {
        "panin_wh_42364": 42364, "panin_wh_divisible_by_7": is_heptad(42364),
        "sblgnt_morphgnt": gen17["gematria"], "sblgnt_divisible_by_7": is_heptad(gen17["gematria"]),
    }

    # ---- write ----
    with (OUT_DIR / "matthew_1_1_11_features.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["feature", "panin", "morphology", "exact", "delta"])
        w.writeheader(); w.writerows(ledger)
    with (OUT_DIR / "passage_vocabularies.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["passage", "panin_vocabulary", "morphology_vocabulary", "delta"])
        w.writeheader(); w.writerows(vocab_rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "panin_morphology",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "MorphGNT (SBLGNT with lemma and part of speech); Panin, Inspiration of the Scriptures (1899)",
        "note": ("Panin counted on Westcott-Hort; MorphGNT is the SBLGNT. The two are "
                 "all but identical in the genealogy, so the lemma and part-of-speech "
                 "features are a fair test of his counting."),
        "matthew_1_1_11_features_exact": f"{exact}/{len(ledger)}",
        "matthew_1_1_11_ledger": ledger,
        "proper_common_note": ("morphology gives 36 proper and 6 common; Panin gives 35 and "
                               "7, the one-word difference being whether Christos is a name "
                               "or a title. It does not affect the 28 male ancestors."),
        "passage_vocabularies": vocab_rows,
        "genealogy_vocabulary_gematria": gematria_note,
        "reading": (
            f"Under real published morphology Panin's Matthew 1:1-11 features reproduce "
            f"exactly, {exact} of {len(ledger)}: 49 vocabulary words, 28 vowel-initial and "
            "21 consonant-initial, 266 letters with 140 vowels and 126 consonants, 35 "
            "recurring and 14 once, 7 in more than one form and 42 in one, 42 nouns and 7 "
            "not, and 28 male ancestors. The lone seam is proper versus common nouns (36 "
            "and 6 here against his 35 and 7), which is only whether Christos is a name or "
            "a title and does not change the 28 ancestors. His other passage vocabularies "
            "land within one (Matthew 1:18-25 is 77 exactly, Matthew 2 is 161 exactly). So "
            "Panin counted accurately; the surface-form mismatch found earlier was a "
            "lemmatization artifact, not an error of his. What this does not rescue is the "
            "inference. These are still features selected from an inexhaustible basket, a "
            "neutral panel still finds no excess of sevens, and the structure is still not "
            "load-bearing. And the figure most often quoted as a flourish, the genealogy's "
            f"vocabulary gematria, is text-bound: 42,364 on his Westcott-Hort text, a "
            f"multiple of seven, but {gen17['gematria']} on the SBLGNT, which is not. "
            "Accurate counting of selected, text-specific features does not prove design."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- console ----
    print(f"Matthew 1:1-11 under MorphGNT morphology: {exact}/{len(ledger)} of Panin's features exact")
    print(f"  {'feature':20s} {'panin':>6} {'morph':>6}  status")
    for r in ledger:
        status = "exact" if r["exact"] else f"{r['delta']:+d}"
        print(f"  {r['feature']:20s} {r['panin']:>6} {r['morphology']:>6}  {status}")
    print(f"\nOther passages, vocabulary (lemma) count vs Panin:")
    for r in vocab_rows:
        print(f"  {r['passage']:28s} panin {r['panin_vocabulary']:>4}  morphology "
              f"{r['morphology_vocabulary']:>4}  ({r['delta']:+d})")
    print(f"\nGenealogy vocabulary gematria: Panin/WH 42364 (div7 {is_heptad(42364)}); "
          f"SBLGNT {gen17['gematria']} (div7 {is_heptad(gen17['gematria'])})")
    print(OUT_DIR / "matthew_1_1_11_features.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
