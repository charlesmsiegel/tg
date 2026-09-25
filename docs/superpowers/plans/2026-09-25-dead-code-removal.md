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

