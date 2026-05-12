# Study Mapping Templates

These CSV files are schema-locked placeholders for future strata that need
human or source-reviewed interpretive mappings before any result-producing run.
`hebrew_root_policy.csv` is included for future `root_only_match` work; it
locks accepted surface-form/root assignments and analyzer provenance before
root-level matching can be used.

Header-only files are valid planning artifacts. Populated files must pass:

```bash
python3 -m scripts.validate_study_mapping_schemas
```

Before a populated mapping is used for claim-level language, lock it with the
study manifest workflow and include it in the relevant preregistration.
