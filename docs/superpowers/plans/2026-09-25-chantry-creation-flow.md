# Mage Chantry Creation Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Route and finish the existing Mage chantry creation wizard, as specified. Fix the crashing Chantry step in the four character wizards. Add a locked points service with undo, submission and revision hooks, and a detail page built on the recovered model methods.

**Architecture:** Five units, each a contiguous run of commits on `code-improvements`:
- **C1** runs right after the dead-code plan's Unit D1.
- **C2–C5** run after its Unit D9.

A new service, `locations/services/chantry_points.py`, holds every cost rule, runs each mutation in a transaction with the chantry row locked, and re-checks after locking. Forms and views call only the service. Routing and access use the Step 0 manifest (`core/route_policy_manifest.py`), plus a new `OBJECT_ST_WRITE` policy.

**Tech Stack:** Django 5.2, django-polymorphic 4.1, Django `TestCase`/`TransactionTestCase`, the `tg_schema` migrations app.

**Spec:** `docs/superpowers/specs/2026-09-25-chantry-creation-flow-design.md`. Shared rules and the combined rollout order are in `docs/superpowers/plans/2026-09-25-dead-code-removal.md` (Global Constraints) and its spec.

## Global Constraints

- Only push to branch `code-improvements`.
- Commit messages end with the two trailer lines `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23`.
- Tests run serially: `python manage.py test <label>`.
- The full suite has **0 failures** at every unit gate. The dead-code plan's Unit B0 has already fixed the 5 stale failures on `main`; wherever a drafted gate says "only the 5 baseline failures", read "0".
- Every URL change updates `core/route_policy_manifest.py` in the same commit; `core/tests/security/test_route_policies.py` must pass.
- The four character Chantry-step views keep their dotted paths: `characters.views.mage.mage.MageChantryView`, `…mtahuman.MtAHumanChantryView`, `…sorcerer.SorcererChantryView`, `…companion.CompanionChantryView`.
- All points mutations go through `locations.services.chantry_points`, inside `transaction.atomic()` with `select_for_update()`.
- Players never reach `ChantryCreateView` or `ChantryUpdateView`. They are limited to scoped STs and staff.
- Ruff: no **new** errors in touched files (`ruff check`). Don't reformat files that were already unformatted.

## Review Focus

- **Double submit on the last affordable dot.** Two POSTs must not both spend the same points. C2's stale-instance locking test pins this.
- **A forged remove POST for another chantry's rating.** It must be refused. C4's remove-action test pins this.
- **A linked Node or Library deleted from elsewhere.** The detail page must still render and show the rating as unlinked. C4's detail test pins this.
- **An ST returns a chantry that has effects bought.** The player must land on step 1 with everything kept. C3's revision-hook test pins this.
- **A character joins an Approved chantry.** Only `total_points` and membership change; owner and status never do. C1's join test pins this.

## Reconciliation of the two drafted sections (binding)

The C1–C2 and C3–C5 sections were drafted in parallel. Where they differ, these rulings win:

1. **`linked_object`.** `core.Model` is abstract, so C2 implements `ChantryBackgroundRating.linked_object` as a **property** over two nullable `SET_NULL` foreign keys: `linked_location` (to `LocationModel`) and `linked_character` (to `CharacterModel`). Migration `tg_schema/0002` adds both columns. C3–C5 code only assigns and reads `linked_object`, so it works unchanged. Any `select_related`/`prefetch_related("linked_object")` in C4 must instead name `linked_location` and `linked_character`, and queries must filter on the concrete foreign-key names.
2. **The remove form** is C2's **`ChantryRemoveForm(data, chantry=...)`**, whose target is a rating, `ie` or an effect. Wherever C4 says `ChantryRemovePurchaseForm`, use `ChantryRemoveForm` with the field names C2 defines. C4's test that a rating from another chantry is refused still applies. Add that check to `ChantryRemoveForm` if C2's version doesn't already make it.
3. **`ChantryPointForm.save()`** can raise `ValidationError` from the service. C4 views catch it and re-render with the error.
4. **Service additions in C3–C4** (`affordable_effects`, `has_affordable_effect`, the effect cost and rank check in `ChantryEffectsForm`, `apply_type_grants` after an ST changes the type) are added to C2's module and forms, not duplicated.
5. **`has_affordable_purchase`** must skip allowed backgrounds that have no `Background` row.
6. **`factional_name()`** returns the faction term, e.g. "Covenant". The detail subtitle shows the faction's name next to it, so the page reads "Order of Hermes Covenant". This matches the spec's intent without hard-coding adjectives.
7. **Chantries get their own backgrounds template**, which calls `display_name`. The shared `characters/core/background_block/detail.html` stays unchanged, because about 30 templates use it with group and character ratings.

## Drafting notes

#### From `06-C1-C2.md`

**Interfaces produced (for C3, C4 and C5):**
- `locations.services.chantry_points`:
  - `MAX_BACKGROUND_RATING = 5`, `MAX_IE_SCORE = 10`;
  - `next_dot_cost(chantry, bg, current_rating=None) -> int`;
  - `background_purchase_error(chantry, bg, *, points=None, current_rating=None) -> str | None`;
  - `can_buy_background(chantry, bg) -> bool`;
  - `ie_purchase_error(chantry, *, points=None) -> str | None`;
  - `can_buy_ie(chantry) -> bool`;
  - `affordable_backgrounds(chantry) -> tuple[list[Background], list[ChantryBackgroundRating]]`;
  - `has_affordable_purchase(chantry) -> bool`, used by C3's `submission_errors()` and C4's step-1 Continue rule;
  - `buy_background_dot(chantry, bg, *, note="", display_alt_name=False) -> ChantryBackgroundRating`;
  - `buy_ie_dot(chantry) -> int`;
  - `background_removal_error(rating) -> str | None`;
  - `remove_background_dot(rating) -> ChantryBackgroundRating | None`;
  - `ie_removal_error(chantry) -> str | None`;
  - `remove_ie_dot(chantry) -> int`;
  - `remove_effect(chantry, effect) -> None`;
  - `apply_type_grants(chantry) -> ChantryBackgroundRating | None`.
  
  Every mutation raises `django.core.exceptions.ValidationError`.
- `Chantry.LIBRARY_TYPE_FREE_DOTS = 3`; `Chantry.free_dots(property_name) -> int`. `Chantry.bg_cost`, `total_cost` and `points` respect the floor.
- `ChantryBackgroundRating.linked_location` (FK `LocationModel`), `.linked_character` (FK `CharacterModel`), and `.linked_object` (a property getter/setter that returns the concrete subclass). For C4:
  - The steps' `special_valid_action` sets `self.current_background.linked_object = obj`; `GenericBackgroundView.form_valid` then saves `current_background`.
  - The detail page reads `rating.linked_object` and falls back to `note`/`url` when it is `None`.
- `ChantryPointForm(data, pk=...)` with `IE`/`NEW`/`EXISTING` constants. `save()` may raise `ValidationError`.
- `ChantryRemoveForm(data, chantry=...)` with `ACTION = "remove"` and fields `rating`/`ie`/`effect`. `save()` may raise `ValidationError`.
- `ChantrySelectOrCreateForm(data, character=..., points=...)`.
- `characters.views.mage.background_views.CharacterChantryBackgroundView`.
- `tg_schema.migrations.0002_chantry_rating_linked_object` (`LINKED_FIELDS`, `add_chantry_rating_linked_object`). Any later `tg_schema` migration depends on `("tg_schema", "0002_chantry_rating_linked_object")`.

**Deviations and decisions to carry into the master plan:**
1. **`linked_object` is two FKs plus a property, not `ForeignKey("core.Model")`.** `core.Model` is abstract; this was verified by the syncdb failure. Update spec section 6's wording. Detail-page code and C3's `submission_errors()` must not filter on `linked_object` in querysets; use `linked_location`/`linked_character`.
2. **`apply_type_grants` is defined in C2**, and C2.5 adds the chargen call. C1 doesn't depend on C2. C4 must call `apply_type_grants` in `ChantryBasicsView.form_valid` (after save) and in `ChantryUpdateView.form_valid` (after save).
3. **There is one rating per background per chantry.** The New/Existing split is kept for the UI, but both buy through `buy_background_dot(chantry, bg)`.
4. **C1 removes the `chronicle` field** from `ChantrySelectOrCreateForm` because the chronicle is forced to the character's.
5. **The C4 step views must handle the forms' `ValidationError` on save.** `ChantryPointsView.form_valid` and the remove handler should catch it, call `form.add_error(None, e)` and return `form_invalid`. They must also stop using `obj.points < 2` (use `not has_affordable_purchase(obj)`).
6. **`INTEGRATED_EFFECTS_NUMBERS` on `ChantryPointForm` is kept** for C5 to delete. It has no tests. The Evidence-table items `set_chantry_type`, `points_spent` and so on are also left to C5 and C4. C2 doesn't touch the tests in `locations/tests/models/mage/test_chantry.py`.
7. **The locking test is sequential** (stale instance, then the service re-reads the locked row), because SQLite ignores `select_for_update`.
8. **Full-suite baseline is 5 failures on `main`**, not 0. The unit gates require exactly those 5. The prototype ran the whole suite with C1 and C2 applied: `Ran 7189 tests ... FAILED (failures=5, skipped=49)`, and the 5 failures are exactly the baseline ones.
9. The `tg_schema` test is a `TransactionTestCase` and drops one column at a time, because SQLite rebuilds the table from the live model. It restores any missing column in `addCleanup`.
10. **Verification record.**
    - Each task's fail-then-pass sequence was replayed in a fresh worktree from `1e77e23`, by applying exactly the code in this document. Every "Run the tests and confirm they fail" step failed and every "confirm they pass" step passed, with the counts stated above.
    - The replayed tree matched the prototype except for test-class order in `test_chantry.py` and one blank line.

#### From `07-C3-C4-C5.md`

