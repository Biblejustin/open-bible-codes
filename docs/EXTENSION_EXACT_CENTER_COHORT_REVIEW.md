# Extension Exact-Center Cohort Review

Source run:

- Protocol: `protocols/public_baseline.toml`
- Step: `extension_exact_center_cohort_review`
- Command: `python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cohort_review`
- Generated summary: `reports/extension_exact_center_cohort_review_summary.csv`
- Generated markdown: `reports/extension_exact_center_cohort_review.md`
- Generated letter paths: `reports/extension_exact_center_cohort_letter_paths.md`
- Generated manifest: `reports/extension_exact_center_cohort_review.manifest.json`
- Output size: 4 summary rows
- Runtime observed: 0.821s through the protocol runner

This is the manual context and letter-path sheet for the broader exact-center extension cohort.

## Main Read

All 4 rows pass the exact-center gate because the base normalized term appears in the center verse surface text.

| Row | Center | Surface read | Full extension phrase |
| --- | --- | --- | --- |
| SBLGNT `αιμα` (haima; English: blood) / `ναιμανο` (naimano; English: hidden extension form from haima) | Rev 17:6 | `αἵματος` (haimatos; English: of blood) appears twice in the center verse | not surface text |
| SBLGNT `υιος` (huios; English: son) / `ουουιοσ` (ouhuios; English: hidden extension form from huios) | Luke 19:9 | `υἱὸς` (huios; English: son) appears in the center/hit span | not surface text |
| SBLGNT `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 2Thess 3:1 | `δοξάζηται` (doxazetai; English: may be glorified) appears in the center verse | not surface text |
| TR_NT `δοξα` (doxa; English: glory) / `δοξανωσ` (doxanos; English: hidden extension form from doxa) | 2TH 3:1 | `δοξάζηται` (doxazetai; English: may be glorified) appears in the center verse | not surface text |

## Letter Path Notes

- `αιμα` (haima; English: blood) path crosses Rev 17:5-6; surface context is already blood-heavy, but the extension `ναιμανο` (naimano; English: hidden extension form from haima) is not a surface phrase.
- `υιος` (huios; English: son) path crosses Luke 19:8-10; the center/hit passage discusses sonship, but `ουουιοσ` (ouhuios; English: hidden extension form from huios) is not a surface phrase.
- `δοξα` (doxa; English: glory) path crosses 2 Thessalonians 3:1-2 in both Greek NT texts; the base term is surface-related through `δοξάζηται` (doxazetai; English: may be glorified), but `δόξαν ὡς` (doxan hos; English: glory as) remains hidden-path only.

## Caution

This review strengthens context only for the base terms. It does not promote the full extension strings as readable surface phrases.

## Next Check

- compare exact-center cohort rows against cross-text overlap requirements
- run 200/200 controls only for rows that survive context plus overlap
- keep these as review queue rows unless stronger null controls remain favorable

Cross-text review is now tracked in `docs/EXTENSION_EXACT_CENTER_CROSS_TEXT.md`.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only extension_exact_center_cohort_review
python3 -m scripts.run_protocol protocols/public_baseline.toml --resume --only report_index
```
