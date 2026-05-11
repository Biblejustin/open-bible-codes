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
| Raw rows scanned | 3,580,932 |
| Queue rows | 877 |
| `center_word_exact` queue rows | 100 |
| `center_word_same_concept` queue rows | 3 |
| `center_word_same_category` queue rows | 100 |
| `center_verse_exact` queue rows | 100 |
| `center_verse_same_concept` queue rows | 74 |
| `center_verse_same_category` queue rows | 100 |
| `span_exact` queue rows | 100 |
| `span_same_concept` queue rows | 100 |
| `span_same_category` queue rows | 100 |
| `hidden_path_only` queue rows | 100 |

## Top Queue Rows

### center_word_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `desolation_h` `שממה` (shemamah; English: Desolation) | Desolation | 2 | 7 | Mic 1:7 | `שממה` (shemamah; English: desolation) | not_unusual |
| 2 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 3 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 4 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 10:5 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 5 | all_source | `narrative_solomon_h` `שלמה` (Shlomo; English: Solomon) | Solomon | -3 | 10 | 1Kgs 7:1 | `שלמה` (Shlomo; English: Solomon) | not_unusual |
| 6 | all_source | `solomon_h` `שלמה` (Shlomo; English: Solomon) | Solomon | -3 | 10 | 1Kgs 7:1 | `שלמה` (Shlomo; English: Solomon) | not_unusual |
| 7 | all_source | `lord_h` `אדני` (Adonai; English: Lord) | Lord | 3 | 10 | 1Sam 25:14 | `אדנינו` (dnynw) | not_unusual |
| 8 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:11 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 9 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:16 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 10 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:23 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 11 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Sam 26:9 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 12 | all_source | `angel_h` `מלאכ` (mlk; English: Angel) | Angel | -3 | 10 | 1Sam 29:9 | `כמלאכ` (kmlk) | not_unusual |
| 13 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | 2Chr 21:7 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 14 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Chr 33:15 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 15 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Chr 9:4 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 16 | all_source | `lord_h` `אדני` (Adonai; English: Lord) | Lord | -3 | 10 | 2Kgs 18:27 | `אדני` (Adonai; English: Lord) | not_unusual |
| 17 | all_source | `narrative_solomon_h` `שלמה` (Shlomo; English: Solomon) | Solomon | -3 | 10 | 2Kgs 23:13 | `שלמה` (Shlomo; English: Solomon) | not_unusual |
| 18 | all_source | `solomon_h` `שלמה` (Shlomo; English: Solomon) | Solomon | -3 | 10 | 2Kgs 23:13 | `שלמה` (Shlomo; English: Solomon) | not_unusual |
| 19 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Kgs 23:24 | `יהוה` (YHWH; English: YHWH) | not_unusual |
| 20 | all_source | `narrative_solomon_h` `שלמה` (Shlomo; English: Solomon) | Solomon | -3 | 10 | 2Kgs 24:13 | `שלמה` (Shlomo; English: Solomon) | not_unusual |

