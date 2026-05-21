# Pair Baselines

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `pair_baselines`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only pair_baselines`
- Generated summary: `reports/pair_baselines_summary.csv`
- Generated examples: `reports/pair_baselines_examples.csv`
- Generated markdown: `reports/pair_baselines.md`
- Generated manifest: `reports/pair_baselines.manifest.json`
- Output size: 20 summary rows; 22 example rows
- Runtime observed: 46.266s through the protocol runner

This compares Gog/Magog against unrelated declared term pairs using the same strict observed filters:

- same chapter
- same signed skip
- gap <= 500 normalized letters

No paired-control p-values are computed here. This is a baseline matrix to decide which non-target pairs deserve full controls.

## Main Read

Gog/Magog is not unique in Hebrew under strict observed filters.

| Pair | MT_WLC close pairs | MT_WLC overlaps | Greek close pairs |
| --- | ---: | ---: | ---: |
| Gog/Magog | 112 | 107 | LXX 9; TR_NT 3; SBLGNT 3 |
| Cyrus/Darius | 1 | 0 | all 0 |
| Beast/Dragon | 329 | 39 | all 0 |
| Horn/Seal | 42 | 3 | all 0 |
| Vision/Prophet | 5 | 0 | all 0 |

Read:

- Hebrew Beast/Dragon produces more strict close pairs than Gog/Magog.
- Hebrew Horn/Seal also produces strict overlaps.
- Greek Gog/Magog remains unusual relative to these selected Greek baselines because the other selected Greek pairs mostly have missing or sparse second-term hits.
- This argues against promoting Hebrew Gog/Magog raw proximity alone.

## Caution

The baseline pairs were chosen as declared unrelated comparators, not exhaustive controls. The next rigorous check is full paired controls for any baseline pair with comparable strict observed density.

## Follow-Up Status

- Full strict paired controls for MT_WLC Beast/Dragon are tracked in
  `docs/BEAST_DRAGON_STRICT_CONTROLS.md`.
- Length-matched synthetic 3+4 Hebrew pair baselines are tracked in
  `docs/SYNTHETIC_PAIR_BASELINES.md`.
- Gog/Magog prospective gating is tracked in
  `docs/GOG_MAGOG_PROSPECTIVE_GATED_REPORT.md`.

Gog/Magog claims should remain exploratory unless they beat these baselines
under the same locked controls.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only pair_baselines
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
