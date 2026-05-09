# Prospective Study Preregistration Template

Status: template; copy before use.

Copy this file to a study-specific preregistration document before any
result-producing run. Replace every bracketed placeholder, commit the
preregistration, build a lock manifest, validate it, then run the protocol.

## Study Identity

| Field | Value |
| --- | --- |
| Study name | `[name]` |
| Study status | prospective candidate-discovery screen |
| Preregistration commit | `[commit after this document is committed]` |
| Lock manifest | `reports/study_locks/[name].manifest.json` |
| Report document | `docs/[NAME]_REPORT.md` |

## Question

State the exact question in one paragraph.

Example shape:

Do declared `[language/source scope]` terms produce `[candidate type]` patterns
under fixed `[skip range]`, `[direction]`, `[surface/context]`, and `[control]`
rules?

## Term List

Locked term file:

- `terms/[term_file].csv`

Rules:

- source term files: `[list]`;
- language: `[hebrew|greek|michigan|english]`;
- normalized minimum length: `[n]`;
- dedupe rule: `[rule]`;
- excluded prior rows/forms: `[list]`.

## Source Texts

Corpus/source labels:

- `[LABEL]` from `[config path]`;
- `[LABEL]` from `[config path]`.

State whether the sources are aligned version-comparison sources or broad
corpus-presence sources.

## Locked Settings

| Setting | Value |
| --- | --- |
| Skip range | `[min..max]` |
| Direction | `[forward|backward|both]` |
| Minimum normalized length | `[n]` |
| Candidate selection rule | `[rule]` |
| Context rule | `[rule]` |
| Control budget | `[budget]` |
| Correction method | `[method]` |

## Lock Manifest

Build:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name [name] \
  --path terms/[term_file].csv \
  --path protocols/[protocol].toml \
  --path [config path] \
  --setting skip_range=[min..max] \
  --setting direction=[direction] \
  --setting min_normalized_length=[n] \
  --setting controls=[control budget] \
  --setting correction=[method] \
  --out reports/study_locks/[name].manifest.json
```

Validate:

```bash
python3 -m scripts.check_study_lock_manifest \
  reports/study_locks/[name].manifest.json \
  --required-setting skip_range \
  --required-setting direction \
  --required-setting min_normalized_length \
  --required-setting controls \
  --required-setting correction
```

Do not run the study if the checker fails.

## Protocol

Run:

```bash
python3 -m scripts.run_protocol protocols/[protocol].toml --resume
```

Expected outputs:

- `reports/[name]/[output].csv`;
- `reports/[name]/protocol_run.manifest.json`;
- `docs/[NAME]_REPORT.md`.

## Primary Outcome

Primary row-level outcome:

- `[metric]`

Primary study-level outcome:

- `[metric and threshold]`

## Candidate Labels

Allowed labels:

- `prospective_review_queue_candidate`;
- `prospective_controlled_review_candidate`;
- `source_specific_review_candidate`;
- `review_hold`;
- `not_reproducible`.

Disallowed labels:

- `confirmed_code`;
- `proof`;
- `prophecy`;
- `statistical discovery`;
- `claim`.

## Failure Criteria

The study fails to produce a controlled review candidate if:

- required lock manifest validation fails;
- required inputs change after locking;
- no candidate rows meet the registered rule;
- required controls fail the registered threshold;
- required examples, context, or letter paths cannot be generated;
- the result depends on unregistered terms, spellings, sources, skip ranges, or
  broadened matching rules.

## Reporting Rules

The report must include:

- command used;
- git commit;
- lock manifest path;
- source text labels;
- term count;
- row counts at each stage;
- exact p/q values for every surviving row;
- examples and warning flags;
- context and letter-path output locations;
- pass/fail table against this preregistration;
- explicit statement that the run is review material, not proof of meaning.

## Interpretation Boundary

This study may identify review candidates. It cannot establish theological,
prophetic, historical, or statistical claims by itself.
