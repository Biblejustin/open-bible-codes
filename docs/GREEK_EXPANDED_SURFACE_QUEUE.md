# Greek Expanded Surface Queue

Status: post-screen exact-center surface queue; no claim.

This report summarizes exact-center surface hits from the expanded Greek
prospective term screen. It does not require same-skip phrase extension and
does not run controls.

## Inputs

- Surface hits: `reports/greek_expanded_prospective_exact_center/surface_context_hits.csv`
- Term scope: `terms/greek_expanded_prospective_terms.csv`
- Compared sources: TR_NT, BYZ_NT, TCG_NT, SBLGNT

## Definition

`exact-center surface` means the ELS hit center falls in a verse where the
normalized term also appears as ordinary surface text. The `Center words`
column reports the actual word at the ELS center offset, so it may differ
from the searched term.

## Scope Counts

| Scope | Patterns |
| --- | ---: |
| `all_sources` | 27 |
| `multi_source` | 58 |
| `source_only` | 76 |

Total exact-center surface patterns: 161.

## Top Term Queue

| Term | Concept | Exact-center hits | Unique patterns | All-source | Multi-source | Source-specific | Read |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| `αμην` (amen; English: Amen) | Amen | 101 | 44 | 11 | 14 | 19 | all-source surface queue; needs controls before interpretation |
| `σιων` (sion; English: Zion) | Zion | 37 | 17 | 4 | 5 | 8 | all-source surface queue; needs controls before interpretation |
| `αραμ` (aram; English: Aram) | Aram | 14 | 5 | 3 | 0 | 2 | all-source surface queue; needs controls before interpretation |
| `δασα` (dasa; English: Lasha) | Lasha | 36 | 21 | 2 | 7 | 12 | all-source surface queue; needs controls before interpretation |
| `ασηρ` (aser; English: Asher) | Asher | 14 | 5 | 2 | 2 | 1 | all-source surface queue; needs controls before interpretation |
| `χουσ` (chous; English: Cush) | Cush | 28 | 17 | 1 | 6 | 10 | all-source surface queue; needs controls before interpretation |
| `ισαακ` (Isaak; English: Isaac) | Isaac | 10 | 4 | 1 | 3 | 0 | all-source surface queue; needs controls before interpretation |
| `τερασ` (teras; English: Wonder) | Wonder | 10 | 5 | 1 | 2 | 2 | all-source surface queue; needs controls before interpretation |
| `σαβα` (saba; English: Seba) | Seba | 9 | 3 | 1 | 2 | 0 | all-source surface queue; needs controls before interpretation |
| `ανομια` (anomia; English: Lawlessness) | Lawlessness | 4 | 1 | 1 | 0 | 0 | all-source surface queue; needs controls before interpretation |
| `ιουδα` (iouda; English: Judah) | Judah | 14 | 7 | 0 | 4 | 3 | multi-source surface queue; inspect source distribution |
| `λεων` (leon; English: Lion) | Lion | 9 | 5 | 0 | 3 | 2 | multi-source surface queue; inspect source distribution |
| `αδαμ` (adam; English: Adam) | Adam | 7 | 4 | 0 | 2 | 2 | multi-source surface queue; inspect source distribution |
| `ελαμ` (elam; English: Elam) | Elam | 6 | 3 | 0 | 2 | 1 | multi-source surface queue; inspect source distribution |
| `λευι` (leui; English: Levi) | Levi | 6 | 5 | 0 | 1 | 4 | multi-source surface queue; inspect source distribution |
| `μαρια` (maria; English: Mary) | Mary | 4 | 3 | 0 | 1 | 2 | multi-source surface queue; inspect source distribution |
| `ελισα` (elisa; English: Elishah) | Elishah | 3 | 2 | 0 | 1 | 1 | multi-source surface queue; inspect source distribution |
| `νομοσ` (nomos; English: Law) | Law | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `λουδ` (loud; English: Lud) | Lud | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `πασχα` (pascha; English: Passover) | Passover | 2 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `σαλα` (sala; English: Shelah) | Shelah | 2 | 2 | 0 | 0 | 2 | source-specific surface queue |
| `εικων` (eikon; English: Image) | Image | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ισραηλ` (israel; English: Israel) | Israel | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ιακωβ` (iakob; English: Jacob) | Jacob | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `φρεαρ` (phrear; English: Pit) | Pit | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `οργη` (orge; English: Wrath) | Wrath | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |

