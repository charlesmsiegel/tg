"""
Django Widgets App - Reusable Form Components

A centralized app for form widgets, fields, and mixins.
Consolidates reusable form components from across the codebase.

Chained Select Usage:
    from django import forms
    from widgets import ChainedChoiceField, ChainedSelectMixin

    class MyForm(ChainedSelectMixin, forms.Form):
        parent = ChainedChoiceField(choices=[('a', 'A'), ('b', 'B')])
        child = ChainedChoiceField(
            parent_field='parent',
            choices_map={'a': [('a1', 'A1')], 'b': [('b1', 'B1')]}
        )

Template:
    {{ form.as_p }}

That's it!
"""

# Chained Select exports (primary widget functionality)
from .fields.chained import ChainedChoiceField, ChainedModelChoiceField
from .mixins.chained import ChainedSelectMixin
from .views import ChainedSelectAjaxView, auto_chained_ajax_view, make_ajax_view
from .widgets.chained import ChainedSelect, ChainedSelectMultiple

__all__ = [
    # Widgets
    "ChainedSelect",
    "ChainedSelectMultiple",
    # Fields
    "ChainedChoiceField",
    "ChainedModelChoiceField",
    # Mixins
    "ChainedSelectMixin",
    # Views
    "ChainedSelectAjaxView",
    "auto_chained_ajax_view",
    "make_ajax_view",
]

__version__ = "1.0.0"
