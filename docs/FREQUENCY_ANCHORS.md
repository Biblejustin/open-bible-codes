# Frequency Anchors

Term list:

- `terms/frequency_anchors.csv`

Purpose:

- Provide high-frequency Hebrew and Greek content-word anchors.
- Calibrate ELS hit counts against common words before interpreting claim terms.
- Help catch obvious pipeline or normalization mistakes.

Not run yet:

- This file is intentionally not wired into `protocols/public_baseline.toml`.

Cautions:

- High-frequency anchors should produce many ELS hits.
- Short anchors are noisy and may be skipped by default settings.
- These rows are calibration terms, not claim terms.
