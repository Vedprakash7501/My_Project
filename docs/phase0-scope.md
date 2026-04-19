# Phase 0 Scope and Foundations

## Goal
Lock project boundaries, choose initial stack, define configuration expectations, and provide a runnable skeleton for local development.

## Product Slice (Milestone 0)
- Primary interaction mode for later phases: **Web UI**
- Development and diagnostics support: **CLI**
- Current phase output: setup and structure only (no recommendation logic yet)

## Stack Decisions (v1)
- **Language:** Python 3.11+
- **Project layout:** modular packages under `src/`
- **Configuration:** environment variables via `.env` (template in `.env.example`)
- **Dataset source:** Hugging Face dataset `ManikaSaini/zomato-restaurant-recommendation`

## Supported Preference Fields (Planned for v1)
- `location` (city-level)
- `budget` (`low`, `medium`, `high`)
- `cuisines` (one or more)
- `minimum_rating` (float, expected range `0-5`)
- `additional_preferences` (optional text)

## Non-Goals (Phase 0 and Early v1)
- User authentication and profile history
- Real-time partner APIs (live Zomato integrations)
- Map integration and geo-distance ranking
- Payments, ordering, booking flows
- Multi-tenant or enterprise deployment concerns

## Success Criteria for Phase 0
- Scope, assumptions, and non-goals are documented
- Dataset contract exists and is versioned in docs
- Environment template is present
- Repository has a local runnable skeleton command

## Risks Identified Early
- Dataset schema drift over time
- Missing or invalid API key configuration
- Scope creep before core recommendation flow is stable

## Next Phase Entry Criteria
Phase 1 can begin once:
1. Phase 0 docs are approved
2. Skeleton run command works locally
3. Dataset contract fields are accepted

