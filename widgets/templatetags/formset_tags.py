"""
Template tags for FormsetManager widget.

Usage:
    {% load formset_tags %}

    {# Render the FormsetManager JavaScript (once per page) #}
    {% formset_script %}

    {# Mark a container for formset management #}
    <div {% formset_container "my_formset" %}>
        ...
    </div>

    {# Render an add button #}
    {% formset_add_btn "my_formset" "Add Item" class="tg-btn btn-primary" %}

    {# Include in your form row template #}
    <button {% formset_remove_btn "my_formset" %} class="tg-btn btn-danger btn-sm">Remove</button>
"""

from django import template
from django.utils.safestring import mark_safe

from ..widgets.formset_manager import render_formset_manager_script_once

register = template.Library()


@register.simple_tag
def formset_script():
    """
    Render the FormsetManager JavaScript.
    Only renders once per page, subsequent calls return empty string.

    Usage:
        {% formset_script %}
    """
    return render_formset_manager_script_once()


@register.simple_tag
def formset_container(prefix, empty_form_id=None, animate=False):
    """
    Return data attributes for a formset container.

    Args:
        prefix: The Django formset prefix (e.g., 'backgrounds', 'resonance')
        empty_form_id: Optional custom ID for the empty form template.
                       Defaults to 'empty_{prefix}_form'
        animate: Whether to animate form additions/removals

    Usage:
        <div {% formset_container "backgrounds" %}>
            {% for form in formset %}
                ...
            {% endfor %}
        </div>

    Returns:
        HTML data attributes string
    """
    attrs = [
        f'data-formset-container=""',
        f'data-formset-prefix="{prefix}"',
    ]

    if empty_form_id:
        attrs.append(f'data-formset-empty-form="{empty_form_id}"')

    if animate:
        attrs.append('data-formset-animate="true"')

    return mark_safe(' '.join(attrs))


@register.simple_tag
def formset_add_btn(prefix, label="Add", **kwargs):
    """
    Render a complete add button for a formset.

    Args:
        prefix: The Django formset prefix
        label: Button text
        **kwargs: Additional HTML attributes (e.g., class="btn btn-primary")

    Usage:
        {% formset_add_btn "resonance" "Add Resonance" class="tg-btn btn-primary" %}

    Returns:
        Complete button HTML element
    """
    attrs = [f'data-formset-add="{prefix}"', 'type="button"']

    for key, value in kwargs.items():
        # Convert underscores to hyphens for HTML attributes
        html_key = key.replace('_', '-')
        attrs.append(f'{html_key}="{value}"')

    attrs_str = ' '.join(attrs)
    return mark_safe(f'<button {attrs_str}>{label}</button>')


@register.simple_tag
def formset_remove_btn(prefix):
    """
    Return data attributes for a remove button.

    Args:
        prefix: The Django formset prefix

    Usage:
        <button {% formset_remove_btn "resonance" %} type="button" class="btn btn-danger">
            Remove
        </button>

    Returns:
        HTML data attribute string
    """
    return mark_safe(f'data-formset-remove="{prefix}"')


@register.simple_tag
def formset_form_wrapper():
    """
    Return data attribute to mark a form row/wrapper for proper removal.

    Usage:
        <div {% formset_form_wrapper %} class="form-row">
            ...
        </div>

    Returns:
        HTML data attribute string
    """
    return mark_safe('data-formset-form=""')


@register.inclusion_tag('widgets/formset_empty_form.html')
def formset_empty_form(formset, prefix, template_name=None):
    """
    Render a hidden empty form template for JavaScript cloning.

    Args:
        formset: The Django formset object
        prefix: The formset prefix
        template_name: Optional custom template for the empty form

    Usage:
        {% formset_empty_form formset "backgrounds" %}

    Note: You need to create the template at widgets/formset_empty_form.html
          or use the template_name parameter.
    """
    return {
        'empty_form': formset.empty_form,
        'prefix': prefix,
        'template_name': template_name,
    }
