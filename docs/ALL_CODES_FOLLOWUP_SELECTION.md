# All-Codes Follow-Up Selection

Status: compact post-screen review selection, not a claim.

This narrows the relaxed all-codes triage queues into a small manual-review
set. It keeps hidden-path-only rows eligible while ranking rows from same
center-word, related center-word, center-verse, and span-context buckets first.

## Inputs

- `hebrew_theology`: `reports/hebrew_theology_all_codes/triage_queue.csv`
- `hebrew_screening`: `reports/hebrew_screening_all_codes/triage_queue.csv`
- `greek_screening`: `reports/greek_screening_all_codes/triage_queue.csv`
- `english_screening`: `reports/english_screening_all_codes/triage_queue.csv`

## Selection Rule

- max rows per queue: 30
- max rows per bucket: 3
- max rows per term: 2
- prefer all-source rows, then multi-source, then source-specific rows;
- deduplicate exact term/skip/ref keys across source queues;
- do not require an open-text surface echo; hidden-path-only rows remain eligible.

## Counts

| Queue | Queue rows | Selected rows |
| --- | ---: | ---: |
| english_screening | 700 | 21 |
| greek_screening | 700 | 21 |
| hebrew_screening | 875 | 27 |
| hebrew_theology | 700 | 11 |

| Selected bucket | Rows |
| --- | ---: |
| `center_word_exact` | 11 |
| `center_word_same_concept` | 2 |
| `center_word_same_category` | 12 |
| `center_verse_exact` | 9 |
| `center_verse_same_concept` | 3 |
| `center_verse_same_category` | 12 |
| `span_exact` | 9 |
| `span_same_concept` | 1 |
| `span_same_category` | 12 |
| `hidden_path_only` | 9 |

## Selected Rows

