# Mage Chantry Creation Flow Design

## Goal

Route and finish the Mage chantry creation wizard that already exists, unrouted, in `locations/views/mage/chantry.py`. The owner treats it as intended product logic, not dead code: Step 1 (dead-code removal) lists it as candidate 5, and this spec records the decision to **wire it up**.

When this ships:

- A player can create a chantry, choose its total points, and spend those points through a wizard that enforces M20 costs and caps.
- The player can undo purchases, and submits the chantry for ST approval only when it is valid.
- A scoped ST can reject the chantry, including for an unreasonable point total. When the ST returns it for revision, the player re-enters the wizard with every purchase kept.
- The Chantry background in the four Mage-family character wizards stops crashing. It feeds this wizard: it creates a player-owned chantry, or adds points to an existing one.

## Owner decisions

These answers were given during brainstorming on 2026-09-25.

| # | Question | Decision |
|---|---|---|
| 1 | How does the character-wizard Chantry background connect to this wizard? | A new chantry created from chargen starts `Un`, is owned by the player and has `total_points` equal to the background rating. The player finishes it in this wizard. "Add to existing" only adds points. |
| 2 | Points added to an **Approved** chantry | They accumulate as unspent points. A scoped ST spends them in the direct edit form. Approval state does not change. |
| 3 | Personnel step (7) | Dropped from the wizard. Personnel is edited by STs in the direct form. |
| 4 | "Create Chantry" entry point | It goes to the wizard. The all-fields direct create form is limited to STs scoped to the chosen chronicle, and to staff. |
| 5 | Who sets `total_points` | The player enters it in Basics, and the wizard makes sure what is spent is valid. The ST can reject a chantry whose total they dislike. This supports player-created chantries staffed mostly by NPCs. |
| 6 | Returned for revision (`Rev`) | Target behaviour: the chantry re-enters the wizard at step 1 with its purchases kept, and a remove-one-dot action lets the player adjust. |
| 7 | Dead or broken `Chantry` methods | Before deleting a model method, check whether it belongs on the detail page. Methods that do are recovered and fixed. |
| 8 | Library-type chantries | A chantry of type `library` gets 3 free Library dots that cannot be removed (the intent of `set_chantry_type`). |
| 9 | `factional_names` | Recovered as the faction-specific term shown on the detail page, e.g. "Hermetic Covenant". |

## Evidence

Everything below was checked at `093e3cc`. Line numbers are approximate.

**The wizard exists but has no route.** It is made up of:
- `ChantryBasicsView` (`chantry.py:176`);
- the steps `ChantryPointsView` (1), `ChantryIntegratedEffectsView` (2), `ChantryNodeView` (3), `ChantryLibrarysView` (4), `ChantryAlliesView` (5) and `ChantrySanctumView` (6);
- the router `ChantryCreationView(DictView)` (`:287`, `chargen_router = True`, `default_redirect = ChantryDetailView`).

Every step redirects to `get_absolute_url()`, which resolves to `locations:location` → `GenericLocationDetailView`. That is the same detail-URL-as-router pattern `GenericCharacterDetailView` uses for characters. Today `"chantry"` maps directly to `ChantryDetailView`. Nothing in `locations/urls/**` or `core/route_policy_manifest.py` names these classes.

