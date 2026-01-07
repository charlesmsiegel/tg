"""
Template tags for conditional field rendering.

Usage:
    {% load conditional_fields %}

    {# Wrap a field in a conditional visibility container #}
    {% conditional_wrap form.pooled %}
    {% conditional_wrap form.pooled "Pooled?" %}

    {# Render the conditional JavaScript (place at end of form) #}
    {{ form.conditional_js }}
"""

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def conditional_wrap(bound_field, label_prefix="", css_class="col-sm"):
    """
    Wrap a form field in a conditional visibility container.

    Args:
        bound_field: The bound form field (e.g., form.pooled)
        label_prefix: Optional text to prepend (e.g., "Pooled?")
        css_class: CSS class for the wrapper div (default: "col-sm")

    Returns:
        HTML string with the field wrapped in a visibility container.

    Usage:
        {% conditional_wrap form.pooled %}
        {% conditional_wrap form.pooled "Pooled?" %}
        {% conditional_wrap form.pooled "" "col-md-6" %}
    """
    field_name = bound_field.name
    form = bound_field.form

    # Get visibility rules from form if available
    rules = {}
    if hasattr(form, "get_conditional_rules"):
        rules = form.get_conditional_rules()

    field_rules = rules.get(field_name, {})

    # Determine initial visibility (default to hidden)
    initially_hidden = field_rules.get("initially_hidden", True)
    hidden_class = " d-none" if initially_hidden else ""

    wrapper_id = f"{field_name}_wrap"

    # Build content
    if label_prefix:
        content = f"{label_prefix} {bound_field}"
    else:
        content = str(bound_field)

    # Add error display if present
    if bound_field.errors:
        errors_html = '<div class="text-danger" style="font-size: 0.875rem;">{}</div>'.format(
            bound_field.errors
        )
        content += errors_html

    return format_html(
        '<div id="{}" class="{}{}">{}</div>',
        wrapper_id,
        css_class,
        hidden_class,
        mark_safe(content),
    )


@register.filter
def as_conditional(bound_field, label_prefix=""):
    """
    Filter version of conditional_wrap for simpler usage.

    Usage:
        {{ form.pooled|as_conditional }}
        {{ form.pooled|as_conditional:"Pooled?" }}
    """
    return conditional_wrap(bound_field, label_prefix)
