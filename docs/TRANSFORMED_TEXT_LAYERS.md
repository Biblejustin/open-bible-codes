# Transformed Text Layers

This note documents opt-in deterministic text transforms for ELS searches.
These layers widen the search surface and are not part of routine claim
promotion. A transformed-text finding needs the same transform applied to
language-matched controls before it can support comparative language.

## Implemented Transforms

| Transform | Language | Rule | Runner |
| --- | --- | --- | --- |
| `hebrew_atbash` | Hebrew | א↔ת, ב↔ש, ג↔ר, and so on | `scripts.search_transformed_els` |
| `hebrew_albam` | Hebrew | א↔ל, ב↔מ, ג↔נ, and so on | `scripts.search_transformed_els` |

Both transforms preserve corpus offsets and original surface-word metadata.
The hidden path is found in the transformed letter stream, then reported
against the original corpus references.

## Current Audits

The committed Atbash and ALBAM audits use the same declared Jeremiah
cryptogram term set. This allows the transform layer to vary while the target
terms and controls stay fixed.

```bash
python3 -m scripts.run_protocol protocols/hebrew_atbash_audit.toml --resume
python3 -m scripts.run_protocol protocols/hebrew_albam_audit.toml --resume
```

Outputs:

- `reports/hebrew_atbash_audit/summary.csv`
- `docs/HEBREW_ATBASH_AUDIT.md`
- `reports/hebrew_albam_audit/summary.csv`
- `docs/HEBREW_ALBAM_AUDIT.md`

## Layered Pairing

To compare ordinary ELS hits against transformed-layer hits at the same declared
anchor, use:

```bash
python3 -m scripts.build_cipher_layered_pairs \
  --plain-hits reports/plain_hits.csv \
  --cipher-hits reports/hebrew_atbash_audit/MT_WLC_hits.csv \
  --out reports/cipher_layered_pairs/pairs.csv \
  --summary-out reports/cipher_layered_pairs/summary.csv \
  --manifest-out reports/cipher_layered_pairs/manifest.json
```

By default, the pairing key is corpus label, term id, center reference, and
center normalized word. Override it with repeated `--anchor-field` arguments
only in a locked protocol. The summary file counts pairs by transform, corpus,
and term; the manifest records input paths, output paths, anchor fields, row
counts, elapsed time, and the local git commit.

## Custom ALBAM Search

Example:

```bash
python3 -m scripts.search_transformed_els \
  --config configs/example_oshb_wlc.toml \
  --corpus-label MT_WLC \
  --transform hebrew_albam \
  --terms terms/hebrew_atbash_audit_terms.csv \
  --min-skip 2 \
  --max-skip 100 \
  --direction both \
  --out reports/transformed_els/hebrew_albam_hits.csv
```

## Read

- A transform layer is a different search family from plain-text ELS.
- Each additional transform increases the multiple-testing burden.
- The transform rule must be locked before looking at density or highlight
  outputs.
- Non-Bible controls must be transformed with the same rule before any
  Bible-vs-control comparison.
- Atbash has explicit historical precedent in Jeremiah cryptogram discussion;
  ALBAM is included as a deterministic Jewish cipher layer. Both remain
  opt-in widened search families.
