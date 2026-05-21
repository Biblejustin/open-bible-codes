# Synthetic Pair Baselines

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `synthetic_pair_baselines`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only synthetic_pair_baselines`
- Generated summary: `reports/synthetic_pair_baselines_summary.csv`
- Generated comparison: `reports/synthetic_pair_baselines_comparison.csv`
- Generated markdown: `reports/synthetic_pair_baselines.md`
- Generated manifest: `reports/synthetic_pair_baselines.manifest.json`
- Output size: 25 synthetic rows; 2 comparison rows
- Runtime observed: 13.809s through the protocol runner

This runs length-matched MT_WLC synthetic Hebrew pair baselines for short 3+4 letter pair density.

## Main Read

Synthetic 3+4 letter pairs often match or exceed the strict close-pair density of both Gog/Magog and Beast/Dragon.

| Target | Target close pairs | Synthetic close mean | Synthetic >= target | p_ge |
| --- | ---: | ---: | ---: | ---: |
| Gog/Magog | 112 | 935.04 | 20 / 25 | 0.807692 |
| Beast/Dragon | 329 | 935.04 | 12 / 25 | 0.5 |

Overlap comparison:

| Target | Target overlaps | Synthetic overlap mean | Synthetic >= target | p_ge |
| --- | ---: | ---: | ---: | ---: |
| Gog/Magog | 107 | 133.8 | 5 / 25 | 0.230769 |
| Beast/Dragon | 39 | 133.8 | 14 / 25 | 0.576923 |

## Verdict

This strongly cautions against reading short Hebrew pair proximity as meaningful by itself. The search space and common Hebrew letter patterns can generate many strict same-chapter and same-signed-skip close pairs.

## Caution

These synthetic strings are sampled from MT_WLC letter frequencies. They are not filtered for pronounceability or lexical validity. That is intentional: this is a density/control baseline, not a word-list claim.

## Follow-Up Status

- Gog/Magog strict-pair limits are tracked in
  `docs/GOG_MAGOG_STRICT_PAIR_CONTROLS.md`.
- Beast/Dragon strict-pair controls are tracked in
  `docs/BEAST_DRAGON_STRICT_CONTROLS.md`.
- Broader pair baselines are tracked in `docs/PAIR_BASELINES.md`.

Short Hebrew pair hits should remain exploratory unless a newly locked study
requires semantic surface context and stronger length-matched controls.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only synthetic_pair_baselines
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