### center_word_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 5 | 16 | Job 5:12 | `ערומימ` (arumim; English: crafty/shrewd) | not_unusual |
| 2 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -42 | 127 | Eccl 10:6 | `במרומימ` (ba-meromim; English: in the heights) | not_unusual |
| 3 | multi_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 7 | 22 | 1Chr 11:33 | `הבחרומי` (hbchrwmy) | not_unusual |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `germany_h` `גרמניה` (grmnyh; English: Germany) | Germany | -18 | 91 | Jer 42:15 | `מצרימ` (Mitzrayim; English: Egypt) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `amorite_h` `אמרי` (mry; English: Amorite) | Amorite | -2 | 7 | 1Chr 15:22 | `במשא` (be-massa; English: in bearing/song service) | not_unusual |
| 3 | all_source | `amorite_h` `אמרי` (mry; English: Amorite) | Amorite | 2 | 7 | 1Chr 15:27 | `המשררימ` (ha-meshorerim; English: the singers) | not_unusual |
| 4 | all_source | `asshur_h` `אשור` (shwr; English: Asshur) | Asshur | 2 | 7 | 1Chr 7:23 | `שמו` (shmw) | not_unusual |
| 5 | all_source | `shinar_h` `שנער` (shnr; English: Shinar) | Shinar | 2 | 7 | 1Chr 8:22 | `ועבר` (wbr) | not_unusual |
| 6 | all_source | `locust_h` `ארבה` (rbh; English: Locust) | Locust | 2 | 7 | 1Kgs 12:12 | `דבר` (davar; English: word/matter) | not_unusual |
| 7 | all_source | `locust_plague_h` `ארבה` (rbh; English: Locust Plague) | Locust Plague | 2 | 7 | 1Kgs 12:12 | `דבר` (davar; English: word/matter) | not_unusual |
| 8 | all_source | `locusts_plague_h` `ארבה` (rbh; English: Locusts) | Locusts | 2 | 7 | 1Kgs 12:12 | `דבר` (davar; English: word/matter) | not_unusual |
| 9 | all_source | `shinar_h` `שנער` (shnr; English: Shinar) | Shinar | 2 | 7 | 1Kgs 15:1 | `שמנה` (shmnh) | not_unusual |
| 10 | all_source | `asshur_h` `אשור` (shwr; English: Asshur) | Asshur | -2 | 7 | 1Kgs 18:25 | `בשמ` (bshm) | not_unusual |
| 11 | all_source | `shinar_h` `שנער` (shnr; English: Shinar) | Shinar | 2 | 7 | 1Kgs 7:15 | `שמנה` (shmnh) | not_unusual |
| 12 | all_source | `peace_h` `שלומ` (shlwm; English: Peace) | Peace | 2 | 7 | 1Sam 18:30 | `דוד` (dwd; English: David) | not_unusual |
| 13 | all_source | `peace_h` `שלומ` (shlwm; English: Peace) | Peace | 2 | 7 | 1Sam 20:28 | `דוד` (dwd; English: David) | not_unusual |
| 14 | all_source | `locust_h` `ארבה` (rbh; English: Locust) | Locust | 2 | 7 | 2Chr 10:12 | `דבר` (davar; English: word/matter) | not_unusual |
| 15 | all_source | `locust_plague_h` `ארבה` (rbh; English: Locust Plague) | Locust Plague | 2 | 7 | 2Chr 10:12 | `דבר` (davar; English: word/matter) | not_unusual |
| 16 | all_source | `locusts_plague_h` `ארבה` (rbh; English: Locusts) | Locusts | 2 | 7 | 2Chr 10:12 | `דבר` (davar; English: word/matter) | not_unusual |
| 17 | all_source | `prophet_h` `נביא` (navi; English: Prophet) | Prophet | 2 | 7 | 2Chr 21:7 | `הברית` (hbryt) | not_unusual |
| 18 | all_source | `locust_h` `ארבה` (rbh; English: Locust) | Locust | -2 | 7 | 2Chr 26:23 | `הקבורה` (hqbwrh) | not_unusual |
| 19 | all_source | `desolation_h` `שממה` (shemamah; English: Desolation) | Desolation | 2 | 7 | 2Chr 32:30 | `למטהמערבה` (lmthmrbh) | not_unusual |
| 20 | all_source | `elam_h` `עילמ` (ylm; English: Elam) | Elam | -2 | 7 | 2Chr 32:31 | `המשלחימ` (hmshlchym) | not_unusual |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `bibi_h` `ביבי` (byby; English: Bibi) | Bibi | -2 | 7 | 1Chr 2:55 | `ישבו` (yashvu; English: they dwelt/sat) | not_unusual |
| 2 | all_source | `lion_h` `אריה` (ryh; English: Lion) | Lion | 2 | 7 | 1Kgs 13:26 | `איש` (ish; English: man) | not_unusual |
| 3 | all_source | `prophet_joel_h` `יואל` (ywl; English: Joel) | Joel | 2 | 7 | 1Kgs 20:23 | `במישור` (bmyshwr) | not_unusual |
| 4 | all_source | `lord_h` `אדני` (Adonai; English: Lord) | Lord | -2 | 7 | 1Kgs 20:9 | `בנהדד` (Ben-Hadad; English: Ben-Hadad) | not_unusual |
| 5 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Kgs 2:42 | `הלוא` (hlw) | not_unusual |
| 6 | all_source | `heaven_h` `שמימ` (shmym; English: Heaven) | Heaven | -2 | 7 | 1Kgs 8:22 | `ויעמד` (wymd) | not_unusual |
| 7 | all_source | `hell_sheol_h` `שאול` (shwl; English: Sheol) | Sheol | 2 | 7 | 1Sam 14:47 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 8 | all_source | `paul_h` `שאול` (shwl; English: Paul) | Paul | 2 | 7 | 1Sam 14:47 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 9 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 1Sam 17:46 | `היומ` (hywm) | not_unusual |
| 10 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 13:10 | `וכהנימ` (wkhnym) | not_unusual |
| 11 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 2 | 7 | 2Chr 20:15 | `ההמונ` (hhmwn) | not_unusual |
| 12 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Chr 24:8 | `חוצה` (chwtsh) | not_unusual |
| 13 | all_source | `mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 2Chr 28:15 | `מערמיהמ` (mrmyhm) | not_unusual |
| 14 | all_source | `heaven_h` `שמימ` (shmym; English: Heaven) | Heaven | 2 | 7 | 2Chr 30:27 | `ויקמו` (wyqmw) | not_unusual |
| 15 | all_source | `asshur_h` `אשור` (shwr; English: Asshur) | Asshur | -2 | 7 | 2Kgs 17:6 | `וישב` (wyshb) | not_unusual |
| 16 | all_source | `assyria_h` `אשור` (shwr; English: Assyria) | Assyria | -2 | 7 | 2Kgs 17:6 | `וישב` (wyshb) | not_unusual |
| 17 | all_source | `tabernacle_temple_h` `היכל` (hykl; English: Temple) | Temple | -2 | 7 | 2Kgs 23:4 | `כלהכלימ` (klhklym) | not_unusual |
| 18 | all_source | `temple_h` `היכל` (hykl; English: Temple) | Temple | -2 | 7 | 2Kgs 23:4 | `כלהכלימ` (klhklym) | not_unusual |
| 19 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | 2Kgs 5:11 | `והניפ` (whnyp) | not_unusual |
| 20 | all_source | `prophet_joel_h` `יואל` (ywl; English: Joel) | Joel | 2 | 7 | 2Sam 16:11 | `יהוה` (YHWH; English: YHWH) | not_unusual |

### center_verse_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | -6 | 19 | 1Kgs 7:40 | `ואתהמזרקות` (ve-et ha-mizraqot; English: and the basins) | not_unusual |
| 2 | all_source | `am_5708_full_h` `התשח` (htshch; English: Hebrew year 5708) | Hebrew year 5708 | 6 | 19 | Isa 37:30 | `אכול` (kwl) | not_unusual |
| 3 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 6 | 19 | Josh 22:5 | `אתכמ` (etkhem; English: you) | not_unusual |
| 4 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | -8 | 25 | Gen 42:7 | `באתמ` (btm) | not_unusual |
| 5 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | -9 | 28 | Gen 7:19 | `עלהארצ` (lhrts) | not_unusual |
| 6 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 11 | 34 | 2Chr 15:17 | `והבמות` (whbmwt) | not_unusual |
| 7 | all_source | `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 11 | 56 | Ezek 7:8 | `עליכ` (alekha; English: upon you) | not_unusual |
| 8 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 14 | 43 | 2Sam 17:20 | `עבדי` (bdy) | not_unusual |
| 9 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -14 | 43 | Num 11:4 | `ישראל` (Yisrael; English: Israel) | not_unusual |
| 10 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 16 | 49 | Isa 29:18 | `דבריספר` (dbryspr) | not_unusual |
| 11 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -16 | 49 | Jer 50:41 | `וגוי` (wgwy) | not_unusual |
| 12 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 19 | 58 | Num 11:4 | `בני` (bny) | not_unusual |
| 13 | all_source | `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | -19 | 96 | Exod 10:1 | `בקרבו` (bqrbw) | not_unusual |
| 14 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 23 | 70 | Deut 2:6 | `מאתמ` (mtm) | not_unusual |
| 15 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -24 | 73 | 1Sam 23:22 | `הכינו` (hkynw) | not_unusual |
| 16 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 28 | 85 | 2Sam 22:17 | `ישלח` (yshlch) | not_unusual |
| 17 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 29 | 88 | Job 22:6 | `תפשיט` (tpshyt) | not_unusual |
| 18 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -33 | 100 | 2Sam 17:20 | `מיכל` (mykl) | not_unusual |
| 19 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -33 | 100 | Ezek 34:14 | `יהיה` (yhyh) | not_unusual |
| 20 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | -35 | 106 | Isa 38:14 | `כסוס` (ksws) | not_unusual |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 9 | 46 | Jer 43:3 | `בבל` (Bavel; English: Babylon) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -11 | 56 | Num 29:29 | `ארבעה` (arbaah; English: four) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `timothy_h` `טימותי` (tymwty; English: Timothy) | Timothy | 16 | 81 | Gen 30:20 | `אתשמו` (et shemo; English: his name) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `pathrusim_h` `פתרסימ` (ptrsym; English: Pathrusim) | Pathrusim | 28 | 141 | 2Kgs 15:31 | `עשה` (shh) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `pathrusim_h` `פתרסימ` (ptrsym; English: Pathrusim) | Pathrusim | -37 | 186 | Zech 11:13 | `השליכהו` (hshlykhw) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 38 | 191 | Hag 2:16 | `והיתה` (whyth) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `germany_h` `גרמניה` (grmnyh; English: Germany) | Germany | -61 | 306 | Dan 2:49 | `מדינת` (mdynt) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -92 | 461 | Gen 46:27 | `לביתיעקב` (lbytyqb) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -100 | 501 | Neh 7:11 | `מאות` (mwt) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `locust_h` `ארבה` (rbh; English: Locust) | Locust | 2 | 7 | 1Chr 10:14 | `דרש` (drsh) | not_unusual |
| 11 | all_source | `elul_h` `אלול` (lwl; English: Elul) | Elul | 2 | 7 | 1Chr 10:4 | `כליו` (klyw) | not_unusual |
| 12 | all_source | `heaven_h` `שמימ` (shmym; English: Heaven) | Heaven | -2 | 7 | 1Chr 10:4 | `ויאמר` (wymr) | not_unusual |
| 13 | all_source | `teeth_h` `שנימ` (shnym; English: Teeth) | Teeth | -2 | 7 | 1Chr 11:19 | `בנפשותמ` (bnpshwtm) | not_unusual |
| 14 | all_source | `mary_h` `מרימ` (mrym; English: Mary) | Mary | 2 | 7 | 1Chr 13:2 | `מגרשיהמ` (mgrshyhm) | not_unusual |
| 15 | all_source | `obal_h` `עובל` (wbl; English: Obal) | Obal | 2 | 7 | 1Chr 14:11 | `בבעל` (bbl) | not_unusual |
| 16 | all_source | `amorite_h` `אמרי` (mry; English: Amorite) | Amorite | 2 | 7 | 1Chr 15:13 | `פרצ` (prts) | not_unusual |
| 17 | all_source | `riphath_h` `ריפת` (rypt; English: Riphath) | Riphath | -2 | 7 | 1Chr 15:24 | `לפני` (lpny) | not_unusual |
| 18 | all_source | `heshvan_h` `חשונ` (chshwn; English: Heshvan) | Heshvan | -2 | 7 | 1Chr 16:29 | `השתחוו` (hshtchww) | not_unusual |
| 19 | all_source | `jobab_h` `יובב` (ywbb; English: Jobab) | Jobab | 2 | 7 | 1Chr 17:1 | `יושב` (ywshb) | not_unusual |
| 20 | all_source | `torment_h` `ענוי` (nwy; English: Torment) | Torment | -2 | 7 | 1Chr 17:9 | `בני` (bny) | not_unusual |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `heaven_h` `שמימ` (shmym; English: Heaven) | Heaven | 2 | 7 | Judg 19:3 | `ויקמ` (vayaqom; English: and he arose) | not_unusual |
| 2 | all_source | `heaven_h` `שמימ` (shmym; English: Heaven) | Heaven | 2 | 7 | Neh 3:1 | `ויקמ` (vayaqom; English: and he arose) | not_unusual |
| 3 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -2 | 7 | Neh 8:13 | `התורה` (htwrh) | not_unusual |
| 4 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Chr 28:7 | `הזה` (hzh) | not_unusual |
| 5 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 3:6 | `הזה` (hzh) | not_unusual |
| 6 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 1Kgs 8:24 | `הזה` (hzh) | not_unusual |
| 7 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | 2Chr 6:15 | `הזה` (hzh) | not_unusual |
| 8 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Exod 32:10 | `ועתה` (wth) | not_unusual |
| 9 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Ezek 22:13 | `והנה` (whnh) | not_unusual |
| 10 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Ezek 2:5 | `והמה` (whmh) | not_unusual |
| 11 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Ezek 30:9 | `ביומ` (bywm) | not_unusual |
| 12 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Ezek 44:14 | `בו` (bw) | not_unusual |
| 13 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Ezra 9:7 | `הזה` (hzh) | not_unusual |
| 14 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Gen 24:53 | `ויוצא` (wywts) | not_unusual |
| 15 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 1:3 | `התבוננ` (htbwnn) | not_unusual |
| 16 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 3:18 | `ביומ` (bywm) | not_unusual |
| 17 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | -3 | 10 | Isa 3:18 | `ביומ` (bywm) | not_unusual |
| 18 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Isa 58:6 | `הלוא` (hlw) | not_unusual |
| 19 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Jer 44:6 | `הזה` (hzh) | not_unusual |
| 20 | all_source | `yhwh_h` `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 10 | Josh 4:9 | `הזה` (hzh) | not_unusual |

