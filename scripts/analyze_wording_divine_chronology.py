#!/usr/bin/env python3
"""Chronology and direction of divine-name WORDING variants (CNTR data).

The companion whole-verse analysis (analyze_doctrinal_variant_witnesses) showed
that the verses the Alexandrian text omits are LESS Christological than average
and that, by manuscript age, the longer readings are expansions. This script
asks the same question one level finer, at the WORDING level, where the deity
of Christ actually rides (1Tim 3:16 God/who, John 1:18 Son/God, Acts 20:28,
Col 1:14, the many places the TR carries an extra "Lord"/"Christ"/"Jesus").

Two readings of the same fact have to be told apart:

  A. divine names skew toward the TR side of wording differences (the TR has
     more "God/Lord/Christ/Son/Spirit" tokens that WH lacks than the reverse).
     This is real, but it is consistent with EITHER "Alexandrian scribes removed
     the divine name" OR "Byzantine/TR scribes added it." Direction alone cannot
     decide; the TR text is simply fuller (it loses more of every word).

  B. The manuscript ages decide it. If the TR-extra divine names were original
     and later removed, the OLDEST witnesses (the papyri, then Sinaiticus and
     Vaticanus) would carry them. If they are accretions, the oldest witnesses
     lack them and side with WH.

Parts:

  1. Per-token significance. Over every TR-vs-WH wording difference, a 2x2 of
     {divine, non-divine} x {TR-side, WH-side} with a chi-square: is a divine
     token over-represented on the TR side beyond the text's general fullness?

  2. TR-extra divine tokens by manuscript age. For each divine token the TR has
     and WH lacks, every dated witness that covers the verse either sides with
     the TR (still has it) or with WH (lacks it). Reported by century bucket and
     per manuscript. Removal would need old witnesses to side with the TR.

  3. The reverse: WH-extra divine tokens (e.g. John 1:18 "only-begotten God").
     Do the oldest witnesses side with WH, i.e. is the Alexandrian higher-
     Christology reading itself early?

All pure data over the CNTR transcriptions (CC BY-SA 4.0, Alan Bunning,
data/raw/cntr). Outputs under reports/wording_divine_chronology/.
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
OUT_DIR = Path("reports/wording_divine_chronology")

_DIVINE_FORMS = [
    "θεός", "θεοῦ", "θεῷ", "θεόν", "θεέ",
    "κύριος", "κυρίου", "κυρίῳ", "κύριον", "κύριε",
    "Ἰησοῦς", "Ἰησοῦ", "Ἰησοῦν",
    "Χριστός", "Χριστοῦ", "Χριστῷ", "Χριστόν", "Χριστέ",
    "υἱός", "υἱοῦ", "υἱῷ", "υἱόν", "υἱέ",
    "πνεῦμα", "πνεύματος", "πνεύματι", "πνεύματα",
]
DIVINE = {normalize_greek(form) for form in _DIVINE_FORMS}

# Standard paleographic mid-century datings (INTF Liste / NA28 / Aland).
MANUSCRIPT_DATES: dict[str, int] = {
    "P46": 200, "P66": 200, "P75": 200,
    "P45": 250, "P69": 250, "P47": 250, "P115": 250,
    "0171": 300,
    "01": 350, "03": 350,
    "05": 400, "032": 400,
    "02": 450, "04": 450, "P19": 450,
}


def load_edition(siglum: str) -> dict[str, str]:
    for path in glob.glob(f"{CNTR_ROOT}/**/{siglum}.txt", recursive=True):
        out: dict[str, str] = {}
        with open(path, encoding="utf-8") as handle:
            for line in handle:
                if len(line) >= 8 and line[:8].isdigit():
                    out[line[:8]] = line[9:].rstrip("\n")
        return out
    raise SystemExit(f"edition/manuscript {siglum} not found under {CNTR_ROOT}")


def is_present(edition: dict[str, str], code: str) -> bool:
    body = edition.get(code)
    return bool(body) and not body.startswith("-")


def norm_tokens(text: str) -> list[str]:
    return [w for tok in text.replace("¶", " ").split() if (w := normalize_greek(tok))]


def divine_counts(text: str) -> Counter[str]:
    return Counter(t for t in norm_tokens(text) if t in DIVINE)


NT_BOOK = {
    40: "Matt", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Rom",
    46: "1Cor", 47: "2Cor", 48: "Gal", 49: "Eph", 50: "Phil", 51: "Col",
    52: "1Thess", 53: "2Thess", 54: "1Tim", 55: "2Tim", 56: "Titus", 57: "Phlm",
    58: "Heb", 59: "Jas", 60: "1Pet", 61: "2Pet", 62: "1John", 63: "2John",
    64: "3John", 65: "Jude", 66: "Rev",
}


def fmt_ref(code: str) -> str:
    return f"{NT_BOOK.get(int(code[:2]), code[:2])} {int(code[2:5])}:{int(code[5:8])}"


def byzantine_share(rp_text: str, token: str, tr_count: int) -> bool:
    """Whether the Byzantine (RP) reading carries the divine token as fully as TR."""
    return divine_counts(rp_text).get(token, 0) >= tr_count


def token_direction(tr_text: str, wh_text: str) -> dict[str, int]:
    """Tokens present on the TR side of a wording difference but not the WH side
    (tr_total) and vice versa (wh_total), with the divine subset of each."""
    tr_words, wh_words = norm_tokens(tr_text), norm_tokens(wh_text)
    out = {"tr_total": 0, "wh_total": 0, "tr_divine": 0, "wh_divine": 0}
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, tr_words, wh_words).get_opcodes():
        if tag == "equal":
            continue
        tr_chunk, wh_chunk = tr_words[i1:i2], wh_words[j1:j2]
        out["tr_total"] += len(tr_chunk)
        out["wh_total"] += len(wh_chunk)
        out["tr_divine"] += sum(w in DIVINE for w in tr_chunk)
        out["wh_divine"] += sum(w in DIVINE for w in wh_chunk)
    return out


def extra_divine_tokens(have_text: str, lack_text: str) -> list[tuple[str, int, int]]:
    """Divine tokens that occur more often in have_text than lack_text:
    (token, have_count, lack_count)."""
    have, lack = divine_counts(have_text), divine_counts(lack_text)
    return [(tok, have[tok], lack.get(tok, 0)) for tok in have if have[tok] > lack.get(tok, 0)]


def witness_side(ms_count: int, have_count: int, lack_count: int) -> str:
    """Which reading a witness with ms_count of the token agrees with."""
    if ms_count >= have_count:
        return "have"
    if ms_count <= lack_count:
        return "lack"
    return "ambiguous"


def century_bucket(year: int) -> str:
    if year <= 250:
        return "II-III (papyri, c.200-250)"
    if year <= 350:
        return "III-IV (c.300-350)"
    return "IV-V (c.400-450)"


def chi2_2x2(a: int, b: int, c: int, d: int) -> float:
    n = a + b + c + d
    if n == 0:
        return 0.0
    row1, row2, col1, col2 = a + b, c + d, a + c, b + d
    expected = [row1 * col1 / n, row1 * col2 / n, row2 * col1 / n, row2 * col2 / n]
    observed = [a, b, c, d]
    return round(sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0), 3)


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


def age_direction(targets, manuscripts, side_when_have):
    """For each (code, token, have_count, lack_count) target and each dated
    witness covering it, tally agreement with the longer reading by age.
    side_when_have maps witness_side -> 'longer'/'shorter'. Returns
    (bucket_rows, per_ms_rows, pearson_age_vs_longer)."""
    buckets: dict[str, list[int]] = {}
    per_ms: dict[str, list[int]] = {}
    for code, token, have_c, lack_c in targets:
        for ms, year in MANUSCRIPT_DATES.items():
            body = manuscripts[ms].get(code)
            if not body or body.startswith("-"):
                continue
            ms_count = sum(1 for t in norm_tokens(body) if t == token)
            side = side_when_have[witness_side(ms_count, have_c, lack_c)]
            if side is None:
                continue
            b = buckets.setdefault(century_bucket(year), [0, 0])
            p = per_ms.setdefault(ms, [0, 0])
            idx = 0 if side == "longer" else 1
            b[idx] += 1
            p[idx] += 1
    bucket_rows = [
        {"century": c, "with_longer": lo, "with_shorter": sh,
         "longer_agreement": round(lo / (lo + sh), 4) if lo + sh else 0.0,
         "observations": lo + sh}
        for c, (lo, sh) in sorted(buckets.items())
    ]
    per_ms_rows = [
        {"manuscript": m, "date": MANUSCRIPT_DATES[m],
         "with_longer": lo, "with_shorter": sh,
         "longer_agreement": round(lo / (lo + sh), 4) if lo + sh else 0.0,
         "observations": lo + sh}
        for m, (lo, sh) in sorted(per_ms.items(), key=lambda kv: (MANUSCRIPT_DATES[kv[0]], kv[0]))
    ]
    xs = [r["date"] for r in per_ms_rows if r["observations"] >= 10]
    ys = [r["longer_agreement"] for r in per_ms_rows if r["observations"] >= 10]
    return bucket_rows, per_ms_rows, pearson(xs, ys)


def main() -> int:
    eds = {s: load_edition(s) for s in ("KJTR", "WH", "RP")}
    kjtr, wh, rp = eds["KJTR"], eds["WH"], eds["RP"]
    manuscripts = {ms: load_edition(ms) for ms in MANUSCRIPT_DATES}
    shared = [c for c in kjtr if is_present(kjtr, c) and is_present(wh, c)]

    # ---- Part 1: per-token direction significance ----
    tot = {"tr_total": 0, "wh_total": 0, "tr_divine": 0, "wh_divine": 0}
    tr_extra_targets: list[tuple[str, int, int]] = []
    wh_extra_targets: list[tuple[str, int, int]] = []
    tr_extra = []  # (code, token, trc, whc)
    wh_extra = []
    for code in shared:
        if norm_tokens(kjtr[code]) == norm_tokens(wh[code]):
            continue
        counts = token_direction(kjtr[code], wh[code])
        for key in tot:
            tot[key] += counts[key]
        for tok, h, l in extra_divine_tokens(kjtr[code], wh[code]):
            tr_extra.append((code, tok, h, l))
        for tok, h, l in extra_divine_tokens(wh[code], kjtr[code]):
            wh_extra.append((code, tok, h, l))

    tr_div, wh_div = tot["tr_divine"], tot["wh_divine"]
    tr_non, wh_non = tot["tr_total"] - tr_div, tot["wh_total"] - wh_div
    divine_tr_share = round(tr_div / (tr_div + wh_div), 4) if tr_div + wh_div else 0.0
    nondiv_tr_share = round(tr_non / (tr_non + wh_non), 4) if tr_non + wh_non else 0.0
    part1 = {
        "tr_side_divine": tr_div, "wh_side_divine": wh_div,
        "tr_side_nondivine": tr_non, "wh_side_nondivine": wh_non,
        "divine_tr_side_share": divine_tr_share,
        "nondivine_tr_side_share": nondiv_tr_share,
        "all_token_ratio_tr_over_wh": round(tot["tr_total"] / tot["wh_total"], 3) if tot["wh_total"] else None,
        "divine_ratio_tr_over_wh": round(tr_div / wh_div, 3) if wh_div else None,
        "chi2_divine_vs_nondivine_by_side": chi2_2x2(tr_div, wh_div, tr_non, wh_non),
    }

    # ---- Part 2: TR-extra divine tokens by age (do old witnesses side with TR?) ----
    # for TR-extra tokens, a witness that HAS the token sides with the longer TR reading.
    tr_targets = [(c, tok, h, l) for (c, tok, h, l) in tr_extra]
    tr_buckets, tr_per_ms, tr_pearson = age_direction(
        tr_targets, manuscripts, {"have": "longer", "lack": "shorter", "ambiguous": None})

    # ---- Part 3: WH-extra divine tokens by age (do old witnesses side with WH?) ----
    wh_targets = [(c, tok, h, l) for (c, tok, h, l) in wh_extra]
    wh_buckets, wh_per_ms, wh_pearson = age_direction(
        wh_targets, manuscripts, {"have": "longer", "lack": "shorter", "ambiguous": None})

    # ---- Part 4: how much of the TR-extra divine material is even Byzantine? ----
    # The popular framing is Alexandrian vs Byzantine. So of the divine names the
    # TR carries beyond WH, how many does the Byzantine majority (RP) share, and
    # how many are TR-only (absent from the Byzantine text too)?
    byz_shares = tr_only = rp_absent = 0
    tr_only_rows = []
    for code, tok, have_c, _lack_c in tr_extra:
        if not is_present(rp, code):
            rp_absent += 1
            continue
        if byzantine_share(rp[code], tok, have_c):
            byz_shares += 1
        else:
            tr_only += 1
            tr_only_rows.append({"ref": fmt_ref(code), "code": code, "token": tok})
    byz_present = byz_shares + tr_only
    byz_share_rate = round(byz_shares / byz_present, 4) if byz_present else 0.0

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    def write_csv(name, rows):
        fields = list(rows[0].keys()) if rows else ["x"]
        with (OUT_DIR / name).open("w", encoding="utf-8", newline="") as h:
            w = csv.DictWriter(h, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    write_csv("per_token_direction.csv", [{"metric": k, "value": v} for k, v in part1.items()])
    write_csv("tr_extra_divine_by_age.csv", tr_buckets)
    write_csv("tr_extra_divine_by_manuscript.csv", tr_per_ms)
    write_csv("wh_extra_divine_by_age.csv", wh_buckets)
    write_csv("wh_extra_divine_by_manuscript.csv", wh_per_ms)
    write_csv("tr_only_divine_names.csv", tr_only_rows)

    manifest = {
        "tool": "wording_divine_chronology",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "editions": ["KJTR", "WH"],
        "dated_manuscripts": MANUSCRIPT_DATES,
        "divine_forms": sorted(DIVINE),
        "shared_verses": len(shared),
        "part1_per_token_direction": part1,
        "tr_extra_divine_token_instances": len(tr_extra),
        "wh_extra_divine_token_instances": len(wh_extra),
        "tr_extra_pearson_date_vs_tr_agreement": tr_pearson,
        "wh_extra_pearson_date_vs_wh_agreement": wh_pearson,
        "part4_byzantine_sharing": {
            "tr_extra_with_rp_present": byz_present,
            "byzantine_shares": byz_shares,
            "byzantine_share_rate": byz_share_rate,
            "tr_only": tr_only,
            "rp_verse_absent": rp_absent,
        },
        "reading": (
            "Part 1: divine_tr_side_share well above nondivine_tr_side_share with a "
            "large chi-square means divine tokens skew to the TR side beyond the "
            "text's general fullness. Parts 2-3: if TR-extra divine names were "
            "original-and-removed, the oldest witnesses would side with the TR "
            "(high longer_agreement at c.200-350). Near-zero agreement there means "
            "the early text lacks them: expansion, not removal."
        ),
    }
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"shared verses: {len(shared)}")
    print("\nPart 1 - per-token direction (all TR-vs-WH wording differences):")
    print(f"  divine tokens on TR side / WH side: {tr_div} / {wh_div}")
    print(f"  divine TR-side share:    {divine_tr_share}")
    print(f"  non-divine TR-side share: {nondiv_tr_share}  (general fullness baseline)")
    print(f"  chi2(divine vs non-divine by side): {part1['chi2_divine_vs_nondivine_by_side']}")
    print(f"\nPart 2 - TR-extra divine tokens ({len(tr_extra)} instances): does the early text side with the TR?")
    for r in tr_buckets:
        print(f"  {r['century']:28s} TR-agreement {r['longer_agreement']:.3f}  (n={r['observations']})")
    print(f"  Pearson(date, TR-agreement) = {tr_pearson}")
    print(f"\nPart 3 - WH-extra divine tokens ({len(wh_extra)} instances): does the early text side with WH?")
    for r in wh_buckets:
        print(f"  {r['century']:28s} WH-agreement {r['longer_agreement']:.3f}  (n={r['observations']})")
    tr_only_pct = tr_only / byz_present if byz_present else 0.0
    print(f"\nPart 4 - of {byz_present} TR-extra divine names, how many are even Byzantine (RP)?")
    print(f"  Byzantine (RP) shares: {byz_shares} ({byz_share_rate:.1%})   "
          f"TR-only: {tr_only} ({tr_only_pct:.1%})")
    print(OUT_DIR / "tr_extra_divine_by_age.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
