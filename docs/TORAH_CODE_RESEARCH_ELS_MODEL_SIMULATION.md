# Torah-Code ELS Model Simulation

Status: simulation harness; not a Torah-code result.

Source leads:

- `https://www.torah-code.org/research/research_3c.html`
- `https://www.torah-code.org/research/research_12.shtml`

This implements a level-1 ELS analogue of the research-program model:
two random ELS sets are generated under a null model; under the
alternative, a declared fraction of the second set is translated toward
its best resonant-cylinder meeting in the first set.

The implementation uses the repo's WRR row-width helper as a transparent
resonance proxy: candidate cylinder sizes are the intersection of the
first row widths derived from each ELS skip. Pair distance is the best
symmetric Hausdorff letter distance across those shared cylinder sizes.

Statistics compared here are arithmetic, geometric, harmonic, and a simple
trimmed order-statistic mean. The source statistic-selection page mentions
a Fisher linear discriminant over order statistics, but does not provide
weights here; that remains a later upgrade.

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
| 10 | 0.5 | 0.25 | harmonic_mean | 18.5355 | 13.8846 | 0.285 | low_power_for_declared_model |
| 10 | 0.5 | 0.25 | geometric_mean | 25.4167 | 19.6139 | 0.265 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | order_trimmed_mean | 59.4635 | 53.0823 | 0.135 | low_power_for_declared_model |
| 10 | 0.5 | 0.25 | arithmetic_mean | 53.8513 | 48.0991 | 0.125 | low_power_for_declared_model |
| 10 | 0.5 | 0.25 | order_trimmed_mean | 56.2816 | 50.3248 | 0.125 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | arithmetic_mean | 56.8993 | 50.7848 | 0.125 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | geometric_mean | 26.5721 | 23.7799 | 0.09 | low_power_for_declared_model |
| 10 | 0.5 | 0.75 | harmonic_mean | 19.2516 | 17.0559 | 0.09 | low_power_for_declared_model |
| 10 | 0.25 | 0.75 | geometric_mean | 25.5037 | 24.6078 | 0.085 | low_power_for_declared_model |
| 10 | 0.5 | 0.5 | harmonic_mean | 18.7506 | 15.5288 | 0.085 | low_power_for_declared_model |
| 10 | 0.25 | 0.25 | harmonic_mean | 18.4633 | 16.4926 | 0.075 | low_power_for_declared_model |
| 10 | 0.25 | 0.5 | arithmetic_mean | 57.1433 | 56.7139 | 0.075 | low_power_for_declared_model |

## Caveats

- This is model-design scaffolding only.
- It does not test real Torah text.
- It translates generated ELS start positions; it does not require
  the moved ELS to spell a real word in a real corpus.
- The resonant-cylinder definition is explicit and reproducible but
  narrower than a complete source-method reconstruction.
