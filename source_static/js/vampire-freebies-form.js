/**
 * Vampire Freebies Form JavaScript
 *
 * Manages the freebie point spending form for Vampire characters.
 * Handles category selection, AJAX loading of examples and values,
 * and conditional visibility of form fields.
 */

/**
 * Initialize the vampire freebies form on page load.
 *
 * Configuration is read from data attributes on #freebies-form:
 *   data-load-examples-url: URL for loading examples based on category
 *   data-load-values-url: URL for loading values for merits/flaws
 *   data-object-id: The character object ID
 *   data-is-group-member: Whether the character is a group member ("true"/"false")
 */
function initVampireFreebiesForm() {
    var form = document.getElementById('freebies-form');
    if (!form) {
        return;
    }

    var categorySelectMenu = document.getElementById('id_category');
    var exampleSelectMenu = document.getElementById('id_example');
    var exampleElement = document.getElementById('example_wrap');
    var valueElement = document.getElementById('value_wrap');
    var noteElement = document.getElementById('note_wrap');
    var pooledWrap = document.getElementById('pooled_wrap');

    if (!categorySelectMenu || !exampleSelectMenu) {
        return;
    }

    // Read configuration from data attributes
    var loadExamplesUrl = form.dataset.loadExamplesUrl;
    var loadValuesUrl = form.dataset.loadValuesUrl;
    var objectId = form.dataset.objectId;
    var isGroupMember = form.dataset.isGroupMember === 'true';

    categorySelectMenu.addEventListener('change', function() {
        var selectedValue = this.value;

        // Update visibility based on category
        if (['Willpower', '-----', 'Humanity', 'Path Rating'].includes(selectedValue)) {
            exampleElement.classList.add('d-none');
            valueElement.classList.add('d-none');
            noteElement.classList.add('d-none');
            pooledWrap.classList.add('d-none');
        } else {
            exampleElement.classList.remove('d-none');
            valueElement.classList.add('d-none');
            noteElement.classList.add('d-none');
            pooledWrap.classList.add('d-none');
        }
        if (selectedValue === 'MeritFlaw') {
            valueElement.classList.remove('d-none');
            noteElement.classList.add('d-none');
            pooledWrap.classList.add('d-none');
        }
        if (selectedValue === 'Background') {
            exampleElement.classList.remove('d-none');
            noteElement.classList.remove('d-none');
            valueElement.classList.add('d-none');
            if (isGroupMember) {
                pooledWrap.classList.remove('d-none');
            } else {
                pooledWrap.classList.add('d-none');
            }
        }

        // Make the AJAX call to load examples
        $.ajax({
            url: loadExamplesUrl,
            data: {
                'category': selectedValue,
                'object': objectId
            },
            success: function(data) {
                populateDropdown('#id_example', data.options);
                populateDropdownFromValues('#id_value', []);
            }
        });
    });

    exampleSelectMenu.addEventListener('change', function() {
        var selectedValue = this.value;
        if (categorySelectMenu.value === 'MeritFlaw') {
            $.ajax({
                url: loadValuesUrl,
                data: {
                    'example': selectedValue,
                    'object': objectId
                },
                success: function(data) {
                    populateDropdownFromValues('#id_value', data.values);
                }
            });
        }
        // Hide pooled checkbox for non-poolable backgrounds
        if (categorySelectMenu.value === 'Background' && isGroupMember) {
            if (isSelectedOptionPoolable('#id_example')) {
                pooledWrap.classList.remove('d-none');
            } else {
                pooledWrap.classList.add('d-none');
            }
        }
    });
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initVampireFreebiesForm);
