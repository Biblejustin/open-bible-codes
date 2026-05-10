# Hebrew Screening All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/hebrew_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/hebrew_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Queue CSV: `reports/hebrew_screening_all_codes/triage_queue.csv`
- Corpora: `EBIBLE_WLC, MAM, MT_WLC, UHB, UXLC`

## Counts

| Metric | Count |
| --- | ---: |
| Raw rows scanned | 3,196,917 |
| Queue rows | 875 |
| `center_word_exact` queue rows | 100 |
| `center_word_same_concept` queue rows | 3 |
| `center_word_same_category` queue rows | 100 |
| `center_verse_exact` queue rows | 100 |
| `center_verse_same_concept` queue rows | 72 |
| `center_verse_same_category` queue rows | 100 |
| `span_exact` queue rows | 100 |
| `span_same_concept` queue rows | 100 |
| `span_same_category` queue rows | 100 |
| `hidden_path_only` queue rows | 100 |

## Top Queue Rows

### center_word_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `desolation_h` | Desolation | 2 | 7 | Mic 1:7 | `שממה` | not_unusual |
| 2 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` | not_unusual |
| 3 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` | not_unusual |
| 4 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` | not_unusual |
| 5 | all_source | `solomon_h` | Solomon | -3 | 10 | 1Kgs 7:1 | `שלמה` | not_unusual |
| 6 | all_source | `lord_h` | Lord | 3 | 10 | 1Sam 25:14 | `אדנינו` | not_unusual |
| 7 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` | not_unusual |
| 8 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` | not_unusual |
| 9 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` | not_unusual |
| 10 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Sam 26:9 | `יהוה` | not_unusual |
| 11 | all_source | `angel_h` | Angel | -3 | 10 | 1Sam 29:9 | `כמלאכ` | not_unusual |
| 12 | all_source | `yhwh_h` | YHWH | -3 | 10 | 2Chr 21:7 | `יהוה` | not_unusual |
| 13 | all_source | `yhwh_h` | YHWH | 3 | 10 | 2Chr 33:15 | `יהוה` | not_unusual |
| 14 | all_source | `yhwh_h` | YHWH | 3 | 10 | 2Chr 9:4 | `יהוה` | not_unusual |
| 15 | all_source | `lord_h` | Lord | -3 | 10 | 2Kgs 18:27 | `אדני` | not_unusual |
| 16 | all_source | `solomon_h` | Solomon | -3 | 10 | 2Kgs 23:13 | `שלמה` | not_unusual |
| 17 | all_source | `yhwh_h` | YHWH | 3 | 10 | 2Kgs 23:24 | `יהוה` | not_unusual |
| 18 | all_source | `solomon_h` | Solomon | -3 | 10 | 2Kgs 24:13 | `שלמה` | not_unusual |
| 19 | all_source | `yhwh_h` | YHWH | 3 | 10 | 2Kgs 25:13 | `ביתיהוה` | not_unusual |
| 20 | all_source | `yhwh_h` | YHWH | -3 | 10 | 2Kgs 8:19 | `יהוה` | not_unusual |

