#!/usr/bin/env python3
"""Messianic prophecy: Hebrew (MT) vs Greek (LXX), and which the NT quotes.

The New Testament writers, quoting the Old, usually quote it in Greek, from the
Septuagint (LXX), the translation the synagogues of the diaspora used. At several
of the great messianic texts the Greek LXX differs from the Hebrew Masoretic
Text (MT) in a way that matters, and the New Testament follows the LXX. This
script lays the three readings side by side for a fixed set of loci and measures,
by Greek token overlap, how closely the NT quotation tracks the LXX.

  Isaiah 7:14   Hebrew almah (young woman) vs LXX parthenos (virgin); Matthew
                quotes the LXX (Matt 1:23).
  Psalm 40:6    Hebrew "ears you have opened" vs LXX "a body you prepared for
                me"; Hebrews 10:5 quotes the LXX.
  Deut 32:43    the LXX (and a Qumran Hebrew copy) has "let all God's angels
                worship him," absent from the MT; Hebrews 1:6 quotes it.
  Amos 9:12     Hebrew "possess the remnant of Edom" vs LXX "that the rest of
                men may seek the Lord"; James quotes the LXX (Acts 15:17).
  Isaiah 53:7-8 the Ethiopian's text (Acts 8:32-33) is the LXX.
  Psalm 110:1   "The LORD said to my Lord" (Jesus's own argument, Matt 22:44).
  Micah 5:2     Bethlehem (Matt 2:6).

This is reading comparison, not a single statistic: the Hebrew and Greek are
different languages, so the script shows all three texts and scores only the
NT-to-LXX Greek overlap. Pure data over the OSHB WLC, the eBible Greek LXX, and
the SBLGNT. Outputs under reports/messianic_mt_lxx/.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path

from els.corpus import load_corpus
from els.normalization import normalize_greek

WLC_CONFIG = Path("configs/example_oshb_wlc.toml")
LXX_CONFIG = Path("configs/example_ebible_grclxx.toml")
NT_CONFIG = Path("configs/example_sblgnt.toml")
OUT_DIR = Path("reports/messianic_mt_lxx")

# name, mt(book,ch,vs), lxx(book,ch,vs), nt(book,ch,vs), the issue,
# lxx_key (LXX-distinctive Greek the NT may share), mt_key (the Hebrew-side Greek
# the NT may share instead). The NT's choice between them marks which reading it
# treats as the inspired one at that point.
LOCI = [
    ("Isaiah 7:14 the virgin", ("Isa", "7", "14"), ("ISA", "7", "14"), ("Matt", "1", "23"),
     "Hebrew almah (young woman) vs LXX parthenos (virgin)", "παρθεν", ""),
    ("Psalm 40:6 a body prepared", ("Ps", "40", "7"), ("PSA", "39", "7"), ("Heb", "10", "5"),
     "Hebrew 'ears you opened' vs LXX 'a body you prepared for me'", "σωμα", ""),
    ("Deut 32:43 angels worship him", ("Deut", "32", "43"), ("DEU", "32", "43"), ("Heb", "1", "6"),
     "LXX (and Qumran) 'let all God's angels worship him,' absent from MT", "προσκυν", ""),
    ("Amos 9:12 the rest of men", ("Amos", "9", "12"), ("AMO", "9", "12"), ("Acts", "15", "17"),
     "Hebrew 'remnant of Edom' vs LXX 'that the rest of men may seek the Lord'", "εκζητη", ""),
    ("Isaiah 53:7 led as a sheep", ("Isa", "53", "7"), ("ISA", "53", "7"), ("Acts", "8", "32"),
     "the Ethiopian eunuch reads the LXX of the Suffering Servant", "σφαγη", ""),
    ("Psalm 110:1 the LORD to my Lord", ("Ps", "110", "1"), ("PSA", "109", "1"), ("Matt", "22", "44"),
     "Jesus' own argument from the Messiah being David's Lord", "κυρι", ""),
    ("Micah 5:2 Bethlehem", ("Mic", "5", "1"), ("MIC", "5", "1"), ("Matt", "2", "6"),
     "the birthplace of the ruler", "βηθλε", ""),
    # counter-cases: where the NT follows the Hebrew against the Greek
    ("Hosea 11:1 my son", ("Hos", "11", "1"), ("HOS", "11", "1"), ("Matt", "2", "15"),
     "Hebrew 'my son' (singular) vs LXX 'his children'; Matthew has 'my son'", "τεκν", "υιον"),
    ("Zech 12:10 whom they pierced", ("Zech", "12", "10"), ("ZEC", "12", "10"), ("John", "19", "37"),
     "Hebrew 'pierced' vs LXX 'mocked/danced'; John has 'pierced'", "κατωρχ", "εξεκεντ"),
]


def verse_map(corpus) -> dict[tuple[str, str, str], str]:
    out = {}
    for v in corpus.verses:
        out[(str(v.book).upper(), str(v.chapter), str(v.verse))] = v.raw_text
    return out


def lookup(vmap: dict, ref: tuple[str, str, str]) -> str:
    book, ch, vs = ref
    return vmap.get((book.upper(), ch, vs), "")


def greek_tokens(text: str) -> list[str]:
    return [w for tok in text.split() if (w := normalize_greek(tok))]


def greek_overlap(a: str, b: str) -> float:
    """Token-sequence similarity of two Greek texts (0..1)."""
    return round(SequenceMatcher(None, greek_tokens(a), greek_tokens(b)).ratio(), 4)


def has_stem(text: str, stem: str) -> bool:
    return any(t.startswith(stem) for t in greek_tokens(text))


def nt_alignment(nt_text: str, lxx_key: str, mt_key: str) -> str:
    """Which reading the NT carries at a divergence: the LXX-distinctive word or
    the Hebrew-side word. The NT's choice is the inspired reading at that point."""
    has_lxx = bool(lxx_key) and has_stem(nt_text, lxx_key)
    has_mt = bool(mt_key) and has_stem(nt_text, mt_key)
    if has_lxx and not has_mt:
        return "follows_LXX"
    if has_mt and not has_lxx:
        return "follows_MT"
    return "ambiguous"


