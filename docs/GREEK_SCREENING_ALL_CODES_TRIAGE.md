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
| 1 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 8 | 25 | Rom 5:10 | `θανατου` (thanatou; English: death) |  |
| 2 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -9 | 28 | Matt 23:17 | `ναοσ` (naos; English: temple) |  |
| 3 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Rev 19:13 | `αιματι` (haimati; English: blood) |  |
| 4 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Rev 19:13 | `αιματι` (haimati; English: blood) |  |
| 5 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 13 | 40 | 1Pet 1:19 | `αιματι` (haimati; English: blood) |  |
| 6 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 13 | 40 | 1Pet 1:19 | `αιματι` (haimati; English: blood) |  |
| 7 | all_source | `god_g` `θεοσ` (theos; English: God) | God | -21 | 64 | 2Cor 6:16 | `θεοσ` (theos; English: God) |  |
| 8 | all_source | `wisdom_g` `σοφια` (sophia; English: Wisdom) | Wisdom | -24 | 97 | Acts 6:10 | `σοφια` (sophia; English: wisdom) |  |
| 9 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -50 | 151 | Rom 8:6 | `θανατοσ` (thanatos; English: death) |  |
| 10 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -54 | 163 | Heb 5:7 | `θανατου` (thanatou; English: death) |  |
| 11 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 54 | 163 | Rev 20:13 | `θανατοσ` (thanatos; English: death) |  |
| 12 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 64 | 193 | Heb 9:15 | `θανατου` (thanatou; English: death) |  |
| 13 | all_source | `god_g` `θεοσ` (theos; English: God) | God | -66 | 199 | Acts 10:38 | `θεοσ` (theos; English: God) |  |
| 14 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 72 | 217 | Heb 9:15 | `θανατου` (thanatou; English: death) |  |
| 15 | multi_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 3 | 10 | Rev 21:8 | `θανατοσ` (thanatos; English: death) |  |
| 16 | multi_source | `son_g` `υιοσ` (huios; English: Son) | Son | -5 | 16 | John 1:42 | `υιοσ` (huios; English: son) |  |
| 17 | multi_source | `son_g` `υιοσ` (huios; English: Son) | Son | 5 | 16 | Luke 14:5 | `υιοσ` (huios; English: son) |  |
| 18 | multi_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 14 | 43 | Heb 2:14 | `θανατου` (thanatou; English: death) |  |
| 19 | multi_source | `son_g` `υιοσ` (huios; English: Son) | Son | 14 | 43 | Luke 11:11 | `υιοσ` (huios; English: son) |  |
| 20 | multi_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -17 | 52 | 2Cor 3:7 | `θανατου` (thanatou; English: death) |  |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `lud_g` `λουδ` (loud; English: Lud) | Lud | -2 | 7 | Phil 2:7 | `δουλου` (doulou; English: servant) |  |
| 2 | all_source | `javan_g` `ιωυαν` (Iouan; English: Javan) | Javan | -2 | 9 | 1Pet 5:13 | `βαβυλωνι` (babuloni; English: Babylon) |  |
| 3 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -3 | 10 | 1Tim 5:14 | `βουλομαι` (boulomai; English: I want) |  |
| 4 | all_source | `zion_g` `σιων` (Sion; English: Zion) | Zion | 3 | 10 | Acts 7:12 | `ιακωβ` (iakob; English: Jacob) |  |
| 5 | all_source | `eber_g` `εβερ` (eber; English: Eber) | Eber | 4 | 13 | Luke 22:42 | `βουλει` (boulei; English: you want) |  |
| 6 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | 4 | 13 | Luke 3:27 | `σαλαθιηλ` (salathiel; English: Salathiel) |  |
| 7 | all_source | `china_g` `κινα` (kina; English: China) | China | -4 | 13 | Mark 12:3 | `εδειραν` (edeiran; English: they beat) |  |
| 8 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | Matt 4:15 | `ζαβουλων` (zaboulon; English: Zebulun) |  |
| 9 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | 5 | 16 | 2Pet 1:10 | `σπουδασατε` (spoudasate; English: be diligent) |  |
| 10 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 6 | 19 | John 7:6 | `ιησουσ` (Iesous; English: Jesus/Joshua) |  |
| 11 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -6 | 19 | Luke 10:22 | `βουληται` (bouletai; English: he wills) |  |
| 12 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -6 | 19 | Luke 1:80 | `ισραηλ` (israel; English: Israel) |  |
| 13 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -6 | 19 | Matt 11:27 | `βουληται` (bouletai; English: he wills) |  |
| 14 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | 6 | 19 | Rom 16:10 | `αριστοβουλου` (aristoboulou; English: Aristobulus) |  |
| 15 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -6 | 19 | Rom 16:10 | `αριστοβουλου` (aristoboulou; English: Aristobulus) |  |
| 16 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 7 | 22 | Acts 7:11 | `θλιψισ` (thlipsis; English: Tribulation) |  |
| 17 | all_source | `eber_g` `εβερ` (eber; English: Eber) | Eber | 7 | 22 | Matt 1:17 | `βαβυλωνοσ` (babulonos; English: Babylon) |  |
| 18 | all_source | `china_g` `κινα` (kina; English: China) | China | -7 | 22 | Rev 6:8 | `θανατοσ` (thanatos; English: death) |  |
| 19 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 8 | 25 | 1John 2:22 | `χριστοσ` (Christos; English: Christ) |  |
| 20 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 9 | 28 | Rev 18:10 | `βαβυλων` (babulon; English: Babylon) |  |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | Acts 9:11 | `ταρσεα` (tarsea; English: of Tarsus) |  |
| 2 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 2 | 7 | Matt 13:55 | `μαριαμ` (mariam; English: Mary) |  |
| 3 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 2 | 7 | Matt 13:55 | `μαριαμ` (mariam; English: Mary) |  |
| 4 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | -3 | 10 | Acts 23:6 | `φαρισαιοσ` (pharisaios; English: Pharisee) |  |
| 5 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 3 | 10 | Eph 4:17 | `εν` (en; English: in) |  |
| 6 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 3 | 10 | Eph 4:17 | `εν` (en; English: in) |  |
| 7 | all_source | `amen_g` `αμην` (amen; English: Amen) | Amen | -3 | 10 | John 5:24 | `ζωην` (zoen; English: life) |  |
| 8 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -3 | 10 | Rev 2:10 | `στεφανον` (stephanon; English: crown) |  |
| 9 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | 1Cor 9:22 | `τοισ` (tois; English: to the) |  |
| 10 | all_source | `god_g` `θεοσ` (theos; English: God) | God | 4 | 13 | 1John 4:9 | `εισ` (eis; English: into/for) |  |
| 11 | all_source | `zion_g` `σιων` (Sion; English: Zion) | Zion | -4 | 13 | Acts 19:34 | `επι` (epi; English: on/upon) |  |
| 12 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -4 | 13 | Col 1:11 | `δυναμουμενοι` (dunamoumenoi; English: being strengthened) |  |
| 13 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -4 | 13 | Col 1:11 | `δυναμουμενοι` (dunamoumenoi; English: being strengthened) |  |
| 14 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 4 | 13 | Gal 4:7 | `ει` (ei; English: if/you are) |  |
| 15 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 4 | 13 | John 1:42 | `σιμων` (simon; English: Simon) |  |
| 16 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | Luke 3:31 | `ματταθα` (mattatha; English: Mattatha) |  |
| 17 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | Matt 4:18 | `αυτου` (autou; English: of him) |  |
| 18 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -4 | 13 | Rom 1:32 | `πρασσοντεσ` (prassontes; English: practicing) |  |
| 19 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 5 | 16 | 1Cor 15:17 | `αμαρτιαισ` (hamartiais; English: sins) |  |
| 20 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 5 | 16 | 1Cor 15:17 | `αμαρτιαισ` (hamartiais; English: sins) |  |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | 1Cor 10:16 | `του` (tou; English: of the) |  |
| 2 | all_source | `china_g` `κινα` (kina; English: China) | China | 2 | 7 | 1John 2:1 | `δικαιον` (dikaion; English: righteous) |  |
| 3 | all_source | `boils_g` `ελκη` (elke; English: Boils) | Boils | 2 | 7 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte; English: co-elect) |  |
| 4 | all_source | `sores_g` `ελκη` (elke; English: Sores) | Sores | 2 | 7 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte; English: co-elect) |  |
| 5 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | 1Tim 5:13 | `μανθανουσι` (manthanousi; English: they learn) |  |
| 6 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | 2 | 7 | 1Tim 6:9 | `και` (kai; English: and) |  |
| 7 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 1:22 | `καρδιαισ` (kardiais; English: hearts) |  |
| 8 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 3:2 | `καρδιαισ` (kardiais; English: hearts) |  |
| 9 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 4:6 | `καρδιαισ` (kardiais; English: hearts) |  |
| 10 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Cor 7:3 | `καρδιαισ` (kardiais; English: hearts) |  |
| 11 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 2Tim 1:10 | `αφθαρσιαν` (aphtharsian; English: incorruption) |  |
| 12 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | 2 | 7 | 2Tim 1:9 | `εργα` (erga; English: works) |  |
| 13 | all_source | `adam_g` `αδαμ` (adam; English: Adam) | Adam | 2 | 7 | Acts 13:22 | `καρδιαν` (kardian; English: heart) |  |
| 14 | all_source | `iran_g` `ιραν` (iran; English: Iran) | Iran | -2 | 7 | Acts 15:23 | `χαιρειν` (chairein; English: greetings) |  |
| 15 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | Acts 16:22 | `και` (kai; English: and) |  |
| 16 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -2 | 7 | Acts 7:58 | `ποδασ` (podas; English: feet) |  |
| 17 | all_source | `god_g` `θεοσ` (theos; English: God) | God | -2 | 7 | Acts 9:11 | `πορευθητι` (poreutheti; English: go) |  |
| 18 | all_source | `china_g` `κινα` (kina; English: China) | China | 2 | 7 | Heb 11:19 | `εν` (en; English: in) |  |
| 19 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | Heb 2:17 | `τοισ` (tois; English: to the) |  |
| 20 | all_source | `cush_g` `χουσ` (chous; English: Cush) | Cush | -2 | 7 | Heb 4:7 | `τοσουτον` (tosouton; English: so much) |  |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `god_g` `θεοσ` (theos; English: God) | God | 2 | 7 | Rom 14:2 | `εσθιει` (esthiei; English: eats) |  |
| 2 | all_source | `iran_g` `ιραν` (iran; English: Iran) | Iran | -4 | 13 | Mark 14:48 | `αποκριθεισ` (apokritheis; English: having answered) |  |
| 3 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 7 | 22 | 1Cor 1:27 | `μωρα` (mora; English: foolish things) |  |
| 4 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 7 | 22 | Matt 27:33 | `ελθοντεσ` (elthontes; English: having come) |  |
| 5 | all_source | `amen_g` `αμην` (amen; English: Amen) | Amen | -9 | 28 | 1John 1:1 | `ακηκοαμεν` (akekoamen; English: we have heard) |  |
| 6 | all_source | `god_g` `θεοσ` (theos; English: God) | God | 9 | 28 | Acts 17:29 | `ειναι` (einai; English: to be) |  |
| 7 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 10 | 31 | Acts 11:14 | `λαλησει` (lalesei; English: he will speak) |  |
| 8 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Luke 11:52 | `τοισ` (tois; English: to the) |  |
| 9 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -10 | 31 | Luke 11:52 | `τοισ` (tois; English: to the) |  |
| 10 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -10 | 31 | Matt 4:15 | `εθνων` (ethnon; English: nations) |  |
| 11 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | 11 | 34 | Luke 11:52 | `τοισ` (tois; English: to the) |  |
| 12 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | 11 | 34 | Luke 11:52 | `τοισ` (tois; English: to the) |  |
| 13 | all_source | `asher_g` `ασηρ` (aser; English: Asher) | Asher | -11 | 34 | Luke 23:8 | `ιδων` (idon; English: having seen) |  |
| 14 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -13 | 40 | Rom 3:16 | `ταλαιπωρια` (talaiporia; English: misery) |  |
| 15 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -13 | 40 | Rom 3:16 | `ταλαιπωρια` (talaiporia; English: misery) |  |
| 16 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 13 | 40 | Rom 8:5 | `οντεσ` (ontes; English: being) |  |
| 17 | all_source | `cush_g` `χουσ` (chous; English: Cush) | Cush | 14 | 43 | John 12:9 | `εκ` (ek; English: from) |  |
| 18 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | 15 | 46 | 1Cor 15:53 | `αθανασιαν` (athanasian; English: immortality) |  |
| 19 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | -16 | 49 | Acts 16:2 | `λυστροισ` (lustrois; English: Lystra) |  |
| 20 | all_source | `nato_g` `νατο` (nato; English: NATO) | NATO | -17 | 52 | 2Cor 13:10 | `τουτο` (touto; English: this) |  |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 2 | 7 | Acts 7:42 | `ισραηλ` (israel; English: Israel) |  |
| 2 | all_source | `adam_g` `αδαμ` (adam; English: Adam) | Adam | 2 | 7 | Gal 4:27 | `ανδρα` (andra; English: man) |  |
| 3 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -3 | 10 | Heb 10:30 | `οιδαμεν` (oidamen; English: we know) |  |
| 4 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | -3 | 10 | Heb 7:16 | `ου` (ou; English: not) |  |
| 5 | all_source | `gomer_g` `γαμερ` (gamer; English: Gomer) | Gomer | -3 | 13 | 2Cor 10:3 | `στρατευομεθα` (strateuometha; English: we wage war) |  |
| 6 | all_source | `vance_g` `βανσ` (bans; English: Vance) | Vance | -4 | 13 | 1Thess 5:19 | `πνευμα` (pneuma; English: spirit) |  |
| 7 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | 2Cor 1:13 | `αλλα` (alla; English: but) |  |
| 8 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | 4 | 13 | Acts 13:35 | `διαφθοραν` (diaphthoran; English: corruption) |  |
| 9 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | Acts 15:11 | `αλλα` (alla; English: but) |  |
| 10 | all_source | `china_g` `κινα` (kina; English: China) | China | -4 | 13 | Gal 6:15 | `κτισισ` (ktisis; English: creation) |  |
| 11 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -4 | 13 | Heb 10:30 | `αυτου` (autou; English: of him) |  |
| 12 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 4 | 13 | John 6:25 | `ευροντεσ` (heurontes; English: having found) |  |
| 13 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -4 | 13 | Matt 12:26 | `αυτου` (autou; English: of him) |  |
| 14 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 4 | 13 | Rev 21:17 | `αγγελου` (aggelou; English: angel) |  |
| 15 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | 5 | 16 | 1Cor 15:3 | `παρεδωκα` (paredoka; English: I delivered) |  |
| 16 | all_source | `aram_g` `αραμ` (aram; English: Aram) | Aram | -5 | 16 | 2Cor 4:16 | `ημερα` (emera; English: Day) |  |
| 17 | all_source | `elam_g` `ελαμ` (Elam; English: Elam) | Elam | 5 | 16 | Acts 24:25 | `μετακαλεσομαι` (metakalesomai; English: I will summon) |  |
| 18 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -5 | 16 | Col 2:20 | `δογματιζεσθε` (dogmatizesthe; English: you submit to decrees) |  |
| 19 | all_source | `seba_g` `σαβα` (saba; English: Seba) | Seba | -5 | 16 | Gal 4:6 | `αββα` (abba; English: Abba) |  |
| 20 | all_source | `china_g` `κινα` (kina; English: China) | China | 5 | 16 | Heb 10:3 | `ενιαυτον` (eniauton; English: year) |  |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `shelah_g` `σαλα` (Sala; English: Shelah) | Shelah | 2 | 7 | 1Cor 10:18 | `ισραηλ` (israel; English: Israel) |  |
| 2 | all_source | `amen_g` `αμην` (amen; English: Amen) | Amen | 2 | 7 | 1Cor 1:10 | `μη` (me; English: not) |  |
| 3 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 2 | 7 | 1Cor 5:12 | `τουσ` (tous; English: the/those) |  |
| 4 | all_source | `levi_g` `λευι` (leui; English: Levi) | Levi | -2 | 7 | 1Cor 6:10 | `ουτε` (oute; English: nor) |  |
| 5 | all_source | `levi_g` `λευι` (leui; English: Levi) | Levi | -2 | 7 | 1Cor 6:10 | `ουτε` (oute; English: nor) |  |
| 6 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 6:8 | `υμεισ` (umeis; English: you) |  |
| 7 | all_source | `elam_g` `ελαμ` (Elam; English: Elam) | Elam | 2 | 7 | 1Cor 6:8 | `αλλα` (alla; English: but) |  |
| 8 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 6:8 | `υμεισ` (umeis; English: you) |  |
| 9 | all_source | `blood_g` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 9:15 | `μοι` (moi; English: to me) |  |
| 10 | all_source | `haima_gnt` `αιμα` (haima; English: Blood) | Blood | -2 | 7 | 1Cor 9:15 | `μοι` (moi; English: to me) |  |
| 11 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 1John 2:10 | `σκανδαλον` (skandalon; English: stumbling block) |  |
| 12 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | 2 | 7 | 1John 2:18 | `εσχατη` (eschate; English: last) |  |
| 13 | all_source | `son_g` `υιοσ` (huios; English: Son) | Son | 2 | 7 | 1John 2:8 | `υμιν` (umin; English: to you) |  |
| 14 | all_source | `hell_hades_g` `αδησ` (ades; English: Hades) | Hades | -2 | 7 | 1Pet 1:13 | `τησ` (tes; English: of the) |  |
| 15 | all_source | `zion_g` `σιων` (Sion; English: Zion) | Zion | -2 | 7 | 1Pet 2:7 | `γωνιασ` (gonias; English: corner) |  |
| 16 | all_source | `lasha_g` `δασα` (dasa; English: Lasha) | Lasha | -2 | 7 | 1Pet 3:15 | `καρδιαισ` (kardiais; English: hearts) |  |
| 17 | all_source | `obal_g` `ευαλ` (eual; English: Obal) | Obal | -2 | 7 | 1Pet 3:21 | `συνειδησεωσ` (suneideseos; English: conscience) |  |
| 18 | all_source | `temple_g` `ναοσ` (naos; English: Temple) | Temple | 2 | 7 | 1Pet 3:6 | `καλουσα` (kalousa; English: calling) |  |
| 19 | all_source | `cush_g` `χουσ` (chous; English: Cush) | Cush | -2 | 7 | 1Pet 4:13 | `αυτου` (autou; English: of him) |  |
| 20 | all_source | `levi_g` `λευι` (leui; English: Levi) | Levi | -2 | 7 | 1Pet 5:13 | `συνεκλεκτη` (suneklekte; English: co-elect) |  |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
