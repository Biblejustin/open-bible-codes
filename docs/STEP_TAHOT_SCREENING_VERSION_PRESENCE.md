# STEP TAHOT Screening Version Presence

Last run: 2026-05-05.

## Scope

This is the broader Hebrew screening exact-hit version-presence pass with
`STEP_TAHOT` added as a separately labeled source. It uses the same term-file
scope as `docs/HEBREW_SCREENING_VERSION_PRESENCE.md`, but it does not replace
that baseline report.

`STEP_TAHOT` remains outside the Leningrad-family label because it is a selected
translator stream that may follow qere, restored readings, and LXX-preserved
additions.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/step_tahot_screening_version_presence.toml --resume
```

Outputs:

- `reports/step_tahot_screening_version_presence/hit_patterns.csv`
- `reports/step_tahot_screening_version_presence/term_summary.csv`
- `reports/step_tahot_screening_version_presence/step_tahot_screening_version_presence.md`
- `reports/step_tahot_screening_version_presence/manifest.json`

## Run Metrics

| Metric | Value |
| --- | ---: |
| Duration | 23.295s |
| Summarized terms | 417 |
| Pattern rows | 15,478 |
| Patterns with `STEP_TAHOT` present | 12,084 |
| `STEP_TAHOT`-only patterns | 379 |
| No-hit summarized terms | 101 |

## Pattern Scope Counts

| Scope | Patterns |
| --- | ---: |
| Present in all observed sources | 9,287 |
| Present in all Leningrad-family streams | 2,311 |
| Present in multiple sources | 2,057 |
| Source-specific | 1,823 |

## Comparison To Five-Source Hebrew Screening

| Report | Pattern rows | All-source rows | Leningrad-family rows | Source-specific rows |
| --- | ---: | ---: | ---: | ---: |
| Five-source Hebrew screening | 15,099 | 9,432 | 2,166 | 2,600 |
| Six-source with `STEP_TAHOT` | 15,478 | 9,287 | 2,311 | 1,823 |

Adding `STEP_TAHOT` changes the distribution but not the interpretation. Short
forms still dominate exact all-source stability; long modern/local phrases are
still absent or sparse; source-specific rows remain review queues.

## Read

The broader result supports the same rule as the focused result: `STEP_TAHOT`
is useful for asking which patterns survive a selected translator stream, but
it should not be merged into all-Leningrad evidence.

Rows that are `STEP_TAHOT`-only should be audited against TAHOT source-type
policy (`Q`, `R`, `X`, or other selected readings) before further review.

That follow-up audit is tracked in `docs/STEP_TAHOT_POLICY_HIT_AUDIT.md`.

The matching STEP_TAHOT null/frequency control follow-up is tracked in
`docs/STEP_TAHOT_CONTROL_VERSION_PRESENCE.md`.

The consolidated final gate is tracked in `docs/STEP_TAHOT_FINAL_GATE.md`.
