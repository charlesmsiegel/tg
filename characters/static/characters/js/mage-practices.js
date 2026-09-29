(function () {
    'use strict';
    var source = document.getElementById('mage-practice-limits');
    var budget = document.querySelector('[data-practice-budget]');
    if (!source || !budget) return;
    var limits = JSON.parse(source.textContent);
    var form = budget.closest('form');
    var count = budget.querySelector('[data-practice-count]');

    function rows() {
        return Array.prototype.slice.call(form.querySelectorAll('select[name$="-practice"]')).map(function (select) {
            var prefix = select.name.slice(0, -'practice'.length);
            return { practice: select, rating: form.elements.namedItem(prefix + 'rating') };
        }).filter(function (row) { return row.rating; });
    }

    function update() {
        var total = 0;
        rows().forEach(function (row) {
            var max = Number(limits[row.practice.value] || 0);
            var control = row.rating.closest('[data-dot-rating]');
            row.rating.max = String(max);
            if (control) {
                control.dataset.max = String(max);
                control.querySelectorAll('.tg-dot').forEach(function (dot) {
                    dot.hidden = Number(dot.dataset.value) > max;
                });
            }
            if (Number(row.rating.value) > max) {
                row.rating.value = String(max);
                row.rating.dispatchEvent(new Event('input', { bubbles: true }));
            }
            total += Number(row.rating.value) || 0;
        });
        count.textContent = total + ' / ' + budget.dataset.target;
    }
    form.addEventListener('input', update);
    form.addEventListener('change', update);
    document.addEventListener('formset:added', function (event) {
        if (window.TGDots) window.TGDots.enhance(event.detail.form);
        update();
    });
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', update);
    } else {
        update();
    }
})();
