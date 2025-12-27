"""
AJAX utilities for safe JSON responses.

This module provides utilities for returning JSON responses from AJAX endpoints,
replacing the pattern of returning HTML fragments that are inserted with jQuery .html().

Using JSON responses with client-side DOM manipulation:
1. Prevents XSS vulnerabilities from unsafe HTML injection
2. Allows for Content Security Policy strict mode
3. Makes the data flow explicit and auditable
"""

from django.http import JsonResponse


def dropdown_options_response(queryset, value_attr="pk", label_attr="name"):
    """
    Return a JSON response suitable for populating a dropdown/select element.

    Args:
        queryset: A Django queryset or iterable of objects
        value_attr: Attribute name to use for option value (default: 'pk')
        label_attr: Attribute name to use for option label (default: 'name')
                   Can also be '__str__' to use the object's string representation

    Returns:
        JsonResponse with list of {value, label} objects

    Example:
        # In view:
        factions = MageFaction.objects.filter(affiliation=affiliation)
        return dropdown_options_response(factions)

        # In JavaScript:
        success: function(data) {
            const select = document.getElementById('id_faction');
            populateDropdown(select, data.options);
        }
    """
    options = []
    for obj in queryset:
        if value_attr == "pk":
            value = obj.pk
        else:
            value = getattr(obj, value_attr)

        if label_attr == "__str__":
            label = str(obj)
        elif label_attr == "name":
            label = getattr(obj, "name", str(obj))
        else:
            label = getattr(obj, label_attr)

        options.append({"value": value, "label": label})

    return JsonResponse({"options": options})


def simple_values_response(values):
    """
    Return a JSON response for a list of simple values (e.g., rating numbers).

    Args:
        values: An iterable of simple values (strings, integers, etc.)

    Returns:
        JsonResponse with list of values

    Example:
        # In view:
        ratings = [1, 2, 3, 4, 5]
        return simple_values_response(ratings)

        # In JavaScript:
        success: function(data) {
            const select = document.getElementById('id_rating');
            populateDropdownFromValues(select, data.values);
        }
    """
    return JsonResponse({"values": list(values)})
