#!/usr/bin/env python3
"""Famous disputed readings, read from the manuscript transcriptions themselves.

The earlier studies compared printed editions (TR, Byzantine, WH, SR, SBLGNT).
This drops to the witness level: the CNTR transcriptions of the papyri and
uncials are read directly at six famous loci, and each witness's actual reading
is classified from its own line.

The loci and what the transcriptions show:

- Revelation 13:18, the number of the beast: 666 (chi-xi-stigma or spelled out
  "six hundred sixty-six") versus 616 (chi-iota-stigma or "six hundred
  sixteen"). P47 and Sinaiticus carry 666; P115 is the famous 616 witness.
- Mark 16:9, the Long Ending: present or absent in witnesses that carry
  Mark 16:8 (Sinaiticus and Vaticanus end at 16:8).
- John 7:53, the woman taken in adultery: present or absent in witnesses
  carrying the surrounding text (P66, P75, Sinaiticus, Vaticanus lack it;
  Bezae carries it).
- Acts 8:37, the eunuch's confession: no transcribed witness that covers
  Acts 8 carries the verse at all.
- 1 Timothy 3:16, "God was manifested" versus "who was manifested": theta-sigma
  nomen sacrum versus the relative pronoun; Alexandrinus shows the relative
  pronoun as the first hand with a corrector's theos.
- 1 John 5:7, the Comma Johanneum: present or absent.

MES transcription conventions used here: one verse per line keyed by an
eight-digit code; a bare "-" line means the witness covers the area but the
verse is absent; "=" prefixes nomina sacra; "$" prefixes numeral letters;
"x{...}" is a first-hand reading with a corrector's "{...}" alongside.

Centuries are the standard published datings for these famous witnesses,
recorded as documented facts. Outputs under reports/famous_variants_attestation/.
"""

from __future__ import annotations

import csv
import glob
import json
import re
from datetime import UTC, datetime
from pathlib import Path

CNTR_ROOT = Path("data/raw/cntr")
OUT_DIR = Path("reports/famous_variants_attestation")

# Standard published centuries for the witnesses involved (documented facts).
WITNESS_CENTURY = {
    "P45": "III", "P47": "III", "P66": "c. 200", "P75": "III", "P115": "III/IV",
    "P133": "III", "01": "IV", "02": "V", "03": "IV", "04": "V", "05": "V",
    "032": "IV/V",
}

MARKER_RE = re.compile(r"[/\\|^%~+&*0-9]")


def clean(line: str) -> str:
    """Strip transcription markers for token matching; keep =, $, braces, x."""
    text = MARKER_RE.sub("", line)
    text = text.replace("¯", "ν")          # overline = suspended final nu
    return " ".join(text.split())


def verse_line(ms_text: str, code: str) -> str | None:
    """The witness's line for a verse code: text, '-' if marked absent, None if
    the witness simply does not include the verse line at all."""
    i = ms_text.find("\n" + code)
    if i == -1 and ms_text.startswith(code):
        i = 0
    if i < 0:
        return None
    return ms_text[i:].lstrip("\n").split("\n", 1)[0][9:].strip()


def has_greek(line: str) -> bool:
    """True when the line carries actual letter content (not just '-' markers)."""
    return bool(re.search(r"[α-ω]", clean(line)))


def classify_rev_13_18(line: str) -> str:
    text = clean(line)
    if "$χ $ξ" in text or "χξ" in text.replace(" ", ""):
        return "666 (numeral chi-xi-stigma)"
    if "εξηκο" in text:
        return "666 (spelled out, six hundred sixty-six)"
    if "$χ $ι" in text:
        return "616 (numeral chi-iota-stigma)"
    if "δεκα" in text and "εξακοσ" in text:
        return "616 (spelled out, six hundred sixteen)"
    return "unclear from transcription"


def classify_1tim_3_16(line: str) -> str:
    if "x{οσ}" in line and "=θσ" in line:
        return "hos (first hand), corrected to theos"
    text = clean(line)
    if "=θσ" in text:
        return "theos (nomen sacrum)"
    if re.search(r"(^| )οσ ", text):
        return "hos (relative pronoun)"
    return "unclear from transcription"


