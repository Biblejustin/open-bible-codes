# Word Counts Study

Goal:

- Count content words by corpus.
- Export counts total, by book, by chapter, and by verse.
- Flag counts that are multiples of 3, 7, 12, 40, or 70.
- Test whether TR verse blocks absent from SBLGNT break count-multiple patterns.

Command:

```bash
python3 -m scripts.analyze_word_counts
```

Outputs:

- `reports/word_counts_by_word.csv`
- `reports/word_counts_by_book.csv`
- `reports/word_counts_by_chapter.csv`
- `reports/word_counts_by_verse.csv`
- `reports/word_count_multiples.csv`
- `reports/critical_word_multiples_breaks.csv`
- `reports/word_counts.manifest.json`

Method:

- Counts normalized surface words.
- Filters common stopwords: articles, conjunctions, prepositions, common pronouns, and other function words.
- Hebrew OSHB slash-marked prefixes are reduced to the final lexical segment, e.g. `וַ/יֹּאמֶר` counts as `יאמר`.
- Multiples checked: 3, 7, 12, 40, 70.
- Critical-text break test compares TR NT full counts vs TR NT with deleted SBLGNT-missing verse blocks removed.

Limits:

- This is not full lemmatization yet.
- Greek inflected forms remain separate, e.g. `θεος`, `θεου`, `κυριος`, `κυριου`.
- Hebrew roots/lemmas are not resolved yet.
- POS filtering is approximate stopword filtering, not true noun/verb/adjective tagging.

Corpus Summary:

| Corpus | Content word types | Content word tokens |
| --- | ---: | ---: |
| MT WLC | 26,113 | 197,923 |
| LXX | 33,979 | 245,864 |
| TR NT | 17,134 | 72,479 |
| SBLGNT | 17,257 | 71,342 |

Top Total Counts:

| Corpus | Top terms |
| --- | --- |
| MT WLC | `יהוה` 5,558; `יאמר` 2,120; `מלכ` 1,853; `ארצ` 1,851; `ישראל` 1,796 |
| LXX | `κυριοσ` 3,391; `ισραηλ` 2,463; `ειπεν` 2,309; `κυριου` 2,158; `θεοσ` 1,505 |
| TR NT | `θεου` 706; `ειπεν` 643; `ιησουσ` 503; `ιησου` 338; `λεγει` 337 |
| SBLGNT | `θεου` 687; `ειπεν` 612; `ιησουσ` 461; `λεγει` 336; `ιησου` 322 |

Notable Multiples:

- MT WLC `יהוה`: 5,558 = multiple of 7.
- MT WLC `יאמר`: 2,120 = multiple of 40.
- LXX `θεοσ`: 1,505 = multiple of 7.
- TR NT `χριστου`: 270 = multiple of 3.
- SBLGNT `λεγει`: 336 = multiple of 3, 7, and 12.

Critical-Text Multiple Breaks:

- Rows with multiple state changed after removing deleted TR blocks: 92.
- Rows where a previous multiple was broken: 59.
- Rows where a new multiple was created: 46.

Examples:

| Word | Full TR count | TR minus deleted | Deleted | Broken | Created |
| --- | ---: | ---: | ---: | --- | --- |
| `σβεννυται` | 3 | 1 | 2 | 3 | |
| `σκωληξ` | 3 | 1 | 2 | 3 | |
| `τελευτα` | 3 | 1 | 2 | 3 | |
| `χριστου` | 270 | 268 | 2 | 3 | |
| `αγγελοσ` | 57 | 56 | 1 | 3 | 7 |

Next Improvements:

- Add Greek lemma/POS data, likely MorphGNT or another open morphology source.
- Add Hebrew lemma/POS from OSHB morphology instead of only slash-segment normalization.
- Add per-lemma count reports beside surface-form reports.
