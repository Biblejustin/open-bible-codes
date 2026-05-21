# Clean-Lock Results Summary

Status: summary of completed clean-lock runs; no claim.

This page summarizes the clean prospective lanes that were added after prior
evidence rows were excluded. It points to the detailed generated reports and
keeps the conservative read visible in one place.

## Lanes

| Lane | Terms | Primary result | Controls | Conservative read |
| --- | ---: | --- | --- | --- |
| Greek surface new terms | 236 | 9 selected all-source length-5 surface rows | 5 control rows reached `q <= 0.05` | Controlled review material; manual review required before any claim |
| Hebrew Gospel/genealogy | 27 | 21 rows with all-source exact patterns | 22 rows with representative controls; 3 uncorrected-only; 0 adjusted support | No adjusted representative-control support |
| Hebrew concordance words | 3,577 | 3,372 rows with all-source exact patterns | 3,398 terms with representative controls; 87 uncorrected-only; 0 adjusted support | No adjusted representative-control support |

## Detailed Reports

| Lane | Report |
| --- | --- |
| Greek surface new terms | `docs/GREEK_SURFACE_NEW_TERMS_REPORT.md` |
| Greek surface new terms controls | `docs/GREEK_SURFACE_NEW_TERMS_CONTROL_EVALUATION.md` |
| Hebrew Gospel/genealogy | `docs/COMPOUND_EXTENSION_PROSPECTIVE_REPORT.md` |
| Hebrew concordance words | `docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md` |
| Hebrew concordance control pilot | `docs/HEBREW_CONCORDANCE_WORDS_CONTROL_PILOT_REPORT.md` |

## Read

The new clean-lock work produced review queues, not proof claims.

The two Hebrew exact-version lanes had many exact-version rows, but neither lane
produced adjusted representative-control support. The Hebrew concordance full
control run reduced 6,790 control rows to 136 uncorrected-only control rows and
0 adjusted-support rows. At the term-summary level that reads as 87
uncorrected-only terms and 0 adjusted-support terms.

The Greek surface new-terms lane remains different: 5 controlled surface rows
met the registered `q <= 0.05` threshold. Those rows need manual context review
before any stronger statement, because the report is surface-context review
material and not a theological, prophetic, historical, or statistical claim.

## Next Work

1. Manual context review for the 5 Greek surface new-terms control rows.
2. If desired, inspect the 87 Hebrew concordance uncorrected-only terms as review prompts only.
3. Decide whether any follow-up lane should be preregistered from the Greek manual review, instead of mining the full result table after the fact.
