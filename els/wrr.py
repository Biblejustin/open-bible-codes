"""WRR-style statistic helpers.

These helpers cover arithmetic that is independent of the disputed term list:
skip-window expectation, low-level WRR ELS proximity primitives, Q aggregation
for already-domain-labeled ELS rows, P1/P2 aggregate transforms, and
permutation ranks. They do not implement the full corrected distance c(w,w').
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable, Iterator, Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class WrrElsOccurrence:
    """One ELS occurrence plus its half-open domain of minimality."""

    offsets: tuple[int, ...]
    skip: int
    domain_start: int
    domain_end: int


@dataclass(frozen=True)
class WrrDomainAssignment:
    """Domain-labeling result for one ELS candidate."""

    offsets: tuple[int, ...]
    skip: int
    domain_start: int | None
    domain_end: int | None
    status: str
    reason: str = ""
    candidate_count: int = 0

    def to_occurrence(self) -> WrrElsOccurrence:
        if (
            self.status != "defined"
            or self.domain_start is None
            or self.domain_end is None
        ):
            raise ValueError("domain assignment is not defined")
        return WrrElsOccurrence(
            self.offsets,
            self.skip,
            self.domain_start,
            self.domain_end,
        )

def perturbation_triples(radius: int = 2) -> tuple[tuple[int, int, int], ...]:
    """Return WRR perturbation triples `(x, y, z)`.

    WRR's corrected-distance construction compares the ordinary ELS to
    perturbations where each of the last three gaps is shifted by a cumulative
    value from `{-2, -1, 0, 1, 2}`. The default radius therefore yields 125
    triples.
    """

    if radius < 0:
        raise ValueError("radius must be >= 0")
    values = range(-radius, radius + 1)
    return tuple((x, y, z) for x in values for y in values for z in values)


def perturbed_offsets(
    start: int,
    skip: int,
    word_length: int,
    perturbation: tuple[int, int, int],
) -> tuple[int, ...]:
    """Return offsets for a WRR last-three-gap perturbation."""

    if skip == 0:
        raise ValueError("skip must not be 0")
    if word_length < 4:
        raise ValueError("word_length must be >= 4")
    if len(perturbation) != 3:
        raise ValueError("perturbation must contain exactly 3 integers")
    x, y, z = perturbation
    offsets: list[int] = []
    for index in range(word_length):
        if index <= word_length - 4:
            adjustment = 0
        elif index == word_length - 3:
            adjustment = x
        elif index == word_length - 2:
            adjustment = x + y
        else:
            adjustment = x + y + z
        offsets.append(start + index * skip + adjustment)
    return tuple(offsets)


def is_perturbed_els_match(
    text: str,
    word: str,
    start: int,
    skip: int,
    perturbation: tuple[int, int, int],
) -> bool:
    """Return whether one WRR perturbed ELS exactly spells `word` in `text`."""

    if not text:
        raise ValueError("text must not be empty")
    if not word:
        raise ValueError("word must not be empty")
    offsets = perturbed_offsets(start, skip, len(word), perturbation)
    return all(
        0 <= offset < len(text) and text[offset] == letter
        for offset, letter in zip(offsets, word)
    )


def iter_perturbed_els_matches(
    text: str,
    word: str,
    *,
    min_skip: int,
    max_skip: int,
    direction: str = "both",
    perturbation: tuple[int, int, int] = (0, 0, 0),
    max_hits: int | None = None,
) -> Iterator[tuple[int, int, tuple[int, ...]]]:
    """Yield exact WRR perturbed ELS matches for bounded diagnostics."""

    if not text:
        raise ValueError("text must not be empty")
    if not word:
        raise ValueError("word must not be empty")
    if min_skip < 1:
        raise ValueError("min_skip must be >= 1")
    if max_skip < min_skip:
        raise ValueError("max_skip must be >= min_skip")
    if direction not in {"forward", "backward", "both"}:
        raise ValueError("direction must be forward, backward, or both")
    if max_hits is not None and max_hits < 1:
        raise ValueError("max_hits must be >= 1")

    yielded = 0
    skips: list[int] = []
    if direction in {"forward", "both"}:
        skips.extend(range(min_skip, max_skip + 1))
    if direction in {"backward", "both"}:
        skips.extend(range(-min_skip, -max_skip - 1, -1))
    for skip in skips:
        for start in range(len(text)):
            offsets = perturbed_offsets(start, skip, len(word), perturbation)
            if all(
                0 <= offset < len(text) and text[offset] == letter
                for offset, letter in zip(offsets, word)
            ):
                yield start, skip, offsets
                yielded += 1
                if max_hits is not None and yielded >= max_hits:
                    return


def nearest_integer_half_up(numerator: int, denominator: int) -> int:
    """Round `numerator / denominator` to nearest integer, halves upward."""

    if numerator < 0:
        raise ValueError("numerator must be >= 0")
    if denominator <= 0:
        raise ValueError("denominator must be > 0")
    quotient, remainder = divmod(numerator, denominator)
    if remainder * 2 >= denominator:
        return quotient + 1
    return quotient


def wrr_row_widths(skip: int, *, count: int = 10) -> tuple[int, ...]:
    """Return the first WRR candidate row widths for an ELS skip.

    The paper describes the first ten integer widths nearest to `|d| / i`,
    with half-integers rounded up. This helper preserves that ordered sequence;
    a later corrected-distance aggregation can decide whether duplicate widths
    should be retained or coalesced.
    """

    if skip == 0:
        raise ValueError("skip must not be 0")
    if count < 1:
        raise ValueError("count must be >= 1")
    absolute_skip = abs(skip)
    return tuple(
        max(1, nearest_integer_half_up(absolute_skip, index))
        for index in range(1, count + 1)
    )


def ordinary_els_offsets(start: int, skip: int, word_length: int) -> tuple[int, ...]:
    """Return ordinary ELS offsets in reading order."""

    if skip == 0:
        raise ValueError("skip must not be 0")
    if word_length < 1:
        raise ValueError("word_length must be >= 1")
    return tuple(start + index * skip for index in range(word_length))


def cylindrical_letter_distance_squared(
    left_offset: int,
    right_offset: int,
    row_width: int,
) -> int:
    """Return squared letter distance on a cylindrical WRR-style table."""

    if row_width <= 0:
        raise ValueError("row_width must be > 0")
    if left_offset < 0 or right_offset < 0:
        raise ValueError("offsets must be >= 0")
    left_row, left_col = divmod(left_offset, row_width)
    right_row, right_col = divmod(right_offset, row_width)
    raw_col_delta = abs(left_col - right_col)
    col_delta = min(raw_col_delta, row_width - raw_col_delta)
    row_delta = abs(left_row - right_row)
    return col_delta * col_delta + row_delta * row_delta


def wrr2_els_sl_distance_at_row_width(
    els_offsets: Iterable[int],
    *,
    sl_start: int,
    sl_length: int,
    row_width: int,
) -> int:
    """Return the WRR2/Nations ELS-vs-surface-string distance at one width.

    The WRR2 methodology defines the fixed-array distance as
    `f^2 + f'^2 + l^2 + 1`, where `f` is the distance between the first two
    ELS letters, `f'` is `1` for a surface-letter string, and `l` is the
    nearest letter-to-letter distance between the ELS and surface string.
    """

    offsets = tuple(els_offsets)
    if len(offsets) < 2:
        raise ValueError("els_offsets must contain at least two offsets")
    if sl_start < 0:
        raise ValueError("sl_start must be >= 0")
    if sl_length < 1:
        raise ValueError("sl_length must be >= 1")
    f_squared = cylindrical_letter_distance_squared(offsets[0], offsets[1], row_width)
    sl_offsets = range(sl_start, sl_start + sl_length)
    nearest_squared = min(
        cylindrical_letter_distance_squared(els_offset, sl_offset, row_width)
        for els_offset in offsets
        for sl_offset in sl_offsets
    )
    return f_squared + nearest_squared + 2


def wrr2_els_sl_proximity_at_row_width(
    els_offsets: Iterable[int],
    *,
    sl_start: int,
    sl_length: int,
    row_width: int,
) -> float:
    """Return inverse WRR2/Nations ELS-vs-surface-string distance."""

    return 1.0 / wrr2_els_sl_distance_at_row_width(
        els_offsets,
        sl_start=sl_start,
        sl_length=sl_length,
        row_width=row_width,
    )


def wrr2_els_sl_proximity(
    els_offsets: Iterable[int],
    *,
    sl_start: int,
    sl_length: int,
    row_widths: Iterable[int],
) -> float:
    """Return summed WRR2/Nations proximity across candidate row widths."""

    widths = tuple(row_widths)
    if not widths:
        raise ValueError("row_widths must not be empty")
    offsets = tuple(els_offsets)
    return sum(
        wrr2_els_sl_proximity_at_row_width(
            offsets,
            sl_start=sl_start,
            sl_length=sl_length,
            row_width=row_width,
        )
        for row_width in widths
    )


def wrr2_ordinary_els_sl_proximity(
    *,
    start: int,
    skip: int,
    word_length: int,
    sl_start: int,
    sl_length: int,
    row_width_count: int = 10,
) -> float:
    """Return WRR2/Nations proximity for one ordinary ELS and one SL."""

    return wrr2_els_sl_proximity(
        ordinary_els_offsets(start, skip, word_length),
        sl_start=sl_start,
        sl_length=sl_length,
        row_widths=wrr_row_widths(skip, count=row_width_count),
    )


def wrr_els_els_distance_at_row_width(
    left_offsets: Iterable[int],
    right_offsets: Iterable[int],
    *,
    row_width: int,
) -> int:
    """Return WRR 1994 ELS-vs-ELS distance at one row width.

    The 1994 paper defines the fixed-array distance as
    `f^2 + f'^2 + l^2`, where `f` and `f'` are the distances between
    consecutive letters of each ELS and `l` is the nearest letter-to-letter
    distance between the two ELS rows.
    """

    left = tuple(left_offsets)
    right = tuple(right_offsets)
    if len(left) < 2 or len(right) < 2:
        raise ValueError("both ELS offset sequences must contain at least two offsets")
    left_f_squared = cylindrical_letter_distance_squared(left[0], left[1], row_width)
    right_f_squared = cylindrical_letter_distance_squared(right[0], right[1], row_width)
    nearest_squared = min(
        cylindrical_letter_distance_squared(left_offset, right_offset, row_width)
        for left_offset in left
        for right_offset in right
    )
    return left_f_squared + right_f_squared + nearest_squared


def wrr_els_els_proximity_at_row_width(
    left_offsets: Iterable[int],
    right_offsets: Iterable[int],
    *,
    row_width: int,
) -> float:
    """Return inverse WRR 1994 ELS-vs-ELS distance at one row width."""

    return 1.0 / wrr_els_els_distance_at_row_width(
        left_offsets,
        right_offsets,
        row_width=row_width,
    )


def wrr_els_els_alpha(
    left_offsets: Iterable[int],
    right_offsets: Iterable[int],
    *,
    left_skip: int,
    right_skip: int,
    row_width_count: int = 10,
) -> float:
    """Return WRR 1994 `alpha(e,e')` over both ELS row-width series."""

    left = tuple(left_offsets)
    right = tuple(right_offsets)
    widths = wrr_row_widths(left_skip, count=row_width_count) + wrr_row_widths(
        right_skip,
        count=row_width_count,
    )
    return sum(
        wrr_els_els_proximity_at_row_width(left, right, row_width=row_width)
        for row_width in widths
    )


def wrr_ordinary_els_els_alpha(
    *,
    left_start: int,
    left_skip: int,
    left_word_length: int,
    right_start: int,
    right_skip: int,
    right_word_length: int,
    row_width_count: int = 10,
) -> float:
    """Return WRR 1994 `alpha(e,e')` for two ordinary ELS rows."""

    return wrr_els_els_alpha(
        ordinary_els_offsets(left_start, left_skip, left_word_length),
        ordinary_els_offsets(right_start, right_skip, right_word_length),
        left_skip=left_skip,
        right_skip=right_skip,
        row_width_count=row_width_count,
    )


def wrr_offsets_span(offsets: Iterable[int], *, text_length: int) -> tuple[int, int]:
    """Return the half-open text span containing one ELS offset row."""

    if text_length < 1:
        raise ValueError("text_length must be > 0")
    positions = tuple(offsets)
    if not positions:
        raise ValueError("offsets must not be empty")
    if any(offset < 0 or offset >= text_length for offset in positions):
        raise ValueError("offsets must be inside text")
    return min(positions), max(positions) + 1


def wrr_minimality_domain(
    target_offsets: Iterable[int],
    *,
    target_skip: int,
    competing_occurrences: Iterable[tuple[Iterable[int], int]],
    text_length: int,
) -> tuple[int, int] | None:
    """Return the unambiguous half-open WRR domain of minimality for one ELS.

    The source domain is the maximal segment containing `target_offsets` that
    does not contain any same-word ELS with smaller absolute skip. If a smaller
    ELS is inside the target span, no such domain can contain the target. If a
    smaller ELS strictly encloses the target span, there are two incomparable
    maximal choices; this helper returns `None` for that unresolved case.
    """

    candidates = wrr_minimality_domain_candidates(
        target_offsets,
        target_skip=target_skip,
        competing_occurrences=competing_occurrences,
        text_length=text_length,
    )
    if len(candidates) != 1:
        return None
    return candidates[0]


def wrr_minimality_domain_candidates(
    target_offsets: Iterable[int],
    *,
    target_skip: int,
    competing_occurrences: Iterable[tuple[Iterable[int], int]],
    text_length: int,
) -> tuple[tuple[int, int], ...]:
    """Return maximal half-open WRR minimality-domain candidates.

    A shorter-skip same-word ELS inside the target span blocks every domain.
    A shorter-skip ELS strictly enclosing the target span creates multiple
    incomparable maximal segments; this helper exposes those candidates instead
    of choosing one.
    """

    if target_skip == 0:
        raise ValueError("target_skip must not be 0")
    target_start, target_end = wrr_offsets_span(target_offsets, text_length=text_length)
    target_last = target_end - 1
    domain_start = 0
    domain_end = text_length
    enclosing: list[tuple[int, int]] = []
    target_abs_skip = abs(target_skip)
    for competing_offsets, competing_skip in competing_occurrences:
        competing_positions = tuple(competing_offsets)
        if competing_skip == 0:
            raise ValueError("competing skip must not be 0")
        if abs(competing_skip) >= target_abs_skip:
            continue
        competing_start, competing_end = wrr_offsets_span(
            competing_positions,
            text_length=text_length,
        )
        competing_last = competing_end - 1
        if competing_start >= target_start and competing_last <= target_last:
            return ()
        if competing_start < target_start and competing_last > target_last:
            enclosing.append((competing_start, competing_last))
            continue
        if competing_start < target_start:
            domain_start = max(domain_start, competing_start + 1)
        if competing_last > target_last:
            domain_end = min(domain_end, competing_last)
    if domain_start > target_start or domain_end < target_end:
        return ()
    if not enclosing:
        return ((domain_start, domain_end),)

    starts = {domain_start, *(start + 1 for start, _ in enclosing)}
    ends = {domain_end, *(last for _, last in enclosing)}
    candidates: list[tuple[int, int]] = []
    for start in starts:
        if start < domain_start or start > target_start:
            continue
        for end in ends:
            if end > domain_end or end < target_end or start >= end:
                continue
            if all(start > enc_start or end <= enc_last for enc_start, enc_last in enclosing):
                candidates.append((start, end))
    return maximal_intervals(candidates)


def maximal_intervals(intervals: Iterable[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    """Return intervals not strictly contained by another interval."""

    unique = sorted(set(intervals))
    maximal: list[tuple[int, int]] = []
    for candidate in unique:
        if any(
            other != candidate and other[0] <= candidate[0] and other[1] >= candidate[1]
            for other in unique
        ):
            continue
        maximal.append(candidate)
    return tuple(maximal)


def wrr_label_minimality_domains(
    occurrences: Iterable[tuple[Iterable[int], int]],
    *,
    text_length: int,
) -> tuple[WrrDomainAssignment, ...]:
    """Label every same-word ELS row with its conservative minimality domain."""

    rows = tuple((tuple(offsets), skip) for offsets, skip in occurrences)
    assignments: list[WrrDomainAssignment] = []
    for index, (offsets, skip) in enumerate(rows):
        competitors = (
            (other_offsets, other_skip)
            for other_index, (other_offsets, other_skip) in enumerate(rows)
            if other_index != index
        )
        domains = wrr_minimality_domain_candidates(
            offsets,
            target_skip=skip,
            competing_occurrences=competitors,
            text_length=text_length,
        )
        if len(domains) != 1:
            reason = (
                "blocked_by_inner_shorter_skip"
                if len(domains) == 0
                else "ambiguous_enclosing_shorter_skip"
            )
            assignments.append(
                WrrDomainAssignment(
                    offsets,
                    skip,
                    None,
                    None,
                    "undefined",
                    reason=reason,
                    candidate_count=len(domains),
                )
            )
        else:
            domain_start, domain_end = domains[0]
            assignments.append(
                WrrDomainAssignment(
                    offsets,
                    skip,
                    domain_start,
                    domain_end,
                    "defined",
                    candidate_count=1,
                )
            )
    return tuple(assignments)


def validate_wrr_occurrence(occurrence: WrrElsOccurrence, *, text_length: int) -> None:
    if text_length < 1:
        raise ValueError("text_length must be > 0")
    if occurrence.skip == 0:
        raise ValueError("skip must not be 0")
    if len(occurrence.offsets) < 2:
        raise ValueError("offsets must contain at least two positions")
    if any(offset < 0 or offset >= text_length for offset in occurrence.offsets):
        raise ValueError("offsets must be inside text")
    if not (0 <= occurrence.domain_start < occurrence.domain_end <= text_length):
        raise ValueError("domain must be a non-empty half-open interval inside text")
    if min(occurrence.offsets) < occurrence.domain_start:
        raise ValueError("domain must include occurrence offsets")
    if max(occurrence.offsets) >= occurrence.domain_end:
        raise ValueError("domain must include occurrence offsets")


def wrr_domain_intersection_length(
    left: WrrElsOccurrence,
    right: WrrElsOccurrence,
    *,
    text_length: int,
) -> int:
    """Return `X(e,e')`, the overlap length of two domains of minimality."""

    validate_wrr_occurrence(left, text_length=text_length)
    validate_wrr_occurrence(right, text_length=text_length)
    start = max(left.domain_start, right.domain_start)
    end = min(left.domain_end, right.domain_end)
    return max(0, end - start)


def wrr_domain_weight(
    left: WrrElsOccurrence,
    right: WrrElsOccurrence,
    *,
    text_length: int,
) -> float:
    """Return WRR `omega(e,e') = X(e,e') / X(G)` for two ELS occurrences."""

    return wrr_domain_intersection_length(left, right, text_length=text_length) / text_length


def wrr_weighted_els_pair_proximity(
    left: WrrElsOccurrence,
    right: WrrElsOccurrence,
    *,
    text_length: int,
    row_width_count: int = 10,
) -> float:
    """Return one WRR `omega(e,e') * alpha(e,e')` contribution."""

    return wrr_domain_weight(left, right, text_length=text_length) * wrr_els_els_alpha(
        left.offsets,
        right.offsets,
        left_skip=left.skip,
        right_skip=right.skip,
        row_width_count=row_width_count,
    )


def wrr_word_pair_proximity(
    left_occurrences: Iterable[WrrElsOccurrence],
    right_occurrences: Iterable[WrrElsOccurrence],
    *,
    text_length: int,
    row_width_count: int = 10,
) -> float:
    """Return WRR `Q(w,w')` from already-domain-labeled ELS occurrences."""

    left_rows = tuple(left_occurrences)
    right_rows = tuple(right_occurrences)
    if not left_rows or not right_rows:
        return 0.0
    return sum(
        wrr_weighted_els_pair_proximity(
            left,
            right,
            text_length=text_length,
            row_width_count=row_width_count,
        )
        for left in left_rows
        for right in right_rows
    )


def corrected_distance_rank(
    ordinary_proximity: float,
    perturbation_proximities: Iterable[float],
    *,
    minimum_valid: int = 10,
) -> float:
    """Rank ordinary proximity among already-computed perturbation proximities.

    WRR's corrected distance is small when ordinary proximity is unusually
    large. This helper only performs the source-described ranking step; callers
    still need to compute the actual proximity values and valid-perturbation
    set. The ordinary `(0, 0, 0)` value must be present in that set.
    """

    values = validate_corrected_distance_inputs(
        ordinary_proximity,
        perturbation_proximities,
        minimum_valid=minimum_valid,
    )
    equal = sum(1 for value in values if value == ordinary_proximity)
    greater = sum(1 for value in values if value > ordinary_proximity)
    tied_others = equal - 1
    rank = greater + 0.5 * tied_others
    return rank / len(values)


def corrected_distance_wrr_rank(
    ordinary_proximity: float,
    perturbation_proximities: Iterable[float],
    *,
    minimum_valid: int = 10,
) -> float:
    """Return WRR 1994 Appendix A.2 corrected-distance rank `v / m`.

    Source descriptions define `v(w,w')` as the number of valid perturbation
    proximities greater than or equal to the ordinary proximity and `m(w,w')`
    as the number of valid perturbation triples. Unlike the WRR2 tie-aware
    helper above, this source formula gives full weight to tied perturbations.
    """

    values = validate_corrected_distance_inputs(
        ordinary_proximity,
        perturbation_proximities,
        minimum_valid=minimum_valid,
    )
    greater_or_equal = sum(1 for value in values if value >= ordinary_proximity)
    return greater_or_equal / len(values)


def corrected_distance_strict_rank(
    ordinary_proximity: float,
    perturbation_proximities: Iterable[float],
    *,
    minimum_valid: int = 10,
) -> float:
    """Backward-compatible name for `corrected_distance_wrr_rank`.

    The old name meant "not tie-aware"; source checks now show the WRR count
    includes perturbation proximities greater than or equal to ordinary.
    """

    return corrected_distance_wrr_rank(
        ordinary_proximity,
        perturbation_proximities,
        minimum_valid=minimum_valid,
    )


def validate_corrected_distance_inputs(
    ordinary_proximity: float,
    perturbation_proximities: Iterable[float],
    *,
    minimum_valid: int,
) -> list[float]:
    if minimum_valid < 1:
        raise ValueError("minimum_valid must be >= 1")
    if not math.isfinite(ordinary_proximity):
        raise ValueError("ordinary_proximity must be finite")
    values = list(perturbation_proximities)
    if len(values) < minimum_valid:
        raise ValueError("not enough valid perturbation proximities")
    for value in values:
        if not math.isfinite(value):
            raise ValueError("perturbation proximities must be finite")
    equal = sum(1 for value in values if value == ordinary_proximity)
    if equal == 0:
        raise ValueError("ordinary proximity must be present in perturbation set")
    return values


def els_window_count(text_length: int, word_length: int, max_skip: int) -> int:
    """Count signed ELS windows with 2 <= |skip| <= max_skip.

    Formula from the WRR appendix:
    (D - 1) * (2L - (k - 1) * (D + 2)).
    """

    if text_length < 1:
        raise ValueError("text_length must be > 0")
    if word_length < 1:
        raise ValueError("word_length must be > 0")
    if max_skip < 2:
        return 0
    return max(0, (max_skip - 1) * (2 * text_length - (word_length - 1) * (max_skip + 2)))


def relative_letter_frequencies(text: str) -> dict[str, float]:
    if not text:
        raise ValueError("text must not be empty")
    counts = Counter(text)
    length = len(text)
    return {letter: count / length for letter, count in counts.items()}


def expected_els_count(
    text_length: int,
    word: str,
    max_skip: int,
    frequencies: Mapping[str, float],
) -> float:
    if not word:
        raise ValueError("word must not be empty")
    probability = 1.0
    for letter in word:
        probability *= frequencies.get(letter, 0.0)
    return probability * els_window_count(text_length, len(word), max_skip)


def skip_cap_for_expected_count(
    text: str,
    word: str,
    *,
    target_expected: float = 10.0,
    max_skip_limit: int | None = None,
) -> int:
    """Return the first D whose expected count reaches target_expected.

    The WRR appendix describes choosing D(w) so the expected ELS count is 10.
    Since D is integral in this implementation, this returns the smallest D
    with expected count >= target_expected, capped by max_skip_limit.
    """

    if target_expected <= 0:
        raise ValueError("target_expected must be > 0")
    if not text:
        raise ValueError("text must not be empty")
    if not word:
        raise ValueError("word must not be empty")
    possible_limit = max(2, (len(text) - 1) // max(1, len(word) - 1))
    limit = min(max_skip_limit or possible_limit, possible_limit)
    frequencies = relative_letter_frequencies(text)
    for max_skip in range(2, limit + 1):
        if expected_els_count(len(text), word, max_skip, frequencies) >= target_expected:
            return max_skip
    return limit


def p1_binomial_tail(c_values: Iterable[float], *, threshold: float = 0.2) -> float:
    values = valid_c_values(c_values)
    n = len(values)
    if n == 0:
        raise ValueError("at least one c value is required")
    k = sum(1 for value in values if value <= threshold)
    return binomial_upper_tail(n, k, threshold)


def binomial_upper_tail(n: int, k: int, probability: float) -> float:
    if n < 0:
        raise ValueError("n must be >= 0")
    if k < 0:
        return 1.0
    if k > n:
        return 0.0
    if not 0 <= probability <= 1:
        raise ValueError("probability must be in [0, 1]")
    return sum(
        math.comb(n, j) * probability**j * (1.0 - probability) ** (n - j)
        for j in range(k, n + 1)
    )


def p2_product_statistic(c_values: Iterable[float]) -> float:
    values = valid_c_values(c_values)
    if not values:
        raise ValueError("at least one c value is required")
    if any(value == 0 for value in values):
        return 0.0
    log_product = sum(math.log(value) for value in values)
    return product_uniform_cdf_from_log(log_product, len(values))


def product_uniform_cdf_from_log(log_product: float, n: int) -> float:
    """CDF for product of n independent U(0,1) variables at exp(log_product)."""

    if n < 1:
        raise ValueError("n must be >= 1")
    if log_product > 0:
        raise ValueError("log_product must be <= 0")
    s = -log_product
    if s == 0:
        return 1.0
    log_terms = [j * math.log(s) - math.lgamma(j + 1) for j in range(n)]
    max_log = max(log_terms)
    log_sum = max_log + math.log(sum(math.exp(term - max_log) for term in log_terms))
    return math.exp(-s + log_sum)


def permutation_rank_rho(observed: float, permuted: Iterable[float]) -> float:
    """Return WRR-style rank proportion with half-weighted ties."""

    samples = list(permuted)
    less = sum(1 for value in samples if value < observed)
    equal = sum(1 for value in samples if value == observed)
    rank = 1.0 + less + 0.5 * equal
    return rank / (len(samples) + 1)


def bonferroni_rho0(rhos: Iterable[float], *, statistic_count: int = 4) -> float:
    values = list(rhos)
    if not values:
        raise ValueError("at least one rho is required")
    if statistic_count < 1:
        raise ValueError("statistic_count must be >= 1")
    return statistic_count * min(values)


def valid_c_values(c_values: Iterable[float]) -> list[float]:
    values = list(c_values)
    for value in values:
        if not 0 <= value <= 1:
            raise ValueError("c values must be in [0, 1]")
    return values
