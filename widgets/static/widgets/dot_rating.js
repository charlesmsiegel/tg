/* Clickable dots over a number input, without Alpine (widgets.widgets.dots,
 * alpine=False). The same control as the Alpine tgDots component on interactive
 * pages: the number input stays the form field; the dots drive it.
 *
 * Markup: [data-dot-rating][data-min][data-max] > input + .tg-dot-buttons[hidden]
 * > button.tg-dot[data-value]. Enhancing hides the input and shows the dots.
 * Clicking dot n sets the rating to n, or one lower when n is the current top
 * dot, clamped to data-min..data-max; it fires input + change so running totals
 * and validators update. Typing into the input (or a script setting it and
 * firing input/change) repaints the dots.
 *
 * Plain script, safe with or without defer and more than once; listeners are
 * delegated, and controls swapped in by htmx are enhanced after the swap.
 */
(function () {
    'use strict';
    if (window.TGDots) return;

    var CONTROL = '[data-dot-rating]';

    function parts(control) {
        return {
            input: control.querySelector('input'),
            group: control.querySelector('.tg-dot-buttons'),
            dots: Array.prototype.slice.call(control.querySelectorAll('.tg-dot'))
        };
    }

    function rating(input) {
        var value = parseInt(input.value, 10);
        return isNaN(value) ? 0 : value;
    }

    function paint(control) {
        var p = parts(control);
        if (!p.input) return;
        var value = rating(p.input);
        p.dots.forEach(function (dot) {
            var n = Number(dot.dataset.value);
            dot.classList.toggle('is-filled', n <= value);
            dot.setAttribute('aria-pressed', n === value ? 'true' : 'false');
        });
    }

    function enhance(root) {
        var scope = root && root.querySelectorAll ? root : document;
        var controls = Array.prototype.slice.call(scope.querySelectorAll(CONTROL));
        if (scope.matches && scope.matches(CONTROL)) controls.push(scope);
        controls.forEach(function (control) {
            if (control.dataset.dotsReady) return;
            var p = parts(control);
            if (!p.input || !p.group) return;
            control.dataset.dotsReady = '1';
            p.input.hidden = true;
            p.group.hidden = false;
            paint(control);
        });
    }

    function pick(control, dot) {
        var p = parts(control);
        var min = Number(control.dataset.min) || 0;
        var max = Number(control.dataset.max) || 5;
        var current = rating(p.input);
        var next = dot === current ? dot - 1 : dot;
        next = Math.max(min, Math.min(max, next));
        p.input.value = String(next);
        paint(control);
        p.input.dispatchEvent(new Event('input', { bubbles: true }));
        p.input.dispatchEvent(new Event('change', { bubbles: true }));
    }

    document.addEventListener('click', function (event) {
        var dot = event.target.closest ? event.target.closest('.tg-dot') : null;
        var control = dot && dot.closest(CONTROL);
        if (!control || !control.dataset.dotsReady) return;
        event.preventDefault();
        pick(control, Number(dot.dataset.value));
    });

    function repaint(event) {
        var control = event.target.closest ? event.target.closest(CONTROL) : null;
        if (control && event.target.tagName === 'INPUT') paint(control);
    }
    document.addEventListener('input', repaint);
    document.addEventListener('change', repaint);

    document.addEventListener('htmx:afterSwap', function (event) { enhance(event.target); });
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () { enhance(document); });
    } else {
        enhance(document);
    }

    window.TGDots = { enhance: enhance, paint: paint };
})();
