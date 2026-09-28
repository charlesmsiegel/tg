"""Field selection for Spread create / edit forms.

One template often serves several views whose forms differ (the create form, the
Storyteller's full edit form, an owner's limited form). These filters pick fields by
name from whatever form the view supplied, so a template never renders a field the
form lacks and never silently drops one it has:

    {% load tl_forms %}
    {% for field in form|fields_only:"name owner concept" %}...{% endfor %}
    {% include "core/misc/field_sections.html" with fields=form|fields_except:"name owner concept" %}

Names are separated by spaces or commas.
"""

from django import template

register = template.Library()


def _names(names):
    return [name for name in str(names or "").replace(",", " ").split() if name]


@register.filter
def fields_only(form, names):
    """The bound fields of ``form`` named in ``names``, in that order; missing names are skipped."""
    if form is None or not hasattr(form, "fields"):
        return []
    return [form[name] for name in _names(names) if name in form.fields]


@register.filter
def fields_except(form, names):
    """The visible bound fields of ``form`` not named in ``names``, in form order."""
    if form is None or not hasattr(form, "visible_fields"):
        return []
    skip = set(_names(names))
    return [field for field in form.visible_fields() if field.name not in skip]


@register.filter
def numeric_fields(fields):
    """The number inputs among ``fields`` (ratings, pools, ages)."""
    return [field for field in fields or () if field.widget_type == "number"]


@register.filter
def other_fields(fields):
    """Everything among ``fields`` that is not a number input."""
    return [field for field in fields or () if field.widget_type != "number"]
