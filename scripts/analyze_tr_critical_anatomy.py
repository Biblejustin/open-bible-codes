#!/usr/bin/env python3
"""Complete anatomy of the Textus Receptus vs the critical text (CNTR data).

Every famous variant (Mark 16, the Comma, 1Tim 3:16) is one entry in a much
larger ledger. This script builds the whole ledger: it walks every verse of the
New Testament and classifies the relationship between the Textus Receptus (KJTR,
the text behind the KJV) and the Westcott-Hort critical text (WH), so the marquee
variants can be seen in proportion to the thousands of small ones.

Categories per verse, after normalizing Greek (accents and punctuation stripped,
final sigma folded, so spelling and accent differences do not count):

  identical          both present, same words.
  alex_shorter       both present; the critical text drops words the TR has.
  alex_longer        both present; the critical text has words the TR lacks.
  substitution       both present; words are swapped, no net length change.
  mixed              both present; a combination of the above.
  alex_omits_verse   the TR has the whole verse; the critical text marks it absent.
  tr_omits_verse     the critical text has the whole verse; the TR lacks it.

Reported by category and by book, with token-delta totals (how many words the
critical text drops versus adds across all wording differences). Pure data over
the CNTR editions (CC BY-SA 4.0, Alan Bunning, data/raw/cntr). Outputs under
reports/tr_critical_anatomy/.
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path

from els.normalization import normalize_greek

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/tr_critical_anatomy")

NT_BOOK = {
    40: "Matt", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Rom",
    46: "1Cor", 47: "2Cor", 48: "Gal", 49: "Eph", 50: "Phil", 51: "Col",
    52: "1Thess", 53: "2Thess", 54: "1Tim", 55: "2Tim", 56: "Titus", 57: "Phlm",
    58: "Heb", 59: "Jas", 60: "1Pet", 61: "2Pet", 62: "1John", 63: "2John",
    64: "3John", 65: "Jude", 66: "Rev",
}
NT_ORDER = [NT_BOOK[k] for k in sorted(NT_BOOK)]

WORDING = ("alex_shorter", "alex_longer", "substitution", "mixed")
WHOLE_VERSE = ("alex_omits_verse", "tr_omits_verse")


def load_edition(siglum: str) -> dict[str, str]:
    for path in glob.glob(f"{CNTR_ROOT}/**/{siglum}.txt", recursive=True):
        out: dict[str, str] = {}
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if len(line) >= 8 and line[:8].isdigit():
                    out[line[:8]] = line[9:].rstrip("\n")
        return out
    raise SystemExit(f"edition {siglum} not found under {CNTR_ROOT}")


def is_present(edition: dict[str, str], code: str) -> bool:
    body = edition.get(code)
    return bool(body) and not body.startswith("-")


def norm_tokens(text: str) -> list[str]:
    return [w for tok in text.replace("¶", " ").split() if (w := normalize_greek(tok))]


def wording_type(tr: list[str], wh: list[str]) -> str:
    ops = set()
    for tag, _i1, _i2, _j1, _j2 in SequenceMatcher(None, tr, wh).get_opcodes():
        if tag != "equal":
            ops.add(tag)
    if ops == {"delete"}:
        return "alex_shorter"
    if ops == {"insert"}:
        return "alex_longer"
    if ops == {"replace"}:
        return "substitution"
    return "mixed"


def classify_pair(tr_present: bool, wh_present: bool,
                  tr_tokens: list[str], wh_tokens: list[str]) -> str:
    if tr_present and not wh_present:
        return "alex_omits_verse"
    if wh_present and not tr_present:
        return "tr_omits_verse"
    if not tr_present and not wh_present:
        return "both_absent"
    if tr_tokens == wh_tokens:
        return "identical"
    return wording_type(tr_tokens, wh_tokens)


def token_delta(tr: list[str], wh: list[str]) -> tuple[int, int]:
    """Tokens the critical text drops (TR-side) and adds (WH-side) at a wording diff."""
    dropped = added = 0
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, tr, wh).get_opcodes():
        if tag == "equal":
            continue
        dropped += i2 - i1
        added += j2 - j1
    return dropped, added


def book_of(code: str) -> str:
    return NT_BOOK.get(int(code[:2]), code[:2])


def main() -> int:
    kjtr, wh = load_edition("KJTR"), load_edition("WH")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    codes = sorted(set(kjtr) | set(wh))
    by_book: dict[str, Counter] = defaultdict(Counter)
    totals: Counter = Counter()
    dropped_total = added_total = 0
    for code in codes:
        tr_p, wh_p = is_present(kjtr, code), is_present(wh, code)
        tr_t = norm_tokens(kjtr.get(code, "")) if tr_p else []
        wh_t = norm_tokens(wh.get(code, "")) if wh_p else []
        cat = classify_pair(tr_p, wh_p, tr_t, wh_t)
        if cat == "both_absent":
            continue
        by_book[book_of(code)][cat] += 1
        totals[cat] += 1
        if cat in WORDING:
            d, a = token_delta(tr_t, wh_t)
            dropped_total += d
            added_total += a

    categories = ["identical", *WORDING, *WHOLE_VERSE]
    book_rows = []
    for book in NT_ORDER:
        c = by_book.get(book, Counter())
        verses = sum(c.values())
        differing = verses - c["identical"]
        row = {"book": book, "verses": verses, "differing": differing,
               "pct_differing": round(differing / verses, 4) if verses else 0.0}
        row.update({cat: c[cat] for cat in categories})
        book_rows.append(row)

    total_verses = sum(totals.values())
    total_diff = total_verses - totals["identical"]
    summary = [{"category": cat, "verses": totals[cat],
                "pct_of_all": round(totals[cat] / total_verses, 4) if total_verses else 0.0,
                "pct_of_differences": round(totals[cat] / total_diff, 4) if total_diff and cat != "identical" else ""}
               for cat in categories]

    with (OUT_DIR / "anatomy_by_book.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(book_rows[0].keys()))
        w.writeheader(); w.writerows(book_rows)
    with (OUT_DIR / "anatomy_summary.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=["category", "verses", "pct_of_all", "pct_of_differences"])
        w.writeheader(); w.writerows(summary)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "tr_critical_anatomy",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "editions": {"TR": "KJTR", "critical": "WH"},
        "total_verses": total_verses, "differing_verses": total_diff,
        "pct_verses_differing": round(total_diff / total_verses, 4) if total_verses else 0.0,
        "category_totals": dict(totals),
        "wording_token_delta": {"critical_dropped": dropped_total, "critical_added": added_total,
                                "net_dropped": dropped_total - added_total},
        "reading": ("Most verses are identical. Of the differing ones, the great "
                    "majority are small wording variants; whole-verse omissions are "
                    "a small slice. The net token delta shows the critical text is "
                    "shorter overall, the expansion-vs-removal question by volume."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"NT verses compared: {total_verses}   differing: {total_diff} "
          f"({round(100 * total_diff / total_verses, 1)}%)")
    print("\ncategory breakdown:")
    for s in summary:
        share = f"{s['pct_of_differences']:.1%}" if s["pct_of_differences"] != "" else "  -  "
        print(f"  {s['category']:18s} {s['verses']:>6}  {s['pct_of_all']:.3f} of all   {share} of differences")
    print(f"\nwording token delta: critical text drops {dropped_total}, adds {added_total} "
          f"(net {dropped_total - added_total} fewer words)")
    print("\nmost-divergent books (by % verses differing):")
    for r in sorted(book_rows, key=lambda r: r["pct_differing"], reverse=True)[:6]:
        print(f"  {r['book']:7s} {r['pct_differing']:.3f}  ({r['differing']}/{r['verses']})")
    print(OUT_DIR / "anatomy_summary.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
