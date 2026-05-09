# Greek Surface Prospective Control Pool

Status: real-word control-pool construction; no ELS control statistic yet.

This report prepares fair controls for the tighter expanded Greek surface
triage. It counts normalized surface-substring verse frequency for every
term in the expanded Greek prospective list, then selects same-length real
Greek terms with the closest surface-frequency vectors across TR_NT,
BYZ_NT, TCG_NT, and SBLGNT.
Selected target terms are excluded from the control candidate pool.

## Inputs

- Terms: `terms/greek_surface_prospective_terms.csv`
- Selected triage rows: `reports/greek_surface_prospective/selected_patterns.csv`

## Surface-Frequency Scope

- terms measured: 288
- all-source surface-present terms: 162
- selected targets: 0
- matched controls per target requested: 999

## Selected Targets

| Term | Concept | Length | Surface verse vector | Sum | Controls found |
| --- | --- | ---: | --- | ---: | ---: |

## Closest Controls

| Target | Control | Control concept | Surface vector | Sum delta | Vector delta |
| --- | --- | --- | --- | ---: | ---: |

## Read

This is a control-pool report, not a significance test. It uses the same
normalized substring rule as the current surface-context path and avoids
the bad control design of comparing surface-context rows against random
strings. The next step can freeze one matched-control set per target and
then run the ELS exact-center surface statistic against those real-word
controls.
