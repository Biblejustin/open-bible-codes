# KJVA Apocrypha Bridge Confirmatory Follow-Up Preregistration

Status: post-screen confirmatory follow-up, not an original prospective discovery.

This freezes a narrower rerun for the 15 KJVA bridge terms that passed the
1000-sample term-level shuffled-control screen at Benjamini-Hochberg
`q_ge <= 0.05`. It does not add variants, widen the source set, change the
boundary, or inspect additional terms.

## Registered Terms

The registered term file is:

- `terms/kjv_apocrypha_bridge_confirmatory_terms.csv`

Registered normalized English terms:

`nato`, `seba`, `sign`, `eber`, `satan`, `moab`, `sidon`, `sivan`, `gallus`,
`otho`, `seal`, `house`, `tomb`, `noah`, `abib`.

These terms were selected from `docs/KJV_APOCRYPHA_BRIDGE_TERM_SHUFFLED_CONTROLS_1000.md`.
Because the selection used earlier results, this is confirmatory/post-screen
work, not a clean prospective discovery.

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
- observed rows: `reports/kjv_apocrypha_bridge_candidates/bridge_candidates.csv`
- control shape: shuffle the apocrypha/deuterocanon insertion block while
  keeping canonical prefix length and apocrypha block length fixed
- control samples: `5000`
- seed: `20260509`
- correction: Benjamini-Hochberg across the 15 registered terms

## Primary Analysis

Run:

```bash
python3 -m scripts.run_protocol protocols/kjv_apocrypha_bridge_confirmatory_controls_5000.toml --resume
```

Primary outputs:

- `reports/kjv_apocrypha_bridge_confirmatory_controls_5000/sample_summary.csv`
- `reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_samples.csv`
- `reports/kjv_apocrypha_bridge_confirmatory_controls_5000/term_summary.csv`
- `docs/KJVA_APOCRYPHA_BRIDGE_CONFIRMATORY_CONTROLS_5000.md`
- `reports/kjv_apocrypha_bridge_confirmatory_controls_5000/manifest.json`

## Primary Outcome

Primary row outcome:

- per-term `q_ge` from add-one empirical `p_ge`, BH-corrected across the 15
  registered terms.

Primary study outcome:

- number of registered terms with `q_ge <= 0.01`;
- number of registered terms with observed bridge rows above every shuffled
  sample.

## Pass Criteria

This follow-up remains review-only unless all required outputs are reproduced.
For a term to be promoted to stronger follow-up material, it must have:

1. observed bridge rows present in the registered observed file;
2. `q_ge <= 0.01` in the 5000-sample term-level shuffled controls;
3. no dependence on unregistered variants, alternate spellings, broader skip
   ranges, or different boundary placement.

Passing terms may be described only as:

- `post_screen_confirmatory_review_candidate`

They may not be described as:

- `confirmed_code`
- `conclusive evidence`
- `prophecy`
- `original prospective discovery`

## Failure Criteria

A term fails this follow-up if:

- it has `q_ge > 0.01`;
- it is absent from the registered observed bridge rows;
- its result depends on changing the term list, skip range, direction,
  boundary, or control shape after this preregistration.

## Interpretation Boundary

This study can stress-test a post-screen KJVA bridge-term signal. It cannot by
itself establish a theological claim or validate inspiration. A stronger claim
would require a fresh prospective study with the candidate list fixed before
any result is observed.