**Assumed C1/C2 interfaces** (all in `locations/services/chantry_points.py` unless noted; refusals raise `django.core.exceptions.ValidationError`):
- `has_affordable_purchase(chantry) -> bool`, used by C3.2 and C4.5. It must tolerate allowed backgrounds that have no `Background` row: the tests create only the rows they need, for example only Allies in `test_continue_when_everything_is_capped`.
- `apply_type_grants(chantry) -> None`, used by C4.2 and C4.3. The tests create `Background(name="Library", property_name="library")` with `get_or_create` and expect a Library rating of 3.
- `remove_effect(chantry, effect) -> None` (C4.6) and `remove_ie_dot` refusing an over-commit (C4.5's `test_refused_removal_changes_nothing_and_says_why`).
- `ChantryRemovePurchaseForm(data, chantry=<Chantry>)` in `locations/forms/mage/chantry.py`, with `is_valid()` and `save()`. `save()` lets the service's `ValidationError` propagate; C4.5 catches it and shows a message. `target` must accept `"ie"` or the pk of a rating **of this chantry**. `test_another_chantrys_rating_cannot_be_removed` fails if the form accepts any rating pk, which would let a player decrement someone else's chantry. If C2's constructor differs, adapt the one call in `ChantryPointsView.post`.
- `ChantryPointForm(pk=...)`: the view still passes `pk` through `get_form_kwargs`.
- `ChantryBackgroundRating.linked_object` **cannot be a ForeignKey to `core.Model`**: `core.Model` is abstract (`Meta.abstract = True`; `apps.get_model("core", "Model")` raises), so Django refuses such a field. C2 needs a `GenericForeignKey` (content type plus object id) or separate FKs. The C4 code only assigns `rating.linked_object = obj`, reads it (`None` when unset or when the target is gone) and uses `prefetch_related("linked_object")`, which works for a FK or a GFK. I prototyped with a GFK: `test_node_deleted_after_linking_shows_as_unlinked` passes because a GFK getter returns `None` for a deleted target. If C2 uses a GFK, the spec's `SET_NULL` wording and the `tg_schema` migration shape change; tell the C2 author.

**Things this section adds that might overlap C2:**
- C3.2 appends `affordable_effects()` and `has_affordable_effect()` to the points service. The spec names no effect-affordability predicate, but both `submission_errors` and the step-2 Continue rule need one. Drop them if C2 has an equivalent.
- C4.6 adds the server-side cost and rank check to `ChantryEffectsForm.clean()` and points its queryset at `affordable_effects`. The spec's Testing section lists "the IE-effect cost limit" under the forms tests (C2); if C2 did it, keep only C4.6's view, template and test parts.
- C4.2 calls `apply_type_grants` from `ChantryUpdateView` when the type changes (spec section 2). Drop it if C2 already does.
- C4.3 changes `ChantryCreateForm.save()` so `commit=False` does not save (it used to save regardless), which lets `ChantryBasicsView` save once. C1 edits `ChantrySelectOrCreateForm` in the same file; there is no overlap.

**Decisions to confirm:**
- New tests go in new sibling files (`test_chantry_update.py`, `test_chantry_create.py`, `test_chantry_wizard.py`, `test_chantry_detail.py`, helpers in `chantry_fixtures.py`) rather than appending to the existing `locations/tests/views/mage/test_chantry.py` the spec names, to keep each task's imports self-contained.
- `factional_name()` returns the table term only, for example "Covenant". The spec's example "Hermetic Covenant" needs an adjective that `factional_names` doesn't hold.
- The shared `characters/core/background_block/detail.html` is not changed: 30 character and group templates use it, and `PooledBackgroundRating` has no `display_name`. Chantries get their own `display_includes/backgrounds.html`, which uses `display_name` and adds the "−" buttons.
- The "−" and Remove buttons use the HTML `form` attribute to reach small forms placed in `{% block footer %}`, outside `core/form.html`'s main `<form>`. They POST `action=remove` + `target`, or `action=remove_effect` + `effect`.
- The "Create directly" link appears on the Basics page (for scoped STs and staff) and on the chantry list, which only staff see; everyone else gets the public list.
- After step 6 the chantry sits at `creation_status = 7` on the detail page. The spec gives no Back action from there; a returned chantry restarts at step 1 through `on_returned_for_revision`.
- `locations/docs/codemap.html` still mentions `Chantry.set_rank()`. It is generated documentation and C5 does not edit it.

**Verification done while drafting** (throwaway worktree, stub C2 service, GFK `linked_object` and remove form): every step's fail-then-pass run as written, `core.tests.security` green, and `scripts/build_route_policy_manifest.py` reproducing the C4 manifest classes (its only diff is pre-existing sort order). Route count at `1e77e23`: 1833, 1834 after C4, 1833 after C5.

**Full-suite result of the prototype** (C3, C4 and C5 on `1e77e23` with the C2 stubs, run serially): 7,184 tests, 49 skipped, **5 failures**, exactly the 5 baseline failures listed in the dead-code spec's *Removal safety* section (three vampire Basics views, the wraith circle create, and the companion attach test). No other failures or errors. Each unit gate says "0 failures". If those 5 have not been fixed by an earlier unit when this section runs, read the gate as "exactly those 5 and no others".

---

## Unit C1: Fix the character-wizard Chantry step (spec section 4)

**Goal.** The Chantry background step in the Mage, MtA Human, Sorcerer and Companion wizards stops returning a 500. Creating a chantry makes an unfinished (`Un`), player-owned chantry funded with the background rating. Joining one adds the rating to its `total_points` and membership, and changes nothing else. The Mage template renders the step at the number its router uses.

**Verified facts (at `1e77e23`):**
- `view_mapping` numbers: `MageCharacterCreationView` 20 → `MageChantryView`, 21 → `MageSpecialtiesView` (`characters/views/mage/mage.py`); `MtAHumanCharacterCreationView` 13 (`mtahuman.py`); `CopanionCharacterCreationView` 13 (`companion.py`, the class name has that typo); `SorcererCharacterCreationView` 17 (`sorcerer.py`).
- `characters/templates/characters/mage/mage/chargen.html` renders the Chantry include at `creation_status == 17` and Specialties at `== 18`. The other three templates already match their routers.
- All four views read `form.chantry_creation_form`, which does not exist, so a GET raises `AttributeError`. Running the new tests before the fix gives 24 errors with exactly that message.
- The manifest (`core/route_policy_manifest.py`) lists the four views as `characters.views.mage.<module>.<Class>` under `CHARGEN_STEP`. A subclass defined in `mage.py` keeps `__module__ == "characters.views.mage.mage"` even though its base class lives in `background_views.py`, so no manifest edit is needed. `CharacterChantryBackgroundView` is not routed, so it needs no manifest entry, and `test_route_policies` stays green (verified).
- Tests build a character on a step with `Mage.objects.create(..., creation_status=N, arete=1)` (`MtAHuman`/`Companion` need no extra fields; `Sorcerer` needs `sorcerer_type="hedge_mage"`), then `BackgroundRating.objects.create(char=..., bg=Background(property_name="chantry"), rating=N)`. The pattern is in `characters/tests/views/mage/test_background_views.py`. `characters/tests/utils.py::mage_setup()` also creates the `chantry` Background, but the new tests use `get_or_create` and don't need the whole fixture.
- `locations/templates/locations/mage/chantry/select_or_create_form.html` uses **CRLF** line endings. Keep them (see Task C1.3).
- `core.models.Model.save()` runs `full_clean()`, and `name` is required there, so the form's own name check gives a clear field error before the model check runs.

**Decision: `apply_type_grants`.** C1 does **not** call it. `apply_type_grants` is created in C2 (Task C2.5), and that task adds the call to `ChantrySelectOrCreateForm.save()` on the create path, with a test. This keeps C1 independent of C2 and mergeable first. Until C2 merges, a `library`-type chantry created from chargen has no free Library dots. That doesn't matter because the chantry wizard isn't routed until C4.

**Decision: persistence lives in `ChantrySelectOrCreateForm.save()`.** The view's `form_valid` wraps it in `transaction.atomic()` and does the membership, rating and `creation_status` work. The form already owned save semantics and tests. The spec's create and join behaviours are the same either way.

**Decision: `chronicle` is removed from the form's fields.** The chronicle is forced to `character.chronicle`, so a dropdown for it would be ignored. The template row is removed too.

### Task 1: [C1.1] `ChantrySelectOrCreateForm` takes `points`, validates the name, and no longer overwrites

**Files:**
- Modify: `locations/forms/mage/chantry.py` (the `ChantrySelectOrCreateForm` class and one import)
- Modify (test): `locations/tests/forms/mage/test_chantry.py` (replace every class from `class TestChantrySelectOrCreateFormSetup` to the end of the file)

**Interfaces:**
- `ChantrySelectOrCreateForm(data=None, *, character: Human, points: int = 0, **kwargs)`, a ModelForm on `Chantry`. Fields: `create_new`, `existing_chantry`, `name`, `contained_within`, `description`, `faction`, `leadership_type`, `season`, `chantry_type`, `gauntlet`, `shroud`, `dimension_barrier`. There is no `total_points` and no `chronicle` field, and every field has `required=False`.
- `existing_chantry` queryset: `Chantry.objects.filter(chronicle=character.chronicle).exclude(status__in=["Ret", "Dec"])`.
- `clean()`: when creating, `name` must be non-blank (error on `name`). When selecting, the mixin puts the error on `existing_chantry`.
- `save(commit=True) -> Chantry` always commits, inside `transaction.atomic()`.
  - Create: `owner=character.owner`, `chronicle=character.chronicle`, `status="Un"`, `creation_status=1`, `total_points=points`, then `save_m2m()`.
  - Join: `select_for_update()` the chosen row, `total_points += points`, `save(update_fields=["total_points"])`. Nothing else changes.

- [ ] **Step 1: Write the failing tests.** In `locations/tests/forms/mage/test_chantry.py`, delete everything from the line `class TestChantrySelectOrCreateFormSetup(TestCase):` to the end of the file and put this in its place (the imports at the top of the file stay unchanged):

```python
class TestChantrySelectOrCreateFormSetup(TestCase):
    """Shared setup for ChantrySelectOrCreateForm tests."""

    @classmethod
    def setUpTestData(cls):
        """Create test data for ChantrySelectOrCreateForm tests."""
        mage_setup()
        cls.user = User.objects.create_user(username="testuser", password="password")
        cls.other = User.objects.create_user(username="other", password="password")
        cls.chronicle = Chronicle.objects.create(name="Test Chronicle")
        cls.character = Mage.objects.create(
            name="Test Mage", owner=cls.user, chronicle=cls.chronicle
        )
        cls.existing_chantry = Chantry.objects.create(
            name="Existing Chantry",
            owner=cls.other,
            chronicle=cls.chronicle,
            status="App",
            total_points=20,
        )


class TestChantrySelectOrCreateFormBasics(TestChantrySelectOrCreateFormSetup):
    """Test basic ChantrySelectOrCreateForm structure and fields."""

    def test_form_has_required_fields(self):
        """The form offers create/select and basics, but no points field."""
        form = ChantrySelectOrCreateForm(character=self.character, points=3)

        self.assertIn("create_new", form.fields)
        self.assertIn("existing_chantry", form.fields)
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertNotIn("total_points", form.fields)
        self.assertNotIn("chronicle", form.fields)

    def test_existing_chantry_queryset_filtered_by_chronicle(self):
        """Test that existing_chantry queryset is filtered by character's chronicle."""
        other_chronicle = Chronicle.objects.create(name="Other Chronicle")
        other_chantry = Chantry.objects.create(name="Other Chantry", chronicle=other_chronicle)

        form = ChantrySelectOrCreateForm(character=self.character, points=3)

        self.assertIn(self.existing_chantry, form.fields["existing_chantry"].queryset)
        self.assertNotIn(other_chantry, form.fields["existing_chantry"].queryset)

    def test_existing_chantry_queryset_excludes_retired_and_deceased(self):
        retired = Chantry.objects.create(name="Retired", chronicle=self.chronicle, status="Ret")
        dead = Chantry.objects.create(name="Dead", chronicle=self.chronicle, status="Dec")

        queryset = (
            ChantrySelectOrCreateForm(character=self.character, points=3)
            .fields["existing_chantry"]
            .queryset
        )

        self.assertNotIn(retired, queryset)
        self.assertNotIn(dead, queryset)
        self.assertIn(self.existing_chantry, queryset)

    def test_all_fields_optional(self):
        """Test that all fields are optional."""
        form = ChantrySelectOrCreateForm(character=self.character, points=3)

        for field in form.fields.values():
            self.assertFalse(field.required)


class TestChantrySelectOrCreateFormValidation(TestChantrySelectOrCreateFormSetup):
    """Test ChantrySelectOrCreateForm validation logic."""

    def test_valid_select_existing(self):
        """Test that selecting existing chantry is valid."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )

        self.assertTrue(form.is_valid())

    def test_invalid_no_selection_when_not_creating(self):
        """Test that not creating and no selection is invalid."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": ""}, character=self.character, points=5
        )

        self.assertFalse(form.is_valid())
        self.assertIn("existing_chantry", form.errors)

    def test_invalid_create_without_name(self):
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "   "}, character=self.character, points=5
        )

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_valid_create_new_with_valid_data(self):
        """Test that creating new with valid data is valid."""
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "New Chantry", "description": "Test"},
            character=self.character,
            points=10,
        )

        self.assertTrue(form.is_valid())


class TestChantrySelectOrCreateFormSave(TestChantrySelectOrCreateFormSetup):
    """Test ChantrySelectOrCreateForm save logic."""

    def test_save_returns_existing_chantry(self):
        """Test that saving with existing selection returns the existing chantry."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )
        self.assertTrue(form.is_valid())
        chantry = form.save()

        self.assertEqual(chantry.pk, self.existing_chantry.pk)

    def test_save_adds_points_to_existing_chantry_and_nothing_else(self):
        """Joining adds the points; owner, chronicle and status stay."""
        form = ChantrySelectOrCreateForm(
            data={"existing_chantry": self.existing_chantry.pk},
            character=self.character,
            points=5,
        )
        self.assertTrue(form.is_valid())
        form.save()

        self.existing_chantry.refresh_from_db()
        self.assertEqual(self.existing_chantry.total_points, 25)
        self.assertEqual(self.existing_chantry.owner, self.other)
        self.assertEqual(self.existing_chantry.status, "App")
        self.assertEqual(self.existing_chantry.chronicle, self.chronicle)

    def test_save_creates_new_chantry(self):
        """Creating makes an unfinished chantry owned by the character's player."""
        initial_count = Chantry.objects.count()

        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "Created Chantry", "description": "New"},
            character=self.character,
            points=15,
        )
        self.assertTrue(form.is_valid())
        chantry = form.save()

        self.assertEqual(Chantry.objects.count(), initial_count + 1)
        self.assertEqual(chantry.name, "Created Chantry")
        self.assertEqual(chantry.total_points, 15)
        self.assertEqual(chantry.owner, self.user)
        self.assertEqual(chantry.chronicle, self.chronicle)
        self.assertEqual(chantry.status, "Un")
        self.assertEqual(chantry.creation_status, 1)
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.forms.mage.test_chantry`.
  - Expected: `ERROR`s with `TypeError: BaseModelForm.__init__() got an unexpected keyword argument 'points'` in the `TestChantrySelectOrCreateForm*` classes, giving `FAILED (errors=11)`.

- [ ] **Step 3: Implement the form change.**
  - In `locations/forms/mage/chantry.py`, add `from django.db import transaction` right after `from django import forms`.
  - Replace the whole `ChantrySelectOrCreateForm` class (it is the last class in the file) with:

```python
class ChantrySelectOrCreateForm(CreateOrSelectMixin, forms.ModelForm):
    """Create a chantry for a character's Chantry background, or join one.

    ``points`` is the character's Chantry background rating. A new chantry is
    owned by the character's player, starts unfinished in the chantry wizard and
    is funded with exactly those points. Joining only adds the points; the
    chosen chantry's owner, chronicle and status are never touched.
    """

    create_or_select_config = {
        "toggle_field": "create_new",
        "select_field": "existing_chantry",
        "error_message": "Please select an existing Chantry.",
    }

    create_new = CreateOrSelectField(label="Create a new Chantry?")
    existing_chantry = forms.ModelChoiceField(
        queryset=Chantry.objects.none(),
        required=False,
        label="Select an existing Chantry",
    )

    class Meta:
        model = Chantry
        fields = [
            "create_new",
            "existing_chantry",
            "name",
            "contained_within",
            "description",
            "faction",
            "leadership_type",
            "season",
            "chantry_type",
            "gauntlet",
            "shroud",
            "dimension_barrier",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter name here"}),
            "description": forms.Textarea(attrs={"placeholder": "Enter description here"}),
        }

    def __init__(self, *args, character, points=0, **kwargs):
        self.character = character
        self.points = points
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
        self.fields["existing_chantry"].queryset = Chantry.objects.filter(
            chronicle=character.chronicle
        ).exclude(status__in=["Ret", "Dec"])

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("create_new") and not (cleaned_data.get("name") or "").strip():
            self.add_error("name", "A new Chantry needs a name.")
        return cleaned_data

    def save(self, commit=True):
        """Create or join the chantry and return it. Always commits."""
        with transaction.atomic():
            if self.is_creating():
                chantry = super().save(commit=False)
                chantry.owner = self.character.owner
                chantry.chronicle = self.character.chronicle
                chantry.status = "Un"
                chantry.creation_status = 1
                chantry.total_points = self.points
                chantry.save()
                self.save_m2m()
                return chantry
            chantry = Chantry.objects.select_for_update().get(
                pk=self.cleaned_data["existing_chantry"].pk
            )
            chantry.total_points += self.points
            chantry.save(update_fields=["total_points"])
            return chantry
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.forms.mage.test_chantry`.
  - Expected: `OK` (33 tests).

- [ ] **Step 5: Commit.**

```bash
git add locations/forms/mage/chantry.py locations/tests/forms/mage/test_chantry.py
git commit -m "Chantry background form: points kwarg, name check, join adds points only

ChantrySelectOrCreateForm no longer has total_points or chronicle fields.
The view passes the character's Chantry rating as points. Creating makes
an Un chantry owned by the character's player in the character's
chronicle; joining locks the row and only adds points. Retired and
deceased chantries are no longer offered.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 2: [C1.2] Mage chargen template renders Chantry at 20 and Specialties at 21

**Files:**
- Modify: `characters/templates/characters/mage/mage/chargen.html` (two `{% if %}` conditions)
- Create (test): `characters/tests/views/mage/test_mage_chantry_template.py`

**Interfaces:** none. After this task the Mage template's Chantry block shows only at `creation_status == 20` and Specialties only at `== 21`.

- [ ] **Step 1: Write the failing tests.** Create `characters/tests/views/mage/test_mage_chantry_template.py`:

```python
"""The Mage chargen template renders Chantry at step 20 and Specialties at 21."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.mage import Mage


class TestMageChargenTemplateNumbering(TestCase):
    """The Mage template renders Chantry at 20 and Specialties at 21."""

    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="password")
        self.client.login(username="owner", password="password")

    def test_chantry_block_not_rendered_at_mentor_step(self):
        mentor_bg, _ = Background.objects.get_or_create(
            property_name="mentor", defaults={"name": "Mentor"}
        )
        mage = Mage.objects.create(
            name="Mentor Step Mage", owner=self.owner, creation_status=17, arete=1
        )
        BackgroundRating.objects.create(char=mage, bg=mentor_bg, rating=1)
        response = self.client.get(mage.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Chantry Background")

    def test_specialties_block_rendered_at_step_21(self):
        mage = Mage.objects.create(
            name="Specialty Step Mage", owner=self.owner, creation_status=21, arete=1
        )
        response = self.client.get(mage.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Choose Specialties")
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test characters.tests.views.mage.test_mage_chantry_template`.
  - Expected: 2 failures:
    - `AssertionError: 1 != 0 : 'Chantry Background' unexpectedly found`, because step 17 is the Mentor step;
    - `Couldn't find 'Choose Specialties'`.

- [ ] **Step 3: Implement the change.** In `characters/templates/characters/mage/mage/chargen.html`, make exactly these two edits:

```diff
         {% block chantry %}
-            {% if object.creation_status == 17 %}
+            {% if object.creation_status == 20 %}
                 {% include "locations/mage/chantry/select_or_create_form.html" %}
             {% endif %}
         {% endblock chantry %}
         {% block specialties_form %}
-            {% if object.creation_status == 18 %}
+            {% if object.creation_status == 21 %}
                 {% include "characters/mage/mage/mage_specialties_block_form.html" %}
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test characters.tests.views.mage.test_mage_chantry_template`.
  - Expected: `OK` (2 tests).

- [ ] **Step 5: Commit.**

```bash
git add characters/templates/characters/mage/mage/chargen.html characters/tests/views/mage/test_mage_chantry_template.py
git commit -m "Mage chargen template: Chantry at step 20, Specialties at 21

MageCharacterCreationView maps Chantry to 20 and Specialties to 21; the
template rendered them at 17 and 18 (the Mentor and Contacts steps).

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 3: [C1.3] Collapse the four Chantry views into `CharacterChantryBackgroundView`

**Files:**
- Modify: `characters/views/mage/background_views.py` (imports, new class at the end)
- Modify: `characters/views/mage/mage.py`, `characters/views/mage/mtahuman.py`, `characters/views/mage/sorcerer.py`, `characters/views/mage/companion.py` (imports, and each `*ChantryView` class body)
- Modify: `locations/templates/locations/mage/chantry/select_or_create_form.html` (keep CRLF)
- Create (test): `characters/tests/views/mage/test_chantry_background.py`

**Interfaces:**
- `characters.views.mage.background_views.CharacterChantryBackgroundView(GenericBackgroundView)`:
  - class attributes: `background_name = "chantry"`, `form_class = ChantrySelectOrCreateForm`;
  - `get_form_kwargs()` adds `character=self.get_object()` and `points=self.current_background.rating` (0 when there is no incomplete rating);
  - `form_valid(form)` runs in `transaction.atomic()`:
    1. `form.save()`;
    2. `chantry.members.add(character)`;
    3. the rating gets `note=chantry.name`, `url=chantry.get_absolute_url()` and `complete=True`;
    4. `character.creation_status += 1` when no incomplete `chantry` rating remains;
    5. the view redirects to `character.get_absolute_url()`.
  
  It never calls `GenericBackgroundView.form_valid`, so it never overwrites the owner or status.
- The subclasses keep their dotted paths and set only `primary_object_class` and `template_name`: `characters.views.mage.mage.MageChantryView`, `characters.views.mage.mtahuman.MtAHumanChantryView`, `characters.views.mage.sorcerer.SorcererChantryView` and `characters.views.mage.companion.CompanionChantryView`.

- [ ] **Step 1: Write the failing tests.** Create `characters/tests/views/mage/test_chantry_background.py`:

```python
"""Regression tests for the Chantry background step in the Mage-family wizards."""

from django.contrib.auth.models import User
from django.test import TestCase

from characters.models.core.background_block import Background, BackgroundRating
from characters.models.mage.companion import Companion
from characters.models.mage.mage import Mage
from characters.models.mage.mtahuman import MtAHuman
from characters.models.mage.sorcerer import Sorcerer
from game.models import Chronicle
from locations.models.mage.chantry import Chantry


class ChantryBackgroundStepMixin:
    """Build a character sitting on its wizard's Chantry step."""

    chantry_step = None

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="owner", password="password")
        cls.other = User.objects.create_user(username="other", password="password")
        cls.chronicle = Chronicle.objects.create(name="Chantry Chronicle")
        cls.chantry_bg, _ = Background.objects.get_or_create(
            property_name="chantry", defaults={"name": "Chantry"}
        )

    def make_character(self):
        raise NotImplementedError

    def setUp(self):
        self.character = self.make_character()
        self.rating = BackgroundRating.objects.create(
            char=self.character, bg=self.chantry_bg, rating=3
        )
        self.client.login(username="owner", password="password")
        self.url = self.character.get_absolute_url()

    def test_step_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chantry Background")
        self.assertContains(response, 'name="existing_chantry"')
        self.assertNotContains(response, 'name="total_points"')

    def test_create_makes_unfinished_player_owned_chantry(self):
        response = self.client.post(
            self.url,
            {"create_new": "on", "name": "House of Winds", "description": "Windy"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.character.get_absolute_url())
        chantry = Chantry.objects.get(name="House of Winds")
        self.assertEqual(chantry.owner, self.owner)
        self.assertEqual(chantry.chronicle, self.chronicle)
        self.assertEqual(chantry.status, "Un")
        self.assertEqual(chantry.creation_status, 1)
        self.assertEqual(chantry.total_points, 3)
        self.assertIn(self.character.pk, chantry.members.values_list("pk", flat=True))
        self.rating.refresh_from_db()
        self.assertTrue(self.rating.complete)
        self.assertEqual(self.rating.note, "House of Winds")
        self.assertEqual(self.rating.url, chantry.get_absolute_url())
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step + 1)

    def test_join_existing_only_adds_points_and_membership(self):
        existing = Chantry.objects.create(
            name="Old Tower",
            owner=self.other,
            chronicle=self.chronicle,
            status="App",
            creation_status=7,
            total_points=10,
        )
        response = self.client.post(self.url, {"existing_chantry": existing.pk, "name": "Ignored"})
        self.assertEqual(response.status_code, 302)
        existing.refresh_from_db()
        self.assertEqual(existing.total_points, 13)
        self.assertEqual(existing.owner, self.other)
        self.assertEqual(existing.chronicle, self.chronicle)
        self.assertEqual(existing.status, "App")
        self.assertEqual(existing.creation_status, 7)
        self.assertEqual(existing.name, "Old Tower")
        self.assertIn(self.character.pk, existing.members.values_list("pk", flat=True))
        self.assertFalse(Chantry.objects.filter(name="Ignored").exists())
        self.rating.refresh_from_db()
        self.assertTrue(self.rating.complete)
        self.assertEqual(self.rating.note, "Old Tower")
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step + 1)

    def test_create_without_name_is_form_error(self):
        response = self.client.post(self.url, {"create_new": "on", "name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.context["form"].errors)
        self.assertFalse(Chantry.objects.exists())
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step)

    def test_select_without_choice_is_form_error(self):
        response = self.client.post(self.url, {"existing_chantry": ""})
        self.assertEqual(response.status_code, 200)
        self.assertIn("existing_chantry", response.context["form"].errors)
        self.character.refresh_from_db()
        self.assertEqual(self.character.creation_status, self.chantry_step)

    def test_retired_chantry_cannot_be_joined(self):
        retired = Chantry.objects.create(
            name="Ruin", owner=self.other, chronicle=self.chronicle, status="Ret", total_points=5
        )
        response = self.client.post(self.url, {"existing_chantry": retired.pk})
        self.assertEqual(response.status_code, 200)
        self.assertIn("existing_chantry", response.context["form"].errors)
        retired.refresh_from_db()
        self.assertEqual(retired.total_points, 5)


class TestMageChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 20

    def make_character(self):
        return Mage.objects.create(
            name="Chantry Mage",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
            arete=1,
        )


class TestMtAHumanChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 13

    def make_character(self):
        return MtAHuman.objects.create(
            name="Chantry Human",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
        )


class TestCompanionChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 13

    def make_character(self):
        return Companion.objects.create(
            name="Chantry Companion",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
        )


class TestSorcererChantryStep(ChantryBackgroundStepMixin, TestCase):
    chantry_step = 17

    def make_character(self):
        return Sorcerer.objects.create(
            name="Chantry Sorcerer",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=self.chantry_step,
            sorcerer_type="hedge_mage",
        )
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test characters.tests.views.mage.test_chantry_background`.
  - Expected: `FAILED (errors=24)`. Every error is `AttributeError: 'ChantrySelectOrCreateForm' object has no attribute 'chantry_creation_form'`, which is the live 500.

- [ ] **Step 3: Add the shared view.** In `characters/views/mage/background_views.py`:
  - add `from django.db import transaction` after `from typing import Any` and its blank line, before `from django.http import HttpResponseRedirect`;
  - add `from characters.views.core.generic_background import GenericBackgroundView` after `from characters.models.core.human import Human`;
  - add `from locations.forms.mage.chantry import ChantrySelectOrCreateForm` after the `core.mixins` import block;
  - append at the end of the file:

```python
class CharacterChantryBackgroundView(GenericBackgroundView):
    """Chantry background step shared by the Mage-family character wizards.

    Subclasses set only ``primary_object_class`` and ``template_name``.
    ``form_valid`` replaces the generic version, which would overwrite the
    owner, chronicle and status of a chantry the character merely joins.
    """

    background_name = "chantry"
    form_class = ChantrySelectOrCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["character"] = self.get_object()
        rating = getattr(self, "current_background", None)
        kwargs["points"] = rating.rating if rating is not None else 0
        return kwargs

    def form_valid(self, form):
        character = self.get_object()
        with transaction.atomic():
            chantry = form.save()
            chantry.members.add(character)
            self.current_background.note = chantry.name
            self.current_background.url = chantry.get_absolute_url()
            self.current_background.complete = True
            self.current_background.save()
            if not character.backgrounds.filter(
                bg__property_name=self.background_name, complete=False
            ).exists():
                character.creation_status += 1
                character.save()
        return HttpResponseRedirect(character.get_absolute_url())
```

- [ ] **Step 4: Point the four subclasses at it.** In each of `characters/views/mage/mage.py`, `mtahuman.py`, `sorcerer.py` and `companion.py`:
  - delete the line `from locations.forms.mage.chantry import ChantrySelectOrCreateForm`;
  - replace the line `from characters.views.mage.background_views import MtAEnhancementView` with:

```python
from characters.views.mage.background_views import (
    CharacterChantryBackgroundView,
    MtAEnhancementView,
)
```

  - Then replace each whole `*ChantryView` class, including its `get_form_kwargs` and `get_form` methods, with the matching block below. Leave the `*CharacterCreationView` classes that follow unchanged.

```python
# characters/views/mage/mage.py
class MageChantryView(CharacterChantryBackgroundView):
    primary_object_class = Mage
    template_name = "characters/mage/mage/chargen.html"
```

```python
# characters/views/mage/mtahuman.py
class MtAHumanChantryView(CharacterChantryBackgroundView):
    primary_object_class = MtAHuman
    template_name = "characters/mage/mtahuman/chargen.html"
```

```python
# characters/views/mage/sorcerer.py
class SorcererChantryView(CharacterChantryBackgroundView):
    primary_object_class = Sorcerer
    template_name = "characters/mage/sorcerer/chargen.html"
```

```python
# characters/views/mage/companion.py
class CompanionChantryView(CharacterChantryBackgroundView):
    primary_object_class = Companion
    template_name = "characters/mage/companion/chargen.html"
```

  `get_object_or_404` is still used elsewhere in all four modules, so keep that import. `ruff check` confirms there are no unused imports.

- [ ] **Step 5: Update the include template.** Replace the whole content of `locations/templates/locations/mage/chantry/select_or_create_form.html` with the text below:
  - The file uses CRLF line endings. Write it with CRLF, for example save the text to `/tmp/soc.html` and run `python -c "import sys; s=open('/tmp/soc.html').read(); open(sys.argv[1],'w',newline='\r\n').write(s)" locations/templates/locations/mage/chantry/select_or_create_form.html`.
  - Then check `git diff --stat`: it should show about 5 insertions and 12 deletions, not a whole-file rewrite.
  - The edit drops the empty row, the `chronicle` and `total_points` widgets, and adds field errors and a points notice.

```html
<div class="row {{ object.get_heading }}">
    <h2 class="col-sm">Chantry Background</h2>
</div>
<div class="row">
    <div class="col-sm">Create New? {{ form.create_new }}</div>
</div>
<div data-create-or-select-container="{{ form.create_new.name }}" data-create-or-select-mode="select">
    <div class="row">
        <div class="col-sm">Add {{ current_background.rating }} points to existing Chantry:</div>
        <div class="col-sm">{{ form.existing_chantry }} {{ form.existing_chantry.errors }}</div>
    </div>
</div>
<div data-create-or-select-container="{{ form.create_new.name }}" data-create-or-select-mode="create" class="d-none">
    <div class="row">
        <h3 class="col-sm">{{ form.name }}</h3>
        {{ form.name.errors }}
    </div>
    <div class="row">
        <div class="col-sm">{{ form.contained_within }}</div>
    </div>
    <div class="row">
        <div class="col-sm">Gauntlet</div>
        <div class="col-sm">{{ form.gauntlet }}</div>
        <div class="col-sm">Shroud</div>
        <div class="col-sm">{{ form.shroud }}</div>
        <div class="col-sm">Dimension Barrier</div>
        <div class="col-sm">{{ form.dimension_barrier }}</div>
    </div>
    <div class="row">
        <div class="col-sm">Faction</div>
        <div class="col-sm">{{ form.faction }}</div>
        <div class="col-sm">Season</div>
        <div class="col-sm">{{ form.season }}</div>
        <div class="col-sm">Type</div>
        <div class="col-sm">{{ form.chantry_type }}</div>
    </div>
    <div class="row">
        <div class="col-sm">Leadership Type</div>
        <div class="col-sm">{{ form.leadership_type }}</div>
    </div>
    <div class="row">
        <div class="col-sm">The new Chantry starts with {{ current_background.rating }} points. You will spend them in the Chantry wizard.</div>
    </div>
    <div class="row">
        <div class="col-sm">{{ form.description }}</div>
    </div>
</div>
```

- [ ] **Step 6: Run the tests and confirm they pass.**
  - Run `python manage.py test characters.tests.views.mage.test_chantry_background characters.tests.views.mage.test_mage_chantry_template locations.tests.forms.mage.test_chantry core.tests.security.test_route_policies`.
  - Expected: `OK` (24 + 2 + 33 + 4 tests).

- [ ] **Step 7: Commit.**

```bash
git add characters/views/mage/background_views.py characters/views/mage/mage.py characters/views/mage/mtahuman.py characters/views/mage/sorcerer.py characters/views/mage/companion.py locations/templates/locations/mage/chantry/select_or_create_form.html characters/tests/views/mage/test_chantry_background.py
git commit -m "Fix the Chantry background step in the four Mage-family wizards

The four *ChantryView classes read form.chantry_creation_form, which does
not exist, so the step returned a 500. They now subclass one
CharacterChantryBackgroundView that passes the background rating as
points and replaces GenericBackgroundView.form_valid, which rewrote the
owner, chronicle and status of a chantry the character merely joined.
Creating makes an Un player-owned chantry; joining adds points and
membership only. Both complete the rating and advance the character.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

- [ ] **Unit gate:** Run each check below; every one must pass before C1 is done.
  - Run the full suite serially: `python manage.py test > /tmp/c1-full.log 2>&1; tail -3 /tmp/c1-full.log; grep -E "^(FAIL|ERROR):" /tmp/c1-full.log`.
    - Expected: `FAILED (failures=5, ...)`, and the failures are exactly the 5 baseline failures on `main` (recorded in the dead-code spec's *Removal safety* section):
      - `test_other_player_cannot_attach_companion_to_mage`;
      - `test_basics_view_creates_ghoul`;
      - `test_basics_view_creates_vampire`;
      - `test_basics_view_creates_vtmhuman`;
      - `test_create_circle_successfully`.
    - Any other failure is a regression; fix it before merging. The full suite, including all of C2, was run on the prototype worktree.
  - `python manage.py check`: no issues.
  - `python manage.py test core.tests.security.test_route_policies`: `OK`.
  - `ruff check characters/tests/views/mage/test_chantry_background.py characters/tests/views/mage/test_mage_chantry_template.py characters/views/mage/background_views.py locations/tests/forms/mage/test_chantry.py`: `All checks passed!`.
  - `ruff check locations/forms/mage/chantry.py`: exactly one finding, the pre-existing `B007` (`cat_label`) in `ChantryPointForm.__init__`. C2.6 rewrites that method and removes it.
  - `ruff check characters/views/mage/mage.py characters/views/mage/mtahuman.py characters/views/mage/sorcerer.py characters/views/mage/companion.py --statistics`: only the pre-existing codes `E402` (mage.py), `F841` (mage.py), `C416`, `C419` and `E712`. There must be no `F401`.
  - `black --check characters/views/mage/background_views.py characters/views/mage/mage.py characters/views/mage/mtahuman.py characters/views/mage/sorcerer.py characters/views/mage/companion.py locations/forms/mage/chantry.py locations/tests/forms/mage/test_chantry.py characters/tests/views/mage/test_chantry_background.py characters/tests/views/mage/test_mage_chantry_template.py`: unchanged.

## Unit C2: Points service, forms, undo, `linked_object` schema and the Library rule

**Goal.** One module, `locations/services/chantry_points.py`, holds every chantry cost rule and every point mutation (locked and re-checked). `ChantryPointForm` offers and accepts only purchases the service allows. `ChantryRemoveForm` undoes one purchase. Library-type chantries get 3 free, irremovable Library dots. A background rating can record the object realised for it. Nothing is routed in this unit (C4 wires views).

**Verified facts and a spec deviation that the plan author must accept:**
- **`core.Model` is abstract** (`core/models.py`: `class Meta: abstract = True`), so the spec's `ForeignKey("core.Model", …)` cannot be built: syncdb fails with `ValueError: Related model 'core.Model' cannot be resolved`. The linked objects come from two concrete polymorphic roots: Node, Library and Sanctum are `locations.LocationModel`, and Allies NPCs from `LinkedNPCForm` are `characters.CharacterModel`.
  - This plan adds **two** nullable `SET_NULL` FKs with `related_name="+"`: `linked_location` → `locations.LocationModel` and `linked_character` → `characters.CharacterModel`.
  - It also adds a **`linked_object` property** (getter and setter) that gives the spec's single interface. The getter returns the concrete subclass through `get_real_instance()`. The setter routes by type, clears the other FK, and raises `TypeError` for anything else, such as an item.
  - `SET_NULL`-on-delete (spec section 6) works on both FKs; there is a test for a deleted Node.
- `locations` has no migration files. `tg/test_runner.py` syncs such apps, so fresh test databases get both columns from the model. `tg_schema/migrations/0002_chantry_rating_linked_object.py` copies `0001_scene_visibility`: it introspects the table and calls `schema_editor.add_field` for each missing column.
  - `0001` has no test. `0002` gets one, a `TransactionTestCase` that uses real DDL.
  - SQLite rebuilds the table from the live model on `remove_field`, so the test drops **one column at a time**.
  - DB: `DATABASES` is SQLite (`ATOMIC_REQUESTS=True`), and SQLite ignores `select_for_update()`. The locking test is therefore the spec's sequential option: a stale instance must be refused because the service re-reads the locked row.
- The spec's `buy_background_dot(chantry, bg, …)` either creates the rating at 1 or increments it. The service therefore keeps **one rating per background per chantry**:
  - "New Background" offers allowed backgrounds that aren't held;
  - "Existing Background" offers held ratings;
  - both call `buy_background_dot(chantry, bg)`.
  
  With legacy duplicate ratings for one background, the lowest-pk rating is incremented.
- `ChantryPointForm.INTEGRATED_EFFECTS_NUMBERS` is left in place: C5 deletes it, with its tests, according to the spec's Evidence table.
- Effects: `Effect.save()` sets `rote_cost` to the sum of sphere dots and `max_sphere` to the highest one.

### Task 4: [C2.1] `ChantryBackgroundRating.linked_object` with `tg_schema` migration 0002

**Files:**
- Modify: `locations/models/mage/chantry.py` (one import, two FKs, one property on `ChantryBackgroundRating`)
- Create: `tg_schema/migrations/0002_chantry_rating_linked_object.py`
- Create (test): `tg_schema/tests/__init__.py` (empty), `tg_schema/tests/test_chantry_rating_linked_object.py`, `locations/tests/models/mage/test_chantry_rating_link.py`

**Interfaces:**
- `ChantryBackgroundRating.linked_location`: `ForeignKey("locations.LocationModel", null=True, blank=True, on_delete=SET_NULL, related_name="+")`, column `linked_location_id`.
- `ChantryBackgroundRating.linked_character`: `ForeignKey("characters.CharacterModel", null=True, blank=True, on_delete=SET_NULL, related_name="+")`, column `linked_character_id`.
- `ChantryBackgroundRating.linked_object` property. Getter: returns the concrete `LocationModel`/`CharacterModel` subclass instance, or `None`. Setter: accepts `LocationModel | CharacterModel | None` and raises `TypeError` otherwise. The caller saves.
- `tg_schema.migrations.0002_chantry_rating_linked_object`:
  - `LINKED_FIELDS = ("linked_location", "linked_character")`;
  - `add_chantry_rating_linked_object(apps, schema_editor) -> None`;
  - depends on `("tg_schema", "0001_scene_visibility")`.

- [ ] **Step 1: Write the failing tests.**
  - Create `tg_schema/tests/__init__.py` as an empty file.
  - Create `tg_schema/tests/test_chantry_rating_linked_object.py`:

```python
"""tg_schema 0002 adds ChantryBackgroundRating's linked-object columns exactly once."""

import importlib

from django.db import connection
from django.test import TransactionTestCase

from locations.models.mage.chantry import ChantryBackgroundRating

migration = importlib.import_module("tg_schema.migrations.0002_chantry_rating_linked_object")

LINKED_COLUMNS = {"linked_location_id", "linked_character_id"}


def rating_columns():
    with connection.cursor() as cursor:
        return {
            column.name
            for column in connection.introspection.get_table_description(
                cursor, ChantryBackgroundRating._meta.db_table
            )
        }


class ChantryRatingLinkedObjectMigrationTests(TransactionTestCase):
    def fields(self):
        return [ChantryBackgroundRating._meta.get_field(name) for name in migration.LINKED_FIELDS]

    def restore_columns(self):
        missing = [field for field in self.fields() if field.column not in rating_columns()]
        with connection.schema_editor() as editor:
            for field in missing:
                editor.add_field(ChantryBackgroundRating, field)

    def test_adds_each_missing_column(self):
        self.addCleanup(self.restore_columns)
        for field in self.fields():
            with self.subTest(column=field.column):
                # SQLite rebuilds the table from the live model, so drop one
                # column at a time.
                with connection.schema_editor() as editor:
                    editor.remove_field(ChantryBackgroundRating, field)
                self.assertNotIn(field.column, rating_columns())

                with connection.schema_editor() as editor:
                    migration.add_chantry_rating_linked_object(None, editor)

                self.assertEqual(rating_columns() & LINKED_COLUMNS, LINKED_COLUMNS)

    def test_existing_columns_are_left_alone(self):
        self.assertEqual(rating_columns() & LINKED_COLUMNS, LINKED_COLUMNS)
        with connection.schema_editor(collect_sql=True) as editor:
            migration.add_chantry_rating_linked_object(None, editor)
            self.assertEqual(editor.collected_sql, [])
```

  - Create `locations/tests/models/mage/test_chantry_rating_link.py`:

```python
"""ChantryBackgroundRating.linked_object: one link across two polymorphic trees."""

from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from items.models.mage.grimoire import Grimoire
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.node import Node


class TestChantryRatingLinkedObject(TestCase):
    def setUp(self):
        self.chantry = Chantry.objects.create(name="Linked Chantry", total_points=10)
        self.node_bg, _ = Background.objects.get_or_create(
            property_name="node", defaults={"name": "Node"}
        )
        self.rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=self.node_bg, rating=2
        )

    def test_defaults_to_none(self):
        self.assertIsNone(self.rating.linked_object)

    def test_links_a_location_and_returns_the_concrete_class(self):
        node = Node.objects.create(name="Spring", rank=2)
        self.rating.linked_object = node
        self.rating.save()
        rating = ChantryBackgroundRating.objects.get(pk=self.rating.pk)
        self.assertIsInstance(rating.linked_object, Node)
        self.assertEqual(rating.linked_object.pk, node.pk)
        self.assertIsNone(rating.linked_character)

    def test_links_a_character(self):
        ally = Human.objects.create(name="Ally")
        self.rating.linked_object = ally
        self.rating.save()
        rating = ChantryBackgroundRating.objects.get(pk=self.rating.pk)
        self.assertEqual(rating.linked_object.pk, ally.pk)
        self.assertIsNone(rating.linked_location)

    def test_relinking_replaces_the_other_tree(self):
        self.rating.linked_object = Human.objects.create(name="Ally")
        self.rating.linked_object = Node.objects.create(name="Spring", rank=2)
        self.assertIsNone(self.rating.linked_character)
        self.rating.linked_object = None
        self.assertIsNone(self.rating.linked_location)

    def test_rejects_other_objects(self):
        with self.assertRaises(TypeError):
            self.rating.linked_object = Grimoire.objects.create(name="Book")

    def test_deleting_the_linked_node_clears_the_link(self):
        node = Node.objects.create(name="Doomed", rank=2)
        self.rating.linked_object = node
        self.rating.note = "Doomed"
        self.rating.save()
        node.delete()
        self.rating.refresh_from_db()
        self.assertIsNone(self.rating.linked_object)
        self.assertEqual(self.rating.note, "Doomed")
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test tg_schema locations.tests.models.mage.test_chantry_rating_link`.
  - Expected:
    - the `tg_schema` module fails to import: `ModuleNotFoundError: No module named 'tg_schema.migrations.0002_chantry_rating_linked_object'`;
    - the link tests error with `AttributeError: 'ChantryBackgroundRating' object has no attribute 'linked_object'` (or `linked_character`);
    - result: `FAILED (failures=2, errors=5)` over 7 tests.

- [ ] **Step 3: Implement the model fields.** In `locations/models/mage/chantry.py`:
  - add `from characters.models.core.character import CharacterModel` after `from characters.models.core.background_block import BackgroundBlock`;
  - in `ChantryBackgroundRating`, add the fields right after `display_alt_name = models.BooleanField(default=False)`:

```python
    # The object realised for this rating in the chantry wizard: a Node, Library
    # or Sanctum (a location) or an Allies NPC (a character). ``core.Model`` is
    # abstract, so one FK per polymorphic tree; use ``linked_object`` to read or
    # write. Columns added to legacy databases by tg_schema 0002.
    linked_location = models.ForeignKey(
        "locations.LocationModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    linked_character = models.ForeignKey(
        "characters.CharacterModel",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
```

  - add the property right before `def display_name(self):` in `ChantryBackgroundRating`:

```python
    @property
    def linked_object(self):
        """The concrete linked Node, Library, Sanctum or character, or None."""
        linked = self.linked_location or self.linked_character
        return linked.get_real_instance() if linked is not None else None

    @linked_object.setter
    def linked_object(self, obj):
        if obj is not None and not isinstance(obj, LocationModel | CharacterModel):
            raise TypeError(f"Cannot link {type(obj).__name__} to a chantry background")
        self.linked_location = obj if isinstance(obj, LocationModel) else None
        self.linked_character = obj if isinstance(obj, CharacterModel) else None
```

- [ ] **Step 4: Add the migration.** Create `tg_schema/migrations/0002_chantry_rating_linked_object.py`:

```python
"""Add ChantryBackgroundRating's linked-object columns to legacy databases."""

from django.db import migrations

from locations.models.mage.chantry import ChantryBackgroundRating

LINKED_FIELDS = ("linked_location", "linked_character")


def add_chantry_rating_linked_object(apps, schema_editor):
    # ``locations`` has no migration state on legacy installations, so its
    # models are intentionally absent from this migration's historical app
    # registry. Use the live model solely to describe the columns being added.
    rating = ChantryBackgroundRating
    table = rating._meta.db_table
    with schema_editor.connection.cursor() as cursor:
        columns = {
            column.name
            for column in schema_editor.connection.introspection.get_table_description(
                cursor, table
            )
        }
    # Test syncdb already creates these columns from the current model. Existing
    # deployments need the DDL exactly once.
    for name in LINKED_FIELDS:
        field = rating._meta.get_field(name)
        if field.column not in columns:
            schema_editor.add_field(rating, field)


class Migration(migrations.Migration):
    dependencies = [("tg_schema", "0001_scene_visibility")]
    operations = [migrations.RunPython(add_chantry_rating_linked_object, migrations.RunPython.noop)]
```

- [ ] **Step 5: Run the tests and confirm they pass.**
  - Run `python manage.py test tg_schema locations.tests.models.mage.test_chantry_rating_link locations.tests.models.mage.test_chantry`.
  - Expected: `OK`.

- [ ] **Step 6: Commit.**

```bash
git add locations/models/mage/chantry.py tg_schema/migrations/0002_chantry_rating_linked_object.py tg_schema/tests/__init__.py tg_schema/tests/test_chantry_rating_linked_object.py locations/tests/models/mage/test_chantry_rating_link.py
git commit -m "Chantry background ratings can link the object realised for them

core.Model is abstract, so a single FK to it cannot exist. Ratings get
linked_location (Node, Library, Sanctum) and linked_character (Allies
NPCs), both SET_NULL, behind one linked_object property that returns the
concrete subclass. tg_schema 0002 adds the columns to legacy databases
only when missing, following 0001.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 5: [C2.2] Library-type floor in `Chantry` costs

**Files:**
- Modify: `locations/models/mage/chantry.py` (`Chantry`: the new constant, `free_dots`, `bg_cost`, `total_cost`)
- Create (test): `locations/tests/models/mage/test_chantry_library_floor.py`

**Interfaces:**
- `Chantry.LIBRARY_TYPE_FREE_DOTS = 3`.
- `Chantry.free_dots(property_name: str) -> int`: returns 3 for `"library"` when `chantry_type == "library"`, and 0 otherwise. This is the free-dot helper, and it doubles as the removal floor.
- `Chantry.bg_cost(rating) -> int`: `trait_cost(prop) * max(0, rating.rating - free_dots(prop))`.
- `Chantry.total_cost()`: unchanged except that it uses `select_related("bg")`. `points` therefore reflects the floor.

- [ ] **Step 1: Write the failing tests.** Create `locations/tests/models/mage/test_chantry_library_floor.py`:

```python
"""Library-type chantries hold free Library dots that cost nothing."""

from django.test import TestCase

from characters.models.core.background_block import Background
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating


class TestChantryLibraryFloorCost(TestCase):
    def setUp(self):
        self.library_bg, _ = Background.objects.get_or_create(
            property_name="library", defaults={"name": "Library"}
        )

    def make(self, chantry_type, rating):
        chantry = Chantry.objects.create(name="Stacks", total_points=20, chantry_type=chantry_type)
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=self.library_bg, rating=rating)
        return chantry

    def test_free_dots_only_for_library_type_library(self):
        chantry = Chantry(name="Stacks", chantry_type="library")
        self.assertEqual(chantry.free_dots("library"), Chantry.LIBRARY_TYPE_FREE_DOTS)
        self.assertEqual(chantry.free_dots("node"), 0)
        self.assertEqual(Chantry(name="War", chantry_type="war").free_dots("library"), 0)

    def test_library_type_pays_only_above_the_floor(self):
        self.assertEqual(self.make("library", 3).total_cost(), 0)
        self.assertEqual(self.make("library", 5).total_cost(), 4)

    def test_other_types_pay_every_library_dot(self):
        self.assertEqual(self.make("war", 3).total_cost(), 6)
        self.assertEqual(self.make(None, 3).points, 14)
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.models.mage.test_chantry_library_floor`.
  - Expected:
    - `AttributeError: 'Chantry' object has no attribute 'free_dots'`;
    - `AssertionError: 6 != 0` in `test_library_type_pays_only_above_the_floor`;
    - result: `FAILED (failures=1, errors=1)`.

- [ ] **Step 3: Implement the floor.** In `locations/models/mage/chantry.py`:
  - add `LIBRARY_TYPE_FREE_DOTS = 3` as the first line after the closing `}` of `INTEGRATED_EFFECTS_NUMBERS`, followed by a blank line, before `type = "chantry"`;
  - replace the existing `bg_cost` and the first three lines of `total_cost` (through the `for` loop) with:

```python
    def free_dots(self, property_name):
        """Dots of a background this chantry holds at no cost.

        A library-type chantry gets ``LIBRARY_TYPE_FREE_DOTS`` free Library dots,
        which also act as a floor that cannot be removed.
        """
        if property_name == "library" and self.chantry_type == "library":
            return self.LIBRARY_TYPE_FREE_DOTS
        return 0

    def bg_cost(self, background_rating):
        property_name = background_rating.bg.property_name
        paid_dots = max(0, background_rating.rating - self.free_dots(property_name))
        return self.trait_cost(property_name) * paid_dots

    def total_cost(self):
        tot = 0
        for bgr in self.backgrounds.select_related("bg"):
            tot += self.bg_cost(bgr)
