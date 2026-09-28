document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    var statusEl = document.getElementById('abilities-validation-status');
    var form = statusEl && statusEl.closest('form');
    if (!form || !statusEl || !window.TG || !TG.validation) return;

    var targetsLabel = [statusEl.dataset.primary, statusEl.dataset.secondary, statusEl.dataset.tertiary].join('/');
    var TARGETS = [Number(statusEl.dataset.tertiary), Number(statusEl.dataset.secondary), Number(statusEl.dataset.primary)].sort(function(a, b) { return a - b; });

    // Ability rows lay out three .dots cells per row: Talents, Skills,
    // Knowledges. The grid is static, so grouping the inputs once here
    // (not re-querying on each validate) is intentional. Group by column. The length-3
    // guard is sufficient because this include renders only on the
    // ability step, where the attribute block shows as a display (no
    // inputs) — input-bearing three-cell rows are the ability grid.
    var groups = [[], [], []];
    // Spread steps mark each column ([data-ability-group], chargen/abilities.html).
    var columns = form.querySelectorAll('[data-ability-group]');
    if (columns.length === 3) {
        Array.prototype.forEach.call(columns, function(column, i) {
            groups[i] = Array.prototype.slice.call(
                column.querySelectorAll('input:not([type="radio"]), select')
            );
        });
    } else {
        Array.prototype.forEach.call(form.querySelectorAll('.row'), function(row) {
            var cells = row.querySelectorAll(':scope > .dots');
            if (cells.length !== 3) return;
            for (var i = 0; i < 3; i++) {
                var input = cells[i].querySelector('input, select');
                if (input) groups[i].push(input);
            }
        });
    }
    // Optional status tag beside the message (Spread steps): IN PROGRESS / TOO MANY / READY.
    var tag = form.querySelector('[data-allocation-tag]');
    var TARGET_SUM = TARGETS.reduce(function(a, b) { return a + b; }, 0);
    if (!groups[0].length) return;

    // Each ability is capped at 3 dots in chargen (HumanAbilityView
    // form_valid rejects ratings above 3), but the rendered inputs allow
    // higher values, so the client must enforce the cap too.
    var MAX_RATING = 3;

    // Parallel to TG.validation.sumFields but takes a pre-grouped array of
    // inputs (not a selector), so it can't delegate to that helper.
    function groupTotal(group) {
        var total = 0;
        group.forEach(function(field) {
            var value = parseInt(field.value, 10);
            if (!isNaN(value)) total += value;
        });
        return total;
    }

    // Every ability must be a whole number in 0..MAX_RATING. The server
    // (HumanAbilityView.form_valid and variants) rejects values below 0 or
    // above 3, and IntegerField rejects fractions, so checking only the
    // category totals would let an out-of-range value pass the client.
    // Detection only — the client never clamps/mutates the input value.
    function anyOutOfRange() {
        return groups.some(function(group) {
            return group.some(function(field) {
                // The ModelForm field is required, so a cleared input is
                // invalid even if other ratings offset the category total.
                var raw = field.value.trim();
                if (raw === '') return true;
                var value = Number(raw);
                var isInt = isFinite(value) && Math.floor(value) === value;
                return !isInt || value < 0 || value > MAX_RATING;
            });
        });
    }

    // Each column's target from its PRI / SEC / TER choice (the radio's
    // data-target), or null when there is no picker or its ranks are not three
    // different ones: then any order of the targets will do, as on the server.
    function chosenTargets() {
        if (columns.length !== 3) return null;
        var ranks = [];
        var targets = Array.prototype.map.call(columns, function(column) {
            var radio = column.querySelector('[data-priority-picker] input[type="radio"]:checked');
            if (!radio) return null;
            ranks.push(radio.value);
            return Number(radio.dataset.target);
        });
        var unique = ranks.filter(function(rank, i) { return ranks.indexOf(rank) === i; });
        return unique.length === 3 && targets.indexOf(null) === -1 ? targets : null;
    }

    function validate() {
        var columnTotals = groups.map(groupTotal);
        var totals = columnTotals.slice().sort(function(a, b) { return a - b; });
        var outOfRange = anyOutOfRange();
        var chosen = chosenTargets();
        var totalsMatch = chosen
            ? columnTotals.every(function(t, i) { return t === chosen[i]; })
            : totals.every(function(t, i) { return t === TARGETS[i]; });
        var valid = !outOfRange && totalsMatch;
        var message;
        if (valid) {
            message = 'Valid (' + targetsLabel + ')';
        } else if (outOfRange) {
            message = 'Each ability must be a whole number from 0 to ' + MAX_RATING;
        } else {
            message = 'Distribute ' + targetsLabel + ' dots across categories (currently ' + totals.slice().reverse().join('/') + ')';
            if (chosen) {
                message = 'Distribute ' + targetsLabel + ' dots as ranked (currently ' + columnTotals.join('/') + ')';
            }
        }
        TG.validation.setStatus(statusEl, valid, message);
        if (tag) {
            var over = !valid && (totals.reduce(function(a, b) { return a + b; }, 0) > TARGET_SUM ||
                (chosen && columnTotals.some(function(t, i) { return t > chosen[i]; })));
            tag.textContent = valid ? 'Ready' : over ? 'Too many' : 'In progress';
            tag.classList.toggle('is-ready', valid);
            tag.classList.toggle('is-over', over);
        }
        // Abilities block submit until the distribution is valid; the
        // backgrounds/virtues counters are status-only by design.
        TG.validation.setSubmitEnabled(form, valid);
    }

    form.addEventListener('change', validate);
    form.addEventListener('input', validate);
    validate();
});
