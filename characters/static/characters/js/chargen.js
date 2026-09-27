/* htmx glue for interactive character creation.
 *
 * The server decides everything (step, verdict, totals, options, visibility);
 * this file only keeps the swaps safe and accessible:
 *  - swap a response only if its TG-Fragment header is what the requesting
 *    element expects (data-tg-expect); otherwise load the URL as a full page
 *    (expired session, error page, a step that left the wizard);
 *  - drop validation/option responses that belong to a step no longer shown,
 *    and option responses for chain values the player has since changed
 *    (a validation still in flight when the step is saved; htmx resolved its
 *    target when it started, and never starts requests from removed elements);
 *  - move focus to the errors or the new step heading after a step swap.
 */
(function () {
    'use strict';
    if (window.TGChargen) return;

    function expectation(elt) {
        var holder = elt && elt.closest ? elt.closest('[data-tg-expect]') : null;
        return holder ? holder.getAttribute('data-tg-expect') : null;
    }

    function currentStep() {
        var form = document.getElementById('chargen-step');
        return form ? form.getAttribute('data-step') : null;
    }

    /* Options answer for the chain values they were computed from (TG-Chain);
     * if any of those selects changed since, a newer request owns the chain. */
    function chainStillMatches(header) {
        if (!header) return true;
        var form = document.getElementById('chargen-step');
        var expected = JSON.parse(header);
        return Object.keys(expected).every(function (name) {
            var field = form && form.elements.namedItem(name);
            return !!field && field.value === expected[name];
        });
    }

    document.addEventListener('htmx:beforeSwap', function (evt) {
        var detail = evt.detail;
        var source = detail.requestConfig && detail.requestConfig.elt;
        var wanted = expectation(source);
        if (!wanted) return;
        var received = detail.xhr.getResponseHeader('TG-Fragment');
        if (received === wanted) {
            if (wanted === 'chargen-step') return;
            var stale = !document.body.contains(source) ||
                detail.xhr.getResponseHeader('TG-Step') !== currentStep() ||
                !chainStillMatches(detail.xhr.getResponseHeader('TG-Chain'));
            if (stale) detail.shouldSwap = false;
            return;
        }
        detail.shouldSwap = false;
        if (wanted === 'chargen-step') {
            window.location.assign(detail.xhr.responseURL || window.location.href);
        }
    });

    document.addEventListener('htmx:afterSettle', function (evt) {
        var source = evt.detail.requestConfig && evt.detail.requestConfig.elt;
        if (expectation(source) !== 'chargen-step') return;
        var form = document.getElementById('chargen-step');
        if (!form) return;
        var target = form.querySelector('#chargen-errors') ||
            document.getElementById('chargen-step-heading');
        if (target) target.focus();
    });

    window.TGChargen = { expectation: expectation, currentStep: currentStep };
})();