```

  - `total_cost` ends as before, with `tot += self.integrated_effects_score * 2` and `return tot`.

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.models.mage.test_chantry_library_floor locations.tests.models.mage.test_chantry locations.tests.forms.mage.test_chantry`.
  - Expected: `OK`.

- [ ] **Step 5: Commit.**

```bash
git add locations/models/mage/chantry.py locations/tests/models/mage/test_chantry_library_floor.py
git commit -m "Library-type chantries get 3 free Library dots in their costs

Chantry.free_dots() gives the floor; bg_cost charges only the dots
above it, so points reflects the Library-type rule. Changing the type
away from library makes the dots paid again.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 6: [C2.3] Points service, purchases (predicates, `buy_background_dot`, `buy_ie_dot`)

**Files:**
- Create: `locations/services/__init__.py` (empty), `locations/services/chantry_points.py`
- Create (test): `locations/tests/services/__init__.py` (empty), `locations/tests/services/test_chantry_points.py`

**Interfaces** (module `locations.services.chantry_points`):
- constants: `MAX_BACKGROUND_RATING = 5`, `MAX_IE_SCORE = 10`.
- `next_dot_cost(chantry, bg, current_rating=None) -> int`: 0 below `chantry.free_dots(bg.property_name)`, otherwise `trait_cost`.
- `background_purchase_error(chantry, bg, *, points=None, current_rating=None) -> str | None`: returns the allow-list, 5-cap or cost message, or `None`.
- `can_buy_background(chantry, bg) -> bool`.
- `ie_purchase_error(chantry, *, points=None) -> str | None`; `can_buy_ie(chantry) -> bool`, which is true when `score < 10` and `points >= 2`.
- `affordable_backgrounds(chantry) -> tuple[list[Background], list[ChantryBackgroundRating]]`: the allowed backgrounds not yet held that can take a dot, and the held ratings that can take a dot. It computes `points` once.
- `has_affordable_purchase(chantry) -> bool`.
- `buy_background_dot(chantry, bg, *, note="", display_alt_name=False) -> ChantryBackgroundRating`: creates the rating at 1 or increments the held one.
- `buy_ie_dot(chantry) -> int` returns the new score and also updates the passed instance's `integrated_effects_score`.
- Both `buy_*` functions run in `transaction.atomic()`, lock with `Chantry.objects.select_for_update()`, re-check against the locked row, and raise `django.core.exceptions.ValidationError(message)` when refused.

- [ ] **Step 1: Write the failing tests.**
  - Create `locations/tests/services/__init__.py` as an empty file.
  - Create `locations/tests/services/test_chantry_points.py` with the header, base class and the first two test classes. Tasks C2.4 and C2.5 append the rest.

```python
"""Tests for the chantry points service (M20 chantry costs and caps)."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.tests.utils import mage_setup
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.services import chantry_points as svc


class ChantryPointsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        mage_setup()
        cls.allies = Background.objects.get(property_name="allies")
        cls.node = Background.objects.get(property_name="node")
        cls.resources = Background.objects.get(property_name="resources")
        cls.requisitions = Background.objects.get(property_name="requisitions")
        cls.sanctum = Background.objects.get(property_name="sanctum")
        cls.library = Background.objects.get(property_name="library")
        cls.fame = Background.objects.get(property_name="fame")

    def make_chantry(self, total_points=20, **kwargs):
        return Chantry.objects.create(name="Test Chantry", total_points=total_points, **kwargs)

    def rate(self, chantry, bg, rating):
        return ChantryBackgroundRating.objects.create(chantry=chantry, bg=bg, rating=rating)


class TestCostsAndCaps(ChantryPointsTestCase):
    def test_every_cost_tier(self):
        chantry = self.make_chantry(total_points=100)
        for bg, cost in [
            (self.allies, 2),
            (self.node, 3),
            (self.resources, 3),
            (self.requisitions, 4),
            (self.sanctum, 5),
        ]:
            with self.subTest(bg=bg.property_name):
                self.assertEqual(svc.next_dot_cost(chantry, bg), cost)
                before = chantry.points
                svc.buy_background_dot(chantry, bg)
                self.assertEqual(before - chantry.points, cost)
        before = chantry.points
        svc.buy_ie_dot(chantry)
        self.assertEqual(before - chantry.points, 2)

    def test_only_allowed_backgrounds(self):
        chantry = self.make_chantry()
        self.assertFalse(svc.can_buy_background(chantry, self.fame))
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.fame)
        self.assertFalse(chantry.backgrounds.exists())

    def test_five_dot_cap(self):
        chantry = self.make_chantry(total_points=100)
        self.rate(chantry, self.allies, 5)
        self.assertFalse(svc.can_buy_background(chantry, self.allies))
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.allies)

    def test_ie_cap_of_ten(self):
        chantry = self.make_chantry(total_points=100, integrated_effects_score=10)
        self.assertFalse(svc.can_buy_ie(chantry))
        with self.assertRaises(ValidationError):
            svc.buy_ie_dot(chantry)
        chantry.refresh_from_db()
        self.assertEqual(chantry.integrated_effects_score, 10)

    def test_insufficient_points(self):
        chantry = self.make_chantry(total_points=4)
        self.assertTrue(svc.can_buy_background(chantry, self.requisitions))
        self.assertFalse(svc.can_buy_background(chantry, self.sanctum))
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.sanctum)
        chantry.total_points = 1
        chantry.save()
        self.assertFalse(svc.can_buy_ie(chantry))
        with self.assertRaises(ValidationError):
            svc.buy_ie_dot(chantry)

    def test_buy_creates_then_increments_one_rating(self):
        chantry = self.make_chantry()
        first = svc.buy_background_dot(chantry, self.allies, note="Friends", display_alt_name=True)
        self.assertEqual((first.rating, first.note, first.display_alt_name), (1, "Friends", True))
        second = svc.buy_background_dot(chantry, self.allies)
        self.assertEqual(second.pk, first.pk)
        self.assertEqual(second.rating, 2)
        self.assertEqual(chantry.backgrounds.count(), 1)

    def test_purchase_rechecks_the_locked_row(self):
        chantry = self.make_chantry(total_points=10)
        stale = Chantry.objects.get(pk=chantry.pk)
        Chantry.objects.filter(pk=chantry.pk).update(total_points=0)
        # ``stale`` still says 10 points; the service must trust the locked row.
        self.assertEqual(stale.total_points, 10)
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(stale, self.allies)
        with self.assertRaises(ValidationError):
            svc.buy_ie_dot(stale)
        self.assertFalse(ChantryBackgroundRating.objects.filter(chantry=chantry).exists())

    def test_sequential_double_spend_is_refused(self):
        chantry = self.make_chantry(total_points=2)
        first_view = Chantry.objects.get(pk=chantry.pk)
        second_view = Chantry.objects.get(pk=chantry.pk)
        svc.buy_background_dot(first_view, self.allies)
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(second_view, self.node)
        chantry.refresh_from_db()
        self.assertEqual(chantry.points, 0)


class TestHasAffordablePurchase(ChantryPointsTestCase):
    def test_true_with_points_to_spend(self):
        self.assertTrue(svc.has_affordable_purchase(self.make_chantry(total_points=2)))

    def test_false_with_one_point(self):
        self.assertFalse(svc.has_affordable_purchase(self.make_chantry(total_points=1)))

    def test_false_when_everything_affordable_is_capped(self):
        chantry = self.make_chantry(total_points=200, integrated_effects_score=10)
        for property_name in Chantry.allowed_backgrounds:
            bg, _ = Background.objects.get_or_create(
                property_name=property_name, defaults={"name": property_name.title()}
            )
            self.rate(chantry, bg, 5)
        self.assertGreater(chantry.points, 0)
        self.assertFalse(svc.has_affordable_purchase(chantry))

    def test_affordable_backgrounds_splits_new_and_existing(self):
        chantry = self.make_chantry(total_points=5)  # 3 left after Allies 1
        allies = self.rate(chantry, self.allies, 1)
        new, existing = svc.affordable_backgrounds(chantry)
        self.assertEqual(existing, [allies])
        self.assertIn(self.node, new)
        self.assertNotIn(self.allies, new)
        self.assertNotIn(self.sanctum, new)
        self.assertNotIn(self.fame, new)
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.services.test_chantry_points`.
  - Expected: `ModuleNotFoundError: No module named 'locations.services'`, then `FAILED`.

- [ ] **Step 3: Implement the service.**
  - Create `locations/services/__init__.py` as an empty file.
  - Create `locations/services/chantry_points.py`:

```python
"""M20 chantry point rules: the single source of chantry costs and caps.

Predicates (``can_*``, ``*_error``, ``has_affordable_purchase``) read the
chantry as passed. Mutations lock the chantry row with ``select_for_update``
inside ``transaction.atomic()``, re-check their preconditions against the
locked row and raise ``ValidationError`` when a rule is broken. Views, forms
and templates never compute costs themselves.
"""

from django.core.exceptions import ValidationError
from django.db import transaction

from characters.models.core.background_block import Background
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating

MAX_BACKGROUND_RATING = 5
MAX_IE_SCORE = 10


def _lock(chantry):
    return Chantry.objects.select_for_update().get(pk=chantry.pk)


def _held_rating(chantry, bg):
    return chantry.backgrounds.filter(bg=bg).order_by("pk").first()


def next_dot_cost(chantry, bg, current_rating=None):
    """Point cost of the next dot of ``bg``; dots under the free floor cost 0."""
    if current_rating is None:
        held = _held_rating(chantry, bg)
        current_rating = held.rating if held is not None else 0
    if current_rating < chantry.free_dots(bg.property_name):
        return 0
    return chantry.trait_cost(bg.property_name)


def background_purchase_error(chantry, bg, *, points=None, current_rating=None):
    """Why one more dot of ``bg`` cannot be bought, or None when it can."""
    if bg.property_name not in Chantry.allowed_backgrounds:
        return f"{bg} is not a chantry background."
    if current_rating is None:
        held = _held_rating(chantry, bg)
        current_rating = held.rating if held is not None else 0
    if current_rating >= MAX_BACKGROUND_RATING:
        return f"{bg} is already at {MAX_BACKGROUND_RATING} dots."
    if points is None:
        points = chantry.points
    cost = next_dot_cost(chantry, bg, current_rating)
    if cost > points:
        return f"{bg} costs {cost} points; {points} remain."
    return None


def can_buy_background(chantry, bg):
    return background_purchase_error(chantry, bg) is None


def ie_purchase_error(chantry, *, points=None):
    """Why one more Integrated Effects dot cannot be bought, or None."""
    if chantry.integrated_effects_score >= MAX_IE_SCORE:
        return f"Integrated Effects is already at {MAX_IE_SCORE}."
    if points is None:
        points = chantry.points
    cost = chantry.trait_cost("integrated_effects")
    if cost > points:
        return f"Integrated Effects costs {cost} points; {points} remain."
    return None


def can_buy_ie(chantry):
    return ie_purchase_error(chantry) is None


def affordable_backgrounds(chantry):
    """(new, existing): allowed Backgrounds not yet held, and held ratings,
    each of which can take one more dot now."""
    points = chantry.points
    held = {}
    for rating in chantry.backgrounds.select_related("bg").order_by("pk"):
        held.setdefault(rating.bg_id, rating)
    new, existing = [], []
    allowed = Background.objects.filter(property_name__in=Chantry.allowed_backgrounds)
    for bg in allowed.order_by("name"):
        rating = held.get(bg.pk)
        current = rating.rating if rating is not None else 0
        if background_purchase_error(chantry, bg, points=points, current_rating=current):
            continue
        if rating is None:
            new.append(bg)
        else:
            existing.append(rating)
    return new, existing


def has_affordable_purchase(chantry):
    new, existing = affordable_backgrounds(chantry)
    return bool(new or existing) or can_buy_ie(chantry)


def buy_background_dot(chantry, bg, *, note="", display_alt_name=False):
    """Buy one dot of ``bg``: create its rating at 1 or raise the held one."""
    with transaction.atomic():
        locked = _lock(chantry)
        error = background_purchase_error(locked, bg)
        if error:
            raise ValidationError(error)
        rating = _held_rating(locked, bg)
        if rating is None:
            return ChantryBackgroundRating.objects.create(
                chantry=locked,
                bg=bg,
                rating=1,
                note=note,
                display_alt_name=display_alt_name,
            )
        rating.rating += 1
        rating.save(update_fields=["rating"])
        return rating


def buy_ie_dot(chantry):
    """Buy one Integrated Effects dot. Returns the new score."""
    with transaction.atomic():
        locked = _lock(chantry)
        error = ie_purchase_error(locked)
        if error:
            raise ValidationError(error)
        locked.integrated_effects_score += 1
        locked.save(update_fields=["integrated_effects_score"])
        chantry.integrated_effects_score = locked.integrated_effects_score
        return locked.integrated_effects_score
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.services.test_chantry_points`.
  - Expected: `OK` (12 tests).

- [ ] **Step 5: Commit.**

```bash
git add locations/services/__init__.py locations/services/chantry_points.py locations/tests/services/__init__.py locations/tests/services/test_chantry_points.py
git commit -m "Add the chantry points service: purchase rules

One module owns chantry costs: allow-list, 5-dot cap, IE cap of 10, cost
against remaining points and the Library free-dot floor. Purchases lock
the chantry row and re-check against it, so a stale or concurrent spend
is refused with ValidationError.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 7: [C2.4] Points service, undo (`remove_background_dot`, `remove_ie_dot`, `remove_effect`)

**Files:**
- Modify: `locations/services/chantry_points.py` (append)
- Modify (test): `locations/tests/services/test_chantry_points.py` (imports, and append `TestRemoval`)

**Interfaces:**
- `background_removal_error(rating) -> str | None`: refuses when `rating.rating <= rating.chantry.free_dots(prop)`.
- `remove_background_dot(rating) -> ChantryBackgroundRating | None`: decrements the rating and deletes it at 0, returning `None`. If the rating was linked, the service:
  - removes the linked location from `chantry.nodes`;
  - if it is `chantry.chantry_library`, removes `chantry` from the library's `contained_within` and sets `chantry_library = None`;
  - clears `linked_object`, `url` and `note`, and sets `complete=False`.
  
  The object itself is never deleted.
- `ie_removal_error(chantry) -> str | None`: refuses at 0, or when `spent_integrated_effect_points()` exceeds `INTEGRATED_EFFECTS_NUMBERS[score - 1]`.
- `remove_ie_dot(chantry) -> int`: returns the new score and updates the passed instance.
- `remove_effect(chantry, effect) -> None`: raises `ValidationError` if the effect wasn't chosen.
- All three mutations are locked and re-checked the same way as the purchases.

- [ ] **Step 1: Write the failing tests.**
  - In `locations/tests/services/test_chantry_points.py`, replace the import block (everything above `class ChantryPointsTestCase`) with:

```python
"""Tests for the chantry points service (M20 chantry costs and caps)."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.models.mage.effect import Effect
from characters.tests.utils import mage_setup
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.library import Library
from locations.models.mage.node import Node
from locations.services import chantry_points as svc
```

  - Append to the file:

```python
class TestRemoval(ChantryPointsTestCase):
    def test_refund_one_dot(self):
        chantry = self.make_chantry()
        rating = self.rate(chantry, self.node, 2)
        points = chantry.points
        result = svc.remove_background_dot(rating)
        self.assertEqual(result.rating, 1)
        self.assertEqual(chantry.points, points + 3)

    def test_rating_deleted_at_zero(self):
        chantry = self.make_chantry()
        rating = self.rate(chantry, self.allies, 1)
        self.assertIsNone(svc.remove_background_dot(rating))
        self.assertFalse(ChantryBackgroundRating.objects.filter(pk=rating.pk).exists())

    def test_removal_detaches_linked_node(self):
        chantry = self.make_chantry()
        node = Node.objects.create(name="Well", rank=2)
        chantry.add_node(node)
        rating = self.rate(chantry, self.node, 2)
        rating.linked_object = node
        rating.note = "Well"
        rating.url = node.get_absolute_url()
        rating.complete = True
        rating.save()

        svc.remove_background_dot(rating)

        rating.refresh_from_db()
        self.assertEqual(rating.rating, 1)
        self.assertIsNone(rating.linked_object)
        self.assertEqual((rating.note, rating.url, rating.complete), ("", "", False))
        self.assertFalse(chantry.nodes.filter(pk=node.pk).exists())
        self.assertTrue(Node.objects.filter(pk=node.pk).exists())

    def test_removal_detaches_linked_library(self):
        chantry = self.make_chantry()
        library = Library.objects.create(name="Stacks", rank=1)
        chantry.chantry_library = library
        chantry.save()
        library.contained_within.add(chantry)
        rating = self.rate(chantry, self.library, 1)
        rating.linked_object = library
        rating.complete = True
        rating.save()

        self.assertIsNone(svc.remove_background_dot(rating))

        chantry.refresh_from_db()
        self.assertIsNone(chantry.chantry_library)
        self.assertFalse(library.contained_within.filter(pk=chantry.pk).exists())
        self.assertTrue(Library.objects.filter(pk=library.pk).exists())

    def test_removal_unlinks_ally_without_deleting_it(self):
        chantry = self.make_chantry()
        ally = Human.objects.create(name="Friendly Face")
        rating = self.rate(chantry, self.allies, 2)
        rating.linked_object = ally
        rating.complete = True
        rating.save()

        svc.remove_background_dot(rating)

        rating.refresh_from_db()
        self.assertIsNone(rating.linked_object)
        self.assertFalse(rating.complete)
        self.assertTrue(Human.objects.filter(pk=ally.pk).exists())

    def test_ie_removal_refused_when_effects_would_overcommit(self):
        chantry = self.make_chantry(integrated_effects_score=2)  # 8 IE points
        effect = Effect.objects.create(name="Big Ward", forces=3, prime=2)  # rote_cost 5
        chantry.integrated_effects.add(effect)
        with self.assertRaises(ValidationError):
            svc.remove_ie_dot(chantry)  # IE 1 allows only 4
        chantry.refresh_from_db()
        self.assertEqual(chantry.integrated_effects_score, 2)

        svc.remove_effect(chantry, effect)
        self.assertEqual(svc.remove_ie_dot(chantry), 1)
        chantry.refresh_from_db()
        self.assertEqual(chantry.integrated_effects_score, 1)

    def test_ie_removal_refused_at_zero(self):
        chantry = self.make_chantry()
        with self.assertRaises(ValidationError):
            svc.remove_ie_dot(chantry)

    def test_remove_effect_not_chosen_is_refused(self):
        chantry = self.make_chantry()
        effect = Effect.objects.create(name="Loose", forces=1)
        with self.assertRaises(ValidationError):
            svc.remove_effect(chantry, effect)
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.services.test_chantry_points`.
  - Expected: 8 errors, `AttributeError: module 'locations.services.chantry_points' has no attribute 'remove_background_dot'` (or `remove_ie_dot`/`remove_effect`).

- [ ] **Step 3: Implement the undo functions.** Append to `locations/services/chantry_points.py`:

```python
def background_removal_error(rating):
    """Why ``rating`` cannot lose a dot, or None when it can."""
    floor = rating.chantry.free_dots(rating.bg.property_name)
    if rating.rating <= floor:
        return f"The first {floor} {rating.bg} dots are free and cannot be removed."
    return None


def _detach_linked_object(chantry, rating):
    linked_location_id = rating.linked_location_id
    if linked_location_id is not None:
        chantry.nodes.remove(linked_location_id)
        if chantry.chantry_library_id == linked_location_id:
            chantry.chantry_library.contained_within.remove(chantry)
            chantry.chantry_library = None
            chantry.save(update_fields=["chantry_library"])
    rating.linked_object = None
    rating.url = ""
    rating.note = ""
    rating.complete = False


def remove_background_dot(rating):
    """Refund one dot. A rating that reaches 0 is deleted.

    A linked Node or Library is detached from the chantry and the link, note
    and URL are cleared so the wizard asks for it again. The linked object
    itself is never deleted.
    """
    with transaction.atomic():
        locked = _lock(rating.chantry)
        rating = ChantryBackgroundRating.objects.select_related("bg").get(
            pk=rating.pk, chantry=locked
        )
        rating.chantry = locked
        error = background_removal_error(rating)
        if error:
            raise ValidationError(error)
        if rating.linked_location_id or rating.linked_character_id:
            _detach_linked_object(locked, rating)
        rating.rating -= 1
        if rating.rating == 0:
            rating.delete()
            return None
        rating.save()
        return rating


def ie_removal_error(chantry):
    """Why the Integrated Effects score cannot drop by one, or None."""
    score = chantry.integrated_effects_score
    if score <= 0:
        return "Integrated Effects is already at 0."
    allowance = Chantry.INTEGRATED_EFFECTS_NUMBERS[score - 1]
    spent = chantry.spent_integrated_effect_points()
    if spent > allowance:
        return (
            f"Chosen effects use {spent} points; Integrated Effects {score - 1} "
            f"allows {allowance}. Remove an effect first."
        )
    return None


def remove_ie_dot(chantry):
    """Refund one Integrated Effects dot. Returns the new score."""
    with transaction.atomic():
        locked = _lock(chantry)
        error = ie_removal_error(locked)
        if error:
            raise ValidationError(error)
        locked.integrated_effects_score -= 1
        locked.save(update_fields=["integrated_effects_score"])
        chantry.integrated_effects_score = locked.integrated_effects_score
        return locked.integrated_effects_score


def remove_effect(chantry, effect):
    """Remove a chosen integrated effect, freeing its IE points."""
    with transaction.atomic():
        locked = _lock(chantry)
        if not locked.integrated_effects.filter(pk=effect.pk).exists():
            raise ValidationError(f"{effect} is not one of this chantry's effects.")
        locked.integrated_effects.remove(effect)
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.services.test_chantry_points`.
  - Expected: `OK` (20 tests).

- [ ] **Step 5: Commit.**

```bash
git add locations/services/chantry_points.py locations/tests/services/test_chantry_points.py
git commit -m "Chantry points service: refund a dot, an IE dot or an effect

Removing a background dot refunds it, deletes the rating at 0 and, when
the rating was linked, detaches the Node or Library from the chantry and
clears the link so the wizard asks again. An IE removal that would leave
chosen effects over budget is refused. The free Library floor cannot be
removed.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 8: [C2.5] `apply_type_grants`, and chargen-created chantries receive it

**Files:**
- Modify: `locations/services/chantry_points.py` (append)
- Modify: `locations/forms/mage/chantry.py` (import, and one line in `ChantrySelectOrCreateForm.save`)
- Modify (test): `locations/tests/services/test_chantry_points.py` (append `TestLibraryTypeRule`), `locations/tests/forms/mage/test_chantry.py` (append `TestChantrySelectOrCreateFormTypeGrants`)

**Interfaces:**
- `apply_type_grants(chantry) -> ChantryBackgroundRating | None`:
  - for a `library`-type chantry, it creates the Library rating at `LIBRARY_TYPE_FREE_DOTS` or raises it to that level; dots above 3 are kept;
  - for other types it returns `None` and changes nothing;
  - it is locked, and it `get_or_create`s the `library` Background.
  
  C4 calls it after `ChantryBasicsView` saves and after `ChantryUpdateView` saves.
- `ChantrySelectOrCreateForm.save()` (create path) now calls `chantry_points.apply_type_grants(chantry)` after `save_m2m()`.

- [ ] **Step 1: Write the failing tests.**
  - Append to `locations/tests/services/test_chantry_points.py`:

```python
class TestLibraryTypeRule(ChantryPointsTestCase):
    def test_apply_type_grants_creates_free_library_dots(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        rating = svc.apply_type_grants(chantry)
        self.assertEqual((rating.bg, rating.rating), (self.library, 3))
        self.assertEqual(chantry.points, 10)

    def test_apply_type_grants_raises_to_floor_and_keeps_more(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        rating = self.rate(chantry, self.library, 1)
        svc.apply_type_grants(chantry)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)
        rating.rating = 4
        rating.save()
        svc.apply_type_grants(chantry)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 4)
        self.assertEqual(chantry.backgrounds.count(), 1)

    def test_apply_type_grants_ignores_other_types(self):
        chantry = self.make_chantry(chantry_type="war")
        self.assertIsNone(svc.apply_type_grants(chantry))
        self.assertFalse(chantry.backgrounds.exists())

    def test_dots_above_floor_are_paid_and_capped(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        svc.apply_type_grants(chantry)
        self.assertEqual(svc.next_dot_cost(chantry, self.library), 2)
        svc.buy_background_dot(chantry, self.library)
        svc.buy_background_dot(chantry, self.library)
        self.assertEqual(chantry.points, 6)
        with self.assertRaises(ValidationError):
            svc.buy_background_dot(chantry, self.library)

    def test_floor_cannot_be_removed(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        rating = svc.apply_type_grants(chantry)
        svc.buy_background_dot(chantry, self.library)
        rating.refresh_from_db()
        svc.remove_background_dot(rating)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)
        with self.assertRaises(ValidationError):
            svc.remove_background_dot(rating)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 3)

    def test_dots_become_paid_when_type_changes(self):
        chantry = self.make_chantry(total_points=10, chantry_type="library")
        svc.apply_type_grants(chantry)
        chantry.chantry_type = "war"
        chantry.save()
        self.assertEqual(chantry.points, 4)
```

  - Append to `locations/tests/forms/mage/test_chantry.py`:

