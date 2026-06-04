#!/usr/bin/env python3
"""Chronology test: does omission of presence-disputed NT verses track manuscript
date? Reads the CNTR MES transcriptions (data/raw/cntr, CC BY-SA 4.0, Bunning).

For each presence-disputed verse (some witness has text, some marks "-"), and each
dated manuscript that COVERS it (present or omitted, excluding lacunae), the verse
is present(1) or omitted(0). Aggregated by manuscript and by century bucket.

Hypothesis framing (pure data; interpretation noted, not asserted):
  - If the longer readings are later additions (scribal expansion), later
    manuscripts include them MORE -> omission rate DECREASES with date.
  - If original material was removed over time, omission rate would INCREASE with
    date.

Manuscript dates are standard paleographic century datings (INTF Kurzgefasste
Liste / NA28 / Aland, "The Text of the New Testament"), representative mid-century
years, century-level confidence. Only confidently-dated witnesses are scored;
others are reported as undated.

Outputs under reports/manuscript_omission_chronology/.
"""

from __future__ import annotations

import csv
import glob
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/manuscript_omission_chronology")
EDITIONS = {"RP", "WH", "SR", "KJTR", "ST", "NA", "TR", "BG"}

# Representative mid-century year per witness (standard paleographic datings).
MANUSCRIPT_DATES: dict[str, int] = {
    "P46": 200, "P66": 200, "P75": 200,            # c. 200 (II/III)
    "P45": 250, "P69": 250, "P47": 250, "P115": 250,  # III
    "0171": 300,                                    # III/IV
    "01": 350, "03": 350,                           # IV (Sinaiticus, Vaticanus)
    "05": 400, "032": 400,                          # IV/V (Bezae, Washingtonianus)
    "02": 450, "04": 450, "P19": 450,               # V (Alexandrinus, Ephraemi)
}


def century_bucket(year: int) -> str:
    if year <= 250:
        return "II-III (papyri, c.200-250)"
    if year <= 350:
        return "III-IV (c.300-350)"
    return "V (c.400-450)"


def load_statuses(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if len(line) >= 8 and line[:8].isdigit():
                code, body = line[:8], line[9:].strip()
                out[code] = "omitted" if body.startswith("-") else ("present" if body else "omitted")
    return out


def pearson(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 3:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    if sxx == 0 or syy == 0:
        return None
    return round(sxy / (sxx * syy) ** 0.5, 4)


def main() -> int:
    files = sorted(glob.glob(f"{CNTR_ROOT}/**/*.txt", recursive=True))
    if not files:
        raise SystemExit(f"no CNTR transcriptions under {CNTR_ROOT}")
    witnesses = {Path(p).stem: load_statuses(Path(p)) for p in files}

    # Disputed verses: some witness present, some omits.
    all_codes = {c for st in witnesses.values() for c in st}
    disputed = [c for c in all_codes
                if any(st.get(c) == "present" for st in witnesses.values())
                and any(st.get(c) == "omitted" for st in witnesses.values())]

    # Per-manuscript omission over covered disputed verses (dated witnesses only).
    rows = []
    for ms, year in MANUSCRIPT_DATES.items():
        st = witnesses.get(ms, {})
        covered = [c for c in disputed if c in st]
        omitted = [c for c in covered if st[c] == "omitted"]
        if not covered:
            continue
        rows.append({
            "manuscript": ms, "date": year, "century": century_bucket(year),
            "disputed_covered": len(covered), "disputed_omitted": len(omitted),
            "omission_rate": round(len(omitted) / len(covered), 4),
        })
    rows.sort(key=lambda r: (r["date"], r["manuscript"]))

    # Pooled omission rate by century bucket (weighted by coverage).
    buckets: dict[str, list[int]] = {}
    for r in rows:
        b = buckets.setdefault(r["century"], [0, 0])
        b[0] += r["disputed_omitted"]; b[1] += r["disputed_covered"]
    bucket_rows = [{"century": c, "omitted": o, "covered": cov,
                    "pooled_omission_rate": round(o / cov, 4) if cov else 0.0}
                   for c, (o, cov) in sorted(buckets.items())]

    corr = pearson([r["date"] for r in rows], [r["omission_rate"] for r in rows])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "by_manuscript.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with (OUT_DIR / "by_century.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(bucket_rows[0].keys())); w.writeheader(); w.writerows(bucket_rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "manuscript_omission_chronology", "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "disputed_verses": len(disputed), "dated_manuscripts_scored": len(rows),
        "date_basis": "standard paleographic century datings (INTF Liste / NA28 / Aland)",
        "pearson_date_vs_omission_rate": corr,
        "reading": "negative correlation = older witnesses omit more = longer readings accumulate over time",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"disputed verses: {len(disputed)}; dated manuscripts scored: {len(rows)}")
    print("\nomission rate by manuscript (oldest first):")
    print(f"  {'ms':6s} {'date':>4} {'cov':>4} {'omit':>4} {'rate':>6}")
    for r in rows:
        print(f"  {r['manuscript']:6s} {r['date']:>4} {r['disputed_covered']:>4} {r['disputed_omitted']:>4} {r['omission_rate']:>6}")
    print("\npooled omission rate by century (coverage-weighted):")
    for b in bucket_rows:
        print(f"  {b['century']:28s} omit {b['omitted']:>3} / cov {b['covered']:>3} = {b['pooled_omission_rate']}")
    print(f"\nPearson(date, omission_rate) = {corr}  (negative => older omit more => expansion over time)")
    print(OUT_DIR / "by_century.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