### span_same_concept

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 11 | 34 | Num 22:13 | `לתתי` (ltty) | not_unusual |
| 2 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -14 | 43 | Ps 73:7 | `לבב` (lbb) | not_unusual |
| 3 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -21 | 64 | Isa 33:15 | `אזנו` (znw) | not_unusual |
| 4 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -27 | 82 | Isa 53:9 | `ויתנ` (wytn) | not_unusual |
| 5 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 29 | 88 | 1Sam 23:23 | `המחבאימ` (hmchbym) | not_unusual |
| 6 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 32 | 97 | Isa 38:15 | `עלמר` (lmr) | not_unusual |
| 7 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 35 | 106 | Isa 33:17 | `תחזינה` (tchzynh) | not_unusual |
| 8 | all_source | `year_2001_additive_h` `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 35 | 176 | Eccl 3:10 | `לענות` (la-anot; English: to answer/afflict) | not_unusual |
| 9 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 36 | 109 | Gen 42:9 | `אשר` (shr; English: Asher) | not_unusual |
| 10 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -38 | 115 | Ezek 48:11 | `שמרו` (shmrw) | not_unusual |
| 11 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 38 | 115 | Isa 2:12 | `ליהוה` (le-YHWH; English: to/for YHWH) | not_unusual |
| 12 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 39 | 118 | Prov 13:15 | `יתנחנ` (ytnchn) | not_unusual |
| 13 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 40 | 121 | 1Sam 23:20 | `לרדת` (lrdt) | not_unusual |
| 14 | all_source | `am_5708_full_h` `התשח` (htshch; English: Hebrew year 5708) | Hebrew year 5708 | 40 | 121 | Lev 22:27 | `והלאה` (whlh) | not_unusual |
| 15 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -41 | 124 | Deut 20:7 | `ומיהאיש` (wmyhysh) | not_unusual |
| 16 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -42 | 127 | Hab 3:8 | `כי` (ky) | not_unusual |
| 17 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | -43 | 130 | 2Sam 22:19 | `ביומ` (bywm) | not_unusual |
| 18 | all_source | `rome_alt_h` `רומא` (rwm; English: Rome) | Rome | 43 | 130 | Job 22:9 | `אלמנות` (lmnwt) | not_unusual |
| 19 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 44 | 133 | Isa 2:16 | `כלשכיות` (klshkywt) | not_unusual |
| 20 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | -47 | 142 | Gen 7:18 | `ויגברו` (wygbrw) | not_unusual |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -12 | 61 | Jer 38:26 | `בית` (byt; English: House) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -34 | 171 | Lev 9:22 | `ויברכמ` (wybrkm) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `pathrusim_h` `פתרסימ` (ptrsym; English: Pathrusim) | Pathrusim | -52 | 261 | Isa 26:17 | `תזעק` (tizak; English: she cries out) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -57 | 286 | Job 31:35 | `ריבי` (ryby) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 62 | 311 | Prov 24:29 | `כאשר` (kshr) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `timothy_h` `טימותי` (tymwty; English: Timothy) | Timothy | -66 | 331 | Jer 46:28 | `יעקב` (Yaakov; English: Jacob) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -69 | 346 | Ps 99:6 | `אליהוה` (lyhwh) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -73 | 366 | Num 11:16 | `מועד` (mwd) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 78 | 391 | 2Kgs 17:39 | `אמאתיהוה` (mtyhwh) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 82 | 411 | Ezek 20:13 | `חללו` (chllw) | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `2027_additive_h` `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | Gregorian 2027 additive | 86 | 517 | Deut 11:16 | `יפתה` (yifteh; English: will be enticed) | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -88 | 441 | Gen 5:26 | `ושמונימ` (wshmwnym) | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 92 | 461 | Isa 11:4 | `בצדק` (btsdq) | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -99 | 496 | Gen 42:14 | `אלהמ` (lhm) | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `prophet_jonah_h` `יונה` (ywnh; English: Jonah) | Jonah | 2 | 7 | 1Chr 16:6 | `ובניהו` (wbnyhw) | not_unusual |
| 16 | all_source | `yemen_h` `תימנ` (tymn; English: Yemen) | Yemen | 2 | 7 | 1Chr 17:2 | `ויאמר` (wymr) | not_unusual |
| 17 | all_source | `torment_h` `ענוי` (nwy; English: Torment) | Torment | -2 | 7 | 1Chr 19:15 | `ובני` (wbny) | not_unusual |
| 18 | all_source | `rome_h` `רומי` (rwmy; English: Rome) | Rome | 2 | 7 | 1Chr 1:45 | `וימת` (wymt) | not_unusual |
| 19 | all_source | `zion_h` `ציונ` (tsywn; English: Zion) | Zion | -2 | 7 | 1Kgs 11:19 | `וימצא` (wymts) | not_unusual |
| 20 | all_source | `life_h` `חיימ` (chyym; English: Life) | Life | 2 | 7 | 1Kgs 11:23 | `ויקמ` (vayaqom; English: and he arose) | not_unusual |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -2 | 11 | Jer 51:39 | `שנתעולמ` (shntwlm) | paired_uncorrected_p_le_0.05 |
| 2 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -2 | 11 | Jer 51:57 | `שנתעולמ` (shntwlm) | paired_uncorrected_p_le_0.05 |
| 3 | all_source | `day_of_lord_h` `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 4 | 25 | Song 4:6 | `שיפוח` (she-yafuach; English: until it breathes/blows) | paired_uncorrected_p_le_0.05 |
| 4 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 5 | 26 | Isa 60:9 | `תרשיש` (trshysh; English: Tarshish) | paired_uncorrected_p_le_0.05 |
| 5 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -5 | 26 | Judg 8:18 | `הרגתמ` (hrgtm) | paired_uncorrected_p_le_0.05 |
| 6 | all_source | `empty_tomb_h` `קברריק` (qbrryq; English: Empty Tomb) | Empty Tomb | 8 | 41 | Ezek 5:2 | `בתוכ` (betokh; English: in the midst) | paired_uncorrected_p_le_0.05 |
| 7 | all_source | `timothy_h` `טימותי` (tymwty; English: Timothy) | Timothy | -8 | 41 | Ps 37:14 | `ודרכו` (wdrkw) | paired_uncorrected_p_le_0.05 |
| 8 | all_source | `yeshu_declared_perfect_h` `הצהרישומושלמ` (htshryshwmwshlm; English: Jesus Declared Perfect) | Jesus Declared Perfect | 9 | 100 | Gen 22:8 | `לעלה` (le-olah; English: for a burnt offering) | paired_uncorrected_p_le_0.05 |
| 9 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 10 | 51 | Ezek 23:11 | `אהליבה` (hlybh) | paired_uncorrected_p_le_0.05 |
| 10 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -11 | 56 | Num 29:26 | `ארבעה` (arbaah; English: four) | paired_uncorrected_p_le_0.05 |
| 11 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 11 | 56 | Prov 22:18 | `כינעימ` (kynym) | paired_uncorrected_p_le_0.05 |
| 12 | all_source | `day_of_lord_h` `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 12 | 73 | Ezek 29:9 | `וידעו` (wydw) | paired_uncorrected_p_le_0.05 |
| 13 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 20 | 101 | 1Chr 25:26 | `ואחיו` (wchyw) | paired_uncorrected_p_le_0.05 |
| 14 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -20 | 101 | 1Chr 4:38 | `במשפחותמ` (bmshpchwtm) | paired_uncorrected_p_le_0.05 |
| 15 | all_source | `day_of_lord_h` `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 22 | 133 | Josh 8:19 | `ידו` (ydw) | paired_uncorrected_p_le_0.05 |
| 16 | all_source | `germany_h` `גרמניה` (grmnyh; English: Germany) | Germany | -25 | 126 | 1Kgs 7:10 | `ואבני` (wbny) | paired_uncorrected_p_le_0.05 |
| 17 | all_source | `day_of_lord_h` `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 28 | 169 | 1Chr 15:12 | `הכינותי` (hkynwty) | paired_uncorrected_p_le_0.05 |
| 18 | all_source | `timothy_h` `טימותי` (tymwty; English: Timothy) | Timothy | 29 | 146 | Esth 4:14 | `וביתאביכ` (wbytbyk) | paired_uncorrected_p_le_0.05 |
| 19 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | -34 | 171 | Ezek 23:11 | `אחותה` (chwth) | paired_uncorrected_p_le_0.05 |
| 20 | all_source | `second_death_h` `מותשני` (mwtshny; English: Second Death) | Second Death | 34 | 171 | Job 21:28 | `איה` (yh) | paired_uncorrected_p_le_0.05 |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
