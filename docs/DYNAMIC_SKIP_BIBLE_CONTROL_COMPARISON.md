# Dynamic Skip Bible-Control Comparison

This report compares the selected dynamic-skip terms in Bible corpora
against language-matched non-Bible controls using the same search rule.
It reports normalized hit rates per million legal ELS positions, not only
raw hit totals.

The primary hypothesis concerns original-language Bible texts. English
rows are secondary translation evidence: a KJV hit may be interesting,
but KJV absence does not count against an original-language hypothesis.

## Reproduce

```bash
python3 -m scripts.run_protocol protocols/dynamic_skip_focus_counts.toml --resume
python3 -m scripts.compare_dynamic_span_bible_controls
```

## Strongest Bible-Over-Control Rows

| Term | Language | Mode | Bible max | Control max | Control median | Ratio vs max | Read |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `dyn_netanyahu_g` | greek | `full-span` | 1.9e-05 | 0.0 | 0.0 | inf | bible max rate exceeds all observed controls |
| `dyn_netanyahu_g` | greek | `letters-per-term` | 1.9e-05 | 0.0 | 0.0 | inf | bible max rate exceeds all observed controls |
| `dyn_simsberry_e` | english | `full-span` | 2e-06 | 0.0 | 0.0 | inf | bible max rate exceeds all observed controls |
| `dyn_simsberry_e` | english | `letters-per-term` | 2e-06 | 0.0 | 0.0 | inf | bible max rate exceeds all observed controls |
| `dyn_netanyahu_e` | english | `full-span` | 2.1e-05 | 1e-05 | 9e-06 | 2.1 | bible max rate exceeds all observed controls |
| `dyn_netanyahu_e` | english | `letters-per-term` | 2.1e-05 | 1e-05 | 9e-06 | 2.1 | bible max rate exceeds all observed controls |
| `dyn_jesus_g` | greek | `full-span` | 0.156329 | 0.090406 | 0.076193 | 1.729188 | bible max rate exceeds all observed controls |
| `dyn_jesus_g` | greek | `letters-per-term` | 0.156342 | 0.090573 | 0.076367 | 1.726144 | bible max rate exceeds all observed controls |
| `dyn_jesus_e` | english | `letters-per-term` | 0.030918 | 0.021354 | 0.01798 | 1.447879 | bible max rate exceeds all observed controls |
| `dyn_jesus_e` | english | `full-span` | 0.030669 | 0.021227 | 0.018046 | 1.444811 | bible max rate exceeds all observed controls |
| `dyn_vance_g` | greek | `full-span` | 5.635415 | 4.003941 | 3.208866 | 1.407467 | bible max rate exceeds all observed controls |
| `dyn_vance_g` | greek | `letters-per-term` | 5.653076 | 4.021172 | 3.222537 | 1.405828 | bible max rate exceeds all observed controls |
| `dyn_magog_g` | greek | `letters-per-term` | 0.02778 | 0.019933 | 0.019603 | 1.393669 | bible max rate exceeds all observed controls |
| `dyn_iran_h` | hebrew | `full-span` | 1.932174 | 1.389463 | 1.302672 | 1.39059 | bible max rate exceeds all observed controls |
| `dyn_magog_g` | greek | `full-span` | 0.027649 | 0.01991 | 0.019562 | 1.388699 | bible max rate exceeds all observed controls |
| `dyn_iran_h` | hebrew | `letters-per-term` | 1.927104 | 1.389148 | 1.303544 | 1.387256 | bible max rate exceeds all observed controls |
| `dyn_russia_g` | greek | `letters-per-term` | 1.137009 | 0.884142 | 0.796585 | 1.286003 | bible max rate exceeds all observed controls |
| `dyn_russia_g` | greek | `full-span` | 1.138269 | 0.885589 | 0.795961 | 1.285324 | bible max rate exceeds all observed controls |
| `dyn_gog_g` | greek | `letters-per-term` | 8.464734 | 6.639559 | 5.80768 | 1.274894 | bible max rate exceeds all observed controls |
| `dyn_gog_g` | greek | `full-span` | 8.456437 | 6.65261 | 5.877657 | 1.271146 | bible max rate exceeds all observed controls |
| `dyn_yeshua_h` | hebrew | `letters-per-term` | 23.477473 | 18.929987 | 18.281675 | 1.240227 | bible max rate exceeds all observed controls |
| `dyn_yeshua_h` | hebrew | `full-span` | 23.40353 | 18.997337 | 18.228858 | 1.231937 | bible max rate exceeds all observed controls |
| `dyn_messiah_h` | hebrew | `full-span` | 10.997699 | 10.112089 | 8.907085 | 1.087579 | bible max rate exceeds all observed controls |
| `dyn_messiah_h` | hebrew | `letters-per-term` | 10.98166 | 10.100709 | 8.925534 | 1.087217 | bible max rate exceeds all observed controls |
| `dyn_beast_h` | hebrew | `full-span` | 230.650211 | 236.066963 | 214.629105 | 0.977054 | bible max rate exceeds control median but not control max |
| `dyn_beast_h` | hebrew | `letters-per-term` | 228.81664 | 235.154 | 214.787215 | 0.97305 | bible max rate exceeds control median but not control max |
| `dyn_dragon_h` | hebrew | `full-span` | 12.990292 | 14.077855 | 13.142202 | 0.922747 | control background equals or exceeds bible max rate |
| `dyn_dragon_h` | hebrew | `letters-per-term` | 12.877412 | 14.080474 | 13.121939 | 0.914558 | control background equals or exceeds bible max rate |
| `dyn_iran_g` | greek | `letters-per-term` | 31.244304 | 35.243502 | 32.872048 | 0.886527 | control background equals or exceeds bible max rate |
| `dyn_trump_g` | greek | `letters-per-term` | 0.273659 | 0.308695 | 0.296361 | 0.886503 | control background equals or exceeds bible max rate |
| `dyn_iran_g` | greek | `full-span` | 31.230634 | 35.234254 | 32.853146 | 0.886371 | control background equals or exceeds bible max rate |
| `dyn_trump_g` | greek | `full-span` | 0.272729 | 0.308867 | 0.295804 | 0.882998 | control background equals or exceeds bible max rate |
| `dyn_yhwh_h` | hebrew | `full-span` | 90.621568 | 105.435155 | 91.085419 | 0.8595 | control background equals or exceeds bible max rate |
| `dyn_yhwh_h` | hebrew | `letters-per-term` | 90.365364 | 105.679571 | 91.298375 | 0.855088 | control background equals or exceeds bible max rate |
| `dyn_beast_e` | english | `letters-per-term` | 0.93746 | 1.10822 | 0.831949 | 0.845915 | bible max rate exceeds control median but not control max |
| `dyn_beast_e` | english | `full-span` | 0.934809 | 1.110758 | 0.830604 | 0.841596 | bible max rate exceeds control median but not control max |
| `dyn_netanyahu_h` | hebrew | `letters-per-term` | 0.117824 | 0.148157 | 0.128604 | 0.795264 | control background equals or exceeds bible max rate |
| `dyn_netanyahu_h` | hebrew | `full-span` | 0.117744 | 0.148349 | 0.128595 | 0.793696 | control background equals or exceeds bible max rate |
| `dyn_beast_g` | greek | `full-span` | 0.0166 | 0.020947 | 0.019506 | 0.792476 | control background equals or exceeds bible max rate |
| `dyn_beast_g` | greek | `letters-per-term` | 0.016545 | 0.020925 | 0.019372 | 0.790681 | control background equals or exceeds bible max rate |

