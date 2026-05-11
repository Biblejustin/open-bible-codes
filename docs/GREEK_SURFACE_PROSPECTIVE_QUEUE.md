# Greek Surface Prospective Queue

Status: prospective exact-center surface queue; no claim.

This report summarizes exact-center surface hits from the locked Greek surface
prospective term screen after prior selected rows were removed. It does not
require same-skip phrase extension and does not run controls.

## Inputs

- Surface hits: `reports/greek_surface_prospective/surface_context_hits.csv`
- Term scope: `terms/greek_surface_prospective_terms.csv`
- Compared sources: TR_NT, BYZ_NT, TCG_NT, SBLGNT

## Definition

`exact-center surface` means the ELS hit center falls in a verse where the
normalized term also appears as ordinary surface text. The `Center words`
column reports the actual word at the ELS center offset, so it may differ
from the searched term.

## Scope Counts

| Scope | Patterns |
| --- | ---: |
| `all_sources` | 24 |
| `multi_source` | 53 |
| `source_only` | 74 |

Total exact-center surface patterns: 151.

## Top Term Queue

| Term | Concept | Exact-center hits | Unique patterns | All-source | Multi-source | Source-specific | Read |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `αμην` (amen; English: Amen) | Amen | 101 | 44 | 11 | 14 | 19 | all-source surface queue; needs controls before interpretation |
| `σιων` (Sion; English: Zion) | Zion | 37 | 17 | 4 | 5 | 8 | all-source surface queue; needs controls before interpretation |
| `αραμ` (aram; English: Aram) | Aram | 14 | 5 | 3 | 0 | 2 | all-source surface queue; needs controls before interpretation |
| `δασα` (dasa; English: Lasha) | Lasha | 36 | 21 | 2 | 7 | 12 | all-source surface queue; needs controls before interpretation |
| `ασηρ` (aser; English: Asher) | Asher | 14 | 5 | 2 | 2 | 1 | all-source surface queue; needs controls before interpretation |
| `χουσ` (chous; English: Cush) | Cush | 28 | 17 | 1 | 6 | 10 | all-source surface queue; needs controls before interpretation |
| `σαβα` (saba; English: Seba) | Seba | 9 | 3 | 1 | 2 | 0 | all-source surface queue; needs controls before interpretation |
| `ιουδα` (iouda; English: Judah) | Judah | 14 | 7 | 0 | 4 | 3 | multi-source surface queue; inspect source distribution |
| `λεων` (leon; English: Lion) | Lion | 9 | 5 | 0 | 3 | 2 | multi-source surface queue; inspect source distribution |
| `αδαμ` (adam; English: Adam) | Adam | 7 | 4 | 0 | 2 | 2 | multi-source surface queue; inspect source distribution |
| `ελαμ` (Elam; English: Elam) | Elam | 6 | 3 | 0 | 2 | 1 | multi-source surface queue; inspect source distribution |
| `λευι` (leui; English: Levi) | Levi | 6 | 5 | 0 | 1 | 4 | multi-source surface queue; inspect source distribution |
| `μαρια` (Maria; English: Mary) | Mary | 4 | 3 | 0 | 1 | 2 | multi-source surface queue; inspect source distribution |
| `ελισα` (Elisa; English: Elishah) | Elishah | 3 | 2 | 0 | 1 | 1 | multi-source surface queue; inspect source distribution |
| `νομοσ` (nomos; English: Law) | Law | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `λουδ` (loud; English: Lud) | Lud | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `πασχα` (pascha; English: Passover) | Passover | 2 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `σαλα` (Sala; English: Shelah) | Shelah | 2 | 2 | 0 | 0 | 2 | source-specific surface queue |
| `εικων` (eikon; English: Image) | Image | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ισραηλ` (israel; English: Israel) | Israel | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ιακωβ` (iakob; English: Jacob) | Jacob | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `φρεαρ` (phrear; English: Pit) | Pit | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `οργη` (orge; English: Wrath) | Wrath | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |

## All-Source Pattern Examples

