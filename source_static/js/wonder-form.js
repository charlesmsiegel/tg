/**
 * Wonder Form JavaScript
 *
 * Manages formset behavior for the Mage wonder creation form.
 * Handles effect field toggling, adding new resonance/effect forms,
 * and resetting effects formset based on wonder type.
 */

/**
 * Toggle visibility of effect fields based on select_or_create checkbox.
 *
 * @param {string} prefix - The formset prefix (e.g., "effects-0")
 */
function toggleEffectFields(prefix) {
    var subform = document.querySelector('[data-prefix="' + prefix + '"]');
    if (!subform) {
        return;
    }

    var selectCreateCheckbox = subform.querySelector('#id_' + prefix + '-select_or_create');
    var selectRow = subform.querySelector('.effect-select-row');
    var createFields = subform.querySelector('.effect-create-fields');

    if (!selectCreateCheckbox || !selectRow || !createFields) {
        return;
    }

    if (selectCreateCheckbox.checked) {
        selectRow.classList.add('d-none');
        createFields.classList.remove('d-none');
    } else {
        selectRow.classList.remove('d-none');
        createFields.classList.add('d-none');
    }
}

/**
 * Add a new form to a formset.
 *
 * @param {string} formsetPrefix - The formset prefix (e.g., "resonance" or "effects")
 */
function addFormsetForm(formsetPrefix) {
    var totalForms = document.getElementById('id_' + formsetPrefix + '-TOTAL_FORMS');
    var currentFormCount = parseInt(totalForms.value, 10);
    var emptyFormHtml = document.getElementById('empty_' + formsetPrefix + '_form').innerHTML;

    // Replace __prefix__ with the current form count
    var formHtml = emptyFormHtml.replace(/__prefix__/g, currentFormCount);

    totalForms.value = currentFormCount + 1;
    var container = document.getElementById(formsetPrefix + '_formset');
    container.insertAdjacentHTML('beforeend', formHtml);

    // The new prefix is "formsetPrefix-N"
    var newPrefix = formsetPrefix + '-' + currentFormCount;

    toggleEffectFields(newPrefix);

    // Attach event listener for the new form
    var newSubform = container.querySelector('[data-prefix="' + newPrefix + '"]');
    if (newSubform) {
        var checkbox = newSubform.querySelector('#id_' + newPrefix + '-select_or_create');
        if (checkbox) {
            checkbox.addEventListener('change', function() {
                toggleEffectFields(newPrefix);
            });
        }
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

    toggleEffectFields('effects-0');

    var checkbox = document.getElementById('id_effects-0-select_or_create');
    if (checkbox) {
        checkbox.addEventListener('change', function() {
            toggleEffectFields('effects-0');
        });
    }
}

/**
 * Initialize the wonder form on page load.
 */
function initWonderForm() {
    // Initialize existing effect forms
    document.querySelectorAll('.effect-subform').forEach(function(el) {
        var prefix = el.getAttribute('data-prefix');
        toggleEffectFields(prefix);

        var checkbox = el.querySelector('#id_' + prefix + '-select_or_create');
        if (checkbox) {
            checkbox.addEventListener('change', function() {
                toggleEffectFields(prefix);
            });
        }
    });

    // Add resonance forms button
    var addResonanceBtn = document.getElementById('add-resonance');
    if (addResonanceBtn) {
        addResonanceBtn.addEventListener('click', function() {
            addFormsetForm('resonance');
        });
    }

    // Add effect forms button
    var addPowerBtn = document.getElementById('add-power');
    if (addPowerBtn) {
        addPowerBtn.addEventListener('click', function() {
            addFormsetForm('effects');
        });
    }

    // Wonder type change handler - show/hide effects based on type
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
document.addEventListener('DOMContentLoaded', initWonderForm);
