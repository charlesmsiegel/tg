(function () {
    'use strict';

    function init(root) {
        var section = root.querySelector('[data-linked-npc-form]');
        if (!section || section.dataset.ready) return;
        section.dataset.ready = '1';
        var select = section.querySelector('[name="npc_type"]');
        var groups = section.querySelectorAll('[data-npc-types], [data-npc-except]');

        function update() {
            var selected = select.value;
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
        update();
    }

    document.addEventListener('htmx:afterSwap', function (event) { init(event.target); });
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { init(document); });
    } else {
        init(document);
    }
})();
