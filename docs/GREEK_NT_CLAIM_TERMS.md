# Greek NT Claim Terms

Term list:

- `terms/greek_nt_claim_terms.csv`

Purpose:

- Compile a focused Greek New Testament claim-driven ELS search list before running another large search.
- Preserve supplied Greek spellings with accents and breathings.
- Let normal search normalization strip accents, breathings, spaces, and punctuation.

Included categories:

- core names and titles
- key concepts and events
- people
- common search phrases
- Revelation-focused terms

Not run yet:

- This file is intentionally not wired into `protocols/public_baseline.toml`.
- Run after the next search/report optimization pass.

Suggested later command:

```bash
python3 -m els batch \
  --terms terms/greek_nt_claim_terms.csv \
  --corpus TR_NT=configs/example_ebible_grctr.toml \
  --corpus SBLGNT=configs/example_sblgnt.toml \
  --min-skip 2 --max-skip 100 \
  --min-term-length 3 \
  --jobs 0 \
  --out reports/greek_nt_claim_terms_counts.csv \
  --manifest-out reports/greek_nt_claim_terms_counts.manifest.json
```

Cautions:

- Greek accents and breathings normalize away. Final sigma normalizes to sigma. For example `Ἰησοῦς` (Iesous; English: Jesus/Joshua) searches as `ιησουσ` (Iesous; English: Jesus/Joshua).
- Phrase rows normalize by removing spaces. For example `Υἱός τοῦ Θεοῦ` (huios tou theou; English: Son of God) searches as `υιοστουθεου` (huios tou theou; English: Son of God).
- These terms are a screening list, not claims of significance.
