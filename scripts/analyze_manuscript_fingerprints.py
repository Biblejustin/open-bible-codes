#!/usr/bin/env python3
"""Manuscript fingerprints: characterize each witness by behavior, not reputation.

Instead of taking "Alexandrian" or "Byzantine" as labels, this measures how each
dated uncial/papyrus actually behaves across every verse it covers, against the
Byzantine (RP) and Alexandrian-critical (WH) editions:

  byzantine_agreement  at verses where RP and WH word the text differently, how
                       often the manuscript's wording is closer to RP than to WH.
                       Near 0 = behaves Alexandrian; near 1 = behaves Byzantine.
  length_ratio         mean verse token-count relative to WH on shared verses;
                       > 1 = fuller text (Byzantine-like expansion).
  disputed_inclusion   of the disputed whole verses it covers, the share it
                       includes.

Pure data over the CNTR transcriptions (CC BY-SA 4.0, Alan Bunning,
data/raw/cntr). Outputs under reports/manuscript_fingerprints/.
"""

from __future__ import annotations

import csv
import glob
import json
from datetime import UTC, datetime
from difflib import SequenceMatcher
from pathlib import Path

from els.normalization import normalize_greek

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/manuscript_fingerprints")

MANUSCRIPT_DATES: dict[str, int] = {
    "P66": 200, "P75": 200, "P46": 200,
    "P45": 250, "P47": 250, "P115": 250,
    "01": 350, "03": 350,
    "05": 400, "032": 400,
    "02": 450, "04": 450,
}

MANUSCRIPT_NAMES = {
    "P66": "P66", "P75": "P75", "P46": "P46", "P45": "P45", "P47": "P47",
    "P115": "P115", "01": "Sinaiticus", "03": "Vaticanus", "05": "Bezae",
    "032": "Washingtonianus", "02": "Alexandrinus", "04": "Ephraemi",
}

# A few well-known disputed whole verses for the inclusion metric.
DISPUTED_VERSES = [
    "40017021", "40018011", "40023014", "41007016", "41009044", "41009046",
    "41011026", "41015028", "42017036", "42023017", "43005004", "44008037",
    "44015034", "44024007", "44028029", "45016024",
]


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


def norm_tokens(text: str) -> list[str]:
    return [w for tok in text.replace("¶", " ").split() if (w := normalize_greek(tok))]


def similarity(a: list[str], b: list[str]) -> float:
    return SequenceMatcher(None, a, b).ratio()


def classify_agreement(ms: list[str], rp: list[str], wh: list[str]) -> str:
    """Whether the manuscript's wording is closer to the Byzantine or the
    Alexandrian reading at a verse where the two editions differ."""
    s_rp, s_wh = similarity(ms, rp), similarity(ms, wh)
    if s_rp > s_wh:
        return "byzantine"
    if s_wh > s_rp:
        return "alexandrian"
    return "tie"


def main() -> int:
    rp, wh = load_witness("RP"), load_witness("WH")
    witnesses = {ms: load_witness(ms) for ms in MANUSCRIPT_DATES}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for ms, year in sorted(MANUSCRIPT_DATES.items(), key=lambda kv: (kv[1], kv[0])):
        w = witnesses[ms]
        byz = alex = tie = 0
        ms_len = wh_len = 0
        shared = 0
        for code, body in w.items():
            if not is_present(w, code) or not is_present(rp, code) or not is_present(wh, code):
                continue
            mt = norm_tokens(body)
            rt, ht = norm_tokens(rp[code]), norm_tokens(wh[code])
            shared += 1
            ms_len += len(mt)
            wh_len += len(ht)
            if rt == ht:
                continue  # editions agree: not diagnostic
            verdict = classify_agreement(mt, rt, ht)
            if verdict == "byzantine":
                byz += 1
            elif verdict == "alexandrian":
                alex += 1
            else:
                tie += 1
        diagnostic = byz + alex
        covered_disputed = [c for c in DISPUTED_VERSES if c in w]
        included_disputed = [c for c in covered_disputed if is_present(w, c)]
        rows.append({
            "manuscript": ms, "name": MANUSCRIPT_NAMES.get(ms, ms), "date": year,
            "diagnostic_verses": diagnostic,
            "byzantine_agreement": round(byz / diagnostic, 4) if diagnostic else "",
            "alexandrian_agreement": round(alex / diagnostic, 4) if diagnostic else "",
            "ties": tie,
            "length_ratio_vs_wh": round(ms_len / wh_len, 4) if wh_len else "",
            "shared_verses": shared,
            "disputed_covered": len(covered_disputed),
            "disputed_included": len(included_disputed),
            "disputed_inclusion_rate": (
                round(len(included_disputed) / len(covered_disputed), 4) if covered_disputed else ""),
        })

    with (OUT_DIR / "fingerprints.csv").open("w", encoding="utf-8", newline="") as h:
        writer = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "manuscript_fingerprints",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "method": "token-sequence similarity to RP vs WH at verses where they differ",
        "manuscripts": MANUSCRIPT_DATES,
        "reading": ("byzantine_agreement near 0 = behaves Alexandrian, near 1 = "
                    "Byzantine; length_ratio_vs_wh > 1 = fuller text. These are "
                    "behavioral measurements, not text-type labels."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'ms':5s} {'name':16s} {'date':>4} {'byz-agree':>9} {'len/WH':>7} {'disp-incl':>9} {'(diag)':>7}")
    for r in rows:
        print(f"{r['manuscript']:5s} {r['name']:16s} {r['date']:>4} "
              f"{str(r['byzantine_agreement']):>9} {str(r['length_ratio_vs_wh']):>7} "
              f"{str(r['disputed_inclusion_rate']):>9} {r['diagnostic_verses']:>7}")
    print(OUT_DIR / "fingerprints.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
