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
- Hebrew OSHB slash-marked prefixes are reduced to the final lexical segment, e.g. `וַ/יֹּאמֶר` (vayyomer; English: and he said) counts as `יאמר` (yomer/amar-form; English: he said).
- Multiples checked: 3, 7, 12, 40, 70.
- Critical-text break test compares TR NT full counts vs TR NT with deleted SBLGNT-missing verse blocks removed.

Limits:

- This surface-word report is still intentionally separate from lemma/POS reporting.
- Greek inflected forms remain separate here, e.g. `θεος` (theos; English: God), `θεου` (theou; English: of God), `κυριος` (kyrios; English: Lord), and `κυριου` (kyriou; English: of Lord).
- Hebrew OSHB slash-segment reduction is a surface normalization, not a root/lemma analysis.
- POS filtering here is approximate stopword filtering, not true noun/verb/adjective tagging.
- Full lemma/POS counts now live in `MORPHOLOGY_COUNTS_STUDY.md` for OSHB MT and MorphGNT SBLGNT.

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
| MT WLC | `יהוה` (YHWH; English: divine name) 5,558; `יאמר` (yomer/amar-form; English: he said) 2,120; `מלכ` (melekh-root; English: king/kingdom root) 1,853; `ארצ` (eretz-root; English: land/earth root) 1,851; `ישראל` (Yisrael; English: Israel) 1,796 |
| LXX | `κυριοσ` (kyrios; English: Lord) 3,391; `ισραηλ` (Israel; English: Israel) 2,463; `ειπεν` (eipen; English: he said) 2,309; `κυριου` (kyriou; English: of Lord) 2,158; `θεοσ` (theos; English: God) 1,505 |
| TR NT | `θεου` (theou; English: of God) 706; `ειπεν` (eipen; English: he said) 643; `ιησουσ` (Iesous; English: Jesus/Joshua) 503; `ιησου` (Iesou; English: of Jesus/Joshua) 338; `λεγει` (legei; English: he says) 337 |
| SBLGNT | `θεου` (theou; English: of God) 687; `ειπεν` (eipen; English: he said) 612; `ιησουσ` (Iesous; English: Jesus/Joshua) 461; `λεγει` (legei; English: he says) 336; `ιησου` (Iesou; English: of Jesus/Joshua) 322 |

Notable Multiples:

- MT WLC `יהוה` (YHWH; English: divine name): 5,558 = multiple of 7.
- MT WLC `יאמר` (yomer/amar-form; English: he said): 2,120 = multiple of 40.
- LXX `θεοσ` (theos; English: God): 1,505 = multiple of 7.
- TR NT `χριστου` (Christou; English: of Christ): 270 = multiple of 3.
- SBLGNT `λεγει` (legei; English: he says): 336 = multiple of 3, 7, and 12.

Critical-Text Multiple Breaks:

- Rows with multiple state changed after removing deleted TR blocks: 92.
- Rows where a previous multiple was broken: 59.
- Rows where a new multiple was created: 46.

Examples:

| Word | Full TR count | TR minus deleted | Deleted | Broken | Created |
| --- | ---: | ---: | ---: | --- | --- |
| `σβεννυται` (sbennytai; English: is quenched) | 3 | 1 | 2 | 3 | |
| `σκωληξ` (skolex; English: worm) | 3 | 1 | 2 | 3 | |
| `τελευτα` (teleuta; English: ends/dies) | 3 | 1 | 2 | 3 | |
| `χριστου` (Christou; English: of Christ) | 270 | 268 | 2 | 3 | |
| `αγγελοσ` (angelos; English: angel/messenger) | 57 | 56 | 1 | 3 | 7 |

Related Lemma/POS Reports:

- Run `python3 -m scripts.analyze_morphology_counts` for morphology counts.
- Outputs include `reports/morph_counts_by_lemma.csv`, `reports/morph_counts_by_book.csv`, `reports/morph_counts_by_chapter.csv`, `reports/morph_counts_by_verse.csv`, and `reports/morph_count_multiples.csv`.
- Current morphology coverage is OSHB MT and MorphGNT SBLGNT; TR NT morphology is not available in this repo yet.
- MT lemma labels are OSHB/Strong-style IDs rather than Hebrew dictionary headwords.
