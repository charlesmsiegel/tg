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
