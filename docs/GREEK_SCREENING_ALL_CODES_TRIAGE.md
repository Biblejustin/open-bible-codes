# Greek Screening All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/greek_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/greek_screening_all_codes/surface_all_codes_summary.csv`
- Report DB: `reports/db/open_bible_codes.duckdb`
- Queue CSV: `reports/greek_screening_all_codes/triage_queue.csv`
- Corpora: `BYZ_NT, SBLGNT, TCG_NT, TR_NT`

## Counts

| Metric | Count |
| --- | ---: |
| Raw rows scanned | 352,681 |
| Queue rows | 700 |
| `center_word_exact` queue rows | 100 |
| `center_word_same_concept` queue rows | 0 |
| `center_word_same_category` queue rows | 100 |
| `center_verse_exact` queue rows | 100 |
| `center_verse_same_concept` queue rows | 0 |
| `center_verse_same_category` queue rows | 100 |
| `span_exact` queue rows | 100 |
| `span_same_concept` queue rows | 0 |
| `span_same_category` queue rows | 100 |
| `hidden_path_only` queue rows | 100 |

## Top Queue Rows

### center_word_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 8 | 25 | Rom 5:10 | `θανατου` (thanatou) |  |
| 2 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -9 | 28 | Matt 23:17 | `ναοσ` (naos; English: temple) |  |
| 3 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Rev 19:13 | `αιματι` (aimati) |  |
| 4 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Rev 19:13 | `αιματι` (aimati) |  |
| 5 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 13 | 40 | 1Pet 1:19 | `αιματι` (aimati) |  |
| 6 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 13 | 40 | 1Pet 1:19 | `αιματι` (aimati) |  |
| 7 | all_source | `god_g` `θεοσ` (theos; English: God) | God | -21 | 64 | 2Cor 6:16 | `θεοσ` (theos; English: God) |  |
| 8 | all_source | `wisdom_g` `σοφια` (sophia; English: Wisdom) | Wisdom | -24 | 97 | Acts 6:10 | `σοφια` (sophia) |  |
| 9 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -50 | 151 | Rom 8:6 | `θανατοσ` (thanatos) |  |
| 10 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -54 | 163 | Heb 5:7 | `θανατου` (thanatou) |  |
| 11 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 54 | 163 | Rev 20:13 | `θανατοσ` (thanatos) |  |
| 12 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 64 | 193 | Heb 9:15 | `θανατου` (thanatou) |  |
| 13 | all_source | `god_g` `θεοσ` (theos; English: God) | God | -66 | 199 | Acts 10:38 | `θεοσ` (theos; English: God) |  |
| 14 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 72 | 217 | Heb 9:15 | `θανατου` (thanatou) |  |
| 15 | multi_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 3 | 10 | Rev 21:8 | `θανατοσ` (thanatos) |  |
| 16 | multi_source | `son_g` `υιοσ` (huios; English: Son) | Son | -5 | 16 | John 1:42 | `υιοσ` (huios; English: son) |  |
| 17 | multi_source | `son_g` `υιοσ` (huios; English: Son) | Son | 5 | 16 | Luke 14:5 | `υιοσ` (huios; English: son) |  |
| 18 | multi_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 14 | 43 | Heb 2:14 | `θανατου` (thanatou) |  |
| 19 | multi_source | `son_g` `υιοσ` (huios; English: Son) | Son | 14 | 43 | Luke 11:11 | `υιοσ` (huios; English: son) |  |
| 20 | multi_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -17 | 52 | 2Cor 3:7 | `θανατου` (thanatou) |  |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `lud_g` `λουδ` (loud; English: Lud) | Lud | -2 | 7 | Phil 2:7 | `δουλου` (doulou) |  |
| 2 | all_source | `javan_g` `ιωυαν` (Iouan; English: Javan) | Javan | -2 | 9 | 1Pet 5:13 | `βαβυλωνι` (babuloni) |  |
| 3 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -3 | 10 | 1Tim 5:14 | `βουλομαι` (boulomai) |  |
| 4 | all_source | `zion_g` `σιων` (Sion; English: Zion) | Zion | 3 | 10 | Acts 7:12 | `ιακωβ` (iakob) |  |
| 5 | all_source | `eber_g` `εβερ` (eber; English: Eber) | Eber | 4 | 13 | Luke 22:42 | `βουλει` (boulei) |  |
| 6 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | 4 | 13 | Luke 3:27 | `σαλαθιηλ` (salathiel) |  |
| 7 | all_source | `china_g` `κινα` (kina; English: China) | China | -4 | 13 | Mark 12:3 | `εδειραν` (edeiran) |  |
| 8 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | Matt 4:15 | `ζαβουλων` (zaboulon) |  |
| 9 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | 5 | 16 | 2Pet 1:10 | `σπουδασατε` (spoudasate) |  |
| 10 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 6 | 19 | John 7:6 | `ιησουσ` (Iesous; English: Jesus/Joshua) |  |
| 11 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -6 | 19 | Luke 10:22 | `βουληται` (bouletai) |  |
| 12 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -6 | 19 | Luke 1:80 | `ισραηλ` (israel) |  |
| 13 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -6 | 19 | Matt 11:27 | `βουληται` (bouletai) |  |
| 14 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | 6 | 19 | Rom 16:10 | `αριστοβουλου` (aristoboulou) |  |
| 15 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -6 | 19 | Rom 16:10 | `αριστοβουλου` (aristoboulou) |  |
| 16 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 7 | 22 | Acts 7:11 | `θλιψισ` (thlipsis) |  |
| 17 | all_source | `eber_g` `εβερ` (eber; English: Eber) | Eber | 7 | 22 | Matt 1:17 | `βαβυλωνοσ` (babulonos) |  |
| 18 | all_source | `china_g` `κινα` (kina; English: China) | China | -7 | 22 | Rev 6:8 | `θανατοσ` (thanatos) |  |
| 19 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 8 | 25 | 1John 2:22 | `χριστοσ` (Christos; English: Christ) |  |
| 20 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 9 | 28 | Rev 18:10 | `βαβυλων` (babulon) |  |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | Acts 9:11 | `ταρσεα` (tarsea) |  |
| 2 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 2 | 7 | Matt 13:55 | `μαριαμ` (mariam) |  |
| 3 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 2 | 7 | Matt 13:55 | `μαριαμ` (mariam) |  |
| 4 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | -3 | 10 | Acts 23:6 | `φαρισαιοσ` (pharisaios) |  |
| 5 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 3 | 10 | Eph 4:17 | `εν` (en) |  |
| 6 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 3 | 10 | Eph 4:17 | `εν` (en) |  |
| 7 | all_source | `amen_g` `αμην` (amen; English: Amen) | Amen | -3 | 10 | John 5:24 | `ζωην` (zoen) |  |
| 8 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -3 | 10 | Rev 2:10 | `στεφανον` (stephanon) |  |
| 9 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | 1Cor 9:22 | `τοισ` (tois) |  |
| 10 | all_source | `god_g` `θεοσ` (theos; English: God) | God | 4 | 13 | 1John 4:9 | `εισ` (eis) |  |
| 11 | all_source | `zion_g` `σιων` (Sion; English: Zion) | Zion | -4 | 13 | Acts 19:34 | `επι` (epi) |  |
| 12 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -4 | 13 | Col 1:11 | `δυναμουμενοι` (dunamoumenoi) |  |
| 13 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -4 | 13 | Col 1:11 | `δυναμουμενοι` (dunamoumenoi) |  |
| 14 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 4 | 13 | Gal 4:7 | `ει` (ei) |  |
| 15 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 4 | 13 | John 1:42 | `σιμων` (simon) |  |
| 16 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | Luke 3:31 | `ματταθα` (mattatha) |  |
| 17 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | Matt 4:18 | `αυτου` (autou) |  |
| 18 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | Rom 1:32 | `πρασσοντεσ` (prassontes) |  |
| 19 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 5 | 16 | 1Cor 15:17 | `αμαρτιαισ` (amartiais) |  |
| 20 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 5 | 16 | 1Cor 15:17 | `αμαρτιαισ` (amartiais) |  |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | 1Cor 10:16 | `του` (tou) |  |
| 2 | all_source | `china_g` `κινα` (kina; English: China) | China | 2 | 7 | 1John 2:1 | `δικαιον` (dikaion) |  |
| 3 | all_source | `boils_g` `ελκη` (elke; English: Boils) | Boils | 2 | 7 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte) |  |
| 4 | all_source | `sores_g` `ελκη` (elke; English: Sores) | Sores | 2 | 7 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte) |  |
| 5 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | 1Tim 5:13 | `μανθανουσι` (manthanousi) |  |
| 6 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | 2 | 7 | 1Tim 6:9 | `και` (kai) |  |
| 7 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 1:22 | `καρδιαισ` (kardiais) |  |
| 8 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 3:2 | `καρδιαισ` (kardiais) |  |
| 9 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 4:6 | `καρδιαισ` (kardiais) |  |
| 10 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 7:3 | `καρδιαισ` (kardiais) |  |
| 11 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Tim 1:10 | `αφθαρσιαν` (aphtharsian) |  |
| 12 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | 2 | 7 | 2Tim 1:9 | `εργα` (erga) |  |
| 13 | all_source | `adam_g` `αδαμ` (adam; English: Adam) | Adam | 2 | 7 | Acts 13:22 | `καρδιαν` (kardian) |  |
| 14 | all_source | `iran_g` `ιραν` (iran; English: Iran) | Iran | -2 | 7 | Acts 15:23 | `χαιρειν` (chairein) |  |
| 15 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | Acts 16:22 | `και` (kai) |  |
| 16 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -2 | 7 | Acts 7:58 | `ποδασ` (podas) |  |
| 17 | all_source | `god_g` `θεοσ` (theos; English: God) | God | -2 | 7 | Acts 9:11 | `πορευθητι` (poreutheti) |  |
| 18 | all_source | `china_g` `κινα` (kina; English: China) | China | 2 | 7 | Heb 11:19 | `εν` (en) |  |
| 19 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | Heb 2:17 | `τοισ` (tois) |  |
| 20 | all_source | `cush_g` `χουσ` (chous; English: Cush) | Cush | -2 | 7 | Heb 4:7 | `τοσουτον` (tosouton) |  |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `god_g` `θεοσ` (theos; English: God) | God | 2 | 7 | Rom 14:2 | `εσθιει` (esthiei) |  |
| 2 | all_source | `iran_g` `ιραν` (iran; English: Iran) | Iran | -4 | 13 | Mark 14:48 | `αποκριθεισ` (apokritheis) |  |
| 3 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 7 | 22 | 1Cor 1:27 | `μωρα` (mora) |  |
| 4 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 7 | 22 | Matt 27:33 | `ελθοντεσ` (elthontes) |  |
| 5 | all_source | `amen_g` `αμην` (amen; English: Amen) | Amen | -9 | 28 | 1John 1:1 | `ακηκοαμεν` (akekoamen) |  |
| 6 | all_source | `god_g` `θεοσ` (theos; English: God) | God | 9 | 28 | Acts 17:29 | `ειναι` (einai) |  |
| 7 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 10 | 31 | Acts 11:14 | `λαλησει` (lalesei) |  |
| 8 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Luke 11:52 | `τοισ` (tois) |  |
| 9 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Luke 11:52 | `τοισ` (tois) |  |
| 10 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -10 | 31 | Matt 4:15 | `εθνων` (ethnon) |  |
| 11 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 11 | 34 | Luke 11:52 | `τοισ` (tois) |  |
| 12 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 11 | 34 | Luke 11:52 | `τοισ` (tois) |  |
| 13 | all_source | `asher_g` `ασηρ` (aser; English: Asher) | Asher | -11 | 34 | Luke 23:8 | `ιδων` (idon) |  |
| 14 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -13 | 40 | Rom 3:16 | `ταλαιπωρια` (talaiporia) |  |
| 15 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -13 | 40 | Rom 3:16 | `ταλαιπωρια` (talaiporia) |  |
| 16 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 13 | 40 | Rom 8:5 | `οντεσ` (ontes) |  |
| 17 | all_source | `cush_g` `χουσ` (chous; English: Cush) | Cush | 14 | 43 | John 12:9 | `εκ` (ek) |  |
| 18 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 15 | 46 | 1Cor 15:53 | `αθανασιαν` (athanasian) |  |
| 19 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | -16 | 49 | Acts 16:2 | `λυστροισ` (lustrois) |  |
| 20 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -17 | 52 | 2Cor 13:10 | `τουτο` (touto) |  |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 2 | 7 | Acts 7:42 | `ισραηλ` (israel) |  |
| 2 | all_source | `adam_g` `αδαμ` (adam; English: Adam) | Adam | 2 | 7 | Gal 4:27 | `ανδρα` (andra) |  |
| 3 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -3 | 10 | Heb 10:30 | `οιδαμεν` (oidamen) |  |
| 4 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -3 | 10 | Heb 7:16 | `ου` (ou) |  |
| 5 | all_source | `gomer_g` `γαμερ` (gamer; English: Gomer) | Gomer | -3 | 13 | 2Cor 10:3 | `στρατευομεθα` (strateuometha) |  |
| 6 | all_source | `vance_g` `βανσ` (bans; English: Vance) | Vance | -4 | 13 | 1Thess 5:19 | `πνευμα` (pneuma) |  |
| 7 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | 2Cor 1:13 | `αλλα` (alla) |  |
| 8 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | 4 | 13 | Acts 13:35 | `διαφθοραν` (diaphthoran) |  |
| 9 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | Acts 15:11 | `αλλα` (alla) |  |
| 10 | all_source | `china_g` `κινα` (kina; English: China) | China | -4 | 13 | Gal 6:15 | `κτισισ` (ktisis) |  |
| 11 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -4 | 13 | Heb 10:30 | `αυτου` (autou) |  |
| 12 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 4 | 13 | John 6:25 | `ευροντεσ` (eurontes) |  |
| 13 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -4 | 13 | Matt 12:26 | `αυτου` (autou) |  |
| 14 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | Rev 21:17 | `αγγελου` (aggelou) |  |
| 15 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | 5 | 16 | 1Cor 15:3 | `παρεδωκα` (paredoka) |  |
| 16 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | -5 | 16 | 2Cor 4:16 | `ημερα` (emera) |  |
| 17 | all_source | `elam_g` `ελαμ` (Elam; English: Elam) | Elam | 5 | 16 | Acts 24:25 | `μετακαλεσομαι` (metakalesomai) |  |
| 18 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -5 | 16 | Col 2:20 | `δογματιζεσθε` (dogmatizesthe) |  |
| 19 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -5 | 16 | Gal 4:6 | `αββα` (abba) |  |
| 20 | all_source | `china_g` `κινα` (kina; English: China) | China | 5 | 16 | Heb 10:3 | `ενιαυτον` (eniauton) |  |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 2 | 7 | 1Cor 10:18 | `ισραηλ` (israel) |  |
| 2 | all_source | `amen_g` `αμην` (amen; English: Amen) | Amen | 2 | 7 | 1Cor 1:10 | `μη` (me) |  |
| 3 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 2 | 7 | 1Cor 5:12 | `τουσ` (tous) |  |
| 4 | all_source | `levi_g` `λευι` (leui; English: Levi) | Levi | -2 | 7 | 1Cor 6:10 | `ουτε` (oute) |  |
| 5 | all_source | `levi_g` `λευι` (leui; English: Levi) | Levi | -2 | 7 | 1Cor 6:10 | `ουτε` (oute) |  |
| 6 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 6:8 | `υμεισ` (umeis) |  |
| 7 | all_source | `elam_g` `ελαμ` (Elam; English: Elam) | Elam | 2 | 7 | 1Cor 6:8 | `αλλα` (alla) |  |
| 8 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 6:8 | `υμεισ` (umeis) |  |
| 9 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 9:15 | `μοι` (moi) |  |
| 10 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 9:15 | `μοι` (moi) |  |
| 11 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 1John 2:10 | `σκανδαλον` (skandalon) |  |
| 12 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | 2 | 7 | 1John 2:18 | `εσχατη` (eschate) |  |
| 13 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 2 | 7 | 1John 2:8 | `υμιν` (umin) |  |
| 14 | all_source | `hell_hades_g` `αδησ` (ades; English: Hades) | Hades | -2 | 7 | 1Pet 1:13 | `τησ` (tes) |  |
| 15 | all_source | `zion_g` `σιων` (Sion; English: Zion) | Zion | -2 | 7 | 1Pet 2:7 | `γωνιασ` (gonias) |  |
| 16 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 1Pet 3:15 | `καρδιαισ` (kardiais) |  |
| 17 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -2 | 7 | 1Pet 3:21 | `συνειδησεωσ` (suneideseos) |  |
| 18 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | 1Pet 3:6 | `καλουσα` (kalousa) |  |
| 19 | all_source | `cush_g` `χουσ` (chous; English: Cush) | Cush | -2 | 7 | 1Pet 4:13 | `αυτου` (autou) |  |
| 20 | all_source | `levi_g` `λευι` (leui; English: Levi) | Levi | -2 | 7 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte) |  |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
