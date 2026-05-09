# Greek Screening All-Codes Triage

This is a compact review queue built from the relaxed all-codes export.
It ranks same center-word rows first, then related center-word rows,
center-verse rows, span rows, and finally hidden-path-only rows.

It is a triage aid, not a claim-grade filter.

## Inputs

- Hits: `reports/greek_screening_all_codes/surface_all_codes.csv`
- Summary: `reports/greek_screening_all_codes/surface_all_codes_summary.csv`
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
| 1 | all_source | `nato_g` | NATO | 8 | 25 | Rom 5:10 | `θανατου` |  |
| 2 | all_source | `temple_g` | Temple | -9 | 28 | Matt 23:17 | `ναοσ` |  |
| 3 | all_source | `blood_g` | Blood | -10 | 31 | Rev 19:13 | `αιματι` |  |
| 4 | all_source | `haima_gnt` | Blood | -10 | 31 | Rev 19:13 | `αιματι` |  |
| 5 | all_source | `blood_g` | Blood | 13 | 40 | 1Pet 1:19 | `αιματι` |  |
| 6 | all_source | `haima_gnt` | Blood | 13 | 40 | 1Pet 1:19 | `αιματι` |  |
| 7 | all_source | `god_g` | God | -21 | 64 | 2Cor 6:16 | `θεοσ` |  |
| 8 | all_source | `wisdom_g` | Wisdom | -24 | 97 | Acts 6:10 | `σοφια` |  |
| 9 | all_source | `nato_g` | NATO | -50 | 151 | Rom 8:6 | `θανατοσ` |  |
| 10 | all_source | `nato_g` | NATO | -54 | 163 | Heb 5:7 | `θανατου` |  |
| 11 | all_source | `nato_g` | NATO | 54 | 163 | Rev 20:13 | `θανατοσ` |  |
| 12 | all_source | `nato_g` | NATO | 64 | 193 | Heb 9:15 | `θανατου` |  |
| 13 | all_source | `god_g` | God | -66 | 199 | Acts 10:38 | `θεοσ` |  |
| 14 | all_source | `nato_g` | NATO | 72 | 217 | Heb 9:15 | `θανατου` |  |
| 15 | multi_source | `nato_g` | NATO | 3 | 10 | Rev 21:8 | `θανατοσ` |  |
| 16 | multi_source | `son_g` | Son | -5 | 16 | John 1:42 | `υιοσ` |  |
| 17 | multi_source | `son_g` | Son | 5 | 16 | Luke 14:5 | `υιοσ` |  |
| 18 | multi_source | `nato_g` | NATO | 14 | 43 | Heb 2:14 | `θανατου` |  |
| 19 | multi_source | `son_g` | Son | 14 | 43 | Luke 11:11 | `υιοσ` |  |
| 20 | multi_source | `nato_g` | NATO | -17 | 52 | 2Cor 3:7 | `θανατου` |  |

### center_word_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `lud_g` | Lud | -2 | 7 | Phil 2:7 | `δουλου` |  |
| 2 | all_source | `javan_g` | Javan | -2 | 9 | 1Pet 5:13 | `βαβυλωνι` |  |
| 3 | all_source | `obal_g` | Obal | -3 | 10 | 1Tim 5:14 | `βουλομαι` |  |
| 4 | all_source | `zion_g` | Zion | 3 | 10 | Acts 7:12 | `ιακωβ` |  |
| 5 | all_source | `eber_g` | Eber | 4 | 13 | Luke 22:42 | `βουλει` |  |
| 6 | all_source | `obal_g` | Obal | 4 | 13 | Luke 3:27 | `σαλαθιηλ` |  |
| 7 | all_source | `china_g` | China | -4 | 13 | Mark 12:3 | `εδειραν` |  |
| 8 | all_source | `shelah_g` | Shelah | 4 | 13 | Matt 4:15 | `ζαβουλων` |  |
| 9 | all_source | `seba_g` | Seba | 5 | 16 | 2Pet 1:10 | `σπουδασατε` |  |
| 10 | all_source | `son_g` | Son | 6 | 19 | John 7:6 | `ιησουσ` |  |
| 11 | all_source | `seba_g` | Seba | -6 | 19 | Luke 10:22 | `βουληται` |  |
| 12 | all_source | `nato_g` | NATO | -6 | 19 | Luke 1:80 | `ισραηλ` |  |
| 13 | all_source | `seba_g` | Seba | -6 | 19 | Matt 11:27 | `βουληται` |  |
| 14 | all_source | `seba_g` | Seba | 6 | 19 | Rom 16:10 | `αριστοβουλου` |  |
| 15 | all_source | `seba_g` | Seba | -6 | 19 | Rom 16:10 | `αριστοβουλου` |  |
| 16 | all_source | `blood_g` | Blood | 7 | 22 | Acts 7:11 | `θλιψισ` |  |
| 17 | all_source | `eber_g` | Eber | 7 | 22 | Matt 1:17 | `βαβυλωνοσ` |  |
| 18 | all_source | `china_g` | China | -7 | 22 | Rev 6:8 | `θανατοσ` |  |
| 19 | all_source | `son_g` | Son | 8 | 25 | 1John 2:22 | `χριστοσ` |  |
| 20 | all_source | `shelah_g` | Shelah | 9 | 28 | Rev 18:10 | `βαβυλων` |  |

