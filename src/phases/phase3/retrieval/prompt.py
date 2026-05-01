from __future__ import annotations

from phases.phase1.ingestion.model import Restaurant
from phases.phase2.preferences.model import UserPreferences


def _candidate_row(candidate: Restaurant) -> dict[str, object]:
    return {
        "id": candidate.id,
        "name": candidate.name,
        "location": candidate.location,
        "cuisines": candidate.cuisines,
        "rating": candidate.rating,
        "rating_votes": candidate.rating_votes,
        "cost_for_two": candidate.cost_for_two,
        "cost_band": candidate.cost_band,
    }


def build_prompt_payload(
    prefs: UserPreferences,
    candidates: list[Restaurant],
    *,
    top_k: int = 5,
) -> dict[str, object]:
    return {
        "system_instruction": (
            "Recommend restaurants using ONLY the provided candidates. "
            "Do not invent restaurants. Prefer better match quality and explain each choice briefly."
        ),
        "output_contract": {
            "format": "json",
            "schema": {
                "recommendations": [
                    {
                        "restaurant_id": "string",
                        "rank": "integer",
                        "explanation": "string",
                    }
                ],
                "summary": "string",
            },
            "max_recommendations": top_k,
        },
        "user_preferences": prefs.to_dict(),
        "candidates": [_candidate_row(item) for item in candidates],
    }

