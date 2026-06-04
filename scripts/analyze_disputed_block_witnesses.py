#!/usr/bin/env python3
"""Witness-level presence of disputed multi-verse BLOCKS (CNTR data).

The single-verse and wording analyses cover small variants. This one takes the
famous disputed passages that are whole blocks (the woman taken in adultery, the
longer ending of Mark, the agony in Gethsemane, the angel at Bethesda) and lays
out, verse by verse, which editions and which dated witnesses carry them, so the
blocks can be compared on the same footing.

The point it surfaces: these blocks are NOT textually equal. The Pericope
Adulterae is carried by only one early majuscule (Bezae); Mark's longer ending
is omitted by only Sinaiticus and Vaticanus and is present in Alexandrinus,
Ephraemi, Bezae, and Washingtonianus. "Disputed" is not one category.

Pure data over the CNTR editions and dated uncials/papyri (CC BY-SA 4.0, Alan
Bunning, data/raw/cntr). Per-block "note" fields carry documented external
context (the Pericope's floating location, the Mark double-ending, the
Alexandrinus/Ephraemi space calculations); those are labelled as scholarly
background, NOT derived from this verse-keyed dataset, which cannot show
relocation. Outputs under reports/disputed_block_witnesses/.
"""

from __future__ import annotations

import csv
import glob
import json
from datetime import UTC, datetime
from pathlib import Path

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/disputed_block_witnesses")

MANUSCRIPT_DATES: dict[str, int] = {
    "P46": 200, "P66": 200, "P75": 200,
    "P45": 250, "P69": 250, "P47": 250, "P115": 250,
    "0171": 300,
    "01": 350, "03": 350,
    "05": 400, "032": 400,
    "02": 450, "04": 450, "P19": 450,
}


def block_codes(book: int, chapter: int, v1: int, v2: int) -> list[str]:
    return [f"{book:02d}{chapter:03d}{v:03d}" for v in range(v1, v2 + 1)]


