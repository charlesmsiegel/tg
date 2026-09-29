# XP, freebies and approvals

This page describes how objects move through their approval status, how storytellers find
and act on what is waiting for them, how characters earn experience (XP), how XP and
freebie points are spent and decided, and who may do each of these things. It is for
developers working on approval, XP or spending code and for agents that need to change it
safely. Character creation itself (the wizard that ends in a submission) is covered in
[Character creation](character-creation.md); roles and permissions in general in
[Authorization](authorization.md).

Terms such as ST (storyteller), freebies and XP are defined in the
[glossary](../reference/glossary.md).

## Status lifecycle

Every polymorphic object (`core.models.Model`: characters, items, locations, groups, rotes,
effects, chimerae, character templates) has a `status` field whose values come from
`core.constants.CharacterStatus`:

| Code | Label | Meaning |
|------|-------|---------|
| `Un` | Unapproved | A draft; the default for new rows |
| `Sub` | Submitted | Waiting for a storyteller |
| `Rev` | Returned for revisions | Sent back to the creator; editable again |
| `App` | Approved | In play |
| `Ret` | Retired | Out of play; can be reactivated |
| `Dec` | Deceased | Final |

For characters the allowed moves are enforced on every save.
`Character.STATUS_TRANSITIONS` in [`characters/models/core/character.py`](../../characters/models/core/character.py)
lists them, `Character.clean()` rejects any other change of `status` with a
`ValidationError`, and `core.models.Model.save()` runs `full_clean()` unless called with
`skip_validation=True`:

```text
Un  -> Sub, Ret
Sub -> Rev, App, Ret
Rev -> Sub, Ret
App -> Ret, Dec
Ret -> App
Dec -> (none)
```

When a character moves to `Ret` or `Dec`, `Character.save()` also calls
`remove_from_organizations()`, which removes it from groups and other organisations through
`CharacterOrganizationRegistry.cleanup_character`.

Other object types have no transition table; the approval endpoints below check the
status they expect themselves.

### Who can change status

| Change | Endpoint | Code path | Rule |
|--------|----------|-----------|------|
| Submit (`Un`/`Rev` -> `Sub`) | `POST accounts:object_submission` (`/accounts/submit/<object_type>/<pk>/`) | `ObjectSubmissionView` -> `ApprovalService.transition_object(..., "Sub")` | `VIEW_FULL` and `EDIT_FULL` on the object; the object's optional `submission_errors()` must return nothing |
| Return for revisions (`Sub` -> `Rev`) | `POST accounts:object_revision` (`/accounts/revise/<object_type>/<pk>/`) | `ObjectRevisionView` -> `transition_object(..., "Rev")` | `VIEW_FULL` and `APPROVE` |
| Approve (`Sub` -> `App`) | `POST accounts:object_approval` (`/accounts/approve/<object_type>/<pk>/`) | `ObjectApprovalView` -> `ApprovalService.approve_object` | ST for the object's chronicle and gameline (`verify_st_for_chronicle`), then `APPROVE` |
| Approve an image | `POST accounts:image_approval` | `ImageApprovalView` -> `ApprovalService.approve_image` | ST for the object's chronicle and gameline |
| Retire (-> `Ret`) | `POST characters:retire` (`/characters/<pk>/retire/`) | `CharacterRetireView` -> `characters.services.status.change_character_status` | Owner, or admin / head ST / chronicle ST for the character |
| Mark deceased (-> `Dec`) | `POST characters:decease` | `CharacterDeceaseView` -> `change_character_status` | Admin / head ST / chronicle ST for the character |

