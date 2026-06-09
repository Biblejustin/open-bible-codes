#!/usr/bin/env python3
"""How much of the Greek Old Testament does the New Testament reproduce? (broad sweep)

The companion messianic analysis keys nine famous divergences. This widens the
lens: a fixed set of about forty New Testament quotations of the Old, each paired
with its Septuagint (LXX) source verse, scored by how much of the Greek verse the
New Testament reproduces in order (an ordered-recall measure, robust to the
"as it is written" framing the NT wraps a quotation in).

A high recall means the New Testament is quoting the Greek almost word for word.
A low recall means it diverges, either following the Hebrew (as at Hosea 11:1 and
Zechariah 12:10) or paraphrasing. The distribution puts a real number on the
common claim that the apostles quote overwhelmingly from the Greek.

Versification note: for the Psalms the LXX numbering runs one behind the Hebrew
in this range (Hebrew Psalm 110 is LXX Psalm 109), and a verse can shift by one
where the Hebrew counts the superscription. Each pair carries its own LXX
reference. Pure data over the eBible Greek LXX and the SBLGNT. Outputs under
reports/nt_lxx_quotation_overlap/.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path

from els.corpus import load_corpus
from els.textstats import verse_map
from els.normalization import normalize_greek

LXX_CONFIG = Path("configs/example_ebible_grclxx.toml")
NT_CONFIG = Path("configs/example_sblgnt.toml")
OUT_DIR = Path("reports/nt_lxx_quotation_overlap")

# (label, nt(book,ch,vs), lxx(book,ch,vs)). LXX Psalm refs already offset.
QUOTATIONS = [
    ("Matt 1:23 <- Isa 7:14", ("Matt", "1", "23"), ("ISA", "7", "14")),
    ("Matt 3:3 <- Isa 40:3", ("Matt", "3", "3"), ("ISA", "40", "3")),
    ("Matt 4:4 <- Deut 8:3", ("Matt", "4", "4"), ("DEU", "8", "3")),
    ("Matt 4:7 <- Deut 6:16", ("Matt", "4", "7"), ("DEU", "6", "16")),
    ("Matt 4:10 <- Deut 6:13", ("Matt", "4", "10"), ("DEU", "6", "13")),
    ("Matt 13:35 <- Ps 78:2", ("Matt", "13", "35"), ("PSA", "77", "2")),
    ("Matt 15:8 <- Isa 29:13", ("Matt", "15", "8"), ("ISA", "29", "13")),
    ("Matt 21:42 <- Ps 118:22", ("Matt", "21", "42"), ("PSA", "117", "22")),
    ("Matt 22:44 <- Ps 110:1", ("Matt", "22", "44"), ("PSA", "109", "1")),
    ("Matt 2:15 <- Hos 11:1 (MT)", ("Matt", "2", "15"), ("HOS", "11", "1")),
    ("Mark 1:3 <- Isa 40:3", ("Mark", "1", "3"), ("ISA", "40", "3")),
    ("Mark 12:36 <- Ps 110:1", ("Mark", "12", "36"), ("PSA", "109", "1")),
    ("Luke 4:18 <- Isa 61:1", ("Luke", "4", "18"), ("ISA", "61", "1")),
    ("John 12:38 <- Isa 53:1", ("John", "12", "38"), ("ISA", "53", "1")),
    ("John 19:37 <- Zech 12:10 (MT)", ("John", "19", "37"), ("ZEC", "12", "10")),
    ("Acts 2:25 <- Ps 16:8", ("Acts", "2", "25"), ("PSA", "15", "8")),
    ("Acts 2:31 <- Ps 16:10", ("Acts", "2", "31"), ("PSA", "15", "10")),
    ("Acts 8:32 <- Isa 53:7", ("Acts", "8", "32"), ("ISA", "53", "7")),
    ("Acts 13:33 <- Ps 2:7", ("Acts", "13", "33"), ("PSA", "2", "7")),
    ("Acts 15:17 <- Amos 9:12", ("Acts", "15", "17"), ("AMO", "9", "12")),
    ("Rom 1:17 <- Hab 2:4", ("Rom", "1", "17"), ("HAB", "2", "4")),
    ("Rom 4:3 <- Gen 15:6", ("Rom", "4", "3"), ("GEN", "15", "6")),
    ("Rom 9:17 <- Exod 9:16", ("Rom", "9", "17"), ("EXO", "9", "16")),
    ("Rom 10:11 <- Isa 28:16", ("Rom", "10", "11"), ("ISA", "28", "16")),
    ("Rom 11:34 <- Isa 40:13", ("Rom", "11", "34"), ("ISA", "40", "13")),
    ("Rom 15:12 <- Isa 11:10", ("Rom", "15", "12"), ("ISA", "11", "10")),
    ("1Cor 15:54 <- Isa 25:8", ("1Cor", "15", "54"), ("ISA", "25", "8")),
    ("2Cor 6:2 <- Isa 49:8", ("2Cor", "6", "2"), ("ISA", "49", "8")),
    ("Gal 3:11 <- Hab 2:4", ("Gal", "3", "11"), ("HAB", "2", "4")),
    ("Heb 1:6 <- Deut 32:43", ("Heb", "1", "6"), ("DEU", "32", "43")),
    ("Heb 1:7 <- Ps 104:4", ("Heb", "1", "7"), ("PSA", "103", "4")),
    ("Heb 1:8 <- Ps 45:6", ("Heb", "1", "8"), ("PSA", "44", "7")),
    ("Heb 3:7 <- Ps 95:7", ("Heb", "3", "7"), ("PSA", "94", "8")),
    ("Heb 10:5 <- Ps 40:6", ("Heb", "10", "5"), ("PSA", "39", "7")),
    ("Heb 13:6 <- Ps 118:6", ("Heb", "13", "6"), ("PSA", "117", "6")),
    ("Jas 2:23 <- Gen 15:6", ("Jas", "2", "23"), ("GEN", "15", "6")),
    ("Jas 4:6 <- Prov 3:34", ("Jas", "4", "6"), ("PRO", "3", "34")),
    ("1Pet 2:6 <- Isa 28:16", ("1Pet", "2", "6"), ("ISA", "28", "16")),
    ("1Pet 2:22 <- Isa 53:9", ("1Pet", "2", "22"), ("ISA", "53", "9")),
    ("1Pet 5:5 <- Prov 3:34", ("1Pet", "5", "5"), ("PRO", "3", "34")),
]


def lookup(vmap: dict, ref: tuple[str, str, str]) -> str:
    book, ch, vs = ref
    return vmap.get((book.upper(), ch, vs), "")


def greek_tokens(text: str) -> list[str]:
    return [w for tok in text.split() if (w := normalize_greek(tok))]


def ordered_recall(nt_text: str, lxx_text: str) -> float:
    """Fraction of the LXX verse's tokens reproduced, in order, in the NT verse.
    Robust to the NT's surrounding framing words."""
    nt, lx = greek_tokens(nt_text), greek_tokens(lxx_text)
    if not lx:
        return 0.0
    matched = sum(block.size for block in SequenceMatcher(None, nt, lx).get_matching_blocks())
    return round(matched / len(lx), 4)


