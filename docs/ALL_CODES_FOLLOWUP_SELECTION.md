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
| 1 | english_screening | `center_word_exact` | all_source | `eng_heth` | Heth | -2 | Acts 25:20 | `whether` |
| 2 | english_screening | `center_word_exact` | all_source | `eng_heth` | Heth | -2 | Deut 24:14 | `whether` |
| 3 | english_screening | `center_word_exact` | all_source | `eng_aids` | AIDS | -3 | Isa 47:7 | `saidst` |
| 4 | english_screening | `center_word_same_category` | all_source | `eng_edom` | Edom | -2 | 1Chr 19:1 | `ammon` |
| 5 | english_screening | `center_word_same_category` | all_source | `eng_shem` | Shem | -2 | 1Chr 4:26 | `hamuel` |
| 6 | english_screening | `center_word_same_category` | all_source | `eng_seba` | Seba | -2 | 1Chr 4:28 | `beersheba` |
| 7 | english_screening | `center_verse_exact` | all_source | `eng_hand` | Hand | -2 | 1Chr 2:2 | `and` |
| 8 | english_screening | `center_verse_exact` | all_source | `eng_heal` | Heal | -2 | 1Kgs 1:6 | `displeased` |
| 9 | english_screening | `center_verse_exact` | all_source | `eng_hand` | Hand | -2 | 1Kgs 3:6 | `according` |
| 10 | english_screening | `center_verse_same_category` | all_source | `eng_sign` | Sign | -2 | 1Chr 10:13 | `against` |
| 11 | english_screening | `center_verse_same_category` | all_source | `eng_adar` | Adar | -2 | 1Chr 11:19 | `and` |
| 12 | english_screening | `center_verse_same_category` | all_source | `eng_adam` | Adam | -2 | 1Chr 12:31 | `and` |
| 13 | english_screening | `span_exact` | all_source | `eng_lord` | Lord | -3 | 1Sam 30:24 | `who` |
| 14 | english_screening | `span_exact` | all_source | `eng_lord_2` | Lord | -3 | 1Sam 30:24 | `who` |
| 15 | english_screening | `span_exact` | all_source | `eng_isis` | ISIS | -3 | Josh 15:19 | `springs` |
| 16 | english_screening | `span_same_category` | all_source | `eng_adar` | Adar | -2 | 1Sam 15:14 | `and` |
| 17 | english_screening | `span_same_category` | all_source | `eng_mash` | Mash | -2 | 1Sam 28:18 | `day` |
| 18 | english_screening | `span_same_category` | all_source | `eng_adam` | Adam | -2 | 1Sam 9:22 | `and` |
| 19 | english_screening | `hidden_path_only` | all_source | `eng_heal` | Heal | -2 | 1Chr 10:11 | `jabeshgilead` |
| 20 | english_screening | `hidden_path_only` | all_source | `eng_cush` | Cush | -2 | 1Chr 10:4 | `these` |
| 21 | english_screening | `hidden_path_only` | all_source | `eng_bear` | Bear | 2 | 1Chr 11:8 | `repaired` |
| 22 | greek_screening | `center_word_exact` | all_source | `nato_g` | NATO | 8 | Rom 5:10 | `θανατου` |
| 23 | greek_screening | `center_word_exact` | all_source | `temple_g` | Temple | -9 | Matt 23:17 | `ναοσ` |
| 24 | greek_screening | `center_word_exact` | all_source | `blood_g` | Blood | -10 | Rev 19:13 | `αιματι` |
| 25 | greek_screening | `center_word_same_category` | all_source | `lud_g` | Lud | -2 | Phil 2:7 | `δουλου` |
| 26 | greek_screening | `center_word_same_category` | all_source | `javan_g` | Javan | -2 | 1Pet 5:13 | `βαβυλωνι` |
| 27 | greek_screening | `center_word_same_category` | all_source | `obal_g` | Obal | -3 | 1Tim 5:14 | `βουλομαι` |
| 28 | greek_screening | `center_verse_exact` | all_source | `lasha_g` | Lasha | -2 | Acts 9:11 | `ταρσεα` |
| 29 | greek_screening | `center_verse_exact` | all_source | `blood_g` | Blood | 2 | Matt 13:55 | `μαριαμ` |
| 30 | greek_screening | `center_verse_exact` | all_source | `haima_gnt` | Blood | 2 | Matt 13:55 | `μαριαμ` |
| 31 | greek_screening | `center_verse_same_category` | all_source | `temple_g` | Temple | 2 | 1Cor 10:16 | `του` |
| 32 | greek_screening | `center_verse_same_category` | all_source | `china_g` | China | 2 | 1John 2:1 | `δικαιον` |
| 33 | greek_screening | `center_verse_same_category` | all_source | `boils_g` | Boils | 2 | 1Pet 5:13 | `συνεκλεκτη` |
| 34 | greek_screening | `span_exact` | all_source | `god_g` | God | 2 | Rom 14:2 | `εσθιει` |
| 35 | greek_screening | `span_exact` | all_source | `iran_g` | Iran | -4 | Mark 14:48 | `αποκριθεισ` |
| 36 | greek_screening | `span_exact` | all_source | `nato_g` | NATO | 7 | 1Cor 1:27 | `μωρα` |
| 37 | greek_screening | `span_same_category` | all_source | `shelah_g` | Shelah | 2 | Acts 7:42 | `ισραηλ` |
| 38 | greek_screening | `span_same_category` | all_source | `adam_g` | Adam | 2 | Gal 4:27 | `ανδρα` |
| 39 | greek_screening | `span_same_category` | all_source | `gomer_g` | Gomer | -3 | 2Cor 10:3 | `στρατευομεθα` |
| 40 | greek_screening | `hidden_path_only` | all_source | `shelah_g` | Shelah | 2 | 1Cor 10:18 | `ισραηλ` |
| 41 | greek_screening | `hidden_path_only` | all_source | `amen_g` | Amen | 2 | 1Cor 1:10 | `μη` |
| 42 | greek_screening | `hidden_path_only` | all_source | `son_g` | Son | 2 | 1Cor 5:12 | `τουσ` |
| 43 | hebrew_screening | `center_word_exact` | all_source | `desolation_h` | Desolation | 2 | Mic 1:7 | `שממה` |
| 44 | hebrew_screening | `center_word_exact` | all_source | `yhwh_h` | YHWH | 3 | 1Chr 26:27 | `יהוה` |
| 45 | hebrew_screening | `center_word_exact` | all_source | `yhwh_h` | YHWH | 3 | 1Chr 28:20 | `ביתיהוה` |
| 46 | hebrew_screening | `center_word_same_concept` | all_source | `rome_alt_h` | Rome | 5 | Job 5:12 | `ערומימ` |
| 47 | hebrew_screening | `center_word_same_concept` | all_source | `rome_alt_h` | Rome | -42 | Eccl 10:6 | `במרומימ` |
| 48 | hebrew_screening | `center_word_same_category` | all_source | `germany_h` | Germany | -18 | Jer 42:15 | `מצרימ` |
| 49 | hebrew_screening | `center_word_same_category` | all_source | `amorite_h` | Amorite | -2 | 1Chr 15:22 | `במשא` |
| 50 | hebrew_screening | `center_word_same_category` | all_source | `amorite_h` | Amorite | 2 | 1Chr 15:27 | `המשררימ` |
| 51 | hebrew_screening | `center_verse_exact` | all_source | `bibi_h` | Bibi | -2 | 1Chr 2:55 | `ישבו` |
| 52 | hebrew_screening | `center_verse_exact` | all_source | `lion_h` | Lion | 2 | 1Kgs 13:26 | `איש` |
| 53 | hebrew_screening | `center_verse_exact` | all_source | `lord_h` | Lord | -2 | 1Kgs 20:9 | `בנהדד` |
| 54 | hebrew_screening | `center_verse_same_concept` | all_source | `rome_h` | Rome | -6 | 1Kgs 7:40 | `ואתהמזרקות` |
| 55 | hebrew_screening | `center_verse_same_concept` | all_source | `rome_h` | Rome | 6 | Josh 22:5 | `אתכמ` |
| 56 | hebrew_screening | `center_verse_same_concept` | all_source | `year_2001_additive_h` | Gregorian 2001 | 11 | Ezek 7:8 | `עליכ` |
| 57 | hebrew_screening | `center_verse_same_category` | all_source | `second_death_h` | Second Death | 9 | Jer 43:3 | `בבל` |
| 58 | hebrew_screening | `center_verse_same_category` | all_source | `second_death_h` | Second Death | -11 | Num 29:29 | `ארבעה` |
| 59 | hebrew_screening | `center_verse_same_category` | all_source | `timothy_h` | Timothy | 16 | Gen 30:20 | `אתשמו` |
| 60 | hebrew_screening | `span_exact` | all_source | `heaven_h` | Heaven | 2 | Judg 19:3 | `ויקמ` |
| 61 | hebrew_screening | `span_exact` | all_source | `heaven_h` | Heaven | 2 | Neh 3:1 | `ויקמ` |
| 62 | hebrew_screening | `span_exact` | all_source | `mary_h` | Mary | -3 | Mic 6:5 | `זכרנא` |
| 63 | hebrew_screening | `span_same_concept` | all_source | `year_2001_additive_h` | Gregorian 2001 | 35 | Eccl 3:10 | `לענות` |
| 64 | hebrew_screening | `span_same_category` | all_source | `pathrusim_h` | Pathrusim | -52 | Isa 26:17 | `תזעק` |
| 65 | hebrew_screening | `span_same_category` | all_source | `timothy_h` | Timothy | -66 | Jer 46:28 | `יעקב` |
| 66 | hebrew_screening | `span_same_category` | all_source | `2027_additive_h` | Gregorian 2027 additive | 86 | Deut 11:16 | `יפתה` |
| 67 | hebrew_screening | `hidden_path_only` | all_source | `day_of_lord_h` | Day Of The Lord | 4 | Song 4:6 | `שיפוח` |
| 68 | hebrew_screening | `hidden_path_only` | all_source | `empty_tomb_h` | Empty Tomb | 8 | Ezek 5:2 | `בתוכ` |
| 69 | hebrew_screening | `hidden_path_only` | all_source | `yeshu_declared_perfect_h` | Jesus Declared Perfect | 9 | Gen 22:8 | `לעלה` |
| 70 | hebrew_theology | `center_word_exact` | all_source | `htp_yhwh_h` | YHWH | 3 | 1Chr 26:27 | `יהוה` |
| 71 | hebrew_theology | `center_word_exact` | all_source | `htp_yhwh_h` | YHWH | 3 | 1Chr 28:20 | `ביתיהוה` |
| 72 | hebrew_theology | `center_word_same_category` | all_source | `htp_torah_h` | Torah | 7 | 1Chr 5:1 | `בנישראל` |
| 73 | hebrew_theology | `center_word_same_category` | all_source | `htp_torah_h` | Torah | -7 | 2Kgs 17:20 | `ישראל` |
| 74 | hebrew_theology | `center_word_same_category` | all_source | `htp_covenant_h` | Covenant | 8 | Deut 34:9 | `חכמה` |
| 75 | hebrew_theology | `center_verse_same_category` | all_source | `htp_love_h` | Love | 2 | 2Sam 14:21 | `אתהדבר` |
| 76 | hebrew_theology | `center_verse_same_category` | all_source | `htp_love_h` | Love | 2 | 2Sam 15:27 | `שבה` |
| 77 | hebrew_theology | `center_verse_same_category` | all_source | `htp_wisdom_h` | Wisdom | 3 | Isa 49:8 | `כה` |
| 78 | hebrew_theology | `span_same_category` | all_source | `htp_messiah_h` | Messiah | 6 | Ezra 2:5 | `ושבעימ` |
| 79 | hebrew_theology | `span_same_category` | all_source | `htp_messiah_h` | Messiah | 6 | Neh 7:10 | `ושנימ` |
| 80 | hebrew_theology | `span_same_category` | all_source | `htp_covenant_h` | Covenant | -10 | Prov 30:4 | `עלהשמימ` |

## Read

This is a work queue. Rows here should receive letter-path and surface
context review next. Statistical status remains inherited from the source
triage/control columns; this selector does not add significance.
