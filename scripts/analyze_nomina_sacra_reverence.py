#!/usr/bin/env python3
"""Nomina sacra: do the earliest manuscripts revere Christ's divine titles? (CNTR)

A different angle on the same question. The omission and wording analyses ask
what the Alexandrian text leaves out. This asks how the earliest scribes wrote
what they DID keep. From the second century, Christian copyists marked the
sacred names with a contraction and an overline, the nomina sacra: God (ΘΣ),
Lord (ΚΣ), Jesus (ΙΣ), Christ (ΧΣ), Son (ΥΣ), Spirit, Father. It is a mark of
reverence reserved for the divine.

The test: at the passages where a divine title is applied to JESUS (John 1:1
"the Word was God", John 20:28 Thomas's "my Lord and my God", Romans 9:5
"Christ ... God over all", Titus 2:13, Hebrews 1:8), do the very manuscripts
accused of lowering Christ write those titles as nomina sacra? And across their
whole text, how consistently do they contract the divine names at all?

The CNTR MES transcriptions encode a nomen sacrum with "=" before the contracted
letters (e.g. "=θσ" for ΘΣ). This reads them straight from the data
(CC BY-SA 4.0, Alan Bunning, data/raw/cntr). Outputs under
reports/nomina_sacra_reverence/.
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/nomina_sacra_reverence")

MANUSCRIPT_DATES: dict[str, int] = {
    "P66": 200, "P75": 200, "P46": 200,
    "P45": 250, "P47": 250, "P115": 250,
    "01": 350, "03": 350,
    "05": 400, "032": 400,
    "02": 450, "04": 450,
}

# Core divine names tracked, with their full-form prefixes (spelled out).
FULL_PREFIXES = {
    "THEOS": ("θεο", "θεε"),
    "KYRIOS": ("κυρι",),
    "IESOUS": ("ιησ",),
    "CHRISTOS": ("χριστ",),
    "HUIOS": ("υιο", "υιε"),
}
CORE_NAMES = list(FULL_PREFIXES)

# Passages where a divine title is applied to Christ. expected = the deity-
# asserting title(s) we check are written sacred.
# expected = the deity-asserting title(s) we check are written sacred. Where a
# verse has the theos/kyrios variant (Acts 20:28, 2Pet 1:1), either title is a
# sacred divine name applied to Christ, so both count.
CHRIST_DEITY_VERSES = [
    ("43001001", "John 1:1 the Word was God", ("THEOS",)),
    ("43001018", "John 1:18 only-begotten God", ("THEOS",)),
    ("43020028", "John 20:28 my Lord and my God", ("KYRIOS", "THEOS")),
    ("46008006", "1Cor 8:6 one Lord Jesus Christ", ("KYRIOS",)),
    ("45009005", "Rom 9:5 Christ, God over all", ("THEOS",)),
    ("50002006", "Phil 2:6 in the form of God", ("THEOS",)),
    ("56002013", "Titus 2:13 great God and Savior", ("THEOS",)),
    ("61001001", "2Pet 1:1 God and Savior Jesus Christ", ("THEOS", "KYRIOS")),
    ("58001008", "Heb 1:8 thy throne, O God (to the Son)", ("THEOS",)),
    ("44020028", "Acts 20:28 the church of God", ("THEOS", "KYRIOS")),
]

_MARKUP = str.maketrans("", "", "/\\|¶+^~%&*{}=0123456789x")


def load_witness(siglum: str) -> dict[str, str]:
    for path in glob.glob(f"{CNTR_ROOT}/**/{siglum}.txt", recursive=True):
        out: dict[str, str] = {}
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if len(line) >= 8 and line[:8].isdigit():
                    out[line[:8]] = line[9:].rstrip("\n")
        return out
    raise SystemExit(f"witness {siglum} not found under {CNTR_ROOT}")


def is_present(witness: dict[str, str], code: str) -> bool:
    body = witness.get(code)
    return bool(body) and not body.startswith("-")


def raw_tokens(text: str) -> list[str]:
    for ch in "¶/\\|":
        text = text.replace(ch, " ")
    return text.split()


def bare(token: str) -> str:
    return token.translate(_MARKUP)


def is_nomen_sacrum(token: str) -> bool:
    return "=" in token


def nomen_sacrum_name(bare_form: str) -> str | None:
    """Classify a (bare) nomen sacrum contraction into a core divine name.
    Only meaningful for tokens that are nomina sacra; the contraction is short."""
    if not bare_form:
        return None
    first = bare_form[0]
    if first == "θ":
        return "THEOS"
    if first == "κ":
        return "KYRIOS"
    if first == "ι":
        return "IESOUS"
    if first == "χ":
        return "CHRISTOS"
    if first == "υ":
        return "HUIOS"
    return None  # other nomina sacra (Spirit, Father, Savior, cross ...) not tracked here


def full_name(bare_form: str) -> str | None:
    """Classify a spelled-out (non-contracted) token as a core divine name."""
    for name, prefixes in FULL_PREFIXES.items():
        if bare_form.startswith(prefixes):
            return name
    return None


def verse_nomina_sacra(text: str) -> set[str]:
    """Core divine names written as nomina sacra in one verse."""
    found = set()
    for token in raw_tokens(text):
        if is_nomen_sacrum(token):
            name = nomen_sacrum_name(bare(token))
            if name:
                found.add(name)
    return found


def count_forms(witness: dict[str, str]) -> dict[str, dict[str, int]]:
    """Per core divine name, count nomen-sacrum vs spelled-out occurrences."""
    counts = {name: {"nomen_sacrum": 0, "full": 0} for name in CORE_NAMES}
    for body in witness.values():
        if not body or body.startswith("-"):
            continue
        for token in raw_tokens(body):
            b = bare(token)
            if not b:
                continue
            if is_nomen_sacrum(token):
                name = nomen_sacrum_name(b)
                if name:
                    counts[name]["nomen_sacrum"] += 1
            else:
                name = full_name(b)
                if name:
                    counts[name]["full"] += 1
    return counts


def main() -> int:
    witnesses = {ms: load_witness(ms) for ms in MANUSCRIPT_DATES}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Part A: Christ-deity passages ----
    deity_rows = []
    for code, label, expected in CHRIST_DEITY_VERSES:
        for ms, year in sorted(MANUSCRIPT_DATES.items(), key=lambda kv: (kv[1], kv[0])):
            if not is_present(witnesses[ms], code):
                continue
            found = verse_nomina_sacra(witnesses[ms][code])
            deity_rows.append({
                "ref": label, "code": code, "manuscript": ms, "date": year,
                "expected_title": "+".join(expected),
                "nomina_sacra_found": "+".join(sorted(found)) or "(none)",
                "christ_title_sacred": any(t in found for t in expected),
            })

    # ---- Part B: contraction consistency per manuscript ----
    rate_rows = []
    for ms, year in sorted(MANUSCRIPT_DATES.items(), key=lambda kv: (kv[1], kv[0])):
        counts = count_forms(witnesses[ms])
        row = {"manuscript": ms, "date": year}
        for name in CORE_NAMES:
            ns, full = counts[name]["nomen_sacrum"], counts[name]["full"]
            total = ns + full
            row[f"{name}_ns"] = ns
            row[f"{name}_full"] = full
            row[f"{name}_rate"] = round(ns / total, 4) if total else ""
        rate_rows.append(row)

    # Part A summary: share of (verse, witness) cells where the deity title is sacred
    sacred_cells = sum(r["christ_title_sacred"] for r in deity_rows)
    total_cells = len(deity_rows)

    with (OUT_DIR / "christ_deity_nomina_sacra.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(deity_rows[0].keys()))
        w.writeheader(); w.writerows(deity_rows)
    with (OUT_DIR / "contraction_rates.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rate_rows[0].keys()))
        w.writeheader(); w.writerows(rate_rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "nomina_sacra_reverence",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "manuscripts": MANUSCRIPT_DATES,
        "core_names": CORE_NAMES,
        "christ_deity_verses": [v[1] for v in CHRIST_DEITY_VERSES],
        "christ_title_sacred_cells": f"{sacred_cells}/{total_cells}",
        "reading": ("christ_title_sacred is True when the divine title the verse "
                    "applies to Jesus is written as a nomen sacrum. High THEOS_rate "
                    "everywhere, with no Alexandrian-vs-other gap, means the earliest "
                    "scribes revered the divine names uniformly."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Part A - Christ-deity titles written as nomina sacra: "
          f"{sacred_cells}/{total_cells} (witness, verse) cells")
    by_verse: dict[str, Counter] = {}
    for r in deity_rows:
        by_verse.setdefault(r["ref"], Counter())["sacred" if r["christ_title_sacred"] else "not"] += 1
    for ref, c in by_verse.items():
        print(f"  {ref:42s} sacred in {c['sacred']}/{c['sacred'] + c['not']} witnesses")
    print("\nPart B - divine-name nomen-sacrum contraction rate per manuscript:")
    print(f"  {'ms':5s} {'date':>4}  " + "  ".join(f"{n[:5]:>6}" for n in CORE_NAMES))
    for r in rate_rows:
        print(f"  {r['manuscript']:5s} {r['date']:>4}  "
              + "  ".join(f"{str(r[f'{n}_rate']):>6}" for n in CORE_NAMES))
    print(OUT_DIR / "christ_deity_nomina_sacra.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