### center_verse_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `lasha_g` | Lasha | -2 | 7 | Acts 9:11 | `ταρσεα` |  |
| 2 | all_source | `blood_g` | Blood | 2 | 7 | Matt 13:55 | `μαριαμ` |  |
| 3 | all_source | `haima_gnt` | Blood | 2 | 7 | Matt 13:55 | `μαριαμ` |  |
| 4 | all_source | `son_g` | Son | -3 | 10 | Acts 23:6 | `φαρισαιοσ` |  |
| 5 | all_source | `blood_g` | Blood | 3 | 10 | Eph 4:17 | `εν` |  |
| 6 | all_source | `haima_gnt` | Blood | 3 | 10 | Eph 4:17 | `εν` |  |
| 7 | all_source | `amen_g` | Amen | -3 | 10 | John 5:24 | `ζωην` |  |
| 8 | all_source | `nato_g` | NATO | -3 | 10 | Rev 2:10 | `στεφανον` |  |
| 9 | all_source | `nato_g` | NATO | -4 | 13 | 1Cor 9:22 | `τοισ` |  |
| 10 | all_source | `god_g` | God | 4 | 13 | 1John 4:9 | `εισ` |  |
| 11 | all_source | `zion_g` | Zion | -4 | 13 | Acts 19:34 | `επι` |  |
| 12 | all_source | `blood_g` | Blood | -4 | 13 | Col 1:11 | `δυναμουμενοι` |  |
| 13 | all_source | `haima_gnt` | Blood | -4 | 13 | Col 1:11 | `δυναμουμενοι` |  |
| 14 | all_source | `son_g` | Son | 4 | 13 | Gal 4:7 | `ει` |  |
| 15 | all_source | `son_g` | Son | 4 | 13 | John 1:42 | `σιμων` |  |
| 16 | all_source | `nato_g` | NATO | -4 | 13 | Luke 3:31 | `ματταθα` |  |
| 17 | all_source | `nato_g` | NATO | -4 | 13 | Matt 4:18 | `αυτου` |  |
| 18 | all_source | `nato_g` | NATO | -4 | 13 | Rom 1:32 | `πρασσοντεσ` |  |
| 19 | all_source | `blood_g` | Blood | 5 | 16 | 1Cor 15:17 | `αμαρτιαισ` |  |
| 20 | all_source | `haima_gnt` | Blood | 5 | 16 | 1Cor 15:17 | `αμαρτιαισ` |  |

### center_verse_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `temple_g` | Temple | 2 | 7 | 1Cor 10:16 | `του` |  |
| 2 | all_source | `china_g` | China | 2 | 7 | 1John 2:1 | `δικαιον` |  |
| 3 | all_source | `boils_g` | Boils | 2 | 7 | 1Pet 5:13 | `συνεκλεκτη` |  |
| 4 | all_source | `sores_g` | Sores | 2 | 7 | 1Pet 5:13 | `συνεκλεκτη` |  |
| 5 | all_source | `temple_g` | Temple | 2 | 7 | 1Tim 5:13 | `μανθανουσι` |  |
| 6 | all_source | `seba_g` | Seba | 2 | 7 | 1Tim 6:9 | `και` |  |
| 7 | all_source | `lasha_g` | Lasha | -2 | 7 | 2Cor 1:22 | `καρδιαισ` |  |
| 8 | all_source | `lasha_g` | Lasha | -2 | 7 | 2Cor 3:2 | `καρδιαισ` |  |
| 9 | all_source | `lasha_g` | Lasha | -2 | 7 | 2Cor 4:6 | `καρδιαισ` |  |
| 10 | all_source | `lasha_g` | Lasha | -2 | 7 | 2Cor 7:3 | `καρδιαισ` |  |
| 11 | all_source | `lasha_g` | Lasha | -2 | 7 | 2Tim 1:10 | `αφθαρσιαν` |  |
| 12 | all_source | `aram_g` | Aram | 2 | 7 | 2Tim 1:9 | `εργα` |  |
| 13 | all_source | `adam_g` | Adam | 2 | 7 | Acts 13:22 | `καρδιαν` |  |
| 14 | all_source | `iran_g` | Iran | -2 | 7 | Acts 15:23 | `χαιρειν` |  |
| 15 | all_source | `temple_g` | Temple | 2 | 7 | Acts 16:22 | `και` |  |
| 16 | all_source | `temple_g` | Temple | -2 | 7 | Acts 7:58 | `ποδασ` |  |
| 17 | all_source | `god_g` | God | -2 | 7 | Acts 9:11 | `πορευθητι` |  |
| 18 | all_source | `china_g` | China | 2 | 7 | Heb 11:19 | `εν` |  |
| 19 | all_source | `temple_g` | Temple | 2 | 7 | Heb 2:17 | `τοισ` |  |
| 20 | all_source | `cush_g` | Cush | -2 | 7 | Heb 4:7 | `τοσουτον` |  |

