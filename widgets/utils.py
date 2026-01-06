"""
Utility functions for the widgets app.

Shared helpers for response handling and choice normalization.
"""


def normalize_choices(choices):
    """
    Normalize choices to a list of {value, label} dicts.

    Args:
        choices: An iterable of choices. Can be:
            - List of (value, label) tuples
            - QuerySet of model instances
            - List of model instances

    Returns:
        List of dicts with 'value' and 'label' keys
    """
    choices_list = []
    for item in choices:
        if isinstance(item, (list, tuple)) and len(item) >= 2:
            choices_list.append({"value": str(item[0]), "label": str(item[1])})
        elif hasattr(item, "pk"):
            # Model instance
            choices_list.append({"value": str(item.pk), "label": str(item)})
    return choices_list
