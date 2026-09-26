document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    var statusEl = document.getElementById('backgrounds-validation-status');
    var form = statusEl && statusEl.closest('form');
    if (!form || !statusEl || !window.TG || !TG.validation) return;

    var BUDGET = Number(statusEl.dataset.budget);
    // Some backgrounds (Enhancements, Sanctum, Totem...) cost more per dot.
    // background_multipliers (from the view) maps every selectable
    // background's pk to its multiplier — not just the allowed subset —
    // because the formset add-row can select any background. pk and
    // multiplier are both integers; json_script transports the serialized map.

    // Built from all backgrounds; only empty on an unseeded table, in which
    // case costs fall back to 1/dot (the server still enforces the budget).

    var MULTIPLIERS = JSON.parse(JSON.parse(document.getElementById('background-multipliers').textContent));

    // BackgroundRatingForm's rating is an IntegerField clamped to 0..5, so a
    // negative or fractional rating is rejected server-side; the counter must
    // treat such a row as invalid rather than folding it into the total.
    var RATING_MIN = 0;
    var RATING_MAX = 5;

    function validate() {
        var total = 0;
        var outOfRange = false;
        Array.prototype.forEach.call(form.querySelectorAll('select[name$="-bg"]'), function(select) {
            if (select.name.indexOf('__prefix__') !== -1) return;  // hidden empty-form template
            // A rating with no background chosen can't be saved (bg is
            // required), so it must not count toward the total.
            if (!select.value) return;
            var prefix = select.name.replace(/-bg$/, '');
            var deleteBox = form.querySelector('input[name="' + prefix + '-DELETE"]');
            if (deleteBox && deleteBox.checked) return;
            var ratingInput = form.querySelector('input[name="' + prefix + '-rating"]');
            if (!ratingInput) return;
            var raw = ratingInput.value.trim();
            if (raw === '') {
                // A selected background requires a rating (form field is
                // required); a blank rating can't save, so mark invalid.
                outOfRange = true;
                return;
            }
            var rating = Number(raw);
            var isInt = isFinite(rating) && Math.floor(rating) === rating;
            if (!isInt || rating < RATING_MIN || rating > RATING_MAX) {
                outOfRange = true;
                return;
            }
            var multiplier = MULTIPLIERS[select.value] || 1;
            total += rating * multiplier;
        });
        // Counter only — submit stays enabled (unlike abilities) so players
        // can save partial progress; the server still enforces the budget.
        var valid = !outOfRange && (total === BUDGET);
        var message;
        if (outOfRange) {
            message = 'Each rating must be a whole number from ' + RATING_MIN + ' to ' + RATING_MAX;
        } else if (valid) {
            message = 'Valid (' + total + '/' + BUDGET + ' points)';
        } else if (total > BUDGET) {
            message = (total - BUDGET) + ' point(s) over budget (' + total + '/' + BUDGET + ')';
        } else {
            message = (BUDGET - total) + ' point(s) remaining (' + total + '/' + BUDGET + ')';
        }
        TG.validation.setStatus(statusEl, valid, message);
    }

    form.addEventListener('change', validate);
    form.addEventListener('input', validate);
    // The dynamic formset's Remove button deletes the row and fires
    // formset:removed on document without an input/change event, so the
    // counter would otherwise keep the removed row's dots in the total.
    // (Dispatched on `document` by widgets/widgets/formset_manager.py.)
    // Assumes the backgrounds step renders a single formset; re-validating
    // on any formset removal is harmless since validate() rescans bg rows.
    document.addEventListener('formset:removed', validate);
    validate();
});
