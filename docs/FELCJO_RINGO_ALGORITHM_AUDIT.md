# Felcjo Ringo Algorithm Source Audit

Source: [Bible Codes: Making an Algorithm to Find Hidden Word Sequences in
Text](https://felcjo-ringo.medium.com/bible-codes-making-an-algorithm-to-find-hidden-word-sequences-in-text-c36e94556469),
Felcjo Ringo, Medium, March 19, 2019.

Related code link from the article:
`https://github.com/pringithub/bible-codes-algebraic-text-anomalies`.

Status: public methodology audit. This is not a reproduction report, and no
code from the linked repository is imported.

## Why This Source Matters

This article is useful mainly as an implementation/control caution rather than
as a new claim source. It describes a simple ELS finder that:

- normalizes text by removing spaces, punctuation, and case distinctions;
- splits text into stride lanes for each skip value;
- searches both forward and reverse directions;
- uses an English dictionary of about 3,800 words for candidate detection;
- reports a non-Bible control run against the first paragraph of `Siddhartha`;
- found 622 distinct words longer than two letters in a 927-letter paragraph;
- reports the longest result as `another` and common short results such as
  `the`, `tie`, and `tea`;
- reports about 210 seconds for the forward-plus-reverse pass on that short
  paragraph;
- estimates the brute-force approach as roughly cubic in text size;
- explicitly notes that word-search and "find all dictionary words" are
  different algorithmic tasks.

## Project Relevance

The article reinforces several choices already made in this repository:

- lane-based skip scanning is the right conceptual model;
- forward and backward directions both need to be searched;
- naive exhaustive dictionary scanning over many skips is too slow for large
  corpora;
- short dictionary words create many ordinary hits in non-Bible text;
- non-Bible controls are mandatory before interpreting ELS counts;
- language-specific normalization and lexicons matter.

## Claim-Catalog Handling

The claim catalog includes this as a methodology/control row, not a positive
Bible-code claim. The only Bible-code example cited by the article is the common
Drosnin Rabin/Yitzhak Rabin/assassin/Yigal Amir example, which remains
under-specified unless independently locked from a primary source.

## License And Reuse Notes

The Medium article is a public web article. The linked GitHub repository is
small and public, but this project does not import or derive code from it. Any
future code comparison should treat the repository as source-audit context only
unless its license is verified.

## Cautions

- The article is an educational implementation note, not a statistical study.
- The English dictionary test is a useful control intuition, not a formal null
  model.
- The reported runtime reflects a naive implementation and should not be used
  as a benchmark for this project.
- The article's Rabin example is a popular Drosnin-style reference; it is not
  locked enough for reproduction status here.
