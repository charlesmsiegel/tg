// Dynamic form behavior for archetype-specific fields.
// Each field sits in a Spread .tl-field wrapper; a field the form renders as a hidden
// input has no wrapper and is left alone.
document.addEventListener('DOMContentLoaded', function() {
    const archetypeField = document.querySelector('[name="archetype"]');
    if (!archetypeField) {
        return;
    }
    const wrapper = function(name) {
        const input = document.querySelector('[name="' + name + '"]');
        return input ? input.closest('.tl-field') : null;
    };
    const academyAbility = wrapper('academy_ability');
    const hearthAbility = wrapper('hearth_ability');
    const dualNatureArchetype = wrapper('dual_nature_archetype');
    const dualNatureAbility = wrapper('dual_nature_ability');
    const show = function(element, visible) {
        if (element) {
            element.style.display = visible ? '' : 'none';
        }
    };

    function updateFieldVisibility() {
        const selectedArchetype = archetypeField.value;
        const selectedPowers = Array.from(document.querySelectorAll('[name="powers"]:checked')).map(cb => cb.value);

        // Show/hide archetype-specific fields
        show(academyAbility, selectedArchetype === 'academy');
        show(hearthAbility, selectedArchetype === 'hearth');

        // Show/hide dual nature fields
        const hasDualNature = selectedPowers.includes('dual_nature');
        show(dualNatureArchetype, hasDualNature);
        show(dualNatureAbility, hasDualNature);
    }

    archetypeField.addEventListener('change', updateFieldVisibility);
    document.querySelectorAll('[name="powers"]').forEach(cb => {
        cb.addEventListener('change', updateFieldVisibility);
    });

    updateFieldVisibility();
});