```python
class TestChantrySelectOrCreateFormTypeGrants(TestChantrySelectOrCreateFormSetup):
    def test_creating_library_type_grants_free_library_dots(self):
        form = ChantrySelectOrCreateForm(
            data={"create_new": "on", "name": "Stacks", "chantry_type": "library"},
            character=self.character,
            points=4,
        )
        self.assertTrue(form.is_valid(), form.errors)
        chantry = form.save()
        rating = chantry.backgrounds.get(bg__property_name="library")
        self.assertEqual(rating.rating, 3)
        self.assertEqual(chantry.points, 4)
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.services.test_chantry_points locations.tests.forms.mage.test_chantry`.
  - Expected:
    - `AttributeError: module 'locations.services.chantry_points' has no attribute 'apply_type_grants'` (6 errors);
    - `ChantryBackgroundRating.DoesNotExist` in `test_creating_library_type_grants_free_library_dots`;
    - result: `FAILED (errors=7)`.

- [ ] **Step 3: Implement the grants.**
  - Append to `locations/services/chantry_points.py`:

```python
def apply_type_grants(chantry):
    """Give a library-type chantry its free Library dots.

    Creates the Library rating at the free floor or raises it to the floor.
    Does nothing for other types; dots already above the floor are kept.
    Returns the Library rating, or None when no grant applies.
    """
    with transaction.atomic():
        locked = _lock(chantry)
        floor = locked.free_dots("library")
        if floor == 0:
            return None
        library, _ = Background.objects.get_or_create(
            property_name="library", defaults={"name": "Library"}
        )
        rating = _held_rating(locked, library)
        if rating is None:
            return ChantryBackgroundRating.objects.create(chantry=locked, bg=library, rating=floor)
        if rating.rating < floor:
            rating.rating = floor
            rating.save(update_fields=["rating"])
        return rating
```

  - In `locations/forms/mage/chantry.py`, add `from locations.services import chantry_points` after `from locations.models.mage.chantry import ChantryBackgroundRating`.
  - In `ChantrySelectOrCreateForm.save`, change the create branch's tail to:

```python
                chantry.save()
                self.save_m2m()
                chantry_points.apply_type_grants(chantry)
                return chantry
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.services.test_chantry_points locations.tests.forms.mage.test_chantry characters.tests.views.mage.test_chantry_background`.
  - Expected: `OK`.

- [ ] **Step 5: Commit.**

```bash
git add locations/services/chantry_points.py locations/forms/mage/chantry.py locations/tests/services/test_chantry_points.py locations/tests/forms/mage/test_chantry.py
git commit -m "Library-type chantries receive their 3 free Library dots

apply_type_grants creates or raises the Library rating to the free
floor. Chantries created from a character's Chantry background get it
immediately; C4 wires it into the wizard Basics and the ST edit form.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 9: [C2.6] `ChantryPointForm` offers and accepts only what the service allows

**Files:**
- Modify: `locations/forms/mage/chantry.py` (`ChantryPointForm` body, everything after `INTEGRATED_EFFECTS_NUMBERS`)
- Modify (test): `locations/tests/forms/mage/test_chantry.py` (import `ValidationError`; append two classes)

**Interfaces:**
- `ChantryPointForm(data=None, *, pk: int)`, unchanged construction.
  - Class constants: `IE = "Integrated Effects"`, `NEW = "New Background"`, `EXISTING = "Existing Background"`.
  - `category` choices: `"-----"`, plus each of IE, NEW and EXISTING only when the service offers something in it.
  - `example.choices_map[NEW]` holds `(str(Background.pk), str(bg))` pairs; `[EXISTING]` holds `(str(ChantryBackgroundRating.pk), str(rating))` pairs.
- `clean()` re-runs `ie_purchase_error`/`background_purchase_error`. A forged, disallowed, unaffordable, capped, foreign-rating or non-numeric `example` is a non-field error. It sets `self.background`.
- `save() -> int | ChantryBackgroundRating | None` goes through the service. It **may raise `ValidationError`** when a concurrent spend used the points after `is_valid()`, so C4's view must catch it, call `form.add_error(None, e)` and re-render.

- [ ] **Step 1: Write the failing tests.**
  - In `locations/tests/forms/mage/test_chantry.py`, add `from django.core.exceptions import ValidationError` after `from django.contrib.auth.models import User`.
  - Append to the file:

```python
class TestChantryPointFormRules(TestChantryPointFormSetup):
    """Choices and validation follow the points service."""

    def form(self, data=None, **chantry_fields):
        Chantry.objects.filter(pk=self.chantry.pk).update(**chantry_fields)
        return ChantryPointForm(data=data, pk=self.chantry.pk)

    def examples(self, form, category):
        return {value for value, _ in form.fields["example"].choices_map[category]}

    def test_new_background_choices_are_allowed_and_affordable(self):
        form = self.form(total_points=4)
        examples = self.examples(form, "New Background")
        self.assertIn(str(self.background.pk), examples)
        requisitions = Background.objects.get(property_name="requisitions")
        self.assertIn(str(requisitions.pk), examples)
        for property_name in ["sanctum", "fame", "avatar"]:
            bg = Background.objects.get(property_name=property_name)
            self.assertNotIn(str(bg.pk), examples)

    def test_capped_rating_not_offered_as_existing(self):
        capped = ChantryBackgroundRating.objects.create(
            bg=self.background, chantry=self.chantry, rating=5
        )
        form = self.form()
        self.assertNotIn("Existing Background", dict(form.fields["category"].choices))
        self.assertNotIn(str(capped.pk), self.examples(form, "Existing Background"))
        self.assertNotIn(str(self.background.pk), self.examples(form, "New Background"))

    def test_no_points_leaves_only_placeholder(self):
        form = self.form(total_points=1)
        self.assertEqual([value for value, _ in form.fields["category"].choices], ["-----"])

    def test_forged_disallowed_background_fails(self):
        fame = Background.objects.get(property_name="fame")
        form = self.form({"category": "New Background", "example": str(fame.pk)})
        self.assertFalse(form.is_valid())

    def test_forged_unaffordable_background_fails(self):
        sanctum = Background.objects.get(property_name="sanctum")
        form = self.form({"category": "New Background", "example": str(sanctum.pk)}, total_points=4)
        self.assertFalse(form.is_valid())

    def test_forged_ie_at_cap_fails(self):
        form = self.form({"category": "Integrated Effects"}, integrated_effects_score=10)
        self.assertFalse(form.is_valid())

    def test_forged_other_chantrys_rating_fails(self):
        other = Chantry.objects.create(name="Other", total_points=20)
        foreign = ChantryBackgroundRating.objects.create(
            bg=self.background, chantry=other, rating=1
        )
        form = self.form({"category": "Existing Background", "example": str(foreign.pk)})
        self.assertFalse(form.is_valid())

    def test_forged_non_numeric_example_fails(self):
        form = self.form({"category": "New Background", "example": "allies"})
        self.assertFalse(form.is_valid())

    def test_save_new_background_keeps_note_and_alt_name(self):
        form = self.form(
            {
                "category": "New Background",
                "example": str(self.background.pk),
                "note": "Old friends",
                "display_alt_name": True,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        rating = form.save()
        self.assertEqual(
            (rating.rating, rating.note, rating.display_alt_name), (1, "Old friends", True)
        )
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.points, 18)

    def test_save_raises_when_points_were_spent_meanwhile(self):
        form = self.form({"category": "Integrated Effects"}, total_points=2)
        self.assertTrue(form.is_valid())
        Chantry.objects.filter(pk=self.chantry.pk).update(total_points=0)
        with self.assertRaises(ValidationError):
            form.save()


class TestChantryEffectsFormCostLimit(TestCase):
    """Only effects that fit the remaining IE points and chantry rank are offered."""

    @classmethod
    def setUpTestData(cls):
        mage_setup()
        cls.chantry = Chantry.objects.create(
            name="Ward Chantry", total_points=20, integrated_effects_score=1
        )  # rank 2, 4 IE points
        cls.fits = Effect.objects.create(name="Small Ward", forces=2, prime=2)  # cost 4
        cls.too_costly = Effect.objects.create(name="Big Ward", forces=2, prime=2, mind=1)

    def test_queryset_respects_remaining_ie_points(self):
        form = ChantryEffectsForm(pk=self.chantry.pk)
        self.assertIn(self.fits, form.fields["select"].queryset)
        self.assertNotIn(self.too_costly, form.fields["select"].queryset)
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.forms.mage.test_chantry`.
  - Expected: `FAILED (failures=6, errors=1)`, verified by replay:
    - failures:
      - `test_new_background_choices_are_allowed_and_affordable` (Sanctum, Fame and Avatar are offered);
      - `test_capped_rating_not_offered_as_existing`;
      - `test_no_points_leaves_only_placeholder`;
      - `test_forged_disallowed_background_fails`;
      - `test_forged_unaffordable_background_fails`;
      - `test_save_raises_when_points_were_spent_meanwhile`;
    - the error is `test_save_new_background_keeps_note_and_alt_name` (the old save returns `None`).
  - `test_forged_ie_at_cap_fails`, `test_forged_other_chantrys_rating_fails` and `test_forged_non_numeric_example_fails` already pass. The old category and choice checks reject those inputs; the tests keep them rejected after the rewrite.
  - `TestChantryEffectsFormCostLimit` already passes. It pins the spec's IE-effect cost limit for C4.

- [ ] **Step 3: Implement the form.** In `locations/forms/mage/chantry.py`, keep `class ChantryPointForm(...)` and its `INTEGRATED_EFFECTS_NUMBERS` dict (C5 deletes it). Replace everything after that dict, up to the `# Form for choosing effects` comment, with:

```python
    IE = "Integrated Effects"
    NEW = "New Background"
    EXISTING = "Existing Background"

    category = ChainedChoiceField(choices=[])
    example = ChainedChoiceField(parent_field="category", choices_map={}, required=False)
    note = forms.CharField(max_length=300, required=False)
    display_alt_name = forms.BooleanField(required=False)

    # Conditional field visibility rules
    conditional_fields = {
        "category": {
            "example": {"exclude": ["-----", "Integrated Effects"]},
            "note": {"values": ["New Background"]},
            "display_alt_name": {"values": ["New Background"]},
        }
    }

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        self.object = Chantry.objects.get(pk=pk)
        super().__init__(*args, **kwargs)

        # Only options the points service says are allowed and affordable.
        new, existing = chantry_points.affordable_backgrounds(self.object)
        category_choices = [("-----", "-----")]
        if chantry_points.can_buy_ie(self.object):
            category_choices.append((self.IE, self.IE))
        if new:
            category_choices.append((self.NEW, self.NEW))
        if existing:
            category_choices.append((self.EXISTING, self.EXISTING))
        self.fields["category"].choices = category_choices

        example_choices_map = {value: [] for value, _ in category_choices}
        example_choices_map[self.NEW] = [(str(bg.pk), str(bg)) for bg in new]
        example_choices_map[self.EXISTING] = [(str(r.pk), str(r)) for r in existing]
        self.fields["example"].choices_map = example_choices_map

        # Re-run chain setup after choices configured
        self._setup_chains()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        example = str(cleaned_data.get("example") or "")
        self.background = None

        if category == self.IE:
            error = chantry_points.ie_purchase_error(self.object)
        elif category in (self.NEW, self.EXISTING):
            if not example:
                raise forms.ValidationError("Need to choose a Background")
            if not example.isdigit():
                raise forms.ValidationError("Choose a valid Background.")
            if category == self.NEW:
                self.background = Background.objects.filter(pk=example).first()
                current = None
            else:
                rating = self.object.backgrounds.select_related("bg").filter(pk=example).first()
                self.background = rating.bg if rating is not None else None
                current = rating.rating if rating is not None else None
            if self.background is None:
                raise forms.ValidationError("Choose a valid Background.")
            error = chantry_points.background_purchase_error(
                self.object, self.background, current_rating=current
            )
        else:
            error = None
        if error:
            raise forms.ValidationError(error)
        return cleaned_data

    def save(self, commit=True):
        """Spend the points through the service.

        Returns the new Integrated Effects score, the bought
        ``ChantryBackgroundRating``, or None for "-----". Raises
        ``ValidationError`` if a concurrent purchase used the points first.
        """
        category = self.cleaned_data["category"]
        if category == self.IE:
            return chantry_points.buy_ie_dot(self.object)
        if category == self.NEW:
            return chantry_points.buy_background_dot(
                self.object,
                self.background,
                note=self.cleaned_data["note"],
                display_alt_name=self.cleaned_data["display_alt_name"],
            )
        if category == self.EXISTING:
            return chantry_points.buy_background_dot(self.object, self.background)
        return None
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.forms.mage.test_chantry`.
  - Expected: `OK`. The existing `TestChantryPointForm*` tests still pass: with 20 points the IE, New and Existing categories stay as they were.

- [ ] **Step 5: Commit.**

```bash
git add locations/forms/mage/chantry.py locations/tests/forms/mage/test_chantry.py
git commit -m "ChantryPointForm: offer and accept only allowed, affordable dots

Category and example choices come from the points service, clean()
re-checks the same predicates so forged POSTs fail, and save() spends
through the service. Background choices are limited to
Chantry.allowed_backgrounds instead of every Background.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

### Task 10: [C2.7] `ChantryRemoveForm` (undo one purchase)

**Files:**
- Modify: `locations/forms/mage/chantry.py` (a new class right after `ChantryPointForm`)
- Modify (test): `locations/tests/forms/mage/test_chantry.py` (import, and append `TestChantryRemoveForm`)

**Interfaces:**
- `ChantryRemoveForm(data=None, *, chantry: Chantry)`, with `ACTION = "remove"`.
- Hidden fields: `rating` (a `ModelChoiceField` over `chantry.backgrounds`), `ie` (`BooleanField`) and `effect` (a `ModelChoiceField` over `chantry.integrated_effects`).
- `clean()` requires exactly one of them, and runs `background_removal_error`/`ie_removal_error`. A rating from another chantry is a field error.
- `save()` returns what the service returns (a rating or `None`, the new IE score, or `None`) and may raise `ValidationError` on a race.
- POST contract for C4: `action=remove` plus one of `rating=<pk>`, `ie=on` or `effect=<pk>`.

- [ ] **Step 1: Write the failing tests.**
  - In `locations/tests/forms/mage/test_chantry.py`, add `ChantryRemoveForm,` to the `from locations.forms.mage.chantry import (...)` list, after `ChantryPointForm,`.
  - Append:

```python
class TestChantryRemoveForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        mage_setup()
        cls.allies = Background.objects.get(property_name="allies")
        cls.library = Background.objects.get(property_name="library")

    def setUp(self):
        self.chantry = Chantry.objects.create(name="Undo Chantry", total_points=20)

    def test_removes_a_background_dot(self):
        rating = ChantryBackgroundRating.objects.create(
            bg=self.allies, chantry=self.chantry, rating=2
        )
        form = ChantryRemoveForm({"rating": rating.pk}, chantry=self.chantry)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 1)

    def test_removes_an_ie_dot(self):
        self.chantry.integrated_effects_score = 2
        self.chantry.save()
        form = ChantryRemoveForm({"ie": "on"}, chantry=self.chantry)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.save(), 1)

    def test_removes_an_effect(self):
        effect = Effect.objects.create(name="Chosen", forces=1)
        self.chantry.integrated_effects.add(effect)
        form = ChantryRemoveForm({"effect": effect.pk}, chantry=self.chantry)
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        self.assertFalse(self.chantry.integrated_effects.exists())

    def test_requires_exactly_one_target(self):
        self.assertFalse(ChantryRemoveForm({}, chantry=self.chantry).is_valid())
        rating = ChantryBackgroundRating.objects.create(
            bg=self.allies, chantry=self.chantry, rating=1
        )
        form = ChantryRemoveForm({"rating": rating.pk, "ie": "on"}, chantry=self.chantry)
        self.assertFalse(form.is_valid())

    def test_other_chantrys_rating_is_invalid(self):
        other = Chantry.objects.create(name="Other", total_points=20)
        foreign = ChantryBackgroundRating.objects.create(bg=self.allies, chantry=other, rating=2)
        form = ChantryRemoveForm({"rating": foreign.pk}, chantry=self.chantry)
        self.assertFalse(form.is_valid())

    def test_free_library_floor_is_invalid(self):
        self.chantry.chantry_type = "library"
        self.chantry.save()
        rating = ChantryBackgroundRating.objects.create(
            bg=self.library, chantry=self.chantry, rating=3
        )
        form = ChantryRemoveForm({"rating": rating.pk}, chantry=self.chantry)
        self.assertFalse(form.is_valid())

    def test_ie_overcommit_is_invalid(self):
        self.chantry.integrated_effects_score = 1
        self.chantry.save()
        self.chantry.integrated_effects.add(Effect.objects.create(name="Used", forces=1))
        form = ChantryRemoveForm({"ie": "on"}, chantry=self.chantry)
        self.assertFalse(form.is_valid())
```

- [ ] **Step 2: Run the tests and confirm they fail.**
  - Run `python manage.py test locations.tests.forms.mage.test_chantry`.
  - Expected: `ImportError: cannot import name 'ChantryRemoveForm' from 'locations.forms.mage.chantry'`, and the module errors.

- [ ] **Step 3: Implement the form.** In `locations/forms/mage/chantry.py`, insert this class after `ChantryPointForm` and before `# Form for choosing effects`:

```python
class ChantryRemoveForm(forms.Form):
    """Undo one purchase: a background dot, an Integrated Effects dot or an effect.

    POST ``action=remove`` plus exactly one of ``rating=<ChantryBackgroundRating
    pk>``, ``ie=on`` or ``effect=<Effect pk>``.
    """

    ACTION = "remove"

    rating = forms.ModelChoiceField(
        queryset=ChantryBackgroundRating.objects.none(),
        required=False,
        widget=forms.HiddenInput,
    )
    ie = forms.BooleanField(required=False, widget=forms.HiddenInput)
    effect = forms.ModelChoiceField(
        queryset=Effect.objects.none(), required=False, widget=forms.HiddenInput
    )

    def __init__(self, *args, chantry, **kwargs):
        self.chantry = chantry
        super().__init__(*args, **kwargs)
        self.fields["rating"].queryset = chantry.backgrounds.select_related("bg")
        self.fields["effect"].queryset = chantry.integrated_effects.all()

    def clean(self):
        cleaned_data = super().clean()
        if self.errors:
            return cleaned_data
        chosen = [name for name in ("rating", "ie", "effect") if cleaned_data.get(name)]
        if len(chosen) != 1:
            raise forms.ValidationError("Choose exactly one thing to remove.")
        if chosen == ["rating"]:
            error = chantry_points.background_removal_error(cleaned_data["rating"])
        elif chosen == ["ie"]:
            error = chantry_points.ie_removal_error(self.chantry)
        else:
            error = None
        if error:
            raise forms.ValidationError(error)
        return cleaned_data

    def save(self):
        """Apply the removal through the service; may raise ``ValidationError``."""
        if self.cleaned_data.get("rating"):
            return chantry_points.remove_background_dot(self.cleaned_data["rating"])
        if self.cleaned_data.get("ie"):
            return chantry_points.remove_ie_dot(self.chantry)
        return chantry_points.remove_effect(self.chantry, self.cleaned_data["effect"])
```

- [ ] **Step 4: Run the tests and confirm they pass.**
  - Run `python manage.py test locations.tests.forms.mage.test_chantry`.
  - Expected: `OK` (52 tests).

- [ ] **Step 5: Commit.**

```bash
git add locations/forms/mage/chantry.py locations/tests/forms/mage/test_chantry.py
git commit -m "Add ChantryRemoveForm to undo one chantry purchase

A small form for the wizard's remove action: one background dot, one
Integrated Effects dot or one chosen effect, validated and applied
through the points service.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23"
```

- [ ] **Unit gate:** Run each check below; every one must pass before C2 is done.
  - Run the full suite serially: `python manage.py test > /tmp/c2-full.log 2>&1; tail -3 /tmp/c2-full.log; grep -E "^(FAIL|ERROR):" /tmp/c2-full.log`.
    - Expected: `FAILED (failures=5, ...)`, and those are exactly the 5 baseline failures listed in the C1 gate. Anything else is a regression.
  - `python manage.py check`: no issues.
  - `python manage.py test core.tests.security.test_route_policies`: `OK`. C2 adds no routes.
  - `ruff check locations/services locations/tests/services tg_schema locations/models/mage/chantry.py locations/forms/mage/chantry.py locations/tests/forms/mage/test_chantry.py locations/tests/models/mage/test_chantry_rating_link.py locations/tests/models/mage/test_chantry_library_floor.py`: `All checks passed!`. C2.6 removes the old B007.
  - `black --check locations/services/chantry_points.py locations/tests/services/test_chantry_points.py tg_schema/tests/test_chantry_rating_linked_object.py locations/models/mage/chantry.py locations/forms/mage/chantry.py locations/tests/forms/mage/test_chantry.py locations/tests/models/mage/test_chantry_rating_link.py locations/tests/models/mage/test_chantry_library_floor.py`: unchanged.
    - Pass files, not directories: running black on `locations/tests/models/mage/` reformats unrelated legacy files.
    - `migrations` is excluded from black and ruff by `pyproject.toml`; the migration above is already written in black style.


## Unit C3: Submission and revision hooks

Spec section 3. After this unit, `ApprovalService.transition_object` asks a model what blocks its submission and lets it reset itself when an ST returns it. `Chantry` is the first model to use both hooks, and `{% object_actions %}` shows the reasons in place of the Submit button. Models without the hooks behave exactly as before.

Conventions for every task in this section:
- `PY=/tmp/claude-0/venv/bin/python` and `RUFF=/tmp/claude-0/venv/bin/ruff`. Run tests serially: `$PY manage.py test <label>`.
- Commit messages end with the two trailer lines shown in each commit step.
- Several chantry templates use CRLF line endings (`locgen.html`, `form.html`, `effects_form.html`, `display_includes/integrated_effects.html`, `display_includes/basics.html`). Make partial edits with the Edit tool so the endings are kept. A template this plan replaces in full may be written with LF.

### Task 11: [C3.1] Opt-in hooks in `ApprovalService.transition_object`

**Files:**
- Modify: `core/services/approval.py`
- Create: `core/tests/services/test_approval_hooks.py`

**Interfaces:**
- Produces: inside the existing locked transaction, before a `→ Sub` transition, `transition_object` calls `obj.submission_errors() -> list[str]` when the object defines it and raises `django.core.exceptions.ValidationError("; ".join(errors))` when the list is not empty. Before saving a `→ Rev` transition it calls `obj.on_returned_for_revision() -> list[str]` when defined, and adds the returned field names to `update_fields`.
- Consumes: nothing new. `ObjectSubmissionView` already turns `ValidationError` into a 400.

- [ ] **Step 1: Write the failing test.** Create `core/tests/services/test_approval_hooks.py`:

```python
"""Opt-in submission and revision hooks in ApprovalService.transition_object."""

from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from characters.models.core.human import Human
from core.services import ApprovalService
from game.models import Chronicle
from locations.models.core.location import LocationModel


class TransitionHookTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("hook_owner")
        self.staff = users.objects.create_user("hook_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Hook chronicle")
        self.location = LocationModel.objects.create(
            name="Hooked", owner=self.owner, chronicle=self.chronicle, status="Un"
        )

    def test_submission_errors_block_submit_with_every_reason(self):
        with mock.patch.object(
            LocationModel,
            "submission_errors",
            create=True,
            new=lambda self: ["First problem", "Second problem"],
        ):
            with self.assertRaises(ValidationError) as caught:
                ApprovalService.transition_object("location", self.location.pk, self.owner, "Sub")
        self.assertEqual(caught.exception.messages, ["First problem; Second problem"])
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "Un")

    def test_empty_submission_errors_allow_submit(self):
        with mock.patch.object(
            LocationModel, "submission_errors", create=True, new=lambda self: []
        ):
            obj = ApprovalService.transition_object("location", self.location.pk, self.owner, "Sub")
        self.assertEqual(obj.status, "Sub")
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "Sub")

    def test_return_hook_fields_are_saved(self):
        self.location.status = "Sub"
        self.location.creation_status = 7
        self.location.save()

        def reset(obj):
            obj.creation_status = 1
            return ["creation_status"]

        with mock.patch.object(LocationModel, "on_returned_for_revision", create=True, new=reset):
            ApprovalService.transition_object("location", self.location.pk, self.staff, "Rev")
        self.location.refresh_from_db()
        self.assertEqual(self.location.status, "Rev")
        self.assertEqual(self.location.creation_status, 1)

    def test_submit_does_not_call_return_hook(self):
        called = []
        with mock.patch.object(
            LocationModel,
            "on_returned_for_revision",
            create=True,
            new=lambda self: called.append(True) or [],
        ):
            ApprovalService.transition_object("location", self.location.pk, self.owner, "Sub")
        self.assertEqual(called, [])

    def test_models_without_hooks_are_unaffected(self):
        self.assertFalse(hasattr(Human, "submission_errors"))
        self.assertFalse(hasattr(Human, "on_returned_for_revision"))
        character = Human.objects.create(
            name="Plain", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        ApprovalService.transition_object("character", character.pk, self.owner, "Sub")
        character.refresh_from_db()
        self.assertEqual(character.status, "Sub")
        ApprovalService.transition_object("character", character.pk, self.staff, "Rev")
        character.refresh_from_db()
        self.assertEqual(character.status, "Rev")
        self.assertFalse(hasattr(LocationModel, "submission_errors"))
        location_obj = ApprovalService.transition_object(
            "location", self.location.pk, self.owner, "Sub"
        )
        self.assertEqual(location_obj.status, "Sub")
```

- [ ] **Step 2: Run it and watch it fail.** `$PY manage.py test core.tests.services.test_approval_hooks`. Expected: `FAILED (failures=2)`, namely `test_submission_errors_block_submit_with_every_reason` (`ValidationError not raised`) and `test_return_hook_fields_are_saved` (`7 != 1`).

- [ ] **Step 3: Implement.** In `core/services/approval.py`, replace the body of the `with transaction.atomic():` block in `transition_object`.

Before:
```python
                if not PermissionManager.user_has_permission(
                    user, obj, Permission.EDIT_FULL
                ):
                    raise PermissionDenied("Cannot submit this object")
            else:
                if obj.status != "Sub":
                    raise ValidationError("Only submitted objects can be returned")
                if not PermissionManager.user_has_permission(
                    user, obj, Permission.APPROVE
                ):
                    raise PermissionDenied("Matching chronicle ST required")
            obj.status = target_status
            obj.save(update_fields=["status"])
            return obj
```
After:
```python
                if not PermissionManager.user_has_permission(
                    user, obj, Permission.EDIT_FULL
                ):
                    raise PermissionDenied("Cannot submit this object")
                # Opt-in hook: a model lists what still blocks submission.
                submission_errors = getattr(obj, "submission_errors", None)
                if submission_errors is not None:
                    errors = submission_errors()
                    if errors:
                        raise ValidationError("; ".join(errors))
            else:
                if obj.status != "Sub":
                    raise ValidationError("Only submitted objects can be returned")
                if not PermissionManager.user_has_permission(
                    user, obj, Permission.APPROVE
                ):
                    raise PermissionDenied("Matching chronicle ST required")
            update_fields = ["status"]
            if target_status == "Rev":
                # Opt-in hook: a model resets its own state and names the fields.
                on_returned = getattr(obj, "on_returned_for_revision", None)
                if on_returned is not None:
                    update_fields.extend(on_returned())
            obj.status = target_status
            obj.save(update_fields=update_fields)
            return obj
```
Then fix the pre-existing import-order warning in the same file: `$RUFF check --fix --select I001 core/services/approval.py` (it moves the `Chimera` import above `Character`; nothing else changes).

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test core.tests.services.test_approval_hooks core.tests.services.test_approval core.tests.security.test_object_workflow`. Expected: `OK` (24 tests).

- [ ] **Step 5: Commit.**
```bash
git add core/services/approval.py core/tests/services/test_approval_hooks.py
git commit -F - <<'EOF'
ApprovalService: opt-in submission_errors and on_returned_for_revision hooks

Before a submit, a model that defines submission_errors() can refuse it
with its reasons. Before a return for revision, on_returned_for_revision()
may reset state and name extra fields to save. Models without the hooks
are unchanged.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 12: [C3.2] `Chantry.submission_errors` and `Chantry.on_returned_for_revision`

**Files:**
- Modify: `locations/services/chantry_points.py` (created by C2; append two functions)
- Modify: `locations/models/mage/chantry.py`
- Create: `locations/tests/models/mage/test_chantry_submission.py`
- Create: `core/tests/services/test_chantry_approval.py`

