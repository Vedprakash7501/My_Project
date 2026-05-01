from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .model import UserPreferences
from .validate import (
    BUDGET_OPTIONS,
    PreferenceValidationError,
    normalize_city,
    normalize_text,
    parse_cuisines,
    parse_minimum_rating,
    validate_allowed_city,
)


MAX_ADDITIONAL_PREF_CHARS = 300


def preferences_from_mapping(
    payload: Mapping[str, Any],
    *,
    allowed_cities: Iterable[str] | None = None,
) -> UserPreferences:
    errors: list[str] = []

    location_raw = payload.get("location")
    location = normalize_city(normalize_text(location_raw))
    if not location:
        errors.append("location is required")
    elif not validate_allowed_city(location, allowed_cities):
        errors.append(f"location '{location}' is not supported")

    budget = normalize_text(payload.get("budget")).lower()
    if not budget:
        errors.append("budget is required")
    elif budget not in BUDGET_OPTIONS:
        errors.append("budget must be one of: low, medium, high")

    cuisines = parse_cuisines(payload.get("cuisines"))
    if not cuisines:
        errors.append("cuisines is required (comma-separated values accepted)")

    minimum_rating = parse_minimum_rating(payload.get("minimum_rating"))
    if minimum_rating is None:
        errors.append("minimum_rating is required and must be a number")
    elif not (0.0 <= minimum_rating <= 5.0):
        errors.append("minimum_rating must be in range 0.0 to 5.0")

    additional_preferences = normalize_text(payload.get("additional_preferences"))
    if additional_preferences:
        if len(additional_preferences) > MAX_ADDITIONAL_PREF_CHARS:
            additional_preferences = additional_preferences[:MAX_ADDITIONAL_PREF_CHARS]
    else:
        additional_preferences = None

    if errors:
        raise PreferenceValidationError(errors)

    return UserPreferences(
        location=location,
        budget=budget,
        cuisines=cuisines,
        minimum_rating=minimum_rating,
        additional_preferences=additional_preferences,
    )

