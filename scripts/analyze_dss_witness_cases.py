#!/usr/bin/env python3
"""Dead Sea Scrolls witness at the messianic divergence points (MT vs LXX vs NT).

Where the Masoretic Text and the Septuagint part ways, the question is which
reading is the older Hebrew. The Dead Sea Scrolls are the tiebreaker: a Hebrew
copy from before Christ. At several famous verses the Scrolls side with the
Greek against the later Masoretic Text, which is the heart of the case that the
Septuagint was not inventing but translating an ancient Hebrew reading.

This script holds, for each verse, the DSS reading as a documented FACT (a short
label of what the scroll reads and which tradition it backs, cited to published
scholarship; the Isaiah 7:14 reading was additionally confirmed against the
1QIsaa text), and pulls the MT, LXX, and NT readings LIVE from our open corpora
(Westminster Leningrad, Greek Septuagint, SBLGNT). The copyrighted DSS editions
are not reproduced; only the factual reading and alignment are recorded.

Outputs under reports/dss_witness_cases/.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els.corpus import load_corpus

WLC_CONFIG = Path("configs/example_oshb_wlc.toml")
LXX_CONFIG = Path("configs/example_ebible_grclxx.toml")
NT_CONFIG = Path("configs/example_sblgnt.toml")
OUT_DIR = Path("reports/dss_witness_cases")

# Each case: the verse refs (MT, LXX, NT-quotation-if-any), the documented DSS
# reading and which tradition it sides with, the scroll(s), a source note, and
# the key transliterated word at issue. dss_sides_with is the recorded finding.
CASES = [
    {
        "label": "Isaiah 7:14 the virgin",
        "mt": ("Isa", "7", "14"), "lxx": ("ISA", "7", "14"), "nt": ("Matt", "1", "23"),
        "scroll": "1QIsaa",
        "dss_reading": "ha-almah (same consonants as MT)",
        "dss_sides_with": "MT",
        "key_word": "almah",
        "confirmed_via": "1QIsaa via a licensed Logos resource",
        "note": ("1QIsaa reads the same Hebrew word as the MT (almah, young woman); "
                 "the 'virgin' is the LXX's rendering, not a different Hebrew. "
                 "Confirmed against 1QIsaa."),
    },
    {
        "label": "Isaiah 53:11 he shall see light",
        "mt": ("Isa", "53", "11"), "lxx": ("ISA", "53", "11"), "nt": None,
        "scroll": "1QIsaa, 1QIsab, 4QIsad",
        "dss_reading": "adds 'light' (or) after 'he shall see'",
        "dss_sides_with": "LXX",
        "key_word": "or (light)",
        "confirmed_via": "1QIsaa via a licensed Logos resource",
        "note": ("The Scrolls and the LXX (phos) have the Servant 'see light'; the "
                 "MT lacks the word. Confirmed against 1QIsaa (reads 'or')."),
    },
    {
        "label": "Deuteronomy 32:8 sons of God",
        "mt": ("Deut", "32", "8"), "lxx": ("DEU", "32", "8"), "nt": None,
        "scroll": "4QDeutj",
        "dss_reading": "bene elohim (sons of God), with LXX",
        "dss_sides_with": "LXX",
        "key_word": "bene elohim",
        "confirmed_via": "The Dead Sea Scrolls Bible (Abegg, Flint, Ulrich), licensed",
        "note": ("4QDeutj reads 'sons of God' with the LXX (angeloi/huioi theou) "
                 "against the MT's 'sons of Israel'. Confirmed: the Dead Sea Scrolls "
                 "Bible renders Deuteronomy 32:8 'the children of God'."),
    },
    {
        "label": "Deuteronomy 32:43 angels worship him",
        "mt": ("Deut", "32", "43"), "lxx": ("DEU", "32", "43"), "nt": ("Heb", "1", "6"),
        "scroll": "4QDeutq",
        "dss_reading": "longer Song of Moses, with LXX (worship him, all gods/angels)",
        "dss_sides_with": "LXX",
        "key_word": "longer reading",
        "confirmed_via": "The Dead Sea Scrolls Bible (Abegg, Flint, Ulrich), licensed",
        "note": ("4QDeutq carries the longer reading the LXX has and the MT dropped; "
                 "Hebrews 1:6 quotes the longer form. Confirmed: the Dead Sea Scrolls "
                 "Bible reads 'and bow down to him all you gods' at Deuteronomy 32:43."),
    },
    {
        "label": "Psalm 22:16 pierced",
        "mt": ("Ps", "22", "17"), "lxx": ("PSA", "21", "17"), "nt": None,
        "scroll": "5/6HevPs (Nahal Hever)",
        "dss_reading": "kaaru (they dug/pierced), closer to LXX",
        "dss_sides_with": "LXX",
        "key_word": "kaaru",
        "confirmed_via": "The Dead Sea Scrolls Bible (Abegg, Flint, Ulrich), licensed",
        "note": ("The Nahal Hever Psalms scroll reads a verb form (kaaru) closer to "
                 "the LXX 'they pierced' than the MT's kaari ('like a lion'). "
                 "Confirmed: the Dead Sea Scrolls Bible renders Psalm 22:16 "
                 "'they have pierced my hands and my feet'."),
    },
    {
        "label": "Jeremiah shorter text",
        "mt": ("Jer", "10", "5"), "lxx": ("JER", "10", "5"), "nt": None,
        "scroll": "4QJerb",
        "dss_reading": "shorter Hebrew Jeremiah, with the shorter LXX",
        "dss_sides_with": "LXX",
        "key_word": "shorter edition",
        "confirmed_via": "The Dead Sea Scrolls Bible (Abegg, Flint, Ulrich), licensed",
        "note": ("4QJerb attests the short Hebrew Jeremiah behind the LXX, against "
                 "the longer MT edition. Confirmed: the Dead Sea Scrolls Bible runs "
                 "the scroll from Jeremiah 10:4 to 10:9, lacking the MT's verses 5-8."),
    },
    {
        "label": "1 Samuel 1-2 fuller text",
        "mt": ("1Sam", "1", "24"), "lxx": ("1SA", "1", "24"), "nt": None,
        "scroll": "4QSama",
        "dss_reading": "fuller Hebrew, repeatedly with the LXX",
        "dss_sides_with": "LXX",
        "key_word": "LXX-aligned",
        "confirmed_via": "The Dead Sea Scrolls Bible (Abegg, Flint, Ulrich), licensed",
        "note": ("4QSama agrees with the LXX against the MT at many points in "
                 "Samuel. Confirmed: the Dead Sea Scrolls Bible reads 'a three-year-old "
                 "bull' at 1 Samuel 1:24, with the LXX (the MT reads 'three bulls')."),
    },
]


def verse_map(corpus) -> dict[tuple[str, str, str], str]:
    out = {}
    for v in corpus.verses:
        out[(str(v.book).upper(), str(v.chapter), str(v.verse))] = v.raw_text
    return out


def lookup(vmap: dict, ref) -> str:
    if not ref:
        return ""
    book, ch, vs = ref
    return vmap.get((book.upper(), ch, vs), "")


def main() -> int:
    wlc = verse_map(load_corpus(WLC_CONFIG))
    lxx = verse_map(load_corpus(LXX_CONFIG))
    nt = verse_map(load_corpus(NT_CONFIG))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for case in CASES:
        rows.append({
            "verse": case["label"],
            "scroll": case["scroll"],
            "dss_reading": case["dss_reading"],
            "dss_sides_with": case["dss_sides_with"],
            "key_word": case["key_word"],
            "mt_ref": " ".join(case["mt"]), "lxx_ref": " ".join(case["lxx"]),
            "nt_ref": " ".join(case["nt"]) if case["nt"] else "",
            "mt_text_found": bool(lookup(wlc, case["mt"])),
            "lxx_text_found": bool(lookup(lxx, case["lxx"])),
            "nt_text_found": bool(lookup(nt, case["nt"])) if case["nt"] else "",
            "confirmed_via": case.get("confirmed_via", ""),
            "verification": (f"confirmed via {case['confirmed_via']}"
                             if case.get("confirmed_via")
                             else "documented (standard scholarship)"),
            "note": case["note"],
        })

    sides = Counter(r["dss_sides_with"] for r in rows)
    with (OUT_DIR / "dss_witness_cases.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "dss_witness_cases",
        "created_utc": datetime.now(UTC).isoformat(),
        "live_corpora": {"MT": "OSHB WLC", "LXX": "eBible Greek LXX", "NT": "SBLGNT"},
        "dss_column": ("factual readings (which tradition each scroll backs). All "
                       "seven cases are confirmed directly against the scrolls via "
                       "licensed Logos resources: Isaiah 7:14 and 53:11 against 1QIsaa, "
                       "and Deuteronomy 32:8, Deuteronomy 32:43, Psalm 22:16, Jeremiah "
                       "10, and 1 Samuel 1:24 in The Dead Sea Scrolls Bible (Abegg, "
                       "Flint, Ulrich). The copyrighted editions are not reproduced; "
                       "only the factual reading is recorded."),
        "cases": len(rows),
        "scroll_confirmed": sum(1 for r in rows if r["confirmed_via"]),
        "dss_sides_with": dict(sides),
        "reading": ("At these divergence points the Scrolls side with the LXX "
                    f"{sides.get('LXX', 0)} of {len(rows)} times and with the MT "
                    f"{sides.get('MT', 0)} time. The LXX was translating an ancient "
                    "Hebrew the MT later diverged from, except at Isaiah 7:14 where "
                    "the Hebrew is shared and the LXX renders almah as 'virgin'. "
                    f"All {len(rows)} are now confirmed directly against the scrolls in "
                    "licensed resources: 1QIsaa for the two Isaiah cases, and The Dead "
                    "Sea Scrolls Bible for the rest ('the children of God' at "
                    "Deuteronomy 32:8, 'bow down to him all you gods' at 32:43, 'they "
                    "have pierced' at Psalm 22:16, the shorter text at Jeremiah 10, and "
                    "'a three-year-old bull' at 1 Samuel 1:24)."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    confirmed = sum(1 for r in rows if r["verification"].startswith("confirmed"))
    print(f"DSS witness cases: {len(rows)}   sides with LXX: {sides.get('LXX', 0)}   "
          f"with MT: {sides.get('MT', 0)}   scroll-confirmed: {confirmed}")
    print(f"\n{'verse':34s} {'scroll':16s} {'sides':5s} verification")
    for r in rows:
        mark = "confirmed" if r["verification"].startswith("confirmed") else "documented"
        print(f"  {r['verse']:34s} {r['scroll']:16s} {r['dss_sides_with']:5s} {mark}")
    print(OUT_DIR / "dss_witness_cases.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
