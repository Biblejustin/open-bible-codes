# KJVA Apocrypha Bridge Candidates

Status: bounded bridge-candidate scan. This is not a claim report.

A bridge candidate is an ELS path whose matched letters include at least
one canonical-book letter and at least one deuterocanon/apocrypha-book
letter in the declared expanded stream.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_candidates --corpus-label KJVA --config configs/example_ebible_engkjv_apocrypha.toml --terms terms/english_search_terms.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv --summary-out reports/kjv_apocrypha_bridge_candidates/summary.csv --markdown-out docs/KJV_APOCRYPHA_BRIDGE_CANDIDATES.md --manifest-out reports/kjv_apocrypha_bridge_candidates/manifest.json
```

## Summary

- corpus: KJVA
- corpus_letters: 3816315
- queries_tested: 968
- min_skip: 2
- max_skip: 250
- direction: both
- jobs: 0
- bridge_rows: 535
- terms_with_bridge_rows: 114
- apocrypha_books_touched: 2
- bridge_type:apocrypha_to_canonical: 270
- bridge_type:canonical_to_apocrypha: 265

## Top Bridge Rows

| Rank | Type | Term | Skip | Start | Center | End | Apocrypha books | Class path |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | `apocrypha_to_canonical` | `heth` | 3 | 2ES 16:78 | 2ES 16:78 | MAT 1:1 | 2ES | `AAAC` |
| 2 | `canonical_to_apocrypha` | `otho` | 11 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 3 | `apocrypha_to_canonical` | `eden` | 12 | 2ES 16:78 | 2ES 16:78 | MAT 1:1 | 2ES | `AACC` |
| 4 | `apocrypha_to_canonical` | `tree` | -12 | TOB 1:1 | MAL 4:6 | MAL 4:6 | TOB | `ACCC` |
| 5 | `apocrypha_to_canonical` | `tree` | -15 | TOB 1:1 | TOB 1:1 | MAL 4:6 | TOB | `AACC` |
| 6 | `canonical_to_apocrypha` | `teeth` | 17 | MAL 4:6 | TOB 1:1 | TOB 1:1 | TOB | `CCAAA` |
| 7 | `canonical_to_apocrypha` | `heth` | 22 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 8 | `canonical_to_apocrypha` | `seba` | 22 | MAL 4:6 | TOB 1:1 | TOB 1:1 | TOB | `CCAA` |
| 9 | `apocrypha_to_canonical` | `thin` | 24 | 2ES 16:78 | 2ES 16:78 | MAT 1:1 | 2ES | `AAAC` |
| 10 | `apocrypha_to_canonical` | `nisan` | -24 | TOB 1:1 | MAL 4:6 | MAL 4:6 | TOB | `AACCC` |
| 11 | `canonical_to_apocrypha` | `tree` | 27 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 12 | `canonical_to_apocrypha` | `trees` | 27 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCAA` |
| 13 | `canonical_to_apocrypha` | `nato` | 33 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 14 | `apocrypha_to_canonical` | `noah` | -33 | TOB 1:1 | MAL 4:6 | MAL 4:6 | TOB | `AACC` |
| 15 | `apocrypha_to_canonical` | `isis` | -34 | TOB 1:1 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 16 | `apocrypha_to_canonical` | `tree` | 36 | 2ES 16:77 | 2ES 16:78 | MAT 1:1 | 2ES | `AAAC` |
| 17 | `canonical_to_apocrypha` | `hand` | 40 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 18 | `apocrypha_to_canonical` | `tree` | 42 | 2ES 16:77 | 2ES 16:78 | MAT 1:1 | 2ES | `AAAC` |
| 19 | `canonical_to_apocrypha` | `annas` | -45 | MAT 1:1 | 2ES 16:78 | 2ES 16:77 | 2ES | `CCAAA` |
| 20 | `canonical_to_apocrypha` | `rome` | -45 | MAT 1:1 | 2ES 16:78 | 2ES 16:77 | 2ES | `CAAA` |
| 21 | `apocrypha_to_canonical` | `soot` | -47 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 22 | `apocrypha_to_canonical` | `seed` | -53 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `ACCC` |
| 23 | `canonical_to_apocrypha` | `nato` | 54 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 24 | `canonical_to_apocrypha` | `seed` | 54 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 25 | `apocrypha_to_canonical` | `iran` | 55 | 2ES 16:77 | 2ES 16:77 | MAT 1:1 | 2ES | `AAAC` |
| 26 | `apocrypha_to_canonical` | `edom` | 55 | 2ES 16:77 | 2ES 16:78 | MAT 1:1 | 2ES | `AACC` |
| 27 | `apocrypha_to_canonical` | `noah` | 56 | 2ES 16:78 | MAT 1:1 | MAT 1:2 | 2ES | `ACCC` |
| 28 | `canonical_to_apocrypha` | `heth` | 57 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 29 | `apocrypha_to_canonical` | `life` | -58 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 30 | `canonical_to_apocrypha` | `joel` | -59 | MAT 1:2 | MAT 1:1 | 2ES 16:77 | 2ES | `CCAA` |
| 31 | `apocrypha_to_canonical` | `house` | 60 | 2ES 16:78 | MAT 1:2 | MAT 1:4 | 2ES | `ACCCC` |
| 32 | `canonical_to_apocrypha` | `aids` | 63 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 33 | `canonical_to_apocrypha` | `heth` | 65 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAA` |
| 34 | `apocrypha_to_canonical` | `tree` | -65 | TOB 1:1 | MAL 4:6 | MAL 4:6 | TOB | `AACC` |
| 35 | `apocrypha_to_canonical` | `rent` | 66 | 2ES 16:77 | 2ES 16:77 | MAT 1:1 | 2ES | `AAAC` |
| 36 | `canonical_to_apocrypha` | `heth` | 67 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCAA` |
| 37 | `canonical_to_apocrypha` | `seed` | 67 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 38 | `apocrypha_to_canonical` | `star` | 68 | 2ES 16:78 | MAT 1:2 | MAT 1:3 | 2ES | `ACCC` |
| 39 | `canonical_to_apocrypha` | `nato` | -68 | MAT 1:3 | MAT 1:2 | 2ES 16:78 | 2ES | `CCCA` |
| 40 | `canonical_to_apocrypha` | `amen` | 70 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAA` |
| 41 | `apocrypha_to_canonical` | `soot` | -70 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 42 | `canonical_to_apocrypha` | `nero` | 73 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 43 | `canonical_to_apocrypha` | `rent` | 73 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAA` |
| 44 | `apocrypha_to_canonical` | `nero` | -73 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `ACCC` |
| 45 | `apocrypha_to_canonical` | `seed` | -73 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 46 | `apocrypha_to_canonical` | `hits` | -73 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 47 | `canonical_to_apocrypha` | `iron` | 74 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 48 | `canonical_to_apocrypha` | `seal` | 75 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 49 | `apocrypha_to_canonical` | `otho` | -75 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `ACCC` |
| 50 | `canonical_to_apocrypha` | `eber` | -75 | MAT 1:3 | MAT 1:1 | 2ES 16:77 | 2ES | `CCAA` |
| ... | ... | ... | ... | ... | ... | ... | ... | 485 more rows in CSV |

## Read

- These are bridge candidates, not significance claims.
- The current KJVA stream is tested in its declared
  source order, so this first pass mostly tests the first
  canonical/apocrypha boundary rather than a manuscript-specific
  insertion model.
- Removing the apocrypha/deuterocanon letters would break the expanded-stream ELS path.
- The next control should insert comparable non-Bible blocks at the same boundary positions.
- Letter-level provenance is in the CSV `letter_path` column.
