from django import template

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
