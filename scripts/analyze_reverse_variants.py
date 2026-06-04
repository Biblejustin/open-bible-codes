#!/usr/bin/env python3
"""Reverse cases: where the usual pattern flips (CNTR data).

The usual shape is TR/Byzantine longer, Alexandrian shorter. Two popular
corollaries ride on it: that "the Alexandrian text" is a single agenda, and that
the modern critical text just follows Vaticanus. Both are testable, and both
fail. This script measures the places the pattern reverses:

  Part A. Sinaiticus-vs-Vaticanus presence splits. Across every verse both
    cover, how often does one of the two great Alexandrian uncials include a
    verse the other omits? A single Alexandrian agenda would not split. The
    agony in Gethsemane (Luke 22:43-44) is the marquee case: Sinaiticus has it,
    Vaticanus does not.

  Part B. Where the critical text is SHORTER than Vaticanus. Verses Vaticanus
    carries but Westcott-Hort marks absent: the "Western non-interpolations,"
    where the editors followed the shorter Western text against their own
    flagship manuscript. The critical text is not simply Vaticanus.

  Part C. Matthew 27:49, the spear-thrust. Sinaiticus and Vaticanus carry a
    clause borrowed from John 19:34 (a soldier pierces Jesus' side BEFORE he
    dies); the critical text rejects it. Here the Alexandrian uncials are the
    longer, harmonizing text, and the critical text is shorter. Detected by the
    presence of the word for spear (lonche).

Pure data over the CNTR transcriptions (CC BY-SA 4.0, Alan Bunning,
data/raw/cntr). Outputs under reports/reverse_variants/.
"""

from __future__ import annotations

import csv
import glob
import json
from datetime import UTC, datetime
from pathlib import Path

from els.normalization import normalize_greek

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/reverse_variants")

NT_BOOK = {
    40: "Matt", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Rom",
    46: "1Cor", 47: "2Cor", 48: "Gal", 49: "Eph", 50: "Phil", 51: "Col",
    52: "1Thess", 53: "2Thess", 54: "1Tim", 55: "2Tim", 56: "Titus", 57: "Phlm",
    58: "Heb", 59: "Jas", 60: "1Pet", 61: "2Pet", 62: "1John", 63: "2John",
    64: "3John", 65: "Jude", 66: "Rev",
}


def load_witness(siglum: str) -> dict[str, str]:
    for path in glob.glob(f"{CNTR_ROOT}/**/{siglum}.txt", recursive=True):
        out: dict[str, str] = {}
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if len(line) >= 8 and line[:8].isdigit():
                    out[line[:8]] = line[9:].rstrip("\n")
        return out
    raise SystemExit(f"witness {siglum} not found under {CNTR_ROOT}")


def covers(witness: dict[str, str], code: str) -> bool:
    return code in witness


def is_present(witness: dict[str, str], code: str) -> bool:
    body = witness.get(code)
    return bool(body) and not body.startswith("-")


def has_token_stem(text: str, stem: str) -> bool:
    return any(normalize_greek(tok).startswith(stem) for tok in text.replace("¶", " ").split())


def fmt_ref(code: str) -> str:
    return f"{NT_BOOK.get(int(code[:2]), code[:2])} {int(code[2:5])}:{int(code[5:8])}"


def main() -> int:
    aleph, b, wh, kjtr = (load_witness(s) for s in ("01", "03", "WH", "KJTR"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Part A: Sinaiticus vs Vaticanus presence splits ----
    both_cover = [c for c in set(aleph) & set(b) if covers(aleph, c) and covers(b, c)]
    split_rows = []
    for c in sorted(both_cover):
        pa, pb = is_present(aleph, c), is_present(b, c)
        if pa != pb:
            split_rows.append({
                "ref": fmt_ref(c), "code": c,
                "sinaiticus": "present" if pa else "absent",
                "vaticanus": "present" if pb else "absent",
            })
    # how many disputed verses do they agree vs disagree on?
    both_codes = len(both_cover)

    # ---- Part B: critical text shorter than Vaticanus (Western non-interpolations) ----
    crit_shorter = []
    for c in sorted(set(b) & set(wh)):
        if is_present(b, c) and covers(wh, c) and not is_present(wh, c):
            crit_shorter.append({"ref": fmt_ref(c), "code": c,
                                 "vaticanus": "present", "critical_wh": "absent"})

    # ---- Part C: Matthew 27:49 spear-thrust (lonche) ----
    spear_code = "40027049"
    spear_rows = []
    for label, w in [("KJTR/TR", kjtr), ("WH/critical", wh),
                     ("Sinaiticus", aleph), ("Vaticanus", b)]:
        body = w.get(spear_code, "")
        spear_rows.append({
            "witness": label,
            "has_spear_clause": has_token_stem(body, "λογχη") if is_present(w, spear_code) else False,
        })

    with (OUT_DIR / "aleph_b_splits.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=["ref", "code", "sinaiticus", "vaticanus"])
        w.writeheader(); w.writerows(split_rows)
    with (OUT_DIR / "critical_shorter_than_vaticanus.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=["ref", "code", "vaticanus", "critical_wh"])
        w.writeheader(); w.writerows(crit_shorter)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "reverse_variants",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "aleph_b_codes_both_cover": both_codes,
        "aleph_b_presence_splits": len(split_rows),
        "critical_shorter_than_vaticanus": len(crit_shorter),
        "matthew_27_49_spear": {r["witness"]: r["has_spear_clause"] for r in spear_rows},
        "reading": ("Sinaiticus and Vaticanus split on presence in some verses, so "
                    "'the Alexandrian text' is not one agenda. The critical text is "
                    "shorter than Vaticanus in the Western non-interpolations, so it "
                    "does not simply follow Vaticanus. At Matt 27:49 the Alexandrian "
                    "uncials are the longer, harmonizing text and the critical text "
                    "is shorter."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Part A - Sinaiticus vs Vaticanus presence splits: {len(split_rows)} "
          f"(of {both_codes} verses both cover)")
    for r in split_rows[:12]:
        print(f"  {r['ref']:14s} Sinaiticus={r['sinaiticus']:8s} Vaticanus={r['vaticanus']}")
    print(f"\nPart B - critical text (WH) shorter than Vaticanus: {len(crit_shorter)} verses")
    for r in crit_shorter[:12]:
        print(f"  {r['ref']:14s} Vaticanus has it, critical text omits")
    print("\nPart C - Matt 27:49 spear-thrust clause (borrowed from John 19:34):")
    for r in spear_rows:
        print(f"  {r['witness']:14s} carries the spear clause: {r['has_spear_clause']}")
    print(OUT_DIR / "aleph_b_splits.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