BLOCKS = [
    {
        "id": "pericope_adulterae",
        "label": "Pericope Adulterae (woman taken in adultery)",
        "ref": "John 7:53-8:11",
        "theme": "mercy and forgiveness",
        "codes": ["43007053", *block_codes(43, 8, 1, 11)],
        "note": ("Floats in the tradition: family 13 places it after Luke 21:38, "
                 "other witnesses after John 21:25 or 7:36, a classic sign of a "
                 "later insertion; its vocabulary and style are non-Johannine. "
                 "Alexandrinus and Ephraemi are lacunose here, but page-space "
                 "calculations indicate they did not contain it. (External context.)"),
    },
    {
        "id": "mark_longer_ending",
        "label": "Longer ending of Mark",
        "ref": "Mark 16:9-20",
        "theme": "resurrection appearances and commission",
        "codes": block_codes(41, 16, 9, 20),
        "note": ("Omitted by Sinaiticus and Vaticanus but present in Alexandrinus, "
                 "Ephraemi, Bezae, Washingtonianus, and the great majority; some "
                 "witnesses carry a shorter ending instead, and a few mark the "
                 "longer ending with obeli. (External context.)"),
    },
    {
        "id": "luke_agony",
        "label": "Agony in Gethsemane (the bloody sweat)",
        "ref": "Luke 22:43-44",
        "theme": "Christ's human suffering",
        "codes": block_codes(42, 22, 43, 44),
        "note": ("A disputed passage whose omission REMOVES Christ's agony rather "
                 "than reducing a doctrine; the witnesses divide early. (External context.)"),
    },
    {
        "id": "john_bethesda_angel",
        "label": "Angel troubling the water",
        "ref": "John 5:4",
        "theme": "narrative aetiology",
        "codes": ["43005004"],
        "note": "Explains the stirring of the pool; absent from the earliest witnesses. (External context.)",
    },
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


def classify_block(witness: dict[str, str], codes: list[str]) -> tuple[str, int, int]:
    """Return (state, present_count, covered_count) for a block in one witness.
    state is 'include' (>= half the covered verses present), 'omit' (covered but
    below half), or 'lacuna' (no verse of the block is even present-or-absent)."""
    present = sum(1 for c in codes if is_present(witness, c))
    covered = sum(1 for c in codes if c in witness)
    if covered == 0:
        return "lacuna", present, covered
    if present * 2 >= covered:
        return "include", present, covered
    return "omit", present, covered


def fmt_ref(code: str) -> str:
    return f"{int(code[:2])}:{int(code[2:5])}:{int(code[5:8])}"


def main() -> int:
    editions = {s: load_witness(s) for s in ("KJTR", "RP", "WH", "SR")}
    manuscripts = {ms: load_witness(ms) for ms in MANUSCRIPT_DATES}
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    verse_rows = []
    for block in BLOCKS:
        codes = block["codes"]
        # per-verse presence across editions
        for code in codes:
            verse_rows.append({
                "block": block["id"], "ref_code": fmt_ref(code),
                "kjtr": "present" if is_present(editions["KJTR"], code) else "absent",
                "rp": "present" if is_present(editions["RP"], code) else "absent",
                "wh": "present" if is_present(editions["WH"], code) else "absent",
                "sr": "present" if is_present(editions["SR"], code) else "absent",
            })
        # edition pattern
        ed_present = {s: sum(is_present(editions[s], c) for c in codes) for s in editions}
        n = len(codes)
        ed_pattern = ", ".join(
            f"{s}={'all' if ed_present[s] == n else ('none' if ed_present[s] == 0 else ed_present[s])}"
            for s in ("KJTR", "RP", "WH", "SR"))
        # dated witnesses
        include, omit, lacuna = [], [], []
        for ms, year in sorted(MANUSCRIPT_DATES.items(), key=lambda kv: (kv[1], kv[0])):
            state, _p, _c = classify_block(manuscripts[ms], codes)
            tag = f"{ms}({year})"
            {"include": include, "omit": omit, "lacuna": lacuna}[state].append(tag)
        covering = len(include) + len(omit)
        earliest_inc = include[0] if include else "(none)"
        earliest_omit = omit[0] if omit else "(none)"
        summary_rows.append({
            "block": block["id"], "label": block["label"], "ref": block["ref"],
            "theme": block["theme"], "editions": ed_pattern,
            "dated_include": ";".join(include) or "(none)",
            "dated_omit": ";".join(omit) or "(none)",
            "dated_lacuna_count": len(lacuna),
            "include_rate_of_covering": round(len(include) / covering, 3) if covering else None,
            "earliest_including": earliest_inc,
            "earliest_omitting": earliest_omit,
            "note": block["note"],
        })

    with (OUT_DIR / "block_summary.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(summary_rows[0].keys()))
        w.writeheader(); w.writerows(summary_rows)
    with (OUT_DIR / "block_verse_witnesses.csv").open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(verse_rows[0].keys()))
        w.writeheader(); w.writerows(verse_rows)
    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "disputed_block_witnesses",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "editions": ["KJTR", "RP", "WH", "SR"],
        "dated_manuscripts": MANUSCRIPT_DATES,
        "blocks": [b["ref"] for b in BLOCKS],
        "reading": ("include_rate_of_covering is the fraction of dated witnesses that "
                    "cover the block and include it. The Pericope Adulterae sits far "
                    "below Mark's longer ending: 'disputed' is not one category."),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"{'block':22s} {'editions':28s} {'inc/cov':>8}  earliest-incl  earliest-omit")
    for r in summary_rows:
        cov = (r["include_rate_of_covering"])
        print(f"{r['block']:22s} {r['editions']:28s} {str(cov):>8}  "
              f"{r['earliest_including']:>13}  {r['earliest_omitting']}")
    print("\nper-block detail:")
    for r in summary_rows:
        print(f"  {r['label']} ({r['ref']}, theme: {r['theme']})")
        print(f"     include: {r['dated_include']}")
        print(f"     omit:    {r['dated_omit']}")
    print(OUT_DIR / "block_summary.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
