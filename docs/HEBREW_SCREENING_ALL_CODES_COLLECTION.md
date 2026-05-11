# Hebrew Screening All-Codes Collection

This report intentionally keeps every hidden-path ELS row from the surface-context collection and then flags same-word, related-center, center-verse, and span context. It is a collection index, not a claim-grade filter.

## Inputs

- Hits: `reports/hebrew_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/hebrew_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `not used`
- Corpora: `EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC`

## Collection Counts

| Metric | Count |
| --- | ---: |
| Terms represented | 726 |
| Corpus-term summary rows | 3,830 |
| Hidden-path rows retained | 3,680,528 |
| Total hits from summary | 3,680,528 |
| Any surface-context hits | 1,828,415 |
| Center word contains same term | 9,266 |
| Center word contains related term | 111,654 |
| Center verse contains same term | 119,153 |
| Center verse contains related term | 1,018,957 |
| Hit span contains same/related term | 1,986,939 |

## Context Labels

| Best context | Rows |
| --- | ---: |
| `hidden_path_only` | 1,852,113 |
| `same_category_center` | 953,242 |
| `same_category_span` | 677,798 |
| `exact_center` | 119,153 |
| `exact_span` | 76,629 |
| `same_concept_span` | 878 |
| `same_concept_center` | 715 |

## Top Terms

| Term | Concept | Hidden hits | Center word same | Center word related | Center verse same | Center verse related | Span context |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `יהוה` (YHWH; English: YHWH) | YHWH | 216,640 | 6,658 | 12,875 | 83,838 | 98,141 | 283,038 |
| `מרימ` (mrym; English: Mary) | Mary | 108,806 | 102 | 2,257 | 1,414 | 24,667 | 52,512 |
| `יואל` (ywl; English: Joel) | Joel | 85,440 | 1 | 424 | 901 | 4,518 | 14,505 |
| `נביא` (navi; English: Prophet) | Prophet | 83,913 | 153 | 1,624 | 1,662 | 17,441 | 43,302 |
| `אהיה` (hyh; English: Ehyeh) | Ehyeh | 83,036 | 42 | 9,277 | 914 | 66,070 | 83,188 |
| `אהבה` (hbh; English: Love) | Love | 79,150 | 20 | 1,123 | 314 | 11,890 | 24,029 |
| `שלומ` (shlwm; English: Peace) | Peace | 75,338 | 180 | 985 | 1,462 | 11,138 | 25,125 |
| `אייר` (yyr; English: Iyyar) | Iyyar | 72,657 | 0 | 1,471 | 35 | 17,865 | 39,974 |
| `רומי` (rwmy; English: Rome) | Rome | 69,341 | 6 | 1,645 | 217 | 16,567 | 38,090 |
| `ראוי` (rwy; English: Worthy) | Worthy | 68,787 | 0 | 207 | 90 | 3,372 | 10,170 |
| `עילמ` (ylm; English: Elam) | Elam | 62,028 | 0 | 3,315 | 140 | 27,741 | 44,938 |
| `אותו` (wtw; English: Otho) | Otho | 58,270 | 16 | 0 | 670 | 10 | 1,803 |
| `יובל` (ywbl; English: Jubilee) | Jubilee | 58,070 | 14 | 174 | 123 | 2,246 | 6,459 |
| `אלול` (lwl; English: Elul) | Elul | 57,414 | 8 | 1,146 | 274 | 14,415 | 32,520 |
| `יונה` (ywnh; English: Jonah) | Jonah | 56,927 | 10 | 248 | 331 | 3,404 | 9,581 |
| `אריה` (ryh; English: Lion) | Lion | 52,033 | 0 | 2,654 | 146 | 26,544 | 44,300 |
| `אמרי` (mry; English: Amorite) | Amorite | 49,829 | 54 | 4,363 | 3,731 | 34,827 | 55,743 |
| `ביבי` (byby; English: Bibi) | Bibi | 49,308 | 0 | 11 | 249 | 270 | 1,460 |
| `רומא` (rwm; English: Rome) | Rome | 47,072 | 0 | 1,028 | 42 | 11,161 | 24,976 |
| `שמימ` (shmym; English: Heaven) | Heaven | 46,923 | 121 | 81 | 1,361 | 1,045 | 6,217 |
| `יובב` (ywbb; English: Jobab) | Jobab | 46,688 | 0 | 3,831 | 127 | 31,266 | 43,752 |
| `תהומ` (thwm; English: Abyss) | Abyss | 46,075 | 10 | 2,219 | 75 | 23,746 | 39,993 |
| `מואב` (mwb; English: Moab) | Moab | 44,467 | 32 | 886 | 645 | 9,681 | 23,996 |
| `שואה` (shwh; English: Shoah) | Shoah | 41,491 | 0 | 95 | 4 | 1,240 | 3,758 |
| `שאול` (shwl; English: Sheol) | Sheol | 37,020 | 137 | 62 | 1,420 | 728 | 4,997 |
| `שאול` (shwl; English: Paul) | Paul | 37,020 | 137 | 416 | 1,420 | 5,470 | 13,951 |
| `מיכה` (mykh; English: Micah) | Micah | 36,642 | 6 | 104 | 119 | 1,990 | 5,354 |
| `הוכה` (hwkh; English: Beaten) | Beaten | 36,228 | 0 | 91 | 65 | 1,681 | 5,203 |
| `שממה` (shemamah; English: Desolation) | Desolation | 34,908 | 22 | 2,038 | 140 | 20,643 | 31,545 |
| `מהרל` (mhrl; English: Maharal) | Maharal | 34,750 | 0 | 0 | 0 | 130 | 344 |

## Read

This output is deliberately broad. Hidden-path-only rows are retained for
inspection. Same-center-word rows are a narrower subset. Same-concept and
same-category center-word rows are related-surface prompts, not automatic
interpretations. Claim-grade filtering still belongs in the controlled
reports.