### center_word_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `rome_alt_h` | Rome | 5 | 16 | Job 5:12 | `ערומימ` | not_unusual |
| 2 | all_source | `rome_alt_h` | Rome | -42 | 127 | Eccl 10:6 | `במרומימ` | not_unusual |
| 3 | multi_source | `rome_alt_h` | Rome | 7 | 22 | 1Chr 11:33 | `הבחרומי` | not_unusual |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `germany_h` | Germany | -18 | 91 | Jer 42:15 | `מצרימ` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `amorite_h` | Amorite | -2 | 7 | 1Chr 15:22 | `במשא` | not_unusual |
| 3 | all_source | `amorite_h` | Amorite | 2 | 7 | 1Chr 15:27 | `המשררימ` | not_unusual |
| 4 | all_source | `asshur_h` | Asshur | 2 | 7 | 1Chr 7:23 | `שמו` | not_unusual |
| 5 | all_source | `shinar_h` | Shinar | 2 | 7 | 1Chr 8:22 | `ועבר` | not_unusual |
| 6 | all_source | `locust_h` | Locust | 2 | 7 | 1Kgs 12:12 | `דבר` | not_unusual |
| 7 | all_source | `locust_plague_h` | Locust Plague | 2 | 7 | 1Kgs 12:12 | `דבר` | not_unusual |
| 8 | all_source | `locusts_plague_h` | Locusts | 2 | 7 | 1Kgs 12:12 | `דבר` | not_unusual |
| 9 | all_source | `shinar_h` | Shinar | 2 | 7 | 1Kgs 15:1 | `שמנה` | not_unusual |
| 10 | all_source | `asshur_h` | Asshur | -2 | 7 | 1Kgs 18:25 | `בשמ` | not_unusual |
| 11 | all_source | `shinar_h` | Shinar | 2 | 7 | 1Kgs 7:15 | `שמנה` | not_unusual |
| 12 | all_source | `peace_h` | Peace | 2 | 7 | 1Sam 18:30 | `דוד` | not_unusual |
| 13 | all_source | `peace_h` | Peace | 2 | 7 | 1Sam 20:28 | `דוד` | not_unusual |
| 14 | all_source | `locust_h` | Locust | 2 | 7 | 2Chr 10:12 | `דבר` | not_unusual |
| 15 | all_source | `locust_plague_h` | Locust Plague | 2 | 7 | 2Chr 10:12 | `דבר` | not_unusual |
| 16 | all_source | `locusts_plague_h` | Locusts | 2 | 7 | 2Chr 10:12 | `דבר` | not_unusual |
| 17 | all_source | `prophet_h` | Prophet | 2 | 7 | 2Chr 21:7 | `הברית` | not_unusual |
| 18 | all_source | `locust_h` | Locust | -2 | 7 | 2Chr 26:23 | `הקבורה` | not_unusual |
| 19 | all_source | `desolation_h` | Desolation | 2 | 7 | 2Chr 32:30 | `למטהמערבה` | not_unusual |
| 20 | all_source | `elam_h` | Elam | -2 | 7 | 2Chr 32:31 | `המשלחימ` | not_unusual |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `bibi_h` | Bibi | -2 | 7 | 1Chr 2:55 | `ישבו` | not_unusual |
| 2 | all_source | `lion_h` | Lion | 2 | 7 | 1Kgs 13:26 | `איש` | not_unusual |
| 3 | all_source | `lord_h` | Lord | -2 | 7 | 1Kgs 20:9 | `בנהדד` | not_unusual |
| 4 | all_source | `yhwh_h` | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` | not_unusual |
| 5 | all_source | `heaven_h` | Heaven | -2 | 7 | 1Kgs 8:22 | `ויעמד` | not_unusual |
| 6 | all_source | `hell_sheol_h` | Sheol | 2 | 7 | 1Sam 14:47 | `ישראל` | not_unusual |
| 7 | all_source | `paul_h` | Paul | 2 | 7 | 1Sam 14:47 | `ישראל` | not_unusual |
| 8 | all_source | `yhwh_h` | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` | not_unusual |
| 9 | all_source | `yhwh_h` | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` | not_unusual |
| 10 | all_source | `yhwh_h` | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` | not_unusual |
| 11 | all_source | `yhwh_h` | YHWH | -2 | 7 | 2Chr 24:8 | `חוצה` | not_unusual |
| 12 | all_source | `mary_h` | Mary | 2 | 7 | 2Chr 28:15 | `מערמיהמ` | not_unusual |
| 13 | all_source | `heaven_h` | Heaven | 2 | 7 | 2Chr 30:27 | `ויקמו` | not_unusual |
| 14 | all_source | `asshur_h` | Asshur | -2 | 7 | 2Kgs 17:6 | `וישב` | not_unusual |
| 15 | all_source | `assyria_h` | Assyria | -2 | 7 | 2Kgs 17:6 | `וישב` | not_unusual |
| 16 | all_source | `temple_h` | Temple | -2 | 7 | 2Kgs 23:4 | `כלהכלימ` | not_unusual |
| 17 | all_source | `yhwh_h` | YHWH | -2 | 7 | 2Kgs 5:11 | `והניפ` | not_unusual |
| 18 | all_source | `peace_h` | Peace | 2 | 7 | 2Sam 20:9 | `לו` | not_unusual |
| 19 | all_source | `hell_sheol_h` | Sheol | 2 | 7 | 2Sam 3:10 | `ישראל` | not_unusual |
| 20 | all_source | `paul_h` | Paul | 2 | 7 | 2Sam 3:10 | `ישראל` | not_unusual |

