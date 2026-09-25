# Task: Design the dead-code removal for the `tg` Django app (Step 1)

You are designing, **not implementing**, the removal of dead, unreachable and superseded code from this repository (`charlesmsiegel/tg`, Django 5.2 with django-polymorphic 4.1; a World of Darkness character/chronicle manager). The goal is to shrink the surface area before the larger refactors (Steps 2–11) start, so later work doesn't waste effort keeping dead code working. You produce a design doc and an implementation plan that another engineer can execute as a series of small PRs.

## Before you start

- Read `CLAUDE.md` and `.claude/skills/tg-testing/SKILL.md`.
- Read the existing docs in `docs/superpowers/specs/` and `docs/superpowers/plans/` and follow their format. If a Step 0 design (`*-authorization-hardening-design.md`) exists, read it; it may repurpose code listed here. Write:
  - `docs/superpowers/specs/2026-09-25-dead-code-removal-design.md`
  - `docs/superpowers/plans/2026-09-25-dead-code-removal.md`
- Django may not be installed in your environment. Run `pip install -r requirements.txt` if needed.
- The findings come from a code-reading audit at commit `c1c509a`, so line numbers are approximate. **Confirmed** items were re-checked against the source. **Reported** items are credible but unverified: confirm or refute each one before designing around it, and say in the doc which ones you confirmed.

## Candidates

### Confirmed dead or unreferenced

1. **The `chained_select` app.**
   - It is listed in INSTALLED_APPS as `"chained_select",  # Deprecated - backward compatibility only` (`tg/settings/base.py:37`).
   - Its `__init__` re-exports from `widgets` with a DeprecationWarning.
   - The only importer outside the app is `widgets/tests/test_chained_select.py:343-373`, whose compatibility tests exist only to test this shim.
   - Per the audit, its `widgets.py` and `views.py` are about 95% copies of `widgets/widgets/chained.py` and `widgets/views.py`.
2. **The `django-smart-selects==1.7.2` dependency** in `requirements.txt`. It has zero imports anywhere, including in migrations.
3. **Mixins in `core/mixins.py` with no non-test users:**
   - `STRequiredMixin` (:238). It also references a nonexistent `chronicle.head_storytellers`.
   - `SpendXPPermissionMixin` (:106).
   - `DeleteMessageMixin` (:409). It overrides `delete()`, which Django ≥4's DeleteView no longer calls.
   - `FreebieApprovalMixin` (:791).

   **Coordinate with Step 0:** the authorization design may adopt `SpendXPPermissionMixin`, or a chronicle-scoped ST mixin. Don't delete permission mixins until Step 0 has decided.
4. **Twelve AJAX endpoints that no template, JS file or Python code references.**
   - Names: `load_examples`, `load_values`, `load_mf_ratings`, `load_xp_examples`, `load_companion_examples`, `load_sorcerer_examples`, `load_advantage_values`, `get_abilities`, `get_practice_abilities`, `load_attributes`, `load_affinities`, `load_chantry_examples`.
   - Routes live in `characters/urls/core/ajax.py`, `characters/urls/mage/ajax.py` and `locations/urls/mage/ajax.py`.
   - Their views include `LoadXPExamplesView` (`characters/views/mage/mage.py:~107`, 125 lines), `HumanFreebieFormPopulationView` (`characters/views/core/human.py:~331`), and the `LoadExamplesView` classes in `mage/companion.py` and `mage/sorcerer.py`.
   - The ajax URL modules for changeling, vampire, wraith and werewolf are empty, as is `locations/urls/vampire/ajax.py`.
5. **The unrouted Mage chantry creation flow.**
   - `ChantryCreationView`, `ChantryBasicsView`, `ChantryPointsView`, `ChantryIntegratedEffectsView`, `ChantryNodeView`, `ChantryLibrarysView`, `ChantryAlliesView` and `ChantrySanctumView` (`locations/views/mage/chantry.py:~176-301`) have no route in `locations/urls`.
   - **Product question:** delete these, or wire them up? The Mage character wizard has its own separate `MageChantryView`.
