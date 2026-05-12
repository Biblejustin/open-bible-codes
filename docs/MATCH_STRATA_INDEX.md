# Extended Match Strata Index

This index annotates the current centered occurrence index with cheap
post-search strata. It does not promote any row to claim status. The
extra flags are review-prioritization metadata that still require the
same preregistered controls described in `docs/HYPOTHESIS_ANALYSIS_FRAMEWORK.md`.

## Reproduce

```bash
python3 -m scripts.build_match_strata_index --occurrences reports/centered_occurrence_index/centered_occurrences.csv --meaningful-constants terms/meaningful_constants.csv --thematic-chapters data/study/mappings/thematic_chapters.csv --author-book-mapping data/study/mappings/author_book_mapping.csv --protagonist-narrative-mapping data/study/mappings/protagonist_narrative_mapping.csv --out reports/match_strata_index/occurrence_strata.csv --summary-out reports/match_strata_index/strata_summary.csv --markdown-out docs/MATCH_STRATA_INDEX.md --manifest-out reports/match_strata_index/manifest.json --cross-skip-letter-distance 10
```

## Bottom Line

- annotated occurrence rows: 923
- materialized now: `forward_only`, `backward_only`, `bidirectional_present`, `canonical_first_occurrence`, available `boundary_*` endpoint strata, and cross-skip pair strata.
- mapping-dependent strata use locked CSVs under `data/study/mappings/`; only rows matching populated entries are flagged.
- meaningful skip strata use the locked constants file and standard Hebrew/Greek gematria only as review flags.
- bigram-surprise strata compare the hidden term's adjacent letter pairs to the matched corpus text.
- letter-frequency anomaly strata compare the hidden term's individual letters to the matched corpus text.
- center-position strata flag when the center verse is first/last in its chapter or book.
- boundary strata are exact only when the source occurrence row retains endpoint offsets for a mapped corpus.

## Strata Counts

| Stratum | Rows |
| --- | ---: |
| `bidirectional_present` | 780 |
| `centered_self_exact_word` | 623 |
| `protagonist_in_own_narrative` | 305 |
| `cross_skip_pair_within_N_letters` | 228 |
| `span_relevant` | 205 |
| `cross_skip_pair_at_letter` | 171 |
| `canonical_first_occurrence` | 153 |
| `cross_skip_pair_at_word` | 122 |
| `center_verse_first_in_chapter` | 82 |
| `backward_only` | 77 |
| `center_verse_relevant` | 73 |
| `forward_only` | 66 |
| `center_verse_last_in_chapter` | 64 |
| `center_verse_first_in_book` | 50 |
| `low_bigram_surprise` | 49 |
| `center_verse_last_in_book` | 42 |
| `boundary_start_verse` | 22 |
| `relevant_center_same_category` | 14 |
| `boundary_end_verse` | 13 |
| `skip_equals_meaningful_constant` | 10 |
| `canonical_first_in_thematic_chapter` | 6 |
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

## Center Position Rows

