# Gans Communities Source Audit

Status: source-shape audit only. This is not an ELS result, not a
compactness calculation, and not a claim-ready replication.

## Source

- Data PDF: `https://www.torah-code.org/papers/communities_data.pdf`
- Local ignored file: `reports/wrr_1994/gans_communities_data.pdf`
- SHA-256: `ac0b221064e144ca9a70d616064bcd58f7d8e68cd2fe6bedb202dd81991feb86`
- Bytes: 349586

## Parsed Shape

| Item | Count |
| --- | ---: |
| pages from extracted text | 8 |
| data records | 66 |
| record index minimum | 1 |
| record index maximum | 66 |
| records with trace word 1 | 66 |
| records with trace word 2 | 66 |
| explicit community rows | 128 |
| reused community rows | 82 |
| total community rows | 210 |
| records with no personality marker | 2 |
| records with malformed trace line | 0 |

## Protocol Anchors

Found anchors: 6 of 6.

| Anchor | Status | Diagnostic |
| --- | --- | --- |
| `wrr_lists_1_and_2_names` | found | personality names/appellations source rule found |
| `community_prefixes_lhq_tlhq` | found | community prefix rule found |
| `length_window_5_8` | found | length filter rule found |
| `rabbi_appellation_ybr_exclusion` | found | Rabbi-prefix exclusion rule found |
| `additional_qq_nonconforming_experiment` | found | separate qq experiment caveat found |
| `trace_words_defined` | found | trace-word definitions found |

## Use Boundary

This audit makes the source usable as a future locked-data intake target.
It does not yet normalize Hebrew spellings, add community prefixes, apply
the length/Rabbi-prefix filters, compute ELS hits, or test compactness.

Next result-bearing step, if chosen later: write a separate preregistered
communities protocol that freezes source rows, normalization, filters,
Genesis text, skip caps, compactness metric, and controls before running
any ELS search.
