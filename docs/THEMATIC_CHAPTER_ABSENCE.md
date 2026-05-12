# Thematic Chapter Absence

This report records declared passages where selected ELS terms are absent, sparse, or present when centered inside the passage.
It is intentionally a screening ledger: absence inside a short passage is often expected, so the useful rows are the terms that are absent in the passage while recurring elsewhere in the same corpus, or present at notably lower density than a uniform placement expectation.

## Run Settings

- Passages: `configs/notable_passage_gap_passages.csv`
- Config passages disabled: `true`
- Terms: `terms/notable_passage_gap_terms.csv`
- Thematic chapters: `data/study/mappings/thematic_chapters.csv`
- Skip range: `2..100`
- Direction: `both`
- Jobs: `0`
- Minimum normalized term length: `3`
- Common-elsewhere threshold: `10` centered hits outside the passage
- Missing declared passages skipped: `true`

## Highest Gap Passage Rows

These rows rank declared passages by how many eligible terms are absent inside the passage while recurring at least the threshold count elsewhere in the same corpus. Short passages naturally rank high, so use this as a triage list rather than a formal significance test.

| Passage | Corpus | Letters | Present | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Wound Thematic Chapter | EBIBLE_WLC | 666 | 0 | 1 | 0 | 0 | 0.081 |
| Wound Thematic Chapter | MAM | 666 | 0 | 1 | 0 | 0 | 0.078 |
| Wound Thematic Chapter | MT_WLC | 666 | 0 | 1 | 0 | 0 | 0.081 |
| Wound Thematic Chapter | UHB | 666 | 0 | 1 | 0 | 0 | 0.081 |
| Wound Thematic Chapter | UXLC | 666 | 0 | 1 | 0 | 0 | 0.081 |
| Grave Thematic Chapter | LXX | 1434 | 0 | 1 | 0 | 0 | 0.105 |
| Iniquity Thematic Chapter | LXX | 1434 | 0 | 1 | 0 | 0 | 0.088 |
| Silent Thematic Chapter | LXX | 1434 | 0 | 1 | 0 | 0 | 0.013 |
| Bruised Thematic Chapter | EBIBLE_WLC | 666 | 1 | 0 | 0 | 3 | 11.346 |
| Bruised Thematic Chapter | MAM | 666 | 1 | 0 | 0 | 3 | 11.382 |
| Bruised Thematic Chapter | MT_WLC | 666 | 1 | 0 | 0 | 3 | 11.339 |
| Bruised Thematic Chapter | UHB | 666 | 1 | 0 | 0 | 3 | 11.333 |
| Bruised Thematic Chapter | UXLC | 666 | 1 | 0 | 0 | 3 | 11.340 |
| Grave Thematic Chapter | EBIBLE_WLC | 666 | 1 | 0 | 0 | 2 | 5.647 |
| Grave Thematic Chapter | MAM | 666 | 1 | 0 | 0 | 2 | 5.584 |
| Grave Thematic Chapter | MT_WLC | 666 | 1 | 0 | 0 | 2 | 5.649 |
| Grave Thematic Chapter | UHB | 666 | 1 | 0 | 0 | 2 | 5.657 |
| Grave Thematic Chapter | UXLC | 666 | 1 | 0 | 0 | 2 | 5.650 |
| Iniquity Thematic Chapter | EBIBLE_WLC | 666 | 1 | 0 | 0 | 52 | 24.349 |
| Iniquity Thematic Chapter | MAM | 666 | 1 | 0 | 0 | 52 | 24.421 |
| Iniquity Thematic Chapter | MT_WLC | 666 | 1 | 0 | 0 | 52 | 24.347 |
| Iniquity Thematic Chapter | UHB | 666 | 1 | 0 | 0 | 52 | 24.396 |
| Iniquity Thematic Chapter | UXLC | 666 | 1 | 0 | 0 | 52 | 24.350 |
| Lamb Thematic Chapter | EBIBLE_WLC | 666 | 0 | 0 | 0 | 0 | 0.000 |
| Lamb Thematic Chapter | MAM | 666 | 0 | 0 | 0 | 0 | 0.000 |
| Lamb Thematic Chapter | MT_WLC | 666 | 0 | 0 | 0 | 0 | 0.000 |
| Lamb Thematic Chapter | UHB | 666 | 0 | 0 | 0 | 0 | 0.000 |
| Lamb Thematic Chapter | UXLC | 666 | 0 | 0 | 0 | 0 | 0.000 |
| Servant Thematic Chapter | EBIBLE_WLC | 666 | 1 | 0 | 0 | 7 | 7.108 |
| Servant Thematic Chapter | MAM | 666 | 1 | 0 | 0 | 7 | 7.133 |

## Passage Summary

