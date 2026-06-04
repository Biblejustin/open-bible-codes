#!/usr/bin/env python3
"""Within-verse Byzantine-vs-Alexandrian wording differences from CNTR data.

Word-level diff of the Byzantine edition (RP, Robinson-Pierpont) against the
Alexandrian-critical edition (WH, Westcott-Hort) across every verse both contain,
using the CNTR MES transcriptions (data/raw/cntr, CC BY-SA 4.0, Alan Bunning).

Pure data. Words are normalized with the project's Greek normalizer (accents and
punctuation stripped, lowercased, final sigma folded), so the diff reflects real
wording, not case or accent. "Direction" is reported objectively:

  - length: alex_shorter / alex_longer / substitution / mixed
  - divine-name gain/loss: which divine-name or Christological-title tokens appear
    in one edition's reading but not the other (theos, kyrios, iesous, christos,
    huios, pneuma forms). This is a factual flag, NOT a judgment that a reading
    "weakens" or "strengthens" anything; sort by it and read the verses yourself.

Whole-verse omissions are out of scope here (see analyze_byz_vs_alexandrian_variants).

Outputs:
  reports/byz_vs_alexandrian/wording_diff.csv      (one row per differing verse)
  reports/byz_vs_alexandrian/wording_divine.csv     (subset: divine-name changes)
  reports/byz_vs_alexandrian/wording_summary.csv
  reports/byz_vs_alexandrian/wording_manifest.json
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path

from els.normalization import normalize_greek

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/byz_vs_alexandrian")
BYZ, ALEX = "RP", "WH"

NT_BOOK = {
    40: "Matt", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Rom",
    46: "1Cor", 47: "2Cor", 48: "Gal", 49: "Eph", 50: "Phil", 51: "Col",
    52: "1Thess", 53: "2Thess", 54: "1Tim", 55: "2Tim", 56: "Titus", 57: "Phlm",
    58: "Heb", 59: "Jas", 60: "1Pet", 61: "2Pet", 62: "1John", 63: "2John",
    64: "3John", 65: "Jude", 66: "Rev",
}

# Divine-name / Christological-title forms. Run each through the same normalizer
# used on the text so final-sigma folding (ς->σ) matches (e.g. θεός -> θεοσ);
# otherwise the nominative forms (θεος, κυριος, ιησους, χριστος, υιος) silently
# miss. Membership is objective.
_DIVINE_FORMS = [
    "θεός", "θεοῦ", "θεῷ", "θεόν", "θεέ",
    "κύριος", "κυρίου", "κυρίῳ", "κύριον", "κύριε",
    "Ἰησοῦς", "Ἰησοῦ", "Ἰησοῦν",
    "Χριστός", "Χριστοῦ", "Χριστῷ", "Χριστόν", "Χριστέ",
    "υἱός", "υἱοῦ", "υἱῷ", "υἱόν", "υἱέ",
    "πνεῦμα", "πνεύματος", "πνεύματι", "πνεύματα",
]
DIVINE = {normalize_greek(form) for form in _DIVINE_FORMS}


def load_edition(siglum: str) -> dict[str, str]:
    for path in glob.glob(f"{CNTR_ROOT}/**/{siglum}.txt", recursive=True):
        out: dict[str, str] = {}
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if len(line) >= 8 and line[:8].isdigit():
                    code, body = line[:8], line[9:].strip()
                    if body and not body.startswith("-"):
                        out[code] = body
        return out
    raise SystemExit(f"edition {siglum} not found under {CNTR_ROOT}")


def norm_words(text: str) -> list[str]:
    out = []
    for tok in text.replace("¶", " ").split():
        w = normalize_greek(tok)
        if w:
            out.append(w)
    return out


def fmt_ref(code: str) -> tuple[str, str, str, str]:
    book = NT_BOOK.get(int(code[:2]), code[:2])
    return f"{book} {int(code[2:5])}:{int(code[5:8])}", book, str(int(code[2:5])), str(int(code[5:8]))


def diff_verse(byz_words: list[str], alex_words: list[str]) -> tuple[list[str], list[str], str]:
    byz_only, alex_only = [], []
    ops = set()
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, byz_words, alex_words).get_opcodes():
        if tag == "equal":
            continue
        ops.add(tag)
        byz_only.extend(byz_words[i1:i2])
        alex_only.extend(alex_words[j1:j2])
    if ops == {"delete"}:
        dtype = "alex_shorter"
    elif ops == {"insert"}:
        dtype = "alex_longer"
    elif ops == {"replace"}:
        dtype = "substitution"
    else:
        dtype = "mixed"
    return byz_only, alex_only, dtype


def main() -> int:
    byz, alex = load_edition(BYZ), load_edition(ALEX)
    shared = sorted(set(byz) & set(alex))
    rows, divine_rows = [], []
    identical = 0
    for code in shared:
        bw, aw = norm_words(byz[code]), norm_words(alex[code])
        if bw == aw:
            identical += 1
            continue
        byz_only, alex_only, dtype = diff_verse(bw, aw)
        d_byz = [w for w in byz_only if w in DIVINE]
        d_alex = [w for w in alex_only if w in DIVINE]
        ref, book, chapter, verse = fmt_ref(code)
        row = {
            "ref": ref, "book": book, "chapter": chapter, "verse": verse,
            "diff_type": dtype,
            "byz_words": len(bw), "alex_words": len(aw), "length_delta": len(aw) - len(bw),
            "byz_only": ";".join(byz_only), "alex_only": ";".join(alex_only),
            "divine_byz_only": ";".join(d_byz), "divine_alex_only": ";".join(d_alex),
            "byz_text": byz[code], "alex_text": alex[code],
        }
        rows.append(row)
        if d_byz or d_alex:
            divine_rows.append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else ["ref"]
    for name, data in [("wording_diff.csv", rows), ("wording_divine.csv", divine_rows)]:
        with (OUT_DIR / name).open("w", encoding="utf-8", newline="") as h:
            w = csv.DictWriter(h, fieldnames=fields); w.writeheader(); w.writerows(data)

    dtype_counts = Counter(r["diff_type"] for r in rows)
    summary = (
        [{"metric": "shared_verses", "value": len(shared)},
         {"metric": "identical_after_normalization", "value": identical},
         {"metric": "differing_verses", "value": len(rows)},
         {"metric": "verses_with_divine_name_change", "value": len(divine_rows)},
         {"metric": "divine_name_only_in_byzantine", "value": sum(1 for r in divine_rows if r["divine_byz_only"] and not r["divine_alex_only"])},
         {"metric": "divine_name_only_in_alexandrian", "value": sum(1 for r in divine_rows if r["divine_alex_only"] and not r["divine_byz_only"])}]
        + [{"metric": f"diff_type:{k}", "value": v} for k, v in sorted(dtype_counts.items())]
    )
    with (OUT_DIR / "wording_summary.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=["metric", "value"]); w.writeheader(); w.writerows(summary)

    (OUT_DIR / "wording_manifest.json").write_text(json.dumps({
        "tool": "byz_vs_alexandrian_wording",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "byzantine_edition": BYZ, "alexandrian_edition": ALEX,
        "normalization": "els.normalization.normalize_greek (accents/punct stripped, lowercased, final sigma folded)",
        "divine_name_forms": sorted(DIVINE),
        "shared_verses": len(shared), "differing_verses": len(rows),
        "scope": "within-verse wording only; whole-verse omissions excluded; divine-name flag is factual, not a doctrinal judgment",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"shared verses: {len(shared)}  identical(normalized): {identical}  differing: {len(rows)}")
    print(f"verses with a divine-name gain/loss: {len(divine_rows)}")
    for r in summary:
        if r["metric"].startswith(("divine_name_only", "diff_type")):
            print(f"  {r['metric']}: {r['value']}")
    print(OUT_DIR / "wording_diff.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
