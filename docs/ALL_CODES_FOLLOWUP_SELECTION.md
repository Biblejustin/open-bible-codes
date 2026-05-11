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
| hebrew_screening | 909 | 30 |
| hebrew_theology | 700 | 11 |

| Selected bucket | Rows |
| --- | ---: |
| `center_word_exact` | 11 |
| `center_word_same_concept` | 3 |
| `center_word_same_category` | 12 |
| `center_verse_exact` | 9 |
| `center_verse_same_concept` | 3 |
| `center_verse_same_category` | 12 |
| `span_exact` | 9 |
| `span_same_concept` | 3 |
| `span_same_category` | 12 |
| `hidden_path_only` | 9 |

## Selected Rows

| Rank | Queue | Bucket | Scope | Term | Concept | Skip | Center | Center word |
| ---: | --- | --- | --- | --- | --- | ---: | --- | --- |
| 1 | english_screening | `center_word_exact` | all_source | `baal` | Baal | 2 | 2Kgs 10:19 | `baal` |
| 2 | english_screening | `center_word_exact` | all_source | `heth` | Heth | -2 | Acts 25:20 | `whether` |
| 3 | english_screening | `center_word_exact` | all_source | `heth` | Heth | -2 | Deut 24:14 | `whether` |
| 4 | english_screening | `center_word_same_category` | all_source | `obed` | Obed | 2 | 1Chr 16:3 | `bread` |
| 5 | english_screening | `center_word_same_category` | all_source | `obed` | Obed | 2 | 1Chr 16:3 | `bread` |
| 6 | english_screening | `center_word_same_category` | all_source | `edom` | Edom | -2 | 1Chr 19:1 | `ammon` |
| 7 | english_screening | `center_verse_exact` | all_source | `hand` | Hand | -2 | 1Chr 2:2 | `and` |
| 8 | english_screening | `center_verse_exact` | all_source | `heal` | Heal | -2 | 1Kgs 1:6 | `displeased` |
| 9 | english_screening | `center_verse_exact` | all_source | `hand` | Hand | -2 | 1Kgs 3:6 | `according` |
| 10 | english_screening | `center_verse_same_category` | all_source | `sign` | Sign | -2 | 1Chr 10:13 | `against` |
| 11 | english_screening | `center_verse_same_category` | all_source | `adar` | Adar | -2 | 1Chr 11:19 | `and` |
| 12 | english_screening | `center_verse_same_category` | all_source | `adam` | Adam | -2 | 1Chr 12:31 | `and` |
| 13 | english_screening | `span_exact` | all_source | `thin` | Thin | -2 | 1John 2:5 | `him` |
| 14 | english_screening | `span_exact` | all_source | `rent` | Rent | -2 | Gen 31:55 | `and` |
| 15 | english_screening | `span_exact` | all_source | `wine` | Wine | -2 | Isa 22:14 | `and` |
| 16 | english_screening | `span_same_category` | all_source | `adar` | Adar | -2 | 1Sam 15:14 | `and` |
| 17 | english_screening | `span_same_category` | all_source | `mash` | Mash | -2 | 1Sam 28:18 | `day` |
| 18 | english_screening | `span_same_category` | all_source | `adam` | Adam | -2 | 1Sam 9:22 | `and` |
| 19 | english_screening | `hidden_path_only` | all_source | `heal` | Heal | -2 | 1Chr 10:11 | `jabeshgilead` |
| 20 | english_screening | `hidden_path_only` | all_source | `sign` | Sign | -2 | 1Chr 10:13 | `against` |
| 21 | english_screening | `hidden_path_only` | all_source | `cush` | Cush | -2 | 1Chr 10:4 | `these` |
| 22 | greek_screening | `center_word_exact` | all_source | `παισ` (pais; English: Servant) | Servant | -7 | Luke 22:64 | `παισασ` (paisas) |
| 23 | greek_screening | `center_word_exact` | all_source | `αννα` (anna; English: Hannah) | Hannah | 8 | Matt 21:9 | `ωσαννα` (osanna; English: Hosanna) |
| 24 | greek_screening | `center_word_exact` | all_source | `αννα` (anna; English: Hannah) | Hannah | -8 | Matt 21:9 | `ωσαννα` (osanna; English: Hosanna) |
| 25 | greek_screening | `center_word_same_category` | all_source | `λουδ` (loud; English: Lud) | Lud | -2 | Phil 2:7 | `δουλου` (doulou; English: servant) |
| 26 | greek_screening | `center_word_same_category` | all_source | `ιωυαν` (Iouan; English: Javan) | Javan | -2 | 1Pet 5:13 | `βαβυλωνι` (babuloni; English: Babylon) |
| 27 | greek_screening | `center_word_same_category` | all_source | `ευαλ` (eual; English: Obal) | Obal | -3 | 1Tim 5:14 | `βουλομαι` (boulomai; English: I want) |
| 28 | greek_screening | `center_verse_exact` | all_source | `δασα` (dasa; English: Lasha) | Lasha | -2 | Acts 9:11 | `ταρσεα` (tarsea; English: of Tarsus) |
| 29 | greek_screening | `center_verse_exact` | all_source | `αιμα` (haima; English: Blood) | Blood | 2 | Matt 13:55 | `μαριαμ` (mariam; English: Mary) |
| 30 | greek_screening | `center_verse_exact` | all_source | `αιμα` (haima; English: Blood) | Blood | 2 | Matt 13:55 | `μαριαμ` (mariam; English: Mary) |
| 31 | greek_screening | `center_verse_same_category` | all_source | `ναοσ` (naos; English: Temple) | Temple | 2 | 1Cor 10:16 | `του` (tou; English: of the) |
| 32 | greek_screening | `center_verse_same_category` | all_source | `κινα` (kina; English: China) | China | 2 | 1John 2:1 | `δικαιον` (dikaion; English: righteous) |
| 33 | greek_screening | `center_verse_same_category` | all_source | `ελκη` (elke; English: Boils) | Boils | 2 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte; English: co-elect) |
| 34 | greek_screening | `span_exact` | all_source | `θεοσ` (theos; English: God) | God | 2 | Rom 14:2 | `εσθιει` (esthiei; English: eats) |
| 35 | greek_screening | `span_exact` | all_source | `ιραν` (iran; English: Iran) | Iran | -4 | Mark 14:48 | `αποκριθεισ` (apokritheis; English: having answered) |
| 36 | greek_screening | `span_exact` | all_source | `νατο` (nato; English: NATO) | NATO | 7 | 1Cor 1:27 | `μωρα` (mora; English: foolish things) |
| 37 | greek_screening | `span_same_category` | all_source | `σαλα` (Sala; English: Shelah) | Shelah | 2 | Acts 7:42 | `ισραηλ` (israel; English: Israel) |
| 38 | greek_screening | `span_same_category` | all_source | `αδαμ` (adam; English: Adam) | Adam | 2 | Gal 4:27 | `ανδρα` (andra; English: man) |
| 39 | greek_screening | `span_same_category` | all_source | `ναοσ` (naos; English: Temple) | Temple | -3 | Heb 10:30 | `οιδαμεν` (oidamen; English: we know) |
| 40 | greek_screening | `hidden_path_only` | all_source | `ναοσ` (naos; English: Temple) | Temple | 2 | 1Cor 10:16 | `του` (tou; English: of the) |
| 41 | greek_screening | `hidden_path_only` | all_source | `σαλα` (Sala; English: Shelah) | Shelah | 2 | 1Cor 10:18 | `ισραηλ` (israel; English: Israel) |
| 42 | greek_screening | `hidden_path_only` | all_source | `αμην` (amen; English: Amen) | Amen | 2 | 1Cor 1:10 | `μη` (me; English: not) |
| 43 | hebrew_screening | `center_word_exact` | all_source | `שממה` (shemamah; English: Desolation) | Desolation | 2 | Mic 1:7 | `שממה` (shemamah; English: desolation) |
| 44 | hebrew_screening | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |
| 45 | hebrew_screening | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |
| 46 | hebrew_screening | `center_word_same_concept` | all_source | `רומא` (rwm; English: Rome) | Rome | 5 | Job 5:12 | `ערומימ` (arumim; English: crafty/shrewd) |
| 47 | hebrew_screening | `center_word_same_concept` | all_source | `רומא` (rwm; English: Rome) | Rome | -42 | Eccl 10:6 | `במרומימ` (ba-meromim; English: in the heights) |
| 48 | hebrew_screening | `center_word_same_concept` | all_source | `ערוב` (rwb; English: Flies Plague) | Flies Plague | -3 | 2Chr 13:11 | `ובערב` (wbrb) |
| 49 | hebrew_screening | `center_word_same_category` | all_source | `גרמניה` (grmnyh; English: Germany) | Germany | -18 | Jer 42:15 | `מצרימ` (Mitzrayim; English: Egypt) |
| 50 | hebrew_screening | `center_word_same_category` | all_source | `אמרי` (mry; English: Amorite) | Amorite | -2 | 1Chr 15:22 | `במשא` (be-massa; English: in bearing/song service) |
| 51 | hebrew_screening | `center_word_same_category` | all_source | `אמרי` (mry; English: Amorite) | Amorite | 2 | 1Chr 15:27 | `המשררימ` (ha-meshorerim; English: the singers) |
| 52 | hebrew_screening | `center_verse_exact` | all_source | `ביבי` (byby; English: Bibi) | Bibi | -2 | 1Chr 2:55 | `ישבו` (yashvu; English: they dwelt/sat) |
| 53 | hebrew_screening | `center_verse_exact` | all_source | `אריה` (ryh; English: Lion) | Lion | 2 | 1Kgs 13:26 | `איש` (ish; English: man) |
| 54 | hebrew_screening | `center_verse_exact` | all_source | `יואל` (ywl; English: Joel) | Joel | 2 | 1Kgs 20:23 | `במישור` (bmyshwr) |
| 55 | hebrew_screening | `center_verse_same_concept` | all_source | `רומי` (rwmy; English: Rome) | Rome | -6 | 1Kgs 7:40 | `ואתהמזרקות` (ve-et ha-mizraqot; English: and the basins) |
| 56 | hebrew_screening | `center_verse_same_concept` | all_source | `התשח` (htshch; English: Hebrew year 5708) | Hebrew year 5708 | 6 | Isa 37:30 | `אכול` (kwl) |
| 57 | hebrew_screening | `center_verse_same_concept` | all_source | `רומי` (rwmy; English: Rome) | Rome | 6 | Josh 22:5 | `אתכמ` (etkhem; English: you) |
| 58 | hebrew_screening | `center_verse_same_category` | all_source | `מותשני` (mwtshny; English: Second Death) | Second Death | 9 | Jer 43:3 | `בבל` (Bavel; English: Babylon) |
| 59 | hebrew_screening | `center_verse_same_category` | all_source | `מותשני` (mwtshny; English: Second Death) | Second Death | -11 | Num 29:29 | `ארבעה` (arbaah; English: four) |
| 60 | hebrew_screening | `center_verse_same_category` | all_source | `טימותי` (tymwty; English: Timothy) | Timothy | 16 | Gen 30:20 | `אתשמו` (et shemo; English: his name) |
| 61 | hebrew_screening | `span_exact` | all_source | `שמימ` (shmym; English: Heaven) | Heaven | 2 | Judg 19:3 | `ויקמ` (vayaqom; English: and he arose) |
| 62 | hebrew_screening | `span_exact` | all_source | `שמימ` (shmym; English: Heaven) | Heaven | 2 | Neh 3:1 | `ויקמ` (vayaqom; English: and he arose) |
| 63 | hebrew_screening | `span_exact` | all_source | `מרימ` (mrym; English: Mary) | Mary | -3 | Mic 6:5 | `זכרנא` (zekhor na; English: remember, please) |
| 64 | hebrew_screening | `span_same_concept` | all_source | `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | 35 | Eccl 3:10 | `לענות` (la-anot; English: to answer/afflict) |
| 65 | hebrew_screening | `span_same_concept` | all_source | `התשח` (htshch; English: Hebrew year 5708) | Hebrew year 5708 | 40 | Lev 22:27 | `והלאה` (whlh) |
| 66 | hebrew_screening | `span_same_concept` | all_source | `תתתתתא` (ttttt; English: Gregorian 2001) | Gregorian 2001 | -48 | Gen 6:15 | `חמשימ` (chmshym) |
| 67 | hebrew_screening | `span_same_category` | all_source | `פתרסימ` (ptrsym; English: Pathrusim) | Pathrusim | -52 | Isa 26:17 | `תזעק` (tizak; English: she cries out) |
| 68 | hebrew_screening | `span_same_category` | all_source | `טימותי` (tymwty; English: Timothy) | Timothy | -66 | Jer 46:28 | `יעקב` (Yaakov; English: Jacob) |
| 69 | hebrew_screening | `span_same_category` | all_source | `תתתתתכז` (tttttkz; English: Gregorian 2027 additive) | Gregorian 2027 additive | 86 | Deut 11:16 | `יפתה` (yifteh; English: will be enticed) |
| 70 | hebrew_screening | `hidden_path_only` | all_source | `יומיהוה` (yom YHWH; English: Day Of The Lord) | Day Of The Lord | 4 | Song 4:6 | `שיפוח` (she-yafuach; English: until it breathes/blows) |
| 71 | hebrew_screening | `hidden_path_only` | all_source | `קברריק` (qbrryq; English: Empty Tomb) | Empty Tomb | 8 | Ezek 5:2 | `בתוכ` (betokh; English: in the midst) |
| 72 | hebrew_screening | `hidden_path_only` | all_source | `הצהרישומושלמ` (htshryshwmwshlm; English: Jesus Declared Perfect) | Jesus Declared Perfect | 9 | Gen 22:8 | `לעלה` (le-olah; English: for a burnt offering) |
| 73 | hebrew_theology | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 26:27 | `יהוה` (YHWH; English: YHWH) |
| 74 | hebrew_theology | `center_word_exact` | all_source | `יהוה` (YHWH; English: YHWH) | YHWH | 3 | 1Chr 28:20 | `יהוה` (YHWH; English: YHWH) |
| 75 | hebrew_theology | `center_word_same_category` | all_source | `תורה` (twrh; English: Torah) | Torah | 7 | 1Chr 5:1 | `בנישראל` (bnei Yisrael; English: children of Israel) |
| 76 | hebrew_theology | `center_word_same_category` | all_source | `תורה` (twrh; English: Torah) | Torah | -7 | 2Kgs 17:20 | `ישראל` (Yisrael; English: Israel) |
| 77 | hebrew_theology | `center_word_same_category` | all_source | `ברית` (bryt; English: Covenant) | Covenant | 8 | Deut 34:9 | `חכמה` (chkmh; English: Wisdom) |
| 78 | hebrew_theology | `center_verse_same_category` | all_source | `אהבה` (hbh; English: Love) | Love | 2 | 2Sam 14:21 | `הדבר` (ha-davar; English: the word/matter) |
| 79 | hebrew_theology | `center_verse_same_category` | all_source | `אהבה` (hbh; English: Love) | Love | 2 | 2Sam 15:27 | `שבה` (shuvah; English: return) |
| 80 | hebrew_theology | `center_verse_same_category` | all_source | `חכמה` (chkmh; English: Wisdom) | Wisdom | 3 | Isa 49:8 | `כה` (koh; English: thus) |
| 81 | hebrew_theology | `span_same_category` | all_source | `משיח` (Mashiach; English: Messiah) | Messiah | 6 | Ezra 2:5 | `ושבעימ` (ve-shivim; English: and seventy) |
| 82 | hebrew_theology | `span_same_category` | all_source | `משיח` (Mashiach; English: Messiah) | Messiah | 6 | Neh 7:10 | `ושנימ` (ve-shenayim; English: and two) |
| 83 | hebrew_theology | `span_same_category` | all_source | `ברית` (bryt; English: Covenant) | Covenant | -10 | Prov 30:4 | `עלהשמימ` (alah shamayim; English: went up to heaven) |

## Read

This is a work queue. Rows here should receive letter-path and surface
context review next. Statistical status remains inherited from the source
triage/control columns; this selector does not add significance.
