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
    var sphereMap = {};
    try { sphereMap = JSON.parse(form.elements.affinity_sphere.dataset.sphereMap || '{}'); }
    catch (err) { /* The server still validates the form. */ }
    var updating = false;

    function setRating(input, value) {
        if (Number(input.value) === value && input.value !== '') return;
        input.value = String(value);
        var control = input.closest('[data-dot-rating]');
        if (control && window.TGDots) window.TGDots.paint(control);
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function update() {
        if (updating) return;
        updating = true;
        var arete = Number(form.elements.arete.value);
        var maxDots = Math.max(1, Math.min(5, arete || 1));
        var affinity = form.elements.affinity_sphere.selectedOptions[0];
        var affinityName = affinity ? sphereMap[affinity.value] : null;
        names.forEach(function (name) {
            var input = form.elements[name];
            var control = input.closest('[data-dot-rating]');
            var minimum = name === affinityName ? 1 : 0;
            input.min = String(minimum);
            if (control) {
                control.dataset.min = String(minimum);
                control.querySelectorAll('.tg-dot').forEach(function (dot) {
                    dot.hidden = Number(dot.dataset.value) > maxDots;
                });
            }
            if (Number(input.value) > maxDots) setRating(input, maxDots);
            if (minimum && Number(input.value) < 1) setRating(input, 1);
        });
        var ratings = names.map(function (name) { return Number(form.elements[name].value); });
        var total = ratings.reduce(function (sum, value) { return sum + value; }, 0);
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
        updating = false;
    }
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    update();
})();