### span_exact

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `god_g` | God | 2 | 7 | Rom 14:2 | `εσθιει` |  |
| 2 | all_source | `iran_g` | Iran | -4 | 13 | Mark 14:48 | `αποκριθεισ` |  |
| 3 | all_source | `nato_g` | NATO | 7 | 22 | 1Cor 1:27 | `μωρα` |  |
| 4 | all_source | `nato_g` | NATO | 7 | 22 | Matt 27:33 | `ελθοντεσ` |  |
| 5 | all_source | `amen_g` | Amen | -9 | 28 | 1John 1:1 | `ακηκοαμεν` |  |
| 6 | all_source | `god_g` | God | 9 | 28 | Acts 17:29 | `ειναι` |  |
| 7 | all_source | `nato_g` | NATO | 10 | 31 | Acts 11:14 | `λαλησει` |  |
| 8 | all_source | `blood_g` | Blood | -10 | 31 | Luke 11:52 | `τοισ` |  |
| 9 | all_source | `haima_gnt` | Blood | -10 | 31 | Luke 11:52 | `τοισ` |  |
| 10 | all_source | `nato_g` | NATO | -10 | 31 | Matt 4:15 | `εθνων` |  |
| 11 | all_source | `blood_g` | Blood | 11 | 34 | Luke 11:52 | `τοισ` |  |
| 12 | all_source | `haima_gnt` | Blood | 11 | 34 | Luke 11:52 | `τοισ` |  |
| 13 | all_source | `asher_g` | Asher | -11 | 34 | Luke 23:8 | `ιδων` |  |
| 14 | all_source | `blood_g` | Blood | -13 | 40 | Rom 3:16 | `ταλαιπωρια` |  |
| 15 | all_source | `haima_gnt` | Blood | -13 | 40 | Rom 3:16 | `ταλαιπωρια` |  |
| 16 | all_source | `nato_g` | NATO | 13 | 40 | Rom 8:5 | `οντεσ` |  |
| 17 | all_source | `cush_g` | Cush | 14 | 43 | John 12:9 | `εκ` |  |
| 18 | all_source | `nato_g` | NATO | 15 | 46 | 1Cor 15:53 | `αθανασιαν` |  |
| 19 | all_source | `son_g` | Son | -16 | 49 | Acts 16:2 | `λυστροισ` |  |
| 20 | all_source | `nato_g` | NATO | -17 | 52 | 2Cor 13:10 | `τουτο` |  |

