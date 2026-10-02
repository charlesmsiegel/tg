# Mage chantries

This page explains how a Mage `Chantry` works: its fields and personnel, the point
rules that price its backgrounds and Integrated Effects, the service that spends and
refunds points, the three ways a chantry is created, the seven-step creation wizard,
and submission for approval. It is for developers changing chantry behaviour and for
agents that create or edit chantries. Terms such as Background, Integrated Effects and
Effect are defined in the [glossary](../../docs/reference/glossary.md).

## The model

Source: [`locations/models/mage/chantry.py`](../models/mage/chantry.py).

`Chantry` (`type = "chantry"`, `gameline = "mta"`) extends `BackgroundBlock` and
`LocationModel`.

| Field | Meaning |
|-------|---------|
| `faction` | FK `characters.MageFaction` |
| `leadership_type` | `panel`, `teachers`, `triumvirate`, `democracy`, `anarchy`, `single_deacon`, `council_of_elders`, `meritocracy` |
| `season` | `spring`, `winter`, `summer`, `autumn` |
| `chantry_type` | `exploration`, `ancestral`, `hereditary`, `college`, `squatter`, `war`, `library`, `healing`, `research`, `fortress`, `diplomatic` |
| `total_points` | The points the chantry has to spend |
| `integrated_effects_score` | The Integrated Effects rating, 0–10 |
| `integrated_effects` | M2M `characters.Effect`: the effects bought with that rating |
| `nodes` | M2M `Node` (related name `chantry_nodes`) |
| `chantry_library` | FK `Library` (related name `chantry`) |
| `members`, `leaders`, `investigator`, `guardian`, `teacher` | M2M `characters.Human` (related names `member_of`, `chantry_leader_at`, `investigator_at`, `guardian_of`, `teacher_at`) |
| `ambassador`, `node_tender` | FK `characters.Human` (related names `ambassador_from`, `tends_node_at`) |
| `cabals` | M2M `characters.Cabal` |

The chantry's backgrounds are `ChantryBackgroundRating` rows, reached through
`chantry.backgrounds`. `total_background_rating(property_name)` sums them, and the
`BackgroundBlock` properties (`chantry.allies`, `chantry.resources`...) read it; they are
read-only, since only the points service may change ratings. `node`, `library` and
`sanctum` are not such properties (django-polymorphic's accessors for those location
types hold the names), so call `total_background_rating()` for them. `get_traits()`
returns every allowed background's rating plus `integrated_effects` (the score);
`points_spent()` is `total_cost()`; `has_node()` compares the ranks of `nodes` with the
Node rating; `set_chantry_type()` saves and applies the type's free dots
(`apply_type_grants()`). `rank` is derived from `total_points` and cannot be set.

`get_independent_members()` returns members who belong to none of the chantry's
cabals. `Chantry.cleanup_character_organizations(character)` removes a character from
every chantry role; the module registers it with
`core.utils.CharacterOrganizationRegistry`, so it runs wherever that registry's
cleanup handlers are called.

### `ChantryBackgroundRating`

One purchased background. It inherits `bg` (FK `characters.Background`), `rating`
(0–10), `note`, `url` and `complete` from `core.models.BaseBackgroundRating`, and adds:

| Field | Meaning |
|-------|---------|
| `chantry` | FK `Chantry`, related name `backgrounds` |
| `display_alt_name` | Show the background's alternate name |
| `linked_location`, `linked_character` | The object created for this rating in the wizard: a Node, Library or Sanctum (a location), or an Allies NPC (a character) |

Read and write the link through the `linked_object` property. The getter returns the
concrete (polymorphic) instance or `None`; the setter accepts a `LocationModel`, a
`CharacterModel` or `None` and raises `TypeError` for anything else. Two foreign keys
are needed because `core.Model` is abstract, so there is no single table to point at.

## Point rules

The model defines the prices; the service in
[`locations/services/chantry_points.py`](../services/chantry_points.py) is the only
code that spends or refunds points. Views, forms and templates read the results and
never compute costs themselves.

### Background costs

`Chantry.allowed_backgrounds` lists the backgrounds a chantry may hold. Each dot costs
`trait_cost(property_name)` points:

| Cost per dot | Backgrounds |
|--------------|-------------|
| 2 | `allies`, `arcane`, `backup`, `cult`, `elders`, `library`, `retainers`, `spies`, and Integrated Effects |
| 3 | `node`, `resources` |
| 4 | `enhancement`, `requisitions` |
| 5 | `sanctum` |

Any other name costs 1000, which makes it unaffordable.

`free_dots(property_name)` returns the dots held at no cost. A chantry whose
`chantry_type` is `library` gets `LIBRARY_TYPE_FREE_DOTS` (3) free Library dots; those
dots are also a floor that cannot be refunded.

- `bg_cost(rating)` = `trait_cost × max(0, rating - free_dots)`.
- `total_cost()` = the sum of `bg_cost` over every rating, plus
  `2 × integrated_effects_score`.
- `points` (property) = `total_points - total_cost()`: the points left to spend.

### Funding

`total_points` is written only by the points service: `set_total_points(chantry, total)`
and `add_points(chantry, points)`. `funding_error(chantry, total)` is the rule they
apply: the total must be 0 or more and, on a saved chantry, at least `total_cost()`, so
the balance can never go negative behind the wizard's back. Every form that funds a
chantry goes through them:

| Form | How it funds |
|------|--------------|
| `ChantryCreateForm` (wizard entry) | `set_total_points()` on the unsaved chantry with the entered total |
| `ChantrySelectOrCreateForm`, creating | `set_total_points()` with the character's Chantry background rating |
| `ChantrySelectOrCreateForm`, joining | `add_points()` with that rating, as one atomic `UPDATE` |
| The direct create and update forms | `ChantryFundingMixin.clean_total_points()` asks `funding_error()`; the storyteller cannot lower the total below what is spent |

`rank` follows `total_points`, so funding a chantry is the only way to raise its rank.

### Rank

`rank` is a read-only property computed from `total_points`:

| `total_points` | Rank |
|----------------|------|
| 0–10 | 1 |
| 11–20 | 2 |
| 21–30 | 3 |
| 31–70 | 4 |
| 71 or more | 5 |

### Integrated Effects

`INTEGRATED_EFFECTS_NUMBERS` maps the Integrated Effects score to the effect points it
provides:

| Score | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|-------|---|---|---|---|---|---|---|---|---|---|----|
| Effect points | 0 | 4 | 8 | 15 | 20 | 25 | 35 | 45 | 55 | 70 | 90 |

- `integrated_effects_number()` is the allowance for the current score.
- `spent_integrated_effect_points()` sums `rote_cost` over the chosen effects.
- `current_ie_points()` is the allowance minus the spent points.

An effect can be integrated when its `rote_cost` is positive and at most
`current_ie_points()`, and its `max_sphere` is at most the chantry's rank
(`chantry_points.affordable_effects()`).

## The points service

Source: [`locations/services/chantry_points.py`](../services/chantry_points.py).

Predicates read the chantry as passed. Mutations run inside `transaction.atomic()`,
lock the chantry row with `select_for_update()`, re-check their preconditions against
the locked row and raise `ValidationError` when a rule is broken or the chantry has
been deleted. `MAX_BACKGROUND_RATING` is 5 and `MAX_IE_SCORE` is 10.

