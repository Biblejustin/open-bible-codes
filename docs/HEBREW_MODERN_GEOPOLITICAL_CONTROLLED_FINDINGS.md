# Hebrew Modern Geopolitical Controlled Findings

Status: generated controlled follow-up complete; no claim-grade row.

Source report:

- `docs/HEBREW_MODERN_GEOPOLITICAL_VERSION_PRESENCE.md`
- `docs/HEBREW_MODERN_GEOPOLITICAL_CONTROLLED_REVIEW.md`

## What Was Run

The broad Hebrew modern/geopolitical run checked every Hebrew row in
`terms/modern_names_dates.csv` across MT_WLC, UXLC, EBIBLE_WLC, MAM, and UHB
with skip `2..100`, both directions, and max `200` hits per term per corpus.

The controlled review then ran representative paired controls for nonzero rows
in MT_WLC and UHB:

- shuffled-letter controls preserving target letters;
- same-length random controls drawn from same-corpus letter frequencies;
- `100` samples for each control family;
- Benjamini-Hochberg correction across emitted representative rows.

## Results

| Metric | Count |
| --- | ---: |
| Target rows | 73 |
| Representative-control rows | 108 |
| Terms with representative controls | 54 |
| Terms not unusual under representative controls | 50 |
| Terms with only uncorrected p<=0.05 prompts | 4 |
| Terms with adjusted representative-control support | 0 |
| Terms absent in capped exact-version matrix | 18 |

Uncorrected-only prompts:

| Term | Concept | Exact hits | Best p | Best q |
| --- | --- | ---: | ---: | ---: |
| `iraq_h` | Iraq | 385 | 0.039604 | 0.840171 |
| `germany_h` | Germany | 38 | 0.049505 | 0.840171 |
| `2027_additive_h` | Gregorian 2027 additive | 11 | 0.049505 | 0.840171 |
| `2025_additive_h` | Gregorian 2025 additive | 6 | 0.039604 | 0.840171 |

Those rows are review prompts only. They did not survive the row-family
correction.

## Requested Terms

Current read for selected requested terms:

| Term ID | Exact read | Control read |
| --- | --- | --- |
| `trump_h` | present; 31 capped hits; 6 all-source exact patterns | not unusual |
| `vance_h` | present; capped at 1000 hits; 160 all-source exact patterns | not unusual |
| `netanyahu_h` | present; 131 capped hits; 15 all-source exact patterns | not unusual |
| `iran_h` | present; capped at 1000 hits; 159 all-source exact patterns | not unusual |
| `russia_h` | present; 460 capped hits; 58 all-source exact patterns | not unusual |
| `france_h` | present; 782 capped hits; 127 all-source exact patterns | not unusual |
| `europe_h` | present; 105 capped hits; 10 all-source exact patterns | not unusual |
| `usa_abbrev_h` | present; capped at 1000 hits; 178 all-source exact patterns | not unusual |
| `cowboy_h` | present; 62 capped hits; 8 all-source exact patterns | not unusual |
| `united_states_h` | absent in capped exact-version matrix | not controlled |
| `united_nations_h` | absent in capped exact-version matrix | not controlled |
| `european_union_h` | absent in capped exact-version matrix | not controlled |
| `catering_h` | absent in capped exact-version matrix | not controlled |
| `cowboy_catering_h` | absent in capped exact-version matrix | not controlled |
| `simsberry_h` | absent in capped exact-version matrix | not controlled |
| `simscorner_h` | absent in capped exact-version matrix | not controlled |

## Interpretation

Version stability remains useful as a reproducibility filter. It answers which
exact hidden-letter paths survive across MT-family source streams.

It does not establish significance by itself. In this controlled follow-up, the
stable short-form rows behaved like ordinary same-length or same-letter
controls. The longer phrase and local rows remained mostly absent in the capped
exact-version matrix.

Current status: review material only; no modern/geopolitical/local term is
promoted to claim status.
