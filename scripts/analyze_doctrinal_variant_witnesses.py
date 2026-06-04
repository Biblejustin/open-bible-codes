#!/usr/bin/env python3
"""Witness-level analysis of doctrinally-loaded NT textual variants (CNTR data).

Tests one popular claim, with the data and not the gut: that the verses
omitted or changed in the Alexandrian-critical text disproportionately touch
contested doctrine (deity of Christ, the Trinity, the blood atonement), and that
this clusters in the Alexandrian text-type.

Sources (CNTR transcriptions, CC BY-SA 4.0, Alan Bunning, data/raw/cntr):
  editions    KJTR (Textus Receptus / KJV base), RP (Byzantine, Robinson-Pierpont),
              WH (Westcott-Hort), SR (Statistical Restoration); all full texts.
  manuscripts the dated uncials/papyri (01 Sinaiticus, 03 Vaticanus, 02, 04, 05,
              032, P45/46/47/66/75 ...) for witness-level presence.

Four reported parts, all pure data:

  A. Named loaded variants. For a fixed, transparent list (1Tim 3:16, John 1:18,
     the Comma, Acts 8:37, Mark 16, the Pericope, Col 1:14, Acts 20:28, ...), the
     actual reading of each edition, and an OBJECTIVE tradition pattern:
       alex_omits_byz_keeps  TR and Byzantine have the verse; WH/SR omit it.
       tr_only               TR has it; Byzantine AND Alexandrian omit it (so it
                             is a TR/Latin reading, not an Alexandrian deletion).
       wording_variant       all present; the wording differs.
     This is the honesty check: several of the most-cited "Alexandrian attacks"
     (the Comma, Acts 8:37, Col 1:14 "through his blood") are tr_only, absent from
     the Byzantine majority too; and at John 1:18 the Alexandrian reading is the
     HIGHER Christology ("only-begotten God" vs "only-begotten Son").

  B. Expansion or removal, for the whole-verse cases: which DATED witnesses
     include vs omit each verse. If the longer reading were original and later
     removed, the OLDEST witnesses would have it; if it is a later growth, the
     oldest witnesses lack it. (Companion to analyze_manuscript_omission_chronology.)

  C. Base-rate clustering test, on the FULL set of whole-verse omissions (every
     verse present in KJTR and absent in WH; no hand-picking). Objective doctrinal
     proxies, run on each omitted verse's TR text:
       divine token    a divine-name / Christological-title form is present
                       (theos, kyrios, iesous, christos, huios, pneuma).
       atonement token a blood/cross/redemption stem is present.
     Each rate is compared, with a 2x2 chi-square, to the rate among the verses
     WH keeps. If omitted verses carry these tokens no more than kept verses, the
     "omissions cluster on doctrine" claim fails at the whole-verse level.

  D. Wording-level direction. Among verses present in both KJTR and WH but worded
     differently, count the divine-token changes by direction: a divine token the
     TR has and WH drops, vs one WH has and the TR lacks. A systematic
     deity-lowering tendency would be lopsided toward TR-side losses.

Outputs under reports/doctrinal_variant_witnesses/.
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
OUT_DIR = Path("reports/doctrinal_variant_witnesses")

NT_BOOK = {
    40: "Matt", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts", 45: "Rom",
    46: "1Cor", 47: "2Cor", 48: "Gal", 49: "Eph", 50: "Phil", 51: "Col",
    52: "1Thess", 53: "2Thess", 54: "1Tim", 55: "2Tim", 56: "Titus", 57: "Phlm",
    58: "Heb", 59: "Jas", 60: "1Pet", 61: "2Pet", 62: "1John", 63: "2John",
    64: "3John", 65: "Jude", 66: "Rev",
}

# Objective Christological-title / divine-name forms, normalized the same way as
# the text (final sigma folded) so nominatives match. Membership is factual.
_DIVINE_FORMS = [
    "θεός", "θεοῦ", "θεῷ", "θεόν", "θεέ",
    "κύριος", "κυρίου", "κυρίῳ", "κύριον", "κύριε",
    "Ἰησοῦς", "Ἰησοῦ", "Ἰησοῦν",
    "Χριστός", "Χριστοῦ", "Χριστῷ", "Χριστόν", "Χριστέ",
    "υἱός", "υἱοῦ", "υἱῷ", "υἱόν", "υἱέ",
    "πνεῦμα", "πνεύματος", "πνεύματι", "πνεύματα",
]
DIVINE = {normalize_greek(form) for form in _DIVINE_FORMS}
# Atonement vocabulary by normalized stem: blood, cross/crucify, redeem/ransom.
ATONEMENT_STEMS = ("αιμα", "αιματ", "σταυρ", "λυτρ", "απολυτρωσ")

# Standard paleographic mid-century datings (INTF Liste / NA28 / Aland), as in
# analyze_manuscript_omission_chronology.
MANUSCRIPT_DATES: dict[str, int] = {
    "P46": 200, "P66": 200, "P75": 200,
    "P45": 250, "P69": 250, "P47": 250, "P115": 250,
    "0171": 300,
    "01": 350, "03": 350,
    "05": 400, "032": 400,
    "02": 450, "04": 450, "P19": 450,
}

# Fixed, transparent list of loaded variant units: (code, label, doctrine tag).
# The doctrine tag is a human-readable note only; it is NOT used in the Part C/D
# statistics, which use objective token proxies instead.
LOADED_VARIANTS: list[tuple[str, str, str]] = [
    ("54003016", "1Tim 3:16 God/who manifest", "deity_of_christ"),
    ("43001018", "John 1:18 only-begotten Son/God", "christology"),
    ("62005007", "1John 5:7 Johannine Comma", "trinity"),
    ("44008037", "Acts 8:37 eunuch's confession", "christology"),
    ("51001014", "Col 1:14 through his blood", "atonement"),
    ("44020028", "Acts 20:28 church of God / his blood", "deity_atonement"),
    ("66001011", "Rev 1:11 I am Alpha and Omega", "deity_of_christ"),
    ("49003009", "Eph 3:9 created by Jesus Christ", "christology_creation"),
    ("45014010", "Rom 14:10 judgment seat of Christ/God", "christology"),
    ("46015047", "1Cor 15:47 the Lord from heaven", "christology"),
    ("43003013", "John 3:13 Son of Man in heaven", "christology"),
    ("41016009", "Mark 16:9 longer ending (block)", "resurrection"),
    ("43007053", "John 7:53 Pericope Adulterae (block)", "mercy_forgiveness"),
    ("40017021", "Matt 17:21 prayer and fasting", "discipleship"),
    ("40018011", "Matt 18:11 Son of Man came to save", "soteriology"),
    ("41009044", "Mark 9:44 worm dieth not", "judgment"),
    ("42023017", "Luke 23:17 release at feast", "narrative"),
    ("44028029", "Acts 28:29 Jews departed", "narrative"),
    ("45016024", "Rom 16:24 grace benediction", "benediction"),
    ("43005004", "John 5:4 angel troubling the water", "narrative"),
]


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
    """Verse text physically present (covered and not marked absent with '-')."""
    body = edition.get(code)
    return bool(body) and not body.startswith("-")


def covers(edition: dict[str, str], code: str) -> bool:
    """Witness contains the verse code at all (present OR explicitly '-' absent),
    as opposed to a lacuna where the code is simply missing from the file."""
    return code in edition


def norm_tokens(text: str) -> list[str]:
    out = []
    for tok in text.replace("¶", " ").split():
        w = normalize_greek(tok)
        if w:
            out.append(w)
    return out


def has_divine(text: str) -> bool:
    return any(tok in DIVINE for tok in norm_tokens(text))


def has_atonement(text: str) -> bool:
    return any(
        any(tok.startswith(stem) for stem in ATONEMENT_STEMS)
        for tok in norm_tokens(text)
    )


def fmt_ref(code: str) -> str:
    book = NT_BOOK.get(int(code[:2]), code[:2])
    return f"{book} {int(code[2:5])}:{int(code[5:8])}"


def classify_tradition_pattern(tr: bool, rp: bool, wh: bool, sr: bool) -> str:
    """Objective pattern from the four edition presence flags."""
    if not tr:
        return "not_in_tr"
    alex_absent = not wh and not sr
    if alex_absent:
        return "alex_omits_byz_keeps" if rp else "tr_only"
    if not wh or not sr:
        return "alex_split"
    return "wording_variant" if rp else "tr_and_alex_only"


def chi2_2x2(a: int, b: int, c: int, d: int) -> float:
    """Pearson chi-square for a 2x2 table [[a,b],[c,d]] (no continuity fix)."""
    n = a + b + c + d
    if n == 0:
        return 0.0
    row1, row2, col1, col2 = a + b, c + d, a + c, b + d
    expected = [row1 * col1 / n, row1 * col2 / n, row2 * col1 / n, row2 * col2 / n]
    observed = [a, b, c, d]
    return round(sum((o - e) ** 2 / e for o, e in zip(observed, expected) if e > 0), 3)


def wording_divine_direction(tr_text: str, wh_text: str) -> tuple[list[str], list[str]]:
    """Divine tokens the TR reading has that WH drops, and vice versa."""
    tr_words, wh_words = norm_tokens(tr_text), norm_tokens(wh_text)
    tr_drop, wh_gain = [], []
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, tr_words, wh_words).get_opcodes():
        if tag == "equal":
            continue
        tr_drop.extend(w for w in tr_words[i1:i2] if w in DIVINE)
        wh_gain.extend(w for w in wh_words[j1:j2] if w in DIVINE)
    return tr_drop, wh_gain


def wording_token_direction(tr_text: str, wh_text: str) -> dict[str, int]:
    """Per-verse token-direction tally: total tokens the TR has that WH lacks
    (tr_total) and vice versa (wh_total), and the divine-token subset of each.
    The divine ratio is only meaningful against the total ratio, because the
    Byzantine/TR text is fuller overall and so loses more of every word."""
    tr_words, wh_words = norm_tokens(tr_text), norm_tokens(wh_text)
    counts = {"tr_total": 0, "wh_total": 0, "tr_divine": 0, "wh_divine": 0}
    for tag, i1, i2, j1, j2 in SequenceMatcher(None, tr_words, wh_words).get_opcodes():
        if tag == "equal":
            continue
        tr_chunk, wh_chunk = tr_words[i1:i2], wh_words[j1:j2]
        counts["tr_total"] += len(tr_chunk)
        counts["wh_total"] += len(wh_chunk)
        counts["tr_divine"] += sum(w in DIVINE for w in tr_chunk)
        counts["wh_divine"] += sum(w in DIVINE for w in wh_chunk)
    return counts


def main() -> int:
    eds = {s: load_edition(s) for s in ("KJTR", "RP", "WH", "SR")}
    kjtr, rp, wh, sr = eds["KJTR"], eds["RP"], eds["WH"], eds["SR"]
    manuscripts = {ms: load_edition(ms) for ms in MANUSCRIPT_DATES}

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- Part A: named loaded variants ----
    variant_rows = []
    presence_codes = []
    for code, label, doctrine in LOADED_VARIANTS:
        flags = (is_present(kjtr, code), is_present(rp, code),
                 is_present(wh, code), is_present(sr, code))
        pattern = classify_tradition_pattern(*flags)
        row = {
            "ref": fmt_ref(code), "code": code, "label": label, "doctrine": doctrine,
            "pattern": pattern,
            "tr_present": flags[0], "byz_rp_present": flags[1],
            "alex_wh_present": flags[2], "alex_sr_present": flags[3],
            "tr_text": kjtr.get(code, ""), "wh_text": wh.get(code, ""),
        }
        if pattern == "wording_variant":
            tr_drop, wh_gain = wording_divine_direction(kjtr[code], wh[code])
            row["divine_tr_drops"] = ";".join(tr_drop)
            row["divine_wh_gains"] = ";".join(wh_gain)
        else:
            row["divine_tr_drops"] = ""
            row["divine_wh_gains"] = ""
            presence_codes.append((code, label, doctrine, pattern))
        variant_rows.append(row)

    # ---- Part B: expansion vs removal for the whole-verse cases ----
    presence_rows = []
    for code, label, _doctrine, pattern in presence_codes:
        incl, omit, lac = [], [], []
        for ms, year in sorted(MANUSCRIPT_DATES.items(), key=lambda kv: kv[1]):
            mss = manuscripts[ms]
            if not covers(mss, code):
                lac.append(ms)
            elif is_present(mss, code):
                incl.append(f"{ms}({year})")
            else:
                omit.append(f"{ms}({year})")
        presence_rows.append({
            "ref": fmt_ref(code), "code": code, "label": label, "pattern": pattern,
            "dated_include": ";".join(incl) or "(none)",
            "dated_omit": ";".join(omit) or "(none)",
            "dated_lacuna": ";".join(lac) or "(none)",
            "oldest_witness_has_it": incl[0].split("(")[0] if incl else "(none cover present)",
        })

    # ---- Part C: base-rate clustering test over ALL whole-verse omissions ----
    kjtr_codes = [c for c in kjtr if is_present(kjtr, c)]
    n_all = len(kjtr_codes)
    omitted = [c for c in kjtr_codes if not is_present(wh, c)]
    kept = [c for c in kjtr_codes if is_present(wh, c)]
    byz_keeps = [c for c in omitted if is_present(rp, c)]
    tr_only = [c for c in omitted if not is_present(rp, c)]

    def proxy_counts(codes, fn):
        k = sum(fn(kjtr[c]) for c in codes)
        return k, len(codes)

    clustering_rows = []
    for proxy_name, fn in (("divine_token", has_divine), ("atonement_token", has_atonement)):
        kept_k, kept_n = proxy_counts(kept, fn)
        for group_name, codes in (("all_wh_omissions", omitted),
                                   ("genuine_alex_omission_byz_keeps", byz_keeps),
                                   ("tr_only", tr_only)):
            k, n = proxy_counts(codes, fn)
            base = kept_k / kept_n if kept_n else 0.0
            rate = k / n if n else 0.0
            clustering_rows.append({
                "proxy": proxy_name, "group": group_name,
                "verses": n, "with_token": k, "rate": round(rate, 4),
                "kept_baseline_rate": round(base, 4),
                "ratio_vs_kept": round(rate / base, 2) if base else "",
                "chi2_vs_kept": chi2_2x2(k, n - k, kept_k, kept_n - kept_k),
            })

    # ---- Part D: wording-level divine-token direction (KJTR vs WH) ----
    shared = [c for c in kjtr_codes if is_present(wh, c)]
    tot = {"tr_total": 0, "wh_total": 0, "tr_divine": 0, "wh_divine": 0}
    wording_divine_verses = 0
    for c in shared:
        if norm_tokens(kjtr[c]) == norm_tokens(wh[c]):
            continue
        counts = wording_token_direction(kjtr[c], wh[c])
        for key in tot:
            tot[key] += counts[key]
        if counts["tr_divine"] or counts["wh_divine"]:
            wording_divine_verses += 1
    tr_side_losses, wh_side_gains = tot["tr_divine"], tot["wh_divine"]
    total_ratio = round(tot["tr_total"] / tot["wh_total"], 2) if tot["wh_total"] else None
    divine_ratio = round(tr_side_losses / wh_side_gains, 2) if wh_side_gains else None
    # divine over-representation: how much more lopsided the divine direction is
    # than the all-token direction. >1 means divine names skew TR-ward beyond the
    # general fullness of the TR text; ~1 means no targeting.
    over_rep = round(divine_ratio / total_ratio, 2) if (divine_ratio and total_ratio) else None

    # ---- write outputs ----
    def write_csv(name, rows):
        fields = list(rows[0].keys()) if rows else ["ref"]
        with (OUT_DIR / name).open("w", encoding="utf-8", newline="") as h:
            writer = csv.DictWriter(h, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    write_csv("variant_witnesses.csv", variant_rows)
    write_csv("presence_witnesses.csv", presence_rows)
    write_csv("clustering_test.csv", clustering_rows)

    pattern_counts = Counter(r["pattern"] for r in variant_rows)
    manifest = {
        "tool": "doctrinal_variant_witnesses",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR transcriptions (CC BY-SA 4.0, Alan Bunning), data/raw/cntr",
        "editions": ["KJTR", "RP", "WH", "SR"],
        "dated_manuscripts": MANUSCRIPT_DATES,
        "divine_forms": sorted(DIVINE),
        "atonement_stems": list(ATONEMENT_STEMS),
        "named_variants": len(variant_rows),
        "named_variant_patterns": dict(sorted(pattern_counts.items())),
        "whole_verse_omissions": len(omitted),
        "genuine_alex_omission_byz_keeps": len(byz_keeps),
        "tr_only": len(tr_only),
        "wording_divine_direction": {
            "verses_with_divine_change": wording_divine_verses,
            "tr_side_divine_losses": tr_side_losses,
            "wh_side_divine_gains": wh_side_gains,
            "all_token_tr_losses": tot["tr_total"],
            "all_token_wh_gains": tot["wh_total"],
            "all_token_ratio_tr_over_wh": total_ratio,
            "divine_ratio_tr_over_wh": divine_ratio,
            "divine_over_representation_vs_all_tokens": over_rep,
        },
        "reading": (
            "Whole-verse: divine-token ratio_vs_kept below 1.0 means Alexandrian "
            "omissions are LESS Christological than the verses WH keeps, not more. "
            "Wording: the TR text is fuller (all-token ratio ~1.4), so its larger "
            "raw divine-token count is expected; over_representation > 1 is the only "
            "evidence of a divine-name-specific skew, and it is modest."
        ),
    }
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- console summary ----
    print(f"named loaded variants: {len(variant_rows)}")
    for pat, count in sorted(pattern_counts.items()):
        print(f"  {pat}: {count}")
    print(f"\nwhole-verse omissions (KJTR present, WH absent): {len(omitted)}"
          f"  [genuine alex={len(byz_keeps)}, tr_only={len(tr_only)}]")
    print("clustering test (rate vs verses WH keeps):")
    for r in clustering_rows:
        print(f"  {r['proxy']:16s} {r['group']:32s} "
              f"{r['with_token']:>3}/{r['verses']:<3} = {r['rate']:.3f}  "
              f"base {r['kept_baseline_rate']:.3f}  x{r['ratio_vs_kept']}  chi2={r['chi2_vs_kept']}")
    print(f"\nwording divine-token direction (KJTR vs WH, {wording_divine_verses} verses):")
    print(f"  all tokens:    TR-side losses {tot['tr_total']:>5}   WH-side gains {tot['wh_total']:>5}   ratio {total_ratio}")
    print(f"  divine tokens: TR-side losses {tr_side_losses:>5}   WH-side gains {wh_side_gains:>5}   ratio {divine_ratio}")
    print(f"  divine over-representation vs all tokens: {over_rep}  (~1.0 = no divine-specific skew)")
    print(OUT_DIR / "variant_witnesses.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
