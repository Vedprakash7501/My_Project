"""Phase 2 preferences package."""

from .model import UserPreferences
from .parse import preferences_from_mapping
from .validate import PreferenceValidationError

__all__ = ["UserPreferences", "PreferenceValidationError", "preferences_from_mapping"]

