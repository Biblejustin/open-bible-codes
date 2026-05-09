# Gog/Magog Pair Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `gog_magog_pairs`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only gog_magog_pairs`
- Generated summary: `reports/gog_magog_pairs_summary.csv`
- Generated examples: `reports/gog_magog_pairs_examples.csv`
- Generated markdown: `reports/gog_magog_pairs.md`
- Generated manifest: `reports/gog_magog_pairs.manifest.json`
- Output size: 4 summary rows; 36 example rows
- Runtime observed: 64.289s through the protocol runner

This tracked document summarizes the generated Gog/Magog proximity report. The generated `reports/` files remain local run artifacts.

## Method

For each corpus, the script:

- finds all Gog ELS hits and Magog ELS hits at skips `2..50`, both directions
- counts nearby pair candidates with span gap <= 500 normalized letters
- counts overlapping ELS spans
- records best span gap and best center distance
- compares those metrics with paired controls

Controls:

- 100 term-shuffle pair controls per corpus
- 5 same-length same-corpus random pair controls per corpus

Random pair controls are intentionally small because random 3-letter strings create very large hit lists. These controls are enough to show density risk, not enough for strong claim-making.

## Main Read

Gog/Magog proximity is worth review, but not a claim.

All four corpora crossed the current exploratory q <= 0.10 screen. None crossed q <= 0.05. Every row also carries limited-control warnings, especially `few_random_pair_controls`.

## Summary

| Corpus | Gog hits | Magog hits | Close pairs | Overlaps | Best gap | Combined p | Combined q | Band | Read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| MT_WLC | 1,364 | 104 | 712 | 376 | 0 | 0.079208 | 0.09901 | `pair_q_le_0.10` | pair-control screen; inspect examples |
| LXX | 1,800 | 9 | 28 | 18 | 0 | 0.049505 | 0.09901 | `pair_q_le_0.10` | pair-control screen; inspect examples |
| TR_NT | 594 | 3 | 10 | 8 | 0 | 0.09901 | 0.09901 | `pair_q_le_0.10` | pair-control screen; inspect examples |
| SBLGNT | 572 | 3 | 6 | 6 | 0 | 0.089109 | 0.09901 | `pair_q_le_0.10` | pair-control screen; inspect examples |

## Control Means

| Corpus | Term close mean | Random close mean | Term overlap mean | Random overlap mean |
| --- | ---: | ---: | ---: | ---: |
| MT_WLC | 476.23 | 58,647.0 | 189.98 | 6,532.6 |
| LXX | 10.22 | 26,608.4 | 4.6 | 3,591.0 |
| TR_NT | 5.77 | 1,216.4 | 2.86 | 189.6 |
| SBLGNT | 3.28 | 1,010.4 | 1.62 | 121.0 |

Read:

- Term-shuffle controls make observed Gog/Magog proximity mildly interesting.
- Random controls show why short-form density is dangerous: random 3-letter controls can produce far more close pairs.
- The current result should be treated as a review queue, not as evidence of encoding.

## Example Rows

The generated examples file keeps the nearest observed pairs. Examples include same-chapter overlaps such as:

- MT_WLC: `1Chr 5`, `Lev 13`, `1Sam 15`, `Josh 6`
- LXX: `PSA 70`, `JER 51`, `GEN 25`, `EZK 20`, `GEN 48`

These are examples to inspect manually. The pair-control result itself is the main screen.

## Verdict

This is the first focused result that merits review attention, but the controls are still exploratory:

- q-value only reaches `0.09901`
- random controls are intentionally limited
- Gog is only 3 letters
- many examples come from dense short-form overlap behavior

Next stronger run:

- increase random pair controls if runtime is acceptable
- add same-book/chapter pair controls
- require same skip or related skip patterns as a stricter filter
- compare against unrelated 3-letter / 5-letter prophetic term pairs

Same-chapter plus same-signed-skip follow-up is now tracked in
`docs/GOG_MAGOG_STRICT_PAIR_CONTROLS.md`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only gog_magog_pairs
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
