from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any


BUDGET_OPTIONS = {"low", "medium", "high"}
CITY_ALIASES = {
    "bengaluru": "bangalore",
    "blr": "bangalore",
    "bombay": "mumbai",
    "new delhi": "delhi",
}


class PreferenceValidationError(ValueError):
    """Raised when user preference input is invalid."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def normalize_city(value: str) -> str:
    city = normalize_text(value).lower()
    return CITY_ALIASES.get(city, city)


def parse_cuisines(value: Any) -> list[str]:
    text = normalize_text(value).lower()
    if not text:
        return []
    parts = re.split(r"[,/|]", text)
    cleaned = [normalize_text(part).lower() for part in parts]
    deduped: list[str] = []
    for part in cleaned:
        if part and part not in deduped:
            deduped.append(part)
    return deduped


def parse_minimum_rating(value: Any) -> float | None:
    text = normalize_text(value)
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def validate_allowed_city(city: str, allowed_cities: Iterable[str] | None) -> bool:
    if allowed_cities is None:
        return True
    normalized_allowed = {normalize_city(item) for item in allowed_cities if normalize_text(item)}
    return city in normalized_allowed