### span_same_category

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `shelah_g` | Shelah | 2 | 7 | Acts 7:42 | `ισραηλ` |  |
| 2 | all_source | `adam_g` | Adam | 2 | 7 | Gal 4:27 | `ανδρα` |  |
| 3 | all_source | `temple_g` | Temple | -3 | 10 | Heb 10:30 | `οιδαμεν` |  |
| 4 | all_source | `temple_g` | Temple | -3 | 10 | Heb 7:16 | `ου` |  |
| 5 | all_source | `gomer_g` | Gomer | -3 | 13 | 2Cor 10:3 | `στρατευομεθα` |  |
| 6 | all_source | `vance_g` | Vance | -4 | 13 | 1Thess 5:19 | `πνευμα` |  |
| 7 | all_source | `shelah_g` | Shelah | 4 | 13 | 2Cor 1:13 | `αλλα` |  |
| 8 | all_source | `aram_g` | Aram | 4 | 13 | Acts 13:35 | `διαφθοραν` |  |
| 9 | all_source | `shelah_g` | Shelah | 4 | 13 | Acts 15:11 | `αλλα` |  |
| 10 | all_source | `china_g` | China | -4 | 13 | Gal 6:15 | `κτισισ` |  |
| 11 | all_source | `obal_g` | Obal | -4 | 13 | Heb 10:30 | `αυτου` |  |
| 12 | all_source | `son_g` | Son | 4 | 13 | John 6:25 | `ευροντεσ` |  |
| 13 | all_source | `obal_g` | Obal | -4 | 13 | Matt 12:26 | `αυτου` |  |
| 14 | all_source | `shelah_g` | Shelah | 4 | 13 | Rev 21:17 | `αγγελου` |  |
| 15 | all_source | `aram_g` | Aram | 5 | 16 | 1Cor 15:3 | `παρεδωκα` |  |
| 16 | all_source | `aram_g` | Aram | -5 | 16 | 2Cor 4:16 | `ημερα` |  |
| 17 | all_source | `elam_g` | Elam | 5 | 16 | Acts 24:25 | `μετακαλεσομαι` |  |
| 18 | all_source | `lasha_g` | Lasha | -5 | 16 | Col 2:20 | `δογματιζεσθε` |  |
| 19 | all_source | `seba_g` | Seba | -5 | 16 | Gal 4:6 | `αββα` |  |
| 20 | all_source | `china_g` | China | 5 | 16 | Heb 10:3 | `ενιαυτον` |  |

### hidden_path_only

| Rank | Scope | Term | Concept | Skip | Span | Center | Center word | Control |
| ---: | --- | --- | --- | ---: | ---: | --- | --- | --- |
| 1 | all_source | `shelah_g` | Shelah | 2 | 7 | 1Cor 10:18 | `ισραηλ` |  |
| 2 | all_source | `amen_g` | Amen | 2 | 7 | 1Cor 1:10 | `μη` |  |
| 3 | all_source | `son_g` | Son | 2 | 7 | 1Cor 5:12 | `τουσ` |  |
| 4 | all_source | `levi_g` | Levi | -2 | 7 | 1Cor 6:10 | `ουτε` |  |
| 5 | all_source | `levi_g` | Levi | -2 | 7 | 1Cor 6:10 | `ουτε` |  |
| 6 | all_source | `blood_g` | Blood | -2 | 7 | 1Cor 6:8 | `υμεισ` |  |
| 7 | all_source | `elam_g` | Elam | 2 | 7 | 1Cor 6:8 | `αλλα` |  |
| 8 | all_source | `haima_gnt` | Blood | -2 | 7 | 1Cor 6:8 | `υμεισ` |  |
| 9 | all_source | `blood_g` | Blood | -2 | 7 | 1Cor 9:15 | `μοι` |  |
| 10 | all_source | `haima_gnt` | Blood | -2 | 7 | 1Cor 9:15 | `μοι` |  |
| 11 | all_source | `lasha_g` | Lasha | -2 | 7 | 1John 2:10 | `σκανδαλον` |  |
| 12 | all_source | `lasha_g` | Lasha | 2 | 7 | 1John 2:18 | `εσχατη` |  |
| 13 | all_source | `son_g` | Son | 2 | 7 | 1John 2:8 | `υμιν` |  |
| 14 | all_source | `hell_hades_g` | Hades | -2 | 7 | 1Pet 1:13 | `τησ` |  |
| 15 | all_source | `zion_g` | Zion | -2 | 7 | 1Pet 2:7 | `γωνιασ` |  |
| 16 | all_source | `lasha_g` | Lasha | -2 | 7 | 1Pet 3:15 | `καρδιαισ` |  |
| 17 | all_source | `obal_g` | Obal | -2 | 7 | 1Pet 3:21 | `συνειδησεωσ` |  |
| 18 | all_source | `temple_g` | Temple | 2 | 7 | 1Pet 3:6 | `καλουσα` |  |
| 19 | all_source | `cush_g` | Cush | -2 | 7 | 1Pet 4:13 | `αυτου` |  |
| 20 | all_source | `levi_g` | Levi | -2 | 7 | 1Pet 5:13 | `συνεκλεκτη` |  |

## Read

Rows at the top are good manual-review candidates because their hidden ELS
path center is located on, or near, surface language from the same declared
term set. The `presence_scope` column reports whether the selected exact
ref-key pattern appears in every configured source, multiple sources, or
only one source among the selected candidate keys.