| Function | Kind | Behaviour |
|----------|------|-----------|
| `next_dot_cost(chantry, bg, current_rating=None)` | Predicate | 0 below the free floor, otherwise `trait_cost` |
| `background_purchase_error(chantry, bg, *, points=None, current_rating=None)` | Predicate | Why one more dot cannot be bought (not allowed, already at 5, too expensive), or `None` |
| `can_buy_background(chantry, bg)` | Predicate | `background_purchase_error(...) is None` |
| `ie_purchase_error(chantry, *, points=None)` / `can_buy_ie(chantry)` | Predicate | The same for an Integrated Effects dot |
| `affordable_backgrounds(chantry)` | Predicate | `(new, existing)`: allowed backgrounds not yet held, and held ratings, that can take one more dot now |
| `has_affordable_purchase(chantry)` | Predicate | Any background or Integrated Effects dot is affordable |
| `affordable_effects(chantry)` / `has_affordable_effect(chantry)` | Predicate | Effects that fit the remaining effect points and the rank |
| `buy_background_dot(chantry, bg, *, note="", display_alt_name=False)` | Mutation | Creates the rating at 1 or raises the held one; returns the rating |
| `buy_ie_dot(chantry)` | Mutation | Raises `integrated_effects_score`; returns the new score and updates the passed instance |
| `background_removal_error(rating)` | Predicate | Refuses to go below the free floor |
| `remove_background_dot(rating)` | Mutation | Refunds one dot and deletes the rating at 0. A linked Node is removed from `chantry.nodes`, a linked Library is detached from `chantry_library` (and the chantry removed from its containers); the link, note and URL are cleared and `complete` reset, so the wizard asks again. The linked object is never deleted. |
| `ie_removal_error(chantry)` / `remove_ie_dot(chantry)` | Predicate / Mutation | Lowers the score unless the chosen effects would exceed the lower allowance |
| `remove_effect(chantry, effect)` | Mutation | Removes a chosen effect |
| `apply_type_grants(chantry)` | Mutation | For a library-type chantry, creates the Library rating at the floor or raises it to the floor; does nothing for other types |
| `funding_error(chantry, total)` | Predicate | Why `total` cannot be the chantry's `total_points` (negative, or below `total_cost()` on a saved chantry), or `None` |
| `set_total_points(chantry, total)` | Mutation | Sets `total_points` after `funding_error`; on a saved chantry locks and writes the row and updates the instance, on an unsaved one only sets the attribute for the caller to save. Returns the total |
| `add_points(chantry, points)` | Mutation | Adds a non-negative amount with one atomic `UPDATE ... SET total_points = total_points + points` (no read, so concurrent joins never lose points); refuses a vanished chantry. Returns the new total |

## Three ways to create a chantry

| Route | Who | What happens |
|-------|-----|--------------|
| `/locations/mage/create/chantry/` (`locations:mage:create:chantry`, `ChantryBasicsView`) | Any logged-in user | The player names the chantry, sets its details and `total_points` with `ChantryCreateForm`. The view sets `owner` to the user, `status = "Un"`, `creation_status = 1`, calls `apply_type_grants()` and redirects to the chantry, which opens the wizard. This is the chantry's `get_creation_url()` and the menu target. |
| `/locations/mage/create/chantry/direct/` (`locations:mage:create:chantry_direct`, `ChantryCreateView`) | Staff, and Mage storytellers or head storytellers of at least one chronicle | An all-fields form (`chronicle` plus `DIRECT_FORM_FIELDS` in [`views/mage/chantry.py`](../views/mage/chantry.py)), with `ChantryFundingMixin` so `total_points` passes `funding_error()`. `dispatch()` refuses users with no eligible chronicle; `post()` also requires `PermissionManager.user_can_manage_creation()` for the chosen chronicle. The chronicle choices are `direct_create_chronicles(user)`. `apply_type_grants()` runs after saving. |
| The Chantry background step of the Mage-family character wizards (`characters.views.mage.background_views.CharacterChantryBackgroundView`) | The character's player | `ChantrySelectOrCreateForm` either creates a chantry funded with the background's rating (owner = the character's player, chronicle = the character's chronicle, `status = "Un"`, `creation_status = 1`) or adds that rating, through `chantry_points.add_points()`, to one of the player's own unfinished chantries in the same chronicle (`joinable_chantries()`). The character is added to `members`. See [forms](forms.md#chantryselectorcreateform). |

The chantry list page shows a link to the direct form when
`direct_create_chronicles(user)` is not empty (`can_create_directly` in the context).

## The creation wizard

A chantry's `get_absolute_url()` is the polymorphic router `/locations/<pk>/`. For a
`Chantry` the registry's `dispatch_view` sends that request to `ChantryCreationView`,
a `core.views.generic.DictView` keyed on `creation_status`:

| `creation_status` | View | Step |
|-------------------|------|------|
| 1 | `ChantryPointsView` | Buy background and Integrated Effects dots with `ChantryPointForm` |
| 2 | `ChantryIntegratedEffectsView` | Choose or create effects with `ChantryEffectsForm` |
| 3 | `ChantryNodeView` | Detail each Node rating with `NodeForm` |
| 4 | `ChantryLibrarysView` | Detail each Library rating with `LibraryForm` |
| 5 | `ChantryAlliesView` | Detail each Allies rating with `characters.forms.core.linked_npc.LinkedNPCForm` |
| 6 | `ChantrySanctumView` | Detail each Sanctum rating with `SanctumForm` |

