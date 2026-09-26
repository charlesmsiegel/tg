"""
Conditional Fields Mixin

Provides declarative visibility rules for form fields based on other field
values or option metadata. Automatically generates JavaScript to show/hide
fields without requiring template authors to write any JavaScript.

Usage:
    class FreebiesForm(ConditionalFieldsMixin, ChainedSelectMixin, forms.Form):
        category = ChainedChoiceField(choices=[...])
        example = ChainedChoiceField(parent_field='category', choices_map={...})
        value = forms.ChoiceField(required=False)
        note = forms.CharField(required=False)
        pooled = forms.BooleanField(required=False)

        # Declarative visibility rules
        conditional_fields = {
            # Show 'example' field when category is NOT in these values
            'example': {
                'hidden_when': {'category': {'value_in': ['-----', 'Willpower']}},
            },
            # Show 'value' field only when category is 'MeritFlaw'
            'value': {
                'visible_when': {'category': {'value_is': 'MeritFlaw'}},
            },
            # Show 'note' field when category is 'Background'
            'note': {
                'visible_when': {'category': {'value_is': 'Background'}},
            },
            # Show 'pooled' based on metadata AND a context variable
            'pooled': {
                'visible_when': {
                    'category': {'value_is': 'Background'},
                    'example': {'metadata_is': {'poolable': 'true'}},
                    '_context': {'is_group_member': True},
                },
            },
        }

Template (wrap each conditional field in a container whose id is
"<field>_wrap"; add "d-none" when the field starts hidden):
    <div class="row">
        {{ form.category }}
        <div class="col-sm d-none" id="example_wrap">{{ form.example }}</div>
        <div class="col-sm d-none" id="value_wrap">{{ form.value }}</div>
        <div class="col-sm d-none" id="note_wrap">{{ form.note }}</div>
        <div class="col-sm d-none" id="pooled_wrap">Pooled? {{ form.pooled }}</div>
    </div>
    {{ form.conditional_js }}
"""

from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from widgets.utils import config_script


class ConditionalFieldsMixin:
    """
    Mixin for forms with conditional field visibility.

    Define `conditional_fields` as a class attribute with rules for
    when fields should be shown or hidden. The mixin generates JavaScript
    that handles visibility changes automatically.

    Rule format:
        conditional_fields = {
            'field_name': {
                'wrapper_id': 'custom-id',               # Custom element ID (default: {field}_wrap)
                'visible_when': {
                    'source_field': {
                        'value_is': 'specific_value',     # Exact match
                        'value_in': ['val1', 'val2'],     # In list
                        'value_not_in': ['val1'],         # Not in list
                        'checked_is': True,               # Checkbox checked state
                        'metadata_is': {'key': 'value'},  # Metadata exact match
                        'metadata_truthy': 'key',         # Metadata is truthy
                    },
                    '_context': {'var': True},            # Context variable
                },
                'hidden_when': { ... },  # Same format, field hidden if any match
                'initially_hidden': True,  # Start hidden (default: True)
            },
        }
    """

    conditional_fields = {}
    conditional_context = {}  # Override in __init__ or set on form

    def __init__(self, *args, **kwargs):
        # Allow passing context via kwargs
        context = kwargs.pop("conditional_context", None)
        super().__init__(*args, **kwargs)

        if context:
            self.conditional_context = context

    def get_conditional_context(self):
        """
        Override to provide dynamic context variables.

        Returns dict of context variables available in visibility rules.
        Example: {'is_group_member': self.instance.is_group_member}
        """
        return dict(self.conditional_context)

    def get_conditional_rules(self):
        """
        Override to provide dynamic rules.

        Returns dict of field visibility rules.
        """
        return dict(self.conditional_fields)

    @property
    def media(self):
        return super().media + forms.Media(js=("widgets/conditional.js",))

    def conditional_js(self):
        """Render inert visibility rules; behavior is supplied by form.media."""
        rules = self.get_conditional_rules()
        if not rules:
            return ""
        return config_script(
            {"rules": rules, "context": self.get_conditional_context()},
            **{"data-conditional-rules": ""},
        )

    def wrap_field(self, field_name, label_prefix=""):
        """
        Wrap a field in a conditional visibility container.

        Usage in template: {{ form.wrap_field('pooled', 'Pooled?') }}
        """
        if field_name not in self.fields:
            return ""

        field = self[field_name]
        rules = self.get_conditional_rules()
        field_rules = rules.get(field_name, {})

        # Determine initial visibility
        initially_hidden = field_rules.get("initially_hidden", True)
        hidden_class = " d-none" if initially_hidden else ""

        wrapper_id = f"{field_name}_wrap"

        if label_prefix:
            content = f"{label_prefix} {field}"
        else:
            content = str(field)

        return format_html(
            '<div id="{}" class="col-sm{}">{}</div>', wrapper_id, hidden_class, mark_safe(content)
        )