| Rank | Term | Center | Center position strata | Evidence | Source |
| ---: | --- | --- | --- | --- | --- |
| 20 | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 23:1 `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) | center_verse_first_in_chapter | EBIBLE_WLC:center_verse_first_in_chapter | `original_language_findings` |
| 44 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:42 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_last_in_chapter | LXX:center_verse_last_in_chapter | `original_language_findings` |
| 48 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 13:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `original_language_findings` |
| 51 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_last_in_chapter | LXX:center_verse_last_in_chapter | `original_language_findings` |
| 53 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 23:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `original_language_findings` |
| 54 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `original_language_findings` |
| 75 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:33 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_last_in_chapter | LXX:center_verse_last_in_chapter | `original_language_findings` |
| 79 | `ιησουσ` (Iesous; English: Jesus/Joshua) | SIR 46:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `original_language_findings` |
| 96 | `משיח` (Mashiach; English: Messiah/anointed one) | 2SA 23:1 `מְשִׁ֨יחַ֙` (Mashiach; English: Messiah/anointed one) | center_verse_first_in_chapter | EBIBLE_WLC:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 101 | `jesus` | ACT 18:28 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 107 | `jesus` | MAT 18:1 `Jesus,` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 112 | `jesus` | MAT 2:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 114 | `jesus` | MAT 8:34 `Jesus:` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 123 | `jesus` | ACT 28:31 `Jesus` | center_verse_last_in_book;center_verse_last_in_chapter | KJV:center_verse_last_in_chapter,center_verse_last_in_book | `strong_full_span_exact_center` |
| 129 | `jesus` | GAL 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 139 | `jesus` | JHN 21:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 152 | `jesus` | LUK 19:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 162 | `jesus` | MAT 13:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 165 | `jesus` | MAT 15:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 174 | `jesus` | MAT 24:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 178 | `jesus` | MAT 26:75 `Jesus,` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 189 | `jesus` | MRK 11:33 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 196 | `jesus` | ROM 8:39 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 211 | `jesus` | 1TH 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 233 | `jesus` | ACT 5:42 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 237 | `jesus` | COL 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 245 | `jesus` | JAS 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 263 | `jesus` | JHN 17:1 `Jesus,` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 287 | `jesus` | JHN 21:25 `Jesus` | center_verse_last_in_book;center_verse_last_in_chapter | KJV:center_verse_last_in_chapter,center_verse_last_in_book | `strong_full_span_exact_center` |
| 292 | `jesus` | JHN 4:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 311 | `jesus` | JHN 8:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 321 | `jesus` | JHN 8:59 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 342 | `jesus` | LUK 2:52 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 344 | `jesus` | LUK 4:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 364 | `jesus` | MAT 11:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 365 | `jesus` | MAT 12:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 368 | `jesus` | MAT 14:1 `Jesus,` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 380 | `jesus` | MAT 19:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 386 | `jesus` | MAT 1:25 `JESUS.` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 392 | `jesus` | MAT 22:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 396 | `jesus` | MAT 23:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 414 | `jesus` | MAT 4:1 `Jesus` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 434 | `jesus` | MRK 10:52 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 450 | `jesus` | MRK 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 470 | `jesus` | PHP 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 473 | `jesus` | PHP 4:23 `Jesus` | center_verse_last_in_book;center_verse_last_in_chapter | KJV:center_verse_last_in_chapter,center_verse_last_in_book | `strong_full_span_exact_center` |
| 475 | `jesus` | ROM 13:14 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 477 | `jesus` | ROM 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 481 | `jesus` | ROM 6:23 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 483 | `jesus` | ROM 7:25 `Jesus` | center_verse_last_in_chapter | KJV:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 484 | `jesus` | ROM 8:1 `Jesus,` | center_verse_first_in_chapter | KJV:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 485 | `jesus` | TIT 1:1 `Jesus` | center_verse_first_in_book;center_verse_first_in_chapter | KJV:center_verse_first_in_chapter,center_verse_first_in_book | `strong_full_span_exact_center` |
| 497 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 10:42 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_last_in_chapter | LXX:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 501 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 13:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 504 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 22:34 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_last_in_chapter | LXX:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 506 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 23:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 507 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 24:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 528 | `ιησουσ` (Iesous; English: Jesus/Joshua) | JOS 9:33 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_last_in_chapter | LXX:center_verse_last_in_chapter | `strong_full_span_exact_center` |
| 532 | `ιησουσ` (Iesous; English: Jesus/Joshua) | SIR 46:1 `Ἰησοῦς` (Iesous; English: Jesus/Joshua) | center_verse_first_in_chapter | LXX:center_verse_first_in_chapter | `strong_full_span_exact_center` |
| 636 | `תורה` (twrh; English: Torah) | 1Chr 5:1 `בֶּן־יִשְׂרָאֵ֑ל` (bnyshrl) | center_verse_first_in_chapter | MAM:center_verse_first_in_chapter;MT_WLC:center_verse_first_in_chapter;UXLC:center_verse_first_in_chapter | `all_codes_followup` |
| 644 | `μαρια` (Maria; English: Mary) | MAL 4:6 `Ἰσραὴλ` (israel; English: Israel) | center_verse_last_in_book;center_verse_last_in_chapter | LXX:center_verse_last_in_chapter,center_verse_last_in_book | `apocrypha_bridge_context` |
| 645 | `torah` | MAT 1:1 `Abraham.` | center_verse_first_in_book;center_verse_first_in_chapter | KJVA:center_verse_first_in_chapter,center_verse_first_in_book | `kjv_apocrypha_bridge_context` |
| 649 | `ביבי` (byby; English: Bibi) | 1Chr 2:55 `ישבו` (yashvu; English: they dwelt/sat) | center_verse_last_in_chapter | MAM:center_verse_last_in_chapter;MT_WLC:center_verse_last_in_chapter;UXLC:center_verse_last_in_chapter | `all_codes_followup` |
| 662 | `κινα` (kina; English: China) | 1John 2:1 `δίκαιον` (dikaion; English: righteous) | center_verse_first_in_chapter | SBLGNT:center_verse_first_in_chapter | `all_codes_followup` |
| 670 | `αμην` (amen; English: Amen) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | center_verse_last_in_book;center_verse_last_in_chapter | LXX:center_verse_last_in_chapter,center_verse_last_in_book | `apocrypha_bridge_context` |
| 672 | `σιων` (Sion; English: Zion) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | center_verse_last_in_book;center_verse_last_in_chapter | LXX:center_verse_last_in_chapter,center_verse_last_in_book | `apocrypha_bridge_context` |
| 674 | `ahab` | MAT 1:1 `generation` | center_verse_first_in_book;center_verse_first_in_chapter | KJVA:center_verse_first_in_chapter,center_verse_first_in_book | `kjv_apocrypha_bridge_context` |
| 682 | `gate` | MAL 4:6 `children` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 684 | `hail` | 2ES 16:78 `be` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 685 | `hand` | MAL 4:6 `their` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 686 | `hand` | MAL 4:6 `lest` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 690 | `hits` | MAL 4:6 `heart` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 691 | `hits` | MAL 4:6 `fathers` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 695 | `lane` | MAL 4:6 `children,` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 696 | `lane` | MAL 4:6 `fathers,` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 697 | `lane` | MAL 4:6 `heart` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 698 | `lane` | MAL 4:6 `and` | center_verse_last_in_book;center_verse_last_in_chapter | KJVA:center_verse_last_in_chapter,center_verse_last_in_book | `kjv_apocrypha_bridge_context` |
| 706 | `seed` | TOB 1:1 `the` | center_verse_first_in_book;center_verse_first_in_chapter | KJVA:center_verse_first_in_chapter,center_verse_first_in_book | `kjv_apocrypha_bridge_context` |
| 707 | `seed` | TOB 1:1 `tribe` | center_verse_first_in_book;center_verse_first_in_chapter | KJVA:center_verse_first_in_chapter,center_verse_first_in_book | `kjv_apocrypha_bridge_context` |
| 708 | `seed` | TOB 1:1 `son` | center_verse_first_in_book;center_verse_first_in_chapter | KJVA:center_verse_first_in_chapter,center_verse_first_in_book | `kjv_apocrypha_bridge_context` |
| ... | ... | ... | ... | ... | 66 more center-position rows in CSV |

## Cross-Skip Pair Rows

| Rank | Term | Center | At word | At letter | Within N letters | Source |
| ---: | --- | --- | --- | --- | --- | --- |
| 639 | `ιωυαν` (Iouan; English: Javan) | 1Pet 5:13 `Βαβυλῶνι` (babuloni; English: Babylon) |  |  | 1: ελκη; min=4 | `all_codes_followup` |
| 644 | `μαρια` (Maria; English: Mary) | MAL 4:6 `Ἰσραὴλ` (israel; English: Israel) |  | 2: αδαμ;ελαμ | 2: αδαμ;ελαμ; min=0 | `apocrypha_bridge_context` |
| 645 | `torah` | MAT 1:1 `Abraham.` |  | 1: gate | 5: bread;gate;herod;horn;sheba; min=4 | `kjv_apocrypha_bridge_context` |
| 661 | `ελκη` (elke; English: Boils) | 1Pet 5:13 `συνεκλεκτή` (suneklekte; English: co-elect) |  |  | 1: ιωυαν; min=4 | `all_codes_followup` |
| 670 | `αμην` (amen; English: Amen) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | 2: ελαμ;σιων |  | 1: θεοσ; min=2 | `apocrypha_bridge_context` |
| 671 | `αμμων` (ammon; English: Ammon) | TOB 1:3 `ἐμοῦ` (emou; English: of me) |  | 1: αμην | 2: αιμα;αμην; min=0 | `apocrypha_bridge_context` |
| 672 | `σιων` (Sion; English: Zion) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | 2: αμην;ελαμ |  | 1: βασαν; min=10 | `apocrypha_bridge_context` |
| 673 | `admah` | MAT 1:4 `Salmon;` |  | 1: heth | 3: earth;hail;heth; min=0 | `kjv_apocrypha_bridge_context` |
| 674 | `ahab` | MAT 1:1 `generation` | 3: gate;obal;star | 1: sheba | 6: heth;hits;horn;star;tomb; min=1 | `kjv_apocrypha_bridge_context` |
| 675 | `altar` | TOB 1:4 `country,` |  | 1: rent | 4: eber;rent;rome; min=0 | `kjv_apocrypha_bridge_context` |
| 676 | `aram` | MAT 1:4 `begat` |  | 1: adam | 3: aaron;sheba;tomb; min=7 | `kjv_apocrypha_bridge_context` |
| 677 | `bush` | 2ES 16:77 `a` |  |  | 9: hail;hand;hits;horn;house;mash;otho;resen; min=3 | `kjv_apocrypha_bridge_context` |
| 678 | `eden` | MAL 4:4 `judgments.` | 1: heth |  | 15: heart;heth;hits;king;seed;shem;sidon;soot;yhwh; min=2 | `kjv_apocrypha_bridge_context` |
| 679 | `ehyeh` | 2ES 16:76 `you` |  | 1: teeth | 2: sivan;teeth; min=5 | `kjv_apocrypha_bridge_context` |
| 680 | `elam` | TOB 1:2 `at` |  |  | 7: eden;hits;lane;life;rent;rome;water; min=1 | `kjv_apocrypha_bridge_context` |
| 681 | `eyes` | 2ES 16:77 `field` | 1: tomb | 1: soot | 3: bread;obed;soot; min=0 | `kjv_apocrypha_bridge_context` |
| 682 | `gate` | MAL 4:6 `children` |  |  | 9: heart;heth;holy;lane;leah;love;noah;ruth;torah; min=5 | `kjv_apocrypha_bridge_context` |
| 683 | `gate` | MAT 1:2 `his` |  | 1: torah | 6: heth;image;obal;seed; min=1 | `kjv_apocrypha_bridge_context` |
| 684 | `hail` | 2ES 16:78 `be` | 2: soot;thin | 2: lamb;thin | 7: ahab;annas;hits;lamb;lane;lion;thin; min=0 | `kjv_apocrypha_bridge_context` |
| 685 | `hand` | MAL 4:6 `their` | 1: seed | 3: hits;lane;wine | 7: ehyeh;hits;rent;teeth;torah; min=0 | `kjv_apocrypha_bridge_context` |
| 686 | `hand` | MAL 4:6 `lest` |  | 1: lane | 9: ahab;edom;lane;leah;life; min=1 | `kjv_apocrypha_bridge_context` |
| 688 | `hannah` | MAT 1:6 `Jesse` |  | 1: obal | 3: gate;horn;lane; min=2 | `kjv_apocrypha_bridge_context` |
| 689 | `hannah` | MAT 1:6 `Jesse` |  | 1: obal | 3: gate;horn;lane; min=2 | `kjv_apocrypha_bridge_context` |
| 690 | `hits` | MAL 4:6 `heart` | 3: lane;soot;torah | 2: heth;thin | 8: gate;heth;life;lord;love;noah;seed; min=0 | `kjv_apocrypha_bridge_context` |
| 691 | `hits` | MAL 4:6 `fathers` | 2: soot;wine | 2: ahab;sign | 9: death;fire;heart;leah;nato;rent;sign;tyre; min=0 | `kjv_apocrypha_bridge_context` |
| 692 | `house` | TOB 1:3 `justice,` | 1: hits | 1: noah | 8: eden;hits;holy;lane;noah;seed;sivan;thin; min=0 | `kjv_apocrypha_bridge_context` |
| 693 | `isaac` | MAT 1:2 `Judas` | 1: tomb | 2: star;water | 3: ahab;mash;obed; min=6 | `kjv_apocrypha_bridge_context` |
| 694 | `king` | MAL 4:5 `the` | 2: hail;yhwh | 1: sign | 7: eden;hits;seed;soot; min=2 | `kjv_apocrypha_bridge_context` |
| 695 | `lane` | MAL 4:6 `children,` |  | 5: hand;leah;rent;wine | 9: ahab;gate;nato;seed;shem;soot;torah;wine; min=1 | `kjv_apocrypha_bridge_context` |
| 696 | `lane` | MAL 4:6 `fathers,` | 2: seed;soot | 1: hand | 2: leah;lord; min=5 | `kjv_apocrypha_bridge_context` |
| 697 | `lane` | MAL 4:6 `heart` | 3: hits;soot;torah | 4: heal;heart;life;rent | 15: ahab;hail;hand;heart;hits;leah;life;seed;wine; min=0 | `kjv_apocrypha_bridge_context` |
| 698 | `lane` | MAL 4:6 `and` | 2: eden;seed | 2: leah;noah | 10: ahab;hand;leah;life;soot; min=0 | `kjv_apocrypha_bridge_context` |
| 699 | `lane` | MAT 1:2 `Isaac` | 2: horn |  | 11: ahab;annas;gate;hail;hannah;horn;lamb;lion;obed;thin; min=2 | `kjv_apocrypha_bridge_context` |
| 700 | `light` | TOB 1:2 `Galilee` | 1: tyre | 2: heart;life | 8: heth;hits;life;seed;soot;water;wine; min=0 | `kjv_apocrypha_bridge_context` |
| 701 | `lion` | 2ES 16:77 `may` | 1: fire | 2: otho;sivan | 8: annas;hail;horn;lamb;lane;obed;thin; min=2 | `kjv_apocrypha_bridge_context` |
| 702 | `love` | TOB 1:2 `of` | 1: holy | 2: noah;sivan | 11: ahab;gate;hail;heart;hits;life;lord;noah;seed;thin; min=1 | `kjv_apocrypha_bridge_context` |
| 703 | `obal` | MAT 1:3 `begat` | 1: seed | 3: ahab;hannah | 5: adam;gate;seed; min=1 | `kjv_apocrypha_bridge_context` |
| 704 | `rome` | TOB 1:2 `Nephthali` |  |  | 6: altar;eber;eden;lane;rent;tyre; min=6 | `kjv_apocrypha_bridge_context` |
| 705 | `rome` | TOB 1:2 `properly` | 2: eden;seed | 3: rent;sidon;torah | 5: death;eber;elam;life;rent; min=0 | `kjv_apocrypha_bridge_context` |
| 706 | `seed` | TOB 1:1 `the` | 7: ahab;fire;gate;life;rent;tyre | 3: dedan;hits;wine | 9: eden;hail;heth;hits;light;soot;star;water;wine; min=0 | `kjv_apocrypha_bridge_context` |
| 707 | `seed` | TOB 1:1 `tribe` |  | 1: hits | 9: gate;heart;heth;hits;light;soot;water;wine; min=0 | `kjv_apocrypha_bridge_context` |
| 708 | `seed` | TOB 1:1 `son` | 2: ahab;hand | 4: eden;hits;leah;soot | 14: eden;hail;hits;house;noah;sivan;soot;star;yhwh; min=0 | `kjv_apocrypha_bridge_context` |
| 709 | `seed` | TOB 1:1 `Tobiel,` |  | 1: sidon | 4: ehyeh;gate;hits;nato; min=2 | `kjv_apocrypha_bridge_context` |
| 710 | `seed` | TOB 1:1 `of` | 4: hits;nato;sign;soot | 2: eden;lord | 9: ahab;hits;life;lord;love;noah;sidon; min=0 | `kjv_apocrypha_bridge_context` |
| 711 | `seed` | TOB 1:2 `captive` | 1: hits | 1: hits | 7: eber;eden;hand;heth;hits;life;thin; min=0 | `kjv_apocrypha_bridge_context` |
| 712 | `seed` | TOB 1:2 `properly` | 2: eden;rome | 3: edom;life;wine | 3: eber;nato;sivan; min=3 | `kjv_apocrypha_bridge_context` |
| 713 | `soot` | MAL 4:6 `fathers,` | 2: lane;seed | 5: hits;holy;seed | 10: eden;hail;hits;seed;star;torah;yhwh; min=0 | `kjv_apocrypha_bridge_context` |
| 714 | `soot` | MAL 4:6 `fathers` | 2: hits;wine | 1: torah | 8: eden;haifa;heart;seed;shem;torah;wine; min=1 | `kjv_apocrypha_bridge_context` |
| 715 | `soot` | MAL 4:6 `heart` | 3: hits;lane;torah |  | 3: edom;lane;leah; min=5 | `kjv_apocrypha_bridge_context` |
| 716 | `star` | 2ES 16:77 `man` |  | 2: heth;hits | 5: ahab;heth;tomb; min=2 | `kjv_apocrypha_bridge_context` |
| 717 | `tomb` | 2ES 16:77 `field` | 1: eyes |  | 3: fire;obed;star; min=5 | `kjv_apocrypha_bridge_context` |
| 718 | `tyre` | TOB 1:2 `Galilee` | 1: light | 3: gate;wine;yhwh | 6: eber;noah;rent;rome;ruth;wine; min=0 | `kjv_apocrypha_bridge_context` |
| 743 | `αδαμ` (adam; English: Adam) | TOB 1:1 `Νεφθαλίμ,` (nephthalim; English: Naphtali) |  |  | 3: αιμα;ναοσ;σιων; min=7 | `apocrypha_bridge_context` |
| 744 | `αδαμ` (adam; English: Adam) | TOB 1:2 `Τωβὶτ` (tobit; English: Tobit) |  | 2: ελαμ;μαρια | 3: ελαμ;μαρια;σιων; min=0 | `apocrypha_bridge_context` |
| 745 | `αιμα` (haima; English: Blood) | TOB 1:1 `τοῦ` (tou; English: of the) |  |  | 2: αδαμ;αμην; min=5 | `apocrypha_bridge_context` |
| 746 | `αιμα` (haima; English: Blood) | TOB 1:2 `ὁδοῖς` (odois; English: ways) | 1: βασαν | 1: σιων |  | `apocrypha_bridge_context` |
| 747 | `αιμα` (haima; English: Blood) | TOB 1:2 `ᾐχμαλωτεύθη` (echmaloteuthe; English: was taken captive) |  |  | 2: σιων; min=1 | `apocrypha_bridge_context` |
| 748 | `αιμα` (haima; English: Blood) | TOB 1:2 `ἀληθείας` (aletheias; English: truth) |  |  | 2: αμην;αμμων; min=1 | `apocrypha_bridge_context` |
| 749 | `αιμα` (haima; English: Blood) | TOB 1:3 `τοῖς` (tois; English: to the) |  |  | 1: σιων; min=2 | `apocrypha_bridge_context` |
| 750 | `αιμα` (haima; English: Blood) | TOB 1:3 `τοῖς` (tois; English: to the) |  |  | 1: βασαν; min=7 | `apocrypha_bridge_context` |
| 752 | `αμην` (amen; English: Amen) | TOB 1:1 `Τωβιήλ,` (tobiel; English: Tobiel) | 1: ρωμη |  | 1: αιμα; min=5 | `apocrypha_bridge_context` |
| 753 | `αμην` (amen; English: Amen) | TOB 1:2 `ὑπεράνω` (uperano; English: above) |  | 2: αμμων;ελαμ | 2: αιμα;αμμων; min=0 | `apocrypha_bridge_context` |
| 754 | `βασαν` (basan; English: Bashan) | TOB 1:2 `ὁδοῖς` (odois; English: ways) | 1: αιμα |  | 2: αιμα;σιων; min=7 | `apocrypha_bridge_context` |
| 755 | `ελαμ` (Elam; English: Elam) | MAL 4:6 `δικαιώματα.` (dikaiomata; English: ordinances) | 2: αμην;σιων |  |  | `apocrypha_bridge_context` |
| 756 | `ελαμ` (Elam; English: Elam) | TOB 1:2 `βασιλέως` (basileos; English: king) | 1: σιων | 1: αμην | 1: θεοσ; min=9 | `apocrypha_bridge_context` |
| 757 | `ελαμ` (Elam; English: Elam) | TOB 1:2 `Ἐνεμεσσάρου` (enemessarou; English: Enemessar) |  | 2: αδαμ;μαρια | 3: αδαμ;θεοσ;μαρια; min=0 | `apocrypha_bridge_context` |
| 758 | `θεοσ` (theos; English: God) | MAL 4:4 `ἐπιφανῆ,` (epiphane; English: manifest/glorious) |  | 1: σιων | 2: σιων; min=0 | `apocrypha_bridge_context` |
| 759 | `θεοσ` (theos; English: God) | TOB 1:1 `Τωβίτ,` (tobit; English: Tobit) |  |  | 3: αμην;ελαμ; min=2 | `apocrypha_bridge_context` |
| 760 | `ναοσ` (naos; English: Temple) | TOB 1:2 `Θίσβης,` (thisbes; English: Thisbe) |  |  | 1: αδαμ; min=9 | `apocrypha_bridge_context` |
| 761 | `ρωμη` (rome; English: Rome) | TOB 1:1 `Τωβιήλ,` (tobiel; English: Tobiel) | 1: αμην |  | 1: σιων; min=5 | `apocrypha_bridge_context` |
| 763 | `σιων` (Sion; English: Zion) | MAL 4:5 `πρὸς` (pros; English: toward) |  |  | 1: θεοσ; min=8 | `apocrypha_bridge_context` |
| 764 | `σιων` (Sion; English: Zion) | MAL 4:5 `υἱὸν` (uion; English: son) |  | 1: θεοσ | 1: θεοσ; min=0 | `apocrypha_bridge_context` |
| 765 | `σιων` (Sion; English: Zion) | TOB 1:1 `Γαβαήλ,` (gabael; English: Gabael) |  |  | 2: αιμα;ρωμη; min=1 | `apocrypha_bridge_context` |
| 766 | `σιων` (Sion; English: Zion) | TOB 1:2 `ἐπορευόμην` (eporeuomen; English: I walked) |  | 1: αιμα | 2: αδαμ;αιμα; min=2 | `apocrypha_bridge_context` |
| 767 | `σιων` (Sion; English: Zion) | TOB 1:2 `βασιλέως` (basileos; English: king) | 1: ελαμ |  | 2: αδαμ;αιμα; min=3 | `apocrypha_bridge_context` |
| 768 | `aaron` | 2ES 16:78 `undressed,` | 1: obed | 1: sheba | 3: aram;sheba;tomb; min=0 | `kjv_apocrypha_bridge_context` |
| 769 | `aaron` | MAT 1:3 `Esrom` |  | 2: adam;horn | 6: adam;gate;heth;shoah;thin;wine; min=0 | `kjv_apocrypha_bridge_context` |
| 770 | `adam` | MAT 1:3 `Aram;` |  | 1: hail | 4: obal;seed; min=3 | `kjv_apocrypha_bridge_context` |
| 771 | `adam` | MAT 1:4 `Naasson;` |  | 2: aaron;aram | 4: aaron;heth;mash;thin; min=0 | `kjv_apocrypha_bridge_context` |
| 772 | `ahab` | 2ES 16:78 `consumed` |  | 2: horn;obal | 7: hail;hits;horn;isaac;lane;obed;thin; min=3 | `kjv_apocrypha_bridge_context` |
| ... | ... | ... | ... | ... | ... | 151 more cross-skip rows in CSV |

## Mapping-Dependent Rows

| Rank | Term | Center | Thematic first | Author scope | Protagonist scope | Source |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | `γωγ` (Gog; English: Gog) | REV 20:8=4 `Gog` | gog_revelation_g:Rev 20-20 |  |  | `gog_source_review` |
| 2 | `γωγ` (Gog; English: Gog) | Rev 20:8=4 `Gog` | gog_revelation_g:Rev 20-20 |  |  | `gog_source_review` |
| 3 | `γωγ` (Gog; English: Gog) | REV 20:8=4 `Gog` | gog_revelation_g:Rev 20-20 |  |  | `gog_source_review` |
| 4 | `γωγ` (Gog; English: Gog) | REV 20:8=2 `Gog` | gog_revelation_g:Rev 20-20 |  |  | `gog_source_review` |
| 22 | `γωγ` (Gog; English: Gog) | REV 20:8 `Γὼγ` (Gog; English: Gog) | gog_revelation_g:Rev 20-20 |  |  | `original_language_findings` |
| 98 | `jesus` | MAT 4:10 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 99 | `jesus` | MRK 10:5 `Jesus` |  |  | jesus_mark_e:Jesus Mark 1:1-Mark 16:20 | `strong_full_span_exact_center` |
| 100 | `γωγ` (Gog; English: Gog) | REV 20:8 `Γὼγ` (Gog; English: Gog) | gog_revelation_g:Rev 20-20 |  |  | `strong_full_span_exact_center` |
| 102 | `jesus` | JHN 12:21 `Jesus.` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 103 | `jesus` | JHN 21:20 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 104 | `jesus` | LUK 17:17 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 105 | `jesus` | LUK 9:42 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 106 | `jesus` | MAT 12:15 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 107 | `jesus` | MAT 18:1 `Jesus,` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 108 | `jesus` | MAT 20:22 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 109 | `jesus` | MAT 20:25 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 110 | `jesus` | MAT 21:24 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 111 | `jesus` | MAT 26:17 `Jesus,` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 112 | `jesus` | MAT 2:1 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 113 | `jesus` | MAT 3:13 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 114 | `jesus` | MAT 8:34 `Jesus:` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 115 | `jesus` | MRK 10:23 `Jesus` |  |  | jesus_mark_e:Jesus Mark 1:1-Mark 16:20 | `strong_full_span_exact_center` |
| 116 | `jesus` | MRK 5:27 `Jesus,` |  |  | jesus_mark_e:Jesus Mark 1:1-Mark 16:20 | `strong_full_span_exact_center` |
| 130 | `jesus` | JHN 12:11 `Jesus.` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 131 | `jesus` | JHN 12:35 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 132 | `jesus` | JHN 18:7 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 133 | `jesus` | JHN 18:8 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 134 | `jesus` | JHN 19:28 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 135 | `jesus` | JHN 19:38 `Jesus,` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 136 | `jesus` | JHN 19:40 `Jesus,` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 137 | `jesus` | JHN 20:12 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 138 | `jesus` | JHN 20:26 `Jesus,` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 139 | `jesus` | JHN 21:1 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 140 | `jesus` | JHN 21:5 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 141 | `jesus` | JHN 2:13 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 142 | `jesus` | JHN 3:10 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 143 | `jesus` | JHN 4:2 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 144 | `jesus` | JHN 4:44 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 145 | `jesus` | JHN 4:7 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 146 | `jesus` | JHN 6:24 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 147 | `jesus` | JHN 6:61 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 148 | `jesus` | JHN 7:50 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 149 | `jesus` | JHN 7:6 `Jesus` |  |  | jesus_john_e:Jesus John 1:1-John 21:25 | `strong_full_span_exact_center` |
| 150 | `jesus` | LUK 18:19 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 151 | `jesus` | LUK 18:40 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 152 | `jesus` | LUK 19:1 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 153 | `jesus` | LUK 19:3 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 154 | `jesus` | LUK 19:9 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 155 | `jesus` | LUK 23:52 `Jesus.` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 156 | `jesus` | LUK 24:15 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 157 | `jesus` | LUK 4:8 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 158 | `jesus` | LUK 5:10 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 159 | `jesus` | LUK 6:11 `Jesus.` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 160 | `jesus` | LUK 8:50 `Jesus` |  |  | jesus_luke_e:Jesus Luke 1:1-Luke 24:53 | `strong_full_span_exact_center` |
| 161 | `jesus` | MAT 10:5 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 162 | `jesus` | MAT 13:1 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 163 | `jesus` | MAT 13:53 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 164 | `jesus` | MAT 14:16 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 165 | `jesus` | MAT 15:1 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 166 | `jesus` | MAT 15:32 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 167 | `jesus` | MAT 16:21 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 168 | `jesus` | MAT 16:8 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 169 | `jesus` | MAT 17:11 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 170 | `jesus` | MAT 18:22 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 171 | `jesus` | MAT 19:28 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 172 | `jesus` | MAT 21:16 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 173 | `jesus` | MAT 21:31 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 174 | `jesus` | MAT 24:1 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 175 | `jesus` | MAT 26:55 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 176 | `jesus` | MAT 26:57 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 177 | `jesus` | MAT 26:71 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 178 | `jesus` | MAT 26:75 `Jesus,` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 179 | `jesus` | MAT 27:46 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 180 | `jesus` | MAT 28:9 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 181 | `jesus` | MAT 8:18 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 182 | `jesus` | MAT 8:20 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 183 | `jesus` | MAT 8:4 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 184 | `jesus` | MAT 9:10 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 185 | `jesus` | MAT 9:15 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| 186 | `jesus` | MAT 9:19 `Jesus` |  |  | jesus_matthew_e:Jesus Matt 1:1-Matt 28:20 | `strong_full_span_exact_center` |
| ... | ... | ... | ... | ... | ... | 231 more mapping rows in CSV |

## Meaningful Skip Rows

| Rank | Term | Center | Skip | Constant match | Term gematria match | Center-word gematria match | Source |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 2 | `γωγ` (Gog; English: Gog) | Rev 20:8=4 `Gog` | -7;7;-4423;4423 | 7: Sabbath / completeness |  |  | `gog_source_review` |
| 626 | `παισ` (pais; English: Servant) | Luke 22:64 `παίσας` (paisas) | -7 | 7: Sabbath / completeness |  |  | `all_codes_followup` |
| 636 | `תורה` (twrh; English: Torah) | 1Chr 5:1 `בֶּן־יִשְׂרָאֵ֑ל` (bnyshrl) | 7 | 7: Sabbath / completeness |  |  | `all_codes_followup` |
| 637 | `תורה` (twrh; English: Torah) | 2Kgs 17:20 `יִשְׂרָאֵל֙` (Yisrael; English: Israel) | -7 | 7: Sabbath / completeness |  |  | `all_codes_followup` |
| 685 | `hand` | MAL 4:6 `their` | 40 | 40: Wilderness / testing |  |  | `kjv_apocrypha_bridge_context` |
| 720 | `התשח` (htshch; English: Hebrew year 5708) | Lev 22:27 `וָהָ֔לְאָה` (whlh) | 40 | 40: Wilderness / testing |  |  | `all_codes_followup` |
| 735 | `νατο` (nato; English: NATO) | 1Cor 1:27 `μωρὰ` (mora; English: foolish things) | 7 | 7: Sabbath / completeness |  |  | `all_codes_followup` |
| 795 | `gate` | MAL 4:5 `great` | -144 | 144: Revelation square of twelve |  |  | `kjv_apocrypha_bridge_context` |
| 829 | `hits` | MAL 4:5 `before` | 144 | 144: Revelation square of twelve |  |  | `kjv_apocrypha_bridge_context` |
| 896 | `soot` | TOB 1:1 `of` | -70 | 70: Nations / exile years |  |  | `kjv_apocrypha_bridge_context` |

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
- Center-position strata use the center verse reference, not ELS path endpoints.
- `cross_skip_pair_at_word` means at least one other normalized term shares the same center word/reference in the indexed family at a different skip.
- `cross_skip_pair_at_letter` means two different terms at different skips share at least one retained letter-path position.
- `cross_skip_pair_within_N_letters` means two different terms at different skips have endpoints within the configured letter distance.
- `canonical_first_in_thematic_chapter`, `author_in_own_book`, and `protagonist_in_own_narrative` are locked-mapping annotations only; empty or nonmatching mapping entries do not flag rows.
- Meaningful-skip and gematria-skip strata are metadata flags; they do not change the search space or promote claim status.
- Bigram-surprise strata are corpus-local review aids, not claim promotion rules; missing adjacent surface bigrams count as rare.
- Letter-frequency anomaly strata are corpus-local review aids; missing letters count as rare.
- Matrix, cipher, broader cross-skip, and cohort-density strata widen the review surface and need separate locked controls before claim language.

