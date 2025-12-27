from django import template

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
