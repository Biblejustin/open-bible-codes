# Greek Surface Length-4 Follow-Up Triage

Status: post-discovery length-4 follow-up; no claim.

This report follows up the all-source length-4 bucket exposed by the locked
Greek surface prospective run. It is not prospective discovery.

## Inputs

- Term list: `terms/greek_surface_prospective_terms.csv`
- Surface patterns: `reports/greek_surface_prospective/surface_patterns.csv`
- Term summary: `reports/greek_surface_prospective/term_summary.csv`

## Filter

- keep only patterns present in every compared Greek NT source;
- require normalized term length >= 4;
- keep hidden-path-only rows as review candidates rather than failures;
- do not use random nonsense terms as surface controls, because surface
  context requires real words that can appear openly in a verse.

This follow-up deliberately includes the dense length-4 bucket. Treat
short-form all-source rows as post-discovery review material unless a
separate prospective study registers them in advance.

## Result

- selected patterns: 24
- selected terms: 7
- all-source patterns below length threshold: 0
- total cohort terms: 288

| Term | Concept | Length | Center | Skip | Direction | Length-cohort rank | Center words |
| --- | --- | ---: | --- | ---: | --- | ---: | --- |
| `αμην` (amen; English: Amen) | Amen | 4 | John 10:7 | -42 | backward | 1 | TR_NT:`οὖν` (oun; English: therefore); BYZ_NT:`ουν` (oun; English: therefore); TCG_NT:`οὖν` (oun; English: therefore); SBLGNT:`οὖν` (oun; English: therefore) |
| `αμην` (amen; English: Amen) | Amen | 4 | John 6:53 | -42 | backward | 1 | TR_NT:`ἀνθρώπου` (anthropou; English: man/human); BYZ_NT:`ανθρωπου` (anthropou; English: man/human); TCG_NT:`ἀνθρώπου` (anthropou; English: man/human); SBLGNT:`ἀνθρώπου` (anthropou; English: man/human) |
| `αμην` (amen; English: Amen) | Amen | 4 | Mark 8:12 | -13 | backward | 1 | TR_NT:`ταύτῃ` (taute; English: to this/in this); BYZ_NT:`ταυτη` (taute; English: to this/in this); TCG_NT:`ταύτῃ` (taute; English: to this/in this); SBLGNT:`ταύτῃ` (taute; English: to this/in this) |
| `αμην` (amen; English: Amen) | Amen | 4 | Matt 5:18 | -8 | backward | 1 | TR_NT:`ἰῶτα` (iota; English: iota); BYZ_NT:`ιωτα` (iota; English: iota); TCG_NT:`ἰῶτα` (iota; English: iota); SBLGNT:`ἰῶτα` (iota; English: iota) |
| `αμην` (amen; English: Amen) | Amen | 4 | Matt 18:13 | -7 | backward | 1 | TR_NT:`λέγω` (lego; English: I say); BYZ_NT:`λεγω` (lego; English: I say); TCG_NT:`λέγω` (lego; English: I say); SBLGNT:`λέγω` (lego; English: I say) |
| `αμην` (amen; English: Amen) | Amen | 4 | John 5:24 | -3 | backward | 1 | TR_NT:`ζωήν` (zoen; English: life); BYZ_NT:`ζωην` (zoen; English: life); TCG_NT:`ζωήν` (zoen; English: life); SBLGNT:`ζωήν.` (zoen; English: life) |
| `αμην` (amen; English: Amen) | Amen | 4 | Luke 18:17 | 8 | forward | 1 | TR_NT:`εἰσέλθῃ` (eiselthe; English: enter); BYZ_NT:`εισελθη` (eiselthe; English: enter); TCG_NT:`εἰσέλθῃ` (eiselthe; English: enter); SBLGNT:`εἰσέλθῃ` (eiselthe; English: enter) |
| `αμην` (amen; English: Amen) | Amen | 4 | Mark 10:15 | 8 | forward | 1 | TR_NT:`εἰσέλθῃ` (eiselthe; English: enter); BYZ_NT:`εισελθη` (eiselthe; English: enter); TCG_NT:`εἰσέλθῃ` (eiselthe; English: enter); SBLGNT:`εἰσέλθῃ` (eiselthe; English: enter) |
| `αμην` (amen; English: Amen) | Amen | 4 | Acts 22:28 | 14 | forward | 1 | TR_NT:`Παῦλος` (paulos; English: Paul); BYZ_NT:`παυλοσ` (paulos; English: Paul); TCG_NT:`Παῦλος` (paulos; English: Paul); SBLGNT:`Παῦλος` (paulos; English: Paul) |
| `αμην` (amen; English: Amen) | Amen | 4 | Luke 21:32 | 17 | forward | 1 | TR_NT:`μὴ` (me; English: not); BYZ_NT:`μη` (me; English: not); TCG_NT:`μὴ` (me; English: not); SBLGNT:`μὴ` (me; English: not) |
| `αμην` (amen; English: Amen) | Amen | 4 | Matt 18:18 | 19 | forward | 1 | TR_NT:`δήσητε` (desete; English: you bind); BYZ_NT:`δησητε` (desete; English: you bind); TCG_NT:`δήσητε` (desete; English: you bind); SBLGNT:`δήσητε` (desete; English: you bind) |
| `σιων` (Sion; English: Zion) | Zion | 4 | 1Pet 2:6 | -25 | backward | 2 | TR_NT:`καταισχυνθῇ` (kataischunthe; English: be put to shame); BYZ_NT:`καταισχυνθη` (kataischunthe; English: be put to shame); TCG_NT:`καταισχυνθῇ.` (kataischunthe; English: be put to shame); SBLGNT:`καταισχυνθῇ.` (kataischunthe; English: be put to shame) |
| `σιων` (Sion; English: Zion) | Zion | 4 | Acts 19:34 | -4 | backward | 2 | TR_NT:`ἐπὶ` (epi; English: on/upon); BYZ_NT:`επι` (epi; English: on/upon); TCG_NT:`ἐπὶ` (epi; English: on/upon); SBLGNT:`ἐπὶ` (epi; English: on/upon) |
| `σιων` (Sion; English: Zion) | Zion | 4 | Matt 21:5 | 6 | forward | 2 | TR_NT:`ἐπιβεβηκὼς` (epibebekos; English: having mounted); BYZ_NT:`επιβεβηκωσ` (epibebekos; English: having mounted); TCG_NT:`ἐπιβεβηκὼς` (epibebekos; English: having mounted); SBLGNT:`ἐπιβεβηκὼς` (epibebekos; English: having mounted) |
| `σιων` (Sion; English: Zion) | Zion | 4 | Rev 14:20 | 9 | forward | 2 | TR_NT:`χαλινῶν` (chalinon; English: bridles); BYZ_NT:`χαλινων` (chalinon; English: bridles); TCG_NT:`χαλινῶν` (chalinon; English: bridles); SBLGNT:`χαλινῶν` (chalinon; English: bridles) |
| `αραμ` (aram; English: Aram) | Aram | 4 | Phil 2:1 | -12 | backward | 3 | TR_NT:`παράκλησις` (paraklesis; English: comfort/encouragement); BYZ_NT:`παρακλησισ` (paraklesis; English: comfort/encouragement); TCG_NT:`παράκλησις` (paraklesis; English: comfort/encouragement); SBLGNT:`παράκλησις` (paraklesis; English: comfort/encouragement) |
| `αραμ` (aram; English: Aram) | Aram | 4 | John 11:19 | -10 | backward | 3 | TR_NT:`ἵνα` (hina; English: that); BYZ_NT:`ινα` (hina; English: that); TCG_NT:`ἵνα` (hina; English: that); SBLGNT:`ἵνα` (hina; English: that) |
| `αραμ` (aram; English: Aram) | Aram | 4 | 1Cor 16:6 | 24 | forward | 3 | TR_NT:`ὑμᾶς` (umas; English: you); BYZ_NT:`υμασ` (umas; English: you); TCG_NT:`ὑμᾶς` (umas; English: you); SBLGNT:`ὑμᾶς` (umas; English: you) |
| `δασα` (dasa; English: Lasha) | Lasha | 4 | Acts 9:11 | -2 | backward | 4 | TR_NT:`Ταρσέα` (tarsea; English: of Tarsus); BYZ_NT:`ταρσεα` (tarsea; English: of Tarsus); TCG_NT:`Ταρσέα` (tarsea; English: of Tarsus); SBLGNT:`Ταρσέα,` (tarsea; English: of Tarsus) |
| `δασα` (dasa; English: Lasha) | Lasha | 4 | Acts 5:10 | 30 | forward | 4 | TR_NT:`εἰσελθόντες` (eiselthontes; English: having entered); BYZ_NT:`εισελθοντεσ` (eiselthontes; English: having entered); TCG_NT:`εἰσελθόντες` (eiselthontes; English: having entered); SBLGNT:`εἰσελθόντες` (eiselthontes; English: having entered) |
| `ασηρ` (aser; English: Asher) | Asher | 4 | Luke 2:36 | -18 | backward | 5 | TR_NT:`πολλαῖς` (pollais; English: many); BYZ_NT:`πολλαισ` (pollais; English: many); TCG_NT:`πολλαῖς,` (pollais; English: many); SBLGNT:`πολλαῖς,` (pollais; English: many) |
| `ασηρ` (aser; English: Asher) | Asher | 4 | Luke 3:1 | 16 | forward | 5 | TR_NT:`Πιλάτου` (pilatou; English: Pilate); BYZ_NT:`πιλατου` (pilatou; English: Pilate); TCG_NT:`Πιλάτου` (pilatou; English: Pilate); SBLGNT:`Πιλάτου` (pilatou; English: Pilate) |
| `χουσ` (chous; English: Cush) | Cush | 4 | Matt 6:2 | 27 | forward | 6 | TR_NT:`οὖν` (oun; English: therefore); BYZ_NT:`ουν` (oun; English: therefore); TCG_NT:`οὖν` (oun; English: therefore); SBLGNT:`οὖν` (oun; English: therefore) |
| `σαβα` (saba; English: Seba) | Seba | 4 | Jas 5:4 | 37 | forward | 7 | TR_NT:`θερισάντων` (therisanton; English: having harvested); BYZ_NT:`θερισαντων` (therisanton; English: having harvested); TCG_NT:`θερισάντων` (therisanton; English: having harvested); SBLGNT:`θερισάντων` (therisanton; English: having harvested) |

## Cohort Counts

| Bucket | Terms |
| --- | ---: |
| multi-source broader surface queue | 10 |
| no exact-center surface pattern | 265 |
| selected | 7 |
| source-specific broader surface queue | 6 |

## Read

This creates a smaller review queue: `αμην` (amen; English: Amen), `αραμ` (aram; English: Aram), `ασηρ` (aser; English: Asher), `δασα` (dasa; English: Lasha), `σαβα` (saba; English: Seba), `σιων` (Sion; English: Zion), `χουσ` (chous; English: Cush).
It is not a claim-grade result. The next statistically honest control
compares these rows against real Greek terms matched by length and
surface frequency, not against random strings that cannot satisfy the
surface-context condition.
