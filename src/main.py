"""Phase 0 runnable skeleton and diagnostics entrypoint."""

from __future__ import annotations

import argparse
import json

from phases.phase0 import cmd_doctor, cmd_info
from phases.phase1.ingestion import load_restaurants
from phases.phase2.preferences import PreferenceValidationError, preferences_from_mapping
from phases.phase3.retrieval import build_prompt_payload, retrieve_candidates
from phases.phase4.recommendation import recommend_with_fallback


def cmd_phase1_ingest_smoke(source: str, limit: int, split: str) -> int:
    try:
        restaurants = load_restaurants(source=source, limit=limit, split=split)
    except Exception as exc:
        print(f"Phase 1 ingest-smoke failed: {exc}")
        return 1

    print(f"Phase 1 ingest-smoke :: source={source}, split={split}, count={len(restaurants)}")
    for item in restaurants[:5]:
        print(
            f"- {item.name} | {item.location} | rating={item.rating} | "
            f"cost_band={item.cost_band} | cuisines={', '.join(item.cuisines)}"
        )
    return 0


def _allowed_cities_from_restaurants(source: str, split: str, limit: int) -> set[str]:
    restaurants = load_restaurants(source=source, split=split, limit=limit)
    return {item.location.lower() for item in restaurants}


def cmd_phase2_prefs_parse(
    *,
    location: str,
    budget: str,
    cuisines: str,
    minimum_rating: str,
    additional_preferences: str | None,
    validate_city: bool,
    city_source: str,
    city_split: str,
    city_limit: int,
) -> int:
    allowed_cities = None
    if validate_city:
        try:
            allowed_cities = _allowed_cities_from_restaurants(
                source=city_source, split=city_split, limit=city_limit
            )
        except Exception as exc:
            print(f"Phase 2 city-validation bootstrap failed: {exc}")
            return 1

    payload = {
        "location": location,
        "budget": budget,
        "cuisines": cuisines,
        "minimum_rating": minimum_rating,
        "additional_preferences": additional_preferences,
    }
    try:
        prefs = preferences_from_mapping(payload, allowed_cities=allowed_cities)
    except PreferenceValidationError as exc:
        print("Phase 2 preference validation failed:")
        for err in exc.errors:
            print(f"- {err}")
        return 1

    print("Phase 2 preference validation passed.")
    print(json.dumps(prefs.to_dict(), indent=2))
    return 0


def cmd_phase3_retrieve_smoke(
    *,
    location: str,
    budget: str,
    cuisines: str,
    minimum_rating: str,
    additional_preferences: str | None,
    source: str,
    split: str,
    data_limit: int,
    candidate_cap: int,
    top_k: int,
) -> int:
    payload = {
        "location": location,
        "budget": budget,
        "cuisines": cuisines,
        "minimum_rating": minimum_rating,
        "additional_preferences": additional_preferences,
    }
    try:
        prefs = preferences_from_mapping(payload)
    except PreferenceValidationError as exc:
        print("Phase 3 failed at preference validation:")
        for err in exc.errors:
            print(f"- {err}")
        return 1

    try:
        restaurants = load_restaurants(source=source, split=split, limit=data_limit)
    except Exception as exc:
        print(f"Phase 3 data load failed: {exc}")
        return 1

    result = retrieve_candidates(restaurants, prefs, candidate_cap=candidate_cap)
    prompt_payload = build_prompt_payload(prefs, result.candidates, top_k=top_k)

    print(
        f"Phase 3 retrieval :: input_rows={len(restaurants)} "
        f"matched={result.total_before_cap} returned={len(result.candidates)} "
        f"cap={result.candidate_cap}"
    )
    if not result.candidates:
        print("No candidates found for current constraints.")
    else:
        for item in result.candidates[:5]:
            print(
                f"- {item.name} | {item.location} | rating={item.rating} | "
                f"cost_band={item.cost_band} | cuisines={', '.join(item.cuisines)}"
            )

    print("Prompt payload preview:")
    print(json.dumps(prompt_payload, indent=2))
    return 0


