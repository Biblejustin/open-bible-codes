# All-Codes Follow-Up Letter Paths

Status: audit sheet for selected Hebrew and Greek all-codes follow-up rows; no claim.

This report reconstructs the actual ELS letter positions for the selected
Hebrew and Greek all-codes follow-up rows. Hidden-path-only rows are
audited the same way as rows with open-text surface echoes. This is an
audit sheet, not an added statistical test.

## Inputs

- Selected rows: `reports/all_codes_followup_selection/selected_rows.csv`

## Counts

- selected input rows: 80
- path summary rows: 295
- letter rows: 1,348
- sequence mismatches: 0
- selected by queue: `{'english_screening': 21, 'greek_screening': 21, 'hebrew_screening': 27, 'hebrew_theology': 11}`
- path rows by corpus: `{'BYZ_NT': 21, 'EBIBLE_WLC': 38, 'KJV': 21, 'MAM': 38, 'MT_WLC': 38, 'SBLGNT': 21, 'TCG_NT': 21, 'TR_NT': 21, 'UHB': 38, 'UXLC': 38}`
- path rows by bucket: `{'center_verse_exact': 30, 'center_verse_same_category': 45, 'center_verse_same_concept': 15, 'center_word_exact': 40, 'center_word_same_category': 45, 'center_word_same_concept': 10, 'hidden_path_only': 30, 'span_exact': 30, 'span_same_category': 45, 'span_same_concept': 5}`

## Path Summary

