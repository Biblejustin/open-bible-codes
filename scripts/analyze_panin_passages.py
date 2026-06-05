#!/usr/bin/env python3
"""Panin beyond the showcase: his other passage counts, and the load-bearing test.

Two questions this answers that the showcase study did not.

First, did we test all of Panin's pamphlet, or only Matthew 1:1-11? Here we test
the further counts he gives (Matthew 1:18-25, Matthew 2, the Long Ending of Mark)
at the level we can compute without a Greek lemmatizer, which is running words
(tokens) and distinct inflected forms. Where his unit is the running text and he
used Westcott-Hort, his counts tend to land (his "161 words" for the birth
narrative is exactly the WH token count). Where his unit is the vocabulary
(lemmas) or his textual form differs, they diverge, which is the same lesson as
before: the counts are real but tied to his text and his counting unit.

Second, and the pointed one: Panin argued the heptadic structure is so tight that
nothing can be removed without breaking it, and used this to defend disputed
passages such as the Long Ending of Mark. We test removal directly. For each
textually disputed passage (Mark 16:9-20, the woman taken in adultery John
7:53-8:11, the Comma Johanneum 1 John 5:7), we count the host unit with and
without the passage and ask whether divisibility by seven is load-bearing or
merely shuffles with chance. It shuffles: removing the Long Ending makes Mark's
word count a multiple of seven, removing the pericope makes John 8 a multiple of
seven, while the Comma's presence makes 1 John 5's letters a multiple of seven.
The sevens are not holding the disputed verses in place; if anything removal
improves them. The argument from numerics to authenticity does not hold.

Outputs under reports/panin_passages/.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from scripts.analyze_heptadic_counts import greek_tokens, is_heptad, load_edition

OUT_DIR = Path("reports/panin_passages")

# Book numbers in the CNTR code scheme (BBCCCVVV).
MATT, MARK, JOHN, FIRST_JOHN = 40, 41, 43, 62


def verse_codes(book: int, chapter: int, verses) -> list[str]:
    return [f"{book:02d}{chapter:03d}{v:03d}" for v in verses]


def tally(edition: dict[str, str], codes) -> tuple[int, int]:
    """(token count, letter count) over the given verse codes of one edition."""
    toks: list[str] = []
    for c in codes:
        toks += greek_tokens(edition.get(c, ""))
    return len(toks), sum(len(t) for t in toks)


def forms_count(edition: dict[str, str], codes) -> int:
    toks: list[str] = []
    for c in codes:
        toks += greek_tokens(edition.get(c, ""))
    return len(set(toks))


def chapter_codes(edition: dict[str, str], book: int, chapter: int) -> list[str]:
    """Verse codes of a chapter that actually carry Greek text in this edition
    (so an edition that marks a verse absent with a placeholder is handled)."""
    pre = f"{book:02d}{chapter:03d}"
    return sorted(c for c in edition if c.startswith(pre) and greek_tokens(edition.get(c, "")))


def book_codes(edition: dict[str, str], book: int) -> list[str]:
    pre = f"{book:02d}"
    return sorted(c for c in edition if c.startswith(pre) and greek_tokens(edition.get(c, "")))


def mark(n: int) -> str:
    return "yes" if is_heptad(n) else "no"


def main() -> int:
    ed = {n: load_edition(s) for n, s in [("TR", "KJTR"), ("Byzantine", "RP"), ("WH", "WH")]}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Part A: Panin's further counts, computable level (tokens / forms) ----
    # Each: label, edition we read (his WH where possible), the verse codes, the
    # metric, Panin's number, and a note. Vocabulary (lemma) and vocabulary-letter
    # claims need a real lemmatizer and are recorded but not asserted here.
    a_rows = []
    panin_a = [
        ("Matthew 1:18-25 birth", "WH", verse_codes(MATT, 1, range(18, 26)), "tokens", 161,
         "Panin's running-word count; matches WH, while TR and Byzantine read 167"),
        ("Matthew 1:18-25 birth", "WH", verse_codes(MATT, 1, range(18, 26)), "forms", 105,
         "distinct forms; WH gives 104, off by one (a normalization edge)"),
        ("Matthew 2 childhood", "WH", chapter_codes(ed["WH"], MATT, 2), "forms", 238,
         "distinct forms; WH gives 235. Panin's 161 vocabulary and 896 vocab-letters need a lemmatizer"),
        ("Mark 16:9-20 Long Ending", "Byzantine", verse_codes(MARK, 16, range(9, 21)), "tokens", 175,
         "WH omits the Long Ending; the Byzantine form is 166 words, not Panin's 175"),
        ("Mark 16:9-20 Long Ending", "Byzantine", verse_codes(MARK, 16, range(9, 21)), "forms", 133,
         "Byzantine gives 130 distinct forms"),
    ]
    for label, edn, codes, metric, claim, note in panin_a:
        got = forms_count(ed[edn], codes) if metric == "forms" else tally(ed[edn], codes)[0]
        a_rows.append({"section": "panin_further_counts", "passage": label, "edition": edn,
                       "metric": metric, "panin": claim, "computed": got,
                       "matches": got == claim, "note": note})

    # ---- Part B: the load-bearing / removal test ----
    b_rows = []

    def removal_case(label: str, edn: str, host_label: str, host_codes, block_codes):
        block = set(block_codes)
        without = [c for c in host_codes if c not in block]
        wt, wl = tally(ed[edn], host_codes)
        ot, ol = tally(ed[edn], without)
        bt, bl = tally(ed[edn], list(block_codes))
        for scope, (t, l) in [(f"{host_label} WITH", (wt, wl)),
                              (f"{host_label} WITHOUT", (ot, ol)),
                              ("the passage itself", (bt, bl))]:
            b_rows.append({"section": "removal_test", "passage": label, "edition": edn,
                           "scope": scope, "words": t, "words_div7": mark(t),
                           "letters": l, "letters_div7": mark(l)})
        # what removal does to divisibility by seven
        gained = [m for m, a, b in [("words", is_heptad(ot), is_heptad(wt)),
                                    ("letters", is_heptad(ol), is_heptad(wl))] if a and not b]
        lost = [m for m, a, b in [("words", is_heptad(ot), is_heptad(wt)),
                                  ("letters", is_heptad(ol), is_heptad(wl))] if b and not a]
        return gained, lost

    byz = "Byzantine"
    mk16 = chapter_codes(ed[byz], MARK, 16)
    le = verse_codes(MARK, 16, range(9, 21))
    g1, l1 = removal_case("Mark Long Ending 16:9-20", byz, "Mark 16", mk16, le)
    g1b, l1b = removal_case("Mark Long Ending 16:9-20 (whole book)", byz, "Mark book",
                            book_codes(ed[byz], MARK), le)
    j8 = chapter_codes(ed[byz], JOHN, 8)
    pa = verse_codes(JOHN, 8, range(1, 12))   # the chapter-8 core; 7:53 sits in chapter 7
    g2, l2 = removal_case("Pericope Adulterae John 8:1-11", byz, "John 8", j8, pa)

    # Comma Johanneum: a within-verse plus in the TR, absent in WH. Compare the
    # host chapter between the two texts rather than removing a verse.
    c5_tr = chapter_codes(ed["TR"], FIRST_JOHN, 5)
    c5_wh = chapter_codes(ed["WH"], FIRST_JOHN, 5)
    tr_t, tr_l = tally(ed["TR"], c5_tr)
    wh_t, wh_l = tally(ed["WH"], c5_wh)
    v7_tr = tally(ed["TR"], ["62005007"])[0]
    v7_wh = tally(ed["WH"], ["62005007"])[0]
    for scope, edn, t, l in [("1 John 5 WITH Comma", "TR", tr_t, tr_l),
                             ("1 John 5 WITHOUT Comma", "WH", wh_t, wh_l)]:
        b_rows.append({"section": "removal_test", "passage": "Comma Johanneum 1 John 5:7",
                       "edition": edn, "scope": scope, "words": t, "words_div7": mark(t),
                       "letters": l, "letters_div7": mark(l)})

    # tally the direction of removal effects across the clean (verse-presence) cases
    gains = sum(len(g) for g in (g1, g1b, g2))   # divisibility gained BY removal
    losses = sum(len(x) for x in (l1, l1b, l2))  # divisibility lost BY removal

    rows = a_rows + b_rows
    fields = sorted({k for r in rows for k in r})
    with (OUT_DIR / "panin_passages.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in fields} for r in rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "panin_passages",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "Ivan Panin, The Inspiration of the Scriptures Scientifically Demonstrated (1899). Public domain.",
        "did_we_test_all": ("No. The showcase study tested Matthew 1:1-11. Here we add his "
                            "Matthew 1:18-25, Matthew 2, and Mark 16:9-20 counts at the "
                            "token and form level. His running-word counts on Westcott-Hort "
                            "tend to match (161 words for Matthew 1:18-25 is exact); his "
                            "vocabulary (lemma) and vocabulary-letter counts need a "
                            "lemmatizer we do not have, and his Mark figures sit on a "
                            "textual form (175 words) that the Byzantine manuscripts (166) "
                            "do not share."),
        "part_a_further_counts": a_rows,
        "removal_test": b_rows,
        "removal_div7_gained_by_removal": gains,
        "removal_div7_lost_by_removal": losses,
        "comma_verse_words": {"TR": v7_tr, "WH": v7_wh},
        "pericope_note": ("the John test removes the chapter-8 core 8:1-11; the traditional "
                          "span 7:53-8:11 adds one verse (7:53, seven words) from chapter 7"),
        "reading": (
            "Panin's load-bearing claim fails the removal test. Mark 16 with the Long "
            f"Ending is {tally(ed[byz], mk16)[0]} words (not a multiple of seven); without "
            "9-20 it is 133, which IS a multiple of seven. The whole book of Mark without "
            "the ending is 11,452 words, a multiple of seven, and with it is not. John 8 "
            "without the woman taken in adultery (8:1-11) is 931 words, a multiple of "
            "seven, and with it is not. The Long Ending as it actually stands in the Byzantine "
            "manuscripts is 166 words, not the 175 of Panin's form, so even its own "
            "'heptad' depends on a textual reconstruction. The Comma Johanneum runs the "
            "other way: its presence makes 1 John 5 total 1981 letters, a multiple of "
            "seven, which absence breaks. So across the disputed passages divisibility by "
            f"seven is gained by removal {gains} times and lost {losses} times, shuffling "
            "with chance in both directions. The sevens do not hold the disputed verses in "
            "place. Panin's inference from numerics to authenticity is not supported, and "
            "at Mark and John it inverts: removing the disputed text improves the count."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- console ----
    print("Part A: Panin's further counts vs our computable level (tokens / forms)")
    print(f"  {'passage':28s} {'metric':7s} {'panin':>6} {'got':>6}  match  note")
    for r in a_rows:
        print(f"  {r['passage']:28s} {r['metric']:7s} {r['panin']:>6} {r['computed']:>6}  "
              f"{'yes' if r['matches'] else 'no ':>5}  {r['note'][:54]}")
    print("\nPart B: load-bearing / removal test (does removing a disputed passage break sevens?)")
    print(f"  {'passage / scope':40s} {'words':>6} /7 {'letters':>7} /7")
    for r in b_rows:
        print(f"  {r['passage'][:22] + ' | ' + r['scope']:40s} {r['words']:>6} {r['words_div7']:>2} "
              f"{r['letters']:>7} {r['letters_div7']:>2}")
    print(f"\n  divisibility by seven GAINED by removal: {gains}   LOST by removal: {losses}")
    print(f"  -> sevens shuffle with chance; they are not load-bearing on the disputed verses")
    print(OUT_DIR / "panin_passages.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
