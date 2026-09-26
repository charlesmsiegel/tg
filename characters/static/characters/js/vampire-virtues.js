document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    var statusEl = document.getElementById('virtues-validation-status');
    var form = statusEl && statusEl.closest('form');
    if (!form || !statusEl || !window.TG || !TG.validation) return;

    // Status only — submit stays enabled; the
    // server enforces the 7-dot total.
    // Vampire only; Demon's total is 6 — make this
    // context-driven when Demon chargen exists.
    var TARGET = 7;
    // Inactive virtues render as hidden inputs and don't count
    var SELECTOR = [
        '#id_conscience', '#id_conviction',
        '#id_self_control', '#id_instinct',
        '#id_courage'
    ].map(function(id) { return id + ':not([type="hidden"])'; }).join(', ');

    function activeInvalid() {
        // Each active virtue (Courage + the two
        // chosen pair members) must be a whole
        // number >= 1, per Vampire.clean() and
        // IntegerField. parseInt would truncate a
        // fractional value the server then rejects,
        // so check the raw value is an integer too.
        var fields = form.querySelectorAll(SELECTOR);
        return Array.prototype.some.call(fields, function(f) {
            var value = Number(f.value);
            var isInt = isFinite(value) && Math.floor(value) === value;
            return !isInt || value < 1;
        });
    }

    function validate() {
        var total = TG.validation.sumFields(form, SELECTOR);
        var invalid = activeInvalid();
        var valid = (total === TARGET) && !invalid;
        var message;
        if (valid) {
            message = 'Valid (' + total + '/' + TARGET + ')';
        } else if (invalid) {
            message = 'Each virtue must be a whole number of at least 1 (' + total + '/' + TARGET + ')';
        } else {
            message = total + '/' + TARGET + ' dots';
        }
        TG.validation.setStatus(statusEl, valid, message);
    }

    form.addEventListener('change', validate);
    form.addEventListener('input', validate);
    validate();
});