def cmd_phase4_recommend_smoke(
    *,
    location: str,
    budget: str,
    cuisines: str,
    minimum_rating: str,
    additional_preferences: str | None,
    source: str,
    split: str,
    data_limit: int,
    candidate_cap: int,
    top_k: int,
    llm_model: str | None,
) -> int:
    payload = {
        "location": location,
        "budget": budget,
        "cuisines": cuisines,
        "minimum_rating": minimum_rating,
        "additional_preferences": additional_preferences,
    }
    try:
        prefs = preferences_from_mapping(payload)
    except PreferenceValidationError as exc:
        print("Phase 4 failed at preference validation:")
        for err in exc.errors:
            print(f"- {err}")
        return 1

    try:
        restaurants = load_restaurants(source=source, split=split, limit=data_limit)
    except Exception as exc:
        print(f"Phase 4 data load failed: {exc}")
        return 1

    retrieval = retrieve_candidates(restaurants, prefs, candidate_cap=candidate_cap)
    prompt_payload = build_prompt_payload(prefs, retrieval.candidates, top_k=top_k)
    result = recommend_with_fallback(
        prompt_payload=prompt_payload,
        candidates=retrieval.candidates,
        top_k=top_k,
        model=llm_model,
    )

    print(
        f"Phase 4 recommendation :: input_rows={len(restaurants)} "
        f"matched={retrieval.total_before_cap} returned={len(retrieval.candidates)} "
        f"fallback={result.used_fallback}"
    )
    if result.failure_reason:
        print(f"Failure reason: {result.failure_reason}")
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project utility commands")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("info", help="Show project phase information")
    subparsers.add_parser("doctor", help="Run phase-0 setup checks")
    ingest_parser = subparsers.add_parser(
        "phase1-ingest-smoke", help="Run phase-1 ingestion smoke check"
    )
    ingest_parser.add_argument("--source", choices=["sample", "hf"], default="sample")
    ingest_parser.add_argument("--split", default="train")
    ingest_parser.add_argument("--limit", type=int, default=10)

    prefs_parser = subparsers.add_parser(
        "phase2-prefs-parse", help="Validate and parse phase-2 user preferences"
    )
    prefs_parser.add_argument("--location", required=True)
    prefs_parser.add_argument("--budget", required=True, choices=["low", "medium", "high"])
    prefs_parser.add_argument("--cuisines", required=True)
    prefs_parser.add_argument("--minimum-rating", required=True, dest="minimum_rating")
    prefs_parser.add_argument("--additional-preferences", default=None, dest="additional_preferences")
    prefs_parser.add_argument("--validate-city", action="store_true")
    prefs_parser.add_argument("--city-source", default="sample", choices=["sample", "hf"])
    prefs_parser.add_argument("--city-split", default="train")
    prefs_parser.add_argument("--city-limit", type=int, default=2000)

    retrieve_parser = subparsers.add_parser(
        "phase3-retrieve-smoke", help="Run phase-3 retrieval and prompt assembly smoke check"
    )
    retrieve_parser.add_argument("--location", required=True)
    retrieve_parser.add_argument("--budget", required=True, choices=["low", "medium", "high"])
    retrieve_parser.add_argument("--cuisines", required=True)
    retrieve_parser.add_argument("--minimum-rating", required=True, dest="minimum_rating")
    retrieve_parser.add_argument("--additional-preferences", default=None, dest="additional_preferences")
    retrieve_parser.add_argument("--source", default="sample", choices=["sample", "hf"])
    retrieve_parser.add_argument("--split", default="train")
    retrieve_parser.add_argument("--data-limit", type=int, default=500, dest="data_limit")
    retrieve_parser.add_argument("--candidate-cap", type=int, default=20, dest="candidate_cap")
    retrieve_parser.add_argument("--top-k", type=int, default=5, dest="top_k")

    phase4_parser = subparsers.add_parser(
        "phase4-recommend-smoke", help="Run phase-4 LLM recommendation with Groq and fallback"
    )
    phase4_parser.add_argument("--location", required=True)
    phase4_parser.add_argument("--budget", required=True, choices=["low", "medium", "high"])
    phase4_parser.add_argument("--cuisines", required=True)
    phase4_parser.add_argument("--minimum-rating", required=True, dest="minimum_rating")
    phase4_parser.add_argument("--additional-preferences", default=None, dest="additional_preferences")
    phase4_parser.add_argument("--source", default="sample", choices=["sample", "hf"])
    phase4_parser.add_argument("--split", default="train")
    phase4_parser.add_argument("--data-limit", type=int, default=500, dest="data_limit")
    phase4_parser.add_argument("--candidate-cap", type=int, default=20, dest="candidate_cap")
    phase4_parser.add_argument("--top-k", type=int, default=5, dest="top_k")
    phase4_parser.add_argument("--llm-model", default=None, dest="llm_model")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "info":
        return cmd_info()
    if args.command == "doctor":
        return cmd_doctor()
    if args.command == "phase1-ingest-smoke":
        return cmd_phase1_ingest_smoke(source=args.source, limit=args.limit, split=args.split)
    if args.command == "phase2-prefs-parse":
        return cmd_phase2_prefs_parse(
            location=args.location,
            budget=args.budget,
            cuisines=args.cuisines,
            minimum_rating=args.minimum_rating,
            additional_preferences=args.additional_preferences,
            validate_city=args.validate_city,
            city_source=args.city_source,
            city_split=args.city_split,
            city_limit=args.city_limit,
        )
    if args.command == "phase3-retrieve-smoke":
        return cmd_phase3_retrieve_smoke(
            location=args.location,
            budget=args.budget,
            cuisines=args.cuisines,
            minimum_rating=args.minimum_rating,
            additional_preferences=args.additional_preferences,
            source=args.source,
            split=args.split,
            data_limit=args.data_limit,
            candidate_cap=args.candidate_cap,
            top_k=args.top_k,
        )
    if args.command == "phase4-recommend-smoke":
        return cmd_phase4_recommend_smoke(
            location=args.location,
            budget=args.budget,
            cuisines=args.cuisines,
            minimum_rating=args.minimum_rating,
            additional_preferences=args.additional_preferences,
            source=args.source,
            split=args.split,
            data_limit=args.data_limit,
            candidate_cap=args.candidate_cap,
            top_k=args.top_k,
            llm_model=args.llm_model,
        )

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

