from django import template

register = template.Library()


@register.filter(name="get_specialty")
def get_specialty(character, stat):
    """
    Get the specialty for a given stat on a character.

    Usage in templates:
        {% load get_specialty %}
        {{ character|get_specialty:'firearms' }}

    This filter calls character.get_specialty(stat) to retrieve
    any specialty the character has for the specified stat.
    """
    return character.get_specialty(stat)
