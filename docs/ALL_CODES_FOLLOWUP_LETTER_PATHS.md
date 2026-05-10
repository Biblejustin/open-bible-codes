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
| 22 | greek_screening | `center_word_exact` | `νατο` (nato; English: NATO) | BYZ_NT | `νατο` (nato; English: NATO) | 8 | ROM 5:10 | `θανατου` (thanatou) | ROM 5:10 |
| 22 | greek_screening | `center_word_exact` | `νατο` (nato; English: NATO) | SBLGNT | `νατο` (nato; English: NATO) | 8 | Rom 5:10 | `θανάτου` (thanatou) | Rom 5:10 |
| 22 | greek_screening | `center_word_exact` | `νατο` (nato; English: NATO) | TCG_NT | `νατο` (nato; English: NATO) | 8 | ROM 5:10 | `θανάτου` (thanatou) | ROM 5:10 |
| 22 | greek_screening | `center_word_exact` | `νατο` (nato; English: NATO) | TR_NT | `νατο` (nato; English: NATO) | 8 | ROM 5:10 | `θανάτου` (thanatou) | ROM 5:10 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` (naos; English: Temple) | BYZ_NT | `ναοσ` (naos; English: Temple) | -9 | MAT 23:17 | `ναοσ` (naos; English: temple) | MAT 23:17 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` (naos; English: Temple) | SBLGNT | `ναοσ` (naos; English: Temple) | -9 | Matt 23:17 | `ναὸς` (naos; English: temple) | Matt 23:17 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` (naos; English: Temple) | TCG_NT | `ναοσ` (naos; English: Temple) | -9 | MAT 23:17 | `ναὸς` (naos; English: temple) | MAT 23:17 |
| 23 | greek_screening | `center_word_exact` | `ναοσ` (naos; English: Temple) | TR_NT | `ναοσ` (naos; English: Temple) | -9 | MAT 23:17 | `ναὸς` (naos; English: temple) | MAT 23:17 |
| 24 | greek_screening | `center_word_exact` | `αιμα` (haima; English: Blood) | BYZ_NT | `αιμα` (haima; English: Blood) | -10 | REV 19:13 | `αιματι` (aimati) | REV 19:13 |
| 24 | greek_screening | `center_word_exact` | `αιμα` (haima; English: Blood) | SBLGNT | `αιμα` (haima; English: Blood) | -10 | Rev 19:13 | `αἵματι,` (aimati) | Rev 19:13 |
| 24 | greek_screening | `center_word_exact` | `αιμα` (haima; English: Blood) | TCG_NT | `αιμα` (haima; English: Blood) | -10 | REV 19:13 | `αἵματι,` (aimati) | REV 19:13 |
| 24 | greek_screening | `center_word_exact` | `αιμα` (haima; English: Blood) | TR_NT | `αιμα` (haima; English: Blood) | -10 | REV 19:13 | `αἵματι` (aimati) | REV 19:13 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | BYZ_NT | `λουδ` (loud; English: Lud) | -2 | PHP 2:7 | `δουλου` (doulou) | PHP 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | SBLGNT | `λουδ` (loud; English: Lud) | -2 | Phil 2:7 | `δούλου` (doulou) | Phil 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | TCG_NT | `λουδ` (loud; English: Lud) | -2 | PHP 2:7 | `δούλου` (doulou) | PHP 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | TR_NT | `λουδ` (loud; English: Lud) | -2 | PHP 2:7 | `δούλου` (doulou) | PHP 2:7 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | BYZ_NT | `ιωυαν` (Iouan; English: Javan) | -2 | 1PE 5:13 | `βαβυλωνι` (babuloni) | 1PE 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | SBLGNT | `ιωυαν` (Iouan; English: Javan) | -2 | 1Pet 5:13 | `Βαβυλῶνι` (babuloni) | 1Pet 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | TCG_NT | `ιωυαν` (Iouan; English: Javan) | -2 | 1PE 5:13 | `Βαβυλῶνι` (babuloni) | 1PE 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | TR_NT | `ιωυαν` (Iouan; English: Javan) | -2 | 1PE 5:13 | `Βαβυλῶνι` (babuloni) | 1PE 5:13 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | BYZ_NT | `ευαλ` (eual; English: Obal) | -3 | 1TI 5:14 | `βουλομαι` (boulomai) | 1TI 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | SBLGNT | `ευαλ` (eual; English: Obal) | -3 | 1Tim 5:14 | `βούλομαι` (boulomai) | 1Tim 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | TCG_NT | `ευαλ` (eual; English: Obal) | -3 | 1TI 5:14 | `Βούλομαι` (boulomai) | 1TI 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | TR_NT | `ευαλ` (eual; English: Obal) | -3 | 1TI 5:14 | `Βούλομαι` (boulomai) | 1TI 5:14 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | BYZ_NT | `δασα` (dasa; English: Lasha) | -2 | ACT 9:11 | `ταρσεα` (tarsea) | ACT 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | SBLGNT | `δασα` (dasa; English: Lasha) | -2 | Acts 9:11 | `Ταρσέα,` (tarsea) | Acts 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | TCG_NT | `δασα` (dasa; English: Lasha) | -2 | ACT 9:11 | `Ταρσέα` (tarsea) | ACT 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | TR_NT | `δασα` (dasa; English: Lasha) | -2 | ACT 9:11 | `Ταρσέα` (tarsea) | ACT 9:11 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | BYZ_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `μαριαμ` (mariam) | MAT 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | SBLGNT | `αιμα` (haima; English: Blood) | 2 | Matt 13:55 | `Μαριὰμ` (mariam) | Matt 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TCG_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ,` (mariam) | MAT 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ` (mariam) | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | BYZ_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `μαριαμ` (mariam) | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | SBLGNT | `αιμα` (haima; English: Blood) | 2 | Matt 13:55 | `Μαριὰμ` (mariam) | Matt 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TCG_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ,` (mariam) | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ` (mariam) | MAT 13:55 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | BYZ_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `του` (tou) | 1CO 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | SBLGNT | `ναοσ` (naos; English: Temple) | 2 | 1Cor 10:16 | `τοῦ` (tou) | 1Cor 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | TCG_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `τοῦ` (tou) | 1CO 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | TR_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `τοῦ` (tou) | 1CO 10:16 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | BYZ_NT | `κινα` (kina; English: China) | 2 | 1JN 2:1 | `δικαιον` (dikaion) | 1JN 2:1; 1JN 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | SBLGNT | `κινα` (kina; English: China) | 2 | 1John 2:1 | `δίκαιον,` (dikaion) | 1John 2:1; 1John 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | TCG_NT | `κινα` (kina; English: China) | 2 | 1JN 2:1 | `δίκαιον.` (dikaion) | 1JN 2:1; 1JN 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | TR_NT | `κινα` (kina; English: China) | 2 | 1JN 2:1 | `δίκαιον` (dikaion) | 1JN 2:1; 1JN 2:2 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | BYZ_NT | `ελκη` (elke; English: Boils) | 2 | 1PE 5:13 | `συνεκλεκτη` (suneklekte) | 1PE 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | SBLGNT | `ελκη` (elke; English: Boils) | 2 | 1Pet 5:13 | `συνεκλεκτὴ` (suneklekte) | 1Pet 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | TCG_NT | `ελκη` (elke; English: Boils) | 2 | 1PE 5:13 | `συνεκλεκτὴ` (suneklekte) | 1PE 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | TR_NT | `ελκη` (elke; English: Boils) | 2 | 1PE 5:13 | `συνεκλεκτή` (suneklekte) | 1PE 5:13 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | BYZ_NT | `θεοσ` (theos; English: God) | 2 | ROM 14:2 | `εσθιει` (esthiei) | ROM 14:2; ROM 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | SBLGNT | `θεοσ` (theos; English: God) | 2 | Rom 14:2 | `ἐσθίει.` (esthiei) | Rom 14:2; Rom 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | TCG_NT | `θεοσ` (theos; English: God) | 2 | ROM 14:2 | `ἐσθίει.` (esthiei) | ROM 14:2; ROM 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | TR_NT | `θεοσ` (theos; English: God) | 2 | ROM 14:2 | `ἐσθίει` (esthiei) | ROM 14:2; ROM 14:3 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | BYZ_NT | `ιραν` (iran; English: Iran) | -4 | MRK 14:48 | `αποκριθεισ` (apokritheis) | MRK 14:48; MRK 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | SBLGNT | `ιραν` (iran; English: Iran) | -4 | Mark 14:48 | `ἀποκριθεὶς` (apokritheis) | Mark 14:48; Mark 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | TCG_NT | `ιραν` (iran; English: Iran) | -4 | MRK 14:48 | `ἀποκριθεὶς` (apokritheis) | MRK 14:48; MRK 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | TR_NT | `ιραν` (iran; English: Iran) | -4 | MRK 14:48 | `ἀποκριθεὶς` (apokritheis) | MRK 14:48; MRK 14:47 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | BYZ_NT | `νατο` (nato; English: NATO) | 7 | 1CO 1:27 | `μωρα` (mora) | 1CO 1:26; 1CO 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | SBLGNT | `νατο` (nato; English: NATO) | 7 | 1Cor 1:27 | `μωρὰ` (mora) | 1Cor 1:26; 1Cor 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | TCG_NT | `νατο` (nato; English: NATO) | 7 | 1CO 1:27 | `μωρὰ` (mora) | 1CO 1:26; 1CO 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | TR_NT | `νατο` (nato; English: NATO) | 7 | 1CO 1:27 | `μωρὰ` (mora) | 1CO 1:26; 1CO 1:27 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | BYZ_NT | `σαλα` (Sala; English: Shelah) | 2 | ACT 7:42 | `ισραηλ` (israel; English: Israel) | ACT 7:42; ACT 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | SBLGNT | `σαλα` (Sala; English: Shelah) | 2 | Acts 7:42 | `Ἰσραήλ;` (israel; English: Israel) | Acts 7:42; Acts 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | TCG_NT | `σαλα` (Sala; English: Shelah) | 2 | ACT 7:42 | `Ἰσραήλ;` (israel; English: Israel) | ACT 7:42; ACT 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | TR_NT | `σαλα` (Sala; English: Shelah) | 2 | ACT 7:42 | `Ἰσραήλ` (israel; English: Israel) | ACT 7:42; ACT 7:43 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | BYZ_NT | `αδαμ` (adam; English: Adam) | 2 | GAL 4:27 | `ανδρα` (andra) | GAL 4:27; GAL 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | SBLGNT | `αδαμ` (adam; English: Adam) | 2 | Gal 4:27 | `ἄνδρα.` (andra) | Gal 4:27; Gal 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | TCG_NT | `αδαμ` (adam; English: Adam) | 2 | GAL 4:27 | `ἄνδρα.` (andra) | GAL 4:27; GAL 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | TR_NT | `αδαμ` (adam; English: Adam) | 2 | GAL 4:27 | `ἄνδρα` (andra) | GAL 4:27; GAL 4:28 |
| 39 | greek_screening | `span_same_category` | `γαμερ` (gamer; English: Gomer) | BYZ_NT | `γαμερ` (gamer; English: Gomer) | -3 | 2CO 10:3 | `στρατευομεθα` (strateuometha) | 2CO 10:4; 2CO 10:3 |
| 39 | greek_screening | `span_same_category` | `γαμερ` (gamer; English: Gomer) | SBLGNT | `γαμερ` (gamer; English: Gomer) | -3 | 2Cor 10:3 | `στρατευόμεθα—` (strateuometha) | 2Cor 10:4; 2Cor 10:3 |
| 39 | greek_screening | `span_same_category` | `γαμερ` (gamer; English: Gomer) | TCG_NT | `γαμερ` (gamer; English: Gomer) | -3 | 2CO 10:3 | `στρατευόμεθα—` (strateuometha) | 2CO 10:4; 2CO 10:3 |
| 39 | greek_screening | `span_same_category` | `γαμερ` (gamer; English: Gomer) | TR_NT | `γαμερ` (gamer; English: Gomer) | -3 | 2CO 10:3 | `στρατευόμεθα` (strateuometha) | 2CO 10:4; 2CO 10:3 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | BYZ_NT | `σαλα` (Sala; English: Shelah) | 2 | 1CO 10:18 | `ισραηλ` (israel; English: Israel) | 1CO 10:18 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | SBLGNT | `σαλα` (Sala; English: Shelah) | 2 | 1Cor 10:18 | `Ἰσραὴλ` (israel; English: Israel) | 1Cor 10:18 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | TCG_NT | `σαλα` (Sala; English: Shelah) | 2 | 1CO 10:18 | `Ἰσραὴλ` (israel; English: Israel) | 1CO 10:18 |
| 40 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | TR_NT | `σαλα` (Sala; English: Shelah) | 2 | 1CO 10:18 | `Ἰσραὴλ` (israel; English: Israel) | 1CO 10:18 |
| 41 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | BYZ_NT | `αμην` (amen; English: Amen) | 2 | 1CO 1:10 | `μη` (me) | 1CO 1:10 |
| 41 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | SBLGNT | `αμην` (amen; English: Amen) | 2 | 1Cor 1:10 | `μὴ` (me) | 1Cor 1:10 |
| 41 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | TCG_NT | `αμην` (amen; English: Amen) | 2 | 1CO 1:10 | `μὴ` (me) | 1CO 1:10 |
| 41 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | TR_NT | `αμην` (amen; English: Amen) | 2 | 1CO 1:10 | `μὴ` (me) | 1CO 1:10 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` (huios; English: Son) | BYZ_NT | `υιοσ` (huios; English: Son) | 2 | 1CO 5:12 | `τουσ` (tous) | 1CO 5:12 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` (huios; English: Son) | SBLGNT | `υιοσ` (huios; English: Son) | 2 | 1Cor 5:12 | `τοὺς` (tous) | 1Cor 5:12 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` (huios; English: Son) | TCG_NT | `υιοσ` (huios; English: Son) | 2 | 1CO 5:12 | `τοὺς` (tous) | 1CO 5:12 |
| 42 | greek_screening | `hidden_path_only` | `υιοσ` (huios; English: Son) | TR_NT | `υιοσ` (huios; English: Son) | 2 | 1CO 5:12 | `τοὺς` (tous) | 1CO 5:12 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shmmh; English: Desolation) | EBIBLE_WLC | `שממה` (shmmh; English: Desolation) | 2 | MIC 1:7 | `שְׁמָמָ֑ה` (shmmh; English: Desolation) | MIC 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shmmh; English: Desolation) | MAM | `שממה` (shmmh; English: Desolation) | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shmmh; English: Desolation) | Mic 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shmmh; English: Desolation) | MT_WLC | `שממה` (shmmh; English: Desolation) | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shmmh; English: Desolation) | Mic 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shmmh; English: Desolation) | UHB | `שממה` (shmmh; English: Desolation) | 2 | MIC 1:7 | `שְׁמָמָ֑ה` (shmmh; English: Desolation) | MIC 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shmmh; English: Desolation) | UXLC | `שממה` (shmmh; English: Desolation) | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shmmh; English: Desolation) | Mic 1:7 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | 3 | 1CH 26:27 | `יְהוָֽה׃` (YHWH; English: YHWH) | 1CH 26:27; 1CH 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | MAM | `יהוה` (YHWH; English: YHWH) | 3 | 1 Chr 26:27 | `יְהֹוָֽה׃` (YHWH; English: YHWH) | 1 Chr 26:27; 1 Chr 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | MT_WLC | `יהוה` (YHWH; English: YHWH) | 3 | 1Chr 26:27 | `יְהוָֽה` (YHWH; English: YHWH) | 1Chr 26:27; 1Chr 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UHB | `יהוה` (YHWH; English: YHWH) | 3 | 1CH 26:27 | `יְהוָֽה׃` (YHWH; English: YHWH) | 1CH 26:27; 1CH 26:28 |
| 44 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `יהוה` (YHWH; English: YHWH) | 3 | 1 Chr 26:27 | `יְהוָֽה׃` (YHWH; English: YHWH) | 1 Chr 26:27; 1 Chr 26:28 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | EBIBLE_WLC | `יהוה` (YHWH; English: YHWH) | 3 | 1CH 28:20 | `בֵּית־יְהוָֽה׃` (beit YHWH; English: house of YHWH) | 1CH 28:20; 1CH 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | MAM | `יהוה` (YHWH; English: YHWH) | 3 | 1 Chr 28:20 | `בֵּית־יְהֹוָֽה׃` (beit YHWH; English: house of YHWH) | 1 Chr 28:20; 1 Chr 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | MT_WLC | `יהוה` (YHWH; English: YHWH) | 3 | 1Chr 28:20 | `יְהוָֽה` (YHWH; English: YHWH) | 1Chr 28:20; 1Chr 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UHB | `יהוה` (YHWH; English: YHWH) | 3 | 1CH 28:20 | `בֵּית־יְהוָֽה׃` (beit YHWH; English: house of YHWH) | 1CH 28:20; 1CH 28:21 |
| 45 | hebrew_screening | `center_word_exact` | `יהוה` (YHWH; English: YHWH) | UXLC | `יהוה` (YHWH; English: YHWH) | 3 | 1 Chr 28:20 | `יְהוָֽה׃` (YHWH; English: YHWH) | 1 Chr 28:20; 1 Chr 28:21 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | 175 more rows in CSV |

## Read

Every path row should spell the selected normalized term exactly. Center
word is recorded separately: it identifies the surface word at the center
offset, not a requirement that hidden path and surface word be identical.
Exact surface echo and hidden-path-only rows are both retained for review.
