/* Priority totals on the Attributes and Abilities steps.
 * Mage ranks are inferred from dots; other workflows can show PRI / SEC / TER.
 *
 * Markup: [data-priority] > [data-priority-group] columns, each with a
 * [data-priority-count] span and a [data-priority-picker] of three radios
 * (value primary/secondary/tertiary, data-target = the column total that rank
 * needs). The radios are ordinary form fields posted with the step; the server
 * validates against them. This script only:
 *  - swaps: choosing a rank another column holds gives that column the rank
 *    this one gave up, so the three ranks stay unique; the swapped radio fires
 *    change so validators recount;
 *  - keeps each column's "n left" / "done" / "n over" count current, against
 *    the chosen ranks (or, if they are not three distinct ranks, the ranking
 *    the dots imply, as the server does).
 * Plain script, safe with or without defer and more than once; listeners are
 * delegated, and htmx swaps are recounted after they settle.
 */
(function () {
    'use strict';
    if (window.TGPriority) return;

    var RADIO = 'input[type="radio"]';

    function columns(container) {
        return Array.prototype.slice.call(container.querySelectorAll('[data-priority-group]'));
    }

    function checked(column) {
        return column.querySelector('[data-priority-picker] ' + RADIO + ':checked');
    }

    function total(column) {
        var sum = 0;
        column.querySelectorAll('input[type="number"], select').forEach(function (field) {
            var value = parseInt(field.value, 10);
            if (!isNaN(value)) sum += value;
        });
        return sum;
    }

    /* {group: target}: the chosen ranks when all columns hold different ones,
     * otherwise the columns ranked by total (ties keep their order). */
    function targets(container) {
        var cols = columns(container);
        var picks = cols.map(checked);
        var values = picks.map(function (radio) { return radio ? radio.value : null; });
        var distinct = values.filter(function (value, i) {
            return value && values.indexOf(value) === i;
        });
        var result = {};
        if (distinct.length === cols.length) {
            cols.forEach(function (column, i) {
                result[column.dataset.priorityGroup] = Number(picks[i].dataset.target);
            });
            return result;
        }
        var totals = cols.map(total);
        var order = cols.map(function (_, i) { return i; }).sort(function (a, b) {
            return totals[b] - totals[a] || a - b;
        });
        order.forEach(function (index, rank) {
            var radios = cols[index].querySelectorAll('[data-priority-picker] ' + RADIO);
            if (radios[rank]) {
                result[cols[index].dataset.priorityGroup] = Number(radios[rank].dataset.target);
            } else {
                var head = cols[index].querySelector('[data-priority-targets]');
                if (head) result[cols[index].dataset.priorityGroup] = Number(head.dataset.priorityTargets.split(',')[rank]);
            }
        });
        return result;
    }

    function recount(container) {
        var goals = targets(container);
        var rankedGoals = columns(container).map(function (column) {
            return goals[column.dataset.priorityGroup];
        }).sort(function (a, b) { return b - a; });
        var ranks = ['Primary', 'Secondary', 'Tertiary'];
        columns(container).forEach(function (column) {
            var count = column.querySelector('[data-priority-count]');
            var goal = goals[column.dataset.priorityGroup];
            var rank = column.querySelector('[data-inferred-priority]');
            if (rank) rank.textContent = ranks[rankedGoals.indexOf(goal)] || '';
            if (!count || goal === undefined) return;
            var left = goal - total(column);
            count.textContent = left > 0 ? left + ' left' : left < 0 ? -left + ' over' : 'done';
            count.classList.toggle('is-done', left === 0);
            count.classList.toggle('is-over', left < 0);
        });
    }

    /* The rank this column gave up is the one no column holds now. */
    function swap(container, radio) {
        var own = radio.closest('[data-priority-group]');
        var cols = columns(container);
        var holder = cols.filter(function (column) {
            var pick = column !== own && checked(column);
            return pick && pick.value === radio.value;
        })[0];
        if (!holder) return;
        var held = cols.map(function (column) {
            var pick = checked(column);
            return pick ? pick.value : null;
        });
        var free = Array.prototype.slice.call(own.querySelectorAll(RADIO)).map(function (option) {
            return option.value;
        }).filter(function (value) { return held.indexOf(value) === -1; })[0];
        var replacement = free && holder.querySelector(RADIO + '[value="' + free + '"]');
        if (!replacement) return;
        replacement.checked = true;
        replacement.dispatchEvent(new Event('change', { bubbles: true }));
    }

    function containerOf(target) {
        return target && target.closest ? target.closest('[data-priority]') : null;
    }

    document.addEventListener('change', function (event) {
        var container = containerOf(event.target);
        if (!container) return;
        if (event.target.matches('[data-priority-picker] ' + RADIO)) swap(container, event.target);
        recount(container);
    });
    document.addEventListener('input', function (event) {
        var container = containerOf(event.target);
        if (container) recount(container);
    });

    function recountAll() {
        document.querySelectorAll('[data-priority]').forEach(recount);
    }
    document.addEventListener('htmx:afterSettle', recountAll);
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', recountAll);
    } else {
        recountAll();
    }

    window.TGPriority = { targets: targets, recount: recount };
})();
