from __future__ import annotations

from dataclasses import dataclass

from phases.phase1.ingestion.model import Restaurant
from phases.phase2.preferences.model import UserPreferences


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    candidates: list[Restaurant]
    total_before_cap: int
    candidate_cap: int


def _location_matches(restaurant: Restaurant, prefs: UserPreferences) -> bool:
    return restaurant.location.lower() == prefs.location.lower()


def _rating_matches(restaurant: Restaurant, prefs: UserPreferences) -> bool:
    if restaurant.rating is None:
        return False
    return restaurant.rating >= prefs.minimum_rating


def _budget_matches(restaurant: Restaurant, prefs: UserPreferences) -> bool:
    return restaurant.cost_band.lower() == prefs.budget.lower()


def _cuisine_matches(restaurant: Restaurant, prefs: UserPreferences) -> bool:
    restaurant_tokens = {token.lower() for token in restaurant.cuisines}
    pref_tokens = {token.lower() for token in prefs.cuisines}
    if not pref_tokens:
        return True
    if restaurant_tokens.intersection(pref_tokens):
        return True

    # Soft partial match to reduce strict exact-match misses.
    for pref in pref_tokens:
        for rc in restaurant_tokens:
            if pref in rc or rc in pref:
                return True
    return False


def _sort_key(restaurant: Restaurant) -> tuple[float, int]:
    # Higher rating first, then vote count.
    rating = restaurant.rating if restaurant.rating is not None else -1.0
    votes = restaurant.rating_votes if restaurant.rating_votes is not None else -1
    return (rating, votes)


def retrieve_candidates(
    restaurants: list[Restaurant],
    prefs: UserPreferences,
    *,
    candidate_cap: int = 20,
) -> RetrievalResult:
    if candidate_cap < 1:
        raise ValueError("candidate_cap must be >= 1")

    filtered = [
        item
        for item in restaurants
        if _location_matches(item, prefs)
        and _rating_matches(item, prefs)
        and _budget_matches(item, prefs)
        and _cuisine_matches(item, prefs)
    ]
    filtered.sort(key=_sort_key, reverse=True)
    total_before_cap = len(filtered)
    capped = filtered[:candidate_cap]
    return RetrievalResult(
        candidates=capped,
        total_before_cap=total_before_cap,
        candidate_cap=candidate_cap,
    )