**Interfaces:**
- Consumes (C2): `locations.services.chantry_points.has_affordable_purchase(chantry) -> bool`.
- Produces: `affordable_effects(chantry) -> QuerySet[Effect]` (effects not yet integrated, `0 < rote_cost <= current_ie_points()`, `max_sphere <= rank`), `has_affordable_effect(chantry) -> bool`, `Chantry.WIZARD_RESOURCES = ("node", "library", "allies", "sanctum")`, `Chantry.FINAL_WIZARD_STEP = 6`, `Chantry.submission_errors() -> list[str]`, `Chantry.on_returned_for_revision() -> list[str]` (sets `creation_status = 1`, returns `["creation_status"]`). C4 uses `affordable_effects`, `has_affordable_effect` and `WIZARD_RESOURCES`.

- [ ] **Step 1: Write the failing tests.** Create `locations/tests/models/mage/test_chantry_submission.py`:

```python
"""Chantry.submission_errors and Chantry.on_returned_for_revision."""

from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.services.chantry_points import affordable_effects, has_affordable_effect


def finished_chantry(**overrides):
    """A chantry that passes every submission check: 2 points, all spent on Allies."""
    fields = {"name": "Finished", "total_points": 2, "creation_status": 7, "status": "Un"}
    fields.update(overrides)
    chantry = Chantry.objects.create(**fields)
    allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
    ChantryBackgroundRating.objects.create(chantry=chantry, bg=allies, rating=1, complete=True)
    return chantry


class AffordableEffectTests(TestCase):
    def setUp(self):
        self.chantry = Chantry.objects.create(
            name="Effects", total_points=30, integrated_effects_score=1
        )  # rank 3, 4 IE points
        self.cheap = Effect.objects.create(name="Cheap", forces=2)
        self.too_costly = Effect.objects.create(name="Costly", forces=3, prime=2)
        self.too_high = Effect.objects.create(name="High", forces=4)
        self.empty = Effect.objects.create(name="Empty")

    def test_only_affordable_unowned_effects_within_rank(self):
        self.assertEqual(list(affordable_effects(self.chantry)), [self.cheap])
        self.assertTrue(has_affordable_effect(self.chantry))

    def test_owned_effects_are_not_offered(self):
        self.chantry.integrated_effects.add(self.cheap)
        self.assertFalse(has_affordable_effect(self.chantry))


class SubmissionErrorsTests(TestCase):
    def test_finished_chantry_has_no_errors(self):
        self.assertEqual(finished_chantry().submission_errors(), [])

    def test_unfinished_wizard(self):
        chantry = finished_chantry(creation_status=6)
        self.assertEqual(
            chantry.submission_errors(),
            ["Finish every creation step (the chantry is on step 6 of 6)."],
        )

    def test_overspent_points(self):
        chantry = finished_chantry(total_points=1)
        self.assertIn("1 more point spent than the chantry has.", chantry.submission_errors())

    def test_affordable_purchase_left(self):
        chantry = finished_chantry(total_points=4)
        self.assertIn(
            "2 unspent points can still buy a background or Integrated Effects dot.",
            chantry.submission_errors(),
        )

    def test_integrated_effects_overcommitted(self):
        chantry = finished_chantry()
        chantry.integrated_effects.add(Effect.objects.create(name="Bolt", forces=1))
        self.assertIn(
            "Integrated effects cost 1 more point than the Integrated Effects score allows.",
            chantry.submission_errors(),
        )

    def test_affordable_effect_left(self):
        chantry = finished_chantry(total_points=4, integrated_effects_score=1)
        Effect.objects.create(name="Bolt", forces=1)
        self.assertIn(
            "4 Integrated Effects points can still buy an effect.",
            chantry.submission_errors(),
        )

    def test_background_not_allowed(self):
        chantry = finished_chantry(total_points=1002)
        avatar = Background.objects.get_or_create(name="Avatar", property_name="avatar")[0]
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=avatar, rating=1)
        self.assertIn("Avatar is not a chantry background.", chantry.submission_errors())

    def test_rating_out_of_range(self):
        chantry = finished_chantry(total_points=12)
        chantry.backgrounds.update(rating=6)
        self.assertIn("Allies must be rated 1 to 5.", chantry.submission_errors())

    def test_incomplete_resource(self):
        chantry = finished_chantry()
        chantry.backgrounds.update(complete=False)
        self.assertIn("Allies has not been set up yet.", chantry.submission_errors())

    def test_incomplete_non_resource_background_is_fine(self):
        chantry = finished_chantry(total_points=4)
        cult = Background.objects.get_or_create(name="Cult", property_name="cult")[0]
        ChantryBackgroundRating.objects.create(chantry=chantry, bg=cult, rating=1)
        self.assertEqual(chantry.submission_errors(), [])


class ReturnedForRevisionTests(TestCase):
    def test_resets_to_first_step_and_names_the_field(self):
        chantry = finished_chantry(status="Sub")
        self.assertEqual(chantry.on_returned_for_revision(), ["creation_status"])
        self.assertEqual(chantry.creation_status, 1)
```

Create `core/tests/services/test_chantry_approval.py`:

```python
"""Chantry submission and revision through the approval endpoints."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from characters.models.core.background_block import Background
from game.models import Chronicle, Gameline, STRelationship
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating


class ChantrySubmissionFlowTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("flow_owner")
        self.st = users.objects.create_user("flow_st")
        self.chronicle = Chronicle.objects.create(name="Flow chronicle")
        mage = Gameline.objects.get_or_create(name="Mage: the Ascension")[0]
        STRelationship.objects.create(user=self.st, chronicle=self.chronicle, gameline=mage)
        self.chantry = Chantry.objects.create(
            name="Flow",
            owner=self.owner,
            chronicle=self.chronicle,
            total_points=2,
            creation_status=2,
        )
        allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
        self.allies = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=allies, rating=1, complete=False
        )
        self.submit = reverse("accounts:object_submission", args=["location", self.chantry.pk])
        self.revise = reverse("accounts:object_revision", args=["location", self.chantry.pk])

    def test_submit_refused_with_reasons(self):
        self.client.force_login(self.owner)
        response = self.client.post(self.submit)
        self.assertContains(
            response,
            "Finish every creation step (the chantry is on step 2 of 6).; "
            "Allies has not been set up yet.",
            status_code=400,
        )
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Un")

    def test_valid_chantry_submits_and_return_resets_the_wizard(self):
        self.allies.complete = True
        self.allies.save()
        self.chantry.creation_status = 7
        self.chantry.save()

        self.client.force_login(self.owner)
        self.assertEqual(self.client.post(self.submit).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Sub")

        self.client.force_login(self.st)
        self.assertEqual(self.client.post(self.revise).status_code, 302)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.status, "Rev")
        self.assertEqual(self.chantry.creation_status, 1)
        self.assertEqual(self.chantry.backgrounds.get().rating, 1)
```

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.models.mage.test_chantry_submission core.tests.services.test_chantry_approval`. Expected: `ImportError: cannot import name 'affordable_effects' from 'locations.services.chantry_points'` for the first module, and in the second `test_submit_refused_with_reasons` fails (`302 != 400`) and `test_valid_chantry_submits_and_return_resets_the_wizard` fails (`7 != 1`).

- [ ] **Step 3: Implement.** Append to `locations/services/chantry_points.py`:

```python
def affordable_effects(chantry):
    """Effects the chantry can still integrate: within its rank and its remaining IE points."""
    from characters.models.mage.effect import Effect

    return Effect.objects.filter(
        rote_cost__gt=0,
        rote_cost__lte=chantry.current_ie_points(),
        max_sphere__lte=chantry.rank,
    ).exclude(pk__in=chantry.integrated_effects.values("pk"))


def has_affordable_effect(chantry):
    return affordable_effects(chantry).exists()
```

In `locations/models/mage/chantry.py`, insert immediately above `    def get_independent_members(self):`:

```python
    # Ratings for these backgrounds are finished by creating an object in wizard steps 3-6.
    WIZARD_RESOURCES = ("node", "library", "allies", "sanctum")
    FINAL_WIZARD_STEP = 6

    def submission_errors(self):
        """Reasons this chantry cannot be submitted yet; empty when it can."""
        from locations.services.chantry_points import (
            has_affordable_effect,
            has_affordable_purchase,
        )

        def plural(count, word):
            return f"{count} {word}{'' if count == 1 else 's'}"

        errors = []
        if self.creation_status <= self.FINAL_WIZARD_STEP:
            errors.append(
                f"Finish every creation step (the chantry is on step "
                f"{self.creation_status} of {self.FINAL_WIZARD_STEP})."
            )
        if self.points < 0:
            errors.append(f"{plural(-self.points, 'more point')} spent than the chantry has.")
        if has_affordable_purchase(self):
            errors.append(
                f"{plural(self.points, 'unspent point')} can still buy a background "
                "or Integrated Effects dot."
            )
        ie_points = self.current_ie_points()
        if ie_points < 0:
            errors.append(
                f"Integrated effects cost {plural(-ie_points, 'more point')} than the "
                "Integrated Effects score allows."
            )
        if has_affordable_effect(self):
            errors.append(
                f"{plural(ie_points, 'Integrated Effects point')} can still buy an effect."
            )
        for rating in self.backgrounds.select_related("bg"):
            name = rating.bg.name if rating.bg else "A deleted background"
            if rating.bg is None or rating.bg.property_name not in self.allowed_backgrounds:
                errors.append(f"{name} is not a chantry background.")
            elif not 1 <= rating.rating <= 5:
                errors.append(f"{name} must be rated 1 to 5.")
            if (
                rating.bg is not None
                and rating.bg.property_name in self.WIZARD_RESOURCES
                and not rating.complete
            ):
                errors.append(f"{name} has not been set up yet.")
        return errors

    def on_returned_for_revision(self):
        """ApprovalService hook: a returned chantry re-enters the wizard at step 1."""
        self.creation_status = 1
        return ["creation_status"]

```
The service import stays inside the method so the model module never imports the service at load time.

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.models.mage.test_chantry_submission core.tests.services.test_chantry_approval core.tests.services.test_approval_hooks`. Expected: `OK` (20 tests).

- [ ] **Step 5: Commit.**
```bash
git add locations/services/chantry_points.py locations/models/mage/chantry.py \
  locations/tests/models/mage/test_chantry_submission.py core/tests/services/test_chantry_approval.py
git commit -F - <<'EOF'
Chantry: list submission blockers; reset the wizard when returned

submission_errors() refuses a chantry whose wizard is unfinished, whose
points or Integrated Effects are overspent or still spendable, or whose
backgrounds are invalid or unlinked. on_returned_for_revision() sends it
back to step 1 with every purchase kept.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 13: [C3.3] `{% object_actions %}` hides Submit and lists the reasons

**Files:**
- Modify: `core/templatetags/object_actions.py`
- Modify: `core/templates/core/object_actions.html`
- Create: `core/tests/templatetags/test_object_actions.py`

**Interfaces:**
- Consumes: `obj.submission_errors()` (optional, from C3.2).
- Produces: tag context key `submission_errors: list[str]`; `can_submit` is false while that list is non-empty. Reasons are shown only to a user who could otherwise submit.

- [ ] **Step 1: Write the failing test.** Create `core/tests/templatetags/test_object_actions.py`:

```python
"""The object_actions tag hides Submit while a model reports submission errors."""

from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from characters.models.core.human import Human
from game.models import Chronicle
from locations.models.mage.chantry import Chantry


def render_actions(obj, user):
    request = RequestFactory().get("/")
    request.user = user
    template = Template("{% load object_actions %}{% object_actions %}")
    return template.render(Context({"object": obj, "request": request}))


class ObjectActionsTagTests(TestCase):
    def setUp(self):
        self.owner = get_user_model().objects.create_user("actions_owner")
        self.chronicle = Chronicle.objects.create(name="Actions chronicle")

    def test_unfinished_chantry_lists_reasons_instead_of_submit(self):
        chantry = Chantry.objects.create(
            name="Draft", owner=self.owner, chronicle=self.chronicle, creation_status=3
        )
        html = render_actions(chantry, self.owner)
        self.assertNotIn("Submit for approval", html)
        self.assertIn("Finish creation first", html)
        self.assertIn("Finish every creation step (the chantry is on step 3 of 6).", html)

    def test_finished_chantry_shows_submit(self):
        chantry = Chantry.objects.create(
            name="Done",
            owner=self.owner,
            chronicle=self.chronicle,
            creation_status=7,
            total_points=0,
        )
        html = render_actions(chantry, self.owner)
        self.assertIn("Submit for approval", html)
        self.assertNotIn("Finish creation first", html)

    def test_model_without_hook_shows_submit(self):
        character = Human.objects.create(
            name="Plain", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        html = render_actions(character, self.owner)
        self.assertIn("Submit for approval", html)
        self.assertNotIn("Finish creation first", html)

    def test_reasons_hidden_from_viewers_who_cannot_submit(self):
        chantry = Chantry.objects.create(
            name="Draft", owner=self.owner, chronicle=self.chronicle, creation_status=3
        )
        stranger = get_user_model().objects.create_user("actions_stranger")
        self.assertNotIn("Finish creation first", render_actions(chantry, stranger))
```

- [ ] **Step 2: Run it and watch it fail.** `$PY manage.py test core.tests.templatetags.test_object_actions`. Expected: `FAILED (failures=1)`: `test_unfinished_chantry_lists_reasons_instead_of_submit` (`'Submit for approval' unexpectedly found`).

- [ ] **Step 3: Implement.** In `core/templatetags/object_actions.py`:

Before:
```python
    can_edit = PermissionManager.user_has_permission(user, obj, Permission.EDIT_FULL)
    can_approve = PermissionManager.user_has_permission(user, obj, Permission.APPROVE)
    return {
        "object_type": object_type,
        "object_pk": obj.pk,
        "can_submit": can_edit and obj.status in {"Un", "Rev"},
        "can_review": can_approve and obj.status == "Sub",
    }
```
After:
```python
    can_edit = PermissionManager.user_has_permission(user, obj, Permission.EDIT_FULL)
    can_approve = PermissionManager.user_has_permission(user, obj, Permission.APPROVE)
    can_submit = can_edit and obj.status in {"Un", "Rev"}
    # Models may opt in to listing what blocks submission (see ApprovalService).
    submission_errors = []
    if can_submit and hasattr(obj, "submission_errors"):
        submission_errors = obj.submission_errors()
    return {
        "object_type": object_type,
        "object_pk": obj.pk,
        "can_submit": can_submit and not submission_errors,
        "submission_errors": submission_errors,
        "can_review": can_approve and obj.status == "Sub",
    }
```
Run `$RUFF check --fix --select I001 core/templatetags/object_actions.py` (pre-existing import order: moves the `Chimera` import up).

Replace `core/templates/core/object_actions.html` with:
```django
{% if can_submit or can_review or submission_errors %}
<section class="container mb-4" aria-label="Approval actions">
  {% if can_submit %}
  <form method="post" action="{% url 'accounts:object_submission' object_type object_pk %}">
    {% csrf_token %}<button type="submit" class="btn btn-primary">Submit for approval</button>
  </form>
  {% endif %}
  {% if submission_errors %}
  <div class="tg-card">
    <div class="tg-card-body">
      <h2 class="h5">Finish creation first</h2>
      <ul class="mb-0">
        {% for error in submission_errors %}<li>{{ error }}</li>{% endfor %}
      </ul>
    </div>
  </div>
  {% endif %}
  {% if can_review %}
  <form method="post" action="{% url 'accounts:object_revision' object_type object_pk %}">
    {% csrf_token %}<button type="submit" class="btn btn-secondary">Return for revisions</button>
  </form>
  <form method="post" action="{% url 'accounts:object_approval' object_type object_pk %}">
    {% csrf_token %}<button type="submit" class="btn btn-success">Approve</button>
  </form>
  {% endif %}
</section>
{% endif %}
```

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test core.tests.templatetags.test_object_actions core.tests.services`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add core/templatetags/object_actions.py core/templates/core/object_actions.html \
  core/tests/templatetags/test_object_actions.py
git commit -F - <<'EOF'
object_actions: show "Finish creation first" instead of Submit

When the object reports submission errors, the Submit button is hidden
and the reasons are listed for the user who would submit it.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:** run each and require the stated result.
  1. `$PY manage.py test` (serially, about 40 minutes): 0 failures, 0 errors.
  2. `$PY manage.py check`: `System check identified no issues`.
  3. `$PY manage.py test core.tests.security.test_route_policies`: `OK`.
  4. `$RUFF check core/services/approval.py core/templatetags/object_actions.py locations/models/mage/chantry.py locations/services/chantry_points.py core/tests/services/test_approval_hooks.py core/tests/services/test_chantry_approval.py core/tests/templatetags/test_object_actions.py locations/tests/models/mage/test_chantry_submission.py`: `All checks passed!`; and `$RUFF format --check` on the four new test files: already formatted.

## Unit C4: Go live (routes, access, wizard steps, detail page)

Spec sections 1, 2 (step changes) and 5. After this unit, "Create Chantry" opens the wizard, a chantry's URL routes its editor through steps 1 to 6 while it is `Un` or `Rev`, the direct create and edit forms are limited to scoped Mage STs and staff, the edit form keeps every field, and the detail page shows the faction term, the points and a Resources card.

Tasks C4.4 to C4.8 extend `locations/templates/locations/mage/chantry/locgen.html` and `locations/views/mage/chantry.py` step by step. The before snippets are quoted from `1e77e23`. If C2 changed the same lines, apply the same change to C2's version.

### Task 14: [C4.1] `OBJECT_ST_WRITE` route policy

**Files:**
- Modify: `core/access_policy.py`
- Modify: `scripts/inventory_authorization_routes.py`
- Create: `core/tests/security/test_object_st_write.py`

**Interfaces:**
- Produces: manifest policy name `"OBJECT_ST_WRITE"`. It runs every `OBJECT_WRITE` check (edit permission and the ownership/approval field guard) and first requires `PermissionManager.user_has_scoped_editor_role(request.user, obj, request=request)` (staff, head ST, or the ST of the object's chronicle and gameline). Refusal is `PermissionDenied` (403).

- [ ] **Step 1: Write the failing test.** Create `core/tests/security/test_object_st_write.py`:

```python
"""OBJECT_ST_WRITE: the OBJECT_WRITE checks plus a scoped storyteller role."""

from unittest import mock

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, TestCase

from core.access_policy import authorize_route, route_name
from core.route_policy_manifest import VIEW_POLICIES
from game.models import Chronicle, Gameline, STRelationship
from locations.models.mage.chantry import Chantry


class _STWriteProbeView:
    """Stands in for a routed view declared OBJECT_ST_WRITE."""

    model = Chantry
    fields = ["name", "total_points"]


class ObjectSTWritePolicyTests(TestCase):
    def setUp(self):
        users = get_user_model()
        self.owner = users.objects.create_user("stw_owner")
        self.mage_st = users.objects.create_user("stw_mage_st")
        self.vampire_st = users.objects.create_user("stw_vampire_st")
        self.other_st = users.objects.create_user("stw_other_st")
        self.staff = users.objects.create_user("stw_staff", is_staff=True)
        self.chronicle = Chronicle.objects.create(name="Home")
        other = Chronicle.objects.create(name="Away")
        mage = Gameline.objects.get_or_create(name="Mage: the Ascension")[0]
        vampire = Gameline.objects.get_or_create(name="Vampire: the Masquerade")[0]
        STRelationship.objects.create(user=self.mage_st, chronicle=self.chronicle, gameline=mage)
        STRelationship.objects.create(
            user=self.vampire_st, chronicle=self.chronicle, gameline=vampire
        )
        STRelationship.objects.create(user=self.other_st, chronicle=other, gameline=mage)
        self.chantry = Chantry.objects.create(
            name="Probe", owner=self.owner, chronicle=self.chronicle, status="Un"
        )
        patcher = mock.patch.dict(VIEW_POLICIES, {route_name(_STWriteProbeView): "OBJECT_ST_WRITE"})
        patcher.start()
        self.addCleanup(patcher.stop)

    def authorize(self, user, method="get", data=None):
        request = getattr(RequestFactory(), method)("/", data or {})
        request.user = user
        return authorize_route(request, _STWriteProbeView, kwargs={"pk": self.chantry.pk})

    def test_scoped_st_and_staff_pass(self):
        for user in (self.mage_st, self.staff):
            with self.subTest(user=user.username):
                self.assertIsNone(self.authorize(user))
                self.assertIsNone(self.authorize(user, "post", {"name": "Renamed"}))

    def test_owner_of_a_draft_is_refused(self):
        with self.assertRaises(PermissionDenied):
            self.authorize(self.owner)
        with self.assertRaises(PermissionDenied):
            self.authorize(self.owner, "post", {"total_points": "99"})

    def test_wrong_gameline_and_wrong_chronicle_sts_are_refused(self):
        for user in (self.vampire_st, self.other_st):
            with self.subTest(user=user.username):
                with self.assertRaises(PermissionDenied):
                    self.authorize(user)

    def test_object_write_field_guard_still_applies(self):
        with self.assertRaises(PermissionDenied):
            self.authorize(self.mage_st, "post", {"name": "Probe", "status": "App"})
```

- [ ] **Step 2: Run it and watch it fail.** `$PY manage.py test core.tests.security.test_object_st_write`. Expected: `FAILED (errors=2)`: both subtests of `test_scoped_st_and_staff_pass` raise `PermissionDenied: Unknown access policy`.

- [ ] **Step 3: Implement.** In `core/access_policy.py`:

Before:
```python
    if policy in {"OBJECT_WRITE", "OBJECT_ACTION"}:
        if (
```
After:
```python
    if policy in {"OBJECT_WRITE", "OBJECT_ACTION", "OBJECT_ST_WRITE"}:
        if policy == "OBJECT_ST_WRITE" and not PermissionManager.user_has_scoped_editor_role(
            request.user, obj, request=request
        ):
            raise PermissionDenied("A storyteller for this chronicle is required")
        if (
```
Before:
```python
            if policy == "OBJECT_WRITE":
                form_class = getattr(view, "form_class", None)
```
After:
```python
            if policy in {"OBJECT_WRITE", "OBJECT_ST_WRITE"}:
                form_class = getattr(view, "form_class", None)
```
In `scripts/inventory_authorization_routes.py`, `main()`, `effective_login`: add `"OBJECT_ST_WRITE",` between `"OBJECT_CREATE",` and `"OBJECT_WRITE",` in the first set.

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test core.tests.security`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add core/access_policy.py scripts/inventory_authorization_routes.py core/tests/security/test_object_st_write.py
git commit -F - <<'EOF'
access_policy: add OBJECT_ST_WRITE (OBJECT_WRITE plus scoped ST role)

For player-owned objects whose edit form holds ST-only fields: the
owner of a draft has EDIT_FULL but must not use such a form.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 15: [C4.2] ST-only direct edit form that keeps every field

**Files:**
- Modify: `locations/views/mage/chantry.py`
- Replace: `locations/templates/locations/mage/chantry/form.html`
- Create: `locations/templates/locations/mage/chantry/field_row.html`
- Modify: `core/route_policy_manifest.py`
- Modify: `scripts/build_route_policy_manifest.py`
- Create: `locations/tests/views/mage/chantry_fixtures.py`
- Create: `locations/tests/views/mage/test_chantry_update.py`

**Interfaces:**
- Consumes (C2): `apply_type_grants(chantry) -> None`.
- Produces: `locations.views.mage.chantry.DIRECT_FORM_FIELDS`, the 20 fields the direct form edits and `form.html` renders: `name, contained_within, gauntlet, shroud, dimension_barrier, description, faction, leadership_type, season, chantry_type, total_points, integrated_effects, leaders, members, cabals, ambassador, node_tender, investigator, guardian, teacher`. The parent template renders the first six; `form.html` renders the rest, plus `chronicle` when the form has it (direct create, C4.3). The update form calls `apply_type_grants` when `chantry_type` changes. Test helpers `add_chantry_actors(testcase)` and `submitted_values(response)` for the later C4 tasks.
- This rewrite deletes the never-rendered `{% block prominents %}` from `form.html` (a C5 Evidence-table row).

- [ ] **Step 1: Write the failing tests.** Create `locations/tests/views/mage/chantry_fixtures.py` (a helper module, not collected as tests):

```python
"""Users, chronicles and form helpers shared by the chantry view tests."""

from html.parser import HTMLParser

from django.contrib.auth import get_user_model

from game.models import Chronicle, Gameline, STRelationship


def add_chantry_actors(testcase):
    """Attach player, st (Mage ST of chronicle), vampire_st, other_st, staff to testcase."""
    users = get_user_model()
    testcase.player = users.objects.create_user("chantry_player")
    testcase.st = users.objects.create_user("chantry_st")
    testcase.vampire_st = users.objects.create_user("chantry_vampire_st")
    testcase.other_st = users.objects.create_user("chantry_other_st")
    testcase.staff = users.objects.create_user("chantry_staff", is_staff=True)
    testcase.chronicle = Chronicle.objects.create(name="Chantry chronicle")
    testcase.other_chronicle = Chronicle.objects.create(name="Other chronicle")
    mage = Gameline.objects.get_or_create(name="Mage: the Ascension")[0]
    vampire = Gameline.objects.get_or_create(name="Vampire: the Masquerade")[0]
    STRelationship.objects.create(user=testcase.st, chronicle=testcase.chronicle, gameline=mage)
    STRelationship.objects.create(
        user=testcase.vampire_st, chronicle=testcase.chronicle, gameline=vampire
    )
    STRelationship.objects.create(
        user=testcase.other_st, chronicle=testcase.other_chronicle, gameline=mage
    )


class FormValues(HTMLParser):
    """Collect what a browser would submit for every control in a rendered page."""

    def __init__(self):
        super().__init__()
        self.data = {}
        self._select = None
        self._select_multiple = False
        self._first_option = None
        self._textarea = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        name = attrs.get("name")
        if tag == "input" and name and name != "csrfmiddlewaretoken":
            kind = attrs.get("type", "text")
            if kind in {"submit", "button", "reset"}:
                return
            if kind in {"checkbox", "radio"} and "checked" not in attrs:
                return
            self.data.setdefault(name, []).append(attrs.get("value", "on"))
        elif tag == "select" and name:
            self._select = name
            self._select_multiple = "multiple" in attrs
            self._first_option = None
            self.data.setdefault(name, [])
        elif tag == "option" and self._select:
            value = attrs.get("value", "")
            if self._first_option is None:
                self._first_option = value
            if "selected" in attrs:
                self.data[self._select].append(value)
        elif tag == "textarea" and name:
            self._textarea = name
            self.data[name] = [""]

    def handle_endtag(self, tag):
        if tag == "select" and self._select:
            chosen = self.data[self._select]
            if not chosen and not self._select_multiple and self._first_option is not None:
                chosen.append(self._first_option)
            self._select = None
        elif tag == "textarea":
            self._textarea = None

    def handle_data(self, data):
        if self._textarea:
            self.data[self._textarea][0] += data


def submitted_values(response):
    parser = FormValues()
    parser.feed(response.content.decode())
    return parser.data
```

Create `locations/tests/views/mage/test_chantry_update.py`:

```python
"""The direct chantry edit form: scoped-ST access and a lossless round trip."""

from django.forms.models import model_to_dict
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.models.mage.cabal import Cabal
from characters.models.mage.effect import Effect
from characters.models.mage.faction import MageFaction
from locations.models.core.location import LocationModel
from locations.models.mage.chantry import Chantry
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors, submitted_values
from locations.views.mage.chantry import ChantryUpdateView


class ChantryUpdateAccessTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Guarded",
            owner=self.player,
            chronicle=self.chronicle,
            status="Un",
            total_points=10,
        )
        self.url = self.chantry.get_update_url()

    def test_owner_of_a_draft_is_refused(self):
        self.client.force_login(self.player)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        response = self.client.post(self.url, {"name": "Guarded", "total_points": 99})
        self.assertEqual(response.status_code, 403)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.total_points, 10)

    def test_wrong_chronicle_and_wrong_gameline_sts_are_refused(self):
        for user in (self.other_st, self.vampire_st):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_scoped_st_and_staff_get_the_form(self):
        for user in (self.st, self.staff):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertEqual(self.client.get(self.url).status_code, 200)

    def test_changing_type_to_library_grants_library_dots(self):
        Background.objects.get_or_create(name="Library", property_name="library")
        self.client.force_login(self.st)
        data = submitted_values(self.client.get(self.url))
        data["chantry_type"] = ["library"]
        self.assertEqual(self.client.post(self.url, data).status_code, 302)
        self.assertEqual(self.chantry.backgrounds.get(bg__property_name="library").rating, 3)


