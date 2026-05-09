# STEP TAHOT Version Presence Review

Last run: 2026-05-05.

## Scope

This is a focused modern/local Hebrew exact-hit version-presence pass with
`STEP_TAHOT` added as a separately labeled source. It keeps the existing
Leningrad-family labels unchanged:

- Stable Leningrad family: `MT_WLC`, `UXLC`, `EBIBLE_WLC`
- Additional MT-family streams: `MAM`, `UHB`
- Optional selected translator stream: `STEP_TAHOT`

`STEP_TAHOT` is not counted as Leningrad-family because its upstream header says
the selected text may follow qere, restore missing text, and include
LXX-preserved additions converted to Hebrew.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/step_tahot_version_presence.toml --resume
```

Outputs:

- `reports/step_tahot_version_presence/hit_patterns.csv`
- `reports/step_tahot_version_presence/term_summary.csv`
- `reports/step_tahot_version_presence/step_tahot_version_presence.md`
- `reports/step_tahot_version_presence/manifest.json`

## Run Metrics

| Metric | Value |
| --- | ---: |
| Duration | 24.038s |
| Terms reviewed | 21 |
| Pattern rows | 1,236 |
| Patterns with `STEP_TAHOT` present | 961 |
| `STEP_TAHOT`-only patterns | 34 |

## Pattern Scope Counts

| Scope | Patterns |
| --- | ---: |
| Present in all observed sources | 745 |
| Present in all Leningrad-family streams | 191 |
| Present in multiple sources | 107 |
| Source-specific | 193 |

## Term-Level Read

| Term | `STEP_TAHOT` hits | Read |
| --- | ---: | --- |
| `vance_h` | 200 | Stable exact patterns exist across all observed streams. |
| `iran_h` | 200 | Stable exact patterns exist across all observed streams. |
| `usa_abbrev_h` | 200 | Stable exact patterns exist across all observed streams. |
| `france_h` | 158 | Stable exact patterns exist across all observed streams. |
| `russia_h` | 93 | Stable exact patterns exist across all observed streams. |
| `turkey_alt_h` | 35 | Stable exact patterns exist across all observed streams. |
| `netanyahu_h` | 30 | Stable exact patterns exist across all observed streams. |
| `europe_h` | 19 | Stable exact patterns exist across all observed streams. |
| `cowboy_h` | 10 | Stable exact patterns exist across all observed streams. |
| `germany_h` | 8 | Stable exact patterns exist across all observed streams. |
| `trump_h` | 7 | Stable exact patterns exist across all observed streams. |
| `turkey_h` | 1 | Stable exact patterns exist across all observed streams. |
| `catering_h` | 0 | No exact patterns in capped scan. |
| `cowboy_catering_h` | 0 | No exact patterns in capped scan. |
| `donald_trump_h` | 0 | No exact patterns in capped scan. |
| `european_union_h` | 0 | No exact patterns in capped scan. |
| `simsberry_h` | 0 | No exact patterns in capped scan. |
| `simscorner_h` | 0 | No exact patterns in capped scan. |
| `united_nations_h` | 0 | No exact patterns in capped scan. |
| `united_states_america_h` | 0 | No exact patterns in capped scan. |
| `united_states_h` | 0 | No exact patterns in capped scan. |

## Read

Adding `STEP_TAHOT` did not erase the strongest focused modern/local exact-hit
pattern families. Many short transliterations still have broad exact ref-key
survival across all six observed streams.

The meaningful new information is source-family separation:

- Some patterns survive in `STEP_TAHOT` despite its qere/restoration/addition
  policy.
- Some patterns are `STEP_TAHOT`-only and should be reviewed as source-policy
  artifacts before being treated as notable.
- Zero-hit longer phrases remain zero in this capped pass.

## Cautions

This is still a capped exact-hit screen, not significance testing. Short terms
such as `vance_h`, `iran_h`, and `usa_abbrev_h` hit the 200-per-corpus cap, so
their totals are discovery pointers rather than complete counts.
