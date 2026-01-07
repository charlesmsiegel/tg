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

Create or Select Usage:
    from django import forms
    from widgets import CreateOrSelectField, CreateOrSelectMixin

    class EffectCreateOrSelectForm(CreateOrSelectMixin, forms.ModelForm):
        create_or_select_config = {
            'toggle_field': 'select_or_create',
            'select_field': 'select',
        }

        select_or_create = CreateOrSelectField(label="Create new?")
        select = forms.ModelChoiceField(queryset=Effect.objects.all(), required=False)

        class Meta:
            model = Effect
            fields = ['name', 'description', ...]

Template:
    {{ form.select_or_create }}
    <div data-create-or-select-container="{{ form.select_or_create.name }}"
         data-create-or-select-mode="select">
        {{ form.select }}
    </div>
    <div data-create-or-select-container="{{ form.select_or_create.name }}"
         data-create-or-select-mode="create" class="d-none">
        <!-- creation fields -->
    </div>

JavaScript is auto-injected. No {{ form.media }} needed!
"""

# Chained Select exports (primary widget functionality)
from .fields.chained import ChainedChoiceField, ChainedModelChoiceField
from .fields.create_or_select import CreateOrSelectField, CreateOrSelectModelChoiceField
from .mixins.chained import ChainedSelectMixin
from .mixins.conditional import ConditionalFieldsMixin
from .mixins.create_or_select import CreateOrSelectMixin
from .views import ChainedSelectAjaxView, auto_chained_ajax_view, make_ajax_view
from .widgets.chained import ChainedSelect, ChainedSelectMultiple
from .widgets.create_or_select import CreateOrSelectWidget

# FilterableList exports
from .widgets.filterable import get_filterable_list_js, render_filterable_list_script
from .widgets.metadata_select import OptionMetadataSelect, OptionMetadataSelectMultiple

__all__ = [
    # Widgets
    "ChainedSelect",
    "ChainedSelectMultiple",
    "CreateOrSelectWidget",
    "OptionMetadataSelect",
    "OptionMetadataSelectMultiple",
    # Fields
    "ChainedChoiceField",
    "ChainedModelChoiceField",
    "CreateOrSelectField",
    "CreateOrSelectModelChoiceField",
    # Mixins
    "ChainedSelectMixin",
    "ConditionalFieldsMixin",
    "CreateOrSelectMixin",
    # Views
    "ChainedSelectAjaxView",
    "auto_chained_ajax_view",
    "make_ajax_view",
    # FilterableList
    "get_filterable_list_js",
    "render_filterable_list_script",
]

__version__ = "1.0.0"
