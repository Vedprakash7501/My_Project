from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class UserPreferences:
    """Validated user preference object for retrieval layer input."""

    location: str
    budget: str
    cuisines: list[str]
    minimum_rating: float
    additional_preferences: str | None = None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

