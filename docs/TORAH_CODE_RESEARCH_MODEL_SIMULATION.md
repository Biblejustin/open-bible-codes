# Torah-Code Research Model Simulation

Status: simulation harness; not a Torah-code result.

Source lead:

- `https://www.torah-code.org/research/research_3.html`

This implements the first geometric level-1 model described by the
Torah-code.org research-program page. Each run compares two independent
uniform point sets in the unit square against an alternative where a
declared fraction of the second set is moved toward its nearest point in
the first set. The statistic is mean nearest-neighbor distance from the
second set to the first set; smaller values mean more compact meetings.

The page does not specify a final test statistic, so this harness is a
transparent power/sanity check for one simple statistic, not a source
replication claim.

Reproduce with:

```bash
python3 -m scripts.simulate_torah_code_research_model
```

## Settings

- replicates per setting: `200`
- alpha: `0.05`
- base seed: `20260520`

## Strongest Settings

| N | moved fraction | closeness factor | null mean | alternative mean | power | read |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 50 | 0.5 | 0.25 | 0.0749874 | 0.0418513 | 1 | high_power_for_declared_model |
| 50 | 0.5 | 0.5 | 0.0744848 | 0.0461563 | 0.995 | high_power_for_declared_model |
| 25 | 0.5 | 0.25 | 0.108683 | 0.0628766 | 0.98 | high_power_for_declared_model |
| 50 | 0.5 | 0.75 | 0.0740752 | 0.0516159 | 0.97 | high_power_for_declared_model |
| 25 | 0.5 | 0.5 | 0.106736 | 0.0688542 | 0.955 | high_power_for_declared_model |
| 10 | 0.5 | 0.25 | 0.171902 | 0.0966589 | 0.84 | high_power_for_declared_model |
| 50 | 0.25 | 0.25 | 0.0745132 | 0.0591979 | 0.835 | high_power_for_declared_model |
| 25 | 0.5 | 0.75 | 0.10703 | 0.0760967 | 0.805 | high_power_for_declared_model |
| 10 | 0.5 | 0.5 | 0.172954 | 0.109006 | 0.73 | moderate_power_for_declared_model |
| 50 | 0.25 | 0.5 | 0.0741073 | 0.0604713 | 0.685 | moderate_power_for_declared_model |

## Caveats

- This is model-design scaffolding only.
- It uses Euclidean unit-square distance.
- It interprets the page's movement description as a distance factor
  sampled uniformly from `[0, closeness_factor]`.
- ELS cylinder geometry remains separate work.
