from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="field")
def field(form, field_name):
    try:
        return form[field_name]
    except:
        return ""


@register.filter(name="add_class")
def add_class(field, css_class):
    """
    Add CSS class to a form field widget.
    Usage: {{ form.field|add_class:"my-class" }}
    """
    if hasattr(field, "as_widget"):
        return field.as_widget(attrs={"class": css_class})
    return field


@register.filter(name="add_attr")
def add_attr(field, attr_string):
    """
    Add an attribute to a form field widget.
    Usage: {{ form.field|add_attr:"rows:5" }}
           {{ form.field|add_class:"form-control"|add_attr:"placeholder:Enter text" }}
    """
    if not hasattr(field, "as_widget"):
        return field

    try:
        attr_name, attr_value = attr_string.split(":", 1)
    except ValueError:
        return field

    # Get existing attrs from the rendered field
    existing_attrs = {}
    if hasattr(field, "field") and hasattr(field.field, "widget"):
        existing_attrs = dict(field.field.widget.attrs)

    existing_attrs[attr_name] = attr_value
    return field.as_widget(attrs=existing_attrs)
