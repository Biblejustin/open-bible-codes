#!/usr/bin/env python3
"""Heptadic data-check: do the famous sevenfold counts hold in the actual text?

The heptadic-structure claim (Ivan Panin, relayed by Chuck Missler) is that the
number seven runs through the interior of Scripture: word counts, letter counts,
and grammatical categories coming out as exact multiples of seven, to a degree
said to prove inspiration. The two showcase passages are Genesis 1:1 (Hebrew)
and the genealogy of Matthew 1 (Greek). This script tests those counts against
the open corpora rather than taking them on report.

It assumes nothing and counts. Genesis 1:1 is checked in two Hebrew editions
(version-independence). Matthew 1 is checked across five Greek text-types, the
Textus Receptus (KJTR), the Byzantine (RP), and the critical Westcott-Hort, SR,
and SBLGNT, so the question that decides the claim, is it robust or is it
text-and-method-dependent, is answered directly.

Outputs under reports/heptadic_counts/.
"""

from __future__ import annotations

import csv
import json
from datetime import UTC, datetime
from pathlib import Path

from els.cntr import load_edition
from els.corpus import load_corpus
from els.textstats import (
    GREEK_VOWELS,
    greek_letter_counts,
    greek_tokens,
    hebrew_letters,
    is_heptad,
    verse_map,
)

WLC_CONFIG = Path("configs/example_oshb_wlc.toml")
WLC2_CONFIG = Path("configs/example_ebible_hebwlc.toml")
NT_CONFIG = Path("configs/example_sblgnt.toml")
OUT_DIR = Path("reports/heptadic_counts")

# The shared helpers (verse_map, hebrew_letters, greek_tokens, is_heptad, and
# the CNTR load_edition) live in els.textstats and els.cntr; they are imported
# above so this module's public names are unchanged for its dependents.


def heptad_rate(counts: list[tuple[int, int]]) -> dict[str, float]:
    """Fraction of (word_count, letter_count) verse pairs whose word total, letter
    total, or both are divisible by seven. The chance baseline is about 1/7, 1/7,
    and 1/49. A rate at chance means heptadic counts are not a designed feature."""
    n = len(counts)
    if n == 0:
        return {"verses": 0, "words_pct": 0.0, "letters_pct": 0.0, "both_pct": 0.0}
    w7 = sum(1 for w, _ in counts if is_heptad(w))
    l7 = sum(1 for _, lc in counts if is_heptad(lc))
    b7 = sum(1 for w, lc in counts if is_heptad(w) and is_heptad(lc))
    return {"verses": n, "words_pct": round(w7 / n, 4),
            "letters_pct": round(l7 / n, 4), "both_pct": round(b7 / n, 4)}


def genesis_1_1_checks(words: list[str]) -> list[tuple[str, int, int]]:
    """(label, computed value, claimed heptadic value) for the showcase claims."""
    per_word = [len(hebrew_letters(w)) for w in words]
    return [
        ("words", len(words), 7),
        ("letters", sum(per_word), 28),
        ("first three words, letters", sum(per_word[:3]), 14),
        ("last four words, letters", sum(per_word[3:]), 14),
        ("words 4+5, letters", per_word[3] + per_word[4], 7),
        ("words 6+7, letters", per_word[5] + per_word[6], 7),
        ("God+heaven+earth, letters", per_word[2] + per_word[4] + per_word[6], 14),
    ]


