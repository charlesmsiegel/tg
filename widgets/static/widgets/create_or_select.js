(function() {
    'use strict';

    // Prevent double-initialization
    if (window.CreateOrSelect) return;

    class CreateOrSelectManager {
        constructor() {
            this.initialized = new WeakSet();
        }

        init() {
            document.querySelectorAll('[data-create-or-select-toggle]').forEach(toggle => {
                if (!this.initialized.has(toggle)) {
                    this.registerToggle(toggle);
                    this.initialized.add(toggle);
                }
            });
        }

        registerToggle(toggle) {
            const groupId = toggle.dataset.createOrSelectGroup;
            const selectContainer = document.querySelector(
                `[data-create-or-select-container="${groupId}"][data-create-or-select-mode="select"]`
            );
            const createContainer = document.querySelector(
                `[data-create-or-select-container="${groupId}"][data-create-or-select-mode="create"]`
            );

            if (!selectContainer || !createContainer) {
                console.warn(`CreateOrSelect: Missing containers for group "${groupId}"`);
                return;
            }

            // Store references on the toggle
            toggle._selectContainer = selectContainer;
            toggle._createContainer = createContainer;

            // Set initial state
            this.updateVisibility(toggle);

            // Listen for changes
            toggle.addEventListener('change', () => this.updateVisibility(toggle));
        }

        updateVisibility(toggle) {
            const selectContainer = toggle._selectContainer;
            const createContainer = toggle._createContainer;

            if (toggle.checked) {
                // Create mode: hide select, show create
                selectContainer.classList.add('d-none');
                createContainer.classList.remove('d-none');
            } else {
                // Select mode: show select, hide create
                selectContainer.classList.remove('d-none');
                createContainer.classList.add('d-none');
            }
        }

        // Programmatic toggle
        setMode(groupId, createMode) {
            const toggle = document.querySelector(
                `[data-create-or-select-toggle][data-create-or-select-group="${groupId}"]`
            );
            if (toggle) {
                toggle.checked = createMode;
                this.updateVisibility(toggle);
            }
        }

        getMode(groupId) {
            const toggle = document.querySelector(
                `[data-create-or-select-toggle][data-create-or-select-group="${groupId}"]`
            );
            return toggle ? toggle.checked : null;
        }
    }

    window.CreateOrSelect = new CreateOrSelectManager();

    const init = () => window.CreateOrSelect.init();

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