The router shows a step only while the chantry's `status` is `Un` or `Rev` and the
user has `EDIT_FULL` on it; a reader with `VIEW_FULL` but no edit right is sent to the
detail page, and anyone else gets a 404. Once `creation_status` passes 6, or the
chantry is submitted or approved, the router renders `ChantryDetailView`. Before any of
this, the generic router checks the `OBJECT_DETAIL` policy, so a user without
`VIEW_FULL` sees only the public projection. All steps use the template
`locations/mage/chantry/locgen.html` and post back to `/locations/<pk>/`.

### Step 1: backgrounds

`ChantryPointForm` offers only what the service allows: the category (`Integrated
Effects`, `New Background`, `Existing Background`) and, chained to it, the backgrounds
from `affordable_backgrounds()`. Saving calls `buy_ie_dot()` or
`buy_background_dot()`. A POST when fewer than 2 points remain (the cheapest purchase)
advances to step 2 instead of buying. The service re-checks the rule under the row lock,
so a purchase it refuses after the form validated (a double click, a chantry deleted
meanwhile) re-renders the step with the service's message rather than failing.

### Step 2: Integrated Effects

`ChantryEffectsForm` selects an existing Effect (limited to `max_sphere <= rank`,
`rote_cost <= current_ie_points()`, not already chosen) or creates one, and adds it to
`integrated_effects`. A POST when no effect points remain advances to step 3.

### Steps 3 to 6: detailing resources

`ChantryBackgroundView` (the base of the four step views) finds the chantry's first
incomplete rating of its background (`node`, `library`, `allies` or `sanctum`):

- With nothing to detail, GET shows the step without a form and POST advances.
- Otherwise, when the form has a `rank` field, it is fixed to the rating (the input's
  `min` and `max` are both set to it). On a valid POST the new
  object takes the chantry's owner and chronicle and `status = "Sub"`, and the rating
  records it: `note` (the object's name), `url`, `linked_object` and `complete = True`.
  When no incomplete rating of that background remains, the chantry advances.

A model form's instance gets the owner and chronicle before it is first saved, so a
library's generated books share them. The node step also adds the new node to
`chantry.nodes`, and the library step sets it as `chantry_library` (`set_library()`,
which also places the library inside the chantry), so `has_node()`, `has_library()` and
the refund service see them.

## Submission and return

Chantries go through the shared approval flow in `core.services.approval`
(see [XP and approvals](../../docs/architecture/xp-and-approvals.md)), which calls two
hooks on the model:

- `submission_errors()` returns the reasons the chantry cannot be submitted yet; the
  approval service refuses submission while the list is not empty, and the object
  actions template tag hides the submit button. The checks are: every wizard step
  finished (`creation_status > 6`); no more points spent than held; no affordable
  background or Integrated Effects purchase left; the chosen effects within the
  allowance; no affordable effect left; every rating an allowed background rated 1–5;
  and every Node, Library, Allies and Sanctum rating `complete`.
- `on_returned_for_revision()` sets `creation_status` back to 1 when a storyteller
  returns the chantry, so the owner re-enters the wizard at step 1.

## Editing an existing chantry

`/locations/mage/update/chantry/<pk>/` (`locations:mage:update:chantry`,
`ChantryUpdateView`) is the all-fields form for storytellers. Its policy is
`OBJECT_ST_WRITE`: the user needs a scoped editor role (admin, head storyteller or
storyteller of the chantry's chronicle) as well as `EDIT_FULL`. Changing
`chantry_type` runs `apply_type_grants()` after saving. The template
`locations/mage/chantry/form.html` must render every field in `DIRECT_FORM_FIELDS`;
a field the template omits is blanked on save.

`ChantryRemoveForm` in [`forms/mage/chantry.py`](../forms/mage/chantry.py) validates
and applies one refund (a background dot, an Integrated Effects dot or an effect)
through the service. No view uses it.

## See also

- [Location models](models.md)
- [Nodes](nodes.md)
- [Location forms](forms.md)
- [Views and URLs](views-and-urls.md)
- [Character creation](../../docs/architecture/character-creation.md)
- [XP and approvals](../../docs/architecture/xp-and-approvals.md)