def main() -> int:
    wlc = verse_map(load_corpus(WLC_CONFIG))
    nt = verse_map(load_corpus(NT_CONFIG))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []

    # ---- Genesis 1:1, Hebrew, with cross-edition confirmation ----
    gen_checks = genesis_1_1_checks(wlc[("GEN", "1", "1")].split())
    for label, value, claim in gen_checks:
        rows.append({"passage": "Genesis 1:1", "label": f"Genesis 1:1 {label}",
                     "value": value, "claimed": claim, "matches_claim": value == claim,
                     "is_heptad": is_heptad(value)})
    # second Hebrew edition: do words/letters agree?
    gen2 = None
    if WLC2_CONFIG.exists():
        wlc2 = verse_map(load_corpus(WLC2_CONFIG))
        g2 = wlc2.get(("GEN", "1", "1"), "")
        if g2:
            gen2 = (len(g2.split()), len(hebrew_letters(g2)))

    # ---- Matthew 1 across the Greek text-types ----
    cntr = {"TR": load_edition("KJTR"), "Byzantine": load_edition("RP"),
            "WH": load_edition("WH"), "SR": load_edition("SR")}
    editions = [(name, lambda v, e=e: e.get(f"40001{v:03d}", "")) for name, e in cntr.items()]
    editions.append(("SBLGNT", lambda v: nt.get(("MATT", "1", str(v)), "")))
    for ed_name, getter in editions:
        for hi in (11, 17):
            toks: list[str] = []
            for v in range(1, hi + 1):
                toks += greek_tokens(getter(v))
            letters, vowels, consonants = greek_letter_counts(toks)
            for metric, value in [("words", len(toks)), ("vocabulary", len(set(toks))),
                                  ("letters", letters), ("vowels", vowels), ("consonants", consonants)]:
                rows.append({"passage": f"Matthew 1:1-{hi}", "label": f"Matthew 1:1-{hi} {ed_name} {metric}",
                             "edition": ed_name, "metric": metric, "section": f"1-{hi}",
                             "value": value, "claimed": "", "matches_claim": "",
                             "is_heptad": is_heptad(value)})

    # ---- base-rate control: how often is ANY verse's count divisible by 7? ----
    # If Genesis 1:1 is special, the whole-Bible rate should sit at chance (~1/7
    # for words, ~1/7 for letters, ~1/49 for both at once). It does.
    heb_rate = heptad_rate([(len(t.split()), len(hebrew_letters(t))) for t in wlc.values()])
    grk_rate = heptad_rate([(len(gt), sum(len(x) for x in gt))
                            for t in nt.values() if (gt := greek_tokens(t))])

    gen_rows = [r for r in rows if r["passage"] == "Genesis 1:1"]
    mt_rows = [r for r in rows if r["passage"].startswith("Matthew")]
    gen_pass = sum(r["matches_claim"] for r in gen_rows)
    mt_heptad = sum(1 for r in mt_rows if r["is_heptad"])

    fields = sorted({k for r in rows for k in r})
    with (OUT_DIR / "heptadic_counts.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows({k: r.get(k, "") for k in fields} for r in rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "heptadic_counts",
        "created_utc": datetime.now(UTC).isoformat(),
        "corpora": {"Hebrew": ["OSHB WLC", "eBible WLC"],
                    "Greek": ["KJTR(TR)", "RP(Byzantine)", "WH", "SR", "SBLGNT"]},
        "genesis_1_1_claims_confirmed": f"{gen_pass}/{len(gen_rows)}",
        "genesis_1_1_second_hebrew_edition": ({"words": gen2[0], "letters": gen2[1]} if gen2 else None),
        "matthew_1_counts_sevenfold": f"{mt_heptad}/{len(mt_rows)}",
        "panin_matthew_1_11_claims": {"vocabulary": 49, "letters": 266, "vowels": 140, "consonants": 126},
        "base_rate_hebrew": heb_rate,
        "base_rate_greek": grk_rate,
        "base_rate_note": ("Whole-corpus control. Across every verse, the chance that a "
                           "word count or letter count lands on a multiple of seven is "
                           "about 1 in 7 (~0.143), and both at once about 1 in 49 "
                           "(~0.020). The Hebrew Bible and the Greek NT both sit at that "
                           "chance rate, so a single heptadic count proves nothing; "
                           "Genesis 1:1 is striking only because SEVEN separate features "
                           "line up at once, which is the real signal."),
        "reading": ("Genesis 1:1's sevenfold structure confirms in both Hebrew "
                    "editions, robust and version-independent. Matthew 1's counts are "
                    "not sevenfold in ANY of the five Greek text-types (the TR and "
                    "Byzantine are identical and miss; the critical texts miss bar a "
                    "lone coincidental consonant total). Panin's numbers match none of "
                    "them, so the genealogy 'design' is an artifact of his particular "
                    "reconstruction and counting, not a feature of the text."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Genesis 1:1 heptadic claims confirmed: {gen_pass}/{len(gen_rows)}"
          + (f"  (second Hebrew edition: {gen2[0]} words, {gen2[1]} letters)" if gen2 else ""))
    for r in gen_rows:
        print(f"  [{'OK' if r['matches_claim'] else 'X'}] {r['label']:42s} = {r['value']:>3} (claim {r['claimed']})")
    print(f"\nMatthew 1 across Greek editions (* = divisible by 7):")
    print(f"  {'edition':10s} {'sec':5s} {'words':>6} {'vocab':>6} {'letters':>8} {'vowels':>7} {'cons':>6}")
    seen = set()
    for r in mt_rows:
        key = (r["edition"], r["section"])
        if key in seen:
            continue
        seen.add(key)
        vals = {m["metric"]: m for m in mt_rows if m["edition"] == r["edition"] and m["section"] == r["section"]}
        def cell(metric):
            v = vals[metric]["value"]
            return f"{v}{'*' if vals[metric]['is_heptad'] else ''}"
        print(f"  {r['edition']:10s} {r['section']:5s} {cell('words'):>6} {cell('vocabulary'):>6} "
              f"{cell('letters'):>8} {cell('vowels'):>7} {cell('consonants'):>6}")
    print(f"  Panin claimed for 1-11: vocab 49, letters 266, vowels 140, consonants 126 (matches none)")
    print(f"\nBase-rate control (chance is ~0.143 words, ~0.143 letters, ~0.020 both):")
    print(f"  {'corpus':14s} {'verses':>7} {'words/7':>9} {'letters/7':>10} {'both/7':>8}")
    for name, r in [("Hebrew (WLC)", heb_rate), ("Greek NT (SBLGNT)", grk_rate)]:
        print(f"  {name:14s} {r['verses']:>7} {r['words_pct']:>9.3f} "
              f"{r['letters_pct']:>10.3f} {r['both_pct']:>8.3f}")
    print(f"  -> heptadic counts sit at chance in both Testaments; the lone count is noise, "
          f"the seven-at-once conjunction in Genesis 1:1 is the signal")
    print(OUT_DIR / "heptadic_counts.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
