# Dead-Code Removal (Step 1) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Carry out every decision in the Step 1 dead-code design: delete what is dead, recover what was meant to be used, keep routed pages, and leave deferred items to their owning steps. First, fix the 5 stale tests on `main` so the suite starts at 0 failures.

**Architecture:** The work comes in units, each a contiguous, separately reviewable run of commits on `code-improvements`, in the spec's rollout order: B0, D1, (chantry C1), D2–D9, (chantry C2–C5), D10. Removals follow a guard-test cycle: a test in `core/tests/test_dead_code_removed.py` fails while the dead code exists, then the code is deleted. Recoveries use normal TDD. Route changes always update `core/route_policy_manifest.py` in the same commit.

**Tech Stack:** Django 5.2, django-polymorphic 4.1, Django `TestCase`/`SimpleTestCase`, `scripts/find_dead_code.py`, ruff.

**Spec:** `docs/superpowers/specs/2026-09-25-dead-code-removal-design.md` (appendix: `2026-09-25-dead-code-removal-report.md`). The chantry units live in `docs/superpowers/plans/2026-09-25-chantry-creation-flow.md`, which implements `docs/superpowers/specs/2026-09-25-chantry-creation-flow-design.md`.

## Global Constraints

- Only push to branch `code-improvements`.
- Commit messages end with the two trailer lines `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23`.
- Tests run **serially**: `python manage.py test <label>`. Parallel runs crash in Django's runner.
- **Baseline:** after Unit B0 the full suite has **0 failures**, and every later unit keeps it at 0. This supersedes the spec's earlier "exactly 5 failing" rule.
- A route is deleted only if it is a JSON/AJAX endpoint that nothing calls. Routed pages are kept, even when nothing links to them.
- Every URL addition or removal updates `core/route_policy_manifest.py` in the same commit. `core/tests/security/test_route_policies.py` must pass.
- `characters/urls/__init__.py` and `locations/urls/__init__.py` swallow `ImportError`. Remove `from . import ajax` in the same commit as the module it imports, and compare route counts before and after.
- Deleting a class also removes its package `__init__` import and its `__all__` entry.
- Before deleting a model method or display include, check whether it belongs on the model's detail page. If it does, recover it.
- Never touch deferred items: `core/templatetags/permissions.py`, `core.context_processors.permissions` (Step 6); `core/views/reference.py` (Step 7); `attribute_form.py`, `attribute_block/form_pool.html`, `ability_form.py`, `SphereForm` (Step 10); the Fetish views and `human/abilities.html` (Step 2).
- Never skip, disable or quarantine a test. Ruff gates require **no new** ruff errors in touched files: `ruff check` only, because `ruff format` disagrees with the repo's black formatting.

## Review Focus

- **A deleted `ajax.py` still imported by a gameline URL loader.** The whole gameline's routes vanish silently. Each D4 task pins this with a route-count check.
- **Deleting a symbol still reached indirectly** (string import, template include, `__all__` re-export, JS string constant). The expected behaviour is that nothing a user can reach changes. Each removal task's guard test, plus the unit gate's full suite and `find_dead_code.py` run, pin this.
- **A recovered route missing its manifest entry.** In production that is a 403, because the middleware fails closed. The route-policy test in every D9 task pins it.
- **The `accounts:user` redirect and cached home page.** A redirect must still reach home when the page cache is warm. D8.2's test clears the cache and asserts the redirect chain.
- **Story XP awarded by an ST scoped to only some of the story's characters.** The expected behaviour is refusal with nothing written. D10's partially-scoped test pins it.

## Drafting notes

These are facts discovered while the plan was drafted and verified against scratch clones of `1e77e23`. They apply across units.

#### From `01-baseline-and-D1.md`

- **New baseline.** After B0 the full suite has **0 failing tests**. The spec's "exactly these 5 failing" rule (Removal safety → Test baseline) is superseded: every later unit must keep the suite at 0 failures. Update each PR-description checklist accordingly.
- **Test counts.** At `1e77e23` the suite has 7,105 tests. B0 adds 2 and D1 adds 37 (26 heuristics + 1 TSV + 3 auth redirects + 2 Demesne + 5 routed-template), so 7,144 after D1. Verified: with every B0 and D1 change applied to a scratch clone of `1e77e23`, `python manage.py test` gave `Ran 7144 tests … OK (skipped=49)`.
- **Product gap found in B0 (not fixed, report to the owner).** `readable_chronicles()` has no "player member" concept: a player is in a chronicle only by already owning a character there. A brand-new player therefore cannot pick any chronicle in a Basics/create form (the dropdown is empty; they can only create without a chronicle), and `CircleCreateView` (no `ScopedCreationFormMixin`) still lists every chronicle and answers 403 on submit rather than a form error. Neither is a security hole; both are UX follow-ups for the Step 0 owner. B0 deliberately does not touch production code.
- **`CustomLoginView` ignores `?next=`** (verified: login with `?next=/game/` still lands on the profile). Out of scope for D1; worth a row in the deferred register (accounts).
- **Demesne create POST**: with an empty reality-zone formset the form refuses with "Positive Reality Zone Ratings must sum to Demesne rating" (a game rule, not a bug). D1.4 only tests GET rendering.
- **`KNOWN_MISSING` is a contract for later units.** Any unit that writes one of the 10 templates (Step 2 chargen templates, Step 7 ritual/Wraith pages) must delete its entry in the same commit, or `test_known_missing_templates_are_still_missing` fails. Any unit that routes a new view (C4 routes the chantry wizard; D9 routes `DroneUpdateView`, `SeptPositionUpdateView`, `RevenantFamilyListView`, `TremereChantryListView`, `BarrensListView`) is now checked by `test_no_new_missing_templates`. I pre-checked those: every chantry wizard step (`locations/mage/chantry/locgen.html`), `ChantryBasicsView`, `ChantryCreateView`/`ChantryUpdateView` (`chantry/form.html`) and all five D9 views resolve their full template chain today, so none needs an allowlist entry. A view added with no `template_name` gets Django's derived name (e.g. `characters/drone_form.html`), which usually does not exist — set `template_name` explicitly.
- **Deleting views (D4/D7)** cannot break `test_routed_templates.py` unless a deleted class is named in `KNOWN_MISSING` (none are: `RitualUpdateView`, `RitualListView`, `WraithUpdateView` and the chargen step views are all kept). If D4 changes `scripts/inventory_authorization_routes.py` (it drops the `AjaxLoginRequiredMixin` import), `descendants` must keep its signature: both `test_route_policies.py` and `test_routed_templates.py` import it.
- **Names introduced:** module `scripts/dead_code_heuristics.py` (exports `URL_FUNCS`, `TEMPLATE_FUNCS`, `CALL_CTX`, `SEED_METHODS`, `PAGE_KINDS`, `call_name`, `object_type_seed`, `str_parts`, `find_computed`, `pattern_regex`, `classify_dead_route(view, name, route, *, alias_target, router_bases)`); tests `core/tests/test_dead_code_heuristics.py`, `core/tests/test_routed_templates.py` (`KNOWN_MISSING`, `NON_RENDERING_VIEWS`, `missing_routed_templates()`), `accounts/tests/views/test_auth_redirects.py`; `locations/tests/views/mage/test_demesne.py` now holds `DemesneFormPagesTest`. `scripts/` stays in `find_dead_code.SKIP_DIRS`, so the new module is not itself scanned.
- **`scripts/` is a namespace package** (no `__init__.py`); `from scripts.… import …` works because tests run from the repo root. Do not add an `__init__.py` casually: the existing imports already rely on this.
- **Pre-existing ruff error** in a file B0 touches: `characters/tests/views/mage/test_companion_comprehensive.py` F841 (line 277 → 281 after B0.3), inside a skipped AJAX test class that D4 deletes. Unit gates should require "no new ruff errors", not "zero".
- **Spec wording to correct:** section 7 calls `mage_wonder_block_form.html` "Companion step 9" and the allies includes "Fera step 10". They are included (inside `{% if creation_status == … %}`) by the shared `characters/mage/companion/chargen.html` and `characters/werewolf/fera/chargen.html`, so every Companion step (14 views) and every Fera step (11 views) reaches them; the Companion page 500s at step 9, and the Fera page at step 10 and every later step (`allies_display.html` renders for `creation_status > 10`). `KNOWN_MISSING` names one representative view per template; the test checks that view is among those reaching it.

#### From `02-D2-D3-D4.md`

- **Shared guard module:** `core/tests/test_dead_code_removed.py`, created in Task D2.1. Its helper mixin `RemovalAssertions` provides `assertRequirementRemoved`, `assertModuleRemoved`, `assertAttributesRemoved(module, *names)` (also checks `__all__`), `assertUrlNamesRemoved`, `assertUrlNamespaceRemoved("a:b:c")` and `assertTemplatesRemoved`, plus `REPO_ROOT`. Convention: one `D<n>…RemovedTest(RemovalAssertions, SimpleTestCase)` class per PR, appended at the end. After D4 the module imports `importlib`, `importlib.util`, `re`, `Path`, `settings`, `TemplateDoesNotExist`, `get_template`, `SimpleTestCase`, `NoReverseMatch`, `get_resolver`, `resolve` and `reverse`. If D5–D10 run before D4 lands, they must add a missing import themselves (`resolve` is added in Task D4.2).
- **Guards must not spell a kept-but-dead URL name.** `find_dead_code.py` counts any test occurrence of a name as "tests only". That is why the chantry keep-guard resolves a path and compares `view_class`.
- **C5 must:** delete `locations/urls/mage/ajax.py` together with its `from . import ajax` and `include()` in `locations/urls/mage/__init__.py` (rule 3; `test_every_gameline_urlconf_still_mounted` catches a miss). Remove `locations.views.mage.chantry.LoadExamplesView` from the manifest's `LOGIN` group. Delete `core/ajax.py` and `core/tests/test_ajax.py` (only `TestDropdownOptionsResponse` remains in it). Delete `test_chantry_ajax_endpoint_kept_until_c5`. Extend `test_ajax_view_bases_removed` with `self.assertModuleRemoved("core.ajax")`, and `test_empty_gameline_ajax_modules_removed` with `locations:mage:ajax`. Expected route delta −1 (`locations/mage/` 46 → 45 at `1e77e23`).
- **Spec corrections:**
  1. `core/ajax.py` cannot be deleted in D4: `dropdown_options_response` is still used by the chantry `LoadExamplesView`. D4 removes only `simple_values_response`.
  2. The spec's per-endpoint test list is incomplete. D4 also deletes the whole of `characters/tests/views/core/test_character.py`, not only lines 37–150, because the rest is a comment. It also deletes the empty `TestWraithFreebieFormPopulationView` (`test_wraith_chargen.py:406`), `CharactersAjaxUrlsTest` (`characters/tests/urls/test_url_patterns.py:111`) and `test_characters_ajax_namespace` (`core/tests/urls/test_url_namespaces.py:72`). The last two pass whether or not the namespace exists, because `/characters/ajax/` resolves to `characters:character`. `test_public_detail_authorization.py`'s AJAX cases are lines 232–247 (the file ends at 247), and they leave `ObjectType` unused.
  3. `characters/views/mage/mage.py:8-37` (`_calculate_xp_cost`, `_mage_sphere_xp_cost`, `_mage_practice_xp_cost`, and the `characters.costs` import) die with `LoadXPExamplesView`; the spec does not list them. That view also called `get_meritflaw_xp_cost` with one argument, a latent `TypeError` that is now moot.
  4. `scripts/inventory_authorization_routes.py` also names `"OBJECT_AJAX"` (line 180), not only `AjaxLoginRequiredMixin`.
  5. `git rm -r chained_select` leaves ignored `__pycache__/`, which keeps `chained_select` importable as a namespace package. `rm -rf chained_select` is required.
  6. The spec's baseline is 7,104 tests at `093e3cc`; at `1e77e23` discovery finds 7,105.
- **Tooling:** do not use `scripts/build_route_policy_manifest.py` to regenerate or check the manifest. At `1e77e23` its output differs from the committed manifest by 16 lines. Its per-policy counts after D4 match (`LOGIN: 36`, no `OBJECT_AJAX`).
- **Generated docs:** `*/docs/*.html` and `docs/code-overview.json` (generated code-overview pages; no generator is in the repo) still link to `chained_select/docs/*.html` and list the deleted templates. They were left untouched as generated artifacts; regenerate them with the tool that produced them if wanted.
- **Line numbers:** the numbers here are at `1e77e23`. B0.3 shifts `test_companion_comprehensive.py` by +4 from line 13 on (noted in Task D4.2). C1 (character-wizard Chantry step) may edit `characters/views/mage/mage.py`. Match the quoted anchors, not the line numbers. D1's `test_routed_templates.py` imports `descendants` from `scripts/inventory_authorization_routes.py`; Tasks D4.4/D4.5 leave `descendants`, `walk` and `get_resolver` unchanged.
- **Ruff baseline:** 14 non-E402 ruff violations and 42 E402s remain in D4-touched files, all pre-existing (listed in the D4.1/D4.2 verify steps). None is introduced. Six touched files were already not `ruff format`-clean and must not be reformatted in these PRs.

#### From `03-D5-D6.md`

- **Verified end to end.** Every D5 and D6 edit above was applied in a scratch worktree at `1e77e23`. The combined guard (`D5RemovedTests` + `D6RemovedTests`, 15 tests) fails with 55 subtest failures at `1e77e23` and passes after the edits; the two Keep guards pass throughout. Affected-app runs were green (`core.tests widgets.tests locations.tests`: 1,929 tests OK; `core.tests.templatetags widgets.tests items.tests locations.tests.views game.tests`: 1,429 OK). Full serial suite with D5+D6 applied on `1e77e23` (without B0): `Ran 7013 tests … FAILED (failures=5, skipped=49)`, exactly the 5 baseline failures B0 fixes and nothing else. Route count is 1,833 before and after (D5/D6 touch no URL, so `core/route_policy_manifest.py` is untouched, rule 2).
- **Guard-file coordination.** D5/D6 append two classes and use only function-local imports, so they never edit the module header D4 creates. Each class defines its own `_module_exists` staticmethod to avoid depending on a D4 helper; if D4 already has an equivalent module-level helper, the classes can call it instead, but that is optional.
- **Extra test found beyond the design's test column:** `core/tests/mixins/test_mixins.py:138-167` `ObjectCachingMixinTest.test_st_required_mixin_caches_object` also uses the deleted `STRequiredMixin` (the design lists only 950–1040 for that class). D6.1 deletes it. Design line ranges for `test_permissions_deployment.py` (410–412, 392–394) are one line short of the trailing/leading blank line; D6.1 uses 392–395 and 409–412.
- **CRLF files.** `core/templatetags/dots.py`, `items/templatetags/__init__.py` and `items/templatetags/item_filters.py` are CRLF; the last two are deleted whole. D5.2 truncates `dots.py` with `head -n 118` so the diff is a pure 221-line deletion.
- **`items/templatetags/` package is removed entirely** (its `__init__.py` holds only a comment) and so are `items/tests/templatetags/` and `locations/tests/templatetags/` (their `__init__.py` files are empty). `locations/templatetags/` never had an `__init__.py` (a namespace package). No other app loads from these packages.
- **Stale agent/instruction docs (owner decision, not edited by this plan):** `CLAUDE.md:106` shows `from core.mixins import (…, STRequiredMixin, …)`; `.claude/skills/tg-standards/references/permissions.md:17,21` lists `SpendXPPermissionMixin` and `STRequiredMixin`; `.claude/skills/tg-standards/references/views.md:13,24` imports and stacks `STRequiredMixin`. After D6 those imports raise `ImportError`. Suggested fix: replace `STRequiredMixin` with the live chronicle-scoped `StorytellerRequiredMixin` in all three and delete the `SpendXPPermissionMixin` line. These are agent-instruction files, so they need the owner's explicit OK; add them to D6.1's commit if approved.
- **Other stale docs left alone:** `core/README.md` still shows `from core.permissions import user_can_edit_object` (no such function) and points to `pytest core/tests/` and `core/test_permissions.py` (neither applies). D6.2 only removes the decorator references it owns.
- **Newly test-only method (not a module-level symbol, so the script cannot flag it):** `core.cache.CacheKeyGenerator.make_model_key` was used only by `get_cached_queryset`; after D6.3 only `core/tests/test_cache.py` calls it. `CacheInvalidator.invalidate_model_cache` still clears the `queryset` key category, which nothing writes any more. Both are kept (non-goal: refactoring kept code); list them for Step 6/7 cache work if wanted.
- **`widgets/docs/*.html`, `core/docs/*.html`, `locations/docs/health.html`, `docs/health.html`, `docs/codemap.html`** are generated snapshot reports that mention some deleted names; they are not code and are not regenerated here.
- **Order sensitivity with D3/D4.** D3 edits `widgets/__init__.py` and `widgets/widgets/__init__.py`; D4 edits `core/mixins.py` (and may drop its `View` import). D6's snippets never overlap their lines, but the absolute line numbers quoted for those three files are valid only at `1e77e23`; match on text.
- **Test-count bookkeeping (verified by diffing discovered test ids).** D5 removes 40 tests and adds 7 guards (net −33); D6 removes 69 and adds 8 (net −61); `test_get_filterable_list_js_returns_string` is renamed to `test_filterable_list_js_is_string`. At `1e77e23` discovery finds 7,105 tests; with D5+D6 applied (and no other unit) it finds 7,011. Other units shift the absolute number, so each gate compares against its own pre-unit run.

#### From `04-D7-D8.md`

- **`items/forms/mage/periapt.py` is not deleted in D7.** Its `PeriaptForm.clean()` holds the only copies of two rules (arete ≥ rank; current charges ≤ max charges), which D9 moves into `Periapt.clean()`. D9 runs after D7, so deleting the module in D7 would lose the rules for one PR. **Move the deletion of `items/forms/mage/periapt.py` (with its `from .periapt import PeriaptForm` / `"PeriaptForm"` entries in `items/forms/mage/__init__.py` and its tests) into D9, after the rules are recovered.** D7 leaves `items/forms/mage/__init__.py` as `from .periapt import PeriaptForm` / `from .wonder import WonderForm` / `__all__ = ["PeriaptForm", "WonderForm"]`.
- **The spec holds for every D7/D8 item** after re-checking at `1e77e23`; no item had to be kept. Details the spec didn't mention:
  - Only two `FORM_FIELDS` lists are borrowed (`ctdhuman.py:106`, `vtmhuman.py:125`). `MageCreateView.FORM_FIELDS` is routed and unrelated.
  - `characters/forms/vampire/freebies.py` goes whole (`VAMPIRE_CATEGORY_CHOICES` is used only by the two deleted forms and their test).
  - `TestImageUploadForm` in `characters/tests/forms/core/test_character.py` also tests only `LimitedCharacterEditForm`, so it goes too.
  - `characters/tests/views/vampire/test_revenant.py` is a 5-line stub about `RevenantListView`.
  - `characters/README.md` and `.claude/skills/tg-standards/references/permissions.md` named deleted classes and are updated.
  - `.claude/skills/tg-standards/references/urls.md` documented the `app_name` pattern and is rewritten to the real one.
  - `HumanUrlBlock`'s test is retargeted to `Human` and renamed `test_human_urls.py`, not deleted.
- **Interaction with D4–D6 (line drift).**
  - D4 edits `characters/views/demon/__init__.py`, `characters/views/mage/__init__.py` and the top of `characters/views/werewolf/garou.py`, and deletes the `ajax.py` URL modules. So D8.1's file count is 82 minus those modules; the script and the guard handle whatever remains.
  - D6 removes `level_name`/`tree_sort` from `locations/views/core/__init__.py` lines 6/240–241. D8.4 doesn't touch those lines.
  - Quote-based locating is given for every edit.
- **Guard-test file.** Helpers `assert_names_absent` / `assert_modules_absent` / `assert_templates_absent` are methods on `D7RemovedTests`, so they don't clash with anything D4–D6 put in the shared module. The `app_name` guard walks files rather than using `pkgutil`, because `characters/urls/core`, `items/urls/core` and `locations/urls/core` have no `__init__.py` (namespace packages) and `pkgutil.walk_packages` skips them. That would miss 13 modules.
- **Pre-existing lint.** Only `ruff check` is gated. `ruff format` (0.3.4) disagrees with the repo's black formatting on three touched files at `1e77e23` (`werewolf/fomor.py`, `werewolf/garou.py`, `models/werewolf/test_kinfolk.py`). D7.1's F401 fix incidentally drops the already-unused `Background` import in `garou.py`.
- **Left alone on purpose:**
  - `items/views/core/__init__.py` also re-exports never-used imports (`defaultdict`, `Http404`, `get_gameline_name`) through `__all__`. `locations/views/core/__init__.py` does the same with `Http404` and `get_gameline_name`.
  - They are outside the spec's "model imports used only by `items`/`locs`" scope and are left for Step 7.
  - `core/tests/views/test_errors.py::TestPermissionDenied` posts to `accounts:user` and accepts 302. It is unchanged, but it no longer tests a permission path; Step 6/7 may want to retarget it.
- **Verification performed.** Every task was applied to a throwaway worktree at `1e77e23`, in this order: D7.1–D7.5, then D8.1–D8.4.
  - All guard tests failed before their change and passed after (D7: 72 failing subtests + 1 error before; D8 `app_name`: 82 failing subtests before).
  - The targeted D7 test set ran 468 tests: 1 failure, the baseline `test_basics_view_creates_vtmhuman`.
  - `manage.py check` was clean.
  - The route inventory was unchanged after D7 and changed only on the `accounts:user` callback after D8 (1833 routes at `1e77e23`).
  - `find_dead_code.py` lost exactly the rows listed in the gates, and no new rows appeared.
  - `ruff check` found no new findings.
  - Full suite on `1e77e23`+D7+D8: 7032 tests, 49 skipped. Failures were the 5 baseline ones plus `accounts…TestProfileView.test_template_logged_out`. That test broke because of D8.2: the redirect now lands on the `cache_page`'d `/`. D8.2 Step 3 now includes the fix, which was verified.
  - **D7 alone adds no failures.** That test is the only one outside the baseline set, and it is caused by D8.2.

#### From `05-D9-D10.md`

- **Verified.** Every test and implementation above was run in a throwaway worktree of `1e77e23` (no D1–D8 applied): each failing run failed as stated, each passing run passed, `manage.py check` and `test_route_policies` pass, and the resolver count went 1833 → 1841 (+7 for D9, +1 for D10). Full serial suite on the combined D9+D10 worktree: `Ran 7127 tests`, `FAILED (failures=5, skipped=49)`, the 5 failures being exactly the spec's baseline set; 0 errors.
- **Baseline vs "0 failures".** The spec's baseline has 5 failing tests unrelated to these units (listed in *Removal safety*); the gates accept exactly those. If an earlier unit fixes them, the gate becomes "0 failures".
- **Dependencies on earlier units.** D9.7 assumes D7 left `items/forms/mage/periapt.py` and its test in place (per the spec it does) and may or may not have removed `SorcererArtifactForm` from `items/forms/mage/__init__.py`; the edit only touches the `PeriaptForm` line and `__all__` entry. D8's removal of `app_name` lines does not affect the anchored inserts in `locations/urls/vampire/*.py`. D9.2 references D1's `core/tests/test_routed_templates.py`/`KNOWN_MISSING`; I could not see D1's final shape, so the step says what to do if the new `drone/<pk>/` route surfaces the known Drone chargen gap.
- **Drone router GET is untested on purpose.** `drone/<pk>/` dispatches to Drone chargen steps whose template extends the missing `characters/core/character/chargen.html` (Step 2 gap), so D9.2 tests only that the URL resolves to `DroneCharacterCreationView`. Note that kinfolk's `kinfolk/<pk>/` points at `KinfolkUpdateView`, not a router; the spec (and this plan) follow the fomor/fera shape for Drone.
- **Periapt rules are model-level and non-field.** Copied messages verbatim; errors are non-field so `core/form.html` shows them and model forms without `arete`/`current_charges` don't hit Django's `ValueError` for field-keyed model errors. This changes behaviour for any stored Periapt with `arete < rank` or `current_charges > max_charges`: its next save raises. There are no such rows in `populate_db`; production data was not checked; consider a one-off query before release (`Periapt.objects.filter(arete__lt=F("rank"))`, `...filter(current_charges__gt=F("max_charges"))`).
- **Freehold behaviour change.** `powers` now rejects values outside `PowerChoices` (the old `JSONField` form field accepted any list). The existing tests only post valid values.
- **Story XP decisions to confirm:**
  - *Profile filter.* The spec says "at least one request the user may award"; the plan lists only stories whose **every** requested character the user may award, because the view refuses anything less (a listed form would always 403). Switch `get_storyxp_forms` to `any(...)` if the owner prefers to show partially-scoped stories.
  - *Refusal = 403.* Follows `verify_st_for_chronicle` (message + `PermissionDenied`), the convention of `SceneXPAwardView`. A story with no requests is not an authorization failure: it redirects with an error message and writes nothing.
  - *Duplicate requests* for one character in one story (no DB constraint prevents them) merge by OR-ing booleans and taking the max duration, so accidental duplicates never double-award. Alternative: reject the form.
  - *Whose scope.* The profile uses `self.object.user` (like the scene forms); only the profile owner sees the section anyway (`user == object.user` in `detail.html`). A staff user who has no `STRelationship` does not see the ST sections at all (`object.is_st`), exactly like the scene forms, but can still POST to the award view.
- **Not recovered here:** the player-side `accounts/includes/xp_story.html` include stays commented (it only has a heading); `Profile.xp_story()`/`dashboard.xp_story()` remain unused by the profile context.
- **Tooling.** After both units, `scripts/find_dead_code.py` should no longer report `RevenantFamilyListView`, `DroneUpdateView`, `SeptPositionUpdateView`, `TremereChantryListView`, `BarrensListView`, `PowerChoices`, `health.html`, `PeriaptForm` or `StoryXP`; run it per the spec's per-PR check 4 (after D1 makes it side-effect free).

---

## Unit B0: Fix the 5 pre-existing failing tests

**Diagnosis (run at `1e77e23`; all five reproduced).** All five failures are **stale tests**, not code bugs. They were written before Step 0 (`446eee3`, and the create-form scoping added in `b4f2155` "Address authorization hardening review feedback") and post a `chronicle` that the logged-in user has no part in. Step 0 intentionally made that invalid:

- `game.security.readable_chronicles(user)` returns only chronicles where the user is `head_st`, a `game_storytellers` member, has an `STRelationship`, or **owns a `CharacterModel`** (`played`). Staff see all.
- `core.mixins.ScopedCreationFormMixin.get_form` narrows `form.fields["chronicle"].queryset` to `readable_chronicles(self.request.user)`, so an unrelated chronicle is a form error ("Select a valid choice…") and the view re-renders with **200** instead of redirecting.
- `core.mixins.prepare_created_object(form, request)` (called from `MessageMixin.form_valid`, `core/mixins.py:432`, and from `CompanionBasicsView.form_valid`) raises `PermissionDenied("Cannot create an object in this chronicle")` for the same case when the form did **not** scope the field, giving **403**.

| Test | Observed | Root cause (verified in a Django test shell) | Verdict |
|---|---|---|---|
| `test_vampire_chargen.TestVampireBasicsView.test_basics_view_creates_vampire` | 200 ≠ 302 | `VampireBasicsView` uses `ScopedCreationFormMixin`; `form.errors == {"chronicle": ["Select a valid choice. That choice is not one of the available choices."]}`. `testuser` owns nothing in `self.chronicle`. | Test stale |
| `test_ghoul_chargen.TestGhoulBasicsView.test_basics_view_creates_ghoul` | 200 ≠ 302 | Same (the `setUp` domitor Vampire has no chronicle). | Test stale |
| `test_vtmhuman.TestVtMHumanBasicsView.test_basics_view_creates_vtmhuman` | 200 ≠ 302 | Same. | Test stale |
| `test_circle.TestCircleCreateView.test_create_circle_successfully` | 403 ≠ 302 | `CircleCreateView(LoginRequiredMixin, MessageMixin, CreateView)` has no `ScopedCreationFormMixin`; the chronicle passes form validation, then `MessageMixin.form_valid` → `prepare_created_object` → `PermissionDenied`. The sibling `test_create_circle_with_leader_adds_to_members` passes only because it first creates a `Human` owned by the user in the chronicle. | Test stale |
| `test_companion_comprehensive.TestCompanionCreationWorkflow.test_other_player_cannot_attach_companion_to_mage` | 200 ≠ 403 | The test means to prove the `companion_of` ownership check in `CompanionBasicsView.form_valid` (`characters/views/mage/companion.py:251-265`). But `other` has no part in the chronicle, so `ScopedCreationFormMixin` rejects the chronicle first (form error, 200) and the `companion_of` check is never reached. The security property (nothing created) still holds. | Test stale (its setup no longer reaches the code under test) |

**Fix, for every test:** make the acting user a legitimate participant of the chronicle by giving them an existing character there (`Human.objects.create(name=…, owner=<user>, chronicle=self.chronicle)`, the same fixture `test_create_circle_with_leader_adds_to_members` already uses). No production code changes; no security check is weakened. To keep the Step 0 behaviour pinned, B0.1 and B0.2 each add a test asserting that the unrelated chronicle is refused (form error for the scoped Basics form; 403 for Circle). Verified in a scratch copy: all five pass, the two new tests pass, and the companion test now gets its 403 from the `companion_of` check.

### Task 1: [B0.1] Vampire, Ghoul and VtM Human Basics tests join the chronicle first

**Files:**
- Modify (test): `characters/tests/views/vampire/test_vampire_chargen.py` (imports lines 19-25; `test_basics_view_creates_vampire` lines 138-157)
- Modify (test): `characters/tests/views/vampire/test_ghoul_chargen.py` (imports lines 18-23; `test_basics_view_creates_ghoul` lines 114-131)
- Modify (test): `characters/tests/views/vampire/test_vtmhuman.py` (imports lines 17-19; `test_basics_view_creates_vtmhuman` lines 121-138)

**Interfaces:**
- Consumes: `characters.models.core.human.Human`; URL names `characters:vampire:create:vampire`, `characters:vampire:create:ghoul`, `characters:vampire:create:vtm_human`; `core.mixins.ScopedCreationFormMixin` behaviour.
- Produces: new test `TestVampireBasicsView.test_basics_view_rejects_chronicle_user_is_not_in`.

- [ ] **Step 1: Confirm the three failures and their cause**

```bash
python manage.py test characters.tests.views.vampire.test_vampire_chargen.TestVampireBasicsView.test_basics_view_creates_vampire characters.tests.views.vampire.test_ghoul_chargen.TestGhoulBasicsView.test_basics_view_creates_ghoul characters.tests.views.vampire.test_vtmhuman.TestVtMHumanBasicsView.test_basics_view_creates_vtmhuman
```
Expected: `FAILED (failures=3)`, each `AssertionError: 200 != 302`.

- [ ] **Step 2: Update `test_vampire_chargen.py`**

Add the import after `from characters.models.core.archetype import Archetype`:

```python
from characters.models.core.human import Human
```

Replace the start of `test_basics_view_creates_vampire`:

```python
    def test_basics_view_creates_vampire(self):
        """Test that submitting form creates a vampire."""
        self.client.login(username="testuser", password="testpassword")
```
with:
```python
    def test_basics_view_creates_vampire(self):
        """Test that submitting form creates a vampire."""
        # A player may only pick a chronicle they already take part in.
        Human.objects.create(name="Existing PC", owner=self.user, chronicle=self.chronicle)
        self.client.login(username="testuser", password="testpassword")
```

Replace the end of the same test:
```python
        # Vampire should be created
        vampire = Vampire.objects.get(name="Test Vampire")
        self.assertEqual(vampire.owner, self.user)
        self.assertEqual(vampire.clan, self.brujah)
```
with:
```python
        # Vampire should be created
        vampire = Vampire.objects.get(name="Test Vampire")
        self.assertEqual(vampire.owner, self.user)
        self.assertEqual(vampire.clan, self.brujah)
        self.assertEqual(vampire.chronicle, self.chronicle)

    def test_basics_view_rejects_chronicle_user_is_not_in(self):
        """A chronicle the user neither plays in nor runs is not a valid choice."""
        self.client.login(username="testuser", password="testpassword")
        url = reverse("characters:vampire:create:vampire")
        data = {
            "name": "Gatecrasher",
            "chronicle": self.chronicle.pk,
            "nature": self.nature.pk,
            "demeanor": self.demeanor.pk,
            "clan": self.brujah.pk,
            "concept": "Warrior",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("chronicle", response.context["form"].errors)
        self.assertFalse(Vampire.objects.filter(name="Gatecrasher").exists())
```

- [ ] **Step 3: Update `test_ghoul_chargen.py`**

Add after `from characters.models.core.archetype import Archetype`:
```python
from characters.models.core.human import Human
```
In `test_basics_view_creates_ghoul`, insert before `self.client.login(username="testuser", password="testpassword")`:
```python
        # A player may only pick a chronicle they already take part in.
        Human.objects.create(name="Existing PC", owner=self.user, chronicle=self.chronicle)
```
and after `self.assertEqual(ghoul.owner, self.user)` (end of that test) add:
```python
        self.assertEqual(ghoul.chronicle, self.chronicle)
```

- [ ] **Step 4: Update `test_vtmhuman.py`**

Add after `from characters.models.core.archetype import Archetype`:
```python
from characters.models.core.human import Human
```
In `test_basics_view_creates_vtmhuman`, insert before `self.client.login(username="testuser", password="testpassword")`:
```python
        # A player may only pick a chronicle they already take part in.
        Human.objects.create(name="Existing PC", owner=self.user, chronicle=self.chronicle)
```
and after `self.assertEqual(vtmhuman.owner, self.user)` (end of that test) add:
```python
        self.assertEqual(vtmhuman.chronicle, self.chronicle)
```

- [ ] **Step 5: Run the three files**

```bash
python manage.py test characters.tests.views.vampire.test_vampire_chargen characters.tests.views.vampire.test_ghoul_chargen characters.tests.views.vampire.test_vtmhuman
```
Expected: `OK` (some `skipped` are pre-existing), no failures. `test_basics_view_rejects_chronicle_user_is_not_in` passes immediately: it pins existing Step 0 behaviour (it would fail if `ScopedCreationFormMixin` were removed from `VampireBasicsView`).

- [ ] **Step 6: Lint and commit**

```bash
ruff check characters/tests/views/vampire/test_vampire_chargen.py characters/tests/views/vampire/test_ghoul_chargen.py characters/tests/views/vampire/test_vtmhuman.py
ruff format --check characters/tests/views/vampire/test_vampire_chargen.py characters/tests/views/vampire/test_ghoul_chargen.py characters/tests/views/vampire/test_vtmhuman.py
git add characters/tests/views/vampire/test_vampire_chargen.py characters/tests/views/vampire/test_ghoul_chargen.py characters/tests/views/vampire/test_vtmhuman.py
git commit -m "test(vampire): Basics tests pick a chronicle the player is in" -m "Step 0 scopes the create-form chronicle field to readable_chronicles(); the tests posted a chronicle the user had no part in and got a form error (200). Give the user a character in the chronicle, and pin the refusal of an unrelated chronicle." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```
Expected: ruff reports no errors and "3 files already formatted".

### Task 2: [B0.2] Circle create test joins the chronicle; pin the 403 for an unrelated chronicle

**Files:**
- Modify (test): `characters/tests/views/wraith/test_circle.py` (`TestCircleCreateView.test_create_circle_successfully`, lines 43-56). `Human` is already imported (line 7).

**Interfaces:**
- Consumes: URL `characters:wraith:create:circle`; `core.mixins.prepare_created_object` (sets `owner=request.user`, `status="Un"` for non-staff; raises `PermissionDenied` for an unreadable chronicle).
- Produces: new test `TestCircleCreateView.test_create_circle_in_chronicle_user_is_not_in_is_refused`.

- [ ] **Step 1: Confirm the failure**

```bash
python manage.py test characters.tests.views.wraith.test_circle.TestCircleCreateView.test_create_circle_successfully
```
Expected: `AssertionError: 403 != 302`.

- [ ] **Step 2: Update the test**

Replace:
```python
    def test_create_circle_successfully(self):
        """Test creating a circle successfully."""
        self.client.login(username="testuser", password="password")
```
with:
```python
    def test_create_circle_successfully(self):
        """Test creating a circle successfully."""
        # A player may only create in a chronicle they already take part in.
        Human.objects.create(name="Existing PC", owner=self.user, chronicle=self.chronicle)
        self.client.login(username="testuser", password="password")
```
and replace the end of that test:
```python
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Circle.objects.filter(name="Test Circle").exists())
```
with:
```python
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        circle = Circle.objects.get(name="Test Circle")
        self.assertEqual(circle.owner, self.user)
        self.assertEqual(circle.status, "Un")

    def test_create_circle_in_chronicle_user_is_not_in_is_refused(self):
        """Creating in a chronicle the user neither plays in nor runs is refused."""
        self.client.login(username="testuser", password="password")
        url = reverse("characters:wraith:create:circle")
        data = {
            "name": "Gatecrasher Circle",
            "description": "A test circle",
            "chronicle": self.chronicle.pk,
            "public_info": "",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Circle.objects.filter(name="Gatecrasher Circle").exists())
```

- [ ] **Step 3: Run**

```bash
python manage.py test characters.tests.views.wraith.test_circle
```
Expected: `OK`.

- [ ] **Step 4: Lint and commit**

```bash
ruff check characters/tests/views/wraith/test_circle.py
ruff format --check characters/tests/views/wraith/test_circle.py
git add characters/tests/views/wraith/test_circle.py
git commit -m "test(wraith): Circle create test uses a chronicle the player is in" -m "prepare_created_object() refuses a chronicle outside readable_chronicles() with 403; the test posted an unrelated chronicle. Give the user a character there, assert owner/status are set server-side, and pin the 403." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 3: [B0.3] The forged-companion test reaches the `companion_of` check

**Files:**
- Modify (test): `characters/tests/views/mage/test_companion_comprehensive.py` (imports lines 9-15; `test_other_player_cannot_attach_companion_to_mage` lines 83-99)

**Interfaces:**
- Consumes: URL `characters:mage:create:companion`; `CompanionBasicsView.form_valid` (`characters/views/mage/companion.py:251-265`) raising `PermissionDenied("Cannot attach a companion to this character")`.
- Produces: nothing new.

- [ ] **Step 1: Confirm the failure**

```bash
python manage.py test characters.tests.views.mage.test_companion_comprehensive.TestCompanionCreationWorkflow.test_other_player_cannot_attach_companion_to_mage
```
Expected: `AssertionError: 200 != 403`.

- [ ] **Step 2: Update the test**

Add after `from characters.models.core.background_block import Background, BackgroundRating`:
```python
from characters.models.core.human import Human
```
Replace:
```python
    def test_other_player_cannot_attach_companion_to_mage(self):
        other = User.objects.create_user("other_companion_creator")
        self.client.force_login(other)
```
with:
```python
    def test_other_player_cannot_attach_companion_to_mage(self):
        other = User.objects.create_user("other_companion_creator")
        # Another player in the same chronicle, so the chronicle choice is valid and
        # the companion_of ownership check is what refuses the request.
        Human.objects.create(name="Other PC", owner=other, chronicle=self.chronicle)
        self.client.force_login(other)
```
The assertions (403, and no "Forged Companion") stay as they are.

- [ ] **Step 3: Run**

```bash
python manage.py test characters.tests.views.mage.test_companion_comprehensive
```
Expected: `OK (skipped=…)` — the skipped classes are pre-existing and D4 deletes them.

- [ ] **Step 4: Lint and commit**

```bash
ruff check characters/tests/views/mage/test_companion_comprehensive.py
ruff format --check characters/tests/views/mage/test_companion_comprehensive.py
git add characters/tests/views/mage/test_companion_comprehensive.py
git commit -m "test(mage): forged companion test reaches the companion_of check" -m "The other player had no part in the chronicle, so Step 0's chronicle scoping rejected the form (200) before the companion_of ownership check ran. Put the player in the chronicle so the test proves the 403 it was written for." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```
Expected ruff output: exactly one **pre-existing** error, `characters/tests/views/mage/test_companion_comprehensive.py:281:9: F841 Local variable 'advantage' is assigned to but never used` (line 277 before this task). It sits in a skipped AJAX test class that D4 deletes; do not fix it here.

- [ ] **Unit gate:**

```bash
python manage.py test            # serial, ≈40 min
python manage.py check
python manage.py test core.tests.security.test_route_policies
ruff check characters/tests/views/vampire/test_vampire_chargen.py characters/tests/views/vampire/test_ghoul_chargen.py characters/tests/views/vampire/test_vtmhuman.py characters/tests/views/wraith/test_circle.py characters/tests/views/mage/test_companion_comprehensive.py
ruff format --check characters/tests/views/vampire/test_vampire_chargen.py characters/tests/views/vampire/test_ghoul_chargen.py characters/tests/views/vampire/test_vtmhuman.py characters/tests/views/wraith/test_circle.py characters/tests/views/mage/test_companion_comprehensive.py
```
Required: the full suite reports **0 failures and 0 errors** (this is the new baseline for every later unit; previously 5 failing). `check` reports no issues; the route-policy test passes; ruff reports only the pre-existing F841 noted in B0.3; all files already formatted.

## Unit D1: Safety net and live 500s

Order matters: the routed-template test (D1.5) asserts that no routed template fails to compile, so it lands after the Demesne fix (D1.4).

### Task 4: [D1.1] Move the dead-code heuristics into a side-effect-free module, with unit tests

`scripts/find_dead_code.py` re-points `DATABASES["default"]` and calls `django.setup()` at import, so its helpers cannot be imported by tests. Every moved helper depends only on `ast`, `re`, `inspect` and Django's generic view classes (importable without settings, verified). The two project-dependent inputs of `classify_dead_route` — `absolute_url_name` (needs the URLconf) and `DictView` (project code) — become keyword arguments, so the module imports no project code.

**Files:**
- Create: `scripts/dead_code_heuristics.py`
- Modify: `scripts/find_dead_code.py` (docstring line 9; imports lines 53-61 and 67; constants lines 83-90, 98, 100, 110-112; `call_name` lines 132-136; `object_type_seed`…`pattern_regex` lines 196-295; `classify_dead_route` lines 462-482; call site line 518)
- Test: `core/tests/test_dead_code_heuristics.py` (create)

**Interfaces:**
- Produces (module `scripts.dead_code_heuristics`): constants `URL_FUNCS`, `TEMPLATE_FUNCS`, `CALL_CTX`, `SEED_METHODS`, `PAGE_KINDS`; functions `call_name(node) -> str | None`, `object_type_seed(call) -> tuple[str, str, str] | None`, `str_parts(node) -> list[str | None] | None`, `find_computed(node, out: list, ctx: str | None) -> None` (appends `(kind, lineno, parts, expr)`), `pattern_regex(parts, wildcard) -> re.Pattern`, `classify_dead_route(view, name, route, *, alias_target=lambda model: None, router_bases=()) -> str`.
- Consumes (in `find_dead_code.py`): the above; `classify_dead_route(view, name, route, alias_target=absolute_url_name, router_bases=(DictView,))`.

- [ ] **Step 1: Snapshot the script's current output**

```bash
mkdir -p /tmp/d1 && python scripts/find_dead_code.py --format tsv > /tmp/d1/before.tsv
```
Expected: exit 0, ≈570 lines (the first begins `# urls\t747 project URL names`).

- [ ] **Step 2: Write the failing unit tests** — create `core/tests/test_dead_code_heuristics.py`:

```python
"""Unit tests for the pure heuristics in scripts/dead_code_heuristics.py.

Only the heuristics module is imported: find_dead_code.py re-points the default
database when imported, so it is exercised in a subprocess instead
(core/tests/test_find_dead_code_script.py).
"""

import ast
import os
import subprocess
import sys
from pathlib import Path

from django.http import JsonResponse
from django.test import SimpleTestCase
from django.views import View
from django.views.generic import CreateView, DetailView

from scripts.dead_code_heuristics import (
    classify_dead_route,
    find_computed,
    object_type_seed,
    pattern_regex,
    str_parts,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
URL_WILDCARD = r"[\w:-]*"


def expr(source):
    return ast.parse(source, mode="eval").body


def computed(source):
    out = []
    find_computed(ast.parse(source), out, None)
    return out


class StrPartsTest(SimpleTestCase):
    def test_plain_string_is_one_literal_part(self):
        self.assertEqual(str_parts(expr('"shop:item_list"')), ["shop:item_list"])

    def test_f_string_placeholders_become_none(self):
        self.assertEqual(str_parts(expr('f"shop:{kind}_detail"')), ["shop:", None, "_detail"])

    def test_percent_formatting(self):
        self.assertEqual(str_parts(expr('"shop/%s.html" % kind')), ["shop/", None, ".html"])
        self.assertEqual(
            str_parts(expr('"shop/%(kind)s/%d.html" % values')),
            ["shop/", None, "/", None, ".html"],
        )

    def test_str_format(self):
        self.assertEqual(str_parts(expr('"shop:{}_list".format(kind)')), ["shop:", None, "_list"])
        self.assertEqual(
            str_parts(expr('"shop/{kind}.html".format(kind=k)')), ["shop/", None, ".html"]
        )

    def test_concatenation(self):
        self.assertEqual(str_parts(expr('"shop:" + kind')), ["shop:", None])
        self.assertEqual(str_parts(expr('kind + "_detail"')), [None, "_detail"])
        self.assertEqual(str_parts(expr('"shop/" + kind + ".html"')), ["shop/", None, ".html"])

    def test_expressions_without_literals_are_not_strings(self):
        self.assertIsNone(str_parts(expr("first + second")))
        self.assertIsNone(str_parts(expr("kind")))
        self.assertIsNone(str_parts(expr("build_name(kind)")))
        self.assertIsNone(str_parts(expr("fmt % kind")))


class FindComputedTest(SimpleTestCase):
    def test_literal_reverse_is_ignored(self):
        self.assertEqual(computed('reverse("shop:item_list")'), [])

    def test_reverse_of_a_variable_is_recorded(self):
        self.assertEqual(computed("reverse(target)"), [("url", 1, [None], "target")])
        self.assertEqual(
            computed("reverse_lazy(self.success_name)"),
            [("url", 1, [None], "self.success_name")],
        )

    def test_redirect_to_an_object_is_ignored(self):
        self.assertEqual(computed("redirect(item)"), [])
        self.assertEqual(computed("redirect(item.get_absolute_url())"), [])

    def test_redirect_to_a_built_name_is_recorded(self):
        self.assertEqual(
            computed('redirect(f"shop:{kind}_detail", pk=1)'),
            [("url", 1, ["shop:", None, "_detail"], "f'shop:{kind}_detail'")],
        )

    def test_template_name_keyword_is_a_template(self):
        self.assertEqual(
            computed('show(template_name="shop/" + kind + ".html")'),
            [("template", 1, ["shop/", None, ".html"], "'shop/' + kind + '.html'")],
        )

    def test_template_name_assignment_is_a_template(self):
        source = 'class ItemView:\n    template_name = "shop/%s/detail.txt" % kind\n'
        self.assertEqual(
            computed(source),
            [("template", 2, ["shop/", None, "/detail.txt"], "'shop/%s/detail.txt' % kind")],
        )

    def test_render_takes_its_template_from_the_second_argument(self):
        self.assertEqual(
            computed('render(request, f"shop/{kind}.html")'),
            [("template", 1, ["shop/", None, ".html"], "f'shop/{kind}.html'")],
        )

    def test_viewname_keyword_counts_only_for_url_functions(self):
        self.assertEqual(computed("reverse(viewname=target)"), [("url", 1, [None], "target")])
        self.assertEqual(computed("audit(viewname=target)"), [])

    def test_unanchored_builds_are_classified_by_their_literal(self):
        self.assertEqual(
            computed('name = f"shop:{kind}_list"'),
            [("url", 1, ["shop:", None, "_list"], "f'shop:{kind}_list'")],
        )
        self.assertEqual(computed('label = f"{first}:{second}"'), [])


class ObjectTypeSeedTest(SimpleTestCase):
    def test_keyword_fields(self):
        call = expr('ObjectType.objects.get_or_create(name="vampire", type="char", gameline="vtm")')
        self.assertEqual(object_type_seed(call), ("vampire", "char", "vtm"))

    def test_defaults_dict_fields(self):
        call = expr(
            'ObjectType.objects.update_or_create(name="node", '
            'defaults={"type": "loc", "gameline": "mta"})'
        )
        self.assertEqual(object_type_seed(call), ("node", "loc", "mta"))

    def test_non_literal_or_incomplete_calls_are_skipped(self):
        for source in (
            'ObjectType.objects.get_or_create(name=kind, type="char", gameline="vtm")',
            'ObjectType.objects.get_or_create(name="vampire", type="char")',
            'ObjectType.objects.filter(name="vampire", type="char", gameline="vtm")',
            'Clan.objects.create(name="vampire", type="char", gameline="vtm")',
        ):
            with self.subTest(source=source):
                self.assertIsNone(object_type_seed(expr(source)))


class PatternRegexTest(SimpleTestCase):
    def test_placeholders_match_the_wildcard_and_literals_are_escaped(self):
        regex = pattern_regex(["shop:", None, "_detail"], URL_WILDCARD)
        self.assertTrue(regex.match("shop:item_detail"))
        self.assertIsNone(regex.match("shop:item_detail_extra"))
        self.assertIsNone(regex.match("other:item_detail"))

        template = pattern_regex(["shop/", None, ".html"], r".*")
        self.assertTrue(template.match("shop/items/list.html"))
        self.assertIsNone(template.match("shop/items/listXhtml"))


class Item:
    """Stands in for a model: classify_dead_route only needs a class."""


class ItemDetail(DetailView):
    model = Item


class ItemCreate(CreateView):
    model = Item


class ItemData(View):
    def get(self, request):
        return JsonResponse({})


class Router(View):
    pass


class RoutedChild(Router):
    pass


def plain_view(request):
    return None


class ClassifyDeadRouteTest(SimpleTestCase):
    def test_json_and_ajax_endpoints(self):
        self.assertEqual(
            classify_dead_route(Router, "shop:ajax:load_items", "shop/ajax/"),
            "(b) JSON/AJAX endpoint",
        )
        self.assertEqual(
            classify_dead_route(ItemData, "shop:item_data", "shop/data/"),
            "(b) JSON/AJAX endpoint",
        )

    def test_function_view(self):
        self.assertEqual(
            classify_dead_route(plain_view, "shop:plain", "shop/plain/"),
            "(d) other (function view)",
        )

    def test_alias_detail_route(self):
        self.assertEqual(
            classify_dead_route(
                ItemDetail,
                "shop:item_alias",
                "shop/alias/<pk>/",
                alias_target=lambda m: "shop:item",
            ),
            "(a) alias: Item.get_absolute_url() -> shop:item",
        )

    def test_canonical_detail_route_is_an_unlinked_page(self):
        self.assertEqual(
            classify_dead_route(
                ItemDetail, "shop:item", "shop/<pk>/", alias_target=lambda m: "shop:item"
            ),
            "(c) detail page with no link",
        )
        self.assertEqual(
            classify_dead_route(ItemDetail, "shop:item", "shop/<pk>/"),
            "(c) detail page with no link",
        )

    def test_page_kinds(self):
        self.assertEqual(
            classify_dead_route(ItemCreate, "shop:create", "shop/create/"),
            "(c) create page with no link",
        )

    def test_routers_are_named_only_when_their_base_is_given(self):
        self.assertEqual(
            classify_dead_route(RoutedChild, "shop:router", "shop/r/", router_bases=(Router,)),
            "(d) other (DictView router)",
        )
        self.assertEqual(classify_dead_route(RoutedChild, "shop:router", "shop/r/"), "(d) other")


class HeuristicsImportTest(SimpleTestCase):
    def test_import_does_not_configure_django(self):
        env = {k: v for k, v in os.environ.items() if k != "DJANGO_SETTINGS_MODULE"}
        code = (
            "import django.apps, django.conf, scripts.dead_code_heuristics; "
            "print(django.apps.apps.ready, django.conf.settings.configured)"
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            cwd=REPO_ROOT,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "False False")
```

- [ ] **Step 3: Run them to see them fail**

```bash
python manage.py test core.tests.test_dead_code_heuristics
```
Expected: `ImportError: Failed to import test module: test_dead_code_heuristics` … `ModuleNotFoundError: No module named 'scripts.dead_code_heuristics'`.

- [ ] **Step 4: Create `scripts/dead_code_heuristics.py`**

The function bodies are moved verbatim from `find_dead_code.py`; only `classify_dead_route` gains the two keyword arguments.

```python
"""Pure heuristics behind scripts/find_dead_code.py.

Importing this module has no side effects: it does not configure Django, open a
database or import project code. Everything here works on AST nodes, strings and
classes passed in, so the tests can import it directly.
"""

import ast
import inspect
import re

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

URL_FUNCS = {"reverse", "reverse_lazy", "redirect", "resolve_url"}
TEMPLATE_FUNCS = {
    "render",
    "render_to_string",
    "get_template",
    "select_template",
    "TemplateResponse",
}
CALL_CTX = {**dict.fromkeys(URL_FUNCS, "url"), **dict.fromkeys(TEMPLATE_FUNCS, "template")}
SEED_METHODS = {"create", "get_or_create", "update_or_create"}
PAGE_KINDS = [(CreateView, "create"), (UpdateView, "update"), (DeleteView, "delete")]
PAGE_KINDS += [(ListView, "list"), (DetailView, "detail"), (FormView, "form")]
PAGE_KINDS += [(TemplateView, "template")]


def call_name(node):
    func = node.func
    return func.id if isinstance(func, ast.Name) else getattr(func, "attr", None)


def object_type_seed(call):
    """(name, category, gameline) from a literal ObjectType.objects.get_or_create(...) call."""
    func = call.func
    if not (isinstance(func, ast.Attribute) and func.attr in SEED_METHODS):
        return None
    if ast.unparse(func.value) != "ObjectType.objects":
        return None
    fields = {k.arg: k.value for k in call.keywords if k.arg}
    defaults = fields.get("defaults")
    if isinstance(defaults, ast.Dict):
        fields.update(
            {
                getattr(k, "value", None): v
                for k, v in zip(defaults.keys, defaults.values, strict=True)
            }
        )
    try:
        return tuple(ast.literal_eval(fields[f]) for f in ("name", "type", "gameline"))
    except (KeyError, ValueError):
        return None


def str_parts(node):
    """Flatten a string-building expression into literal parts; None marks a placeholder."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, ast.JoinedStr):
        return [v.value if isinstance(v, ast.Constant) else None for v in node.values]
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = str_parts(node.left), str_parts(node.right)
        if left is None and right is None:
            return None
        return (left or [None]) + (right or [None])
    fmt, pattern = None, None
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        fmt, pattern = node.left, r"%(?:\(\w+\))?[sdrf]"
    elif isinstance(node, ast.Call) and getattr(node.func, "attr", None) == "format":
        fmt, pattern = node.func.value, r"\{[^{}]*\}"
    if isinstance(fmt, ast.Constant) and isinstance(fmt.value, str):
        pieces = re.split(pattern, fmt.value)
        return [x for piece in pieces for x in (piece, None)][:-1]
    return None


def find_computed(node, out, ctx):
    """Record string-building expressions (and variable reverse() args) for manual review."""
    parts = str_parts(node) if isinstance(node, ast.JoinedStr | ast.BinOp | ast.Call) else None
    if parts and None in parts and any(parts):
        literal = "".join(p for p in parts if p)
        kind = ctx
        if kind is None and re.search(r"\.(html|txt)\b", literal):
            kind = "template"
        elif kind is None and re.fullmatch(r"[a-z_]+:[\w:-]*", parts[0] or ""):
            kind = "url"
        if kind:
            out.append((kind, node.lineno, parts, ast.unparse(node)))
        return
    if ctx == "url" and (
        isinstance(node, ast.Name | ast.Attribute | ast.Subscript)
        # A nested reverse() or a model get_*url() is resolved elsewhere.
        or (
            isinstance(node, ast.Call)
            and call_name(node) not in CALL_CTX
            and not re.fullmatch(r"get_\w*url", call_name(node) or "")
        )
    ):
        out.append(("url", node.lineno, [None], ast.unparse(node)))
    if isinstance(node, ast.Call):
        name = call_name(node)
        arg_ctx = CALL_CTX.get(name)
        for index, child in enumerate(node.args):
            # redirect() often takes a model object first, so only a string-building
            # first arg counts there; render()'s name is its second arg.
            builds_string = isinstance(child, ast.JoinedStr | ast.BinOp | ast.Call)
            wanted = (
                index == 0 and arg_ctx == "url" and (name != "redirect" or builds_string)
            ) or (arg_ctx == "template" and index == (1 if name == "render" else 0))
            find_computed(child, out, arg_ctx if wanted else None)
        find_computed(node.func, out, None)
        for keyword in node.keywords:
            if keyword.arg == "template_name":
                kw_ctx = "template"
            elif keyword.arg == "viewname" and arg_ctx == "url":
                kw_ctx = "url"
            else:
                kw_ctx = None
            find_computed(keyword.value, out, kw_ctx)
        return
    if isinstance(node, ast.Assign) and any(
        getattr(t, "id", "") == "template_name" for t in node.targets
    ):
        return find_computed(node.value, out, "template")
    for child in ast.iter_child_nodes(node):
        find_computed(child, out, None)


def pattern_regex(parts, wildcard):
    return re.compile("".join(re.escape(p) if p is not None else wildcard for p in parts) + r"\Z")


def classify_dead_route(view, name, route, *, alias_target=lambda model: None, router_bases=()):
    """(a) alias detail, (b) JSON/AJAX, (c) unlinked page view, (d) other.

    alias_target(model) returns the URL name that model's get_absolute_url() resolves
    to, or None. router_bases are the classes whose subclasses count as routers
    (find_dead_code.py passes DictView).
    """
    try:
        source = inspect.getsource(view)
    except (OSError, TypeError):
        source = ""
    if re.search(r"ajax|json|load_", f"{name} {route}", re.I) or "JsonResponse" in source:
        return "(b) JSON/AJAX endpoint"
    if not isinstance(view, type):
        return "(d) other (function view)"
    model = getattr(view, "model", None)
    if issubclass(view, DetailView) and isinstance(model, type):
        target = alias_target(model)
        if target and target != name:
            return f"(a) alias: {model.__name__}.get_absolute_url() -> {target}"
    for base, kind in PAGE_KINDS:
        if issubclass(view, base):
            return f"(c) {kind} page with no link"
    if router_bases and issubclass(view, tuple(router_bases)):
        return "(d) other (DictView router)"
    return "(d) other"
```

- [ ] **Step 5: Make `find_dead_code.py` import them**

1. Docstring: after the line `Importing this module has the same database side effect; run it as a script.` insert:
   ```
   The pure AST/string heuristics live in scripts/dead_code_heuristics.py, which
   has no import side effects and is unit-tested directly.
   ```
2. Delete the import block at lines 53-61 (`from django.views.generic import (` … `CreateView, DeleteView, DetailView, FormView, ListView, TemplateView, UpdateView,` … `)`); they were used only by `PAGE_KINDS` and `classify_dead_route`. Keep `from django.views.generic.base import TemplateResponseMixin`.
3. Replace line 67:
   ```python
   from scripts.inventory_authorization_routes import descendants
   ```
   with:
   ```python
   from scripts.dead_code_heuristics import (
       call_name,
       classify_dead_route,
       find_computed,
       object_type_seed,
       pattern_regex,
   )
   from scripts.inventory_authorization_routes import descendants
   ```
4. Delete these module constants: `URL_FUNCS = {…}` and the whole `TEMPLATE_FUNCS = {…}` literal (lines 83-90), `CALL_CTX = …` (line 98), `SEED_METHODS = …` (line 100), and the three `PAGE_KINDS` lines (110-112).
5. Delete `def call_name(node):` and its 2-line body (lines 132-134, plus the two blank lines after).
6. Delete everything from `def object_type_seed(call):` (line 196) up to, but not including, `def load_sources():` (line 296) — that is `object_type_seed`, `str_parts`, `find_computed` and `pattern_regex`.
7. Delete everything from `def classify_dead_route(view, name, route):` (line 462) up to, but not including, `def section_urls():` (line 483).
8. In `section_urls()`, replace
   ```python
               kind = classify_dead_route(view, name, route)
   ```
   with
   ```python
               kind = classify_dead_route(
                   view, name, route, alias_target=absolute_url_name, router_bases=(DictView,)
               )
   ```

`ast`, `inspect`, `re`, `models`, `DictView` and `TemplateResponseMixin` are still used by the script (`ruff check` confirms no unused import).

- [ ] **Step 6: Run the tests and prove the script output is unchanged**

```bash
python manage.py test core.tests.test_dead_code_heuristics core.tests.test_find_dead_code_script
python scripts/find_dead_code.py --format tsv > /tmp/d1/after.tsv && diff /tmp/d1/before.tsv /tmp/d1/after.tsv && echo IDENTICAL
```
Expected: `Ran 27 tests … OK` (26 heuristics tests + the existing smoke test, ≈40 s for the subprocess); `IDENTICAL` (verified: the refactor changes no row).

- [ ] **Step 7: Lint and commit**

```bash
ruff check scripts/dead_code_heuristics.py scripts/find_dead_code.py core/tests/test_dead_code_heuristics.py
ruff format --check scripts/dead_code_heuristics.py scripts/find_dead_code.py core/tests/test_dead_code_heuristics.py
git add scripts/dead_code_heuristics.py scripts/find_dead_code.py core/tests/test_dead_code_heuristics.py
git commit -m "refactor(scripts): move dead-code heuristics into an importable module" -m "find_dead_code.py re-points the database and runs django.setup() at import. Its pure helpers (str_parts, find_computed, object_type_seed, pattern_regex, classify_dead_route, call_name) now live in scripts/dead_code_heuristics.py, which imports no project code, and are unit-tested. classify_dead_route takes alias_target/router_bases instead of reaching for the URLconf and DictView. Script output is byte-identical." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 5: [D1.2] Subprocess test for `--format tsv`

**Files:**
- Modify (test): `core/tests/test_find_dead_code_script.py` (append a method to `FindDeadCodeScriptTest`, after line 37)

**Interfaces:**
- Consumes: `SCRIPT`, `REPO_ROOT` module constants already in that file; the `emit()` TSV contract (`# <section>\t<summary>`, then per table a `section\ttable\t<headers…>` row followed by rows with the same field count).
- Produces: `FindDeadCodeScriptTest.test_tsv_format_is_one_tab_separated_row_per_line`.

- [ ] **Step 1: Write the test** — append to class `FindDeadCodeScriptTest`:

```python
    def test_tsv_format_is_one_tab_separated_row_per_line(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--section=urls", "--format=tsv"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        lines = result.stdout.splitlines()
        self.assertTrue(lines[0].startswith("# urls\t"), lines[0])
        self.assertNotIn("**Summary:**", result.stdout)
        headers, rows = None, 0
        for line in lines[1:]:
            fields = line.split("\t")
            if fields[:2] == ["section", "table"]:
                headers = fields
                continue
            self.assertIsNotNone(headers, f"row before any header: {line!r}")
            self.assertEqual(fields[0], "urls", line)
            self.assertEqual(len(fields), len(headers), line)
            rows += 1
        self.assertGreater(rows, 0)
        self.assertIn(
            "\t".join(
                ("section", "table", "URL name", "Route", "View", "Status", "Dead-route kind")
            ),
            lines,
        )
```

- [ ] **Step 2: Run it**

```bash
python manage.py test core.tests.test_find_dead_code_script
```
Expected: `Ran 2 tests … OK`. This is a characterization test of existing behaviour, so it passes at once. Check it bites by temporarily changing `print("\t".join((section, title, *(…))))` in `emit()` to join with `" "`; the test must fail with `AssertionError: 'urls' != …`. Revert that change before committing.

- [ ] **Step 3: Lint and commit**

```bash
ruff check core/tests/test_find_dead_code_script.py
ruff format --check core/tests/test_find_dead_code_script.py
git add core/tests/test_find_dead_code_script.py
git commit -m "test(scripts): cover find_dead_code --format tsv" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 6: [D1.3] Fix the login/logout redirect settings (logout is a 500)

**Semantics checked.** `/accounts/login/` resolves to `accounts.views.CustomLoginView` (the `accounts` URLconf is included before `django.contrib.auth.urls`, so Django's own `LoginView` at the same path is shadowed). `CustomLoginView.get_success_url()` always returns `request.user.profile.get_absolute_url()`, so `LOGIN_REDIRECT_URL` is only a fallback that no routed view reads today; it must still resolve. The old value `"user"` meant `accounts:user` (`HomeListView`, a duplicate of `core:home`, which D8 turns into a redirect to `core:home`), so `"core:home"` is the correct value. `/accounts/logout/` is Django's `LogoutView` (the base template POSTs to `{% url 'logout' %}`); with no `next`, it calls `resolve_url(settings.LOGOUT_REDIRECT_URL)`, and `"home"` raises `NoReverseMatch` (verified: 500). `LOGIN_URL = "login"` resolves and stays.

**Files:**
- Modify: `tg/settings/base.py` lines 142-143
- Test: `accounts/tests/views/test_auth_redirects.py` (create)

**Interfaces:**
- Consumes: URL names `login`, `logout` (django.contrib.auth), `core:home`; `Profile.get_absolute_url()`.
- Produces: `settings.LOGIN_REDIRECT_URL == settings.LOGOUT_REDIRECT_URL == "core:home"`.

- [ ] **Step 1: Write the failing test** — create `accounts/tests/views/test_auth_redirects.py`:

```python
"""Login and logout redirect settings resolve; logout used to return a 500."""

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from django.urls import reverse


class AuthRedirectSettingsTest(TestCase):
    def test_redirect_settings_resolve_to_home(self):
        home = reverse("core:home")
        self.assertEqual(resolve_url(settings.LOGIN_REDIRECT_URL), home)
        self.assertEqual(resolve_url(settings.LOGOUT_REDIRECT_URL), home)

    def test_logout_redirects_home_and_ends_the_session(self):
        user = User.objects.create_user("logout_user", password="pw-12345")
        self.client.force_login(user)

        response = self.client.post(reverse("logout"))

        self.assertRedirects(response, reverse("core:home"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_still_lands_on_the_profile(self):
        # CustomLoginView overrides get_success_url; LOGIN_REDIRECT_URL is only its fallback.
        user = User.objects.create_user("login_user", password="pw-12345")

        response = self.client.post(
            reverse("login"), {"username": "login_user", "password": "pw-12345"}
        )

        self.assertRedirects(
            response, user.profile.get_absolute_url(), fetch_redirect_response=False
        )
```

- [ ] **Step 2: Run it to see it fail**

```bash
python manage.py test accounts.tests.views.test_auth_redirects
```
Expected: `FAILED (errors=2)`: `test_redirect_settings_resolve_to_home` → `NoReverseMatch: Reverse for 'user' not found`; `test_logout_redirects_home_and_ends_the_session` → `NoReverseMatch: Reverse for 'home' not found`. `test_login_still_lands_on_the_profile` passes (it guards the `CustomLoginView` override).

- [ ] **Step 3: Fix the settings** — in `tg/settings/base.py` replace:

```python
LOGIN_REDIRECT_URL = "user"
LOGOUT_REDIRECT_URL = "home"
```
with:
```python
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
```
(`development.py`/`production.py` do not override either setting.)

- [ ] **Step 4: Run it**

```bash
python manage.py test accounts.tests.views
```
Expected: `OK`.

- [ ] **Step 5: Lint and commit**

```bash
ruff check tg/settings/base.py accounts/tests/views/test_auth_redirects.py
ruff format --check tg/settings/base.py accounts/tests/views/test_auth_redirects.py
git add tg/settings/base.py accounts/tests/views/test_auth_redirects.py
git commit -m "fix(settings): login/logout redirects resolve to core:home" -m "LOGOUT_REDIRECT_URL = 'home' and LOGIN_REDIRECT_URL = 'user' name no URL (both live under namespaces), so POST /accounts/logout/ raised NoReverseMatch (500). CustomLoginView still sends users to their profile." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 7: [D1.4] Demesne form pages stop loading `widget_tweaks` (500)

`locations/templates/locations/mage/demesne/form_include.html` line 1 is `{% load widget_tweaks %}`; `widget_tweaks` is not installed, so both `DemesneCreateView` (`locations:mage:create:demesne`, policy `LOGIN`) and `DemesneUpdateView` (`locations:mage:update:demesne`, `OBJECT_WRITE`) raise `TemplateSyntaxError`. The file uses no `widget_tweaks` tag or filter (it only renders `{{ form.<field> }}`; `grep -n "render_field\|add_class\|attr:" …` finds nothing), and it is the only `widget_tweaks` reference in the repo.

**Files:**
- Modify: `locations/templates/locations/mage/demesne/form_include.html` (delete line 1)
- Test: `locations/tests/views/mage/test_demesne.py` (replace the 4-line TODO placeholder)

**Interfaces:**
- Consumes: URL names `locations:mage:create:demesne`, `locations:mage:update:demesne` (kwarg `pk`); `locations.models.mage.demesne.Demesne`.
- Produces: `DemesneFormPagesTest`.

- [ ] **Step 1: Write the failing test** — replace the whole content of `locations/tests/views/mage/test_demesne.py` with:

```python
"""Tests for the Demesne create and update pages."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from locations.models.mage.demesne import Demesne


class DemesneFormPagesTest(TestCase):
    """The shared form include used to load the uninstalled widget_tweaks library (500)."""

    def setUp(self):
        self.user = User.objects.create_user("demesne_owner", password="pw-12345")
        self.client.force_login(self.user)

    def test_create_page_renders(self):
        response = self.client.get(reverse("locations:mage:create:demesne"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/demesne/form_include.html")
        self.assertContains(response, 'name="rank"')

    def test_owner_update_page_renders_while_unfinished(self):
        demesne = Demesne.objects.create(name="Quiet Garden", owner=self.user, status="Un")

        response = self.client.get(
            reverse("locations:mage:update:demesne", kwargs={"pk": demesne.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/demesne/form_include.html")
        self.assertContains(response, "Quiet Garden")
```

- [ ] **Step 2: Run it to see it fail**

```bash
python manage.py test locations.tests.views.mage.test_demesne
```
Expected: `FAILED (errors=2)`, both `TemplateSyntaxError: 'widget_tweaks' is not a registered tag library.`

- [ ] **Step 3: Fix** — delete the first line of `locations/templates/locations/mage/demesne/form_include.html`:

```html
{% load widget_tweaks %}
```
The file then starts with `<div class="row">`.

- [ ] **Step 4: Run it**

```bash
python manage.py test locations.tests.views.mage.test_demesne
```
Expected: `Ran 2 tests … OK`.

- [ ] **Step 5: Lint and commit**

```bash
ruff check locations/tests/views/mage/test_demesne.py
ruff format --check locations/tests/views/mage/test_demesne.py
git add locations/templates/locations/mage/demesne/form_include.html locations/tests/views/mage/test_demesne.py
git commit -m "fix(locations): drop uninstalled widget_tweaks from the Demesne form" -m "The include used no widget_tweaks tag, but loading the unregistered library made the Demesne create and update pages return 500." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 8: [D1.5] Routed-template inventory test with a `KNOWN_MISSING` allowlist

**Approach (decided and verified).** Django loads a template's `{% extends %}` parent and `{% include %}` targets only at render time, so `get_template()` on a view's own template does not surface a missing parent (verified: `characters/werewolf/drone/basics.html` compiles although its parent `characters/core/character/chargen.html` does not exist). The test therefore:

1. collects every project view class reached by a URL pattern or by a `DictView` mapping/default/public target (the same traversal as `core/tests/security/test_route_policies.py`, reusing `scripts.inventory_authorization_routes.descendants` and `core.access_policy.PROJECT_PREFIXES`/`route_name`) — 974 view classes at `1e77e23`;
2. gets each `TemplateResponseMixin` view's names with `get_template_names()` on a bare instance (the approach `find_dead_code.view_template_names` uses; it raises for none of the 974 today), taking the first loadable name as `select_template()` does;
3. walks the closure of **constant** `{% extends %}`/`{% include %}` targets from the compiled nodelist (`nodelist.get_nodes_by_type(ExtendsNode | IncludeNode)`; this descends into `{% if %}`/`{% block %}` bodies), recording `TemplateDoesNotExist` as missing and `TemplateSyntaxError` as broken. Variable names cannot be followed and are skipped.

The one project function view (`widgets.views.auto_chained_ajax_view`) is JSON and has no template. One routed class view never renders its derived name: `CharacterTemplateExportView` (a `DetailView` whose `get()` returns a JSON download; its derived `core/charactertemplate_detail.html` does not exist) — it is listed in `NON_RENDERING_VIEWS`, and a test keeps that list honest.

**Exact current missing set** (from running the walker at `1e77e23`; demesne excluded because D1.4 fixed it; it was the only `TemplateSyntaxError`):

| Missing template | Reached by (all routed views) | Owner |
|---|---|---|
| `characters/core/character/chargen.html` (extended by `werewolf/drone/basics.html` and `drone/chargen.html`) | 8 Drone views (`DroneBasicsView` and the 7 `drone.Drone*View` steps) | Step 2 |
| `characters/core/human/allies_display.html`, `characters/core/human/allies_form.html` (included by `werewolf/fera/chargen.html`) | 11 `fera.Fera*View` steps | Step 2 |
| `characters/demon/demon/chargen.html` | 15 `demon_chargen.Demon*View` steps | Step 2 |
| `characters/demon/dtfhuman/chargen.html` | 8 `dtfhuman_chargen.DtFHuman*View` steps | Step 2 |
| `characters/demon/thrall/chargen.html` | 9 `thrall_chargen.Thrall*View` steps | Step 2 |
| `characters/mage/mage/mage_wonder_block_form.html` (included by `mage/companion/chargen.html`) | 14 `companion.Companion*View` steps (including `CompanionChantryView`, which C1 touches) | Step 2 |
| `characters/demon/ritual/form.html` | `RitualUpdateView` | Step 7 |
| `characters/demon/ritual/list.html` | `RitualListView` | Step 7 |
| `characters/wraith/wraith/form.html` | `WraithUpdateView` | Step 7 |

This matches spec section 7 exactly (10 templates).

**Files:**
- Test: `core/tests/test_routed_templates.py` (create)

**Interfaces:**
- Consumes: `scripts.inventory_authorization_routes.descendants`, `core.access_policy.PROJECT_PREFIXES`, `core.access_policy.route_name`.
- Produces: `core/tests/test_routed_templates.py` with module constants `KNOWN_MISSING: dict[str, tuple[str, str]]` (template → (view dotted path, owning step)) and `NON_RENDERING_VIEWS: dict[str, str]`, helper `missing_routed_templates() -> (dict[str, set[str]], dict[str, str])`, and class `RoutedTemplatesTest`.

- [ ] **Step 1: Write the test** — create `core/tests/test_routed_templates.py`:

```python
"""Every routed page's template, and each template it extends or includes, exists.

The scan starts from every project view class that a URL pattern or a DictView
mapping reaches, takes its template names the way Django does, and follows each
constant {% extends %} and {% include %} target. Templates only load their parent
and includes at render time, so compiling the view's own template is not enough.
Names built from variables cannot be followed and are not checked.

KNOWN_MISSING lists the routed pages that return a 500 today because a template was
never written (dead-code design, section 7). Each entry names the template, one
view that reaches it and the step that owns the fix. The test fails when another
template goes missing, and when an allowlisted template exists but its entry stays.
"""

from functools import cache

from django.db import models
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.loader import get_template
from django.template.loader_tags import ExtendsNode, IncludeNode
from django.test import SimpleTestCase
from django.urls import URLResolver, get_resolver
from django.views.generic.base import TemplateResponseMixin

from core.access_policy import PROJECT_PREFIXES, route_name
from scripts.inventory_authorization_routes import descendants

KNOWN_MISSING = {
    "characters/core/character/chargen.html": (
        "characters.views.werewolf.drone.DroneBasicsView",
        "Step 2",
    ),
    "characters/core/human/allies_display.html": (
        "characters.views.werewolf.fera.FeraAbilityView",
        "Step 2",
    ),
    "characters/core/human/allies_form.html": (
        "characters.views.werewolf.fera.FeraAbilityView",
        "Step 2",
    ),
    "characters/demon/demon/chargen.html": (
        "characters.views.demon.demon_chargen.DemonAttributeView",
        "Step 2",
    ),
    "characters/demon/dtfhuman/chargen.html": (
        "characters.views.demon.dtfhuman_chargen.DtFHumanAttributeView",
        "Step 2",
    ),
    "characters/demon/thrall/chargen.html": (
        "characters.views.demon.thrall_chargen.ThrallAttributeView",
        "Step 2",
    ),
    "characters/mage/mage/mage_wonder_block_form.html": (
        "characters.views.mage.companion.CompanionAbilityView",
        "Step 2",
    ),
    "characters/demon/ritual/form.html": (
        "characters.views.demon.ritual.RitualUpdateView",
        "Step 7",
    ),
    "characters/demon/ritual/list.html": (
        "characters.views.demon.ritual.RitualListView",
        "Step 7",
    ),
    "characters/wraith/wraith/form.html": (
        "characters.views.wraith.wraith.WraithUpdateView",
        "Step 7",
    ),
}

# Routed template views that return their own response and never render the
# template name Django would derive for them.
NON_RENDERING_VIEWS = {
    "core.views.character_template.CharacterTemplateExportView": "returns a JSON download",
}


def iter_routed_views(patterns):
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            yield from iter_routed_views(pattern.url_patterns)
            continue
        view = getattr(pattern.callback, "view_class", None)
        if view is None:  # the one project function view is a JSON endpoint
            continue
        yield view
        yield from (target for _, target, _ in descendants(view) if target is not None)


def routed_project_views():
    views = set(iter_routed_views(get_resolver().url_patterns))
    return {view for view in views if route_name(view).startswith(PROJECT_PREFIXES)}


def view_template_names(view):
    """The names Django would try for this view, without a request or an object."""
    if not issubclass(view, TemplateResponseMixin) or route_name(view) in NON_RENDERING_VIEWS:
        return []
    instance = view()
    instance.request, instance.args, instance.kwargs, instance.object = None, (), {}, None
    model = getattr(view, "model", None)
    is_model = isinstance(model, type) and issubclass(model, models.Model)
    instance.object_list = model._default_manager.none() if is_model else []
    return list(instance.get_template_names())


def constant_name(expression):
    """A quoted template name with no filters, else None."""
    return expression.var if not expression.filters and isinstance(expression.var, str) else None


@cache
def referenced_templates(name):
    """Constant extends/include targets of one template; raises if it cannot load."""
    nodelist = get_template(name).template.nodelist
    targets = {constant_name(node.parent_name) for node in nodelist.get_nodes_by_type(ExtendsNode)}
    targets |= {constant_name(node.template) for node in nodelist.get_nodes_by_type(IncludeNode)}
    return tuple(sorted(targets - {None}))


def scan_templates(root, missing, broken):
    seen, stack = set(), [root]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        try:
            stack.extend(referenced_templates(name))
        except TemplateDoesNotExist:
            missing.add(name)
        except TemplateSyntaxError as exc:
            broken[name] = str(exc).splitlines()[0]


def first_loadable(names):
    """The name select_template() would use: the first that exists, else the first name."""
    for name in names:
        try:
            get_template(name)
        except TemplateDoesNotExist:
            continue
        except TemplateSyntaxError:
            pass  # it exists; scan_templates reports the error
        return name
    return names[0]


def missing_routed_templates():
    """({missing template: {views reaching it}}, {broken template: first error line})."""
    missing_by_template, broken = {}, {}
    for view in routed_project_views():
        names = view_template_names(view)
        if not names:
            continue
        missing = set()
        scan_templates(first_loadable(names), missing, broken)
        for name in missing:
            missing_by_template.setdefault(name, set()).add(route_name(view))
    return missing_by_template, broken


class RoutedTemplatesTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.missing, cls.broken = missing_routed_templates()

    def test_routed_templates_compile(self):
        self.assertEqual(self.broken, {})

    def test_no_new_missing_templates(self):
        new = {t: sorted(views) for t, views in self.missing.items() if t not in KNOWN_MISSING}
        self.assertEqual(
            new, {}, "Routed pages whose template is missing: write it, or add to KNOWN_MISSING"
        )

    def test_known_missing_templates_are_still_missing(self):
        written = sorted(set(KNOWN_MISSING) - set(self.missing))
        self.assertEqual(written, [], "These templates exist now: remove them from KNOWN_MISSING")

    def test_known_missing_entries_name_a_view_that_reaches_them(self):
        for template, (view, _step) in KNOWN_MISSING.items():
            with self.subTest(template=template):
                self.assertIn(view, self.missing.get(template, {view}))

    def test_non_rendering_views_are_still_routed(self):
        routed = {route_name(view) for view in routed_project_views()}
        self.assertEqual(set(NON_RENDERING_VIEWS) - routed, set())
```

- [ ] **Step 2: Run it**

```bash
python manage.py test core.tests.test_routed_templates
```
Expected: `Ran 5 tests … OK` (≈1 s). Each entry in `KNOWN_MISSING` was produced by the walker, and D1.4 already removed the only compile error.

- [ ] **Step 3: Prove each guard fails when it should** (scratch changes, all reverted before commit)

```bash
sed -i '1i {% load widget_tweaks %}' locations/templates/locations/mage/demesne/form_include.html
echo x > characters/templates/characters/demon/ritual/list.html
echo '{% include "core/does_not_exist.html" %}' >> core/templates/core/form.html
python manage.py test core.tests.test_routed_templates
```
Expected: `FAILED (failures=3)`:
- `test_routed_templates_compile` lists `locations/mage/demesne/form_include.html: 'widget_tweaks' is not a registered tag library…`;
- `test_known_missing_templates_are_still_missing` lists `characters/demon/ritual/list.html`;
- `test_no_new_missing_templates` lists `core/does_not_exist.html` with the views that reach it.

Revert:
```bash
git checkout -- core/templates/core/form.html locations/templates/locations/mage/demesne/form_include.html
rm characters/templates/characters/demon/ritual/list.html
git status --short   # must show only core/tests/test_routed_templates.py as untracked
python manage.py test core.tests.test_routed_templates   # OK again
```

- [ ] **Step 4: Lint and commit**

```bash
ruff check core/tests/test_routed_templates.py
ruff format --check core/tests/test_routed_templates.py
git add core/tests/test_routed_templates.py
git commit -m "test(core): every routed page's template chain exists" -m "Walk every routed view and DictView target, resolve its template names, and follow constant extends/include targets (they only load at render time). Missing templates must match KNOWN_MISSING, which records the 10 known gaps from the dead-code design section 7 with their owning step; the test also fails when an allowlisted template is written but its entry stays, and on any template that fails to compile." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

- [ ] **Unit gate:**

```bash
python manage.py test            # serial, ≈40 min
python manage.py check
python manage.py test core.tests.security.test_route_policies
python scripts/find_dead_code.py --format tsv > /tmp/d1/gate.tsv && diff /tmp/d1/before.tsv /tmp/d1/gate.tsv && echo IDENTICAL
ruff check scripts/dead_code_heuristics.py scripts/find_dead_code.py core/tests/test_dead_code_heuristics.py core/tests/test_find_dead_code_script.py tg/settings/base.py accounts/tests/views/test_auth_redirects.py locations/tests/views/mage/test_demesne.py core/tests/test_routed_templates.py
ruff format --check scripts/dead_code_heuristics.py scripts/find_dead_code.py core/tests/test_dead_code_heuristics.py core/tests/test_find_dead_code_script.py tg/settings/base.py accounts/tests/views/test_auth_redirects.py locations/tests/views/mage/test_demesne.py core/tests/test_routed_templates.py
```
`/tmp/d1/before.tsv` is the snapshot from D1.1 Step 1; if it is gone, regenerate it on a checkout of the commit before D1.1.

Required: the full suite reports **0 failures and 0 errors** (baseline after B0); expected result `Ran 7144 tests … OK (skipped=49)` (verified by running the whole suite on a scratch copy with all of B0 and D1 applied; it took ≈70 min there); `check` clean; route-policy test passes; `find_dead_code.py` output is identical to the pre-D1 snapshot (D1 deletes nothing, and the new test files add no literal that changes a status — verified); ruff clean, all files formatted. Route count is unchanged (D1 adds no URL).


## Unit D2: Remove the `django-smart-selects` dependency

Spec: `docs/superpowers/specs/2026-09-25-dead-code-removal-design.md` §1, *Removal safety*, *Rollout* row 3. Every command below runs from the repo root with the project venv's `python` and `ruff` (`/tmp/claude-0/venv/bin/python` in this environment). Run tests serially: parallel runs crash the runner.

All line numbers are at `1e77e23`. D1 and C1 land first and may shift them; every edit below is also anchored on exact text, which is what to match.

### Task 9: [D2.1] Shared guard module, route-count snippet, and the requirement removal

**Files:**
- Create: `core/tests/test_dead_code_removed.py` (shared by every Step 1 PR; structure defined here)
- Modify: `requirements.txt:3`
- Create (outside the repo, not committed): `/tmp/route_count.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `core.tests.test_dead_code_removed.RemovalAssertions` (helpers `assertRequirementRemoved`, `assertModuleRemoved`, `assertAttributesRemoved`, `assertUrlNamesRemoved`, `assertUrlNamespaceRemoved`, `assertTemplatesRemoved`), `REPO_ROOT`, class `D2DependencyRemovedTest`. The route-count snippet `/tmp/route_count.py`, used by every later task.

- [ ] **Step 1: Create the shared guard module with the D2 guard.** The convention for every later PR: add exactly one class per PR, named `D<n><What>RemovedTest(RemovalAssertions, SimpleTestCase)`, appended at the end of the file. Guards need no database. Extend the imports only when a new helper or class needs them. Write `core/tests/test_dead_code_removed.py`:

```python
"""Guards for code deleted by the Step 1 dead-code removal.

Design: docs/superpowers/specs/2026-09-25-dead-code-removal-design.md. Each rollout PR adds
one ``SimpleTestCase`` subclass named after its PR ID (``D2DependencyRemovedTest``, ...) that
mixes in ``RemovalAssertions``. A guard fails while the dead code exists and keeps it from
coming back. Guards need no database, so every class is a ``SimpleTestCase``.
"""

import importlib
import importlib.util
import re
from pathlib import Path

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import SimpleTestCase
from django.urls import NoReverseMatch, get_resolver, reverse

REPO_ROOT = Path(settings.BASE_DIR)


class RemovalAssertions:
    """Assertions shared by every removal guard in this module."""

    def assertRequirementRemoved(self, distribution):
        names = set()
        for line in (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                names.add(re.split(r"[\s<>=!~;\[]", line, maxsplit=1)[0].lower())
        self.assertNotIn(distribution.lower(), names)

    def assertModuleRemoved(self, dotted_path):
        try:
            spec = importlib.util.find_spec(dotted_path)
        except ModuleNotFoundError:  # a parent package is gone too
            spec = None
        self.assertIsNone(spec, f"{dotted_path} still exists")

    def assertAttributesRemoved(self, module_path, *names):
        module = importlib.import_module(module_path)
        for name in names:
            with self.subTest(name=f"{module_path}.{name}"):
                self.assertFalse(hasattr(module, name), f"{module_path}.{name} still exists")
                self.assertNotIn(name, getattr(module, "__all__", ()))

    def assertUrlNamesRemoved(self, *names):
        for name in names:
            with self.subTest(name=name), self.assertRaises(NoReverseMatch):
                reverse(name)

    def assertUrlNamespaceRemoved(self, namespace):
        *parents, leaf = namespace.split(":")
        resolver = get_resolver()
        for parent in parents:
            resolver = resolver.namespace_dict[parent][1]
        self.assertNotIn(leaf, resolver.namespace_dict, f"{namespace} is still mounted")

    def assertTemplatesRemoved(self, *names):
        for name in names:
            with self.subTest(name=name), self.assertRaises(TemplateDoesNotExist):
                get_template(name)


class D2DependencyRemovedTest(RemovalAssertions, SimpleTestCase):
    """D2: django-smart-selects is not a dependency."""

    def test_django_smart_selects_not_in_requirements(self):
        self.assertRequirementRemoved("django-smart-selects")
```

- [ ] **Step 2: Run it; expect FAIL.**

```bash
python manage.py test core.tests.test_dead_code_removed
```

Expected: `FAILED (failures=1)`, with `AssertionError: 'django-smart-selects' unexpectedly found in {...}`.

- [ ] **Step 3: Write the route-count snippet and record the "before" numbers.** Save this file outside the repo as `/tmp/route_count.py`:

```python
from django.urls import URLPattern, URLResolver, get_resolver


def walk(patterns, prefix=""):
    for pattern in patterns:
        if isinstance(pattern, URLResolver):
            yield from walk(pattern.url_patterns, prefix + str(pattern.pattern))
        elif isinstance(pattern, URLPattern):
            yield prefix + str(pattern.pattern)


routes = list(walk(get_resolver().url_patterns))
print("total", len(routes))
gamelines = ("vampire", "werewolf", "mage", "wraith", "changeling", "demon", "mummy", "hunter")
for app in ("characters", "locations"):
    print(app, {g: sum(r.startswith(f"{app}/{g}/") for r in routes) for g in gamelines})
print("ajax", sorted(r for r in routes if "/ajax/" in r))
```

Run it (`-v 0` hides Django 5.2's shell auto-import banner) and save the output:

```bash
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())" | tee /tmp/routes-before-D2.txt
```

At `1e77e23` the output is (C1 may change the mage numbers; the deltas below are what matter):

```
total 1833
characters {'vampire': 43, 'werewolf': 76, 'mage': 83, 'wraith': 35, 'changeling': 46, 'demon': 52, 'mummy': 16, 'hunter': 20}
locations {'vampire': 22, 'werewolf': 4, 'mage': 46, 'wraith': 24, 'changeling': 18, 'demon': 8, 'mummy': 12, 'hunter': 10}
ajax ['characters/ajax/load_examples/', 'characters/ajax/load_values/', 'characters/mage/ajax/get_abilities/', 'characters/mage/ajax/get_practice_abilities/', 'characters/mage/ajax/load_advantage_values/', 'characters/mage/ajax/load_affinities/', 'characters/mage/ajax/load_attributes/', 'characters/mage/ajax/load_companion_examples/', 'characters/mage/ajax/load_mf_ratings/', 'characters/mage/ajax/load_sorcerer_examples/', 'characters/mage/ajax/load_xp_examples/', 'locations/mage/ajax/load_chantry_examples/']
```

A gameline showing `0` means its URLconf was silently dropped (see Unit D4).

- [ ] **Step 4: Delete the requirement.** `requirements.txt`, before (lines 1–4):

```
Django>=5.2.9
django-polymorphic==4.1.0
django-smart-selects==1.7.2
django-tinymce4-lite==1.8.0
```

After:

```
Django>=5.2.9
django-polymorphic==4.1.0
django-tinymce4-lite==1.8.0
```

- [ ] **Step 5: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed            # OK (1 test)
python manage.py check                                              # no issues
python manage.py test core.tests.security.test_route_policies      # OK (4 tests)
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())" | diff /tmp/routes-before-D2.txt -   # no output: delta 0
grep -rn "smart_selects\|smart-selects" --include=*.py --include=*.html --include=*.js --include=*.txt --include=*.toml --include=*.sh . | grep -v "^./docs/"   # no output
# prove nothing imports the package even though the venv still has it installed:
python -c "
import os, sys
sys.modules['smart_selects'] = None  # any 'import smart_selects' now raises ImportError
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tg.settings')
import django
django.setup()
from django.core.management import call_command
from django.urls import get_resolver
call_command('check')
get_resolver().url_patterns
print('smart_selects never imported')
"
ruff check core/tests/test_dead_code_removed.py && ruff format --check core/tests/test_dead_code_removed.py
```

Expected: every command passes; the last `python -c` prints `System check identified no issues (0 silenced).` then `smart_selects never imported`. Optionally run `pip uninstall -y django-smart-selects` in your own venv; nothing needs it.

- [ ] **Step 6: Commit.**

```bash
git add requirements.txt core/tests/test_dead_code_removed.py
git commit -F- <<'EOF'
Remove unused django-smart-selects dependency (D2)

Nothing imports smart_selects and it was never in INSTALLED_APPS. Adds
core/tests/test_dead_code_removed.py, the shared guard module that every
Step 1 removal PR extends with one RemovalAssertions test class.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**
  - `python manage.py test` (serial, about 40 min): **0 failures** (the baseline failures are fixed by the earlier unit). At `1e77e23` the suite has 7,105 tests; D2 adds 1.
  - `python manage.py check`: no issues.
  - `python manage.py test core.tests.security.test_route_policies`: OK.
  - Route count: identical to `/tmp/routes-before-D2.txt` (delta 0).
  - `python scripts/find_dead_code.py --section symbols`: unchanged. The dependency is not something the script tracks; the `grep` in Step 5 is this unit's detection check.
  - `ruff check core/tests/test_dead_code_removed.py` and `ruff format --check core/tests/test_dead_code_removed.py`: clean.

## Unit D3: Remove the deprecated `chained_select` app and the widgets-side copies

Spec §1 rows 2–3. The live `/__chained_select__/` endpoint (`widgets.views.auto_chained_ajax_view`, name `__chained_select_ajax__`, injected by `widgets/apps.py:19-46`, manifest policy `WIDGET`) is **kept**.

### Task 10: [D3.1] Delete `chained_select`, `make_ajax_view`, `ChainedSelectAjaxView`, `ChainedSelectMultiple`

**Files:**
- Delete (directory, 15 tracked files): `chained_select/` — `README.md`, `__init__.py`, `apps.py`, `fields.py`, `views.py`, `widgets.py`, `docs/{codemap,health,measurement,summary,theory}.html`, `examples/{__init__,database_backed,mage_model,mage_simple}.py`, **plus its untracked `__pycache__/` directories**
- Modify: `tg/settings/base.py:37-38`
- Modify: `widgets/__init__.py:83-84, 95, 115, 117`
- Modify: `widgets/views.py:4, 58-145`
- Modify: `widgets/widgets/__init__.py:5, 14`
- Modify: `widgets/widgets/chained.py:322-326` (+ the two blank lines after)
- Modify: `widgets/tests/test_chained_select.py:13, 159-166, 318-336, 339-375`
- Modify: `core/tests/test_dead_code_removed.py` (append class `D3ChainedSelectRemovedTest`)

**Interfaces:**
- Consumes: `RemovalAssertions` from Task D2.1.
- Produces: `widgets` exports without `ChainedSelectAjaxView`, `make_ajax_view` and `ChainedSelectMultiple`. `INSTALLED_APPS` without `chained_select`. `widgets.views` now holds only `auto_chained_ajax_view` and its private helpers.

- [ ] **Step 1: Append the D3 guard** to the end of `core/tests/test_dead_code_removed.py` (no new imports needed):

```python


class D3ChainedSelectRemovedTest(RemovalAssertions, SimpleTestCase):
    """D3: the deprecated chained_select app and its widgets-side copies are gone."""

    def test_chained_select_app_removed(self):
        self.assertNotIn("chained_select", settings.INSTALLED_APPS)
        self.assertModuleRemoved("chained_select")

    def test_widgets_copies_removed(self):
        self.assertAttributesRemoved("widgets", "ChainedSelectAjaxView", "make_ajax_view")
        self.assertAttributesRemoved("widgets", "ChainedSelectMultiple")
        self.assertAttributesRemoved("widgets.views", "ChainedSelectAjaxView", "make_ajax_view")
        self.assertAttributesRemoved("widgets.widgets", "ChainedSelectMultiple")
        self.assertAttributesRemoved("widgets.widgets.chained", "ChainedSelectMultiple")

    def test_live_widget_endpoint_kept(self):
        self.assertEqual(reverse("__chained_select_ajax__"), "/__chained_select__/")
```

- [ ] **Step 2: Run it; expect FAIL.**

```bash
python manage.py test core.tests.test_dead_code_removed.D3ChainedSelectRemovedTest
```

Expected: `FAILED (failures=8)`: `test_chained_select_app_removed` once, and 7 subtests of `test_widgets_copies_removed`. `test_live_widget_endpoint_kept` passes (it is a keep-guard).

- [ ] **Step 3: Delete the app, including its bytecode.** `git rm` leaves the ignored `__pycache__/` behind, and an `chained_select/` directory holding only `__pycache__` is still importable as a namespace package, so `find_spec("chained_select")` keeps succeeding.

```bash
git rm -r -q chained_select
rm -rf chained_select
test ! -e chained_select && echo gone
```

- [ ] **Step 4: Edit `tg/settings/base.py`.** Before (lines 37–38):

```python
    "widgets",  # Reusable form widgets (replaces chained_select)
    "chained_select",  # Deprecated - backward compatibility only
```

After:

```python
    "widgets",  # Reusable form widgets
```

- [ ] **Step 5: Edit `widgets/__init__.py`.** Before (lines 83–84):

```python
from .views import ChainedSelectAjaxView, auto_chained_ajax_view, make_ajax_view
from .widgets.chained import ChainedSelect, ChainedSelectMultiple
```

After:

```python
from .views import auto_chained_ajax_view
from .widgets.chained import ChainedSelect
```

In `__all__`, before (lines 94–95 and 114–117):

```python
    "ChainedSelect",
    "ChainedSelectMultiple",
```
```python
    # Views
    "ChainedSelectAjaxView",
    "auto_chained_ajax_view",
    "make_ajax_view",
```

After:

```python
    "ChainedSelect",
```
```python
    # Views
    "auto_chained_ajax_view",
```

- [ ] **Step 6: Edit `widgets/views.py`.** Delete line 4, `from django.views import View` (no other user). Delete everything from line 58 (the two blank lines before `class ChainedSelectAjaxView(View):`) to the end of the file (line 145, `    return ConfiguredAjaxView.as_view()`): the whole `ChainedSelectAjaxView` class (lines 60–96) and the whole `make_ajax_view` function (lines 99–145, including the nested `ConfiguredAjaxView`). The file must now end with:

```python
    callback = form.fields[field_name].choices_callback
    return JsonResponse({"choices": normalize_choices(callback(parent_id))})
```

followed by a single newline.

- [ ] **Step 7: Edit `widgets/widgets/__init__.py`.** Line 5 `from .chained import ChainedSelect, ChainedSelectMultiple` becomes `from .chained import ChainedSelect`. In `__all__` delete line 14, `    "ChainedSelectMultiple",`.

- [ ] **Step 8: Edit `widgets/widgets/chained.py`.** Delete lines 322–328, so that `reset_js_rendered` is followed directly by the signal block. Before:

```python
        cls._js_rendered = False


class ChainedSelectMultiple(ChainedSelect, forms.SelectMultiple):
    """Multiple-select variant of ChainedSelect."""

    pass


# Reset flag between requests using Django's request_finished signal
```

After:

```python
        cls._js_rendered = False


# Reset flag between requests using Django's request_finished signal
```

(`forms` stays imported; `ChainedSelect` still uses it.)

- [ ] **Step 9: Edit `widgets/tests/test_chained_select.py`.**
  - Module import (lines 8–14): delete line 13, `    ChainedSelectMultiple,`.
  - Delete the whole `TestChainedSelectMultiple` class, lines 159–166 and the two blank lines after it:

    ```python
    class TestChainedSelectMultiple(TestCase):
        """Tests for ChainedSelectMultiple widget."""

        def test_multiple_select_inherits_chained_select(self):
            """Test ChainedSelectMultiple inherits from ChainedSelect."""
            widget = ChainedSelectMultiple()
            self.assertIsInstance(widget, ChainedSelect)
    ```

  - `TestWidgetsImports.test_all_exports_available`, before (lines 318–336):

    ```python
            from widgets import (
                ChainedChoiceField,
                ChainedSelect,
                ChainedSelectAjaxView,
                ChainedSelectMixin,
                ChainedSelectMultiple,
                auto_chained_ajax_view,
                make_ajax_view,
            )

            # Just verify imports work
            self.assertIsNotNone(ChainedChoiceField)
            self.assertIsNotNone(ChainedModelChoiceField)
            self.assertIsNotNone(ChainedSelect)
            self.assertIsNotNone(ChainedSelectMultiple)
            self.assertIsNotNone(ChainedSelectMixin)
            self.assertIsNotNone(ChainedSelectAjaxView)
            self.assertIsNotNone(auto_chained_ajax_view)
            self.assertIsNotNone(make_ajax_view)
    ```

    After:

    ```python
            from widgets import (
                ChainedChoiceField,
                ChainedSelect,
                ChainedSelectMixin,
                auto_chained_ajax_view,
            )

            # Just verify imports work
            self.assertIsNotNone(ChainedChoiceField)
            self.assertIsNotNone(ChainedModelChoiceField)
            self.assertIsNotNone(ChainedSelect)
            self.assertIsNotNone(ChainedSelectMixin)
            self.assertIsNotNone(auto_chained_ajax_view)
    ```

  - Delete the whole `TestBackwardCompatibility` class (lines 339–375, from `class TestBackwardCompatibility(TestCase):` through `        self.assertIs(NewField, OldField)`) and the two blank lines before it. The file now ends with `        self.assertIsNotNone(auto_chained_ajax_view)` and one newline. This also removes the file's only pre-existing ruff violation (F841 `has_warning`).

- [ ] **Step 10: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed widgets     # OK (150 tests at 1e77e23+D2)
python manage.py check                                                # no issues
python manage.py test core.tests.security.test_route_policies        # OK
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())" | diff /tmp/routes-before-D2.txt -   # no output: delta 0 (/__chained_select__/ is still counted)
grep -rn "chained_select" --include=*.py . | grep -v "^./docs/"      # only: scripts/inventory_authorization_routes.py:102, widgets/apps.py:38/43/45, widgets/mixins/chained.py:110, widgets/tests/test_ajax_authorization.py:10, core/tests/test_dead_code_removed.py (the D3 guard), and the test-method names test_*_chained_select* (all refer to the kept endpoint, the guard or are test names)
ruff check tg/settings/base.py widgets/__init__.py widgets/views.py widgets/widgets/__init__.py widgets/widgets/chained.py widgets/tests/test_chained_select.py core/tests/test_dead_code_removed.py
ruff format --check tg/settings/base.py widgets/__init__.py widgets/views.py widgets/widgets/__init__.py widgets/widgets/chained.py widgets/tests/test_chained_select.py core/tests/test_dead_code_removed.py
```

Expected: both ruff commands report clean (`All checks passed!`, `7 files already formatted`).

- [ ] **Step 11: Commit.**

```bash
git add tg/settings/base.py widgets/__init__.py widgets/views.py widgets/widgets/__init__.py widgets/widgets/chained.py widgets/tests/test_chained_select.py core/tests/test_dead_code_removed.py
git status --short chained_select   # the 15 deletions are already staged by git rm
git commit -F- <<'EOF'
Remove deprecated chained_select app and unused widgets copies (D3)

chained_select had no models, migrations, URLs or templates and only
re-exported widgets. Also drop widgets.views.make_ajax_view,
ChainedSelectAjaxView and ChainedSelectMultiple, which only chained_select
and tests used. The live /__chained_select__/ endpoint
(auto_chained_ajax_view) is unchanged.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**
  - `python manage.py test` (serial): **0 failures**. D3 removes 3 tests and adds 3.
  - `python manage.py check`: no issues. `python manage.py test core.tests.security.test_route_policies`: OK.
  - Route count: delta 0 against `/tmp/routes-before-D2.txt`.
  - `python scripts/find_dead_code.py --section views --section symbols --format tsv | grep -ciE "chained_select|make_ajax_view|ChainedSelectAjaxView|ChainedSelectMultiple"` prints `0`. The summaries change from `views ... 1032 project view classes; ... referenced in code (review): 3` to `1030 ...; referenced in code (review): 1` (only `RitualCreateView` remains), and `symbols ... only referenced from tests: 33, unreferenced: 16` to `29` and `11` (the 5 `chained_select.examples` forms, the two `chained_select` copies and the two widgets symbols are gone).
  - `ruff check` / `ruff format --check` on the 7 touched files: clean.

## Unit D4: Remove the 11 unused AJAX endpoints and everything only they used

Spec §3. Removes `characters:ajax:{load_examples,load_values}` and `characters:mage:ajax:{load_mf_ratings,load_xp_examples,get_abilities,load_companion_examples,load_advantage_values,load_sorcerer_examples,get_practice_abilities,load_attributes,load_affinities}`. **Keeps** `locations:mage:ajax:load_chantry_examples` (removed by chantry PR C5), and therefore keeps `locations/urls/mage/ajax.py` and `core.ajax.dropdown_options_response`, which that view still calls.

**Why the route count matters here (spec rule 3).** `characters/urls/__init__.py:13-24` and `locations/urls/__init__.py:13-24` wrap each gameline import in `except (ImportError, AttributeError): pass`. If a gameline `__init__.py` still says `from . import ajax` after its `ajax.py` is deleted, that gameline's whole URLconf vanishes and `manage.py check` still passes. This was reproduced: deleting only `characters/urls/vampire/ajax.py` drops the total from 1822 to 1779 and shows `'vampire': 0`. Every D4 task runs the route-count snippet, and Task D4.3 adds a permanent guard test for this.

**Expected totals across D4** (from the D3 "after" numbers, which equal `1e77e23`'s if C1 adds no routes): routes 1833 → 1822 (−11, all under `characters/`: `characters/mage/` 83 → 74, and the two top-level `characters/ajax/` routes); every other gameline count unchanged; `ajax` list = `['locations/mage/ajax/load_chantry_examples/']`. Manifest: `VIEW_POLICIES` 975 → 964 entries (−11 view names), `POLICIES` 16 → 15 keys (`OBJECT_AJAX` gone), `LOGIN` 41 → 36.

### Task 11: [D4.1] Delete the 5 freebie population views and the 7 dropdown templates

These are unrouted, so the route count and manifest do not change.

**Files:**
- Modify: `characters/views/core/human.py:6` (`from django.views import View`), `:330-446` (`HumanFreebieFormPopulationView`)
- Modify: `characters/views/werewolf/garou.py:22, 401-404`
- Modify: `characters/views/demon/demon_chargen.py:15, 21, 452-467`
- Modify: `characters/views/demon/dtfhuman_chargen.py:17, 240-243`
- Modify: `characters/views/demon/thrall_chargen.py:13, 204-207`
- Modify: `characters/views/demon/__init__.py:17, 28, 56, 75, 82, 114`
- Modify: `characters/tests/views/wraith/test_wraith_chargen.py:406-421` (`TestWraithFreebieFormPopulationView`, a class with a `setUp` and no tests, for a view that no longer exists)
- Delete: `characters/templates/characters/core/human/load_examples_dropdown_list.html`, `characters/templates/characters/core/human/load_values_dropdown_list.html`, `characters/templates/characters/mage/mage/load_faction_dropdown_list.html`, `characters/templates/characters/mage/mage/load_mf_rating_dropdown_list.html`, `characters/templates/characters/mage/mage/load_subfaction_dropdown_list.html`, `characters/templates/characters/mage/sorcerer/load_affinity_dropdown_list.html`, `characters/templates/characters/mage/sorcerer/load_attribute_dropdown_list.html`
- Modify: `core/tests/test_dead_code_removed.py` (append class `D4AjaxEndpointsRemovedTest`)

**Interfaces:**
- Consumes: `RemovalAssertions`.
- Produces: `characters.views.core.human` without `HumanFreebieFormPopulationView` (and without the `View` import). `characters.views.demon` package exports without the 3 demon population views. Class `D4AjaxEndpointsRemovedTest`, which Tasks D4.2–D4.5 extend by appending methods at the end of the class body.

- [ ] **Step 1: Record the route count, then append the D4 guard class.**

```bash
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())" | tee /tmp/routes-before-D4.txt
```

Append to `core/tests/test_dead_code_removed.py`:

```python


class D4AjaxEndpointsRemovedTest(RemovalAssertions, SimpleTestCase):
    """D4: the unused AJAX endpoints, their views, templates and bases are gone."""

    def test_freebie_population_views_removed(self):
        for module_path, name in [
            ("characters.views.core.human", "HumanFreebieFormPopulationView"),
            ("characters.views.werewolf.garou", "WerewolfFreebieFormPopulationView"),
            ("characters.views.demon.demon_chargen", "DemonFreebieFormPopulationView"),
            ("characters.views.demon.dtfhuman_chargen", "DtFHumanFreebieFormPopulationView"),
            ("characters.views.demon.thrall_chargen", "ThrallFreebieFormPopulationView"),
            ("characters.views.demon", "DemonFreebieFormPopulationView"),
            ("characters.views.demon", "DtFHumanFreebieFormPopulationView"),
            ("characters.views.demon", "ThrallFreebieFormPopulationView"),
        ]:
            self.assertAttributesRemoved(module_path, name)

    def test_dropdown_templates_removed(self):
        self.assertTemplatesRemoved(
            "characters/core/human/load_examples_dropdown_list.html",
            "characters/core/human/load_values_dropdown_list.html",
            "characters/mage/mage/load_faction_dropdown_list.html",
            "characters/mage/mage/load_mf_rating_dropdown_list.html",
            "characters/mage/mage/load_subfaction_dropdown_list.html",
            "characters/mage/sorcerer/load_affinity_dropdown_list.html",
            "characters/mage/sorcerer/load_attribute_dropdown_list.html",
        )
```

- [ ] **Step 2: Run it; expect FAIL.**

```bash
python manage.py test core.tests.test_dead_code_removed.D4AjaxEndpointsRemovedTest
```

Expected: `FAILED (failures=15)` (7 template subtests and 8 view subtests).

- [ ] **Step 3: Record the ruff baseline for the files this task edits.**

```bash
FILES="characters/views/core/human.py characters/views/werewolf/garou.py characters/views/demon/demon_chargen.py characters/views/demon/dtfhuman_chargen.py characters/views/demon/thrall_chargen.py characters/views/demon/__init__.py characters/tests/views/wraith/test_wraith_chargen.py"
ruff check --output-format concise $FILES | grep -E '^[^ ]+:[0-9]+:[0-9]+: ' | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort > /tmp/ruff-before-D4.1.txt
```

- [ ] **Step 4: Delete the population views and their imports/exports.**
  - `characters/views/core/human.py`: delete the whole class from `class HumanFreebieFormPopulationView(View):` (line 330) through `        return examples.filter(id__in=affordable_mfs)` (line 444) and the two blank lines after it, so the preceding `LoadValuesView` is followed by two blank lines and `class HumanFreebiesView(SpendFreebiesPermissionMixin, UpdateView):`. Then delete line 6, `from django.views import View` (its only user was this class; F401 otherwise).
  - `characters/views/werewolf/garou.py`: delete line 22, `    HumanFreebieFormPopulationView,`, from the `from characters.views.core.human import (...)` block. Delete lines 401–404:

    ```python
    class WerewolfFreebieFormPopulationView(HumanFreebieFormPopulationView):
        primary_class = Werewolf


    ```

    so `WerewolfExtrasView` is followed directly by `class WerewolfFreebiesView(HumanFreebiesView):`. (Do not touch the pre-existing unused `Background` import on line 14; it is outside this PR's scope.)
  - `characters/views/demon/demon_chargen.py`: delete line 21, `    HumanFreebieFormPopulationView,`. Delete lines 452–467:

    ```python
    class DemonFreebieFormPopulationView(HumanFreebieFormPopulationView):
        primary_class = Demon

        def category_method_map(self):
            d = super().category_method_map()
            d.update(
                {
                    "Lore": self.lore_options,
                }
            )
            return d

        def lore_options(self):
            return Lore.objects.all().order_by("name")


    ```

    so `DemonSpecialtiesView` is followed directly by `class DemonCharacterCreationView(HumanCharacterCreationView):`. Then delete line 15, `from characters.models.demon.lore import Lore` (its only user was `lore_options`).
  - `characters/views/demon/dtfhuman_chargen.py`: delete line 17, `    HumanFreebieFormPopulationView,`, and lines 240–243:

    ```python
    class DtFHumanFreebieFormPopulationView(HumanFreebieFormPopulationView):
        primary_class = DtFHuman


    ```

  - `characters/views/demon/thrall_chargen.py`: delete line 13, `    HumanFreebieFormPopulationView,`, and lines 204–207:

    ```python
    class ThrallFreebieFormPopulationView(HumanFreebieFormPopulationView):
        primary_class = Thrall


    ```

  - `characters/views/demon/__init__.py`: delete these six lines: 17 `    DemonFreebieFormPopulationView,`, 28 `    DtFHumanFreebieFormPopulationView,`, 56 `    ThrallFreebieFormPopulationView,`, 75 `    "DemonFreebieFormPopulationView",`, 82 `    "DtFHumanFreebieFormPopulationView",`, 114 `    "ThrallFreebieFormPopulationView",`. Result, for example:

    ```python
    from .demon_chargen import (
        DemonBasicsView,
        DemonCharacterCreationView,
    )
    ```

  - `characters/tests/views/wraith/test_wraith_chargen.py`: delete lines 406–421 (the class and the two blank lines after it):

    ```python
    class TestWraithFreebieFormPopulationView(TestCase):
        """Test WraithFreebieFormPopulationView for populating freebie options."""

        def setUp(self):
            self.client = Client()
            self.owner = User.objects.create_user(
                username="owner", email="owner@test.com", password="password"
            )
            self.wraith = Wraith.objects.create(
                name="Test Wraith",
                owner=self.owner,
                creation_status=9,
                freebies=15,
            )


    ```

- [ ] **Step 5: Delete the 7 templates.**

```bash
git rm -q characters/templates/characters/core/human/load_examples_dropdown_list.html \
  characters/templates/characters/core/human/load_values_dropdown_list.html \
  characters/templates/characters/mage/mage/load_faction_dropdown_list.html \
  characters/templates/characters/mage/mage/load_mf_rating_dropdown_list.html \
  characters/templates/characters/mage/mage/load_subfaction_dropdown_list.html \
  characters/templates/characters/mage/sorcerer/load_affinity_dropdown_list.html \
  characters/templates/characters/mage/sorcerer/load_attribute_dropdown_list.html
```

- [ ] **Step 6: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed characters.tests.views.demon characters.tests.views.werewolf characters.tests.views.wraith characters.tests.views.core
python manage.py check
python manage.py test core.tests.security.test_route_policies
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())" | diff /tmp/routes-before-D4.txt -   # no output: delta 0
ruff check --output-format concise $FILES core/tests/test_dead_code_removed.py | grep -E '^[^ ]+:[0-9]+:[0-9]+: ' | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort > /tmp/ruff-after-D4.1.txt
comm -13 /tmp/ruff-before-D4.1.txt /tmp/ruff-after-D4.1.txt   # must print nothing (no new violations)
ruff format --check $FILES core/tests/test_dead_code_removed.py
```

Expected: tests OK (364 tests in this label set at `1e77e23`; the circle test is one of the baseline failures and is fixed by the earlier unit). Ruff: only these pre-existing violations remain in `$FILES`: `test_wraith_chargen.py` F841 ×3, `demon_chargen.py` F841 (`demon`), `garou.py` F401 (`Background`). `ruff format --check`: only `characters/views/werewolf/garou.py` "would reformat", and it already did at `1e77e23` (a `help_text` assignment at line 340, untouched). `human.py` becomes formatted, because its unformatted lines were in the deleted classes.

- [ ] **Step 7: Commit.**

```bash
git add characters/views/core/human.py characters/views/werewolf/garou.py characters/views/demon/demon_chargen.py characters/views/demon/dtfhuman_chargen.py characters/views/demon/thrall_chargen.py characters/views/demon/__init__.py characters/tests/views/wraith/test_wraith_chargen.py core/tests/test_dead_code_removed.py
git commit -F- <<'EOF'
Remove unrouted freebie population views and orphan dropdown templates (D4)

The five *FreebieFormPopulationView classes were never routed; the chained
freebies forms replaced them. Nothing renders the seven
load_*_dropdown_list.html templates.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 12: [D4.2] Delete the 11 endpoint routes, views, manifest lines and endpoint-only tests

**Files:**
- Delete: `characters/urls/core/ajax.py`, `characters/urls/mage/ajax.py`
- Modify: `characters/urls/__init__.py:8, 29`; `characters/urls/mage/__init__.py:3, 6`
- Modify: `characters/views/core/human.py:12-13, 15, 23, 26, 267-329` (`LoadExamplesView`, `LoadValuesView`; line numbers before Task D4.1's edits)
- Modify: `characters/views/mage/mage.py:8-37` (dead cost helpers), `:48, 59-60, 62-63, 66, 70, 86, 88, 93`, `:103-252` (`LoadMFRatingsView`, `LoadXPExamplesView`, `GetAbilitiesView`)
- Modify: `characters/views/mage/companion.py:6, 38, 46, 155-218` (`LoadExamplesView`, `LoadCompanionValuesView`)
- Modify: `characters/views/mage/sorcerer.py:5, 8, 26, 48, 50, 60, 110-127, 159-231, 258-267` (`LoadAttributesView`, `LoadAffinitiesView`, `LoadExamplesView`, `GetPracticeAbilitiesView`)
- Modify: `characters/views/mage/__init__.py:8, 61-62, 86-88, 106, 152-153, 174-176`
- Modify: `core/route_policy_manifest.py:306-307, 311-313, 342-349`
- Delete: `characters/tests/views/core/test_character.py` (all 155 lines are AJAX-auth tests for these endpoints), `characters/tests/views/core/test_ajax_json_responses.py` (all 232 lines test these endpoints)
- Modify: `characters/tests/views/core/test_human.py:8-10, 34-84`
- Modify: `characters/tests/views/mage/test_mage_comprehensive.py:3-4, 12, 14, 179-345, 490-518`
- Modify: `characters/tests/views/mage/test_companion_comprehensive.py:3-4, 12, 219-308` (at `1e77e23`; after unit B0's Task B0.3 adds one import and three test lines, these are `3-4, 13, 223-312`)
- Modify: `characters/tests/views/mage/test_sorcerer_comprehensive.py:3-4, 12, 303-415`
- Modify: `characters/tests/views/test_public_detail_authorization.py:13, 231-247`
- Modify: `characters/tests/urls/test_url_patterns.py:111-119` (`CharactersAjaxUrlsTest`)
- Modify: `core/tests/urls/test_url_namespaces.py:72-76` (`test_characters_ajax_namespace`)
- Modify: `core/tests/test_dead_code_removed.py` (import `resolve`; append 3 methods)

**Interfaces:**
- Consumes: `D4AjaxEndpointsRemovedTest` from Task D4.1.
- Produces: no `characters:ajax` or `characters:mage:ajax` namespace. Manifest without the 11 view names and without the `OBJECT_AJAX` key. `core.mixins.DropdownOptionsView`, `SimpleValuesView`, `JsonListView` and `AjaxLoginRequiredMixin` left with no subclasses (removed in Task D4.5). `core.access_policy`'s `OBJECT_AJAX` branch left unreachable (removed in Task D4.4).

- [ ] **Step 1: Extend the guard.** In `core/tests/test_dead_code_removed.py` change the import line

```python
from django.urls import NoReverseMatch, get_resolver, reverse
```

to

```python
from django.urls import NoReverseMatch, get_resolver, resolve, reverse
```

and append inside `D4AjaxEndpointsRemovedTest` (after `test_dropdown_templates_removed`):

```python

    REMOVED_AJAX_URL_NAMES = (
        "characters:ajax:load_examples",
        "characters:ajax:load_values",
        "characters:mage:ajax:load_mf_ratings",
        "characters:mage:ajax:load_xp_examples",
        "characters:mage:ajax:get_abilities",
        "characters:mage:ajax:load_companion_examples",
        "characters:mage:ajax:load_advantage_values",
        "characters:mage:ajax:load_sorcerer_examples",
        "characters:mage:ajax:get_practice_abilities",
        "characters:mage:ajax:load_attributes",
        "characters:mage:ajax:load_affinities",
    )
    REMOVED_AJAX_VIEWS = (
        "characters.views.core.human.LoadExamplesView",
        "characters.views.core.human.LoadValuesView",
        "characters.views.mage.mage.LoadMFRatingsView",
        "characters.views.mage.mage.LoadXPExamplesView",
        "characters.views.mage.mage.GetAbilitiesView",
        "characters.views.mage.companion.LoadExamplesView",
        "characters.views.mage.companion.LoadCompanionValuesView",
        "characters.views.mage.sorcerer.LoadExamplesView",
        "characters.views.mage.sorcerer.GetPracticeAbilitiesView",
        "characters.views.mage.sorcerer.LoadAttributesView",
        "characters.views.mage.sorcerer.LoadAffinitiesView",
    )

    def test_ajax_url_names_removed(self):
        self.assertUrlNamesRemoved(*self.REMOVED_AJAX_URL_NAMES)
        self.assertUrlNamespaceRemoved("characters:ajax")
        self.assertUrlNamespaceRemoved("characters:mage:ajax")
        self.assertModuleRemoved("characters.urls.core.ajax")
        self.assertModuleRemoved("characters.urls.mage.ajax")

    def test_ajax_views_removed(self):
        from core.route_policy_manifest import VIEW_POLICIES

        for dotted in self.REMOVED_AJAX_VIEWS:
            module_path, name = dotted.rsplit(".", 1)
            self.assertAttributesRemoved(module_path, name)
            self.assertNotIn(dotted, VIEW_POLICIES)
        self.assertAttributesRemoved(
            "characters.views.mage",
            "LoadCompanionValuesView",
            "GetAbilitiesView",
            "LoadMFRatingsView",
            "GetPracticeAbilitiesView",
            "LoadAffinitiesView",
            "LoadAttributesView",
        )

    def test_chantry_ajax_endpoint_kept_until_c5(self):
        # resolve() a path and never spell the URL name, so find_dead_code.py still reports
        # the route as dead until chantry PR C5 deletes it together with this test.
        from locations.views.mage.chantry import LoadExamplesView

        match = resolve("/locations/mage/ajax/load_chantry_examples/")
        self.assertIs(match.func.view_class, LoadExamplesView)
```

- [ ] **Step 2: Run it; expect FAIL.**

```bash
python manage.py test core.tests.test_dead_code_removed.D4AjaxEndpointsRemovedTest
```

Expected: `FAILED (failures=14)`: 11 URL-name subtests plus the non-subtest failure of `test_ajax_url_names_removed`, and `test_ajax_views_removed` (subtest `characters.views.core.human.LoadExamplesView` plus the test itself). `test_chantry_ajax_endpoint_kept_until_c5` passes.

- [ ] **Step 3: Record the ruff baseline** for the existing files this task edits:

```bash
FILES="characters/urls/__init__.py characters/urls/mage/__init__.py characters/views/core/human.py characters/views/mage/mage.py characters/views/mage/companion.py characters/views/mage/sorcerer.py characters/views/mage/__init__.py core/route_policy_manifest.py characters/tests/views/core/test_human.py characters/tests/views/mage/test_mage_comprehensive.py characters/tests/views/mage/test_companion_comprehensive.py characters/tests/views/mage/test_sorcerer_comprehensive.py characters/tests/views/test_public_detail_authorization.py characters/tests/urls/test_url_patterns.py core/tests/urls/test_url_namespaces.py"
ruff check --output-format concise $FILES | grep -E '^[^ ]+:[0-9]+:[0-9]+: ' | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort > /tmp/ruff-before-D4.2.txt
```

- [ ] **Step 4: URLs.** Delete both URL modules:

```bash
git rm -q characters/urls/core/ajax.py characters/urls/mage/ajax.py
```

`characters/urls/__init__.py`: line 8 `from .core import ajax, create, detail, index, update` becomes `from .core import create, detail, index, update`; delete line 29:

```python
        path("ajax/", include((ajax.urls, "characters_ajax"), namespace="ajax")),
```

`characters/urls/mage/__init__.py`: line 3 `from characters.urls.mage import ajax, create, detail, index, update` becomes `from characters.urls.mage import create, detail, index, update`; delete line 6:

```python
    path("ajax/", include((ajax.urls, "mage_ajax"), namespace="ajax")),
```

- [ ] **Step 5: `characters/views/core/human.py`.** Delete from `class LoadExamplesView(DropdownOptionsView):` (line 267) through `        return ratings` at the end of `LoadValuesView` (line 327) and the two blank lines after it; `HumanBiographicalInformation` is now followed directly by `class HumanFreebiesView(`. Then remove the imports only those classes used. Before:

```python
from characters.models.core import Human
from characters.models.core.ability_block import Ability
from characters.models.core.attribute_block import Attribute
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.merit_flaw_block import MeritFlaw
from characters.models.core.specialty import Specialty
```
```python
from core.mixins import (
    DropdownOptionsView,
    EditPermissionMixin,
    MessageMixin,
    SimpleValuesView,
    SpendFreebiesPermissionMixin,
    prepare_created_object,
)
```

After:

```python
from characters.models.core import Human
from characters.models.core.background_block import Background, BackgroundRating
from characters.models.core.specialty import Specialty
```
```python
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    SpendFreebiesPermissionMixin,
    prepare_created_object,
)
```

- [ ] **Step 6: `characters/views/mage/mage.py`.**
  - Delete lines 8–37: the `characters.costs` import, the `LimitedHumanEditForm` import, and the three module-level helpers `_calculate_xp_cost`, `_mage_sphere_xp_cost` and `_mage_practice_xp_cost` (their only caller was `LoadXPExamplesView`; `characters/forms/core/xp.py` and `characters/forms/mage/xp.py` have their own copies). Before (lines 6–39):

    ```python
    logger = logging.getLogger(__name__)

    from characters.costs import get_meritflaw_xp_cost, get_xp_cost
    from characters.forms.core.limited_edit import LimitedHumanEditForm


    def _calculate_xp_cost(trait_type, current_value):
        ...  # lines 12-19
    def _mage_sphere_xp_cost(character, sphere):
        ...  # lines 22-28
    def _mage_practice_xp_cost(character, practice):
        ...  # lines 31-36


    import re
    ```

    After:

    ```python
    logger = logging.getLogger(__name__)

    import re
    ```

    Re-add `LimitedHumanEditForm` in sorted position in the first-party block, immediately above `from characters.forms.core.linked_npc import LinkedNPCForm`:

    ```python
    from characters.forms.core.limited_edit import LimitedHumanEditForm
    from characters.forms.core.linked_npc import LinkedNPCForm
    ```

  - Delete from `class LoadMFRatingsView(SimpleValuesView):` (line 103) through `        return [{"id": ability.id, "name": ability.name} for ability in abilities]` at the end of `GetAbilitiesView` (line 250) and the two blank lines after it; the import block is now followed by two blank lines and `class MageDetailView(HumanDetailView):`.
  - Remove the now-unused imports. Before → after:
    - line 48 `from django.views import View` → delete
    - line 59 `from characters.models.core.ability_block import Ability` → delete
    - line 60 `from characters.models.core.attribute_block import Attribute` → delete
    - line 62 `from characters.models.core.human import Human` → delete
    - line 63 `from characters.models.core.merit_flaw_block import MeritFlaw` → delete
    - line 66 `from characters.models.mage.focus import Practice, SpecializedPractice, Tenet` → `from characters.models.mage.focus import Tenet`
    - line 70 `from characters.models.mage.sphere import Sphere` → delete
    - lines 86 and 88 in `from core.mixins import (...)`: delete `    JsonListView,` and `    SimpleValuesView,`, leaving `EditPermissionMixin`, `MessageMixin`, `SpecialUserMixin`
    - line 93 `from game.models import ObjectType, XPSpendingRequest` → `from game.models import XPSpendingRequest`

    Shortcut with the same result: after the two block deletions, run `ruff check --fix --select F401,I001 characters/views/mage/mage.py`. It makes exactly the edits above. Confirm with `git diff`. Do not run it on `characters/views/werewolf/garou.py`, which has an unrelated pre-existing F401.

- [ ] **Step 7: `characters/views/mage/companion.py`.** Delete from `class LoadExamplesView(LoginRequiredMixin, View):` (line 155) through `        return ratings` at the end of `LoadCompanionValuesView` (line 216) and the two blank lines after it; `CompanionUpdateView` is followed by `class CompanionBasicsView(`. Remove the imports: line 6 `from django.views import View`, line 38 `    SimpleValuesView,` (inside `from core.mixins import (...)`), line 46 `from game.models import ObjectType`.

- [ ] **Step 8: `characters/views/mage/sorcerer.py`.** Delete three blocks, each with the two blank lines after it:
  - `class LoadAttributesView(DropdownOptionsView):` (line 110) through `        return sf.favored_paths.all()` (line 125, end of `LoadAffinitiesView`); `SorcererBasicsView` is followed by `class SorcererUpdateView(`.
  - `class LoadExamplesView(LoginRequiredMixin, View):` (line 159) through `        return dropdown_options_response(examples, label_attr="__str__")` (line 229); `SorcererDetailView` is followed by `class SorcererAttributeView(HumanAttributeView):`.
  - `class GetPracticeAbilitiesView(JsonListView):` (line 258) through `        return [{"id": ability.id, "name": ability.name} for ability in abilities]` (line 265); `SorcererBackgroundsView` is followed by `class SorcererPsychicView(`.

  Remove the imports: line 5 `from django.db.models import Q`, line 8 `from django.views import View`, line 26 `from characters.models.core.merit_flaw_block import MeritFlaw`, lines 48 `    DropdownOptionsView,` and 50 `    JsonListView,` (inside `from core.mixins import (...)`), and line 60 `from game.models import ObjectType`. This also removes the pre-existing C416 at line 181, which was inside `LoadExamplesView`.

- [ ] **Step 9: `characters/views/mage/__init__.py`.** Delete the 12 lines `    LoadCompanionValuesView,` (8), `    GetAbilitiesView,` (61), `    LoadMFRatingsView,` (62), `    GetPracticeAbilitiesView,` (86), `    LoadAffinitiesView,` (87), `    LoadAttributesView,` (88), `    "LoadCompanionValuesView",` (106), `    "GetAbilitiesView",` (152), `    "LoadMFRatingsView",` (153), `    "GetPracticeAbilitiesView",` (174), `    "LoadAffinitiesView",` (175), `    "LoadAttributesView",` (176). For example, after:

```python
from .mage import (
    MageBasicsView,
    MageCharacterCreationView,
    MageCreateView,
    MageDetailView,
    MageUpdateView,
)
```

- [ ] **Step 10: `core/route_policy_manifest.py`** (spec rule 2: same commit as the URL deletion). In the `'LOGIN'` block delete the 5 lines:

```
characters.views.mage.companion.LoadCompanionValuesView
characters.views.mage.mage.LoadMFRatingsView
characters.views.mage.sorcerer.GetPracticeAbilitiesView
characters.views.mage.sorcerer.LoadAffinitiesView
characters.views.mage.sorcerer.LoadAttributesView
```

Delete the whole `OBJECT_AJAX` entry (lines 342–349), so `'OBJECT_ACTION'` is followed directly by `'OBJECT_CREATE'`:

```python
    'OBJECT_AJAX': frozenset("""
characters.views.core.human.LoadExamplesView
characters.views.core.human.LoadValuesView
characters.views.mage.companion.LoadExamplesView
characters.views.mage.mage.GetAbilitiesView
characters.views.mage.mage.LoadXPExamplesView
characters.views.mage.sorcerer.LoadExamplesView
    """.split()),
```

Keep `locations.views.mage.chantry.LoadExamplesView` in `LOGIN` (C5 removes it).

- [ ] **Step 11: Tests that exist only for these endpoints.**

```bash
git rm -q characters/tests/views/core/test_character.py characters/tests/views/core/test_ajax_json_responses.py
```

  - `characters/tests/views/core/test_human.py`: delete `class TestLoadValuesView(TestCase):` (line 34) through line 82 (`        self.assertEqual(response.status_code, 200)`) and the two blank lines after it. Delete imports lines 8–10: `from characters.models.core.merit_flaw_block import MeritFlaw`, `from core.models import Number`, `from game.models import ObjectType`.
  - `characters/tests/views/mage/test_mage_comprehensive.py`:
    - Delete `class TestMageAjaxViews(TestCase):` (line 179) through line 343 (the last line of `TestMageXPExamplesView.test_load_xp_examples_practice`) and the two blank lines after it. This removes `TestMageAjaxViews`, the `@unittest.skip`'d `TestMageFreebieFormPopulationView` (it reverses the nonexistent `characters:mage:ajax:load_freebie_examples`) and `TestMageXPExamplesView`. `TestMageDetailViewPost` is now followed by `class TestMageCharacterCreationWorkflow(TestCase):`.
    - Delete `class TestGetAbilitiesView(TestCase):` (line 492) to the end of the file (line 518) and the two blank lines before it. The file ends with `        self.assertEqual(response.status_code, 302)` and one newline.
    - Imports: delete `import unittest` (line 3) and the blank line after it; delete `from characters.models.core.merit_flaw_block import MeritFlaw` (line 12); `from characters.models.mage.focus import Practice, Tenet` (line 14) → `from characters.models.mage.focus import Tenet`.
  - `characters/tests/views/mage/test_companion_comprehensive.py`: delete from `@unittest.skip("URL 'companion_load_examples' not implemented yet")` (line 219) through line 306 (the end of the second skipped class, `TestCompanionValuesView`, which reverses the nonexistent `load_companion_values`) and the two blank lines after it; `TestCompanionFreebiesView` is followed by `class TestCompanionLanguagesView(TestCase):`. Imports: delete `import unittest` (line 3) and the blank line after it; `from characters.models.mage.companion import Advantage, Companion` (line 12) → `from characters.models.mage.companion import Companion`. This also removes the pre-existing F841 `advantage` (line 277 at `1e77e23`, 281 after B0.3) that the B0 plan leaves for D4.
  - `characters/tests/views/mage/test_sorcerer_comprehensive.py`: delete from `@unittest.skip("URLs 'load_sorcerer_attributes' and 'load_sorcerer_affinities' not implemented yet")` (line 305) to the end of the file (line 415), and the two blank lines before it. This removes the two skipped classes `TestSorcererAjaxViews` and `TestSorcererExamplesView` and `TestGetPracticeAbilitiesView`. The file ends with `        self.assertEqual(response.status_code, 200)` (end of `TestSorcererFreebiesView`). Imports: delete `import unittest` (line 3) and the blank line after it; delete `from characters.models.mage.focus import Practice` (line 12).
  - `characters/tests/views/test_public_detail_authorization.py`: delete from `    def test_character_dependent_ajax_requires_full_read(self):` (line 232) to the end of the file (line 247, `        self.assertEqual(ObjectType.objects.count(), before)`), and the blank line before it. That removes both path-string tests of `/characters/mage/ajax/load_xp_examples/`. The file ends with `        self.assertEqual(self.mage.status, "Dec")`. Line 13 `from game.models import Chronicle, Gameline, ObjectType, STRelationship` → `from game.models import Chronicle, Gameline, STRelationship`.
  - `characters/tests/urls/test_url_patterns.py`: delete lines 111–119. `/characters/ajax/` resolves to `characters:character` both before and after, so this test proves nothing:

    ```python
    class CharactersAjaxUrlsTest(TestCase):
        """Tests for AJAX URL patterns."""

        def test_ajax_namespace_exists(self):
            """Test that ajax namespace is accessible."""
            resolver = resolve("/characters/ajax/")
            self.assertIsNotNone(resolver)


    ```

  - `core/tests/urls/test_url_namespaces.py`: delete lines 72–76, for the same reason:

    ```python
        def test_characters_ajax_namespace(self):
            """Test that characters:ajax namespace is accessible."""
            resolver = resolve("/characters/ajax/")
            self.assertIsNotNone(resolver)

    ```

- [ ] **Step 12: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed core.tests.security.test_route_policies core.tests.urls characters.tests.urls
python manage.py test characters.tests.views.mage characters.tests.views.core characters.tests.views.test_public_detail_authorization
python manage.py check
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())" | diff /tmp/routes-before-D4.txt -
python manage.py shell -v 0 -c "
from core.route_policy_manifest import POLICIES, VIEW_POLICIES
print(len(VIEW_POLICIES), len(POLICIES), len(POLICIES['LOGIN']), 'OBJECT_AJAX' in POLICIES)"
ruff check --output-format concise $FILES core/tests/test_dead_code_removed.py | grep -E '^[^ ]+:[0-9]+:[0-9]+: ' | sed -E 's/:[0-9]+:[0-9]+:/:/' | sort > /tmp/ruff-after-D4.2.txt
comm -13 /tmp/ruff-before-D4.2.txt /tmp/ruff-after-D4.2.txt   # must print nothing
ruff format --check $FILES core/tests/test_dead_code_removed.py
```

Expected:
- The first test run is OK (43 tests); the second is OK (224 tests at `1e77e23`, once the earlier unit has fixed the companion baseline failure).
- Route diff, exactly (numbers at `1e77e23`):

  ```
  < total 1833
  < characters {'vampire': 43, 'werewolf': 76, 'mage': 83, ...
  < ajax ['characters/ajax/load_examples/', ... 'locations/mage/ajax/load_chantry_examples/']
  > total 1822
  > characters {'vampire': 43, 'werewolf': 76, 'mage': 74, 'wraith': 35, 'changeling': 46, 'demon': 52, 'mummy': 16, 'hunter': 20}
  > ajax ['locations/mage/ajax/load_chantry_examples/']
  ```

  The `locations` line is unchanged. The total drops by exactly 11, `characters/mage/` by 9, and no gameline changes otherwise.
- Manifest line: `964 15 36 False`.
- `comm` prints nothing.
- `ruff format --check`: "would reformat" only for `characters/tests/views/test_public_detail_authorization.py`, `characters/views/mage/mage.py` and `core/route_policy_manifest.py`, all pre-existing at `1e77e23` in untouched lines. Do not reformat them. If one of the three edited test files is flagged, it is a leftover blank line from the `import unittest` or end-of-file deletions: `ruff format` on that one file fixes it. All three were formatted at `1e77e23`.

- [ ] **Step 13: Commit.**

```bash
git add characters/urls/__init__.py characters/urls/mage/__init__.py characters/views/core/human.py characters/views/mage/mage.py characters/views/mage/companion.py characters/views/mage/sorcerer.py characters/views/mage/__init__.py core/route_policy_manifest.py characters/tests/views/core/test_human.py characters/tests/views/mage/test_mage_comprehensive.py characters/tests/views/mage/test_companion_comprehensive.py characters/tests/views/mage/test_sorcerer_comprehensive.py characters/tests/views/test_public_detail_authorization.py characters/tests/urls/test_url_patterns.py core/tests/urls/test_url_namespaces.py core/tests/test_dead_code_removed.py
git commit -F- <<'EOF'
Remove 11 unused character AJAX endpoints (D4)

Nothing in templates, Python or JS calls characters:ajax:* or
characters:mage:ajax:* (except the chantry endpoint, which C5 removes).
Deletes their views, re-exports, route-policy manifest entries (5 LOGIN,
6 OBJECT_AJAX), the Mage XP cost helpers only LoadXPExamplesView used, and
the tests that existed only for them. Route count 1833 -> 1822.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 13: [D4.3] Delete the empty gameline `ajax.py` modules and their `include()`s

**Files:**
- Delete: `characters/urls/changeling/ajax.py`, `characters/urls/vampire/ajax.py`, `characters/urls/werewolf/ajax.py`, `characters/urls/wraith/ajax.py`, `locations/urls/vampire/ajax.py` (each defines only `app_name` and `urls = []`)
- Modify: `characters/urls/changeling/__init__.py:3, 6`; `characters/urls/vampire/__init__.py:3, 6`; `characters/urls/werewolf/__init__.py:3, 6`; `characters/urls/wraith/__init__.py:3, 6`; `locations/urls/vampire/__init__.py:3, 9`
- Modify: `core/tests/test_dead_code_removed.py` (append 2 methods)
- Unchanged: `locations/urls/mage/ajax.py` and its include (C5).

**Interfaces:**
- Consumes: `D4AjaxEndpointsRemovedTest`.
- Produces: no `ajax` namespace under any `characters` gameline or `locations:vampire`. The permanent guard `test_every_gameline_urlconf_still_mounted`.

- [ ] **Step 1: Extend the guard.** Append inside `D4AjaxEndpointsRemovedTest`:

```python

    def test_empty_gameline_ajax_modules_removed(self):
        for namespace in (
            "characters:changeling:ajax",
            "characters:vampire:ajax",
            "characters:werewolf:ajax",
            "characters:wraith:ajax",
            "locations:vampire:ajax",
        ):
            app, gameline, _ = namespace.split(":")
            self.assertModuleRemoved(f"{app}.urls.{gameline}.ajax")
            self.assertUrlNamespaceRemoved(namespace)

    def test_every_gameline_urlconf_still_mounted(self):
        # characters/urls/__init__.py and locations/urls/__init__.py swallow ImportError,
        # so a dangling "from . import ajax" would silently drop a whole gameline.
        from core.constants import GameLine

        for app in ("characters", "locations"):
            mounted = get_resolver().namespace_dict[app][1].namespace_dict
            for _url_path, module_name, namespace in GameLine.URL_PATTERNS:
                with self.subTest(app=app, gameline=module_name):
                    module = importlib.import_module(f"{app}.urls.{module_name}")
                    self.assertTrue(hasattr(module, "urls"))
                    self.assertIn(namespace, mounted)
```

- [ ] **Step 2: Run it; expect FAIL.**

```bash
python manage.py test core.tests.test_dead_code_removed.D4AjaxEndpointsRemovedTest
```

Expected: `FAILED (failures=1)`: `test_empty_gameline_ajax_modules_removed` fails on its first module. `test_every_gameline_urlconf_still_mounted` passes now; it must keep passing after Step 3. (Verified: deleting only `characters/urls/vampire/ajax.py` makes it ERROR with `ImportError: cannot import name 'ajax' ... characters.urls.vampire`, while `manage.py check` stays green.)

- [ ] **Step 3: Delete the modules and, in the same edit, their imports and `include()`s.**

```bash
git rm -q characters/urls/changeling/ajax.py characters/urls/vampire/ajax.py characters/urls/werewolf/ajax.py characters/urls/wraith/ajax.py locations/urls/vampire/ajax.py
```

For each `G` in `changeling`, `vampire`, `werewolf`, `wraith`, in `characters/urls/G/__init__.py`, line 3:

```python
from . import ajax, create, detail, index, update
```

becomes

```python
from . import create, detail, index, update
```

and delete line 6, which is exactly:

```python
    path("ajax/", include((ajax.urls, "changeling_ajax"), namespace="ajax")),   # changeling
    path("ajax/", include((ajax.urls, "vampire_ajax"), namespace="ajax")),      # vampire
    path("ajax/", include((ajax.urls, "werewolf_ajax"), namespace="ajax")),     # werewolf
    path("ajax/", include((ajax.urls, "wraith_ajax"), namespace="ajax")),       # wraith
```

(the trailing `# ...` comments here only label which file each line belongs to).

In `locations/urls/vampire/__init__.py`, line 3 becomes `from . import create, detail, index, update`, and delete line 9:

```python
    path("ajax/", include((ajax.urls, "vampire_ajax"), namespace="ajax")),
```

Every one of these files still uses `include` and `path`, so no other import changes.

- [ ] **Step 4: Verify.**

```bash
grep -rn "import ajax\|ajax\.urls" characters/urls locations/urls   # only locations/urls/mage/__init__.py (lines 3 and its include), kept for C5
python manage.py test core.tests.test_dead_code_removed core.tests.security.test_route_policies core.tests.urls characters.tests.urls locations.tests.urls
python manage.py check
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())"
ruff check characters/urls/changeling/__init__.py characters/urls/vampire/__init__.py characters/urls/werewolf/__init__.py characters/urls/wraith/__init__.py locations/urls/vampire/__init__.py core/tests/test_dead_code_removed.py
ruff format --check characters/urls/changeling/__init__.py characters/urls/vampire/__init__.py characters/urls/werewolf/__init__.py characters/urls/wraith/__init__.py locations/urls/vampire/__init__.py core/tests/test_dead_code_removed.py
```

Expected: tests OK (56 tests at `1e77e23`). Route count **identical to the end of Task D4.2** (delta 0): `total 1822`, `characters {'vampire': 43, 'werewolf': 76, 'mage': 74, 'wraith': 35, 'changeling': 46, 'demon': 52, 'mummy': 16, 'hunter': 20}`, the `locations` line unchanged, `ajax ['locations/mage/ajax/load_chantry_examples/']`. A `0` for any gameline means a dangling import: stop and fix it. Ruff: clean.

- [ ] **Step 5: Commit.**

```bash
git add characters/urls/changeling/__init__.py characters/urls/vampire/__init__.py characters/urls/werewolf/__init__.py characters/urls/wraith/__init__.py locations/urls/vampire/__init__.py core/tests/test_dead_code_removed.py
git commit -F- <<'EOF'
Remove empty gameline ajax URL modules (D4)

Drops the empty ajax.py modules for character changeling, vampire,
werewolf and wraith and location vampire, together with their imports and
include()s. The gameline URL loaders swallow ImportError, so a new guard
test checks that every gameline URLconf stays mounted. Route count
unchanged.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 14: [D4.4] Delete the unreachable `OBJECT_AJAX` access policy

**Files:**
- Modify: `core/access_policy.py:65-83`
- Modify: `scripts/build_route_policy_manifest.py:40-48`
- Modify: `scripts/inventory_authorization_routes.py:180`
- Modify: `core/tests/test_dead_code_removed.py` (append 1 method)

**Interfaces:**
- Consumes: the manifest without `OBJECT_AJAX` (Task D4.2).
- Produces: `authorize_route` with no `OBJECT_AJAX` branch. Its tests were `test_public_detail_authorization.py`'s two AJAX cases, already deleted in Task D4.2; no other test exercises the branch (checked: `core/tests/views/test_generic.py` and `core/tests/security/*` have none).

- [ ] **Step 1: Extend the guard.** Append inside `D4AjaxEndpointsRemovedTest`:

```python

    def test_object_ajax_policy_removed(self):
        from core.route_policy_manifest import POLICIES

        self.assertNotIn("OBJECT_AJAX", POLICIES)
        for relative in (
            "core/access_policy.py",
            "scripts/build_route_policy_manifest.py",
            "scripts/inventory_authorization_routes.py",
        ):
            with self.subTest(file=relative):
                source = (REPO_ROOT / relative).read_text(encoding="utf-8")
                self.assertNotIn("OBJECT_AJAX", source)
```

- [ ] **Step 2: Run it; expect FAIL.** `python manage.py test core.tests.test_dead_code_removed.D4AjaxEndpointsRemovedTest` gives `FAILED (failures=3)`, one subtest per file.

- [ ] **Step 3: Edit.**
  - `core/access_policy.py`: delete lines 65–83, so `OBJECT_LIST`'s `return None` is followed by `    if policy in {"LOGIN", "ACCOUNT", "GAME", "OBJECT_CREATE"}:`:

    ```python
        if policy == "OBJECT_AJAX":
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)
            object_id = request.GET.get("object")
            if object_id:
                if (
                    len(object_id) > 20
                    or not object_id.isascii()
                    or not object_id.isdecimal()
                    or int(object_id) < 1
                ):
                    raise Http404("Object not found")

                subject = _object(CharacterModel, {"pk": object_id})
                if not PermissionManager.user_has_permission(
                    request.user, subject, Permission.VIEW_FULL, request=request
                ):
                    raise Http404("Object not found")
            return None
    ```

    Every import stays in use: `JsonResponse` (WIDGET), `Http404`/`_object`/`CharacterModel`/`Permission`/`PermissionManager` (CHARGEN_STEP and the object policies).
  - `scripts/build_route_policy_manifest.py`: delete lines 40–48, so `classify()` starts with `    if name == "core.views.public_object.PublicObjectDetailView":`:

    ```python
        if name in {
            "characters.views.core.human.LoadExamplesView",
            "characters.views.core.human.LoadValuesView",
            "characters.views.mage.companion.LoadExamplesView",
            "characters.views.mage.mage.GetAbilitiesView",
            "characters.views.mage.mage.LoadXPExamplesView",
            "characters.views.mage.sorcerer.LoadExamplesView",
        }:
            return "OBJECT_AJAX"
    ```

  - `scripts/inventory_authorization_routes.py`: in `main().effective_login`, delete line 180, `            "OBJECT_AJAX",` (between `"OBJECT_ACTION",` and `"OBJECT_CREATE",`).

- [ ] **Step 4: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed core.tests.security core.tests.views.test_generic   # OK (53 tests)
python manage.py check
python scripts/inventory_authorization_routes.py > /dev/null && echo inventory-ok
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())"   # same as end of D4.2
ruff check core/access_policy.py scripts/build_route_policy_manifest.py scripts/inventory_authorization_routes.py core/tests/test_dead_code_removed.py   # All checks passed!
ruff format --check core/access_policy.py core/tests/test_dead_code_removed.py   # already formatted
```

Do **not** run `scripts/build_route_policy_manifest.py` as a check. It overwrites `core/route_policy_manifest.py`, and at `1e77e23` its output already differs from the reviewed manifest by 16 lines (manual reclassifications). The two `scripts/*.py` files were "would reformat" before this task; leave them unformatted.

- [ ] **Step 5: Commit.**

```bash
git add core/access_policy.py scripts/build_route_policy_manifest.py scripts/inventory_authorization_routes.py core/tests/test_dead_code_removed.py
git commit -F- <<'EOF'
Remove the unused OBJECT_AJAX route policy (D4)

No routed view has the OBJECT_AJAX policy since the character AJAX
endpoints were removed. Drop its evaluator branch and the tooling entries.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 15: [D4.5] Delete the AJAX view bases and `simple_values_response`

Verified: after Tasks D4.1–D4.2, `AjaxLoginRequiredMixin`, `DropdownOptionsView`, `SimpleValuesView` and `JsonListView` have no users except `scripts/inventory_authorization_routes.py`, and `core.ajax.simple_values_response` is used only by `SimpleValuesView` and its tests. **`core/ajax.py` itself stays**: `dropdown_options_response` is still called by `locations/views/mage/chantry.py:119,173` (`LoadExamplesView`, the C5 endpoint).

**Files:**
- Modify: `core/mixins.py:16` (`from django.views import View`), `:555-669` (the 4 classes)
- Modify: `core/ajax.py:65-88` (`simple_values_response`)
- Modify: `core/tests/test_ajax.py:7, 87-131` (`TestSimpleValuesResponse`)
- Modify: `scripts/inventory_authorization_routes.py:27, 79-80`
- Modify: `core/tests/test_dead_code_removed.py` (append 1 method)

**Interfaces:**
- Consumes: the view deletions of Tasks D4.1–D4.2.
- Produces: `core.mixins` without the AJAX bases. `core.ajax` containing only `dropdown_options_response`, for C5 to delete together with `core/tests/test_ajax.py`.

- [ ] **Step 1: Extend the guard.** Append inside `D4AjaxEndpointsRemovedTest`:

```python

    def test_ajax_view_bases_removed(self):
        self.assertAttributesRemoved(
            "core.mixins",
            "AjaxLoginRequiredMixin",
            "DropdownOptionsView",
            "SimpleValuesView",
            "JsonListView",
        )
        # dropdown_options_response stays until chantry PR C5 removes its last caller.
        self.assertAttributesRemoved("core.ajax", "simple_values_response")
```

- [ ] **Step 2: Run it; expect FAIL** (`failures=5`, one per name).

- [ ] **Step 3: Confirm there are no other users**, then edit.

```bash
grep -rn "AjaxLoginRequiredMixin\|DropdownOptionsView\|SimpleValuesView\|JsonListView\|simple_values_response" --include=*.py . | grep -v "^./docs/" | grep -v "^./core/mixins.py\|^./core/ajax.py\|^./core/tests/test_ajax.py\|^./core/tests/test_dead_code_removed.py"
# expected: only scripts/inventory_authorization_routes.py:27,79,80
```

  - `core/mixins.py`: delete from `class AjaxLoginRequiredMixin:` (line 555) through `        return JsonResponse(items, safe=False)` (line 667, end of `JsonListView`) and the two blank lines after it; `CharacterOwnerOrSTMixin` is followed by `class ApprovalMixin:`. Delete line 16, `from django.views import View` (its only users were these classes).
  - `core/ajax.py`: delete from the two blank lines before `def simple_values_response(values):` (line 67) to the end of the file (line 88). The file ends with `    return JsonResponse({"options": options})` and one newline.
  - `core/tests/test_ajax.py`: line 7 `from core.ajax import dropdown_options_response, simple_values_response` → `from core.ajax import dropdown_options_response`. Delete from the two blank lines before `class TestSimpleValuesResponse(SimpleTestCase):` (line 89) to the end of the file (line 131). The file ends with `        self.assertEqual(data["options"][2]["label"], "Second")` and one newline.
  - `scripts/inventory_authorization_routes.py`: before (lines 26–32):

    ```python
    from core.mixins import (  # noqa: E402
        AjaxLoginRequiredMixin,
        CharacterOwnerOrSTMixin,
        OwnerRequiredMixin,
        PermissionRequiredMixin,
        StorytellerRequiredMixin,
    )
    ```

    After:

    ```python
    from core.mixins import (  # noqa: E402
        CharacterOwnerOrSTMixin,
        OwnerRequiredMixin,
        PermissionRequiredMixin,
        StorytellerRequiredMixin,
    )
    ```

    In `gate()`, delete lines 79–80:

    ```python
        if AjaxLoginRequiredMixin in mro:
            return "AjaxLoginRequiredMixin", "yes"
    ```

- [ ] **Step 4: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed core.tests.test_ajax core.tests.security core.tests.mixins locations.tests.views   # OK (214 tests)
python manage.py check
python scripts/inventory_authorization_routes.py > /dev/null && echo inventory-ok
python manage.py shell -v 0 -c "exec(open('/tmp/route_count.py').read())"   # same as end of D4.2
ruff check core/mixins.py core/ajax.py core/tests/test_ajax.py scripts/inventory_authorization_routes.py core/tests/test_dead_code_removed.py   # All checks passed!
ruff format --check core/mixins.py core/ajax.py core/tests/test_ajax.py core/tests/test_dead_code_removed.py   # already formatted (fix a leftover trailing blank line with ruff format if flagged)
```

- [ ] **Step 5: Commit.**

```bash
git add core/mixins.py core/ajax.py core/tests/test_ajax.py scripts/inventory_authorization_routes.py core/tests/test_dead_code_removed.py
git commit -F- <<'EOF'
Remove AJAX view bases left unused by the endpoint removal (D4)

AjaxLoginRequiredMixin, DropdownOptionsView, SimpleValuesView, JsonListView
and core.ajax.simple_values_response have no users left.
dropdown_options_response stays for the chantry endpoint until C5.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**
  - `python manage.py test` (serial): **0 failures**. Verified on a throwaway worktree with D2 → D4.5 applied at `1e77e23`: 7,052 tests found (7,105 before), and the only failures were the 5 baseline ones, which the earlier unit fixes.
  - `python manage.py check`: no issues. `python manage.py test core.tests.security.test_route_policies`: OK.
  - Route count: `total` exactly 11 below `/tmp/routes-before-D4.txt` (1833 → 1822 at `1e77e23`), only `characters/mage/` changing among gamelines (83 → 74), `ajax` list = `['locations/mage/ajax/load_chantry_examples/']`. Manifest: `964 15 36 False`.
  - `python scripts/find_dead_code.py --section urls --section views --section templates --format tsv | grep "^# "` shows these changes against the D3 "after" numbers:
    - `urls`: 747 → 736 names; `tests only` 64 → 53; `tests only (b)` 11 → gone; `dead` stays 104 with `dead (b): 1` (the chantry endpoint).
    - `views`: 1030 → 1011 classes; `routed` 974 → 963; `base of routed` 16 → 13; `base of unrouted views only` 1 → gone; `dead` 38 → 34.
    - `templates`: 900 → 893; `dead` 23 → 16.

    `python scripts/find_dead_code.py --format tsv | grep -E "characters:(mage:)?ajax:|FreebieFormPopulationView|_dropdown_list\.html"` prints nothing.
  - Ruff: `comm` checks of Tasks D4.1/D4.2 empty. `ruff check` on the other touched files clean. `ruff format --check`: only the 6 files that were already unformatted at `1e77e23` remain flagged: `characters/tests/views/test_public_detail_authorization.py`, `characters/views/mage/mage.py`, `characters/views/werewolf/garou.py`, `core/route_policy_manifest.py`, `scripts/build_route_policy_manifest.py`, `scripts/inventory_authorization_routes.py`.


## Unit D5: Template tags

Design reference: `docs/superpowers/specs/2026-09-25-dead-code-removal-design.md` §4 (every row marked **Delete (D5)**), Rules 1–6, Rollout #6. Appendix rows: `2026-09-25-dead-code-removal-report.md` → *tags / Tag libraries* and *tags / Unused tags and filters*.

**Preconditions.** B0 and D1–D4 are merged. `core/tests/test_dead_code_removed.py` exists (created in Unit D4). If it is absent, create it with the single header line `from django.test import SimpleTestCase`. Every guard below uses function-local imports, so D5 and D6 never change the module header.

**Conventions.** `python` and `ruff` are the project venv's binaries (`/tmp/claude-0/venv/bin/python`, `/tmp/claude-0/venv/bin/ruff` in this environment). Run tests serially (the parallel runner crashes). `$SCRATCH` is any directory outside the repo (`export SCRATCH=$(mktemp -d)`). Line numbers are at `1e77e23` and were re-verified by applying every edit below in a scratch worktree and comparing the result byte-for-byte. No file D5 edits is on the design's D1–D4 lists, so they should still hold; wherever a snippet is given, match on the text rather than the number.

**Keep (not touched by D5):** `core/templatetags/permissions.py` (deferred to Step 6), `sanitize_text.render_post_html` (imported by `game/consumers.py:13`), every other tag/filter in `dots`, `json_filters`, `sanitize_text`, `formset_tags`.

**Line endings.** `core/templatetags/dots.py` uses CRLF line terminators. Truncate it with `head` (Task D5.2) so the CRLFs survive; an editor or a Python text-mode rewrite converts the whole file to LF and turns a 221-line deletion into a 339-line rewrite.

### Task 16: [D5.0] Record the baselines

**Files:** none changed.

**Interfaces:** none.

- [ ] **Step 1: Save the tag report and the route count.**

```bash
export SCRATCH=${SCRATCH:-$(mktemp -d)}
python scripts/find_dead_code.py --section tags > "$SCRATCH/tags_before.md"
grep '^\*\*Summary' "$SCRATCH/tags_before.md"
python manage.py shell -v 0 -c 'from django.urls import URLResolver, get_resolver
def walk(r):
    return sum(walk(p) if isinstance(p, URLResolver) else 1 for p in r.url_patterns)
print(walk(get_resolver()))' > "$SCRATCH/routes_before.txt"
```

Expected summary (D1–D4 do not change it): `**Summary:** 14 project tag libraries, 3 not loaded by non-test code; 48 tags/filters, 26 unused in templates`.

### Task 17: [D5.1] Delete the never-loaded `resonance` and `conditional_fields` libraries

**Files:**
- Delete: `core/templatetags/resonance.py` (8 lines), `core/tests/templatetags/test_resonance.py` (4-line TODO stub)
- Delete: `widgets/templatetags/conditional_fields.py` (85 lines; tags `conditional_wrap`, `as_conditional`)
- Modify: `widgets/mixins/conditional.py` (module docstring, lines 41–49)
- Modify (test): `core/tests/test_dead_code_removed.py` (append `class D5RemovedTests`)

**Interfaces:**
- Removes: template libraries `resonance`, `conditional_fields`; filter `resonance`; tag `conditional_wrap`; filter `as_conditional`. No Python or template user exists (report: loaded in 0 files, 0 Python refs).
- Keeps: `widgets.ConditionalFieldsMixin` (its `conditional_fields` rules and `conditional_js`), used by `characters/forms/core/chained_freebies.py`, `characters/forms/core/npc_profile.py` and `locations/forms/mage/chantry.py`.
- Produces: `D5RemovedTests` with helpers `_module_exists(dotted_path)` and `_assert_libraries_removed(libraries, modules)` that Tasks D5.2–D5.4 reuse.

- [ ] **Step 1: Write the guard.** Append to the end of `core/tests/test_dead_code_removed.py`:

```python
class D5RemovedTests(SimpleTestCase):
    """Unit D5: dead template tag libraries, tags, filters and templates stay deleted."""

    @staticmethod
    def _module_exists(dotted_path):
        """Return True when ``dotted_path`` can be imported (parents included)."""
        import importlib.util

        try:
            return importlib.util.find_spec(dotted_path) is not None
        except ModuleNotFoundError:
            return False

    def _assert_libraries_removed(self, libraries, modules):
        from django.template.backends.django import get_installed_libraries

        installed = get_installed_libraries()
        for name in libraries:
            with self.subTest(library=name):
                self.assertNotIn(name, installed)
        for dotted_path in modules:
            with self.subTest(module=dotted_path):
                self.assertFalse(self._module_exists(dotted_path))

    def test_never_loaded_libraries_are_gone(self):
        self._assert_libraries_removed(
            ("resonance", "conditional_fields"),
            ("core.templatetags.resonance", "widgets.templatetags.conditional_fields"),
        )

    def test_conditional_mixin_docstring_no_longer_shows_deleted_filter(self):
        from widgets.mixins import conditional

        self.assertNotIn("conditional_wrap", conditional.__doc__)

    def test_kept_step6_library_and_render_post_html_survive(self):
        from django.template.backends.django import get_installed_libraries

        from core.templatetags import sanitize_text

        self.assertIn("permissions", get_installed_libraries())
        self.assertTrue(callable(sanitize_text.render_post_html))
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests
```

Expected: `FAILED (failures=5)`: `test_never_loaded_libraries_are_gone` fails 4 subtests (`library='resonance'`, `library='conditional_fields'`, and the two `module=` subtests) and `test_conditional_mixin_docstring_no_longer_shows_deleted_filter` fails. `test_kept_step6_library_and_render_post_html_survive` passes (it guards the Keep rows and must stay green through D5).

- [ ] **Step 3: Delete and fix.**

```bash
git rm core/templatetags/resonance.py core/tests/templatetags/test_resonance.py widgets/templatetags/conditional_fields.py
```

In `widgets/mixins/conditional.py`, replace the docstring's template block (lines 41–49). The filter it showed was never loadable; the live templates write the wrapper `div`s by hand (for example `characters/templates/characters/changeling/changeling/freebies_form.html:73-74`, `locations/templates/locations/mage/chantry/point_spend_form.html:27-29`).

Before:
```
Template:
    <div class="row">
        {{ form.category }}
        {{ form.example|conditional_wrap }}
        {{ form.value|conditional_wrap }}
        {{ form.note|conditional_wrap }}
        {{ form.pooled|conditional_wrap:"Pooled?" }}
    </div>
    {{ form.conditional_js }}
```

After:
```
Template (wrap each conditional field in a container whose id is
"<field>_wrap"; add "d-none" when the field starts hidden):
    <div class="row">
        {{ form.category }}
        <div class="col-sm d-none" id="example_wrap">{{ form.example }}</div>
        <div class="col-sm d-none" id="value_wrap">{{ form.value }}</div>
        <div class="col-sm d-none" id="note_wrap">{{ form.note }}</div>
        <div class="col-sm d-none" id="pooled_wrap">Pooled? {{ form.pooled }}</div>
    </div>
    {{ form.conditional_js }}
```

- [ ] **Step 4: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests widgets.tests.test_conditional_fields core.tests.templatetags
python manage.py check
grep -rn "conditional_wrap\|as_conditional\|load resonance\|load conditional_fields" --include=*.py --include=*.html . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
```

Expected: tests `OK`; `System check identified no issues (0 silenced).`; the grep prints nothing. Every `grep` in D5/D6 excludes paths containing `/docs/`: `docs/code-fixing/01-dead-code-removal.md`, the design docs and the generated `*/docs/*.html` snapshot reports mention deleted names and stay as history.

- [ ] **Step 5: Commit.**

```bash
git add widgets/mixins/conditional.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove never-loaded resonance and conditional_fields tag libraries

Neither library was ever {% load %}ed. The resonance test module was a
two-line TODO stub. The ConditionalFieldsMixin docstring showed the
never-loadable conditional_wrap filter; it now shows the hand-written
"<field>_wrap" containers the live templates use.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 18: [D5.2] Delete the pool and linked-stat tags from `dots`

**Files:**
- Modify: `core/templatetags/dots.py` (CRLF; delete lines 119–339: blank lines 119–120, `_extract_pool_values` 121–144, `_render_pool_rows` 147–162, `pool` 165–199, `pool_rows` 202–230, `pool_dots` 233–258, `linked_stat_tag` 261–311, `linked_stat_row` 314–339)
- Delete: `core/templates/core/templatetags/linked_stat_row.html` (9 lines; the directory becomes empty and disappears)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: filters `pool`, `pool_dots`; tags `pool_rows`, `linked_stat`, `linked_stat_row`; helpers `_extract_pool_values`, `_render_pool_rows`. No template, Python caller or test uses any of them (report rows: 0/0/0).
- Keeps: filters `dots`, `boxes`, `abs`, `lore_name`, `linked_dots` (lines 1–118, byte-identical). `mark_safe` stays imported (used by `linked_dots`).

- [ ] **Step 1: Write the guard.** Append this method to `class D5RemovedTests`:

```python
    def test_dots_pool_and_linked_stat_tags_are_gone(self):
        from django.template import TemplateDoesNotExist
        from django.template.loader import get_template

        from core.templatetags import dots

        for name in ("pool", "pool_dots"):
            with self.subTest(filter=name):
                self.assertNotIn(name, dots.register.filters)
        for name in ("pool_rows", "linked_stat", "linked_stat_row"):
            with self.subTest(tag=name):
                self.assertNotIn(name, dots.register.tags)
        for name in (
            "pool",
            "pool_dots",
            "pool_rows",
            "linked_stat_tag",
            "linked_stat_row",
            "_extract_pool_values",
            "_render_pool_rows",
        ):
            with self.subTest(attribute=name):
                self.assertFalse(hasattr(dots, name))
        with self.assertRaises(TemplateDoesNotExist):
            get_template("core/templatetags/linked_stat_row.html")
        for name in ("dots", "boxes", "abs", "lore_name", "linked_dots"):
            with self.subTest(kept_filter=name):
                self.assertIn(name, dots.register.filters)
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests.test_dots_pool_and_linked_stat_tags_are_gone
```

Expected: `FAILED (failures=13)`: 2 `filter=` subtests, 3 `tag=` subtests, 7 `attribute=` subtests and the `TemplateDoesNotExist not raised` failure. No `kept_filter=` subtest fails.

- [ ] **Step 3: Delete, preserving CRLF.**

```bash
head -n 118 core/templatetags/dots.py > "$SCRATCH/dots.py" && mv "$SCRATCH/dots.py" core/templatetags/dots.py
file core/templatetags/dots.py              # must still end "with CRLF line terminators"
git diff --stat core/templatetags/dots.py   # must read: 1 file changed, 221 deletions(-)
git rm core/templates/core/templatetags/linked_stat_row.html
```

After the edit the file ends with the last line of `linked_dots` (lines 116–118):
```python
    return mark_safe(
        f'<span class="dots">{dots_str}</span><br><span class="dots">{boxes_str}</span>'
    )
```

- [ ] **Step 4: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests core.tests.templatetags core.tests.test_linked_stat core.tests.views.test_home
python manage.py check
grep -rnE "\|pool\b|\|pool_dots|\{% *(pool_rows|linked_stat|linked_stat_row)\b|_extract_pool_values|_render_pool_rows|linked_stat_row\.html" --include=*.py --include=*.html . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
```

Expected: tests `OK`; check clean; the grep prints nothing. (`core/widgets/linked_stat.py` mentions a `"pool_dots"` *mode string*; that module is deleted in D6.4 and is not a use of the filter.)

- [ ] **Step 5: Commit.**

```bash
git add core/templatetags/dots.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove unused pool and linked-stat tags from the dots library

pool, pool_dots, pool_rows, linked_stat and linked_stat_row had no
template use, no Python caller and no tests. Their helpers
_extract_pool_values/_render_pool_rows and the linked_stat_row.html
inclusion template go with them. dots.py keeps its CRLF line endings.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 19: [D5.3] Delete `json_filters.get_item`, `sanitize_text.badge_text` and `formset_tags.formset_remove_btn`

**Files:**
- Modify: `core/templatetags/json_filters.py` (delete lines 18–30: two blank lines and `get_item`)
- Modify: `core/templatetags/sanitize_text.py` (delete lines 169–184: two blank lines and `badge_text`)
- Modify: `widgets/templatetags/formset_tags.py` (delete lines 278–283: `formset_remove_btn` and the two blank lines after it)
- Modify (test): `core/tests/templatetags/test_json_filters.py` (line 5; delete lines 103–188 `GetItemFilterTest`)
- Modify (test): `core/tests/templatetags/test_sanitize_text.py` (line 6; delete lines 428–483 `BadgeTextFilterTest`)
- Modify (test): `widgets/tests/test_formset_manager.py` (line 13; delete lines 119–123 `test_formset_remove_btn`; delete lines 334–341 `test_formset_remove_btn_in_template`)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: filter `get_item`, filter `badge_text`, tag `formset_remove_btn` (0 template uses each; only their own tests import them).
- Keeps: `pprint`; `sanitize_html`, `quote_tag`, `safe_post`, `simple_markdown`, `render_post_html`; `formset`, `formset_script`, `formset_container`, `formset_add_btn`, `formset_form_wrapper`. The `{% formset %}` block tag still emits `data-formset-remove` itself (`FormsetNode`), so remove buttons keep working.

- [ ] **Step 1: Write the guard.** Append to `class D5RemovedTests`:

```python
    def test_unused_single_tags_and_filters_are_gone(self):
        from core.templatetags import json_filters, sanitize_text
        from widgets.templatetags import formset_tags

        cases = (
            (json_filters, json_filters.register.filters, "get_item"),
            (sanitize_text, sanitize_text.register.filters, "badge_text"),
            (formset_tags, formset_tags.register.tags, "formset_remove_btn"),
        )
        for module, registry, name in cases:
            with self.subTest(module=module.__name__, name=name):
                self.assertNotIn(name, registry)
                self.assertFalse(hasattr(module, name))
        self.assertIn("pprint", json_filters.register.filters)
        self.assertIn("formset_add_btn", formset_tags.register.tags)
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests.test_unused_single_tags_and_filters_are_gone
```

Expected: `FAILED (failures=3)`, one subtest each for `get_item`, `badge_text`, `formset_remove_btn`.

- [ ] **Step 3: Delete the code.**

`core/templatetags/json_filters.py`: delete lines 18–30, so the file ends at line 17 (`        return str(value)`). Removed block:
```python


@register.filter(name="get_item")
def get_item(dictionary, key):
    """Get an item from a dictionary by key.

    Usage: {{ mydict|get_item:key }}
    """
    if dictionary is None:
        return None
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
```

`core/templatetags/sanitize_text.py`: delete lines 169–184, so the file ends at line 168 (`    return mark_safe(result)`). Removed block:
```python


@register.filter
def badge_text(value):
    """
    Format text for display in badges.
    Replaces underscores with spaces and capitalizes each word.
    Example: 'autumn_person' -> 'Autumn Person'
    """
    if value is None or value == "":
        return ""

    if not isinstance(value, str):
        value = str(value)

    return value.replace("_", " ").title()
```

`widgets/templatetags/formset_tags.py`: delete lines 278–283:
```python
@register.simple_tag
def formset_remove_btn(prefix):
    """Return data attributes for a remove button (advanced use)."""
    return mark_safe(f'data-formset-remove="{prefix}"')


```
After it, `formset_add_btn` (ends line 275) is followed by two blank lines and `@register.simple_tag` / `def formset_form_wrapper():`.

- [ ] **Step 4: Delete the tests that exist only for them.**

`core/tests/templatetags/test_json_filters.py`: line 5 becomes
```python
from core.templatetags.json_filters import pprint
```
and delete lines 103–188 (two blank lines and all of `class GetItemFilterTest(TestCase):`), so the file ends at line 102 (`        self.assertIn("NonSerializable", result)`) with a single trailing newline.

`core/tests/templatetags/test_sanitize_text.py`: delete line 6 (`    badge_text,`) so the import reads
```python
from core.templatetags.sanitize_text import (
    quote_tag,
    safe_post,
    sanitize_html,
    simple_markdown,
)
```
and delete lines 428–483 (from `class BadgeTextFilterTest(TestCase):` up to, not including, `class SafePostFilterTest(TestCase):`).

`widgets/tests/test_formset_manager.py`:
- delete line 13 (`    formset_remove_btn,`) from the `widgets.templatetags.formset_tags` import;
- delete lines 119–123:
```python
    def test_formset_remove_btn(self):
        """Test formset_remove_btn returns correct attribute."""
        result = formset_remove_btn("my_prefix")
        self.assertIn('data-formset-remove="my_prefix"', result)

```
- delete lines 334–341 (the blank line before the method, and the method):
```python

    def test_formset_remove_btn_in_template(self):
        """Test formset_remove_btn tag works in template context."""
        template = Template(
            '{% load formset_tags %}<button {% formset_remove_btn "test" %}>Remove</button>'
        )
        result = template.render(Context({}))
        self.assertIn('data-formset-remove="test"', result)
```
`TestFormsetBlockTag.test_formset_block_tag_renders_remove_buttons` (line 238) stays: it covers the live `data-formset-remove` output of the `{% formset %}` tag.

- [ ] **Step 5: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests core.tests.templatetags widgets.tests.test_formset_manager game.tests
python manage.py check
grep -rnE "get_item\b|badge_text|formset_remove_btn" --include=*.py --include=*.html --include=*.js . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
```

Expected: tests `OK`; check clean; the grep prints nothing (method names such as `get_items`/`get_items_owned` do not match `get_item\b`).

- [ ] **Step 6: Commit.**

```bash
git add core/templatetags/json_filters.py core/templatetags/sanitize_text.py widgets/templatetags/formset_tags.py \
  core/tests/templatetags/test_json_filters.py core/tests/templatetags/test_sanitize_text.py \
  widgets/tests/test_formset_manager.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove unused get_item, badge_text and formset_remove_btn

None of the three is used by any template; only their own tests
imported them. render_post_html (used by game/consumers.py) and the
{% formset %} block tag's own remove-button markup are kept.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 20: [D5.4] Delete the `item_filters` and `location_tags` libraries and their leftover loads

**Files:**
- Delete: `items/templatetags/item_filters.py` (CRLF) and `items/templatetags/__init__.py` (CRLF, one comment line) — the package holds nothing else
- Delete (test): `items/tests/templatetags/test_item_filters.py` (14 tests) and `items/tests/templatetags/__init__.py` (empty)
- Delete: `locations/templatetags/location_tags.py` (the directory has no `__init__.py`; it becomes empty)
- Delete: `locations/templates/locations/location_recursive.html` (39 lines; reachable only through `show_location` and its own recursive include)
- Delete (test): `locations/tests/templatetags/test_location_tags.py` (6 tests) and `locations/tests/templatetags/__init__.py` (empty)
- Modify: `items/templates/items/index.html` (line 3), `locations/templates/locations/index.html` (line 4), `game/templates/game/chronicle/detail.html` (line 107)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: libraries `item_filters` (filter `replace_underscore`) and `location_tags` (inclusion tag `show_location`); template `locations/location_recursive.html`.
- The three pages keep rendering: none of them uses a tag from the removed libraries (report: 0 template uses).

- [ ] **Step 1: Write the guard.** Append to `class D5RemovedTests`:

```python
    def test_item_and_location_tag_libraries_are_gone(self):
        from django.template import TemplateDoesNotExist
        from django.template.loader import get_template

        self._assert_libraries_removed(
            ("item_filters", "location_tags"),
            ("items.templatetags.item_filters", "locations.templatetags.location_tags"),
        )
        with self.assertRaises(TemplateDoesNotExist):
            get_template("locations/location_recursive.html")

    def test_leftover_loads_are_removed_and_templates_compile(self):
        import re
        from pathlib import Path

        from django.conf import settings
        from django.template.loader import get_template

        leftover_loads = (
            ("items/templates/items/index.html", "items/index.html", "item_filters"),
            ("locations/templates/locations/index.html", "locations/index.html", "location_tags"),
            (
                "game/templates/game/chronicle/detail.html",
                "game/chronicle/detail.html",
                "location_tags",
            ),
        )
        base_dir = Path(settings.BASE_DIR)
        for relative_path, template_name, library in leftover_loads:
            with self.subTest(template=template_name, library=library):
                source = (base_dir / relative_path).read_text(encoding="utf-8")
                self.assertIsNone(re.search(r"{%\s*load\b[^%]*\b" + library + r"\b", source))
                get_template(template_name)
```

The `get_template` call is the regression half: a `{% load %}` of a missing library raises `TemplateSyntaxError` at compile time.

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests.test_item_and_location_tag_libraries_are_gone core.tests.test_dead_code_removed.D5RemovedTests.test_leftover_loads_are_removed_and_templates_compile
```

Expected: `FAILED (failures=8)`: 4 subtests in the first test (`library='item_filters'`, `library='location_tags'`, and the two `module=` subtests) plus its `TemplateDoesNotExist not raised`, and 3 subtests in the second (`<re.Match object ...> is not None` for each template).

- [ ] **Step 3: Delete the libraries, the template and their tests.**

```bash
git rm items/templatetags/item_filters.py items/templatetags/__init__.py \
  items/tests/templatetags/test_item_filters.py items/tests/templatetags/__init__.py \
  locations/templatetags/location_tags.py locations/templates/locations/location_recursive.html \
  locations/tests/templatetags/test_location_tags.py locations/tests/templatetags/__init__.py
rm -rf items/templatetags items/tests/templatetags locations/templatetags locations/tests/templatetags core/templates/core/templatetags
```

The `rm -rf` only removes untracked `__pycache__` leftovers so no namespace package lingers locally.

- [ ] **Step 4: Remove the three leftover `{% load %}` lines.**

`items/templates/items/index.html` lines 1–4, before:
```django
{% extends "core/base.html" %}
{% load field %}
{% load item_filters %}

```
after:
```django
{% extends "core/base.html" %}
{% load field %}

```

`locations/templates/locations/index.html` lines 1–5, before:
```django
{% extends "core/base.html" %}
{% load field %}
{% load sanitize_text %}
{% load location_tags %}

```
after:
```django
{% extends "core/base.html" %}
{% load field %}
{% load sanitize_text %}

```

`game/templates/game/chronicle/detail.html` lines 105–108, before:
```django
{% block content %}
    {% load sanitize_text %}
    {% load location_tags %}
    {% load field %}
```
after:
```django
{% block content %}
    {% load sanitize_text %}
    {% load field %}
```

- [ ] **Step 5: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D5RemovedTests items.tests locations.tests game.tests
python manage.py check
grep -rnE "item_filters|location_tags|replace_underscore|show_location|location_recursive" --include=*.py --include=*.html . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
```

Expected: tests `OK`; check clean; the grep prints nothing.

- [ ] **Step 6: Commit.**

```bash
git add items/templates/items/index.html locations/templates/locations/index.html \
  game/templates/game/chronicle/detail.html core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove item_filters and location_tags libraries and leftover loads

replace_underscore and show_location were never used; the three
{% load %} lines were leftovers. location_recursive.html was reachable
only through show_location. Test modules for both libraries go too.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**

```bash
python manage.py test                                   # serial, about 40 min
python manage.py check
python manage.py test core.tests.security.test_route_policies
python manage.py shell -v 0 -c 'from django.urls import URLResolver, get_resolver
def walk(r):
    return sum(walk(p) if isinstance(p, URLResolver) else 1 for p in r.url_patterns)
print(walk(get_resolver()))' | diff "$SCRATCH/routes_before.txt" - && echo ROUTES-UNCHANGED
python scripts/find_dead_code.py --section tags > "$SCRATCH/tags_after.md"
grep '^\*\*Summary' "$SCRATCH/tags_after.md"
grep -cE '\| (conditional_fields|resonance|item_filters|location_tags) \||\| dots \| (filter|tag) \| (pool|pool_dots|pool_rows|linked_stat|linked_stat_row) \||\| json_filters \| filter \| get_item \||\| sanitize_text \| filter \| badge_text \||\| formset_tags \| tag \| formset_remove_btn \|' "$SCRATCH/tags_before.md" "$SCRATCH/tags_after.md"
diff <(grep '^| ' "$SCRATCH/tags_before.md" | sed -E 's/\.py:[0-9]+/.py/') <(grep '^| ' "$SCRATCH/tags_after.md" | sed -E 's/\.py:[0-9]+/.py/') | grep '^>'
D5_PY="core/templatetags/dots.py core/templatetags/json_filters.py core/templatetags/sanitize_text.py widgets/templatetags/formset_tags.py widgets/mixins/conditional.py core/tests/templatetags/test_json_filters.py core/tests/templatetags/test_sanitize_text.py widgets/tests/test_formset_manager.py core/tests/test_dead_code_removed.py"
ruff check $D5_PY
ruff format --check $D5_PY
```

Required:
- Full suite: **0 failures, 0 errors** (the post-B0 baseline). The test count drops by exactly 33 against the pre-D5 run: 40 removed (9 `GetItemFilterTest`, 9 `BadgeTextFilterTest`, 2 `formset_remove_btn` cases, 14 `test_item_filters`, 6 `test_location_tags`; the resonance stub had none) and 7 `D5RemovedTests` added.
- `check` clean; route-policy test passes; `ROUTES-UNCHANGED` printed.
- Tag summary: `**Summary:** 10 project tag libraries, 1 not loaded by non-test code; 35 tags/filters, 13 unused in templates`. The `grep -c` prints `17` for `tags_before.md` and `0` for `tags_after.md` (4 library rows and 13 tag/filter rows gone). The 13 remaining unused rows are all `permissions` (deferred to Step 6).
- The final `diff | grep '^>'` prints exactly one line, the `sanitize_text` library row whose "Loaded in (files)" count dropped by one (127 → 126 at `1e77e23`, because `location_recursive.html` loaded it). Any other `>` line is a regression.
- ruff: the only finding is the pre-existing `core/templatetags/dots.py:91:10: UP038` inside the kept `linked_dots` (present at `1e77e23`, line 91 is unchanged); `ruff format --check` reports all 9 files formatted. Do not fix UP038 here (non-goal: refactoring kept code).

## Unit D6: Mixins, decorators and utilities

Design reference: `docs/superpowers/specs/2026-09-25-dead-code-removal-design.md` §2 (every **Delete (D6)** row) and §5 rows `core.linked_stat…/core/widgets/linked_stat.py/core.utils…` and `CreateOrSelectModelChoiceField, get_filterable_list_js, OptionMetadataSelectMultiple`; Rules 1–6 (rule 4: re-exports go with the class); Rollout #7. Appendix: `2026-09-25-dead-code-removal-report.md` → *symbols*.

**Preconditions.** D5 is merged. `core/tests/test_dead_code_removed.py` exists (Unit D4; if absent, create it with the header `from django.test import SimpleTestCase`).

**Line numbers** are at `1e77e23`, re-verified by applying every edit in a scratch worktree and comparing byte-for-byte. Two earlier units touch D6 files: **D3** removes `ChainedSelectMultiple`, `make_ajax_view` and `ChainedSelectAjaxView` from `widgets/__init__.py` and `ChainedSelectMultiple` from `widgets/widgets/__init__.py`; **D4** removes `AjaxLoginRequiredMixin`, `DropdownOptionsView`, `SimpleValuesView` and `JsonListView` from `core/mixins.py` (lines 555–668). So in those three files line numbers after the first D3/D4 hunk have moved: match on the quoted text, which is unique in each file. No D6 snippet overlaps a D3/D4 line.

**Keep (not touched by D6):** `core.context_processors.permissions` (Step 6); `core.mixins` `ViewPermissionMixin`, `EditPermissionMixin`, `SpendFreebiesPermissionMixin`, `OwnerRequiredMixin`, `StorytellerRequiredMixin`, `XPApprovalMixin`, `ApprovalMixin`, `MessageMixin`; `core.cache.cache_function`, `get_cached_reference_list`, `CacheKeyGenerator`, `CacheInvalidator`, the `CACHE_TIMEOUT_*` constants; `core.linked_stat.LinkedStat`/`LinkedStatAccessor`/`linked_stat_fields`/`linked_stat_constraints`; `core.widgets.AutocompleteTextInput`; `core.utils.get_gameline_name` and the rest of `core/utils.py`; `widgets.CreateOrSelectField`, `OptionMetadataSelect`, `render_filterable_list_script`, `FILTERABLE_LIST_JS`.

**Whole-module deadness, verified at `1e77e23`:**
- `core/decorators.py` — `grep -rn "core.decorators\|from core import decorators"` finds only `core/tests/test_decorators.py` and a stale README example (`from core.decorators import require_storyteller`, a function that never existed). All six functions including `require_permission` go, so the module is deleted.
- `core/middleware/cache_middleware.py` — its only symbol is `PerUserCacheMiddleware`; not in `MIDDLEWARE` (`tg/settings/base.py:44-55`), not exported by `core/middleware/__init__.py`. Module deleted.
- `core/widgets/linked_stat.py` — `LinkedStatWidget`, `LinkedStatFormField`, `DotsBoxesWidget`, `PoolWidget` are imported only by `core/widgets/__init__.py`; no form, template or test uses them (`PointPoolWidget` hits are the unrelated `widgets` app). Module deleted; `AutocompleteTextInput` stays the package's only export.
- `core.utils.fast_selector`, `level_name`, `tree_sort`, `compute_level` — no user in Python, templates, `populate_db/` or JS; `level_name`/`tree_sort` are only re-exported by `locations/views/core/__init__.py:6` and its `__all__` (lines 240–241); `compute_level` is only called by `level_name` and itself. No test covers them.

### Task 21: [D6.0] Record the baselines

**Files:** none changed.

**Interfaces:** none.

- [ ] **Step 1: Save the symbol report and the route count.**

```bash
export SCRATCH=${SCRATCH:-$(mktemp -d)}
python scripts/find_dead_code.py --section symbols > "$SCRATCH/symbols_before.md"
grep '^\*\*Summary' "$SCRATCH/symbols_before.md"
python manage.py shell -v 0 -c 'from django.urls import URLResolver, get_resolver
def walk(r):
    return sum(walk(p) if isinstance(p, URLResolver) else 1 for p in r.url_patterns)
print(walk(get_resolver()))' > "$SCRATCH/routes_before_d6.txt"
```

The summary numbers depend on what D3/D4/D7-prep removed; the gate compares row sets, not totals.

### Task 22: [D6.1] Delete the unused permission and message mixins

**Files:**
- Modify: `core/mixins.py` — delete `SpendXPPermissionMixin` (lines 118–127 incl. the two blank lines after it), `STRequiredMixin` (248–268), `DeleteMessageMixin` (436–464), `FreebieApprovalMixin` (781–807: the two blank lines before it and the class; the file then ends with `        return XPSpendingRequest`)
- Modify: `core/views/character_template.py` — line 5 import; delete `STRequiredMixin` (lines 34–64 incl. the two blank lines after it)
- Modify (test): `core/tests/mixins/test_mixins.py` — line 11 import; lines 16, 25, 27 of the `core.mixins` import; delete `ObjectCachingMixinTest.test_st_required_mixin_caches_object` (138–167), `SpendXPPermissionMixinTest` (388–433), `STRequiredMixinTest` (950–1040), `DeleteMessageMixinTest` (1470–1541)
- Modify (test): `core/tests/permissions/test_permissions_deployment.py` — lines 19–20 import; delete `test_spend_xp_mixin_exists` (392–395) and `test_st_required_mixin_exists` (409–412)
- Modify (test): `core/tests/views/test_character_template.py` — lines 6–7 imports; lines 13–16 import; delete `STRequiredMixinTest` (22–101)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: `core.mixins.SpendXPPermissionMixin`, `core.mixins.STRequiredMixin` (referenced the nonexistent `chronicle.head_storytellers`), `core.mixins.DeleteMessageMixin` (overrode `delete()`, which Django's `DeleteView` no longer calls on POST), `core.mixins.FreebieApprovalMixin` (no users, no tests), `core.views.character_template.STRequiredMixin` (unused since Step 0, `446eee3`). No package `__init__` re-exports any of them (`core/views/__init__.py` imports only the eight `CharacterTemplate*View` classes).
- Consumers: none outside the tests listed. Access for the template views is enforced by the Step 0 manifest (`core/route_policy_manifest.py`) and `PermissionManager.can_manage_scope` inside the views; nothing changes there.

- [ ] **Step 1: Write the guard.** Append to the end of `core/tests/test_dead_code_removed.py`:

```python
class D6RemovedTests(SimpleTestCase):
    """Unit D6: dead mixins, decorators, middleware, cache helpers and utilities stay deleted."""

    @staticmethod
    def _module_exists(dotted_path):
        """Return True when ``dotted_path`` can be imported (parents included)."""
        import importlib.util

        try:
            return importlib.util.find_spec(dotted_path) is not None
        except ModuleNotFoundError:
            return False

    def test_dead_core_mixins_are_gone(self):
        import core.mixins

        for name in (
            "STRequiredMixin",
            "SpendXPPermissionMixin",
            "DeleteMessageMixin",
            "FreebieApprovalMixin",
        ):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.mixins, name))
        for name in ("SpendFreebiesPermissionMixin", "XPApprovalMixin", "MessageMixin"):
            with self.subTest(kept=name):
                self.assertTrue(hasattr(core.mixins, name))

    def test_character_template_st_mixin_is_gone(self):
        from core.views import character_template

        self.assertFalse(hasattr(character_template, "STRequiredMixin"))

    def test_kept_step6_context_processor_survives(self):
        from core import context_processors

        self.assertTrue(callable(context_processors.permissions))
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests
```

Expected: `FAILED (failures=5)`: four `name=` subtests of `test_dead_core_mixins_are_gone` and `test_character_template_st_mixin_is_gone`. `test_kept_step6_context_processor_survives` passes.

- [ ] **Step 3: Delete the mixins from `core/mixins.py`.** Remove each block below together with the two blank lines that follow it (for `FreebieApprovalMixin`, the two blank lines that precede it), so the neighbouring classes stay separated by exactly two blank lines.

```python
class SpendXPPermissionMixin(PermissionRequiredMixin):
    """
    Require XP spending permission for CBV.
    Raises 403 if user cannot spend XP.
    """

    required_permission = Permission.SPEND_XP
    raise_404_on_deny = False
```
(now `EditPermissionMixin` is followed directly by `class SpendFreebiesPermissionMixin(PermissionRequiredMixin):`)

```python
class STRequiredMixin(ObjectCachingMixin):
    """
    Mixin that restricts access to chronicle STs and admins only.
    ...
        raise PermissionDenied("Only storytellers can perform this action")
```
(lines 248–266; now `OwnerRequiredMixin` is followed by `class SpecialUserMixin:`)

```python
class DeleteMessageMixin:
    """
    Mixin to add a success message when an object is deleted.
    ...
        return super().delete(request, *args, **kwargs)
```
(lines 436–462; now `MessageMixin` is followed by `class StorytellerRequiredMixin:`)

```python
class FreebieApprovalMixin(ApprovalMixin):
    """
    Mixin for handling freebie spending request approval and denial.
    ...
        return FreebieSpendingRecord
```
(lines 783–807, the end of the file). All imports stay used (`messages` by `SuccessMessageMixin`/`ErrorMessageMixin`, `PermissionDenied` by `OwnerRequiredMixin`, `PermissionManager`/`Permission` by `PermissionRequiredMixin`); `ruff check` confirms.

- [ ] **Step 4: Delete `STRequiredMixin` from `core/views/character_template.py`.**

Line 5, before → after:
```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
```
```python
from django.contrib.auth.mixins import LoginRequiredMixin
```
Delete lines 34–64, from `class STRequiredMixin(UserPassesTestMixin):` up to, not including, `class CharacterTemplateListView(LoginRequiredMixin, ListView):`. `messages`, `redirect` and `PermissionManager` stay (used by the import and quick-NPC views).

- [ ] **Step 5: Delete the tests that exist only for these classes.**

`core/tests/mixins/test_mixins.py`:
- line 11 becomes `from django.views.generic import DetailView, ListView, UpdateView` (`DeleteView` was used only by `DeleteMessageMixinTest`);
- in the `from core.mixins import (...)` block delete the lines `    DeleteMessageMixin,` (16), `    SpendXPPermissionMixin,` (25) and `    STRequiredMixin,` (27);
- delete lines 138–167: the method `test_st_required_mixin_caches_object` in `ObjectCachingMixinTest` and its trailing blank line (the next line is `    def test_character_owner_or_st_mixin_caches_object(self):`). This case is not listed in the design's test column but exists only for the deleted mixin; `test_permission_mixin_caches_object` and `test_character_owner_or_st_mixin_caches_object` keep `ObjectCachingMixin` covered;
- delete lines 388–433 (from `class SpendXPPermissionMixinTest(TestCase):` up to, not including, `class SpendFreebiesPermissionMixinTest(TestCase):`);
- delete lines 950–1040 (from `class STRequiredMixinTest(TestCase):` up to, not including, `class StorytellerRequiredMixinTest(TestCase):`);
- delete lines 1470–1541 (from `class DeleteMessageMixinTest(TestCase):` up to, not including, `class ApprovalMixinTest(TestCase):`).
`get_messages`, `FallbackStorage` and `PermissionDenied` stay imported (used by `ErrorMessageMixinTest`, `ApprovalMixinTest` and others).

`core/tests/permissions/test_permissions_deployment.py`:
- delete lines 19–20 (`    SpendXPPermissionMixin,`, `    STRequiredMixin,`) from the `core.mixins` import;
- delete lines 392–395:
```python
    def test_spend_xp_mixin_exists(self):
        """SpendXPPermissionMixin exists and has correct permission."""
        self.assertEqual(SpendXPPermissionMixin.required_permission, Permission.SPEND_XP)

```
- delete lines 409–412 (the blank line and the last method of the file), so the file ends with `        self.assertTrue(hasattr(OwnerRequiredMixin, "dispatch"))`:
```python

    def test_st_required_mixin_exists(self):
        """STRequiredMixin exists."""
        self.assertTrue(hasattr(STRequiredMixin, "dispatch"))
```
The module docstring's "Expected: 37 tests passing" was stale (39 at `1e77e23`) and is correct again afterwards; leave it.

`core/tests/views/test_character_template.py`:
- delete lines 6–7 (`from django.contrib.messages import get_messages`, `from django.contrib.messages.storage.fallback import FallbackStorage`; only `STRequiredMixinTest` used them);
- lines 13–16 become `from core.views.character_template import CharacterTemplateQuickNPCView`;
- delete lines 22–101 (from `class STRequiredMixinTest(TestCase):` up to, not including, `class CharacterTemplateListViewTest(TestCase):`).

- [ ] **Step 6: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests core.tests.mixins core.tests.permissions core.tests.views.test_character_template
python manage.py check
grep -rnE "\b(STRequiredMixin|SpendXPPermissionMixin|DeleteMessageMixin|FreebieApprovalMixin)\b" --include=*.py --include=*.html . | grep -v "core/tests/test_dead_code_removed.py"
ruff check core/mixins.py core/views/character_template.py core/tests/mixins/test_mixins.py core/tests/permissions/test_permissions_deployment.py core/tests/views/test_character_template.py
```

Expected: tests `OK`; check clean; the grep prints nothing (`CLAUDE.md` and `.claude/skills/tg-standards/references/*.md` still name `STRequiredMixin`/`SpendXPPermissionMixin`; see Notes — they are `.md`, so not matched here); ruff reports only the two pre-existing `F841` in `core/tests/mixins/test_mixins.py` (`response` assigned but unused in `OwnerRequiredMixinTest.test_owner_via_user_attribute` and `ErrorMessageMixinTest.test_form_invalid_shows_error_message`; lines 677 and 1453 at `1e77e23`, 598 and 1283 after D6.1).

- [ ] **Step 7: Commit.**

```bash
git add core/mixins.py core/views/character_template.py core/tests/mixins/test_mixins.py \
  core/tests/permissions/test_permissions_deployment.py core/tests/views/test_character_template.py \
  core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove unused permission and message mixins

core.mixins.STRequiredMixin, SpendXPPermissionMixin, DeleteMessageMixin
and FreebieApprovalMixin had no users, and the character-template
STRequiredMixin has been unused since Step 0 moved access control to
the route manifest. DeleteMessageMixin overrode delete(), which
DeleteView no longer calls on POST. Their tests go with them.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 23: [D6.2] Delete `core/decorators.py` and `PerUserCacheMiddleware`

**Files:**
- Delete: `core/decorators.py` (136 lines: `require_permission`, `require_view_permission`, `require_edit_permission`, `require_spend_xp_permission`, `require_spend_freebies_permission`, `require_model_permission`)
- Delete (test): `core/tests/test_decorators.py` (473 lines, 6 classes, 25 tests)
- Delete: `core/middleware/cache_middleware.py` (67 lines, `PerUserCacheMiddleware` only)
- Delete (test): `core/tests/middleware/test_cache_middleware.py` (180 lines, 14 tests)
- Modify: `core/README.md` (lines 10, 34–36, 60, 110–115)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: module `core.decorators`, module `core.middleware.cache_middleware`. `core/middleware/__init__.py` (exports only `UserListMiddleware`) is unchanged; `MIDDLEWARE` is unchanged.

- [ ] **Step 1: Write the guard.** Append to `class D6RemovedTests`:

```python
    def test_decorators_and_cache_middleware_modules_are_gone(self):
        from django.conf import settings

        for dotted_path in ("core.decorators", "core.middleware.cache_middleware"):
            with self.subTest(module=dotted_path):
                self.assertFalse(self._module_exists(dotted_path))
        self.assertNotIn(
            "core.middleware.cache_middleware.PerUserCacheMiddleware", settings.MIDDLEWARE
        )
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests.test_decorators_and_cache_middleware_modules_are_gone
```

Expected: `FAILED (failures=2)` (`module='core.decorators'`, `module='core.middleware.cache_middleware'`).

- [ ] **Step 3: Delete the modules and their tests.**

```bash
git rm core/decorators.py core/tests/test_decorators.py \
  core/middleware/cache_middleware.py core/tests/middleware/test_cache_middleware.py
```

- [ ] **Step 4: Drop the decorator references from `core/README.md`.**

Line 10: `- Permission systems and decorators` → `- Permission system`.

Delete lines 34–36:
```markdown
### Decorators (`decorators.py`)
Custom decorators for views, including permission checks.

```

Delete line 60 (`├── decorators.py               # Custom decorators`) from the directory tree.

Lines 108–122, before:
```python
from core.permissions import user_can_edit_object
from core.decorators import require_storyteller

@require_storyteller
def storyteller_only_view(request):
    # Only accessible to storytellers
    pass

def edit_view(request, pk):
```
after:
```python
from core.permissions import user_can_edit_object

def edit_view(request, pk):
```
(The remaining example's `user_can_edit_object` is also stale; that is outside D6, see Notes.)

- [ ] **Step 5: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests core.tests.middleware
python manage.py check
grep -rnE "core\.decorators|require_(permission|view_permission|edit_permission|spend_xp_permission|spend_freebies_permission|model_permission)\b|PerUserCacheMiddleware|cache_middleware" --include=*.py --include=*.md --include=*.html . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
```

Expected: tests `OK`; check clean; the grep prints nothing (`require_spending_approver` in `game/` does not match).

- [ ] **Step 6: Commit.**

```bash
git add core/README.md core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove core.decorators and the unregistered PerUserCacheMiddleware

The require_* decorators had no importer outside their tests (there are
no function-based object views; the route manifest enforces access).
PerUserCacheMiddleware was never in MIDDLEWARE. Both modules and their
test modules are deleted, and the README stops advertising decorators.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 24: [D6.3] Delete the unused queryset cache helpers

**Files:**
- Modify: `core/cache.py` — docstring lines 7 and 9; imports lines 17–19; delete `cache_queryset` (127–175), `invalidate_cache_on_save` (225–257), `# Example usage functions` + `get_cached_queryset` (266–302); docstring line 180; docstring lines 312–318; comment lines 352–353
- Modify (test): `core/tests/test_cache.py` — import lines 18, 19, 21; delete `CacheQuerysetDecoratorTest` (172–264); delete `InvalidateCacheOnSaveDecoratorTest` and `GetCachedQuerysetTest` (355–434)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: `core.cache.cache_queryset`, `core.cache.get_cached_queryset`, `core.cache.invalidate_cache_on_save`.
- Keeps (live users): `cache_function` + `CACHE_TIMEOUT_MEDIUM` (`characters/views/core/character.py:11`), `get_cached_reference_list` (`characters/forms/core/chained_freebies.py:17`), `CACHE_TIMEOUT_LONG` (`core/views/generic.py:9`), `CacheKeyGenerator` (including `make_model_key`, now used only by tests), `CacheInvalidator` (still clears both `queryset` and `reference_list` key categories).

- [ ] **Step 1: Write the guard.** Append to `class D6RemovedTests`:

```python
    def test_dead_cache_helpers_are_gone(self):
        import core.cache

        for name in ("cache_queryset", "get_cached_queryset", "invalidate_cache_on_save"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.cache, name))
        self.assertTrue(callable(core.cache.cache_function))
        self.assertTrue(callable(core.cache.get_cached_reference_list))
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests.test_dead_cache_helpers_are_gone
```

Expected: `FAILED (failures=3)`, one subtest per helper.

- [ ] **Step 3: Edit `core/cache.py`.**

Module docstring, lines 6–9, before → after:
```
- Cache key generation utilities
- Queryset caching decorators
- Cache invalidation helpers
- Model-based cache invalidation hooks
```
```
- Cache key generation utilities
- A function-result caching decorator
- Cache invalidation helpers
- A cached reference-list helper
```

Imports, lines 16–19, before → after (`QuerySet`, the signals and `receiver` were used only by the deleted helpers):
```python
from django.core.cache import cache
from django.db.models import Model, QuerySet
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
```
```python
from django.core.cache import cache
from django.db.models import Model
```

Delete, each with the two blank lines that follow it:
- `def cache_queryset(timeout: int = 300, key_prefix: str = "") -> Callable:` through its `    return decorator` (lines 127–173);
- `def invalidate_cache_on_save(*models: type[Model]) -> Callable:` through its `    return decorator` (lines 225–255);
- the comment `# Example usage functions` and `def get_cached_queryset(` through `    return queryset` (lines 266–300).

In `cache_function`'s docstring, line 180, before → after:
```
    Similar to cache_queryset but works with any function return type.
```
```
    Works with any function return type.
```

In `get_cached_reference_list`'s docstring, lines 312–318, before:
```
    Unlike get_cached_queryset, this evaluates the queryset immediately and
    caches the resulting list. This is useful for forms that iterate over
    reference data multiple times, as it avoids repeated database queries.

    This function is designed for small reference tables (typically <100 records)
    like Attributes, Abilities, Backgrounds, etc. For larger datasets, consider
    using get_cached_queryset() instead to avoid high memory usage.
```
after:
```
    The queryset is evaluated immediately and the resulting list is cached.
    This is useful for forms that iterate over reference data multiple times,
    as it avoids repeated database queries.

    This function is designed for small reference tables (typically <100 records)
    like Attributes, Abilities, Backgrounds, etc. Avoid it for large tables,
    because the whole list is held in the cache.
```

Lines 352–353, before → after:
```python
    # Use "reference_list" category instead of "queryset" to avoid cache key collisions
    # with get_cached_queryset, which caches QuerySets rather than evaluated lists
```
```python
    # "reference_list" keys are cleared by CacheInvalidator.invalidate_model_cache()
```

- [ ] **Step 4: Edit `core/tests/test_cache.py`.**

The `from core.cache import (...)` block (lines 9–22) becomes:
```python
from core.cache import (
    CACHE_TIMEOUT_DAY,
    CACHE_TIMEOUT_LONG,
    CACHE_TIMEOUT_MEDIUM,
    CACHE_TIMEOUT_SHORT,
    CACHE_TIMEOUT_VERY_LONG,
    CacheInvalidator,
    CacheKeyGenerator,
    cache_function,
    get_cached_reference_list,
)
```
Delete lines 172–264 (from `class CacheQuerysetDecoratorTest(TestCase):` up to, not including, `class CacheFunctionDecoratorTest(TestCase):`) and lines 355–434 (from `class InvalidateCacheOnSaveDecoratorTest(TestCase):` through the end of `GetCachedQuerysetTest`, up to, not including, `class GetCachedReferenceListTest(TestCase):`). `GetCachedReferenceListTest.test_cache_invalidation_clears_reference_list` keeps the invalidation path covered.

- [ ] **Step 5: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests core.tests.test_cache characters.tests.forms
python manage.py check
grep -rnE "cache_queryset|get_cached_queryset|invalidate_cache_on_save" --include=*.py --include=*.md . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
ruff check core/cache.py core/tests/test_cache.py
```

Expected: tests `OK`; check clean; grep prints nothing; `ruff check` clean (the unused-import findings the deletions would otherwise leave are handled in Step 3; the five pre-existing findings in `test_cache.py` at `1e77e23` all sat inside the deleted classes).

- [ ] **Step 6: Commit.**

```bash
git add core/cache.py core/tests/test_cache.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove unused queryset cache helpers

cache_queryset, get_cached_queryset and invalidate_cache_on_save were
used only by their tests. The live helpers cache_function and
get_cached_reference_list stay; docstrings no longer point at the
deleted functions.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 25: [D6.4] Delete the linked-stat aliases and widgets and the tree utilities

**Files:**
- Modify: `core/linked_stat.py` (delete lines 501–521: two blank lines, the `# Convenience aliases…` comment, `MaxCurrentStat`, `PermanentTemporaryStat`; the file ends with `    return constraints`)
- Delete: `core/widgets/linked_stat.py` (442 lines)
- Modify: `core/widgets/__init__.py` (whole file, 15 lines)
- Modify: `core/utils.py` (delete lines 47–65 `compute_level`/`level_name`/`tree_sort`; delete lines 111–118 `fast_selector`)
- Modify: `locations/views/core/__init__.py` (line 6; `__all__` lines 240–241)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: `core.linked_stat.MaxCurrentStat`, `PermanentTemporaryStat`; module `core.widgets.linked_stat` (`LinkedStatWidget`, `LinkedStatFormField`, `DotsBoxesWidget`, `PoolWidget`) and their `core.widgets` re-exports; `core.utils.fast_selector`, `level_name`, `tree_sort`, `compute_level` and the `locations.views.core` re-exports of `level_name`/`tree_sort`.
- Keeps: `core.widgets.AutocompleteTextInput` (imported by 9 non-test modules and 1 test as `from core.widgets import AutocompleteTextInput`); `core.utils.random` import (still used by `weighted_choice` and `dice`).

- [ ] **Step 1: Write the guard.** Append to `class D6RemovedTests`:

```python
    def test_linked_stat_aliases_and_widgets_are_gone(self):
        import core.linked_stat
        import core.widgets

        for name in ("MaxCurrentStat", "PermanentTemporaryStat"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.linked_stat, name))
        self.assertFalse(self._module_exists("core.widgets.linked_stat"))
        self.assertEqual(core.widgets.__all__, ["AutocompleteTextInput"])
        for name in ("DotsBoxesWidget", "LinkedStatFormField", "LinkedStatWidget", "PoolWidget"):
            with self.subTest(name=name):
                self.assertFalse(hasattr(core.widgets, name))

    def test_dead_utils_and_reexports_are_gone(self):
        import core.utils
        import locations.views.core

        for name in ("fast_selector", "level_name", "tree_sort", "compute_level"):
            with self.subTest(module="core.utils", name=name):
                self.assertFalse(hasattr(core.utils, name))
        for name in ("level_name", "tree_sort"):
            with self.subTest(module="locations.views.core", name=name):
                self.assertFalse(hasattr(locations.views.core, name))
                self.assertNotIn(name, locations.views.core.__all__)
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests.test_linked_stat_aliases_and_widgets_are_gone core.tests.test_dead_code_removed.D6RemovedTests.test_dead_utils_and_reexports_are_gone
```

Expected: `FAILED (failures=9)`: `MaxCurrentStat`, `PermanentTemporaryStat` and the `_module_exists` assertion (it stops the first test; the `__all__` and widget-name checks run after the fix), plus 4 `core.utils` subtests and 2 `locations.views.core` subtests.

- [ ] **Step 3: Delete and edit.**

```bash
git rm core/widgets/linked_stat.py
```

`core/widgets/__init__.py`, whole file before:
```python
from .autocomplete import AutocompleteTextInput
from .linked_stat import (
    DotsBoxesWidget,
    LinkedStatFormField,
    LinkedStatWidget,
    PoolWidget,
)

__all__ = [
    "AutocompleteTextInput",
    "DotsBoxesWidget",
    "LinkedStatFormField",
    "LinkedStatWidget",
    "PoolWidget",
]
```
after:
```python
from .autocomplete import AutocompleteTextInput

__all__ = [
    "AutocompleteTextInput",
]
```

`core/linked_stat.py`: delete lines 501–521 (two blank lines and):
```python
# Convenience aliases for different naming conventions
class MaxCurrentStat(LinkedStat):
    """
    LinkedStat variant for max/current naming (e.g., max_blood_pool/blood_pool).

    The "permanent" value is the max, and "temporary" is current.
    """

    pass


class PermanentTemporaryStat(LinkedStat):
    """
    LinkedStat variant for permanent/temporary naming (standard WoD pattern).

    This is identical to LinkedStat but makes the naming convention explicit.
    """

    pass
```

`core/utils.py`: delete lines 47–65 (each function and the two blank lines after it; `dice` is then followed by `def filepath(instance, filename):`):
```python
def compute_level(x, level=0):
    if x.parent is None:
        return level
    return compute_level(x.parent, level=level + 1)


def level_name(x):
    return (compute_level(x) * "&emsp;&emsp;") + x.name


def tree_sort(x, l=None):
    if l is None:
        l = []
    l.append(x)
    for y in x.children.order_by("name"):
        tree_sort(y, l=l)
    return l
```
and lines 111–118 (`get_short_gameline_name` is then followed by `def display_queryset(prop):`):
```python
def fast_selector(cls):
    max_value = cls.objects.last().id
    index = random.randint(1, max_value)
    while not cls.objects.filter(pk=index).exists():
        index = random.randint(1, max_value)
    return cls.objects.get(pk=index)
```

`locations/views/core/__init__.py` line 6, before → after:
```python
from core.utils import get_gameline_name, level_name, tree_sort
```
```python
from core.utils import get_gameline_name
```
and in `__all__` delete lines 240–241 (`    "level_name",`, `    "tree_sort",`), so `"get_gameline_name",` is followed by `"DictView",`.

- [ ] **Step 4: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests core.tests.test_linked_stat core.tests.widgets locations.tests.views
python manage.py check
grep -rnE "\b(MaxCurrentStat|PermanentTemporaryStat|LinkedStatWidget|LinkedStatFormField|DotsBoxesWidget|PoolWidget|fast_selector|level_name|tree_sort|compute_level)\b|widgets\.linked_stat|widgets/linked_stat" --include=*.py --include=*.html --include=*.js . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
ruff check core/linked_stat.py core/utils.py core/widgets/__init__.py locations/views/core/__init__.py
```

Expected: tests `OK`; check clean; the grep prints nothing (`PointPoolWidget` does not match `\bPoolWidget\b`); ruff reports only the pre-existing `core/utils.py:26:5: E741 Ambiguous variable name: l` in the kept `weighted_choice` (the other two E741 at `1e77e23` were in `tree_sort` and are gone).

- [ ] **Step 5: Commit.**

```bash
git add core/linked_stat.py core/widgets/__init__.py core/utils.py locations/views/core/__init__.py \
  core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove linked-stat aliases, linked-stat widgets and tree utilities

MaxCurrentStat/PermanentTemporaryStat and core/widgets/linked_stat.py
had no users. core.utils fast_selector, level_name, tree_sort and
compute_level had none either; level_name and tree_sort were only
re-exported by locations.views.core, and that re-export goes too.
core.widgets now exports only AutocompleteTextInput.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 26: [D6.5] Delete the unused `widgets` field, JS getter and multi-select widget

**Files:**
- Modify: `widgets/fields/create_or_select.py` (delete lines 74–94; the file ends with `        return bool(value)`)
- Modify: `widgets/widgets/filterable.py` (delete lines 419–423, `get_filterable_list_js` and the two blank lines after it)
- Modify: `widgets/widgets/metadata_select.py` (delete lines 256–261, `OptionMetadataSelectMultiple` and the two blank lines after it)
- Modify: `widgets/__init__.py` (lines 78, 88, 89; `__all__` lines 98, 106, 119)
- Modify: `widgets/widgets/__init__.py` (lines 10, 18)
- Modify (test): `widgets/tests/test_create_or_select.py` (lines 6, 12, 17–28, 137–157, 252, 259)
- Modify (test): `widgets/tests/test_metadata_select.py` (lines 8, 85–93, 228, 231)
- Modify (test): `widgets/tests/test_filterable_list.py` (lines 11, 17–19, 33, 60, 67, 121–124, 128–133)
- Modify (test): `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: `widgets.CreateOrSelectModelChoiceField` (`widgets.fields.create_or_select`), `widgets.get_filterable_list_js` (`widgets.widgets.filterable`), `widgets.OptionMetadataSelectMultiple` and `widgets.widgets.OptionMetadataSelectMultiple` (`widgets.widgets.metadata_select`). Only tests used them.
- Tests move to the live APIs: the JS assertions read the module constant `widgets.widgets.filterable.FILTERABLE_LIST_JS` (which `get_filterable_list_js` merely returned, and which `render_filterable_list_script` embeds); the create-or-select and metadata tests keep covering `CreateOrSelectField`/`CreateOrSelectWidget`/`CreateOrSelectMixin` and `OptionMetadataSelect`.

- [ ] **Step 1: Write the guard.** Append to `class D6RemovedTests`:

```python
    def test_dead_widgets_leftovers_are_gone(self):
        import widgets
        import widgets.widgets
        from widgets.fields import create_or_select
        from widgets.widgets import filterable, metadata_select

        gone = (
            (widgets, "CreateOrSelectModelChoiceField"),
            (widgets, "get_filterable_list_js"),
            (widgets, "OptionMetadataSelectMultiple"),
            (widgets.widgets, "OptionMetadataSelectMultiple"),
            (create_or_select, "CreateOrSelectModelChoiceField"),
            (filterable, "get_filterable_list_js"),
            (metadata_select, "OptionMetadataSelectMultiple"),
        )
        for module, name in gone:
            with self.subTest(module=module.__name__, name=name):
                self.assertFalse(hasattr(module, name))
                self.assertNotIn(name, getattr(module, "__all__", ()))
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests.test_dead_widgets_leftovers_are_gone
```

Expected: `FAILED (failures=7)`, one subtest per `(module, name)` pair.

- [ ] **Step 3: Delete the code.**

`widgets/fields/create_or_select.py`: delete lines 74–94 (two blank lines and):
```python
class CreateOrSelectModelChoiceField(forms.ModelChoiceField):
    """
    A ModelChoiceField variant designed to work with CreateOrSelectField.

    Provides automatic required validation based on the toggle state.
    """

    def __init__(self, queryset, *, toggle_field="select_or_create", **kwargs):
        ...
        super().__init__(queryset, **kwargs)
```
(`forms` stays imported; `CreateOrSelectField` extends `forms.BooleanField`.)

`widgets/widgets/filterable.py`: delete lines 419–423:
```python
def get_filterable_list_js():
    """Return the FilterableList JavaScript code."""
    return FILTERABLE_LIST_JS


```

`widgets/widgets/metadata_select.py`: delete lines 256–261:
```python
class OptionMetadataSelectMultiple(OptionMetadataSelect, forms.SelectMultiple):
    """Multiple-select variant of OptionMetadataSelect."""

    pass


```

`widgets/__init__.py` (match on text; D3 has already removed its own lines here):
```python
from .fields.create_or_select import CreateOrSelectField, CreateOrSelectModelChoiceField
```
→ `from .fields.create_or_select import CreateOrSelectField`
```python
from .widgets.filterable import get_filterable_list_js, render_filterable_list_script
```
→ `from .widgets.filterable import render_filterable_list_script`
```python
from .widgets.metadata_select import OptionMetadataSelect, OptionMetadataSelectMultiple
```
→ `from .widgets.metadata_select import OptionMetadataSelect`
and in `__all__` delete the three lines `    "OptionMetadataSelectMultiple",`, `    "CreateOrSelectModelChoiceField",` and `    "get_filterable_list_js",`.

`widgets/widgets/__init__.py` line 10:
```python
from .metadata_select import OptionMetadataSelect, OptionMetadataSelectMultiple
```
→ `from .metadata_select import OptionMetadataSelect`; delete line 18 (`    "OptionMetadataSelectMultiple",`).

- [ ] **Step 4: Adjust the tests.**

`widgets/tests/test_create_or_select.py`, lines 5–29 before:
```python
from django import forms
from django.db import models
from django.test import TestCase

from widgets import (
    CreateOrSelectField,
    CreateOrSelectMixin,
    CreateOrSelectModelChoiceField,
    CreateOrSelectWidget,
)


# Test model for ModelChoiceField tests
class TestItem(models.Model):
    """Test model for create-or-select tests."""

    name = models.CharField(max_length=100)
    value = models.IntegerField(default=0)

    class Meta:
        app_label = "widgets"
        managed = False  # Don't create table


class TestCreateOrSelectWidget(TestCase):
```
after (`TestItem` was used only by the deleted class):
```python
from django import forms
from django.test import TestCase

from widgets import (
    CreateOrSelectField,
    CreateOrSelectMixin,
    CreateOrSelectWidget,
)


class TestCreateOrSelectWidget(TestCase):
```
Delete lines 137–157 (from `class TestCreateOrSelectModelChoiceField(TestCase):` up to, not including, `class TestCreateOrSelectMixin(TestCase):`). In `TestWidgetsCreateOrSelectImports.test_all_exports_available` delete line 252 (`            CreateOrSelectModelChoiceField,`) and line 259 (`        self.assertIsNotNone(CreateOrSelectModelChoiceField)`).

`widgets/tests/test_metadata_select.py`: line 8 → `from widgets import OptionMetadataSelect`; delete lines 85–93 (from `class TestOptionMetadataSelectMultiple(TestCase):` up to, not including, `class TestNormalizeChoicesWithMetadata(TestCase):`); in `TestImports.test_option_metadata_exports` line 228 → `        from widgets import OptionMetadataSelect` and delete line 231 (`        self.assertIsNotNone(OptionMetadataSelectMultiple)`).

`widgets/tests/test_filterable_list.py`:
- line 11 → two lines:
```python
from widgets import render_filterable_list_script
from widgets.widgets.filterable import FILTERABLE_LIST_JS
```
- lines 17–19, before → after:
```python
    def test_get_filterable_list_js_returns_string(self):
        """Test that get_filterable_list_js returns JavaScript code."""
        js = get_filterable_list_js()
```
```python
    def test_filterable_list_js_is_string(self):
        """Test that FILTERABLE_LIST_JS holds the JavaScript code."""
        js = FILTERABLE_LIST_JS
```
- lines 33, 60 and 67: `        js = get_filterable_list_js()` → `        js = FILTERABLE_LIST_JS`
- lines 121–124, before → after:
```python
        from widgets import get_filterable_list_js, render_filterable_list_script

        self.assertIsNotNone(get_filterable_list_js)
        self.assertIsNotNone(render_filterable_list_script)
```
```python
        from widgets import render_filterable_list_script

        self.assertIsNotNone(render_filterable_list_script)
```
- lines 128–133, before → after:
```python
        from widgets.widgets.filterable import (
            get_filterable_list_js,
            render_filterable_list_script,
        )

        self.assertIsNotNone(get_filterable_list_js)
```
```python
        from widgets.widgets.filterable import (
            FILTERABLE_LIST_JS,
            render_filterable_list_script,
        )

        self.assertIsNotNone(FILTERABLE_LIST_JS)
```

- [ ] **Step 5: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D6RemovedTests widgets.tests
python manage.py check
grep -rnE "CreateOrSelectModelChoiceField|get_filterable_list_js|OptionMetadataSelectMultiple" --include=*.py --include=*.html --include=*.md --include=*.js . | grep -v "/docs/\|core/tests/test_dead_code_removed.py"
ruff check widgets/__init__.py widgets/widgets/__init__.py widgets/fields/create_or_select.py widgets/widgets/filterable.py widgets/widgets/metadata_select.py widgets/tests/test_create_or_select.py widgets/tests/test_metadata_select.py widgets/tests/test_filterable_list.py
```

Expected: tests `OK`; check clean; the grep prints nothing; ruff reports only the two pre-existing `F841` in `widgets/tests/test_create_or_select.py` (`expected_select`, `expected_create` in `TestJavaScriptBehavior`, present at `1e77e23`).

- [ ] **Step 6: Commit.**

```bash
git add widgets/__init__.py widgets/widgets/__init__.py widgets/fields/create_or_select.py \
  widgets/widgets/filterable.py widgets/widgets/metadata_select.py \
  widgets/tests/test_create_or_select.py widgets/tests/test_metadata_select.py \
  widgets/tests/test_filterable_list.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove unused widgets field, JS getter and multi-select widget

CreateOrSelectModelChoiceField, get_filterable_list_js and
OptionMetadataSelectMultiple were used only by tests. The package
exports go with them, and the filterable-list tests now assert on the
FILTERABLE_LIST_JS constant that render_filterable_list_script embeds.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**

```bash
python manage.py test                                   # serial, about 40 min
python manage.py check
python manage.py test core.tests.security.test_route_policies
python manage.py shell -v 0 -c 'from django.urls import URLResolver, get_resolver
def walk(r):
    return sum(walk(p) if isinstance(p, URLResolver) else 1 for p in r.url_patterns)
print(walk(get_resolver()))' | diff "$SCRATCH/routes_before_d6.txt" - && echo ROUTES-UNCHANGED
python scripts/find_dead_code.py --section symbols > "$SCRATCH/symbols_after.md"
D6_RE='core\.(mixins\.(STRequiredMixin|SpendXPPermissionMixin|DeleteMessageMixin|FreebieApprovalMixin)|views\.character_template\.STRequiredMixin|decorators\.|middleware\.cache_middleware\.|cache\.(cache_queryset|get_cached_queryset|invalidate_cache_on_save)|linked_stat\.(MaxCurrentStat|PermanentTemporaryStat)|widgets\.linked_stat\.|utils\.(fast_selector|level_name|tree_sort|compute_level))|widgets\.(fields\.create_or_select\.CreateOrSelectModelChoiceField|widgets\.filterable\.get_filterable_list_js|widgets\.metadata_select\.OptionMetadataSelectMultiple)'
grep -cE "$D6_RE" "$SCRATCH/symbols_before.md" "$SCRATCH/symbols_after.md"
diff <(grep '^| ' "$SCRATCH/symbols_before.md" | sed -E 's/:[0-9]+ \|$/ |/') <(grep '^| ' "$SCRATCH/symbols_after.md" | sed -E 's/:[0-9]+ \|$/ |/') | grep '^>'
D6_PY="core/mixins.py core/views/character_template.py core/cache.py core/linked_stat.py core/utils.py core/widgets/__init__.py locations/views/core/__init__.py widgets/__init__.py widgets/widgets/__init__.py widgets/fields/create_or_select.py widgets/widgets/filterable.py widgets/widgets/metadata_select.py core/tests/mixins/test_mixins.py core/tests/permissions/test_permissions_deployment.py core/tests/views/test_character_template.py core/tests/test_cache.py widgets/tests/test_create_or_select.py widgets/tests/test_metadata_select.py widgets/tests/test_filterable_list.py core/tests/test_dead_code_removed.py"
ruff check $D6_PY
ruff format --check $D6_PY
```

Required:
- Full suite: **0 failures, 0 errors**. Removed tests: 9 in `test_mixins.py`, 2 in `test_permissions_deployment.py`, 4 in `test_character_template.py`, 25 in `test_decorators.py`, 14 in `test_cache_middleware.py`, 11 in `test_cache.py`, 3 in `test_create_or_select.py`, 1 in `test_metadata_select.py` (69; the filterable-list test is renamed, not removed); added: 8 `D6RemovedTests`. So the count drops by exactly 61 against the pre-D6 run.
- `check` clean; route-policy test passes; `ROUTES-UNCHANGED` printed.
- The `grep -c` prints `23` for `symbols_before.md` and `0` for `symbols_after.md`: these 23 rows are gone — unreferenced: `core.linked_stat.MaxCurrentStat`, `core.linked_stat.PermanentTemporaryStat`, `core.mixins.FreebieApprovalMixin`, `core.utils.fast_selector`, `core.utils.level_name`, `core.widgets.linked_stat.LinkedStatFormField`, `core.widgets.linked_stat.PoolWidget`; only-from-tests: `core.cache.cache_queryset`, `core.cache.get_cached_queryset`, `core.cache.invalidate_cache_on_save`, `core.decorators.require_edit_permission`, `…require_model_permission`, `…require_spend_freebies_permission`, `…require_spend_xp_permission`, `…require_view_permission`, `core.middleware.cache_middleware.PerUserCacheMiddleware`, `core.mixins.DeleteMessageMixin`, `core.mixins.STRequiredMixin`, `core.mixins.SpendXPPermissionMixin`, `core.views.character_template.STRequiredMixin`, `widgets.fields.create_or_select.CreateOrSelectModelChoiceField`, `widgets.widgets.filterable.get_filterable_list_js`, `widgets.widgets.metadata_select.OptionMetadataSelectMultiple`.
- The `diff | grep '^>'` prints nothing: no symbol became newly dead (verified in the scratch run: the before/after diff at `1e77e23` contains only `<` lines).
- `ruff check` reports exactly the pre-existing findings: `core/tests/mixins/test_mixins.py` F841 ×2, `core/utils.py:26:5` E741, `widgets/tests/test_create_or_select.py` F841 ×2. `ruff format --check` lists exactly the four files that were already unformatted at `1e77e23` (`core/tests/mixins/test_mixins.py`, `core/tests/test_cache.py`, `core/views/character_template.py`, `widgets/widgets/metadata_select.py`; their diffs are in lines D6 does not touch). Do not reformat them in D6.


## Unit D7: Superseded views, forms and templates

Design reference: `docs/superpowers/specs/2026-09-25-dead-code-removal-design.md` §5 (rows marked **Delete (D7)**), Rules 1–6, Rollout #8. Appendix rows: `2026-09-25-dead-code-removal-report.md` → *views / Unrouted view classes*, *templates / Unreferenced templates*, *symbols*.

**Preconditions.** D1–D6 are merged. `core/tests/test_dead_code_removed.py` exists (created by D4). If it does not, create it with the single header line `from django.test import SimpleTestCase` before Task D7.1.

**Line numbers** below are at `1e77e23`. D4 edits `characters/views/demon/__init__.py`, `characters/views/mage/__init__.py` and `characters/views/werewolf/garou.py` (import block only) and deletes the `ajax.py` URL modules. D6 edits `locations/views/core/__init__.py`. Where a line number has moved, find the line by the quoted text; the text is unique in each file.

**Not in D7 (and not touched):** `items/forms/mage/periapt.py` (see Notes), Fetish views, `RevenantFamilyListView` and `revenant_family/list.html`, `DroneUpdateView` and `drone/form.html`, `SeptPositionUpdateView`, `TremereChantryListView`/`BarrensListView` and their list templates, `locations/demon/reliquary/display_includes/health.html`, `SphereForm`, `characters/forms/core/ability_form.py`, `attribute_form.py`, `attribute_block/form_pool.html`, `characters/core/human/abilities.html`, all chantry code, `ArtifactCreateOrSelectForm`, `OwnerUnapprovedCharacterEditForm`, `LimitedHumanEditForm`, `CompanionFreebiesForm`, `SorcererFreebiesForm`.

### Task 27: [D7.0] Record the baselines

**Files:** none changed. Outputs go to `$SCRATCH` (any directory outside the repo, for example `export SCRATCH=$(mktemp -d)`).

**Interfaces:** none.

- [ ] **Step 1: Save the route inventory.** From the repo root:

```bash
python manage.py shell -v 0 -c '
from django.urls import URLPattern, URLResolver, get_resolver
def walk(ps, pre="", ns=""):
    for p in ps:
        if isinstance(p, URLResolver):
            yield from walk(p.url_patterns, pre + str(p.pattern), ns + (p.namespace + ":" if p.namespace else ""))
        elif isinstance(p, URLPattern):
            cb = getattr(p.callback, "view_class", p.callback)
            yield "\t".join([pre + str(p.pattern), ns + (p.name or ""), cb.__module__ + "." + cb.__qualname__])
print("\n".join(sorted(walk(get_resolver().url_patterns))))
' > "$SCRATCH/routes_before_d7.tsv"
wc -l "$SCRATCH/routes_before_d7.tsv"
```

(At `1e77e23` this prints 1833. After D4 it is lower by the AJAX routes D4 removed; the absolute number doesn't matter, only the diff in the gate.)

- [ ] **Step 2: Save the dead-code report.**

```bash
python scripts/find_dead_code.py --section views --section templates --format tsv > "$SCRATCH/fdc_before_d7.tsv"
```

- [ ] **Step 3: Save the ruff baseline for the files D7 touches.** The files already have these findings at `1e77e23`, and D7 must not add any: `characters/forms/mage/freebies.py` (4× B007, 1× F841), `characters/views/werewolf/kinfolk.py` (F841 `resources_total`), `characters/views/werewolf/garou.py` (F401 `Background`; D7.1 removes it), `characters/tests/views/demon/test_demon.py` (2× F841), `test_dtfhuman.py` (F841), `test_thrall.py` (F841), `characters/tests/views/werewolf/test_wtahuman.py` (F841), `characters/tests/models/changeling/test_changeling.py` (E402). `ruff format --check` also already flags `characters/views/werewolf/{fomor,garou}.py` and `characters/tests/models/werewolf/test_kinfolk.py` (black vs ruff-format drift). The gate therefore uses `ruff check`, not `ruff format`.

### Task 28: [D7.1] Delete the 15 superseded character `*CreateView`s

Every type's create route is its `*BasicsView` (checked with `resolve()`: e.g. `characters:vampire:create:vampire` → `VampireBasicsView`, `characters:werewolf:create:werewolf` → `WerewolfBasicsView`). The only attributes other classes borrow from the create views are the two `FORM_FIELDS` lists (`CtDHumanUpdateView.fields`, `VtMHumanUpdateView.fields`); `grep -rnE "(Changeling|CtDHuman|Demon|DtFHuman|Thrall|MtAHuman|Ghoul|Vampire|VtMHuman|Fomor|Werewolf|Kinfolk|WtAHuman|Wraith|WtOHuman)CreateView\." --include=*.py .` finds only those two. `MageCreateView.FORM_FIELDS` (used by `MageUpdateView`) is a different, routed class and is not touched. Nothing in `scripts/`, the manifest or the URLconfs names the 15 classes.

**Files:**
- Modify `characters/views/changeling/changeling.py` (import line 8, `MessageMixin,` line 29, delete class lines 63–152 plus the two blank lines after it)
- Modify `characters/views/changeling/ctdhuman.py` (import line 9, `MessageMixin,` line 30, class lines 45–99 become a module constant, line 106)
- Modify `characters/views/demon/demon.py` (line 1, `MessageMixin,` line 7, class lines 24–109)
- Modify `characters/views/demon/dtfhuman.py` (line 1, line 7, class lines 20–90)
- Modify `characters/views/demon/thrall.py` (line 1, line 7, class lines 20–94)
- Modify `characters/views/mage/mtahuman.py` (line 9, line 32, class lines 55–166)
- Modify `characters/views/vampire/ghoul.py` (line 3, class lines 22–37)
- Modify `characters/views/vampire/vampire.py` (line 3, class lines 24–42)
- Modify `characters/views/vampire/vtmhuman.py` (line 9, line 31, class lines 46–118 become a module constant, line 125)
- Modify `characters/views/werewolf/fomor.py` (line 7, line 28, class lines 42–106)
- Modify `characters/views/werewolf/garou.py` (line 4, line 14, line 30, class lines 141–221)
- Modify `characters/views/werewolf/kinfolk.py` (line 2, line 21, class lines 57–130)
- Modify `characters/views/werewolf/wtahuman.py` (line 9, line 31, class lines 45–106)
- Modify `characters/views/wraith/wraith.py` (line 3, class lines 25–41)
- Modify `characters/views/wraith/wtohuman.py` (line 9, line 30, class lines 45–105)
- Modify package exports: `characters/views/changeling/__init__.py` (lines 13, 23, 49, 59), `characters/views/demon/__init__.py` (13, 20, 52, 69, 76, 108), `characters/views/mage/__init__.py` (73, 162), `characters/views/vampire/__init__.py` (19, 59, 81, 100, 135, 153), `characters/views/werewolf/__init__.py` (32, 50, 58, 81, 113, 127, 136, 167), `characters/views/wraith/__init__.py` (22, 42, 73, 92)
- Modify tests: `characters/tests/views/demon/test_demon.py` (93–94, 126–140), `characters/tests/views/demon/test_dtfhuman.py` (65–66, 86–100), `characters/tests/views/demon/test_thrall.py` (65–66), `characters/tests/views/wraith/test_wraith.py` (159–160), `characters/tests/views/werewolf/test_wtahuman.py` (261–262), `characters/tests/views/vampire/test_vtmhuman.py` (line 5), `characters/tests/models/changeling/test_changeling.py` (580), `characters/tests/models/changeling/test_ctdhuman.py` (227), `characters/tests/models/vampire/test_vtmhuman.py` (216), `characters/tests/models/wraith/test_wtohuman.py` (195), `characters/tests/models/mage/test_mtahuman.py` (608), `characters/tests/models/werewolf/test_fomor.py` (66), `characters/tests/models/werewolf/test_wtahuman.py` (277), `characters/tests/models/werewolf/test_kinfolk.py` (153), `characters/tests/models/werewolf/test_garou.py` (349)
- Modify `characters/README.md` (lines 187–190)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removed: the 15 `*CreateView` classes and the package aliases `characters.views.changeling.ChangelingCharacterListView` / `CtDHumanCharacterListView` (both misnamed aliases of create views).
- Added: module constants `characters.views.changeling.ctdhuman.CTDHUMAN_FORM_FIELDS` and `characters.views.vampire.vtmhuman.VTMHUMAN_FORM_FIELDS`. `CtDHumanUpdateView.fields` / `VtMHumanUpdateView.fields` keep exactly the same list (same entries, same order, including the existing duplicate entries in the VtM list).

- [ ] **Step 1: Write the guard test.** Make sure the top of `core/tests/test_dead_code_removed.py` has these imports (merge with what D4–D6 added; keep isort order):

```python
import importlib
import importlib.util

from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.test import SimpleTestCase
```

Append:

```python
class D7RemovedTests(SimpleTestCase):
    """Unit D7: superseded views, forms and templates stay deleted."""

    def assert_names_absent(self, names_by_module):
        for module_path, names in names_by_module.items():
            module = importlib.import_module(module_path)
            for name in names:
                with self.subTest(module=module_path, name=name):
                    self.assertFalse(hasattr(module, name))
                    self.assertNotIn(name, getattr(module, "__all__", ()))

    def assert_modules_absent(self, module_paths):
        for module_path in module_paths:
            with self.subTest(module=module_path):
                self.assertIsNone(importlib.util.find_spec(module_path))

    def assert_templates_absent(self, template_names):
        for template_name in template_names:
            with self.subTest(template=template_name):
                with self.assertRaises(TemplateDoesNotExist):
                    get_template(template_name)

    def test_superseded_character_create_views_removed(self):
        self.assert_names_absent(
            {
                "characters.views.changeling.changeling": ["ChangelingCreateView"],
                "characters.views.changeling.ctdhuman": ["CtDHumanCreateView"],
                "characters.views.changeling": [
                    "ChangelingCharacterListView",
                    "CtDHumanCharacterListView",
                ],
                "characters.views.demon.demon": ["DemonCreateView"],
                "characters.views.demon.dtfhuman": ["DtFHumanCreateView"],
                "characters.views.demon.thrall": ["ThrallCreateView"],
                "characters.views.demon": [
                    "DemonCreateView",
                    "DtFHumanCreateView",
                    "ThrallCreateView",
                ],
                "characters.views.mage.mtahuman": ["MtAHumanCreateView"],
                "characters.views.mage": ["MtAHumanCreateView"],
                "characters.views.vampire.ghoul": ["GhoulCreateView"],
                "characters.views.vampire.vampire": ["VampireCreateView"],
                "characters.views.vampire.vtmhuman": ["VtMHumanCreateView"],
                "characters.views.vampire": [
                    "GhoulCreateView",
                    "VampireCreateView",
                    "VtMHumanCreateView",
                ],
                "characters.views.werewolf.fomor": ["FomorCreateView"],
                "characters.views.werewolf.garou": ["WerewolfCreateView"],
                "characters.views.werewolf.kinfolk": ["KinfolkCreateView"],
                "characters.views.werewolf.wtahuman": ["WtAHumanCreateView"],
                "characters.views.werewolf": [
                    "FomorCreateView",
                    "WerewolfCreateView",
                    "KinfolkCreateView",
                    "WtAHumanCreateView",
                ],
                "characters.views.wraith.wraith": ["WraithCreateView"],
                "characters.views.wraith.wtohuman": ["WtOHumanCreateView"],
                "characters.views.wraith": ["WraithCreateView", "WtOHumanCreateView"],
            }
        )

    def test_update_views_keep_their_field_lists(self):
        from characters.views.changeling import ctdhuman
        from characters.views.vampire import vtmhuman

        self.assertIs(ctdhuman.CtDHumanUpdateView.fields, ctdhuman.CTDHUMAN_FORM_FIELDS)
        self.assertIs(vtmhuman.VtMHumanUpdateView.fields, vtmhuman.VTMHUMAN_FORM_FIELDS)
        self.assertIn("kenning", ctdhuman.CTDHUMAN_FORM_FIELDS)
        self.assertIn("finance", vtmhuman.VTMHUMAN_FORM_FIELDS)
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
python manage.py test core.tests.test_dead_code_removed.D7RemovedTests
```

Expected: `FAILED (failures=30, errors=1)`: one `FAIL` subtest per (module, name) pair above (30 pairs), and `ERROR: test_update_views_keep_their_field_lists` (`AttributeError: ... has no attribute 'CTDHUMAN_FORM_FIELDS'`).

- [ ] **Step 3a: Move the two borrowed field lists to module constants.**

`characters/views/changeling/ctdhuman.py`, before (lines 45–49 and 97–106):

```python
class CtDHumanCreateView(MessageMixin, CreateView):
    model = CtDHuman
    success_message = "CtD Human created successfully."
    error_message = "Error creating CtD Human."
    FORM_FIELDS = [
        "name",
        # ... lines 51-96 unchanged ...
    ]
    fields = FORM_FIELDS
    template_name = "characters/changeling/ctdhuman/form.html"


class CtDHumanUpdateView(EditPermissionMixin, UpdateView):
    model = CtDHuman
    success_message = "CtD Human updated successfully."
    error_message = "Error updating CtD Human."
    fields = CtDHumanCreateView.FORM_FIELDS
```

After:

```python
CTDHUMAN_FORM_FIELDS = [
    "name",
    # ... the same 47 entries from old lines 50-96, same order, dedented by 4 spaces ...
    "technology",
]


class CtDHumanUpdateView(EditPermissionMixin, UpdateView):
    model = CtDHuman
    success_message = "CtD Human updated successfully."
    error_message = "Error updating CtD Human."
    fields = CTDHUMAN_FORM_FIELDS
```

`characters/views/vampire/vtmhuman.py`: the same change for lines 46–118 and 125. `class VtMHumanCreateView(...)` through `template_name = "characters/vampire/vtmhuman/form.html"` becomes `VTMHUMAN_FORM_FIELDS = [` + the 65 entries from old lines 51–115 (first `"name"`, last `"technology"`), dedented by 4 spaces + `]`; `fields = VtMHumanCreateView.FORM_FIELDS` becomes `fields = VTMHUMAN_FORM_FIELDS`.

This does the same thing mechanically, and asserts if the source text isn't what the plan expects:

```bash
python - <<'EOF'
import re
for path, cls, const in [
    ("characters/views/changeling/ctdhuman.py", "CtDHumanCreateView", "CTDHUMAN_FORM_FIELDS"),
    ("characters/views/vampire/vtmhuman.py", "VtMHumanCreateView", "VTMHUMAN_FORM_FIELDS"),
]:
    s = open(path).read()
    m = re.search(
        rf"class {cls}\(MessageMixin, CreateView\):\n(    .*\n)*?    FORM_FIELDS = \[\n"
        rf"((        .*\n)*?)    \]\n    fields = FORM_FIELDS\n    template_name = .*\n",
        s,
    )
    assert m, path
    items = "".join(line[4:] + "\n" for line in m.group(2).splitlines())
    s = s[: m.start()] + f"{const} = [\n{items}]\n" + s[m.end():]
    assert s.count(f"fields = {cls}.FORM_FIELDS") == 1, path
    s = s.replace(f"fields = {cls}.FORM_FIELDS", f"fields = {const}")
    open(path, "w").write(s)
EOF
```

- [ ] **Step 3b: Delete the other 13 classes.** Delete each whole `class …CreateView(MessageMixin, CreateView):` block, from its `class` line through its last line, together with the two blank lines that follow it (so the next class keeps its two-blank-line separation):

| File | `class` line | last line |
|---|---|---|
| `characters/views/changeling/changeling.py` | 63 `class ChangelingCreateView(MessageMixin, CreateView):` | 152 |
| `characters/views/demon/demon.py` | 24 `class DemonCreateView(MessageMixin, CreateView):` | 109 |
| `characters/views/demon/dtfhuman.py` | 20 `class DtFHumanCreateView(MessageMixin, CreateView):` | 90 |
| `characters/views/demon/thrall.py` | 20 `class ThrallCreateView(MessageMixin, CreateView):` | 94 |
| `characters/views/mage/mtahuman.py` | 55 `class MtAHumanCreateView(MessageMixin, CreateView):` | 166 |
| `characters/views/vampire/ghoul.py` | 22 `class GhoulCreateView(MessageMixin, CreateView):` | 37 |
| `characters/views/vampire/vampire.py` | 24 `class VampireCreateView(MessageMixin, CreateView):` | 42 |
| `characters/views/werewolf/fomor.py` | 42 `class FomorCreateView(MessageMixin, CreateView):` | 106 |
| `characters/views/werewolf/garou.py` | 141 `class WerewolfCreateView(MessageMixin, CreateView):` | 221 |
| `characters/views/werewolf/kinfolk.py` | 57 `class KinfolkCreateView(MessageMixin, CreateView):` | 130 |
| `characters/views/werewolf/wtahuman.py` | 45 `class WtAHumanCreateView(MessageMixin, CreateView):` | 106 |
| `characters/views/wraith/wraith.py` | 25 `class WraithCreateView(MessageMixin, CreateView):` | 41 |
| `characters/views/wraith/wtohuman.py` | 45 `class WtOHumanCreateView(MessageMixin, CreateView):` | 105 |

- [ ] **Step 3c: Drop the imports the deletions leave unused.** Run `ruff check --select F401 --fix` on the 15 view modules, then confirm that `git diff` shows exactly these import changes and nothing else:

```bash
ruff check --select F401 --fix \
  characters/views/changeling/changeling.py characters/views/changeling/ctdhuman.py \
  characters/views/demon/demon.py characters/views/demon/dtfhuman.py characters/views/demon/thrall.py \
  characters/views/mage/mtahuman.py characters/views/vampire/ghoul.py characters/views/vampire/vampire.py \
  characters/views/vampire/vtmhuman.py characters/views/werewolf/fomor.py characters/views/werewolf/garou.py \
  characters/views/werewolf/kinfolk.py characters/views/werewolf/wtahuman.py \
  characters/views/wraith/wraith.py characters/views/wraith/wtohuman.py
```

| File | Before | After |
|---|---|---|
| `changeling/changeling.py:8` | `from django.views.generic import CreateView, DetailView, FormView, UpdateView` | `from django.views.generic import DetailView, FormView, UpdateView` |
| `changeling/ctdhuman.py:9` | `… import CreateView, DetailView, FormView, UpdateView` | `… import DetailView, FormView, UpdateView` |
| `demon/demon.py:1`, `demon/dtfhuman.py:1`, `demon/thrall.py:1` | `from django.views.generic import CreateView, DetailView, ListView, UpdateView` | `from django.views.generic import DetailView, ListView, UpdateView` |
| `mage/mtahuman.py:9`, `vampire/vtmhuman.py:9`, `werewolf/wtahuman.py:9`, `wraith/wtohuman.py:9` | `from django.views.generic import CreateView, FormView, UpdateView` | `from django.views.generic import FormView, UpdateView` |
| `vampire/ghoul.py:3`, `vampire/vampire.py:3` | `from django.views.generic import CreateView, ListView, UpdateView` | `from django.views.generic import ListView, UpdateView` |
| `werewolf/fomor.py:7`, `werewolf/garou.py:4`, `werewolf/kinfolk.py:2` | `… import CreateView, DetailView, FormView, UpdateView` | `… import DetailView, FormView, UpdateView` |
| `wraith/wraith.py:3` | `from django.views.generic import CreateView, UpdateView` | `from django.views.generic import UpdateView` |
| `werewolf/garou.py:14` | `from characters.models.core.background_block import Background, BackgroundRating` | `from characters.models.core.background_block import BackgroundRating` (already unused at `1e77e23`) |
| the `from core.mixins import (` block in `changeling.py:29`, `ctdhuman.py:30`, `demon.py:7`, `dtfhuman.py:7`, `thrall.py:7`, `mtahuman.py:32`, `vtmhuman.py:31`, `fomor.py:28`, `garou.py:30`, `kinfolk.py:21`, `wtahuman.py:31`, `wtohuman.py:30` | `    MessageMixin,` | line removed |

`ghoul.py`, `vampire.py` and `wraith.py` keep `MessageMixin` (their update views use it).

- [ ] **Step 3d: Remove the package exports and the misnamed aliases.**

`characters/views/changeling/__init__.py`: delete line 13 `from .changeling import ChangelingCreateView as ChangelingCharacterListView`, line 23 `from .ctdhuman import CtDHumanCreateView as CtDHumanCharacterListView`, and the `__all__` entries `    "ChangelingCharacterListView",` (49) and `    "CtDHumanCharacterListView",` (59).

`characters/views/demon/__init__.py`:
- line 13 `from .demon import DemonCreateView, DemonDetailView, DemonListView, DemonUpdateView` → `from .demon import DemonDetailView, DemonListView, DemonUpdateView`
- delete `    DtFHumanCreateView,` (20) in the `from .dtfhuman import (` block
- line 52 `from .thrall import ThrallCreateView, ThrallDetailView, ThrallListView, ThrallUpdateView` → `from .thrall import ThrallDetailView, ThrallListView, ThrallUpdateView`
- delete `__all__` entries `"DemonCreateView",` (69), `"DtFHumanCreateView",` (76), `"ThrallCreateView",` (108)

`characters/views/mage/__init__.py`: delete `    MtAHumanCreateView,` (73, in `from .mtahuman import (`) and `    "MtAHumanCreateView",` (162).

`characters/views/vampire/__init__.py`:
- line 19 `from .ghoul import GhoulCreateView, GhoulDetailView, GhoulListView, GhoulUpdateView` → `from .ghoul import GhoulDetailView, GhoulListView, GhoulUpdateView`
- delete `    VampireCreateView,` (59, in `from .vampire import (`) and `    VtMHumanCreateView,` (81, in `from .vtmhuman import (`)
- delete `__all__` entries `"GhoulCreateView",` (100), `"VampireCreateView",` (135), `"VtMHumanCreateView",` (153)

`characters/views/werewolf/__init__.py`: delete `    FomorCreateView,` (32), `    WerewolfCreateView,` (50), `    KinfolkCreateView,` (58), `    WtAHumanCreateView,` (81) from their `from .x import (` blocks, and `__all__` entries `"FomorCreateView",` (113), `"WerewolfCreateView",` (127), `"KinfolkCreateView",` (136), `"WtAHumanCreateView",` (167).

`characters/views/wraith/__init__.py`:
- line 22 `from .wraith import WraithCreateView, WraithDetailView, WraithUpdateView` → `from .wraith import WraithDetailView, WraithUpdateView`
- delete `    WtOHumanCreateView,` (42) and `__all__` entries `"WraithCreateView",` (73), `"WtOHumanCreateView",` (92)

Keep the multi-line `from .x import (` blocks multi-line; the trailing comma stops ruff's isort from collapsing them.

- [ ] **Step 3e: Delete the two tests that only check a deleted class, and rename the route tests.**

Delete the method `test_create_view_has_get_success_url_method` and the blank line before it: `characters/tests/views/demon/test_demon.py` lines 126–140 and `characters/tests/views/demon/test_dtfhuman.py` lines 86–100. Both import the deleted class and assert `get_success_url in DemonCreateView.__dict__`.

The remaining `Test…CreateView` classes never touch a `*CreateView`. They GET/POST the create route (`reverse("characters:…:create:…")` or `Model.get_creation_url()`), which is served by the `*BasicsView`, and the model-test ones assert the `…/basics.html` template. Rename each and replace (or add) its docstring as shown. Test bodies are unchanged.

| File:line | Before | After (class line + docstring line) |
|---|---|---|
| `characters/tests/views/demon/test_demon.py:93-94` | `class TestDemonCreateView(TestCase):` / `"""Test DemonCreateView functionality."""` | `class TestDemonCreateRoute(TestCase):` / `"""The characters:demon:create:demon route, served by DemonBasicsView."""` |
| `characters/tests/views/demon/test_dtfhuman.py:65-66` | `class TestDtFHumanCreateView(TestCase):` / `"""Test DtFHumanCreateView functionality."""` | `class TestDtFHumanCreateRoute(TestCase):` / `"""The characters:demon:create:dtfhuman route, served by DtFHumanBasicsView."""` |
| `characters/tests/views/demon/test_thrall.py:65-66` | `class TestThrallCreateView(TestCase):` / `"""Test ThrallCreateView functionality."""` | `class TestThrallCreateRoute(TestCase):` / `"""The characters:demon:create:thrall route, served by ThrallBasicsView."""` |
| `characters/tests/views/wraith/test_wraith.py:159-160` | `class TestWraithCreateView(TestCase):` / `"""Test WraithCreateView functionality."""` | `class TestWraithCreateRoute(TestCase):` / `"""The characters:wraith:create:wraith route, served by WraithBasicsView."""` |
| `characters/tests/views/werewolf/test_wtahuman.py:261-262` | `class TestWtAHumanCreateView(WtAHumanViewTestCase):` / `"""Tests for WtAHumanCreateView."""` | `class TestWtAHumanCreateRoute(WtAHumanViewTestCase):` / `"""The characters:werewolf:create:wta_human route, served by WtAHumanBasicsView."""` |
| `characters/tests/models/changeling/test_changeling.py:580` | `class TestChangelingCreateView(TestCase):` (no docstring) | `class TestChangelingCreateRoute(TestCase):` + `"""The characters:changeling:create:changeling route, served by ChangelingBasicsView."""` + blank line |
| `characters/tests/models/changeling/test_ctdhuman.py:227` | `class TestCtDHumanCreateView(TestCase):` | `class TestCtDHumanCreateRoute(TestCase):` + `"""The characters:changeling:create:ctd_human route, served by CtDHumanBasicsView."""` + blank line |
| `characters/tests/models/vampire/test_vtmhuman.py:216` | `class TestVtMHumanCreateView(TestCase):` | `class TestVtMHumanCreateRoute(TestCase):` + `"""The characters:vampire:create:vtm_human route, served by VtMHumanBasicsView."""` + blank line |
| `characters/tests/models/wraith/test_wtohuman.py:195` | `class TestWtOHumanCreateView(TestCase):` | `class TestWtOHumanCreateRoute(TestCase):` + `"""The characters:wraith:create:wto_human route, served by WtOHumanBasicsView."""` + blank line |
| `characters/tests/models/mage/test_mtahuman.py:608` | `class TestMtAHumanCreateView(TestCase):` | `class TestMtAHumanCreateRoute(TestCase):` + `"""The characters:mage:create:mta_human route, served by MtAHumanBasicsView."""` + blank line |
| `characters/tests/models/werewolf/test_fomor.py:66` | `class TestFomorCreateView(TestCase):` | `class TestFomorCreateRoute(TestCase):` + `"""The characters:werewolf:create:fomor route, served by FomorBasicsView."""` + blank line |
| `characters/tests/models/werewolf/test_wtahuman.py:277` | `class TestWtAHumanCreateView(TestCase):` | `class TestWtAHumanCreateRoute(TestCase):` + `"""The characters:werewolf:create:wta_human route, served by WtAHumanBasicsView."""` + blank line |
| `characters/tests/models/werewolf/test_kinfolk.py:153` | `class TestKinfolkCreateView(TestCase):` | `class TestKinfolkCreateRoute(TestCase):` + `"""The characters:werewolf:create:kinfolk route, served by KinfolkBasicsView."""` + blank line |
| `characters/tests/models/werewolf/test_garou.py:349` | `class TestWerewolfCreateView(TestCase):` | `class TestWerewolfCreateRoute(TestCase):` + `"""The characters:werewolf:create:werewolf route, served by WerewolfBasicsView."""` + blank line |

None of the new names collide with an existing class in its module (the existing `Test*BasicsView` classes keep their names).

`characters/tests/views/vampire/test_vtmhuman.py`: delete docstring line 5 `- VtMHumanCreateView - Full character creation`.

- [ ] **Step 3f: Update the README example.** `characters/README.md` lines 187–190, before:

```python
class VampireCreateView(CreateView):
    model = Vampire
    form_class = VampireForm
    template_name = 'characters/vampire/vampire/create.html'
```

After:

```python
# views/vampire/vampire_chargen.py - creation starts at the Basics step
class VampireBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = VampireCreationForm
    template_name = 'characters/vampire/vampire/basics.html'
```

- [ ] **Step 4: Verify.**

```bash
grep -rnE "\b(Changeling|CtDHuman|Demon|DtFHuman|Thrall|MtAHuman|Ghoul|Vampire|VtMHuman|Fomor|Werewolf|Kinfolk|WtAHuman|Wraith|WtOHuman)CreateView\b|(Changeling|CtDHuman)CharacterListView\b" --include=*.py --include=*.html --include=*.md . | grep -v "docs/\|\.claude/\|core/tests/test_dead_code_removed.py"
python manage.py test core.tests.test_dead_code_removed.D7RemovedTests \
  characters.tests.views.demon.test_demon characters.tests.views.demon.test_dtfhuman \
  characters.tests.views.demon.test_thrall characters.tests.views.wraith.test_wraith \
  characters.tests.views.werewolf.test_wtahuman characters.tests.views.vampire.test_vtmhuman \
  characters.tests.models.changeling.test_changeling characters.tests.models.changeling.test_ctdhuman \
  characters.tests.models.vampire.test_vtmhuman characters.tests.models.wraith.test_wtohuman \
  characters.tests.models.mage.test_mtahuman characters.tests.models.werewolf.test_fomor \
  characters.tests.models.werewolf.test_wtahuman characters.tests.models.werewolf.test_kinfolk \
  characters.tests.models.werewolf.test_garou
python manage.py check
python manage.py test core.tests.security.test_route_policies
```

Expected: the grep prints nothing (the guard module is excluded because it names the classes on purpose). The test run passes except the one baseline failure `characters.tests.views.vampire.test_vtmhuman.TestVtMHumanBasicsView.test_basics_view_creates_vtmhuman` (200 ≠ 302), which is on the baseline list. `check` reports no issues. The route-policy test passes.

- [ ] **Step 5: Commit.**

```bash
git add characters/views/changeling/changeling.py characters/views/changeling/ctdhuman.py \
  characters/views/changeling/__init__.py characters/views/demon/demon.py \
  characters/views/demon/dtfhuman.py characters/views/demon/thrall.py characters/views/demon/__init__.py \
  characters/views/mage/mtahuman.py characters/views/mage/__init__.py \
  characters/views/vampire/ghoul.py characters/views/vampire/vampire.py characters/views/vampire/vtmhuman.py \
  characters/views/vampire/__init__.py characters/views/werewolf/fomor.py characters/views/werewolf/garou.py \
  characters/views/werewolf/kinfolk.py characters/views/werewolf/wtahuman.py characters/views/werewolf/__init__.py \
  characters/views/wraith/wraith.py characters/views/wraith/wtohuman.py characters/views/wraith/__init__.py \
  characters/tests/views/demon/test_demon.py characters/tests/views/demon/test_dtfhuman.py \
  characters/tests/views/demon/test_thrall.py characters/tests/views/wraith/test_wraith.py \
  characters/tests/views/werewolf/test_wtahuman.py characters/tests/views/vampire/test_vtmhuman.py \
  characters/tests/models/changeling/test_changeling.py characters/tests/models/changeling/test_ctdhuman.py \
  characters/tests/models/vampire/test_vtmhuman.py characters/tests/models/wraith/test_wtohuman.py \
  characters/tests/models/mage/test_mtahuman.py characters/tests/models/werewolf/test_fomor.py \
  characters/tests/models/werewolf/test_wtahuman.py characters/tests/models/werewolf/test_kinfolk.py \
  characters/tests/models/werewolf/test_garou.py characters/README.md core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove the 15 unrouted character CreateViews

Every character type's create route is its *BasicsView, and chargen
continues through the detail router; the full-form CreateViews were
never routed. The two field lists that update views borrowed move to
module constants (CTDHUMAN_FORM_FIELDS, VTMHUMAN_FORM_FIELDS). Also
drops the misnamed ChangelingCharacterListView/CtDHumanCharacterListView
aliases and the package exports, deletes the two tests that only
checked a CreateView method, and renames the route tests to say they
exercise the Basics views.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 29: [D7.2] Delete the unrouted list views and their templates

`CharacterListView` points at `characters/core/character/list.html`, which does not exist (`characters/templates/characters/core/character/` holds only `char_scene_display.html`, `detail.html`, `display_includes/`, `form.html`, `not_owner.html`). The three vampire list views are plain `ListView`s with no visibility filter. The live list is `characters:index`. `RevenantFamilyListView` in the same package is **kept** (D9 routes it).

**Files:**
- Modify `characters/views/core/character.py` (line 7, line 15 `    VisibilityFilterMixin,`, delete class lines 107–123 plus the two blank lines after it)
- Modify `characters/views/vampire/vampire.py` (line 3, delete class lines 116–119 and the two blank lines before it; it is the last class)
- Modify `characters/views/vampire/ghoul.py` (line 3, delete lines 83–86 and the two blank lines before them)
- Modify `characters/views/vampire/revenant.py` (line 3, delete lines 89–95 and the two blank lines before them)
- Modify `characters/views/vampire/__init__.py` (line 19, lines 37, 61, 102, 121, 137)
- Delete `characters/templates/characters/vampire/vampire/list.html`, `characters/templates/characters/vampire/ghoul/list.html`, `characters/templates/characters/vampire/revenant/list.html`
- Delete `characters/tests/views/vampire/test_revenant.py` (5 lines: a module docstring and a comment saying `RevenantListView` has no URL; no tests)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** removed `characters.views.core.character.CharacterListView`, `characters.views.vampire.{VampireListView, GhoulListView, RevenantListView}` (module and package).

- [ ] **Step 1: Write the guard test.** Add to `D7RemovedTests`:

```python
    def test_unrouted_list_views_removed(self):
        self.assert_names_absent(
            {
                "characters.views.core.character": ["CharacterListView"],
                "characters.views.vampire.vampire": ["VampireListView"],
                "characters.views.vampire.ghoul": ["GhoulListView"],
                "characters.views.vampire.revenant": ["RevenantListView"],
                "characters.views.vampire": [
                    "VampireListView",
                    "GhoulListView",
                    "RevenantListView",
                ],
            }
        )
        self.assert_templates_absent(
            [
                "characters/core/character/list.html",
                "characters/vampire/vampire/list.html",
                "characters/vampire/ghoul/list.html",
                "characters/vampire/revenant/list.html",
            ]
        )
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D7RemovedTests.test_unrouted_list_views_removed`. Expected: 10 failing subtests: 7 names and the 3 existing templates. `characters/core/character/list.html` already passes.

- [ ] **Step 3: Delete.**
- `characters/views/core/character.py`: delete `class CharacterListView(VisibilityFilterMixin, ListView):` (line 107) through `return qs.select_related("polymorphic_ctype", "owner", "chronicle").order_by("name")` (line 123) and the two blank lines after it. Line 7 `from django.views.generic import CreateView, DetailView, ListView, UpdateView` → `from django.views.generic import CreateView, DetailView, UpdateView`. In the `from core.mixins import (` block delete `    VisibilityFilterMixin,` (line 15).
- `characters/views/vampire/vampire.py`: delete the two blank lines and `class VampireListView(ListView):` … `template_name = "characters/vampire/vampire/list.html"` (116–119). The file must end with the single newline after `return LimitedHumanEditForm`. After D7.1, line 3 is `from django.views.generic import ListView, UpdateView` → `from django.views.generic import UpdateView`.
- `characters/views/vampire/ghoul.py`: the same for `class GhoulListView(ListView):` (83–86). Line 3 `from django.views.generic import ListView, UpdateView` → `from django.views.generic import UpdateView`.
- `characters/views/vampire/revenant.py`: the same for `class RevenantListView(ListView):` … `return super().get_queryset().select_related("family")` (89–95). Line 3 `from django.views.generic import CreateView, ListView, UpdateView` → `from django.views.generic import CreateView, UpdateView`.
- `characters/views/vampire/__init__.py`: line 19 (after D7.1) `from .ghoul import GhoulDetailView, GhoulListView, GhoulUpdateView` → `from .ghoul import GhoulDetailView, GhoulUpdateView`. Delete `    RevenantListView,` (37), `    VampireListView,` (61), and the `__all__` entries `"GhoulListView",` (102), `"RevenantListView",` (121), `"VampireListView",` (137).
- `git rm characters/templates/characters/vampire/vampire/list.html characters/templates/characters/vampire/ghoul/list.html characters/templates/characters/vampire/revenant/list.html characters/tests/views/vampire/test_revenant.py`

- [ ] **Step 4: Verify.**

```bash
grep -rnE "\b(Character|Vampire|Ghoul|Revenant)ListView\b|(vampire|ghoul|revenant)/list\.html|core/character/list\.html" --include=*.py --include=*.html . | grep -v "docs/\|core/mixins.py\|core/cache.py\|core/tests/test_dead_code_removed.py"
ruff check characters/views/core/character.py characters/views/vampire/
python manage.py test core.tests.test_dead_code_removed.D7RemovedTests characters.tests.views.vampire characters.tests.views.core
python manage.py check
python manage.py test core.tests.security.test_route_policies
```

Expected: the grep prints nothing (`core/mixins.py:146` and, if D6 left it, `core/cache.py:237` hold unrelated docstring examples named `CharacterListView`, and are filtered). `ruff check` is clean. The tests show only the three baseline vampire failures (`test_basics_view_creates_vampire`, `test_basics_view_creates_ghoul`, `test_basics_view_creates_vtmhuman`, each 200 ≠ 302). `check` and the route-policy test pass.

- [ ] **Step 5: Commit.**

```bash
git add characters/views/core/character.py characters/views/vampire/vampire.py \
  characters/views/vampire/ghoul.py characters/views/vampire/revenant.py \
  characters/views/vampire/__init__.py core/tests/test_dead_code_removed.py
# the three list templates and test_revenant.py were staged by `git rm` in Step 3
git commit -F - <<'EOF'
Remove unrouted CharacterListView and the vampire list views

CharacterListView's template never existed. VampireListView,
GhoulListView and RevenantListView were plain ListViews without a
visibility filter and were never routed; characters:index is the live
list. Their three list templates and an empty test stub go with them.
RevenantFamilyListView is kept (routed in D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 30: [D7.3] Delete the superseded forms

Each form is used only by tests. The live replacements: `LimitedHumanEditForm`/`OwnerUnapprovedCharacterEditForm` (for `LimitedCharacterForm`, `LimitedCharacterEditForm`); the chained freebies forms (`ChainedHumanFreebiesForm` family) for `MageFreebiesForm`, `GhoulFreebiesForm`, `VampireFreebiesForm`; the `*CreationForm`/Basics flow for `EarthboundCreationForm`, `RevenantCreationForm`; `ArtifactCreateOrSelectForm` (kept) and the `fields=[…]` item views for `SorcererArtifactForm`, `WonderCreateOrSelectForm`. `VAMPIRE_CATEGORY_CHOICES` exists only for the two vampire freebies forms, so the whole `characters/forms/vampire/freebies.py` module goes. `PeriaptForm` stays (see Notes).

**Files:**
- Delete `characters/forms/core/character.py` (only `LimitedCharacterForm`)
- Modify `characters/forms/core/__init__.py` (lines 1, 4, 8, 11)
- Modify `characters/forms/core/limited_edit.py` (docstring line 11; class lines 23–71 and the two blank lines after)
- Delete `characters/forms/demon/earthbound.py` (only `EarthboundCreationForm`; `characters/forms/demon/__init__.py` does not import it)
- Modify `characters/forms/mage/freebies.py` (imports lines 1, 11, 14, 15; class lines 239–279 and the two blank lines before)
- Modify `characters/forms/mage/__init__.py` (lines 2, 11)
- Delete `characters/forms/vampire/freebies.py`
- Modify `characters/forms/vampire/__init__.py` (lines 1, 7, 8)
- Delete `characters/forms/vampire/revenant.py` (only `RevenantCreationForm`; not imported by the package)
- Modify `items/forms/mage/wonder.py` (class lines 203–247 and the two blank lines before)
- Modify `items/forms/mage/sorcerer_artifact.py` (class lines 7–15 and the two blank lines after)
- Modify `items/forms/mage/__init__.py` (lines 2, 5)
- Delete `characters/tests/forms/vampire/test_freebies.py`, `characters/tests/forms/vampire/test_revenant.py`
- Modify `characters/tests/forms/core/test_character.py`, `characters/tests/forms/mage/test_freebies_comprehensive.py`, `items/tests/forms/mage/test_sorcerer_artifact.py`
- Modify `.claude/skills/tg-standards/references/permissions.md` (line 34)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** removed `characters.forms.core.{LimitedCharacterForm, LimitedCharacterEditForm}`, `characters.forms.mage.MageFreebiesForm`, `characters.forms.vampire.{GhoulFreebiesForm, VampireFreebiesForm}` (and `VAMPIRE_CATEGORY_CHOICES`), `characters.forms.demon.earthbound`, `characters.forms.vampire.revenant`, `items.forms.mage.SorcererArtifactForm`, `items.forms.mage.wonder.WonderCreateOrSelectForm`. Kept: `items.forms.mage.sorcerer_artifact.ArtifactCreateOrSelectForm` (used by `characters/views/mage/sorcerer.py:61`), `items.forms.mage.PeriaptForm`.

- [ ] **Step 1: Write the guard test.** Add to `D7RemovedTests`:

```python
    def test_superseded_forms_removed(self):
        self.assert_names_absent(
            {
                "characters.forms.core": ["LimitedCharacterForm", "LimitedCharacterEditForm"],
                "characters.forms.core.limited_edit": ["LimitedCharacterEditForm"],
                "characters.forms.mage": ["MageFreebiesForm"],
                "characters.forms.mage.freebies": ["MageFreebiesForm"],
                "characters.forms.vampire": ["GhoulFreebiesForm", "VampireFreebiesForm"],
                "items.forms.mage": ["SorcererArtifactForm"],
                "items.forms.mage.sorcerer_artifact": ["SorcererArtifactForm"],
                "items.forms.mage.wonder": ["WonderCreateOrSelectForm"],
            }
        )
        self.assert_modules_absent(
            [
                "characters.forms.core.character",
                "characters.forms.demon.earthbound",
                "characters.forms.vampire.freebies",
                "characters.forms.vampire.revenant",
            ]
        )
        from items.forms.mage.sorcerer_artifact import ArtifactCreateOrSelectForm

        self.assertTrue(callable(ArtifactCreateOrSelectForm))
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D7RemovedTests.test_superseded_forms_removed`. Expected: 14 failing subtests (10 names, 4 modules).

- [ ] **Step 3: Delete.**

`characters/forms/core/__init__.py`, before → after:

```python
from .character import LimitedCharacterForm
from .character_creation import CharacterCreationForm
from .freebies import HumanFreebiesForm
from .limited_edit import LimitedCharacterEditForm, LimitedHumanEditForm
from .npc_profile import NPCProfileForm

__all__ = [
    "LimitedCharacterForm",
    "CharacterCreationForm",
    "HumanFreebiesForm",
    "LimitedCharacterEditForm",
    "LimitedHumanEditForm",
    "NPCProfileForm",
]
```

```python
from .character_creation import CharacterCreationForm
from .freebies import HumanFreebiesForm
from .limited_edit import LimitedHumanEditForm
from .npc_profile import NPCProfileForm

__all__ = [
    "CharacterCreationForm",
    "HumanFreebiesForm",
    "LimitedHumanEditForm",
    "NPCProfileForm",
]
```

`characters/forms/core/limited_edit.py`: delete docstring line 11 `    - LimitedCharacterEditForm: For base Character instances`. Delete `class LimitedCharacterEditForm(forms.ModelForm):` (23) through its closing `        }` (71) and the two blank lines after it, so `class OwnerUnapprovedCharacterEditForm` follows the imports after two blank lines. `Character` stays imported (used by `OwnerUnapprovedCharacterEditForm`).

`characters/forms/mage/freebies.py`: delete the two blank lines and `class MageFreebiesForm(HumanFreebiesForm):` (239) through end of file (279); the file ends after `SorcererFreebiesForm`'s last line. Imports:
- delete line 1 `from django import forms`
- line 11 `from characters.models.mage.focus import Practice, Tenet` → `from characters.models.mage.focus import Practice`
- delete line 14 `from characters.models.mage.sphere import Sphere`
- delete line 15 `from core.widgets import AutocompleteTextInput`

(`MAGE_CATEGORY_CHOICES` and `Resonance` stay; `CompanionFreebiesForm`/`SorcererFreebiesForm` use them.)

`characters/forms/mage/__init__.py`: delete line 2 `from .freebies import MageFreebiesForm` and line 11 `    "MageFreebiesForm",`.

`characters/forms/vampire/__init__.py`: delete line 1 `from .freebies import GhoulFreebiesForm, VampireFreebiesForm` and lines 7–8 `    "GhoulFreebiesForm",` / `    "VampireFreebiesForm",`.

`items/forms/mage/wonder.py`: delete the two blank lines and `class WonderCreateOrSelectForm(forms.Form):` (203) through end of file (247). All imports stay in use (`ruff check` confirms).

`items/forms/mage/sorcerer_artifact.py`: delete `class SorcererArtifactForm(forms.ModelForm):` (7) through line 15 and the two blank lines after it. Imports stay.

`items/forms/mage/__init__.py`, after:

```python
from .periapt import PeriaptForm
from .wonder import WonderForm

__all__ = ["PeriaptForm", "WonderForm"]
```

Tests:
- `characters/tests/forms/core/test_character.py`: docstring line 5 `- LimitedCharacterEditForm field restrictions` → `- LimitedHumanEditForm field restrictions`. Line 15 → `from characters.forms.core import LimitedHumanEditForm`. Line 16 → `from characters.models.core import Human`. Delete `class TestLimitedCharacterEditForm` (19–103 plus the two blank lines after) and `class TestImageUploadForm` (247–273 plus the two blank lines after). Both only exercise `LimitedCharacterEditForm`. `TestLimitedHumanEditForm`, `TestCharacterFormValidation`, `TestXPSpendingForm` and `TestFreebieSpendingForm` stay.
- `characters/tests/forms/mage/test_freebies_comprehensive.py`: delete `    MageFreebiesForm,` (line 8), line 12 `from characters.models.mage.mage import Mage`, line 14 `from characters.models.mage.sphere import Sphere`, and `class TestMageFreebiesForm` (18–93 plus the two blank lines after). `TestSorcererFreebiesForm` and `TestCompanionFreebiesForm` stay.
- `items/tests/forms/mage/test_sorcerer_artifact.py`: docstring lines 5–6 (`- SorcererArtifactForm initialization and field configuration`, `- SorcererArtifactForm validation`) deleted; line 8 `- Save behavior for both form types` → `- ArtifactCreateOrSelectForm save behavior`. Lines 13–16 → `from items.forms.mage.sorcerer_artifact import ArtifactCreateOrSelectForm`. Delete `TestSorcererArtifactFormBasics` (20–44), `TestSorcererArtifactFormValidation` (47–84), `TestSorcererArtifactFormSave` (87–143) and `TestSorcererArtifactFormWithInstance` (337–357), each with its separating blank lines. The four `TestArtifactCreateOrSelectForm*` classes stay.
- `git rm characters/tests/forms/vampire/test_freebies.py characters/tests/forms/vampire/test_revenant.py`. They test only `VAMPIRE_CATEGORY_CHOICES`, `VampireFreebiesForm`, `GhoulFreebiesForm` and `RevenantCreationForm`.

Skill doc: `.claude/skills/tg-standards/references/permissions.md` line 34 `    return LimitedCharacterEditForm` → `    return LimitedHumanEditForm`.

Delete the modules: `git rm characters/forms/core/character.py characters/forms/demon/earthbound.py characters/forms/vampire/freebies.py characters/forms/vampire/revenant.py`.

- [ ] **Step 4: Verify.**

```bash
grep -rnwE "LimitedCharacterForm|LimitedCharacterEditForm|EarthboundCreationForm|WonderCreateOrSelectForm|MageFreebiesForm|GhoulFreebiesForm|VampireFreebiesForm|RevenantCreationForm|SorcererArtifactForm|VAMPIRE_CATEGORY_CHOICES" --include=*.py --include=*.html --include=*.md . | grep -v "docs/\|core/tests/test_dead_code_removed.py"
ruff check characters/forms/core characters/forms/mage characters/forms/vampire items/forms/mage \
  characters/tests/forms/core/test_character.py characters/tests/forms/mage/test_freebies_comprehensive.py \
  items/tests/forms/mage/test_sorcerer_artifact.py
python manage.py test core.tests.test_dead_code_removed.D7RemovedTests characters.tests.forms items.tests.forms
python manage.py check
python manage.py test core.tests.security.test_route_policies
```

Expected: the grep prints nothing. `ruff` reports only the 5 pre-existing `characters/forms/mage/freebies.py` findings (B007 ×4, F841 `adv`). All tests pass. `check` and the route-policy test pass.

- [ ] **Step 5: Commit.**

```bash
git add characters/forms/core/__init__.py characters/forms/core/limited_edit.py \
  characters/forms/mage/freebies.py characters/forms/mage/__init__.py characters/forms/vampire/__init__.py \
  items/forms/mage/wonder.py items/forms/mage/sorcerer_artifact.py items/forms/mage/__init__.py \
  characters/tests/forms/core/test_character.py characters/tests/forms/mage/test_freebies_comprehensive.py \
  items/tests/forms/mage/test_sorcerer_artifact.py .claude/skills/tg-standards/references/permissions.md \
  core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove superseded character and item forms

LimitedCharacterForm, LimitedCharacterEditForm, EarthboundCreationForm,
WonderCreateOrSelectForm, MageFreebiesForm, GhoulFreebiesForm,
VampireFreebiesForm, RevenantCreationForm and SorcererArtifactForm were
only used by their own tests; each has a live replacement. Their tests
and package exports go with them. ArtifactCreateOrSelectForm and
PeriaptForm are kept (PeriaptForm's rules move to Periapt.clean() in D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

(`git rm` in Step 3 already staged the six deleted files.)

### Task 31: [D7.4] Delete `HumanUrlBlock`

`characters/models/core/human.py:174-…` defines the same five methods ("URL Methods (formerly from HumanUrlBlock)"). No model inherits `HumanUrlBlock`, and the only importer is its test. The test's 20 cases apply to `Human` unchanged, so the test is kept and pointed at `Human` rather than deleted.

**Files:**
- Delete `characters/models/core/human_url_block.py`
- Rename `characters/tests/models/core/test_human_url_block.py` → `characters/tests/models/core/test_human_urls.py` and modify it (lines 1, 8, 13, 17–62, 66, 126)
- Modify `characters/models/core/human.py` (line 175)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** removed module `characters.models.core.human_url_block`. `Human.get_gameline_for_url`, `get_creation_url`, `get_full_creation_url`, `get_update_url` and `get_full_update_url` are unchanged.

- [ ] **Step 1: Write the guard test.** Add to `D7RemovedTests`:

```python
    def test_human_url_block_removed(self):
        self.assert_modules_absent(["characters.models.core.human_url_block"])
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D7RemovedTests.test_human_url_block_removed` → 1 failing subtest.

- [ ] **Step 3: Delete and retarget.**

```bash
git rm characters/models/core/human_url_block.py
git mv characters/tests/models/core/test_human_url_block.py characters/tests/models/core/test_human_urls.py
```

In `characters/tests/models/core/test_human_urls.py`:
- line 1 `"""Tests for human_url_block module."""` → `"""Tests for the URL methods on Human (formerly HumanUrlBlock)."""`
- delete line 8 `from characters.models.core.human_url_block import HumanUrlBlock`
- replace every `HumanUrlBlock.get_gameline_for_url` with `Human.get_gameline_for_url` (the class docstring on line 13 and the ten calls on lines 17–62)
- line 66 `class TestHumanUrlBlockOnHuman(TestCase):` → `class TestHumanUrlMethods(TestCase):`
- line 126 `class TestHumanUrlBlockWithMultipleCharacters(TestCase):` → `class TestHumanUrlsWithMultipleCharacters(TestCase):`

`characters/models/core/human.py` line 175 `    # URL Methods (formerly from HumanUrlBlock)` → `    # URL Methods`.

- [ ] **Step 4: Verify.**

```bash
grep -rn "human_url_block\|HumanUrlBlock" --include=*.py . | grep -v "docs/\|core/tests/test_dead_code_removed.py"
python manage.py test core.tests.test_dead_code_removed.D7RemovedTests characters.tests.models.core.test_human_urls characters.tests.models.core.test_human
ruff check characters/tests/models/core/test_human_urls.py characters/models/core/human.py
python manage.py check
```

Expected: the grep shows only the new docstring on `test_human_urls.py:1`. Tests pass (`test_human_urls`: 20 tests). `ruff` and `check` are clean.

- [ ] **Step 5: Commit.**

```bash
git add characters/models/core/human.py characters/tests/models/core/test_human_urls.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove HumanUrlBlock; test the URL methods on Human

Human already defines the same URL methods and nothing inherits the
block. Its test now exercises Human directly.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 32: [D7.5] Delete the orphan templates

Rechecked at `1e77e23`: none of the 17 paths below appears in any `.py`, `.html` or `.js` file outside `docs/` and the templates themselves, apart from `human/create.html` including `human/basics_block_form.html`, `stat_card.html` including `stat_row.html`, the usage comments inside the three `core/includes` files, and `core/tests/templatetags/test_includes.py`. No `{% include %}` in the project takes a variable template name, and the script's only computed template names (`core/views/reference.py:89-91`) are `detail/list/form.html`. The spec's detail-page check holds: each display include's fields already show on the live detail page.

**Files:**
- Delete:
  - `characters/templates/characters/core/human/create.html`
  - `characters/templates/characters/core/human/basics_block_form.html`
  - `characters/templates/characters/mage/mage/create.html`
  - `characters/templates/characters/mage/mage/mage_basics_block_form.html`
  - `characters/templates/characters/mage/effect/create.html`
  - `characters/templates/characters/mage/spheres/display.html`
  - `characters/templates/characters/mage/tenet/display_includes/basics.html`
  - `characters/templates/characters/mage/corrupted_practice/display_includes/specialization.html`
  - `characters/templates/characters/mage/specialized_practice/display_includes/specialization.html`
  - `characters/templates/characters/werewolf/renownincident/display_includes/temporary_renown.html`
  - `items/templates/items/demon/relic/display_includes/basics.html`
  - `items/templates/items/demon/relic/display_includes/powers.html`
  - `locations/templates/locations/core/city/display_includes/basics.html`
  - `locations/templates/locations/core/location/display_includes/title.html`
  - `core/templates/core/includes/property_row.html`
  - `core/templates/core/includes/stat_card.html`
  - `core/templates/core/includes/stat_row.html`
- Modify `core/tests/templatetags/test_includes.py` (docstring lines 1–8; delete lines 24–228)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** none (templates only). The `get_specialty` filter and its `TestGetSpecialtyFilter` stay; the filter is used by many live templates (e.g. `characters/changeling/ctdhuman/ability_block_display.html`).

- [ ] **Step 1: Write the guard test.** Add to `D7RemovedTests`:

```python
    def test_orphan_templates_removed(self):
        self.assert_templates_absent(
            [
                "characters/core/human/create.html",
                "characters/core/human/basics_block_form.html",
                "characters/mage/mage/create.html",
                "characters/mage/mage/mage_basics_block_form.html",
                "characters/mage/effect/create.html",
                "characters/mage/spheres/display.html",
                "characters/mage/tenet/display_includes/basics.html",
                "characters/mage/corrupted_practice/display_includes/specialization.html",
                "characters/mage/specialized_practice/display_includes/specialization.html",
                "characters/werewolf/renownincident/display_includes/temporary_renown.html",
                "items/demon/relic/display_includes/basics.html",
                "items/demon/relic/display_includes/powers.html",
                "locations/core/city/display_includes/basics.html",
                "locations/core/location/display_includes/title.html",
                "core/includes/property_row.html",
                "core/includes/stat_card.html",
                "core/includes/stat_row.html",
            ]
        )
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D7RemovedTests.test_orphan_templates_removed` → 17 failing subtests.

- [ ] **Step 3: Delete.** `git rm` the 17 files listed under **Files**. In `core/tests/templatetags/test_includes.py`:
- replace the module docstring (lines 1–8, `"""` … `- property_row.html for simple label/value rows` … `"""`) with `"""Tests for the get_specialty template filter."""`
- delete lines 24–228: `class TestStatRowInclude(TestCase):` through the end of `TestPropertyRowInclude` and the two blank lines after it. After the edit the two blank lines after `MockCharacter` are followed directly by `class TestGetSpecialtyFilter(TestCase):`. `MockCharacter` and the imports `Context, Template` and `TestCase` stay in use.

- [ ] **Step 4: Verify.**

```bash
for t in characters/core/human/create.html characters/core/human/basics_block_form.html \
  characters/mage/mage/create.html characters/mage/mage/mage_basics_block_form.html \
  characters/mage/effect/create.html characters/mage/spheres/display.html \
  characters/mage/tenet/display_includes/basics.html \
  characters/mage/corrupted_practice/display_includes/specialization.html \
  characters/mage/specialized_practice/display_includes/specialization.html \
  characters/werewolf/renownincident/display_includes/temporary_renown.html \
  items/demon/relic/display_includes/basics.html items/demon/relic/display_includes/powers.html \
  locations/core/city/display_includes/basics.html locations/core/location/display_includes/title.html \
  core/includes/property_row.html core/includes/stat_card.html core/includes/stat_row.html; do
  grep -rn -F "$t" --include=*.py --include=*.html --include=*.js . | grep -v "docs/\|core/tests/test_dead_code_removed.py"; done
ruff check core/tests/templatetags/test_includes.py
python manage.py test core.tests.test_dead_code_removed.D7RemovedTests core.tests.templatetags core.tests.test_routed_templates
python manage.py check
```

Expected: no grep output. `ruff` is clean. Tests pass; `core.tests.test_routed_templates` (from D1) confirms no routed page lost a template. `check` passes.

- [ ] **Step 5: Commit.**

```bash
git add core/tests/templatetags/test_includes.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove 17 orphan templates

Unreferenced create/basics-block templates, display includes whose
fields the live detail pages already show, and the never-adopted
core/includes stat_row/stat_card/property_row components with their
include tests.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**
  1. `python manage.py test` (serial, about 40 min). Expected: no failures other than the 5 baseline failures listed in the design (vampire/ghoul/vtmhuman basics 200≠302, `TestCircleCreateView.test_create_circle_successfully`, `test_other_player_cannot_attach_companion_to_mage`). The test count drops by the deleted tests. Verified on a scratch tree (D7+D8 applied to `1e77e23`): only those 5 failed.
  2. `python manage.py check` → no issues.
  3. `python manage.py test core.tests.security.test_route_policies` → OK.
  4. `python scripts/find_dead_code.py --section views --section templates --format tsv > "$SCRATCH/fdc_after_d7.tsv"`, then `diff "$SCRATCH/fdc_before_d7.tsv" "$SCRATCH/fdc_after_d7.tsv"`. Expected: only removed rows (`<` lines) plus the two summary lines. Gone: the 15 `*CreateView` rows, `CharacterListView`, `GhoulListView`, `RevenantListView`, `VampireListView` (views 19 fewer "dead"); the 17 orphan templates and the 3 vampire list templates (templates: `dead` −13, `only referenced by dead templates` −2, `only used by unrouted view` −3, `tests only` −2). No new row (`>` line). "routed" (views) and "referenced" (templates) counts are unchanged. On `1e77e23` + D7 the summary reads `views … dead: 19` and `templates 880 … dead: 10, only referenced by dead templates: 3, only used by unrouted view: 6, referenced: 861`; D4/D6 lower these further.
  5. Route inventory: rerun Task D7.0 Step 1 into `$SCRATCH/routes_after_d7.tsv`; `diff` against `routes_before_d7.tsv` must be empty (D7 changes no route).
  6. `ruff check $(git diff --name-only HEAD~5 HEAD --diff-filter=AMR -- '*.py')` (D7 is five commits) reports only the pre-existing findings listed in Task D7.0 Step 3 (minus the `garou.py` F401 that D7.1 fixes).

## Unit D8: URL and index hygiene

Design reference: §6 of the design (rows marked D8), Rules 1–4, Rollout #9. `LOGIN_REDIRECT_URL`/`LOGOUT_REDIRECT_URL` are fixed by D1 and are **not** part of D8.

### Task 33: [D8.0] Record the baselines

**Files:** none changed.

**Interfaces:** none.

- [ ] **Step 1: Route inventory.** Run the command from Task D7.0 Step 1 into `"$SCRATCH/routes_before_d8.tsv"`.
- [ ] **Step 2: Dead-code report.** `python scripts/find_dead_code.py --section urls --section symbols --format tsv > "$SCRATCH/fdc_before_d8.tsv"`.

### Task 34: [D8.1] Delete the no-op `app_name` assignments

Every one of these modules exports a list named `urls`, and every include of it passes that list or a `(list, app_name)` tuple: `include((create.urls, "items_create"), namespace="create")`, `include(detail.urls)`, and `include((gameline_module.urls, module_name), namespace=namespace)` in `characters/urls/__init__.py`, `items/urls/__init__.py` and `locations/urls/__init__.py`. Django reads `app_name` only from a urlconf **module**, so these assignments are never read. `grep -rn "include(" items/urls locations/urls characters/urls` shows no string include. `game/urls.py:6` is **kept**: `tg/urls.py:32` includes it by module string.

At `1e77e23` there are 82 such lines: 25 in `items/urls/**`, 37 in `locations/urls/**` (the 62 from the audit) and 20 in `characters/urls/**`. D4 deletes some of the modules that hold them: `characters/urls/{changeling,core,mage,vampire,werewolf,wraith}/ajax.py` and `locations/urls/vampire/ajax.py`. So after D4 the count is 82 minus the ajax modules D4 removed (normally 75). The step below handles whatever remains.

**Files:** every file under `items/urls/`, `locations/urls/` and `characters/urls/` that has a line matching `^app_name = "…"$`. At `1e77e23`:
- `items/urls/core/{create,detail,index,update}.py`, `items/urls/demon/{create,detail,index,update}.py`, `items/urls/hunter/{create,detail,index,update}.py`, `items/urls/mage/detail.py`, `items/urls/mummy/{create,detail,update}.py`, `items/urls/vampire/{create,detail,index,update}.py`, `items/urls/werewolf/detail.py`, `items/urls/wraith/{create,detail,index,update}.py`, all at line 5
- `locations/urls/changeling/{create,detail,index,update}.py`, `locations/urls/core/{create,detail,index,update}.py`, `locations/urls/demon/{__init__,create,detail,index,update}.py`, `locations/urls/hunter/{__init__,create,detail,index,update}.py`, `locations/urls/mage/{create,detail,index,update}.py`, `locations/urls/mummy/{create,detail,update}.py`, `locations/urls/vampire/{ajax (line 2),create,detail,index,update}.py`, `locations/urls/werewolf/{create,detail,index,update}.py`, `locations/urls/wraith/{create,detail,update}.py`, at line 5 unless noted
- `characters/urls/core/{ajax (5),create (12),detail (10),index (8),update (11)}.py`, `characters/urls/mage/{ajax,create,index,update}.py` (5) and `characters/urls/mage/detail.py` (9), `characters/urls/mummy/{create,detail,update}.py` (5), `characters/urls/vampire/{create,detail,update}.py` (5), `characters/urls/{changeling,vampire,werewolf,wraith}/ajax.py` (2)
- `.claude/skills/tg-standards/references/urls.md`
- `core/tests/test_dead_code_removed.py`

**Interfaces:** none. Every URL name, namespace and path is unchanged, which the route inventory diff checks.

- [ ] **Step 1: Write the guard test.** Make sure `core/tests/test_dead_code_removed.py` has the imports listed in Task D7.1 Step 1, then append:

```python
class D8RemovedTests(SimpleTestCase):
    """Unit D8: URL and index hygiene."""

    def test_list_included_url_modules_have_no_app_name(self):
        from pathlib import Path

        from django.conf import settings

        # Walk the files, not pkgutil: the */urls/core directories have no __init__.py.
        base = Path(settings.BASE_DIR)
        checked = 0
        for app in ("characters", "items", "locations"):
            for path in sorted((base / app / "urls").rglob("*.py")):
                parts = path.relative_to(base).with_suffix("").parts
                module_name = ".".join(parts[:-1] if parts[-1] == "__init__" else parts)
                with self.subTest(module=module_name):
                    module = importlib.import_module(module_name)
                    self.assertFalse(hasattr(module, "app_name"))
                checked += 1
        self.assertGreater(checked, 100)

    def test_game_urls_keep_app_name(self):
        from game import urls as game_urls

        self.assertEqual(game_urls.app_name, "game")
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D8RemovedTests` → one failing subtest per remaining `app_name` line (82 at `1e77e23`). `test_game_urls_keep_app_name` passes.

- [ ] **Step 3: Delete the lines.** From the repo root:

```bash
python - <<'EOF'
import pathlib
import re

edited = 0
for root in ("items/urls", "locations/urls", "characters/urls"):
    for path in sorted(pathlib.Path(root).rglob("*.py")):
        lines = path.read_text().split("\n")
        idx = [i for i, line in enumerate(lines) if re.fullmatch(r'app_name = "[^"]*"', line)]
        if not idx:
            continue
        assert len(idx) == 1, path
        i = idx[0]
        drop = [i]
        # locations/urls/{demon,hunter}/__init__.py have a blank line on both sides
        if 0 < i < len(lines) - 1 and lines[i - 1] == "" and lines[i + 1] == "":
            drop.append(i + 1)
        for j in reversed(drop):
            del lines[j]
        path.write_text("\n".join(lines))
        edited += 1
        print(path)
print("edited", edited)
EOF
```

Typical before → after (`items/urls/demon/create.py`):

```python
from items import views

app_name = "demon:create"
urls = [
```

```python
from items import views

urls = [
```

`locations/urls/demon/__init__.py` (and `hunter/__init__.py`), before → after:

```python
from . import create, detail, index, update

app_name = "demon"

urls = [
```

```python
from . import create, detail, index, update

urls = [
```

- [ ] **Step 4: Update the URL skill reference** so it stops telling authors to add `app_name`. In `.claude/skills/tg-standards/references/urls.md`, replace the sections from `## Main Router` up to (not including) `## Namespace Convention` with:

````markdown
## Main Router

```python
# app/urls/__init__.py (see items/urls/__init__.py)
from importlib import import_module

from django.urls import include, path

from core.constants import GameLine

from .core import create, detail, index, update

urlpatterns = []
for url_path, module_name, namespace in GameLine.URL_PATTERNS:
    try:
        gameline_module = import_module(f".{module_name}", package="app.urls")
        urlpatterns.append(
            path(f"{url_path}/", include((gameline_module.urls, module_name), namespace=namespace))
        )
    except (ImportError, AttributeError):
        pass

urlpatterns.extend(
    [
        path("create/", include((create.urls, "app_create"), namespace="create")),
        path("update/", include((update.urls, "app_update"), namespace="update")),
        path("list/", include((index.urls, "app_list"), namespace="list")),
        path("", include(detail.urls)),
    ]
)
```

## Gameline Router

```python
# app/urls/mygameline/__init__.py (see items/urls/demon/__init__.py)
from django.urls import include, path

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "mygameline_create"), namespace="create")),
    path("update/", include((update.urls, "mygameline_update"), namespace="update")),
    path("list/", include((index.urls, "mygameline_list"), namespace="list")),
    path("", include(detail.urls)),
]
```

## Leaf modules (create / update / list / detail)

Each leaf module exports a plain `urls` list. Do **not** add `app_name`: the list is
included directly or as a `(urls, app_name)` tuple, so Django never reads a module-level
`app_name` (`core/tests/test_dead_code_removed.py` fails if one is added).

```python
# app/urls/mygameline/create.py
from django.urls import path

from app import views

urls = [
    path("my_character/", views.mygameline.MyCharacterCreateView.as_view(), name="my_character"),
    path("my_reference/", views.mygameline.MyReferenceCreateView.as_view(), name="my_reference"),
]
```

`update.py` uses `<int:pk>/` paths, `index.py` holds list views, and `detail.py` holds
`<int:pk>/` detail routes, all in the same shape.
````

- [ ] **Step 5: Verify.**

```bash
grep -rn "^app_name" items/urls locations/urls characters/urls --include=*.py
python manage.py test core.tests.test_dead_code_removed.D8RemovedTests core.tests.security.test_route_policies \
  core.tests.urls characters.tests.urls locations.tests.urls
python manage.py check
```

Then re-dump the route inventory (Task D7.0 Step 1) to `$SCRATCH/routes_after_d8_1.tsv` and `diff "$SCRATCH/routes_before_d8.tsv" "$SCRATCH/routes_after_d8_1.tsv"`. Expected: the grep prints nothing, the tests pass, `check` is clean, and the diff is **empty**, meaning every URL name, namespace, path and callback is identical. (`items/tests/urls` does not exist at `1e77e23`, so no items URL test label is listed.)

- [ ] **Step 6: Commit.**

```bash
git add items/urls locations/urls characters/urls .claude/skills/tg-standards/references/urls.md core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Drop no-op app_name assignments from list-included URL modules

Every items/locations/characters URL module exports a `urls` list that
is included as a list or a (list, app_name) tuple, so Django never
reads the module-level app_name. The route inventory is byte-for-byte
unchanged. game/urls.py keeps its app_name (included by module string).
The URL skill reference now shows the real pattern.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 35: [D8.2] Make `accounts:user` a redirect to `core:home`

`/accounts/` (`accounts:user`) served a second copy of `core.views.home.HomeListView`, which is also `core:home` at `/`. It becomes `RedirectView.as_view(pattern_name="core:home")` with the same name, so the path and `reverse("accounts:user")` keep working. D1 points `LOGIN_REDIRECT_URL` at `core:home`, so nothing in settings uses `"user"` any more.

Manifest and middleware: `RedirectView`'s module is `django.views.generic.base`, which is not in `core.access_policy.PROJECT_PREFIXES`. `AuthorizationMiddleware.process_view` returns `None` for it (no policy lookup), and `test_route_policies` / `scripts/build_route_policy_manifest.py` filter it out, the same way they treat `django.views.static.serve` and `django.contrib.auth.urls`. `core.views.home.HomeListView` keeps its `PUBLIC_READ` manifest entry (`core/route_policy_manifest.py:843`) because `core:home` still routes it. **No manifest change.**

**Files:**
- Modify `accounts/urls.py` (lines 1–4, line 57)
- Modify `accounts/tests/views/test_views.py` (import block line 5–6; lines 25–30; `test_template_logged_out` lines 61–63)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** `accounts:user` → `django.views.generic.base.RedirectView` with `view_initkwargs == {"pattern_name": "core:home"}`. Response: 302 to `/`, for any method RedirectView accepts.

- [ ] **Step 1: Write the guard test.** Add to `D8RemovedTests`:

```python
    def test_accounts_root_redirects_to_home(self):
        from django.urls import resolve, reverse
        from django.views.generic import RedirectView

        self.assertEqual(reverse("accounts:user"), "/accounts/")
        match = resolve("/accounts/")
        self.assertEqual(match.view_name, "accounts:user")
        self.assertIs(match.func.view_class, RedirectView)
        self.assertEqual(match.func.view_initkwargs, {"pattern_name": "core:home"})
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D8RemovedTests.test_accounts_root_redirects_to_home` → `AssertionError: <class 'core.views.home.HomeListView'> is not <class 'django.views.generic.base.RedirectView'>`.

- [ ] **Step 3: Change the route.** `accounts/urls.py`, before:

```python
from django.urls import path

from accounts import views
from core import views as core_views
...
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("", core_views.HomeListView.as_view(), name="user"),
]
```

After (`core_views` was only used on that line):

```python
from django.urls import path
from django.views.generic import RedirectView

from accounts import views
...
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("", RedirectView.as_view(pattern_name="core:home"), name="user"),
]
```

`accounts/tests/views/test_views.py` lines 25–30, before:

```python
class TestSignUpView(TestCase):
    """Class that Tests SignUpView"""

    def test_correct_template(self):
        self.client.get("/accounts/")
        self.assertTemplateUsed("registration/login.html")
```

(`assertTemplateUsed` with one argument returns an unused context manager, so this test never asserted anything.) After:

```python
class TestAccountsRootRedirect(TestCase):
    """/accounts/ (accounts:user) redirects to the home page."""

    def test_accounts_root_redirects_to_home(self):
        self.assertEqual(reverse("accounts:user"), "/accounts/")
        response = self.client.get("/accounts/")
        self.assertRedirects(response, reverse("core:home"))
```

`TestProfileView.test_template_logged_out` (lines 61–63) **must change**. Before D8 it fetched `/accounts/`, which had its own `cache_page` key. Now `follow=True` lands on `/`, whose `HomeListView` is wrapped in `cache_page(60 * 5)` (`core/views/home.py:8`) with a process-wide LocMemCache. In a full serial run, an earlier test has already cached `/`, so the followed response renders **no templates** and `assertTemplateUsed` fails. This was confirmed: the scratch full-suite run failed on exactly this test, and it fails in isolation when a test that GETs `/` runs first. Add `from django.core.cache import cache` after `from django.contrib.auth.models import User`, and change the test.

Before:

```python
    def test_template_logged_out(self):
        response = self.client.get("/accounts/", follow=True)
        self.assertTemplateUsed(response, "core/index.html")
```

After:

```python
    def test_template_logged_out(self):
        # "/" is cache_page'd; a response cached by an earlier test renders no templates.
        cache.clear()
        response = self.client.get("/accounts/", follow=True)
        self.assertEqual(response.redirect_chain, [(reverse("core:home"), 302)])
        self.assertTemplateUsed(response, "core/index.html")
```

`TestAccountsRootRedirect` does not depend on the cache: `assertRedirects` only checks the 302 target and that fetching it returns 200, which a cached response also does. `core/tests/views/test_errors.py:120` (`client.post(reverse("accounts:user"))`, accepting `[200, 302, 403, 405]`) is unchanged and now gets 302.

- [ ] **Step 4: Verify.**

```bash
python manage.py test core.tests.test_dead_code_removed.D8RemovedTests accounts.tests.views.test_views \
  core.tests.views.test_errors core.tests.security.test_route_policies core.tests.test_routed_templates
python manage.py check
ruff check accounts/urls.py accounts/tests/views/test_views.py
```

Re-dump the route inventory to `$SCRATCH/routes_after_d8_2.tsv`; `diff "$SCRATCH/routes_before_d8.tsv" "$SCRATCH/routes_after_d8_2.tsv"` must show exactly:

```
< accounts/	accounts:user	core.views.home.HomeListView
---
> accounts/	accounts:user	django.views.generic.base.RedirectView
```

Expected: tests pass, and `check` is clean. `ruff` reports only the pre-existing F841 in `accounts/tests/views/test_views.py`. To prove the cache fix, temporarily add `accounts/tests/views/test_aa_prime_cache.py` containing a `TestCase` whose one test does `self.client.get("/")`. Run `python manage.py test accounts.tests.views.test_aa_prime_cache accounts.tests.views.test_views`, which must be OK, then delete the temporary file.

- [ ] **Step 5: Commit.**

```bash
git add accounts/urls.py accounts/tests/views/test_views.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Redirect /accounts/ to the home page instead of a second HomeListView

accounts:user rendered a duplicate of core:home. It is now a
RedirectView to core:home under the same name, so the path and
reverse() keep working. RedirectView is a Django view, which the
access-policy middleware and the route-policy test skip, so the
manifest is unchanged (HomeListView keeps its entry for core:home).
Replaces a test that asserted nothing with a redirect assertion.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 36: [D8.3] Delete `error_401`

Django has no `handler401`. `tg/urls.py:49-51` sets only `handler403/404/500`, and the only caller of `error_401` is its test. `core/templates/core/errors/401.html` is **kept**: `core/middleware/auth_error_handler.py:40` renders it directly.

**Files:**
- Modify `core/views/errors.py` (delete lines 6–15)
- Modify `core/tests/views/test_errors.py` (delete lines 27–37)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** removed `core.views.errors.error_401`. `error_403`, `error_404` and `error_500` are unchanged.

- [ ] **Step 1: Write the guard test.** Add to `D8RemovedTests`:

```python
    def test_error_401_view_removed_but_template_kept(self):
        from core.views import errors

        self.assertFalse(hasattr(errors, "error_401"))
        # AuthErrorHandlerMiddleware still renders this template directly.
        get_template("core/errors/401.html")
```

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D8RemovedTests.test_error_401_view_removed_but_template_kept` → `AssertionError: True is not false`.

- [ ] **Step 3: Delete.** In `core/views/errors.py`, delete from `def error_401(request, exception=None):` (line 6) through `    return render(request, "core/errors/401.html", status=401)` (line 13) and the two blank lines after it, so `def error_403` follows the import after two blank lines. In `core/tests/views/test_errors.py`, delete the method `test_error_401_view` (lines 27–36) and the blank line after it (37). The file docstring line 5 ("Unauthenticated users get 401 …") stays true: the middleware tests in the same file still cover it.

- [ ] **Step 4: Verify.**

```bash
grep -rn "error_401" --include=*.py . | grep -v "docs/\|core/tests/test_dead_code_removed.py"
python manage.py test core.tests.test_dead_code_removed.D8RemovedTests core.tests.views.test_errors core.tests.middleware
ruff check core/views/errors.py core/tests/views/test_errors.py
python manage.py check
```

Expected: no grep output, and the tests pass. `ruff` reports only the pre-existing F841 (`user`) in `test_errors.py`. `check` is clean.

- [ ] **Step 5: Commit.**

```bash
git add core/views/errors.py core/tests/views/test_errors.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove error_401: Django has no handler401

Only its own test called it. core/errors/401.html stays; the auth
error middleware renders it directly.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 37: [D8.4] Delete `ItemIndexView.items` and `LocationIndexView.locs`

Neither class attribute is read anywhere. `ItemIndexView.get_context` and `LocationIndexView.get_context` query `ObjectType`/`ItemModel`/`LocationModel` directly. The 27 item and 34 location model imports exist only to fill these dicts. `grep -rn "from items.views.core import\|from locations.views.core import\|import items.views.core\|import locations.views.core" --include=*.py .` returns nothing, and no code accesses `views.core.<Model>` (checked with `grep -rnE "views\.core\.(Weapon|Wonder|City|Chantry|…)\b"` over all 61 names). So the imports and their `__all__` re-exports go too. `ItemModel` and `LocationModel` stay: `GenericItemDetailView`/`GenericLocationDetailView` and both `get()` methods use them.

**Files:**
- Modify `items/views/core/__init__.py` (import lines 13–58 → one line; delete lines 141–179 plus the blank line after; `__all__` entries)
- Modify `locations/views/core/__init__.py` (import lines 11–63 → one line; delete lines 130–175 plus the blank line after; `__all__` entries)
- Modify `core/tests/test_dead_code_removed.py`

**Interfaces:** removed `ItemIndexView.items`, `LocationIndexView.locs`, and the module attributes and `__all__` entries of `items.views.core` for `Artifact, Bloodstone, Charm, DemonRelic, Dross, Fetish, Grimoire, HunterGear, HunterRelic, Material, Medium, MeleeWeapon, MummyRelic, Periapt, RangedWeapon, SorcererArtifact, Talen, Talisman, ThrownWeapon, Treasure, Ushabti, VampireArtifact, Vessel, Weapon, Wonder, WraithArtifact, WraithRelic`, and of `locations.views.core` for `Barrens, Bastion, Byway, Caern, Chantry, Citadel, City, CultTemple, Demesne, Domain, DreamRealm, Elysium, Freehold, Haunt, Haven, Holding, HorizonRealm, HuntingGround, Library, Necropolis, Nihil, Node, ParadoxRealm, Rack, RealityZone, Reliquary, Safehouse, Sanctum, Sector, Tomb, TremereChantry, Trod, UndergroundSanctuary, WraithFreehold`. The view classes `items.views.core.Material*View` etc. are unaffected (they come from the `.material` etc. submodules, not these model imports).

- [ ] **Step 1: Write the guard test.** Add to `D8RemovedTests`:

```python
    REMOVED_ITEM_VIEW_NAMES = [
        "Artifact",
        "Bloodstone",
        "Charm",
        "DemonRelic",
        "Dross",
        "Fetish",
        "Grimoire",
        "HunterGear",
        "HunterRelic",
        "Material",
        "Medium",
        "MeleeWeapon",
        "MummyRelic",
        "Periapt",
        "RangedWeapon",
        "SorcererArtifact",
        "Talen",
        "Talisman",
        "ThrownWeapon",
        "Treasure",
        "Ushabti",
        "VampireArtifact",
        "Vessel",
        "Weapon",
        "Wonder",
        "WraithArtifact",
        "WraithRelic",
    ]
    REMOVED_LOCATION_VIEW_NAMES = [
        "Barrens",
        "Bastion",
        "Byway",
        "Caern",
        "Chantry",
        "Citadel",
        "City",
        "CultTemple",
        "Demesne",
        "Domain",
        "DreamRealm",
        "Elysium",
        "Freehold",
        "Haunt",
        "Haven",
        "Holding",
        "HorizonRealm",
        "HuntingGround",
        "Library",
        "Necropolis",
        "Nihil",
        "Node",
        "ParadoxRealm",
        "Rack",
        "RealityZone",
        "Reliquary",
        "Safehouse",
        "Sanctum",
        "Sector",
        "Tomb",
        "TremereChantry",
        "Trod",
        "UndergroundSanctuary",
        "WraithFreehold",
    ]

    def test_index_view_type_maps_removed(self):
        from items.views import core as item_views
        from locations.views import core as location_views

        self.assertFalse(hasattr(item_views.ItemIndexView, "items"))
        self.assertFalse(hasattr(location_views.LocationIndexView, "locs"))
        for module, names in (
            (item_views, self.REMOVED_ITEM_VIEW_NAMES),
            (location_views, self.REMOVED_LOCATION_VIEW_NAMES),
        ):
            for name in names:
                with self.subTest(module=module.__name__, name=name):
                    self.assertFalse(hasattr(module, name))
                    self.assertNotIn(name, module.__all__)
        self.assertIn("ItemModel", item_views.__all__)
        self.assertIn("LocationModel", location_views.__all__)
```

(Put the two list attributes at the top of the `D8RemovedTests` class body, above the first test method.)

- [ ] **Step 2: Run it and watch it fail.** `python manage.py test core.tests.test_dead_code_removed.D8RemovedTests.test_index_view_type_maps_removed` → the first assertion fails (`True is not false`).

- [ ] **Step 3: Delete.**

`items/views/core/__init__.py`: replace lines 12–59, from `from items.forms.core.item_creation import ItemCreationForm` through `from items.views import mage, werewolf` (the eight `# <Gameline> models` comment groups and every model import in them), with:

```python
from items.forms.core.item_creation import ItemCreationForm
from items.models.core.item import ItemModel
from items.views import mage, werewolf
```

Delete `    items = {` (141) through its closing `    }` (179) and the blank line after it, so `class ItemIndexView(View):` is followed directly by `    def get(self, request, *args, **kwargs):`. Delete the 27 names above from `__all__` (each is one `    "Name",` line; keep `"ItemModel"`).

`locations/views/core/__init__.py`: replace lines 10–64, from `from locations.forms.core.location_creation import LocationCreationForm` through `from locations.views import mage, werewolf`, with:

```python
from locations.forms.core.location_creation import LocationCreationForm
from locations.models.core.location import LocationModel
from locations.views import mage, werewolf
```

Delete `    locs = {` (130) through `    }` (175) and the blank line after it. Delete the 34 names above from `__all__` (keep `"LocationModel"`). The `core.utils` import and its `__all__` entries (`get_gameline_name`, and `level_name`/`tree_sort` if D6 has not already removed them) are not part of this task.

This does both files mechanically, and asserts if the source text isn't what the plan expects:

```bash
python - <<'EOF'
import ast
import re

def strip(path, cls, attr, keep, keep_import, tail):
    s = open(path).read()
    lines = s.split("\n")
    node = next(n for n in ast.parse(s).body if isinstance(n, ast.ClassDef) and n.name == cls)
    assign = next(m for m in node.body if isinstance(m, ast.Assign) and m.targets[0].id == attr)
    start, end = assign.lineno - 1, assign.end_lineno
    if lines[end] == "":
        end += 1
    names = {v.id for v in assign.value.values} - {keep}
    del lines[start:end]
    s = "\n".join(lines)
    i, j = s.index("\n\n# Changeling models\n"), s.index(tail)
    s = s[:i] + "\n" + keep_import + s[j:]
    for name in names:
        s, n = re.subn(rf'^    "{name}",\n', "", s, flags=re.M)
        assert n == 1, (path, name)
    open(path, "w").write(s)
    print(path, len(names))

strip("items/views/core/__init__.py", "ItemIndexView", "items", "ItemModel",
      "from items.models.core.item import ItemModel\n", "from items.views import mage, werewolf\n")
strip("locations/views/core/__init__.py", "LocationIndexView", "locs", "LocationModel",
      "from locations.models.core.location import LocationModel\n", "from locations.views import mage, werewolf\n")
EOF
```

It prints `items/views/core/__init__.py 27` and `locations/views/core/__init__.py 34`.

- [ ] **Step 4: Verify.**

```bash
ruff check items/views/core/__init__.py locations/views/core/__init__.py
python manage.py test core.tests.test_dead_code_removed.D8RemovedTests items.tests.views locations.tests.views.core \
  core.tests.security.test_route_policies core.tests.test_routed_templates
python manage.py check
```

Expected: `ruff` is clean (no I001: the three imports stay contiguous in the first-party block), all tests pass, and `check` is clean.

- [ ] **Step 5: Commit.**

```bash
git add items/views/core/__init__.py locations/views/core/__init__.py core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Remove unread ItemIndexView.items and LocationIndexView.locs

Neither type map was ever read; the index views query ObjectType and
the base models directly. The 61 model imports and __all__ re-exports
that existed only to fill them go too (nothing imports them from
items.views.core or locations.views.core).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**
  1. `python manage.py test` (serial, about 40–70 min). Expected: exactly the 5 baseline failures and nothing else. On the scratch tree (`1e77e23` + D7 + D8) the run was `Ran 7032 tests … FAILED (failures=6, skipped=49)`: the 5 baseline failures plus `TestProfileView.test_template_logged_out`, which is the cache-order issue fixed in D8.2 Step 3. The fix was verified afterwards: the test fails without it and passes with it after `/` is primed.
  2. `python manage.py check` → no issues.
  3. `python manage.py test core.tests.security.test_route_policies` → OK.
  4. `python scripts/find_dead_code.py --section urls --section symbols --format tsv > "$SCRATCH/fdc_after_d8.tsv"`; `diff "$SCRATCH/fdc_before_d8.tsv" "$SCRATCH/fdc_after_d8.tsv"`. Expected: the `accounts:user … core.views.home.HomeListView … tests only` row is gone (RedirectView isn't a project view, so the name leaves the report; URL names −1, `tests only (c)` −1); the symbols row `core.views.error_401 … Only referenced from tests` is gone; the two `Computed URL names` rows for `items/views/core/__init__.py` and `locations/views/core/__init__.py` change only their line numbers (206→121 and 202→103 at `1e77e23`); nothing else changes.
  5. Route inventory: re-dump and `diff` against `routes_before_d8.tsv`. The only difference is the `accounts/ accounts:user` callback line shown in Task D8.2. The route count is unchanged.
  6. `ruff check $(git diff --name-only HEAD~4 HEAD --diff-filter=AMR -- '*.py')` (D8 is four commits) reports only the pre-existing F841s in `accounts/tests/views/test_views.py` and `core/tests/views/test_errors.py`.


## Unit D9: Small recoveries

Recovers the seven "Recover" rows of spec section 5/6 that are not the chantry wizard or Story XP. Every task is TDD: failing test, run, implement, run, commit. D9 lands after D7 and D8, so every edit below is anchored on a neighbouring line that D7/D8 do not touch (D8 deletes the `app_name = ...` lines in `locations/urls/**`, D7 deletes `SorcererArtifactForm` from `items/forms/mage/__init__.py`); do not paste whole files over those modules.

Shorthands used in every command below (run from the repo root):

```bash
PY=/tmp/claude-0/venv/bin/python
RUFF=/tmp/claude-0/venv/bin/ruff
```

Record the resolver route count before starting the unit (D9 adds exactly **7** URL patterns):

```bash
$PY manage.py shell -c "from django.urls import URLResolver, get_resolver; c = lambda ps: sum(c(p.url_patterns) if isinstance(p, URLResolver) else 1 for p in ps); print(c(get_resolver().url_patterns))"
```

### Task 38: [D9.1] Route RevenantFamilyListView

**Files:**
- Modify: `characters/urls/vampire/index.py`
- Modify: `core/route_policy_manifest.py` (`PUBLIC_READ`)
- Rewrite (currently a TODO stub): `characters/tests/views/vampire/test_revenant_family.py`

**Interfaces:**
- URL name `characters:vampire:list:revenant_family` → `/characters/vampire/list/revenant_family/` → `characters.views.vampire.revenant_family.RevenantFamilyListView` (existing class, `ordering = ["name"]`, template `characters/vampire/revenant_family/list.html` exists).
- Manifest: `characters.views.vampire.revenant_family.RevenantFamilyListView` in `PUBLIC_READ` (the view has no `post`, so `test_public_reference_views_do_not_accept_mutating_methods` holds).

- [ ] **Step 1: Write the failing test.** Replace the whole content of `characters/tests/views/vampire/test_revenant_family.py` with:

```python
"""Tests for the RevenantFamily views."""

from django.test import TestCase
from django.urls import reverse

from characters.models.vampire.revenant import RevenantFamily


class TestRevenantFamilyListView(TestCase):
    """The revenant family list is public reference data like the clan list."""

    def setUp(self):
        RevenantFamily.objects.create(name="Zantosa")
        RevenantFamily.objects.create(name="Bratovich")
        self.url = reverse("characters:vampire:list:revenant_family")

    def test_list_url_resolves(self):
        self.assertEqual(self.url, "/characters/vampire/list/revenant_family/")

    def test_list_is_public(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/vampire/revenant_family/list.html")

    def test_list_shows_families_in_name_order(self):
        response = self.client.get(self.url)
        self.assertEqual(
            [family.name for family in response.context["object_list"]],
            ["Bratovich", "Zantosa"],
        )
        self.assertContains(response, "Zantosa")
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
$PY manage.py test characters.tests.views.vampire.test_revenant_family
```

Expected: `FAILED (errors=3)`, each `NoReverseMatch: Reverse for 'revenant_family' not found`.

- [ ] **Step 3: Implement.** In `characters/urls/vampire/index.py`, directly after the `clan/` entry:

```python
    path("clan/", views.vampire.VampireClanListView.as_view(), name="clan"),
```

insert:

```python
    path(
        "revenant_family/",
        views.vampire.RevenantFamilyListView.as_view(),
        name="revenant_family",
    ),
```

In `core/route_policy_manifest.py`, in the `PUBLIC_READ` block, directly after the line `characters.views.vampire.revenant_family.RevenantFamilyDetailView` add:

```
characters.views.vampire.revenant_family.RevenantFamilyListView
```

(`RevenantFamilyListView` is already exported from `characters/views/vampire/__init__.py`.)

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test characters.tests.views.vampire.test_revenant_family core.tests.security.test_route_policies
```

Expected: `Ran 7 tests ... OK`.

- [ ] **Step 5: Commit.**

```bash
git add characters/urls/vampire/index.py core/route_policy_manifest.py characters/tests/views/vampire/test_revenant_family.py
git commit -F - <<'EOF'
Route RevenantFamilyListView as characters:vampire:list:revenant_family

Every sibling vampire reference type has a public list route; the revenant
family list view and template existed but were unrouted (dead-code spec D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 39: [D9.2] Drone update routes

**Files:**
- Modify: `characters/urls/werewolf/update.py`
- Modify: `core/route_policy_manifest.py` (`OBJECT_WRITE`)
- Rewrite (currently a TODO stub): `characters/tests/views/werewolf/test_drone.py`

**Interfaces:**
- `characters:werewolf:update:drone` → `drone/<pk>/` → `characters.views.werewolf.drone.DroneCharacterCreationView` (the exact class name; it is **already** in the manifest as `ROUTER` because `GenericCharacterDetailView` maps `"drone"` to it, so the manifest does not change for this route).
- `characters:werewolf:update:drone_full` → `drone/full/<pk>/` → `characters.views.werewolf.drone.DroneUpdateView` (new `OBJECT_WRITE` entry).
- After this task `Drone.get_update_url()` (`Human.get_update_url`, builds `characters:werewolf:update:drone`) and `Drone.get_full_update_url()` (`...:drone_full`) resolve; today both raise `NoReverseMatch`.

- [ ] **Step 1: Write the failing test.** Replace the whole content of `characters/tests/views/werewolf/test_drone.py` with:

```python
"""Tests for the Drone update routes."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from characters.models.werewolf.drone import Drone
from characters.views.werewolf.drone import DroneCharacterCreationView, DroneUpdateView
from game.models import Chronicle


class TestDroneUpdateRoutes(TestCase):
    """Drone follows the fomor pattern: a router route and a full-edit route."""

    def setUp(self):
        self.player = User.objects.create_user("player", "p@test.com", "password")
        self.st = User.objects.create_user("st", "st@test.com", "password")
        self.other = User.objects.create_user("other", "o@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle", head_st=self.st)
        self.drone = Drone.objects.create(
            name="Test Drone",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            gnosis=1,
        )

    def test_update_url_resolves_to_creation_router(self):
        url = self.drone.get_update_url()
        self.assertEqual(url, f"/characters/werewolf/update/drone/{self.drone.pk}/")
        self.assertIs(resolve(url).func.view_class, DroneCharacterCreationView)

    def test_full_update_url_resolves_to_update_view(self):
        url = self.drone.get_full_update_url()
        self.assertEqual(url, f"/characters/werewolf/update/drone/full/{self.drone.pk}/")
        self.assertIs(resolve(url).func.view_class, DroneUpdateView)

    def test_st_can_open_full_update(self):
        self.client.force_login(self.st)
        response = self.client.get(self.drone.get_full_update_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/werewolf/drone/form.html")

    def test_st_can_save_full_update(self):
        self.client.force_login(self.st)
        url = self.drone.get_full_update_url()
        form = self.client.get(url).context["form"]
        data = {name: form[name].value() for name in form.fields if form[name].value() is not None}
        data.update({"name": "Renamed Drone", "gnosis": 3})
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.drone.refresh_from_db()
        self.assertEqual(self.drone.name, "Renamed Drone")
        self.assertEqual(self.drone.gnosis, 3)

    def test_unrelated_user_cannot_open_full_update(self):
        self.client.force_login(self.other)
        response = self.client.get(self.drone.get_full_update_url())
        self.assertEqual(response.status_code, 403)
```

(The save test round-trips the rendered form because, for a scoped ST, `DroneUpdateView.get_form_class()` returns a full Drone model form with every attribute/ability required, not just the three `fields` the class lists. The router GET itself is not exercised: the Drone chargen template extends the missing `characters/core/character/chargen.html`, a known Step 2 gap.)

- [ ] **Step 2: Run it and watch it fail.**

```bash
$PY manage.py test characters.tests.views.werewolf.test_drone
```

Expected: `FAILED (errors=5)`: `NoReverseMatch: Reverse for 'drone' not found` (router test) and `Reverse for 'drone_full' not found` (the other four).

- [ ] **Step 3: Implement.** In `characters/urls/werewolf/update.py`, directly before the entry

```python
    path(
        "werewolf/full/<pk>/",
```

insert:

```python
    path(
        "drone/<pk>/",
        views.werewolf.DroneCharacterCreationView.as_view(),
        name="drone",
    ),
    path(
        "drone/full/<pk>/",
        views.werewolf.DroneUpdateView.as_view(),
        name="drone_full",
    ),
```

In `core/route_policy_manifest.py`, in the `OBJECT_WRITE` block, directly before `characters.views.werewolf.fera.FeraUpdateView` add:

```
characters.views.werewolf.drone.DroneUpdateView
```

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test characters.tests.views.werewolf.test_drone core.tests.security.test_route_policies
```

Expected: `Ran 9 tests ... OK`. Then run D1's routed-template inventory, since this adds a URL route to a view whose chargen targets use a missing template:

```bash
$PY manage.py test core.tests.test_routed_templates
```

Expected: OK. If it reports the Drone chargen template under the new `drone/<pk>/` route, extend the existing Drone `KNOWN_MISSING` entry (owner: Step 2) to cover it rather than adding a new owner; the template gap itself is out of scope.

- [ ] **Step 5: Commit.**

```bash
git add characters/urls/werewolf/update.py core/route_policy_manifest.py characters/tests/views/werewolf/test_drone.py
git commit -F - <<'EOF'
Route Drone update pages like kinfolk/fomor

drone/<pk>/ goes to DroneCharacterCreationView (already a ROUTER target) and
drone/full/<pk>/ to DroneUpdateView (OBJECT_WRITE), so Drone.get_update_url
and get_full_update_url stop raising NoReverseMatch (dead-code spec D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 40: [D9.3] SeptPosition update route

**Files:**
- Modify: `characters/urls/werewolf/update.py`
- Modify: `core/route_policy_manifest.py` (`STAFF_WRITE`)
- Rewrite (currently a TODO stub): `characters/tests/views/werewolf/test_septposition.py`

**Interfaces:**
- `characters:werewolf:update:septposition` → `septposition/<pk>/` → `characters.views.werewolf.septposition.SeptPositionUpdateView` (existing; `form_class = SeptPositionForm`, template `characters/werewolf/septposition/form.html`).
- Manifest: `STAFF_WRITE` (matches `SeptPositionCreateView`). `SeptPosition.get_update_url()` already reverses this name.

- [ ] **Step 1: Write the failing test.** Replace the whole content of `characters/tests/views/werewolf/test_septposition.py` with:

```python
"""Tests for the SeptPosition views."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from characters.models.werewolf.septposition import SeptPosition
from characters.views.werewolf.septposition import SeptPositionUpdateView


class TestSeptPositionUpdateView(TestCase):
    """SeptPosition is reference data: only staff may edit it."""

    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        self.player = User.objects.create_user("player", "p@test.com", "password")
        self.position = SeptPosition.objects.create(name="Warder", description="Guards the caern.")
        self.url = self.position.get_update_url()

    def test_update_url_resolves(self):
        self.assertEqual(self.url, f"/characters/werewolf/update/septposition/{self.position.pk}/")
        self.assertIs(resolve(self.url).func.view_class, SeptPositionUpdateView)

    def test_staff_can_open_update(self):
        self.client.force_login(self.staff)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "characters/werewolf/septposition/form.html")

    def test_staff_can_save_update(self):
        self.client.force_login(self.staff)
        response = self.client.post(
            self.url, {"name": "Master of the Challenge", "description": "Rules on duels."}
        )
        self.assertEqual(response.status_code, 302)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Master of the Challenge")

    def test_non_staff_cannot_update(self):
        self.client.force_login(self.player)
        response = self.client.post(self.url, {"name": "Hijacked", "description": ""})
        self.assertEqual(response.status_code, 403)
        self.position.refresh_from_db()
        self.assertEqual(self.position.name, "Warder")
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
$PY manage.py test characters.tests.views.werewolf.test_septposition
```

Expected: `FAILED (errors=4)`, each `NoReverseMatch: Reverse for 'septposition' not found` (raised by `get_update_url()` in `setUp`).

- [ ] **Step 3: Implement.** In `characters/urls/werewolf/update.py`, directly before the entry

```python
    path(
        "battlescar/<pk>/",
```

insert:

```python
    path(
        "septposition/<pk>/",
        views.werewolf.SeptPositionUpdateView.as_view(),
        name="septposition",
    ),
```

In `core/route_policy_manifest.py`, in the `STAFF_WRITE` block, directly after `characters.views.werewolf.septposition.SeptPositionCreateView` add:

```
characters.views.werewolf.septposition.SeptPositionUpdateView
```

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test characters.tests.views.werewolf.test_septposition core.tests.security.test_route_policies
```

Expected: `Ran 8 tests ... OK`.

- [ ] **Step 5: Commit.**

```bash
git add characters/urls/werewolf/update.py core/route_policy_manifest.py characters/tests/views/werewolf/test_septposition.py
git commit -F - <<'EOF'
Route SeptPositionUpdateView at characters:werewolf:update:septposition

SeptPosition.get_update_url raised NoReverseMatch; every other Werewolf
reference type has an update route. Staff-only, like its create view
(dead-code spec D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 41: [D9.4] Tremere Chantry and Barrens list routes, create:tremere_chantry

**Files:**
- Modify: `locations/urls/vampire/index.py`
- Modify: `locations/urls/vampire/create.py`
- Modify: `core/route_policy_manifest.py` (`OBJECT_LIST`)
- Create: `locations/tests/views/vampire/test_chantry_barrens_routes.py`

**Interfaces:**
- `locations:vampire:list:tremere_chantry` → `/locations/vampire/list/tremere_chantry/` → `locations.views.vampire.TremereChantryListView` (template `locations/vampire/chantry/list.html`).
- `locations:vampire:list:barrens` → `/locations/vampire/list/barrens/` → `locations.views.vampire.BarrensListView` (template `locations/vampire/barrens/list.html`).
- `locations:vampire:create:tremere_chantry` → `/locations/vampire/create/tremere_chantry/` → `locations.views.vampire.TremereChantryCreateView` (already `OBJECT_CREATE`; the existing `create:chantry` name stays, because `chantry/list.html` links to it).
- These are the seeded `ObjectType` names (`populate_db/objects.py:52-53`), so `core.create_redirects.resolve_object_type_url("loc", "tremere_chantry"|"barrens", ...)` stops raising `Http404`. `create:barrens` already exists.
- Manifest: both list views in `OBJECT_LIST` like their routed siblings (non-staff GET gets the public projection).

- [ ] **Step 1: Write the failing test.** Create `locations/tests/views/vampire/test_chantry_barrens_routes.py`:

```python
"""Routes for the Tremere Chantry and Barrens object types (seeded names)."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from core.create_redirects import resolve_object_type_url
from game.models import ObjectType
from locations.models.vampire import Barrens, TremereChantry
from locations.views.vampire import (
    BarrensListView,
    TremereChantryCreateView,
    TremereChantryListView,
)


class TestSeededVampireLocationRoutes(TestCase):
    """The index resolves seeded type names; these three used to 404."""

    def setUp(self):
        ObjectType.objects.create(name="tremere_chantry", type="loc", gameline="vtm")
        ObjectType.objects.create(name="barrens", type="loc", gameline="vtm")

    def test_tremere_chantry_create_resolves(self):
        url = resolve_object_type_url("loc", "tremere_chantry", "create")
        self.assertEqual(url, "/locations/vampire/create/tremere_chantry/")
        self.assertIs(resolve(url).func.view_class, TremereChantryCreateView)

    def test_old_chantry_create_name_still_resolves(self):
        url = reverse("locations:vampire:create:chantry")
        self.assertIs(resolve(url).func.view_class, TremereChantryCreateView)

    def test_tremere_chantry_list_resolves(self):
        url = resolve_object_type_url("loc", "tremere_chantry", "list")
        self.assertEqual(url, "/locations/vampire/list/tremere_chantry/")
        self.assertIs(resolve(url).func.view_class, TremereChantryListView)

    def test_barrens_list_resolves(self):
        url = resolve_object_type_url("loc", "barrens", "list")
        self.assertEqual(url, "/locations/vampire/list/barrens/")
        self.assertIs(resolve(url).func.view_class, BarrensListView)

    def test_index_create_redirects_to_tremere_chantry_form(self):
        user = User.objects.create_user("player", "p@test.com", "password")
        self.client.force_login(user)
        response = self.client.post(
            reverse("locations:index"),
            {"action": "create", "loc_type": "tremere_chantry", "gameline": "vtm"},
        )
        self.assertRedirects(
            response, "/locations/vampire/create/tremere_chantry/", fetch_redirect_response=False
        )


class TestTremereChantryAndBarrensListViews(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        TremereChantry.objects.create(name="Vienna Chantry")
        Barrens.objects.create(name="Rust Belt")

    def test_staff_sees_tremere_chantry_list(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("locations:vampire:list:tremere_chantry"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/vampire/chantry/list.html")
        self.assertContains(response, "Vienna Chantry")

    def test_staff_sees_barrens_list(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("locations:vampire:list:barrens"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/vampire/barrens/list.html")
        self.assertContains(response, "Rust Belt")

    def test_anonymous_list_gets_public_projection(self):
        for name in ("tremere_chantry", "barrens"):
            with self.subTest(name=name):
                response = self.client.get(reverse(f"locations:vampire:list:{name}"))
                self.assertEqual(response.status_code, 200)
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
$PY manage.py test locations.tests.views.vampire.test_chantry_barrens_routes
```

Expected: `FAILED (failures=1, errors=7)`: `NoReverseMatch`/`Http404: Unsupported object type route` for the new names, and `test_index_create_redirects_to_tremere_chantry_form` fails with `404 != 302`. (`test_old_chantry_create_name_still_resolves` already passes; it guards against renaming.)

- [ ] **Step 3: Implement.** In `locations/urls/vampire/index.py`, append after the last entry (the `racks/` path, whose closing lines are `        name="rack",` / `    ),`) and before the closing `]`:

```python
    path(
        "tremere_chantry/",
        views.vampire.TremereChantryListView.as_view(),
        name="tremere_chantry",
    ),
    path(
        "barrens/",
        views.vampire.BarrensListView.as_view(),
        name="barrens",
    ),
```

In `locations/urls/vampire/create.py`, directly after the existing entry

```python
    path(
        "chantry/",
        views.vampire.TremereChantryCreateView.as_view(),
        name="chantry",
    ),
```

insert:

```python
    path(
        "tremere_chantry/",
        views.vampire.TremereChantryCreateView.as_view(),
        name="tremere_chantry",
    ),
```

In `core/route_policy_manifest.py`, in the `OBJECT_LIST` block: directly after `locations.views.mummy.UndergroundSanctuaryListView` add `locations.views.vampire.BarrensListView`, and directly after `locations.views.vampire.RackListView` add `locations.views.vampire.TremereChantryListView`, so the block reads:

```
locations.views.mummy.UndergroundSanctuaryListView
locations.views.vampire.BarrensListView
locations.views.vampire.DomainListView
locations.views.vampire.ElysiumListView
locations.views.vampire.HavenListView
locations.views.vampire.RackListView
locations.views.vampire.TremereChantryListView
```

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test locations.tests.views.vampire.test_chantry_barrens_routes core.tests.security.test_route_policies
```

Expected: `Ran 12 tests ... OK`.

- [ ] **Step 5: Commit.**

```bash
git add locations/urls/vampire/index.py locations/urls/vampire/create.py core/route_policy_manifest.py locations/tests/views/vampire/test_chantry_barrens_routes.py
git commit -F - <<'EOF'
Route Tremere Chantry/Barrens lists and create:tremere_chantry

The location index resolves seeded object-type names; tremere_chantry
(create, list) and barrens (list) had no route and returned 404. The list
views and templates already existed. create:chantry is kept
(dead-code spec D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 42: [D9.5] Freehold PowerChoices checkboxes

**Files:**
- Modify: `locations/forms/changeling/creation.py` (`FreeholdPowersForm`)
- Modify: `locations/forms/changeling/freehold.py` (`FreeholdForm`)
- Modify: `locations/tests/forms/changeling/test_freehold.py` (new class + import)
- Rewrite (currently a TODO stub): `locations/tests/forms/changeling/test_creation.py`

**Interfaces:**
- Both forms declare `powers = forms.MultipleChoiceField(choices=PowerChoices.choices, widget=forms.CheckboxSelectMultiple, required=False)`; the `"powers": forms.CheckboxSelectMultiple()` entry leaves `Meta.widgets`.
- Storage: `Freehold.powers` is `JSONField(default=list, blank=True)`. `MultipleChoiceField.clean()` returns a `list[str]`, `construct_instance` assigns it, and the JSONField stores/loads it as a list; `model_to_dict` gives the stored list back as `initial`, so saved powers render checked. Verified in the tests below. Unknown values are now rejected (`"Select a valid choice"`), which the JSON form field accepted before.

- [ ] **Step 1: Write the failing tests.** In `locations/tests/forms/changeling/test_freehold.py` change the import

```python
from locations.models.changeling.freehold import Freehold
```

to

```python
from locations.models.changeling.freehold import Freehold, PowerChoices
```

and append at the end of the file:

```python


class TestFreeholdFormPowerChoices(TestFreeholdFormSetup):
    """The powers checkboxes offer PowerChoices and round-trip through the JSONField."""

    def _data(self, **overrides):
        data = {
            "name": "Choice Freehold",
            "description": "Tests power choices",
            "archetype": "homestead",
            "balefire": 1,
            "size": 1,
            "sanctuary": 0,
            "resources": 0,
            "passages": 1,
            "gauntlet": 7,
            "shroud": 7,
            "dimension_barrier": 6,
        }
        data.update(overrides)
        return data

    def test_powers_field_offers_power_choices(self):
        form = FreeholdForm()
        self.assertEqual(list(form.fields["powers"].choices), list(PowerChoices.choices))
        self.assertFalse(form.fields["powers"].required)

    def test_powers_render_as_checkboxes(self):
        html = str(FreeholdForm()["powers"])
        for value, _label in PowerChoices.choices:
            self.assertIn(f'value="{value}"', html)

    def test_chosen_power_is_saved_as_list(self):
        form = FreeholdForm(data=self._data(powers=["warning_call"]))
        self.assertTrue(form.is_valid(), form.errors)
        freehold = form.save()
        freehold.refresh_from_db()
        self.assertEqual(freehold.powers, ["warning_call"])

    def test_unknown_power_is_rejected(self):
        form = FreeholdForm(data=self._data(powers=["not_a_power"]))
        self.assertFalse(form.is_valid())
        self.assertIn("powers", form.errors)

    def test_no_power_saves_empty_list(self):
        form = FreeholdForm(data=self._data())
        self.assertTrue(form.is_valid(), form.errors)
        freehold = form.save()
        freehold.refresh_from_db()
        self.assertEqual(freehold.powers, [])

    def test_saved_powers_are_checked_when_editing(self):
        freehold = Freehold.objects.create(
            name="Existing", archetype="homestead", powers=["resonant_dreams"]
        )
        html = str(FreeholdForm(instance=freehold)["powers"])
        self.assertRegex(html, r'value="resonant_dreams"[^>]*checked')
```

Replace the whole content of `locations/tests/forms/changeling/test_creation.py` with:

```python
"""Tests for the multi-step Freehold creation forms."""

from django.test import TestCase

from locations.forms.changeling.creation import FreeholdPowersForm
from locations.models.changeling.freehold import Freehold, PowerChoices


class TestFreeholdPowersForm(TestCase):
    """Step 3 offers PowerChoices as checkboxes and saves the chosen list."""

    def setUp(self):
        self.freehold = Freehold.objects.create(name="Step Three", archetype="homestead")

    def test_powers_field_offers_power_choices(self):
        form = FreeholdPowersForm(instance=self.freehold)
        self.assertEqual(list(form.fields["powers"].choices), list(PowerChoices.choices))
        self.assertFalse(form.fields["powers"].required)
        html = str(form["powers"])
        for value, _label in PowerChoices.choices:
            self.assertIn(f'value="{value}"', html)

    def test_chosen_powers_are_saved(self):
        form = FreeholdPowersForm(
            data={"powers": ["warning_call", "glamour_to_dross"]}, instance=self.freehold
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.freehold.refresh_from_db()
        self.assertEqual(self.freehold.powers, ["warning_call", "glamour_to_dross"])
        self.assertTrue(self.freehold.has_power("glamour_to_dross"))

    def test_unknown_power_is_rejected(self):
        form = FreeholdPowersForm(data={"powers": ["not_a_power"]}, instance=self.freehold)
        self.assertFalse(form.is_valid())
        self.assertIn("powers", form.errors)

    def test_dual_nature_still_requires_second_archetype(self):
        form = FreeholdPowersForm(data={"powers": ["dual_nature"]}, instance=self.freehold)
        self.assertFalse(form.is_valid())
```

- [ ] **Step 2: Run them and watch them fail.**

```bash
$PY manage.py test locations.tests.forms.changeling.test_freehold locations.tests.forms.changeling.test_creation
```

Expected: `FAILED (failures=4, errors=2)`: `AttributeError: 'JSONField' object has no attribute 'choices'` (x2), the checkbox render/checked tests find only `<div id="id_powers">\n</div>` with no inputs, and both `test_unknown_power_is_rejected` get `True is not false`. (The save tests already pass: the JSON form field passes a list through; they guard the round trip.)

- [ ] **Step 3: Implement `FreeholdPowersForm`.** In `locations/forms/changeling/creation.py`, below `from locations.models.changeling import Freehold` add:

```python
from locations.models.changeling.freehold import PowerChoices
```

and replace

```python
class FreeholdPowersForm(forms.ModelForm):
    """Step 3: Powers selection"""

    class Meta:
        model = Freehold
        fields = ("powers", "dual_nature_archetype", "dual_nature_ability")
        widgets = {
            "powers": forms.CheckboxSelectMultiple(),
        }
```

with

```python
class FreeholdPowersForm(forms.ModelForm):
    """Step 3: Powers selection"""

    powers = forms.MultipleChoiceField(
        choices=PowerChoices.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Freehold
        fields = ("powers", "dual_nature_archetype", "dual_nature_ability")
```

- [ ] **Step 4: Implement `FreeholdForm`.** In `locations/forms/changeling/freehold.py`, below `from locations.models.changeling import Freehold` add:

```python
from locations.models.changeling.freehold import PowerChoices
```

replace

```python
class FreeholdForm(forms.ModelForm):
    """Form for creating and editing Freeholds"""

    class Meta:
```

with

```python
class FreeholdForm(forms.ModelForm):
    """Form for creating and editing Freeholds"""

    powers = forms.MultipleChoiceField(
        choices=PowerChoices.choices,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
```

and delete the last `Meta.widgets` entry (keep the closing `}` of the dict):

```python
            "powers": forms.CheckboxSelectMultiple(),
```

- [ ] **Step 5: Run and pass**, including the existing Freehold view/model tests:

```bash
$PY manage.py test locations.tests.forms.changeling locations.tests.views.changeling locations.tests.models.changeling
```

Expected: `Ran 122 tests ... OK`.

- [ ] **Step 6: Commit.**

```bash
git add locations/forms/changeling/creation.py locations/forms/changeling/freehold.py locations/tests/forms/changeling/test_freehold.py locations/tests/forms/changeling/test_creation.py
git commit -F - <<'EOF'
Offer Freehold PowerChoices in FreeholdForm and FreeholdPowersForm

powers is a JSONField, so its CheckboxSelectMultiple rendered no choices and
no power could be picked. Declare it as a MultipleChoiceField over
PowerChoices; the chosen list round-trips through the JSONField and unknown
values are rejected (dead-code spec D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 43: [D9.6] Reliquary damage bar on the detail page

**Files:**
- Modify: `locations/templates/locations/demon/reliquary/display_includes/basics.html`
- Delete: `locations/templates/locations/demon/reliquary/display_includes/health.html`
- Rewrite (currently a TODO stub): `locations/tests/views/demon/test_reliquary.py`

**Interfaces:**
- Uses existing `Reliquary.is_damaged()` and `Reliquary.damage_percentage()` (their only template user was the orphan). `health.html`'s Pervasiveness/Manifestation cells are already in `basics.html`, so only the bar moves.

- [ ] **Step 1: Write the failing test.** Replace the whole content of `locations/tests/views/demon/test_reliquary.py` with:

```python
"""Tests for the Reliquary detail page."""

from django.contrib.auth.models import User
from django.test import TestCase

from locations.models.demon.reliquary import Reliquary


class TestReliquaryDetailDamageBar(TestCase):
    """The Health cell shows a damage bar once the reliquary is damaged."""

    def setUp(self):
        self.staff = User.objects.create_user("staff", "s@test.com", "password", is_staff=True)
        self.client.force_login(self.staff)

    def test_damaged_reliquary_shows_damage_bar(self):
        reliquary = Reliquary.objects.create(
            name="Cracked Idol", max_health_levels=20, current_health_levels=15
        )
        response = self.client.get(reliquary.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "15/20")
        self.assertContains(response, 'class="progress-bar bg-danger"')
        self.assertContains(response, 'aria-valuenow="25.0"')
        self.assertContains(response, "25% damaged")

    def test_undamaged_reliquary_has_no_damage_bar(self):
        reliquary = Reliquary.objects.create(
            name="Pristine Idol", max_health_levels=20, current_health_levels=20
        )
        response = self.client.get(reliquary.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "20/20")
        self.assertNotContains(response, "progress-bar")
        self.assertNotContains(response, "% damaged")
```

- [ ] **Step 2: Run it and watch it fail.**

```bash
$PY manage.py test locations.tests.views.demon.test_reliquary
```

Expected: `FAILED (failures=1)`: `Couldn't find 'class="progress-bar bg-danger"'` in `test_damaged_reliquary_shows_damage_bar` (the undamaged test already passes and guards the `{% if %}`).

- [ ] **Step 3: Implement.** In `locations/templates/locations/demon/reliquary/display_includes/basics.html`, in the Health cell, directly after this line (it occurs once):

```html
                            <span style="font-weight: 700; color: var(--theme-text-primary);">{{ object.current_health_levels }}/{{ object.max_health_levels }}</span>
```

insert:

```html
                            {% if object.is_damaged %}
                                <div class="progress mt-2" style="height: 8px; min-width: 120px;">
                                    <div class="progress-bar bg-danger" role="progressbar"
                                         style="width: {{ object.damage_percentage }}%;"
                                         aria-valuenow="{{ object.damage_percentage }}"
                                         aria-valuemin="0" aria-valuemax="100">
                                    </div>
                                </div>
                                <small class="text-danger">{{ object.damage_percentage|floatformat:0 }}% damaged</small>
                            {% endif %}
```

(`min-width` because the cell is an `inline-block` sized by its text; without it the bar collapses.) Then delete the orphan:

```bash
git rm locations/templates/locations/demon/reliquary/display_includes/health.html
grep -rn "reliquary/display_includes/health" --include=*.py --include=*.html . | grep -v /docs/
```

Expected grep output: nothing (only the generated `docs/**/codemap.html` reports mention it; leave those).

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test locations.tests.views.demon.test_reliquary
```

Expected: `Ran 2 tests ... OK`.

- [ ] **Step 5: Commit.**

```bash
git add locations/templates/locations/demon/reliquary/display_includes/basics.html locations/templates/locations/demon/reliquary/display_includes/health.html locations/tests/views/demon/test_reliquary.py
git commit -F - <<'EOF'
Show the Reliquary damage bar in the detail page's Health cell

The bar lived only in the unreferenced health.html include, so the detail
page showed health numbers without it. Move it into basics.html and delete
the orphan (dead-code spec D9).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 44: [D9.7] Periapt.clean() rules, then delete PeriaptForm

**Files:**
- Modify: `items/models/mage/periapt.py`
- Modify: `items/tests/models/mage/test_periapt.py`
- Delete: `items/forms/mage/periapt.py`, `items/tests/forms/mage/test_periapt.py`
- Modify: `items/forms/mage/__init__.py`

**Interfaces:**
- `Periapt.clean(self) -> None`: calls `super().clean()` (core `Model.clean`: name/status/image_status), then raises one `ValidationError([...])` holding every broken rule, as **non-field** errors, with the messages copied verbatim from `PeriaptForm.clean()`:
  - `arete < rank` → `"Periapt Arete rating must be at least equal to rank"` (code `arete_below_rank`);
  - `current_charges > max_charges` → `"Current charges cannot exceed maximum charges"` (code `charges_exceed_max`).
- Periapt has no `clean()` of its own today (neither does `Wonder`/`ItemModel`); core `Model.save()` calls `full_clean()`, so these rules now guard every save. Every existing `Periapt.objects.create(...)` in the repo uses `rank=0` and `current_charges <= max_charges` (checked: `items/tests/models/mage/test_periapt.py`, `items/tests/forms/mage/test_periapt.py`; `populate_db` creates no Periapts).
- Non-field errors, not field-keyed: `PeriaptForm` raised them as non-field errors; `core/form.html` renders `form.non_field_errors` while the periapt template renders `{{ form.arete }}` without field errors; and a model form that omits `arete`/`current_charges` would raise `ValueError` on a field-keyed model error.
- The PeriaptForm's other rules (resonance total ≥ rank, one power, effect cost, 3×rank point budget) depend on its formsets and are **not** recovered (spec recovers only the two rules that "exist nowhere else").

- [ ] **Step 1: Write the failing tests.** In `items/tests/models/mage/test_periapt.py` change the imports

```python
from django.contrib.auth.models import User
from django.test import TestCase
```

to

```python
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
```

and append at the end of the file:

```python


class TestPeriaptClean(TestCase):
    """Rules recovered from the deleted Periapt form: arete >= rank, charges <= max."""

    def test_arete_below_rank_is_rejected(self):
        periapt = Periapt(name="Weak", rank=3, arete=2)
        with self.assertRaises(ValidationError) as ctx:
            periapt.full_clean()
        self.assertIn("Periapt Arete rating must be at least equal to rank", ctx.exception.messages)

    def test_save_refuses_arete_below_rank(self):
        with self.assertRaises(ValidationError):
            Periapt.objects.create(name="Weak", rank=3, arete=2)
        self.assertFalse(Periapt.objects.filter(name="Weak").exists())

    def test_arete_equal_to_rank_is_valid(self):
        periapt = Periapt.objects.create(name="Balanced", rank=3, arete=3)
        self.assertEqual(periapt.arete, 3)

    def test_current_charges_above_max_is_rejected(self):
        periapt = Periapt(name="Overfull", max_charges=2, current_charges=3)
        with self.assertRaises(ValidationError) as ctx:
            periapt.full_clean()
        self.assertIn("Current charges cannot exceed maximum charges", ctx.exception.messages)

    def test_current_charges_equal_to_max_is_valid(self):
        periapt = Periapt.objects.create(name="Full", max_charges=2, current_charges=2)
        self.assertEqual(periapt.current_charges, 2)

    def test_both_rules_are_reported_together(self):
        periapt = Periapt(name="Broken", rank=2, arete=1, max_charges=1, current_charges=5)
        with self.assertRaises(ValidationError) as ctx:
            periapt.full_clean()
        self.assertEqual(len(ctx.exception.messages), 2)

    def test_create_view_shows_rule_as_form_error(self):
        user = User.objects.create_user(username="maker", password="password")
        self.client.force_login(user)
        response = self.client.post(
            Periapt.get_creation_url(),
            {
                "name": "Weak Periapt",
                "description": "Too little Arete",
                "rank": 3,
                "background_cost": 0,
                "quintessence_max": 0,
                "arete": 1,
                "max_charges": 1,
                "current_charges": 1,
                "is_consumable": "on",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Periapt Arete rating must be at least equal to rank",
            response.context["form"].non_field_errors(),
        )
        self.assertContains(response, "Periapt Arete rating must be at least equal to rank")
        self.assertFalse(Periapt.objects.filter(name="Weak Periapt").exists())
```

- [ ] **Step 2: Run them and watch them fail.**

```bash
$PY manage.py test items.tests.models.mage.test_periapt
```

Expected: `FAILED (failures=5)`: four `ValidationError not raised` and `test_create_view_shows_rule_as_form_error` with `302 != 200` (the weak periapt is created today).

- [ ] **Step 3: Implement.** In `items/models/mage/periapt.py` add the import at the top:

```python
from django.core.exceptions import ValidationError
```

(directly above `from django.core.validators import MaxValueValidator, MinValueValidator`), and insert this method directly before `def get_update_url(self):`:

```python
    def clean(self):
        """Periapt rules (formerly only in the deleted Periapt form): arete >= rank, charges <= max.

        Raised as non-field errors so any ModelForm shows them, whichever
        fields it includes.
        """
        super().clean()
        errors = []
        if self.arete is not None and self.rank is not None and self.arete < self.rank:
            errors.append(
                ValidationError(
                    "Periapt Arete rating must be at least equal to rank",
                    code="arete_below_rank",
                )
            )
        if (
            self.current_charges is not None
            and self.max_charges is not None
            and self.current_charges > self.max_charges
        ):
            errors.append(
                ValidationError(
                    "Current charges cannot exceed maximum charges",
                    code="charges_exceed_max",
                )
            )
        if errors:
            raise ValidationError(errors)

```

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test items.tests.models.mage.test_periapt
```

Expected: `Ran 30 tests ... OK`.

- [ ] **Step 5: Delete `PeriaptForm` (left for this task by D7).** First confirm it has no users outside its own module and test:

```bash
grep -rn "PeriaptForm\|PeriaptResonanceRatingFormSet\|forms.mage.periapt\|forms/mage/periapt" --include=*.py --include=*.html . | grep -v "^./items/forms/mage/periapt.py\|^./items/tests/forms/mage/test_periapt.py"
```

Expected: exactly one hit, `./items/forms/mage/__init__.py:1:from .periapt import PeriaptForm` (generated `docs/**/*.html` reports are ignored by the `--include`). Then:

```bash
git rm items/forms/mage/periapt.py items/tests/forms/mage/test_periapt.py
```

In `items/forms/mage/__init__.py` delete the line `from .periapt import PeriaptForm` and remove `"PeriaptForm"` from `__all__` (after D7 the file is `from .wonder import WonderForm` / `__all__ = ["WonderForm"]`; if D7 has not removed `SorcererArtifactForm` yet, leave that line and entry alone). Re-run the grep: expected no output.

- [ ] **Step 6: Run and pass** the whole items app (the deleted test module must not be collected, and nothing may import the deleted form):

```bash
$PY manage.py test items
```

Expected: OK, with exactly 36 fewer tests than before Step 5 (the 36 tests of the deleted `items/tests/forms/mage/test_periapt.py`; compare the `Ran N tests` lines).

- [ ] **Step 7: Commit.**

```bash
git add items/models/mage/periapt.py items/tests/models/mage/test_periapt.py items/forms/mage/__init__.py items/forms/mage/periapt.py items/tests/forms/mage/test_periapt.py
git commit -F - <<'EOF'
Move Periapt arete/charge rules into Periapt.clean(); delete PeriaptForm

PeriaptForm was superseded by the fields=[...] views, but two of its rules
existed nowhere else: Arete at least equal to rank, and current charges at
most max charges. They are now model rules (non-field errors, same
messages), so every save and every model form enforces them. The unused
form module and its tests are deleted (dead-code spec D9, D7).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**

```bash
$PY manage.py test 2>&1 | tee /tmp/d9-suite.log | tail -3     # serial, ~40 min
grep -E "^(FAIL|ERROR):" /tmp/d9-suite.log
$PY manage.py check
$PY manage.py test core.tests.security.test_route_policies
$PY manage.py test core.tests.test_routed_templates
$PY manage.py shell -c "from django.urls import URLResolver, get_resolver; c = lambda ps: sum(c(p.url_patterns) if isinstance(p, URLResolver) else 1 for p in ps); print(c(get_resolver().url_patterns))"
$RUFF check characters/urls/vampire/index.py characters/urls/werewolf/update.py locations/urls/vampire/index.py locations/urls/vampire/create.py locations/forms/changeling/creation.py locations/forms/changeling/freehold.py items/models/mage/periapt.py items/forms/mage/__init__.py core/route_policy_manifest.py characters/tests/views/vampire/test_revenant_family.py characters/tests/views/werewolf/test_drone.py characters/tests/views/werewolf/test_septposition.py locations/tests/views/vampire/test_chantry_barrens_routes.py locations/tests/forms/changeling/test_freehold.py locations/tests/forms/changeling/test_creation.py locations/tests/views/demon/test_reliquary.py items/tests/models/mage/test_periapt.py
$RUFF format --check characters/urls/vampire/index.py characters/urls/werewolf/update.py locations/urls/vampire/index.py locations/urls/vampire/create.py locations/forms/changeling/freehold.py items/models/mage/periapt.py items/forms/mage/__init__.py characters/tests/views/vampire/test_revenant_family.py characters/tests/views/werewolf/test_drone.py characters/tests/views/werewolf/test_septposition.py locations/tests/views/vampire/test_chantry_barrens_routes.py locations/tests/forms/changeling/test_freehold.py locations/tests/forms/changeling/test_creation.py locations/tests/views/demon/test_reliquary.py items/tests/models/mage/test_periapt.py
```

Pass criteria: the suite's `FAIL:`/`ERROR:` lines are **empty** except for the spec's five baseline failures (*Removal safety*: the three vampire `test_basics_view_creates_*`, `test_create_circle_successfully`, `test_other_player_cannot_attach_companion_to_mage`), and none of them if an earlier unit fixed them; `check` reports no issues; the route-policy and routed-template tests pass; the route count is exactly **7** higher than the count recorded at the start of the unit; `ruff check` passes. `core/route_policy_manifest.py` and `locations/forms/changeling/creation.py` are left out of `format --check` because they already fail it at HEAD (`1e77e23`) for lines this unit does not touch; do not reformat them here.

## Unit D10: Story XP awards

Recovers `accounts.forms.StoryXP` (spec *Story XP awards*). `Story` has no chronicle and scenes don't link to stories; the only story-to-character link is `game.models.StoryXPRequest` (`story` FK, `character` FK to `characters.CharacterModel`, booleans `success`/`danger`/`growth`/`drama`, int `duration`; reverse accessor `story.storyxprequest_set`). `Story.award_xp(character_awards)` stays the single write path: it maps each categories dict through `core.xp_utils.calculate_story_xp` (duration + 1 per true category) and calls `award_xp_atomically(Story, pk, map)`, which locks the story, raises `ValidationError(code="xp_already_given")` if `xp_given`, adds XP to each `Character` (by pk), and sets `xp_given=True`, all in one transaction.

D10 adds exactly **1** URL pattern. Record the route count before starting (same command as D9).

### Task 45: [D10.1] Rebuild StoryXP around the story's requests

**Files:**
- Modify: `accounts/forms.py`
- Modify: `accounts/tests/forms/test_forms.py` (rewrite `TestStoryXPForm`, extend the `game.models` import)

**Interfaces:**
- Module constant `accounts.forms.STORY_XP_CATEGORIES = ("success", "danger", "growth", "drama")`.
- `StoryXP(data=None, *, story, prefix=None, ...)`:
  - `self.story`; `self.xp_requests: list[StoryXPRequest]` = the story's requests with a character, each `xp_request.character` replaced by its real subclass instance (one polymorphic `in_bulk` query), sorted by `(character.name, pk)`.
  - Fields per request pk `N`: `N-success`, `N-danger`, `N-growth`, `N-drama` (`BooleanField(required=False, initial=<request value>)`), `N-duration` (`IntegerField(min_value=0, required=False, initial=request.duration)`).
  - `characters` (property) → `list` of the requests' characters in row order.
  - `rows()` → `list[tuple[StoryXPRequest, list[BoundField]]]`, fields in order success, danger, growth, drama, duration (the template uses it).
  - `user_can_award(user, request=None) -> bool`: `False` with no requests; `True` for staff/superuser; else `True` only if `PermissionManager.user_has_scoped_editor_role(user, character, request=request)` holds for **every** character.
  - `clean()` → `{character: {"success": bool, "danger": bool, "growth": bool, "drama": bool, "duration": int}}`; duplicate requests for one character are merged (booleans OR, duration max), never summed.
  - `save(commit=True)` → `self.story.award_xp(self.cleaned_data)` (returns the awarded count; raises `ValidationError` on a second award).
- `accounts/forms.py` stops importing `Human` (its only user was the old `StoryXP`) and imports `CharacterModel` and `PermissionManager` instead.

- [ ] **Step 1: Write the failing tests.** In `accounts/tests/forms/test_forms.py` change

```python
from game.models import Chronicle, Scene, Story
```

to

```python
from game.models import Chronicle, Scene, Story, StoryXPRequest
```

and replace the whole `class TestStoryXPForm(TestCase):` block (everything up to, not including, `class TestCustomAuthenticationForm(TestCase):`) with:

```python
class TestStoryXPForm(TestCase):
    """StoryXP builds one row per StoryXPRequest of the story."""

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.chronicle = Chronicle.objects.create(name="Test Chronicle")
        self.story = Story.objects.create(name="Test Story")
        self.other_story = Story.objects.create(name="Other Story")
        self.char1 = Human.objects.create(
            name="Character One",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.char2 = Human.objects.create(
            name="Character Two",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.bystander = Human.objects.create(
            name="Bystander",
            owner=self.user,
            chronicle=self.chronicle,
            concept="Test",
            status="App",
        )
        self.request1 = StoryXPRequest.objects.create(
            story=self.story, character=self.char1, success=True, duration=2
        )
        self.request2 = StoryXPRequest.objects.create(
            story=self.story, character=self.char2, danger=True
        )
        StoryXPRequest.objects.create(story=self.other_story, character=self.bystander)

    def _data(self, request, success="", danger="", growth="", drama="", duration="0"):
        return {
            f"{request.pk}-success": success,
            f"{request.pk}-danger": danger,
            f"{request.pk}-growth": growth,
            f"{request.pk}-drama": drama,
            f"{request.pk}-duration": duration,
        }

    def test_form_lists_only_the_storys_requested_characters(self):
        form = StoryXP(story=self.story)
        self.assertEqual(form.characters, [self.char1, self.char2])
        self.assertNotIn(self.bystander, form.characters)
        self.assertEqual(
            set(form.fields),
            {
                f"{request.pk}-{name}"
                for request in (self.request1, self.request2)
                for name in ("success", "danger", "growth", "drama", "duration")
            },
        )

    def test_fields_are_prefilled_from_the_request(self):
        form = StoryXP(story=self.story)
        self.assertTrue(form.fields[f"{self.request1.pk}-success"].initial)
        self.assertFalse(form.fields[f"{self.request1.pk}-danger"].initial)
        self.assertEqual(form.fields[f"{self.request1.pk}-duration"].initial, 2)
        self.assertTrue(form.fields[f"{self.request2.pk}-danger"].initial)

    def test_rows_pair_each_request_with_its_fields(self):
        form = StoryXP(story=self.story)
        rows = form.rows()
        self.assertEqual([request for request, _fields in rows], [self.request1, self.request2])
        self.assertEqual(
            [field.name for field in rows[0][1]],
            [f"{self.request1.pk}-{name}" for name in ("success", "danger", "growth", "drama")]
            + [f"{self.request1.pk}-duration"],
        )

    def test_clean_returns_categories_per_character(self):
        data = self._data(self.request1, success="on", danger="on", duration="2")
        data.update(self._data(self.request2, drama="on", duration="1"))
        form = StoryXP(data=data, story=self.story)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data,
            {
                self.char1: {
                    "success": True,
                    "danger": True,
                    "growth": False,
                    "drama": False,
                    "duration": 2,
                },
                self.char2: {
                    "success": False,
                    "danger": False,
                    "growth": False,
                    "drama": True,
                    "duration": 1,
                },
            },
        )

    def test_duplicate_requests_for_one_character_are_merged_not_summed(self):
        duplicate = StoryXPRequest.objects.create(story=self.story, character=self.char1)
        data = self._data(self.request1, success="on", duration="2")
        data.update(self._data(self.request2))
        data.update(self._data(duplicate, growth="on", duration="1"))
        form = StoryXP(data=data, story=self.story)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(
            form.cleaned_data[self.char1],
            {"success": True, "danger": False, "growth": True, "drama": False, "duration": 2},
        )

    def test_duration_must_be_a_non_negative_integer(self):
        data = self._data(self.request1, duration="not_an_integer")
        data.update(self._data(self.request2, duration="-1"))
        form = StoryXP(data=data, story=self.story)
        self.assertFalse(form.is_valid())
        self.assertIn(f"{self.request1.pk}-duration", form.errors)
        self.assertIn(f"{self.request2.pk}-duration", form.errors)

    def test_save_awards_computed_xp_and_marks_story(self):
        data = self._data(self.request1, success="on", danger="on", duration="2")
        data.update(self._data(self.request2, drama="on"))
        form = StoryXP(data=data, story=self.story)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.char1.refresh_from_db()
        self.char2.refresh_from_db()
        self.story.refresh_from_db()
        self.assertEqual(self.char1.xp, 4)
        self.assertEqual(self.char2.xp, 1)
        self.assertTrue(self.story.xp_given)


```

- [ ] **Step 2: Run them and watch them fail.**

```bash
$PY manage.py test accounts.tests.forms.test_forms.TestStoryXPForm
```

Expected: `FAILED (failures=4, errors=3)`: `KeyError: '<pk>-success'`, `'StoryXP' object has no attribute 'characters'` / `'rows'`, and the clean/save tests see every approved Human (including "Bystander") with all-false categories.

- [ ] **Step 3: Implement.** In `accounts/forms.py` replace

```python
from accounts.models import Profile
from characters.models.core.human import Human
```

with

```python
from accounts.models import Profile
from characters.models.core.character import CharacterModel
from core.permissions import PermissionManager

STORY_XP_CATEGORIES = ("success", "danger", "growth", "drama")
```

and replace the whole `class StoryXP(forms.Form):` block (up to, not including, `class FreebieAwardForm(forms.Form):`) with:

```python
class StoryXP(forms.Form):
    """Award story XP from the story's StoryXPRequest rows.

    One row per request, keyed by the request pk and pre-filled from it; the
    ST may change any value before submitting. ``clean()`` returns
    ``{character: {"success", "danger", "growth", "drama", "duration"}}``.
    """

    def __init__(self, *args, **kwargs):
        self.story = kwargs.pop("story")
        super().__init__(*args, **kwargs)
        requests = list(
            self.story.storyxprequest_set.filter(character__isnull=False).order_by("pk")
        )
        # Polymorphic in_bulk returns each character as its real subclass.
        characters = CharacterModel.objects.in_bulk([r.character_id for r in requests])
        for xp_request in requests:
            xp_request.character = characters[xp_request.character_id]
        self.xp_requests = sorted(requests, key=lambda r: (r.character.name, r.pk))
        for xp_request in self.xp_requests:
            for category in STORY_XP_CATEGORIES:
                self.fields[f"{xp_request.pk}-{category}"] = forms.BooleanField(
                    required=False,
                    initial=getattr(xp_request, category),
                    label=category.title(),
                )
            self.fields[f"{xp_request.pk}-duration"] = forms.IntegerField(
                min_value=0,
                initial=xp_request.duration,
                required=False,
                label="Duration",
                widget=forms.NumberInput(attrs={"size": "5"}),
            )

    @property
    def characters(self):
        """Characters with a request for this story, in row order."""
        return [xp_request.character for xp_request in self.xp_requests]

    def rows(self):
        """``(request, [success, danger, growth, drama, duration])`` bound fields per row."""
        names = (*STORY_XP_CATEGORIES, "duration")
        return [
            (xp_request, [self[f"{xp_request.pk}-{name}"] for name in names])
            for xp_request in self.xp_requests
        ]

    def user_can_award(self, user, request=None):
        """Staff, or a scoped ST for every requested character; never partial."""
        if not self.xp_requests:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return all(
            PermissionManager.user_has_scoped_editor_role(user, character, request=request)
            for character in self.characters
        )

    def save(self, commit=True):
        """Award through Story.award_xp (atomic; refuses a second award)."""
        return self.story.award_xp(self.cleaned_data)

    def clean(self):
        cleaned_data = super().clean()
        awards = {}
        for xp_request in self.xp_requests:
            categories = {
                category: cleaned_data.get(f"{xp_request.pk}-{category}", False)
                for category in STORY_XP_CATEGORIES
            }
            categories["duration"] = cleaned_data.get(f"{xp_request.pk}-duration") or 0
            previous = awards.get(xp_request.character)
            if previous is not None:
                # Duplicate requests for one character merge; they never add up.
                categories = {
                    **{c: previous[c] or categories[c] for c in STORY_XP_CATEGORIES},
                    "duration": max(previous["duration"], categories["duration"]),
                }
            awards[xp_request.character] = categories
        return awards


```

- [ ] **Step 4: Run and pass.**

```bash
$PY manage.py test accounts.tests.forms.test_forms
```

Expected: `Ran 25 tests ... OK`.

- [ ] **Step 5: Commit.**

```bash
git add accounts/forms.py accounts/tests/forms/test_forms.py
git commit -F - <<'EOF'
Rebuild StoryXP around the story's StoryXPRequest rows

One row per request (fields keyed by request pk, pre-filled from it) instead
of every approved Human keyed by name. clean() returns {character:
categories}; user_can_award() is all-or-nothing over the requested
characters (staff, or scoped ST for every one). Saving still goes through
Story.award_xp (dead-code spec D10).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 46: [D10.2] StoryXPAwardView at accounts:story_xp_award

**Files:**
- Modify: `accounts/views.py`
- Modify: `accounts/urls.py`
- Modify: `core/route_policy_manifest.py` (`ACCOUNT`)
- Modify: `accounts/tests/views/test_profile_actions.py`

**Interfaces:**
- `accounts.views.StoryXPAwardView(LoginRequiredMixin, View)`, `http_method_names = ["post"]`, `post(self, request, story_pk)`.
- URL: `path("story/<int:story_pk>/award-xp/", views.StoryXPAwardView.as_view(), name="story_xp_award")`, mirroring `scene/<int:scene_pk>/award-xp/`; reversed as `reverse("accounts:story_xp_award", kwargs={"story_pk": pk})`.
- Manifest `ACCOUNT` entry `accounts.views.StoryXPAwardView` (anonymous → 401 from `authorize_route`, like `SceneXPAwardView`).
- Flow: `get_object_or_404(Story)` → build `StoryXP(request.POST, story=story, prefix=f"story_{story.pk}")` → no requests: `messages.error(... "has no XP requests to award.")` + redirect, nothing written → `not form.user_can_award(request.user, request=request)`: `messages.error(msg)` + `raise PermissionDenied(msg)` (403), the same convention as `verify_st_for_chronicle`, nothing written → invalid form: `"Failed to award XP. Please check your input."` → `form.save()`; `ValidationError` → `"XP was already awarded for story '<name>'."` (the Scene view's message) → success `"XP awarded for story '<name>'!"`. Always redirects to `accounts:profile` of `request.user` except the 403/404.
- The authorization check runs before any write, and `Story.award_xp` is atomic, so a refused or failed award writes nothing.

- [ ] **Step 1: Write the failing tests.** In `accounts/tests/views/test_profile_actions.py` extend the `game.models` import so it reads (ruff's isort order):

```python
from game.models import (
    Chronicle,
    Gameline,
    Post,
    Scene,
    Story,
    StoryXPRequest,
    STRelationship,
    UserSceneReadStatus,
    Week,
    WeeklyXPRequest,
)
```

and insert directly before `class TestObjectApprovalView(TestCase):`:

```python
class StoryXPTestMixin:
    """Two chronicles; the ST is scoped to chronicle A only."""

    def setUp(self):
        self.player = User.objects.create_user("player", "p@test.com", "password")
        self.st_user = User.objects.create_user("stuser", "st@test.com", "password")
        self.staff = User.objects.create_user("staff", "staff@test.com", "password", is_staff=True)
        self.chronicle_a = Chronicle.objects.create(name="Chronicle A")
        self.chronicle_b = Chronicle.objects.create(name="Chronicle B")
        self.gameline = Gameline.objects.create(name="World of Darkness")
        STRelationship.objects.create(
            user=self.st_user, chronicle=self.chronicle_a, gameline=self.gameline
        )
        self.char_a1 = Human.objects.create(
            name="Alpha", owner=self.player, chronicle=self.chronicle_a, status="App"
        )
        self.char_a2 = Human.objects.create(
            name="Beta", owner=self.player, chronicle=self.chronicle_a, status="App"
        )
        self.char_b = Human.objects.create(
            name="Gamma", owner=self.player, chronicle=self.chronicle_b, status="App"
        )
        self.story = Story.objects.create(name="The Long Night")
        self.request_a1 = StoryXPRequest.objects.create(
            story=self.story, character=self.char_a1, success=True, danger=True, duration=2
        )
        self.request_a2 = StoryXPRequest.objects.create(
            story=self.story, character=self.char_a2, drama=True
        )

    def award_url(self, story=None):
        return reverse("accounts:story_xp_award", kwargs={"story_pk": (story or self.story).pk})

    def post_data(self, story=None):
        """POST exactly what the request rows pre-fill, as the profile form would."""
        story = story or self.story
        data = {}
        for request in StoryXPRequest.objects.filter(story=story):
            prefix = f"story_{story.pk}-{request.pk}"
            for category in ("success", "danger", "growth", "drama"):
                if getattr(request, category):
                    data[f"{prefix}-{category}"] = "on"
            data[f"{prefix}-duration"] = str(request.duration)
        return data


class TestStoryXPAwardView(StoryXPTestMixin, TestCase):
    """POST-only Story XP award: staff or scoped ST for every requested character."""

    def test_scoped_st_awards_computed_xp(self):
        self.client.force_login(self.st_user)
        response = self.client.post(self.award_url(), self.post_data())
        self.assertRedirects(
            response,
            reverse("accounts:profile", kwargs={"pk": self.st_user.profile.pk}),
            fetch_redirect_response=False,
        )
        self.char_a1.refresh_from_db()
        self.char_a2.refresh_from_db()
        self.story.refresh_from_db()
        self.assertEqual(self.char_a1.xp, 4)  # success + danger + duration 2
        self.assertEqual(self.char_a2.xp, 1)  # drama
        self.assertTrue(self.story.xp_given)

    def test_st_can_override_prefilled_values(self):
        self.client.force_login(self.st_user)
        data = self.post_data()
        del data[f"story_{self.story.pk}-{self.request_a1.pk}-danger"]
        data[f"story_{self.story.pk}-{self.request_a1.pk}-duration"] = "0"
        self.client.post(self.award_url(), data)
        self.char_a1.refresh_from_db()
        self.assertEqual(self.char_a1.xp, 1)

    def test_staff_can_award(self):
        self.client.force_login(self.staff)
        response = self.client.post(self.award_url(), self.post_data())
        self.assertEqual(response.status_code, 302)
        self.char_a1.refresh_from_db()
        self.assertEqual(self.char_a1.xp, 4)

    def test_second_award_is_refused(self):
        self.client.force_login(self.st_user)
        self.client.post(self.award_url(), self.post_data())
        response = self.client.post(self.award_url(), self.post_data(), follow=True)
        self.char_a1.refresh_from_db()
        self.assertEqual(self.char_a1.xp, 4)
        self.assertContains(response, "XP was already awarded for story")

    def test_non_scoped_st_is_refused_and_nothing_is_written(self):
        other_st = User.objects.create_user("otherst", "o@test.com", "password")
        STRelationship.objects.create(
            user=other_st, chronicle=self.chronicle_b, gameline=self.gameline
        )
        self.client.force_login(other_st)
        response = self.client.post(self.award_url(), self.post_data())
        self.assertEqual(response.status_code, 403)
        self.char_a1.refresh_from_db()
        self.story.refresh_from_db()
        self.assertEqual(self.char_a1.xp, 0)
        self.assertFalse(self.story.xp_given)

    def test_player_is_refused(self):
        self.client.force_login(self.player)
        response = self.client.post(self.award_url(), self.post_data())
        self.assertEqual(response.status_code, 403)
        self.story.refresh_from_db()
        self.assertFalse(self.story.xp_given)

    def test_partially_scoped_st_is_refused_for_the_whole_story(self):
        StoryXPRequest.objects.create(story=self.story, character=self.char_b, success=True)
        self.client.force_login(self.st_user)
        response = self.client.post(self.award_url(), self.post_data())
        self.assertEqual(response.status_code, 403)
        for character in (self.char_a1, self.char_a2, self.char_b):
            character.refresh_from_db()
            self.assertEqual(character.xp, 0)
        self.story.refresh_from_db()
        self.assertFalse(self.story.xp_given)

    def test_story_without_requests_is_not_awarded(self):
        empty = Story.objects.create(name="Empty Story")
        self.client.force_login(self.staff)
        response = self.client.post(self.award_url(empty), {}, follow=True)
        self.assertContains(response, "has no XP requests")
        empty.refresh_from_db()
        self.assertFalse(empty.xp_given)

    def test_invalid_duration_writes_nothing(self):
        self.client.force_login(self.st_user)
        data = self.post_data()
        data[f"story_{self.story.pk}-{self.request_a1.pk}-duration"] = "lots"
        response = self.client.post(self.award_url(), data, follow=True)
        self.assertContains(response, "Failed to award XP")
        self.story.refresh_from_db()
        self.assertFalse(self.story.xp_given)

    def test_get_is_not_allowed(self):
        self.client.force_login(self.st_user)
        response = self.client.get(self.award_url())
        self.assertEqual(response.status_code, 405)

    def test_nonexistent_story_404(self):
        self.client.force_login(self.st_user)
        response = self.client.post(reverse("accounts:story_xp_award", kwargs={"story_pk": 99999}))
        self.assertEqual(response.status_code, 404)

    def test_not_logged_in_is_refused(self):
        response = self.client.post(self.award_url(), self.post_data())
        self.assertIn(response.status_code, [302, 401])
        self.story.refresh_from_db()
        self.assertFalse(self.story.xp_given)


```

- [ ] **Step 2: Run them and watch them fail.**

```bash
$PY manage.py test accounts.tests.views.test_profile_actions.TestStoryXPAwardView
```

Expected: `FAILED (errors=12)`, each `NoReverseMatch: Reverse for 'story_xp_award' not found`.

- [ ] **Step 3: Implement the view.** In `accounts/views.py`:
  - in the `from accounts.forms import (...)` block add `StoryXP,` after `SceneXP,`;
  - change `from game.models import Scene, UserSceneReadStatus, Week, WeeklyXPRequest` to `from game.models import Scene, Story, UserSceneReadStatus, Week, WeeklyXPRequest`;
  - insert directly before `class ObjectApprovalView(LoginRequiredMixin, View):`:

```python
class StoryXPAwardView(LoginRequiredMixin, View):
    """Award XP for a story from its StoryXPRequests.

    Staff, or a scoped ST for every requested character; otherwise the whole
    award is refused and nothing is written.
    """

    http_method_names = ["post"]

    def post(self, request, story_pk):
        story = get_object_or_404(Story, pk=story_pk)
        form = StoryXP(request.POST, story=story, prefix=f"story_{story.pk}")
        if not form.xp_requests:
            messages.error(request, f"Story '{story.name}' has no XP requests to award.")
            return redirect("accounts:profile", pk=request.user.profile.pk)
        if not form.user_can_award(request.user, request=request):
            msg = (
                "You are not a storyteller for every character in this story. "
                "Cannot perform story XP award."
            )
            messages.error(request, msg)
            raise PermissionDenied(msg)
        if form.is_valid():
            try:
                form.save()
            except ValidationError:
                # e.g. XP already awarded for this story (stale tab/double submit)
                messages.error(request, f"XP was already awarded for story '{story.name}'.")
            else:
                messages.success(request, f"XP awarded for story '{story.name}'!")
        else:
            messages.error(request, "Failed to award XP. Please check your input.")
        return redirect("accounts:profile", pk=request.user.profile.pk)


```

- [ ] **Step 4: Route it.** In `accounts/urls.py`, directly after the `scene_xp_award` entry (before `"scene/<int:scene_pk>/mark-read/"`), insert:

```python
    path(
        "story/<int:story_pk>/award-xp/",
        views.StoryXPAwardView.as_view(),
        name="story_xp_award",
    ),
```

In `core/route_policy_manifest.py`, in the `ACCOUNT` block, directly after `accounts.views.SceneXPAwardView` add:

```
accounts.views.StoryXPAwardView
```

- [ ] **Step 5: Run and pass.**

```bash
$PY manage.py test accounts.tests.views.test_profile_actions core.tests.security.test_route_policies
```

Expected: OK (the 12 new tests plus the existing profile-action and route-policy tests).

- [ ] **Step 6: Commit.**

```bash
git add accounts/views.py accounts/urls.py core/route_policy_manifest.py accounts/tests/views/test_profile_actions.py
git commit -F - <<'EOF'
Add StoryXPAwardView at accounts:story_xp_award

POST-only, modelled on SceneXPAwardView. Staff, or a scoped ST for every
character in the story's requests, may award; anyone else gets a 403 and
nothing is written. Awarding goes through Story.award_xp, so a second award
is refused with the Scene view's "already awarded" message
(dead-code spec D10).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 47: [D10.3] Story XP forms on the ST profile

**Files:**
- Modify: `accounts/views.py` (`ProfileView.get_context_data`, new `ProfileView.get_storyxp_forms`)
- Modify: `accounts/templates/accounts/detail.html`
- Rewrite: `accounts/templates/accounts/includes/xp_story_st.html`
- Modify: `accounts/tests/views/test_profile_actions.py`

**Interfaces:**
- Context key `storyxp_forms: list[StoryXP]` (prefix `story_<pk>`), one per `Story` with `xp_given=False` and at least one request with a character, **kept only if `form.user_can_award(self.object.user, request=self.request)`** (i.e. the profile's user may award every requested character; see Notes). Replaces the two placeholder comments `# story_xp_request_forms` / `# story_xp_request_forms_to_approve`.
- `detail.html`: the commented-out `{% include "accounts/includes/xp_story_st.html" %}` next to `xp_scene_st.html` becomes live (same `{% if object.is_st %}{% if user == object.user %}` block as the scene forms). The player-side `xp_story.html` include stays commented (out of scope).
- `xp_story_st.html` mirrors `xp_scene_st.html` (collapsible `tg-card`, one inner `tg-card` per story), renders a `tg-table` from `storyxp_form.rows`, and posts to `{% url 'accounts:story_xp_award' story_pk=storyxp_form.story.pk %}`. It no longer uses the `field` filter or `char_list`.

- [ ] **Step 1: Write the failing tests.** In `accounts/tests/views/test_profile_actions.py`, insert directly after the `TestStoryXPAwardView` class (before `class TestObjectApprovalView(TestCase):`):

```python
class TestProfileStoryXPForms(StoryXPTestMixin, TestCase):
    """The ST profile lists Story XP forms the ST may submit, next to the scene forms."""

    def test_scoped_st_sees_story_form(self):
        self.client.force_login(self.st_user)
        response = self.client.get(self.st_user.profile.get_absolute_url())
        forms = response.context["storyxp_forms"]
        self.assertEqual([form.story for form in forms], [self.story])
        self.assertContains(response, self.award_url())
        self.assertContains(response, f'name="story_{self.story.pk}-{self.request_a1.pk}-success"')

    def test_awarded_story_is_not_listed(self):
        self.story.xp_given = True
        self.story.save()
        self.client.force_login(self.st_user)
        response = self.client.get(self.st_user.profile.get_absolute_url())
        self.assertEqual(response.context["storyxp_forms"], [])
        self.assertNotContains(response, self.award_url())

    def test_story_with_out_of_scope_character_is_not_listed(self):
        StoryXPRequest.objects.create(story=self.story, character=self.char_b)
        self.client.force_login(self.st_user)
        response = self.client.get(self.st_user.profile.get_absolute_url())
        self.assertEqual(response.context["storyxp_forms"], [])

    def test_story_without_requests_is_not_listed(self):
        Story.objects.create(name="Empty Story")
        self.client.force_login(self.st_user)
        response = self.client.get(self.st_user.profile.get_absolute_url())
        self.assertEqual([form.story for form in response.context["storyxp_forms"]], [self.story])


```

- [ ] **Step 2: Run them and watch them fail.**

```bash
$PY manage.py test accounts.tests.views.test_profile_actions.TestProfileStoryXPForms
```

Expected: `FAILED (errors=4)`, each `KeyError: 'storyxp_forms'`.

- [ ] **Step 3: Implement the context.** In `accounts/views.py`, in `ProfileView.get_context_data`, replace

```python
        # story_xp_request_forms
        # story_xp_request_forms_to_approve
        return context
```

with

```python
        context["storyxp_forms"] = self.get_storyxp_forms()
        return context

    def get_storyxp_forms(self):
        """Story XP forms for unawarded stories this profile's user may award in full."""
        stories = (
            Story.objects.filter(xp_given=False, storyxprequest__character__isnull=False)
            .distinct()
            .order_by("name", "pk")
        )
        forms = [StoryXP(story=story, prefix=f"story_{story.pk}") for story in stories]
        return [
            form for form in forms if form.user_can_award(self.object.user, request=self.request)
        ]
```

- [ ] **Step 4: Implement the template.** In `accounts/templates/accounts/detail.html` replace

```html
                {% comment %} {% include "accounts/includes/xp_story_st.html" %} {% endcomment %}
```

with

```html
                {% include "accounts/includes/xp_story_st.html" %}
```

and replace the whole content of `accounts/templates/accounts/includes/xp_story_st.html` with:

```html
{% if storyxp_forms %}
    <div class="tg-card mb-4">
        <div class="tg-card-header text-center" style="cursor: pointer;" data-toggle="collapse" data-target="#xp-story-st-section" aria-expanded="true">
            <h3 class="tg-card-title {{ user.profile.preferred_heading }}">
                <i class="fas fa-chevron-down"></i> Story XP
            </h3>
        </div>
        <div id="xp-story-st-section" class="collapse show">
            <div class="tg-card-body" style="padding: 20px;">
                {% for storyxp_form in storyxp_forms %}
                    <div class="tg-card mb-3">
                        <div class="tg-card-header text-center">
                            <h5 class="tg-card-title {{ user.profile.preferred_heading }}">
                                <a href="{{ storyxp_form.story.get_absolute_url }}">{{ storyxp_form.story.name }}</a>
                            </h5>
                        </div>
                        <div class="tg-card-body" style="padding: 20px;">
                            <form method="post" action="{% url 'accounts:story_xp_award' story_pk=storyxp_form.story.pk %}">
                                {% csrf_token %}
                                <div class="tg-table-responsive">
                                    <table class="tg-table">
                                        <thead>
                                            <tr>
                                                <th>Character</th>
                                                <th>Success</th>
                                                <th>Danger</th>
                                                <th>Growth</th>
                                                <th>Drama</th>
                                                <th>Duration</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {% for xp_request, fields in storyxp_form.rows %}
                                                <tr>
                                                    <td>
                                                        <a href="{{ xp_request.character.get_absolute_url }}">{{ xp_request.character.name }}</a>
                                                    </td>
                                                    {% for field in fields %}
                                                        <td>{{ field }}{{ field.errors }}</td>
                                                    {% endfor %}
                                                </tr>
                                            {% endfor %}
                                        </tbody>
                                    </table>
                                </div>
                                <div class="text-center mt-4">
                                    <button type="submit" class="tg-btn btn-primary">
                                        <i class="fas fa-paper-plane"></i> Award XP
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>
    </div>
{% endif %}
```

- [ ] **Step 5: Run and pass**, the whole accounts app plus the route policies:

```bash
$PY manage.py test accounts core.tests.security.test_route_policies
```

Expected: `Ran 211 tests ... OK` (count as of `1e77e23` plus D10; earlier units may shift it).

- [ ] **Step 6: Commit.**

```bash
git add accounts/views.py accounts/templates/accounts/detail.html accounts/templates/accounts/includes/xp_story_st.html accounts/tests/views/test_profile_actions.py
git commit -F - <<'EOF'
Show Story XP award forms on the ST profile

ProfileView now builds storyxp_forms (unawarded stories whose every
requested character the ST may award) in place of the placeholder
comments, and the profile renders them next to the scene XP forms, posting
to accounts:story_xp_award (dead-code spec D10).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:**

```bash
$PY manage.py test 2>&1 | tee /tmp/d10-suite.log | tail -3     # serial, ~40 min
grep -E "^(FAIL|ERROR):" /tmp/d10-suite.log
$PY manage.py check
$PY manage.py test core.tests.security.test_route_policies
$PY manage.py test core.tests.test_routed_templates
$PY manage.py shell -c "from django.urls import URLResolver, get_resolver; c = lambda ps: sum(c(p.url_patterns) if isinstance(p, URLResolver) else 1 for p in ps); print(c(get_resolver().url_patterns))"
$RUFF check accounts/forms.py accounts/views.py accounts/urls.py core/route_policy_manifest.py accounts/tests/forms/test_forms.py accounts/tests/views/test_profile_actions.py
$RUFF format --check accounts/urls.py accounts/tests/forms/test_forms.py accounts/tests/views/test_profile_actions.py
$RUFF format --diff accounts/forms.py accounts/views.py
```

Pass criteria: no `FAIL:`/`ERROR:` lines beyond the spec's five baseline failures (none if an earlier unit fixed them); `check` clean; route-policy and routed-template tests pass; route count exactly **1** higher than at the start of the unit; `ruff check` passes; `format --check` passes. `accounts/forms.py` and `accounts/views.py` already fail `format --check` at HEAD (`CustomUserCreationForm.__init__`, `ObjectApprovalView`, `FreebieAwardView` call wrapping); `format --diff` on them must show only those pre-existing hunks, none inside `StoryXP`, `StoryXPAwardView` or `get_storyxp_forms`.

