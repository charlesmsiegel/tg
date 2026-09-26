(function() {
    'use strict';

    /**
     * Toggle visibility of effect fields based on select_or_create checkbox.
     */
    function toggleEffectFields(prefix) {
        var subform = document.querySelector('[data-prefix="' + prefix + '"]');
        if (!subform) return;

        var selectCreateCheckbox = subform.querySelector('#id_' + prefix + '-select_or_create');
        var selectRow = subform.querySelector('.effect-select-row');
        var createFields = subform.querySelector('.effect-create-fields');

        if (!selectCreateCheckbox || !selectRow || !createFields) return;

        if (selectCreateCheckbox.checked) {
            selectRow.classList.add('d-none');
            createFields.classList.remove('d-none');
        } else {
            selectRow.classList.remove('d-none');
            createFields.classList.add('d-none');
        }
    }

    /**
     * Initialize effect form toggle for a subform.
     */
    function initEffectSubform(subform) {
        var prefix = subform.getAttribute('data-prefix');
        if (!prefix) return;

        toggleEffectFields(prefix);

        var checkbox = subform.querySelector('#id_' + prefix + '-select_or_create');
        if (checkbox) {
            checkbox.addEventListener('change', function() {
                toggleEffectFields(prefix);
            });
        }
    }

    /**
     * Reset the effects formset to a single empty form.
     */
    function resetEffectsFormset() {
        var totalForms = document.getElementById('id_effects-TOTAL_FORMS');
        var effectsContainer = document.getElementById('effects_formset');
        var emptyFormHtml = document.getElementById('empty_effects_form').innerHTML;

        effectsContainer.innerHTML = '';
        var newFormHtml = emptyFormHtml.replace(/__prefix__/g, 0);
        effectsContainer.insertAdjacentHTML('beforeend', newFormHtml);

        totalForms.value = 1;

        var newSubform = effectsContainer.querySelector('.effect-subform');
        if (newSubform) {
            initEffectSubform(newSubform);
        }

        // Re-register with FormsetManager
        if (window.FormsetManager) {
            window.FormsetManager.init();
        }
    }

    /**
     * Initialize the wonder form on page load.
     */
    function initWonderForm() {
        // Initialize existing effect forms
        document.querySelectorAll('.effect-subform').forEach(initEffectSubform);

        // Listen for new effects being added via FormsetManager
        document.addEventListener('formset:added', function(e) {
            if (e.detail.prefix === 'effects') {
                var newSubform = e.detail.form;
                if (newSubform) {
                    initEffectSubform(newSubform);
                }
            }
        });

        // Wonder type change handler - show/hide effects add button based on type
        var wonderTypeSelect = document.getElementById('id_wonder_type');
        var wonderEffectAdd = document.getElementById('add-power');
        if (wonderTypeSelect && wonderEffectAdd) {
            wonderTypeSelect.addEventListener('change', function() {
                var selectedValue = this.value;
                if (['artifact', 'charm'].includes(selectedValue)) {
                    wonderEffectAdd.classList.add('d-none');
                    resetEffectsFormset();
                } else {
                    wonderEffectAdd.classList.remove('d-none');
                }
            });
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWonderForm);
    } else {
        initWonderForm();
    }
})();
