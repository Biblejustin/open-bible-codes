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
resonance proxy: candidate cylinder sizes are the intersection of the
first row widths derived from each ELS skip. Pair distance is the best
symmetric Hausdorff letter distance across those shared cylinder sizes.
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

## Strongest Settings

| N | moved fraction | factor | statistic | null mean | alternative mean | power | read |
| ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| 10 | 0.5 | 0.25 | harmonic_mean | 18.5355 | 11.3893 | 0.555 | moderate_power_for_declared_model |
| 10 | 0.5 | 0.25 | fisher_order_split | 60.1061 | 38.3847 | 0.47 | low_power_for_declared_model |
| 10 | 0.5 | 0.25 | geometric_mean | 25.4167 | 17.4211 | 0.41 | low_power_for_declared_model |
| 10 | 0.5 | 0.5 | fisher_order_split | 31.5248 | 23.0422 | 0.24 | low_power_for_declared_model |
| 10 | 0.5 | 0.5 | harmonic_mean | 18.7506 | 13.8274 | 0.21 | low_power_for_declared_model |
| 10 | 0.5 | 0.25 | arithmetic_mean | 53.8513 | 46.9175 | 0.17 | low_power_for_declared_model |
| 10 | 0.5 | 0.25 | order_trimmed_mean | 56.2816 | 49.1586 | 0.17 | low_power_for_declared_model |
| 10 | 0.5 | 0.5 | geometric_mean | 25.927 | 19.8876 | 0.165 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | arithmetic_mean | 56.8993 | 50.1789 | 0.155 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | order_trimmed_mean | 59.4635 | 52.4779 | 0.155 | low_power_for_declared_model |
| 10 | 0.25 | 0.25 | harmonic_mean | 18.4633 | 14.7401 | 0.145 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | geometric_mean | 26.5721 | 22.901 | 0.145 | low_power_for_declared_model |

## Caveats

- This is model-design scaffolding only.
- It does not test real Torah text.
- It translates generated ELS start positions; it does not require
  the moved ELS to spell a real word in a real corpus.
- The moved start search is local around the projected cylinder target,
  not an exhaustive global optimizer.
- The Fisher row is data-driven simulation scaffolding; it is not a
  source-published set of weights.
- The resonant-cylinder definition is explicit and reproducible but
  narrower than a complete source-method reconstruction.
