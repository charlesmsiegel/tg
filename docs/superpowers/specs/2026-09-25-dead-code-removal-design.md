# Dead-Code Removal Design (Step 1)

## Goal

Shrink the codebase before the larger refactors (Steps 2–11) by removing dead, unreachable and superseded code, so later work doesn't spend effort keeping it alive. This design covers **all of `docs/code-fixing/01-dead-code-removal.md` in one effort**, as the owner requested.

It deliberately extends plain removal in two ways the owner decided during brainstorming:

1. **Recover instead of delete when the code was meant to be used.** Several "dead" pieces are finished product logic that was never connected. The main one is the Mage chantry creation flow, which has its own spec: `2026-09-25-chantry-creation-flow-design.md`. The others are listed under *Recover*.
2. **Detail-page rule.** Before any uncalled or broken model method, or orphan display template, is deleted, the decision table records whether it belongs on that model's detail page. If it does, it is recovered and fixed there.

Everything else is **delete**, or **deferred** to the step that owns it.

## Sources and method

- **The audit prompt** (`01-dead-code-removal.md`, written against `c1c509a`).
- **The Step 0 design and plan.** Step 0 has landed (`093e3cc`). It chose a declarative route manifest (`core/route_policy_manifest.py`, enforced by `core/access_policy.py`) instead of permission mixins, so the permission mixins that Step 1 held back can now be decided.
- **`scripts/find_dead_code.py`**, the detection method (below), run at the head of this branch. Its full output is committed as the appendix `2026-09-25-dead-code-removal-report.md`.
- **Checks by hand:** each candidate was confirmed with `grep`, `reverse()` and `get_template()` in a Django shell, and receivers were resolved for methods whose names are shared across models. Every "Reported" audit item was confirmed or refuted (see *Audit verification*).

### Detection method: `scripts/find_dead_code.py`

The script is read-only, needs no database (it refuses anything but SQLite and points it at `:memory:`), and produces stable output.

```
python scripts/find_dead_code.py [--section urls|views|templates|tags|symbols]... [--format md|tsv]
```

| Section | Finds | How it avoids false positives |
|---|---|---|
| `urls` | Named URL patterns never referenced by `reverse`/`redirect`/`{% url %}`/JS/`default_redirect`, or by any model `get_*url()` | Expands `core.create_redirects.resolve_object_type_url`, which builds names from the seeded `ObjectType` rows in `populate_db/objects.py`. Flags f-string and computed names for manual review. Classifies each dead name as (a) an alias detail route, (b) a JSON/AJAX endpoint, (c) an unlinked page or (d) other. Also reports seeded object types whose index route doesn't resolve. |
| `views` | View classes that are never routed | Counts a view as routed when it is a URL callback, a `DictView.view_mapping` target (reusing the expansion in `inventory_authorization_routes.py`), a `default_redirect`/`public_view_class`, or a base class of a routed view. Separately labels views reachable only through an unrouted router. |
| `templates` | Templates never referenced by `template_name`, `get_template_names()`, `render*`, `include`/`extends` or an inclusion tag | Calls `get_template_names()` on routed views. Propagates "only referenced by dead templates" and "only used by an unrouted view". Lists computed names for review. |
| `tags` | Tag libraries never `{% load %}`ed; tags and filters never used | Reads the module-level `register` the way Django does. Python-side uses are counted separately (tests vs. non-test code). |
| `symbols` | Heuristic: module-level classes and functions that no other file names | Clearly labelled as a heuristic. "Only referenced from tests" is listed separately. |

`core/tests/test_find_dead_code_script.py` runs every section in a subprocess and fails on a non-zero exit or any stderr output, such as import failures. PR D1 adds pure-function tests for the trickiest heuristics before any deletion depends on the script.

**Summary at this branch's head** (full tables in the appendix):