**Live defects in code this spec touches:**
- **The four Chantry-background steps crash.** `MageChantryView`, `MtAHumanChantryView`, `SorcererChantryView` and `CompanionChantryView` all read `form.chantry_creation_form` (`mage.py:1080`, `mtahuman.py:792`, `sorcerer.py:914`, `companion.py:684`). `ChantrySelectOrCreateForm` has no such attribute, so the step raises `AttributeError`, which is a 500. No test covers it.
- **Choosing an existing chantry overwrites it.** `GenericBackgroundView.form_valid` rewrites the selected chantry's `owner`, `chronicle` and `status` (`status = "Sub"`).
- **The Mage chargen template has the step at the wrong number.** It renders the Chantry form at `creation_status == 17` and Specialties at 18, but `MageCharacterCreationView` maps Chantry to 20 and Specialties to 21. MtA Human, Sorcerer and Companion line up.
- **The direct edit form wipes fields on save.** `ChantryUpdateView`/`ChantryCreateView` use `chantry/form.html`, whose `{% block prominents %}` is never rendered because the parent defines no such block. As a result:
  - 12 fields in `fields` (faction, leadership_type, season, chantry_type, leaders, members, cabals, ambassador, node_tender, investigator, guardian, teacher) are never shown, so an update POST blanks them;
  - `gauntlet`, `shroud` and `dimension_barrier` are rendered but not in `fields`.
- **Point rules are not enforced.** `ChantryPointForm`:
  - offers every `Background`, not only `allowed_backgrounds`;
  - never checks cost against remaining points, the 5-dot cap or the IE score cap of 10.

  The only affordability filter lives in `LoadExamplesView` (`load_chantry_examples`), which nothing calls.
- **The effects step can get stuck.** `ChantryIntegratedEffectsView` advances only when `current_ie_points() == 0`, so leftover IE points that no effect fits leave the wizard stuck. The JS toggle in `effects_form.html` does the same thing in both branches.
- **Created objects are never attached.** The Node, Library, Allies and Sanctum steps create the object but never attach it to the chantry (`nodes`, `chantry_library`).
- **Step 7 has nothing behind it.** `personnel_form.html` is empty, and `view_mapping` has no key 7.

**Model methods** (receivers verified as `Chantry`):

| Method | State | Disposition |
|---|---|---|
| `points`, `total_cost`, `bg_cost`, `trait_cost`, `integrated_effects_number`, `spent_integrated_effect_points`, `current_ie_points`, `rank`, `get_independent_members`, `cleanup_character_organizations` | live | keep |
| `add_node`, `total_node`, `has_library` | only tests call them; they work | **recover** (wizard steps and detail page) |
| `set_library` | only tests call it; it never saves `chantry_library` | **recover and fix** |
| `has_node` | only tests call it; reads `self.node` (a reverse one-to-one), which raises | **recover and fix**: compare `total_node()` with the Node rating |
| `points_spent` | only tests call it; broken (`self.allies` raises, and it adds M2M managers) | **replace** with a spent-points line built on `total_cost()` |
| `set_chantry_type` | only tests call it; `"library"` raises | **replace** with the Library-type rule in the points service |
| `factional_names` | only tests use it | **recover** (detail subtitle) |
| `ChantryBackgroundRating.display_name` | only tests call it | **recover**: the background block template calls it instead of repeating the logic inline |
| `get_traits`, `set_rank` | broken; superseded by `points`/`total_cost`; `rank` is a read-only property | delete |
| `has_season`/`set_season`, `has_chantry_type`, `has_faction`/`set_faction` | only tests call them; the detail page shows these fields with a "Not specified" default | delete |
| `ChantryPointForm.INTEGRATED_EFFECTS_NUMBERS` | unused duplicate of the model constant | delete |
| `ChantryDetailView` `factions` context | no template reads it | delete |
| `form.html` `prominents` block, `personnel_form.html`, the step-7 block in `locgen.html` | never rendered | delete |
| `LoadExamplesView` and `load_chantry_examples` | routed, no caller | delete (its filtering moves into the points service) |

**Infrastructure this design builds on:**
- The route policy manifest (`core/route_policy_manifest.py`). The `CHARGEN_STEP` policy already means "can fully edit this object, and it is `Un` or `Rev`", and it handles `LocationModel` subjects.
- `PermissionManager.user_has_scoped_editor_role` (staff, head ST, or the ST for this chronicle and gameline).
- `PermissionManager.user_can_manage_creation` (the same check, for the chronicle chosen in a create form).
- `ApprovalService.transition_object` (`Un`/`Rev` → `Sub` → `Rev`).
- The `{% object_actions %}` tag.
- `tg_schema` migrations that add a column only when it is missing (`0001_scene_visibility`).

