"""
Template tags for the FilterableListWidget.

Usage in templates:
    {% load filterable_list %}
    {% filterable_list_script %}

This loads the JavaScript needed for client-side list filtering.
"""

from django import template

from widgets.widgets.filterable import render_filterable_list_script

register = template.Library()


@register.simple_tag
def filterable_list_script():
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
    return render_filterable_list_script()
