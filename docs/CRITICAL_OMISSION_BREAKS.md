# Critical Omission Breaks

## Setup

Question: do TR ELS hits break when verse blocks absent from SBLGNT are removed?

```bash
python3 -m scripts.analyze_critical_omission_breaks
```

Outputs:

- `reports/critical_omission_missing_verses.csv`
- `reports/critical_omission_breaks_summary.csv`
- `reports/critical_omission_breaks_examples.csv`
- `reports/critical_omission_breaks_by_verse.csv`
- `reports/critical_omission_breaks.manifest.json`

## Method

- Base text: local TR Greek NT.
- Critical text: SBLGNT.
- Missing refs detected by TR ref vs SBLGNT ref.
- Adjacent merge and renumber cases are not counted as deleted blocks.
- ELS scope: Greek terms from theological, modern-name/date, Table-of-Nations, and prophetic lists.
- Skip range: 2..50, both directions.
- Break rule: a TR hit breaks if one or more ELS letters fall inside a deleted block, or if the deleted block changes equal spacing between retained letters.

## Results

Current input stats:

- TR Greek NT: 690,831 normalized letters; 7,957 verses.
- SBLGNT: 679,879 normalized letters; 7,939 verses.
- Greek term rows checked: 458.
- TR hits checked: 172,752.
- Ref-missing verses: 20.
- Deleted blocks used: 20.
- Deleted letters used: 1,479.

Broken hits:

- Broken total: 645.
- Broken by removed ELS letter: 637.
- Broken by spacing only: 8.
- Preserved across deleted block: 0.

Top broken terms:

- Eve: `ευα`, 151.
- United Nations: `οηε`, 86.
- Ur: `ουρ`, 55.
- Noah: `νωε`, 46.
- Hul: `ουλ`, 37.
- USA: `ηπα`, 29.
- Temple: `ναοσ`, 21.
- NATO: `νατο`, 20.

Top deleted blocks:

- 2 Corinthians 13:14: 60 broken hits.
- Romans 16:25: 56.
- Mark 11:26: 47.
- Romans 16:27: 44.
- Romans 16:26: 42.
- Acts 28:29: 41.
- John 5:4: 36.
- Mark 9:44: 34.

## Follow-Ups

The follow-up protocol keeps all break counts on the same engine path:

- Reverse insertion survival: `docs/CRITICAL_OMISSION_BREAKS_REVERSE.md`.
- Cross-tradition status in BYZ_NT and TCG_NT: `docs/CRITICAL_OMISSION_BREAKS_CROSS_TRADITION.md`.
- 1000-shuffle null model: `docs/CRITICAL_OMISSION_BREAKS_NULL.md`.
- Length-stratified read: `docs/CRITICAL_OMISSION_BREAKS_LENGTH_STRATIFIED.md`.
- Disputed-passage override and Pericope checks: `docs/CRITICAL_OMISSION_BREAKS_PERICOPE_OVERRIDE.md`.

Latest null run: observed 645 breaks, p_ge 0.9710, null median 727.

## Cautions

- This isolates verse-block removal only.
- It does not measure all TR vs critical textual variants.
- Short terms dominate results.
- Raw break counts are not significance tests.