A character built in the chargen wizard is submitted by its final step instead
(`HumanSpecialtiesView.form_valid()` sets `status = "Sub"`); see
[Character creation](character-creation.md#submission-at-the-end).

`object_type` is a key of `ApprovalService.OBJECT_MODEL_MAP`: `character`, `group`,
`chimera`, `effect`, `location`, `item`, `rote`, `template`. Image approval accepts
`character`, `location` and `item` (`IMAGE_MODEL_MAP`). Any other key answers 404.

### `ApprovalService`

[`core/services/approval.py`](../../core/services/approval.py) holds the status changes the
views call:

- `approve_object(model_type, object_id, approver)` locks the row
  (`select_for_update()`) inside a transaction, requires `Permission.APPROVE` for the
  approver (`PermissionDenied` otherwise), requires status `Sub` (`ValidationError`
  otherwise), saves `status = "App"`, and for a character calls
  `update_pooled_backgrounds()` on each of its groups. It returns `(object, message)`.
- `transition_object(model_type, object_id, user, target_status)` handles `Sub` and `Rev`
  only (`ValueError` for anything else). Under a row lock it first requires `VIEW_FULL`,
  so a user who cannot see the object learns nothing about its state. It then applies the
  rules in the table above. Two optional model hooks let a type take part:
  `submission_errors()` returns the reasons a submit must be refused, and
  `on_returned_for_revision()` resets the model's own state and returns extra field names
  to save. `locations.models.mage.chantry.Chantry` implements both.
- `approve_image(model_type, object_id)` sets `image_status = "app"`. It performs no
  permission check; `ImageApprovalView` does that first.

The views turn a `ValidationError` into flash messages on the object's page
(`object_error_redirect`). The same actions render on object pages through
`{% tl_object_actions %}` ([`core/templatetags/object_actions.py`](../../core/templatetags/object_actions.py),
template `core/tl/object_actions.html`): "Submit for approval" when the user has
`EDIT_FULL` and the status is `Un` or `Rev` (or the blocking `submission_errors` list
instead), and "Return for revisions" / "Approve" when the user has `APPROVE` and the
status is `Sub`.

`verify_st_for_chronicle(request, chronicle, action, gameline=None)` in
[`accounts/views.py`](../../accounts/views.py) raises `PermissionDenied` (a 403 page)
unless `PermissionManager.can_manage_scope(user, chronicle, gameline)` is true: staff and
superusers always, otherwise the head ST or a chronicle ST of that chronicle and gameline.
Called without a gameline it requires `can_manage_chronicle` (the chronicle's head ST, or
staff). An object with no chronicle can only be handled by staff.

## Storyteller queues and the dashboard

[`accounts/dashboard.py`](../../accounts/dashboard.py) `ProfileDashboard(profile)` holds the
queries for everything waiting on a user. `Profile` exposes it as `profile.dashboard` and
forwards the common selectors (`profile.characters_to_approve()`,
`profile.freebies_to_approve()`, ...).

| Selector | Returns |
|----------|---------|
| `characters_to_approve()`, `items_to_approve()`, `locations_to_approve()` | Status `Sub` objects in chronicles the user staffs (`pending_approval_for_user`); staff also see objects with no chronicle |
| `rotes_to_approve()` | Submitted rotes in the user's chronicles, mapped to the mages that know them |
| `freebies_to_approve()` | Characters in the user's chronicles with `freebies_approved=False` whose `creation_status` equals their type's `freebie_step` |
| `character_images_to_approve()` (and location, item) | Rows with `image_status="sub"` and an image, in the user's chronicles |
| `xp_requests()` | Finished scenes with `xp_given=False` in the user's chronicles (`Scene.objects.awaiting_xp()`) |
| `get_unfulfilled_weekly_xp_requests()` | `(character, week)` pairs of the user's own non-NPC characters that have no `WeeklyXPRequest` yet |
| `get_unfulfilled_weekly_xp_requests_to_approve()` | `(character, week)` pairs in the user's chronicles with an unapproved `WeeklyXPRequest` |
| `xp_spend_requests()` | Characters in chronicles the user staffs with a pending `XPSpendingRequest` |
| `unread_scenes()` | Scenes the user may see whose read status for them is unread |

`notification_context()` turns these into the navigation badge: a total and a breakdown by
label ("Characters to Approve", "Freebies to Approve", "XP Spend Requests", ...). Player
counts (unread scenes, weekly XP requests to file) apply to everyone; the storyteller counts
are added when `profile.is_st()` is true. The context processor
`accounts.context_processors.notification_count` caches the result per user for 60 seconds
and falls back to zero on any error, so the badge can lag behind the queues.

`ProfileView` (`accounts:profile`, `/accounts/profile/<pk>/`) renders the dashboard. Users
can only open their own profile (staff can open any). `get_needs_you()` evaluates each queue
once so the "Needs you" tab count and body agree; the storyteller queues and their forms
(`SceneXP`, `FreebieAwardForm`, `WeeklyXPRequestForm`) appear only on a storyteller's own
profile. The `?tab=` parameter picks `needs`, `characters`, `experience` and, for
storytellers, `chronicles` or `journals`; without it the page opens on `needs` when
anything waits, else `characters`.

## Earning XP

A character's unspent XP is `Character.xp` (a non-negative integer, enforced by the
`characters_character_xp_non_negative` check constraint). XP arrives in three ways.

### Scene XP

