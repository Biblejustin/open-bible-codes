# Frequency Anchors

Term list:

- `terms/frequency_anchors.csv`

Purpose:

- Provide high-frequency Hebrew and Greek content-word anchors.
- Calibrate ELS hit counts against common words before interpreting claim terms.
- Help catch obvious pipeline or normalization mistakes.

Current runs:

- `protocols/hebrew_control_version_presence.toml`,
  `protocols/greek_control_version_presence.toml`, and
  `protocols/step_tahot_control_version_presence.toml` use this file for
  exact hit-pattern control comparisons.
- `protocols/broad_search.toml`, `protocols/nonbible_control_counts.toml`, and
  `protocols/real_report_run.toml` include this file in broader calibration and
  control runs.

Cautions:

- High-frequency anchors should produce many ELS hits.
- Short anchors are noisy and may be skipped by default settings.
- These rows are calibration terms, not claim terms.
