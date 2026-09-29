(function () {
    'use strict';

    function init(root) {
        var section = root.querySelector('[data-linked-npc-form]');
        if (!section || section.dataset.ready) return;
        section.dataset.ready = '1';
        var select = section.querySelector('[name="npc_type"]');
        var details = section.querySelector('[data-linked-npc-details]');
        var groups = section.querySelectorAll('[data-npc-types], [data-npc-except]');
        var feraBreeds = JSON.parse(section.dataset.feraBreeds || '{}');
        var factionParents = JSON.parse(section.dataset.factionParents || '{}');
        var feraType = section.querySelector('[name="fera_type"]');
        var feraBreed = section.querySelector('[name="fera_breed"]');
        var affiliation = section.querySelector('[name="affiliation"]');
        var faction = section.querySelector('[name="faction"]');
        var subfaction = section.querySelector('[name="subfaction"]');

        function filterOptions(field, allowed) {
            if (!field) return;
            Array.from(field.options).forEach(function (option) {
                var available = !option.value || allowed.includes(option.value);
                option.hidden = !available;
                option.disabled = !available;
            });
            if (field.value && !allowed.includes(field.value)) field.value = '';
        }

        function updateFeraBreeds() {
            if (feraType && feraBreed) filterOptions(feraBreed, feraBreeds[feraType.value] || []);
        }

        function updateSubfactions() {
            if (faction && subfaction) {
                filterOptions(subfaction, Object.keys(factionParents).filter(function (id) {
                    return !!faction.value && factionParents[id] === faction.value;
                }));
            }
        }

        function updateFactions() {
            if (affiliation && faction) {
                filterOptions(faction, Object.keys(factionParents).filter(function (id) {
                    return !!affiliation.value && factionParents[id] === affiliation.value;
                }));
            }
            updateSubfactions();
        }

        function update() {
            var selected = select.value;
            details.hidden = !selected;
            groups.forEach(function (group) {
                var types = (group.dataset.npcTypes || '').split(' ');
                var excluded = (group.dataset.npcExcept || '').split(' ');
                var visible = !!selected && (group.dataset.npcTypes
                    ? types.includes(selected) : !excluded.includes(selected));
                group.hidden = !visible;
                group.querySelectorAll('input, select, textarea').forEach(function (field) {
                    field.disabled = !visible;
                });
            });
        }

        select.addEventListener('change', update);
        if (feraType) feraType.addEventListener('change', updateFeraBreeds);
        if (affiliation) affiliation.addEventListener('change', updateFactions);
        if (faction) faction.addEventListener('change', updateSubfactions);
        updateFeraBreeds();
        updateFactions();
        update();
    }

    document.addEventListener('htmx:afterSwap', function (event) { init(event.target); });
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { init(document); });
    } else {
        init(document);
    }
})();