## Control-Background Rows

| Term | Language | Mode | Bible max | Control max | Control median | Ratio vs max | Read |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| `dyn_simscorner_e` | english | `full-span` | 0.0 | 1e-06 | 1e-06 | 0.0 | control background equals or exceeds bible max rate |
| `dyn_simscorner_e` | english | `letters-per-term` | 0.0 | 1e-06 | 1e-06 | 0.0 | control background equals or exceeds bible max rate |
| `dyn_cowboy_e` | english | `full-span` | 0.00048 | 0.001423 | 0.000835 | 0.337316 | control background equals or exceeds bible max rate |
| `dyn_cowboy_e` | english | `letters-per-term` | 0.000482 | 0.00142 | 0.000837 | 0.339437 | control background equals or exceeds bible max rate |
| `dyn_catering_e` | english | `full-span` | 6.5e-05 | 0.000169 | 0.000114 | 0.384615 | control background equals or exceeds bible max rate |
| `dyn_catering_e` | english | `letters-per-term` | 6.5e-05 | 0.000164 | 0.000113 | 0.396341 | control background equals or exceeds bible max rate |
| `dyn_gog_h` | hebrew | `full-span` | 7.825524 | 17.169332 | 15.876594 | 0.455785 | control background equals or exceeds bible max rate |
| `dyn_gog_h` | hebrew | `letters-per-term` | 7.91551 | 17.117399 | 15.876582 | 0.462425 | control background equals or exceeds bible max rate |
| `dyn_trump_h` | hebrew | `full-span` | 0.030278 | 0.064413 | 0.059456 | 0.47006 | control background equals or exceeds bible max rate |
| `dyn_trump_h` | hebrew | `letters-per-term` | 0.030551 | 0.064202 | 0.059625 | 0.475857 | control background equals or exceeds bible max rate |
| `dyn_russia_h` | hebrew | `letters-per-term` | 0.399452 | 0.816055 | 0.684429 | 0.489492 | control background equals or exceeds bible max rate |
| `dyn_russia_h` | hebrew | `full-span` | 0.399336 | 0.812461 | 0.684393 | 0.491514 | control background equals or exceeds bible max rate |
| `dyn_magog_h` | hebrew | `full-span` | 0.670453 | 1.357264 | 1.344102 | 0.493974 | control background equals or exceeds bible max rate |
| `dyn_magog_h` | hebrew | `letters-per-term` | 0.673021 | 1.357551 | 1.346352 | 0.495761 | control background equals or exceeds bible max rate |
| `dyn_vance_h` | hebrew | `full-span` | 2.542827 | 5.055542 | 4.683926 | 0.502978 | control background equals or exceeds bible max rate |
| `dyn_vance_h` | hebrew | `letters-per-term` | 2.548545 | 5.041959 | 4.689256 | 0.505467 | control background equals or exceeds bible max rate |
| `dyn_russia_e` | english | `letters-per-term` | 0.023615 | 0.046253 | 0.040265 | 0.510561 | control background equals or exceeds bible max rate |
| `dyn_russia_e` | english | `full-span` | 0.02368 | 0.046168 | 0.040379 | 0.512909 | control background equals or exceeds bible max rate |
| `dyn_trump_e` | english | `full-span` | 0.04288 | 0.081597 | 0.064015 | 0.52551 | control background equals or exceeds bible max rate |
| `dyn_trump_e` | english | `letters-per-term` | 0.042903 | 0.081404 | 0.063723 | 0.527038 | control background equals or exceeds bible max rate |
| `dyn_vance_e` | english | `full-span` | 0.113557 | 0.18896 | 0.150442 | 0.600958 | control background equals or exceeds bible max rate |
| `dyn_vance_e` | english | `letters-per-term` | 0.1139 | 0.188467 | 0.150522 | 0.60435 | control background equals or exceeds bible max rate |
| `dyn_gog_e` | english | `full-span` | 21.679279 | 34.669272 | 31.240092 | 0.625317 | control background equals or exceeds bible max rate |
| `dyn_gog_e` | english | `letters-per-term` | 21.592878 | 34.31608 | 31.481066 | 0.629235 | control background equals or exceeds bible max rate |
| `dyn_magog_e` | english | `letters-per-term` | 0.045264 | 0.06776 | 0.062833 | 0.668005 | control background equals or exceeds bible max rate |
| `dyn_magog_e` | english | `full-span` | 0.045532 | 0.067904 | 0.062663 | 0.670535 | control background equals or exceeds bible max rate |
| `dyn_christ_e` | english | `letters-per-term` | 0.027132 | 0.037219 | 0.03717 | 0.728983 | control background equals or exceeds bible max rate |
| `dyn_christ_e` | english | `full-span` | 0.027221 | 0.037286 | 0.037096 | 0.73006 | control background equals or exceeds bible max rate |
| `dyn_christ_g` | greek | `letters-per-term` | 0.00106 | 0.001416 | 0.001367 | 0.748588 | control background equals or exceeds bible max rate |
| `dyn_dragon_e` | english | `letters-per-term` | 0.019104 | 0.025502 | 0.019881 | 0.749118 | control background equals or exceeds bible max rate |
| `dyn_dragon_e` | english | `full-span` | 0.019125 | 0.025481 | 0.019844 | 0.750559 | control background equals or exceeds bible max rate |
| `dyn_dragon_g` | greek | `letters-per-term` | 0.007334 | 0.009753 | 0.009391 | 0.751974 | control background equals or exceeds bible max rate |
| `dyn_dragon_g` | greek | `full-span` | 0.007337 | 0.009679 | 0.009322 | 0.758033 | control background equals or exceeds bible max rate |
| `dyn_iran_e` | english | `letters-per-term` | 18.524796 | 23.967901 | 21.276435 | 0.7729 | control background equals or exceeds bible max rate |
| `dyn_christ_g` | greek | `full-span` | 0.001103 | 0.001426 | 0.001358 | 0.773492 | control background equals or exceeds bible max rate |
| `dyn_iran_e` | english | `full-span` | 18.585397 | 24.019645 | 21.235366 | 0.773758 | control background equals or exceeds bible max rate |
| `dyn_beast_g` | greek | `letters-per-term` | 0.016545 | 0.020925 | 0.019372 | 0.790681 | control background equals or exceeds bible max rate |
| `dyn_beast_g` | greek | `full-span` | 0.0166 | 0.020947 | 0.019506 | 0.792476 | control background equals or exceeds bible max rate |
| `dyn_netanyahu_h` | hebrew | `full-span` | 0.117744 | 0.148349 | 0.128595 | 0.793696 | control background equals or exceeds bible max rate |
| `dyn_netanyahu_h` | hebrew | `letters-per-term` | 0.117824 | 0.148157 | 0.128604 | 0.795264 | control background equals or exceeds bible max rate |

## Read

- This is an observed-control comparison, not a final claim test.
- A favorable row should still be checked for all-hit context,
  version/source distribution, same-skip extensions, and matched
  shuffled or real-word controls.
- A non-Bible match does not disprove the hypothesis by itself, but it
  raises the background rate that a Bible pattern must exceed.
