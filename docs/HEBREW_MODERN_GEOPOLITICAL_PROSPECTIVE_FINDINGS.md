# Hebrew Modern Geopolitical Prospective Findings

Status: locked source-distribution follow-up; no claim.

Source report: `docs/HEBREW_MODERN_GEOPOLITICAL_PROSPECTIVE_REPORT.md`.
Preregistration: `docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md`.
Lock manifest: `reports/study_locks/hebrew_modern_geopolitical_presence.manifest.json`.
Lock commit: `ed34e03`.

## Run

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/HEBREW_MODERN_GEOPOLITICAL_PRESENCE_PREREGISTRATION.md \
  --manifest reports/study_locks/hebrew_modern_geopolitical_presence.manifest.json \
  --protocol protocols/hebrew_modern_geopolitical_prospective.toml \
  --required-setting max_hits_per_term \
  --required-setting source_set \
  --required-setting representative_control_corpora \
  --required-setting selection_rule \
  --out reports/study_locks/hebrew_modern_geopolitical_presence.preflight.json

python3 -m scripts.run_protocol protocols/hebrew_modern_geopolitical_prospective.toml --resume
```

The lock manifest passed, the prospective preflight passed, and the protocol
completed in about `50.5` seconds.

## Result

The registered source-distribution report produced no adjusted-control support.

| Metric | Count |
| --- | ---: |
| Locked term rows | 77 |
| Rows entering min-length exact/control endpoint | 72 |
| Rows with all-source exact patterns | 45 |
| Rows absent in capped exact-version screen | 27 |
| Representative control rows | 90 |
| Rows not unusual under representative controls | 88 |
| Rows uncorrected-only at p <= 0.05 | 2 |
| Rows surviving BH-adjusted q <= 0.05 | 0 |

## Uncorrected-Only Prompts

These rows cleared only an uncorrected representative-control prompt. They did
not survive row-family correction.

| Term | Normalized | Exact total | All-source patterns | Read |
| --- | --- | ---: | ---: | --- |
| `iraq_h` | `עיראק` | 385 | 53 | uncorrected prompt only |
| `germany_h` | `גרמניה` | 38 | 3 | uncorrected prompt only |

## Selected Requested Terms

| Term ID | Exact read | Control read |
| --- | --- | --- |
| `trump_h` | present; 31 capped hits; 6 all-source exact patterns | not unusual |
| `vance_h` | present; capped at 1,000 aggregate hits; 160 all-source exact patterns | not unusual |
| `netanyahu_h` | present; 131 capped hits; 15 all-source exact patterns | not unusual |
| `iran_h` | present; capped at 1,000 aggregate hits; 159 all-source exact patterns | not unusual |
| `russia_h` | present; 460 capped hits; 58 all-source exact patterns | not unusual |
| `germany_h` | present; 38 capped hits; 3 all-source exact patterns | uncorrected-only prompt |
| `europe_h` | present; 105 capped hits; 10 all-source exact patterns | not unusual |
| `united_states_h` | absent in capped exact-version screen | not controlled |
| `united_nations_h` | absent in capped exact-version screen | not controlled |
| `european_union_h` | absent in capped exact-version screen | not controlled |

## Interpretation

The run confirms the broad-screen pattern in a locked narrower cohort:

- many short Hebrew forms are easy to find across MT-family streams;
- longer modern phrases are often absent under the fixed capped exact-version
  matrix;
- representative controls explain the nonzero rows well enough that none
  currently deserves claim-level treatment.

Use this as source-distribution review material only. It does not establish a
prophetic, historical, theological, or statistical claim.
