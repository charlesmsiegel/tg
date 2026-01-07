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

Template:
    <div class="row">
        {{ form.category }}
        {{ form.example|conditional_wrap }}
        {{ form.value|conditional_wrap }}
        {{ form.note|conditional_wrap }}
        {{ form.pooled|conditional_wrap:"Pooled?" }}
    </div>
    {{ form.conditional_js }}
"""

import json

from django.utils.html import format_html
from django.utils.safestring import mark_safe

# JavaScript for conditional field visibility
CONDITIONAL_FIELDS_JS = """
(function() {
    'use strict';

    if (window.ConditionalFields) return;

    class ConditionalFieldsManager {
        constructor() {
            this.rules = {};
            this.context = {};
            this.initialized = false;
        }

        init() {
            if (this.initialized) return;
            this.initialized = true;

            // Find and parse embedded rules
            document.querySelectorAll('script[data-conditional-rules]').forEach(script => {
                try {
                    const data = JSON.parse(script.textContent);
                    Object.assign(this.rules, data.rules || {});
                    Object.assign(this.context, data.context || {});
                } catch (e) {
                    console.error('ConditionalFields: Failed to parse rules:', e);
                }
            });

            // Set up event listeners
            this.setupListeners();

            // Apply initial visibility
            this.applyAllRules();
        }

        setupListeners() {
            // Listen to all form controls that have rules depending on them
            const watchedFields = new Set();
            for (const [targetField, config] of Object.entries(this.rules)) {
                for (const condition of ['visible_when', 'hidden_when']) {
                    if (config[condition]) {
                        for (const sourceField of Object.keys(config[condition])) {
                            if (!sourceField.startsWith('_')) {
                                watchedFields.add(sourceField);
                            }
                        }
                    }
                }
            }

            watchedFields.forEach(fieldName => {
                const field = document.getElementById('id_' + fieldName);
                if (field) {
                    field.addEventListener('change', () => this.applyAllRules());
                    // Also listen for metadata:change events
                    field.addEventListener('metadata:change', () => this.applyAllRules());
                }
            });
        }

        applyAllRules() {
            for (const [targetField, config] of Object.entries(this.rules)) {
                this.applyRule(targetField, config);
            }
        }

        applyRule(targetField, config) {
            const wrapper = document.getElementById(targetField + '_wrap');
            if (!wrapper) return;

            let visible = true;

            // Check visible_when conditions (all must be true)
            if (config.visible_when) {
                visible = this.checkConditions(config.visible_when, true);
            }

            // Check hidden_when conditions (if any is true, hide)
            if (config.hidden_when && visible) {
                visible = !this.checkConditions(config.hidden_when, false);
            }

            if (visible) {
                wrapper.classList.remove('d-none');
            } else {
                wrapper.classList.add('d-none');
            }
        }

        checkConditions(conditions, requireAll) {
            const results = [];

            for (const [sourceField, checks] of Object.entries(conditions)) {
                if (sourceField === '_context') {
                    // Check context variables
                    for (const [contextVar, expectedValue] of Object.entries(checks)) {
                        results.push(this.context[contextVar] === expectedValue);
                    }
                    continue;
                }

                const field = document.getElementById('id_' + sourceField);
                if (!field) {
                    results.push(false);
                    continue;
                }

                const value = field.value;

                // Check value_is
                if (checks.value_is !== undefined) {
                    results.push(value === checks.value_is);
                }

                // Check value_in
                if (checks.value_in !== undefined) {
                    results.push(checks.value_in.includes(value));
                }

                // Check value_not_in
                if (checks.value_not_in !== undefined) {
                    results.push(!checks.value_not_in.includes(value));
                }

                // Check metadata_is
                if (checks.metadata_is !== undefined) {
                    const metadata = this.getMetadata(field);
                    for (const [key, expected] of Object.entries(checks.metadata_is)) {
                        results.push(metadata[key] === expected);
                    }
                }

                // Check metadata_truthy
                if (checks.metadata_truthy !== undefined) {
                    const metadata = this.getMetadata(field);
                    const val = metadata[checks.metadata_truthy];
                    results.push(val === 'true' || val === 'True' || val === true);
                }
            }

            if (results.length === 0) return true;

            if (requireAll) {
                return results.every(r => r);
            } else {
                return results.some(r => r);
            }
        }

        getMetadata(field) {
            if (window.OptionMetadata) {
                return window.OptionMetadata.get(field);
            }
            // Fallback: read from selected option directly
            if (field.selectedOptions && field.selectedOptions.length > 0) {
                const option = field.selectedOptions[0];
                const metadata = {};
                for (const key in option.dataset) {
                    metadata[key] = option.dataset[key];
                }
                return metadata;
            }
            return {};
        }
    }

    window.ConditionalFields = new ConditionalFieldsManager();

    const init = () => window.ConditionalFields.init();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-init for htmx/Turbo
    document.addEventListener('htmx:afterSwap', init);
    document.addEventListener('turbo:render', init);
    document.addEventListener('turbo:frame-load', init);
})();
"""


class ConditionalFieldsMixin:
    """
    Mixin for forms with conditional field visibility.

    Define `conditional_fields` as a class attribute with rules for
    when fields should be shown or hidden. The mixin generates JavaScript
    that handles visibility changes automatically.

    Rule format:
        conditional_fields = {
            'field_name': {
                'visible_when': {
                    'source_field': {
                        'value_is': 'specific_value',     # Exact match
                        'value_in': ['val1', 'val2'],     # In list
                        'value_not_in': ['val1'],         # Not in list
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

    # Track if JS has been rendered
    _conditional_js_rendered = False

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

    def conditional_js(self):
        """
        Render the JavaScript for conditional field visibility.

        Include this in your template: {{ form.conditional_js }}
        """
        rules = self.get_conditional_rules()
        if not rules:
            return ""

        context = self.get_conditional_context()

        parts = []

        # Inject the manager JavaScript (only once)
        if not ConditionalFieldsMixin._conditional_js_rendered:
            ConditionalFieldsMixin._conditional_js_rendered = True
            parts.append(f"<script data-conditional-fields-js>{CONDITIONAL_FIELDS_JS}</script>")

        # Embed rules as JSON
        data = {
            "rules": rules,
            "context": context,
        }
        parts.append(
            f'<script type="application/json" data-conditional-rules>'
            f"{json.dumps(data)}</script>"
        )

        # Re-init script
        parts.append(
            "<script>if(window.ConditionalFields)window.ConditionalFields.init();</script>"
        )

        return mark_safe("".join(parts))

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

    @classmethod
    def reset_js_rendered(cls):
        """Reset the JS rendered flag."""
        cls._conditional_js_rendered = False


# Reset flag between requests
try:
    from django.core.signals import request_finished

    request_finished.connect(lambda sender, **kwargs: ConditionalFieldsMixin.reset_js_rendered())
except ImportError:
    pass
