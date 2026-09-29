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

  // 5. Let readers reclaim page width without losing the cover on other pages.
  function setupCoverLayout() {
    var spread = document.querySelector('.tl-spread');
    if (!spread) return;
    var toggle = spread.querySelector('[data-cover-toggle]');
    var handle = spread.querySelector('[data-cover-resize]');
    if (!toggle || !handle) return;
    var width = spread.classList.contains('tl-spread--wide') ? 560 : 440;
    var preferredWidth = width;
    var savedWidth;
    var collapsed = false;
    try {
      savedWidth = Number(localStorage.getItem('tl-cover-width'));
      collapsed = localStorage.getItem('tl-cover-collapsed') === '1';
    } catch (err) { /* storage blocked: use the defaults */ }

    function maximum() { return Math.max(240, Math.min(720, window.innerWidth - 460)); }
    function setWidth(value, save) {
      preferredWidth = Math.max(240, Math.min(720, Math.round(value)));
      width = Math.max(240, Math.min(maximum(), preferredWidth));
      spread.style.setProperty('--tl-cover-width', width + 'px');
      handle.setAttribute('aria-valuenow', String(width));
      handle.setAttribute('aria-valuemax', String(maximum()));
      if (save) {
        try { localStorage.setItem('tl-cover-width', String(width)); } catch (err) { /* ignore */ }
      }
      refitTitles();
    }
    function setCollapsed(value) {
      collapsed = value;
      spread.classList.toggle('is-cover-collapsed', collapsed);
      toggle.setAttribute('aria-expanded', String(!collapsed));
      toggle.setAttribute('aria-label', collapsed ? 'Expand sidebar' : 'Collapse sidebar');
      toggle.title = collapsed ? 'Expand sidebar' : 'Collapse sidebar';
      toggle.querySelector('span').textContent = collapsed ? '›' : '‹';
      try { localStorage.setItem('tl-cover-collapsed', collapsed ? '1' : '0'); } catch (err) { /* ignore */ }
      refitTitles();
      if (!collapsed) showCurrentStep();
    }
    setWidth(savedWidth >= 240 ? savedWidth : width, false);
    setCollapsed(collapsed);
    toggle.addEventListener('click', function () { setCollapsed(!collapsed); });

    var drag = null;
    handle.addEventListener('pointerdown', function (event) {
      if (event.button !== 0 || collapsed) return;
      drag = { x: event.clientX, width: width };
      handle.setPointerCapture(event.pointerId);
      event.preventDefault();
    });
    handle.addEventListener('pointermove', function (event) {
      if (drag) setWidth(drag.width + event.clientX - drag.x, false);
    });
    function finishDrag() {
      if (!drag) return;
      drag = null;
      setWidth(width, true);
    }
    handle.addEventListener('pointerup', finishDrag);
    handle.addEventListener('pointercancel', finishDrag);
    handle.addEventListener('lostpointercapture', finishDrag);
    handle.addEventListener('keydown', function (event) {
      var next = width;
      if (event.key === 'ArrowLeft') next -= 20;
      else if (event.key === 'ArrowRight') next += 20;
      else if (event.key === 'Home') next = 240;
      else if (event.key === 'End') next = maximum();
      else return;
      event.preventDefault();
      setWidth(next, true);
    });
    window.addEventListener('resize', function () { setWidth(preferredWidth, false); });
  }

  // 6. Scroll the current chargen step into view inside the cover.
  //    Uses scrollTop, never scrollIntoView (which would move the page too).
  function showCurrentStep() {
    var cur = document.querySelector('.tl-steps [aria-current="step"]');
    if (!cur) return;
    var box = cur.closest('.tl-cover__inner');
    if (box) box.scrollTop = cur.offsetTop - box.clientHeight / 2;
  }

  var t;
  window.addEventListener('resize', function () {
    clearTimeout(t);
    t = setTimeout(refitTitles, 120);
  });
  function init() {
    fitTitles();
    restoreDetails();
    setupCoverLayout();
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
