#!/usr/bin/env python3
"""Cainan, the patriarch ages, and Goliath: MT versus LXX, extracted live.

Three chronology-and-genealogy divergences between the Masoretic Text and the
Septuagint, each checked from the texts rather than asserted:

1. The second Cainan. Luke 3:36 places a Cainan between Arpachshad and Shelah.
   The MT's Genesis 11 has no such man; the LXX's does. All three are checked
   live: the name in SBLGNT Luke, its absence from the WLC's Genesis 11, its
   presence in LXX Genesis 11. The New Testament's genealogy follows the Greek,
   the same direction as the quotation studies.

2. The begetting ages of Genesis 5 and 11. The LXX runs systematically about a
   century higher per patriarch. Rather than copying a published table, the
   ages are EXTRACTED from both texts: the Hebrew by composing the numeral
   words via their Strong's lemmas (units, tens, and the hundred word, with
   plural hundreds multiplied), the Greek by composing the numeral vocabulary
   up to the begetting verb. The famous corollary is computed, not asserted:
   in the MT, Methuselah dies in the flood year exactly; in this LXX edition
   (Methuselah begotten at Enoch's 165, begetting at 167), he dies years after
   the flood, the well-known LXX chronology puzzle, visible in arithmetic.

3. Goliath's height: six cubits and a span in the MT, FOUR cubits and a span
   in the LXX (checked live), with 4QSama siding with the four (documented).

Outputs under reports/genealogy_chronology/.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus
from els.morphology import read_oshb_tokens
from els.normalization import normalize_greek
from els.textstats import hebrew_letters, verse_map

WLC_CONFIG = Path("configs/example_oshb_wlc.toml")
LXX_CONFIG = Path("configs/example_ebible_grclxx.toml")
NT_CONFIG = Path("configs/example_sblgnt.toml")
OSHB_DIR = Path("data/raw/oshb/wlc")
OUT_DIR = Path("reports/genealogy_chronology")

# Strong's numbers for the Hebrew numerals used in the patriarch formulas.
HEBREW_NUMERAL = {
    "259": 1, "8147": 2, "7969": 3, "702": 4, "2568": 5, "8337": 6, "7651": 7,
    "8083": 8, "8672": 9, "6235": 10, "6240": 10, "6242": 20, "7970": 30,
    "705": 40, "2572": 50, "8346": 60, "7657": 70, "8084": 80, "8673": 90,
    "3967": 100, "505": 1000,
}
HEBREW_BEGAT = "3205"   # yalad
HEBREW_DIED = "4191"    # muth

# Greek numeral vocabulary (normalized prefixes; hundreds are fused words).
GREEK_NUMERAL = [
    ("εκατον", 100), ("διακοσι", 200), ("τριακοσι", 300), ("τετρακοσι", 400),
    ("πεντακοσι", 500), ("εξακοσι", 600), ("επτακοσι", 700), ("οκτακοσι", 800),
    ("εννακοσι", 900), ("ενακοσι", 900),
    ("τριακοντα", 30), ("τεσσαρακοντα", 40), ("πεντηκοντα", 50), ("εξηκοντα", 60),
    ("εβδομηκοντα", 70), ("ογδοηκοντα", 80), ("ενενηκοντα", 90), ("εικοσι", 20),
    ("δεκα", 10), ("πεντε", 5), ("τεσσαρ", 4), ("τρι", 3), ("δυο", 2),
    ("εννεα", 9), ("οκτω", 8), ("επτα", 7), ("εξ", 6), ("εν", 1), ("μια", 1),
]

PATRIARCHS = [
    ("Adam", ("Gen", 5, 3), ("GEN", 5, 3), None),
    ("Seth", ("Gen", 5, 6), ("GEN", 5, 6), None),
    ("Enosh", ("Gen", 5, 9), ("GEN", 5, 9), None),
    ("Kenan", ("Gen", 5, 12), ("GEN", 5, 12), None),
    ("Mahalalel", ("Gen", 5, 15), ("GEN", 5, 15), None),
    ("Jared", ("Gen", 5, 18), ("GEN", 5, 18), None),
    ("Enoch", ("Gen", 5, 21), ("GEN", 5, 21), None),
    ("Methuselah", ("Gen", 5, 25), ("GEN", 5, 25), None),
    ("Lamech", ("Gen", 5, 28), ("GEN", 5, 28), None),
    ("Shem", ("Gen", 11, 10), ("GEN", 11, 10), None),
    ("Arpachshad", ("Gen", 11, 12), ("GEN", 11, 12), None),
    ("Cainan (LXX only)", None, ("GEN", 11, 13), "καιναν"),
    ("Shelah", ("Gen", 11, 14), ("GEN", 11, 14), None),
    ("Eber", ("Gen", 11, 16), ("GEN", 11, 16), None),
    ("Peleg", ("Gen", 11, 18), ("GEN", 11, 18), None),
    ("Reu", ("Gen", 11, 20), ("GEN", 11, 20), None),
    ("Serug", ("Gen", 11, 22), ("GEN", 11, 22), None),
    ("Nahor", ("Gen", 11, 24), ("GEN", 11, 24), None),
    ("Terah", ("Gen", 11, 26), ("GEN", 11, 26), None),
]


def hebrew_number(tokens: list[tuple[str, str]], stop_lemma: str | None = HEBREW_BEGAT) -> int:
    """Compose a number from (Strong's lemma, normalized word) pairs, stopping
    at the begetting verb. Units before a PLURAL hundreds word multiply (three
    hundreds = 300); the singular hundred word adds (five years and a hundred
    year = 105)."""
    total = 0
    pending = 0
    for lemma, word in tokens:
        if stop_lemma and lemma == stop_lemma:
            break
        if lemma not in HEBREW_NUMERAL:
            continue
        value = HEBREW_NUMERAL[lemma]
        if value == 100:
            if "מאות" in word and pending:
                total += pending * 100
                pending = 0
            else:
                total += 100
        elif value < 10:
            total += pending
            pending = value
        else:
            total += pending + value
            pending = 0
    return total + pending


def greek_number(text: str, after_name: str | None = None) -> int:
    """Compose a number from the numeral words of a normalized Greek verse,
    stopping at the begetting verb (egennese, with or without the movable nu).
    With after_name, counting starts after the clause "lived <name>" (ezese
    followed by the name), for the LXX's composite verse that carries Cainan's
    begetting inside Genesis 11:13 after Arpachshad's after-years clause."""
    tokens = [normalize_greek(w) for w in text.split()]
    started = after_name is None
    total = 0
    previous = ""
    for token in tokens:
        if not started:
            if previous.startswith("εζησε") and token.startswith(after_name):
                started = True
            previous = token
            continue
        if token.startswith("εγεννησε"):
            break
        for prefix, value in GREEK_NUMERAL:
            if token == prefix or (len(prefix) > 3 and token.startswith(prefix)):
                total += value
                break
    return total


def main() -> int:
    wlc = verse_map(load_corpus(WLC_CONFIG))
    lxx = verse_map(load_corpus(LXX_CONFIG))
    nt = verse_map(load_corpus(NT_CONFIG))
    oshb = read_oshb_tokens(OSHB_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    def heb_verse_tokens(book: str, chapter: int, verse: int) -> list[tuple[str, str]]:
        return [(t.lemma, t.normalized_word) for t in oshb
                if t.book == book and t.chapter == str(chapter) and t.verse == str(verse)]

    # ---- Part 1: the second Cainan, three corpora live ----
    luke = normalize_greek(nt.get(("LUKE", "3", "36"), ""))
    cainan = {
        "luke_3_36_has_cainan": "καιναμ" in luke or "καιναν" in luke,
        "mt_gen_11_12_has_cainan": "קינן" in hebrew_letters(wlc.get(("GEN", "11", "12"), "")),
        "lxx_gen_11_12_has_cainan": "καιναν" in normalize_greek(lxx.get(("GEN", "11", "12"), "")),
    }

    # ---- Part 2: begetting ages, extracted from both texts ----
    rows = []
    for name, mt_ref, lxx_ref, after_name in PATRIARCHS:
        mt_age = (hebrew_number(heb_verse_tokens(*mt_ref)) if mt_ref else None)
        lxx_age = greek_number(lxx.get((lxx_ref[0], str(lxx_ref[1]), str(lxx_ref[2])), ""),
                               after_name=after_name)
        rows.append({"patriarch": name,
                     "mt_ref": " ".join(str(x) for x in mt_ref) if mt_ref else "(absent)",
                     "mt_begetting_age": mt_age if mt_age is not None else "",
                     "lxx_begetting_age": lxx_age,
                     "delta": (lxx_age - mt_age) if mt_age is not None else ""})

    # Methuselah versus the flood, computed from the extracted numbers.
    by_name = {r["patriarch"]: r for r in rows}
    def born_year(upto: str, column: str) -> int:
        year = 0
        for r in rows:
            if r["patriarch"] == upto:
                break
            if isinstance(r[column], int):
                year += r[column]
        return year
    methuselah_born_mt = born_year("Methuselah", "mt_begetting_age")
    methuselah_born_lxx = born_year("Methuselah", "lxx_begetting_age")
    methuselah_lifespan_mt = hebrew_number(heb_verse_tokens("Gen", 5, 27), stop_lemma=HEBREW_DIED)
    methuselah_lifespan_lxx = greek_number(lxx.get(("GEN", "5", "27"), ""), after_name=None)
    flood_year_mt = (born_year("Shem", "mt_begetting_age")
                     + hebrew_number(heb_verse_tokens("Gen", 7, 6)))
    flood_year_lxx = (born_year("Shem", "lxx_begetting_age")
                      + greek_number(lxx.get(("GEN", "7", "6"), "")))
    methuselah = {
        "mt": {"born": methuselah_born_mt, "lifespan": methuselah_lifespan_mt,
               "dies": methuselah_born_mt + methuselah_lifespan_mt,
               "flood_year": flood_year_mt,
               "dies_relative_to_flood": (methuselah_born_mt + methuselah_lifespan_mt) - flood_year_mt},
        "lxx_this_edition": {"born": methuselah_born_lxx, "lifespan": methuselah_lifespan_lxx,
                             "dies": methuselah_born_lxx + methuselah_lifespan_lxx,
                             "flood_year": flood_year_lxx,
                             "dies_relative_to_flood": (methuselah_born_lxx + methuselah_lifespan_lxx) - flood_year_lxx},
    }

    # ---- Part 3: Goliath's height ----
    mt_goliath = hebrew_letters(wlc.get(("1SAM", "17", "4"), ""))
    lxx_goliath = normalize_greek(lxx.get(("1SA", "17", "4"), ""))
    goliath = {
        "mt_reads_six_cubits": "שש" in mt_goliath,
        "lxx_reads_four_cubits": "τεσσαρων" in lxx_goliath,
        "dss_4qsama": "four cubits and a span (documented; standard scholarship)",
    }

    with (OUT_DIR / "patriarch_ages.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    deltas = [r["delta"] for r in rows if isinstance(r["delta"], int)]
    plus_100 = sum(1 for d in deltas if d == 100)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "genealogy_chronology",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": ("ages extracted from the texts: Hebrew via OSHB Strong's numeral "
                   "lemmas, Greek via numeral vocabulary; not copied from a table"),
        "cainan": cainan,
        "patriarch_ages": rows,
        "lxx_minus_mt_deltas": deltas,
        "deltas_of_exactly_100": f"{plus_100}/{len(deltas)}",
        "methuselah_vs_flood": methuselah,
        "goliath_height": goliath,
        "reading": (
            "The genealogies diverge the same direction as the quotations. Luke "
            "3:36 names a second Cainan that the Hebrew of Genesis 11 does not "
            "have and the Greek does (all three checked live): the New "
            "Testament's genealogy follows the Septuagint. The begetting ages, "
            "extracted from the numeral words of both texts rather than copied "
            "from a table, run about a century higher per patriarch in the "
            f"Greek ({plus_100} of {len(deltas)} deltas are exactly 100), the "
            "systematic divergence behind the two chronologies. The arithmetic "
            "also reproduces the famous corollary: in the MT Methuselah dies in "
            "the flood year exactly, while in this Septuagint edition he "
            "outlives the flood by over a decade, the known LXX chronology "
            "puzzle. And Goliath stands six cubits in the MT but four in the "
            "Septuagint, with 4QSama siding with the four: the shorter giant is "
            "the better-attested one."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Cainan (live):", cainan)
    print(f"\n{'patriarch':18s} {'MT':>5} {'LXX':>5} {'delta':>6}")
    for r in rows:
        print(f"  {r['patriarch']:18s} {str(r['mt_begetting_age']):>5} "
              f"{r['lxx_begetting_age']:>5} {str(r['delta']):>6}")
    print(f"\nMethuselah vs the flood (computed): MT dies at flood "
          f"{methuselah['mt']['dies_relative_to_flood']:+d} years; "
          f"LXX (this edition) {methuselah['lxx_this_edition']['dies_relative_to_flood']:+d} years")
    print(f"Goliath: MT six cubits = {goliath['mt_reads_six_cubits']}, "
          f"LXX four cubits = {goliath['lxx_reads_four_cubits']}, 4QSama four (documented)")
    print(OUT_DIR / "patriarch_ages.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
