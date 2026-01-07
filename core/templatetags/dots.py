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

    return mark_safe(f'<span class="dots">{dots_str}</span><br><span class="dots">{boxes_str}</span>')


@register.filter(name="pool")
def pool(value, maximum=None):
    """
    Render a linked stat as a pool (blood pool style).

    Shows filled boxes for current value, empty boxes for remaining capacity.
    The total number of boxes equals the max/permanent value.

    Usage:
        {{ character.blood|pool }}
        {{ character.blood|pool:20 }}  # Override max display

    Accepts:
        - LinkedStatAccessor object (with .permanent and .temporary)
        - tuple/list: (max, current)
        - dict: {'permanent': x, 'temporary': y} or {'max': x, 'current': y}

    Example output for blood_pool=7, max_blood_pool=10:
        ■■■■■■■□□□
    """
    max_val = 0
    current = 0

    # Extract values based on input type
    if hasattr(value, "permanent") and hasattr(value, "temporary"):
        max_val = value.permanent
        current = value.temporary
    elif isinstance(value, (list, tuple)) and len(value) >= 2:
        max_val = value[0]
        current = value[1]
    elif isinstance(value, dict):
        max_val = value.get("permanent", value.get("max", 0))
        current = value.get("temporary", value.get("current", 0))

    # Convert to int safely
    try:
        max_val = int(max_val) if max_val else 0
        current = int(current) if current else 0
    except (ValueError, TypeError):
        max_val = 0
        current = 0

    # Use override maximum if provided, otherwise use the stat's max
    display_max = maximum if maximum is not None else max_val
    display_max = max(display_max, 1)  # At least 1 box

    # Cap current at display max
    current = min(current, display_max)

    # Generate boxes: filled for current, empty for remaining
    boxes_str = "■" * current + "□" * (display_max - current)

    return mark_safe(f'<span class="dots" title="{current}/{max_val}">{boxes_str}</span>')


@register.filter(name="pool_dots")
def pool_dots(value, maximum=None):
    """
    Render a linked stat as a pool using dots instead of boxes.

    Shows filled dots for current value, empty dots for remaining capacity.

    Usage:
        {{ character.gnosis|pool_dots }}

    Example output for gnosis=4, max=6:
        ●●●●○○
    """
    max_val = 0
    current = 0

    # Extract values based on input type
    if hasattr(value, "permanent") and hasattr(value, "temporary"):
        max_val = value.permanent
        current = value.temporary
    elif isinstance(value, (list, tuple)) and len(value) >= 2:
        max_val = value[0]
        current = value[1]
    elif isinstance(value, dict):
        max_val = value.get("permanent", value.get("max", 0))
        current = value.get("temporary", value.get("current", 0))

    # Convert to int safely
    try:
        max_val = int(max_val) if max_val else 0
        current = int(current) if current else 0
    except (ValueError, TypeError):
        max_val = 0
        current = 0

    # Use override maximum if provided, otherwise use the stat's max
    display_max = maximum if maximum is not None else max_val
    display_max = max(display_max, 1)  # At least 1 dot

    # Cap current at display max
    current = min(current, display_max)

    # Generate dots: filled for current, empty for remaining
    dots_str = "●" * current + "○" * (display_max - current)

    return mark_safe(f'<span class="dots" title="{current}/{max_val}">{dots_str}</span>')


@register.simple_tag(name="linked_stat")
def linked_stat_tag(obj, permanent_field, temporary_field=None, maximum=10, show_labels=False):
    """
    Render a linked stat from model fields.

    Usage:
        {% linked_stat character 'willpower' 'temporary_willpower' %}
        {% linked_stat character 'willpower' 'temporary_willpower' 10 True %}

    If temporary_field is not provided, assumes 'temporary_{permanent_field}'.
    """
    if temporary_field is None:
        temporary_field = f"temporary_{permanent_field}"

    permanent = getattr(obj, permanent_field, 0) or 0
    temporary = getattr(obj, temporary_field, 0) or 0

    # Convert to int safely
    try:
        permanent = int(permanent)
        temporary = int(temporary)
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

    if show_labels:
        return mark_safe(
            f'<div class="linked-stat">'
            f'<div class="stat-row"><span class="stat-label">Permanent:</span> '
            f'<span class="dots">{dots_str}</span></div>'
            f'<div class="stat-row"><span class="stat-label">Temporary:</span> '
            f'<span class="dots">{boxes_str}</span></div>'
            f"</div>"
        )

    return mark_safe(
        f'<div class="linked-stat">'
        f'<span class="dots">{dots_str}</span><br>'
        f'<span class="dots">{boxes_str}</span>'
        f"</div>"
    )


@register.inclusion_tag("core/templatetags/linked_stat_row.html")
def linked_stat_row(label, permanent, temporary, maximum=10):
    """
    Render a complete linked stat row with label, dots, and boxes.

    Usage:
        {% linked_stat_row "Willpower" character.willpower character.temporary_willpower %}

    This uses an inclusion tag for better styling control.
    """
    # Convert to int safely
    try:
        permanent = int(permanent) if permanent else 0
        temporary = int(temporary) if temporary else 0
    except (ValueError, TypeError):
        permanent = 0
        temporary = 0

    return {
        "label": label,
        "permanent": permanent,
        "temporary": temporary,
        "maximum": maximum,
        "dots": "●" * min(permanent, maximum) + "○" * (maximum - min(permanent, maximum)),
        "boxes": "■" * min(temporary, maximum) + "□" * (maximum - min(temporary, maximum)),
    }