| Section | Result |
|---|---|
| urls | 747 names: 523 referenced, 45 reached through the object-type index, 9 dynamic (review), 2 share a path with a referenced name, 64 tests only, **104 unreferenced**. Of those 104: 30 alias detail routes, 1 JSON endpoint, 69 unlinked pages, 4 chargen routers. **43 seeded object types give a 404 from the index pages.** |
| views | 1,032 classes: 974 routed, 16 bases of routed views, **38 unrouted** (6 reachable only through the unrouted `ChantryCreationView`), 3 name collisions to review |
| templates | 900: 861 referenced, **23 unreferenced**, 5 only referenced by dead templates, 9 only used by unrouted views, 2 tests only |
| tags | 14 libraries, **3 never loaded** (`permissions`, `resonance`, `conditional_fields`); **26 of 48** tags/filters unused |
| symbols | 16 unreferenced, 33 only referenced from tests (heuristic; each was checked by hand below) |

## Decisions

Legend:
- **Delete**: remove the code and the tests that exist only to test it.
- **Recover**: keep it and connect it.
- **Deferred → Step N**: listed but not touched here.
- **Keep**: a false positive, or a routed page that must keep working.

PR IDs (D1… for dead-code PRs, C1… for chantry PRs) refer to *Rollout*.

### Rules that apply to every row

1. **Routes.** A route is deleted only if it is not a page, meaning a JSON/AJAX endpoint that nothing calls. An unreferenced **page** route (alias detail routes, unlinked list/create/update pages, chargen routers) is **kept**, because deleting it would break a routed page, which the Step 1 constraint forbids. Those routes are recorded for Step 7 (item/location URLs) and Step 2 (chargen routers).
2. **Manifest.** Every URL deletion or addition changes `core/route_policy_manifest.py` in the same commit. `core/tests/security/test_route_policies.py` checks the manifest against the routes in both directions.
3. **Gameline URL loaders.** Deleting an `ajax.py` module also removes its `from . import ajax` and its `include()` in the same commit. `characters/urls/__init__.py` and `locations/urls/__init__.py` swallow `ImportError`/`AttributeError`, so a leftover import would silently drop that gameline's whole URLconf. After each such PR, the plan's check compares the route count before and after.
4. **Re-exports.** Deleting a class also removes its package `__init__` import and its `__all__` entry.
5. **Detail-page rule.** This applies to model methods and display includes; see *Goal*.
6. **Migrations.** Nothing below is referenced by a migration. The only migration file is `tg_schema/migrations/0001_scene_visibility.py`. The removed `chained_select` app has no models or migrations.

### 1. Dependency and deprecated app

| Candidate | Evidence | Decision | Tests |
|---|---|---|---|
| `django-smart-selects==1.7.2` (`requirements.txt:3`) | Zero imports anywhere, including migrations, templates and JS; not in `INSTALLED_APPS` | **Delete** (D2) | none |
| `chained_select` app (`INSTALLED_APPS` "Deprecated – backward compatibility only") | No models, migrations, static files, templates, URLs or template tags. `apps.ready()` does nothing. `__init__` only re-exports from `widgets` and emits a DeprecationWarning at every start. The only external importer is `widgets/tests/test_chained_select.py:339-375` (`TestBackwardCompatibility`). `fields.py`/`widgets.py`/`views.py` are 94–98% copies of `widgets`, and `views.py` still contains the pre-Step-0 unsafe `import_module` view (not mounted). | **Delete** the directory, its settings entry and `TestBackwardCompatibility` (D3). **Keep** the `/__chained_select__/` endpoint, which belongs to `widgets` (`widgets/apps.py:38-46`) and has the manifest entry `WIDGET`. | `TestBackwardCompatibility` |
| `widgets.views.make_ajax_view`, `widgets.views.ChainedSelectAjaxView`, `widgets.widgets.chained.ChainedSelectMultiple` | Only used by `chained_select` and tests. The live endpoint is `auto_chained_ajax_view`. | **Delete** (D3) | the matching cases in `test_chained_select.py` (`TestWidgetsImports`, lines 159-167) |

### 2. Permission mixins, decorators and middleware (Step 0 has decided)