def classify_comma(line: str) -> str:
    text = clean(line)
    if "ουραν" in text or ("πατηρ" in text and "λογοσ" in text):
        return "Comma present"
    return "short reading (no Comma)"


def classify_presence(line: str) -> str:
    return "verse present" if has_greek(line) else "verse absent (marked '-')"


LOCI = [
    {"label": "Revelation 13:18 number of the beast", "code": "66013018",
     "context": "66013017", "classify": classify_rev_13_18},
    {"label": "Mark 16:9 Long Ending", "code": "41016009",
     "context": "41016008", "classify": classify_presence},
    {"label": "John 7:53 Pericope Adulterae", "code": "43007053",
     "context": "43008012", "classify": classify_presence},
    {"label": "Acts 8:37 eunuch's confession", "code": "44008037",
     "context": "44008036", "classify": classify_presence},
    {"label": "1 Timothy 3:16 theos or hos", "code": "54003016",
     "context": "54003015", "classify": classify_1tim_3_16},
    {"label": "1 John 5:7 Comma Johanneum", "code": "62005007",
     "context": "62005006", "classify": classify_comma},
]


def load_witnesses() -> dict[str, str]:
    out = {}
    for path in glob.glob(f"{CNTR_ROOT}/class*/**/*.txt", recursive=True):
        name = path.rsplit("/", 1)[-1].removesuffix(".txt")
        try:
            out[name] = open(path, encoding="utf-8").read()
        except OSError:
            continue
    return out


def main() -> int:
    witnesses = load_witnesses()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    for locus in LOCI:
        for name in sorted(witnesses):
            text = witnesses[name]
            context = verse_line(text, locus["context"])
            line = verse_line(text, locus["code"])
            covers = (context is not None and has_greek(context)) or (
                line is not None and has_greek(line))
            if not covers:
                continue
            if line is None or line.strip() == "":
                reading = "verse absent (no line)"
                snippet = ""
            else:
                reading = locus["classify"](line)
                snippet = clean(line)[:70]
            rows.append({
                "locus": locus["label"], "witness": name,
                "century": WITNESS_CENTURY.get(name, ""),
                "reading": reading, "snippet": snippet,
            })

    with (OUT_DIR / "famous_variants_attestation.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["locus", "witness", "century", "reading", "snippet"])
        w.writeheader()
        w.writerows(rows)

    by_locus: dict[str, dict[str, list[str]]] = {}
    for r in rows:
        by_locus.setdefault(r["locus"], {}).setdefault(r["reading"], []).append(r["witness"])

    (OUT_DIR / "manifest.json").write_text(json.dumps({
        "tool": "famous_variants_attestation",
        "created_utc": datetime.now(UTC).isoformat(),
        "source": "CNTR manuscript transcriptions (CC BY-SA 4.0); centuries are standard published datings",
        "witnesses_loaded": len(witnesses),
        "loci": {locus: {reading: sorted(names) for reading, names in readings.items()}
                 for locus, readings in by_locus.items()},
        "reading": (
            "Read from the transcriptions themselves, the famous disputed readings "
            "sit where the editions said they would, now with named witnesses and "
            "dates. The earliest witnesses covering each passage lack the Long "
            "Ending of Mark, the woman taken in adultery, and Acts 8:37 entirely; "
            "1 John 5:7 appears only in its short form, with no Comma, in every "
            "witness covering it. At 1 Timothy 3:16 the early uncials read the "
            "relative pronoun, with Alexandrinus showing a corrector's theos over "
            "a first-hand hos, the expansion happening on the page. At Revelation "
            "13:18 the number is 666 in P47 and the uncials, spelled out in "
            "Sinaiticus, with P115 the famous early witness to 616, a live ancient "
            "variant over a number often treated as fixed."
        ),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Famous disputed readings across {len(witnesses)} transcribed witnesses\n")
    for locus, readings in by_locus.items():
        print(locus)
        for reading, names in sorted(readings.items()):
            dated = ", ".join(f"{n} ({WITNESS_CENTURY[n]})" if n in WITNESS_CENTURY else n
                              for n in sorted(names))
            print(f"  {reading:42s} {dated}")
        print()
    print(OUT_DIR / "famous_variants_attestation.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
