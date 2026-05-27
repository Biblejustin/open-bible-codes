# Critical Omission Breaks: Gospel People And Genealogy

## Setup

This follow-up runs the TR-vs-SBLGNT critical-omission break detector against
the locked Gospel people, disciples, women, and Christ-genealogy term cohort.

Input term list:

- `terms/gospel_people_genealogy_prospective_terms.csv`

Command:

```bash
python3 -m scripts.analyze_critical_omission_breaks \
  --no-default-terms \
  --extra-terms terms/gospel_people_genealogy_prospective_terms.csv \
  --out-suffix _gospel_people_genealogy \
  --min-term-length 4
```

The `--min-term-length 4` gate matches the prospective study lock. The script's
default remains `3` for older omission-break runs.

## Method

The detector searches Greek TR ELS hits at skip `2..50`, direction `both`, then
checks whether the same letter path survives after removing the SBLGNT-absent
TR verse blocks.

Rows are counted as broken only when:

- a sequence letter falls inside an omitted block; or
- the deleted block changes spacing across the ELS path.

This run uses the same break-counting engine as the main critical-omission
study. Hebrew rows in the cohort are not used here because this detector is a
Greek TR/SBLGNT comparison.

## Results

Output files:

- `reports/critical_omission_breaks_gospel_people_genealogy_summary.csv`
- `reports/critical_omission_breaks_gospel_people_genealogy_examples.csv`
- `reports/critical_omission_breaks_gospel_people_genealogy_by_verse.csv`
- `reports/critical_omission_missing_verses_gospel_people_genealogy.csv`
- `reports/critical_omission_breaks_gospel_people_genealogy.manifest.json`

Observed totals:

| Metric | Value |
| --- | ---: |
| Greek term rows loaded | 98 |
| Minimum normalized length | 4 |
| TR hits searched | 11,860 |
| Span-intersecting hits | 50 |
| Broken hits | 50 |
| Broken by removed letter | 50 |
| Broken by spacing only | 0 |
| Terms with at least one break | 16 |
| Deleted blocks used | 18 |

Top broken terms:

| Term ID | Concept | Normalized | TR hits | Broken hits |
| --- | --- | --- | ---: | ---: |
| `gpg_anna_g` | Anna | `αννα` | 5,396 | 18 |
| `gpg_enos_g` | Enosh | `ενωσ` | 1,281 | 6 |
| `gpg_booz_g` | Boaz | `βοεσ` | 277 | 3 |
| `gpg_thara_g` | Terah | `θαρα` | 453 | 3 |
| `gpg_aram_g` | Ram Aram | `αραμ` | 858 | 2 |
| `gpg_achaz_g` | Ahaz | `αχασ` | 465 | 2 |
| `gpg_achim_g` | Achim | `αχιμ` | 172 | 2 |
| `gpg_mary_g` | Mary | `μαρια` | 77 | 2 |
| `gpg_jared_g` | Jared | `ιαρεδ` | 50 | 2 |
| `gpg_eber_g` | Eber | `εβερ` | 129 | 2 |
| `gpg_nathan_g` | Nathan | `ναθαν` | 80 | 2 |
| `gpg_annas_g` | Annas | `αννασ` | 403 | 2 |

Top omitted verses by broken hits:

| Omitted verse | Broken hits |
| --- | ---: |
| `MRK 9:46` | 12 |
| `LUK 23:17` | 9 |
| `JHN 5:4` | 6 |
| `MRK 15:28` | 4 |
| `ACT 24:7` | 3 |
| `ROM 16:26` | 3 |
| `ROM 16:27` | 3 |

## Cautions

Raw break counts are not significance tests. This report says which locked
Gospel-name ELS rows are disrupted by the registered TR/SBLGNT omission blocks.
It does not by itself establish intent, meaning, theological weight, or unusual
frequency.

Short and common surface forms can dominate raw counts. Matching the prospective
lock's minimum length removes the three-letter rows from this follow-up, but
four-letter forms can still be frequent enough to need controls before
interpretation.
