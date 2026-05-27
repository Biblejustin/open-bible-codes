# Start Here

Status: reader guide over current repository docs. This file does not run a
search and does not promote any row to a public claim.

## Bottom Line

Open Bible Codes is a reproducible ELS research toolkit plus a growing audit
record. It can find hidden letter paths, preserve verse/source context, compare
Bible witnesses, and run controls. Current results include real occurrence rows
and controlled review candidates, but no current row should be presented as a
public claim.

Read the project in this order:

1. `docs/PROJECT_FINDINGS_OVERVIEW.md` for the whole-project findings summary.
2. `docs/FINAL_REPORT.md` for the main reader-facing narrative.
3. `docs/FINAL_REPORT_HIGHLIGHTS.md` for compact occurrence rows.
4. `docs/CLAIM_CATALOG.md` for current claim/reproduction status.
5. `docs/CONSOLIDATED_FINDINGS.md` for the broader evidence read.
6. `docs/REAL_REPORT_RUN.md` for what the formal report assembly checks.
7. `docs/REMAINING_WORK_REGISTER.md` for unresolved work.

## Current Read

The strongest material is best described as review material:

- hidden paths exist;
- exact-centered and relevant-centered occurrences exist;
- some rows survive meaningful follow-up controls;
- short strings, wide skip ranges, and post-search selection explain many
  striking-looking rows;
- source and method locks matter as much as hit counts.

The project therefore separates three questions:

- occurrence: does the path exist in this source text;
- context: what verse, word, and passage does it cross or center on;
- strength: do controls make it unusual.

## What Not To Claim

Do not describe current rows as claim-grade support, validation, prediction, or
settled evidence. The safe wording is occurrence, review candidate, controlled
review candidate, partially reproducible, not reproducible, under-specified, or
license-blocked, depending on the catalog row.

WRR means Witztum-Rips-Rosenberg. The repository has locked local WRR-style
evidence and a compact local-method report, but exact published WRR
reproduction remains caveated by the documented source/method gap. A wider
method-lane check found 0 ordinary Genesis hits through skip 5000 for the 11
OCR-matched method-lane terms, so that lane is not explained by a small
skip-cap extension.

BibleGateway/private English versions are accepted only when lawful local text
is available. Missing private or unsupported versions are deferred rather than
scraped or inferred.

The Cities/Aumann/Simon-McKay source-chain lane is source-review only: source
row candidates exist, but source rows are not imported into result-bearing ELS
runs.

## What To Run

For a tiny no-download demo:

```bash
make demo
```

For normal validation before handoff:

```bash
make fast-validate
```

For a clean-tree pre-push gate:

```bash
make release-ready
```

For formal report assembly:

```bash
make real-report
```

For an ignored public reader package after report assembly:

```bash
make public-reader-package
```

This validates the general-reader findings overview and reader-path links before
copying the whitelisted docs.

## What Remains

Current result-producing prospective lanes are closed, negative, or
context-cautioned. New result-producing work needs a fresh term/source target
set, a clean preregistration, and a lock manifest before search output is
allowed to influence study design.

Near-term useful work is editorial: keep the reader path short, keep the claim
language conservative, and preserve links from every summary back to locked
artifacts.
