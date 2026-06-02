# Fresh Prospective Study Intake

Status: intake gate only; no result-producing run yet.

This document defines what a new study package must include before EDLS runs
new result-bearing searches. It exists because all current tracked prospective
lanes are completed, negative/weak, or context-cautioned review material.

Use this when someone brings a new term set, source set, or study idea. Do not
use it to rebrand an already-screened row as a new discovery.

## Required Intake Package

A new study request must provide or create all of these before any search:

1. study name and short purpose;
2. source text family and source config paths;
3. lawful source-use note for every new source;
4. term source path and term-source rationale;
5. term file with stable `term_id` values;
6. normalized minimum term length;
7. excluded prior-evidence rows;
8. skip range and direction;
9. candidate-selection rule;
10. control design and sample budget;
11. correction method;
12. output paths;
13. preregistration document;
14. study-lock manifest;
15. clean prospective-term audit summary;
16. preflight sidecar.

If any item is missing, the study can be discussed, drafted, or audited, but it
must not produce new result-bearing output.

## Intake Checklist

| Gate | Required evidence | Pass condition |
| --- | --- | --- |
| Source lawfulness | license, public-domain status, or local-use boundary | source is allowed for the intended role |
| Source identity | config path, source path, checksum, and source family | exact source stream is reproducible |
| Term provenance | term file, source note, and term-source rationale | terms were chosen before output inspection |
| Prior-evidence audit | clean audit summary against known reports and queues | reused evidence is excluded or labeled confirmatory |
| Study rule | skip, direction, length, candidate type, and failure criteria | rule is fixed before search |
| Controls | real-word and/or randomized controls with sample budget | controls are fixed before search |
| Multiple testing | correction family and status thresholds | q-value family is predeclared |
| Outputs | report, CSV, manifest, examples, and audit paths | paths are known before search |
| Lock | preregistration plus study-lock manifest | fingerprints exist before search |
| Preflight | preflight sidecar from current tooling | clean enough to run |

## Default Commands

Audit candidate terms before a lock:

```bash
python3 -m scripts.audit_prospective_terms \
  --candidate terms/[study_terms].csv \
  --evidence reports/[prior_evidence].csv \
  --min-normalized-length 5 \
  --out reports/study_locks/[study].term_audit.csv \
  --fail-on-match
```

Build the study lock:

```bash
python3 -m scripts.build_study_lock_manifest \
  --name [study] \
  --path terms/[study_terms].csv \
  --path protocols/[study].toml \
  --path configs/[source].toml \
  --setting skip_range=2..50 \
  --setting direction=both \
  --setting correction=benjamini_hochberg \
  --out reports/study_locks/[study].manifest.json
```

Run preflight before any result-producing protocol:

```bash
python3 -m scripts.preflight_prospective_study \
  --preregistration docs/[STUDY_PREREGISTRATION].md \
  --manifest reports/study_locks/[study].manifest.json \
  --protocol protocols/[study].toml \
  --clean-term-audit reports/study_locks/[study].term_audit.csv.summary.json \
  --out reports/study_locks/[study].preflight.json
```

## Allowed No-Input Work

Without a complete intake package, EDLS may still do:

- source-license audit;
- source-shape audit;
- term-file schema audit;
- prior-evidence audit;
- preregistration drafting;
- protocol dry-run/schema validation;
- checker and documentation work.

Without a complete intake package, EDLS must not do:

- ELS searches for new study results;
- shuffled controls for new study results;
- p-value or q-value reporting for a new study;
- candidate ranking from new output;
- public claim language.

## Relationship To Current Lanes

Current tracked profiles live in `configs/prospective_study_lanes.json` and
are summarized in `docs/PROSPECTIVE_LANE_STATUS.md` and
`docs/PROSPECTIVE_STUDY_READINESS.md`.

As of this intake gate, no tracked lane remains `ready_for_preflight`. A new
result-producing study needs a fresh term/source target set and a new clean
prospective lock.

## Cautions

- A strong post-screen row is still prior evidence.
- A confirmatory follow-up is not an original prospective discovery.
- A source candidate is not a source lock.
- A readable review packet is not a term/source import decision.
- A clean preflight does not make weak results strong; it only makes the run
  reproducible and honest about timing.
