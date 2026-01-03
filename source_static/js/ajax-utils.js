/**
 * AJAX Utility Functions for Safe DOM Manipulation
 *
 * These functions replace the jQuery .html() pattern with safe DOM manipulation
 * that uses textContent instead of innerHTML, preventing XSS vulnerabilities.
 */

/**
 * Populate a select element with options from a JSON response.
 *
 * @param {HTMLSelectElement|string} selectElement - The select element or its ID
 * @param {Array} options - Array of {value, label} objects
 * @param {string} [placeholder="---------"] - Placeholder option text
 *
 * Example usage:
 *   $.ajax({
 *       url: '/ajax/load-factions/',
 *       data: { affiliation: affiliationId },
 *       success: function(data) {
 *           populateDropdown('#id_faction', data.options);
 *       }
 *   });
 */
function populateDropdown(selectElement, options, placeholder) {
    placeholder = placeholder || '---------';

    // Handle both string ID and element reference
    var select = typeof selectElement === 'string'
        ? document.querySelector(selectElement)
        : selectElement;

    if (!select) {
        console.error('Select element not found:', selectElement);
        return;
    }

    // Clear existing options
    select.innerHTML = '';

    // Add placeholder option
    var placeholderOption = document.createElement('option');
    placeholderOption.value = '';
    placeholderOption.textContent = placeholder;
    select.appendChild(placeholderOption);

    // Add options from data
    options.forEach(function(item) {
        var option = document.createElement('option');
        option.value = item.value;
        option.textContent = item.label;
        // Add any extra attributes as data attributes
        for (var key in item) {
            if (key !== 'value' && key !== 'label') {
                option.dataset[key] = item[key];
            }
        }
        select.appendChild(option);
    });
}

/**
 * Populate a select element with simple values (value and label are the same).
 *
 * @param {HTMLSelectElement|string} selectElement - The select element or its ID
 * @param {Array} values - Array of values
 * @param {string} [placeholder="---------"] - Placeholder option text
 *
 * Example usage:
 *   $.ajax({
 *       url: '/ajax/load-values/',
 *       data: { example: exampleId },
 *       success: function(data) {
 *           populateDropdownFromValues('#id_value', data.values);
 *       }
 *   });
 */
/**
 * Get the poolable status of the currently selected background option.
 *
 * @param {HTMLSelectElement|string} selectElement - The select element or its ID
 * @returns {boolean} - True if the selected background is poolable, false otherwise
 *
 * Example usage:
 *   exampleSelectMenu.addEventListener("change", function() {
 *       if (categorySelectMenu.value === "New Background" && isGroupMember) {
 *           if (isSelectedOptionPoolable('#id_example')) {
 *               pooled_wrap.classList.remove("d-none");
 *           } else {
 *               pooled_wrap.classList.add("d-none");
 *           }
 *       }
 *   });
 */
function isSelectedOptionPoolable(selectElement) {
    var select = typeof selectElement === 'string'
        ? document.querySelector(selectElement)
        : selectElement;

    if (!select || !select.selectedOptions || select.selectedOptions.length === 0) {
        return true;  // Default to poolable if no selection
    }

    var selectedOption = select.selectedOptions[0];
    // If poolable attribute is not set, default to true (poolable)
    if (selectedOption.dataset.poolable === undefined) {
        return true;
    }
    return selectedOption.dataset.poolable === 'true' || selectedOption.dataset.poolable === 'True';
}

function populateDropdownFromValues(selectElement, values, placeholder) {
    placeholder = placeholder || '---------';

    // Handle both string ID and element reference
    var select = typeof selectElement === 'string'
        ? document.querySelector(selectElement)
        : selectElement;

    if (!select) {
        console.error('Select element not found:', selectElement);
        return;
    }

    // Clear existing options
    select.innerHTML = '';

    // Add placeholder option
    var placeholderOption = document.createElement('option');
    placeholderOption.value = '';
    placeholderOption.textContent = placeholder;
    select.appendChild(placeholderOption);

    // Add options from values
    values.forEach(function(value) {
        var option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        select.appendChild(option);
    });
}