class ChantryUpdateRoundTripTests(TestCase):
    """Regression: fields missing from form.html used to be blanked on save."""

    def setUp(self):
        add_chantry_actors(self)
        people = [Human.objects.create(name=f"Person {i}") for i in range(8)]
        self.chantry = Chantry.objects.create(
            name="Full",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            description="Old stones",
            faction=MageFaction.objects.create(name="Order of Hermes"),
            leadership_type="democracy",
            season="spring",
            chantry_type="war",
            total_points=25,
            gauntlet=4,
            shroud=5,
            dimension_barrier=3,
            ambassador=people[0],
            node_tender=people[1],
        )
        self.chantry.contained_within.add(LocationModel.objects.create(name="City"))
        self.chantry.integrated_effects.add(Effect.objects.create(name="Ward", prime=1))
        self.chantry.leaders.add(people[2])
        self.chantry.members.add(people[3], people[4])
        self.chantry.cabals.add(Cabal.objects.create(name="Cabal"))
        self.chantry.investigator.add(people[5])
        self.chantry.guardian.add(people[6])
        self.chantry.teacher.add(people[7])
        self.url = self.chantry.get_update_url()

    def snapshot(self):
        chantry = Chantry.objects.get(pk=self.chantry.pk)
        values = model_to_dict(chantry, fields=ChantryUpdateView.fields)
        return {
            name: sorted(x.pk for x in value) if isinstance(value, list) else value
            for name, value in values.items()
        }

    def test_every_field_is_rendered_and_nothing_else(self):
        self.client.force_login(self.st)
        rendered = set(submitted_values(self.client.get(self.url)))
        self.assertEqual(rendered, set(ChantryUpdateView.fields))
        for name in ("gauntlet", "shroud", "dimension_barrier"):
            self.assertIn(name, ChantryUpdateView.fields)

    def test_saving_the_unchanged_form_keeps_every_field(self):
        before = self.snapshot()
        self.client.force_login(self.st)
        data = submitted_values(self.client.get(self.url))
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.snapshot(), before)
```

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_update`. Expected: `FAILED (failures=3, errors=1)`: `test_owner_of_a_draft_is_refused` (`200 != 403`), `test_every_field_is_rendered_and_nothing_else` (set mismatch), `test_saving_the_unchanged_form_keeps_every_field` (faction, leadership_type, season and the personnel fields are blanked), and an error in `test_changing_type_to_library_grants_library_dots` (`ChantryBackgroundRating.DoesNotExist`).

- [ ] **Step 3: Implement.**

(a) `locations/views/mage/chantry.py`. Insert immediately above `class ChantryDetailView(`:
```python
# Every field of the direct (ST) forms; chantry/form.html renders exactly these.
DIRECT_FORM_FIELDS = [
    "name",
    "contained_within",
    "gauntlet",
    "shroud",
    "dimension_barrier",
    "description",
    "faction",
    "leadership_type",
    "season",
    "chantry_type",
    "total_points",
    "integrated_effects",
    "leaders",
    "members",
    "cabals",
    "ambassador",
    "node_tender",
    "investigator",
    "guardian",
    "teacher",
]


```
In `ChantryCreateView`, replace the whole `fields = [ ... ]` list (17 names, `"name"` to `"teacher"`) with `fields = DIRECT_FORM_FIELDS`. Replace `ChantryUpdateView` entirely with:
```python
class ChantryUpdateView(EditPermissionMixin, MessageMixin, UpdateView):
    """Direct edit form; the route policy (OBJECT_ST_WRITE) limits it to scoped STs and staff."""

    model = Chantry
    fields = DIRECT_FORM_FIELDS
    template_name = "locations/mage/chantry/form.html"
    success_message = "Chantry '{name}' updated successfully!"
    error_message = "Failed to update chantry. Please correct the errors below."

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        if "chantry_type" in form.changed_data:
            apply_type_grants(self.object)
        return response
```
Add to the imports (merge with an existing import from the same module if C2 added one):
```python
from locations.services.chantry_points import apply_type_grants
```

(b) Create `locations/templates/locations/mage/chantry/field_row.html`:
```django
<div class="row mb-2">
    <div class="col-sm-4">
        <label for="{{ field.id_for_label }}">{{ field.label }}</label>
    </div>
    <div class="col-sm-8">
        {{ field }}
        {% for error in field.errors %}<div class="tg-error-message">{{ error }}</div>{% endfor %}
    </div>
</div>
```

(c) Replace `locations/templates/locations/mage/chantry/form.html` entirely:
```django
{% extends "locations/core/location/form.html" %}
{% comment %}
    Renders every field of DIRECT_FORM_FIELDS (locations/views/mage/chantry.py).
    The parent renders name, contained_within, gauntlet, shroud,
    dimension_barrier and description; this template renders the rest.
    A field missing here is blanked on save.
{% endcomment %}
{% block creation_title %}
    Create Chantry
{% endblock creation_title %}
{% block other %}
    {% if form.chronicle %}
        {% include "locations/mage/chantry/field_row.html" with field=form.chronicle %}
    {% endif %}
    {% include "locations/mage/chantry/field_row.html" with field=form.faction %}
    {% include "locations/mage/chantry/field_row.html" with field=form.leadership_type %}
    {% include "locations/mage/chantry/field_row.html" with field=form.season %}
    {% include "locations/mage/chantry/field_row.html" with field=form.chantry_type %}
    <h3 class="row {{ object.get_heading }}">
        <div class="col-sm">Points</div>
        <div class="col-sm">{{ form.total_points }}</div>
    </h3>
    {% if object %}
        <p class="text-muted">{{ object.points }} unspent of {{ object.total_points }}</p>
    {% endif %}
    {% include "locations/mage/chantry/field_row.html" with field=form.integrated_effects %}
    <h3 class="{{ object.get_heading }}">Personnel</h3>
    {% include "locations/mage/chantry/field_row.html" with field=form.leaders %}
    {% include "locations/mage/chantry/field_row.html" with field=form.members %}
    {% include "locations/mage/chantry/field_row.html" with field=form.cabals %}
    {% include "locations/mage/chantry/field_row.html" with field=form.ambassador %}
    {% include "locations/mage/chantry/field_row.html" with field=form.node_tender %}
    {% include "locations/mage/chantry/field_row.html" with field=form.investigator %}
    {% include "locations/mage/chantry/field_row.html" with field=form.guardian %}
    {% include "locations/mage/chantry/field_row.html" with field=form.teacher %}
{% endblock other %}
```

(d) `core/route_policy_manifest.py`: delete the line `locations.views.mage.chantry.ChantryUpdateView` from the `'OBJECT_WRITE'` set, and insert a new group between the `'OBJECT_LIST'` group's closing `    """.split()),` and `    'OBJECT_WRITE': frozenset("""`:
```python
    'OBJECT_ST_WRITE': frozenset("""
locations.views.mage.chantry.ChantryUpdateView
    """.split()),
```

(e) `scripts/build_route_policy_manifest.py`, so a regenerated manifest keeps the classification. After the `PLAYER_MODELS = (...)` line add:
```python
# Player-object edit forms that only a scoped storyteller or staff may use.
ST_WRITE_VIEWS = {"locations.views.mage.chantry.ChantryUpdateView"}
```
and in `classify()`, immediately above `    if issubclass(view, DictView):`:
```python
    if name in ST_WRITE_VIEWS:
        return "OBJECT_ST_WRITE"
```

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage locations.tests.models.mage.test_chantry core.tests.security`. Expected: `OK`. The existing `TestChantryUpdateView` tests pass because their user is the chronicle's head ST.

- [ ] **Step 5: Commit.**
```bash
git add locations/views/mage/chantry.py locations/templates/locations/mage/chantry/form.html \
  locations/templates/locations/mage/chantry/field_row.html core/route_policy_manifest.py \
  scripts/build_route_policy_manifest.py locations/tests/views/mage/chantry_fixtures.py \
  locations/tests/views/mage/test_chantry_update.py
git commit -F - <<'EOF'
Chantry edit form: scoped STs only, and it no longer blanks fields

ChantryUpdateView moves to OBJECT_ST_WRITE, closing the draft owner's
total_points bypass. form.html now renders every field in
DIRECT_FORM_FIELDS (the prominents block was never rendered, so 12 fields
were wiped on save); gauntlet, shroud and dimension_barrier join fields.
Changing the chantry type applies the type grants.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 16: [C4.3] The wizard is the entry point; the direct create form is ST-only

**Files:**
- Modify: `locations/views/mage/chantry.py`
- Modify: `locations/forms/mage/chantry.py` (`ChantryCreateForm.save` only)
- Modify: `locations/urls/mage/create.py`
- Modify: `core/route_policy_manifest.py`
- Modify: `locations/templates/locations/mage/chantry/basics.html`
- Modify: `locations/templates/locations/mage/chantry/list.html`
- Modify: `locations/tests/views/mage/test_chantry.py`, `locations/tests/models/mage/test_chantry.py` (template expectation)
- Create: `locations/tests/views/mage/test_chantry_create.py`

**Interfaces:**
- Consumes (C2): `apply_type_grants(chantry)`.
- Produces: URL `locations:mage:create:chantry` → `ChantryBasicsView` (`OBJECT_CREATE`, now a `CreateView`); new URL `locations:mage:create:chantry_direct` (`chantry/direct/`) → `ChantryCreateView` (`OBJECT_CREATE` plus in-view checks); `direct_create_chronicles(user) -> QuerySet[Chronicle]` (all for staff; chronicles the user heads or is a Mage ST of; none for anonymous). `ChantryCreateForm.save(commit=False)` no longer writes to the database.

- [ ] **Step 1: Write the failing tests.** Create `locations/tests/views/mage/test_chantry_create.py`:

```python
"""Chantry creation entry points: the wizard for players, the direct form for STs."""

from django.test import TestCase
from django.urls import reverse

from characters.models.core.background_block import Background
from game.models import Chronicle
from locations.models.mage.chantry import Chantry
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors

WIZARD_URL = reverse("locations:mage:create:chantry")
DIRECT_URL = reverse("locations:mage:create:chantry_direct")


class ChantryBasicsTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)

    def test_create_chantry_goes_to_the_wizard(self):
        self.assertEqual(Chantry.get_creation_url(), WIZARD_URL)
        self.client.force_login(self.player)
        response = self.client.get(WIZARD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/chantry/basics.html")

    def test_anonymous_is_refused(self):
        self.assertEqual(self.client.get(WIZARD_URL).status_code, 401)

    def test_basics_creates_an_unfinished_player_owned_chantry(self):
        self.client.force_login(self.player)
        response = self.client.post(
            WIZARD_URL,
            {
                "name": "Player Chantry",
                "chronicle": self.chronicle.pk,
                "total_points": 12,
                "gauntlet": 5,
                "shroud": 5,
                "dimension_barrier": 5,
            },
        )
        chantry = Chantry.objects.get(name="Player Chantry")
        self.assertRedirects(response, chantry.get_absolute_url(), fetch_redirect_response=False)
        self.assertEqual(chantry.owner, self.player)
        self.assertEqual(chantry.chronicle, self.chronicle)
        self.assertEqual(chantry.status, "Un")
        self.assertEqual(chantry.creation_status, 1)
        self.assertEqual(chantry.total_points, 12)

    def test_basics_applies_library_type_grants(self):
        Background.objects.get_or_create(name="Library", property_name="library")
        self.client.force_login(self.player)
        self.client.post(
            WIZARD_URL,
            {
                "name": "Stacks",
                "chantry_type": "library",
                "total_points": 10,
                "gauntlet": 5,
                "shroud": 5,
                "dimension_barrier": 5,
            },
        )
        chantry = Chantry.objects.get(name="Stacks")
        self.assertEqual(chantry.backgrounds.get(bg__property_name="library").rating, 3)

    def test_list_links_to_both_forms_for_staff(self):
        self.client.force_login(self.staff)
        response = self.client.get(reverse("locations:mage:list:chantry"))
        self.assertContains(response, WIZARD_URL)
        self.assertContains(response, DIRECT_URL)

    def test_create_directly_link_only_for_storytellers(self):
        self.client.force_login(self.player)
        self.assertNotContains(self.client.get(WIZARD_URL), DIRECT_URL)
        self.client.force_login(self.st)
        self.assertContains(self.client.get(WIZARD_URL), DIRECT_URL)


class ChantryDirectCreateTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.data = {
            "name": "Direct",
            "total_points": 30,
            "gauntlet": 5,
            "shroud": 5,
            "dimension_barrier": 5,
        }

    def test_player_is_refused(self):
        self.client.force_login(self.player)
        self.assertEqual(self.client.get(DIRECT_URL).status_code, 403)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Chantry.objects.filter(name="Direct").exists())

    def test_st_of_another_gameline_is_refused(self):
        self.client.force_login(self.vampire_st)
        self.assertEqual(self.client.get(DIRECT_URL).status_code, 403)

    def test_scoped_st_sees_only_their_chronicles(self):
        self.client.force_login(self.st)
        response = self.client.get(DIRECT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")
        self.assertEqual(
            list(response.context["form"].fields["chronicle"].queryset), [self.chronicle]
        )

    def test_scoped_st_creates_in_their_chronicle(self):
        self.client.force_login(self.st)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Chantry.objects.get(name="Direct").chronicle, self.chronicle)

    def test_wrong_chronicle_st_is_refused(self):
        self.client.force_login(self.other_st)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.chronicle.pk})
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Chantry.objects.filter(name="Direct").exists())

    def test_head_st_qualifies(self):
        self.other_chronicle.head_st = self.player
        self.other_chronicle.save()
        self.client.force_login(self.player)
        response = self.client.post(DIRECT_URL, {**self.data, "chronicle": self.other_chronicle.pk})
        self.assertEqual(response.status_code, 302)

    def test_staff_sees_every_chronicle_and_may_leave_it_blank(self):
        self.client.force_login(self.staff)
        response = self.client.get(DIRECT_URL)
        self.assertEqual(
            set(response.context["form"].fields["chronicle"].queryset),
            set(Chronicle.objects.all()),
        )
        self.assertEqual(self.client.post(DIRECT_URL, self.data).status_code, 302)
        self.assertIsNone(Chantry.objects.get(name="Direct").chronicle)
```

Update the two existing template expectations that change meaning. In `locations/tests/views/mage/test_chantry.py`, class `TestChantryCreateView`, and in `locations/tests/models/mage/test_chantry.py`, class `TestChantryCreateView`, method `test_create_view_template`:
```python
        self.assertTemplateUsed(response, "locations/mage/chantry/form.html")
```
becomes
```python
        self.assertTemplateUsed(response, "locations/mage/chantry/basics.html")
```
(Only the occurrence inside `TestChantryCreateView`; the `TestChantryUpdateView` ones stay `form.html`.)

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_create locations.tests.views.mage.test_chantry`. Expected: the new module fails to import with `django.urls.exceptions.NoReverseMatch: Reverse for 'chantry_direct' not found`, and `TestChantryCreateView.test_create_view_template` fails (`form.html` is still used).

- [ ] **Step 3: Implement.**

(a) `locations/views/mage/chantry.py`. Add imports:
```python
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from core.permissions import PermissionManager
from game.models import Chronicle
```
(place each in its sorted import block). Insert immediately below `DIRECT_FORM_FIELDS`:
```python
def direct_create_chronicles(user):
    """Chronicles in which user may create a chantry with the direct form.

    Mirrors PermissionManager.can_manage_scope for the Mage gameline: staff get
    every chronicle; otherwise the chronicles the user heads or is a Mage ST of.
    """
    if not user.is_authenticated:
        return Chronicle.objects.none()
    if user.is_staff or user.is_superuser:
        return Chronicle.objects.all()
    mage = settings.GAMELINES["mta"]["name"]
    return Chronicle.objects.filter(
        Q(head_st=user) | Q(st_relationships__user=user, st_relationships__gameline__name=mage)
    ).distinct()


```
Replace `ChantryListView` with:
```python
class ChantryListView(ListView):
    model = Chantry
    ordering = ["name"]
    template_name = "locations/mage/chantry/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_directly"] = direct_create_chronicles(self.request.user).exists()
        return context
```
Replace `ChantryCreateView` with:
```python
class ChantryCreateView(LoginRequiredMixin, MessageMixin, CreateView):
    """All-fields create form for Mage STs of the chosen chronicle, and staff."""

    model = Chantry
    fields = ["chronicle", *DIRECT_FORM_FIELDS]
    template_name = "locations/mage/chantry/form.html"
    success_message = "Chantry '{name}' created successfully!"
    error_message = "Failed to create chantry. Please correct the errors below."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not direct_create_chronicles(request.user).exists():
            raise PermissionDenied("Only storytellers can create a chantry directly")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["chronicle"].queryset = direct_create_chronicles(self.request.user)
        form.fields["name"].widget.attrs.update({"placeholder": "Enter name here"})
        form.fields["description"].widget.attrs.update({"placeholder": "Enter description here"})
        return form

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if not PermissionManager.user_can_manage_creation(request.user, form, request=request):
            raise PermissionDenied("Choose a chronicle you are a storyteller for")
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)
        apply_type_grants(self.object)
        return response
```
Replace `ChantryBasicsView` with:
```python
class ChantryBasicsView(LoginRequiredMixin, CreateView):
    """Wizard entry: the player names the chantry and chooses its total points."""

    model = Chantry
    form_class = ChantryCreateForm
    template_name = "locations/mage/chantry/basics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_directly"] = direct_create_chronicles(self.request.user).exists()
        return context

    def form_valid(self, form):
        chantry = form.save(commit=False)
        chantry.owner = self.request.user
        chantry.status = "Un"
        chantry.creation_status = 1
        chantry.save()
        form.save_m2m()
        apply_type_grants(chantry)
        self.object = chantry
        return HttpResponseRedirect(chantry.get_absolute_url())
```
`FormView` stays imported: the step views use it.

(b) `locations/forms/mage/chantry.py`, `ChantryCreateForm.save`, so `commit=False` really defers the write (the Basics view saves once):

Before:
```python
    def save(self, commit=True):
        chantry = super().save(commit=commit)
        chantry.total_points = int(self.cleaned_data.get("total_points"))
        chantry.save()
        return chantry
```
After:
```python
    def save(self, commit=True):
        chantry = super().save(commit=False)
        chantry.total_points = self.cleaned_data["total_points"]
        if commit:
            chantry.save()
            self.save_m2m()
        return chantry
```

(c) `locations/urls/mage/create.py`: replace the `"chantry/"` entry with
```python
    path(
        "chantry/",
        views.mage.ChantryBasicsView.as_view(),
        name="chantry",
    ),
    path(
        "chantry/direct/",
        views.mage.ChantryCreateView.as_view(),
        name="chantry_direct",
    ),
```
(`ChantryBasicsView` is already exported from `locations/views/mage/__init__.py`.)

(d) `core/route_policy_manifest.py`, `'OBJECT_CREATE'` group: add `locations.views.mage.chantry.ChantryBasicsView` on the line above `locations.views.mage.chantry.ChantryCreateView`.

(e) `locations/templates/locations/mage/chantry/basics.html`: insert after `{% endblock creation_title %}`:
```django
{% block progress %}
    {% if can_create_directly %}
        <p class="text-right">
            <a href="{% url 'locations:mage:create:chantry_direct' %}">Storytellers: create directly</a>
        </p>
    {% endif %}
{% endblock progress %}
```

(f) `locations/templates/locations/mage/chantry/list.html`: insert as the first child of `<div class="tg-card-body" style="padding: 24px;">`, before `<div class="row">`:
```django
                {% if user.is_authenticated %}
                    <p class="text-center">
                        <a href="{% url 'locations:mage:create:chantry' %}" class="tg-btn btn-primary">Create Chantry</a>
                        {% if can_create_directly %}
                            <a href="{% url 'locations:mage:create:chantry_direct' %}" class="tg-btn btn-secondary">Create directly</a>
                        {% endif %}
                    </p>
                {% endif %}
```
(`list.html` renders only for staff, since other users get the public list, so the Basics page carries the ST link.)

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage locations.tests.models.mage.test_chantry locations.tests.forms.mage.test_chantry core.tests.security.test_route_policies`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add locations/views/mage/chantry.py locations/forms/mage/chantry.py locations/urls/mage/create.py \
  core/route_policy_manifest.py locations/templates/locations/mage/chantry/basics.html \
  locations/templates/locations/mage/chantry/list.html locations/tests/views/mage/test_chantry.py \
  locations/tests/models/mage/test_chantry.py locations/tests/views/mage/test_chantry_create.py
git commit -F - <<'EOF'
Chantry creation: wizard for players, direct form for scoped STs

"Create Chantry" now opens ChantryBasicsView, which saves a player-owned
Un chantry once, applies the type grants and redirects to the chantry.
The all-fields form moves to chantry_direct: its chronicle list holds
only chronicles the user runs, a non-ST GET is refused, and a POST for a
chronicle the user cannot manage is refused.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 17: [C4.4] Route a chantry's URL through the wizard

**Files:**
- Modify: `locations/views/core/__init__.py`
- Modify: `locations/views/mage/chantry.py`
- Modify: `core/route_policy_manifest.py`
- Create: `locations/tests/views/mage/test_chantry_wizard.py`

**Interfaces:**
- Produces: `GenericLocationDetailView.view_mapping["chantry"] = mage.ChantryCreationView`. The existing `DictView` logic then sends a full editor of a `Un`/`Rev` chantry to the step for its `creation_status` (1 to 6), and everyone else to `ChantryDetailView` or the public card. Manifest: `ChantryCreationView` → `ROUTER`, the six step views → `CHARGEN_STEP`. New `ChantryObjectMixin.get_object()` for the two `FormView` steps. Without it, `EditPermissionMixin` raises `AttributeError: 'super' object has no attribute 'get_object'` (a 500) on the first request.

- [ ] **Step 1: Write the failing test.** Create `locations/tests/views/mage/test_chantry_wizard.py`:

```python
"""The chantry URL routes an unfinished chantry's editor into the creation wizard."""

from django.test import TestCase

from locations.models.mage.chantry import Chantry
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors


class ChantryRoutingTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Routed", owner=self.player, chronicle=self.chronicle, total_points=10
        )
        self.url = self.chantry.get_absolute_url()

    def set_state(self, status, creation_status):
        Chantry.objects.filter(pk=self.chantry.pk).update(
            status=status, creation_status=creation_status
        )

    def test_owner_of_a_draft_gets_the_step_for_its_creation_status(self):
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "locations/mage/chantry/locgen.html")
        self.assertTemplateUsed(response, "locations/mage/chantry/point_spend_form.html")
        self.set_state("Un", 2)
        self.assertTemplateUsed(
            self.client.get(self.url), "locations/mage/chantry/effects_form.html"
        )

    def test_returned_chantry_re_enters_the_wizard(self):
        self.set_state("Rev", 1)
        self.client.force_login(self.player)
        self.assertTemplateUsed(
            self.client.get(self.url), "locations/mage/chantry/point_spend_form.html"
        )

    def test_finished_draft_shows_the_detail_page(self):
        self.set_state("Un", 7)
        self.client.force_login(self.player)
        self.assertTemplateUsed(self.client.get(self.url), "locations/mage/chantry/detail.html")

    def test_submitted_and_approved_chantries_show_the_detail_page(self):
        self.client.force_login(self.player)
        for status in ("Sub", "App"):
            with self.subTest(status=status):
                self.set_state(status, 1)
                response = self.client.get(self.url)
                self.assertTemplateUsed(response, "locations/mage/chantry/detail.html")
                self.assertTemplateNotUsed(response, "locations/mage/chantry/locgen.html")

    def test_non_owner_gets_the_public_card_or_404(self):
        self.client.force_login(self.other_st)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/public_object_detail.html")
        self.assertTemplateNotUsed(response, "locations/mage/chantry/locgen.html")
        self.assertEqual(self.client.post(self.url, {}).status_code, 404)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 1)
```

- [ ] **Step 2: Run it and watch it fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_wizard`. Expected: `FAILED (failures=2)`: `test_owner_of_a_draft_gets_the_step_for_its_creation_status` and `test_returned_chantry_re_enters_the_wizard` get `detail.html` instead of the step.

- [ ] **Step 3: Implement.**

(a) `locations/views/core/__init__.py`, `GenericLocationDetailView.view_mapping`:
```python
            "chantry": mage.ChantryDetailView,
```
becomes
```python
            "chantry": mage.ChantryCreationView,
```
(b) `locations/views/mage/chantry.py`: insert above `class ChantryPointsView(`:
```python
class ChantryObjectMixin:
    """Wizard steps 1-2 are FormViews; resolve the chantry for permission checks."""

    def get_object(self, queryset=None):
        return get_object_or_404(Chantry, pk=self.kwargs["pk"])


```
and change the two class lines:
```python
class ChantryPointsView(EditPermissionMixin, FormView):
class ChantryIntegratedEffectsView(EditPermissionMixin, FormView):
```
to
```python
class ChantryPointsView(EditPermissionMixin, ChantryObjectMixin, FormView):
class ChantryIntegratedEffectsView(EditPermissionMixin, ChantryObjectMixin, FormView):
```
(c) `core/route_policy_manifest.py`: in `'CHARGEN_STEP'`, directly after `locations.views.changeling.creation.FreeholdPowersView` add
```
locations.views.mage.chantry.ChantryAlliesView
locations.views.mage.chantry.ChantryIntegratedEffectsView
locations.views.mage.chantry.ChantryLibrarysView
locations.views.mage.chantry.ChantryNodeView
locations.views.mage.chantry.ChantryPointsView
locations.views.mage.chantry.ChantrySanctumView
```
and in `'ROUTER'`, directly after `locations.views.core.GenericLocationDetailView` add
```
locations.views.mage.chantry.ChantryCreationView
```

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage core.tests.security.test_route_policies locations.tests.models.mage.test_chantry`. Expected: `OK`. `test_every_project_route_and_router_target_has_one_policy` now sees the nested router and its seven targets, and `test_player_object_routers_check_before_handoff` accepts `ChantryCreationView` (`chargen_router = True`).

- [ ] **Step 5: Commit.**
```bash
git add locations/views/core/__init__.py locations/views/mage/chantry.py core/route_policy_manifest.py \
  locations/tests/views/mage/test_chantry_wizard.py
git commit -F - <<'EOF'
Route chantries through the creation wizard

The chantry URL now maps to ChantryCreationView: while a chantry is Un or
Rev its full editor gets the step for creation_status, everyone else the
detail page or public card. Steps 1-2 gain the get_object their
permission mixin needs.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 18: [C4.5] Step 1: Continue rule and remove-one-dot

**Files:**
- Modify: `locations/views/mage/chantry.py` (`ChantryPointsView`)
- Modify: `locations/models/mage/chantry.py` (add `background_ratings`)
- Create: `locations/templates/locations/mage/chantry/display_includes/backgrounds.html`
- Modify: `locations/templates/locations/mage/chantry/locgen.html`
- Modify: `locations/tests/views/mage/test_chantry_wizard.py`

**Interfaces:**
- Consumes (C2): `has_affordable_purchase(chantry)`, `ChantryRemovePurchaseForm(data, chantry=chantry)` with `is_valid()` and `save()`; `save()` calls `remove_background_dot` / `remove_ie_dot` and lets their `ValidationError` propagate. `target` must be `"ie"` or the pk of a rating of *this* chantry.
- Produces: POST `action=remove&target=<rating pk|ie>` on the step-1 URL; the step advances only when `not has_affordable_purchase(chantry)`; context `can_continue`; `Chantry.background_ratings()` (ratings with `bg` selected); include `display_includes/backgrounds.html` (uses `rating.display_name`; `removable=True` adds "−" buttons tied to `<form id="chantry-remove-form">` by the HTML `form` attribute).

- [ ] **Step 1: Write the failing tests.** In `locations/tests/views/mage/test_chantry_wizard.py`, replace the import block with:
```python
from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.mage.effect import Effect
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors
```
and append:
```python


class ChantryPointsStepTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
        self.chantry = Chantry.objects.create(
            name="Spender", owner=self.player, chronicle=self.chronicle, total_points=10
        )
        self.url = self.chantry.get_absolute_url()
        self.client.force_login(self.player)

    def test_continue_when_everything_is_capped(self):
        # 3 points left, but Allies is at 5 and Integrated Effects at 10.
        ChantryBackgroundRating.objects.create(chantry=self.chantry, bg=self.allies, rating=5)
        Chantry.objects.filter(pk=self.chantry.pk).update(
            total_points=33, integrated_effects_score=10
        )
        self.assertRedirects(self.client.post(self.url, {}), self.url, target_status_code=200)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 2)

    def test_no_continue_while_a_purchase_is_affordable(self):
        self.client.post(self.url, {"category": "-----"})
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 1)

    def test_remove_one_background_dot(self):
        rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=self.allies, rating=2
        )
        response = self.client.post(self.url, {"action": "remove", "target": rating.pk})
        self.assertRedirects(response, self.url, target_status_code=200)
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 1)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 1)

    def test_remove_one_integrated_effects_dot(self):
        Chantry.objects.filter(pk=self.chantry.pk).update(integrated_effects_score=2)
        self.client.post(self.url, {"action": "remove", "target": "ie"})
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.integrated_effects_score, 1)

    def test_refused_removal_changes_nothing_and_says_why(self):
        Chantry.objects.filter(pk=self.chantry.pk).update(integrated_effects_score=1)
        self.chantry.integrated_effects.add(Effect.objects.create(name="Ward", prime=3))
        response = self.client.post(self.url, {"action": "remove", "target": "ie"}, follow=True)
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.integrated_effects_score, 1)
        self.assertTrue(list(response.context["messages"]))

    def test_another_chantrys_rating_cannot_be_removed(self):
        other = Chantry.objects.create(name="Other", total_points=10)
        rating = ChantryBackgroundRating.objects.create(chantry=other, bg=self.allies, rating=2)
        response = self.client.post(
            self.url, {"action": "remove", "target": rating.pk}, follow=True
        )
        rating.refresh_from_db()
        self.assertEqual(rating.rating, 2)
        self.assertTrue(list(response.context["messages"]))

    def test_each_purchase_has_a_remove_button(self):
        rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=self.allies, rating=1
        )
        Chantry.objects.filter(pk=self.chantry.pk).update(integrated_effects_score=1)
        response = self.client.get(self.url)
        self.assertContains(response, 'id="chantry-remove-form"')
        self.assertContains(
            response, f'form="chantry-remove-form" name="target" value="{rating.pk}"'
        )
        self.assertContains(response, 'form="chantry-remove-form" name="target" value="ie"')