## All-Source Pattern Examples

| Term | Center | Skip | Direction | Present | Center words |
| --- | --- | ---: | --- | --- | --- |
| `αμην` (amen; English: Amen) | John 10:7 | -42 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`οὖν` (oun); BYZ_NT:`ουν` (oun); TCG_NT:`οὖν` (oun); SBLGNT:`οὖν` (oun) |
| `αμην` (amen; English: Amen) | John 6:53 | -42 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἀνθρώπου` (anthropou); BYZ_NT:`ανθρωπου` (anthropou); TCG_NT:`ἀνθρώπου` (anthropou); SBLGNT:`ἀνθρώπου` (anthropou) |
| `αμην` (amen; English: Amen) | Mark 8:12 | -13 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ταύτῃ` (taute); BYZ_NT:`ταυτη` (taute); TCG_NT:`ταύτῃ` (taute); SBLGNT:`ταύτῃ` (taute) |
| `αμην` (amen; English: Amen) | Matt 5:18 | -8 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἰῶτα` (iota); BYZ_NT:`ιωτα` (iota); TCG_NT:`ἰῶτα` (iota); SBLGNT:`ἰῶτα` (iota) |
| `αμην` (amen; English: Amen) | Matt 18:13 | -7 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`λέγω` (lego); BYZ_NT:`λεγω` (lego); TCG_NT:`λέγω` (lego); SBLGNT:`λέγω` (lego) |
| `αμην` (amen; English: Amen) | John 5:24 | -3 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ζωήν` (zoen); BYZ_NT:`ζωην` (zoen); TCG_NT:`ζωήν` (zoen); SBLGNT:`ζωήν.` (zoen) |
| `αμην` (amen; English: Amen) | Luke 18:17 | 8 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`εἰσέλθῃ` (eiselthe); BYZ_NT:`εισελθη` (eiselthe); TCG_NT:`εἰσέλθῃ` (eiselthe); SBLGNT:`εἰσέλθῃ` (eiselthe) |
| `αμην` (amen; English: Amen) | Mark 10:15 | 8 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`εἰσέλθῃ` (eiselthe); BYZ_NT:`εισελθη` (eiselthe); TCG_NT:`εἰσέλθῃ` (eiselthe); SBLGNT:`εἰσέλθῃ` (eiselthe) |
| `αμην` (amen; English: Amen) | Acts 22:28 | 14 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Παῦλος` (paulos); BYZ_NT:`παυλοσ` (paulos); TCG_NT:`Παῦλος` (paulos); SBLGNT:`Παῦλος` (paulos) |
| `αμην` (amen; English: Amen) | Luke 21:32 | 17 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`μὴ` (me); BYZ_NT:`μη` (me); TCG_NT:`μὴ` (me); SBLGNT:`μὴ` (me) |
| `αμην` (amen; English: Amen) | Matt 18:18 | 19 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`δήσητε` (desete); BYZ_NT:`δησητε` (desete); TCG_NT:`δήσητε` (desete); SBLGNT:`δήσητε` (desete) |
| `αραμ` (aram; English: Aram) | Phil 2:1 | -12 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`παράκλησις` (paraklesis); BYZ_NT:`παρακλησισ` (paraklesis); TCG_NT:`παράκλησις` (paraklesis); SBLGNT:`παράκλησις` (paraklesis) |
| `αραμ` (aram; English: Aram) | John 11:19 | -10 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἵνα` (ina); BYZ_NT:`ινα` (ina); TCG_NT:`ἵνα` (ina); SBLGNT:`ἵνα` (ina) |
| `αραμ` (aram; English: Aram) | 1Cor 16:6 | 24 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ὑμᾶς` (umas); BYZ_NT:`υμασ` (umas); TCG_NT:`ὑμᾶς` (umas); SBLGNT:`ὑμᾶς` (umas) |
| `ασηρ` (aser; English: Asher) | Luke 2:36 | -18 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`πολλαῖς` (pollais); BYZ_NT:`πολλαισ` (pollais); TCG_NT:`πολλαῖς,` (pollais); SBLGNT:`πολλαῖς,` (pollais) |
| `ασηρ` (aser; English: Asher) | Luke 3:1 | 16 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Πιλάτου` (pilatou); BYZ_NT:`πιλατου` (pilatou); TCG_NT:`Πιλάτου` (pilatou); SBLGNT:`Πιλάτου` (pilatou) |
| `χουσ` (chous; English: Cush) | Matt 6:2 | 27 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`οὖν` (oun); BYZ_NT:`ουν` (oun); TCG_NT:`οὖν` (oun); SBLGNT:`οὖν` (oun) |
| `ισαακ` (Isaak; English: Isaac) | Heb 11:9 | -7 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`κατοικήσας` (katoikesas); BYZ_NT:`κατοικησασ` (katoikesas); TCG_NT:`κατοικήσας` (katoikesas); SBLGNT:`κατοικήσας` (katoikesas) |
| `δασα` (dasa; English: Lasha) | Acts 9:11 | -2 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Ταρσέα` (tarsea); BYZ_NT:`ταρσεα` (tarsea); TCG_NT:`Ταρσέα` (tarsea); SBLGNT:`Ταρσέα,` (tarsea) |
| `δασα` (dasa; English: Lasha) | Acts 5:10 | 30 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`εἰσελθόντες` (eiselthontes); BYZ_NT:`εισελθοντεσ` (eiselthontes); TCG_NT:`εἰσελθόντες` (eiselthontes); SBLGNT:`εἰσελθόντες` (eiselthontes) |
| `ανομια` (anomia; English: Lawlessness) | Matt 7:23 | 20 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`Οὐδέποτε` (oudepote); BYZ_NT:`ουδεποτε` (oudepote); TCG_NT:`Οὐδέποτε` (oudepote); SBLGNT:`Οὐδέποτε` (oudepote) |
| `σαβα` (saba; English: Seba) | Jas 5:4 | 37 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`θερισάντων` (therisanton); BYZ_NT:`θερισαντων` (therisanton); TCG_NT:`θερισάντων` (therisanton); SBLGNT:`θερισάντων` (therisanton) |
| `τερασ` (teras; English: Wonder) | Heb 9:11 | -13 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`χειροποιήτου` (cheiropoietou); BYZ_NT:`χειροποιητου` (cheiropoietou); TCG_NT:`χειροποιήτου,` (cheiropoietou); SBLGNT:`χειροποιήτου,` (cheiropoietou) |
| `σιων` (sion; English: Zion) | 1Pet 2:6 | -25 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`καταισχυνθῇ` (kataischunthe); BYZ_NT:`καταισχυνθη` (kataischunthe); TCG_NT:`καταισχυνθῇ.` (kataischunthe); SBLGNT:`καταισχυνθῇ.` (kataischunthe) |
| `σιων` (sion; English: Zion) | Acts 19:34 | -4 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἐπὶ` (epi); BYZ_NT:`επι` (epi); TCG_NT:`ἐπὶ` (epi); SBLGNT:`ἐπὶ` (epi) |
| `σιων` (sion; English: Zion) | Matt 21:5 | 6 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`ἐπιβεβηκὼς` (epibebekos); BYZ_NT:`επιβεβηκωσ` (epibebekos); TCG_NT:`ἐπιβεβηκὼς` (epibebekos); SBLGNT:`ἐπιβεβηκὼς` (epibebekos) |
| `σιων` (sion; English: Zion) | Rev 14:20 | 9 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:`χαλινῶν` (chalinon); BYZ_NT:`χαλινων` (chalinon); TCG_NT:`χαλινῶν` (chalinon); SBLGNT:`χαλινῶν` (chalinon) |

## Read

This queue is broader and weaker than the phrase-extension gate. It is useful
for deciding which exact-center surface rows deserve matched controls.
It does not promote any row to claim status.
