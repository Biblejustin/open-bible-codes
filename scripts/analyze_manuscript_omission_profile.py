#!/usr/bin/env python3
"""Per-manuscript omission profile for presence-disputed NT verses (CNTR).

For every verse where the witnesses disagree on presence (at least one has text,
at least one marks it absent with MES "-"), report each manuscript's status:

  present       - the manuscript contains the verse text
  omitted       - the manuscript marks the verse absent ("-"); the scribe did
                  not write it (a real omission)
  not_covered   - the manuscript has no line for the verse (fragmentary / outside
                  its scope); silent, not evidence either way

This separates omission from lacuna, the distinction that matters for "is the
omission concentrated in particular manuscripts." Editions (RP/WH/SR/KJTR/ST)
define the disputed set and are reported separately from manuscripts.

Pure data. Source: CNTR MES transcriptions (data/raw/cntr, CC BY-SA 4.0, Bunning).
Outputs under reports/manuscript_omission_profile/.
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from els.books import CNTR_BOOK_CODES

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/manuscript_omission_profile")
EDITIONS = {"RP", "WH", "SR", "KJTR", "ST", "NA", "TR", "BG"}


def load_statuses(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if len(line) >= 8 and line[:8].isdigit():
                code, body = line[:8], line[9:].strip()
                out[code] = "omitted" if body.startswith("-") else ("present" if body else "omitted")
    return out


def fmt_ref(code: str) -> str:
    return f"{CNTR_BOOK_CODES.get(int(code[:2]), code[:2])} {int(code[2:5])}:{int(code[5:8])}"


def main() -> int:
    files = sorted(glob.glob(f"{CNTR_ROOT}/**/*.txt", recursive=True))
    if not files:
        raise SystemExit(f"no CNTR transcriptions under {CNTR_ROOT}")
    witnesses = {Path(p).stem: load_statuses(Path(p)) for p in files}

    def is_ms(sig: str) -> bool:
        return sig not in EDITIONS and (sig[:1].isdigit() or sig[:1] in {"P", "L"})

    manuscripts = sorted(s for s in witnesses if is_ms(s))

    # Disputed = some witness present, some witness omits (covering it either way).
    all_codes = {c for st in witnesses.values() for c in st}
    disputed = []
    for code in all_codes:
        statuses = [st[code] for st in witnesses.values() if code in st]
        if "present" in statuses and "omitted" in statuses:
            disputed.append(code)
    disputed.sort()

    # Per-verse manuscript attestation.
    verse_rows = []
    for code in disputed:
        present = [m for m in manuscripts if witnesses[m].get(code) == "present"]
        omitted = [m for m in manuscripts if witnesses[m].get(code) == "omitted"]
        verse_rows.append({
            "ref": fmt_ref(code),
            "ms_present_count": len(present), "ms_omitted_count": len(omitted),
            "ms_present": ";".join(present), "ms_omitted": ";".join(omitted),
            "editions_present": ";".join(e for e in sorted(EDITIONS) if witnesses.get(e, {}).get(code) == "present"),
            "editions_omitted": ";".join(e for e in sorted(EDITIONS) if witnesses.get(e, {}).get(code) == "omitted"),
        })

    # Per-manuscript omission rate over the disputed verses it covers.
    ms_rows = []
    for m in manuscripts:
        covered = [c for c in disputed if c in witnesses[m]]
        omits = [c for c in covered if witnesses[m][c] == "omitted"]
        if not covered:
            continue
        ms_rows.append({
            "manuscript": m, "disputed_covered": len(covered), "disputed_omitted": len(omits),
            "omission_rate": round(len(omits) / len(covered), 4),
            "omitted_refs": ";".join(fmt_ref(c) for c in omits),
        })
    ms_rows.sort(key=lambda r: (-r["omission_rate"], -r["disputed_covered"]))

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "by_verse.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(verse_rows[0].keys())); w.writeheader(); w.writerows(verse_rows)
    with (OUT_DIR / "by_manuscript.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(ms_rows[0].keys())); w.writeheader(); w.writerows(ms_rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "manuscript_omission_profile", "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "disputed_verses": len(disputed), "manuscripts": len(manuscripts),
        "status_definitions": {"present": "verse text present", "omitted": "MES '-' absent marker",
                               "not_covered": "no line (fragmentary/out of scope)"},
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"disputed verses (some witness present, some omit): {len(disputed)}")
    print(f"manuscripts covering >=1 disputed verse: {len(ms_rows)}")
    print("\nmanuscript omission rate over disputed verses it covers (top 12):")
    print(f"  {'ms':6s} {'covered':>7} {'omitted':>7} {'rate':>6}")
    for r in ms_rows[:12]:
        print(f"  {r['manuscript']:6s} {r['disputed_covered']:>7} {r['disputed_omitted']:>7} {r['omission_rate']:>6}")
    print("\n", OUT_DIR / "by_manuscript.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