| Rank | Queue | Bucket | Term | Corpus | Sequence | Skip | Center | Center word | Path refs |
| ---: | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | english_screening | `center_word_exact` | `heth` | KJV | `heth` | -2 | ACT 25:20 | `whether` | ACT 25:20 |
| 2 | english_screening | `center_word_exact` | `heth` | KJV | `heth` | -2 | DEU 24:14 | `whether` | DEU 24:14 |
| 3 | english_screening | `center_word_exact` | `aids` | KJV | `aids` | -3 | ISA 47:7 | `saidst,` | ISA 47:7 |
| 4 | english_screening | `center_word_same_category` | `edom` | KJV | `edom` | -2 | 1CH 19:1 | `Ammon` | 1CH 19:1 |
| 5 | english_screening | `center_word_same_category` | `shem` | KJV | `shem` | -2 | 1CH 4:26 | `Hamuel` | 1CH 4:26 |
| 6 | english_screening | `center_word_same_category` | `seba` | KJV | `seba` | -2 | 1CH 4:28 | `Beer-sheba,` | 1CH 4:28 |
| 7 | english_screening | `center_verse_exact` | `hand` | KJV | `hand` | -2 | 1CH 2:2 | `and` | 1CH 2:2 |
| 8 | english_screening | `center_verse_exact` | `heal` | KJV | `heal` | -2 | 1KI 1:6 | `displeased` | 1KI 1:6 |
| 9 | english_screening | `center_verse_exact` | `hand` | KJV | `hand` | -2 | 1KI 3:6 | `according` | 1KI 3:6 |
| 10 | english_screening | `center_verse_same_category` | `sign` | KJV | `sign` | -2 | 1CH 10:13 | `against` | 1CH 10:13 |
| 11 | english_screening | `center_verse_same_category` | `adar` | KJV | `adar` | -2 | 1CH 11:19 | `And` | 1CH 11:19; 1CH 11:18 |
| 12 | english_screening | `center_verse_same_category` | `adam` | KJV | `adam` | -2 | 1CH 12:31 | `and` | 1CH 12:31 |
| 13 | english_screening | `span_exact` | `lord` | KJV | `lord` | -3 | 1SA 30:24 | `who` | 1SA 30:24; 1SA 30:23 |
| 14 | english_screening | `span_exact` | `lord` | KJV | `lord` | -3 | 1SA 30:24 | `who` | 1SA 30:24; 1SA 30:23 |
| 15 | english_screening | `span_exact` | `isis` | KJV | `isis` | -3 | JOS 15:19 | `springs.` | JOS 15:20; JOS 15:19 |
| 16 | english_screening | `span_same_category` | `adar` | KJV | `adar` | -2 | 1SA 15:14 | `And` | 1SA 15:14; 1SA 15:13 |
| 17 | english_screening | `span_same_category` | `mash` | KJV | `mash` | -2 | 1SA 28:18 | `day.` | 1SA 28:19; 1SA 28:18 |
| 18 | english_screening | `span_same_category` | `adam` | KJV | `adam` | -2 | 1SA 9:22 | `And` | 1SA 9:22; 1SA 9:21 |
| 19 | english_screening | `hidden_path_only` | `heal` | KJV | `heal` | -2 | 1CH 10:11 | `Jabesh-gilead` | 1CH 10:11 |
| 20 | english_screening | `hidden_path_only` | `cush` | KJV | `cush` | -2 | 1CH 10:4 | `these` | 1CH 10:4 |
| 21 | english_screening | `hidden_path_only` | `bear` | KJV | `bear` | 2 | 1CH 11:8 | `repaired` | 1CH 11:8 |
| 22 | greek_screening | `center_word_exact` | `νατο` | BYZ_NT | `νατο` | 8 | ROM 5:10 | `θανατου` | ROM 5:10 |
| 22 | greek_screening | `center_word_exact` | `νατο` | SBLGNT | `νατο` | 8 | Rom 5:10 | `θανάτου` | Rom 5:10 |
| 22 | greek_screening | `center_word_exact` | `νατο` | TCG_NT | `νατο` | 8 | ROM 5:10 | `θανάτου` | ROM 5:10 |
| 22 | greek_screening | `center_word_exact` | `νατο` | TR_NT | `νατο` | 8 | ROM 5:10 | `θανάτου` | ROM 5:10 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` | BYZ_NT | `ναοσ` | -9 | MAT 23:17 | `ναοσ` | MAT 23:17 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` | SBLGNT | `ναοσ` | -9 | Matt 23:17 | `ναὸς` | Matt 23:17 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` | TCG_NT | `ναοσ` | -9 | MAT 23:17 | `ναὸς` | MAT 23:17 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` | TR_NT | `ναοσ` | -9 | MAT 23:17 | `ναὸς` | MAT 23:17 |
| 24 | greek_screening | `center_word_exact` | `αιμα` | BYZ_NT | `αιμα` | -10 | REV 19:13 | `αιματι` | REV 19:13 |
| 24 | greek_screening | `center_word_exact` | `αιμα` | SBLGNT | `αιμα` | -10 | Rev 19:13 | `αἵματι,` | Rev 19:13 |
| 24 | greek_screening | `center_word_exact` | `αιμα` | TCG_NT | `αιμα` | -10 | REV 19:13 | `αἵματι,` | REV 19:13 |
| 24 | greek_screening | `center_word_exact` | `αιμα` | TR_NT | `αιμα` | -10 | REV 19:13 | `αἵματι` | REV 19:13 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` | BYZ_NT | `λουδ` | -2 | PHP 2:7 | `δουλου` | PHP 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` | SBLGNT | `λουδ` | -2 | Phil 2:7 | `δούλου` | Phil 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` | TCG_NT | `λουδ` | -2 | PHP 2:7 | `δούλου` | PHP 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` | TR_NT | `λουδ` | -2 | PHP 2:7 | `δούλου` | PHP 2:7 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` | BYZ_NT | `ιωυαν` | -2 | 1PE 5:13 | `βαβυλωνι` | 1PE 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` | SBLGNT | `ιωυαν` | -2 | 1Pet 5:13 | `Βαβυλῶνι` | 1Pet 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` | TCG_NT | `ιωυαν` | -2 | 1PE 5:13 | `Βαβυλῶνι` | 1PE 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` | TR_NT | `ιωυαν` | -2 | 1PE 5:13 | `Βαβυλῶνι` | 1PE 5:13 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` | BYZ_NT | `ευαλ` | -3 | 1TI 5:14 | `βουλομαι` | 1TI 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` | SBLGNT | `ευαλ` | -3 | 1Tim 5:14 | `βούλομαι` | 1Tim 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` | TCG_NT | `ευαλ` | -3 | 1TI 5:14 | `Βούλομαι` | 1TI 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` | TR_NT | `ευαλ` | -3 | 1TI 5:14 | `Βούλομαι` | 1TI 5:14 |
| 28 | greek_screening | `center_verse_exact` | `δασα` | BYZ_NT | `δασα` | -2 | ACT 9:11 | `ταρσεα` | ACT 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` | SBLGNT | `δασα` | -2 | Acts 9:11 | `Ταρσέα,` | Acts 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` | TCG_NT | `δασα` | -2 | ACT 9:11 | `Ταρσέα` | ACT 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` | TR_NT | `δασα` | -2 | ACT 9:11 | `Ταρσέα` | ACT 9:11 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` | BYZ_NT | `αιμα` | 2 | MAT 13:55 | `μαριαμ` | MAT 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` | SBLGNT | `αιμα` | 2 | Matt 13:55 | `Μαριὰμ` | Matt 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` | TCG_NT | `αιμα` | 2 | MAT 13:55 | `Μαριάμ,` | MAT 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` | TR_NT | `αιμα` | 2 | MAT 13:55 | `Μαριάμ` | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` | BYZ_NT | `αιμα` | 2 | MAT 13:55 | `μαριαμ` | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` | SBLGNT | `αιμα` | 2 | Matt 13:55 | `Μαριὰμ` | Matt 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` | TCG_NT | `αιμα` | 2 | MAT 13:55 | `Μαριάμ,` | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` | TR_NT | `αιμα` | 2 | MAT 13:55 | `Μαριάμ` | MAT 13:55 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` | BYZ_NT | `ναοσ` | 2 | 1CO 10:16 | `του` | 1CO 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` | SBLGNT | `ναοσ` | 2 | 1Cor 10:16 | `τοῦ` | 1Cor 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` | TCG_NT | `ναοσ` | 2 | 1CO 10:16 | `τοῦ` | 1CO 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` | TR_NT | `ναοσ` | 2 | 1CO 10:16 | `τοῦ` | 1CO 10:16 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` | BYZ_NT | `κινα` | 2 | 1JN 2:1 | `δικαιον` | 1JN 2:1; 1JN 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` | SBLGNT | `κινα` | 2 | 1John 2:1 | `δίκαιον,` | 1John 2:1; 1John 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` | TCG_NT | `κινα` | 2 | 1JN 2:1 | `δίκαιον.` | 1JN 2:1; 1JN 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` | TR_NT | `κινα` | 2 | 1JN 2:1 | `δίκαιον` | 1JN 2:1; 1JN 2:2 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` | BYZ_NT | `ελκη` | 2 | 1PE 5:13 | `συνεκλεκτη` | 1PE 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` | SBLGNT | `ελκη` | 2 | 1Pet 5:13 | `συνεκλεκτὴ` | 1Pet 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` | TCG_NT | `ελκη` | 2 | 1PE 5:13 | `συνεκλεκτὴ` | 1PE 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` | TR_NT | `ελκη` | 2 | 1PE 5:13 | `συνεκλεκτή` | 1PE 5:13 |
| 34 | greek_screening | `span_exact` | `θεοσ` | BYZ_NT | `θεοσ` | 2 | ROM 14:2 | `εσθιει` | ROM 14:2; ROM 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` | SBLGNT | `θεοσ` | 2 | Rom 14:2 | `ἐσθίει.` | Rom 14:2; Rom 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` | TCG_NT | `θεοσ` | 2 | ROM 14:2 | `ἐσθίει.` | ROM 14:2; ROM 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` | TR_NT | `θεοσ` | 2 | ROM 14:2 | `ἐσθίει` | ROM 14:2; ROM 14:3 |
| 35 | greek_screening | `span_exact` | `ιραν` | BYZ_NT | `ιραν` | -4 | MRK 14:48 | `αποκριθεισ` | MRK 14:48; MRK 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` | SBLGNT | `ιραν` | -4 | Mark 14:48 | `ἀποκριθεὶς` | Mark 14:48; Mark 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` | TCG_NT | `ιραν` | -4 | MRK 14:48 | `ἀποκριθεὶς` | MRK 14:48; MRK 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` | TR_NT | `ιραν` | -4 | MRK 14:48 | `ἀποκριθεὶς` | MRK 14:48; MRK 14:47 |
| 36 | greek_screening | `span_exact` | `νατο` | BYZ_NT | `νατο` | 7 | 1CO 1:27 | `μωρα` | 1CO 1:26; 1CO 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` | SBLGNT | `νατο` | 7 | 1Cor 1:27 | `μωρὰ` | 1Cor 1:26; 1Cor 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` | TCG_NT | `νατο` | 7 | 1CO 1:27 | `μωρὰ` | 1CO 1:26; 1CO 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` | TR_NT | `νατο` | 7 | 1CO 1:27 | `μωρὰ` | 1CO 1:26; 1CO 1:27 |
| 37 | greek_screening | `span_same_category` | `σαλα` | BYZ_NT | `σαλα` | 2 | ACT 7:42 | `ισραηλ` | ACT 7:42; ACT 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` | SBLGNT | `σαλα` | 2 | Acts 7:42 | `Ἰσραήλ;` | Acts 7:42; Acts 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` | TCG_NT | `σαλα` | 2 | ACT 7:42 | `Ἰσραήλ;` | ACT 7:42; ACT 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` | TR_NT | `σαλα` | 2 | ACT 7:42 | `Ἰσραήλ` | ACT 7:42; ACT 7:43 |
| 38 | greek_screening | `span_same_category` | `αδαμ` | BYZ_NT | `αδαμ` | 2 | GAL 4:27 | `ανδρα` | GAL 4:27; GAL 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` | SBLGNT | `αδαμ` | 2 | Gal 4:27 | `ἄνδρα.` | Gal 4:27; Gal 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` | TCG_NT | `αδαμ` | 2 | GAL 4:27 | `ἄνδρα.` | GAL 4:27; GAL 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` | TR_NT | `αδαμ` | 2 | GAL 4:27 | `ἄνδρα` | GAL 4:27; GAL 4:28 |
| 39 | greek_screening | `span_same_category` | `γαμερ` | BYZ_NT | `γαμερ` | -3 | 2CO 10:3 | `στρατευομεθα` | 2CO 10:4; 2CO 10:3 |
| 39 | greek_screening | `span_same_category` | `γαμερ` | SBLGNT | `γαμερ` | -3 | 2Cor 10:3 | `στρατευόμεθα—` | 2Cor 10:4; 2Cor 10:3 |
| 39 | greek_screening | `span_same_category` | `γαμερ` | TCG_NT | `γαμερ` | -3 | 2CO 10:3 | `στρατευόμεθα—` | 2CO 10:4; 2CO 10:3 |
| 39 | greek_screening | `span_same_category` | `γαμερ` | TR_NT | `γαμερ` | -3 | 2CO 10:3 | `στρατευόμεθα` | 2CO 10:4; 2CO 10:3 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` | BYZ_NT | `σαλα` | 2 | 1CO 10:18 | `ισραηλ` | 1CO 10:18 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` | SBLGNT | `σαλα` | 2 | 1Cor 10:18 | `Ἰσραὴλ` | 1Cor 10:18 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` | TCG_NT | `σαλα` | 2 | 1CO 10:18 | `Ἰσραὴλ` | 1CO 10:18 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` | TR_NT | `σαλα` | 2 | 1CO 10:18 | `Ἰσραὴλ` | 1CO 10:18 |
| 41 | greek_screening | `hidden_path_only` | `αμην` | BYZ_NT | `αμην` | 2 | 1CO 1:10 | `μη` | 1CO 1:10 |
| 41 | greek_screening | `hidden_path_only` | `αμην` | SBLGNT | `αμην` | 2 | 1Cor 1:10 | `μὴ` | 1Cor 1:10 |
| 41 | greek_screening | `hidden_path_only` | `αμην` | TCG_NT | `αμην` | 2 | 1CO 1:10 | `μὴ` | 1CO 1:10 |
| 41 | greek_screening | `hidden_path_only` | `αμην` | TR_NT | `αμην` | 2 | 1CO 1:10 | `μὴ` | 1CO 1:10 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` | BYZ_NT | `υιοσ` | 2 | 1CO 5:12 | `τουσ` | 1CO 5:12 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` | SBLGNT | `υιοσ` | 2 | 1Cor 5:12 | `τοὺς` | 1Cor 5:12 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` | TCG_NT | `υιοσ` | 2 | 1CO 5:12 | `τοὺς` | 1CO 5:12 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` | TR_NT | `υιοσ` | 2 | 1CO 5:12 | `τοὺς` | 1CO 5:12 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` | EBIBLE_WLC | `שממה` | 2 | MIC 1:7 | `שְׁמָמָ֑ה` | MIC 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` | MAM | `שממה` | 2 | Mic 1:7 | `שְׁמָמָ֑ה` | Mic 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` | MT_WLC | `שממה` | 2 | Mic 1:7 | `שְׁמָמָ֑ה` | Mic 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` | UHB | `שממה` | 2 | MIC 1:7 | `שְׁמָמָ֑ה` | MIC 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` | UXLC | `שממה` | 2 | Mic 1:7 | `שְׁמָמָ֑ה` | Mic 1:7 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` | EBIBLE_WLC | `יהוה` | 3 | 1CH 26:27 | `יְהוָֽה׃` | 1CH 26:27; 1CH 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` | MAM | `יהוה` | 3 | 1 Chr 26:27 | `יְהֹוָֽה׃` | 1 Chr 26:27; 1 Chr 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` | MT_WLC | `יהוה` | 3 | 1Chr 26:27 | `יְהוָֽה` | 1Chr 26:27; 1Chr 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` | UHB | `יהוה` | 3 | 1CH 26:27 | `יְהוָֽה׃` | 1CH 26:27; 1CH 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` | UXLC | `יהוה` | 3 | 1 Chr 26:27 | `יְהוָֽה׃` | 1 Chr 26:27; 1 Chr 26:28 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` | EBIBLE_WLC | `יהוה` | 3 | 1CH 28:20 | `בֵּית־יְהוָֽה׃` | 1CH 28:20; 1CH 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` | MAM | `יהוה` | 3 | 1 Chr 28:20 | `בֵּית־יְהֹוָֽה׃` | 1 Chr 28:20; 1 Chr 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` | MT_WLC | `יהוה` | 3 | 1Chr 28:20 | `יְהוָֽה` | 1Chr 28:20; 1Chr 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` | UHB | `יהוה` | 3 | 1CH 28:20 | `בֵּית־יְהוָֽה׃` | 1CH 28:20; 1CH 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` | UXLC | `יהוה` | 3 | 1 Chr 28:20 | `יְהוָֽה׃` | 1 Chr 28:20; 1 Chr 28:21 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | 175 more rows in CSV |

## Read

Every path row should spell the selected normalized term exactly. Center
word is recorded separately: it identifies the surface word at the center
offset, not a requirement that hidden path and surface word be identical.
Exact surface echo and hidden-path-only rows are both retained for review.
