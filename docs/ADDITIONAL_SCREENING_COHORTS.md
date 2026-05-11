# Additional Screening Cohorts

This document records the added screening cohorts that expand the broad ELS search lists without treating any row as interpretive evidence by itself.

## Scope

The added CSV files are:

| File | Purpose |
| --- | --- |
| `terms/biblical_narrative_names.csv` | Joshua/Jesus referent guardrail, matriarchs, narrative names, and NT figures not already isolated as a cohort. |
| `terms/biblical_prophets_cohort.csv` | Major and minor prophets as a fixed cohort for book/context clustering checks. |
| `terms/eschatology_expanded_terms.csv` | Antichrist, tribulation, rapture, 666, number of the beast, and end-language terms. |
| `terms/isaiah53_servant_cohort.csv` | Isaiah 53 servant vocabulary for the existing Isaiah 53 claim-source audit path. |
| `terms/tabernacle_temple_terms.csv` | Tabernacle, ark, mercy seat, menorah, cherubim, holy of holies, temple, and altar terms. |
| `terms/daniel_statue_metals.csv` | Gold, silver, bronze, iron, and clay as a Daniel 2/7 thematic cohort. |
| `terms/hebrew_anno_mundi_years.csv` | Hebrew Anno Mundi year encodings for common modern-event years. |
| `terms/modern_disaster_war_terms.csv` | Disaster, disease, and named-war terms for modern-event screening. |
| `terms/maccabean_apocrypha_names.csv` | Named-entity bridge terms for Maccabean and apocrypha-focused follow-up. |
| `terms/theological_terms.csv` | Also includes the expanded names/titles of God additions: El Shaddai, El Elyon, YHWH Tzevaot, Sabaoth, Ehyeh, Yah, Father, Holy Spirit, and Trinity. |

## Wiring

These files are wired into:

- `protocols/broad_search.toml`
- `protocols/hebrew_screening_all_codes_collection.toml`
- `protocols/greek_screening_all_codes_collection.toml`
- `terms/english_search_terms.csv`, generated from declared concept labels

They are not automatically added to the focused full-span dynamic-skip term file. Full-span searches are much more expensive, so promotion into `terms/dynamic_skip_focus_terms.csv` should remain a separate declared step.

## Cautions

- These rows are screening terms, not findings.
- Duplicate concepts across files are intentional when a cohort boundary matters.
- Short terms such as `קץ`, `רות`, or `עון` have high background pressure and should be interpreted through controls.
- Greek `ιησους` can refer to Joshua or Jesus depending on surface context; reports must preserve that referent caveat.
- Hebrew Anno Mundi years map across partial Gregorian years, so report language should say "near" or "spans" unless a study locks an exact calendar window.

## Next Run

Use the broad all-codes protocols for first-pass searches:

```bash
python3 -m scripts.run_protocol protocols/hebrew_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/greek_screening_all_codes_collection.toml --resume
python3 -m scripts.run_protocol protocols/english_screening_all_codes_collection.toml --resume
```

For a counts-only pass across all public corpora:

```bash
python3 -m scripts.run_protocol protocols/broad_search.toml --resume
```
