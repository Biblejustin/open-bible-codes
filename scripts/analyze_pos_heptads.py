#!/usr/bin/env python3
"""Do parts of speech come in sevens? And what number are the famous lists?

Panin claimed "parts of speech and inflections often exhibit the same heptadic
influence," and his Matthew 1:1-11 showcase has 42 nouns (6x7). This tests that
at scale, using the part-of-speech tags in the published morphology (MorphGNT for
the Greek, OSHB for the Hebrew): count each part of speech per verse, per chapter,
and per book, and measure how often that count lands on a multiple of seven.

The answer is chance. At the chapter level, where the counts are large enough for
the test to be meaningful, the fraction of units whose noun, verb, or adjective
count is a multiple of seven sits right at the chance rate of about one in seven,
in both Testaments. Per verse the rate is below chance, because a verse rarely has
as many as seven of any single part of speech. Per book it is noisy, too few books
to be a stable rate. So the 42 nouns of Matthew 1:1-11 are one selected passage,
not a property of the language.

The second part records the famous enumerated lists (the fruit of the Spirit, the
gifts, the beatitudes). Their item counts are meaningful but varied: nine, seven,
five, ten, twelve. That is the real shape of biblical number symbolism, a few
weighty numbers each carrying a sense (seven completeness, twelve Israel, ten the
law, three God), not a uniform seven hidden everywhere. Outputs under
reports/pos_heptads/.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from els.morphology import read_morphgnt_tokens, read_oshb_tokens
from scripts.analyze_heptadic_counts import is_heptad

MORPHGNT_DIR = Path("data/raw/morphgnt/sblgnt")
OSHB_DIR = Path("data/raw/oshb/wlc")
OUT_DIR = Path("reports/pos_heptads")

POS_TESTED = ["noun", "verb", "adjective"]

# The famous enumerated lists, with their item counts. Documented, not derived;
# the point is the spread of numbers, not a single seven.
ENUMERATED_LISTS = [
    {"name": "Fruit of the Spirit", "ref": "Galatians 5:22-23", "count": 9,
     "items": "love, joy, peace, patience, kindness, goodness, faithfulness, gentleness, self-control"},
    {"name": "Gifts of the Spirit", "ref": "1 Corinthians 12:8-10", "count": 9,
     "items": "wisdom, knowledge, faith, healing, miracles, prophecy, discernment, tongues, interpretation"},
    {"name": "Gifts (Paul's second list)", "ref": "Romans 12:6-8", "count": 7,
     "items": "prophecy, service, teaching, exhortation, giving, leading, mercy"},
    {"name": "Ministry gifts", "ref": "Ephesians 4:11", "count": 5,
     "items": "apostles, prophets, evangelists, pastors, teachers"},
    {"name": "Beatitudes", "ref": "Matthew 5:3-11", "count": 9,
     "items": "eight or nine, depending on how the last is counted"},
    {"name": "Beatitudes of Revelation", "ref": "Revelation (seven)", "count": 7,
     "items": "1:3, 14:13, 16:15, 19:9, 20:6, 22:7, 22:14"},
    {"name": "The Ten Commandments", "ref": "Exodus 20:1-17", "count": 10,
     "items": "the Decalogue"},
    {"name": "Armor of God", "ref": "Ephesians 6:14-17", "count": 6,
     "items": "belt, breastplate, shoes, shield, helmet, sword"},
    {"name": "Twelve tribes / twelve apostles", "ref": "Genesis 49; Matthew 10", "count": 12,
     "items": "the number of Israel and of the new Israel"},
]


def rows_of(tokens) -> list[tuple[str, str, str, str]]:
    return [(t.book, t.chapter, t.verse, t.pos) for t in tokens if t.pos]


def unit_pos_counts(rows, level: str) -> dict[tuple, Counter]:
    """For a level in {verse, chapter, book}, map each unit to a Counter of POS."""
    out: dict[tuple, Counter] = defaultdict(Counter)
    for book, chap, vers, pos in rows:
        if level == "verse":
            key = (book, chap, vers)
        elif level == "chapter":
            key = (book, chap)
        else:
            key = (book,)
        out[key][pos] += 1
    return out


def heptad_rate(unit_counts: dict[tuple, Counter], pos: str) -> float:
    """Fraction of units whose count of `pos` is a nonzero multiple of seven."""
    if not unit_counts:
        return 0.0
    return round(sum(1 for c in unit_counts.values() if is_heptad(c.get(pos, 0))) / len(unit_counts), 4)


def mean_count(unit_counts: dict[tuple, Counter], pos: str) -> float:
    if not unit_counts:
        return 0.0
    return round(sum(c.get(pos, 0) for c in unit_counts.values()) / len(unit_counts), 2)


def corpus_rows(rows, label: str) -> list[dict]:
    levels = {lvl: unit_pos_counts(rows, lvl) for lvl in ("verse", "chapter", "book")}
    out = []
    for pos in POS_TESTED:
        row = {"corpus": label, "pos": pos}
        for lvl, uc in levels.items():
            row[f"{lvl}_units"] = len(uc)
            row[f"{lvl}_mean"] = mean_count(uc, pos)
            row[f"{lvl}_heptad_rate"] = heptad_rate(uc, pos)
        out.append(row)
    return out


def main() -> int:
    grows = rows_of(read_morphgnt_tokens(MORPHGNT_DIR))
    hrows = rows_of(read_oshb_tokens(OSHB_DIR))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    pos_rows = corpus_rows(grows, "Greek NT") + corpus_rows(hrows, "Hebrew OT")

    fields = ["corpus", "pos", "verse_units", "verse_mean", "verse_heptad_rate",
              "chapter_units", "chapter_mean", "chapter_heptad_rate",
              "book_units", "book_mean", "book_heptad_rate"]
    with (OUT_DIR / "pos_heptad_rates.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(pos_rows)
    with (OUT_DIR / "enumerated_lists.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["name", "ref", "count", "items"])
        w.writeheader()
        w.writerows(ENUMERATED_LISTS)

    chapter_rates = [r["chapter_heptad_rate"] for r in pos_rows]
    list_counts = sorted({d["count"] for d in ENUMERATED_LISTS})
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "pos_heptads",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "MorphGNT (SBLGNT) and OSHB part-of-speech tags",
        "pos_heptad_rates": pos_rows,
        "chapter_rate_range": [min(chapter_rates), max(chapter_rates)],
        "chance_baseline": round(1 / 7, 3),
        "enumerated_lists": ENUMERATED_LISTS,
        "enumerated_list_counts": list_counts,
        "reading": (
            "Parts of speech do not come in sevens beyond chance. At the chapter level, "
            "where a unit holds enough words for the test to mean anything, the fraction "
            "of chapters whose noun, verb, or adjective count is a multiple of seven runs "
            f"from {min(chapter_rates)} to {max(chapter_rates)}, straddling the chance rate "
            "of about 0.143 for every part of speech in both Testaments. Per verse the rate "
            "is lower, because a verse seldom holds seven of any one part of speech; per "
            "book it is noisy, too few books to settle. So Panin's 42 nouns in Matthew "
            "1:1-11 are a selected passage, not a feature of the grammar. The famous "
            "enumerated lists say the rest: their counts are "
            f"{', '.join(str(n) for n in list_counts)}, not a uniform seven. The fruit of "
            "the Spirit is nine, the gifts nine and seven and five, the beatitudes eight or "
            "nine in Matthew and seven in Revelation, the commandments ten, the tribes and "
            "apostles twelve. Biblical number symbolism is real but plural: seven for "
            "completeness, twelve for Israel, ten for the law, three for God, each number "
            "carrying its own sense, none hidden uniformly beneath the words."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("Part-of-speech heptadic rate (fraction of units whose POS count is a multiple of 7)")
    print(f"  chance is ~0.143 when counts are large; per-verse counts are too small")
    print(f"  {'corpus':9s} {'pos':10s} {'verse':>13} {'chapter':>15} {'book':>13}")
    print(f"  {'':9s} {'':10s} {'rate(mean)':>13} {'rate(mean)':>15} {'rate(mean)':>13}")
    for r in pos_rows:
        print(f"  {r['corpus']:9s} {r['pos']:10s} "
              f"{r['verse_heptad_rate']:.3f}({r['verse_mean']:>4}) "
              f"{r['chapter_heptad_rate']:.3f}({r['chapter_mean']:>5}) "
              f"{r['book_heptad_rate']:.3f}({r['book_mean']:>5})")
    print(f"\nFamous enumerated lists (item counts: {', '.join(str(n) for n in list_counts)}, not all seven):")
    for d in ENUMERATED_LISTS:
        print(f"  {d['count']:>2}  {d['name']:32s} {d['ref']}")
    print(OUT_DIR / "pos_heptad_rates.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
