from __future__ import annotations

import hashlib
import re
from typing import Any

from .model import Restaurant


UNKNOWN_COST_BAND = "unknown"
VALID_COST_BANDS = {"low", "medium", "high", UNKNOWN_COST_BAND}


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()


def _extract_float(value: Any) -> float | None:
    text = _clean_text(value).lower()
    if not text:
        return None
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return None
    return float(match.group(0))


def _extract_int(value: Any) -> int | None:
    text = _clean_text(value).replace(",", "")
    if not text:
        return None
    match = re.search(r"\d+", text)
    if not match:
        return None
    return int(match.group(0))


def _normalize_cuisines(value: Any) -> list[str]:
    text = _clean_text(value).lower()
    if not text:
        return []
    tokens = re.split(r"[,/|]", text)
    cleaned = [re.sub(r"\s+", " ", token).strip() for token in tokens]
    deduped: list[str] = []
    for token in cleaned:
        if token and token not in deduped:
            deduped.append(token)
    return deduped


def _derive_cost_band(cost_for_two: float | None) -> str:
    if cost_for_two is None:
        return UNKNOWN_COST_BAND
    if cost_for_two <= 500:
        return "low"
    if cost_for_two <= 1500:
        return "medium"
    return "high"


def _derive_id(name: str, location: str, row_hash: str, row_index: int) -> str:
    base = f"{name}|{location}|{row_hash}|{row_index}"
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
    return f"r_{digest}"


def _source_row_hash(row: dict[str, Any]) -> str:
    payload = "|".join(f"{key}={_clean_text(row.get(key))}" for key in sorted(row))
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def normalize_row(row: dict[str, Any], row_index: int = 0) -> Restaurant | None:
    """Convert one source row into a canonical Restaurant object.

    Returns None when required fields are missing.
    """

    name = _clean_text(row.get("Restaurant Name") or row.get("name"))
    location = _clean_text(row.get("City") or row.get("Location") or row.get("location"))
    cuisines = _normalize_cuisines(row.get("Cuisines") or row.get("cuisines"))

    if not name or not location or not cuisines:
        return None

    rating = _extract_float(row.get("Aggregate rating") or row.get("rating"))
    if rating is not None and not (0.0 <= rating <= 5.0):
        rating = None

    cost_for_two = _extract_float(
        row.get("Average Cost for two")
        or row.get("Cost for two")
        or row.get("cost_for_two")
    )
    cost_band = _derive_cost_band(cost_for_two)
    if cost_band not in VALID_COST_BANDS:
        cost_band = UNKNOWN_COST_BAND

    rating_votes = _extract_int(row.get("Votes") or row.get("rating_votes"))
    row_hash = _source_row_hash(row)
    identifier = _clean_text(row.get("id")) or _derive_id(name, location, row_hash, row_index)

    return Restaurant(
        id=identifier,
        name=name,
        location=location,
        cuisines=cuisines,
        cost_for_two=cost_for_two,
        cost_band=cost_band,
        rating=rating,
        rating_votes=rating_votes,
        source_row_hash=row_hash,
    )

