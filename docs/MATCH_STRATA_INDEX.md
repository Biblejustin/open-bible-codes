# Extended Match Strata Index

This index annotates the current centered occurrence index with cheap
post-search strata. It does not promote any row to claim status. The
extra flags are review-prioritization metadata that still require the
same preregistered controls described in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`.

## Reproduce

```bash
python3 -m scripts.build_match_strata_index --occurrences reports/centered_occurrence_index/centered_occurrences.csv --meaningful-constants terms/meaningful_constants.csv --out reports/match_strata_index/occurrence_strata.csv --summary-out reports/match_strata_index/strata_summary.csv --markdown-out docs/MATCH_STRATA_INDEX.md --manifest-out reports/match_strata_index/manifest.json
```

## Bottom Line

- annotated occurrence rows: 923
- materialized now: `forward_only`, `backward_only`, `bidirectional_present`, `canonical_first_occurrence`, and available `boundary_*` endpoint strata.
- meaningful skip strata use the locked constants file and standard Hebrew/Greek gematria only as review flags.
- bigram-surprise strata compare the hidden term's adjacent letter pairs to the matched corpus text.
- boundary strata are exact only when the source occurrence row retains endpoint offsets for a mapped corpus.

## Strata Counts

| Stratum | Rows |
| --- | ---: |
| `bidirectional_present` | 780 |
| `centered_self_exact_word` | 623 |
| `span_relevant` | 205 |
| `canonical_first_occurrence` | 153 |
| `cross_skip_pair_at_word` | 122 |
| `backward_only` | 77 |
| `center_verse_relevant` | 73 |
| `forward_only` | 66 |
| `low_bigram_surprise` | 49 |
| `boundary_start_verse` | 22 |
| `relevant_center_same_category` | 14 |
| `boundary_end_verse` | 13 |
| `skip_equals_meaningful_constant` | 10 |
| `centered_self_surface_form` | 5 |
| `relevant_center_same_concept` | 3 |
| `boundary_end_book` | 2 |
| `boundary_end_chapter` | 2 |
| `boundary_both_endpoints` | 1 |
| `boundary_start_book` | 1 |
| `boundary_start_chapter` | 1 |

## Top Annotated Rows

| Rank | Term | Center | Existing type | Direction stratum | Boundary strata | Canonical first | Source |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | `γωγ` (Gog; English: Gog) | REV 20:8=4 `Gog` | `centered_self_exact_word` | `bidirectional_present` |  | yes | `gog_source_review` |
| 2 | `γωγ` (Gog; English: Gog) | Rev 20:8=4 `Gog` | `centered_self_exact_word` | `bidirectional_present` |  | yes | `gog_source_review` |
| 3 | `γωγ` (Gog; English: Gog) | REV 20:8=4 `Gog` | `centered_self_exact_word` | `bidirectional_present` |  | yes | `gog_source_review` |
| 4 | `γωγ` (Gog; English: Gog) | REV 20:8=2 `Gog` | `centered_self_exact_word` | `bidirectional_present` |  | yes | `gog_source_review` |
| 5 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 8:17 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 6 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:2 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 7 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:6 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 8 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 3:9 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 9 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 9:5 `יֵשׁ֣וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 10 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 12:8 `יֵשׁ֧וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 11 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 10:18 `יֵשׁ֤וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 12 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:11 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 13 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 9:4 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 14 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:36 `יֵשׁ֔וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 15 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 12:7 `יֵשֽׁוּעַ׃` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 16 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:39 `יֵשׁ֔וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 17 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:7 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | yes | `original_language_findings` |
| 18 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 3:2 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 19 | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 1:21 `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 20 | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 23:1 `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 21 | `משיח` (Mashiach; English: Messiah/anointed one) | LAM 4:20 `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` |  | yes | `original_language_findings` |
| 22 | `γωγ` (Gog; English: Gog) | REV 20:8 `Γὼγ` (Gog; English: Gog) | `centered_self_exact_word` | `backward_only` |  | yes | `original_language_findings` |
| 23 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 18:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 24 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:7 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 25 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 26 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:24 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 27 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:28 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 28 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:30 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 29 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 4:20 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 30 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:16 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 31 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 32 | `ιησουσ` (Iesous; English: Jesus/Joshua) | NEH 9:5 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 33 | `ιησουσ` (Iesous; English: Jesus/Joshua) | 1MA 2:55 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 34 | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 1:38 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 35 | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 32:44 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 36 | `ιησουσ` (Iesous; English: Jesus/Joshua) | HAG 1:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 37 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JDG 2:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 38 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 39 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:18 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 40 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:20 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 41 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:31 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 42 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 43 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:40 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 44 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:42 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 45 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:7 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 46 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 11:15 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 47 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 11:21 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 48 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 13:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 49 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 17:17 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 50 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 18:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 51 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 52 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 53 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 23:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 54 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 55 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 3:9 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 56 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 4:9 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 57 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:13 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 58 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:13 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 59 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:4 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 60 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 61 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 62 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:26 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 63 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:16 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 64 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:19 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 65 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:25 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 66 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 67 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:7 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 68 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 69 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:18 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 70 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:9 `Ἰησοῦς,` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 71 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:2 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 72 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:2 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 73 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:21 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 74 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:32 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 75 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:33 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 76 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:8 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 77 | `ιησουσ` (Iesous; English: Jesus/Joshua) | NEH 9:4 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 78 | `ιησουσ` (Iesous; English: Jesus/Joshua) | NUM 14:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | yes | `original_language_findings` |
| 79 | `ιησουσ` (Iesous; English: Jesus/Joshua) | SIR 46:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| 80 | `משיח` (Mashiach; English: Messiah/anointed one) | DAN 9:26 `מָשִׁ֖יחַ` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` |  | no | `original_language_findings` |
| ... | ... | ... | ... | ... | ... | ... | 843 more rows in CSV |

## Boundary Rows

| Rank | Term | Center | Boundary strata | Evidence | Source |
| ---: | --- | --- | --- | --- | --- |
| 83 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:6 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | boundary_end_verse | UHB:boundary_end_verse | `strong_full_span_exact_center` |
| 116 | `jesus` | MRK 5:27 `Jesus,` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 162 | `jesus` | MAT 13:1 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 178 | `jesus` | MAT 26:75 `Jesus,` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 191 | `jesus` | MRK 15:37 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 221 | `jesus` | ACT 17:3 `Jesus,` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 237 | `jesus` | COL 1:1 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 241 | `jesus` | GAL 2:4 `Jesus,` | boundary_end_verse | KJV:boundary_end_verse | `strong_full_span_exact_center` |
| 255 | `jesus` | JHN 11:5 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 271 | `jesus` | JHN 19:25 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 282 | `jesus` | JHN 20:19 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 312 | `jesus` | JHN 8:11 `Jesus` | boundary_both_endpoints;boundary_end_verse;boundary_start_verse | KJV:boundary_start_verse,boundary_end_verse,boundary_both_endpoints | `strong_full_span_exact_center` |
| 336 | `jesus` | LUK 20:8 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 377 | `jesus` | MAT 17:22 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 400 | `jesus` | MAT 26:50 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 409 | `jesus` | MAT 28:16 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 458 | `jesus` | MRK 5:19 `Jesus` | boundary_start_verse | KJV:boundary_start_verse | `strong_full_span_exact_center` |
| 488 | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 32:44 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | boundary_start_verse | LXX:boundary_start_verse | `strong_full_span_exact_center` |
| 665 | `adar` | 1Chr 11:19 `And` | boundary_end_verse | KJV:boundary_end_verse | `all_codes_followup` |
| 673 | `admah` | MAT 1:4 `Salmon;` | boundary_start_verse | KJVA:boundary_start_verse | `kjv_apocrypha_bridge_context` |
| 693 | `isaac` | MAT 1:2 `Judas` | boundary_start_verse | KJVA:boundary_start_verse | `kjv_apocrypha_bridge_context` |
| 734 | `ναοσ` (naos; English: Temple) | Heb 10:30 `Οἴδαμεν` (oidamen; English: we know) | boundary_end_verse | BYZ_NT:boundary_end_verse;SBLGNT:boundary_end_verse;TCG_NT:boundary_end_verse;TR_NT:boundary_end_verse | `all_codes_followup` |
| 737 | `adam` | 1Sam 9:22 `And` | boundary_end_verse | KJV:boundary_end_verse | `all_codes_followup` |
| 738 | `adar` | 1Sam 15:14 `And` | boundary_end_verse | KJV:boundary_end_verse | `all_codes_followup` |
| 739 | `mash` | 1Sam 28:18 `day.` | boundary_start_verse | KJV:boundary_start_verse | `all_codes_followup` |
| 767 | `σιων` (Sion; English: Zion) | TOB 1:2 `βασιλέως` (basileos; English: king) | boundary_end_verse | LXX:boundary_end_verse | `apocrypha_bridge_context` |
| 803 | `hail` | 2ES 16:76 `themselves.` | boundary_start_book;boundary_start_chapter;boundary_start_verse | KJVA:boundary_start_verse,boundary_start_chapter,boundary_start_book | `kjv_apocrypha_bridge_context` |
| 812 | `heart` | MAL 4:5 `great` | boundary_start_verse | KJVA:boundary_start_verse | `kjv_apocrypha_bridge_context` |
| 836 | `hits` | TOB 1:3 `justice,` | boundary_end_book;boundary_end_chapter;boundary_end_verse | KJVA:boundary_end_verse,boundary_end_chapter,boundary_end_book | `kjv_apocrypha_bridge_context` |
| 861 | `nato` | TOB 1:2 `was` | boundary_end_verse | KJVA:boundary_end_verse | `kjv_apocrypha_bridge_context` |
| 865 | `noah` | TOB 1:3 `truth` | boundary_start_verse | KJVA:boundary_start_verse | `kjv_apocrypha_bridge_context` |
| 867 | `obed` | 2ES 16:78 `and` | boundary_end_verse | KJVA:boundary_end_verse | `kjv_apocrypha_bridge_context` |
| 902 | `teeth` | MAL 4:3 `tread` | boundary_end_verse | KJVA:boundary_end_verse | `kjv_apocrypha_bridge_context` |
| 918 | `water` | TOB 1:3 `Tobit` | boundary_end_book;boundary_end_chapter;boundary_end_verse | KJVA:boundary_end_verse,boundary_end_chapter,boundary_end_book | `kjv_apocrypha_bridge_context` |

## Cross-Skip Center Rows

| Rank | Term | Center | Pair count | Peer terms | Skip values | Source |
| ---: | --- | --- | ---: | --- | --- | --- |
| 670 | `αμην` (amen; English: Amen) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | 2 | ελαμ;σιων | -209;-154 | `apocrypha_bridge_context` |
| 672 | `σιων` (Sion; English: Zion) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | 2 | αμην;ελαμ | -209;191 | `apocrypha_bridge_context` |
| 674 | `ahab` | MAT 1:1 `generation` | 3 | gate;obal;star | -111;-84;194 | `kjv_apocrypha_bridge_context` |
| 678 | `eden` | MAL 4:4 `judgments.` | 1 | heth | 163 | `kjv_apocrypha_bridge_context` |
| 681 | `eyes` | 2ES 16:77 `field` | 1 | tomb | 134 | `kjv_apocrypha_bridge_context` |
| 684 | `hail` | 2ES 16:78 `be` | 2 | soot;thin | 188;227 | `kjv_apocrypha_bridge_context` |
| 685 | `hand` | MAL 4:6 `their` | 1 | seed | -238 | `kjv_apocrypha_bridge_context` |
| 690 | `hits` | MAL 4:6 `heart` | 3 | lane;soot;torah | -81;226;240 | `kjv_apocrypha_bridge_context` |
| 691 | `hits` | MAL 4:6 `fathers` | 2 | soot;wine | 124;131 | `kjv_apocrypha_bridge_context` |
| 692 | `house` | TOB 1:3 `justice,` | 1 | hits | -210 | `kjv_apocrypha_bridge_context` |
| 693 | `isaac` | MAT 1:2 `Judas` | 1 | tomb | 217 | `kjv_apocrypha_bridge_context` |
| 694 | `king` | MAL 4:5 `the` | 2 | hail;yhwh | -218;189 | `kjv_apocrypha_bridge_context` |
| 696 | `lane` | MAL 4:6 `fathers,` | 2 | seed;soot | -123;-53 | `kjv_apocrypha_bridge_context` |
| 697 | `lane` | MAL 4:6 `heart` | 3 | hits;soot;torah | -85;-81;240 | `kjv_apocrypha_bridge_context` |
| 698 | `lane` | MAL 4:6 `and` | 2 | eden;seed | -115;140 | `kjv_apocrypha_bridge_context` |
| 699 | `lane` | MAT 1:2 `Isaac` | 2 | horn | 126;208 | `kjv_apocrypha_bridge_context` |
| 700 | `light` | TOB 1:2 `Galilee` | 1 | tyre | 198 | `kjv_apocrypha_bridge_context` |
| 701 | `lion` | 2ES 16:77 `may` | 1 | fire | 176 | `kjv_apocrypha_bridge_context` |
| 702 | `love` | TOB 1:2 `of` | 1 | holy | 204 | `kjv_apocrypha_bridge_context` |
| 703 | `obal` | MAT 1:3 `begat` | 1 | seed | -182 | `kjv_apocrypha_bridge_context` |
| 705 | `rome` | TOB 1:2 `properly` | 2 | eden;seed | -238;-197 | `kjv_apocrypha_bridge_context` |
| 706 | `seed` | TOB 1:1 `the` | 7 | ahab;fire;gate;life;rent;tyre | -229;-225;-169;-159;-121;73;229 | `kjv_apocrypha_bridge_context` |
| 708 | `seed` | TOB 1:1 `son` | 2 | ahab;hand | -206;-161 | `kjv_apocrypha_bridge_context` |
| 710 | `seed` | TOB 1:1 `of` | 4 | hits;nato;sign;soot | -222;-73;-70;248 | `kjv_apocrypha_bridge_context` |
| 711 | `seed` | TOB 1:2 `captive` | 1 | hits | -166 | `kjv_apocrypha_bridge_context` |
| 712 | `seed` | TOB 1:2 `properly` | 2 | eden;rome | -197;250 | `kjv_apocrypha_bridge_context` |
| 713 | `soot` | MAL 4:6 `fathers,` | 2 | lane;seed | -53;192 | `kjv_apocrypha_bridge_context` |
| 714 | `soot` | MAL 4:6 `fathers` | 2 | hits;wine | -141;131 | `kjv_apocrypha_bridge_context` |
| 715 | `soot` | MAL 4:6 `heart` | 3 | hits;lane;torah | -85;-81;226 | `kjv_apocrypha_bridge_context` |
| 717 | `tomb` | 2ES 16:77 `field` | 1 | eyes | -143 | `kjv_apocrypha_bridge_context` |
| 718 | `tyre` | TOB 1:2 `Galilee` | 1 | light | -127 | `kjv_apocrypha_bridge_context` |
| 746 | `αιμα` (haima; English: Blood) | TOB 1:2 `ὁδοῖς` (odois; English: ways) | 1 | βασαν | -222 | `apocrypha_bridge_context` |
| 752 | `αμην` (amen; English: Amen) | TOB 1:1 `Τωβιήλ,` (tobiel; English: Tobiel) | 1 | ρωμη | -221 | `apocrypha_bridge_context` |
| 754 | `βασαν` (basan; English: Bashan) | TOB 1:2 `ὁδοῖς` (odois; English: ways) | 1 | αιμα | -210 | `apocrypha_bridge_context` |
| 755 | `ελαμ` (Elam; English: Elam) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | 2 | αμην;σιων | -154;191 | `apocrypha_bridge_context` |
| 756 | `ελαμ` (Elam; English: Elam) | TOB 1:2 `βασιλέως` (basileos; English: king) | 1 | σιων | -218 | `apocrypha_bridge_context` |
| 761 | `ρωμη` (rome; English: Rome) | TOB 1:1 `Τωβιήλ,` (tobiel; English: Tobiel) | 1 | αμην | 247 | `apocrypha_bridge_context` |
| 767 | `σιων` (Sion; English: Zion) | TOB 1:2 `βασιλέως` (basileos; English: king) | 1 | ελαμ | 120 | `apocrypha_bridge_context` |
| 768 | `aaron` | 2ES 16:78 `undressed,` | 1 | obed | -224 | `kjv_apocrypha_bridge_context` |
| 773 | `ahab` | TOB 1:1 `son` | 2 | hand;seed | -206;-73 | `kjv_apocrypha_bridge_context` |
| 774 | `ahab` | TOB 1:1 `the` | 7 | fire;gate;life;rent;seed;tyre | -229;-225;-159;-121;54;73;229 | `kjv_apocrypha_bridge_context` |
| 778 | `death` | TOB 1:2 `Assyrians` | 1 | heart | -165 | `kjv_apocrypha_bridge_context` |
| 781 | `eber` | TOB 1:3 `the` | 1 | noah | -231 | `kjv_apocrypha_bridge_context` |
| 782 | `eber` | TOB 1:3 `days` | 1 | ehyeh | -198 | `kjv_apocrypha_bridge_context` |
| 783 | `eber` | TOB 1:3 `the` | 1 | noah | -231 | `kjv_apocrypha_bridge_context` |
| 785 | `eden` | MAL 4:6 `and` | 2 | lane;seed | -232;-115 | `kjv_apocrypha_bridge_context` |
| 787 | `eden` | TOB 1:2 `properly` | 2 | rome;seed | -238;250 | `kjv_apocrypha_bridge_context` |
| 789 | `ehyeh` | TOB 1:3 `days` | 1 | eber | 211 | `kjv_apocrypha_bridge_context` |
| 791 | `fire` | 2ES 16:77 `may` | 1 | lion | 226 | `kjv_apocrypha_bridge_context` |
| 792 | `fire` | TOB 1:1 `the` | 6 | ahab;gate;life;rent;seed;tyre | -225;-169;-159;-121;54;73 | `kjv_apocrypha_bridge_context` |
| 793 | `fire` | TOB 1:1 `the` | 6 | ahab;gate;life;rent;seed;tyre | -225;-169;-159;-121;54;73 | `kjv_apocrypha_bridge_context` |
| 795 | `gate` | MAL 4:5 `great` | 2 | heart;torah | -130;-85 | `kjv_apocrypha_bridge_context` |
| 796 | `gate` | MAT 1:1 `generation` | 3 | ahab;obal;star | -111;145;194 | `kjv_apocrypha_bridge_context` |
| 798 | `gate` | MAT 1:1 `The` | 1 | water | -200 | `kjv_apocrypha_bridge_context` |
| 801 | `gate` | TOB 1:1 `the` | 7 | ahab;fire;life;rent;seed;tyre | -229;-225;-169;-159;54;73;229 | `kjv_apocrypha_bridge_context` |
| 802 | `haifa` | MAL 4:6 `I` | 1 | life | 250 | `kjv_apocrypha_bridge_context` |
| 804 | `hail` | MAL 4:5 `the` | 2 | king;yhwh | -218;-192 | `kjv_apocrypha_bridge_context` |
| 805 | `hail` | MAL 4:5 `LORD` | 1 | sidon | 224 | `kjv_apocrypha_bridge_context` |
| 806 | `hail` | TOB 1:2 `Who` | 1 | soot | -221 | `kjv_apocrypha_bridge_context` |
| 808 | `hand` | MAL 4:5 `Behold,` | 1 | seed | 189 | `kjv_apocrypha_bridge_context` |
| 809 | `hand` | TOB 1:1 `son` | 2 | ahab;seed | -161;-73 | `kjv_apocrypha_bridge_context` |
| 812 | `heart` | MAL 4:5 `great` | 2 | gate;torah | -144;-85 | `kjv_apocrypha_bridge_context` |
| 814 | `heart` | TOB 1:2 `Assyrians` | 1 | death | 228 | `kjv_apocrypha_bridge_context` |
| 815 | `herod` | 2ES 16:77 `covered` | 2 | hits | 205;215 | `kjv_apocrypha_bridge_context` |
| 816 | `heth` | MAL 4:4 `judgments.` | 1 | eden | 233 | `kjv_apocrypha_bridge_context` |
| 821 | `heth` | MAT 1:2 `Jacob;` | 1 | seed | -156 | `kjv_apocrypha_bridge_context` |
| 822 | `heth` | MAT 1:5 `Booz` | 1 | shoah | 231 | `kjv_apocrypha_bridge_context` |
| 825 | `hits` | 2ES 16:77 `covered` | 1 | herod | 238 | `kjv_apocrypha_bridge_context` |
| 826 | `hits` | 2ES 16:77 `covered` | 1 | herod | 238 | `kjv_apocrypha_bridge_context` |
| 830 | `hits` | MAL 4:5 `dreadful` | 1 | seed | -178 | `kjv_apocrypha_bridge_context` |
| 832 | `hits` | TOB 1:1 `of` | 4 | nato;seed;sign;soot | -222;-178;-70;248 | `kjv_apocrypha_bridge_context` |
| 833 | `hits` | TOB 1:1 `Tobit,` | 1 | lord | -145 | `kjv_apocrypha_bridge_context` |
| 834 | `hits` | TOB 1:2 `captive` | 1 | seed | 125 | `kjv_apocrypha_bridge_context` |
| 836 | `hits` | TOB 1:3 `justice,` | 1 | house | 196 | `kjv_apocrypha_bridge_context` |
| 837 | `holy` | TOB 1:2 `is` | 1 | ruth | -242 | `kjv_apocrypha_bridge_context` |
| 838 | `holy` | TOB 1:2 `of` | 1 | love | 222 | `kjv_apocrypha_bridge_context` |
| 840 | `horn` | MAT 1:2 `Isaac` | 1 | lane | -124 | `kjv_apocrypha_bridge_context` |
| 841 | `horn` | MAT 1:2 `Isaac` | 1 | lane | -124 | `kjv_apocrypha_bridge_context` |
| 851 | `life` | MAL 4:6 `I` | 1 | haifa | -121 | `kjv_apocrypha_bridge_context` |
| 852 | `life` | TOB 1:1 `the` | 7 | ahab;fire;gate;rent;seed;tyre | -229;-225;-169;-121;54;73;229 | `kjv_apocrypha_bridge_context` |
| ... | ... | ... | ... | ... | ... | 42 more cross-skip rows in CSV |

## Meaningful Skip Rows

| Rank | Term | Center | Skip | Constant match | Term gematria match | Source |
| ---: | --- | --- | --- | --- | --- | --- |
| 2 | `γωγ` (Gog; English: Gog) | Rev 20:8=4 `Gog` | -7;7;-4423;4423 | 7: Sabbath / completeness |  | `gog_source_review` |
| 626 | `παισ` (pais; English: Servant) | Luke 22:64 `παίσας` (paisas) | -7 | 7: Sabbath / completeness |  | `all_codes_followup` |
| 636 | `תורה` (twrh; English: Torah) | 1Chr 5:1 `בֶּן־יִשְׂרָאֵ֑ל` (bnyshrl) | 7 | 7: Sabbath / completeness |  | `all_codes_followup` |
| 637 | `תורה` (twrh; English: Torah) | 2Kgs 17:20 `יִשְׂרָאֵל֙` (Yisrael; English: Israel) | -7 | 7: Sabbath / completeness |  | `all_codes_followup` |
| 685 | `hand` | MAL 4:6 `their` | 40 | 40: Wilderness / testing |  | `kjv_apocrypha_bridge_context` |
| 720 | `התשח` (htshch; English: Hebrew year 5708) | Lev 22:27 `וָהָ֔לְאָה` (whlh) | 40 | 40: Wilderness / testing |  | `all_codes_followup` |
| 735 | `νατο` (nato; English: NATO) | 1Cor 1:27 `μωρὰ` (mora; English: foolish things) | 7 | 7: Sabbath / completeness |  | `all_codes_followup` |
| 795 | `gate` | MAL 4:5 `great` | -144 | 144: Revelation square of twelve |  | `kjv_apocrypha_bridge_context` |
| 829 | `hits` | MAL 4:5 `before` | 144 | 144: Revelation square of twelve |  | `kjv_apocrypha_bridge_context` |
| 896 | `soot` | TOB 1:1 `of` | -70 | 70: Nations / exile years |  | `kjv_apocrypha_bridge_context` |

## Bigram Surprise Rows

| Rank | Term | Center | Stratum | Evidence | Min/max counts | Source |
| ---: | --- | --- | --- | --- | --- | --- |
| 644 | `μαρια` (Maria; English: Mary) | MAL 4:6 `Ἰσραὴλ` (israel; English: Israel) | `low_bigram_surprise` | μα:16196;αρ:17084;ρι:20410;ια:32513 | 16196/32513 | `apocrypha_bridge_context` |
| 678 | `eden` | MAL 4:4 `judgments.` | `low_bigram_surprise` | ed:33489;de:17773;en:40399 | 17773/40399 | `kjv_apocrypha_bridge_context` |
| 685 | `hand` | MAL 4:6 `their` | `low_bigram_surprise` | ha:58723;an:90242;nd:76718 | 58723/90242 | `kjv_apocrypha_bridge_context` |
| 686 | `hand` | MAL 4:6 `lest` | `low_bigram_surprise` | ha:58723;an:90242;nd:76718 | 58723/90242 | `kjv_apocrypha_bridge_context` |
| 687 | `hand` | MAT 1:5 `begat` | `low_bigram_surprise` | ha:58723;an:90242;nd:76718 | 58723/90242 | `kjv_apocrypha_bridge_context` |
| 776 | `bear` | MAT 1:3 `and` | `low_bigram_surprise` | be:22507;ea:43577;ar:25373 | 22507/43577 | `kjv_apocrypha_bridge_context` |
| 778 | `death` | TOB 1:2 `Assyrians` | `low_bigram_surprise` | de:17773;ea:43577;at:39393;th:195529 | 17773/195529 | `kjv_apocrypha_bridge_context` |
| 779 | `dedan` | MAL 4:6 `And` | `low_bigram_surprise` | de:17773;ed:33489;da:24821;an:90242 | 17773/90242 | `kjv_apocrypha_bridge_context` |
| 780 | `earth` | 2ES 16:75 `afraid` | `low_bigram_surprise` | ea:43577;ar:25373;rt:18883;th:195529 | 18883/195529 | `kjv_apocrypha_bridge_context` |
| 784 | `eden` | MAL 4:5 `you` | `low_bigram_surprise` | ed:33489;de:17773;en:40399 | 17773/40399 | `kjv_apocrypha_bridge_context` |
| 785 | `eden` | MAL 4:6 `and` | `low_bigram_surprise` | ed:33489;de:17773;en:40399 | 17773/40399 | `kjv_apocrypha_bridge_context` |
| 786 | `eden` | TOB 1:1 `The` | `low_bigram_surprise` | ed:33489;de:17773;en:40399 | 17773/40399 | `kjv_apocrypha_bridge_context` |
| 787 | `eden` | TOB 1:2 `properly` | `low_bigram_surprise` | ed:33489;de:17773;en:40399 | 17773/40399 | `kjv_apocrypha_bridge_context` |
| 807 | `hand` | 2ES 16:77 `their` | `low_bigram_surprise` | ha:58723;an:90242;nd:76718 | 58723/90242 | `kjv_apocrypha_bridge_context` |
| 808 | `hand` | MAL 4:5 `Behold,` | `low_bigram_surprise` | ha:58723;an:90242;nd:76718 | 58723/90242 | `kjv_apocrypha_bridge_context` |
| 809 | `hand` | TOB 1:1 `son` | `low_bigram_surprise` | ha:58723;an:90242;nd:76718 | 58723/90242 | `kjv_apocrypha_bridge_context` |
| 810 | `heal` | MAL 4:4 `law` | `low_bigram_surprise` | he:153400;ea:43577;al:32047 | 32047/153400 | `kjv_apocrypha_bridge_context` |
| 811 | `heart` | MAL 4:4 `commanded` | `low_bigram_surprise` | he:153400;ea:43577;ar:25373;rt:18883 | 18883/153400 | `kjv_apocrypha_bridge_context` |
| 812 | `heart` | MAL 4:5 `great` | `low_bigram_surprise` | he:153400;ea:43577;ar:25373;rt:18883 | 18883/153400 | `kjv_apocrypha_bridge_context` |
| 813 | `heart` | MAL 4:5 `Elijah` | `low_bigram_surprise` | he:153400;ea:43577;ar:25373;rt:18883 | 18883/153400 | `kjv_apocrypha_bridge_context` |
| 814 | `heart` | TOB 1:2 `Assyrians` | `low_bigram_surprise` | he:153400;ea:43577;ar:25373;rt:18883 | 18883/153400 | `kjv_apocrypha_bridge_context` |
| 816 | `heth` | MAL 4:4 `judgments.` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 817 | `heth` | MAL 4:4 `which` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 818 | `heth` | MAL 4:4 `servant,` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 819 | `heth` | MAL 4:5 `will` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 820 | `heth` | MAT 1:1 `son` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 821 | `heth` | MAT 1:2 `Jacob;` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 822 | `heth` | MAT 1:5 `Booz` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 823 | `heth` | TOB 1:3 `nation,` | `low_bigram_surprise` | he:153400;et:40713;th:195529 | 40713/195529 | `kjv_apocrypha_bridge_context` |
| 857 | `mash` | 2ES 16:77 `like` | `low_bigram_surprise` | ma:20579;as:23084;sh:27021 | 20579/27021 | `kjv_apocrypha_bridge_context` |
| 858 | `mash` | MAT 1:2 `begat` | `low_bigram_surprise` | ma:20579;as:23084;sh:27021 | 20579/27021 | `kjv_apocrypha_bridge_context` |
| 870 | `otho` | 2ES 16:76 `weigh` | `low_bigram_surprise` | ot:25564;th:195529;ho:25372 | 25372/195529 | `kjv_apocrypha_bridge_context` |
| 871 | `otho` | 2ES 16:77 `unto` | `low_bigram_surprise` | ot:25564;th:195529;ho:25372 | 25372/195529 | `kjv_apocrypha_bridge_context` |
| 872 | `rent` | TOB 1:1 `the` | `low_bigram_surprise` | re:50330;en:40399;nt:46361 | 40399/50330 | `kjv_apocrypha_bridge_context` |
| 873 | `rent` | TOB 1:2 `which` | `low_bigram_surprise` | re:50330;en:40399;nt:46361 | 40399/50330 | `kjv_apocrypha_bridge_context` |
| 874 | `rent` | TOB 1:2 `right` | `low_bigram_surprise` | re:50330;en:40399;nt:46361 | 40399/50330 | `kjv_apocrypha_bridge_context` |
| 875 | `resen` | 2ES 16:76 `iniquities` | `low_bigram_surprise` | re:50330;es:47860;se:28717;en:40399 | 28717/50330 | `kjv_apocrypha_bridge_context` |
| 886 | `shem` | MAL 4:4 `Israel,` | `low_bigram_surprise` | sh:27021;he:153400;em:21585 | 21585/153400 | `kjv_apocrypha_bridge_context` |
| 904 | `thin` | 2ES 16:77 `travel` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 905 | `thin` | 2ES 16:77 `travel` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 906 | `thin` | 2ES 16:78 `be` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 907 | `thin` | MAL 4:5 `prophet` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 908 | `thin` | MAT 1:5 `Salmon` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 909 | `thin` | TOB 1:1 `Nephthali;` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 910 | `thin` | TOB 1:2 `king` | `low_bigram_surprise` | th:195529;hi:41738;in:55949 | 41738/195529 | `kjv_apocrypha_bridge_context` |
| 919 | `wine` | MAL 4:5 `coming` | `low_bigram_surprise` | wi:17895;in:55949;ne:20523 | 17895/55949 | `kjv_apocrypha_bridge_context` |
| 920 | `wine` | MAL 4:6 `fathers` | `low_bigram_surprise` | wi:17895;in:55949;ne:20523 | 17895/55949 | `kjv_apocrypha_bridge_context` |
| 921 | `wine` | MAT 1:2 `and` | `low_bigram_surprise` | wi:17895;in:55949;ne:20523 | 17895/55949 | `kjv_apocrypha_bridge_context` |
| 922 | `wine` | TOB 1:3 `have` | `low_bigram_surprise` | wi:17895;in:55949;ne:20523 | 17895/55949 | `kjv_apocrypha_bridge_context` |

## Read

- `canonical_first_occurrence` means first centered occurrence within the current indexed family, not first hidden occurrence in every raw hit export.
- Direction strata are computed per source family / queue / corpus set / term group.
- Boundary strata are computed only from retained endpoint offsets, so blank boundary fields mean unavailable evidence, not proven absence.
- `cross_skip_pair_at_word` means at least one other normalized term shares the same center word/reference in the indexed family at a different skip.
- `skip_equals_meaningful_constant` and `skip_equals_term_gematria` are metadata flags; they do not change the search space or promote claim status.
- Bigram-surprise strata are corpus-local review aids, not claim promotion rules; missing adjacent surface bigrams count as rare.
- Matrix, cipher, broader cross-skip, and cohort-density strata widen the review surface and need separate locked controls before claim language.

