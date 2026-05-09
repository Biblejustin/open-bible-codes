# LXX Apocrypha Bridge Candidates

Status: bounded bridge-candidate scan. This is not a claim report.

A bridge candidate is an ELS path whose matched letters include at least
one canonical-book letter and at least one deuterocanon/apocrypha-book
letter in the declared expanded stream.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_candidates --corpus-label LXX --config configs/example_ebible_grclxx.toml --terms terms/theological_terms.csv --terms terms/prophetic_terms.csv --terms terms/greek_nt_claim_terms.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/apocrypha_bridge_candidates/bridge_candidates.csv --summary-out reports/apocrypha_bridge_candidates/summary.csv --markdown-out docs/APOCRYPHA_BRIDGE_CANDIDATES.md --manifest-out reports/apocrypha_bridge_candidates/manifest.json
```

## Summary

- corpus: LXX
- corpus_letters: 2791859
- queries_tested: 292
- min_skip: 2
- max_skip: 250
- direction: both
- jobs: 0
- bridge_rows: 62
- terms_with_bridge_rows: 21
- apocrypha_books_touched: 1
- bridge_type:apocrypha_to_canonical: 27
- bridge_type:canonical_to_apocrypha: 35

## Top Bridge Rows

| Rank | Type | Term | Skip | Start | Center | End | Apocrypha books | Class path |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | `canonical_to_apocrypha` | `μαρια` | 29 | MAL 4:6 | MAL 4:6 | TOB 1:1 | TOB | `CCCAA` |
| 2 | `canonical_to_apocrypha` | `ναοσ` | 40 | MAL 4:6 | TOB 1:1 | TOB 1:1 | TOB | `CCAA` |
| 3 | `canonical_to_apocrypha` | `αδησ` | 43 | MAL 4:6 | TOB 1:1 | TOB 1:1 | TOB | `CCAA` |
| 4 | `canonical_to_apocrypha` | `υιοσ` | 71 | MAL 4:6 | TOB 1:1 | TOB 1:2 | TOB | `CCAA` |
| 5 | `apocrypha_to_canonical` | `λεων` | -83 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AAAC` |
| 6 | `apocrypha_to_canonical` | `ελαμ` | -85 | TOB 1:2 | TOB 1:1 | MAL 4:6 | TOB | `AACC` |
| 7 | `apocrypha_to_canonical` | `αιμα` | -99 | TOB 1:2 | TOB 1:2 | MAL 4:6 | TOB | `AAAC` |
| 8 | `apocrypha_to_canonical` | `υιοσ` | -103 | TOB 1:2 | MAL 4:6 | MAL 4:5 | TOB | `AACC` |
| 9 | `canonical_to_apocrypha` | `ελαμ` | 120 | MAL 4:6 | TOB 1:2 | TOB 1:3 | TOB | `CAAA` |
| 10 | `canonical_to_apocrypha` | `ναοσ` | 130 | MAL 4:2 | MAL 4:5 | TOB 1:1 | TOB | `CCCA` |
| 11 | `canonical_to_apocrypha` | `ναοσ` | 131 | MAL 4:6 | TOB 1:2 | TOB 1:3 | TOB | `CAAA` |
| 12 | `apocrypha_to_canonical` | `οφισ` | -136 | TOB 1:2 | TOB 1:1 | MAL 4:5 | TOB | `AACC` |
| 13 | `apocrypha_to_canonical` | `ελαμ` | -136 | TOB 1:3 | TOB 1:2 | MAL 4:6 | TOB | `AAAC` |
| 14 | `canonical_to_apocrypha` | `ναοσ` | 138 | MAL 4:3 | MAL 4:5 | TOB 1:1 | TOB | `CCCA` |
| 15 | `canonical_to_apocrypha` | `δοξα` | 140 | MAL 4:2 | MAL 4:5 | TOB 1:1 | TOB | `CCCA` |
| 16 | `canonical_to_apocrypha` | `ναοσ` | 140 | MAL 4:6 | TOB 1:2 | TOB 1:3 | TOB | `CAAA` |
| 17 | `canonical_to_apocrypha` | `ελκη` | 147 | MAL 4:6 | TOB 1:2 | TOB 1:4 | TOB | `CAAA` |
| 18 | `apocrypha_to_canonical` | `σιων` | -154 | TOB 1:2 | MAL 4:6 | MAL 4:4 | TOB | `AACC` |
| 19 | `apocrypha_to_canonical` | `οθων` | -156 | TOB 1:3 | TOB 1:2 | MAL 4:5 | TOB | `AAAC` |
| 20 | `canonical_to_apocrypha` | `ναοσ` | 161 | MAL 4:4 | TOB 1:1 | TOB 1:3 | TOB | `CCAA` |
| 21 | `canonical_to_apocrypha` | `υιοσ` | 165 | MAL 4:3 | MAL 4:6 | TOB 1:2 | TOB | `CCAA` |
| 22 | `apocrypha_to_canonical` | `αιμα` | -168 | TOB 1:2 | MAL 4:5 | MAL 4:2 | TOB | `ACCC` |
| 23 | `canonical_to_apocrypha` | `οργη` | 175 | MAL 4:3 | MAL 4:6 | TOB 1:2 | TOB | `CCAA` |
| 24 | `canonical_to_apocrypha` | `ακρισ` | 176 | MAL 4:1 | MAL 4:4 | TOB 1:2 | TOB | `CCCCA` |
| 25 | `apocrypha_to_canonical` | `σιων` | -176 | TOB 1:4 | TOB 1:2 | MAL 4:6 | TOB | `AAAC` |
| 26 | `canonical_to_apocrypha` | `αδησ` | 177 | MAL 4:4 | MAL 4:6 | TOB 1:2 | TOB | `CCAA` |
| 27 | `canonical_to_apocrypha` | `θεοσ` | 184 | MAL 4:6 | TOB 1:2 | TOB 1:4 | TOB | `CAAA` |
| 28 | `canonical_to_apocrypha` | `σιων` | 187 | MAL 4:2 | MAL 4:5 | TOB 1:2 | TOB | `CCCA` |
| 29 | `canonical_to_apocrypha` | `αιμα` | 190 | MAL 4:2 | MAL 4:5 | TOB 1:2 | TOB | `CCCA` |
| 30 | `canonical_to_apocrypha` | `αμην` | 191 | MAL 4:3 | MAL 4:6 | TOB 1:3 | TOB | `CCAA` |
| 31 | `canonical_to_apocrypha` | `αδαμ` | 195 | MAL 4:4 | TOB 1:1 | TOB 1:4 | TOB | `CCAA` |
| 32 | `apocrypha_to_canonical` | `υιοσ` | -195 | TOB 1:4 | TOB 1:2 | MAL 4:5 | TOB | `AAAC` |
| 33 | `apocrypha_to_canonical` | `λεων` | -195 | TOB 1:4 | TOB 1:2 | MAL 4:6 | TOB | `AAAC` |
| 34 | `apocrypha_to_canonical` | `αδαμ` | -195 | TOB 1:4 | TOB 1:2 | MAL 4:6 | TOB | `AAAC` |
| 35 | `canonical_to_apocrypha` | `ελκη` | 196 | MAL 4:2 | MAL 4:5 | TOB 1:2 | TOB | `CCCA` |
| 36 | `apocrypha_to_canonical` | `σιων` | -198 | TOB 1:2 | MAL 4:5 | MAL 4:2 | TOB | `ACCC` |
| 37 | `canonical_to_apocrypha` | `υιοσ` | 203 | MAL 4:6 | TOB 1:2 | TOB 1:4 | TOB | `CAAA` |
| 38 | `apocrypha_to_canonical` | `θεοσ` | -204 | TOB 1:3 | TOB 1:1 | MAL 4:3 | TOB | `AACC` |
| 39 | `apocrypha_to_canonical` | `σιων` | -204 | TOB 1:3 | TOB 1:1 | MAL 4:4 | TOB | `AACC` |
| 40 | `apocrypha_to_canonical` | `ελαμ` | -209 | TOB 1:3 | MAL 4:6 | MAL 4:3 | TOB | `AACC` |
| 41 | `apocrypha_to_canonical` | `αιμα` | -210 | TOB 1:4 | TOB 1:2 | MAL 4:5 | TOB | `AAAC` |
| 42 | `canonical_to_apocrypha` | `υιοσ` | 212 | MAL 4:5 | TOB 1:2 | TOB 1:4 | TOB | `CAAA` |
| 43 | `apocrypha_to_canonical` | `υιοσ` | -213 | TOB 1:3 | MAL 4:6 | MAL 4:3 | TOB | `AACC` |
| 44 | `canonical_to_apocrypha` | `ελκη` | 215 | MAL 4:4 | TOB 1:1 | TOB 1:3 | TOB | `CCAA` |
| 45 | `canonical_to_apocrypha` | `αμην` | 217 | MAL 4:2 | MAL 4:5 | TOB 1:2 | TOB | `CCCA` |
| 46 | `apocrypha_to_canonical` | `σιων` | -218 | TOB 1:4 | TOB 1:2 | MAL 4:4 | TOB | `AAAC` |
| 47 | `apocrypha_to_canonical` | `ρωμη` | -221 | TOB 1:3 | TOB 1:1 | MAL 4:3 | TOB | `AACC` |
| 48 | `apocrypha_to_canonical` | `βασαν` | -222 | TOB 1:5 | TOB 1:2 | MAL 4:4 | TOB | `AAACC` |
| 49 | `canonical_to_apocrypha` | `θεοσ` | 223 | MAL 4:1 | MAL 4:4 | TOB 1:2 | TOB | `CCCA` |
| 50 | `apocrypha_to_canonical` | `αιμα` | -223 | TOB 1:4 | TOB 1:1 | MAL 4:4 | TOB | `AACC` |
| ... | ... | ... | ... | ... | ... | ... | ... | 12 more rows in CSV |

## Read

- These are bridge candidates, not significance claims.
- The current LXX stream is tested in its declared
  source order, so this first pass mostly tests the first
  canonical/apocrypha boundary rather than a manuscript-specific
  insertion model.
- Removing the apocrypha/deuterocanon letters would break the expanded-stream ELS path.
- The next control should insert comparable non-Bible blocks at the same boundary positions.
- Letter-level provenance is in the CSV `letter_path` column.
