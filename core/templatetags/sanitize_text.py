import re

import bleach
from django import template
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

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

    Escapes HTML special characters to prevent XSS attacks while preserving
    the quote styling functionality.
    """
    if not isinstance(value, str):
        return value  # Ensure the value is a string before processing

    def escape_and_wrap(match):
        """Escape the captured content and wrap in styled span."""
        quoted_content = escape(match.group(1))
        return f'<span class="quote">"{quoted_content}"</span>'

    # First, escape content outside quotes, then handle quoted content specially
    # Split on quote patterns, escape non-quoted parts, and wrap quoted parts
    parts = []
    last_end = 0
    for match in re.finditer(r'"([^"]*)"', value):
        # Escape the part before this quote
        parts.append(escape(value[last_end : match.start()]))
        # Add the styled quote with escaped content
        parts.append(escape_and_wrap(match))
        last_end = match.end()
    # Escape the remaining part after the last quote
    parts.append(escape(value[last_end:]))

    result = "".join(parts)
    # Mark as safe since we've escaped user content and only added safe HTML tags
    return mark_safe(result)


@register.filter
def simple_markdown(value):
    """
    Convert simple markdown to HTML.
    Supports: **bold**, *italic*, and preserves line breaks.

    Escapes HTML special characters to prevent XSS attacks while preserving
    markdown formatting functionality.
    """
    if value is None or value == "":
        return ""

    if not isinstance(value, str):
        value = str(value)

    # Process markdown patterns while escaping their content
    # We need to handle this carefully to escape non-markdown text while
    # preserving markdown syntax

    result = ""
    last_end = 0

    # Combined pattern for bold and italic
    # Process bold first (longer delimiter takes precedence)
    combined_pattern = re.compile(r"(\*\*(.+?)\*\*)|(?<!\*)(\*([^*]+?)\*)(?!\*)")

    for match in combined_pattern.finditer(value):
        # Escape text before this match
        result += escape(value[last_end : match.start()])

        if match.group(1):  # Bold match
            result += f"<strong>{escape(match.group(2))}</strong>"
        elif match.group(3):  # Italic match
            result += f"<em>{escape(match.group(4))}</em>"

        last_end = match.end()

    # Escape remaining text
    result += escape(value[last_end:])

    # Convert line breaks to <br> tags, but preserve paragraph breaks
    # First, normalize line endings
    result = result.replace("\r\n", "\n")

    # Convert double newlines to paragraph breaks
    paragraphs = result.split("\n\n")
    paragraphs = [p.replace("\n", "<br>\n") for p in paragraphs]
    result = "</p>\n<p>".join(paragraphs)
    result = f"<p>{result}</p>"

    # Mark as safe since we've escaped user content and only added safe HTML tags
    return mark_safe(result)


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