def main() -> int:
    wlc = verse_map(load_corpus(WLC_CONFIG))
    lxx = verse_map(load_corpus(LXX_CONFIG))
    nt = verse_map(load_corpus(NT_CONFIG))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for name, mt_ref, lxx_ref, nt_ref, issue, lxx_key, mt_key in LOCI:
        mt_text = lookup(wlc, mt_ref)
        lxx_text = lookup(lxx, lxx_ref)
        nt_text = lookup(nt, nt_ref)
        rows.append({
            "locus": name, "issue": issue,
            "mt_ref": " ".join(mt_ref), "lxx_ref": " ".join(lxx_ref), "nt_ref": " ".join(nt_ref),
            "mt_hebrew": mt_text, "lxx_greek": lxx_text, "nt_greek": nt_text,
            "nt_to_lxx_overlap": greek_overlap(nt_text, lxx_text) if (nt_text and lxx_text) else "",
            "nt_follows": nt_alignment(nt_text, lxx_key, mt_key),
            "lxx_key_in_nt": bool(lxx_key) and has_stem(nt_text, lxx_key),
            "mt_key_in_nt": bool(mt_key) and has_stem(nt_text, mt_key),
            "all_three_found": bool(mt_text and lxx_text and nt_text),
        })

    found = sum(r["all_three_found"] for r in rows)
    follows_lxx = sum(r["nt_follows"] == "follows_LXX" for r in rows)
    follows_mt = sum(r["nt_follows"] == "follows_MT" for r in rows)
    overlaps = [r["nt_to_lxx_overlap"] for r in rows if isinstance(r["nt_to_lxx_overlap"], float)]
    mean_overlap = round(sum(overlaps) / len(overlaps), 4) if overlaps else 0.0

    with (OUT_DIR / "messianic_loci.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "messianic_mt_lxx",
        "created_utc": datetime.now(UTC).isoformat(),
        "sources": {"MT": "OSHB WLC", "LXX": "eBible Greek LXX", "NT": "SBLGNT"},
        "loci": len(rows), "loci_all_three_found": found,
        "nt_follows_lxx": follows_lxx, "nt_follows_mt": follows_mt,
        "mean_nt_to_lxx_overlap": mean_overlap,
        "reading": ("nt_follows records which reading the NT carries at each "
                    "divergence. It mostly follows the Greek Septuagint (virgin, "
                    "body, angels-worship), and at Hosea 11:1 and Zechariah 12:10 it "
                    "follows the Hebrew. The inspired NT is the arbiter; its reading "
                    "is the inspired one at each point."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"messianic loci: {len(rows)}  all-three-found: {found}  "
          f"NT follows LXX: {follows_lxx}  NT follows MT/Hebrew: {follows_mt}")
    print(f"\n{'locus':30s} {'NT~LXX':>7}  NT follows")
    for r in rows:
        print(f"{r['locus']:30s} {str(r['nt_to_lxx_overlap']):>7}  {r['nt_follows']}")
    print("\nIsaiah 7:14 side by side:")
    iso = rows[0]
    print(f"  MT : {iso['mt_hebrew']}")
    print(f"  LXX: {iso['lxx_greek']}")
    print(f"  NT : {iso['nt_greek']}")
    print(OUT_DIR / "messianic_loci.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
