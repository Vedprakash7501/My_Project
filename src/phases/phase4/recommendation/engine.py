from __future__ import annotations

from dataclasses import asdict, dataclass

from phases.phase1.ingestion.model import Restaurant

from .groq_client import GroqClientError, call_groq_chat_completion
from .parser import RankedRecommendation, parse_llm_recommendations


@dataclass(frozen=True, slots=True)
class RecommendationResult:
    recommendations: list[RankedRecommendation]
    summary: str
    used_fallback: bool
    failure_reason: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "recommendations": [asdict(item) for item in self.recommendations],
            "summary": self.summary,
            "used_fallback": self.used_fallback,
            "failure_reason": self.failure_reason,
        }


def _fallback_recommendations(
    candidates: list[Restaurant],
    *,
    top_k: int,
) -> list[RankedRecommendation]:
    rows: list[RankedRecommendation] = []
    for idx, item in enumerate(candidates[:top_k], start=1):
        explanation = (
            f"{item.name} matches key filters for location, budget, and cuisine "
            f"with rating {item.rating if item.rating is not None else 'N/A'}."
        )
        rows.append(
            RankedRecommendation(
                restaurant_id=item.id,
                rank=idx,
                explanation=explanation,
            )
        )
    return rows


def recommend_with_fallback(
    *,
    prompt_payload: dict[str, object],
    candidates: list[Restaurant],
    top_k: int = 5,
    max_retries: int = 2,
    model: str | None = None,
) -> RecommendationResult:
    if not candidates:
        return RecommendationResult(
            recommendations=[],
            summary="No matching restaurants found for the provided preferences.",
            used_fallback=True,
            failure_reason="no_candidates",
        )

    last_error: str | None = None
    for _attempt in range(max_retries + 1):
        try:
            content = call_groq_chat_completion(
                prompt_payload=prompt_payload,
                model=model,
            )
            ranked, summary = parse_llm_recommendations(content, candidates, top_k=top_k)
            if ranked:
                return RecommendationResult(
                    recommendations=ranked,
                    summary=summary or "Top recommendations generated successfully.",
                    used_fallback=False,
                )
            last_error = "empty_or_invalid_llm_output"
        except (GroqClientError, ValueError) as exc:
            last_error = str(exc)

    fallback = _fallback_recommendations(candidates, top_k=top_k)
    return RecommendationResult(
        recommendations=fallback,
        summary="Returned deterministic fallback recommendations due to LLM failure.",
        used_fallback=True,
        failure_reason=last_error or "unknown_llm_failure",
    )

