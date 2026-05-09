# All-Codes Compound Extension Confirmatory Preregistration

Status: locked post-discovery confirmatory control plan. This is not an
original prospective discovery.

## Purpose

The broad all-codes follow-up found compound same-skip extension rows where the
letters immediately before or after a hidden term form a longer surface-matching
phrase. The exploratory 250/250 control run left one overlap key with
conservative all-control q <= 0.10:

- base term: `יום יהוה`
- normalized base: `יומיהוה`
- skip: `4`
- direction: `forward`
- extension type: `before_plus_term`
- extended sequence: `היומיהוה`
- overlap key: `יומיהוה|4|forward|before_plus_term|היומיהוה|היומיהוה`

This follow-up reruns only that overlap key with a larger control budget.

## Locked Inputs

- source rows: `reports/all_codes_followup_extensions/compound_extensions.csv`
- script: `scripts/analyze_extension_paired_controls.py`
- Hebrew MT-family configs:
  - `configs/example_oshb_wlc.toml`
  - `configs/example_uxlc.toml`
  - `configs/example_ebible_hebwlc.toml`
  - `configs/example_mam.toml`
  - `configs/example_uhb.toml`

## Locked Settings

- include only overlap key:
  `יומיהוה|4|forward|before_plus_term|היומיהוה|היומיהוה`
- dedupe target rows
- term controls: 5000
- random same-length controls: 5000
- random seed: 314159
- max before letters: 12
- max after letters: 12
- phrase words: 4
- include both-sided extensions
- max extensions per hit: 20
- minimum extension length: 1
- match-kind prefix: empty string

## Primary Outputs

- `reports/all_codes_compound_extension_confirmatory/summary.csv`
- `reports/all_codes_compound_extension_confirmatory/examples.csv`
- `docs/ALL_CODES_COMPOUND_EXTENSION_CONFIRMATORY_CONTROLS.md`
- `reports/all_codes_compound_extension_confirmatory/manifest.json`
- `reports/all_codes_compound_extension_confirmatory/protocol_run.manifest.json`

## Primary Criteria

This remains a post-discovery review candidate only if:

- the registered overlap key is still present;
- every retained row reports its warning flags;
- `all_controls_max_q <= 0.10` for at least one retained row;
- examples remain available for manual passage inspection.

This does not promote the row to a claim. A stronger claim would need a
prospective term/extension rule locked before any row was discovered.

## Run Command

```bash
python3 -m scripts.run_protocol protocols/all_codes_compound_extension_confirmatory.toml --resume
```

## Cautions

- The target was selected after a broad all-codes screen.
- The phrase is short and Hebrew short-form density is a strong confounder.
- The all-codes queue intentionally retains hidden-path-only candidates; that is
  useful for review, not claim language.
- The registered threshold is a review threshold, not a statistical discovery
  threshold.