When a scene is finished it enters the scene-XP queue. The ST ticks the player characters
who earned XP on the `SceneXP` form ([`accounts/forms.py`](../../accounts/forms.py), one
checkbox per `scene.characters.player_characters()`) and posts it to
`accounts:scene_xp_award` (`SceneXPAwardView`, ST for the scene's chronicle and gameline).
`Scene.award_xp()` gives 1 XP to each ticked character through
`core.xp_utils.award_xp_atomically`, which locks the scene, refuses with a
`ValidationError` if `xp_given` is already set, locks and updates each character, then sets
`xp_given`. A second submit shows "XP was already awarded".

### Weekly XP

`Scene.close()` marks a scene finished and adds its characters to the `Week` ending on the
Sunday on or after the scene's last post (`get_next_sunday`), creating the week if needed.
For each `(character, week)` pair:

1. The owner files a `WeeklyXPRequest` from their profile (`accounts:weekly_xp_request`,
   `WeeklyXPRequestView`, owner only). `WeeklyXPRequestForm.player_save()` always sets
   `finishing=True`; the player may also claim `learning`, `rp`, `focus` and
   `standingout`, each of which needs a finished scene of that week
   (`WeeklyXPRequest.clean()` and the form's `clean()`).
2. The ST reviews it (`accounts:weekly_xp_approval`, `WeeklyXPApprovalView`), may change
   the categories, and saves. The approver must pass `require_spending_approver` (see
   [Deciding a spend](#deciding-a-spend)). `WeeklyXPRequest.approve()` locks the request,
   raises `ValueError` if it is already approved, sets `approved`, and adds `total_xp()`
   (1 XP per true category) to the character.

The management command `process_weekly_xp` can create the week and a finishing-only
request for every participating non-NPC character, optionally approving them
(`--auto-approve`); see [Management commands](../reference/management-commands.md).

### Story XP

`Story.award_xp(character_awards)` awards story XP (`core.xp_utils.calculate_story_xp`: 1
XP each for `success`, `danger`, `growth` and `drama`, plus `duration`) through the same
`award_xp_atomically` helper, and `accounts.forms.StoryXP` builds a form for it. No view
currently posts that form. `StoryXPRequest` rows have list, detail, create and update
views under `game:` but no award action.

## Spending XP

Spending is a two-stage process: the XP is deducted when the player files the spend, and
the trait changes only when a storyteller approves. A denial refunds the cost.

### Services

[`characters/services/xp_spending/`](../../characters/services/xp_spending/) has one
service class per character type:

- `XPSpendingService` is the base. Subclasses register methods with `@handler("<category>")`
  (for `spend`) and `@applier("<trait_type>")` (for `apply`); the
  `XPSpendingServiceMeta` metaclass gives each subclass its own registries and inherits the
  parent's.
- `HumanXPSpendingService` handles `Attribute`, `Ability`, `Background`,
  `New Background`, `Existing Background`, `Willpower` and `MeritFlaw`. Gameline services
  (`MageXPSpendingService`, `VampireXPSpendingService`, ...) add their own categories.
- `XPSpendingServiceFactory.get_service(character)` picks the class registered for
  `character.type`, falling back to `HumanXPSpendingService`.
- `XPSpendingServiceFactory.locked(character)` is a context manager that opens a
  transaction, re-reads the character with `select_for_update()` and yields a service
  bound to that fresh row, so concurrent spends serialize and see each other's deduction.
  Views spend through `locked()`.

The service contract:

| Method | Effect | Returns |
|--------|--------|---------|
| `spend(category, example=None, value=None, note="", **kwargs)` | Runs the category's handler in a transaction. Handlers compute the cost (`characters.costs`) and call `Character.spend_xp()`, which locks the row, raises `ValidationError` if `xp < cost`, deducts the cost and creates an `XPSpendingRequest` with status `Pending` | `XPSpendResult(success, trait, cost, message, error)`; a `ValidationError` becomes `success=False` |
| `apply(xp_request, approver)` | Runs the applier for `xp_request.trait_type`: raises the trait (usually through `Character.approve_xp_spend()`, which locks the character and the request, refuses a request that is no longer `Pending`, and sets the trait) and marks the request `Approved` with `approved_by` / `approved_at` | `XPApplyResult(success, trait, message, error)`; any exception becomes `success=False` |
| `deny(xp_request, denier)` | Adds the cost back to `character.xp` and marks the request `Denied` | `XPApplyResult` |

### `XPSpendingRequest`

`game.models.XPSpendingRequest` records one spend: `character`, `trait_name` (display
name), `trait_type` (the applier key, such as `attribute` or `new-background`),
`trait_value` (the rating after the spend), `cost`, `approved` (`Pending`, `Approved` or
`Denied`, from `core.constants.XPApprovalStatus`), `created_at`, `approved_at`,
`approved_by`. Its lifecycle:

```text
spend()  -> Pending   (XP already deducted)
apply()  -> Approved  (trait raised)
deny()   -> Denied    (XP refunded)
```

A storyteller who could approve the request may correct its `trait_name`, `trait_type`
and `trait_value` while it is pending (`game:xp_spending_request:update`,
`XPSpendingRequestUpdateView` with `XPSpendingRequestCorrectionForm`). The cost cannot be
changed there, because it was deducted when the request was filed and a denial refunds
exactly that amount. Players cannot edit their requests.

### The Spend XP page

`XPSpendingRequestCreateView` (`game:xp_spending_request:create`,
`/game/xp-spending-request/create/<character_pk>/`) is the general spend page. It requires
`Permission.SPEND_XP` on the character (an owner has it only while the character is `App`)
and, through `OwnerRequiredMixin`, that the user owns the character or is staff.

- The form is `XPSpendForm` (or `MageXPSpendForm` for a Mage) from
  [`game/forms.py`](../../game/forms.py): trait type, trait and, for a merit or flaw, the
  rating. It offers only the rated trait types in `XP_SPEND_TRAIT_TYPES`; the choices come
  from the character's own XP form, which knows what the character can raise and afford.
- Each select carries `hx-get` to the same URL. A GET with a selection re-renders
  `game/xp_spending_request/_spend_fields.html` (fragment kind `xp-spend`) with the next
  select's options and a preview. Without JavaScript, the "Preview" button posts the
  selection back (`preview` in the POST data) and the full page shows the same preview.
- [`game/xp_spend.py`](../../game/xp_spend.py) `preview()` computes the preview by running
  the character's real service `spend()` inside a transaction that is always rolled back,
  so the page shows exactly what the spend would charge. It returns a `SpendPreview`
  (current and new rating, cost, XP left, a pricing note, dot states) or a `SpendRefusal`
  carrying the service's error.
- A real POST calls `xp_spend.spend()`, which spends through
  `XPSpendingServiceFactory.locked()`, flashes "Requested ... A Storyteller will review
  it." and redirects back to the page.

The Mage sheet has its own combined form: `MageXPSpendView` (`characters:mage:spend_xp`,
`/characters/mage/mage/<pk>/xp/spend/`, `Permission.SPEND_XP`) is an `ObjectActionView`
that calls `characters.services.mage_xp.spend_mage_xp()`. That function stores an image,
learns a rote, or spends XP through the locked service, depending on the category.

### Deciding a spend

[`game/spending_approval.py`](../../game/spending_approval.py) is the single place that
approves or denies a spend.

`can_approve_spending(user, character)` is true when the user has `Permission.APPROVE` on
the character (admin, head ST or chronicle ST in its scope), except that nobody approves a
spend on their own character unless that character is an NPC and they are its chronicle's
head ST or an ST. An admin who owns a player character therefore cannot approve its
spends. `require_spending_approver()` raises `PermissionDenied` when the check fails. The
permission context exposes the result to templates as `object_perms.can_approve_spending`.

`decide_spending_request(record_model, character, record_id, approver, decision)`:

1. Accepts only `XPSpendingRequest` or `FreebieSpendingRecord` and the decisions
   `"approve"` / `"deny"` (`ValueError` otherwise).
2. In one transaction, locks the record (it must belong to `character`, else 404) and
   resolves the concrete character with `get_real_instance()`, because the foreign key
   returns the `CharacterModel` base row and the services need subclass methods.
3. Answers 404 if the approver lacks `VIEW_FULL`, then calls
   `require_spending_approver()`.
4. Only after authorization, refuses a record that is no longer `Pending` by raising
   `SpendingAlreadyDecided` (a subclass of `SpendingDecisionError`). Checking under the
   lock makes a double submit or two storytellers deciding at once safe: exactly one
   decision applies.
5. Re-reads the character with `select_for_update()`, because the services save the
   whole character and would otherwise overwrite a concurrent spend's deduction.
6. Calls the XP or freebie service's `apply()` or `deny()`, and raises
   `SpendingDecisionError` if the result is unsuccessful, which rolls the transaction back.

Two endpoints call it:

| Endpoint | View | On success | Already decided |
|----------|------|------------|-----------------|
| `POST characters:xp_request_approve` / `characters:xp_request_reject` (`/characters/<pk>/xp-requests/<request_pk>/approve/` and `/reject/`) | `XPRequestApproveView` / `XPRequestRejectView` (`ObjectActionView`s; `has_permission` is `can_approve_spending`) | Flash the service message, back to the character | Warning flash, back to the character |
| `POST game:xp_spending_request:approve` with `approved=Approved` or `Denied` | `XPSpendingRequestApproveView` | Flash, redirect to the request list | Error flash, redirect to the request list |

The character sheet's Experience section (`characters/tl/xp_history.html`) lists the
spend history with Approve / Reject buttons for users with `can_approve_spending`, and a
"Spend XP" link for a user who can spend and is the owner or staff.

## Freebies

Freebie points are spent once, during character creation, at the workflow's `freebies`
step. The flow is:

1. `Human.freebies` holds the pool (default 15; some types set their own). The character
   waits at the freebie step until a storyteller assigns backstory freebies.
2. The ST uses the "Freebies to Approve" queue and posts `FreebieAwardForm`
   (0 to 15 points) to `accounts:freebie_award` (`FreebieAwardView`, ST for the
   character's chronicle and gameline). `Human.award_backstory_freebies()` locks the row,
   refuses if `freebies_approved` is already set or the amount is out of range, adds the
   amount and sets `freebies_approved = True`. `freebies_approved` is a field of
   `core.models.Model`.
3. The player spends at the chargen step. `FreebieSpendingView` spends through
   `FreebieSpendingServiceFactory.locked(character)`.

[`characters/services/freebie_spending/`](../../characters/services/freebie_spending/)
mirrors the XP services (`FreebieSpendingService`, `@handler` / `@applier`, a factory with
`get_service()` and `locked()`, `HumanFreebieSpendingService` plus gameline services), with
one difference: a freebie `spend()` applies the trait **immediately**, then records a
`FreebieSpendingRecord` (status `Pending`) and deducts the cost. `apply()` only marks the
record `Approved`; `deny()` refunds the cost and makes a best-effort revert of the trait
through the applier's `deny=True` branch before marking the record `Denied`.

`game.models.FreebieSpendingRecord` has the same shape as `XPSpendingRequest` (`trait_name`,
`trait_type`, `trait_value`, `cost`, `approved`, timestamps, `approved_by`).
`decide_spending_request()` accepts it, but no URL currently routes a freebie decision to
it, so records created by chargen stay `Pending`. The `game:freebie_spending_record:`
views (list, detail, create, update) manage the records themselves: create and update
require `Permission.SPEND_FREEBIES` on the character, only pending records can be edited,
and saving a record there does not change the character's pool.

Once `freebies_approved` is set, chargen back navigation is blocked for good, because an
earlier step's change could invalidate the allocation (see
[Character creation](character-creation.md#advancing-and-going-back)).

## Permission summary

| Action | Required |
|--------|----------|
| Submit a draft | `EDIT_FULL` (owner while `Un`/`Rev`; admin, head ST, chronicle ST) |
| Return, approve an object | ST for the object's chronicle and gameline (or staff) with `APPROVE` |
| Approve an image, award freebies, award scene XP | ST for the chronicle and gameline, or staff |
| File a weekly XP request | Owner of the character |
| Approve a weekly XP request, approve or deny an XP spend, correct a pending spend | `can_approve_spending`: `APPROVE`, and not the approver's own player character |
| Spend XP | `SPEND_XP` (owner only while `App`; scoped STs and admins) and, on the Spend XP page, owner or staff |
| Spend freebies in chargen | `SPEND_FREEBIES` plus the `CHARGEN_STEP` route policy (`EDIT_FULL`, status `Un`/`Rev`) |
| Retire | Owner, or admin / head ST / chronicle ST |
| Mark deceased | Admin / head ST / chronicle ST |

Status also limits owners: `PermissionManager._check_status_restrictions` removes an
owner's `SPEND_XP` unless the character is `App`, and their `EDIT_LIMITED`, `DELETE` and
`SPEND_FREEBIES` unless it is `Un` or `Rev`. See [Authorization](authorization.md).

## See also

- [Character creation](character-creation.md)
- [Authorization](authorization.md)
- [Scenes and real-time updates](scenes-and-realtime.md)
- [`accounts` app](../../accounts/README.md)
- [`game` app](../../game/README.md)
- [`characters` app](../../characters/README.md)
