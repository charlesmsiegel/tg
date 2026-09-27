from django import template

register = template.Library()


@register.filter
def verbose_name(instance):
    """A model instance's (or class's) ``verbose_name``; templates cannot read ``_meta``."""
    return instance._meta.verbose_name
