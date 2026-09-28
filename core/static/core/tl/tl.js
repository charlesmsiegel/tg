/* Tellurium "Spread" helpers. No dependencies; safe to load with defer. */
(function () {
  'use strict';

  // 1. Fit oversized cover titles (README: "Long words in cover titles").
  //    The server already picked a size step; this only shrinks further when a
  //    long word still overflows, then falls back to wrapping anywhere.
  function fitTitles() {
    document.querySelectorAll('[data-fit-title]').forEach(function (el) {
      el.style.fontSize = '';
      if (!el.dataset.base) el.dataset.base = parseFloat(getComputedStyle(el).fontSize);
      var size = +el.dataset.base;
      var min = Math.max(34, Math.round(size * 0.5));
      el.style.fontSize = size + 'px';
      el.style.overflowWrap = 'normal';
      el.style.hyphens = 'manual';
      while (el.scrollWidth > el.clientWidth + 1 && size > min) {
        size -= 2;
        el.style.fontSize = size + 'px';
      }
      if (el.scrollWidth > el.clientWidth + 1) {
        el.style.overflowWrap = 'anywhere';
        el.style.hyphens = 'auto';
      }
    });
  }

  // Responsive breakpoints change the base size, so forget it on resize.
  function refitTitles() {
    document.querySelectorAll('[data-fit-title]').forEach(function (el) {
      el.style.fontSize = '';
      delete el.dataset.base;
    });
    fitTitles();
  }

  // 2. Dismissable messages.
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-tl-dismiss]');
    if (b) {
      var m = b.closest('.tl-message');
      if (m) m.remove();
    }
  });

  // 3. <details class="tl-pop"> popovers: one open at a time, close on outside
  //    click and on Escape (focus returns to the summary).
  function closePops(except) {
    document.querySelectorAll('details.tl-pop[open], details.tl-menu[open]').forEach(function (d) {
      if (d !== except && !d.contains(except)) d.open = false;
    });
  }
  document.addEventListener('toggle', function (e) {
    var d = e.target;
    if (d.matches && d.matches('details.tl-pop, details.tl-menu') && d.open) closePops(d);
  }, true);
  document.addEventListener('click', function (e) {
    if (!e.target.closest('details.tl-pop, details.tl-menu')) closePops(null);
    var c = e.target.closest('[data-tl-close]');
    if (c) {
      var d = c.closest('details');
      if (d) { d.open = false; d.querySelector('summary').focus(); }
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = document.querySelector('details.tl-pop[open], details.tl-menu[open]');
    if (open) { open.open = false; open.querySelector('summary').focus(); }
  });

  // 4. Remember <details data-tl-remember="key"> open state.
  function restoreDetails() {
    document.querySelectorAll('details[data-tl-remember]').forEach(function (d) {
      var k = 'tl-open:' + d.dataset.tlRemember;
      try {
        var v = localStorage.getItem(k);
        if (v !== null) d.open = v === '1';
      } catch (err) { /* storage blocked: keep the server default */ }
      d.addEventListener('toggle', function () {
        try { localStorage.setItem(k, d.open ? '1' : '0'); } catch (err) { /* ignore */ }
      });
    });
  }

  // 5. Scroll the current chargen step into view inside the cover.
  //    Uses scrollTop, never scrollIntoView (which would move the page too).
  function showCurrentStep() {
    var cur = document.querySelector('.tl-steps [aria-current="step"]');
    if (!cur) return;
    var box = cur.closest('.tl-cover__inner');
    if (box) box.scrollTop = cur.offsetTop - box.clientHeight / 2;
  }

  // 6. Bootstrap data-API shim for templates still on legacy markup (collapse, tab,
  //    pill, dropdown, alert dismiss), so legacy pages need neither jQuery nor
  //    bootstrap.js. Toggles the same classes Bootstrap would (.show / .active).
  function targetsFor(el) {
    var sel = el.getAttribute('data-target') || el.getAttribute('data-bs-target') || el.getAttribute('href');
    if (!sel || sel.charAt(0) !== '#' && sel.charAt(0) !== '.') return [];
    try { return Array.prototype.slice.call(document.querySelectorAll(sel)); } catch (err) { return []; }
  }
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-toggle], [data-bs-toggle], [data-dismiss="alert"]');
    if (!el || !el.closest('.tl-legacy, .tl-cover')) {
      if (!e.target.closest('.dropdown-menu')) {
        document.querySelectorAll('.tl-legacy .dropdown-menu.show').forEach(function (m) { m.classList.remove('show'); });
      }
      return;
    }
    var kind = el.getAttribute('data-toggle') || el.getAttribute('data-bs-toggle');
    if (el.getAttribute('data-dismiss') === 'alert') {
      var alert = el.closest('.alert, .tg-message');
      if (alert) alert.remove();
      return;
    }
    if (kind === 'collapse') {
      e.preventDefault();
      var open = null;
      targetsFor(el).forEach(function (t) { t.classList.toggle('show'); open = t.classList.contains('show'); });
      if (open !== null) el.setAttribute('aria-expanded', open ? 'true' : 'false');
      el.classList.toggle('collapsed', open === false);
    } else if (kind === 'tab' || kind === 'pill') {
      e.preventDefault();
      var nav = el.closest('.nav, [role="tablist"]');
      if (nav) nav.querySelectorAll('[data-toggle="tab"], [data-toggle="pill"], [data-bs-toggle="tab"], [data-bs-toggle="pill"]').forEach(function (l) {
        l.classList.remove('active'); l.setAttribute('aria-selected', 'false');
      });
      el.classList.add('active'); el.setAttribute('aria-selected', 'true');
      targetsFor(el).forEach(function (pane) {
        var box = pane.parentElement;
        if (box) Array.prototype.forEach.call(box.children, function (c) { c.classList.remove('active', 'show'); });
        pane.classList.add('active', 'show');
      });
    } else if (kind === 'dropdown') {
      e.preventDefault();
      var menu = el.parentElement && el.parentElement.querySelector('.dropdown-menu');
      if (menu) {
        var wasOpen = menu.classList.contains('show');
        document.querySelectorAll('.tl-legacy .dropdown-menu.show').forEach(function (m) { m.classList.remove('show'); });
        menu.classList.toggle('show', !wasOpen);
        el.setAttribute('aria-expanded', wasOpen ? 'false' : 'true');
      }
    }
  });

  // 7. Legacy pages open with a "header card" holding the page title. Move that title
  //    onto the ink cover so the page reads as a Spread page (the card is hidden).
  function promoteLegacyTitle() {
    var slot = document.querySelector('[data-legacy-title]');
    var main = document.querySelector('main.tl-legacy');
    if (!slot || !main) return;
    var card = main.querySelector('.header-card');
    var title = card && card.querySelector('h1, .tg-card-title');
    if (!title || !title.textContent.trim()) return;
    slot.textContent = title.textContent.trim();
    var sub = card.querySelector('.tg-card-subtitle, p');
    if (sub && sub.textContent.trim()) {
      var subSlot = document.querySelector('[data-legacy-sub]');
      if (subSlot) { subSlot.innerHTML = sub.innerHTML; subSlot.hidden = false; }
    }
    card.hidden = true;
    fitTitles();
  }

  var t;
  window.addEventListener('resize', function () {
    clearTimeout(t);
    t = setTimeout(refitTitles, 120);
  });
  function init() {
    promoteLegacyTitle();
    fitTitles();
    restoreDetails();
    showCurrentStep();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitTitles);
  document.addEventListener('htmx:afterSwap', fitTitles);

  window.TL = { fitTitles: fitTitles };
})();
