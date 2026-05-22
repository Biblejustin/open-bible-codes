# Study Mapping Templates

These CSV files are schema-locked placeholders for future strata that need
human or source-reviewed interpretive mappings before any result-producing run.
`hebrew_root_policy.csv` powers `root_only_match`; it locks accepted
surface-form/root assignments and analyzer provenance before root-level
matching can be used. The matcher performs exact normalized policy matching and
does not infer roots automatically.

Header-only files are valid planning artifacts. Some files contain conservative
seed rows for currently implemented post-search metadata; other files remain
templates for future work. Populated files must pass:

```bash
python3 -m scripts.validate_study_mapping_schemas
```

Before a populated mapping is used for claim-level language, lock it with the
study manifest workflow and include it in the relevant preregistration.

`wrr_manual_decision_records.csv` is a header-only template for future WRR
manual-lock decisions. It is not a decision log until populated with cited
evidence, reviewer lock fields, and selected actions.
