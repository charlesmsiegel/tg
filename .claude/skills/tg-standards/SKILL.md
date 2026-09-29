---
name: tg-standards
description: >-
  Design rules and review checklists for the Tellurium Games Django project (World of
  Darkness characters, items, locations, chronicles and scenes). Load it before you
  design, write or review a model, field, constraint, schema change or tg_schema
  migration, a view, form, URL or template, a route policy or permission check, a cache
  decorator, a management command or a test in this repository, and when reviewing a diff
  or PR that touches any of them. Triggers on: core.models.Model, polymorphic models,
  CharacterModel/Human/ItemModel/LocationModel subclasses, new character/item/location or
  reference type, tg_schema, migrations, route_policy_manifest, AuthorizationMiddleware,
  PermissionManager, core.mixins, ScopedEditFormMixin, crud_fields, items/locations
  registry, core.actions, Spread templates (tl_base.html, core/form.html, tl tags), htmx
  fragments, cache_page, query budgets, template fixtures, chargen workflows.
---

# TG standards

The rules a change must follow to match the current architecture of this repository, and
the checklist a reviewer runs against a diff. Each rule names its reason and, where one
exists, the test that enforces it. Details live in `references/`; explanations live in
the project docs they link to (`docs/architecture/`, `docs/guides/`, `<app>/docs/`).

The code is the source of truth. If a rule here disagrees with the code or a guard test,
trust the code, then fix this skill.

## When to use

