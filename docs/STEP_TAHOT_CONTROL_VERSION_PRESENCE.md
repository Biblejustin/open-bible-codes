# STEP TAHOT Control Version Presence

Last run: 2026-05-05.

## Scope

This is the STEP_TAHOT follow-up for the Hebrew null/frequency control
version-presence run.

The point is not to test a claim term. It asks whether scrambled terms and
frequency anchors also produce exact ref-key patterns that survive when
`STEP_TAHOT` is added as a sixth Hebrew stream.

Reproduce:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_version_presence.toml --resume
```

Outputs:

- `reports/step_tahot_control_version_presence/hit_patterns.csv`
- `reports/step_tahot_control_version_presence/term_summary.csv`
- `reports/step_tahot_control_version_presence/step_tahot_control_version_presence.md`
- `reports/step_tahot_control_version_presence/manifest.json`

## Summary

| Metric | Value |
| --- | ---: |
| Duration | 22.176s |
| Declared Hebrew control rows | 23 |
| Summarized rows after minimum length filter | 13 |
| Hit records | 4,491 |
| Exact pattern rows | 1,005 |
| Patterns with `STEP_TAHOT` present | 749 |
| `STEP_TAHOT`-only patterns | 24 |

Pattern scope counts:

| Scope | Pattern rows |
| --- | ---: |
| `present_all_observed_sources` | 519 |
| `present_all_leningrad_streams` | 146 |
| `present_multiple_sources` | 225 |
| `source_specific` | 115 |

`STEP_TAHOT`-only rows by control term:

| Term | Rows |
| --- | ---: |
| `scrambled_yhwh_h` | 7 |
| `scrambled_elohim_h` | 5 |
| `nonsense_5_b_h` | 4 |
| `scrambled_israel_h` | 4 |
| `shamayim_h` | 2 |
| `panim_h` | 1 |
| `scrambled_torah_h` | 1 |

## Source-Policy Follow-Up

The `STEP_TAHOT`-only control rows can be audited with the same source-policy
path checker:

```bash
python3 -m scripts.run_protocol protocols/step_tahot_control_policy_hits.toml --resume
```

Latest control-row policy audit:

| Metric | Rows |
| --- | ---: |
| `STEP_TAHOT`-only control rows audited | 24 |
| Rows touching `Q` qere-selected words | 3 |
| Rows touching `R` restored words | 0 |
| Rows touching `X` LXX-based Hebrew additions | 0 |
| Rows whose letter path is only L-prefixed words | 21 |

## Read

STEP-specific exact-hit patterns also occur in controls. In this capped run,
749 of 1,005 control pattern rows include `STEP_TAHOT`, and 24 are
`STEP_TAHOT`-only.

That makes the current rule stricter: `STEP_TAHOT` presence can be useful for
source-family review, but `STEP_TAHOT`-only rows are not claim evidence unless
they also survive source-policy audit and matched controls.

The consolidated final gate is tracked in `docs/STEP_TAHOT_FINAL_GATE.md`.
