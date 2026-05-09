# Hebrew Version Presence Comparison

This compares the Hebrew exact-hit version-presence runs now tracked in
the project:

- `docs/HEBREW_HIT_VERSION_PRESENCE.md`
- `docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`
- `docs/HEBREW_CLAIM_VERSION_PRESENCE.md`
- `docs/HEBREW_CONTROL_VERSION_PRESENCE.md`
- `docs/HEBREW_SCREENING_VERSION_PRESENCE.md`

All runs use the same five MT-family source labels:

- `MT_WLC`
- `UXLC`
- `EBIBLE_WLC`
- `MAM`
- `UHB`

## Summary

| Run | Terms summarized | Hit records | Pattern rows | All-source rows | All-source rate | Source-specific rows |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Modern/local focus | 21 | 4,767 | 1,202 | 749 | 62.3% | 244 |
| Modern/geopolitical all Hebrew rows | 73 | 29,835 | 7,567 | 4,612 | 60.9% | 1,577 |
| Hebrew claim terms | 125 | 22,811 | 5,603 | 3,635 | 64.9% | 956 |
| Hebrew controls | 13 | 3,741 | 981 | 526 | 53.6% | 170 |
| Hebrew broader screening | 417 | 60,630 | 15,099 | 9,432 | 62.5% | 2,600 |

## Read

Version stability is common in all four runs, including controls. The control
run no longer has the highest all-source row rate after the current capped
extraction refresh, but it still produces hundreds of all-source rows from
scrambled and frequency-anchor terms. The all-row modern/geopolitical run and
the broader screening run land close to the focused and claim-term rates, again
showing that stability is common for short terms across related MT-family
streams.

That means exact version presence answers a narrow reproducibility question:

Which source streams preserve the same exact ref-key pattern?

It does not answer a significance question:

Is the pattern meaningful?

## Practical Rule

Use Hebrew version-presence reports as a review filter:

- all-source rows are easier to inspect across MT-family corpora;
- Leningrad-only rows should be labeled as Leningrad-family rows;
- source-specific rows should stay version-specific and should not be thrown
  away automatically;
- no row should be promoted without controls and context review.

The current comparison pushes interpretation away from modern or theological
claims and toward cautious review queues.
