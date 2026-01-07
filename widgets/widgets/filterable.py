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

from django.utils.safestring import mark_safe

# The JavaScript code, embedded directly so no static files needed
FILTERABLE_LIST_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.FilterableList) return;

    class FilterableListManager {
        constructor() {
            this.lists = {};
            this.initialized = new WeakSet();
        }

        init() {
            document.querySelectorAll('[data-filterable-list]').forEach(container => {
                if (!this.initialized.has(container)) {
                    this.registerList(container);
                    this.initialized.add(container);
                }
            });
        }

        registerList(container) {
            const listName = container.dataset.filterableList;
            if (!listName) return;

            // Find items within this list
            const items = container.querySelectorAll('[data-filterable-item]');
            if (items.length === 0) return;

            // Find related controls (can be anywhere in document)
            const page = document.body;
            const textInputs = page.querySelectorAll(`[data-filter-input][data-filter-list="${listName}"], [data-filter-input]`);
            const selects = page.querySelectorAll(`[data-filter-select][data-filter-list="${listName}"], [data-filter-select]`);
            const checkboxes = page.querySelectorAll(`[data-filter-checkbox][data-filter-list="${listName}"], [data-filter-checkbox]`);
            const maxInputs = page.querySelectorAll(`[data-filter-max][data-filter-list="${listName}"], [data-filter-max]`);
            const clearBtn = page.querySelector(`[data-filter-clear][data-filter-list="${listName}"], [data-filter-clear]`);
            const countEl = page.querySelector(`[data-filter-count][data-filter-list="${listName}"], [data-filter-count]`);
            const noResultsEl = page.querySelector(`[data-filter-no-results][data-filter-list="${listName}"], [data-filter-no-results]`);

            // Store list info
            this.lists[listName] = {
                container: container,
                items: Array.from(items),
                textInputs: Array.from(textInputs),
                selects: Array.from(selects),
                checkboxes: Array.from(checkboxes),
                maxInputs: Array.from(maxInputs),
                clearBtn: clearBtn,
                countEl: countEl,
                noResultsEl: noResultsEl
            };

            // Bind event listeners
            this.bindListeners(listName);

            // Initial filter
            this.updateFilters(listName);
        }

        bindListeners(listName) {
            const list = this.lists[listName];

            // Text inputs - filter on input
            list.textInputs.forEach(input => {
                input.addEventListener('input', () => this.updateFilters(listName));
            });

            // Selects - filter on change
            list.selects.forEach(select => {
                select.addEventListener('change', () => this.updateFilters(listName));
            });

            // Checkboxes - filter on change
            list.checkboxes.forEach(cb => {
                cb.addEventListener('change', () => this.updateFilters(listName));
            });

            // Max inputs - filter on input
            list.maxInputs.forEach(input => {
                input.addEventListener('input', () => this.updateFilters(listName));
            });

            // Clear button
            if (list.clearBtn) {
                list.clearBtn.addEventListener('click', () => this.clearFilters(listName));
            }
        }

        updateFilters(listName) {
            const list = this.lists[listName];
            if (!list) return;

            let visibleCount = 0;
            const totalCount = list.items.length;

            // Gather active filters
            const textFilters = this.getTextFilters(list);
            const selectFilters = this.getSelectFilters(list);
            const checkboxFilters = this.getCheckboxFilters(list);
            const maxFilters = this.getMaxFilters(list);

            // Apply filters to each item
            list.items.forEach(item => {
                const show = this.itemMatchesFilters(item, textFilters, selectFilters, checkboxFilters, maxFilters);

                if (show) {
                    item.style.display = '';
                    visibleCount++;
                } else {
                    item.style.display = 'none';
                }
            });

            // Update count display
            this.updateCount(list, visibleCount, totalCount);

            // Show/hide no results message
            this.updateNoResults(list, visibleCount, totalCount);
        }

        getTextFilters(list) {
            const filters = {};
            list.textInputs.forEach(input => {
                const field = input.dataset.filterInput;
                const value = input.value.toLowerCase().trim();
                if (value) {
                    filters[field] = value;
                }
            });
            return filters;
        }

        getSelectFilters(list) {
            const filters = {};
            list.selects.forEach(select => {
                const field = select.dataset.filterSelect;
                const value = select.value;
                if (value) {
                    filters[field] = value;
                }
            });
            return filters;
        }

        getCheckboxFilters(list) {
            // Group checkboxes by their filter field
            const groups = {};
            list.checkboxes.forEach(cb => {
                const field = cb.dataset.filterCheckbox;
                if (!groups[field]) {
                    groups[field] = { values: [], mode: 'all' };
                }
                if (cb.checked) {
                    groups[field].values.push(cb.value);
                }
                // Get mode from parent container if available
                const modeContainer = cb.closest('[data-filter-mode]');
                if (modeContainer) {
                    groups[field].mode = modeContainer.dataset.filterMode || 'all';
                }
            });
            return groups;
        }

        getMaxFilters(list) {
            const filters = {};
            list.maxInputs.forEach(input => {
                const field = input.dataset.filterMax;
                const value = input.value.trim();
                if (value !== '') {
                    filters[field] = parseInt(value, 10);
                }
            });
            return filters;
        }

        itemMatchesFilters(item, textFilters, selectFilters, checkboxFilters, maxFilters) {
            // Text filters - check if item's data attribute contains the search text
            for (const [field, query] of Object.entries(textFilters)) {
                const itemValue = item.dataset[field] || '';
                if (!itemValue.toLowerCase().includes(query)) {
                    return false;
                }
            }

            // Select filters - exact match
            for (const [field, value] of Object.entries(selectFilters)) {
                const itemValue = item.dataset[field] || '';
                if (itemValue !== value) {
                    return false;
                }
            }

            // Checkbox filters - depends on mode
            for (const [field, group] of Object.entries(checkboxFilters)) {
                if (group.values.length === 0) continue;

                const mode = group.mode;

                if (mode === 'any') {
                    // ANY mode: item must match at least one selected checkbox
                    let matchesAny = false;
                    for (const val of group.values) {
                        // Check both data-field="value" and data-field-value="true" patterns
                        const directMatch = item.dataset[field] === val;
                        const boolMatch = item.dataset[`${field}${this.capitalize(val)}`] === 'true'
                                       || item.dataset[`${field}_${val}`] === 'true'
                                       || item.dataset[`${field}-${val}`] === 'true';
                        if (directMatch || boolMatch) {
                            matchesAny = true;
                            break;
                        }
                    }
                    if (!matchesAny) return false;

                } else if (mode === 'none') {
                    // NONE mode: item must NOT match any selected checkbox
                    for (const val of group.values) {
                        const directMatch = item.dataset[field] === val;
                        const boolMatch = item.dataset[`${field}${this.capitalize(val)}`] === 'true'
                                       || item.dataset[`${field}_${val}`] === 'true'
                                       || item.dataset[`${field}-${val}`] === 'true';
                        if (directMatch || boolMatch) {
                            return false;
                        }
                    }

                } else {
                    // ALL mode (default): item must match ALL selected checkboxes
                    for (const val of group.values) {
                        const directMatch = item.dataset[field] === val;
                        const boolMatch = item.dataset[`${field}${this.capitalize(val)}`] === 'true'
                                       || item.dataset[`${field}_${val}`] === 'true'
                                       || item.dataset[`${field}-${val}`] === 'true';
                        if (!directMatch && !boolMatch) {
                            return false;
                        }
                    }
                }
            }

            // Max filters - numeric less-than-or-equal comparison
            for (const [field, maxValue] of Object.entries(maxFilters)) {
                const itemValue = parseInt(item.dataset[field] || '0', 10);
                if (itemValue > maxValue) {
                    return false;
                }
            }

            return true;
        }

        capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        }

        updateCount(list, visible, total) {
            if (!list.countEl) return;

            const hasFilters = this.hasActiveFilters(list);

            if (hasFilters) {
                list.countEl.textContent = `Showing ${visible} of ${total}`;
            } else {
                list.countEl.textContent = `${total} items`;
            }
        }

        updateNoResults(list, visible, total) {
            if (!list.noResultsEl) return;

            if (visible === 0 && total > 0) {
                list.noResultsEl.style.display = '';
            } else {
                list.noResultsEl.style.display = 'none';
            }
        }

        hasActiveFilters(list) {
            // Check text inputs
            for (const input of list.textInputs) {
                if (input.value.trim()) return true;
            }
            // Check selects
            for (const select of list.selects) {
                if (select.value) return true;
            }
            // Check checkboxes
            for (const cb of list.checkboxes) {
                if (cb.checked) return true;
            }
            // Check max inputs
            for (const input of list.maxInputs) {
                if (input.value.trim()) return true;
            }
            return false;
        }

        clearFilters(listName) {
            const list = this.lists[listName];
            if (!list) return;

            // Clear text inputs
            list.textInputs.forEach(input => {
                input.value = '';
            });

            // Reset selects
            list.selects.forEach(select => {
                select.value = '';
            });

            // Uncheck checkboxes
            list.checkboxes.forEach(cb => {
                cb.checked = false;
            });

            // Clear max inputs
            list.maxInputs.forEach(input => {
                input.value = '';
            });

            // Re-apply filters (will show all)
            this.updateFilters(listName);
        }

        // Public API for external access
        refresh(listName) {
            if (listName) {
                this.updateFilters(listName);
            } else {
                Object.keys(this.lists).forEach(name => this.updateFilters(name));
            }
        }

        getVisibleItems(listName) {
            const list = this.lists[listName];
            if (!list) return [];
            return list.items.filter(item => item.style.display !== 'none');
        }
    }

    window.FilterableList = new FilterableListManager();

    const init = () => window.FilterableList.init();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-init for htmx/Turbo
    document.addEventListener('htmx:afterSwap', init);
    document.addEventListener('turbo:render', init);
    document.addEventListener('turbo:frame-load', init);
})();
"""


def get_filterable_list_js():
    """Return the FilterableList JavaScript code."""
    return FILTERABLE_LIST_JS


def render_filterable_list_script():
    """
    Render the FilterableList JavaScript as a script tag.

    Use this in your template:
        {{ filterable_list_script }}

    Or via template tag:
        {% load filterable_list %}
        {% filterable_list_script %}
    """
    return mark_safe(f"<script data-filterable-list-js>{FILTERABLE_LIST_JS}</script>")
