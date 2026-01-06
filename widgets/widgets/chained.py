"""
Chained Select Widget for Django

A widget that renders dependent/cascading dropdowns with zero configuration.
Just render the field in your template - no {{ form.media }} needed.
"""

import json

from django import forms
from django.utils.safestring import mark_safe

# The JavaScript code, embedded directly so no static files or {{ form.media }} needed
CHAINED_SELECT_JS = """
(function() {
    'use strict';

    // Prevent double-initialization
    if (window.ChainedSelect) return;

    class ChainedSelectManager {
        constructor() {
            this.chains = {};
            this.choiceTrees = {};
            this.initialized = new WeakSet();
        }

        init() {
            this.loadEmbeddedTrees();
            document.querySelectorAll('[data-chained-select]').forEach(select => {
                if (!this.initialized.has(select)) {
                    this.registerSelect(select);
                    this.initialized.add(select);
                }
            });
        }

        loadEmbeddedTrees() {
            document.querySelectorAll('script[data-chain-tree]').forEach(script => {
                const chainName = script.dataset.chainTree;
                try {
                    this.choiceTrees[chainName] = JSON.parse(script.textContent);
                } catch (e) {
                    console.error(`ChainedSelect: Failed to parse tree for ${chainName}:`, e);
                }
            });
        }

        registerSelect(select) {
            const chainName = select.dataset.chainName;
            const position = parseInt(select.dataset.chainPosition, 10);
            const parentFieldName = select.dataset.parentField;
            const ajaxUrl = select.dataset.ajaxUrl;
            const formPath = select.dataset.formPath;
            const emptyLabel = select.dataset.emptyLabel || '---------';

            if (!chainName) return;

            if (!this.chains[chainName]) {
                this.chains[chainName] = { selects: {}, order: [], formPath: formPath };
            }

            const chain = this.chains[chainName];
            const fieldName = this.getFieldName(select);

            if (formPath) chain.formPath = formPath;

            chain.selects[fieldName] = {
                element: select,
                position: position,
                parentFieldName: parentFieldName,
                ajaxUrl: ajaxUrl,
                formPath: formPath,
                emptyLabel: emptyLabel
            };

            chain.order = Object.keys(chain.selects).sort((a, b) =>
                chain.selects[a].position - chain.selects[b].position
            );

            select.addEventListener('change', () => this.handleChange(chainName, fieldName));
        }

        getFieldName(select) {
            const name = select.name || select.id;
            const parts = name.split('-');
            return parts[parts.length - 1];
        }

        handleChange(chainName, fieldName) {
            const chain = this.chains[chainName];
            const changedInfo = chain.selects[fieldName];
            const changedPosition = changedInfo.position;
            const newValue = changedInfo.element.value;

            const children = chain.order.filter(name =>
                chain.selects[name].position > changedPosition
            );

            if (children.length === 0) return;

            this.updateChildSelect(chainName, children[0], fieldName, newValue);
            children.slice(1).forEach(childName => this.resetSelect(chainName, childName));
        }

        async updateChildSelect(chainName, childFieldName, parentFieldName, parentValue) {
            const chain = this.chains[chainName];
            const childInfo = chain.selects[childFieldName];
            const select = childInfo.element;
            const tree = this.choiceTrees[chainName];

            if (tree && !childInfo.ajaxUrl) {
                const key = `${parentFieldName}:${parentValue}`;
                const choices = tree[key] || [];
                this.setOptions(select, childInfo.emptyLabel, choices);
                select.dispatchEvent(new Event('change', { bubbles: true }));
                return;
            }

            if (!childInfo.ajaxUrl) {
                this.resetSelect(chainName, childFieldName);
                return;
            }

            select.disabled = true;
            this.setOptions(select, 'Loading...', []);

            if (!parentValue) {
                this.resetSelect(chainName, childFieldName);
                return;
            }

            try {
                const url = new URL(childInfo.ajaxUrl, window.location.origin);
                url.searchParams.set('field', childFieldName);
                url.searchParams.set('parent_value', parentValue);

                const formPath = childInfo.formPath || chain.formPath;
                if (formPath) url.searchParams.set('form', formPath);

                const response = await fetch(url, {
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });

                if (!response.ok) throw new Error(`HTTP ${response.status}`);

                const data = await response.json();
                if (data.error) throw new Error(data.error);

                this.setOptions(select, childInfo.emptyLabel, data.choices || []);
                select.disabled = false;
                select.dispatchEvent(new Event('change', { bubbles: true }));

            } catch (error) {
                console.error('ChainedSelect error:', error);
                this.setOptions(select, 'Error loading', []);
                select.disabled = false;
            }
        }

        resetSelect(chainName, fieldName) {
            const chain = this.chains[chainName];
            const info = chain.selects[fieldName];
            const select = info.element;
            this.setOptions(select, info.emptyLabel, []);
            select.disabled = false;
            select.value = '';
        }

        setOptions(select, emptyLabel, choices) {
            select.innerHTML = '';
            const emptyOpt = document.createElement('option');
            emptyOpt.value = '';
            emptyOpt.textContent = emptyLabel;
            select.appendChild(emptyOpt);

            choices.forEach(choice => {
                const option = document.createElement('option');
                option.value = choice.value;
                option.textContent = choice.label;
                // Add metadata as data attributes if present
                if (choice.metadata) {
                    for (const key in choice.metadata) {
                        option.dataset[key] = choice.metadata[key];
                    }
                }
                select.appendChild(option);
            });

            // Fire metadata:change event if OptionMetadata is available
            if (window.OptionMetadata && select.value) {
                window.OptionMetadata.fireMetadataChange(select);
            }
        }

        setValue(chainName, fieldName, value) {
            const chain = this.chains[chainName];
            if (!chain || !chain.selects[fieldName]) return;
            const select = chain.selects[fieldName].element;
            select.value = value;
            this.handleChange(chainName, fieldName);
        }

        getValues(chainName) {
            const chain = this.chains[chainName];
            if (!chain) return {};
            const values = {};
            chain.order.forEach(fieldName => {
                values[fieldName] = chain.selects[fieldName].element.value;
            });
            return values;
        }
    }

    window.ChainedSelect = new ChainedSelectManager();

    const init = () => window.ChainedSelect.init();

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


class ChainedSelect(forms.Select):
    """
    A Select widget for cascading/dependent dropdowns.

    Self-contained: automatically injects JavaScript when rendered.
    No {{ form.media }} or static file configuration needed.
    """

    # Track if JS has been rendered in this request
    _js_rendered = False

    def __init__(
        self,
        chain_name=None,
        chain_position=0,
        parent_field=None,
        choices_tree=None,
        ajax_url=None,
        form_path=None,
        empty_label="---------",
        attrs=None,
        choices=(),
    ):
        self.chain_name = chain_name
        self.chain_position = chain_position
        self.parent_field = parent_field
        self.choices_tree = choices_tree
        self.ajax_url = ajax_url
        self.form_path = form_path
        self.empty_label = empty_label

        super().__init__(attrs=attrs, choices=choices)

    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)

        attrs["data-chained-select"] = "true"

        if self.chain_name:
            attrs["data-chain-name"] = self.chain_name
        attrs["data-chain-position"] = str(self.chain_position)

        if self.parent_field:
            attrs["data-parent-field"] = self.parent_field

        if self.ajax_url:
            attrs["data-ajax-url"] = self.ajax_url

        if self.form_path:
            attrs["data-form-path"] = self.form_path

        attrs["data-empty-label"] = self.empty_label

        existing = attrs.get("class", "")
        attrs["class"] = f"{existing} chained-select".strip()

        return attrs

    def render(self, name, value, attrs=None, renderer=None):
        # Render the standard select
        select_html = super().render(name, value, attrs, renderer)

        parts = [select_html]

        # Inject JavaScript (only once per page)
        # We use a simple marker comment to detect if already injected
        if not ChainedSelect._js_rendered:
            ChainedSelect._js_rendered = True
            parts.append(f"<script data-chained-select-js>{CHAINED_SELECT_JS}</script>")

        # If we have a choices tree and this is the root, embed it
        if self.choices_tree and self.chain_position == 0 and self.chain_name:
            tree_json = json.dumps(self.choices_tree)
            parts.append(
                f'<script type="application/json" data-chain-tree="{self.chain_name}">'
                f"{tree_json}</script>"
            )

        # Add a micro-script to re-initialize (handles dynamic/AJAX-loaded forms)
        parts.append("<script>" "if(window.ChainedSelect)window.ChainedSelect.init();" "</script>")

        return mark_safe("".join(parts))

    @classmethod
    def reset_js_rendered(cls):
        """Reset the JS rendered flag. Called automatically between requests."""
        cls._js_rendered = False


class ChainedSelectMultiple(ChainedSelect, forms.SelectMultiple):
    """Multiple-select variant of ChainedSelect."""

    pass


# Reset flag between requests using Django's request_finished signal
try:
    from django.core.signals import request_finished

    request_finished.connect(lambda sender, **kwargs: ChainedSelect.reset_js_rendered())
except ImportError:
    pass
