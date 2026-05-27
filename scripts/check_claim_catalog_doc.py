#!/usr/bin/env python3
"""Validate claim-catalog markdown summary against the source CSV."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

DEFAULT_CATALOG = Path("claims/claim_catalog.csv")
DEFAULT_DOC = Path("docs/CLAIM_CATALOG.md")

CATALOG_FIELDNAMES = [
    "claim_id",
    "claim_group",
    "source_label",
    "source_url",
    "status",
    "language",
    "corpus_scope",
    "terms",
    "spellings_or_forms",
    "skip_or_rule",
    "layout_or_metric",
    "current_reproduction",
    "evidence",
    "notes",
]

ALLOWED_DOC_STATUSES = {
    "reproducible",
    "partially_reproducible",
    "controlled_review_candidate",
    "not_reproducible",
    "under_specified",
    "license_blocked",
    "mixed",
}

EXPECTED_CURRENT_ENTRY_GROUPS = [
    (
        "Common Torah skip-50 examples",
        [
            "torah_forward_50_genesis",
            "torah_forward_50_exodus",
            "torah_reverse_50_numbers",
            "torah_reverse_49_deuteronomy",
            "yhwh_leviticus_skip8",
        ],
    ),
    ("WRR 1994 rabbis", ["wrr_1994_great_rabbis"]),
    (
        "Torah-code.org Cities/Aumann/Simon-McKay source chain",
        ["cities_aumann_simon_mckay_source_chain"],
    ),
    (
        "Greek `δοξα` (doxa; English: glory) extension follow-up",
        ["doxa_exact_center_extension"],
    ),
    (
        "Greek `γωγ` (Gog; English: Gog) centered occurrence",
        ["gog_rev_20_8_centered_occurrence"],
    ),
    ("Greek expanded surface follow-up", ["greek_expanded_surface_followup"]),
    (
        "Greek lexicon extension prospective follow-up",
        ["greek_lexicon_common_pronoun_extension"],
    ),
    (
        "All-codes `יום יהוה` (yom YHWH; English: day of YHWH) compound-extension follow-up",
        ["all_codes_yom_yhwh_compound_extension"],
    ),
    ("CRD exact center-word broad screen", ["crd_exact_center_word_broad_screen"]),
    ("Greek length-4 surface follow-up", ["greek_surface_length4_vocab_controls"]),
    ("Modern/geopolitical short forms", ["modern_geopolitical_short_forms"]),
    ("Full modern country phrases", ["modern_full_country_phrases"]),
    ("Local business/place terms", ["local_business_place_terms"]),
    (
        "Apocrypha bridge-completion study",
        [
            "lxx_apocrypha_bridge_boundary",
            "kjva_apocrypha_bridge_boundary",
        ],
    ),
    (
        "Bible Code Digest claim families",
        [
            "bcd_yeshua_messiah_extensions",
            "bcd_isaiah53_psalm22_yeshua",
            "bcd_king_david_underscoring",
            "bcd_ezekiel_war_temple",
            "bcd_who_like_god_searches",
            "bcd_shimon_peres_politics",
            "bcd_obama_us_election",
            "bcd_disaster_crisis_clusters",
        ],
    ),
    (
        "TheWordNotes / Rambsel / Jeffrey claim families",
        [
            "thewordnotes_source_version_sensitivity",
            "thewordnotes_grant_jeffrey_historical_clusters",
            "thewordnotes_rambsel_yeshua_examples",
            "thewordnotes_isaiah53_rambsel_table",
        ],
    ),
    (
        "Cosmic Codes claim families",
        [
            "cosmic_codes_torah_tree_wrr_examples",
            "cosmic_codes_holocaust_historical_clusters",
            "cosmic_codes_yeshua_isaiah53_table",
            "cosmic_codes_numerics_macrocodes",
            "cosmic_codes_rabin_microcode",
        ],
    ),
    (
        "Mark Tabata Isaiah 53 claim families",
        [
            "mark_tabata_isaiah53_cluster",
            "mark_tabata_wrr_gans_statistics",
        ],
    ),
    (
        "Felcjo Ringo algorithm/control source",
        ["felcjo_ringo_algorithm_control_source"],
    ),
    (
        "Bible and Science critique/source families",
        [
            "bible_and_science_els_critique_controls",
            "bible_and_science_textual_variation_guardrail",
            "bible_and_science_non_els_codes",
        ],
    ),
    (
        "Religions Wiki scriptural-code critique families",
        [
            "religions_wiki_scriptural_codes_critique",
            "religions_wiki_quran_numeric_codes",
            "religions_wiki_gematria_theomatics",
            "religions_wiki_methodology_guardrails",
        ],
    ),
    (
        "Amandasaurus/Rory Biblecode implementation prior art",
        ["amandasaurus_biblecode_prior_art"],
    ),
    (
        "Bible-codes.org pictogram/source families",
        [
            "bible_codes_org_intro_matrix",
            "bible_codes_org_pictogram_clusters",
            "bible_codes_org_authenticity_criteria",
            "bible_codes_org_prediction_claims",
            "bible_codes_org_warnings",
        ],
    ),
    (
        "Public media-style Hebrew claims",
        [
            "rabin_assassination_hebrew",
            "hitler_shoah_hebrew",
            "jesus_hebrew_phrases",
        ],
    ),
    (
        "Critical omissions / word multiples",
        [
            "critical_omission_breakage",
            "word_multiples_omissions",
        ],
    ),
]


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    failures = validate_claim_catalog_doc(args.catalog, args.doc)
    if failures:
        for failure in failures:
            print(f"claim-catalog doc failure: {failure}", file=sys.stderr)
        return 1
    print(f"claim-catalog doc ok: {args.doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--doc", type=Path, default=DEFAULT_DOC)
    return parser


def validate_claim_catalog_doc(
    catalog: Path = DEFAULT_CATALOG, doc: Path = DEFAULT_DOC
) -> list[str]:
    if not catalog.exists():
        return [f"{catalog} is missing"]
    if not doc.exists():
        return [f"{doc} is missing"]
    catalog_fieldnames, catalog_rows = read_catalog_rows(catalog)
    table_rows = parse_current_entries_table(doc.read_text(encoding="utf-8"))
    if not table_rows:
        return [f"{doc} has no Current Entries table rows"]
    failures: list[str] = []
    if catalog_fieldnames != CATALOG_FIELDNAMES:
        failures.append(f"{catalog} fieldnames drifted")
    entry_total = 0
    for row in table_rows:
        status = unquote_code(row["status"])
        if status not in ALLOWED_DOC_STATUSES:
            failures.append(f"{doc} has unknown Current Entries status: {status}")
        try:
            entries = int(row["entries"])
        except ValueError:
            failures.append(f"{doc} has non-integer entry count for {row['group']}: {row['entries']}")
            continue
        if entries <= 0:
            failures.append(f"{doc} has non-positive entry count for {row['group']}: {entries}")
        entry_total += entries
        if not row["current_read"].strip():
            failures.append(f"{doc} has empty Current read for {row['group']}")
    if entry_total != len(catalog_rows):
        failures.append(
            f"{doc} Current Entries total is {entry_total}, but {catalog} has {len(catalog_rows)} rows"
        )
    failures.extend(validate_expected_current_entries(catalog_rows, table_rows, doc))
    if "claims/claim_catalog.csv" not in doc.read_text(encoding="utf-8"):
        failures.append(f"{doc} does not cite claims/claim_catalog.csv")
    return failures


def validate_expected_current_entries(
    catalog_rows: list[dict[str, str]],
    table_rows: list[dict[str, str]],
    doc: Path,
) -> list[str]:
    by_id = {row.get("claim_id", ""): row for row in catalog_rows}
    expected_ids = {
        claim_id
        for _, claim_ids in EXPECTED_CURRENT_ENTRY_GROUPS
        for claim_id in claim_ids
    }
    if not expected_ids.issubset(by_id):
        return []
    expected_rows = []
    for group, claim_ids in EXPECTED_CURRENT_ENTRY_GROUPS:
        statuses = {by_id[claim_id]["status"] for claim_id in claim_ids}
        status = next(iter(statuses)) if len(statuses) == 1 else "mixed"
        expected_rows.append(
            {
                "group": group,
                "status": status,
                "entries": str(len(claim_ids)),
            }
        )
    actual_rows = [
        {
            "group": row["group"],
            "status": unquote_code(row["status"]),
            "entries": row["entries"],
        }
        for row in table_rows
    ]
    if actual_rows != expected_rows:
        return [f"{doc} Current Entries rows drifted"]
    return []


def read_catalog_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames or [], list(reader)


def parse_current_entries_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_section = False
    for line in text.splitlines():
        if line == "## Current Entries":
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        if line.startswith("| ---") or line.startswith("| Group"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split(" | ")]
        if len(parts) != 4:
            continue
        group, status, entries, current_read = parts
        rows.append(
            {
                "group": group,
                "status": status,
                "entries": entries,
                "current_read": current_read,
            }
        )
    return rows


def unquote_code(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`"):
        return value[1:-1]
    return value


if __name__ == "__main__":
    raise SystemExit(main())
