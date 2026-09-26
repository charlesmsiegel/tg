"""
Template tags for the FilterableListWidget.

Usage in templates:
    {% load filterable_list %}
    {% filterable_list_script %}

This registers media for the base template. Standalone templates must end
with {% load widget_media %}{% page_media %}.
"""

from django import forms, template

from .widget_media import register_media

register = template.Library()


@register.simple_tag(takes_context=True)
def filterable_list_script(context):
    """
    Render the FilterableList JavaScript.

    Include this once in your template (typically in extra_js block):
        {% load filterable_list %}
        {% filterable_list_script %}

    Then use data attributes to configure filtering:
        <div data-filterable-list="my-list">
            <div data-filterable-item data-name="item one" data-type="a">
                Item 1
            </div>
        </div>

        <input type="text" data-filter-input="name" placeholder="Search...">
        <select data-filter-select="type">...</select>
        <button data-filter-clear>Clear</button>
        <span data-filter-count></span>
        <div data-filter-no-results style="display:none;">No results</div>
    """
    register_media(context, forms.Media(js=("widgets/filterable.js",)))
    return ""
