document.addEventListener('DOMContentLoaded', function() {
    const powersCheckboxes = document.querySelectorAll('[name="powers"]');
    const dualNatureFields = document.querySelector('[name="dual_nature_archetype"]').closest('.form-group');
    const dualNatureAbility = document.querySelector('[name="dual_nature_ability"]').closest('.form-group');

    function updateDualNatureVisibility() {
        const selectedPowers = Array.from(powersCheckboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        const hasDualNature = selectedPowers.includes('dual_nature');
        dualNatureFields.style.display = hasDualNature ? 'block' : 'none';
        dualNatureAbility.style.display = hasDualNature ? 'block' : 'none';
    }

    powersCheckboxes.forEach(cb => {
        cb.addEventListener('change', updateDualNatureVisibility);
    });

    updateDualNatureVisibility();
});
