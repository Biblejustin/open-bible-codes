#!/usr/bin/env python3
"""Audit coverage for the latest user-requested term expansion cohorts."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

from els import __version__
from els.normalization import normalize_text
from els.term_display import display_term


DEFAULT_OUT = Path("reports/requested_term_expansion_coverage/coverage.csv")
DEFAULT_MARKDOWN = Path("docs/REQUESTED_TERM_EXPANSION_COVERAGE.md")
DEFAULT_MANIFEST = Path("reports/requested_term_expansion_coverage/manifest.json")

FIELDNAMES = [
    "group",
    "concept",
    "expected_languages",
    "matched_languages",
    "status",
    "matched_files",
    "matched_term_ids",
    "matched_terms",
    "notes",
]


@dataclass(frozen=True)
class RequestedConcept:
    group: str
    concept: str
    expected_languages: frozenset[str]
    expected_terms: tuple[tuple[str, str], ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class TermRow:
    path: Path
    term_id: str
    concept: str
    category: str
    language: str
    term: str
    normalized: str


def req(
    group: str,
    concept: str,
    *expected_languages: str,
    hebrew: str | None = None,
    greek: str | None = None,
    english: str | None = None,
    notes: str = "",
) -> RequestedConcept:
    terms: list[tuple[str, str]] = []
    for language, term in (("hebrew", hebrew), ("greek", greek), ("english", english)):
        if term:
            terms.append((language, term))
    return RequestedConcept(
        group=group,
        concept=concept,
        expected_languages=frozenset(expected_languages),
        expected_terms=tuple(terms),
        notes=notes,
    )


REQUESTED_CONCEPTS: tuple[RequestedConcept, ...] = (
    # Biblical narrative names.
    req("biblical_narrative_names", "Joshua", "hebrew", "greek", hebrew="יהושע", greek="ιησους"),
    req("biblical_narrative_names", "Solomon", "hebrew", "greek", hebrew="שלמה", greek="σολομων"),
    req("biblical_narrative_names", "Esther", "hebrew", "greek", hebrew="אסתר", greek="εσθηρ"),
    req("biblical_narrative_names", "Ruth", "hebrew", "greek", hebrew="רות", greek="ρουθ"),
    req("biblical_narrative_names", "Hannah", "hebrew", "greek", hebrew="חנה", greek="αννα"),
    req("biblical_narrative_names", "Samuel", "hebrew", "greek", hebrew="שמואל", greek="σαμουηλ"),
    req("biblical_narrative_names", "Rebekah", "hebrew", "greek", hebrew="רבקה", greek="ρεβεκκα"),
    req("biblical_narrative_names", "Rachel", "hebrew", "greek", hebrew="רחל", greek="ραχηλ"),
    req("biblical_narrative_names", "Leah", "hebrew", "greek", hebrew="לאה", greek="λεια"),
    req("biblical_narrative_names", "James", "greek", greek="ιακωβος"),
    req("biblical_narrative_names", "Andrew", "greek", greek="ανδρεας"),
    req("biblical_narrative_names", "Thomas", "greek", greek="θωμας"),
    req("biblical_narrative_names", "Matthew", "greek", greek="ματθαιος"),
    req("biblical_narrative_names", "Philip", "greek", greek="φιλιππος"),
    req("biblical_narrative_names", "Stephen", "greek", greek="στεφανος"),
    req("biblical_narrative_names", "Barnabas", "hebrew", "greek", hebrew="ברנבא", greek="βαρναβας"),
    req(
        "biblical_narrative_names",
        "Mary Magdalene",
        "hebrew",
        "greek",
        hebrew="מרים המגדלית",
        greek="μαρια μαγδαληνη",
    ),
    req("biblical_narrative_names", "Lazarus", "hebrew", "greek", hebrew="אלעזר", greek="λαζαρος"),
    req("biblical_narrative_names", "Caiaphas", "hebrew", "greek", hebrew="קיפא", greek="καιαφας"),
    # Prophets.
    req("prophets", "Isaiah", "hebrew", "greek", hebrew="ישעיהו", greek="ησαιας"),
    req("prophets", "Jeremiah", "hebrew", "greek", hebrew="ירמיהו", greek="ιερεμιας"),
    req("prophets", "Ezekiel", "hebrew", "greek", hebrew="יחזקאל", greek="ιεζεκιηλ"),
    req("prophets", "Daniel", "hebrew", "greek", hebrew="דניאל", greek="δανιηλ"),
    req("prophets", "Hosea", "hebrew", "greek", hebrew="הושע", greek="ωσηε"),
    req("prophets", "Joel", "hebrew", "greek", hebrew="יואל", greek="ιωηλ"),
    req("prophets", "Amos", "hebrew", "greek", hebrew="עמוס", greek="αμως"),
    req("prophets", "Obadiah", "hebrew", "greek", hebrew="עבדיה", greek="αβδιου"),
    req("prophets", "Jonah", "hebrew", "greek", hebrew="יונה", greek="ιωνας"),
    req("prophets", "Micah", "hebrew", "greek", hebrew="מיכה", greek="μιχαιας"),
    req("prophets", "Nahum", "hebrew", "greek", hebrew="נחום", greek="ναουμ"),
    req("prophets", "Habakkuk", "hebrew", "greek", hebrew="חבקוק", greek="αμβακουμ"),
    req("prophets", "Zephaniah", "hebrew", "greek", hebrew="צפניה", greek="σοφονιας"),
    req("prophets", "Haggai", "hebrew", "greek", hebrew="חגי", greek="αγγαιος"),
    req("prophets", "Zechariah", "hebrew", "greek", hebrew="זכריה", greek="ζαχαριας"),
    req("prophets", "Malachi", "hebrew", "greek", hebrew="מלאכי", greek="μαλαχιας"),
    # Eschatology.
    req("eschatology", "Antichrist", "greek", greek="αντιχριστος"),
    req("eschatology", "Tribulation", "hebrew", "greek", hebrew="צרה", greek="θλιψις"),
    req("eschatology", "Rapture", "greek", greek="αρπαγη"),
    req("eschatology", "Harpazo", "greek", greek="αρπαζω"),
    req("eschatology", "Millennium", "hebrew", "greek", hebrew="אלף שנים", greek="χιλια ετη"),
    req("eschatology", "Number of the Beast", "hebrew", "greek", hebrew="מספר החיה", greek="αριθμος θηριου"),
    req("eschatology", "666", "hebrew", "greek", hebrew="תרו", greek="χξϛ"),
    req("eschatology", "End", "hebrew", hebrew="קץ"),
    # Isaiah 53 servant cohort.
    req("isaiah53_servant", "Servant", "hebrew", "greek", hebrew="עבד", greek="δουλος"),
    req("isaiah53_servant", "Transgression", "hebrew", "greek", hebrew="פשע", greek="ανομια"),
    req("isaiah53_servant", "Iniquity", "hebrew", "greek", hebrew="עון", greek="αμαρτια"),
    req("isaiah53_servant", "Wound", "hebrew", "greek", hebrew="חבורה", greek="μωλωψ"),
    req("isaiah53_servant", "Lamb", "hebrew", "greek", hebrew="שה", greek="αμνος"),
    req("isaiah53_servant", "Silent", "hebrew", "greek", hebrew="נאלם", greek="αφωνος"),
    req("isaiah53_servant", "Grave", "hebrew", "greek", hebrew="קבר", greek="ταφος"),
    # Tabernacle / temple.
    req("tabernacle_temple", "Mishkan", "hebrew", hebrew="משכן"),
    req("tabernacle_temple", "Ark", "hebrew", "greek", hebrew="ארון", greek="κιβωτος"),
    req("tabernacle_temple", "Mercy Seat", "hebrew", "greek", hebrew="כפרת", greek="ιλαστηριον"),
    req("tabernacle_temple", "Menorah", "hebrew", "greek", hebrew="מנורה", greek="λυχνια"),
    req("tabernacle_temple", "Cherubim", "hebrew", "greek", hebrew="כרובים", greek="χερουβιμ"),
    req("tabernacle_temple", "Holy of Holies", "hebrew", "greek", hebrew="קדש הקדשים", greek="αγια αγιων"),
    # Divine names.
    req("divine_names", "El Shaddai", "hebrew", hebrew="אל שדי"),
    req("divine_names", "El Elyon", "hebrew", hebrew="אל עליון"),
    req("divine_names", "YHWH Tzevaot", "hebrew", hebrew="יהוה צבאות"),
    req("divine_names", "Ehyeh", "hebrew", hebrew="אהיה"),
    req("divine_names", "Yah", "hebrew", hebrew="יה"),
    req("divine_names", "Holy Spirit", "hebrew", "greek", hebrew="רוח הקדש", greek="πνευμα αγιον"),
    req("divine_names", "Trinity", "greek", greek="τριας"),
    req("divine_names", "Father", "greek", greek="πατηρ"),
    # Daniel 2/7 metals.
    req("daniel_metals", "Gold", "hebrew", "greek", hebrew="זהב", greek="χρυσος"),
    req("daniel_metals", "Silver", "hebrew", "greek", hebrew="כסף", greek="αργυρος"),
    req("daniel_metals", "Bronze", "hebrew", "greek", hebrew="נחשת", greek="χαλκος"),
    req("daniel_metals", "Iron", "hebrew", "greek", hebrew="ברזל", greek="σιδηρος"),
    req("daniel_metals", "Clay", "hebrew", "greek", hebrew="חרס", greek="πηλος"),
    # Plagues.
    req("plagues", "Blood Plague", "hebrew", "greek", hebrew="דם", greek="αιμα"),
    req("plagues", "Frogs Plague", "hebrew", "greek", hebrew="צפרדע", greek="βατραχος"),
    req("plagues", "Lice Plague", "hebrew", "greek", hebrew="כנים", greek="σκνιφες"),
    req("plagues", "Flies Plague", "hebrew", "greek", hebrew="ערב", greek="κυνομυια"),
    req("plagues", "Livestock Plague", "hebrew", "greek", hebrew="דבר", greek="θανατος"),
    req("plagues", "Boils Plague", "hebrew", "greek", hebrew="שחין", greek="ελκη"),
    req("plagues", "Hail Plague", "hebrew", "greek", hebrew="ברד", greek="χαλαζα"),
    req("plagues", "Locust Plague", "hebrew", "greek", hebrew="ארבה", greek="ακριδες"),
    req("plagues", "Darkness Plague", "hebrew", "greek", hebrew="חשך", greek="σκοτος"),
    req("plagues", "Plague Of Firstborn", "hebrew", "greek", hebrew="מכת בכורות", greek="πληγη πρωτοτοκων"),
    # Apocrypha / Maccabean bridge names.
    req("maccabean_apocrypha", "Antiochus", "hebrew", "greek", hebrew="אנטיוכוס", greek="αντιοχος"),
    req("maccabean_apocrypha", "Mattathias", "hebrew", "greek", hebrew="מתתיהו", greek="ματταθιας"),
    req("maccabean_apocrypha", "Judah Maccabee", "hebrew", "greek", hebrew="יהודה המכבי", greek="ιουδας μακκαβαιος"),
    req("maccabean_apocrypha", "Eleazar", "hebrew", "greek", hebrew="אלעזר", greek="ελεαζαρ"),
    req("maccabean_apocrypha", "Tobit", "hebrew", "greek", hebrew="טוביה", greek="τωβιτ"),
    req("maccabean_apocrypha", "Judith", "hebrew", "greek", hebrew="יהודית", greek="ιουδιθ"),
    req("maccabean_apocrypha", "Holofernes", "hebrew", "greek", hebrew="הולופרנס", greek="ολοφερνης"),
    # Modern chronology / events.
    req("hebrew_anno_mundi_years", "AM 5708", "hebrew", hebrew="התשח"),
    req("hebrew_anno_mundi_years", "AM 5727", "hebrew", hebrew="התשכז"),
    req("hebrew_anno_mundi_years", "AM 5733", "hebrew", hebrew="התשלג"),
    req("hebrew_anno_mundi_years", "AM 5784", "hebrew", hebrew="התשפד"),
    req("hebrew_anno_mundi_years", "AM 5790", "hebrew", hebrew="התשצ"),
    req("hebrew_anno_mundi_years", "AM 5793", "hebrew", hebrew="התשצג"),
    req("modern_disasters_wars", "Earthquake", "hebrew", "greek", hebrew="רעש", greek="σεισμος"),
    req("modern_disasters_wars", "Tsunami", "hebrew", hebrew="צונאמי"),
    req("modern_disasters_wars", "Volcano", "hebrew", hebrew="הר געש"),
    req("modern_disasters_wars", "Cancer", "hebrew", hebrew="סרטן"),
    req("modern_disasters_wars", "Ebola", "hebrew", hebrew="אבולה"),
    req("modern_disasters_wars", "World War I", "hebrew", hebrew="מלחמת העולם הראשונה"),
    req("modern_disasters_wars", "World War II", "hebrew", hebrew="מלחמת העולם השניה"),
    req("modern_disasters_wars", "Korean War", "hebrew", hebrew="מלחמת קוריאה"),
    req("modern_disasters_wars", "Vietnam War", "hebrew", hebrew="מלחמת וייטנאם"),
    req("modern_disasters_wars", "Cold War", "hebrew", hebrew="המלחמה הקרה"),
    req("modern_disasters_wars", "Six-Day War", "hebrew", hebrew="מלחמת ששת הימים"),
    req("modern_disasters_wars", "Yom Kippur War", "hebrew", hebrew="מלחמת יום הכפורים"),
)


def main(argv: list[str] | None = None) -> int:
    started = time.perf_counter()
    args = build_parser().parse_args(argv)
    term_rows = load_term_rows(args.terms_dir)
    rows = audit_requested_concepts(REQUESTED_CONCEPTS, term_rows)
    write_csv(args.out, rows)
    write_markdown(args.markdown_out, rows, args)
    write_manifest(args.manifest_out, args, rows, started)
    print(args.out)
    print(args.markdown_out)
    print(args.manifest_out)
    if args.fail_on_missing and any(row["status"] == "missing" for row in rows):
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--terms-dir", type=Path, default=Path("terms"))
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--markdown-out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--fail-on-missing", action="store_true")
    return parser


def load_term_rows(terms_dir: Path) -> list[TermRow]:
    rows: list[TermRow] = []
    for path in sorted(terms_dir.glob("*.csv")):
        if path.name == "meaningful_constants.csv":
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "term" not in reader.fieldnames:
                continue
            for row in reader:
                language = row.get("language", "").strip()
                term = row.get("term", "").strip()
                rows.append(
                    TermRow(
                        path=path,
                        term_id=row.get("term_id", "").strip(),
                        concept=row.get("concept", "").strip(),
                        category=row.get("category", "").strip(),
                        language=language,
                        term=term,
                        normalized=normalize_text(term, language) if language else "",
                    )
                )
    return rows


def audit_requested_concepts(
    requested_concepts: Iterable[RequestedConcept],
    term_rows: list[TermRow],
) -> list[dict[str, str]]:
    return [coverage_row(requested, term_rows) for requested in requested_concepts]


def coverage_row(requested: RequestedConcept, term_rows: list[TermRow]) -> dict[str, str]:
    matches = matching_rows(requested, term_rows)
    matched_languages = sorted({row.language for row in matches if row.language})
    missing_languages = sorted(requested.expected_languages - set(matched_languages))
    if not matches:
        status = "missing"
    elif missing_languages:
        status = "partial"
    else:
        status = "covered"
    notes = requested.notes
    if missing_languages:
        suffix = "missing languages: " + ", ".join(missing_languages)
        notes = f"{notes}; {suffix}" if notes else suffix
    return {
        "group": requested.group,
        "concept": requested.concept,
        "expected_languages": ";".join(sorted(requested.expected_languages)),
        "matched_languages": ";".join(matched_languages),
        "status": status,
        "matched_files": ";".join(sorted({str(row.path) for row in matches})),
        "matched_term_ids": ";".join(row.term_id for row in matches),
        "matched_terms": "; ".join(display_match(row) for row in matches),
        "notes": notes,
    }


def matching_rows(requested: RequestedConcept, term_rows: list[TermRow]) -> list[TermRow]:
    expected_by_language = {
        (language, normalize_text(term, language)) for language, term in requested.expected_terms
    }
    concept_key = requested.concept.casefold()
    concept_matches = [row for row in term_rows if row.concept.casefold() == concept_key]
    concept_languages = {row.language for row in concept_matches}
    spelling_fallbacks = [
        row
        for row in term_rows
        if row.language not in concept_languages
        and (row.language, row.normalized) in expected_by_language
    ]
    return dedupe_matches([*concept_matches, *spelling_fallbacks])


def dedupe_matches(matches: list[TermRow]) -> list[TermRow]:
    seen: set[tuple[str, str, str]] = set()
    deduped: list[TermRow] = []
    for row in sorted(matches, key=lambda item: (str(item.path), item.term_id, item.language, item.term)):
        key = (str(row.path), row.term_id, row.term)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(row)
    return deduped


def display_match(row: TermRow) -> str:
    return f"{display_term(row.term, english=row.concept or None)} (`{row.term_id}`)"


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    counts = status_counts(rows)
    lines = [
        "# Requested Term Expansion Coverage",
        "",
        "Status: deterministic coverage audit for the latest user-requested term expansion.",
        "This is not an ELS result and does not promote any term to claim status.",
        "",
        "## Reproduce",
        "",
        "```bash",
        reproduce_command(args),
        "```",
        "",
        "## Summary",
        "",
        f"- Requested concepts audited: {len(rows)}",
        f"- Covered: {counts.get('covered', 0)}",
        f"- Partial: {counts.get('partial', 0)}",
        f"- Missing: {counts.get('missing', 0)}",
        "",
        "## Coverage By Group",
        "",
        "| Group | Concepts | Covered | Partial | Missing |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for group in sorted({row["group"] for row in rows}):
        group_rows = [row for row in rows if row["group"] == group]
        group_counts = status_counts(group_rows)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{group}`",
                    str(len(group_rows)),
                    str(group_counts.get("covered", 0)),
                    str(group_counts.get("partial", 0)),
                    str(group_counts.get("missing", 0)),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Details",
            "",
            "| Group | Concept | Status | Expected | Matched | Files |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        files = ", ".join(f"`{Path(path).name}`" for path in row["matched_files"].split(";") if path)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['group']}`",
                    md_cell(row["concept"]),
                    row["status"],
                    md_cell(row["expected_languages"]),
                    md_cell(row["matched_terms"] or row["notes"]),
                    md_cell(files),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Read",
            "",
            "- `covered` means the requested concept is declared in all expected languages.",
            "- `partial` means the concept is declared, but at least one expected language is missing.",
            "- `missing` means no concept or expected normalized spelling was found in `terms/`.",
            "- Hebrew and Greek terms are rendered with transliteration and English gloss where the display table knows them.",
            "- This audit helps prevent duplicate term additions before broader ELS runs.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def status_counts(rows: Iterable[dict[str, str]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return counts


def write_manifest(
    path: Path,
    args: argparse.Namespace,
    rows: list[dict[str, str]],
    started: float,
) -> None:
    payload = {
        "tool": "audit_requested_term_expansion_coverage",
        "version": __version__,
        "generated_utc": datetime.now(UTC).isoformat(),
        "duration_seconds": round(time.perf_counter() - started, 6),
        "commit": git_commit(),
        "inputs": {"terms_dir": str(args.terms_dir)},
        "outputs": {
            "coverage": str(args.out),
            "markdown": str(args.markdown_out),
            "manifest": str(args.manifest_out),
        },
        "requested_concepts": len(rows),
        "status_counts": status_counts(rows),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def reproduce_command(args: argparse.Namespace) -> str:
    return (
        "python3 -m scripts.audit_requested_term_expansion_coverage "
        f"--terms-dir {args.terms_dir} --out {args.out} "
        f"--markdown-out {args.markdown_out} --manifest-out {args.manifest_out}"
    )


def md_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


if __name__ == "__main__":
    raise SystemExit(main())