| Passage | Corpus | Letters | Eligible Terms | Present | Absent Elsewhere | Absent Common Elsewhere | Low Vs Uniform | Observed Hits | Uniform Expected Hits |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Gog Thematic Chapter | MT_WLC | 3145 | 1 | 1 | 0 | 0 | 0 | 22 | 6.516 |
| Magog Thematic Chapter | MT_WLC | 3145 | 1 | 1 | 0 | 0 | 0 | 3 | 0.486 |
| Beast Thematic Chapter | MT_WLC | 2022 | 1 | 1 | 0 | 0 | 0 | 101 | 86.663 |
| Servant Thematic Chapter | MT_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 7 | 7.110 |
| Transgression Thematic Chapter | MT_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 12 | 3.757 |
| Iniquity Thematic Chapter | MT_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 52 | 24.347 |
| Wound Thematic Chapter | MT_WLC | 666 | 1 | 0 | 1 | 1 | 0 | 0 | 0.081 |
| Lamb Thematic Chapter | MT_WLC | 666 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Silent Thematic Chapter | MT_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 8 | 2.903 |
| Grave Thematic Chapter | MT_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 2 | 5.649 |
| Bruised Thematic Chapter | MT_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 3 | 11.339 |
| Gog Thematic Chapter | UXLC | 3145 | 1 | 1 | 0 | 0 | 0 | 22 | 6.516 |
| Magog Thematic Chapter | UXLC | 3145 | 1 | 1 | 0 | 0 | 0 | 3 | 0.486 |
| Beast Thematic Chapter | UXLC | 2022 | 1 | 1 | 0 | 0 | 0 | 101 | 86.646 |
| Servant Thematic Chapter | UXLC | 666 | 1 | 1 | 0 | 0 | 0 | 7 | 7.113 |
| Transgression Thematic Chapter | UXLC | 666 | 1 | 1 | 0 | 0 | 0 | 12 | 3.758 |
| Iniquity Thematic Chapter | UXLC | 666 | 1 | 1 | 0 | 0 | 0 | 52 | 24.350 |
| Wound Thematic Chapter | UXLC | 666 | 1 | 0 | 1 | 1 | 0 | 0 | 0.081 |
| Lamb Thematic Chapter | UXLC | 666 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Silent Thematic Chapter | UXLC | 666 | 1 | 1 | 0 | 0 | 0 | 8 | 2.903 |
| Grave Thematic Chapter | UXLC | 666 | 1 | 1 | 0 | 0 | 0 | 2 | 5.650 |
| Bruised Thematic Chapter | UXLC | 666 | 1 | 1 | 0 | 0 | 0 | 3 | 11.340 |
| Gog Thematic Chapter | EBIBLE_WLC | 3145 | 1 | 1 | 0 | 0 | 0 | 22 | 6.521 |
| Magog Thematic Chapter | EBIBLE_WLC | 3145 | 1 | 1 | 0 | 0 | 0 | 3 | 0.483 |
| Beast Thematic Chapter | EBIBLE_WLC | 2022 | 1 | 1 | 0 | 0 | 0 | 101 | 86.657 |
| Servant Thematic Chapter | EBIBLE_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 7 | 7.108 |
| Transgression Thematic Chapter | EBIBLE_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 12 | 3.757 |
| Iniquity Thematic Chapter | EBIBLE_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 52 | 24.349 |
| Wound Thematic Chapter | EBIBLE_WLC | 666 | 1 | 0 | 1 | 1 | 0 | 0 | 0.081 |
| Lamb Thematic Chapter | EBIBLE_WLC | 666 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Silent Thematic Chapter | EBIBLE_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 8 | 2.903 |
| Grave Thematic Chapter | EBIBLE_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 2 | 5.647 |
| Bruised Thematic Chapter | EBIBLE_WLC | 666 | 1 | 1 | 0 | 0 | 0 | 3 | 11.346 |
| Gog Thematic Chapter | MAM | 3151 | 1 | 1 | 0 | 0 | 0 | 22 | 6.449 |
| Magog Thematic Chapter | MAM | 3151 | 1 | 1 | 0 | 0 | 0 | 3 | 0.527 |
| Beast Thematic Chapter | MAM | 2104 | 1 | 1 | 0 | 0 | 0 | 103 | 89.980 |
| Servant Thematic Chapter | MAM | 666 | 1 | 1 | 0 | 0 | 0 | 7 | 7.133 |
| Transgression Thematic Chapter | MAM | 666 | 1 | 1 | 0 | 0 | 0 | 12 | 3.765 |
| Iniquity Thematic Chapter | MAM | 666 | 1 | 1 | 0 | 0 | 0 | 52 | 24.421 |
| Wound Thematic Chapter | MAM | 666 | 1 | 0 | 1 | 1 | 0 | 0 | 0.078 |
| Lamb Thematic Chapter | MAM | 666 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Silent Thematic Chapter | MAM | 666 | 1 | 1 | 0 | 0 | 0 | 8 | 2.883 |
| Grave Thematic Chapter | MAM | 666 | 1 | 1 | 0 | 0 | 0 | 2 | 5.584 |
| Bruised Thematic Chapter | MAM | 666 | 1 | 1 | 0 | 0 | 0 | 3 | 11.382 |
| Gog Thematic Chapter | UHB | 3145 | 1 | 1 | 0 | 0 | 0 | 22 | 6.529 |
| Magog Thematic Chapter | UHB | 3145 | 1 | 1 | 0 | 0 | 0 | 3 | 0.502 |
| Beast Thematic Chapter | UHB | 2022 | 1 | 1 | 0 | 0 | 0 | 101 | 86.676 |
| Servant Thematic Chapter | UHB | 666 | 1 | 1 | 0 | 0 | 0 | 7 | 7.095 |
| Transgression Thematic Chapter | UHB | 666 | 1 | 1 | 0 | 0 | 0 | 12 | 3.767 |
| Iniquity Thematic Chapter | UHB | 666 | 1 | 1 | 0 | 0 | 0 | 52 | 24.396 |
| Wound Thematic Chapter | UHB | 666 | 1 | 0 | 1 | 1 | 0 | 0 | 0.081 |
| Lamb Thematic Chapter | UHB | 666 | 0 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Silent Thematic Chapter | UHB | 666 | 1 | 1 | 0 | 0 | 0 | 8 | 2.888 |
| Grave Thematic Chapter | UHB | 666 | 1 | 1 | 0 | 0 | 0 | 2 | 5.657 |
| Bruised Thematic Chapter | UHB | 666 | 1 | 1 | 0 | 0 | 0 | 3 | 11.333 |
| Servant Thematic Chapter | LXX | 1434 | 1 | 1 | 0 | 0 | 0 | 14 | 8.305 |
| Transgression Thematic Chapter | LXX | 1434 | 1 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Iniquity Thematic Chapter | LXX | 1434 | 1 | 0 | 1 | 1 | 0 | 0 | 0.088 |
| Wound Thematic Chapter | LXX | 1434 | 1 | 0 | 0 | 0 | 0 | 0 | 0.000 |
| Lamb Thematic Chapter | LXX | 1434 | 1 | 1 | 0 | 0 | 0 | 1 | 0.496 |
| Silent Thematic Chapter | LXX | 1434 | 1 | 0 | 1 | 1 | 0 | 0 | 0.013 |
| Grave Thematic Chapter | LXX | 1434 | 1 | 0 | 1 | 1 | 0 | 0 | 0.105 |
| Bruised Thematic Chapter | LXX | 1434 | 1 | 0 | 0 | 0 | 0 | 0 | 0.000 |