### center_verse_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `rome_h` | Rome | -6 | 19 | 1Kgs 7:40 | `ואתהמזרקות` | not_unusual |
| 2 | all_source | `rome_h` | Rome | 6 | 19 | Josh 22:5 | `אתכמ` | not_unusual |
| 3 | all_source | `rome_h` | Rome | -8 | 25 | Gen 42:7 | `באתמ` | not_unusual |
| 4 | all_source | `rome_h` | Rome | -9 | 28 | Gen 7:19 | `עלהארצ` | not_unusual |
| 5 | all_source | `rome_alt_h` | Rome | 11 | 34 | 2Chr 15:17 | `והבמות` | not_unusual |
| 6 | all_source | `year_2001_additive_h` | Gregorian 2001 | 11 | 56 | Ezek 7:8 | `עליכ` | not_unusual |
| 7 | all_source | `rome_alt_h` | Rome | 14 | 43 | 2Sam 17:20 | `עבדי` | not_unusual |
| 8 | all_source | `rome_alt_h` | Rome | -14 | 43 | Num 11:4 | `ישראל` | not_unusual |
| 9 | all_source | `rome_h` | Rome | 16 | 49 | Isa 29:18 | `דבריספר` | not_unusual |
| 10 | all_source | `rome_alt_h` | Rome | -16 | 49 | Jer 50:41 | `וגוי` | not_unusual |
| 11 | all_source | `rome_alt_h` | Rome | 19 | 58 | Num 11:4 | `בני` | not_unusual |
| 12 | all_source | `year_2001_additive_h` | Gregorian 2001 | -19 | 96 | Exod 10:1 | `בקרבו` | not_unusual |
| 13 | all_source | `rome_h` | Rome | 23 | 70 | Deut 2:6 | `מאתמ` | not_unusual |
| 14 | all_source | `rome_alt_h` | Rome | -24 | 73 | 1Sam 23:22 | `הכינו` | not_unusual |
| 15 | all_source | `rome_alt_h` | Rome | 28 | 85 | 2Sam 22:17 | `ישלח` | not_unusual |
| 16 | all_source | `rome_alt_h` | Rome | 29 | 88 | Job 22:6 | `תפשיט` | not_unusual |
| 17 | all_source | `rome_alt_h` | Rome | -33 | 100 | 2Sam 17:20 | `מיכל` | not_unusual |
| 18 | all_source | `rome_alt_h` | Rome | -33 | 100 | Ezek 34:14 | `יהיה` | not_unusual |
| 19 | all_source | `rome_h` | Rome | -35 | 106 | Isa 38:14 | `כסוס` | not_unusual |
| 20 | all_source | `rome_alt_h` | Rome | -36 | 109 | Isa 53:8 | `וממשפט` | not_unusual |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `second_death_h` | Second Death | 9 | 46 | Jer 43:3 | `בבל` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `second_death_h` | Second Death | -11 | 56 | Num 29:29 | `ארבעה` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `timothy_h` | Timothy | 16 | 81 | Gen 30:20 | `אתשמו` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `pathrusim_h` | Pathrusim | 28 | 141 | 2Kgs 15:31 | `עשה` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `pathrusim_h` | Pathrusim | -37 | 186 | Zech 11:13 | `השליכהו` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `second_death_h` | Second Death | 38 | 191 | Hag 2:16 | `והיתה` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `germany_h` | Germany | -61 | 306 | Dan 2:49 | `מדינת` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `second_death_h` | Second Death | -92 | 461 | Gen 46:27 | `לביתיעקב` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `second_death_h` | Second Death | -100 | 501 | Neh 7:11 | `מאות` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `locust_h` | Locust | 2 | 7 | 1Chr 10:14 | `דרש` | not_unusual |
| 11 | all_source | `elul_h` | Elul | 2 | 7 | 1Chr 10:4 | `כליו` | not_unusual |
| 12 | all_source | `heaven_h` | Heaven | -2 | 7 | 1Chr 10:4 | `ויאמר` | not_unusual |
| 13 | all_source | `teeth_h` | Teeth | -2 | 7 | 1Chr 11:19 | `בנפשותמ` | not_unusual |
| 14 | all_source | `mary_h` | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` | not_unusual |
| 15 | all_source | `obal_h` | Obal | 2 | 7 | 1Chr 14:11 | `בבעל` | not_unusual |
| 16 | all_source | `amorite_h` | Amorite | 2 | 7 | 1Chr 15:13 | `פרצ` | not_unusual |
| 17 | all_source | `riphath_h` | Riphath | -2 | 7 | 1Chr 15:24 | `לפני` | not_unusual |
| 18 | all_source | `heshvan_h` | Heshvan | -2 | 7 | 1Chr 16:29 | `השתחוו` | not_unusual |
| 19 | all_source | `jobab_h` | Jobab | 2 | 7 | 1Chr 17:1 | `יושב` | not_unusual |
| 20 | all_source | `torment_h` | Torment | -2 | 7 | 1Chr 17:9 | `בני` | not_unusual |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `heaven_h` | Heaven | 2 | 7 | Judg 19:3 | `ויקמ` | not_unusual |
| 2 | all_source | `heaven_h` | Heaven | 2 | 7 | Neh 3:1 | `ויקמ` | not_unusual |
| 3 | all_source | `yhwh_h` | YHWH | -2 | 7 | Neh 8:13 | `התורה` | not_unusual |
| 4 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` | not_unusual |
| 5 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` | not_unusual |
| 6 | all_source | `yhwh_h` | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` | not_unusual |
| 7 | all_source | `yhwh_h` | YHWH | 3 | 10 | 2Chr 6:15 | `הזה` | not_unusual |
| 8 | all_source | `yhwh_h` | YHWH | -3 | 10 | Exod 32:10 | `ועתה` | not_unusual |
| 9 | all_source | `yhwh_h` | YHWH | -3 | 10 | Ezek 22:13 | `והנה` | not_unusual |
| 10 | all_source | `yhwh_h` | YHWH | -3 | 10 | Ezek 2:5 | `והמה` | not_unusual |
| 11 | all_source | `yhwh_h` | YHWH | -3 | 10 | Ezek 30:9 | `ביומ` | not_unusual |
| 12 | all_source | `yhwh_h` | YHWH | 3 | 10 | Ezek 44:14 | `בו` | not_unusual |
| 13 | all_source | `yhwh_h` | YHWH | 3 | 10 | Ezra 9:7 | `הזה` | not_unusual |
| 14 | all_source | `yhwh_h` | YHWH | 3 | 10 | Gen 24:53 | `ויוצא` | not_unusual |
| 15 | all_source | `yhwh_h` | YHWH | 3 | 10 | Isa 1:3 | `התבוננ` | not_unusual |
| 16 | all_source | `yhwh_h` | YHWH | 3 | 10 | Isa 3:18 | `ביומ` | not_unusual |
| 17 | all_source | `yhwh_h` | YHWH | -3 | 10 | Isa 3:18 | `ביומ` | not_unusual |
| 18 | all_source | `yhwh_h` | YHWH | 3 | 10 | Isa 58:6 | `הלוא` | not_unusual |
| 19 | all_source | `yhwh_h` | YHWH | 3 | 10 | Jer 44:6 | `הזה` | not_unusual |
| 20 | all_source | `yhwh_h` | YHWH | 3 | 10 | Josh 4:9 | `הזה` | not_unusual |

