# JavaScript Static Assets Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans; independent page extraction and browser characterization may run in parallel using superpowers:dispatching-parallel-agents. Steps use checkbox syntax for tracking.

**Goal:** Relocate application JavaScript to cacheable static files while preserving behavior.

**Architecture:** Plain script files retain current manager globals and algorithms.
Django Media supplies widget dependencies; HTML data carries configuration.

**Tech Stack:** Django 5.2, Python, plain JavaScript, existing local Chromium.

**Spec:** ../specs/2026-09-25-js-static-assets-design.md

## Global constraints

- No npm, bundler, Vite, frontend framework rewrite or added CSP.
- Preserve Step 0 chained endpoint protocol and Step 4 validation rules.
- Exclude scene chat (Step 11); do not refactor Step 10 candidates.
- Work in the existing 09-js-static-assets worktree; leave a reviewable diff.

## Review focus

- Two independently rendered forms must each declare their scripts.
- Combined Media must deduplicate the same widget dependency.
- Configuration containing quotes, ampersands and closing script tags must round-trip safely.
- Empty formsets and added rows must have the required assets and initialization.
- Page-specific guards and configuration must survive moving out of Django templates.

### Task 1: Characterize and establish regression guards

Files: widgets/tests/test_static_assets_browser.py, widgets/tests/test_static_assets.py.
Interfaces: browser fixtures render existing widgets plus their Media; unchanged behavior assertions run before and after extraction.

- [x] Record existing widget suite baseline.
- [x] Run Chrome characterization for point pools, chains, conditional fields, formsets, filters, create/select and attribute validation before product edits.
- [x] Add failing assertions for external Media, deduplication, safe JSON and the executable-inline allowlist.

### Task 2: Widget extraction (one independently reviewable slice per widget)

Files: the seven Python/static pairs in the spec inventory; existing widgets/tests/test_*.py; widgets/templatetags; core/views/generic.py; core/templates/core/base.html.
Interfaces: widget.media returns Django Media, widget.render returns markup/data; ConditionalFieldsMixin.media merges its parent's assets; existing manager global methods remain unchanged.

- [x] Extract point pools; declare Media on both input/select widgets and safely encode pool config.
- [x] Extract chained selects; declare Media and safely encode choice trees; retain endpoint payload.
- [x] Extract create/select and metadata widgets, each declaring its own Media.
- [x] Extract conditional fields; keep conditional_js as the inert rules output used by 14 templates.
- [x] Extract formset manager and filterable list; replace render-once calls with external Media and remove signal/global state.
- [x] Aggregate form/formset Media in the base template, including empty-form dependencies, and verify standalone helper output.
- [x] Update obsolete inline-emission assertions to assert external assets; run `python manage.py test widgets.tests --noinput` (expected: pass).

### Task 3: Page extraction by app

Files: all destinations in ../specs/js-page-inventory.md plus core/static/core/js/validation.js and core/templates/core/form.html.
Interfaces: existing TG.validation API; data attributes captured from each script element; json_script for multiplier data.

- [x] Move core validation helper verbatim.
- [x] Move character scripts with their original conditional guards and scalar data inputs.
- [x] Move account, item, location and week scripts, preserving script positions and event listeners.
- [x] Run before/after browser assertions and inline allowlist guard (expected: pass).

### Task 4: Cache versioning and integration review

Files: tg/settings/production.py, regression tests, design/plan execution record.
Interfaces: STORAGES['staticfiles'] uses django.contrib.staticfiles.storage.ManifestStaticFilesStorage.

- [x] Enable production content hashes; verify static discovery and collectstatic in a temporary destination.
- [x] Run widget, relevant core/view and template regression tests; record exact results.
- [x] Review full diff for interpolation, shared state, ordering, missing assets and excluded scene changes.
- [x] Update inventory/CSP notes and record any remaining limitations.

## Suggested PR order

Point pool, chained select, create/select, metadata, conditional fields, formset
manager, filterable list (one widget each; foundational media rendering lands
with the first); then core, characters, accounts, items, locations/game page scripts; final
cache/allowlist integration. This worktree implements the full sequence together.

## Execution record

- Existing baseline: 140 widget tests passed before changes.
- Ruling: current user request supersedes the source document's design-only scope and authorizes continuing from plan to implementation.
- Ruling: referenced frontend/testing skills were consolidated into tg-standards; read replacement templates/testing references.
- Ruling: use local Chrome for browser tests because Selenium's driver download is unavailable; no new runtime dependency.

- Baseline browser characterization: eight Chrome tests passed before widget extraction; attribute passed individually before its template move.
- Final verification: `python manage.py test widgets.tests core.tests.views.test_generic core.tests.test_routed_templates characters.tests.test_static_page_assets characters.tests.views.core.test_chargen_validation --noinput` ? 204 tests passed in 32.492s, including 11 real-browser tests and full manifest collection in a temporary directory.
- All 31 application scripts passed `node --check`; no npm or build step was introduced.
- All seven widget algorithm bodies match the evaluated original Python constants. Three formset initialization event subscriptions replace per-control inline initialization.
- Independent review found no blocking regressions; it verified extraction equivalence and media propagation through inherited templates and includes.
- Ruling: collectstatic exposed existing stylesheet font paths escaping the static root. Corrected only those paths to enable production manifest hashing; collection now succeeds.
- Ruling: the executable-inline guard found an additional account profile script. Included it in the relocation and corrected the inventory.
- Existing limits (middle-row formset reindexing and conditional-manager scoping) are documented in the design; they were not rewritten.
- Implementation verified in the 09-js-static-assets worktree. Commit and pull-request publication are authorized by the follow-up request; deployment and framework rewrites remain out of scope.
