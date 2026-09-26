"""
FilterableListWidget for Django

A reusable client-side list filtering component using data attributes.
Just add data attributes to your template - no Python widget needed.
Include the JavaScript via template tag.

Data-attribute API:
  Container:
    data-filterable-list="unique-name"  - Marks the container holding filterable items

  Filter inputs (place in filter panel):
    data-filter-input="field"           - Text input filter (searches data-field attribute)
    data-filter-select="field"          - Select dropdown filter
    data-filter-checkbox="field"        - Checkbox filter
    data-filter-mode="any|all|none"     - Mode for checkbox groups (default: 'all')
    data-filter-max="field"             - Numeric max filter (item's data-field <= input value)
    data-filter-clear                   - Button to clear all filters

  Items (place in list):
    data-filterable-item                - Marks an item in the list
    data-field="value"                  - Any data attribute for filtering

  Counter and no-results:
    data-filter-count                   - Element to show "Showing X of Y items"
    data-filter-no-results              - Element to show when no items match

Example usage:
    <!-- Filter panel -->
    <input type="text" data-filter-input="name" placeholder="Search...">
    <select data-filter-select="type">
        <option value="">All</option>
        <option value="a">Type A</option>
    </select>
    <div data-filter-mode="all">
        <input type="checkbox" data-filter-checkbox="sphere" value="forces">
        <input type="checkbox" data-filter-checkbox="sphere" value="prime">
    </div>
    <button data-filter-clear>Clear</button>
    <span data-filter-count></span>

    <!-- Item list -->
    <div data-filterable-list="my-list">
        <div data-filterable-item data-name="item one" data-type="a" data-sphere-forces="true">
            Item 1
        </div>
        <div data-filterable-item data-name="item two" data-type="b" data-sphere-prime="true">
            Item 2
        </div>
    </div>

    <div data-filter-no-results style="display:none;">No items match.</div>
"""

from django import forms


def render_filterable_list_script():
    """Return external script markup without any request-global state."""
    return forms.Media(js=("widgets/filterable.js",)).render_js()[0]
