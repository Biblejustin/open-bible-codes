#!/usr/bin/env python3
"""Harmonization: are the fuller Byzantine/TR readings imported from parallels? (CNTR)

The expansion finding says the longer readings grew over time. One well-known
mechanism is harmonization: a scribe copying Luke, who knows Matthew by heart,
fills Luke's wording out to match Matthew's. This script tests a fixed set of
classic harmonization loci against the data. For each, a harmonizing phrase is
identified by a distinctive word, and the script checks three things:

  the TR has the phrase at the target verse,
  Westcott-Hort LACKS it at the target verse,
  the PARALLEL source passage genuinely contains the phrase.

When all three hold, the TR reading is the parallel's wording transplanted into
the target: a harmonization, confirmed from the data rather than asserted.

Pure data over the CNTR editions (CC BY-SA 4.0, Alan Bunning, data/raw/cntr).
Outputs under reports/harmonization/.
"""

from __future__ import annotations

import csv
import glob
import json
from datetime import UTC, datetime
from pathlib import Path

from els.normalization import normalize_greek

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/harmonization")

# target_code, target_label, source_code, source_label, phrase_stem, gloss
HARMONIZATIONS = [
    ("42011002", "Luke 11:2", "40006010", "Matt 6:10", "θελημ", "thy will be done, as in heaven"),
    ("42011004", "Luke 11:4", "40006013", "Matt 6:13", "ρυσ", "but deliver us from evil"),
    ("41013014", "Mark 13:14", "40024015", "Matt 24:15", "δανιη", "spoken of by Daniel the prophet"),
    ("40017021", "Matt 17:21", "41009029", "Mark 9:29", "νηστει", "this kind comes out by prayer and fasting"),
    ("51001014", "Col 1:14", "49001007", "Eph 1:7", "αιματ", "redemption through his blood"),
    ("42004004", "Luke 4:4", "40004004", "Matt 4:4", "ρηματ", "but by every word of God"),
    ("41006011", "Mark 6:11", "40010015", "Matt 10:15", "σοδομ", "more tolerable for Sodom and Gomorrha"),
    ("40018011", "Matt 18:11", "42019010", "Luke 19:10", "απολωλ", "Son of Man came to save the lost"),
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


def has_token_stem(text: str, stem: str) -> bool:
    return any(normalize_greek(tok).startswith(stem) for tok in text.replace("¶", " ").split())


def classify(tr_target: bool, wh_target: bool, source_has: bool) -> str:
    """Verdict for one locus from the three booleans."""
    if tr_target and not wh_target and source_has:
        return "byzantine_harmonization"
    if tr_target and wh_target:
        return "both_have_phrase"
    if not tr_target and not wh_target:
        return "neither_has_phrase"
    return "other"


def main() -> int:
    kjtr, wh, rp = (load_witness(s) for s in ("KJTR", "WH", "RP"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for tcode, tlabel, scode, slabel, stem, gloss in HARMONIZATIONS:
        tr_t = is_present(kjtr, tcode) and has_token_stem(kjtr[tcode], stem)
        wh_t = is_present(wh, tcode) and has_token_stem(wh[tcode], stem)
        rp_t = is_present(rp, tcode) and has_token_stem(rp[tcode], stem)
        # source: present in either edition's parallel verse
        src = ((is_present(kjtr, scode) and has_token_stem(kjtr[scode], stem))
               or (is_present(wh, scode) and has_token_stem(wh[scode], stem)))
        rows.append({
            "target": tlabel, "target_code": tcode,
            "parallel_source": slabel, "phrase": gloss, "phrase_stem": stem,
            "tr_has_at_target": tr_t, "byz_rp_has_at_target": rp_t,
            "wh_has_at_target": wh_t, "source_has_phrase": src,
            "verdict": classify(tr_t, wh_t, src),
        })

    confirmed = sum(r["verdict"] == "byzantine_harmonization" for r in rows)

    with (OUT_DIR / "harmonization_loci.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "harmonization",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "loci_tested": len(rows),
        "confirmed_byzantine_harmonizations": confirmed,
        "reading": ("byzantine_harmonization = the TR carries a distinctive phrase "
                    "at the target verse that WH lacks and that the parallel passage "
                    "genuinely contains, i.e. the parallel's wording transplanted in."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"harmonization loci tested: {len(rows)}  confirmed: {confirmed}")
    print(f"{'target':12s} {'<- parallel':14s} {'TR':>3} {'Byz':>4} {'WH':>3} {'src':>4}  verdict")
    for r in rows:
        print(f"{r['target']:12s} {r['parallel_source']:14s} "
              f"{str(r['tr_has_at_target'])[0]:>3} {str(r['byz_rp_has_at_target'])[0]:>4} "
              f"{str(r['wh_has_at_target'])[0]:>3} {str(r['source_has_phrase'])[0]:>4}  {r['verdict']}")
    print(OUT_DIR / "harmonization_loci.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
