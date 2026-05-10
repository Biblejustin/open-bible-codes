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
| `αμην` (amen; English: Amen) | Amen | 4 | John 10:7 | -42 | backward | 1 | TR_NT:`οὖν` (oun); BYZ_NT:`ουν` (oun); TCG_NT:`οὖν` (oun); SBLGNT:`οὖν` (oun) |
| `αμην` (amen; English: Amen) | Amen | 4 | John 6:53 | -42 | backward | 1 | TR_NT:`ἀνθρώπου` (anthropou); BYZ_NT:`ανθρωπου` (anthropou); TCG_NT:`ἀνθρώπου` (anthropou); SBLGNT:`ἀνθρώπου` (anthropou) |
| `αμην` (amen; English: Amen) | Amen | 4 | Mark 8:12 | -13 | backward | 1 | TR_NT:`ταύτῃ` (taute); BYZ_NT:`ταυτη` (taute); TCG_NT:`ταύτῃ` (taute); SBLGNT:`ταύτῃ` (taute) |
| `αμην` (amen; English: Amen) | Amen | 4 | Matt 5:18 | -8 | backward | 1 | TR_NT:`ἰῶτα` (iota); BYZ_NT:`ιωτα` (iota); TCG_NT:`ἰῶτα` (iota); SBLGNT:`ἰῶτα` (iota) |
| `αμην` (amen; English: Amen) | Amen | 4 | Matt 18:13 | -7 | backward | 1 | TR_NT:`λέγω` (lego); BYZ_NT:`λεγω` (lego); TCG_NT:`λέγω` (lego); SBLGNT:`λέγω` (lego) |
| `αμην` (amen; English: Amen) | Amen | 4 | John 5:24 | -3 | backward | 1 | TR_NT:`ζωήν` (zoen); BYZ_NT:`ζωην` (zoen); TCG_NT:`ζωήν` (zoen); SBLGNT:`ζωήν.` (zoen) |
| `αμην` (amen; English: Amen) | Amen | 4 | Luke 18:17 | 8 | forward | 1 | TR_NT:`εἰσέλθῃ` (eiselthe); BYZ_NT:`εισελθη` (eiselthe); TCG_NT:`εἰσέλθῃ` (eiselthe); SBLGNT:`εἰσέλθῃ` (eiselthe) |
| `αμην` (amen; English: Amen) | Amen | 4 | Mark 10:15 | 8 | forward | 1 | TR_NT:`εἰσέλθῃ` (eiselthe); BYZ_NT:`εισελθη` (eiselthe); TCG_NT:`εἰσέλθῃ` (eiselthe); SBLGNT:`εἰσέλθῃ` (eiselthe) |
| `αμην` (amen; English: Amen) | Amen | 4 | Acts 22:28 | 14 | forward | 1 | TR_NT:`Παῦλος` (paulos); BYZ_NT:`παυλοσ` (paulos); TCG_NT:`Παῦλος` (paulos); SBLGNT:`Παῦλος` (paulos) |
| `αμην` (amen; English: Amen) | Amen | 4 | Luke 21:32 | 17 | forward | 1 | TR_NT:`μὴ` (me); BYZ_NT:`μη` (me); TCG_NT:`μὴ` (me); SBLGNT:`μὴ` (me) |
| `αμην` (amen; English: Amen) | Amen | 4 | Matt 18:18 | 19 | forward | 1 | TR_NT:`δήσητε` (desete); BYZ_NT:`δησητε` (desete); TCG_NT:`δήσητε` (desete); SBLGNT:`δήσητε` (desete) |
| `σιων` (Sion; English: Zion) | Zion | 4 | 1Pet 2:6 | -25 | backward | 2 | TR_NT:`καταισχυνθῇ` (kataischunthe); BYZ_NT:`καταισχυνθη` (kataischunthe); TCG_NT:`καταισχυνθῇ.` (kataischunthe); SBLGNT:`καταισχυνθῇ.` (kataischunthe) |
| `σιων` (Sion; English: Zion) | Zion | 4 | Acts 19:34 | -4 | backward | 2 | TR_NT:`ἐπὶ` (epi); BYZ_NT:`επι` (epi); TCG_NT:`ἐπὶ` (epi); SBLGNT:`ἐπὶ` (epi) |
| `σιων` (Sion; English: Zion) | Zion | 4 | Matt 21:5 | 6 | forward | 2 | TR_NT:`ἐπιβεβηκὼς` (epibebekos); BYZ_NT:`επιβεβηκωσ` (epibebekos); TCG_NT:`ἐπιβεβηκὼς` (epibebekos); SBLGNT:`ἐπιβεβηκὼς` (epibebekos) |
| `σιων` (Sion; English: Zion) | Zion | 4 | Rev 14:20 | 9 | forward | 2 | TR_NT:`χαλινῶν` (chalinon); BYZ_NT:`χαλινων` (chalinon); TCG_NT:`χαλινῶν` (chalinon); SBLGNT:`χαλινῶν` (chalinon) |
| `αραμ` (aram; English: Aram) | Aram | 4 | Phil 2:1 | -12 | backward | 3 | TR_NT:`παράκλησις` (paraklesis); BYZ_NT:`παρακλησισ` (paraklesis); TCG_NT:`παράκλησις` (paraklesis); SBLGNT:`παράκλησις` (paraklesis) |
| `αραμ` (aram; English: Aram) | Aram | 4 | John 11:19 | -10 | backward | 3 | TR_NT:`ἵνα` (ina); BYZ_NT:`ινα` (ina); TCG_NT:`ἵνα` (ina); SBLGNT:`ἵνα` (ina) |
| `αραμ` (aram; English: Aram) | Aram | 4 | 1Cor 16:6 | 24 | forward | 3 | TR_NT:`ὑμᾶς` (umas); BYZ_NT:`υμασ` (umas); TCG_NT:`ὑμᾶς` (umas); SBLGNT:`ὑμᾶς` (umas) |
| `δασα` (dasa; English: Lasha) | Lasha | 4 | Acts 9:11 | -2 | backward | 4 | TR_NT:`Ταρσέα` (tarsea); BYZ_NT:`ταρσεα` (tarsea); TCG_NT:`Ταρσέα` (tarsea); SBLGNT:`Ταρσέα,` (tarsea) |
| `δασα` (dasa; English: Lasha) | Lasha | 4 | Acts 5:10 | 30 | forward | 4 | TR_NT:`εἰσελθόντες` (eiselthontes); BYZ_NT:`εισελθοντεσ` (eiselthontes); TCG_NT:`εἰσελθόντες` (eiselthontes); SBLGNT:`εἰσελθόντες` (eiselthontes) |
| `ασηρ` (aser; English: Asher) | Asher | 4 | Luke 2:36 | -18 | backward | 5 | TR_NT:`πολλαῖς` (pollais); BYZ_NT:`πολλαισ` (pollais); TCG_NT:`πολλαῖς,` (pollais); SBLGNT:`πολλαῖς,` (pollais) |
| `ασηρ` (aser; English: Asher) | Asher | 4 | Luke 3:1 | 16 | forward | 5 | TR_NT:`Πιλάτου` (pilatou); BYZ_NT:`πιλατου` (pilatou); TCG_NT:`Πιλάτου` (pilatou); SBLGNT:`Πιλάτου` (pilatou) |
| `χουσ` (chous; English: Cush) | Cush | 4 | Matt 6:2 | 27 | forward | 6 | TR_NT:`οὖν` (oun); BYZ_NT:`ουν` (oun); TCG_NT:`οὖν` (oun); SBLGNT:`οὖν` (oun) |
| `σαβα` (saba; English: Seba) | Seba | 4 | Jas 5:4 | 37 | forward | 7 | TR_NT:`θερισάντων` (therisanton); BYZ_NT:`θερισαντων` (therisanton); TCG_NT:`θερισάντων` (therisanton); SBLGNT:`θερισάντων` (therisanton) |

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