| Rank | Queue | Bucket | Scope | Term | Concept | Skip | Center | Center word |
| ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | english_screening | `center_word_exact` | all_source | `heth` | Heth | -2 | Acts 25:20 | `whether` |
| 2 | english_screening | `center_word_exact` | all_source | `heth` | Heth | -2 | Deut 24:14 | `whether` |
| 3 | english_screening | `center_word_exact` | all_source | `aids` | AIDS | -3 | Isa 47:7 | `saidst` |
| 4 | english_screening | `center_word_same_category` | all_source | `edom` | Edom | -2 | 1Chr 19:1 | `ammon` |
| 5 | english_screening | `center_word_same_category` | all_source | `shem` | Shem | -2 | 1Chr 4:26 | `hamuel` |
| 6 | english_screening | `center_word_same_category` | all_source | `seba` | Seba | -2 | 1Chr 4:28 | `beersheba` |
| 7 | english_screening | `center_verse_exact` | all_source | `hand` | Hand | -2 | 1Chr 2:2 | `and` |
| 8 | english_screening | `center_verse_exact` | all_source | `heal` | Heal | -2 | 1Kgs 1:6 | `displeased` |
| 9 | english_screening | `center_verse_exact` | all_source | `hand` | Hand | -2 | 1Kgs 3:6 | `according` |
| 10 | english_screening | `center_verse_same_category` | all_source | `sign` | Sign | -2 | 1Chr 10:13 | `against` |
| 11 | english_screening | `center_verse_same_category` | all_source | `adar` | Adar | -2 | 1Chr 11:19 | `and` |
| 12 | english_screening | `center_verse_same_category` | all_source | `adam` | Adam | -2 | 1Chr 12:31 | `and` |
| 13 | english_screening | `span_exact` | all_source | `lord` | Lord | -3 | 1Sam 30:24 | `who` |
| 14 | english_screening | `span_exact` | all_source | `lord` | Lord | -3 | 1Sam 30:24 | `who` |
| 15 | english_screening | `span_exact` | all_source | `isis` | ISIS | -3 | Josh 15:19 | `springs` |
| 16 | english_screening | `span_same_category` | all_source | `adar` | Adar | -2 | 1Sam 15:14 | `and` |
| 17 | english_screening | `span_same_category` | all_source | `mash` | Mash | -2 | 1Sam 28:18 | `day` |
| 18 | english_screening | `span_same_category` | all_source | `adam` | Adam | -2 | 1Sam 9:22 | `and` |
| 19 | english_screening | `hidden_path_only` | all_source | `heal` | Heal | -2 | 1Chr 10:11 | `jabeshgilead` |
| 20 | english_screening | `hidden_path_only` | all_source | `cush` | Cush | -2 | 1Chr 10:4 | `these` |
| 21 | english_screening | `hidden_path_only` | all_source | `bear` | Bear | 2 | 1Chr 11:8 | `repaired` |
| 22 | greek_screening | `center_word_exact` | all_source | `νατο` (nato; English: NATO) | NATO | 8 | Rom 5:10 | `θανατου` (thanatou) |
| 23 | greek_screening | `center_word_exact` | all_source | `ναοσ` (naos; English: Temple) | Temple | -9 | Matt 23:17 | `ναοσ` (naos; English: temple) |
| 24 | greek_screening | `center_word_exact` | all_source | `αιμα` (haima; English: Blood) | Blood | -10 | Rev 19:13 | `αιματι` (aimati) |
| 25 | greek_screening | `center_word_same_category` | all_source | `λουδ` (loud; English: Lud) | Lud | -2 | Phil 2:7 | `δουλου` (doulou) |
| 26 | greek_screening | `center_word_same_category` | all_source | `ιωυαν` (Iouan; English: Javan) | Javan | -2 | 1Pet 5:13 | `βαβυλωνι` (babuloni) |
| 27 | greek_screening | `center_word_same_category` | all_source | `ευαλ` (eual; English: Obal) | Obal | -3 | 1Tim 5:14 | `βουλομαι` (boulomai) |
| 28 | greek_screening | `center_verse_exact` | all_source | `δασα` (dasa; English: Lasha) | Lasha | -2 | Acts 9:11 | `ταρσεα` (tarsea) |
| 29 | greek_screening | `center_verse_exact` | all_source | `αιμα` (haima; English: Blood) | Blood | 2 | Matt 13:55 | `μαριαμ` (mariam) |
| 30 | greek_screening | `center_verse_exact` | all_source | `αιμα` (haima; English: Blood) | Blood | 2 | Matt 13:55 | `μαριαμ` (mariam) |
| 31 | greek_screening | `center_verse_same_category` | all_source | `ναοσ` (naos; English: Temple) | Temple | 2 | 1Cor 10:16 | `του` (tou) |
| 32 | greek_screening | `center_verse_same_category` | all_source | `κινα` (kina; English: China) | China | 2 | 1John 2:1 | `δικαιον` (dikaion) |
| 33 | greek_screening | `center_verse_same_category` | all_source | `ελκη` (elke; English: Boils) | Boils | 2 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte) |
| 34 | greek_screening | `span_exact` | all_source | `θεοσ` (theos; English: God) | God | 2 | Rom 14:2 | `εσθιει` (esthiei) |
| 35 | greek_screening | `span_exact` | all_source | `ιραν` (iran; English: Iran) | Iran | -4 | Mark 14:48 | `αποκριθεισ` (apokritheis) |
| 36 | greek_screening | `span_exact` | all_source | `νατο` (nato; English: NATO) | NATO | 7 | 1Cor 1:27 | `μωρα` (mora) |
| 37 | greek_screening | `span_same_category` | all_source | `σαλα` (Sala; English: Shelah) | Shelah | 2 | Acts 7:42 | `ισραηλ` (israel; English: Israel) |
| 38 | greek_screening | `span_same_category` | all_source | `αδαμ` (adam; English: Adam) | Adam | 2 | Gal 4:27 | `ανδρα` (andra) |
| 39 | greek_screening | `span_same_category` | all_source | `γαμερ` (gamer; English: Gomer) | Gomer | -3 | 2Cor 10:3 | `στρατευομεθα` (strateuometha) |
| 40 | greek_screening | `hidden_path_only` | all_source | `σαλα` (Sala; English: Shelah) | Shelah | 2 | 1Cor 10:18 | `ισραηλ` (israel; English: Israel) |
| 41 | greek_screening | `hidden_path_only` | all_source | `αμην` (amen; English: Amen) | Amen | 2 | 1Cor 1:10 | `μη` (me) |
| 42 | greek_screening | `hidden_path_only` | all_source | `υιοσ` (huios; English: Son) | Son | 2 | 1Cor 5:12 | `τουσ` (tous) |
| 43 | hebrew_screening | `center_word_exact` | all_source | `שממה` (shemamah; English: Desolation) | Desolation | 2 | Mic 1:7 | `שממה` (shemamah; English: desolation) |
| 44 | hebrew_screening | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |
| 45 | hebrew_screening | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |
| 46 | hebrew_screening | `center_word_same_concept` | all_source | `רומא` (rwm; English: Rome) | Rome | 5 | Job 5:12 | `ערומימ` (rwmym) |
| 47 | hebrew_screening | `center_word_same_concept` | all_source | `רומא` (rwm; English: Rome) | Rome | -42 | Eccl 10:6 | `במרומימ` (bmrwmym) |
| 48 | hebrew_screening | `center_word_same_category` | all_source | `גרמניה` (grmnyh; English: Germany) | Germany | -18 | Jer 42:15 | `מצרימ` (mtsrym) |
| 49 | hebrew_screening | `center_word_same_category` | all_source | `אמרי` (mry; English: Amorite) | Amorite | -2 | 1Chr 15:22 | `במשא` (bmsh) |
| 50 | hebrew_screening | `center_word_same_category` | all_source | `אמרי` (mry; English: Amorite) | Amorite | 2 | 1Chr 15:27 | `המשררימ` (hmshrrym) |
| 51 | hebrew_screening | `center_verse_exact` | all_source | `ביבי` (byby; English: Bibi) | Bibi | -2 | 1Chr 2:55 | `ישבו` (yshbw) |
| 52 | hebrew_screening | `center_verse_exact` | all_source | `אריה` (ryh; English: Lion) | Lion | 2 | 1Kgs 13:26 | `איש` (ysh) |
| 53 | hebrew_screening | `center_verse_exact` | all_source | `אדני` (Adonai; English: Lord) | Lord | -2 | 1Kgs 20:9 | `בנהדד` (bnhdd) |
| 54 | hebrew_screening | `center_verse_same_concept` | all_source | `רומי` (rwmy; English: Rome) | Rome | -6 | 1Kgs 7:40 | `ואתהמזרקות` (wthmzrqwt) |
| 55 | hebrew_screening | `center_verse_same_concept` | all_source | `רומי` (rwmy; English: Rome) | Rome | 6 | Josh 22:5 | `אתכמ` (tkm) |
| 56 | hebrew_screening | `center_verse_same_concept` | all_source | `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 11 | Ezek 7:8 | `עליכ` (lyk) |
| 57 | hebrew_screening | `center_verse_same_category` | all_source | `מותשני` (mwtshny; English: Second Death) | Second Death | 9 | Jer 43:3 | `בבל` (Bavel; English: Babylon) |
| 58 | hebrew_screening | `center_verse_same_category` | all_source | `מותשני` (mwtshny; English: Second Death) | Second Death | -11 | Num 29:29 | `ארבעה` (rbh) |
| 59 | hebrew_screening | `center_verse_same_category` | all_source | `טימותי` (tymwty; English: Timothy) | Timothy | 16 | Gen 30:20 | `אתשמו` (tshmw) |
| 60 | hebrew_screening | `span_exact` | all_source | `שמימ` (shmym; English: Heaven) | Heaven | 2 | Judg 19:3 | `ויקמ` (wyqm) |
| 61 | hebrew_screening | `span_exact` | all_source | `שמימ` (shmym; English: Heaven) | Heaven | 2 | Neh 3:1 | `ויקמ` (wyqm) |
| 62 | hebrew_screening | `span_exact` | all_source | `מרימ` (mrym; English: Mary) | Mary | -3 | Mic 6:5 | `זכרנא` (zkrn) |
| 63 | hebrew_screening | `span_same_concept` | all_source | `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 35 | Eccl 3:10 | `לענות` (lnwt) |
| 64 | hebrew_screening | `span_same_category` | all_source | `פתרסימ` (ptrsym; English: Pathrusim) | Pathrusim | -52 | Isa 26:17 | `תזעק` (tzq) |
| 65 | hebrew_screening | `span_same_category` | all_source | `טימותי` (tymwty; English: Timothy) | Timothy | -66 | Jer 46:28 | `יעקב` (Yaakov; English: Jacob) |
| 66 | hebrew_screening | `span_same_category` | all_source | `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | Gregorian 2027 additive | 86 | Deut 11:16 | `יפתה` (ypth) |
| 67 | hebrew_screening | `hidden_path_only` | all_source | `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 4 | Song 4:6 | `שיפוח` (shypwch) |
| 68 | hebrew_screening | `hidden_path_only` | all_source | `קברריק` (qbrryq; English: Empty Tomb) | Empty Tomb | 8 | Ezek 5:2 | `בתוכ` (btwk) |
| 69 | hebrew_screening | `hidden_path_only` | all_source | `הצהרישומושלמ` (htshryshwmwshlm; English: Jesus Declared Perfect) | Jesus Declared Perfect | 9 | Gen 22:8 | `לעלה` (llh) |
| 70 | hebrew_theology | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |
| 71 | hebrew_theology | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |
| 72 | hebrew_theology | `center_word_same_category` | all_source | `תורה` (twrh; English: Torah) | Torah | 7 | 1Chr 5:1 | `בנישראל` (bnyshrl) |
| 73 | hebrew_theology | `center_word_same_category` | all_source | `תורה` (twrh; English: Torah) | Torah | -7 | 2Kgs 17:20 | `ישראל` (Yisrael; English: Israel) |
| 74 | hebrew_theology | `center_word_same_category` | all_source | `ברית` (bryt; English: Covenant) | Covenant | 8 | Deut 34:9 | `חכמה` (chkmh; English: Wisdom) |
| 75 | hebrew_theology | `center_verse_same_category` | all_source | `אהבה` (hbh; English: Love) | Love | 2 | 2Sam 14:21 | `הדבר` (hdbr) |
| 76 | hebrew_theology | `center_verse_same_category` | all_source | `אהבה` (hbh; English: Love) | Love | 2 | 2Sam 15:27 | `שבה` (shbh) |
| 77 | hebrew_theology | `center_verse_same_category` | all_source | `חכמה` (chkmh; English: Wisdom) | Wisdom | 3 | Isa 49:8 | `כה` (kh) |
| 78 | hebrew_theology | `span_same_category` | all_source | `משיח` (Mashiach; English: Messiah) | Messiah | 6 | Ezra 2:5 | `ושבעימ` (wshbym) |
| 79 | hebrew_theology | `span_same_category` | all_source | `משיח` (Mashiach; English: Messiah) | Messiah | 6 | Neh 7:10 | `ושנימ` (wshnym) |
| 80 | hebrew_theology | `span_same_category` | all_source | `ברית` (bryt; English: Covenant) | Covenant | -10 | Prov 30:4 | `עלהשמימ` (lhshmym) |

## Read

This is a work queue. Rows here should receive letter-path and surface
context review next. Statistical status remains inherited from the source
triage/control columns; this selector does not add significance.