## Design

### 1. Routing, entry points and access

| URL name | View | Access | Change |
|---|---|---|---|
| `locations:mage:create:chantry` | `ChantryBasicsView` | any logged-in user (`OBJECT_CREATE`) | Replaces `ChantryCreateView` on this name. Sets `owner = request.user`, `status = "Un"` and `creation_status = 1`. Saves once. Redirects to `get_absolute_url()`. |
| `locations:mage:create:chantry_direct` (new) | `ChantryCreateView` | STs scoped to the chosen chronicle (Mage gameline), and staff | `OBJECT_CREATE` in the manifest, plus an in-view check: the POST is refused unless `user_can_manage_creation` passes for the chosen chronicle. The chronicle dropdown lists only chronicles where the user qualifies (all chronicles for staff). A GET from a non-ST is refused. |
| `locations:location` (a chantry's `get_absolute_url`) | `GenericLocationDetailView` → **`ChantryCreationView`** → a step, or `ChantryDetailView` | step: full editor while `Un`/`Rev`; otherwise the detail page | `"chantry"` in `GenericLocationDetailView.view_mapping` switches from `ChantryDetailView` to the router. |
| `locations:mage:detail:chantry` | `ChantryDetailView` | unchanged | Kept as the read-only detail page. |
| `locations:mage:update:chantry` | `ChantryUpdateView` | scoped ST or staff | New manifest policy `OBJECT_ST_WRITE`: the `OBJECT_WRITE` checks plus `user_has_scoped_editor_role`. It closes the owner-edits-`total_points` bypass. `form.html` is fixed to render every field in `fields`, and `fields` and the template agree. |

Manifest entries:
- `ChantryCreationView` → `ROUTER`;
- the six step views → `CHARGEN_STEP`;
- `ChantryBasicsView` → `OBJECT_CREATE`;
- `ChantryUpdateView` → `OBJECT_ST_WRITE` (the policy is added to `core/access_policy.py`);
- `LoadExamplesView` is removed.

`core/tests/security/test_route_policies.py` enforces that the manifest matches the routes exactly, in both directions.

In templates, "Create Chantry" links to the wizard, and a "Create directly" link appears only to users with a scoped ST role or staff. The Edit button on a chantry appears only to scoped STs and staff.

### 2. Point rules, wizard steps and undo

**The points service (`locations/services/chantry_points.py`)** is the single source of cost rules. Each mutation runs in `transaction.atomic()` with `Chantry.objects.select_for_update()` on the row, and re-checks its preconditions after taking the lock. Views, forms and templates never compute costs themselves.

- `can_buy_background(chantry, bg)` is true only when:
  - `bg.property_name` is in `Chantry.allowed_backgrounds`;
  - the current rating is below 5;
  - `trait_cost(bg.property_name)` is no more than `chantry.points`.
- `can_buy_ie(chantry)` is true when `integrated_effects_score < 10` and `chantry.points >= 2`.
- `has_affordable_purchase(chantry)`: any allowed background passes `can_buy_background`, or `can_buy_ie` is true.
- `buy_background_dot(chantry, bg, *, note="", display_alt_name=False)` creates the rating at 1 or increments it. It raises `ValidationError` when not allowed.
- `buy_ie_dot(chantry)`.
- `remove_background_dot(rating)` decrements the rating and deletes it at 0. It is refused below the free-dot floor (see the Library rule). If the rating had a `linked_object`, the service:
  - detaches the object from the chantry (`nodes.remove(node)`, or `chantry_library = None` when it matches);
  - clears `linked_object`, `url` and `note`;
  - sets `complete = False`.

  The object itself is not deleted.
- `remove_ie_dot(chantry)` is refused when `spent_integrated_effect_points()` would exceed the IE total at the new score.
- `remove_effect(chantry, effect)` removes the effect from `integrated_effects`.

**Library-type rule:**
- When a chantry's `chantry_type` is `"library"`, its Library rating has a floor of 3 dots, and those 3 dots cost nothing.
- `bg_cost` counts only the dots above the floor for a library-type chantry.
- `ChantryBasicsView` calls `apply_type_grants(chantry)` after saving, which creates or raises the Library rating to 3. `ChantryUpdateView` calls the same function after an ST changes the type.
- If an ST changes the type away from `library`, the dots stay and become paid; the ST form shows the resulting `points`.
- The 5-dot cap still applies, so at most 2 more Library dots can be bought.

**`ChantryPointForm`:**
- builds its category and example choices from the service predicates, so only affordable, allowed options appear;
- `clean()` calls the same predicates, so a forged POST fails validation;
- `save()` calls the service;
- adds a remove action (a separate small form, POSTing `action=remove` with a rating pk or `ie`), handled by the same step view.

| Step | Continue allowed when | Changes |
|---|---|---|
| 1 Backgrounds | `not has_affordable_purchase()` | A "−" on each background dot and on the IE score. Replaces today's `points < 2` check, which leaves a chantry stuck when everything is capped. |
| 2 Integrated effects | no effect outside `integrated_effects` has `rote_cost <= current_ie_points()` and `max_sphere <= rank` | Effects created or selected here are checked against the remaining IE points on the server. A remove action per bought effect. The JS toggle is fixed. |
| 3 Node, 4 Library, 5 Allies, 6 Sanctum | the existing `GenericBackgroundView` loop finds no incomplete rating of that type | `special_valid_action` stores the created object on `rating.linked_object`. The Node step calls `chantry.add_node(node)`; the Library step calls `chantry.set_library(library)`. |
| after 6 | — | The router falls through to `ChantryDetailView`, which shows Submit (section 3). |

Steps 2–6 show a "Back to point spending" POST action that sets `creation_status = 1` and keeps every purchase. A step with nothing to do already skips itself, so going back and forward is cheap.

`GenericBackgroundView` is shared with characters. The chantry steps only override `special_valid_action` and the new back action; they do not change shared behaviour.

### 3. Submission and revision

`ApprovalService.transition_object` gains two opt-in hooks, called inside its existing locked transaction:

- **Before `→ Sub`:** if the object defines `submission_errors()` and the list it returns is not empty, the service raises `ValidationError("; ".join(errors))`. `ObjectSubmissionView` already turns that into a 400.
- **Before saving `→ Rev`:** if the object defines `on_returned_for_revision()`, the service calls it. The hook returns a list of extra field names, which the service adds to `update_fields`.

Models that don't define these methods behave exactly as before.

`Chantry.submission_errors()` returns one message for each of these failures:
- `creation_status` is 6 or less, meaning the wizard isn't finished (finishing step 6 advances it to 7);
- `points < 0`;
- `has_affordable_purchase()` is true;
- `current_ie_points() < 0`;
- an effect is still affordable;
- a background is not in `allowed_backgrounds`, or its rating is outside 1–5;
- a Node, Library, Allies or Sanctum rating has `complete = False`.

`Chantry.on_returned_for_revision()` sets `creation_status = 1` and returns `["creation_status"]`.

`{% object_actions %}` hides "Submit for approval" when the object has a non-empty `submission_errors()`, and lists the reasons under a "Finish creation first" heading instead.

An approved chantry never enters the wizard. Points that characters add later show on the detail page as "N unspent points", and a scoped ST spends them in the direct form.

### 4. The Chantry background in character creation

The four views collapse into one `CharacterChantryBackgroundView` in `characters/views/mage/background_views.py`. The subclasses `MageChantryView`, `MtAHumanChantryView`, `SorcererChantryView` and `CompanionChantryView` keep their names, so their manifest entries and `view_mapping` keys are unchanged. They set only `primary_object_class` and `template_name`.

**`ChantrySelectOrCreateForm`:**
- `total_points` is no longer a field. The view passes `points = current_background.rating`.
- `clean()` requires `name` when creating and `existing_chantry` when selecting.
- `existing_chantry` is limited to chantries in the character's chronicle, excluding `Ret` and `Dec`.

**`form_valid`** is overridden entirely, not inherited, because the generic version performs the owner and status overwrite. It runs in `transaction.atomic()`.
- **Create:** a new `Chantry` with:
  - `owner = character.owner`;
  - `chronicle = character.chronicle`;
  - `status = "Un"` and `creation_status = 1`;
  - `total_points = rating`.

  Then `apply_type_grants`.
- **Existing:** `select_for_update()` the chantry and add the rating to `total_points`. Owner, chronicle and status are not touched.
- **Both:**
  - `chantry.members.add(character)`;
  - the character's background rating gets `note = chantry.name`, `url = chantry.get_absolute_url()` and `complete = True`;
  - the character's `creation_status` advances, and the view redirects to the character.

The Mage chargen template's Chantry block moves to `creation_status == 20` and Specialties to 21, matching `MageCharacterCreationView`. This is the minimum needed for the step to render. Step 2 of the refactor (chargen step registry) owns renumbering in general.

If a character is later rejected or deleted, the points it contributed stay on the chantry; a scoped ST adjusts them in the direct form. Membership is the only personnel change the design makes; the rest of personnel is ST-only.

### 5. The detail page

`ChantryDetailView` (`detail.html`) gains:
- **a subtitle** with the faction-specific term from `factional_names`, e.g. "Hermetic Covenant". It walks up the faction's parents to the first entry in the table, falls back to "Chantry", and the lookup is a model method with unit tests;
- **a Points line**, "X spent of Y", with "N unspent" when `points > 0`. This replaces `points_spent`;
- **a Resources card** listing:
  - the Nodes, each with its rank, plus `total_node()` against the Node rating and the realised/unassigned status from `has_node()`;
  - the Library, with its book count against its rank from `has_library()`;
  - the Sanctum and the Allies, from `ChantryBackgroundRating.linked_object`;
  - each linked object linking to its own page.

The background block template uses `rating.display_name` instead of repeating the alternate-name logic.

### 6. Schema

`ChantryBackgroundRating.linked_object`:

```python
models.ForeignKey("core.Model", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
```

- It points at the polymorphic base, so it can hold a Node, Library, Sanctum or NPC.
- `locations` has no migration history, so a new migration, `tg_schema/migrations/0002_chantry_rating_linked_object.py`, follows the `0001_scene_visibility` pattern: it introspects the table and calls `schema_editor.add_field` only when the column is missing.
- Fresh test databases get the column from the model.
- No data migration is needed: existing ratings have `NULL`, and the detail page falls back to `note`/`url`.
- The same fallback applies when a linked object is deleted by some other route and `SET_NULL` clears the column. The Resources card then shows the rating as unlinked, with its `note`, and `has_node()`/`has_library()` report it as unrealised. Tests cover a Node deleted after it was linked.

## Testing

TDD: write the failing test first for each behaviour.

- **`locations/tests/services/test_chantry_points.py` (new):**
  - every cost tier;
  - the allow-list;
  - the 5-dot cap and the IE cap of 10;
  - insufficient points;
  - refunds, and a rating deleted at 0;
  - detaching a linked object on removal;
  - refusing an IE removal that would over-commit effects;
  - the Library floor and its free dots;
  - `has_affordable_purchase`;
  - a concurrent double-spend refused (a `TransactionTestCase` with two services racing on the same row, or a sequential test that asserts the re-check after the lock).
- **`locations/tests/forms/mage/test_chantry.py` (exists):**
  - choices contain only affordable, allowed options;
  - forged POSTs fail validation;
  - the IE-effect cost limit.
- **`locations/tests/views/mage/test_chantry.py` (exists), for routing:**
  - an owner of a `Un` chantry at the chantry URL gets the step for its `creation_status`;
  - a non-owner gets the public card or a 404;
  - an `App` chantry shows the detail page;
  - each step's Continue rule, and the Back action.
- **Same file, for access:**
  - a player is refused the direct create and update forms;
  - a scoped ST gets them;
  - the wrong-chronicle ST is refused;
  - staff gets them;
  - `form.html` round-trips every field (a regression test for the blanking bug).
- **`core/tests/services/` (approval):**
  - submit is refused with the reasons listed;
  - a valid chantry submits;
  - returning resets `creation_status`;
  - a model without the hooks is unaffected;
  - the `object_actions` tag hides Submit.
- **`characters/tests/views/mage/`:**
  - step 20 (Mage), 13 (MtA Human, Companion) and 17 (Sorcerer) render (a regression test for the crash);
  - create sets owner, chronicle, `Un`, the points and membership;
  - adding to an existing chantry only increases `total_points` and adds membership, and never changes owner or status;
  - a missing name or selection is a form error.
- **`tg_schema`:** applying the migration adds the column to a table without it, and does nothing when the column exists.
- **`core/tests/security/test_route_policies.py`** stays green.

Every PR runs the full suite serially (`python manage.py test`) before merge. It must show no failures beyond the 5 on `main` recorded in the dead-code spec's *Removal safety* section.

## Rollout

Five PRs, merged in order. Each one can be merged on its own and leaves the suite green. The wizard goes live only once it is fully guarded (PR C4).

| PR | Contents |
|---|---|
| C1 | **Fix the character-wizard Chantry step.** Section 4, including the Mage template renumbering and the crash regression tests. It doesn't depend on the other PRs and fixes a live 500. |
| C2 | **Points service, forms and schema.** Section 2's service, form changes and undo, `linked_object` with its `tg_schema` migration, and the Library rule. Not routed yet. |
| C3 | **Submission and revision hooks.** Section 3 and the `object_actions` change. |
| C4 | **Go live.** Section 1 (routes, manifest, `OBJECT_ST_WRITE`, the `form.html` fix), the step changes from section 2 (Continue rules, linking objects, Back, the JS fix) and section 5 (detail page). |
| C5 | **Chantry cleanup.** Delete the items marked *delete* in the Evidence table, with their tests. The Step 1 dead-code plan schedules this PR (`2026-09-25-dead-code-removal.md`). |

## Non-goals

- A general renumbering of chargen steps or templates (Step 2), or merging duplicate step views across gamelines (Step 3). C1 renumbers only the one Mage block.
- Moving chantry cost tables into a cross-gameline rules layer (Step 4). The points service is written so Step 4 can absorb it.
- htmx or Alpine interactivity (Step 10).
- Player editing of Basics fields (name, description and so on) after creation. Until a later change adds it, an ST edits them in the direct form, or returns the chantry with a note.
- Personnel assignment in the wizard.
- Undoing chargen contributions when a character is rejected or deleted.

## Acceptance criteria

1. A logged-in player can create a chantry, spend its points under M20 costs and caps, undo purchases, attach Nodes, Libraries, Allies and Sanctums, and submit it. Submission is refused, with reasons, until the chantry is valid.
2. A scoped ST can return a chantry for revision. The player lands on step 1 with every purchase kept, can adjust, and can resubmit.
3. Players cannot reach the direct create or update forms. Scoped STs and staff can, and the update form preserves every field.
4. All four Mage-family character wizards complete the Chantry background step without error. Creating makes a `Un` player-owned chantry; joining adds points and membership and nothing else.
5. The chantry detail page shows the faction term, points spent and unspent, and a Resources card built on the recovered model methods.
6. On every PR, the route-policy test and the new tests pass, and the full suite shows no failures beyond the baseline.
