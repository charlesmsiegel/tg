(function() {
    'use strict';

    if (window.ConditionalFields) return;

    class ConditionalFieldsManager {
        constructor() {
            this.rules = {};
            this.context = {};
            this.initialized = false;
        }

        init() {
            if (this.initialized) return;
            this.initialized = true;

            // Find and parse embedded rules
            document.querySelectorAll('script[data-conditional-rules]').forEach(script => {
                try {
                    const data = JSON.parse(script.textContent);
                    Object.assign(this.rules, data.rules || {});
                    Object.assign(this.context, data.context || {});
                } catch (e) {
                    console.error('ConditionalFields: Failed to parse rules:', e);
                }
            });

            // Set up event listeners
            this.setupListeners();

            // Apply initial visibility
            this.applyAllRules();
        }

        setupListeners() {
            // Listen to all form controls that have rules depending on them
            const watchedFields = new Set();
            for (const [targetField, config] of Object.entries(this.rules)) {
                for (const condition of ['visible_when', 'hidden_when']) {
                    if (config[condition]) {
                        for (const sourceField of Object.keys(config[condition])) {
                            if (!sourceField.startsWith('_')) {
                                watchedFields.add(sourceField);
                            }
                        }
                    }
                }
            }

            watchedFields.forEach(fieldName => {
                const field = document.getElementById('id_' + fieldName);
                if (field) {
                    field.addEventListener('change', () => this.applyAllRules());
                    // Also listen for metadata:change events
                    field.addEventListener('metadata:change', () => this.applyAllRules());
                }
            });
        }

        applyAllRules() {
            for (const [targetField, config] of Object.entries(this.rules)) {
                this.applyRule(targetField, config);
            }
        }

        applyRule(targetField, config) {
            // Support custom wrapper_id or default to {field}_wrap
            const wrapperId = config.wrapper_id || (targetField + '_wrap');
            const wrapper = document.getElementById(wrapperId);
            if (!wrapper) return;

            let visible = true;

            // Check visible_when conditions (all must be true)
            if (config.visible_when) {
                visible = this.checkConditions(config.visible_when, true);
            }

            // Check hidden_when conditions (if any is true, hide)
            if (config.hidden_when && visible) {
                visible = !this.checkConditions(config.hidden_when, false);
            }

            if (visible) {
                wrapper.classList.remove('d-none');
            } else {
                wrapper.classList.add('d-none');
            }
        }

        checkConditions(conditions, requireAll) {
            const results = [];

            for (const [sourceField, checks] of Object.entries(conditions)) {
                if (sourceField === '_context') {
                    // Check context variables
                    for (const [contextVar, expectedValue] of Object.entries(checks)) {
                        results.push(this.context[contextVar] === expectedValue);
                    }
                    continue;
                }

                const field = document.getElementById('id_' + sourceField);
                if (!field) {
                    results.push(false);
                    continue;
                }

                // Handle checkbox inputs
                const isCheckbox = field.type === 'checkbox';
                const value = isCheckbox ? field.checked : field.value;

                // Check checked_is (for checkboxes)
                if (checks.checked_is !== undefined) {
                    results.push(field.checked === checks.checked_is);
                    continue;  // Skip other checks for checkbox
                }

                // Check value_is
                if (checks.value_is !== undefined) {
                    results.push(value === checks.value_is);
                }

                // Check value_in
                if (checks.value_in !== undefined) {
                    results.push(checks.value_in.includes(value));
                }

                // Check value_not_in
                if (checks.value_not_in !== undefined) {
                    results.push(!checks.value_not_in.includes(value));
                }

                // Check metadata_is
                if (checks.metadata_is !== undefined) {
                    const metadata = this.getMetadata(field);
                    for (const [key, expected] of Object.entries(checks.metadata_is)) {
                        results.push(metadata[key] === expected);
                    }
                }

                // Check metadata_truthy
                if (checks.metadata_truthy !== undefined) {
                    const metadata = this.getMetadata(field);
                    const val = metadata[checks.metadata_truthy];
                    results.push(val === 'true' || val === 'True' || val === true);
                }
            }

            if (results.length === 0) return true;

            if (requireAll) {
                return results.every(r => r);
            } else {
                return results.some(r => r);
            }
        }

        getMetadata(field) {
            if (window.OptionMetadata) {
                return window.OptionMetadata.get(field);
            }
            // Fallback: read from selected option directly
            if (field.selectedOptions && field.selectedOptions.length > 0) {
                const option = field.selectedOptions[0];
                const metadata = {};
                for (const key in option.dataset) {
                    metadata[key] = option.dataset[key];
                }
                return metadata;
            }
            return {};
        }
    }

    window.ConditionalFields = new ConditionalFieldsManager();

    const init = () => window.ConditionalFields.init();

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
