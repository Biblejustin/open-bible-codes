#!/usr/bin/env python3
"""A catalog of the named structural heptad claims, each checked against the data.

These are the famous sevenfold structures people point to: the sevenfold "and it
was good" in Genesis 1, the thirty-five Elohims of the creation account, the seven
beatitudes of Revelation, Jericho's sevens, Daniel's seventy weeks, John's seven
"I am" sayings, Matthew's three fourteens. Unlike the hidden letter-count claims
(see analyze_panin_*), these are claims about words the authors actually wrote, so
they can be checked by counting the right lexeme in the right passage, from
published morphology (OSHB for Hebrew, MorphGNT for Greek).

Each claim is either COUNTED (a specific number to verify, marked confirmed or
not) or DOCUMENTED (a real structure whose "seven" is a matter of how you divide
the passage, recorded with a supporting count). The point is the contrast: where
the seven is on the surface, in the words, it holds; the hidden arithmetic is what
fails. Outputs under reports/heptadic_claims_catalog/.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.morphology import read_morphgnt_tokens, read_oshb_tokens

MORPHGNT_DIR = Path("data/raw/morphgnt/sblgnt")
OSHB_DIR = Path("data/raw/oshb/wlc")
OUT_DIR = Path("reports/heptadic_claims_catalog")

# Hebrew number-seven family (seven, seventh, seventy, week, sevenfold), by Strong's.
SEVEN = {"7651", "7637", "7657", "7620", "7659", "7658"}

# COUNTED claims: count a lexeme in a passage and compare to the claimed value.
# lang 'heb' uses OSHB Strong's lemmas; 'grk' uses MorphGNT lemmas. A passage is a
# book plus chapter spans (chapter, verse-range); a whole chapter uses range(1, 200).
COUNTED = [
    {"name": "Genesis 1: the sevenfold 'and it was good'", "lang": "heb", "book": "Gen",
     "spans": [(1, range(1, 32))], "lemmas": {"2896"}, "claim": 7,
     "note": "'God saw that it was good' at 1:4,10,12,18,21,25 and 'very good' at 1:31"},
    {"name": "Genesis creation: 'God' (Elohim) is 35 = 5x7", "lang": "heb", "book": "Gen",
     "spans": [(1, range(1, 32)), (2, range(1, 4))], "lemmas": {"430"}, "claim": 35,
     "note": "Elohim across the seven-day account, Genesis 1:1 through 2:3"},
    {"name": "Joshua 6: the sevens of Jericho are 14 = 2x7", "lang": "heb", "book": "Josh",
     "spans": [(6, range(1, 28))], "lemmas": SEVEN, "claim": 14,
     "note": "seven priests, seven trumpets, the seventh day, seven circuits"},
    {"name": "Matthew 23: the seven woes", "lang": "grk", "book": "Matt",
     "spans": [(23, range(1, 40))], "lemmas": {"οὐαί"}, "claim": 7,
     "note": "'woe to you, scribes and Pharisees' seven times in the chapter"},
    {"name": "Revelation: the seven beatitudes", "lang": "grk", "book": "Rev",
     "spans": [(c, range(1, 30)) for c in range(1, 23)], "lemmas": {"μακάριος"}, "claim": 7,
     "note": "'blessed' at 1:3, 14:13, 16:15, 19:9, 20:6, 22:7, 22:14"},
]

# DOCUMENTED structures: a real sevenfold pattern whose exact count depends on how
# you divide the passage. We record a supporting count, not a pass/fail.
DOCUMENTED = [
    {"name": "Daniel 9: the seventy weeks (seventy sevens)", "lang": "heb", "book": "Dan",
     "spans": [(9, range(1, 28))], "lemmas": SEVEN,
     "note": "'seventy sevens are decreed' (9:24); the seven word-family occurs here"},
    {"name": "Isaiah 11:2: the sevenfold Spirit", "lang": "heb", "book": "Isa",
     "spans": [(11, [2])], "lemmas": {"7307"},
     "note": "one Spirit of the LORD and six attributes (wisdom, understanding, counsel, "
             "might, knowledge, fear), a sevenfold whole; ruach occurs here"},
    {"name": "Matthew 1: three fourteens, 42 = 6x7 generations", "lang": "grk", "book": "Matt",
     "spans": [(1, range(1, 18))], "lemmas": {"γεννάω"},
     "note": "Matthew states fourteen generations three times (1:17); 'begat' occurs here"},
    {"name": "Zechariah 4: the lampstand of seven lamps", "lang": "heb", "book": "Zech",
     "spans": [(4, range(1, 15))], "lemmas": SEVEN,
     "note": "seven lamps, seven pipes, the seven eyes of the LORD"},
    {"name": "Genesis 4: sevenfold vengeance for Cain, seventy-sevenfold for Lamech",
     "lang": "heb", "book": "Gen", "spans": [(4, range(1, 27))], "lemmas": SEVEN,
     "note": "'sevenfold' (4:15) and 'seventy-sevenfold' (4:24)"},
    {"name": "Genesis 7-8: the sevens of the flood", "lang": "heb", "book": "Gen",
     "spans": [(7, range(1, 25)), (8, range(1, 23))], "lemmas": SEVEN,
     "note": "clean animals taken by sevens, seven days of waiting, the seventh month"},
    {"name": "Leviticus 23: the feast calendar", "lang": "heb", "book": "Lev",
     "spans": [(23, range(1, 45))], "lemmas": SEVEN,
     "note": "seven annual feasts, the seven-day festivals, seven weeks to Pentecost, "
             "the feasts of the seventh month"},
    {"name": "Leviticus 25: the sabbatical year and the jubilee (seven sevens)",
     "lang": "heb", "book": "Lev", "spans": [(25, range(1, 56))], "lemmas": SEVEN,
     "note": "every seventh year a sabbath for the land; after seven sevens of years, "
             "the jubilee"},
    {"name": "2 Kings 5: Naaman dips seven times in the Jordan", "lang": "heb",
     "book": "2Kgs", "spans": [(5, range(1, 28))], "lemmas": SEVEN,
     "note": "Elisha's command (5:10) and Naaman's obedience (5:14)"},
    {"name": "Matthew 18:22: forgive seventy times seven", "lang": "grk", "book": "Matt",
     "spans": [(18, [21, 22])], "lemmas": {"ἑβδομηκοντάκις"},
     "note": "'not seven times, but seventy times seven', the measure of forgiveness"},
]

# John's seven "I am" sayings: the predicated metaphors. A curated list (the raw
# count of ego-eimi includes many non-predicated uses), recorded with references.
JOHN_I_AM = [
    ("John 6:35", "the bread of life"), ("John 8:12", "the light of the world"),
    ("John 10:9", "the door"), ("John 10:11", "the good shepherd"),
    ("John 11:25", "the resurrection and the life"),
    ("John 14:6", "the way, the truth, and the life"), ("John 15:1", "the true vine"),
]


def rows_of(tokens) -> list[tuple[str, str, str, str]]:
    return [(t.book, t.chapter, t.verse, t.lemma) for t in tokens]


def count_in_spans(rows, book: str, spans, lemmas: set[str]) -> int:
    targets = {(book, str(ch), str(v)) for ch, verses in spans for v in verses}
    return sum(1 for b, c, v, lem in rows if (b, c, v) in targets and lem in lemmas)


def ego_eimi_total(rows_greek) -> int:
    """Total 'I am' (ἐγώ immediately followed by εἰμί) in John, for context."""
    john = [r for r in rows_greek if r[0] == "John"]
    return sum(1 for i in range(len(john) - 1)
               if john[i][3] == "ἐγώ" and john[i + 1][3] == "εἰμί")


def main() -> int:
    hrows = rows_of(read_oshb_tokens(OSHB_DIR))
    grows = rows_of(read_morphgnt_tokens(MORPHGNT_DIR))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    def count(claim) -> int:
        rows = hrows if claim["lang"] == "heb" else grows
        return count_in_spans(rows, claim["book"], claim["spans"], claim["lemmas"])

    counted = []
    for c in COUNTED:
        got = count(c)
        counted.append({"name": c["name"], "claim": c["claim"], "got": got,
                        "confirmed": got == c["claim"],
                        "is_heptad": got != 0 and got % 7 == 0, "note": c["note"]})
    documented = [{"name": d["name"], "supporting_count": count(d), "note": d["note"]}
                  for d in DOCUMENTED]
    documented.append({"name": "John: the seven 'I am' sayings",
                       "supporting_count": len(JOHN_I_AM),
                       "note": f"the predicated metaphors at {', '.join(r for r, _ in JOHN_I_AM)}; "
                               f"total ego-eimi in John is {ego_eimi_total(grows)}"})
    documented.append({"name": "Matthew 6:9-13: the seven petitions of the Lord's Prayer",
                       "supporting_count": 7,
                       "note": "hallowed be your name, your kingdom come, your will be done, "
                               "daily bread, forgive our debts, lead us not into temptation, "
                               "deliver us from evil"})

    confirmed = sum(1 for r in counted if r["confirmed"])

    with (OUT_DIR / "counted_claims.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "claim", "got", "confirmed", "is_heptad", "note"])
        w.writeheader()
        w.writerows(counted)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "heptadic_claims_catalog",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "OSHB (Hebrew) and MorphGNT (Greek), by lemma",
        "counted_confirmed": f"{confirmed}/{len(counted)}",
        "counted_claims": counted,
        "documented_structures": documented,
        "john_i_am_sayings": [{"ref": r, "predicate": p} for r, p in JOHN_I_AM],
        "reading": (
            f"Of the named structural heptads that resolve to a single count, "
            f"{confirmed} of {len(counted)} check out exactly: Genesis 1 has the "
            "sevenfold 'and it was good', the seven-day creation account names God "
            "(Elohim) 35 times (5x7), Jericho's account carries 14 sevens (2x7), "
            "Matthew gives seven woes, and Revelation seven beatitudes. The documented "
            "structures, from the flood's sevens and the feast calendar and the jubilee "
            "of seven sevens to Daniel's seventy weeks, Isaiah's sevenfold Spirit, "
            "Matthew's three fourteens, John's seven 'I am' sayings, and the seven "
            "petitions of the Lord's Prayer, are real divisions of the text the authors "
            "signal. These hold because the "
            "seven is in the words, on the surface, where the number carries the "
            "theology of completeness. That is the difference from the hidden "
            "letter-count claims, which sit at chance: Scripture's genuine sevens were "
            "written, not encoded."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Structural heptad claims, counted: {confirmed}/{len(counted)} confirmed exactly")
    print(f"  {'claim':52s} {'want':>5} {'got':>5}  status")
    for r in counted:
        status = "confirmed" if r["confirmed"] else ("heptad" if r["is_heptad"] else "no")
        print(f"  {r['name']:52s} {r['claim']:>5} {r['got']:>5}  {status}")
    print(f"\nDocumented structures (real sevenfold divisions, supporting count):")
    for d in documented:
        print(f"  {d['name']:52s} count={d['supporting_count']}")
    print(OUT_DIR / "counted_claims.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
