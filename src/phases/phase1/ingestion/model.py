from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Restaurant:
    """Canonical restaurant record for downstream phases."""

    id: str
    name: str
    location: str
    cuisines: list[str]
    cost_for_two: float | None
    cost_band: str
    rating: float | None
    rating_votes: int | None
    source_row_hash: str

