# Extended Match Strata Index

This index annotates the current centered occurrence index with cheap
post-search strata. It does not promote any row to claim status. The
extra flags are review-prioritization metadata that still require the
same preregistered controls described in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`.

## Reproduce

```bash
python3 -m scripts.build_match_strata_index --occurrences reports/centered_occurrence_index/centered_occurrences.csv --out reports/match_strata_index/occurrence_strata.csv --summary-out reports/match_strata_index/strata_summary.csv --markdown-out docs/MATCH_STRATA_INDEX.md --manifest-out reports/match_strata_index/manifest.json
```

## Bottom Line

- annotated occurrence rows: 923
- materialized now: `forward_only`, `backward_only`, `bidirectional_present`, `canonical_first_occurrence`.
- boundary endpoint strata are implemented as offset helpers in `els.match_strata`; they are not materialized from this centered index because the index does not retain every raw endpoint offset.

## Strata Counts

| Stratum | Rows |
| --- | ---: |
| `bidirectional_present` | 780 |
| `centered_self_exact_word` | 623 |
| `span_relevant` | 205 |
| `canonical_first_occurrence` | 153 |
| `backward_only` | 77 |
| `center_verse_relevant` | 73 |
| `forward_only` | 66 |
| `relevant_center_same_category` | 14 |
| `centered_self_surface_form` | 5 |
| `relevant_center_same_concept` | 3 |

## Top Annotated Rows

| Rank | Term | Center | Existing type | Direction stratum | Canonical first | Source |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `γωγ` (Gog; English: Gog) | REV 20:8=4 `Gog` | `centered_self_exact_word` | `bidirectional_present` | yes | `gog_source_review` |
| 2 | `γωγ` (Gog; English: Gog) | Rev 20:8=4 `Gog` | `centered_self_exact_word` | `bidirectional_present` | yes | `gog_source_review` |
| 3 | `γωγ` (Gog; English: Gog) | REV 20:8=4 `Gog` | `centered_self_exact_word` | `bidirectional_present` | yes | `gog_source_review` |
| 4 | `γωγ` (Gog; English: Gog) | REV 20:8=2 `Gog` | `centered_self_exact_word` | `bidirectional_present` | yes | `gog_source_review` |
| 5 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 8:17 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 6 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:2 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 7 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:6 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 8 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 3:9 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 9 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 9:5 `יֵשׁ֣וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 10 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 12:8 `יֵשׁ֧וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 11 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 10:18 `יֵשׁ֤וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 12 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:11 `יֵשׁ֖וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 13 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 9:4 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 14 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 2:36 `יֵשׁ֔וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 15 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 12:7 `יֵשֽׁוּעַ׃` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 16 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:39 `יֵשׁ֔וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 17 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | NEH 7:7 `יֵשׁ֡וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | yes | `original_language_findings` |
| 18 | `ישוע` (Yeshua; English: Yeshua/Jeshua) | EZR 3:2 `יֵשׁ֨וּעַ` (Yeshua; English: Yeshua/Jeshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 19 | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 1:21 `מָשִׁ֥יחַ` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 20 | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 23:1 `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 21 | `משיח` (Mashiach; English: Messiah/anointed one) | LAM 4:20 `מְשִׁ֣יחַ` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` | yes | `original_language_findings` |
| 22 | `γωγ` (Gog; English: Gog) | REV 20:8 `Γὼγ` (Gog; English: Gog) | `centered_self_exact_word` | `backward_only` | yes | `original_language_findings` |
| 23 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 18:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 24 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:7 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 25 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 26 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:24 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 27 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:28 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 28 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:30 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 29 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 4:20 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 30 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:16 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 31 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:3 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 32 | `ιησουσ` (Iesous; English: Jesus/Joshua) | NEH 9:5 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 33 | `ιησουσ` (Iesous; English: Jesus/Joshua) | 1MA 2:55 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 34 | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 1:38 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 35 | `ιησουσ` (Iesous; English: Jesus/Joshua) | DEU 32:44 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 36 | `ιησουσ` (Iesous; English: Jesus/Joshua) | HAG 1:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 37 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JDG 2:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 38 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 39 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:18 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 40 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:20 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 41 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:31 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 42 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 43 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:40 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 44 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:42 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 45 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:7 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 46 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 11:15 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 47 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 11:21 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 48 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 13:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 49 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 17:17 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 50 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 18:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 51 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 52 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 53 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 23:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 54 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 55 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 3:9 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 56 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 4:9 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 57 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:13 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 58 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:13 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 59 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 5:4 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 60 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 61 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:12 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 62 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 6:26 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 63 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:16 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 64 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:19 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 65 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:25 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 66 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 67 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 7:7 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 68 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:10 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 69 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:18 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 70 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 8:9 `Ἰησοῦς,` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 71 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:2 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 72 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:2 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 73 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:21 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 74 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:32 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 75 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:33 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 76 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:8 `Ἰησοῦς·` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 77 | `ιησουσ` (Iesous; English: Jesus/Joshua) | NEH 9:4 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 78 | `ιησουσ` (Iesous; English: Jesus/Joshua) | NUM 14:6 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | yes | `original_language_findings` |
| 79 | `ιησουσ` (Iesous; English: Jesus/Joshua) | SIR 46:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| 80 | `משיח` (Mashiach; English: Messiah/anointed one) | DAN 9:26 `מָשִׁ֖יחַ` (Mashiach; English: Messiah/anointed one) | `centered_self_exact_word` | `bidirectional_present` | no | `original_language_findings` |
| ... | ... | ... | ... | ... | ... | 843 more rows in CSV |

## Read

- `canonical_first_occurrence` means first centered occurrence within the current indexed family, not first hidden occurrence in every raw hit export.
- Direction strata are computed per source family / queue / corpus set / term group.
- Boundary, matrix, cipher, cross-skip, and cohort-density strata widen the review surface and need separate locked controls before claim language.

