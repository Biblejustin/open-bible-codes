# Torah-Code ELS Model Simulation

Status: simulation harness; not a Torah-code result.

Source leads:

- `https://www.torah-code.org/research/research_3c.html`
- `https://www.torah-code.org/research/research_12.shtml`

This implements a level-1 ELS analogue of the research-program model:
two random ELS sets are generated under a null model; under the
alternative, a declared fraction of the second set is repositioned
toward its best resonant-cylinder meeting in the first set.

The implementation uses the repo's WRR row-width helper as a transparent
row-width proxy. It compares two explicit modes: `shared_intersection`,
where candidate cylinder sizes are only the shared first row widths
derived from both ELS skips, and `combined_wrr_series`, where candidates
are the combined first WRR row-width series from both skips.
Pair distance is the best symmetric Hausdorff letter distance across
the candidate cylinder sizes for that mode.
For moved ELSs, the script identifies the best target ELS and row width,
projects the moving start position along the shortest cylinder path, and
then searches nearby valid starts for a distance closest to `a*d`.

Statistics compared here are arithmetic, geometric, harmonic, a simple
trimmed order-statistic mean, and a split-fit Fisher order-statistic
score. The Fisher row learns weights from the first half of generated
null/alternative runs and reports power only on the held-out half.

Reproduce with:

```bash
python3 -m scripts.simulate_torah_code_research_els_model
```

## Settings

- replicates per setting: `200`
- alpha: `0.05`
- base seed: `20260520`
- text length: `5000`
- max skip: `120`
- row-width count: `10`
- row-width modes: `shared_intersection, combined_wrr_series`

## Strongest Settings

| N | width mode | moved fraction | factor | statistic | null mean | alternative mean | power | read |
| ---: | --- | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 10 | shared_intersection | 0.5 | 0.25 | harmonic_mean | 18.5355 | 11.3893 | 0.555 | moderate_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.25 | geometric_mean | 11.6815 | 9.22629 | 0.535 | moderate_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.25 | harmonic_mean | 10.6492 | 8.04212 | 0.525 | moderate_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.25 | fisher_order_split | 134.27 | 105.516 | 0.51 | moderate_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.5 | fisher_order_split | 92.3204 | 75.8265 | 0.51 | moderate_power_for_declared_model |
| 10 | shared_intersection | 0.5 | 0.25 | fisher_order_split | 60.1061 | 38.3847 | 0.47 | low_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.25 | arithmetic_mean | 12.7867 | 10.5487 | 0.465 | low_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.25 | order_trimmed_mean | 13.1496 | 10.8932 | 0.46 | low_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.5 | geometric_mean | 11.7731 | 9.68244 | 0.46 | low_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.5 | arithmetic_mean | 12.8278 | 10.8602 | 0.45 | low_power_for_declared_model |
| 10 | combined_wrr_series | 0.5 | 0.5 | order_trimmed_mean | 13.1931 | 11.1995 | 0.45 | low_power_for_declared_model |
| 10 | shared_intersection | 0.5 | 0.25 | geometric_mean | 25.4167 | 17.4211 | 0.41 | low_power_for_declared_model |

## Caveats

- This is model-design scaffolding only.
- It does not test real Torah text.
- It translates generated ELS start positions; it does not require
  the moved ELS to spell a real word in a real corpus.
- The moved start search is local around the projected cylinder target,
  not an exhaustive global optimizer.
- The Fisher row is data-driven simulation scaffolding; it is not a
  source-published set of weights.
- The row-width definitions are explicit and reproducible, but neither
  mode is a complete source-method reconstruction.
