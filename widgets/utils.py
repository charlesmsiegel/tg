"""
Utility functions for the widgets app.

Shared helpers for response handling and choice normalization.
"""

from django.forms.utils import flatatt
from django.utils.html import json_script
from django.utils.safestring import mark_safe


def config_script(value, **attrs):
    """Encode inert JSON while retaining the managers' existing data selectors."""
    return mark_safe(json_script(value).replace("<script", "<script" + flatatt(attrs), 1))


def normalize_choices(choices):
    """
    Normalize choices to a list of {value, label} dicts.

    Args:
        choices: An iterable of choices. Can be:
            - List of (value, label) tuples
            - List of (value, label, metadata) 3-tuples
            - QuerySet of model instances
            - List of model instances

    Returns:
        List of dicts with 'value', 'label', and optionally 'metadata' keys
    """
    choices_list = []
    for item in choices:
        if isinstance(item, (list, tuple)) and len(item) >= 3:
            # 3-tuple with metadata
            choice_dict = {"value": str(item[0]), "label": str(item[1])}
            if item[2]:
                choice_dict["metadata"] = item[2]
            choices_list.append(choice_dict)
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            choices_list.append({"value": str(item[0]), "label": str(item[1])})
        elif hasattr(item, "pk"):
            # Model instance
            choices_list.append({"value": str(item.pk), "label": str(item)})
    return choices_list
