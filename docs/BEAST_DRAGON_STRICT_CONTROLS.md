# Beast/Dragon Strict Controls

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `beast_dragon_strict_controls`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only beast_dragon_strict_controls`
- Generated summary: `reports/beast_dragon_strict_controls_summary.csv`
- Generated examples: `reports/beast_dragon_strict_controls_examples.csv`
- Generated markdown: `reports/beast_dragon_strict_controls.md`
- Generated manifest: `reports/beast_dragon_strict_controls.manifest.json`
- Output size: 1 summary row; 10 example rows
- Runtime observed: 14.347s through the protocol runner

This is the full paired-control follow-up for the Hebrew baseline pair that exceeded Gog/Magog in observed strict close pairs.

## Main Read

Beast/Dragon is not unusual under the same strict paired controls.

| Corpus | Close pairs | Overlaps | Combined p | Combined q | Band |
| --- | ---: | ---: | ---: | ---: | --- |
| MT_WLC | 329 | 39 | 0.294118 | 0.294118 | `not_unusual` |

Control means:

| Control | Close mean | Overlap mean |
| --- | ---: | ---: |
| shuffled-term | 315.76 | 44.74 |
| same-length random | 505.0 | 65.8 |

Read:

- Beast/Dragon has many more raw strict close pairs than Gog/Magog in MT_WLC.
- Controls explain that density; the row is not unusual.
- This reinforces caution around short Hebrew raw proximity screens.

## Caution

Random controls remain limited to 5 samples because short Hebrew strings can produce very large hit lists. Still, both term-shuffle and random controls point away from significance here.

## Follow-Up Status

- Beast/Dragon now serves as a caution baseline for Gog/Magog review.
- Length-matched synthetic pair controls are tracked in
  `docs/SYNTHETIC_PAIR_BASELINES.md`.
- Broader pair baselines are tracked in `docs/PAIR_BASELINES.md`.

Raw strict close-pair counts should not be promoted without paired controls.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only beast_dragon_strict_controls
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
