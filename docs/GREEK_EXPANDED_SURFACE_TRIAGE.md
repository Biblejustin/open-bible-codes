# Greek Expanded Surface Triage

Status: post-screen triage; no claim and no p-value.

This report narrows the expanded Greek exact-center surface queue with a
mechanical filter before any future controls are designed.

## Inputs

- Term list: `terms/greek_expanded_prospective_terms.csv`
- Surface patterns: `reports/greek_expanded_surface_queue/surface_patterns.csv`
- Term summary: `reports/greek_expanded_surface_queue/term_summary.csv`

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

- selected patterns: 3
- selected terms: 3
- all-source patterns below length threshold: 24
- total cohort terms: 291

| Term | Concept | Length | Center | Skip | Direction | Length-cohort rank | Center words |
| --- | --- | ---: | --- | ---: | --- | ---: | --- |
| `ισαακ` (Isaak; English: Isaac) | Isaac | 5 | Heb 11:9 | -7 | backward | 1 | TR_NT:`κατοικήσας` (katoikesas); BYZ_NT:`κατοικησασ` (katoikesas); TCG_NT:`κατοικήσας` (katoikesas); SBLGNT:`κατοικήσας` (katoikesas) |
| `τερασ` (teras; English: Wonder) | Wonder | 5 | Heb 9:11 | -13 | backward | 2 | TR_NT:`χειροποιήτου` (cheiropoietou); BYZ_NT:`χειροποιητου` (cheiropoietou); TCG_NT:`χειροποιήτου,` (cheiropoietou); SBLGNT:`χειροποιήτου,` (cheiropoietou) |
| `ανομια` (anomia; English: Lawlessness) | Lawlessness | 6 | Matt 7:23 | 20 | forward | 1 | TR_NT:`Οὐδέποτε` (oudepote); BYZ_NT:`ουδεποτε` (oudepote); TCG_NT:`Οὐδέποτε` (oudepote); SBLGNT:`Οὐδέποτε` (oudepote) |

## Cohort Counts

| Bucket | Terms |
| --- | ---: |
| all-source but below length threshold | 7 |
| multi-source broader surface queue | 10 |
| no exact-center surface pattern | 265 |
| selected | 3 |
| source-specific broader surface queue | 6 |

## Read

This creates a smaller review queue: `ανομια` (anomia; English: Lawlessness), `ισαακ` (Isaak; English: Isaac), `τερασ` (teras; English: Wonder).
It is not a claim-grade result. The next statistically honest control
compares these rows against real Greek terms matched by length and
surface frequency, not against random strings that cannot satisfy the
surface-context condition.
