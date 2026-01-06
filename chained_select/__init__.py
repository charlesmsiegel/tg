"""
Django Chained Select - Self-Contained Cascading Dropdowns

Works like native Django form fields. Just render the field in your template.
No {{ form.media }}, no URL configuration, no JavaScript setup.

Example:
    from django import forms
    from chained_select import ChainedChoiceField, ChainedSelectMixin

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

from .fields import ChainedChoiceField, ChainedModelChoiceField, ChainedSelectMixin
from .views import ChainedSelectAjaxView, make_ajax_view
from .widgets import ChainedSelect, ChainedSelectMultiple

# Auto-register URL via AppConfig
default_app_config = "chained_select.apps.ChainedSelectConfig"

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
