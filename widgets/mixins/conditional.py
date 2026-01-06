"""
Conditional Fields Form Mixin

Mixin for forms with conditional field visibility based on other field values.
"""

import json

from django.utils.safestring import mark_safe

# JavaScript for conditional field visibility - embedded directly
CONDITIONAL_FIELDS_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.ConditionalFields) return;

    class ConditionalFieldsManager {
        constructor() {
            this.initialized = new WeakSet();
        }

        init() {
            // Find all elements with conditional rules
            document.querySelectorAll('[data-conditional-rules]').forEach(rulesElement => {
                if (!this.initialized.has(rulesElement)) {
                    this.setupConditionalFields(rulesElement);
                    this.initialized.add(rulesElement);
                }
            });
        }

        setupConditionalFields(rulesElement) {
            const rules = JSON.parse(rulesElement.dataset.conditionalRules);
            const prefix = rulesElement.dataset.formPrefix || '';

            // Find the search context: closest form, parent with data-conditional-rules, or document
            let searchContext = rulesElement.closest('form');
            if (!searchContext) {
                searchContext = rulesElement.parentElement || document;
            }

            // Set up each controller
            Object.keys(rules).forEach(controllerName => {
                const controllerRules = rules[controllerName];
                const controller = this.findField(searchContext, controllerName, prefix);

                if (!controller) {
                    console.warn(`ConditionalFields: Controller '${controllerName}' not found`);
                    return;
                }

                // Initial visibility update
                this.updateVisibility(controller, controllerRules, searchContext, prefix);

                // Add change listener
                controller.addEventListener('change', () => {
                    this.updateVisibility(controller, controllerRules, searchContext, prefix);
                });
            });
        }

        findField(context, fieldName, prefix) {
            // Handle formset prefixes
            const fullName = prefix ? `${prefix}-${fieldName}` : fieldName;
            const root = context === document ? document : context;

            // Try by ID first (Django convention: id_fieldname)
            let field = root.querySelector(`#id_${fullName}`);
            if (field) return field;

            // Try by name
            field = root.querySelector(`[name="${fullName}"]`);
            if (field) return field;

            // Try without prefix
            field = root.querySelector(`#id_${fieldName}`);
            if (field) return field;

            return root.querySelector(`[name="${fieldName}"]`);
        }

        findWrapper(context, fieldName, prefix) {
            const fullName = prefix ? `${prefix}-${fieldName}` : fieldName;
            const root = context === document ? document : context;

            // Try multiple wrapper ID patterns
            let wrapper = root.querySelector(`#${fullName}_wrap`);
            if (wrapper) return wrapper;

            wrapper = root.querySelector(`#id_${fullName}_wrap`);
            if (wrapper) return wrapper;

            wrapper = root.querySelector(`#${fieldName}_wrap`);
            if (wrapper) return wrapper;

            wrapper = root.querySelector(`#id_${fieldName}_wrap`);
            if (wrapper) return wrapper;

            // Try data attribute
            wrapper = root.querySelector(`[data-conditional-field="${fieldName}"]`);
            if (wrapper) return wrapper;

            return root.querySelector(`[data-conditional-field="${fullName}"]`);
        }

        updateVisibility(controller, rules, context, prefix) {
            const value = this.getControllerValue(controller);

            Object.keys(rules).forEach(targetName => {
                const rule = rules[targetName];
                const wrapper = this.findWrapper(context, targetName, prefix);

                if (!wrapper) {
                    console.warn(`ConditionalFields: Wrapper for '${targetName}' not found`);
                    return;
                }

                const shouldShow = this.evaluateRule(value, rule);
                this.setVisibility(wrapper, shouldShow);
            });
        }

        getControllerValue(controller) {
            if (controller.type === 'checkbox') {
                return controller.checked;
            }
            return controller.value;
        }

        evaluateRule(value, rule) {
            // Handle checkbox boolean
            if (typeof value === 'boolean') {
                if (rule.checked !== undefined) {
                    return value === rule.checked;
                }
                return value;
            }

            // String value rules
            const strValue = String(value);

            // Exact match with 'values' array
            if (rule.values !== undefined) {
                return rule.values.includes(strValue);
            }

            // Exclude certain values
            if (rule.exclude !== undefined) {
                return !rule.exclude.includes(strValue);
            }

            // Show when not empty
            if (rule.not_empty !== undefined) {
                return strValue !== '' && strValue !== rule.not_empty;
            }

            // Default: show when controller has a value
            return strValue !== '';
        }

        setVisibility(element, visible) {
            if (visible) {
                element.classList.remove('d-none');
            } else {
                element.classList.add('d-none');
            }
        }
    }

    window.ConditionalFields = new ConditionalFieldsManager();

    const init = () => window.ConditionalFields.init();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-init for htmx/Turbo/dynamic content
    document.addEventListener('htmx:afterSwap', init);
    document.addEventListener('turbo:render', init);
    document.addEventListener('turbo:frame-load', init);
})();
"""


class ConditionalFieldsMixin:
    """
    Mixin for forms with conditional field visibility.

    Automatically shows/hides fields based on another field's value.
    Define rules in the `conditional_fields` class attribute.

    Usage:
        class MyForm(ConditionalFieldsMixin, forms.Form):
            category = forms.ChoiceField(choices=[...])
            example = forms.ChoiceField(choices=[...])
            note = forms.CharField()
            value = forms.IntegerField()

            conditional_fields = {
                'category': {  # The controller field
                    'example': {'exclude': ['-----', 'Willpower']},  # Show except for these
                    'note': {'values': ['Background']},  # Show only for these values
                    'value': {'values': ['MeritFlaw']},
                }
            }

    Rule types:
        - {'values': ['A', 'B']}: Show when controller value is 'A' or 'B'
        - {'exclude': ['X', 'Y']}: Show when controller value is NOT 'X' or 'Y'
        - {'not_empty': ''}: Show when controller has any non-empty value
        - {'checked': True}: For checkboxes, show when checked
        - {'checked': False}: For checkboxes, show when unchecked

    Template:
        The mixin provides a `conditional_fields_script` property that renders
        the necessary JavaScript. Wrap your dependent fields in divs with
        id="fieldname_wrap" and include `d-none` class for initial hidden state.

        Example template:
            {{ form.category }}
            <div class="d-none" id="example_wrap">{{ form.example }}</div>
            <div class="d-none" id="note_wrap">{{ form.note }}</div>
            {{ form.conditional_fields_script }}
    """

    # Override in subclasses to define visibility rules
    conditional_fields = {}

    # Track if JS has been rendered in this request
    _conditional_js_rendered = False

    def get_conditional_fields(self):
        """
        Return the conditional field rules.
        Override this method for dynamic rules based on form instance.
        """
        return self.conditional_fields

    @property
    def conditional_fields_script(self):
        """
        Render the JavaScript for conditional field visibility.
        Include this in your template after the form fields.
        """
        rules = self.get_conditional_fields()
        if not rules:
            return ""

        parts = []

        # Inject JS library only once per request
        if not ConditionalFieldsMixin._conditional_js_rendered:
            ConditionalFieldsMixin._conditional_js_rendered = True
            parts.append(f"<script data-conditional-fields-js>{CONDITIONAL_FIELDS_JS}</script>")

        # Get form prefix for formset support
        prefix = getattr(self, "prefix", "") or ""

        # Create a wrapper div with data attributes
        rules_json = json.dumps(rules)
        parts.append(
            f"<div data-conditional-rules='{rules_json}' "
            f'data-form-prefix="{prefix}" style="display:none;"></div>'
        )

        # Add init trigger
        parts.append(
            "<script>if(window.ConditionalFields)window.ConditionalFields.init();</script>"
        )

        return mark_safe("".join(parts))

    def render_conditional_wrapper(self, field_name, content, extra_classes=""):
        """
        Helper method to render a field wrapped in a conditional div.

        Usage in template tags or custom form rendering:
            {{ form.render_conditional_wrapper('example', form.example) }}
        """
        classes = f"d-none {extra_classes}".strip()
        return mark_safe(
            f'<div id="{field_name}_wrap" class="{classes}" '
            f'data-conditional-field="{field_name}">{content}</div>'
        )


# Reset flag between requests using Django's request_finished signal
try:
    from django.core.signals import request_finished

    def _reset_conditional_js_flag(sender, **kwargs):
        ConditionalFieldsMixin._conditional_js_rendered = False

    request_finished.connect(_reset_conditional_js_flag)
except ImportError:
    pass
