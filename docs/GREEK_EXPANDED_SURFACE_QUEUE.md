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
| `αμην` | Amen | 101 | 44 | 11 | 14 | 19 | all-source surface queue; needs controls before interpretation |
| `σιων` | Zion | 37 | 17 | 4 | 5 | 8 | all-source surface queue; needs controls before interpretation |
| `αραμ` | Aram | 14 | 5 | 3 | 0 | 2 | all-source surface queue; needs controls before interpretation |
| `δασα` | Lasha | 36 | 21 | 2 | 7 | 12 | all-source surface queue; needs controls before interpretation |
| `ασηρ` | Asher | 14 | 5 | 2 | 2 | 1 | all-source surface queue; needs controls before interpretation |
| `χουσ` | Cush | 28 | 17 | 1 | 6 | 10 | all-source surface queue; needs controls before interpretation |
| `ισαακ` | Isaac | 10 | 4 | 1 | 3 | 0 | all-source surface queue; needs controls before interpretation |
| `τερασ` | Wonder | 10 | 5 | 1 | 2 | 2 | all-source surface queue; needs controls before interpretation |
| `σαβα` | Seba | 9 | 3 | 1 | 2 | 0 | all-source surface queue; needs controls before interpretation |
| `ανομια` | Lawlessness | 4 | 1 | 1 | 0 | 0 | all-source surface queue; needs controls before interpretation |
| `ιουδα` | Judah | 14 | 7 | 0 | 4 | 3 | multi-source surface queue; inspect source distribution |
| `λεων` | Lion | 9 | 5 | 0 | 3 | 2 | multi-source surface queue; inspect source distribution |
| `αδαμ` | Adam | 7 | 4 | 0 | 2 | 2 | multi-source surface queue; inspect source distribution |
| `ελαμ` | Elam | 6 | 3 | 0 | 2 | 1 | multi-source surface queue; inspect source distribution |
| `λευι` | Levi | 6 | 5 | 0 | 1 | 4 | multi-source surface queue; inspect source distribution |
| `μαρια` | Mary | 4 | 3 | 0 | 1 | 2 | multi-source surface queue; inspect source distribution |
| `ελισα` | Elishah | 3 | 2 | 0 | 1 | 1 | multi-source surface queue; inspect source distribution |
| `νομοσ` | Law | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `λουδ` | Lud | 3 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `πασχα` | Passover | 2 | 1 | 0 | 1 | 0 | multi-source surface queue; inspect source distribution |
| `σαλα` | Shelah | 2 | 2 | 0 | 0 | 2 | source-specific surface queue |
| `εικων` | Image | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ισραηλ` | Israel | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `ιακωβ` | Jacob | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `φρεαρ` | Pit | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |
| `οργη` | Wrath | 1 | 1 | 0 | 0 | 1 | source-specific surface queue |

## All-Source Pattern Examples

| Term | Center | Skip | Direction | Present | Center words |
| --- | --- | ---: | --- | --- | --- |
| `αμην` | John 10:7 | -42 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:οὖν; BYZ_NT:ουν; TCG_NT:οὖν; SBLGNT:οὖν |
| `αμην` | John 6:53 | -42 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ἀνθρώπου; BYZ_NT:ανθρωπου; TCG_NT:ἀνθρώπου; SBLGNT:ἀνθρώπου |
| `αμην` | Mark 8:12 | -13 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ταύτῃ; BYZ_NT:ταυτη; TCG_NT:ταύτῃ; SBLGNT:ταύτῃ |
| `αμην` | Matt 5:18 | -8 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ἰῶτα; BYZ_NT:ιωτα; TCG_NT:ἰῶτα; SBLGNT:ἰῶτα |
| `αμην` | Matt 18:13 | -7 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:λέγω; BYZ_NT:λεγω; TCG_NT:λέγω; SBLGNT:λέγω |
| `αμην` | John 5:24 | -3 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ζωήν; BYZ_NT:ζωην; TCG_NT:ζωήν; SBLGNT:ζωήν. |
| `αμην` | Luke 18:17 | 8 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:εἰσέλθῃ; BYZ_NT:εισελθη; TCG_NT:εἰσέλθῃ; SBLGNT:εἰσέλθῃ |
| `αμην` | Mark 10:15 | 8 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:εἰσέλθῃ; BYZ_NT:εισελθη; TCG_NT:εἰσέλθῃ; SBLGNT:εἰσέλθῃ |
| `αμην` | Acts 22:28 | 14 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:Παῦλος; BYZ_NT:παυλοσ; TCG_NT:Παῦλος; SBLGNT:Παῦλος |
| `αμην` | Luke 21:32 | 17 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:μὴ; BYZ_NT:μη; TCG_NT:μὴ; SBLGNT:μὴ |
| `αμην` | Matt 18:18 | 19 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:δήσητε; BYZ_NT:δησητε; TCG_NT:δήσητε; SBLGNT:δήσητε |
| `αραμ` | Phil 2:1 | -12 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:παράκλησις; BYZ_NT:παρακλησισ; TCG_NT:παράκλησις; SBLGNT:παράκλησις |
| `αραμ` | John 11:19 | -10 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ἵνα; BYZ_NT:ινα; TCG_NT:ἵνα; SBLGNT:ἵνα |
| `αραμ` | 1Cor 16:6 | 24 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ὑμᾶς; BYZ_NT:υμασ; TCG_NT:ὑμᾶς; SBLGNT:ὑμᾶς |
| `ασηρ` | Luke 2:36 | -18 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:πολλαῖς; BYZ_NT:πολλαισ; TCG_NT:πολλαῖς,; SBLGNT:πολλαῖς, |
| `ασηρ` | Luke 3:1 | 16 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:Πιλάτου; BYZ_NT:πιλατου; TCG_NT:Πιλάτου; SBLGNT:Πιλάτου |
| `χουσ` | Matt 6:2 | 27 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:οὖν; BYZ_NT:ουν; TCG_NT:οὖν; SBLGNT:οὖν |
| `ισαακ` | Heb 11:9 | -7 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:κατοικήσας; BYZ_NT:κατοικησασ; TCG_NT:κατοικήσας; SBLGNT:κατοικήσας |
| `δασα` | Acts 9:11 | -2 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:Ταρσέα; BYZ_NT:ταρσεα; TCG_NT:Ταρσέα; SBLGNT:Ταρσέα, |
| `δασα` | Acts 5:10 | 30 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:εἰσελθόντες; BYZ_NT:εισελθοντεσ; TCG_NT:εἰσελθόντες; SBLGNT:εἰσελθόντες |
| `ανομια` | Matt 7:23 | 20 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:Οὐδέποτε; BYZ_NT:ουδεποτε; TCG_NT:Οὐδέποτε; SBLGNT:Οὐδέποτε |
| `σαβα` | Jas 5:4 | 37 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:θερισάντων; BYZ_NT:θερισαντων; TCG_NT:θερισάντων; SBLGNT:θερισάντων |
| `τερασ` | Heb 9:11 | -13 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:χειροποιήτου; BYZ_NT:χειροποιητου; TCG_NT:χειροποιήτου,; SBLGNT:χειροποιήτου, |
| `σιων` | 1Pet 2:6 | -25 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:καταισχυνθῇ; BYZ_NT:καταισχυνθη; TCG_NT:καταισχυνθῇ.; SBLGNT:καταισχυνθῇ. |
| `σιων` | Acts 19:34 | -4 | backward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ἐπὶ; BYZ_NT:επι; TCG_NT:ἐπὶ; SBLGNT:ἐπὶ |
| `σιων` | Matt 21:5 | 6 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:ἐπιβεβηκὼς; BYZ_NT:επιβεβηκωσ; TCG_NT:ἐπιβεβηκὼς; SBLGNT:ἐπιβεβηκὼς |
| `σιων` | Rev 14:20 | 9 | forward | TR_NT,BYZ_NT,TCG_NT,SBLGNT | TR_NT:χαλινῶν; BYZ_NT:χαλινων; TCG_NT:χαλινῶν; SBLGNT:χαλινῶν |

## Read

This queue is broader and weaker than the phrase-extension gate. It is useful
for deciding which exact-center surface rows deserve matched controls.
It does not promote any row to claim status.