### span_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `rome_h` | Rome | 11 | 34 | Num 22:13 | `לתתי` | not_unusual |
| 2 | all_source | `rome_alt_h` | Rome | -14 | 43 | Ps 73:7 | `לבב` | not_unusual |
| 3 | all_source | `rome_alt_h` | Rome | -21 | 64 | Isa 33:15 | `אזנו` | not_unusual |
| 4 | all_source | `rome_alt_h` | Rome | -27 | 82 | Isa 53:9 | `ויתנ` | not_unusual |
| 5 | all_source | `rome_alt_h` | Rome | 29 | 88 | 1Sam 23:23 | `המחבאימ` | not_unusual |
| 6 | all_source | `rome_h` | Rome | 32 | 97 | Isa 38:15 | `עלמר` | not_unusual |
| 7 | all_source | `rome_alt_h` | Rome | 35 | 106 | Isa 33:17 | `תחזינה` | not_unusual |
| 8 | all_source | `year_2001_additive_h` | Gregorian 2001 | 35 | 176 | Eccl 3:10 | `לענות` | not_unusual |
| 9 | all_source | `rome_h` | Rome | 36 | 109 | Gen 42:9 | `אשר` | not_unusual |
| 10 | all_source | `rome_alt_h` | Rome | -38 | 115 | Ezek 48:11 | `שמרו` | not_unusual |
| 11 | all_source | `rome_h` | Rome | 38 | 115 | Isa 2:12 | `ליהוה` | not_unusual |
| 12 | all_source | `rome_alt_h` | Rome | 39 | 118 | Prov 13:15 | `יתנחנ` | not_unusual |
| 13 | all_source | `rome_alt_h` | Rome | 40 | 121 | 1Sam 23:20 | `לרדת` | not_unusual |
| 14 | all_source | `rome_alt_h` | Rome | -41 | 124 | Deut 20:7 | `ומיהאיש` | not_unusual |
| 15 | all_source | `rome_alt_h` | Rome | -42 | 127 | Hab 3:8 | `כי` | not_unusual |
| 16 | all_source | `rome_alt_h` | Rome | -43 | 130 | 2Sam 22:19 | `ביומ` | not_unusual |
| 17 | all_source | `rome_alt_h` | Rome | 43 | 130 | Job 22:9 | `אלמנות` | not_unusual |
| 18 | all_source | `rome_h` | Rome | 44 | 133 | Isa 2:16 | `כלשכיות` | not_unusual |
| 19 | all_source | `rome_h` | Rome | -47 | 142 | Gen 7:18 | `ויגברו` | not_unusual |
| 20 | all_source | `rome_h` | Rome | 48 | 145 | Jer 19:13 | `יהודה` | not_unusual |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `second_death_h` | Second Death | -12 | 61 | Jer 38:26 | `בית` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `second_death_h` | Second Death | -34 | 171 | Lev 9:22 | `ויברכמ` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `pathrusim_h` | Pathrusim | -52 | 261 | Isa 26:17 | `תזעק` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `second_death_h` | Second Death | -57 | 286 | Job 31:35 | `ריבי` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `second_death_h` | Second Death | 62 | 311 | Prov 24:29 | `כאשר` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `timothy_h` | Timothy | -66 | 331 | Jer 46:28 | `יעקב` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `second_death_h` | Second Death | -69 | 346 | Ps 99:6 | `אליהוה` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `second_death_h` | Second Death | -73 | 366 | Num 11:16 | `מועד` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `second_death_h` | Second Death | 78 | 391 | 2Kgs 17:39 | `אמאתיהוה` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `second_death_h` | Second Death | 82 | 411 | Ezek 20:13 | `חללו` | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `2027_additive_h` | Gregorian 2027 additive | 86 | 517 | Deut 11:16 | `יפתה` | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `second_death_h` | Second Death | -88 | 441 | Gen 5:26 | `ושמונימ` | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `second_death_h` | Second Death | 92 | 461 | Isa 11:4 | `בצדק` | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `second_death_h` | Second Death | -99 | 496 | Gen 42:14 | `אלהמ` | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `yemen_h` | Yemen | 2 | 7 | 1Chr 17:2 | `ויאמר` | not_unusual |
| 16 | all_source | `torment_h` | Torment | -2 | 7 | 1Chr 19:15 | `ובני` | not_unusual |
| 17 | all_source | `rome_h` | Rome | 2 | 7 | 1Chr 1:45 | `וימת` | not_unusual |
| 18 | all_source | `zion_h` | Zion | -2 | 7 | 1Kgs 11:19 | `וימצא` | not_unusual |
| 19 | all_source | `life_h` | Life | 2 | 7 | 1Kgs 11:23 | `ויקמ` | not_unusual |
| 20 | all_source | `teeth_h` | Teeth | -2 | 7 | 1Kgs 16:2 | `יענ` | not_unusual |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `second_death_h` | Second Death | -2 | 11 | Jer 51:39 | `שנתעולמ` | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `second_death_h` | Second Death | -2 | 11 | Jer 51:57 | `שנתעולמ` | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `day_of_lord_h` | Day Of The Lord | 4 | 25 | Song 4:6 | `שיפוח` | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `second_death_h` | Second Death | 5 | 26 | Isa 60:9 | `תרשיש` | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `second_death_h` | Second Death | -5 | 26 | Judg 8:18 | `הרגתמ` | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `empty_tomb_h` | Empty Tomb | 8 | 41 | Ezek 5:2 | `בתוכ` | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `timothy_h` | Timothy | -8 | 41 | Ps 37:14 | `ודרכו` | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `yeshu_declared_perfect_h` | Jesus Declared Perfect | 9 | 100 | Gen 22:8 | `לעלה` | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `second_death_h` | Second Death | 10 | 51 | Ezek 23:11 | `אהליבה` | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `second_death_h` | Second Death | -11 | 56 | Num 29:26 | `ארבעה` | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `second_death_h` | Second Death | 11 | 56 | Prov 22:18 | `כינעימ` | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `day_of_lord_h` | Day Of The Lord | 12 | 73 | Ezek 29:9 | `וידעו` | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `second_death_h` | Second Death | 20 | 101 | 1Chr 25:26 | `ואחיו` | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `second_death_h` | Second Death | -20 | 101 | 1Chr 4:38 | `במשפחותמ` | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `day_of_lord_h` | Day Of The Lord | 22 | 133 | Josh 8:19 | `ידו` | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `germany_h` | Germany | -25 | 126 | 1Kgs 7:10 | `ואבני` | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `day_of_lord_h` | Day Of The Lord | 28 | 169 | 1Chr 15:12 | `הכינותי` | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `timothy_h` | Timothy | 29 | 146 | Esth 4:14 | `וביתאביכ` | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `second_death_h` | Second Death | -34 | 171 | Ezek 23:11 | `אחותה` | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `second_death_h` | Second Death | 34 | 171 | Job 21:28 | `איה` | paired_uncorrected_p_le_0.05 |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
