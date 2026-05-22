# KJVA Prospective Apocrypha Bridge Candidates

Status: bounded bridge-candidate scan. This is not a claim report.

A bridge candidate is an ELS path whose matched letters include at least
one canonical-book letter and at least one deuterocanon/apocrypha-book
letter in the declared expanded stream.

## Reproduce

```bash
python3 -m scripts.analyze_apocrypha_bridge_candidates --corpus-label KJVA Prospective --config configs/example_ebible_engkjv_apocrypha.toml --terms terms/kjv_apocrypha_bridge_prospective_terms.csv --min-skip 2 --max-skip 250 --direction both --min-term-length 4 --jobs 0 --out reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv --summary-out reports/kjv_apocrypha_bridge_prospective/bridge_summary.csv --markdown-out docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md --manifest-out reports/kjv_apocrypha_bridge_prospective/bridge_candidates.manifest.json
```

## Summary

- corpus: KJVA Prospective
- corpus_letters: 3816315
- queries_tested: 7
- min_skip: 2
- max_skip: 250
- direction: both
- jobs: 0
- bridge_rows: 1
- terms_with_bridge_rows: 1
- apocrypha_books_touched: 1
- bridge_type:canonical_to_apocrypha: 1

## Top Bridge Rows

| Rank | Type | Term | Skip | Start | Center | End | Apocrypha books | Class path |
| ---: | --- | --- | ---: | --- | --- | --- | --- | --- |
| 1 | `canonical_to_apocrypha` | `tobit` | -215 | MAT 1:8 | MAT 1:2 | 2ES 16:75 | 2ES | `CCCAA` |

## Read

- These are bridge candidates, not significance claims.
- The current KJVA Prospective stream is tested in its declared
  source order, so this first pass mostly tests the first
  canonical/apocrypha boundary rather than a manuscript-specific
  insertion model.
- Removing the apocrypha/deuterocanon letters would break the expanded-stream ELS path.
- The next control should insert comparable non-Bible blocks at the same boundary positions.
- Letter-level provenance is in the CSV `letter_path` column.
