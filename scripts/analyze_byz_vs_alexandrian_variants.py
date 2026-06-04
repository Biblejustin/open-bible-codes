#!/usr/bin/env python3
"""Byzantine-vs-Alexandrian whole-verse presence/absence table from CNTR data.

Reads the Center for New Testament Restoration (CNTR) MES transcriptions
(data/raw/cntr, CC BY-SA 4.0, Alan Bunning) and reports, witness by witness,
every verse where the witnesses disagree on whether the verse is present.

Pure data: no doctrinal tagging, no interpretation. A verse line beginning with
'-' in MES means the witness marks that verse absent; anything else is text.

Witness roles (by convention in this data set):
  Byzantine/TR editions : RP (Robinson-Pierpont), KJTR, ST (Scrivener)
  Alexandrian/critical  : WH (Westcott-Hort), SR (Statistical Restoration)
  Manuscripts           : numeric Gregory-Aland sigla (01=Sinaiticus, 03=Vaticanus, ...)

Outputs:
  reports/byz_vs_alexandrian/verse_presence_matrix.csv  (every disagreement verse)
  reports/byz_vs_alexandrian/summary.csv
  reports/byz_vs_alexandrian/manifest.json
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/byz_vs_alexandrian")

BYZ_EDITIONS = ("RP", "KJTR", "ST")
ALEX_EDITIONS = ("WH", "SR")

NT_BOOK = {
    40: "Matt", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Rom",
    46: "1Cor", 47: "2Cor", 48: "Gal", 49: "Eph", 50: "Phil", 51: "Col",
    52: "1Thess", 53: "2Thess", 54: "1Tim", 55: "2Tim", 56: "Titus", 57: "Phlm",
    58: "Heb", 59: "Jas", 60: "1Pet", 61: "2Pet", 62: "1John", 63: "2John",
    64: "3John", 65: "Jude", 66: "Rev",
}


def fmt_ref(code: str) -> tuple[str, str, str, str]:
    book = NT_BOOK.get(int(code[:2]), code[:2])
    chapter, verse = str(int(code[2:5])), str(int(code[5:8]))
    return f"{book} {chapter}:{verse}", book, chapter, verse


def load_witness(path: Path) -> tuple[str, dict[str, str]]:
    """Return (siglum, {ref_code: 'text'|'absent'|<verse text>})."""
    siglum = path.stem
    status: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if len(line) >= 8 and line[:8].isdigit():
                code, body = line[:8], line[9:].strip()
                status[code] = "absent" if body.startswith("-") else body
    return siglum, status


def main() -> int:
    files = sorted(glob.glob(f"{CNTR_ROOT}/**/*.txt", recursive=True))
    if not files:
        raise SystemExit(f"no CNTR transcriptions under {CNTR_ROOT} (clone the CNTR repo first)")
    witnesses = dict(load_witness(Path(p)) for p in files)

    def is_manuscript(sig: str) -> bool:
        return sig[:1].isdigit() or sig[:1] in {"P", "L"}

    manuscripts = [s for s in witnesses if is_manuscript(s)]
    editions = [s for s in witnesses if not is_manuscript(s)]

    # Byzantine text for the readable column (first edition that has the verse).
    def byz_text(code: str) -> str:
        for ed in BYZ_EDITIONS:
            v = witnesses.get(ed, {}).get(code, "")
            if v and v != "absent":
                return v
        return ""

    # All verse codes anyone records.
    all_codes = sorted({c for st in witnesses.values() for c in st})

    rows = []
    for code in all_codes:
        present = [s for s, st in witnesses.items() if st.get(code, "") not in ("", "absent")]
        absent = [s for s, st in witnesses.items() if st.get(code, "") == "absent"]
        if not absent:
            continue  # no disagreement on presence
        byz_present = any(e in present for e in BYZ_EDITIONS)
        byz_absent = any(e in absent for e in BYZ_EDITIONS)
        alex_present = any(e in present for e in ALEX_EDITIONS)
        alex_absent = any(e in absent for e in ALEX_EDITIONS)
        if byz_present and alex_absent and not byz_absent:
            diff = "omitted_by_alexandrian"
        elif alex_present and byz_absent and not alex_absent:
            diff = "omitted_by_byzantine"
        else:
            diff = "split"
        ref, book, chapter, verse = fmt_ref(code)
        rows.append({
            "ref": ref, "book": book, "chapter": chapter, "verse": verse,
            "difference_type": diff,
            "byz_present": byz_present, "alex_present": alex_present,
            "absent_editions": ";".join(sorted(e for e in absent if e in editions)),
            "present_editions": ";".join(sorted(e for e in present if e in editions)),
            "manuscripts_absent": ";".join(sorted(s for s in absent if s in manuscripts)),
            "manuscripts_present": ";".join(sorted(s for s in present if s in manuscripts)),
            "byz_text": byz_text(code),
        })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    matrix_path = OUT_DIR / "verse_presence_matrix.csv"
    with matrix_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else ["ref"])
        writer.writeheader()
        writer.writerows(rows)

    diff_counts = Counter(r["difference_type"] for r in rows)
    by_book = Counter(r["book"] for r in rows if r["difference_type"] == "omitted_by_alexandrian")
    summary_rows = (
        [{"metric": f"difference_type:{k}", "value": v} for k, v in sorted(diff_counts.items())]
        + [{"metric": f"alexandrian_omits_in_book:{k}", "value": v} for k, v in by_book.most_common()]
        + [{"metric": "witnesses_total", "value": len(witnesses)},
           {"metric": "manuscripts", "value": len(manuscripts)},
           {"metric": "editions", "value": len(editions)},
           {"metric": "disagreement_verses", "value": len(rows)}]
    )
    summary_path = OUT_DIR / "summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["metric", "value"])
        writer.writeheader()
        writer.writerows(summary_rows)

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps({
        "tool": "byz_vs_alexandrian_variants",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "byzantine_editions": list(BYZ_EDITIONS),
        "alexandrian_editions": list(ALEX_EDITIONS),
        "witnesses": len(witnesses), "manuscripts": len(manuscripts), "editions": len(editions),
        "difference_counts": dict(diff_counts),
        "scope": "whole-verse presence/absence only; within-verse wording differences not included",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(matrix_path)
    print(summary_path)
    print(manifest_path)
    print(f"\nwitnesses={len(witnesses)} (mss={len(manuscripts)}, editions={len(editions)})")
    for k, v in sorted(diff_counts.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
