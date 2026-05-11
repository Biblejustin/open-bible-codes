# Notable Passage Gaps

This report records declared passages where selected ELS terms are absent, sparse, or present when centered inside the passage.
It is intentionally a screening ledger: absence inside a short passage is often expected, so the useful rows are the terms that are absent in the passage while recurring elsewhere in the same corpus, or present at notably lower density than a uniform placement expectation.

## Run Settings

- Passages: `configs/notable_passage_gap_passages.csv`
- Terms: `terms/notable_passage_gap_terms.csv`
- Skip range: `2..100`
- Direction: `both`
- Minimum normalized term length: `3`
- Common-elsewhere threshold: `10` centered hits outside the passage

## Passage Summary

| Passage | Corpus | Letters | Eligible Terms | Present | Absent Elsewhere | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Leviticus 24 Blasphemy Law | MT_WLC | 1037 | 18 | 14 | 4 | 4 | 0 | 226 | 210.738 |
| Leviticus 24 Blasphemy Law | UXLC | 1037 | 18 | 14 | 4 | 4 | 0 | 226 | 210.717 |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | 1037 | 18 | 14 | 4 | 4 | 0 | 226 | 210.749 |
| Leviticus 24 Blasphemy Law | MAM | 1037 | 18 | 14 | 4 | 4 | 0 | 226 | 210.515 |
| Leviticus 24 Blasphemy Law | UHB | 1037 | 18 | 14 | 4 | 4 | 0 | 226 | 210.620 |

## Notable Absence / Low-Density Rows

| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Sample Center Refs |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 2482 | 0 | 2.150 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `ישראל` (Yisrael; English: Israel) | absent_in_passage_common_elsewhere | 427 | 0 | 0.370 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 184 | 0 | 0.159 |  |
| Leviticus 24 Blasphemy Law | EBIBLE_WLC | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 81 | 0 | 0.070 |  |
| Leviticus 24 Blasphemy Law | MAM | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 2460 | 0 | 2.122 |  |
| Leviticus 24 Blasphemy Law | MAM | `ישראל` (Yisrael; English: Israel) | absent_in_passage_common_elsewhere | 400 | 0 | 0.345 |  |
| Leviticus 24 Blasphemy Law | MAM | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 201 | 0 | 0.173 |  |
| Leviticus 24 Blasphemy Law | MAM | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 86 | 0 | 0.074 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 2480 | 0 | 2.148 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `ישראל` (Yisrael; English: Israel) | absent_in_passage_common_elsewhere | 426 | 0 | 0.369 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 185 | 0 | 0.160 |  |
| Leviticus 24 Blasphemy Law | MT_WLC | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 81 | 0 | 0.070 |  |
| Leviticus 24 Blasphemy Law | UHB | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 2482 | 0 | 2.153 |  |
| Leviticus 24 Blasphemy Law | UHB | `ישראל` (Yisrael; English: Israel) | absent_in_passage_common_elsewhere | 425 | 0 | 0.369 |  |
| Leviticus 24 Blasphemy Law | UHB | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 191 | 0 | 0.166 |  |
| Leviticus 24 Blasphemy Law | UHB | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 80 | 0 | 0.069 |  |
| Leviticus 24 Blasphemy Law | UXLC | `גוג` (Gog; English: Gog) | absent_in_passage_common_elsewhere | 2480 | 0 | 2.148 |  |
| Leviticus 24 Blasphemy Law | UXLC | `ישראל` (Yisrael; English: Israel) | absent_in_passage_common_elsewhere | 426 | 0 | 0.369 |  |
| Leviticus 24 Blasphemy Law | UXLC | `מגוג` (Magog; English: Magog) | absent_in_passage_common_elsewhere | 185 | 0 | 0.160 |  |
| Leviticus 24 Blasphemy Law | UXLC | `משפט` (mshpt; English: Judgment) | absent_in_passage_common_elsewhere | 81 | 0 | 0.070 |  |

## Output Files

- Detail CSV: `reports/notable_passage_gaps/term_gap_detail.csv`
- Passage summary CSV: `reports/notable_passage_gaps/passage_summary.csv`
- Manifest: `reports/notable_passage_gaps/manifest.json`

## Cautions

- This report does not treat absence as a negative proof. It records silence and lower-density rows so they can be reviewed alongside positive centered hits.
- `expected_in_passage_uniform` is a descriptive baseline only; it is not a formal p-value.
- Short surface terms can be skipped by the minimum term length rule; skipped rows remain in the detail CSV for auditability.