## Notable Absence / Low-Density Rows

Rows are sorted by gap class first, then by how frequently the term appears centered elsewhere in the same corpus.

| Passage | Corpus | Term | Gap Class | Hits Elsewhere | Hits In Passage | Uniform Expected | Uniform Zero P | Uniform Zero Q | Sample Center Refs |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Grave Thematic Chapter | LXX | `ταφοσ` (taphos; English: Grave) | absent_in_passage_common_elsewhere | 205 | 0 | 0.105 | 0.900059 | 0.987241 |  |
| Iniquity Thematic Chapter | LXX | `ανομια` (anomia; English: Iniquity) | absent_in_passage_common_elsewhere | 171 | 0 | 0.088 | 0.915915 | 0.987241 |  |
| Wound Thematic Chapter | EBIBLE_WLC | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 146 | 0 | 0.081 | 0.921981 | 0.987241 |  |
| Wound Thematic Chapter | MT_WLC | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 146 | 0 | 0.081 | 0.921981 | 0.987241 |  |
| Wound Thematic Chapter | UHB | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 146 | 0 | 0.081 | 0.921893 | 0.987241 |  |
| Wound Thematic Chapter | UXLC | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 146 | 0 | 0.081 | 0.921981 | 0.987241 |  |
| Wound Thematic Chapter | MAM | `חבורה` (chabburah; English: Wound) | absent_in_passage_common_elsewhere | 140 | 0 | 0.078 | 0.925360 | 0.987241 |  |
| Silent Thematic Chapter | LXX | `σιωπαω` (siopao; English: Silent) | absent_in_passage_common_elsewhere | 25 | 0 | 0.013 | 0.987241 | 0.987241 |  |

## Output Files

- Detail CSV: `reports/thematic_chapter_absence/term_gap_detail.csv`
- Passage summary CSV: `reports/thematic_chapter_absence/passage_summary.csv`
- Manifest: `reports/thematic_chapter_absence/manifest.json`

## Cautions

- This report does not treat absence as a negative proof. It records silence and lower-density rows so they can be reviewed alongside positive centered hits.
- `expected_in_passage_uniform` is a descriptive baseline only; it is not a formal p-value.
- `uniform_zero_probability` is the simple Poisson `exp(-expected)` probability of zero hits under that uniform baseline; it is a triage aid, not a formal independence test.
- `uniform_zero_bh_q` applies Benjamini-Hochberg correction to that simple zero-hit triage probability over absent/low-density detail rows.
- Short surface terms can be skipped by the minimum term length rule; skipped rows remain in the detail CSV for auditability.
- Passage ranges are resolved independently per source; versification and source differences can change passage letter counts even when the declared start/end refs are the same.
