window.TG = window.TG || {};
TG.validation = {
    /* Set text and color (green/red) on a status element. */
    setStatus: function(el, valid, message) {
        if (!el) return;
        el.textContent = message;
        el.style.color = valid ? 'var(--color-success, #28a745)' : 'var(--color-danger, #dc3545)';
    },
    /* Enable/disable the form's main submit button (not Back/Cancel). */
    setSubmitEnabled: function(form, enabled) {
        if (!form) return;
        var buttons = form.querySelectorAll(
            'button[type="submit"]:not([formaction]), input[type="submit"]:not([formaction])'
        );
        Array.prototype.forEach.call(buttons, function(btn) {
            btn.disabled = !enabled;
        });
    },
    /* Sum integer values of inputs/selects matching selector.
       Status display only: parseInt truncates fractionals, so
       callers gating validity must reject non-integers
       separately rather than trust this total. */
    sumFields: function(form, selector) {
        if (!form) return 0;
        var total = 0;
        Array.prototype.forEach.call(form.querySelectorAll(selector), function(field) {
            var value = parseInt(field.value, 10);
            if (!isNaN(value)) total += value;
        });
        return total;
    },
    /* Count checked checkboxes matching selector.
       Not used yet; part of the shared API for upcoming
       chargen step validations (e.g. merit/flaw pickers). */
    countChecked: function(form, selector) {
        if (!form) return 0;
        var count = 0;
        Array.prototype.forEach.call(form.querySelectorAll(selector), function(box) {
            if (box.checked) count += 1;
        });
        return count;
    }
};
