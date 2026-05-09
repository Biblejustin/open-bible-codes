# Gog/Magog Strict Pair Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `gog_magog_strict_pairs`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only gog_magog_strict_pairs`
- Generated summary: `reports/gog_magog_strict_pairs_summary.csv`
- Generated examples: `reports/gog_magog_strict_pairs_examples.csv`
- Generated markdown: `reports/gog_magog_strict_pairs.md`
- Generated manifest: `reports/gog_magog_strict_pairs.manifest.json`
- Output size: 4 summary rows; 25 example rows
- Runtime observed: 51.516s through the protocol runner

This reruns the Gog/Magog proximity screen with two stricter filters:

- both ELS spans must share at least one chapter
- both ELS hits must use the same signed skip

## Main Read

The stricter screen reduces raw pair counts sharply.

| Corpus | Loose close pairs | Strict close pairs | Strict overlaps | Combined p | Combined q | Band |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| MT_WLC | 712 | 112 | 107 | 0.188119 | 0.188119 | `not_unusual` |
| LXX | 28 | 9 | 9 | 0.029703 | 0.079208 | `pair_q_le_0.10` |
| TR_NT | 10 | 3 | 3 | 0.059406 | 0.079208 | `pair_q_le_0.10` |
| SBLGNT | 6 | 3 | 3 | 0.049505 | 0.079208 | `pair_q_le_0.10` |

Read:

- MT_WLC no longer screens after same-chapter and same-signed-skip filters.
- Greek corpora still screen at q <= 0.10, not q <= 0.05.
- NT rows have only 3 Magog hits, so they remain low-count review items.
- Random controls remain limited to 5 samples because random short strings produce large hit lists.

## Example Chapters

Examples include:

- MT_WLC: `Josh 6`, `2Sam 22`, `2Kgs 9`, `Ps 18`, `Jer 51`
- LXX: `PSA 70`, `JER 51`, `GEN 25`, `EZK 20`
- TR_NT/SBLGNT: same-skip examples are sparse and should be inspected row by row from `reports/gog_magog_strict_pairs_examples.csv`

## Caution

Same-chapter plus same-skip is a stronger filter than plain proximity, but it still screens short strings. It should be read as a smaller review queue, not a claim.

## Next Check

- inspect the 25 strict examples by passage
- compare Gog/Magog against unrelated 3-letter / 5-letter prophetic pairs
- raise random controls only if runtime remains acceptable

Observed unrelated pair baselines are now tracked in `docs/PAIR_BASELINES.md`.
Length-matched synthetic short-Hebrew pair baselines are tracked in
`docs/SYNTHETIC_PAIR_BASELINES.md`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only gog_magog_strict_pairs
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