6. **Unrouted list views:** `TremereChantryListView` and `BarrensListView` (`locations/views/vampire/__init__.py:~291,359`). **Decide:** route them (they look like missing features) or delete them.
7. **Unused template tags:**
   - `core/templatetags/permissions.py` (205 lines, about 605 lines of tests) is loaded by zero templates. **Leave the decision to Step 6 (permission context)**, which may adopt it.
   - In `core/templatetags/dots.py`, `linked_stat`, `linked_stat_row`, `pool_dots` and `pool_rows` have zero template uses.
8. **The unreferenced "point pool" attribute form.**
   - `characters/forms/core/attribute_form.py` (`AttributeForm`, `HumanAttributeForm`) and `characters/templates/characters/core/attribute_block/form_pool.html` have no non-test users.
   - **Leave the decision to Step 10 (htmx/Alpine chargen)**, which may adopt the `DistributionPoolMixin` approach.

### Reported (verify each one)

- `core/templatetags/resonance.py` is unused. So are `conditional_wrap` and `as_conditional` in `widgets/templatetags/conditional_fields.py`.
- `ItemIndexView.items` and `LocationIndexView.locs` (`items/views/core/__init__.py:~136`, `locations/views/core/__init__.py:~125`) are never read. So are `game_location_types` (`locations/views/core/__init__.py:~205`) and the `factions` context in `ChantryDetailView` (`chantry.py:~33-44`).
- `error_401` (`core/views/errors.py:6`) exists, but there is no `handler401`.
- There are 62 no-op `app_name = "..."` assignments in `items/urls/**` and `locations/urls/**`. The modules export `urls`, not `urlpatterns`, and namespaces come from the `include()` tuples.
- `HomeListView` is routed twice (`core/urls.py:6` and `accounts/urls.py:47`).
- `core.context_processors.permissions` (`core/context_processors.py:15`) isn't registered in settings.
- These legacy HTML-fragment templates are orphaned: `characters/mage/mage/load_{faction,subfaction,mf_rating}_dropdown_list.html`, `mage/sorcerer/load_{affinity,attribute}_dropdown_list.html` and `core/human/load_{examples,values}_dropdown_list.html`.
- Several views reference templates that don't exist:
  - `characters/demon/{demon,thrall,dtfhuman}/chargen.html`
  - `characters/wraith/wraith/form.html`
  - `characters/demon/ritual/{form,list}.html`
  - `mage_wonder_block_form.html`
  - `core/human/allies_form.html`

  These may be dead references or missing features. Classify each one, but don't write the templates in this step.
- `core/views/reference.py` (`create_reference_views`, `ReferenceViewSet`) is only re-exported from `core/views/__init__.py:35,69-70`. **Leave it to Step 7 (items/locations registry)**, which may adopt it as the CRUD factory.

## What the design must deliver

1. **A repeatable detection method,** preferably a script committed under `scripts/`, that finds:
   - URL names never referenced by `reverse`, `{% url %}` or JS;
   - view classes never routed, including DictView `view_mapping` targets;
   - templates never referenced by `template_name`, `get_template_names`, `{% include %}` or `{% extends %}`, or by computed names (flag computed names for manual review);
   - template tags and filters never loaded or used;
   - Python symbols with no references, as a heuristic, since polymorphic and DictView indirection causes false positives.
   Run it and include the output.
2. **A decision table** with one row per candidate: the evidence, the decision (**delete** / **keep: owned by Step N** / **route it** / **needs product decision**), the risk, and the tests to delete or adjust.
3. **Removal safety:**
   - Handle INSTALLED_APPS and migrations correctly, including checking whether `chained_select` has migrations or models.
   - Check static files, and any `populate_db/` or management commands that reference the removed code.
   - Show the full test suite passing after each PR.
4. **PR slicing:** small PRs grouped by area, lowest risk first (the dependency, then the `chained_select` app, then the AJAX endpoints, then the tags, and so on).
5. **Open questions for the owner:** the chantry flow, the unrouted list views and the missing-template features.

## Constraints

- Design only. Don't modify application code. You may commit the detection script if the plan calls for it.
- Remove code only: no behaviour change for any routed page.
- Don't delete anything another step has claimed: permission mixins (Step 0), the permissions template tags (Step 6), `core/views/reference.py` (Step 7), and the point-pool form (Step 10). List these as "deferred to Step N".
