#!/usr/bin/env python3
"""The heptadic structure that is actually there: the seven the authors wrote.

The companion studies (analyze_heptadic_counts, analyze_panin_claims,
analyze_panin_passages, analyze_panin_morphology) settle the hidden, micro-numeric
claim: word and letter counts divisible by seven sit at chance, and Panin's
showcase, though accurately counted, is selected from an inexhaustible basket. But
there is a real sevenfold structure in Scripture, and it is not hidden at all. The
authors say "seven" out loud, constantly, in particular books, because seven
carries the theology of completeness, covenant rest, and consummation.

This script measures that surface structure two ways, from published morphology
(MorphGNT for the Greek, OSHB for the Hebrew, so the Hebrew homograph of seven,
swear, and satisfied is disambiguated by lexeme rather than by consonants).

1. Where the word-family for seven concentrates, per book, per thousand words. In
   the Greek New Testament it is Revelation, by a factor of ten. In the Hebrew
   Bible it is the Torah, Leviticus and Numbers and Genesis, the books of
   creation, sabbath, the feasts, the sabbatical year, and the jubilee.
2. Revelation's explicit seven-series: every "seven X" the seer names (seven
   churches, spirits, stars, lampstands, seals, trumpets, bowls, plagues,
   thunders, horns, heads, and the rest). This is design on the surface, written
   by the author, not encoded beneath the text.

So the honest answer to "is Scripture heptadic" is yes and no: yes, overtly and
thematically, where seven is a named theological number; no, not as a hidden
arithmetic of letter counts. Outputs under reports/heptadic_structure/.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els.morphology import read_morphgnt_tokens, read_oshb_tokens

MORPHGNT_DIR = Path("data/raw/morphgnt/sblgnt")
OSHB_DIR = Path("data/raw/oshb/wlc")
OUT_DIR = Path("reports/heptadic_structure")

# Greek lemmas of the seven word-family (seven, seventh, seven times, seventy,
# seventy times, seven thousand).
GREEK_SEVEN = {"ἑπτά", "ἕβδομος", "ἑπτάκις", "ἑβδομήκοντα", "ἑβδομηκοντάκις",
               "ἑπτακισχίλιοι"}

# Hebrew Strong's numbers for the number-seven family, disambiguated from the
# homographs swear (7650), satisfied (7646-9), oath (7621), and the proper names
# Beersheba (884) and Bathsheba (1339), which share the consonants but not the sense.
HEBREW_SEVEN = {
    "7651": "seven", "7637": "seventh", "7657": "seventy",
    "7620": "week (a seven)", "7659": "sevenfold", "7658": "sevenfold",
}

# Readable glosses for the Revelation seven-series (convenience only).
REV_GLOSS = {
    "ἄγγελος": "angels", "ἐκκλησία": "churches", "πνεῦμα": "spirits",
    "ἀστήρ": "stars", "πληγή": "plagues", "φιάλη": "bowls", "λυχνία": "lampstands",
    "βροντή": "thunders", "κέρας": "horns", "σφραγίς": "seals", "σάλπιγξ": "trumpets",
    "κεφαλή": "heads", "ὀφθαλμός": "eyes", "διάδημα": "diadems", "ὄρος": "mountains",
    "λαμπάς": "lamps", "στόμα": "mouth", "ἀπώλεια": "destruction",
}


def book_counts(items) -> tuple[Counter, Counter]:
    """(seven-count per book, total words per book) over (book, is_seven) pairs."""
    per: Counter = Counter()
    words: Counter = Counter()
    for book, seven in items:
        words[book] += 1
        if seven:
            per[book] += 1
    return per, words


def density_rows(per: Counter, words: Counter) -> list[dict]:
    """Per-book rows with a per-thousand-words rate, ranked by rate then count."""
    rows = [{"book": bk, "seven": per[bk], "words": words[bk],
             "per_1000": round(1000 * per[bk] / words[bk], 2)} for bk in per]
    rows.sort(key=lambda r: (-r["per_1000"], -r["seven"]))
    return rows


def seven_collocations(items) -> Counter:
    """Count 'seven X' noun collocations: each ἑπτά paired with the next noun in
    the same verse. items is an ordered iterable of (ref, lemma, pos)."""
    items = list(items)
    things: Counter = Counter()
    for i, (ref, lemma, _pos) in enumerate(items):
        if lemma == "ἑπτά":
            for ref2, lemma2, pos2 in items[i + 1:i + 6]:
                if ref2 != ref:
                    break
                if pos2 == "noun":
                    things[lemma2] += 1
                    break
    return things


def main() -> int:
    greek = read_morphgnt_tokens(MORPHGNT_DIR)
    hebrew = read_oshb_tokens(OSHB_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    g_per, g_words = book_counts((t.book, t.lemma in GREEK_SEVEN) for t in greek)
    h_per, h_words = book_counts((t.book, t.lemma in HEBREW_SEVEN) for t in hebrew)
    g_rows = density_rows(g_per, g_words)
    h_rows = density_rows(h_per, h_words)
    rev = seven_collocations((t.ref, t.lemma, t.pos) for t in greek if t.book == "Rev")
    rev_rows = [{"thing": lemma, "gloss": REV_GLOSS.get(lemma, ""), "count": c}
                for lemma, c in rev.most_common()]

    g_total, h_total = sum(g_per.values()), sum(h_per.values())
    g_top = max(g_rows, key=lambda r: r["seven"])
    h_top = max(h_rows, key=lambda r: r["seven"])

    for name, rows, fields in [
        ("greek_seven_by_book", g_rows, ["book", "seven", "words", "per_1000"]),
        ("hebrew_seven_by_book", h_rows, ["book", "seven", "words", "per_1000"]),
        ("revelation_seven_series", rev_rows, ["thing", "gloss", "count"]),
    ]:
        with (OUT_DIR / f"{name}.csv").open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "heptadic_structure",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "MorphGNT (SBLGNT) and OSHB (Westminster Leningrad), by lemma",
        "greek_seven_total": g_total,
        "greek_lead_book": {"book": g_top["book"], "count": g_top["seven"], "per_1000": g_top["per_1000"]},
        "greek_by_book": g_rows,
        "hebrew_seven_total": h_total,
        "hebrew_by_lemma": dict(Counter(
            HEBREW_SEVEN[t.lemma] for t in hebrew if t.lemma in HEBREW_SEVEN)),
        "hebrew_lead_book": {"book": h_top["book"], "count": h_top["seven"], "per_1000": h_top["per_1000"]},
        "hebrew_by_book": h_rows[:15],
        "revelation_seven_series": rev_rows,
        "revelation_series_total": sum(rev.values()),
        "revelation_series_distinct": len(rev),
        "revelation_method_note": ("each ἑπτά is paired with the next noun in the verse; "
                                   "this is a heuristic, so a couple of low-count entries "
                                   "(mouth, destruction) are misattributions where seven "
                                   "modifies a different noun nearby. The high-count "
                                   "entries are the genuine series."),
        "reading": (
            "The sevenfold structure that is real is the one on the surface. The "
            f"Greek word-family for seven occurs {g_total} times in the New Testament "
            f"and {g_top['seven']} of them, more than half, are in Revelation, at "
            f"{g_top['per_1000']} per thousand words against well under one for every "
            "other book. The Hebrew family occurs "
            f"{h_total} times, concentrated in the Torah: {h_top['book']} leads in raw "
            f"count, with Leviticus and Numbers and Genesis the densest, the books of "
            "creation and sabbath and the feasts and the sabbatical year and the "
            "jubilee. Revelation then spells its architecture out: the seer names "
            f"{len(rev)} distinct 'seven' things across {sum(rev.values())} mentions, "
            "seven churches and spirits and stars and lampstands and seals and "
            "trumpets and bowls and plagues and thunders and horns and heads. This is "
            "authorial design, written in the open, where seven means completeness and "
            "consummation. It is the opposite of the hidden letter-count claim, which "
            "the companion studies find at chance. Scripture is heptadic the way the "
            "authors made it so, by saying seven, not by encoding it beneath the words."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- console ----
    print(f"Seven word-family, Greek NT: {g_total} occurrences (by book, per 1000 words)")
    print(f"  {'book':6s} {'seven':>5} {'words':>6} {'per1k':>6}")
    for r in g_rows[:6]:
        print(f"  {r['book']:6s} {r['seven']:>5} {r['words']:>6} {r['per_1000']:>6.2f}")
    print(f"  -> Revelation: {g_top['seven']} of {g_total} ({100*g_top['seven']//g_total}%), "
          f"{g_top['per_1000']} per 1000")
    print(f"\nSeven word-family, Hebrew OT: {h_total} occurrences (top books by density)")
    print(f"  {'book':6s} {'seven':>5} {'words':>6} {'per1k':>6}")
    for r in h_rows[:8]:
        print(f"  {r['book']:6s} {r['seven']:>5} {r['words']:>6} {r['per_1000']:>6.2f}")
    print(f"  -> Torah leads: {h_top['book']} has the most ({h_top['seven']})")
    print(f"\nRevelation's explicit seven-series: {sum(rev.values())} mentions, {len(rev)} things")
    for r in rev_rows:
        print(f"  seven {(r['gloss'] or r['thing']):14s} x{r['count']}")
    print(OUT_DIR / "manifest.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
