"""
Django Chained Select - Backward Compatibility Layer

DEPRECATED: This module is deprecated and will be removed in a future version.
Please update your imports to use the widgets app:

    # Old (deprecated):
    from chained_select import ChainedChoiceField, ChainedSelectMixin

    # New:
    from widgets import ChainedChoiceField, ChainedSelectMixin

All functionality has been migrated to the widgets app for better organization.
"""

import warnings

# Re-export everything from widgets for backward compatibility
from widgets import (
    ChainedChoiceField,
    ChainedModelChoiceField,
    ChainedSelect,
    ChainedSelectAjaxView,
    ChainedSelectMixin,
    ChainedSelectMultiple,
    make_ajax_view,
)

# Emit deprecation warning on import
warnings.warn(
    "The 'chained_select' module is deprecated. "
    "Please update your imports to use 'widgets' instead. "
    "Example: from widgets import ChainedChoiceField, ChainedSelectMixin",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = [
    "ChainedSelect",
    "ChainedSelectMultiple",
    "ChainedChoiceField",
    "ChainedModelChoiceField",
    "ChainedSelectMixin",
    "ChainedSelectAjaxView",
    "make_ajax_view",
]

__version__ = "1.0.0"
