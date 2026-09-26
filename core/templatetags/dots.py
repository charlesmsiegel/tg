from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="dots")
def dots(value, maximum=5):
    # Handle None
    if value is None:
        value = 0
    # Handle strings that represent numbers
    if isinstance(value, str):
        try:
            value = int(value)
        except (ValueError, TypeError):
            return value
    # Handle non-integer values
    if not isinstance(value, int):
        return value
    # Handle negative values
    if value < 0:
        value = 0
    # Only auto-expand to 10 if no custom maximum was provided (maximum=5 is default)
    # and value exceeds 5. If a custom maximum was provided, respect it.
    if maximum == 5 and value > 5:
        maximum = 10
    # Cap value at maximum
    if value > maximum:
        value = maximum
    return "●" * value + "○" * (maximum - value)


@register.filter(name="boxes")
def boxes(value, maximum=5):
    if not isinstance(value, int):
        return value
    if value > maximum:
        maximum = 10
    if value < 0:
        value = -value
    return "■" * value + "□" * (maximum - value)


@register.filter(name="abs")
def abs_filter(value):
    """Return the absolute value of a number."""
    if value is None:
        return 0
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        return value


@register.filter(name="lore_name")
def lore_name(value):
    """Convert lore_of_the_beast to 'Lore of the Beast'."""
    if not isinstance(value, str):
        return value
    # Replace underscores with spaces and title case
    return value.replace("_", " ").title()


# ============================================================================
# Linked Stat Template Tags
# ============================================================================


@register.filter(name="linked_dots")
def linked_dots(value, maximum=10):
    """
    Render a linked stat as dots (permanent) and boxes (temporary).

    Usage:
        {{ character.willpower_stat|linked_dots }}
        {{ character.willpower_stat|linked_dots:10 }}

    Accepts:
        - LinkedStatAccessor object (with .permanent and .temporary)
        - tuple/list: (permanent, temporary)
        - dict: {'permanent': x, 'temporary': y}
    """
    permanent = 0
    temporary = 0

    # Extract values based on input type
    if hasattr(value, "permanent") and hasattr(value, "temporary"):
        permanent = value.permanent
        temporary = value.temporary
    elif isinstance(value, (list, tuple)) and len(value) >= 2:
        permanent = value[0]
        temporary = value[1]
    elif isinstance(value, dict):
        permanent = value.get("permanent", 0)
        temporary = value.get("temporary", 0)

    # Convert to int safely
    try:
        permanent = int(permanent) if permanent else 0
        temporary = int(temporary) if temporary else 0
    except (ValueError, TypeError):
        permanent = 0
        temporary = 0

    # Cap at maximum
    permanent = min(permanent, maximum)
    temporary = min(temporary, maximum)

    # Generate dots for permanent (●○)
    dots_str = "●" * permanent + "○" * (maximum - permanent)

    # Generate boxes for temporary (■□)
    boxes_str = "■" * temporary + "□" * (maximum - temporary)

    return mark_safe(
        f'<span class="dots">{dots_str}</span><br><span class="dots">{boxes_str}</span>'
    )
