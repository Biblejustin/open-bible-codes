# Chapter Position Bias

Status: post-search review aid, not claim promotion.

This report summarizes whether centered occurrence rows land in verses
that are first or last in their chapter or book. It depends on the
already-built match-strata index and does not perform a new ELS search.

## Settings

- Strata input: `reports/match_strata_index/occurrence_strata.csv`
- Input rows: `923`

## Overall Position Counts

| Bucket | Rows |
| --- | ---: |
| `center_verse_first_in_chapter` | 82 |
| `center_verse_last_in_chapter` | 64 |
| `center_verse_first_in_book` | 50 |
| `center_verse_last_in_book` | 42 |
| `interior_or_unmapped` | 777 |

## Source / Corpus Summary

| Source family | Corpus class | Corpus | Bucket | Rows | Distinct terms | Share |
| --- | --- | --- | --- | ---: | ---: | ---: |
| `all_codes_followup` | `bible` | `` | `center_verse_first_in_chapter` | 3 | 3 | 0.040541 |
| `all_codes_followup` | `bible` | `` | `center_verse_last_in_chapter` | 3 | 3 | 0.040541 |
| `all_codes_followup` | `bible` | `` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `all_codes_followup` | `bible` | `` | `interior_or_unmapped` | 68 | 51 | 0.918919 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `center_verse_first_in_chapter` | 6 | 6 | 0.206897 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `center_verse_last_in_chapter` | 4 | 4 | 0.137931 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `center_verse_first_in_book` | 6 | 6 | 0.206897 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `center_verse_last_in_book` | 4 | 4 | 0.137931 |
| `apocrypha_bridge_context` | `bible` | `LXX` | `interior_or_unmapped` | 19 | 9 | 0.655172 |
| `gog_source_review` | `bible` | `BYZ_NT` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `BYZ_NT` | `interior_or_unmapped` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `SBLGNT` | `interior_or_unmapped` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TCG_NT` | `interior_or_unmapped` | 1 | 1 | 1.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `gog_source_review` | `bible` | `TR_NT` | `interior_or_unmapped` | 1 | 1 | 1.000000 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `center_verse_first_in_chapter` | 36 | 21 | 0.177340 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `center_verse_last_in_chapter` | 35 | 21 | 0.172414 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `center_verse_first_in_book` | 36 | 21 | 0.177340 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `center_verse_last_in_book` | 35 | 21 | 0.172414 |
| `kjv_apocrypha_bridge_context` | `bible` | `KJVA` | `interior_or_unmapped` | 132 | 63 | 0.650246 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `center_verse_first_in_chapter` | 1 | 1 | 0.250000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `EBIBLE_WLC` | `interior_or_unmapped` | 3 | 1 | 0.750000 |
| `original_language_findings` | `bible` | `LXX` | `center_verse_first_in_chapter` | 4 | 1 | 0.070175 |
| `original_language_findings` | `bible` | `LXX` | `center_verse_last_in_chapter` | 3 | 1 | 0.052632 |
| `original_language_findings` | `bible` | `LXX` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `LXX` | `interior_or_unmapped` | 50 | 1 | 0.877193 |
| `original_language_findings` | `bible` | `TCG_NT` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `TCG_NT` | `interior_or_unmapped` | 1 | 1 | 1.000000 |
| `original_language_findings` | `bible` | `UHB` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `original_language_findings` | `bible` | `UHB` | `interior_or_unmapped` | 14 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `center_verse_first_in_chapter` | 1 | 1 | 0.250000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `EBIBLE_WLC` | `interior_or_unmapped` | 3 | 1 | 0.750000 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `center_verse_first_in_chapter` | 27 | 1 | 0.071618 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `center_verse_last_in_chapter` | 16 | 1 | 0.042440 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `center_verse_first_in_book` | 8 | 1 | 0.021220 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `center_verse_last_in_book` | 3 | 1 | 0.007958 |
| `strong_full_span_exact_center` | `bible` | `KJV` | `interior_or_unmapped` | 334 | 1 | 0.885942 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `center_verse_first_in_chapter` | 4 | 1 | 0.070175 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `center_verse_last_in_chapter` | 3 | 1 | 0.052632 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `LXX` | `interior_or_unmapped` | 50 | 1 | 0.877193 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `TCG_NT` | `interior_or_unmapped` | 1 | 1 | 1.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `center_verse_first_in_chapter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `center_verse_last_in_chapter` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `center_verse_first_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `center_verse_last_in_book` | 0 | 0 | 0.000000 |
| `strong_full_span_exact_center` | `bible` | `UHB` | `interior_or_unmapped` | 14 | 1 | 1.000000 |
| ... | ... | ... | ... | ... | ... | 10 more rows in CSV |

## Read

- `interior_or_unmapped` includes ordinary interior verses and rows whose
  corpus/ref could not be mapped to a loaded boundary index.
- This is a distribution summary. It does not decide whether a position
  is meaningful without matched controls and a locked comparison rule.