def longest_common_run(nt_text: str, lxx_text: str) -> int:
    """Longest run of consecutive tokens shared between the NT and LXX verse. A
    long run is a verbatim Septuagint phrase, even when the NT quotes only part
    of a long LXX verse (so recall is low but the quotation is still the LXX)."""
    nt, lx = greek_tokens(nt_text), greek_tokens(lxx_text)
    blocks = SequenceMatcher(None, nt, lx).get_matching_blocks()
    return max((block.size for block in blocks), default=0)


def main() -> int:
    lxx = verse_map(load_corpus(LXX_CONFIG))
    nt = verse_map(load_corpus(NT_CONFIG))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for label, nt_ref, lxx_ref in QUOTATIONS:
        nt_text, lxx_text = lookup(nt, nt_ref), lookup(lxx, lxx_ref)
        rows.append({
            "quotation": label,
            "nt_ref": " ".join(nt_ref), "lxx_ref": " ".join(lxx_ref),
            "lxx_recall_in_nt": ordered_recall(nt_text, lxx_text) if (nt_text and lxx_text) else "",
            "longest_lxx_run": longest_common_run(nt_text, lxx_text) if (nt_text and lxx_text) else "",
            "found": bool(nt_text and lxx_text),
        })

    scored = [r["lxx_recall_in_nt"] for r in rows if isinstance(r["lxx_recall_in_nt"], float)]
    n = len(scored)
    mean = round(sum(scored) / n, 4) if n else 0.0
    ge70 = sum(1 for x in scored if x >= 0.70)
    ge50 = sum(1 for x in scored if x >= 0.50)
    lt30 = sum(1 for x in scored if x < 0.30)
    # "tracks the LXX" = reproduces most of the verse OR carries a verbatim 4+ token
    # Septuagint phrase (so short quotations of long verses still count).
    tracks = sum(1 for r in rows if isinstance(r["lxx_recall_in_nt"], float)
                 and (r["lxx_recall_in_nt"] >= 0.50 or r["longest_lxx_run"] >= 4))
    not_found = [r["quotation"] for r in rows if not r["found"]]

    with (OUT_DIR / "quotation_overlap.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "nt_lxx_quotation_overlap",
        "created_utc": datetime.now(UTC).isoformat(),
        "sources": {"LXX": "eBible Greek LXX", "NT": "SBLGNT"},
        "quotations_scored": n, "not_found": not_found,
        "mean_lxx_recall": mean,
        "recall_ge_0.70": ge70, "recall_ge_0.50": ge50, "recall_lt_0.30": lt30,
        "tracks_lxx": tracks,
        "reading": ("lxx_recall_in_nt is the share of the Septuagint verse the NT "
                    "reproduces in order; longest_lxx_run is the longest verbatim "
                    "Septuagint phrase in the NT verse. High recall means a close "
                    "quotation. Low recall is ambiguous: it can mean the NT follows "
                    "the Hebrew (Hosea 11:1 run 1, Zech 12:10 run 1) OR that it cites "
                    "a short phrase of a long LXX verse (Heb 1:6 recall 0.13 but a "
                    "verbatim run from the LXX). tracks_lxx counts quotations that "
                    "reproduce most of the verse OR carry a verbatim 4+ token LXX "
                    "phrase, the honest count of 'quotes the Greek.'"),
        "dead_sea_scrolls_note": (
            "A Dead Sea Scrolls analysis is not run here: no Qumran biblical text is "
            "in the corpus. Where the Scrolls bear on this (Deut 32:43 and 32:8, "
            "where a Hebrew Qumran copy sides with the LXX against the later "
            "Masoretic Text) that is well documented externally but not extracted "
            "from data in this project. Acquiring a DSS biblical text, as was done "
            "for the CNTR manuscripts, would make it a real analysis."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"quotations scored: {n}  (not found: {len(not_found)})")
    print(f"mean LXX recall: {mean}   recall>=0.70: {ge70}/{n}   >=0.50: {ge50}/{n}")
    print(f"tracks the LXX (most of verse, or verbatim 4+ token phrase): {tracks}/{n}")
    print("\nlowest-recall quotations (run = longest verbatim LXX phrase):")
    for r in sorted([r for r in rows if isinstance(r["lxx_recall_in_nt"], float)],
                    key=lambda r: r["lxx_recall_in_nt"])[:8]:
        tag = "follows Hebrew/paraphrase" if r["longest_lxx_run"] < 4 else "short cite of long LXX verse"
        print(f"  {r['quotation']:34s} recall {r['lxx_recall_in_nt']:<6} run {r['longest_lxx_run']:<2} ({tag})")
    if not_found:
        print("\nNOT FOUND (ref/versification to fix):", not_found)
    print(OUT_DIR / "quotation_overlap.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
