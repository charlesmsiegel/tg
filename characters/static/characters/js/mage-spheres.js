(function () {
    'use strict';
    var names = ['correspondence', 'time', 'spirit', 'forces', 'matter', 'life', 'entropy', 'mind', 'prime'];
    var budget = document.querySelector('[data-sphere-budget]');
    if (!budget) return;
    var form = budget.closest('form');
    if (!form) return;
    var count = budget.querySelector('[data-sphere-count]');
    var message = budget.querySelector('[data-sphere-message]');
    var save = form.querySelector('.tl-chargen__actions button[type="submit"]:not([formnovalidate])');

    function update() {
        var arete = Number(form.elements.arete.value);
        var ratings = names.map(function (name) { return Number(form.elements[name].value); });
        var total = ratings.reduce(function (sum, value) { return sum + value; }, 0);
        var affinity = form.elements.affinity_sphere.selectedOptions[0];
        var affinityName = affinity && affinity.value ? affinity.textContent.split(' (')[0].toLowerCase() : '';
        var affinityRating = names.indexOf(affinityName) >= 0
            ? ratings[names.indexOf(affinityName)] : 0;
        var validArete = Number.isInteger(arete) && arete >= 1 &&
            (budget.dataset.npc === 'true' || arete <= 3);
        var validRatings = ratings.every(function (value) {
            return Number.isInteger(value) && value >= 0 && value <= arete;
        });
        var ready = total === Number(budget.dataset.target) && validArete && validRatings &&
            affinityRating > 0 && form.elements.resonance.value.trim() !== '';
        count.textContent = total + ' / ' + budget.dataset.target;
        message.textContent = ready ? 'Ready to continue' :
            total !== 6 ? 'Place exactly six dots.' :
            !validArete || !validRatings ? 'Check Arete and Sphere ratings.' :
            !affinityRating ? 'Rate your Affinity Sphere.' : 'Choose Resonance.';
        if (save) save.disabled = !ready;
    }
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    update();
})();
