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
- queries_tested: 575
- min_skip: 2
- max_skip: 250
- direction: both
- jobs: 0
- bridge_rows: 350
- terms_with_bridge_rows: 81
- apocrypha_books_touched: 2
- bridge_type:apocrypha_to_canonical: 178
- bridge_type:canonical_to_apocrypha: 172

## Top Bridge Rows

| Rank | Type | Term | Skip | Start | Center | End | Apocrypha books | Class path |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | `apocrypha_to_canonical` | `heth` | 3 | 2ES 16:78 | 2ES 16:78 | MAT 1:1 | 2ES | `AAAC` |
| 2 | `canonical_to_apocrypha` | `otho` | 11 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 3 | `canonical_to_apocrypha` | `teeth` | 17 | MAL 4:6 | TOB 1:1 | TOB 1:1 | TOB | `CCAAA` |
| 4 | `canonical_to_apocrypha` | `heth` | 22 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 5 | `canonical_to_apocrypha` | `seba` | 22 | MAL 4:6 | TOB 1:1 | TOB 1:1 | TOB | `CCAA` |
| 6 | `apocrypha_to_canonical` | `nisan` | -24 | TOB 1:1 | MAL 4:6 | MAL 4:6 | TOB | `AACCC` |
| 7 | `canonical_to_apocrypha` | `trees` | 27 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCAA` |
| 8 | `canonical_to_apocrypha` | `nato` | 33 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 9 | `apocrypha_to_canonical` | `noah` | -33 | TOB 1:1 | MAL 4:6 | MAL 4:6 | TOB | `AACC` |
| 10 | `apocrypha_to_canonical` | `isis` | -34 | TOB 1:1 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 11 | `canonical_to_apocrypha` | `hand` | 40 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 12 | `canonical_to_apocrypha` | `rome` | -45 | MAT 1:1 | 2ES 16:78 | 2ES 16:77 | 2ES | `CAAA` |
| 13 | `canonical_to_apocrypha` | `nato` | 54 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 14 | `apocrypha_to_canonical` | `iran` | 55 | 2ES 16:77 | 2ES 16:77 | MAT 1:1 | 2ES | `AAAC` |
| 15 | `apocrypha_to_canonical` | `edom` | 55 | 2ES 16:77 | 2ES 16:78 | MAT 1:1 | 2ES | `AACC` |
| 16 | `apocrypha_to_canonical` | `noah` | 56 | 2ES 16:78 | MAT 1:1 | MAT 1:2 | 2ES | `ACCC` |
| 17 | `canonical_to_apocrypha` | `heth` | 57 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 18 | `apocrypha_to_canonical` | `life` | -58 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 19 | `apocrypha_to_canonical` | `house` | 60 | 2ES 16:78 | MAT 1:2 | MAT 1:4 | 2ES | `ACCCC` |
| 20 | `canonical_to_apocrypha` | `aids` | 63 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 21 | `canonical_to_apocrypha` | `heth` | 65 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAA` |
| 22 | `canonical_to_apocrypha` | `heth` | 67 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCAA` |
| 23 | `apocrypha_to_canonical` | `star` | 68 | 2ES 16:78 | MAT 1:2 | MAT 1:3 | 2ES | `ACCC` |
| 24 | `canonical_to_apocrypha` | `nato` | -68 | MAT 1:3 | MAT 1:2 | 2ES 16:78 | 2ES | `CCCA` |
| 25 | `canonical_to_apocrypha` | `amen` | 70 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAA` |
| 26 | `canonical_to_apocrypha` | `nero` | 73 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 27 | `apocrypha_to_canonical` | `nero` | -73 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `ACCC` |
| 28 | `canonical_to_apocrypha` | `seal` | 75 | MAL 4:5 | MAL 4:6 | TOB 1:1 | TOB | `CCCA` |
| 29 | `apocrypha_to_canonical` | `otho` | -75 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `ACCC` |
| 30 | `canonical_to_apocrypha` | `eber` | -75 | MAT 1:3 | MAT 1:1 | 2ES 16:77 | 2ES | `CCAA` |
| 31 | `apocrypha_to_canonical` | `sign` | 76 | 2ES 16:78 | MAT 1:2 | MAT 1:3 | 2ES | `ACCC` |
| 32 | `canonical_to_apocrypha` | `seal` | 77 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 33 | `apocrypha_to_canonical` | `eber` | 77 | 2ES 16:77 | 2ES 16:77 | MAT 1:1 | 2ES | `AAAC` |
| 34 | `apocrypha_to_canonical` | `fire` | -79 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `ACCC` |
| 35 | `apocrypha_to_canonical` | `torah` | -81 | TOB 1:1 | MAL 4:6 | MAL 4:4 | TOB | `AACCC` |
| 36 | `canonical_to_apocrypha` | `sidon` | -83 | MAT 1:1 | 2ES 16:77 | 2ES 16:76 | 2ES | `CAAAA` |
| 37 | `canonical_to_apocrypha` | `star` | -84 | MAT 1:1 | 2ES 16:77 | 2ES 16:77 | 2ES | `CAAA` |
| 38 | `apocrypha_to_canonical` | `torah` | -85 | TOB 1:1 | MAL 4:5 | MAL 4:3 | TOB | `ACCCC` |
| 39 | `apocrypha_to_canonical` | `noah` | -85 | TOB 1:1 | MAL 4:6 | MAL 4:5 | TOB | `AACC` |
| 40 | `canonical_to_apocrypha` | `satan` | -85 | MAT 1:3 | MAT 1:1 | 2ES 16:77 | 2ES | `CCCAA` |
| 41 | `apocrypha_to_canonical` | `isaac` | 86 | 2ES 16:78 | MAT 1:2 | MAT 1:5 | 2ES | `ACCCC` |
| 42 | `canonical_to_apocrypha` | `faith` | 87 | MAL 4:5 | TOB 1:1 | TOB 1:2 | TOB | `CCAAA` |
| 43 | `apocrypha_to_canonical` | `cush` | 88 | 2ES 16:77 | 2ES 16:78 | MAT 1:2 | 2ES | `AACC` |
| 44 | `canonical_to_apocrypha` | `satan` | 89 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAAA` |
| 45 | `canonical_to_apocrypha` | `heth` | 89 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 46 | `apocrypha_to_canonical` | `otho` | -90 | TOB 1:1 | MAL 4:6 | MAL 4:4 | TOB | `ACCC` |
| 47 | `canonical_to_apocrypha` | `mash` | -90 | MAT 1:4 | MAT 1:2 | 2ES 16:77 | 2ES | `CCCA` |
| 48 | `canonical_to_apocrypha` | `heth` | 91 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CAAA` |
| 49 | `apocrypha_to_canonical` | `aids` | -92 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 50 | `canonical_to_apocrypha` | `sadat` | -92 | MAT 1:6 | MAT 1:3 | 2ES 16:78 | 2ES | `CCCCA` |
| ... | ... | ... | ... | ... | ... | ... | ... | 300 more rows in CSV |

## Read

- These are bridge candidates, not significance claims.
- The current KJVA stream is tested in its declared
  source order, so this first pass mostly tests the first
  canonical/apocrypha boundary rather than a manuscript-specific
  insertion model.
- Removing the apocrypha/deuterocanon letters would break the expanded-stream ELS path.
- The next control should insert comparable non-Bible blocks at the same boundary positions.
- Letter-level provenance is in the CSV `letter_path` column.
