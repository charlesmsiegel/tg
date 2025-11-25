import json

from django import template

register = template.Library()


@register.filter(name="pprint")
def pprint(value):
    """Pretty print JSON data"""
    try:
        if isinstance(value, str):
            # If it's already a string, try to parse it first
            value = json.loads(value)
        return json.dumps(value, indent=2, ensure_ascii=False)
    except (TypeError, ValueError, json.JSONDecodeError):
        return str(value)


@register.filter(name="get_item")
def get_item(dictionary, key):
    """Get an item from a dictionary by key.

    Usage: {{ mydict|get_item:key }}
    """
    if dictionary is None:
        return None
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
