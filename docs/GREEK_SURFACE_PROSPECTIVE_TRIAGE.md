# Greek Surface Prospective Triage

Status: prospective triage under registered all-source length filter; no claim.

This report applies the registered all-source exact-center surface filter to
the locked Greek surface prospective cohort.

## Inputs

- Term list: `terms/greek_surface_prospective_terms.csv`
- Surface patterns: `reports/greek_surface_prospective/surface_patterns.csv`
- Term summary: `reports/greek_surface_prospective/term_summary.csv`

## Filter

- keep only patterns present in every compared Greek NT source;
- require normalized term length >= 5;
- keep hidden-path-only rows as review candidates rather than failures;
- do not use random nonsense terms as surface controls, because surface
  context requires real words that can appear openly in a verse.

The length filter is deliberately mechanical. It excludes the dense length-4
bucket, including `αμην` (amen; English: amen), without making a term-specific judgment about
which short terms are meaningful.

## Result

- selected patterns: 0
- selected terms: 0
- all-source patterns below length threshold: 24
- total cohort terms: 288

| Term | Concept | Length | Center | Skip | Direction | Length-cohort rank | Center words |
| --- | --- | ---: | --- | ---: | --- | ---: | --- |

## Cohort Counts

| Bucket | Terms |
| --- | ---: |
| all-source but below length threshold | 7 |
| multi-source broader surface queue | 10 |
| no exact-center surface pattern | 265 |
| source-specific broader surface queue | 6 |

## Read

No row met the registered all-source plus length threshold.
The all-source surface patterns found here were below the length threshold: 24.
This is a negative result for the primary prospective filter, not a claim.
