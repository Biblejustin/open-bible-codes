# Hebrew Theology Prospective Findings

Status: locked registered follow-up run; no claim.

Source report: `docs/HEBREW_THEOLOGY_PROSPECTIVE_REPORT.md`.
Preregistration: `docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md`.
Lock manifest: `reports/study_locks/hebrew_theology_prospective.manifest.json`.
Lock commit: `75e82ba`.

## Run

```bash
python3 -m scripts.build_study_lock_manifest \
  --name hebrew_theology_prospective \
  --path docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md \
  --path terms/hebrew_theology_prospective_terms.csv \
  --path protocols/hebrew_theology_prospective.toml \
  --path configs/example_oshb_wlc.toml \
  --path configs/example_uxlc.toml \
  --path configs/example_ebible_hebwlc.toml \
  --path configs/example_mam.toml \
  --path configs/example_uhb.toml \
  --setting skip_range=2..100 \
  --setting direction=both \
  --setting min_normalized_length=4 \
  --setting controls=1000_term_shuffle_plus_1000_random_same_length_per_selected_MT_WLC_UHB_target \
  --setting correction=benjamini_hochberg \
  --setting source_set=MT_WLC,UXLC,EBIBLE_WLC,MAM,UHB \
  --setting representative_control_corpora=MT_WLC,UHB \
  --setting selection_rule=exact_ref_key_version_presence_with_representative_controls \
  --out reports/study_locks/hebrew_theology_prospective.manifest.json

python3 -m scripts.preflight_prospective_study \
  --preregistration docs/HEBREW_THEOLOGY_PROSPECTIVE_PREREGISTRATION.md \
  --manifest reports/study_locks/hebrew_theology_prospective.manifest.json \
  --protocol protocols/hebrew_theology_prospective.toml \
  --required-setting source_set \
  --required-setting representative_control_corpora \
  --required-setting selection_rule

python3 -m scripts.run_protocol protocols/hebrew_theology_prospective.toml --resume
```

The lock manifest passed, the prospective preflight passed, and the protocol
completed in `37.374` seconds.

## Result

The registered primary outcome was not met.

| Metric | Count |
| --- | ---: |
| Locked terms | 20 |
| Terms entering exact/control endpoint | 18 |
| Rows with all-source exact patterns | 15 |
| Rows absent or unsummarized | 3 |
| Representative control target rows | 30 |
| Rows not unusual under representative controls | 14 |
| Rows uncorrected-only at p <= 0.05 | 1 |
| Rows surviving BH-adjusted q <= 0.05 | 0 |

`htp_truth_h` and `htp_mercy_h` are locked but below the registered normalized
minimum length of 4, so they do not enter the exact/control endpoint.

The three long phrase rows with no exact hits were:

- `htp_lamb_of_god_h` / `כבשהאלוהימ` (kevesh haElohim; English: lamb of God);
- `htp_son_of_god_h` / `בנהאלוהימ` (ben haElohim; English: son of God);
- `htp_yeshua_messiah_h` / `ישועהמשיח` (Yeshua haMashiach; English: Yeshua Messiah).

## Control Read

Only `htp_yhwh_h` (`יהוה` (YHWH; English: YHWH)) cleared an uncorrected representative-control screen:

| Term | Exact hits | All-source patterns | Best p | Best q | Read |
| --- | ---: | ---: | ---: | ---: | --- |
| `htp_yhwh_h` | 108320 | 16312 | 0.018981 | 0.38961 | uncorrected prompt only |

Because the adjusted q-value is `0.38961`, this does not satisfy the
registered claim-grade threshold.

## Interpretation

Short Hebrew terms produce many exact ELS rows under `2..100`, including many
all-source rows. That by itself is not meaningful. The registered control gate
is the useful filter here, and it produced no adjusted support.

Use the YHWH row only as a review prompt if desired. It is not a confirmed
pattern, proof, prophecy, or statistical discovery.

For non-claim-grade inspection, the relaxed all-codes companion run is tracked
in `docs/HEBREW_THEOLOGY_ALL_CODES_COLLECTION.md`. That run keeps every hidden
ELS row and separately flags same-center-word and related-center-word surface
matches.
