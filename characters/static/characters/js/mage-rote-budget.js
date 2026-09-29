(function () {
    'use strict';
    var budget = document.querySelector('[data-rote-budget]');
    if (!budget) return;
    var form = budget.closest('form');
    if (!form) return;
    var preview = budget.querySelector('[data-rote-preview]');
    var remaining = budget.querySelector('[data-rote-remaining]');
    var spheres = ['correspondence', 'time', 'spirit', 'matter', 'life', 'forces', 'entropy', 'mind', 'prime'];
    var roteCosts = JSON.parse(budget.dataset.roteCosts || '{}');
    var effectCosts = JSON.parse(budget.dataset.effectCosts || '{}');
    var available = Number(budget.dataset.available);

    function cost() {
        if (!form.elements.select_or_create_rote.checked) {
            return roteCosts[form.elements.rote_options.value] ?? null;
        }
        if (!form.elements.select_or_create_effect.checked) {
            return effectCosts[form.elements.effect_options.value] ?? null;
        }
        var total = spheres.reduce(function (sum, name) {
            return sum + (Number(form.elements[name].value) || 0);
        }, 0);
        return total > 0 ? total : null;
    }

    function update() {
        var selectedCost = cost();
        preview.hidden = selectedCost === null;
        if (selectedCost !== null) remaining.textContent = String(available - selectedCost);
    }
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    update();
})();
