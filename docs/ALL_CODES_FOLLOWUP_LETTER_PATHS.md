# All-Codes Follow-Up Letter Paths

Status: audit sheet for selected Hebrew and Greek all-codes follow-up rows; no claim.

This report reconstructs the actual ELS letter positions for the selected
Hebrew and Greek all-codes follow-up rows. Hidden-path-only rows are
audited the same way as rows with open-text surface echoes. This is an
audit sheet, not an added statistical test.

## Inputs

- Selected rows: `reports/all_codes_followup_selection/selected_rows.csv`

## Counts

- selected input rows: 83
- path summary rows: 310
- letter rows: 1,404
- sequence mismatches: 0
- selected by queue: `{'english_screening': 21, 'greek_screening': 21, 'hebrew_screening': 30, 'hebrew_theology': 11}`
- path rows by corpus: `{'BYZ_NT': 21, 'EBIBLE_WLC': 41, 'KJV': 21, 'MAM': 41, 'MT_WLC': 41, 'SBLGNT': 21, 'TCG_NT': 21, 'TR_NT': 21, 'UHB': 41, 'UXLC': 41}`
- path rows by bucket: `{'center_verse_exact': 30, 'center_verse_same_category': 45, 'center_verse_same_concept': 15, 'center_word_exact': 40, 'center_word_same_category': 45, 'center_word_same_concept': 15, 'hidden_path_only': 30, 'span_exact': 30, 'span_same_category': 45, 'span_same_concept': 15}`

## Path Summary