- Before designing a model, field, constraint or any schema change.
- Before adding or changing a view, form, URL, template, route policy or cache decorator.
- Before writing tests for any of the above, or a management command.
- When reviewing a diff, branch or PR in this repo: run the [review checklist](#review-checklist).

Not for game rules or sheet content (use `wod-toolkit`) or generic Django refactoring
(use `django-simplifier`).

## Non-negotiable rules

### Schema

1. **Never commit migrations for local apps** (`accounts`, `characters`, `core`, `game`,
   `items`, `locations`, `widgets`). Their `migrations/` hold only `__init__.py`;
   `.gitignore` ignores the rest. *Why:* test and fresh databases build these tables from
   the current models; generated files are per install.
2. **Ship every change an existing database needs as a `tg_schema` migration**: new
   column, table, index or constraint, rename, data backfill, reordered chargen steps.
   Number it `NNNN_snake_name.py` and depend on the previous one. *Why:* it is the only
   committed path that reaches databases created before the change.
3. **In a `tg_schema` migration, import no app model and ignore the `apps` argument.** Look
   models up with `tg_schema.schema.live_model` / `live_field`, or name tables in raw SQL.
   *Why:* a later rename must skip the old migration, not crash every `migrate`
   (`tg_schema/tests/test_schema_helpers.py` enforces both).
4. **Make it idempotent and self-skipping**: add only missing columns
   (`add_missing_columns`), return when a model, field, table or column is gone, guard
   DDL by introspection, backfill only rows that still need it, reverse with
   `RunPython.noop`.
5. **Declare the same field or constraint on the model**, nullable or with a default.
   *Why:* fresh databases get the schema from the model; the migration only patches old
   ones, whose rows need a value.
6. **Test every `tg_schema` migration** in `tg_schema/tests/test_<name>.py`.

### Models

7. **Extend an existing tree**: `Human` (or `CharacterModel`) subclasses for characters,
   `Group` for player groups, `ItemModel`, `LocationModel`, `core.models.Model` for other
   owned or approvable objects and most reference data, `ValidatedSaveMixin` +
   `models.Model` for plain records. *Why:* ownership, approval, visibility, public cards
   and routing are built on these bases.
8. **Set `type` (snake_case, unique in its app) and `gameline` (a key of
   `settings.GAMELINES`)** as class attributes on every `core.models.Model` subclass.
   *Why:* `GenericCharacterDetailView` and `characters.chargen.get_workflow` dispatch on
   `type`; theming, headings and scoped ST roles use `gameline`.
9. **Take choices from settings and constants**: `settings.GAMELINE_CHOICES` /
   `settings.GAMELINES` for gamelines, `core.constants.CharacterStatus` / `ImageStatus` /
   `XPApprovalStatus` for statuses. Never hard-code a gameline or status list.
10. **Validate in `clean()`** (collect a field-keyed dict, raise one `ValidationError`);
    `save()` runs `full_clean()`. Use `save(skip_validation=True)` or `QuerySet.update()`
    only in migrations, fixtures and bulk jobs.
11. **`on_delete=SET_NULL` (with `null=True`) for links to rows that live on their own;
    `CASCADE` only for rows that exist for their parent.** Name every constraint.
12. **Give routable models `get_absolute_url`, `get_update_url` and `get_creation_url`.**
    Items and locations inherit them from the registry (`RegistryURLMixin`); reference
    models may use `URLMethodsMixin`.
13. **Lock before changing XP, freebies or point pools**: `select_for_update()` inside
    `transaction.atomic()`.

### Authorization

14. **Every routed view has exactly one access policy**: an entry in
    `core/route_policy_manifest.py` or its registry `ActionSpec.policy`, never both, and no
    stale entries. *Why:* `AuthorizationMiddleware` denies undeclared views, and
    `core/tests/security/test_route_policies.py` fails on missing, doubled or stale ones.
15. **Choose the narrowest policy.** Reference data: `PUBLIC_READ` to read, `STAFF_WRITE`
    to write. Player objects: `OBJECT_LIST`, `OBJECT_DETAIL`, `OBJECT_CREATE`,
    `OBJECT_WRITE`, `OBJECT_ST_WRITE`, `CHARGEN_STEP`. One-object state changes: `ACTION`.
16. **Decide object access in `PermissionManager`** (always pass `request=`), through
    `core.mixins` or an action's `permission` / `has_permission`, never in view bodies or
    templates. Templates read the `object_perms` booleans.
17. **Never reveal what a user may not see.** A hidden or missing object gets the same
    404; a player object the user cannot fully view gets its public card, never its
    private fields; a 403 only follows a successful view check. *Why:* a 403 or a
    different 404 confirms the object exists.
18. **Only staff change `owner`, `chronicle`, `gameline`, `status`, `npc`, `xp`,
    `freebies_approved`, `approved`, `approved_by` through a write route**; everyone
    else, storytellers included, goes through a dedicated action or service. Owner-editable
    update views use `ScopedEditFormMixin` with a `limited_form_class`. *Why:* the
    `OBJECT_*` field guard in `core/access_policy.py` rejects the change anyway.

### Views, forms and URLs

19. **Detail views never handle POST; each state change is its own POST endpoint**
    (`core.actions.ObjectActionView`), and no view dispatches on posted button names
    (`core/tests/test_action_guard.py`).
20. **`form_invalid` never calls `form_valid`** (`characters/tests/test_view_rules_guard.py`).
21. **Keep rules out of views**: services (`characters/services/`, `core/services/`,
    `game/`) and models make the change; views authorize, bind and render.
22. **Fetch with `get_object_or_404`, `select_related` / `prefetch_related` and
    `.with_polymorphic_ctype()`**; stay inside the query ceilings
    (`core/tests/test_query_budgets.py`).
23. **Create views for `core.models.Model` subclasses include `MessageMixin`** (or come from
    the registry). *Why:* it runs `prepare_created_object`, which sets the owner, checks
    the chronicle and sets the starting status.
24. **List editable fields explicitly**: `fields = [...]` or a form's `Meta.fields`; never
    `"__all__"`, `exclude` or introspection. Character CRUD lists live in
    `characters/forms/core/crud_fields.py` and are pinned by a baseline.
25. **Register every concrete item and location model** in `items/registry.py` /
    `locations/registry.py` (`core/tests/test_model_registry.py`). New routes use
    `<int:pk>` and a name in the app's gameline and action namespaces
    (`characters:vampire:update:clan`).

### Templates and caching

26. **Build on Spread**: extend `core/tl_base.html`, `core/form.html`, `core/object.html`
    or an area shell. No Bootstrap, jQuery, `tg-card`, inline scripts, inline
    `style="..."` or `<style>` blocks (the last two are ratcheted by
    `core/tests/test_template_policy.py`). CSS goes in `core/static/core/tl/tl.css`,
    JavaScript in `<app>/static/<app>/`, page data in `json_script` or `data-*`.
27. **Theme with `{% block gameline %}{{ object|gameline_code }}{% endblock %}`**, render
    fields with `core/tl/field.html`, dots and tracks with `{% load tl %}` tags.
28. **Escape user text**: `|sanitize_html` for rich text, never `|safe`.
29. **Cache pages only with `core.cache.cache_page_per_visitor`** (or `CachedDetailView` /
    `CachedListView`), never Django's `cache_page`, and only pages that read no query
    string and render no CSRF token unless they hold a form. *Why:* `cache_page` serves
    one visitor's page to the next, and a CSRF token keeps a page out of the shared
    anonymous copy.

### Tests and style

30. **Every change ships its tests** in `<app>/tests/`, mirroring the source path: models,
    forms, views, a denial test for each new route, a migration test for each `tg_schema`
    migration.
31. **Change a guard's allowlist, ceiling or baseline only on purpose**, in the same diff,
    with the reason in the commit. *Why:* these files are the ratchets that keep the
    architecture in place.
32. **Format with black and lint with ruff** (100 columns; ruff is the only import sorter)
    through pre-commit, and keep ruff clean repo-wide.

## Review checklist

Run the sections that match the diff. Every unchecked box is a finding.

**Any model change**
- [ ] Right base class; `type` unique and `gameline` valid on polymorphic subclasses.
- [ ] `Meta.verbose_name`, `verbose_name_plural`, `ordering` where lists need it; `__str__`.
- [ ] Choices from settings or `core.constants`; no hard-coded gameline or status lists.
- [ ] `clean()` validates cross-field rules; constraints are named and have messages.
- [ ] `on_delete` and `related_name` chosen deliberately; hot FKs indexed.
- [ ] URL methods present or supplied by the registry.

**Schema change**
- [ ] No files under a local app's `migrations/` besides `__init__.py`.
- [ ] A new `tg_schema` migration, linear dependency, no app-model imports, `apps` unused.
- [ ] Skips cleanly when its model, field, table or column is gone; runs twice safely.
- [ ] Backfills touch only rows that still need it; destructive SQL explained in the
  docstring.
- [ ] Model declares the same field or constraint; new columns nullable or defaulted.
- [ ] `tg_schema/tests/test_<name>.py` covers: adds when missing, no SQL when present,
  backfill result, skip on rename.

**New or changed route**
- [ ] Exactly one policy (manifest or registry), the narrowest that fits; removed views
  removed from the manifest.
- [ ] Hidden objects give the same 404 as missing ones; public card for partial viewers.
- [ ] No POST on detail views; no button-name dispatch; actions use `ObjectActionView`.
- [ ] Protected fields cannot be changed by non-staff; update views scope their form.
- [ ] Queries bounded: `select_related` / `prefetch_related`, no per-row queries in
  templates.
- [ ] Denial tests added (anonymous, other player, wrong-scope ST).

**Form**
- [ ] Explicit field list; chronicle choices limited to `readable_chronicles(user)`.
- [ ] No Bootstrap widget classes; errors reach `core/tl/field.html`.
- [ ] Character CRUD field lists come from `crud_fields.py`; baseline JSON updated on purpose.

**Template**
- [ ] Extends a Spread shell; sets the `gameline` block; uses `tl` tags and partials.
- [ ] No inline styles, `<style>`, inline scripts, Bootstrap, jQuery or `tg-card`.
- [ ] Assets through `{% static %}`; user text through `|sanitize_html`.
- [ ] Permission-dependent controls read `object_perms`, not role logic.
- [ ] htmx fragments marked (`mark_fragment`) and varied (`vary_on_htmx`).

**Cache**
- [ ] Only `cache_page_per_visitor` or the cached view classes; no query-string reads;
  no `{% csrf_token %}` on a cached page without a form.

**Tests and style**
- [ ] Tests for each behaviour and each denial; guard ratchets untouched or justified.
- [ ] New character type: query ceiling, chargen golden fixture, detail router and CRUD
  baseline updated.
- [ ] `pre-commit run --all-files` clean.

## References

| File | Read it when |
|------|--------------|
| [models.md](references/models.md) | Adding or changing any model, field, manager or relation |
| [schema-changes.md](references/schema-changes.md) | Anything that changes tables, columns, constraints or stored data |
| [validation.md](references/validation.md) | Writing `clean()`, constraints, transactions, status changes |
| [permissions.md](references/permissions.md) | Choosing a route policy, checking object access, limited forms |
| [views.md](references/views.md) | Writing a view, action endpoint, router or htmx fragment |
| [forms.md](references/forms.md) | Writing a form or a character CRUD field list |
| [urls.md](references/urls.md) | Adding a route or a URL name |
| [registry.md](references/registry.md) | Adding or changing an item or location type |
| [templates.md](references/templates.md) | Writing a template, partial, tag use, htmx markup |
| [spread.md](references/spread.md) | Spread blocks, components, tokens and page structure |
| [caching.md](references/caching.md) | Caching a page, a function result or a reference list |
| [testing.md](references/testing.md) | Writing or placing tests, fixtures, budgets, browser tests |
| [code-style.md](references/code-style.md) | Formatting, linting, imports, pre-commit |
| [commands.md](references/commands.md) | Writing a management command |
| [character-templates.md](references/character-templates.md) | Working on `CharacterTemplate` and its views |
| [model-inventory.md](references/model-inventory.md) | Finding where a model family lives and its base |
| [domain.md](references/domain.md) | Game terms mapped to models, codes and statuses |
| [deployment.md](references/deployment.md) | Making a change deployable (settings, static, schema) |
