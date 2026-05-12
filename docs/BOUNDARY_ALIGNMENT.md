# Boundary Alignment

Status: post-search review aid, not claim promotion.

This report summarizes whether ELS path starts and ends align with
verse, chapter, or book boundaries. It depends on the already-built
match-strata index and does not perform a new ELS search.

## Settings

- Strata input: `reports/match_strata_index/occurrence_strata.csv`
- Input rows: `923`

## Overall Boundary Counts

| Bucket | Rows |
| --- | ---: |
| `boundary_start_verse` | 22 |
| `boundary_start_chapter` | 1 |
| `boundary_start_book` | 1 |
| `boundary_end_verse` | 13 |
| `boundary_end_chapter` | 2 |
| `boundary_end_book` | 2 |
| `boundary_both_endpoints` | 1 |
| `no_boundary_data` | 889 |

## Source / Corpus Summary

| Source family | Corpus class | Corpus | Bucket | Rows | Distinct terms | Share |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `all_codes_followup` | `bible` | `` | `boundary_start_verse` | 1 | 1 | 0.013514 |
| `all_codes_followup` | `bible` | `` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `boundary_end_verse` | 4 | 3 | 0.054054 |
| `all_codes_followup` | `bible` | `` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `no_boundary_data` | 69 | 52 | 0.932432 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_end_verse` | 1 | 1 | 0.034483 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `no_boundary_data` | 28 | 11 | 0.965517 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `no_boundary_data` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `no_boundary_data` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `no_boundary_data` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `no_boundary_data` | 1 | 1 | 1.000000 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_start_verse` | 5 | 5 | 0.024631 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_start_chapter` | 1 | 1 | 0.004926 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_start_book` | 1 | 1 | 0.004926 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_end_verse` | 5 | 5 | 0.024631 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_end_chapter` | 2 | 2 | 0.009852 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_end_book` | 2 | 2 | 0.009852 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `no_boundary_data` | 193 | 70 | 0.950739 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `no_boundary_data` | 4 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `no_boundary_data` | 57 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_start_verse` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_start_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_start_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_end_verse` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_end_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_end_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `boundary_both_endpoints` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `no_boundary_data` | 1 | 1 | 1.000000 |
| ... | ... | ... | ... | ... | ... | 64 more rows in CSV |

## Read

- Boundary alignment is a review filter for path placement, not a
  finding by itself.
- `no_boundary_data` includes ordinary interior paths and rows whose
  corpus/offsets could not be mapped to a loaded boundary index.
- Claim-grade use needs matched controls with an equivalent structural
  boundary definition.