| Candidate | Evidence | Decision | Tests |
|---|---|---|---|
| `core.mixins.STRequiredMixin` | No non-test users; references a nonexistent `chronicle.head_storytellers` | **Delete** (D6) | `STRequiredMixinTest` (`core/tests/mixins/test_mixins.py:950-1040`); `test_permissions_deployment.py:410-412` |
| `core.views.character_template.STRequiredMixin` | Unused since Step 0 (`446eee3`) took it off all 8 CharacterTemplate views | **Delete** (D6) | `core/tests/views/test_character_template.py:13-101` (`STRequiredMixinTest`) |
| `core.mixins.SpendXPPermissionMixin` | No users; Step 0 routes use manifest policies | **Delete** (D6) | `SpendXPPermissionMixinTest` 388-433; `test_permissions_deployment.py:392-394` |
| `core.mixins.DeleteMessageMixin` | No users, and it overrides `delete()`, which Django 5.2's `DeleteView` doesn't call on POST | **Delete** (D6) | `DeleteMessageMixinTest` 1470-1541 |
| `core.mixins.FreebieApprovalMixin` | No users, no tests | **Delete** (D6) | none |
| `core.decorators.require_*` (6 functions) | No non-test importer; no function-based object views; replaced by the manifest | **Delete** (D6) | `core/tests/test_decorators.py` |
| `core.middleware.cache_middleware.PerUserCacheMiddleware` | Not in `MIDDLEWARE` | **Delete** (D6) | `core/tests/middleware/test_cache_middleware.py` |
| `core.cache.cache_queryset`, `get_cached_queryset`, `invalidate_cache_on_save` | Only tests use them; the live helpers are `cache_function` and `get_cached_reference_list` | **Delete** (D6) | the three matching `TestCase` classes in `core/tests/test_cache.py` |
| `core.context_processors.permissions` | Defined but not registered in `TEMPLATES` | **Deferred → Step 6** (permission context) | – |

### 3. AJAX endpoints

All 12 audit endpoints were confirmed: nothing references them in templates, Python, inline JS, JS inside Python strings, or static JS. **These 12 are the complete set** of AJAX URL names in the project.

| URL name | View | Decision |
|---|---|---|
| `characters:ajax:load_examples`, `…:load_values` | `human.LoadExamplesView`, `human.LoadValuesView` | **Delete** (D4) |
| `characters:mage:ajax:load_mf_ratings`, `load_xp_examples`, `get_abilities` | `mage.LoadMFRatingsView`, `mage.LoadXPExamplesView` (126 lines), `mage.GetAbilitiesView` | **Delete** (D4) |
| `…:load_companion_examples`, `load_advantage_values` | `companion.LoadExamplesView`, `companion.LoadCompanionValuesView` | **Delete** (D4) |
| `…:load_sorcerer_examples`, `get_practice_abilities`, `load_attributes`, `load_affinities` | `sorcerer.LoadExamplesView`, `GetPracticeAbilitiesView`, `LoadAttributesView`, `LoadAffinitiesView` | **Delete** (D4) |
| `locations:mage:ajax:load_chantry_examples` | `chantry.LoadExamplesView` | **Delete**, in chantry PR C5 (its filtering moves into the chantry points service) |

Removed alongside, in D4:
- **Manifest and tooling.** The 6 `OBJECT_AJAX` and 5 `LOGIN` manifest lines. The `OBJECT_AJAX` branch of `core/access_policy.py`, which is then unused, together with its tests. The hard-coded list in `scripts/build_route_policy_manifest.py:40-48`.
- **Re-exports** in `characters/views/mage/__init__.py`.
- **Tests.** The endpoint tests in `characters/tests/views/core/test_character.py` (37-150), `test_ajax_json_responses.py`, `test_human.py` (`TestLoadValuesView`) and `test_mage_comprehensive.py` (`TestMageXPExamplesView`, `TestGetAbilitiesView`, `TestMageAjaxViews`). `test_sorcerer_comprehensive.py` (`TestGetPracticeAbilitiesView`). The path-string case in `characters/tests/views/test_public_detail_authorization.py:232-250`. The already-skipped classes that reverse names which no longer exist: `test_sorcerer_comprehensive.py:305-395`, `test_companion_comprehensive.py:219-308`, `test_mage_comprehensive.py:201-260`.
- **The 7 `load_*_dropdown_list.html` templates.** Nothing references them.
- **The empty `ajax.py` modules** (characters changeling, vampire, werewolf and wraith; locations vampire) and their imports and `include()`s (rule 3). The mage `ajax.py` modules are emptied by the deletions and removed the same way; the locations one in C5.
- **The 5 `*FreebieFormPopulationView` classes**: human `human.py:330`, `garou.py:401`, `demon_chargen.py:452`, `dtfhuman_chargen.py:240`, `thrall_chargen.py:204`. They are unrouted AJAX population views, superseded by the chained freebies forms, and their demon exports go with them.
- **What these views leave unused.** `core/ajax.py` and the `DropdownOptionsView`, `SimpleValuesView`, `JsonListView` and `AjaxLoginRequiredMixin` bases, *if* the script confirms no users remain once the views are gone. `AjaxLoginRequiredMixin` is also imported by `scripts/inventory_authorization_routes.py`, which is updated in the same commit.

