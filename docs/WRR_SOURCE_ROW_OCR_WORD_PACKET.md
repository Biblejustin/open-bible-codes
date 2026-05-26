# WRR Source Row OCR Word Packet

Status: no-input OCR word packet for WRR source-row review.
It lists OCR words by source row and expected columns; it is not transcription verification and does not choose row transcriptions, source corrections, method changes, or pair exclusions.

Reproduce:

```bash
python3 -m scripts.build_wrr_source_row_ocr_word_packet --crop-packet reports/wrr_1994/wrr_source_row_crop_packet.csv --tsv reports/wrr_1994/wrr_primary_table2_row_ocr.tsv --low-conf-threshold 50 --out reports/wrr_1994/wrr_source_row_ocr_word_packet.csv --summary-out reports/wrr_1994/wrr_source_row_ocr_word_summary.csv --markdown-out docs/WRR_SOURCE_ROW_OCR_WORD_PACKET.md --manifest-out reports/wrr_1994/wrr_source_row_ocr_word_packet.manifest.json
```

## Current Read

- Source rows: 22.
- Rows with OCR words: 22.
- Frontier rows: 19.
- Total OCR words: 337.
- Low-confidence OCR words: 78 below 50.
- Boundary: OCR words are review aids only; no row transcription, source correction, pair exclusion, or method change is selected by this packet.

## Row Words

| Rank | Row | Frontier | Words | Low conf | Name-column OCR | Date-column OCR | Next action |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- |
| 1 | `06` | 4 | 15 | 4 | מעשי השם, מעשי י/ה/ו/ה 3251 | כ"ב כסלו, בכ"ב כסלו, כ"ב בכסלו | compare OCR words with crop and source row before any frontier source decision |
| 2 | `14` | 3 | 11 | 4 | חות יאיר ב36ז613ג0 | בא' טבת, אי בטבת | compare OCR words with crop and source row before any frontier source decision |
| 3 | `24` | 3 | 16 | 3 | עמדין, היעב"\, הר"י ה עמדן, הר"י עמדין | ל' ניסן, בל' ניסן, לי בניסן | compare OCR words with crop and source row before any frontier source decision |
| 4 | `01` | 2 | 19 | 4 | רבי הרב אב"ד, אברהם, הראב"ד, הראב"י, האשכול | כי חשון, בכי חשון, כי בחשון | compare OCR words with crop and source row before any frontier source decision |
| 5 | `03` | 2 | 12 | 1 | רבי אברהם, המלאך | י"ב תשרי, בי"ב תשרי, י"ב בתשרי | compare OCR words with crop and source row before any frontier source decision |
| 6 | `09` | 2 | 14 | 2 | רבי דוד, דוד ניטו | כ"ח טבת, בכ"ח טבת, כ"ה בטבת | compare OCR words with crop and source row before any frontier source decision |
| 7 | `10` | 2 | 13 | 4 | רבי חיים | ו' ניסן, בו' ניסן, וי בניסן | compare OCR words with crop and source row before any frontier source decision |
| 8 | `11` | 2 | 13 | 2 | רבי חיים, בנבנשת | י"ט אלול, בי"ט אלול, י"ט באלול | compare OCR words with crop and source row before any frontier source decision |
| 9 | `15` | 2 | 12 | 2 | רבי יהודה | ה' חשון, בה' חשון, ה' בחשון | compare OCR words with crop and source row before any frontier source decision |
| 10 | `22` | 2 | 14 | 4 | חאגיז, בעל הלק"ט 12 | כ"ו שבט, בכ"ו שבט, כ"ו בשבט | compare OCR words with crop and source row before any frontier source decision |
| 11 | `23` | 2 | 24 | 6 | בבר כ הר טַ "לתפול "ל, מלרילל זל\י, להסכרי"ל | כ"ב אלול, לול, בכ"ב " אלול, , כ" כ"ב באלול | compare OCR words with crop and source row before any frontier source decision |
| 12 | `25` | 2 | 16 | 4 | רבי יצחק, הורוויץ, יצחק הלוי | בו' איר, ו' באיר | compare OCR words with crop and source row before any frontier source decision |
| 13 | `26` | 1 | 15 | 4 | רבי מנחם, קרוכמל, רבי מענדל, צמח צדק | בב' שבט | compare OCR words with crop and source row before any frontier source decision |
| 14 | `27` | 1 | 29 | 7 | רבי משה משה, זכותא, זכותא, משה זכותו, זכות, משה מהר"ם זכות, הרמיץ זכות | י"ו כו" תשרי, תשרי, 'בי"ו בט"ז תשרי, תשרק, *"ר ט"ז בתשרי בתשרי | compare OCR words with crop and source row before any frontier source decision |
| 15 | `02` | 1 | 16 | 5 | רבי זרע אברהם אברהם, יצחקי, | ייג סיון, ביייג סיון, י"ג בסיון | compare OCR words with crop and source row before any frontier source decision |
| 16 | `05` | 1 | 13 | 3 | רבי אהרן | י"ט ניסן, בי"ט ניסן, י"ט בניסן | compare OCR words with crop and source row before any frontier source decision |
| 17 | `07` | 1 | 15 | 4 | רבי דוד, אופנהים תוס | +' תשרי, בז' תשרי, ז' בתשרי | compare OCR words with crop and source row before any frontier source decision |
| 18 | `16` | 1 | 14 | 3 | רבי יהודה, מהר"י עיאש | א' תשרי, בא' תשרי, א' בתשרי | compare OCR words with crop and source row before any frontier source decision |
| 19 | `20` | 1 | 15 | 3 | רבי יוסף, תאומים, פרי מגדים | בד' איר, ד' באיר | compare OCR words with crop and source row before any frontier source decision |
| 20 | `30` | 0 | 13 | 3 | א"ח הע"ר, ישר לבב 161 | בא' אדר, א' באדר | keep OCR word read as low-confidence review aid |
| 21 | `32` | 0 | 13 | 3 | רבי שלמה ה[06 | כ"א תמוז, בכ"א תמוז, כ"א בתמוז | keep OCR word read as low-confidence review aid |
| 22 | `29` | 0 | 15 | 3 | רבי עזריה | א' אדר א', בא' אדר א', א' באדר אי | keep OCR word read as low-confidence review aid |

## Boundary

- OCR words are read from the current local Table 2 TSV and row bands.
- OCR word availability is not transcription verification.
- Low confidence counts are review triage only.
- No row here changes the working WRR source or excludes a pair automatically.
