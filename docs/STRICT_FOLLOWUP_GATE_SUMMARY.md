# Strict Follow-Up Gate Summary

Status: conservative gate over the completed clean-lock review queues; no claim.

This page answers whether the current clean-lock queues are ready for another
claim-style follow-up. The answer is no. They are useful audit material, but
the stricter gates produce zero claim-ready rows.

## Gate Rules

| Gate | Rule |
| --- | --- |
| Adjusted support | Row must have corrected `q <= 0.05` in its registered control family |
| Pattern support | Row must not be sparse or control-artifact only |
| Short-string handling | High-volume short strings must be excluded or handled in a separate stratum |
| Gloss handling | Proper-name/gloss rows must be excluded or handled in a separate stratum |
| Context distance | Visible surface wording, self-lexeme hits, and immediate local-context echoes must not drive the read |

## Results

| Lane | Review rows | Rows passing strict gate | Reason |
| --- | ---: | ---: | --- |
| Hebrew concordance uncorrected queue | 87 | 0 | All rows fail adjusted support; audit buckets are triage-only |
| Greek surface new terms controlled rows | 5 | 0 | Manual context review found surface-context/self-lexeme effects |

## Hebrew Concordance

The Hebrew concordance queue has 87 uncorrected-only rows and 0 adjusted-support
rows. The generated audit buckets them as 38 ordinary lexical prompts, 33
proper-name/gloss prompts, 10 high-volume short-string/common-letter prompts,
5 sparse all-source prompts, and 1 control-artifact prompt.

Even before secondary gates, the adjusted-support gate leaves 0 rows. Ignoring
that gate would be post hoc mining, so the current Hebrew concordance queue
should not be promoted into a follow-up claim set.

## Greek Surface New Terms

The Greek surface lane has 5 controlled rows with `q <= 0.05`, but manual
context review found that the rows are tied to visible local wording or direct
self-lexeme effects:

| Term | Strict-gate read |
| --- | --- |
| `ονομα` / ὄνομα | ordinary "name" passages and direct inflected name forms |
| `οικοσ` / οἶκος | household context in Acts 16:31 |
| `σοφια` / σοφία | direct visible `σοφίᾳ` self-lexeme row |
| `θυσια` / θυσία | Hebrews 10 sacrifice/sin context |
| `σκηνη` / σκηνή | Hebrews 9 tabernacle context |

These remain review material. They do not pass a context-distance gate.

## Next Valid Move

The next valid move is a new preregistered study, not promotion of current
queue rows. It should define the candidate list, strata, context-distance rule,
and multiple-comparison correction before searching.
