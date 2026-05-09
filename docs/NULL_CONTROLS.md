# Null Controls

Term list:

- `terms/null_controls.csv`

Purpose:

- Declare scrambled and alphabet-pattern controls before large ELS runs.
- Compare claim-term counts against meaning-poor strings of similar length.
- Support false-positive and multiple-testing discipline.

Not run yet:

- This file is intentionally not wired into `protocols/public_baseline.toml`.

Suggested later command:

```bash
python3 -m els batch \
  --terms terms/null_controls.csv \
  --corpus MT_WLC=configs/example_oshb_wlc.toml \
  --corpus LXX=configs/example_ebible_grclxx.toml \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 100 \
  --min-term-length 3 \
  --jobs 0 \
  --out reports/null_controls_counts.csv \
  --manifest-out reports/null_controls_counts.manifest.json
```

Cautions:

- Controls do not prove or disprove claims by themselves.
- Compare fixed claim lists against fixed control lists before looking at results.
- Very short controls are noisy and may be skipped by default settings.