### 4. Template tags and filters

| Candidate | Evidence | Decision |
|---|---|---|
| `core/templatetags/permissions.py` (13 tags/filters) | Never loaded | **Deferred → Step 6** |
| `core/templatetags/resonance.py` | Never loaded; its test file is a 2-line TODO | **Delete** (D5) |
| `widgets/templatetags/conditional_fields.py` (`conditional_wrap`, `as_conditional`) | Never loaded, no tests. The docstring at `widgets/mixins/conditional.py:43-46` shows the filter and is fixed. | **Delete** (D5) |
| `dots`: `pool`, `pool_dots`, `pool_rows`, `linked_stat`, `linked_stat_row` | 0 template uses, 0 Python callers, no tests. The helpers `_extract_pool_values`/`_render_pool_rows` and `core/templates/core/templatetags/linked_stat_row.html` go with them. | **Delete** (D5) |
| `json_filters.get_item`, `sanitize_text.badge_text`, `formset_tags.formset_remove_btn` | 0 template uses | **Delete** (D5), with their test cases |
| `item_filters` (`replace_underscore`) | Its one `{% load %}` in `items/index.html:3` is left over; the filter is never used | **Delete** the module and the `{% load %}` (D5) |
| `location_tags` (`show_location`) and `locations/location_recursive.html` | Three leftover `{% load %}`s; the tag is never used; the recursive template is reachable only through the tag | **Delete** the module, the template and the 3 `{% load %}`s (D5) |
| `sanitize_text.render_post_html` | Not a filter; imported by `game/consumers.py:13` | **Keep** |

### 5. Views, forms and templates