| Rank | Queue | Bucket | Term | Corpus | Sequence | Skip | Center | Center word | Path refs |
| ---: | --- | --- | --- | --- | --- | ---: | --- | --- | --- |
| 1 | english_screening | `center_word_exact` | `baal` | KJV | `baal` | 2 | 2KI 10:19 | `Baal,` | 2KI 10:19 |
| 2 | english_screening | `center_word_exact` | `heth` | KJV | `heth` | -2 | ACT 25:20 | `whether` | ACT 25:20 |
| 3 | english_screening | `center_word_exact` | `heth` | KJV | `heth` | -2 | DEU 24:14 | `whether` | DEU 24:14 |
| 4 | english_screening | `center_word_same_category` | `obed` | KJV | `obed` | 2 | 1CH 16:3 | `bread,` | 1CH 16:3 |
| 5 | english_screening | `center_word_same_category` | `obed` | KJV | `obed` | 2 | 1CH 16:3 | `bread,` | 1CH 16:3 |
| 6 | english_screening | `center_word_same_category` | `edom` | KJV | `edom` | -2 | 1CH 19:1 | `Ammon` | 1CH 19:1 |
| 7 | english_screening | `center_verse_exact` | `hand` | KJV | `hand` | -2 | 1CH 2:2 | `and` | 1CH 2:2 |
| 8 | english_screening | `center_verse_exact` | `heal` | KJV | `heal` | -2 | 1KI 1:6 | `displeased` | 1KI 1:6 |
| 9 | english_screening | `center_verse_exact` | `hand` | KJV | `hand` | -2 | 1KI 3:6 | `according` | 1KI 3:6 |
| 10 | english_screening | `center_verse_same_category` | `sign` | KJV | `sign` | -2 | 1CH 10:13 | `against` | 1CH 10:13 |
| 11 | english_screening | `center_verse_same_category` | `adar` | KJV | `adar` | -2 | 1CH 11:19 | `And` | 1CH 11:19; 1CH 11:18 |
| 12 | english_screening | `center_verse_same_category` | `adam` | KJV | `adam` | -2 | 1CH 12:31 | `and` | 1CH 12:31 |
| 13 | english_screening | `span_exact` | `thin` | KJV | `thin` | -2 | 1JN 2:5 | `him.` | 1JN 2:6; 1JN 2:5 |
| 14 | english_screening | `span_exact` | `rent` | KJV | `rent` | -2 | GEN 31:55 | `And` | GEN 31:55; GEN 31:54 |
| 15 | english_screening | `span_exact` | `wine` | KJV | `wine` | -2 | ISA 22:14 | `And` | ISA 22:14; ISA 22:13 |
| 16 | english_screening | `span_same_category` | `adar` | KJV | `adar` | -2 | 1SA 15:14 | `And` | 1SA 15:14; 1SA 15:13 |
| 17 | english_screening | `span_same_category` | `mash` | KJV | `mash` | -2 | 1SA 28:18 | `day.` | 1SA 28:19; 1SA 28:18 |
| 18 | english_screening | `span_same_category` | `adam` | KJV | `adam` | -2 | 1SA 9:22 | `And` | 1SA 9:22; 1SA 9:21 |
| 19 | english_screening | `hidden_path_only` | `heal` | KJV | `heal` | -2 | 1CH 10:11 | `Jabesh-gilead` | 1CH 10:11 |
| 20 | english_screening | `hidden_path_only` | `sign` | KJV | `sign` | -2 | 1CH 10:13 | `against` | 1CH 10:13 |
| 21 | english_screening | `hidden_path_only` | `cush` | KJV | `cush` | -2 | 1CH 10:4 | `these` | 1CH 10:4 |
| 22 | greek_screening | `center_word_exact` | `παισ` (pais; English: Servant) | BYZ_NT | `παισ` (pais; English: Servant) | -7 | LUK 22:64 | `παισασ` (paisas) | LUK 22:65; LUK 22:64 |
| 22 | greek_screening | `center_word_exact` | `παισ` (pais; English: Servant) | SBLGNT | `παισ` (pais; English: Servant) | -7 | Luke 22:64 | `παίσας` (paisas) | Luke 22:65; Luke 22:64 |
| 22 | greek_screening | `center_word_exact` | `παισ` (pais; English: Servant) | TCG_NT | `παισ` (pais; English: Servant) | -7 | LUK 22:64 | `παίσας` (paisas) | LUK 22:65; LUK 22:64 |
| 22 | greek_screening | `center_word_exact` | `παισ` (pais; English: Servant) | TR_NT | `παισ` (pais; English: Servant) | -7 | LUK 22:64 | `παίσας` (paisas) | LUK 22:65; LUK 22:64 |
| 23 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | BYZ_NT | `αννα` (anna; English: Hannah) | 8 | MAT 21:9 | `ωσαννα` (osanna; English: Hosanna) | MAT 21:9 |
| 23 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | SBLGNT | `αννα` (anna; English: Hannah) | 8 | Matt 21:9 | `Ὡσαννὰ` (osanna; English: Hosanna) | Matt 21:9 |
| 23 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | TCG_NT | `αννα` (anna; English: Hannah) | 8 | MAT 21:9 | `Ὡσαννὰ` (osanna; English: Hosanna) | MAT 21:9 |
| 23 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | TR_NT | `αννα` (anna; English: Hannah) | 8 | MAT 21:9 | `Ὡσαννὰ` (osanna; English: Hosanna) | MAT 21:9 |
| 24 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | BYZ_NT | `αννα` (anna; English: Hannah) | -8 | MAT 21:9 | `ωσαννα` (osanna; English: Hosanna) | MAT 21:9 |
| 24 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | SBLGNT | `αννα` (anna; English: Hannah) | -8 | Matt 21:9 | `Ὡσαννὰ` (osanna; English: Hosanna) | Matt 21:9 |
| 24 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | TCG_NT | `αννα` (anna; English: Hannah) | -8 | MAT 21:9 | `Ὡσαννὰ` (osanna; English: Hosanna) | MAT 21:9 |
| 24 | greek_screening | `center_word_exact` | `αννα` (anna; English: Hannah) | TR_NT | `αννα` (anna; English: Hannah) | -8 | MAT 21:9 | `Ὡσαννὰ` (osanna; English: Hosanna) | MAT 21:9 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | BYZ_NT | `λουδ` (loud; English: Lud) | -2 | PHP 2:7 | `δουλου` (doulou; English: servant) | PHP 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | SBLGNT | `λουδ` (loud; English: Lud) | -2 | Phil 2:7 | `δούλου` (doulou; English: servant) | Phil 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | TCG_NT | `λουδ` (loud; English: Lud) | -2 | PHP 2:7 | `δούλου` (doulou; English: servant) | PHP 2:7 |
| 25 | greek_screening | `center_word_same_category` | `λουδ` (loud; English: Lud) | TR_NT | `λουδ` (loud; English: Lud) | -2 | PHP 2:7 | `δούλου` (doulou; English: servant) | PHP 2:7 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | BYZ_NT | `ιωυαν` (Iouan; English: Javan) | -2 | 1PE 5:13 | `βαβυλωνι` (babuloni; English: Babylon) | 1PE 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | SBLGNT | `ιωυαν` (Iouan; English: Javan) | -2 | 1Pet 5:13 | `Βαβυλῶνι` (babuloni; English: Babylon) | 1Pet 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | TCG_NT | `ιωυαν` (Iouan; English: Javan) | -2 | 1PE 5:13 | `Βαβυλῶνι` (babuloni; English: Babylon) | 1PE 5:13 |
| 26 | greek_screening | `center_word_same_category` | `ιωυαν` (Iouan; English: Javan) | TR_NT | `ιωυαν` (Iouan; English: Javan) | -2 | 1PE 5:13 | `Βαβυλῶνι` (babuloni; English: Babylon) | 1PE 5:13 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | BYZ_NT | `ευαλ` (eual; English: Obal) | -3 | 1TI 5:14 | `βουλομαι` (boulomai; English: I want) | 1TI 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | SBLGNT | `ευαλ` (eual; English: Obal) | -3 | 1Tim 5:14 | `βούλομαι` (boulomai; English: I want) | 1Tim 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | TCG_NT | `ευαλ` (eual; English: Obal) | -3 | 1TI 5:14 | `Βούλομαι` (boulomai; English: I want) | 1TI 5:14 |
| 27 | greek_screening | `center_word_same_category` | `ευαλ` (eual; English: Obal) | TR_NT | `ευαλ` (eual; English: Obal) | -3 | 1TI 5:14 | `Βούλομαι` (boulomai; English: I want) | 1TI 5:14 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | BYZ_NT | `δασα` (dasa; English: Lasha) | -2 | ACT 9:11 | `ταρσεα` (tarsea; English: of Tarsus) | ACT 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | SBLGNT | `δασα` (dasa; English: Lasha) | -2 | Acts 9:11 | `Ταρσέα,` (tarsea; English: of Tarsus) | Acts 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | TCG_NT | `δασα` (dasa; English: Lasha) | -2 | ACT 9:11 | `Ταρσέα` (tarsea; English: of Tarsus) | ACT 9:11 |
| 28 | greek_screening | `center_verse_exact` | `δασα` (dasa; English: Lasha) | TR_NT | `δασα` (dasa; English: Lasha) | -2 | ACT 9:11 | `Ταρσέα` (tarsea; English: of Tarsus) | ACT 9:11 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | BYZ_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `μαριαμ` (mariam; English: Mary) | MAT 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | SBLGNT | `αιμα` (haima; English: Blood) | 2 | Matt 13:55 | `Μαριὰμ` (mariam; English: Mary) | Matt 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TCG_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ,` (mariam; English: Mary) | MAT 13:55 |
| 29 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ` (mariam; English: Mary) | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | BYZ_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `μαριαμ` (mariam; English: Mary) | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | SBLGNT | `αιμα` (haima; English: Blood) | 2 | Matt 13:55 | `Μαριὰμ` (mariam; English: Mary) | Matt 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TCG_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ,` (mariam; English: Mary) | MAT 13:55 |
| 30 | greek_screening | `center_verse_exact` | `αιμα` (haima; English: Blood) | TR_NT | `αιμα` (haima; English: Blood) | 2 | MAT 13:55 | `Μαριάμ` (mariam; English: Mary) | MAT 13:55 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | BYZ_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `του` (tou; English: of the) | 1CO 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | SBLGNT | `ναοσ` (naos; English: Temple) | 2 | 1Cor 10:16 | `τοῦ` (tou; English: of the) | 1Cor 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | TCG_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `τοῦ` (tou; English: of the) | 1CO 10:16 |
| 31 | greek_screening | `center_verse_same_category` | `ναοσ` (naos; English: Temple) | TR_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `τοῦ` (tou; English: of the) | 1CO 10:16 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | BYZ_NT | `κινα` (kina; English: China) | 2 | 1JN 2:1 | `δικαιον` (dikaion; English: righteous) | 1JN 2:1; 1JN 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | SBLGNT | `κινα` (kina; English: China) | 2 | 1John 2:1 | `δίκαιον,` (dikaion; English: righteous) | 1John 2:1; 1John 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | TCG_NT | `κινα` (kina; English: China) | 2 | 1JN 2:1 | `δίκαιον.` (dikaion; English: righteous) | 1JN 2:1; 1JN 2:2 |
| 32 | greek_screening | `center_verse_same_category` | `κινα` (kina; English: China) | TR_NT | `κινα` (kina; English: China) | 2 | 1JN 2:1 | `δίκαιον` (dikaion; English: righteous) | 1JN 2:1; 1JN 2:2 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | BYZ_NT | `ελκη` (elke; English: Boils) | 2 | 1PE 5:13 | `συνεκλεκτη` (suneklekte; English: co-elect) | 1PE 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | SBLGNT | `ελκη` (elke; English: Boils) | 2 | 1Pet 5:13 | `συνεκλεκτὴ` (suneklekte; English: co-elect) | 1Pet 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | TCG_NT | `ελκη` (elke; English: Boils) | 2 | 1PE 5:13 | `συνεκλεκτὴ` (suneklekte; English: co-elect) | 1PE 5:13 |
| 33 | greek_screening | `center_verse_same_category` | `ελκη` (elke; English: Boils) | TR_NT | `ελκη` (elke; English: Boils) | 2 | 1PE 5:13 | `συνεκλεκτή` (suneklekte; English: co-elect) | 1PE 5:13 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | BYZ_NT | `θεοσ` (theos; English: God) | 2 | ROM 14:2 | `εσθιει` (esthiei; English: eats) | ROM 14:2; ROM 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | SBLGNT | `θεοσ` (theos; English: God) | 2 | Rom 14:2 | `ἐσθίει.` (esthiei; English: eats) | Rom 14:2; Rom 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | TCG_NT | `θεοσ` (theos; English: God) | 2 | ROM 14:2 | `ἐσθίει.` (esthiei; English: eats) | ROM 14:2; ROM 14:3 |
| 34 | greek_screening | `span_exact` | `θεοσ` (theos; English: God) | TR_NT | `θεοσ` (theos; English: God) | 2 | ROM 14:2 | `ἐσθίει` (esthiei; English: eats) | ROM 14:2; ROM 14:3 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | BYZ_NT | `ιραν` (iran; English: Iran) | -4 | MRK 14:48 | `αποκριθεισ` (apokritheis; English: having answered) | MRK 14:48; MRK 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | SBLGNT | `ιραν` (iran; English: Iran) | -4 | Mark 14:48 | `ἀποκριθεὶς` (apokritheis; English: having answered) | Mark 14:48; Mark 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | TCG_NT | `ιραν` (iran; English: Iran) | -4 | MRK 14:48 | `ἀποκριθεὶς` (apokritheis; English: having answered) | MRK 14:48; MRK 14:47 |
| 35 | greek_screening | `span_exact` | `ιραν` (iran; English: Iran) | TR_NT | `ιραν` (iran; English: Iran) | -4 | MRK 14:48 | `ἀποκριθεὶς` (apokritheis; English: having answered) | MRK 14:48; MRK 14:47 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | BYZ_NT | `νατο` (nato; English: NATO) | 7 | 1CO 1:27 | `μωρα` (mora; English: foolish things) | 1CO 1:26; 1CO 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | SBLGNT | `νατο` (nato; English: NATO) | 7 | 1Cor 1:27 | `μωρὰ` (mora; English: foolish things) | 1Cor 1:26; 1Cor 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | TCG_NT | `νατο` (nato; English: NATO) | 7 | 1CO 1:27 | `μωρὰ` (mora; English: foolish things) | 1CO 1:26; 1CO 1:27 |
| 36 | greek_screening | `span_exact` | `νατο` (nato; English: NATO) | TR_NT | `νατο` (nato; English: NATO) | 7 | 1CO 1:27 | `μωρὰ` (mora; English: foolish things) | 1CO 1:26; 1CO 1:27 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | BYZ_NT | `σαλα` (Sala; English: Shelah) | 2 | ACT 7:42 | `ισραηλ` (israel; English: Israel) | ACT 7:42; ACT 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | SBLGNT | `σαλα` (Sala; English: Shelah) | 2 | Acts 7:42 | `Ἰσραήλ;` (israel; English: Israel) | Acts 7:42; Acts 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | TCG_NT | `σαλα` (Sala; English: Shelah) | 2 | ACT 7:42 | `Ἰσραήλ;` (israel; English: Israel) | ACT 7:42; ACT 7:43 |
| 37 | greek_screening | `span_same_category` | `σαλα` (Sala; English: Shelah) | TR_NT | `σαλα` (Sala; English: Shelah) | 2 | ACT 7:42 | `Ἰσραήλ` (israel; English: Israel) | ACT 7:42; ACT 7:43 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | BYZ_NT | `αδαμ` (adam; English: Adam) | 2 | GAL 4:27 | `ανδρα` (andra; English: man) | GAL 4:27; GAL 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | SBLGNT | `αδαμ` (adam; English: Adam) | 2 | Gal 4:27 | `ἄνδρα.` (andra; English: man) | Gal 4:27; Gal 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | TCG_NT | `αδαμ` (adam; English: Adam) | 2 | GAL 4:27 | `ἄνδρα.` (andra; English: man) | GAL 4:27; GAL 4:28 |
| 38 | greek_screening | `span_same_category` | `αδαμ` (adam; English: Adam) | TR_NT | `αδαμ` (adam; English: Adam) | 2 | GAL 4:27 | `ἄνδρα` (andra; English: man) | GAL 4:27; GAL 4:28 |
| 39 | greek_screening | `span_same_category` | `ναοσ` (naos; English: Temple) | BYZ_NT | `ναοσ` (naos; English: Temple) | -3 | HEB 10:30 | `οιδαμεν` (oidamen; English: we know) | HEB 10:30; HEB 10:29 |
| 39 | greek_screening | `span_same_category` | `ναοσ` (naos; English: Temple) | SBLGNT | `ναοσ` (naos; English: Temple) | -3 | Heb 10:30 | `οἴδαμεν` (oidamen; English: we know) | Heb 10:30; Heb 10:29 |
| 39 | greek_screening | `span_same_category` | `ναοσ` (naos; English: Temple) | TCG_NT | `ναοσ` (naos; English: Temple) | -3 | HEB 10:30 | `Οἴδαμεν` (oidamen; English: we know) | HEB 10:30; HEB 10:29 |
| 39 | greek_screening | `span_same_category` | `ναοσ` (naos; English: Temple) | TR_NT | `ναοσ` (naos; English: Temple) | -3 | HEB 10:30 | `Οἴδαμεν` (oidamen; English: we know) | HEB 10:30; HEB 10:29 |
| 40 | greek_screening | `hidden_path_only` | `ναοσ` (naos; English: Temple) | BYZ_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `του` (tou; English: of the) | 1CO 10:16 |
| 40 | greek_screening | `hidden_path_only` | `ναοσ` (naos; English: Temple) | SBLGNT | `ναοσ` (naos; English: Temple) | 2 | 1Cor 10:16 | `τοῦ` (tou; English: of the) | 1Cor 10:16 |
| 40 | greek_screening | `hidden_path_only` | `ναοσ` (naos; English: Temple) | TCG_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `τοῦ` (tou; English: of the) | 1CO 10:16 |
| 40 | greek_screening | `hidden_path_only` | `ναοσ` (naos; English: Temple) | TR_NT | `ναοσ` (naos; English: Temple) | 2 | 1CO 10:16 | `τοῦ` (tou; English: of the) | 1CO 10:16 |
| 41 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | BYZ_NT | `σαλα` (Sala; English: Shelah) | 2 | 1CO 10:18 | `ισραηλ` (israel; English: Israel) | 1CO 10:18 |
| 41 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | SBLGNT | `σαλα` (Sala; English: Shelah) | 2 | 1Cor 10:18 | `Ἰσραὴλ` (israel; English: Israel) | 1Cor 10:18 |
| 41 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | TCG_NT | `σαλα` (Sala; English: Shelah) | 2 | 1CO 10:18 | `Ἰσραὴλ` (israel; English: Israel) | 1CO 10:18 |
| 41 | greek_screening | `hidden_path_only` | `σαλα` (Sala; English: Shelah) | TR_NT | `σαλα` (Sala; English: Shelah) | 2 | 1CO 10:18 | `Ἰσραὴλ` (israel; English: Israel) | 1CO 10:18 |
| 42 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | BYZ_NT | `αμην` (amen; English: Amen) | 2 | 1CO 1:10 | `μη` (me; English: not) | 1CO 1:10 |
| 42 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | SBLGNT | `αμην` (amen; English: Amen) | 2 | 1Cor 1:10 | `μὴ` (me; English: not) | 1Cor 1:10 |
| 42 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | TCG_NT | `αμην` (amen; English: Amen) | 2 | 1CO 1:10 | `μὴ` (me; English: not) | 1CO 1:10 |
| 42 | greek_screening | `hidden_path_only` | `αμην` (amen; English: Amen) | TR_NT | `αμην` (amen; English: Amen) | 2 | 1CO 1:10 | `μὴ` (me; English: not) | 1CO 1:10 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shemamah; English: Desolation) | EBIBLE_WLC | `שממה` (shemamah; English: Desolation) | 2 | MIC 1:7 | `שְׁמָמָ֑ה` (shemamah; English: desolation) | MIC 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shemamah; English: Desolation) | MAM | `שממה` (shemamah; English: Desolation) | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shemamah; English: desolation) | Mic 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shemamah; English: Desolation) | MT_WLC | `שממה` (shemamah; English: Desolation) | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shemamah; English: desolation) | Mic 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shemamah; English: Desolation) | UHB | `שממה` (shemamah; English: Desolation) | 2 | MIC 1:7 | `שְׁמָמָ֑ה` (shemamah; English: desolation) | MIC 1:7 |
| 43 | hebrew_screening | `center_word_exact` | `שממה` (shemamah; English: Desolation) | UXLC | `שממה` (shemamah; English: Desolation) | 2 | Mic 1:7 | `שְׁמָמָ֑ה` (shemamah; English: desolation) | Mic 1:7 |
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
| ... | ... | ... | ... | ... | ... | ... | ... | ... | 190 more rows in CSV |

## Read

Every path row should spell the selected normalized term exactly. Center
word is recorded separately: it identifies the surface word at the center
offset, not a requirement that hidden path and surface word be identical.
Exact surface echo and hidden-path-only rows are both retained for review.
