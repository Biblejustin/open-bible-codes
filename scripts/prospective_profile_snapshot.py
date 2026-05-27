"""Shared prospective-profile status snapshot helpers."""

from __future__ import annotations

from collections import Counter


def status_count_phrases(profiles: list[dict[str, object]]) -> tuple[str, ...]:
    counts = Counter(str(profile.get("status", "")) for profile in profiles)
    return (
        f"Tracked profiles: {len(profiles)}.",
        *(f"`{status}`: {counts[status]}." for status in sorted(counts)),
    )