| Candidate | Evidence | Decision |
|---|---|---|
| 15 character `*CreateView`s (Changeling, CtDHuman, Demon, DtFHuman, Thrall, MtAHuman, Ghoul, Vampire, VtMHuman, Fomor, Werewolf, Kinfolk, WtAHuman, Wraith, WtOHuman) | Unrouted. Every type's create route is its `*BasicsView`, and chargen continues through the detail router. | **Delete** (D7). First move the `FORM_FIELDS` constants that the update views borrow (`ctdhuman.py:106`, `vtmhuman.py:125`). Remove the misnamed aliases `ChangelingCreateView as ChangelingCharacterListView` / `CtDHumanCreateView as CtDHumanCharacterListView`. Delete the two tests that only check a method exists (`test_demon.py:127-140`, `test_dtfhuman.py:87-100`); rename the route tests that actually exercise the Basics views. |
| `CharacterListView`, `VampireListView`, `GhoulListView`, `RevenantListView` and their `list.html` | Unrouted. `CharacterListView`'s template doesn't exist. The other three are plain `ListView`s with no visibility filter, so routing them would list hidden characters. The live replacement is `characters:index`. | **Delete** (D7) |
| `RevenantFamilyListView` | Every sibling vampire reference type (clan, coterie, discipline, path, sect, title) has a list route; `revenant_family/list.html` exists | **Recover**: route `characters:vampire:list:revenant_family` with `PUBLIC_READ` (D9) |
| `DroneUpdateView` | Every other Werewolf character type has update routes; `Drone.get_update_url`/`get_full_update_url` raise `NoReverseMatch` | **Recover**: `drone/<pk>/` → `DroneCharacterCreationView` (already `ROUTER`) and `drone/full/<pk>/` → `DroneUpdateView` (`OBJECT_WRITE`), following the kinfolk/fomor pattern (D9) |
| `SeptPositionUpdateView` | `SeptPosition.get_update_url` raises `NoReverseMatch`; every other Werewolf reference type has an update route | **Recover**: route `characters:werewolf:update:septposition` with `STAFF_WRITE` (D9) |
| `TremereChantryListView`, `BarrensListView` | Unrouted, but the templates exist and siblings are routed one line each | **Recover** (owner decision): list routes named `tremere_chantry` and `barrens` (the seeded object-type names), plus the `create:tremere_chantry` name, which fixes the index's Create 404 (D9) |
| `WerewolfFetishView`, `FeraFetishView` | `fetish` is an allowed background, but no chargen step resolves it. `form_class = None` crashes if routed. | **Deferred → Step 2** (owner decision); **keep** the classes |
| Mage chantry wizard (8 views, forms, templates) | Unrouted, but intended | **Recover**: see the chantry spec (C1–C5) |
| Superseded forms: `LimitedCharacterForm`, `LimitedCharacterEditForm`, `EarthboundCreationForm`, `WonderCreateOrSelectForm` (also broken), `MageFreebiesForm`, `GhoulFreebiesForm`, `VampireFreebiesForm`, `RevenantCreationForm`, `SorcererArtifactForm` | Only tests use them; each has a named live replacement (appendix and classification notes) | **Delete** (D7), with their tests and package exports. Keep `ArtifactCreateOrSelectForm`. |
| `PeriaptForm` (and the resonance form/formset in `items/forms/mage/periapt.py`) | Superseded by the `fields=[…]` views. Two of its rules exist nowhere else: arete ≥ rank, and current charges ≤ max charges. | **Recover the rules** into `Periapt.clean()` with tests (D9), then **delete** the module (D7) |
| `SphereForm`, `characters/forms/core/ability_form.py` (`HumanAbilityForm`), `attribute_form.py`, `attribute_block/form_pool.html` | The point-pool form family | **Deferred → Step 10** |
| `characters/core/human/abilities.html` | A counterpart of the attribute-step template; the live Human ability step renders a Wraith template. Its include path is also broken. | **Deferred → Step 2**, recorded as a bug |
| `HumanUrlBlock` | `Human` defines the same methods | **Delete** (D7); point `test_human_url_block.py` at `Human` or delete it |
| `core.linked_stat.MaxCurrentStat`/`PermanentTemporaryStat`; `core/widgets/linked_stat.py` (whole module); `core.utils.fast_selector`, `level_name`, `tree_sort`, `compute_level` | Unused. `level_name` is only re-exported. | **Delete** (D6), including the re-export at `locations/views/core/__init__.py:6,240` |
| `CreateOrSelectModelChoiceField`, `get_filterable_list_js`, `OptionMetadataSelectMultiple` | Only tests use them | **Delete** (D6); adjust the tests to the live APIs |
| `accounts.forms.StoryXP` | The only caller of `Story.award_xp`; nothing turns `StoryXPRequest`s into XP | **Recover** (owner decision): see *Story XP awards* (D10) |
| `locations.models.changeling.freehold.PowerChoices` | `Freehold.powers` checkboxes render with **no choices** in both `FreeholdPowersForm` and `FreeholdForm`, so no power can be picked | **Recover**: declare `powers` as `MultipleChoiceField(choices=PowerChoices.choices, widget=CheckboxSelectMultiple, required=False)` in both forms (D9) |
| Orphan templates: `human/create.html`, `human/basics_block_form.html`, `mage/create.html`, `mage/mage_basics_block_form.html`, `mage/effect/create.html`, `mage/spheres/display.html`, `tenet/display_includes/basics.html`, `corrupted_practice/…/specialization.html`, `specialized_practice/…/specialization.html`, `renownincident/…/temporary_renown.html`, `items/demon/relic/display_includes/{basics,powers}.html`, `locations/core/city/display_includes/basics.html`, `locations/core/location/display_includes/title.html`, `core/includes/{property_row,stat_card,stat_row}.html` | Unreferenced. **Detail-page rule checked:** each display include's fields are already shown on the live detail page, as the classification notes record. | **Delete** (D7), with `TestStatRowInclude`, `TestStatCardInclude` and `TestPropertyRowInclude` |
| `locations/demon/reliquary/display_includes/health.html` | The detail page shows health numbers but not the damage bar; `Reliquary.is_damaged()`/`damage_percentage()` are used only here | **Recover**: move the damage bar into `reliquary/display_includes/basics.html`, then delete the orphan (D9) |

