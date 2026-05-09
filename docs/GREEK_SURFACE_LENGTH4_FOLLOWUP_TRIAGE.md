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
| `αμην` | Amen | 4 | John 10:7 | -42 | backward | 1 | TR_NT:οὖν; BYZ_NT:ουν; TCG_NT:οὖν; SBLGNT:οὖν |
| `αμην` | Amen | 4 | John 6:53 | -42 | backward | 1 | TR_NT:ἀνθρώπου; BYZ_NT:ανθρωπου; TCG_NT:ἀνθρώπου; SBLGNT:ἀνθρώπου |
| `αμην` | Amen | 4 | Mark 8:12 | -13 | backward | 1 | TR_NT:ταύτῃ; BYZ_NT:ταυτη; TCG_NT:ταύτῃ; SBLGNT:ταύτῃ |
| `αμην` | Amen | 4 | Matt 5:18 | -8 | backward | 1 | TR_NT:ἰῶτα; BYZ_NT:ιωτα; TCG_NT:ἰῶτα; SBLGNT:ἰῶτα |
| `αμην` | Amen | 4 | Matt 18:13 | -7 | backward | 1 | TR_NT:λέγω; BYZ_NT:λεγω; TCG_NT:λέγω; SBLGNT:λέγω |
| `αμην` | Amen | 4 | John 5:24 | -3 | backward | 1 | TR_NT:ζωήν; BYZ_NT:ζωην; TCG_NT:ζωήν; SBLGNT:ζωήν. |
| `αμην` | Amen | 4 | Luke 18:17 | 8 | forward | 1 | TR_NT:εἰσέλθῃ; BYZ_NT:εισελθη; TCG_NT:εἰσέλθῃ; SBLGNT:εἰσέλθῃ |
| `αμην` | Amen | 4 | Mark 10:15 | 8 | forward | 1 | TR_NT:εἰσέλθῃ; BYZ_NT:εισελθη; TCG_NT:εἰσέλθῃ; SBLGNT:εἰσέλθῃ |
| `αμην` | Amen | 4 | Acts 22:28 | 14 | forward | 1 | TR_NT:Παῦλος; BYZ_NT:παυλοσ; TCG_NT:Παῦλος; SBLGNT:Παῦλος |
| `αμην` | Amen | 4 | Luke 21:32 | 17 | forward | 1 | TR_NT:μὴ; BYZ_NT:μη; TCG_NT:μὴ; SBLGNT:μὴ |
| `αμην` | Amen | 4 | Matt 18:18 | 19 | forward | 1 | TR_NT:δήσητε; BYZ_NT:δησητε; TCG_NT:δήσητε; SBLGNT:δήσητε |
| `σιων` | Zion | 4 | 1Pet 2:6 | -25 | backward | 2 | TR_NT:καταισχυνθῇ; BYZ_NT:καταισχυνθη; TCG_NT:καταισχυνθῇ.; SBLGNT:καταισχυνθῇ. |
| `σιων` | Zion | 4 | Acts 19:34 | -4 | backward | 2 | TR_NT:ἐπὶ; BYZ_NT:επι; TCG_NT:ἐπὶ; SBLGNT:ἐπὶ |
| `σιων` | Zion | 4 | Matt 21:5 | 6 | forward | 2 | TR_NT:ἐπιβεβηκὼς; BYZ_NT:επιβεβηκωσ; TCG_NT:ἐπιβεβηκὼς; SBLGNT:ἐπιβεβηκὼς |
| `σιων` | Zion | 4 | Rev 14:20 | 9 | forward | 2 | TR_NT:χαλινῶν; BYZ_NT:χαλινων; TCG_NT:χαλινῶν; SBLGNT:χαλινῶν |
| `αραμ` | Aram | 4 | Phil 2:1 | -12 | backward | 3 | TR_NT:παράκλησις; BYZ_NT:παρακλησισ; TCG_NT:παράκλησις; SBLGNT:παράκλησις |
| `αραμ` | Aram | 4 | John 11:19 | -10 | backward | 3 | TR_NT:ἵνα; BYZ_NT:ινα; TCG_NT:ἵνα; SBLGNT:ἵνα |
| `αραμ` | Aram | 4 | 1Cor 16:6 | 24 | forward | 3 | TR_NT:ὑμᾶς; BYZ_NT:υμασ; TCG_NT:ὑμᾶς; SBLGNT:ὑμᾶς |
| `δασα` | Lasha | 4 | Acts 9:11 | -2 | backward | 4 | TR_NT:Ταρσέα; BYZ_NT:ταρσεα; TCG_NT:Ταρσέα; SBLGNT:Ταρσέα, |
| `δασα` | Lasha | 4 | Acts 5:10 | 30 | forward | 4 | TR_NT:εἰσελθόντες; BYZ_NT:εισελθοντεσ; TCG_NT:εἰσελθόντες; SBLGNT:εἰσελθόντες |
| `ασηρ` | Asher | 4 | Luke 2:36 | -18 | backward | 5 | TR_NT:πολλαῖς; BYZ_NT:πολλαισ; TCG_NT:πολλαῖς,; SBLGNT:πολλαῖς, |
| `ασηρ` | Asher | 4 | Luke 3:1 | 16 | forward | 5 | TR_NT:Πιλάτου; BYZ_NT:πιλατου; TCG_NT:Πιλάτου; SBLGNT:Πιλάτου |
| `χουσ` | Cush | 4 | Matt 6:2 | 27 | forward | 6 | TR_NT:οὖν; BYZ_NT:ουν; TCG_NT:οὖν; SBLGNT:οὖν |
| `σαβα` | Seba | 4 | Jas 5:4 | 37 | forward | 7 | TR_NT:θερισάντων; BYZ_NT:θερισαντων; TCG_NT:θερισάντων; SBLGNT:θερισάντων |

## Cohort Counts

| Bucket | Terms |
| --- | ---: |
| multi-source broader surface queue | 10 |
| no exact-center surface pattern | 265 |
| selected | 7 |
| source-specific broader surface queue | 6 |

## Read

This creates a smaller review queue: `αμην`, `αραμ`, `ασηρ`, `δασα`, `σαβα`, `σιων`, `χουσ`.
It is not a claim-grade result. The next statistically honest control
compares these rows against real Greek terms matched by length and
surface frequency, not against random strings that cannot satisfy the
surface-context condition.
