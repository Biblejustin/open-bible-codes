# Hebrew Version-Specific Distribution

This summarizes where version-specific exact-hit rows land across the three
Hebrew version-presence screens:

- Modern/local focus
- Hebrew claim terms
- Hebrew null/frequency controls
- Hebrew broader screening

## Source-Specific Rows

Rows labeled `source_specific` are exact ref-key patterns found in only one of
the five observed Hebrew streams.

| Run | MAM-only | UHB-only | UXLC-only | EBIBLE_WLC-only | MT_WLC-only |
| --- | ---: | ---: | ---: | ---: | ---: |
| Modern/local focus | 137 | 88 | 8 | 2 | 0 |
| Hebrew claim terms | 417 | 403 | 41 | 2 | 0 |
| Hebrew controls | 53 | 60 | 9 | 3 | 0 |
| Hebrew broader screening | 956 | 1,084 | 111 | 22 | 2 |

## Leningrad-Family Rows

Rows labeled `present_all_leningrad_streams` are present in all three
Leningrad-family streams (`MT_WLC`, `UXLC`, `EBIBLE_WLC`) but not every observed
Hebrew source.

| Run | Missing MAM only | Missing UHB only | Missing both MAM and UHB |
| --- | ---: | ---: | ---: |
| Modern/local focus | 98 | 59 | 29 |
| Hebrew claim terms | 288 | 324 | 109 |
| Hebrew controls | 43 | 46 | 13 |
| Hebrew broader screening | 756 | 887 | 230 |

## Current Read

Most version-specific behavior comes from MAM and UHB. That matches what the
source comparison already suggested: the three Leningrad-family streams are
very close to each other, while MAM and UHB introduce more ref-key shifts,
normalization differences, or verse coverage differences.

`MT_WLC` has no one-source-only rows in the first three screens and only 2 in
the broader screen. `EBIBLE_WLC` has very few. That is expected because eBible
WLC is mostly a packaging/check stream for the same Leningrad tradition.

## Practical Rule

When reviewing a Hebrew hit:

- all-source rows are the easiest review targets;
- Leningrad-family rows should be labeled as Leningrad-family, not universal MT;
- MAM-only and UHB-only rows should be reviewed as source-specific;
- source-specific rows should not be treated as broken or invalid, but they
  should not be promoted as cross-version support.
