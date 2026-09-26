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

# JavaScript for metadata handling - embedded directly so no static files needed


class OptionMetadataSelect(forms.Select):
    """
    A Select widget that attaches data attributes to options.

    Choices can be provided in two formats:
    - Standard: [(value, label), ...]
    - With metadata: [(value, label, {'key': 'value'}), ...]

    The widget also supports a `metadata_fields` configuration for
    model-based choices where metadata is extracted from model fields.
    """

    class Media:
        js = ("widgets/metadata_select.js",)

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
