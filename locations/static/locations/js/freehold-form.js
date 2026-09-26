// Dynamic form behavior for archetype-specific fields
document.addEventListener('DOMContentLoaded', function() {
    const archetypeField = document.querySelector('[name="archetype"]');
    const academyAbility = document.querySelector('[name="academy_ability"]').closest('.form-group');
    const hearthAbility = document.querySelector('[name="hearth_ability"]').closest('.form-group');
    const powersField = document.querySelector('[name="powers"]');
    const dualNatureArchetype = document.querySelector('[name="dual_nature_archetype"]').closest('.form-group');
    const dualNatureAbility = document.querySelector('[name="dual_nature_ability"]').closest('.form-group');

    function updateFieldVisibility() {
        const selectedArchetype = archetypeField.value;
        const selectedPowers = Array.from(document.querySelectorAll('[name="powers"]:checked')).map(cb => cb.value);

        // Show/hide archetype-specific fields
        academyAbility.style.display = selectedArchetype === 'academy' ? 'block' : 'none';
        hearthAbility.style.display = selectedArchetype === 'hearth' ? 'block' : 'none';

        // Show/hide dual nature fields
        const hasDualNature = selectedPowers.includes('dual_nature');
        dualNatureArchetype.style.display = hasDualNature ? 'block' : 'none';
        dualNatureAbility.style.display = hasDualNature ? 'block' : 'none';
    }

    archetypeField.addEventListener('change', updateFieldVisibility);
    if (powersField) {
        document.querySelectorAll('[name="powers"]').forEach(cb => {
            cb.addEventListener('change', updateFieldVisibility);
        });
    }

    updateFieldVisibility();
});
