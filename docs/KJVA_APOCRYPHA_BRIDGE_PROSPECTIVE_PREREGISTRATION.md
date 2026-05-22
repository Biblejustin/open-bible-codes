# KJVA Apocrypha Bridge Prospective Preregistration

Status: preregistration/protocol lock; completed negative controlled result.

This freezes a fresh KJVA apocrypha/deuterocanon bridge study before running
the observed bridge scan or shuffled-insertion controls for this term cohort.
It is separate from the earlier post-screen confirmatory follow-up over 15
terms selected from prior KJVA bridge results.

Lock basis: commit `b4a5799` added this preregistration, the fixed term file,
and the protocol before the result-bearing run. This older lane does not have a
`reports/study_locks/*.manifest.json` or preflight sidecar. Any future KJVA
bridge follow-up should use the current full study-lock-manifest and preflight
workflow before producing new result-bearing output.

## Registered Terms

The registered term file is:

- `terms/kjv_apocrypha_bridge_prospective_terms.csv`

Registered normalized English terms:

`antiochus`, `mattathias`, `judasmaccabeus`, `eleazar`, `tobit`, `judith`,
`holofernes`.

Term-selection rule:

- use a small fixed English proper-name cohort tied directly to major
  apocrypha/deuterocanon narrative figures;
- do not add terms from the previous KJVA bridge survivor list;
- do not add variants after seeing this protocol's observed rows or controls.

## Source Text And Boundary

The source text is fixed:

- KJVA from `configs/example_ebible_engkjv_apocrypha.toml`

The boundary is fixed:

- canonical prefix before the apocrypha/deuterocanon block;
- apocrypha/deuterocanon block inserted at its existing KJVA position;
- bridge row requires at least one matched letter from canonical text and at
  least one matched letter from the apocrypha/deuterocanon block.

## Locked Search Settings

- skip range: `2..250`
- direction: `both`
- minimum normalized term length: `4`
- observed-row output:
  `reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv`
- control shape: shuffle the apocrypha/deuterocanon insertion block while
  keeping canonical prefix length and apocrypha block length fixed
- control samples: `5000`
- seed: `20260522`
- correction: Benjamini-Hochberg across the 7 registered terms

## Primary Analysis

Run:

```bash
python3 -m scripts.run_protocol protocols/kjv_apocrypha_bridge_prospective_controls_5000.toml --resume
```

Primary outputs:

- `reports/kjv_apocrypha_bridge_prospective/bridge_candidates.csv`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CANDIDATES.md`
- `reports/kjv_apocrypha_bridge_prospective/term_summary.csv`
- `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md`

## Primary Outcome

Primary row outcome:

- per-term `q_ge` from add-one empirical `p_ge`, BH-corrected across the 7
  registered terms.

Primary study outcome:

- number of registered terms with `q_ge <= 0.01`;
- number of registered terms with observed bridge rows above every shuffled
  sample.

## Pass Criteria

For a term to be promoted to prospective review material, it must have:

1. observed bridge rows present in the registered observed file;
2. `q_ge <= 0.01` in the 5000-sample term-level shuffled controls;
3. no dependence on unregistered variants, alternate spellings, broader skip
   ranges, or different boundary placement.

Passing terms may be described only as:

- `prospective_review_candidate`

They may not be described as:

- `confirmed_code`
- `conclusive evidence`
- `prophecy`
- `proof`

## Failure Criteria

A term fails this prospective run if:

- it has `q_ge > 0.01`;
- it is absent from the registered observed bridge rows;
- its result depends on changing the term list, skip range, direction,
  boundary, or control shape after this preregistration.

## Interpretation Boundary

This study can test whether a fixed, non-survivor-selected KJVA
apocrypha/deuterocanon proper-name cohort behaves unusually under the current
bridge-row definition. It cannot by itself establish a theological claim or
validate inspiration.

Claim-grade language would still require non-Bible insertion controls and an
independent replication design fixed before any new result-bearing output.