```

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_wizard.ChantryPointsStepTests`. Expected: `FAILED (failures=6)`: `test_continue_when_everything_is_capped` (`200 != 302`, the old `points < 2` rule), `test_remove_one_background_dot` (`200 != 302`), `test_remove_one_integrated_effects_dot` (`2 != 1`), `test_refused_removal_changes_nothing_and_says_why` and `test_another_chantrys_rating_cannot_be_removed` (`[] is not true`), and `test_each_purchase_has_a_remove_button`.

- [ ] **Step 3: Implement.**

(a) `locations/views/mage/chantry.py`. Add imports: `from django.contrib import messages`, add `ValidationError` to `from django.core.exceptions import PermissionDenied`, add `ChantryRemovePurchaseForm` to the `from locations.forms.mage.chantry import (...)` list, and add `has_affordable_purchase` to the `from locations.services.chantry_points import ...` line. In `ChantryPointsView.get_context_data`, below `context["is_approved_user"] = True  # If we got here, user has permission`, add:
```python
        context["can_continue"] = not has_affordable_purchase(self.object)
```
Replace `ChantryPointsView.post`:

Before:
```python
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))
        if obj.points < 2:
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().post(request, *args, **kwargs)
```
After:
```python
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))
        if request.POST.get("action") == "remove":
            remove_form = ChantryRemovePurchaseForm(request.POST, chantry=obj)
            if not remove_form.is_valid():
                messages.error(request, "That purchase cannot be removed.")
            else:
                try:
                    remove_form.save()
                except ValidationError as exc:
                    messages.error(request, " ".join(exc.messages))
            return HttpResponseRedirect(obj.get_absolute_url())
        if not has_affordable_purchase(obj):
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().post(request, *args, **kwargs)
```

(b) `locations/models/mage/chantry.py`: insert above `    def integrated_effects_number(self):`:
```python
    def background_ratings(self):
        """This chantry's background ratings with their Background, for templates."""
        return self.backgrounds.select_related("bg")

```

(c) Create `locations/templates/locations/mage/chantry/display_includes/backgrounds.html`:
```django
{% load dots %}
{% comment %}
    Chantry backgrounds. With removable=True (wizard step 1) each dot and the
    Integrated Effects score get a "−" button that submits #chantry-remove-form.
{% endcomment %}
<div class="tg-card mb-3">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title mta_heading">Backgrounds</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        {% with ratings=object.background_ratings %}
            {% if ratings %}
                <div class="d-flex justify-content-center align-items-center flex-wrap">
                    {% for rating in ratings %}
                        <div class="px-3 py-2">
                            <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">{{ rating.display_name }}:</span>
                            <span class="dots colored-dots">{{ rating.rating|dots }}</span>
                            {% if removable %}
                                <button type="submit" form="chantry-remove-form" name="target" value="{{ rating.pk }}" class="tg-btn btn-sm btn-secondary" aria-label="Remove one {{ rating.display_name }} dot">−</button>
                            {% endif %}
                            {% if rating.note %}
                                <br>
                                <small class="text-muted">
                                    {% if rating.url %}
                                        <a href="{{ rating.url }}">{{ rating.note }}</a>
                                    {% else %}
                                        {{ rating.note }}
                                    {% endif %}
                                </small>
                            {% endif %}
                        </div>
                    {% endfor %}
                </div>
            {% else %}
                <p class="text-muted mb-0">No backgrounds defined.</p>
            {% endif %}
        {% endwith %}
        {% if removable and object.integrated_effects_score %}
            <div class="px-3 py-2">
                <span style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-secondary); margin-right: 8px;">Integrated Effects:</span>
                <span class="dots colored-dots">{{ object.integrated_effects_score|dots:10 }}</span>
                <button type="submit" form="chantry-remove-form" name="target" value="ie" class="tg-btn btn-sm btn-secondary" aria-label="Remove one Integrated Effects dot">−</button>
            </div>
        {% endif %}
    </div>
</div>
```
This chantry-only include replaces the shared `characters/core/background_block/detail.html` for chantries. The shared template is used by 30 character and group templates, and `PooledBackgroundRating` has no `display_name`, so it is left unchanged.

(d) `locations/templates/locations/mage/chantry/locgen.html` (CRLF; use Edit). Replace the `points` block:

Before:
```django
    {% block points %}
        {% include "locations/mage/chantry/display_includes/resources_remaining.html" %}
        {% include "characters/core/background_block/detail.html" with backgrounds=object.backgrounds %}
        {% if object.creation_status == 1 %}
            {% if is_approved_user %}
                {% include "locations/mage/chantry/point_spend_form.html" %}
            {% endif %}
        {% endif %}
    {% endblock points %}
```
After:
```django
    {% block points %}
        {% include "locations/mage/chantry/display_includes/resources_remaining.html" %}
        {% if object.creation_status == 1 and is_approved_user %}
            {% include "locations/mage/chantry/display_includes/backgrounds.html" with removable=True %}
            {% if can_continue %}
                <p class="text-center">Nothing else can be bought. Save to continue.</p>
            {% endif %}
            {% include "locations/mage/chantry/point_spend_form.html" %}
        {% else %}
            {% include "locations/mage/chantry/display_includes/backgrounds.html" %}
        {% endif %}
    {% endblock points %}
```
Append at the end of the file (after `{% endblock buttons %}`). The remove form must sit outside the main `<form>` of `core/form.html`; `footer` is the first `core/base.html` block after it.
```django
{% block footer %}
    {# Outside the main form: the "−" buttons reach it through their form attribute. #}
    {% if is_approved_user and object.creation_status == 1 %}
        <form id="chantry-remove-form" method="post" action="{{ object.get_absolute_url }}">
            {% csrf_token %}
            <input type="hidden" name="action" value="remove">
        </form>
    {% endif %}
{% endblock footer %}
```

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage.test_chantry_wizard`. Expected: `OK` (12 tests).

- [ ] **Step 5: Commit.**
```bash
git add locations/views/mage/chantry.py locations/models/mage/chantry.py \
  locations/templates/locations/mage/chantry/display_includes/backgrounds.html \
  locations/templates/locations/mage/chantry/locgen.html locations/tests/views/mage/test_chantry_wizard.py
git commit -F - <<'EOF'
Chantry wizard step 1: continue when nothing is affordable; remove a dot

The step advances when has_affordable_purchase() is false, so a chantry
with every background and Integrated Effects capped no longer gets stuck.
Each background dot and the IE score get a "-" button that POSTs
action=remove to ChantryRemovePurchaseForm; refusals are shown as messages.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 19: [C4.6] Step 2: effect affordability, remove an effect, working toggle

**Files:**
- Modify: `locations/forms/mage/chantry.py` (`ChantryEffectsForm`)
- Modify: `locations/views/mage/chantry.py` (`ChantryIntegratedEffectsView.post`)
- Replace: `locations/templates/locations/mage/chantry/effects_form.html`
- Modify: `locations/templates/locations/mage/chantry/display_includes/integrated_effects.html`
- Modify: `locations/templates/locations/mage/chantry/locgen.html`
- Modify: `locations/tests/views/mage/test_chantry_wizard.py`

**Interfaces:**
- Consumes: `affordable_effects`, `has_affordable_effect` (C3.2); `remove_effect(chantry, effect)` (C2).
- Produces: step 2 advances only when `not has_affordable_effect(chantry)`; POST `action=remove_effect&effect=<pk>` (only an effect already in `integrated_effects`); `ChantryEffectsForm.clean()` refuses a created effect that costs 0, costs more than `current_ie_points()`, or has a Sphere above `rank`; its `select` queryset is `affordable_effects(chantry)`.

- [ ] **Step 1: Write the failing tests.** Append to `locations/tests/views/mage/test_chantry_wizard.py`:
```python


class ChantryEffectsStepTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        # rank 3, Integrated Effects 1 = 4 IE points
        self.chantry = Chantry.objects.create(
            name="Warded",
            owner=self.player,
            chronicle=self.chronicle,
            total_points=30,
            integrated_effects_score=1,
            creation_status=2,
        )
        self.url = self.chantry.get_absolute_url()
        self.client.force_login(self.player)

    def test_continue_when_no_effect_fits(self):
        Effect.objects.create(name="Big", forces=3, prime=2)  # costs 5
        self.client.post(self.url, {})
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 3)

    def test_leftover_points_do_not_block_when_nothing_fits(self):
        self.chantry.integrated_effects.add(Effect.objects.create(name="Ward", prime=3))
        Effect.objects.create(name="Bolt", forces=2)  # 1 IE point left, costs 2
        self.client.post(self.url, {})
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 3)

    def test_no_continue_while_an_effect_fits(self):
        Effect.objects.create(name="Bolt", forces=2)
        self.client.post(self.url, {})
        self.chantry.refresh_from_db()
        self.assertEqual(self.chantry.creation_status, 2)

    def test_selecting_an_affordable_effect_integrates_it(self):
        bolt = Effect.objects.create(name="Bolt", forces=2)
        self.client.post(self.url, {"select": bolt.pk})
        self.assertIn(bolt, self.chantry.integrated_effects.all())

    def test_creating_an_effect_over_the_remaining_points_is_refused(self):
        Effect.objects.create(name="Bolt", forces=1)  # keeps the step open
        response = self.client.post(
            self.url,
            {"select_or_create": "on", "name": "Too big", "forces": 3, "prime": 2},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Effect.objects.filter(name="Too big").exists())
        self.assertFalse(self.chantry.integrated_effects.exists())

    def test_creating_an_effect_above_the_chantry_rank_is_refused(self):
        Effect.objects.create(name="Bolt", forces=1)
        self.client.post(self.url, {"select_or_create": "on", "name": "Too high", "forces": 4})
        self.assertFalse(Effect.objects.filter(name="Too high").exists())

    def test_creating_an_affordable_effect_integrates_it(self):
        Effect.objects.create(name="Bolt", forces=1)
        self.client.post(self.url, {"select_or_create": "on", "name": "Shield", "forces": 2})
        self.assertTrue(self.chantry.integrated_effects.filter(name="Shield").exists())

    def test_remove_an_integrated_effect(self):
        ward = Effect.objects.create(name="Ward", prime=2)
        self.chantry.integrated_effects.add(ward)
        response = self.client.post(self.url, {"action": "remove_effect", "effect": ward.pk})
        self.assertRedirects(response, self.url, target_status_code=200)
        self.assertFalse(self.chantry.integrated_effects.exists())
        self.assertTrue(Effect.objects.filter(pk=ward.pk).exists())

    def test_the_page_offers_remove_buttons_and_a_working_toggle(self):
        ward = Effect.objects.create(name="Ward", prime=2)
        self.chantry.integrated_effects.add(ward)
        Effect.objects.create(name="Bolt", forces=1)
        response = self.client.get(self.url)
        self.assertContains(
            response, f'form="chantry-remove-effect-form" name="effect" value="{ward.pk}"'
        )
        self.assertContains(
            response,
            'data-create-or-select-container="select_or_create" data-create-or-select-mode="select"',
        )
        self.assertContains(
            response,
            'data-create-or-select-container="select_or_create" data-create-or-select-mode="create"',
        )
        self.assertNotContains(response, 'id="effect creation"')
```

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_wizard.ChantryEffectsStepTests`. Expected: `FAILED (failures=6)`: `test_continue_when_no_effect_fits` and `test_leftover_points_do_not_block_when_nothing_fits` (`2 != 3`, the old `current_ie_points() == 0` rule), `test_creating_an_effect_over_the_remaining_points_is_refused` (`302 != 200`), `test_creating_an_effect_above_the_chantry_rank_is_refused`, `test_remove_an_integrated_effect` and `test_the_page_offers_remove_buttons_and_a_working_toggle`.

- [ ] **Step 3: Implement.**

(a) `locations/forms/mage/chantry.py`: add `from locations.services.chantry_points import affordable_effects` to the imports, then replace the head of `ChantryEffectsForm` (its `save` stays):

Before:
```python
class ChantryEffectsForm(EffectCreateOrSelectForm):
    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        self.object = Chantry.objects.get(pk=pk)
        super().__init__(*args, **kwargs)
        q = Effect.objects.filter(max_sphere__lte=self.object.rank)
        q = q.exclude(pk__in=self.object.integrated_effects.all())
        q = q.exclude(rote_cost__gt=self.object.current_ie_points())
        self.fields["select"].queryset = q
```
After:
```python
class ChantryEffectsForm(EffectCreateOrSelectForm):
    SPHERES = (
        "correspondence",
        "time",
        "spirit",
        "matter",
        "life",
        "forces",
        "entropy",
        "mind",
        "prime",
    )

    def __init__(self, *args, **kwargs):
        pk = kwargs.pop("pk")
        self.object = Chantry.objects.get(pk=pk)
        super().__init__(*args, **kwargs)
        self.fields["select"].queryset = affordable_effects(self.object)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("select_or_create"):
            return cleaned_data  # a selection is limited by the queryset
        dots = [cleaned_data.get(sphere) or 0 for sphere in self.SPHERES]
        cost = sum(dots)
        if cost < 1:
            raise forms.ValidationError("An effect needs at least one Sphere dot.")
        if cost > self.object.current_ie_points():
            raise forms.ValidationError(
                f"This effect costs {cost}; only {self.object.current_ie_points()} "
                "Integrated Effects points remain."
            )
        if max(dots) > self.object.rank:
            raise forms.ValidationError(
                f"A rank {self.object.rank} chantry cannot integrate Spheres above "
                f"{self.object.rank}."
            )
        return cleaned_data
```
Then delete `from characters.models.mage.effect import Effect` if ruff reports it unused (`$RUFF check locations/forms/mage/chantry.py`).

(b) `locations/views/mage/chantry.py`: add `has_affordable_effect` and `remove_effect` to the `from locations.services.chantry_points import (...)` list. Replace `ChantryIntegratedEffectsView.post`:

Before:
```python
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))
        if obj.current_ie_points() == 0:
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().post(request, *args, **kwargs)
```
After:
```python
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))
        if request.POST.get("action") == "remove_effect":
            effect = obj.integrated_effects.filter(pk=request.POST.get("effect") or None).first()
            if effect is None:
                messages.error(request, "That effect is not integrated into this chantry.")
            else:
                try:
                    remove_effect(obj, effect)
                except ValidationError as exc:
                    messages.error(request, " ".join(exc.messages))
            return HttpResponseRedirect(obj.get_absolute_url())
        if not has_affordable_effect(obj):
            obj.creation_status += 1
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        return super().post(request, *args, **kwargs)
```

(c) Replace `locations/templates/locations/mage/chantry/effects_form.html` entirely. The old hand-written script hid the selector in both branches; the `CreateOrSelectWidget` already injects a toggle script for containers marked with data attributes.
```django
{% include "locations/mage/chantry/display_includes/integrated_effects.html" with removable=True %}
<div class="row">
    <div class="col-sm">Create New Effect: {{ form.select_or_create }}</div>
