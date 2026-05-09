# Greek Exact-Center Final Gate

Last run: 2026-05-05.

## Scope

This report consolidates the current Greek exact-center extension review queue:

- pattern version presence from `docs/GREEK_PATTERN_VERSION_SUMMARY.md`;
- row-local paired controls;
- context review and letter-path surface checks;
- same-length synthetic extension baselines where available.

Reproduce after the upstream Greek exact-center protocols have been run:

```bash
python3 -m scripts.run_protocol protocols/greek_exact_center_final_gate.toml --resume
```

Generated local outputs:

- `reports/greek_exact_center_final_gate/summary.csv`
- `reports/greek_exact_center_final_gate/greek_exact_center_final_gate.md`
- `reports/greek_exact_center_final_gate/manifest.json`

## Results

| Pattern | Present | Missing | Best q | Surface phrase in span | Synthetic >= target | Gate |
| --- | --- | --- | ---: | --- | ---: | --- |
| `δοξα|21|forward|term_plus_after|δοξανωσ|δοξανωσ` | TR_NT, BYZ_NT, TCG_NT, SBLGNT | none | 0.001332 | none | 10 | `cross_version_controlled_surface_anchored_hidden_candidate` |
| `υιοσ|25|forward|before_plus_term|ουουιοσ|ουουιοσ` | BYZ_NT, SBLGNT | TR_NT, TCG_NT | 0.001249 | none | 7 | `multi_source_hidden_path_candidate` |
| `αιμα|14|forward|before_plus_term_plus_after|ναιμανο|ναιμανο` | SBLGNT | TR_NT, BYZ_NT, TCG_NT | 0.000999 | none | 0 | `source_specific_hidden_path_candidate` |
| `υιοσ|-46|backward|before_plus_term|ειουιοσ|ειουιοσ` | BYZ_NT | TR_NT, TCG_NT, SBLGNT | 0.000999 | none | 0 | `source_specific_hidden_path_candidate` |

## Gate Counts

| Gate | Rows |
| --- | ---: |
| `cross_version_controlled_surface_anchored_hidden_candidate` | 1 |
| `multi_source_hidden_path_candidate` | 1 |
| `source_specific_hidden_path_candidate` | 2 |

## Read

This gate separates candidate type from claim status. Hidden-path-only phrases
are normal ELS candidates, not failures. A same-span surface echo would be a
rarer and stronger subtype.

`δοξα` is still the strongest row because the same exact extension key appears
in all four compared Greek NT sources, passes q <= 0.01 row-local controls, and
has related surface context around glory/glorified. Its current type is a
cross-version controlled surface-anchored hidden candidate.

`υιοσ` and `αιμα` stay weaker because their exact patterns are missing from one
or more compared Greek NT sources. They remain source-distribution review rows,
not cross-text evidence.

None of these rows is a claim yet. That requires a predeclared study-level
standard, not just a row-level candidate label.
