# Greek Surface New Terms Triage

Status: prospective triage under registered all-source length filter; no claim.

This report applies the registered all-source exact-center surface filter to
the locked Greek surface new-terms cohort.

## Inputs

- Term list: `terms/greek_surface_new_terms_clean_lock.csv`
- Surface patterns: `reports/greek_surface_new_terms/surface_patterns.csv`
- Term summary: `reports/greek_surface_new_terms/term_summary.csv`

## Filter

- keep only patterns present in every compared Greek NT source;
- require normalized term length >= 5;
- keep hidden-path-only rows as review candidates rather than failures;
- do not use random nonsense terms as surface controls, because surface
  context requires real words that can appear openly in a verse.

The length filter is deliberately mechanical. It excludes the dense length-4
bucket, including `αμην` (amen; English: Amen), without making a term-specific judgment about
which short terms are meaningful.

## Result

- selected patterns: 9
- selected terms: 5
- all-source patterns below length threshold: 0
- total cohort terms: 236

| Term | Concept | Length | Center | Skip | Direction | Length-cohort rank | Center words |
| --- | --- | ---: | --- | ---: | --- | ---: | --- |
| `ονομα` (onoma; English: Name) | ὄνομα | 5 | Luke 19:38 | -15 | backward | 1 | TR_NT:`Εὐλογημένος` (eulogemenos); BYZ_NT:`ευλογημενοσ` (eulogemenos); TCG_NT:`Εὐλογημένος` (eulogemenos); SBLGNT:`Εὐλογημένος` (eulogemenos) |
| `ονομα` (onoma; English: Name) | ὄνομα | 5 | Acts 9:28 | -3 | backward | 1 | TR_NT:`παρρησιαζόμενος` (parresiazomenos); BYZ_NT:`παρρησιαζομενοσ` (parresiazomenos); TCG_NT:`παρρησιαζόμενος` (parresiazomenos); SBLGNT:`παρρησιαζόμενος` (parresiazomenos) |
| `ονομα` (onoma; English: Name) | ὄνομα | 5 | Matt 10:2 | 3 | forward | 1 | TR_NT:`ὀνόματά` (onomata); BYZ_NT:`ονοματα` (onomata); TCG_NT:`ὀνόματά` (onomata); SBLGNT:`ὀνόματά` (onomata) |
| `ονομα` (onoma; English: Name) | ὄνομα | 5 | Phil 4:3 | 3 | forward | 1 | TR_NT:`ὀνόματα` (onomata); BYZ_NT:`ονοματα` (onomata); TCG_NT:`ὀνόματα` (onomata); SBLGNT:`ὀνόματα` (onomata) |
| `ονομα` (onoma; English: Name) | ὄνομα | 5 | Matt 24:9 | 27 | forward | 1 | TR_NT:`μισούμενοι` (misoumenoi); BYZ_NT:`μισουμενοι` (misoumenoi); TCG_NT:`μισούμενοι` (misoumenoi); SBLGNT:`μισούμενοι` (misoumenoi) |
| `οικοσ` (oikos; English: House) | οἶκος | 5 | Acts 16:31 | 4 | forward | 2 | TR_NT:`Κύριον` (kurion); BYZ_NT:`κυριον` (kurion); TCG_NT:`Κύριον` (kurion); SBLGNT:`κύριον` (kurion) |
| `σοφια` (sophia; English: wisdom) | σοφία | 5 | Acts 6:10 | -24 | backward | 3 | TR_NT:`σοφίᾳ` (sophia; English: wisdom); BYZ_NT:`σοφια` (sophia; English: wisdom); TCG_NT:`σοφίᾳ` (sophia; English: wisdom); SBLGNT:`σοφίᾳ` (sophia; English: wisdom) |
| `θυσια` (thusia; English: Sacrifice) | θυσία | 5 | Heb 10:11 | -36 | backward | 4 | TR_NT:`ἁμαρτίας` (amartias); BYZ_NT:`αμαρτιασ` (amartias); TCG_NT:`ἁμαρτίας·` (amartias); SBLGNT:`ἁμαρτίας.` (amartias) |
| `σκηνη` (skene; English: Tabernacle) | σκηνή | 5 | Heb 9:8 | -9 | backward | 5 | TR_NT:`τῆς` (tes; English: of the); BYZ_NT:`τησ` (tes; English: of the); TCG_NT:`τῆς` (tes; English: of the); SBLGNT:`τῆς` (tes; English: of the) |

## Cohort Counts

| Bucket | Terms |
| --- | ---: |
| multi-source broader surface queue | 4 |
| no exact-center surface pattern | 221 |
| selected | 5 |
| source-specific broader surface queue | 6 |

## Read

This creates a smaller review queue: `θυσια` (thusia; English: Sacrifice), `οικοσ` (oikos; English: House), `ονομα` (onoma; English: Name), `σκηνη` (skene; English: Tabernacle), `σοφια` (sophia; English: wisdom).
It is not a claim-grade result. The next statistically honest control
compares these rows against real Greek terms matched by length and
surface frequency, not against random strings that cannot satisfy the
surface-context condition.
