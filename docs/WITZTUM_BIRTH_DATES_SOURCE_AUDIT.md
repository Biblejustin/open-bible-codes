# Witztum Birth Dates Source Audit

Status: source-shape audit only. This is not an ELS result, not a
statistical test, and not a claim-ready replication.

## Sources

- Paper PDF: `https://www.torah-code.org/papers/witztum.pdf`
- Data PDF: `https://www.torah-code.org/papers/personaldata.pdf`
- Paper SHA-256: `e1c4ee142c5138af53cdcbeded23a6ae724000b82c5f015b07f1e212c05ec56e`
- Data SHA-256: `20296eaa82a60065e5f01032833da76eaf004c0f11801617e6646bb33f83dcfe`

## Parsed Shape

| Item | Count |
| --- | ---: |
| paper PDF pages from extracted text | 4 |
| data PDF pages from extracted text | 4 |
| sample tables | 2 |
| total table rows | 28 |
| S1 rows | 14 |
| S2 rows | 14 |
| S1 name variants | 18 |
| S2 name variants | 15 |
| S1 date forms | 51 |
| S2 date forms | 51 |
| S1 starred date forms | 4 |
| S2 starred date forms | 4 |
| S1 pair forms after star filter | 59 |
| S2 pair forms after star filter | 50 |

## Protocol Anchors

Found anchors: 9 of 9.

| Source | Anchor | Status | Diagnostic |
| --- | --- | --- | --- |
| paper | `pattern_type_b_definition` | found | type-B pattern framing found |
| paper | `one_million_permutation_rank` | found | one-million rank procedure found |
| paper | `sample_s1_s2_results` | found | published S1/S2 result numbers found |
| data | `list_l_definition` | found | List L size rule found |
| data | `sample_s1_definition` | found | Sample S1 definition found |
| data | `sample_s2_definition` | found | Sample S2 definition found |
| data | `date_three_fixed_forms` | found | date-form rule found |
| data | `length_range_5_8` | found | length range rule found |
| data | `asterisk_short_date_exclusion` | found | asterisk exclusion rule found |

## Use Boundary

This audit only verifies that the paper and data PDFs expose stable source
shape for the S1/S2 birth-date samples. It does not normalize terms into
repo search rows, compute ELS/SL proximity, rank permutations, or evaluate
the published p-levels.

Next result-bearing step, if chosen later: write a separate preregistered
birth-date protocol that freezes source rows, name/date normalization, text
source, skip caps, proximity metric, permutation schedule, and controls
before any ELS search.
