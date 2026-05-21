# Extension Paired Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_paired_controls`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_paired_controls`
- Generated summary: `reports/extension_paired_controls_summary.csv`
- Generated examples: `reports/extension_paired_controls_examples.csv`
- Generated markdown: `reports/extension_paired_controls.md`
- Generated manifest: `reports/extension_paired_controls.manifest.json`
- Output size: 32 summary rows; 32 example rows
- Runtime observed: 70.911s through the protocol runner

This tracked document summarizes the generated extension-control report. The generated `reports/` files remain local run artifacts.

## Method

The step tests the filtered NT extension top rows:

- TR_NT top file: 11 rows
- SBLGNT top file: 21 rows
- target rows: 32 total

For each target row, controls use the same corpus, same skip, same direction, and same extension settings:

- 10 shuffled-term controls preserving the target's normalized letters
- 10 random same-length strings drawn from same-corpus letter frequencies
- same-skip extension scan with `max_before=12`, `max_after=12`, `phrase_words=4`
- filtered to phrase matches and extension length at least 3

The score ranks longer and stronger extension shapes higher:

- both-sided phrase extensions outrank one-sided phrase extensions
- phrase matches outrank plain word matches
- higher corpus surface match count breaks ties

## Main Read

All 32 rows crossed the current exploratory q <= 0.10 screen.

Band counts:

| Band | Rows |
| --- | ---: |
| `extension_q_le_0.10` | 32 |

Every row has `combined_min_p = 0.090909` and `combined_min_q = 0.090909`. With 10 controls, no sampled control matched or exceeded the observed score, so add-one smoothing sets the floor at `1 / 11`.

This makes the result a review queue, not a claim.

## Strongest Review Queue

The generated summary should be read alongside `docs/EXTENSION_TOP_HITS_REVIEW.md`.

Rows to inspect first:

- strict TR_NT/SBLGNT overlaps: `υιος` (huios; English: son) skip `-4`, `αδαμ` (Adam; English: Adam) skip `11`, `δοξα` (doxa; English: glory) skip `21`
- SBLGNT rows with exact center/span context, especially `υιος` (huios; English: son), `αιμα` (haima; English: blood), and `ΝΑΤΟ` (NATO; English: NATO)
- TR_NT rows with same-category center/span context, especially `θεος` (theos; English: God), `ναος` (naos; English: temple), `υιος` (huios; English: son), and `αιμα` (haima; English: blood)

## Cautions

- 10/10 controls are intentionally coarse because extension controls are slower than raw count controls.
- The p-value floor is `0.090909`, so q <= 0.10 here only means none of the small sampled controls beat the observed row.
- Most extensions are ordinary Greek phrase completions around short theological terms.
- Duplicate-looking rows can appear when separate term rows normalize to the same ELS term.
- This is not enough for external claim-making.

## Follow-Up Status

- Overlap-only follow-up is tracked in
  `docs/EXTENSION_OVERLAP_CONTROLS.md`.
- Exact-center surface-context follow-up is tracked in
  `docs/EXTENSION_EXACT_CENTER_CONTROLS.md`.
- Four-source and confirmatory doxa follow-ups are tracked in
  `docs/DOXA_FOUR_SOURCE_CLAIM_FOLLOWUP_REPORT.md` and
  `docs/DOXA_FOUR_SOURCE_CONFIRMATORY_FOLLOWUP_REPORT.md`.

Any stronger run should now be a newly locked prospective design, not a rerun
of this post-screen queue.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_paired_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
