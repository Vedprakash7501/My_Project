# Dataset Contract (v1)

## Source
- **Provider:** Hugging Face
- **Dataset:** `ManikaSaini/zomato-restaurant-recommendation`
- **Usage mode:** offline-friendly local load/cache after fetch

## Contract Purpose
Define the minimum fields and normalization behavior required by this project so downstream phases can rely on stable internal data.

## Canonical Restaurant Model (v1)

| Internal Field | Type | Required | Description |
|---|---|---|---|
| `id` | `str` | Yes | Stable row identifier (derived if not present in source) |
| `name` | `str` | Yes | Restaurant display name |
| `location` | `str` | Yes | City/locality text used for filtering |
| `cuisines` | `list[str]` | Yes | Normalized cuisine tokens |
| `cost_for_two` | `float \| None` | No | Parsed estimated cost for two, if available |
| `cost_band` | `str` | Yes | Derived bucket: `low`, `medium`, `high`, `unknown` |
| `rating` | `float \| None` | No | Numeric rating in 0-5 range when parseable |
| `rating_votes` | `int \| None` | No | Number of votes/reviews if present |
| `source_row_hash` | `str` | Yes | Hash for traceability/dedup |

## Normalization Rules (v1)
- Trim and normalize whitespace for text fields
- Parse rating strings into float where possible; otherwise set `None`
- Parse cost values to numeric where possible; derive `cost_band`
- Split cuisines into list by delimiters (comma/slash), lowercase and trim
- Drop rows missing required fields (`name`, `location`, `cuisines`) after normalization

## Validation Rules
- `rating` must be within `[0.0, 5.0]` when present
- `cost_band` must be one of `low`, `medium`, `high`, `unknown`
- `cuisines` must contain at least one non-empty token

## Schema Drift Policy
- Use an explicit allowlist for consumed source columns
- Fail loudly if required source columns are missing
- Ignore unknown source columns by default
- Review this file when source schema changes

## Consumer Guarantees for Downstream Phases
- Phase 2+ can assume `Restaurant` records meet this schema
- Missing optional data is represented as `None`/`unknown`, not invalid strings
- Deterministic filtering can run without additional parsing