### 6. URL and index hygiene

| Candidate | Evidence | Decision |
|---|---|---|
| 62 `app_name = "..."` assignments in `items/urls/**` and `locations/urls/**` | Have no effect: the modules export `urls`, and every include passes a list or a tuple, so Django never reads `app_name` | **Delete** (D8). The 20 similar ones in `characters/urls/**` go too. `game/urls.py:6` is **kept**, because it is included by module string. |
| `HomeListView` at `accounts:user` (`/accounts/`) | Duplicate of `core:home`; reversed only in one test | Replace with `RedirectView(pattern_name="core:home")` so `/accounts/` keeps working (D8) |
| `LOGIN_REDIRECT_URL = "user"`, `LOGOUT_REDIRECT_URL = "home"` | Neither resolves. **Logout returns a 500.** | Change both to `"core:home"` (D1, live bug) |
| `core.views.errors.error_401` | No `handler401` exists in Django | **Delete** the function and `test_errors.py:27-36` (D8). **Keep** `core/errors/401.html`, which `core/middleware/auth_error_handler.py:40` renders. |
| `ItemIndexView.items`, `LocationIndexView.locs` | Never read | **Delete** the attributes and the model imports that exist only for them. Their `__all__` re-exports go too, once the plan's `grep` for `from items.views.core import`/`from locations.views.core import` confirms nothing uses them (D8). |
| `ChantryDetailView` `factions` context | No template reads it | **Delete** (C5) |
| 30 alias detail routes, 69 unlinked page routes, 4 chargen routers | Routed pages | **Keep** (rule 1). Listed in the appendix for Step 7 and Step 2. |
| **43 index 404s**: seeded object types whose create/list route name doesn't exist | Appendix table *index-requested route fails* | **Deferred** (owner decision): items and locations → **Step 7**; characters (`dtf_human`, `htr_human`, `mtr_human`, 12 Fera breeds, `spirit_character`) → **Step 2**. **Exception:** `tremere_chantry` (create, list) and `barrens` (list) are fixed here (D9). A test asserting that every seeded type resolves is written by the owning step. |

### 7. Routed pages that fail because a template is missing (owner decision: A)

| Page | Problem | Decision |
|---|---|---|
| Logout | Invalid redirect setting | **Fix** (D1) |
| Demesne create/update (`locations/mage/demesne/form_include.html:1`) | `{% load widget_tweaks %}`, which isn't installed; the file uses none of its tags | **Fix**: drop the `{% load %}` (D1) |
| Demon, Thrall and DtF Human chargen (`…/chargen.html`); Demon ritual list/edit (`ritual/{list,form}.html`); Wraith full edit (`wraith/form.html`); Companion step 9 (`mage_wonder_block_form.html`); Fera step 10 (`core/human/allies_form.html`, `allies_display.html`); Drone (extends the missing `characters/core/character/chargen.html`) | The template doesn't exist; the page returns a 500 | **Keep routed; record as a known gap.** Chargen → **Step 2**; ritual and Wraith CRUD → **Step 7**. |
| `RitualCreateView` (demon, unrouted); `Ritual.get_creation_url` raises `NoReverseMatch` | Dead view with a broken reverse | **Deferred → Step 7**, together with the ritual pages above |

D1 adds `core/tests/test_routed_templates.py`. It walks every routed view and router target, resolves each template with `get_template()`, and compares the missing ones with an explicit `KNOWN_MISSING` allowlist. Each allowlist entry names its template, its view and its owning step. The test fails when a new page loses its template. It also fails when an allowlisted template is written but the entry isn't removed. No test is skipped or marked as an expected failure.

### 8. Chantry-area items

