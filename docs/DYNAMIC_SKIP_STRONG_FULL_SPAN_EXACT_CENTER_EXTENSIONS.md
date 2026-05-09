# Strong Full-Span Exact-Center Extensions

This report checks same-skip letters immediately before and after the
exact-center paths. It asks whether an exact-centered hidden term
can extend into a surface word or short phrase from the same corpus.

## Reproduce

```bash
python3 -m scripts.build_dynamic_span_exact_center_extension_hits ... # build hit-compatible exact-center input
python3 -m els extensions ... # one run per corpus in the input directory
python3 -m els extension-summary ... # one summary per corpus with --match-kind-prefix phrase_
python3 -m scripts.build_dynamic_span_exact_center_extensions_report --input-dir reports/dynamic_skip_focus/exact_center_extensions --markdown-out docs/DYNAMIC_SKIP_STRONG_FULL_SPAN_EXACT_CENTER_EXTENSIONS.md --manifest-out reports/dynamic_skip_focus/exact_center_extensions/report.manifest.json --title 'Strong Full-Span Exact-Center Extensions' --top 25 --summary-row-limit 0
```

## Scope

- exact-center paths scanned for extensions: 1,582
- raw same-skip extension rows: 2,093
- phrase-filtered summary groups: 38
- strong phrase-extension rows: 5
- input directory: `reports/dynamic_skip_focus/exact_center_extensions`

## Corpus Counts

| Corpus | Exact-center paths | Raw extension rows | Phrase summary groups | Strong phrase rows |
| --- | ---: | ---: | ---: | ---: |
| EBIBLE_WLC | 75 | 92 | 1 | 0 |
| KJV | 492 | 698 | 26 | 5 |
| LXX | 70 | 176 | 5 | 0 |
| TCG_NT | 4 | 4 | 1 | 0 |
| UHB | 941 | 1,123 | 5 | 0 |

## Strong Phrase Rows

| Corpus | Term | Center | Extension | Match kind | Match count | Matched examples |
| --- | --- | --- | --- | --- | ---: | --- |
| KJV | `jesus` | ACT 9:29 | `jesusand` (term_plus_after) | phrase_2 | 44 | Jesus: and; Jesus, and; Jesus and; Jesus, And; Jesus. And |
| KJV | `jesus` | MAT 2:1 | `jesusthe` (term_plus_after) | phrase_2 | 13 | Jesus the; JESUS THE; Jesus, the; Jesus. The |
| KJV | `jesus` | 2CO 1:14 | `forjesus` (before_plus_term) | phrase_2 | 9 | For Jesus; for Jesus; for Jesus.; for Jesus,; for Jesus’ |
| KJV | `jesus` | JHN 19:40 | `jesusyet` (term_plus_after) | phrase_2 | 1 | Jesus yet |
| KJV | `jesus` | PHP 2:5 | `jesusout` (term_plus_after) | phrase_2 | 1 | Jesus out |

## Phrase Summary Rows

| Corpus | Term | Skip | Direction | Type | Match kind | Rows | Max length | Max match count |
| --- | --- | ---: | --- | --- | --- | ---: | ---: | ---: |
| EBIBLE_WLC | `משיח` | -10396 | backward | before_match | phrase_2 | 1 | 5 | 3 |
| KJV | `jesus` | -164165 | backward | term_plus_after | phrase_2 | 1 | 3 | 1 |
| KJV | `jesus` | -136692 | backward | after_match | phrase_2 | 1 | 4 | 15 |
| KJV | `jesus` | -136692 | backward | after_match | phrase_2+word | 1 | 3 | 70 |
| KJV | `jesus` | -132550 | backward | term_plus_after | phrase_2 | 1 | 3 | 13 |
| KJV | `jesus` | -109854 | backward | after_match | phrase_2 | 1 | 5 | 8 |
| KJV | `jesus` | -95343 | backward | after_match | phrase_2 | 1 | 3 | 63 |
| KJV | `jesus` | -95343 | backward | after_match | phrase_3 | 1 | 4 | 4 |
| KJV | `jesus` | -49304 | backward | term_plus_after | phrase_2 | 1 | 3 | 1 |
| KJV | `jesus` | -31651 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| KJV | `jesus` | -25740 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| KJV | `jesus` | -4934 | backward | before_match | phrase_2 | 1 | 3 | 1 |
| KJV | `jesus` | -3121 | backward | after_match | phrase_2 | 1 | 4 | 3 |
| KJV | `jesus` | -1685 | backward | before_match | phrase_2 | 1 | 4 | 7 |
| KJV | `jesus` | 2459 | forward | after_match | phrase_2+word | 1 | 3 | 5 |
| KJV | `jesus` | 5033 | forward | after_match | phrase_2 | 1 | 3 | 30 |
| KJV | `jesus` | 14590 | forward | after_match | phrase_2 | 1 | 3 | 36 |
| KJV | `jesus` | 19047 | forward | before_match | phrase_2 | 1 | 5 | 3 |
| KJV | `jesus` | 35303 | forward | after_match | phrase_2 | 1 | 5 | 3 |
| KJV | `jesus` | 35303 | forward | term_plus_after | phrase_2 | 1 | 3 | 44 |
| KJV | `jesus` | 39560 | forward | before_match | phrase_2 | 1 | 3 | 41 |
| KJV | `jesus` | 85029 | forward | before_match | phrase_2 | 1 | 3 | 18 |
| KJV | `jesus` | 98457 | forward | before_plus_term | phrase_2 | 1 | 3 | 9 |
| KJV | `jesus` | 102698 | forward | after_match | phrase_2 | 1 | 3 | 454 |
| KJV | `jesus` | 224928 | forward | before_match | phrase_2 | 1 | 4 | 1 |
| KJV | `jesus` | 305395 | forward | before_match | phrase_2 | 1 | 3 | 37 |
| KJV | `jesus` | 334349 | forward | before_match | phrase_2+word | 1 | 4 | 38 |
| LXX | `ιησουσ` | -234932 | backward | before_match | phrase_2 | 1 | 4 | 4 |
| LXX | `ιησουσ` | -53401 | backward | after_match | phrase_2 | 1 | 4 | 1 |
| LXX | `ιησουσ` | 38593 | forward | before_match | phrase_2 | 1 | 3 | 2 |
| LXX | `ιησουσ` | 119233 | forward | after_match | phrase_2 | 1 | 4 | 1 |
| LXX | `ιησουσ` | 201469 | forward | after_match | phrase_2 | 1 | 4 | 9 |
| TCG_NT | `γωγ` | -4568 | backward | after_match | phrase_2 | 1 | 3 | 56 |
| UHB | `ישוע` | -81473 | backward | after_match | phrase_2 | 1 | 6 | 1 |
| UHB | `ישוע` | -40029 | backward | before_match | phrase_2 | 1 | 4 | 1 |
| UHB | `ישוע` | -26675 | backward | after_match | phrase_2 | 1 | 5 | 1 |
| UHB | `ישוע` | -11422 | backward | after_match | phrase_2+word | 2 | 5 | 7 |
| UHB | `ישוע` | 98746 | forward | before_match | phrase_2+word | 1 | 5 | 4 |

## Read

- `Strong phrase rows` require the hidden term plus adjacent same-skip letters to match a surface phrase.
- `Phrase summary rows` also include before-only or after-only phrase matches, which are weaker.
- Strong phrase-extension rows remain post-screen review material; compare Bible and control reports before treating a row as notable.
- This remains post-screen review material; matched phrases can occur elsewhere in the corpus and need manual context checks.
