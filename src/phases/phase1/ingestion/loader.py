from __future__ import annotations

from typing import Any, Iterable

from .model import Restaurant
from .normalize import normalize_row
from .sample_data import SAMPLE_ROWS


HF_DATASET = "ManikaSaini/zomato-restaurant-recommendation"


def _iter_hf_rows(split: str = "train", limit: int | None = None) -> Iterable[dict[str, Any]]:
    try:
        from datasets import load_dataset  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Missing optional dependency 'datasets'. Install with: pip install datasets"
        ) from exc

    dataset = load_dataset(HF_DATASET, split=split)
    for idx, row in enumerate(dataset):
        if limit is not None and idx >= limit:
            break
        yield dict(row)


def iter_restaurants(
    *,
    source: str = "sample",
    split: str = "train",
    limit: int | None = None,
) -> Iterable[Restaurant]:
    """Yield normalized restaurants from source rows.

    source:
      - "sample": use packaged fallback rows
      - "hf": load from Hugging Face dataset
    """

    if source not in {"sample", "hf"}:
        raise ValueError("source must be 'sample' or 'hf'")

    rows: Iterable[dict[str, Any]]
    if source == "sample":
        rows = SAMPLE_ROWS if limit is None else SAMPLE_ROWS[:limit]
    else:
        rows = _iter_hf_rows(split=split, limit=limit)

    for idx, row in enumerate(rows):
        normalized = normalize_row(row, row_index=idx)
        if normalized is not None:
            yield normalized


def load_restaurants(
    *,
    source: str = "sample",
    split: str = "train",
    limit: int | None = None,
) -> list[Restaurant]:
    return list(iter_restaurants(source=source, split=split, limit=limit))