</div>
{# The CreateOrSelect widget script toggles these two containers. #}
<div data-create-or-select-container="{{ form.select_or_create.name }}" data-create-or-select-mode="select">
    <div class="row">
        <div class="col-sm">{{ form.select }}</div>
    </div>
</div>
<div data-create-or-select-container="{{ form.select_or_create.name }}" data-create-or-select-mode="create" class="d-none">
    <div class="row">
        <div class="col-sm">Name</div>
        <div class="col-sm">{{ form.name }}</div>
    </div>
    {% include "characters/mage/spheres/form.html" %}
    <div class="row">
        <div class="col-sm">Systems</div>
        <div class="col-sm">{{ form.description }}</div>
    </div>
</div>
```

(d) `locations/templates/locations/mage/chantry/display_includes/integrated_effects.html` (CRLF; use Edit): after the line `                                <p>{{ effect.spheres }}</p>` insert
```django
                                {% if removable %}
                                    <button type="submit" form="chantry-remove-effect-form" name="effect" value="{{ effect.pk }}" class="tg-btn btn-sm btn-secondary">Remove</button>
                                {% endif %}
```

(e) `locgen.html`, inside `{% block footer %}`, after the `chantry-remove-form` `{% endif %}`:
```django
    {% if is_approved_user and object.creation_status == 2 %}
        <form id="chantry-remove-effect-form" method="post" action="{{ object.get_absolute_url }}">
            {% csrf_token %}
            <input type="hidden" name="action" value="remove_effect">
        </form>
    {% endif %}
```

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage.test_chantry_wizard locations.tests.forms.mage.test_chantry`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add locations/forms/mage/chantry.py locations/views/mage/chantry.py \
  locations/templates/locations/mage/chantry/effects_form.html \
  locations/templates/locations/mage/chantry/display_includes/integrated_effects.html \
  locations/templates/locations/mage/chantry/locgen.html locations/tests/views/mage/test_chantry_wizard.py
git commit -F - <<'EOF'
Chantry wizard step 2: affordable effects, remove an effect, fix toggle

The step advances when no effect fits the remaining IE points and rank,
instead of only at exactly 0 points. Created effects are checked on the
server against cost and rank. Each integrated effect gets a Remove
button, and the create/select toggle uses the widget's own script.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 20: [C4.7] Steps 3 to 6 link what they create; "Back to point spending"

**Files:**
- Modify: `locations/views/mage/chantry.py`
- Modify: `locations/models/mage/chantry.py` (`set_library`)
- Create: `locations/templates/locations/mage/chantry/skip_step.html`
- Modify: `locations/templates/locations/mage/chantry/locgen.html`
- Modify: `locations/tests/views/mage/test_chantry_wizard.py`

**Interfaces:**
- Consumes (C2): `ChantryBackgroundRating.linked_object` (assignable; `None` when unset or when the target is gone).
- Produces: `ChantryBackToPointsMixin` (`back_to_points(request)` returns a redirect for POST `action=back_to_points`, else `None`; its `post` tries it first), used by steps 2 to 6. `ChantryBackgroundStepView(ChantryBackToPointsMixin, GenericBackgroundView)` is the base of steps 3 to 6: `special_valid_action` stores the created object on `self.current_background.linked_object` (saved by `GenericBackgroundView.form_valid` right after), Node also calls `chantry.add_node(node)` and Library `chantry.set_library(library)`, and a step with nothing to set up renders `skip_step.html` (Continue plus Back). `Chantry.set_library` now persists `chantry_library`. `GenericBackgroundView` itself is unchanged.

- [ ] **Step 1: Write the failing tests.** In `locations/tests/views/mage/test_chantry_wizard.py` add to the imports:
```python
from locations.models.mage.library import Library
from locations.models.mage.node import Node
from locations.models.mage.sanctum import Sanctum
from locations.views.mage.chantry import ChantryLibrarysView, ChantryNodeView, ChantrySanctumView
```
and append:
```python


class ChantryResourceStepTests(TestCase):
    """Steps 3-6 create a Node, Library, Allies or Sanctum and link it to the rating."""

    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Resourced", owner=self.player, chronicle=self.chronicle, total_points=30
        )
        self.url = self.chantry.get_absolute_url()
        self.client.force_login(self.player)

    def rating(self, property_name, rating=1):
        bg = Background.objects.get_or_create(
            name=property_name.title(), property_name=property_name
        )[0]
        return ChantryBackgroundRating.objects.create(chantry=self.chantry, bg=bg, rating=rating)

    def step_view(self, view_class, rating):
        view = view_class()
        view.kwargs = {"pk": self.chantry.pk}
        view.object = self.chantry
        view.current_background = rating
        return view

    def test_allies_step_links_the_created_npc(self):
        rating = self.rating("allies")
        Chantry.objects.filter(pk=self.chantry.pk).update(creation_status=5)
        response = self.client.post(
            self.url, {"npc_type": "mtahuman", "name": "Friendly Acolyte", "rank": 1}
        )
        self.assertRedirects(response, self.url, fetch_redirect_response=False)
        rating.refresh_from_db()
        self.assertTrue(rating.complete)
        self.assertEqual(rating.linked_object.name, "Friendly Acolyte")

    def test_node_step_links_and_attaches_the_node(self):
        rating = self.rating("node", 2)
        node = Node.objects.create(name="Spring", rank=2)
        self.step_view(ChantryNodeView, rating).special_valid_action(node)
        self.assertEqual(rating.linked_object, node)
        self.assertIn(node, self.chantry.nodes.all())

    def test_library_step_links_and_sets_the_library(self):
        rating = self.rating("library", 2)
        library = Library.objects.create(name="Stacks", rank=2)
        self.step_view(ChantryLibrarysView, rating).special_valid_action(library)
        self.assertEqual(rating.linked_object, library)
        self.assertEqual(Chantry.objects.get(pk=self.chantry.pk).chantry_library, library)

    def test_sanctum_step_links_the_sanctum(self):
        rating = self.rating("sanctum")
        sanctum = Sanctum.objects.create(name="Sanctum", rank=1)
        self.step_view(ChantrySanctumView, rating).special_valid_action(sanctum)
        self.assertEqual(rating.linked_object, sanctum)

    def test_step_with_an_open_rating_renders_its_form(self):
        self.rating("allies")
        Chantry.objects.filter(pk=self.chantry.pk).update(creation_status=5)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "characters/core/ally/form_include.html")


class ChantryBackToPointsTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Returning",
            owner=self.player,
            chronicle=self.chronicle,
            total_points=30,
            integrated_effects_score=1,
        )
        self.ward = Effect.objects.create(name="Ward", prime=1)
        self.chantry.integrated_effects.add(self.ward)
        allies = Background.objects.get_or_create(name="Allies", property_name="allies")[0]
        self.allies = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=allies, rating=2
        )
        self.url = self.chantry.get_absolute_url()
        self.client.force_login(self.player)

    def test_every_later_step_can_go_back_keeping_purchases(self):
        for step in range(2, 7):
            with self.subTest(step=step):
                Chantry.objects.filter(pk=self.chantry.pk).update(creation_status=step)
                page = self.client.get(self.url)
                self.assertContains(page, 'name="action" value="back_to_points"')
                response = self.client.post(self.url, {"action": "back_to_points"})
                self.assertRedirects(response, self.url, fetch_redirect_response=False)
                self.chantry.refresh_from_db()
                self.assertEqual(self.chantry.creation_status, 1)
                self.assertEqual(self.chantry.integrated_effects_score, 1)
                self.assertEqual(list(self.chantry.integrated_effects.all()), [self.ward])
                self.allies.refresh_from_db()
                self.assertEqual(self.allies.rating, 2)

    def test_first_step_has_no_back_button(self):
        self.assertNotContains(self.client.get(self.url), 'value="back_to_points"')
```
Steps 3, 4 and 6 in the Back test have no open rating, so they exercise the skip page; step 5 has an open Allies rating, so it exercises the `locgen.html` form.

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_wizard.ChantryResourceStepTests locations.tests.views.mage.test_chantry_wizard.ChantryBackToPointsTests`. Expected: `FAILED (failures=8, errors=1)`: an error in `test_allies_step_links_the_created_npc` (`'NoneType' object has no attribute 'name'`), failures in the Node, Library and Sanctum link tests (`None != <...>`), and in all five subtests of `test_every_later_step_can_go_back_keeping_purchases`.

- [ ] **Step 3: Implement.**

(a) `locations/views/mage/chantry.py`: change `from django.shortcuts import get_object_or_404` to `from django.shortcuts import get_object_or_404, render`. Insert above `class ChantryIntegratedEffectsView(`:
```python
class ChantryBackToPointsMixin:
    """Steps 2-6: POST action=back_to_points returns to step 1 and keeps every purchase."""

    def back_to_points(self, request):
        """Handle the Back action; None when the POST is something else."""
        if request.POST.get("action") != "back_to_points":
            return None
        chantry = get_object_or_404(Chantry, pk=self.kwargs["pk"])
        chantry.creation_status = 1
        chantry.save(update_fields=["creation_status"])
        return HttpResponseRedirect(chantry.get_absolute_url())

    def post(self, request, *args, **kwargs):
        return self.back_to_points(request) or super().post(request, *args, **kwargs)


```
Change the effects step's class line and the start of its `post` (it defines its own `post`, so it calls the helper directly):
```python
class ChantryIntegratedEffectsView(EditPermissionMixin, ChantryObjectMixin, FormView):
```
becomes
```python
class ChantryIntegratedEffectsView(
    ChantryBackToPointsMixin, EditPermissionMixin, ChantryObjectMixin, FormView
):
```
and in its `post`, before `obj = get_object_or_404(Chantry, pk=kwargs.get("pk"))`, insert:
```python
        back = self.back_to_points(request)
        if back is not None:
            return back
```
Replace the four classes `ChantryNodeView`, `ChantryLibrarysView`, `ChantryAlliesView` and `ChantrySanctumView` (everything from `class ChantryNodeView(GenericBackgroundView):` up to `class ChantryCreationView(DictView):`) with:
```python
class ChantryBackgroundStepView(ChantryBackToPointsMixin, GenericBackgroundView):
    """Steps 3-6: create the object a Node/Library/Allies/Sanctum rating stands for."""

    primary_object_class = Chantry
    is_owned = False
    template_name = "locations/mage/chantry/locgen.html"

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if not obj.backgrounds.filter(
            bg__property_name=self.background_name, complete=False
        ).exists():
            return render(
                request,
                "locations/mage/chantry/skip_step.html",
                {"object": obj, "background_name": self.background_name},
            )
        return super().get(request, *args, **kwargs)

    def special_valid_action(self, background_object):
        # GenericBackgroundView.form_valid saves current_background after this call.
        self.current_background.linked_object = background_object


class ChantryNodeView(ChantryBackgroundStepView):
    background_name = "node"
    form_class = NodeForm

    def special_valid_action(self, background_object):
        super().special_valid_action(background_object)
        self.get_object().add_node(background_object)


class ChantryLibrarysView(ChantryBackgroundStepView):
    background_name = "library"
    form_class = LibraryForm

    def special_valid_action(self, background_object):
        super().special_valid_action(background_object)
        self.get_object().set_library(background_object)


class ChantryAlliesView(ChantryBackgroundStepView):
    background_name = "allies"
    form_class = LinkedNPCForm


class ChantrySanctumView(ChantryBackgroundStepView):
    background_name = "sanctum"
    form_class = SanctumForm


```
The routed class names are unchanged, so the manifest needs no edit; `ChantryBackgroundStepView` is not routed.

(b) `locations/models/mage/chantry.py`, `set_library`:
```python
    def set_library(self, library):
        self.chantry_library = library
        library.contained_within.add(self)
        return True
```
becomes
```python
    def set_library(self, library):
        self.chantry_library = library
        self.save(update_fields=["chantry_library"])
        library.contained_within.add(self)
        return True
```

(c) Create `locations/templates/locations/mage/chantry/skip_step.html`:
```django
{% extends "core/base.html" %}
{% block title %}
    Continue {{ object.name }}
{% endblock title %}
{% block content %}
    <main class="container py-4">
        <h1 class="{{ object.get_heading }}">{{ object.name }}</h1>
        <p>No {{ background_name }} background was bought, so there is nothing to set up in this step.</p>
        <form method="post" action="{{ object.get_absolute_url }}">
            {% csrf_token %}
            <button type="submit" class="tg-btn btn-primary">Continue</button>
            <button type="submit" name="action" value="back_to_points" class="tg-btn btn-secondary">
                Back to point spending
            </button>
        </form>
    </main>
{% endblock content %}
```

(d) `locations/templates/locations/mage/chantry/locgen.html` (CRLF; use Edit). Replace the `buttons` block:

Before:
```django
{% block buttons %}
    {% if not is_approved_user %}
    {% else %}
        {{ block.super }}
    {% endif %}
{% endblock buttons %}
```
After (keep the button tag on one line):
```django
{% block buttons %}
    {% if is_approved_user %}
        {{ block.super }}
        {% if object.creation_status > 1 %}
            <div class="tg-card mt-3">
                <div class="tg-card-body text-center">
                    <button type="submit" name="action" value="back_to_points" formnovalidate class="tg-btn btn-secondary btn-lg">
                        <i class="fas fa-arrow-left"></i> Back to point spending
                    </button>
                </div>
            </div>
        {% endif %}
    {% endif %}
{% endblock buttons %}
```
Pass the open rating to the two includes that read it under another name:
```django
                {% include "locations/mage/node/form_include.html" %}
```
becomes
```django
                {% include "locations/mage/node/form_include.html" with current_node=current_background %}
```
and
```django
                {% include "locations/mage/sanctum/form_include.html" %}
```
becomes
```django
                {% include "locations/mage/sanctum/form_include.html" with current_sanctum=current_background %}
```
(`is_approved_user` is already set for steps 3 to 6 by `PermissionRequiredMixin.get_context_data`, through `GenericBackgroundView`'s `SpendFreebiesPermissionMixin`.)

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage locations.tests.models.mage.test_chantry`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add locations/views/mage/chantry.py locations/models/mage/chantry.py \
  locations/templates/locations/mage/chantry/skip_step.html \
  locations/templates/locations/mage/chantry/locgen.html locations/tests/views/mage/test_chantry_wizard.py
git commit -F - <<'EOF'
Chantry wizard steps 3-6: link created objects; add Back to point spending

Node, Library, Allies and Sanctum steps store the created object on the
rating's linked_object; the Node is added to nodes and the Library set as
chantry_library (set_library now saves it). Steps 2-6 and their skip
page offer a Back action that returns to step 1 keeping every purchase.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 21: [C4.8] Detail page: faction term, points, Resources card, ST-only Edit

**Files:**
- Modify: `locations/models/mage/chantry.py`
- Modify: `locations/views/mage/chantry.py` (`ChantryDetailView`)
- Create: `locations/templates/locations/mage/chantry/display_includes/resource_card.html`
- Modify: `locations/templates/locations/mage/chantry/detail.html`
- Create: `locations/tests/views/mage/test_chantry_detail.py`

**Interfaces:**
- Consumes (C2): `ChantryBackgroundRating.linked_object`, which works with `prefetch_related("linked_object")` (true for both a ForeignKey and a GenericForeignKey).
- Produces: `Chantry.factional_name() -> str` (first term of the first faction, walking up `parent`, listed in `factional_names`; `"Chantry"` otherwise); `Chantry.node_rating() -> int`; fixed `Chantry.has_node()` (`node_rating() > 0 and total_node() == node_rating()`); `Chantry.resource_ratings()`; context `can_st_edit` on `ChantryDetailView`.

- [ ] **Step 1: Write the failing tests.** Create `locations/tests/views/mage/test_chantry_detail.py`:

```python
"""The chantry detail page: faction term, points, Resources card and ST-only Edit."""

from django.test import TestCase

from characters.models.core.background_block import Background
from characters.models.core.human import Human
from characters.models.mage.faction import MageFaction
from locations.models.mage.chantry import Chantry, ChantryBackgroundRating
from locations.models.mage.library import Library
from locations.models.mage.node import Node
from locations.tests.views.mage.chantry_fixtures import add_chantry_actors


def background(property_name, **extra):
    return Background.objects.get_or_create(
        name=property_name.title(), property_name=property_name, defaults=extra
    )[0]


class FactionalNameTests(TestCase):
    def test_no_faction_is_a_chantry(self):
        self.assertEqual(Chantry(name="Plain").factional_name(), "Chantry")

    def test_faction_in_the_table_uses_its_first_term(self):
        hermes = MageFaction.objects.create(name="Order of Hermes")
        self.assertEqual(Chantry(name="C", faction=hermes).factional_name(), "Covenant")

    def test_sub_faction_walks_up_to_the_first_listed_parent(self):
        hermes = MageFaction.objects.create(name="Order of Hermes")
        house = MageFaction.objects.create(name="House Tytalus", parent=hermes)
        self.assertEqual(Chantry(name="C", faction=house).factional_name(), "Covenant")

    def test_unlisted_faction_tree_falls_back_to_chantry(self):
        root = MageFaction.objects.create(name="Unlisted")
        child = MageFaction.objects.create(name="Also unlisted", parent=root)
        self.assertEqual(Chantry(name="C", faction=child).factional_name(), "Chantry")


class NodeRealisationTests(TestCase):
    def setUp(self):
        self.chantry = Chantry.objects.create(name="Noded", total_points=20)
        self.rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=background("node"), rating=2, complete=True
        )

    def test_nodes_matching_the_rating_realise_it(self):
        self.assertFalse(self.chantry.has_node())
        self.chantry.add_node(Node.objects.create(name="Spring", rank=2))
        self.assertEqual(self.chantry.node_rating(), 2)
        self.assertTrue(self.chantry.has_node())

    def test_no_node_rating_is_not_realised(self):
        self.rating.delete()
        self.assertFalse(self.chantry.has_node())


class ChantryDetailPageTests(TestCase):
    def setUp(self):
        add_chantry_actors(self)
        self.chantry = Chantry.objects.create(
            name="Shown",
            owner=self.player,
            chronicle=self.chronicle,
            status="App",
            total_points=20,
            creation_status=7,
            faction=MageFaction.objects.create(name="Order of Hermes"),
        )
        self.url = self.chantry.get_absolute_url()

    def test_subtitle_and_points_line(self):
        ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=background("allies"), rating=1, complete=True
        )
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertContains(response, "Covenant")
        self.assertContains(response, "2 spent of 20")
        self.assertContains(response, "18 unspent")

    def test_no_unspent_note_when_everything_is_spent(self):
        Chantry.objects.filter(pk=self.chantry.pk).update(total_points=0)
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertContains(response, "0 spent of 0")
        self.assertNotContains(response, "unspent")

    def test_resources_card_links_realised_resources(self):
        node = Node.objects.create(name="Spring", rank=2)
        self.chantry.add_node(node)
        library = Library.objects.create(name="Stacks", rank=0)
        self.chantry.set_library(library)
        ally = Human.objects.create(name="Old Friend")
        rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=background("allies"), rating=1, complete=True
        )
        rating.linked_object = ally
        rating.save()
        ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=background("node"), rating=2, complete=True
        )
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertContains(response, f'href="{node.get_absolute_url()}"')
        self.assertContains(response, "2 of 2 Node dots")
        self.assertContains(response, "Realised")
        self.assertContains(response, f'href="{library.get_absolute_url()}"')
        self.assertContains(response, "0 of 0 books")
        self.assertContains(response, f'href="{ally.get_absolute_url()}"')

    def test_node_deleted_after_linking_shows_as_unlinked(self):
        node = Node.objects.create(name="Doomed", rank=2)
        self.chantry.add_node(node)
        rating = ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=background("node"), rating=2, complete=True, note="Doomed"
        )
        rating.linked_object = node
        rating.save()
        self.assertTrue(self.chantry.has_node())

        node.delete()

        self.assertFalse(self.chantry.has_node())
        rating.refresh_from_db()
        self.assertIsNone(rating.linked_object)
        self.client.force_login(self.player)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unlinked")
        self.assertContains(response, "Unassigned")
        self.assertContains(response, "Doomed")

    def test_background_block_uses_display_name(self):
        bg = background("spies", alternate_name="")
        ChantryBackgroundRating.objects.create(
            chantry=self.chantry, bg=bg, rating=1, display_alt_name=True
        )
        self.client.force_login(self.player)
        self.assertContains(self.client.get(self.url), "Spies:")

    def test_edit_button_only_for_scoped_sts_and_staff(self):
        edit = f'href="{self.chantry.get_update_url()}"'
        self.client.force_login(self.player)
        self.assertNotContains(self.client.get(self.url), edit)
        for user in (self.st, self.staff):
            with self.subTest(user=user.username):
                self.client.force_login(user)
                self.assertContains(self.client.get(self.url), edit)
```

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test locations.tests.views.mage.test_chantry_detail`. Expected: errors in `FactionalNameTests` (`AttributeError: 'Chantry' object has no attribute 'factional_name'`), `NodeRealisationTests` and `test_node_deleted_after_linking_shows_as_unlinked` (the old `has_node` reads `self.node`), and failures in the page tests (no `2 spent of 20`, no Edit link, and `Spies:` missing because the shared block prints the empty alternate name).

- [ ] **Step 3: Implement.**

(a) `locations/models/mage/chantry.py`: replace the broken `has_node`:
```python
    def has_node(self):
        return self.total_node() == self.node
```
with
```python
    def factional_name(self):
        """The faction's own word for a chantry, e.g. "Covenant" for the Order of Hermes.

        Walks up the faction's parents to the first one listed in factional_names.
        """
        faction, seen = self.faction, set()
        while faction is not None and faction.pk not in seen:
            names = self.factional_names.get(faction.name)
            if names:
                return names[0]
            seen.add(faction.pk)
            faction = faction.parent
        return "Chantry"

    def node_rating(self):
        """Total Node dots bought, across every Node rating."""
        return sum(r.rating for r in self.backgrounds.filter(bg__property_name="node"))

    def has_node(self):
        """Whether the attached Nodes realise the whole Node rating."""
        rating = self.node_rating()
        return rating > 0 and self.total_node() == rating

    def resource_ratings(self):
        """Node, Library, Allies and Sanctum ratings with the objects they are linked to."""
        return (
            self.backgrounds.filter(bg__property_name__in=self.WIZARD_RESOURCES)
            .select_related("bg")
            .prefetch_related("linked_object")
        )
```

(b) `locations/views/mage/chantry.py`, `ChantryDetailView.get_context_data`: directly after `context = super().get_context_data(**kwargs)` insert
```python
        context["can_st_edit"] = PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.object, request=self.request
        )
```
(The unused `factions` context below it is removed in C5.2.)

(c) Create `locations/templates/locations/mage/chantry/display_includes/resource_card.html`:
```django
{% load dots %}
<div class="tg-card mb-4">
    <div class="tg-card-header">
        <h5 class="tg-card-title mta_heading">Resources</h5>
    </div>
    <div class="tg-card-body">
        <p class="mb-2">
            <strong>Points:</strong>
            {{ object.total_cost }} spent of {{ object.total_points }}{% if object.points > 0 %} ({{ object.points }} unspent){% endif %}
        </p>
        {% with node_rating=object.node_rating nodes=object.nodes.all %}
            {% if node_rating or nodes %}
                <p class="mb-1">
                    <strong>Nodes:</strong>
                    {{ object.total_node }} of {{ node_rating }} Node dots
                    {% if object.has_node %}
                        <span class="tg-badge badge-success">Realised</span>
                    {% else %}
                        <span class="tg-badge badge-warning">Unassigned</span>
                    {% endif %}
                </p>
                <ul class="mb-2">
                    {% for node in nodes %}
                        <li>
                            <a href="{{ node.get_absolute_url }}">{{ node.name }}</a>
                            <span class="dots colored-dots">{{ node.rank|dots }}</span>
                        </li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        {% if object.chantry_library %}
            <p class="mb-2">
                <strong>Library:</strong>
                <a href="{{ object.chantry_library.get_absolute_url }}">{{ object.chantry_library.name }}</a>,
                {{ object.chantry_library.num_books }} of {{ object.chantry_library.rank }} books
                {% if object.has_library %}
                    <span class="tg-badge badge-success">Complete</span>
                {% else %}
                    <span class="tg-badge badge-warning">Incomplete</span>
                {% endif %}
            </p>
        {% endif %}
        {% with ratings=object.resource_ratings %}
            {% if ratings %}
                <ul class="mb-0">
                    {% for rating in ratings %}
                        <li>
                            {{ rating.display_name }}
                            <span class="dots colored-dots">{{ rating.rating|dots }}</span>:
                            {% if rating.linked_object %}
                                <a href="{{ rating.linked_object.get_absolute_url }}">{{ rating.linked_object.name }}</a>
                            {% else %}
                                <span class="text-muted">Unlinked</span>{% if rating.note %} ({{ rating.note }}){% endif %}
                            {% endif %}
                        </li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    </div>
</div>
```

(d) `locations/templates/locations/mage/chantry/detail.html`: after the `</h1>` in `objectname`, insert
```django
            <p class="tg-card-subtitle mb-0">{{ object.factional_name }}</p>
```
In `model_specific`, replace
```django
    {% include "characters/core/background_block/detail.html" with backgrounds=object.backgrounds %}
```
with
```django
    {% include "locations/mage/chantry/display_includes/backgrounds.html" %}
    {% include "locations/mage/chantry/display_includes/resource_card.html" %}
```
and append at the end of the file:
```django
{% block buttons %}
    {% if can_st_edit %}
        <div class="text-center mb-4">
            <a href="{{ object.get_update_url }}" class="tg-btn btn-primary">Edit</a>
        </div>
    {% endif %}
{% endblock buttons %}
```

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test locations.tests.views.mage locations.tests.models.mage`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add locations/models/mage/chantry.py locations/views/mage/chantry.py \
  locations/templates/locations/mage/chantry/display_includes/resource_card.html \
  locations/templates/locations/mage/chantry/detail.html locations/tests/views/mage/test_chantry_detail.py
git commit -F - <<'EOF'
Chantry detail: faction term, points line, Resources card, ST Edit

Recovers factional_names as factional_name() (walks up faction parents,
falls back to "Chantry"), fixes has_node() to compare attached Nodes with
the Node rating, and adds a Resources card listing Nodes, the Library and
each linked resource, with unlinked ratings shown by their note. The
background block uses display_name. Edit shows only to scoped STs and staff.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:** run each and require the stated result.
  1. `$PY manage.py test` (serially): 0 failures, 0 errors.
  2. `$PY manage.py check`: `System check identified no issues`.
  3. `$PY manage.py test core.tests.security.test_route_policies`: `OK`.
  4. `$RUFF check core/access_policy.py scripts/inventory_authorization_routes.py scripts/build_route_policy_manifest.py locations/views/core/__init__.py locations/views/mage/chantry.py locations/models/mage/chantry.py locations/urls/mage/create.py core/tests/security/test_object_st_write.py locations/tests/views/mage/`: no new findings. `B007` at `ChantryPointForm.__init__` (`cat_label`) predates this unit; if C2 rewrote that loop it is gone. `$RUFF check locations/forms/mage/chantry.py` must show no `F401`. Also run `$RUFF format --check` on every test file this unit created: already formatted.
  5. Route count: `$PY manage.py shell -c "from django.urls import get_resolver; from scripts.inventory_authorization_routes import walk; print(sum(1 for r in walk(get_resolver().url_patterns) if r[1] == ''))"` prints exactly one more than before the unit (the new `chantry_direct`; 1833 → 1834 at `1e77e23`).

## Unit C5: Chantry cleanup

Deletes the rows marked *delete* in the chantry spec's Evidence table, together with their tests. Guard tests live in `core/tests/test_dead_code_removed.py` as `class C5RemovedTests(SimpleTestCase)`. If another unit already created that file, add the imports and the class to it; otherwise create it with the content shown.

The `form.html` `{% block prominents %}` row was deleted by C4.2's rewrite; C5.2 only guards it.

### Task 22: [C5.1] Delete dead `Chantry` methods and the duplicate IE table

**Files:**
- Modify: `locations/models/mage/chantry.py`
- Modify: `locations/forms/mage/chantry.py`
- Modify: `locations/tests/models/mage/test_chantry.py`
- Modify: `locations/tests/views/mage/test_chantry.py`
- Create or modify: `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: `Chantry.get_traits`, `set_rank`, `has_season`, `set_season`, `has_chantry_type`, `set_chantry_type`, `has_faction`, `set_faction`, `points_spent`, and `ChantryPointForm.INTEGRATED_EFFECTS_NUMBERS`. Nothing outside tests calls them. `rank` is still the read-only property, the Library-type rule lives in C2's `apply_type_grants`, and the Points line uses `total_cost()` (C4.8). `Chantry.INTEGRATED_EFFECTS_NUMBERS` stays.

- [ ] **Step 1: Write the failing test.** `core/tests/test_dead_code_removed.py` (merge into the existing file if present):

```python
"""Guards: removed dead code stays removed."""

from django.test import SimpleTestCase

from locations.forms.mage.chantry import ChantryPointForm
from locations.models.mage.chantry import Chantry


class C5RemovedTests(SimpleTestCase):
    """Chantry cleanup (chantry spec, Evidence table rows marked delete)."""

    def test_dead_chantry_methods_are_gone(self):
        for name in (
            "get_traits",
            "set_rank",
            "has_season",
            "set_season",
            "has_chantry_type",
            "set_chantry_type",
            "has_faction",
            "set_faction",
            "points_spent",
        ):
            with self.subTest(name=name):
                self.assertFalse(hasattr(Chantry, name))

    def test_duplicate_ie_table_is_gone_from_the_point_form(self):
        self.assertFalse(hasattr(ChantryPointForm, "INTEGRATED_EFFECTS_NUMBERS"))
        self.assertEqual(Chantry.INTEGRATED_EFFECTS_NUMBERS[10], 90)
```

- [ ] **Step 2: Run it and watch it fail.** `$PY manage.py test core.tests.test_dead_code_removed.C5RemovedTests`. Expected: `FAILED (failures=10)`: nine subtests of `test_dead_chantry_methods_are_gone` and `test_duplicate_ie_table_is_gone_from_the_point_form`. (If C2 already dropped the form constant, 9 failures.)

- [ ] **Step 3: Implement.**

(a) `locations/models/mage/chantry.py`: delete these method blocks entirely, each with its trailing blank line:
```python
    def has_season(self):
        return self.season is not None

    def set_season(self, season):
        self.season = season
        self.save()
        return True

    def has_chantry_type(self):
        return self.chantry_type is not None

    def set_chantry_type(self, chantry_type):
        self.chantry_type = chantry_type
        if chantry_type == "library":
            self.library = 3
        self.save()
        return True
```
```python
    def points_spent(self):
        return (
            2
            * (
                self.allies
                + self.arcane
                + self.backup
                + self.cult
                + self.elders
                + self.integrated_effects
                + self.library
                + self.retainers
                + self.spies
            )
            + 3 * (self.node + self.resources)
            + 4 * (self.enhancement + self.requisitions)
            + 5 * (self.sanctum)
        )
```
```python
    def set_rank(self, rank):
        self.rank = rank
        return True

    def get_traits(self):
        return {
            "allies": self.allies,
            "arcane": self.arcane,
            "backup": self.backup,
            "cult": self.cult,
            "elders": self.elders,
            "integrated_effects": self.integrated_effects,
            "retainers": self.retainers,
            "spies": self.spies,
            "resources": self.resources,
            "enhancement": self.enhancement,
            "requisitions": self.requisitions,
            "reality_zone": self.sanctum,
            "node": self.node,
            "library": self.library,
        }
```
```python
    def set_faction(self, faction):
        self.faction = faction
        return True

    def has_faction(self):
        return self.faction is not None
```

(b) `locations/forms/mage/chantry.py`: in `ChantryPointForm`, delete the class attribute `INTEGRATED_EFFECTS_NUMBERS = { 0: 0, ..., 10: 90, }` (13 lines plus the blank line after it), if it is still there after C2.

(c) Delete the tests of the removed methods. In `locations/tests/models/mage/test_chantry.py`, class `TestChantry`, delete the methods `test_points_spent`, `test_set_rank`, `test_has_faction`, `test_set_faction`, `test_has_chantry_type`, `test_set_chantry_type`, `test_has_season`, `test_set_season` and `test_get_traits`. The `MageFaction` import stays, because `setUp` uses it. In `locations/tests/views/mage/test_chantry.py`, class `TestChantryModel`, delete `test_chantry_has_season`, `test_chantry_set_season`, `test_chantry_has_chantry_type` and `test_chantry_set_chantry_type`. `rank` is still covered by `test_chantry_rank_property`.

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test core.tests.test_dead_code_removed locations.tests.models.mage.test_chantry locations.tests.views.mage.test_chantry locations.tests.forms.mage.test_chantry`. Expected: `OK`. Then `$RUFF check locations/models/mage/chantry.py locations/tests/models/mage/test_chantry.py locations/tests/views/mage/test_chantry.py core/tests/test_dead_code_removed.py`: `All checks passed!`.

- [ ] **Step 5: Commit.**
```bash
git add locations/models/mage/chantry.py locations/forms/mage/chantry.py \
  locations/tests/models/mage/test_chantry.py locations/tests/views/mage/test_chantry.py \
  core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Chantry: delete dead model methods and the duplicate IE table

get_traits, set_rank, has/set_season, has_chantry_type, has/set_faction,
set_chantry_type and points_spent were broken or test-only; points,
total_cost, the read-only rank and apply_type_grants replace them.
ChantryPointForm.INTEGRATED_EFFECTS_NUMBERS duplicated the model's table.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 23: [C5.2] Delete the unused faction breadcrumb, the personnel template and the step-7 block

**Files:**
- Modify: `locations/views/mage/chantry.py` (`ChantryDetailView`)
- Delete: `locations/templates/locations/mage/chantry/personnel_form.html`
- Modify: `locations/templates/locations/mage/chantry/locgen.html`
- Modify: `core/tests/test_dead_code_removed.py`
- Modify: `locations/tests/views/mage/test_chantry_detail.py`

**Interfaces:**
- Removes: context key `factions` from `ChantryDetailView` (no template reads it; `form.html` used it only inside the deleted `prominents` block), `personnel_form.html` (empty), and `{% block personnel %}` in `locgen.html` (the wizard ends at step 6, so `locgen.html` never renders at `creation_status >= 7`).

- [ ] **Step 1: Write the failing tests.** In `core/tests/test_dead_code_removed.py` add the imports
```python
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
```
and add to `C5RemovedTests`:
```python
    def test_personnel_step_templates_are_gone(self):
        with self.assertRaises(TemplateDoesNotExist):
            get_template("locations/mage/chantry/personnel_form.html")
        locgen = get_template("locations/mage/chantry/locgen.html").template.source
        self.assertNotIn("block personnel", locgen)
        form = get_template("locations/mage/chantry/form.html").template.source
        self.assertNotIn("block prominents", form)
```
Append to `ChantryDetailPageTests` in `locations/tests/views/mage/test_chantry_detail.py`:
```python
    def test_no_unused_faction_breadcrumb_in_context(self):
        self.client.force_login(self.player)
        self.assertNotIn("factions", self.client.get(self.url).context)
```

- [ ] **Step 2: Run them and watch them fail.** `$PY manage.py test core.tests.test_dead_code_removed.C5RemovedTests locations.tests.views.mage.test_chantry_detail`. Expected: `FAILED (failures=2)`: `test_personnel_step_templates_are_gone` and `test_no_unused_faction_breadcrumb_in_context`.

- [ ] **Step 3: Implement.**

(a) `locations/views/mage/chantry.py`, `ChantryDetailView.get_context_data`: delete
```python
        factions = []
        f = self.object.faction
        while f is not None:
            factions.append(f)
            f = f.parent
        factions.reverse()
        factions = [f'<a href="{x.get_absolute_url()}">{x}</a>' for x in factions]
        factions = "/".join(factions)
        context["factions"] = factions
```
leaving
```python
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["can_st_edit"] = PermissionManager.user_has_scoped_editor_role(
            self.request.user, self.object, request=self.request
        )
        return context
```
(b) `git rm locations/templates/locations/mage/chantry/personnel_form.html` (this stages the deletion for the commit).

(c) `locations/templates/locations/mage/chantry/locgen.html` (CRLF; use Edit): delete
```django
    {% block personnel %}
        {% if object.creation_status == 7 %}
            {% if is_approved_user %}
                {% include "locations/mage/chantry/personnel_form.html" %}
            {% endif %}
        {% elif object.creation_status > 7 %}
            {% include "locations/mage/chantry/display_includes/members.html" %}
        {% endif %}
    {% endblock personnel %}
```
(`display_includes/members.html` stays; `detail.html` uses it.)

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test core.tests.test_dead_code_removed locations.tests.views.mage`. Expected: `OK`.

- [ ] **Step 5: Commit.**
```bash
git add locations/views/mage/chantry.py locations/templates/locations/mage/chantry/locgen.html \
  core/tests/test_dead_code_removed.py locations/tests/views/mage/test_chantry_detail.py
git commit -F - <<'EOF'
Chantry: delete the unused faction breadcrumb and the step-7 personnel stub

ChantryDetailView built a "factions" context no template reads;
personnel_form.html was empty and locgen.html's personnel block could
never render once the wizard ends at step 6.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

### Task 24: [C5.3] Delete `LoadExamplesView` and the Mage location ajax URLs

**Files:**
- Modify: `locations/views/mage/chantry.py`
- Delete: `locations/urls/mage/ajax.py`
- Modify: `locations/urls/mage/__init__.py`
- Modify: `core/route_policy_manifest.py`
- Modify: `core/tests/test_dead_code_removed.py`

**Interfaces:**
- Removes: `LoadExamplesView`, route `locations:mage:ajax:load_chantry_examples` (`locations/mage/ajax/load_chantry_examples/`), the whole `locations:mage:ajax` namespace (it held only that route), and the manifest entry `locations.views.mage.chantry.LoadExamplesView` (`'LOGIN'`). Its affordability filtering now lives in C2's points service.
- Hazard: `locations/urls/__init__.py` wraps each gameline URL import in `except (ImportError, AttributeError): pass`. If `ajax.py` is deleted but `from . import ajax, ...` stays in `locations/urls/mage/__init__.py`, every Mage location route disappears silently. Remove the import in the same commit; the guard test and the route count below catch a mistake.

- [ ] **Step 1: Write the failing test.** In `core/tests/test_dead_code_removed.py` add the imports
```python
import importlib.util

from django.urls import NoReverseMatch, reverse

from locations.views.mage import chantry as chantry_views
```
(each in its sorted block) and add to `C5RemovedTests`:
```python
    def test_chantry_examples_ajax_endpoint_is_gone(self):
        self.assertFalse(hasattr(chantry_views, "LoadExamplesView"))
        self.assertIsNone(importlib.util.find_spec("locations.urls.mage.ajax"))
        with self.assertRaises(NoReverseMatch):
            reverse("locations:mage:ajax:load_chantry_examples")
        # locations/urls/__init__.py swallows ImportError; the Mage routes must survive.
        self.assertEqual(reverse("locations:mage:create:chantry"), "/locations/mage/create/chantry/")
```
Record the route count before changing anything:
```bash
$PY manage.py shell -c "from django.urls import get_resolver; from scripts.inventory_authorization_routes import walk; print(sum(1 for r in walk(get_resolver().url_patterns) if r[1] == ''))"
```
(1834 on top of C4 at `1e77e23`.)

- [ ] **Step 2: Run it and watch it fail.** `$PY manage.py test core.tests.test_dead_code_removed.C5RemovedTests`. Expected: `FAILED (failures=1)`: `test_chantry_examples_ajax_endpoint_is_gone`.

- [ ] **Step 3: Implement.**

(a) `locations/views/mage/chantry.py`: delete the whole `class LoadExamplesView(View):` (from its `class` line through `return dropdown_options_response(examples, label_attr="__str__")`). Then run `$RUFF check --fix --select F401 locations/views/mage/chantry.py`. At `1e77e23` plus C4 it removes `from django.views import View`, `from characters.models.core.background_block import Background` and `ChantryBackgroundRating` from the `locations.models.mage.chantry` import. Keep whatever C2 still uses; ruff decides.

(b) `locations/urls/mage/__init__.py`:
```python
from . import ajax, create, detail, index, update
```
becomes
```python
from . import create, detail, index, update
```
and delete the line
```python
    path("ajax/", include((ajax.urls, "mage_ajax"), namespace="ajax")),
```
(c) `git rm locations/urls/mage/ajax.py` (this stages the deletion for the commit).

(d) `core/route_policy_manifest.py`: delete the line `locations.views.mage.chantry.LoadExamplesView` from the `'LOGIN'` group.

- [ ] **Step 4: Run the tests and watch them pass.** `$PY manage.py test core.tests.test_dead_code_removed core.tests.security.test_route_policies locations.tests.views.mage`. Expected: `OK`. Re-run the route-count command: it must print exactly one less than in Step 1 (1833). `$PY scripts/find_dead_code.py --section urls | grep -c load_chantry_examples` must print `0`.

- [ ] **Step 5: Commit.**
```bash
git add locations/views/mage/chantry.py locations/urls/mage/__init__.py core/route_policy_manifest.py \
  core/tests/test_dead_code_removed.py
git commit -F - <<'EOF'
Chantry: delete LoadExamplesView and the Mage location ajax URLs

load_chantry_examples had no caller; its affordability filter now lives
in the chantry points service. The ajax import goes in the same commit
because locations/urls/__init__.py would swallow the ImportError and
drop every Mage location route. Route count: -1.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01QtsFBQPr531MfBmvN3JL23
EOF
```

- [ ] **Unit gate:** run each and require the stated result.
  1. `$PY manage.py test` (serially): 0 failures, 0 errors.
  2. `$PY manage.py check`: `System check identified no issues`.
  3. `$PY manage.py test core.tests.security.test_route_policies`: `OK`.
  4. `$RUFF check locations/models/mage/chantry.py locations/forms/mage/chantry.py locations/views/mage/chantry.py locations/urls/mage/__init__.py core/tests/test_dead_code_removed.py locations/tests/models/mage/test_chantry.py locations/tests/views/mage/`: no new findings (at most the pre-existing `B007` in `ChantryPointForm` if C2 kept that loop); `$RUFF format --check core/tests/test_dead_code_removed.py`: already formatted.
  5. Route count exactly 1 below the count before C5.3; `scripts/find_dead_code.py --section urls` no longer lists `locations:mage:ajax:load_chantry_examples`.

