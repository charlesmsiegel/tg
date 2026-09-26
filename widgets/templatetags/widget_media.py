"""Combine page form assets using Django Media, including empty formset rows.

Templates pass forms under several names and formsets in *_context dictionaries.
Only inspect those known shapes: walking arbitrary context objects could evaluate
querysets or call model properties just to discover scripts.
"""

from django import forms, template
from django.forms.formsets import BaseFormSet

register = template.Library()


def register_media(context, media):
    """Collect tag dependencies in the current top-level template render.

    Included templates push their own render_context frame. The first render
    frame belongs to the outer Template.render call and disappears when it ends,
    even when the same Context is reused for another response.
    """
    frame = context.render_context.dicts[min(1, len(context.render_context.dicts) - 1)]
    frame["widget_media"] = frame.get("widget_media", forms.Media()) + media


@register.simple_tag(takes_context=True)
def page_media(context):
    frame = context.render_context.dicts[min(1, len(context.render_context.dicts) - 1)]
    media = frame.get("widget_media", forms.Media())
    for value in context.flatten().values():
        if isinstance(value, forms.BaseForm):
            media += value.media
        else:
            if isinstance(value, dict):
                value = value.get("formset")
            if isinstance(value, BaseFormSet):
                media += value.media + value.empty_form.media
                media += forms.Media(js=["widgets/formset_manager.js"])
    return media
