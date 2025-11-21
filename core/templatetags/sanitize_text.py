import re

import bleach
from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def sanitize_html(value):
    # Handle None, empty strings, and non-string types
    if value is None or value == "":
        return ""

    # Convert to string if not already (handles Message objects, etc.)
    if not isinstance(value, str):
        value = str(value)

    allowed_tags = ["b", "i", "em", "strong", "p", "br", "strike", "ul", "li", "span"]
    allowed_attributes = {
        "span": lambda tag, name, value: name == "class" and value == "quote"
    }

    # Clean the HTML
    cleaned_text = bleach.clean(
        value, tags=allowed_tags, attributes=allowed_attributes, strip=True
    )

    return format_html(cleaned_text)


@register.filter
def quote_tag(value):
    """
    Wrap text between quotation marks in <span class="quote"> </span> tags.
    """
    if not isinstance(value, str):
        return value  # Ensure the value is a string before processing
    # Replace text between quotes with a <span class="quote">
    return re.sub(r'"([^"]*)"', r'<span class="quote">"\1"</span>', value)
