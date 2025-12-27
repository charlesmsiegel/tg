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

    allowed_tags = ["a", "b", "i", "em", "strong", "u", "p", "br", "strike", "ul", "li", "span"]
    allowed_attributes = {
        "a": ["href"],
        "span": lambda tag, name, value: name == "class" and value == "quote",
    }
    # Only allow safe protocols in links
    allowed_protocols = ["http", "https", "mailto"]

    # Clean the HTML
    cleaned_text = bleach.clean(
        value,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=allowed_protocols,
        strip=True,
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


@register.filter
def simple_markdown(value):
    """
    Convert simple markdown to HTML.
    Supports: **bold**, *italic*, and preserves line breaks.
    """
    if value is None or value == "":
        return ""

    if not isinstance(value, str):
        value = str(value)

    # Convert **bold** to <strong>
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)

    # Convert *italic* to <em> (but not if already part of **)
    value = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", value)

    # Convert line breaks to <br> tags, but preserve paragraph breaks
    # First, normalize line endings
    value = value.replace("\r\n", "\n")

    # Convert double newlines to paragraph breaks
    paragraphs = value.split("\n\n")
    paragraphs = [p.replace("\n", "<br>\n") for p in paragraphs]
    value = "</p>\n<p>".join(paragraphs)
    value = f"<p>{value}</p>"

    # Clean with bleach to ensure safety
    allowed_tags = ["strong", "em", "p", "br"]
    cleaned_text = bleach.clean(value, tags=allowed_tags, strip=True)

    return format_html(cleaned_text)


@register.filter
def badge_text(value):
    """
    Format text for display in badges.
    Replaces underscores with spaces and capitalizes each word.
    Example: 'autumn_person' -> 'Autumn Person'
    """
    if value is None or value == "":
        return ""

    if not isinstance(value, str):
        value = str(value)

    return value.replace("_", " ").title()
