# Greek Version Presence Comparison

This compares the Greek NT exact-hit version-presence runs:

- `docs/GREEK_NT_CLAIM_VERSION_PRESENCE.md`
- `docs/GREEK_CONTROL_VERSION_PRESENCE.md`

## Summary

| Run | Terms summarized | Hit records | Pattern rows | All-source rows | All-source rate | Source-specific rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Greek NT claim terms | 32 | 1,467 | 787 | 109 | 13.9% | 428 |
| Greek controls | 19 | 2,003 | 826 | 270 | 32.7% | 319 |

## Source-Specific Rows

| Run | SBLGNT-only | BYZ_NT-only | TR_NT-only | TCG_NT-only |
| --- | ---: | ---: | ---: | ---: |
| Greek NT claim terms | 212 | 97 | 73 | 46 |
| Greek controls | 160 | 63 | 64 | 32 |

## Current Read

Greek NT patterns are more version-sensitive than the Hebrew MT-family screens.
The common multi-source shape is often `BYZ_NT,TCG_NT,TR_NT` with SBLGNT absent,
or SBLGNT-only.

Controls again prevent over-reading:

- Greek controls have a higher all-source rate than Greek claim terms.
- Scrambled Theos has 72 all-source exact patterns.
- Common content anchors like `λαοσ`, `χειρ`, and `οικοσ` are dense and stable.

## Practical Rule

For Greek NT review:

- all-source rows are useful review candidates;
- `BYZ_NT,TCG_NT,TR_NT` rows should be labeled as non-SBLGNT shared rows, not
  universal Greek NT rows;
- SBLGNT-only rows can still matter as critical-text review rows, but they do
  not provide cross-version support;
- controls remain mandatory before any interpretive claim.
