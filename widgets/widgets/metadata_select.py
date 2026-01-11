"""
Option Metadata Select Widget for Django

A widget that attaches data attributes to select options and provides
JavaScript hooks for accessing that metadata. Fires custom events when
selection changes, making it easy to show/hide dependent form elements.

Usage:
    # In your form field:
    background = forms.ChoiceField(
        widget=OptionMetadataSelect(
            metadata_fields={
                'poolable': 'is_poolable',  # Maps to data-poolable
                'cost': lambda obj: obj.get_cost(),  # Computed value
            }
        ),
        choices=get_background_choices(),
    )

    # Choices with metadata (3-tuple format):
    choices = [
        ('val1', 'Label 1', {'poolable': 'true', 'cost': '5'}),
        ('val2', 'Label 2', {'poolable': 'false', 'cost': '3'}),
    ]

    # In JavaScript:
    selectElement.addEventListener('metadata:change', (e) => {
        console.log(e.detail.metadata);  // {'poolable': 'true', ...}
    });

    // Or use the global API:
    const metadata = OptionMetadata.get(selectElement);
"""


from django import forms
from django.utils.safestring import mark_safe

# JavaScript for metadata handling - embedded directly so no static files needed
OPTION_METADATA_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.OptionMetadata) return;

    class OptionMetadataManager {
        constructor() {
            this.initialized = new WeakSet();
        }

        init() {
            document.querySelectorAll('[data-metadata-select]').forEach(select => {
                if (!this.initialized.has(select)) {
                    this.registerSelect(select);
                    this.initialized.add(select);
                }
            });
        }

        registerSelect(select) {
            // Fire metadata:change event on selection change
            select.addEventListener('change', () => this.fireMetadataChange(select));

            // Fire initial event if there's a selected value
            if (select.value) {
                this.fireMetadataChange(select);
            }
        }

        fireMetadataChange(select) {
            const metadata = this.get(select);
            const event = new CustomEvent('metadata:change', {
                bubbles: true,
                detail: {
                    value: select.value,
                    metadata: metadata,
                    select: select
                }
            });
            select.dispatchEvent(event);
        }

        /**
         * Get metadata from the currently selected option.
         * @param {HTMLSelectElement|string} selectElement - Select element or selector
         * @returns {Object} - Object with all data-* attributes from selected option
         */
        get(selectElement) {
            const select = typeof selectElement === 'string'
                ? document.querySelector(selectElement)
                : selectElement;

            if (!select || !select.selectedOptions || select.selectedOptions.length === 0) {
                return {};
            }

            const selectedOption = select.selectedOptions[0];
            const metadata = {};

            // Copy all data attributes from the option
            for (const key in selectedOption.dataset) {
                metadata[key] = selectedOption.dataset[key];
            }

            return metadata;
        }

        /**
         * Check if a specific metadata field is truthy.
         * @param {HTMLSelectElement|string} selectElement - Select element or selector
         * @param {string} field - The metadata field name (without 'data-' prefix)
         * @returns {boolean} - True if field value is 'true' or 'True'
         */
        isTrue(selectElement, field) {
            const metadata = this.get(selectElement);
            const value = metadata[field];
            return value === 'true' || value === 'True' || value === true;
        }

        /**
         * Get a specific metadata field value.
         * @param {HTMLSelectElement|string} selectElement - Select element or selector
         * @param {string} field - The metadata field name
         * @param {*} defaultValue - Default value if field not found
         * @returns {*} - The field value or default
         */
        getField(selectElement, field, defaultValue) {
            const metadata = this.get(selectElement);
            return metadata[field] !== undefined ? metadata[field] : defaultValue;
        }
    }

    window.OptionMetadata = new OptionMetadataManager();

    const init = () => window.OptionMetadata.init();

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


class OptionMetadataSelect(forms.Select):
    """
    A Select widget that attaches data attributes to options.

    Choices can be provided in two formats:
    - Standard: [(value, label), ...]
    - With metadata: [(value, label, {'key': 'value'}), ...]

    The widget also supports a `metadata_fields` configuration for
    model-based choices where metadata is extracted from model fields.
    """

    # Track if JS has been rendered in this request
    _js_rendered = False

    def __init__(self, metadata_fields=None, attrs=None, choices=()):
        """
        Initialize the widget.

        Args:
            metadata_fields: Dict mapping data attribute names to model field
                            names or callables. Used when choices are model instances.
                            Example: {'poolable': 'is_poolable', 'cost': lambda x: x.get_cost()}
            attrs: Standard Django widget attrs
            choices: Choice tuples, can include metadata as 3rd element
        """
        self.metadata_fields = metadata_fields or {}
        # Store the original choices with metadata
        self._choices_with_metadata = {}
        super().__init__(attrs=attrs, choices=choices)

    @property
    def choices(self):
        """Get choices as 2-tuples for Django's Select widget."""
        return self._choices

    @choices.setter
    def choices(self, value):
        """Set choices, extracting metadata from 3-tuples."""
        self._choices_with_metadata = {}
        normalized = []
        for choice in value:
            if len(choice) >= 3:
                # 3-tuple with metadata
                normalized.append((choice[0], choice[1]))
                self._choices_with_metadata[str(choice[0])] = choice[2]
            else:
                normalized.append(choice)
        self._choices = normalized

    def build_attrs(self, base_attrs, extra_attrs=None):
        """Add data-metadata-select attribute for JavaScript initialization."""
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs["data-metadata-select"] = "true"
        return attrs

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Create an option with data attributes from metadata."""
        # Get the base option dict from parent
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        # Check if we have metadata for this choice
        metadata = self._get_option_metadata(value, index)
        if metadata:
            if option["attrs"] is None:
                option["attrs"] = {}
            for key, val in metadata.items():
                option["attrs"][f"data-{key}"] = str(val)

        return option

    def _get_option_metadata(self, value, index):
        """
        Extract metadata for a specific option value.

        Looks up metadata from the stored _choices_with_metadata dict.
        """
        return self._choices_with_metadata.get(str(value))

    def render(self, name, value, attrs=None, renderer=None):
        """Render the select with injected JavaScript."""
        # Render the standard select
        select_html = super().render(name, value, attrs, renderer)

        parts = [select_html]

        # Inject JavaScript (only once per page)
        if not OptionMetadataSelect._js_rendered:
            OptionMetadataSelect._js_rendered = True
            parts.append(f"<script data-option-metadata-js>{OPTION_METADATA_JS}</script>")

        # Add a micro-script to re-initialize (handles dynamic/AJAX-loaded forms)
        parts.append(
            "<script>" "if(window.OptionMetadata)window.OptionMetadata.init();" "</script>"
        )

        return mark_safe("".join(parts))

    @classmethod
    def reset_js_rendered(cls):
        """Reset the JS rendered flag. Called automatically between requests."""
        cls._js_rendered = False


class OptionMetadataSelectMultiple(OptionMetadataSelect, forms.SelectMultiple):
    """Multiple-select variant of OptionMetadataSelect."""

    pass


# Reset flag between requests using Django's request_finished signal
try:
    from django.core.signals import request_finished

    request_finished.connect(lambda sender, **kwargs: OptionMetadataSelect.reset_js_rendered())
except ImportError:
    pass
