/* Spend XP (Spread M8): keep the htmx swaps of #xp-spend-fields safe.
 *
 * Each select asks the page for the next select's options and the preview; the
 * server answers with the "xp-spend" fragment (TG-Fragment header). Any other
 * answer (a login page after the session expired, an error, a permission change)
 * loads that URL as a whole page instead of landing inside the form.
 */
(function () {
    'use strict';
    if (window.TGXPSpend) return;
    window.TGXPSpend = true;

    document.addEventListener('htmx:beforeSwap', function (event) {
        var detail = event.detail;
        var source = detail.requestConfig && detail.requestConfig.elt;
        var holder = source && source.closest ? source.closest('[data-tg-expect="xp-spend"]') : null;
        if (!holder) return;
        if (detail.xhr.getResponseHeader('TG-Fragment') === 'xp-spend') return;
        detail.shouldSwap = false;
        window.location.assign(detail.xhr.responseURL || window.location.href);
    });
})();
