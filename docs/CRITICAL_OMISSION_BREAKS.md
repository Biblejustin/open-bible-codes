# Critical Omission Breaks

Question:

- Do TR ELS hits break when verse blocks absent from SBLGNT are removed?

Method:

- Base text: local TR Greek NT.
- Critical text: SBLGNT.
- Missing refs detected by TR ref vs SBLGNT ref.
- Adjacent merge and renumber cases are not counted as deleted blocks.
- ELS scope: Greek terms from theological, modern-name/date, and Table-of-Nations lists.
- Skip range: 2..50, both directions.
- Break rule: a TR hit breaks if one or more ELS letters fall inside a deleted block, or if the deleted block changes equal spacing between retained letters.

Command:

```bash
python3 -m scripts.analyze_critical_omission_breaks
```

Outputs:

- `reports/critical_omission_missing_verses.csv`
- `reports/critical_omission_breaks_summary.csv`
- `reports/critical_omission_breaks_examples.csv`
- `reports/critical_omission_breaks_by_verse.csv`
- `reports/critical_omission_breaks.manifest.json`

Input Stats:

- TR Greek NT: 692,948 normalized letters; 7,957 verses.
- SBLGNT: 679,879 normalized letters; 7,939 verses.
- Greek term rows checked: 160.
- TR hits checked: 60,381.
- Ref-missing verses: 20.
- Deleted blocks used: 18.
- Deleted letters used: 1,223.

Ref-Missing But Not Counted As Deleted:

- Acts 19:41: adjacent merge into SBLGNT Acts 19:40.
- 2 Corinthians 13:14: content renumbered as SBLGNT 2 Corinthians 13:13, minus final `αμην` (amen; English: amen).

Broken Hits:

- Broken total: 202.
- Broken by removed ELS letter: 197.
- Broken by spacing only: 5.
- Preserved across deleted block: 0.

Top Broken Terms:

- Noah: `νωε` (Noe; English: Noah), 49.
- Hul: `ουλ` (Oul; English: Hul), 41.
- Temple: `ναος` (naos; English: temple), 18.
- Son: `υιος` (huios; English: son), 13.
- Iran: `ιραν` (iran; English: Iran), 8.
- Blood: `αιμα` (haima; English: blood), 7.
- Shem: `σημ` (Sem; English: Shem), 7.
- Ham: `χαμ` (Cham; English: Ham), 7.

Top Deleted Blocks:

- Romans 16:25: 22 broken hits.
- Mark 9:44: 19.
- John 5:4: 19.
- Mark 11:26: 18.
- Mark 9:46: 16.
- Matthew 23:14: 13.
- Romans 16:26: 13.

Cautions:

- This isolates verse-block removal only.
- It does not measure all TR vs critical textual variants.
- Short terms dominate results.
- Raw break counts are not significance tests.
