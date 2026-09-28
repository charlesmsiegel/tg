// Show the Dual Nature fields (Spread .tl-field wrappers) only when that power is chosen.
document.addEventListener('DOMContentLoaded', function() {
    const powersCheckboxes = document.querySelectorAll('[name="powers"]');
    const wrapper = function(name) {
        const input = document.querySelector('[name="' + name + '"]');
        return input ? input.closest('.tl-field') : null;
    };
    const dualNatureFields = [wrapper('dual_nature_archetype'), wrapper('dual_nature_ability')].filter(Boolean);

    function updateDualNatureVisibility() {
        const hasDualNature = Array.from(powersCheckboxes).some(cb => cb.checked && cb.value === 'dual_nature');
        dualNatureFields.forEach(element => {
            element.style.display = hasDualNature ? '' : 'none';
        });
    }

    powersCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateDualNatureVisibility);
    });

    updateDualNatureVisibility();
});
