from __future__ import annotations

import json
from dataclasses import dataclass

from phases.phase1.ingestion.model import Restaurant


@dataclass(frozen=True, slots=True)
class RankedRecommendation:
    restaurant_id: str
    rank: int
    explanation: str


def _strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.startswith("json"):
            stripped = stripped[4:].strip()
    return stripped


def parse_llm_recommendations(
    content: str,
    candidates: list[Restaurant],
    *,
    top_k: int,
) -> tuple[list[RankedRecommendation], str]:
    candidate_ids = {item.id for item in candidates}
    cleaned = _strip_code_fences(content)
    parsed = json.loads(cleaned)
    recommendations = parsed.get("recommendations", [])
    summary = str(parsed.get("summary", "")).strip()

    if not isinstance(recommendations, list):
        raise ValueError("recommendations must be a list")

    ranked: list[RankedRecommendation] = []
    for row in recommendations:
        if not isinstance(row, dict):
            continue
        rid = str(row.get("restaurant_id", "")).strip()
        explanation = str(row.get("explanation", "")).strip()
        rank_value = row.get("rank", 0)
        try:
            rank_int = int(rank_value)
        except (TypeError, ValueError):
            continue

        if rid not in candidate_ids:
            continue
        if rank_int < 1:
            continue
        if not explanation:
            continue
        ranked.append(
            RankedRecommendation(restaurant_id=rid, rank=rank_int, explanation=explanation)
        )

    ranked.sort(key=lambda item: item.rank)
    return ranked[:top_k], summary

