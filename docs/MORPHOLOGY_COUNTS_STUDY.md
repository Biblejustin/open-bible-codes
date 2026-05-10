# Morphology Counts Study

Goal:

- Count nouns, verbs, and adjectives by lemma.
- Export totals, book counts, chapter counts, and verse counts.
- Flag multiples of 3, 7, 12, 40, and 70.

Sources:

- MT WLC morphology: OSHB XML in `data/raw/oshb/wlc`.
- Greek NT morphology: MorphGNT SBLGNT in `data/raw/morphgnt/sblgnt`.

Commands:

```bash
python3 -m scripts.download_oshb_wlc
python3 -m scripts.download_morphgnt_sblgnt
python3 -m scripts.analyze_morphology_counts
```

Outputs:

- `reports/morph_counts_by_lemma.csv`
- `reports/morph_counts_by_book.csv`
- `reports/morph_counts_by_chapter.csv`
- `reports/morph_counts_by_verse.csv`
- `reports/morph_count_multiples.csv`
- `reports/morph_counts.manifest.json`

Results:

| Corpus | Token rows | Content tokens | Lemma/POS rows |
| --- | ---: | ---: | ---: |
| MT WLC morphology | 306,785 | 201,177 | 8,648 |
| SBLGNT MorphGNT | 137,554 | 65,420 | 5,047 |

Top MT WLC Lemmas:

- noun `3068`, surface `יְהוָ֖ה` (YHWH; English: divine name): 6,521.
- verb `559`, surface `וַ/יֹּ֣אמֶר` (vayyomer; English: and he said): 5,272.
- noun `3605`, surface `כָּל` (kol; English: all/every): 5,200; multiple of 40.
- noun `1121`, surface `בֶּן` (ben; English: son): 4,010.
- verb `1961`, surface `וַ/יְהִ֣י` (vayehi; English: and it was): 3,543; multiple of 3.

Top SBLGNT Lemmas:

- verb `εἰμί` (eimi; English: to be): 2,456.
- verb `λέγω` (lego; English: to say): 2,345; multiple of 7.
- noun `θεός` (theos; English: God): 1,307.
- adjective `πᾶς` (pas; English: all/every): 1,244.
- noun `Ἰησοῦς` (Iesous; English: Jesus/Joshua): 906; multiple of 3.
- noun `Χριστός` (Christos; English: Christ): 528; multiple of 3 and 12.

Limits:

- MT lemma labels are OSHB/Strong-style IDs, not Hebrew dictionary headwords.
- TR NT morphology is not available yet in this repo.
- MorphGNT tracks SBLGNT, not TR.