These are fully specified in the chantry spec. In summary:
- **Recovered:** `add_node`, `total_node`, `has_node` (fixed), `has_library`, `set_library` (fixed), `factional_names`, `display_name`, and the `points_spent` intent (rebuilt on `total_cost`).
- **Replaced:** `set_chantry_type` (the Library-type rule).
- **Deleted in C5:** `get_traits`, `set_rank`, `has_/set_season`, `has_chantry_type`, `has_/set_faction`, the duplicate IE table, the `factions` context, the `prominents` block, `personnel_form.html` and `LoadExamplesView`.

### Story XP awards (recover `StoryXP`, D10)

`Story` has no chronicle, and scenes don't link to stories. The only link between a story and characters is its `StoryXPRequest` rows, which STs create per character. So:

- **The form.** `StoryXP` is rebuilt around the story's requests: one row per `StoryXPRequest` (success, danger, growth, drama, duration), pre-filled from the request and editable by the ST. Fields are keyed by the request pk, not the character name.
- **Scope.** The form covers only characters that have a request for this story, replacing today's "every approved Human in the database".
- **`StoryXPAwardView`** is modelled on `SceneXPAwardView`: POST only, at `accounts:story_xp_award`, with an `ACCOUNT` manifest entry. The user must be staff, or a scoped ST (`PermissionManager.user_has_scoped_editor_role`) for **every** character in the story's requests. Otherwise the view refuses the whole award, and nothing is awarded partially.
- **Awarding.** `Story.award_xp` stays the single write path. It is atomic, sets `xp_given`, and refuses a second award. The view turns a `ValidationError` into the same "already awarded" message the Scene view uses.
- **Profile.** The placeholders at `accounts/views.py:319-320` become `storyxp_forms`, one per story with `xp_given=False` and at least one request the user may award, rendered like the scene forms.
- **Tests:**
  - the award applies the computed XP to each character;
  - a second POST is refused;
  - a non-scoped ST is refused and nothing is written;
  - an ST scoped for only some of the characters is refused;
  - the form lists only the story's requested characters;
  - `accounts/tests/forms/test_forms.py` (`TestStoryXPForm`) is updated.

## Audit verification ("Reported" items)

| Reported item | Result |
|---|---|
| `resonance.py`, `conditional_wrap`/`as_conditional` unused | **Confirmed** |
| `ItemIndexView.items`, `LocationIndexView.locs` never read | **Confirmed** |
| `game_location_types` never read | **Refuted**: it no longer exists (removed by `446eee3`) |
| `ChantryDetailView` `factions` context unused | **Confirmed** |
| `error_401` without `handler401` | **Confirmed** |
| 62 no-op `app_name` assignments | **Confirmed**: exactly 62 in 62 files (25 items, 37 locations); 20 more in `characters/urls/**` |
| `HomeListView` routed twice | **Confirmed** (`core:home`, `accounts:user`) |
| `core.context_processors.permissions` unregistered | **Confirmed** (the only unregistered processor) |
| 7 orphan `load_*_dropdown_list.html` templates | **Confirmed** |
| Views referencing missing templates | **Confirmed, and they are worse than dead references.** Most are **routed and return a 500** (section 7). The scan also found the Drone base template, the Demesne `widget_tweaks` load and the broken include in `human/abilities.html`. |
| `core/views/reference.py` only re-exported | **Confirmed**; **Deferred → Step 7** |

The audit's "Confirmed" items 1–8 were re-checked and hold, with these additions:
- `FreebieApprovalMixin` has no tests at all.
- The second `STRequiredMixin` became unused with Step 0.
- The AJAX removal also makes `core/ajax.py` and its view bases and the `OBJECT_AJAX` policy dead.

## Removal safety

- **INSTALLED_APPS and migrations.** Only `chained_select` leaves `INSTALLED_APPS`. It has no models, tables or migrations, so no migration or data step is needed. No deleted symbol is referenced by a migration.
- **Static files.** No project static file references any deleted endpoint or tag; the only tracked JS is vendored Bootstrap. `collectstatic` output is unaffected.
- **`populate_db/` and management commands.** None import deleted code. The seeded `ObjectType` rows are untouched; the index 404s are deferred except the three fixed in D9.
- **Tooling.** `scripts/build_route_policy_manifest.py` and `scripts/inventory_authorization_routes.py` are updated in the same PR as any class they name.
- **Per-PR checks** (the plan lists the exact commands):
  1. the full test suite passes;
  2. `python manage.py check` passes;
  3. the route-policy test passes;
  4. `scripts/find_dead_code.py` has fewer rows in the affected section, and none reappear;
  5. the resolver route count changes exactly by the routes the PR deliberately adds or removes, which catches rule 3's silent URL loss.