| Term | Center | Skip | Direction | Present | Center words |
| --- | --- | ---: | --- | --- | --- |
| `αμην` (amen; English: Amen) | John 10:7 | -42 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`οὖν` (oun; English: therefore); BYZ_NT:`ουν` (oun; English: therefore); TCG_NT:`οὖν` (oun; English: therefore); SBLGNT:`οὖν` (oun; English: therefore) |
| `αμην` (amen; English: Amen) | John 6:53 | -42 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἀνθρώπου` (anthropou; English: man/human); BYZ_NT:`ανθρωπου` (anthropou; English: man/human); TCG_NT:`ἀνθρώπου` (anthropou; English: man/human); SBLGNT:`ἀνθρώπου` (anthropou; English: man/human) |
| `αμην` (amen; English: Amen) | Mark 8:12 | -13 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ταύτῃ` (taute; English: to this/in this); BYZ_NT:`ταυτη` (taute; English: to this/in this); TCG_NT:`ταύτῃ` (taute; English: to this/in this); SBLGNT:`ταύτῃ` (taute; English: to this/in this) |
| `αμην` (amen; English: Amen) | Matt 5:18 | -8 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἰῶτα` (iota; English: iota); BYZ_NT:`ιωτα` (iota; English: iota); TCG_NT:`ἰῶτα` (iota; English: iota); SBLGNT:`ἰῶτα` (iota; English: iota) |
| `αμην` (amen; English: Amen) | Matt 18:13 | -7 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`λέγω` (lego; English: I say); BYZ_NT:`λεγω` (lego; English: I say); TCG_NT:`λέγω` (lego; English: I say); SBLGNT:`λέγω` (lego; English: I say) |
| `αμην` (amen; English: Amen) | John 5:24 | -3 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ζωήν` (zoen; English: life); BYZ_NT:`ζωην` (zoen; English: life); TCG_NT:`ζωήν` (zoen; English: life); SBLGNT:`ζωήν.` (zoen; English: life) |
| `αμην` (amen; English: Amen) | Luke 18:17 | 8 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`εἰσέλθῃ` (eiselthe; English: enter); BYZ_NT:`εισελθη` (eiselthe; English: enter); TCG_NT:`εἰσέλθῃ` (eiselthe; English: enter); SBLGNT:`εἰσέλθῃ` (eiselthe; English: enter) |
| `αμην` (amen; English: Amen) | Mark 10:15 | 8 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`εἰσέλθῃ` (eiselthe; English: enter); BYZ_NT:`εισελθη` (eiselthe; English: enter); TCG_NT:`εἰσέλθῃ` (eiselthe; English: enter); SBLGNT:`εἰσέλθῃ` (eiselthe; English: enter) |
| `αμην` (amen; English: Amen) | Acts 22:28 | 14 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Παῦλος` (paulos; English: Paul); BYZ_NT:`παυλοσ` (paulos; English: Paul); TCG_NT:`Παῦλος` (paulos; English: Paul); SBLGNT:`Παῦλος` (paulos; English: Paul) |
| `αμην` (amen; English: Amen) | Luke 21:32 | 17 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`μὴ` (me; English: not); BYZ_NT:`μη` (me; English: not); TCG_NT:`μὴ` (me; English: not); SBLGNT:`μὴ` (me; English: not) |
| `αμην` (amen; English: Amen) | Matt 18:18 | 19 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`δήσητε` (desete; English: you bind); BYZ_NT:`δησητε` (desete; English: you bind); TCG_NT:`δήσητε` (desete; English: you bind); SBLGNT:`δήσητε` (desete; English: you bind) |
| `αραμ` (aram; English: Aram) | Phil 2:1 | -12 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`παράκλησις` (paraklesis; English: comfort/encouragement); BYZ_NT:`παρακλησισ` (paraklesis; English: comfort/encouragement); TCG_NT:`παράκλησις` (paraklesis; English: comfort/encouragement); SBLGNT:`παράκλησις` (paraklesis; English: comfort/encouragement) |
| `αραμ` (aram; English: Aram) | John 11:19 | -10 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἵνα` (hina; English: that); BYZ_NT:`ινα` (hina; English: that); TCG_NT:`ἵνα` (hina; English: that); SBLGNT:`ἵνα` (hina; English: that) |
| `αραμ` (aram; English: Aram) | 1Cor 16:6 | 24 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ὑμᾶς` (umas; English: you); BYZ_NT:`υμασ` (umas; English: you); TCG_NT:`ὑμᾶς` (umas; English: you); SBLGNT:`ὑμᾶς` (umas; English: you) |
| `ασηρ` (aser; English: Asher) | Luke 2:36 | -18 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`πολλαῖς` (pollais; English: many); BYZ_NT:`πολλαισ` (pollais; English: many); TCG_NT:`πολλαῖς,` (pollais; English: many); SBLGNT:`πολλαῖς,` (pollais; English: many) |
| `ασηρ` (aser; English: Asher) | Luke 3:1 | 16 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Πιλάτου` (pilatou; English: Pilate); BYZ_NT:`πιλατου` (pilatou; English: Pilate); TCG_NT:`Πιλάτου` (pilatou; English: Pilate); SBLGNT:`Πιλάτου` (pilatou; English: Pilate) |
| `χουσ` (chous; English: Cush) | Matt 6:2 | 27 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`οὖν` (oun; English: therefore); BYZ_NT:`ουν` (oun; English: therefore); TCG_NT:`οὖν` (oun; English: therefore); SBLGNT:`οὖν` (oun; English: therefore) |
| `δασα` (dasa; English: Lasha) | Acts 9:11 | -2 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Ταρσέα` (tarsea; English: of Tarsus); BYZ_NT:`ταρσεα` (tarsea; English: of Tarsus); TCG_NT:`Ταρσέα` (tarsea; English: of Tarsus); SBLGNT:`Ταρσέα,` (tarsea; English: of Tarsus) |
| `δασα` (dasa; English: Lasha) | Acts 5:10 | 30 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`εἰσελθόντες` (eiselthontes; English: having entered); BYZ_NT:`εισελθοντεσ` (eiselthontes; English: having entered); TCG_NT:`εἰσελθόντες` (eiselthontes; English: having entered); SBLGNT:`εἰσελθόντες` (eiselthontes; English: having entered) |
| `σαβα` (saba; English: Seba) | Jas 5:4 | 37 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`θερισάντων` (therisanton; English: having harvested); BYZ_NT:`θερισαντων` (therisanton; English: having harvested); TCG_NT:`θερισάντων` (therisanton; English: having harvested); SBLGNT:`θερισάντων` (therisanton; English: having harvested) |
| `σιων` (Sion; English: Zion) | 1Pet 2:6 | -25 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`καταισχυνθῇ` (kataischunthe; English: be put to shame); BYZ_NT:`καταισχυνθη` (kataischunthe; English: be put to shame); TCG_NT:`καταισχυνθῇ.` (kataischunthe; English: be put to shame); SBLGNT:`καταισχυνθῇ.` (kataischunthe; English: be put to shame) |
| `σιων` (Sion; English: Zion) | Acts 19:34 | -4 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἐπὶ` (epi; English: on/upon); BYZ_NT:`επι` (epi; English: on/upon); TCG_NT:`ἐπὶ` (epi; English: on/upon); SBLGNT:`ἐπὶ` (epi; English: on/upon) |
| `σιων` (Sion; English: Zion) | Matt 21:5 | 6 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἐπιβεβηκὼς` (epibebekos; English: having mounted); BYZ_NT:`επιβεβηκωσ` (epibebekos; English: having mounted); TCG_NT:`ἐπιβεβηκὼς` (epibebekos; English: having mounted); SBLGNT:`ἐπιβεβηκὼς` (epibebekos; English: having mounted) |
| `σιων` (Sion; English: Zion) | Rev 14:20 | 9 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`χαλινῶν` (chalinon; English: bridles); BYZ_NT:`χαλινων` (chalinon; English: bridles); TCG_NT:`χαλινῶν` (chalinon; English: bridles); SBLGNT:`χαλινῶν` (chalinon; English: bridles) |

## Read

This queue is broader and weaker than the phrase-extension gate. It is useful
for deciding which exact-center surface rows deserve matched controls.
It does not promote any row to claim status.
