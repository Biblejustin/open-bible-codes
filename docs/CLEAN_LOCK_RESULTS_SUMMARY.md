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
| KJVA apocrypha bridge prospective | 7 | 1 observed bridge row (`tobit`) | 0 terms with BH `q_ge <= 0.05`; 1 of 3 non-Bible controls matched observed total | Negative under shuffled and non-Bible controls |

## Detailed Reports

| Lane | Report |
| --- | --- |
| Greek surface new terms | `docs/GREEK_SURFACE_NEW_TERMS_REPORT.md` |
| Greek surface new terms controls | `docs/GREEK_SURFACE_NEW_TERMS_CONTROL_EVALUATION.md` |
| Greek surface new terms context review | `docs/GREEK_SURFACE_NEW_TERMS_CONTEXT_REVIEW.md` |
| Hebrew Gospel/genealogy | `docs/COMPOUND_EXTENSION_PROSPECTIVE_REPORT.md` |
| Hebrew concordance words | `docs/HEBREW_CONCORDANCE_WORDS_PROSPECTIVE_REPORT.md` |
| Hebrew concordance control pilot | `docs/HEBREW_CONCORDANCE_WORDS_CONTROL_PILOT_REPORT.md` |
| Hebrew concordance uncorrected queue | `docs/HEBREW_CONCORDANCE_UNCORRECTED_QUEUE.md` |
| Hebrew concordance uncorrected audit | `docs/HEBREW_CONCORDANCE_UNCORRECTED_SCREENING_AUDIT.md` |
| KJVA apocrypha bridge preregistration | `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_PREREGISTRATION.md` |
| KJVA apocrypha bridge shuffled controls | `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_CONTROLS_5000.md` |
| KJVA apocrypha bridge non-Bible controls | `docs/KJVA_APOCRYPHA_BRIDGE_PROSPECTIVE_NONBIBLE_CONTROLS.md` |

## Read

The new clean-lock work produced review queues, not proof claims.

The two Hebrew exact-version lanes had many exact-version rows, but neither lane
produced adjusted representative-control support. The Hebrew concordance full
control run reduced 6,790 control rows to 136 uncorrected-only control rows and
0 adjusted-support rows. At the term-summary level that reads as 87
uncorrected-only terms and 0 adjusted-support terms.

The Hebrew concordance uncorrected audit keeps those 87 terms bounded as a
triage list: 38 ordinary lexical prompts, 33 proper-name/gloss prompts, 10
high-volume short-string/common-letter prompts, 5 sparse all-source prompts,
and 1 control-artifact prompt. It does not create a claim list.

The Greek surface new-terms lane remains different: 5 controlled surface rows
met the registered `q <= 0.05` threshold. Manual context review found ordinary
local surface-context/self-lexeme effects, so the result stays in the
review-material category and not a theological, prophetic, historical, or
statistical claim.

The KJVA apocrypha bridge prospective lane is also negative. Its fixed
seven-term run found one `tobit` bridge row, but no registered term survived
BH correction, no term exceeded every shuffled sample, and one same-length
non-Bible replacement block matched the observed total.

## Next Work

1. Any next follow-up should be preregistered from stricter gates before searching.
2. Hebrew concordance follow-up gates should exclude adjusted-negative, sparse, high-volume short-string, and proper-name/gloss rows unless they are handled in separate strata.
3. Greek follow-up gates should exclude direct self-lexeme rows and define a context-distance rule before rerunning controls.
4. KJVA bridge follow-up needs independent replication or a new locked design that survives both shuffled and non-Bible insertion controls.
