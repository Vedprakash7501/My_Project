"""Phase 1 ingestion package.

This package provides:
- Canonical `Restaurant` model
- Row normalization/parsing
- Dataset loading helpers
"""

from .loader import iter_restaurants, load_restaurants
from .model import Restaurant

__all__ = ["Restaurant", "iter_restaurants", "load_restaurants"]

