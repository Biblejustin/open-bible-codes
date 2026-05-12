# Direction Asymmetry

Status: post-search review aid, not claim promotion.

This report summarizes whether a term/corpus group appears only in the
forward direction, only in the backward direction, or in both directions.
It depends on the already-built match-strata index and does not perform
a new ELS search.

## Settings

- Strata input: `reports/match_strata_index/occurrence_strata.csv`
- Input rows: `923`
- Term/corpus groups: `153`

## Overall Direction Counts

| Bucket | Term/corpus groups |
| --- | ---: |
| `forward_only` | 49 |
| `backward_only` | 51 |
| `bidirectional_present` | 53 |
| `no_direction_data` | 0 |

## Source / Corpus Summary

| Source family | Corpus class | Corpus | Bucket | Term groups | Hit rows | Forward hits | Backward hits | Share |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `all_codes_followup` | `bible` | `` | `forward_only` | 23 | 29 | 29 | 0 | 0.425926 |
| `all_codes_followup` | `bible` | `` | `backward_only` | 21 | 25 | 0 | 25 | 0.388889 |
| `all_codes_followup` | `bible` | `` | `bidirectional_present` | 10 | 20 | 10 | 10 | 0.185185 |
| `all_codes_followup` | `bible` | `` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `forward_only` | 2 | 2 | 2 | 0 | 0.181818 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `backward_only` | 3 | 3 | 0 | 3 | 0.272727 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `bidirectional_present` | 6 | 24 | 10 | 14 | 0.545455 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `bidirectional_present` | 1 | 1 | 2 | 2 | 1.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `bidirectional_present` | 1 | 1 | 2 | 2 | 1.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `bidirectional_present` | 1 | 1 | 2 | 2 | 1.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `bidirectional_present` | 1 | 1 | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `forward_only` | 23 | 34 | 34 | 0 | 0.319444 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `backward_only` | 25 | 47 | 0 | 47 | 0.347222 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `bidirectional_present` | 24 | 122 | 58 | 64 | 0.333333 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `bidirectional_present` | 1 | 4 | 1 | 3 | 1.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `bidirectional_present` | 1 | 57 | 27 | 30 | 1.000000 |
| `original_language_findings` | `bible` | `LXX` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `backward_only` | 1 | 1 | 0 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `bidirectional_present` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `bidirectional_present` | 1 | 14 | 8 | 6 | 1.000000 |
| `original_language_findings` | `bible` | `UHB` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `bidirectional_present` | 1 | 4 | 1 | 3 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `bidirectional_present` | 1 | 377 | 203 | 174 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `bidirectional_present` | 1 | 57 | 27 | 30 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `backward_only` | 1 | 1 | 0 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `bidirectional_present` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `bidirectional_present` | 1 | 14 | 8 | 6 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `forward_only` | 1 | 1 | 1 | 0 | 1.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `bidirectional_present` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `ENG_PG_SHAKESPEARE` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `forward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `backward_only` | 0 | 0 | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `bidirectional_present` | 2 | 83 | 45 | 38 | 1.000000 |
| `strong_full_span_exact_center` | `control` | `HEB_PBY_BIALIK` | `no_direction_data` | 0 | 0 | 0 | 0 | 0.000000 |

## Read

- Direction asymmetry is counted per term/corpus group, not per isolated hit.
- `forward_only` and `backward_only` are review filters. They are not
  findings without matched controls and a locked comparison rule.
- The term-level CSV preserves hit-row counts and grouped forward/backward
  totals for later filtering.
