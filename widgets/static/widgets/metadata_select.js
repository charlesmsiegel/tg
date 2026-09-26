(function() {
    'use strict';

    // Prevent double-initialization
    if (window.OptionMetadata) return;

    class OptionMetadataManager {
        constructor() {
            this.initialized = new WeakSet();
        }

        init() {
            document.querySelectorAll('[data-metadata-select]').forEach(select => {
                if (!this.initialized.has(select)) {
                    this.registerSelect(select);
                    this.initialized.add(select);
                }
            });
        }

        registerSelect(select) {
            // Fire metadata:change event on selection change
            select.addEventListener('change', () => this.fireMetadataChange(select));

            // Fire initial event if there's a selected value
            if (select.value) {
                this.fireMetadataChange(select);
            }
        }

        fireMetadataChange(select) {
            const metadata = this.get(select);
            const event = new CustomEvent('metadata:change', {
                bubbles: true,
                detail: {
                    value: select.value,
                    metadata: metadata,
                    select: select
                }
            });
            select.dispatchEvent(event);
        }

        /**
         * Get metadata from the currently selected option.
         * @param {HTMLSelectElement|string} selectElement - Select element or selector
         * @returns {Object} - Object with all data-* attributes from selected option
         */
        get(selectElement) {
            const select = typeof selectElement === 'string'
                ? document.querySelector(selectElement)
                : selectElement;

            if (!select || !select.selectedOptions || select.selectedOptions.length === 0) {
                return {};
            }

            const selectedOption = select.selectedOptions[0];
            const metadata = {};

            // Copy all data attributes from the option
            for (const key in selectedOption.dataset) {
                metadata[key] = selectedOption.dataset[key];
            }

            return metadata;
        }

        /**
         * Check if a specific metadata field is truthy.
         * @param {HTMLSelectElement|string} selectElement - Select element or selector
         * @param {string} field - The metadata field name (without 'data-' prefix)
         * @returns {boolean} - True if field value is 'true' or 'True'
         */
        isTrue(selectElement, field) {
            const metadata = this.get(selectElement);
            const value = metadata[field];
            return value === 'true' || value === 'True' || value === true;
        }

        /**
         * Get a specific metadata field value.
         * @param {HTMLSelectElement|string} selectElement - Select element or selector
         * @param {string} field - The metadata field name
         * @param {*} defaultValue - Default value if field not found
         * @returns {*} - The field value or default
         */
        getField(selectElement, field, defaultValue) {
            const metadata = this.get(selectElement);
            return metadata[field] !== undefined ? metadata[field] : defaultValue;
        }
    }

    window.OptionMetadata = new OptionMetadataManager();

    const init = () => window.OptionMetadata.init();

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Re-init for htmx/Turbo/dynamic content
    document.addEventListener('formset:widgetsInit', init);
    document.addEventListener('htmx:afterSwap', init);
    document.addEventListener('turbo:render', init);
    document.addEventListener('turbo:frame-load', init);
})();