- **Test baseline.** The full suite is recorded on `main` before D1. Parallel runs currently crash in Django's runner with an unpicklable traceback, so the baseline and the per-PR checks run serially until that is fixed.

## Rollout (combined PR order)

The order is lowest risk first. Each PR can be merged on its own and leaves the suite green. C1–C5 are defined in the chantry spec.

| # | PR | Contents |
|---|---|---|
| 1 | **D1: safety net and live 500s** | Heuristic unit tests for `find_dead_code.py`. The routed-template inventory test with its `KNOWN_MISSING` allowlist. The logout redirect fix. The Demesne `{% load %}` fix. |
| 2 | **C1: character-wizard Chantry step** | Fixes the live 500 (chantry spec). |
| 3 | **D2: dependency** | Remove `django-smart-selects`. |
| 4 | **D3: `chained_select`** | Remove the app, its settings entry, its compatibility tests and the widgets-side copies. |
| 5 | **D4: AJAX endpoints** | 11 endpoints (the chantry one waits for C5), the population views, the dropdown templates, the empty `ajax.py` modules, the unused `core/ajax.py` bases, the `OBJECT_AJAX` policy and the manifest/tooling updates. |
| 6 | **D5: template tags** | Section 4. |
| 7 | **D6: mixins, decorators and utilities** | Sections 2 and 5 (`linked_stat`, `utils`, `widgets` leftovers, the cache helpers, the middleware). |
| 8 | **D7: superseded views, forms and templates** | Section 5 deletions. |
| 9 | **D8: URL and index hygiene** | Section 6. |
| 10 | **D9: small recoveries** | SeptPosition, Drone and RevenantFamily routes; the Tremere Chantry and Barrens lists plus `create:tremere_chantry`; Freehold `PowerChoices`; the Reliquary damage bar; `Periapt.clean()`. |
| 11 | **C2–C4: the chantry wizard** | Points service and schema, submission/revision hooks, going live. |
| 12 | **C5: chantry cleanup** | Includes `load_chantry_examples`. |
| 13 | **D10: Story XP awards** | The Story XP section above. |

## Deferred register

These are known gaps, not deletions. Each owning step gets these rows.

| Owner | Items |
|---|---|
| Step 2 (chargen) | Werewolf/Fera Fetish step. Missing chargen templates: Demon, Thrall, DtF Human, Companion step 9, Fera step 10, the Drone base. `human/abilities.html` and the Human ability step that renders a Wraith template. Werewolf, Demon, DtF Human and Thrall freebies forms whose example dropdowns lost their data source. Character object-type index 404s. 4 unlinked chargen routers. |
| Step 6 (permission context) | `core/templatetags/permissions.py`, `core.context_processors.permissions` |
| Step 7 (items/locations registry) | `core/views/reference.py`. Item and location object-type index 404s. 30 alias detail routes and the unlinked item/location page routes. Demon ritual list/edit/create and the Wraith full-edit page. |
| Step 10 (htmx chargen) | `attribute_form.py`, `attribute_block/form_pool.html`, `ability_form.py`, `SphereForm` |

## Non-goals

- Writing missing templates (section 7), except where a recovery above needs a template line.
- Renaming routes or seeds to fix the deferred index 404s.
- Deleting routed pages, even ones nothing links to.
- Refactoring code that is kept.

## Acceptance criteria

1. Every row marked **Delete** is gone, together with the tests that existed only for it. `find_dead_code.py` no longer reports it.
2. Every **Recover** row works, and a test covers it.
3. Every **Deferred** and **Keep** row is untouched and appears in the deferred register or the appendix.
4. The logout and Demesne pages work, and `test_routed_templates.py` fails on any new missing template.
5. The full suite, `manage.py check` and the route-policy test pass after every PR, and route counts change only as intended.
