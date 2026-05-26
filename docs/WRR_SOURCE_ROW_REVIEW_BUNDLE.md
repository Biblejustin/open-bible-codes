# WRR Source Row Review Bundle

Status: no-input row-review bundle for WRR source-row review.
It combines row-checklist, crop-path, and OCR-word evidence; it does not choose row transcriptions, source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_row_review_bundle --row-checklist reports/wrr_1994/wrr_source_transcription_row_review_checklist.csv --crop-packet reports/wrr_1994/wrr_source_row_crop_packet.csv --ocr-word-packet reports/wrr_1994/wrr_source_row_ocr_word_packet.csv --out reports/wrr_1994/wrr_source_row_review_bundle.csv --summary-out reports/wrr_1994/wrr_source_row_review_bundle_summary.csv --markdown-out docs/WRR_SOURCE_ROW_REVIEW_BUNDLE.md --manifest-out reports/wrr_1994/wrr_source_row_review_bundle.manifest.json
```

## Current Read

- Row review clusters: 22.
- Frontier rows: 19.
- Rows with generated crops: 22.
- Rows with OCR words: 22.
- Low-confidence OCR words: 78.
- Boundary: No row transcription, source correction, pair exclusion, or method change is selected by this bundle.

## Row Bundle

| Rank | Row | Frontier | Terms | Words | Low conf | Crop | Name-column OCR | Date-column OCR | Next action |
| ---: | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `06` | 4 | 4 | 15 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row06_auto.png) | מעשי השם, מעשי י/ה/ו/ה 3251 | כ"ב כסלו, בכ"ב כסלו, כ"ב בכסלו | review crop and OCR words together before any frontier source decision |
| 2 | `14` | 3 | 3 | 11 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row14_auto.png) | חות יאיר ב36ז613ג0 | בא' טבת, אי בטבת | review crop and OCR words together before any frontier source decision |
| 3 | `24` | 3 | 3 | 16 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row24_auto.png) | עמדין, היעב"\, הר"י ה עמדן, הר"י עמדין | ל' ניסן, בל' ניסן, לי בניסן | review crop and OCR words together before any frontier source decision |
| 4 | `01` | 2 | 2 | 19 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row01_auto.png) | רבי הרב אב"ד, אברהם, הראב"ד, הראב"י, האשכול | כי חשון, בכי חשון, כי בחשון | review crop and OCR words together before any frontier source decision |
| 5 | `03` | 2 | 2 | 12 | 1 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row03_auto.png) | רבי אברהם, המלאך | י"ב תשרי, בי"ב תשרי, י"ב בתשרי | review crop and OCR words together before any frontier source decision |
| 6 | `09` | 2 | 2 | 14 | 2 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row09_auto.png) | רבי דוד, דוד ניטו | כ"ח טבת, בכ"ח טבת, כ"ה בטבת | review crop and OCR words together before any frontier source decision |
| 7 | `10` | 2 | 2 | 13 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row10_auto.png) | רבי חיים | ו' ניסן, בו' ניסן, וי בניסן | review crop and OCR words together before any frontier source decision |
| 8 | `11` | 2 | 2 | 13 | 2 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row11_auto.png) | רבי חיים, בנבנשת | י"ט אלול, בי"ט אלול, י"ט באלול | review crop and OCR words together before any frontier source decision |
| 9 | `15` | 2 | 2 | 12 | 2 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row15_auto.png) | רבי יהודה | ה' חשון, בה' חשון, ה' בחשון | review crop and OCR words together before any frontier source decision |
| 10 | `22` | 2 | 2 | 14 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row22_auto.png) | חאגיז, בעל הלק"ט 12 | כ"ו שבט, בכ"ו שבט, כ"ו בשבט | review crop and OCR words together before any frontier source decision |
| 11 | `23` | 2 | 2 | 24 | 6 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row23_auto.png) | בבר כ הר טַ "לתפול "ל, מלרילל זל\י, להסכרי"ל | כ"ב אלול, לול, בכ"ב " אלול, , כ" כ"ב באלול | review crop and OCR words together before any frontier source decision |
| 12 | `25` | 2 | 2 | 16 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row25_auto.png) | רבי יצחק, הורוויץ, יצחק הלוי | בו' איר, ו' באיר | review crop and OCR words together before any frontier source decision |
| 13 | `26` | 1 | 2 | 15 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row26_auto.png) | רבי מנחם, קרוכמל, רבי מענדל, צמח צדק | בב' שבט | review crop and OCR words together before any frontier source decision |
| 14 | `27` | 1 | 1 | 29 | 7 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row27_auto.png) | רבי משה משה, זכותא, זכותא, משה זכותו, זכות, משה מהר"ם זכות, הרמיץ זכות | י"ו כו" תשרי, תשרי, 'בי"ו בט"ז תשרי, תשרק, *"ר ט"ז בתשרי בתשרי | review crop and OCR words together before any frontier source decision |
| 15 | `02` | 1 | 1 | 16 | 5 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row02_auto.png) | רבי זרע אברהם אברהם, יצחקי, | ייג סיון, ביייג סיון, י"ג בסיון | review crop and OCR words together before any frontier source decision |
| 16 | `05` | 1 | 1 | 13 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row05_auto.png) | רבי אהרן | י"ט ניסן, בי"ט ניסן, י"ט בניסן | review crop and OCR words together before any frontier source decision |
| 17 | `07` | 1 | 1 | 15 | 4 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row07_auto.png) | רבי דוד, אופנהים תוס | +' תשרי, בז' תשרי, ז' בתשרי | review crop and OCR words together before any frontier source decision |
| 18 | `16` | 1 | 1 | 14 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row16_auto.png) | רבי יהודה, מהר"י עיאש | א' תשרי, בא' תשרי, א' בתשרי | review crop and OCR words together before any frontier source decision |
| 19 | `20` | 1 | 1 | 15 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row20_auto.png) | רבי יוסף, תאומים, פרי מגדים | בד' איר, ד' באיר | review crop and OCR words together before any frontier source decision |
| 20 | `30` | 0 | 4 | 13 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row30_auto.png) | א"ח הע"ר, ישר לבב 161 | בא' אדר, א' באדר | review after frontier rows unless policy scope changes |
| 21 | `32` | 0 | 2 | 13 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row32_auto.png) | רבי שלמה ה[06 | כ"א תמוז, בכ"א תמוז, כ"א בתמוז | review after frontier rows unless policy scope changes |
| 22 | `29` | 0 | 1 | 15 | 3 | [crop](../reports/wrr_1994/source_review_crops_auto/wrr_table2_row29_auto.png) | רבי עזריה | א' אדר א', בא' אדר א', א' באדר אי | review after frontier rows unless policy scope changes |

## Boundary

- Crop and OCR availability is not transcription verification.
- OCR confidence is review triage only.
- Manual row decisions still require a separate citable decision record.
- No row here changes the working WRR source or excludes a pair automatically.
