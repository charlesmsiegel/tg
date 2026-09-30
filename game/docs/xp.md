# Experience and spending records

This page is the app-level reference for how the `game` app records experience (XP):
the four ways characters earn it (scene, weekly, story and backstory-freebie awards),
how players spend it through `XPSpendingRequest`, how storytellers decide those
requests, and the `FreebieSpendingRecord` pages. It is for developers changing an award
rule, an approval check or a spending page. The cross-app flow, including the character
sheet side, is in [XP and approvals](../../docs/architecture/xp-and-approvals.md).

The character fields involved live on `characters.models.core.CharacterModel` and its
subclasses: `xp` is the **unspent** pool (spending deducts from it immediately), and
`freebies` / `freebies_approved` hold character-creation points. Terms such as ST and
freebies are in the [glossary](../../docs/reference/glossary.md).

## Earning XP

| Source | Record | Award code | Endpoint |
|--------|--------|------------|----------|
| Scene | `Scene.xp_given` | `Scene.award_xp` | `accounts:scene_xp_award` |
| Weekly | `WeeklyXPRequest` | `WeeklyXPRequest.approve` | `accounts:weekly_xp_approval`, `game:weekly_xp_request:approve`, `game:weekly_xp_request:batch_approve` |
| Story | `Story.xp_given` | `Story.award_xp` | None (see [Story XP](#story-xp)) |
| Backstory freebies | `Human.freebies_approved` | `Human.award_backstory_freebies` | `accounts:freebie_award` |

### Scene XP

A finished scene with `xp_given=False` is in `Scene.objects.awaiting_xp()`. A
storyteller sees it on their profile's Experience tab
(`accounts.dashboard.ProfileDashboard.xp_requests`, limited to their staffed
chronicles) as an `accounts.forms.SceneXP` card: one checkbox per player character
(`scene.characters.player_characters()`).

Posting the card to `accounts:scene_xp_award` requires
`PermissionManager.can_manage_scope(user, scene.chronicle, scene.gameline)`. The form
calls `Scene.award_xp({character: bool})`, which converts each `True` to 1 XP and
calls `core.xp_utils.award_xp_atomically(Scene, pk, xp_map)`:

1. Locks the scene row (`select_for_update`).
2. Raises `ValidationError` (code `xp_already_given`) if `xp_given` is already true;
   the view reports "XP was already awarded" for a double submit.
3. Locks each character with a positive award and adds to its `xp`.
4. Sets `xp_given=True` on the scene.

Unticked characters get nothing, but the scene is still marked awarded.

### Weekly XP

A `Week` is identified by its `end_date` (a Sunday in practice); `start_date` is
`end_date - 7 days` and both ends are inclusive.

**Enrollment.** `Scene.close()` finds the date of the scene's latest post (today if
there is none), takes `get_next_sunday()` of it (the same day if it is a Sunday),
gets or creates the `Week` with that `end_date`, and adds every character in the scene
to `Week.characters`. Marking a scene finished through `SceneUpdateView` does not run
`close()` and enrolls no one.

**Filing.** For each `(character, week)` pair where the user owns the non-NPC character,
the character is enrolled and no request exists,
`ProfileDashboard.get_unfulfilled_weekly_xp_requests` puts a
`game.forms.WeeklyXPRequestForm` on the player's Experience tab. The player ticks the
criteria they claim and picks, for each, a scene from `Week.finished_scenes()` that the
character played in:

| Field | Meaning | Scene field |
|-------|---------|-------------|
| `finishing` | Always set to `True` by `player_save()`; the forms hide it | none |
| `learning` | Learned something | `learning_scene` |
| `rp` | Good roleplay | `rp_scene` |
| `focus` | Pursued the character's focus | `focus_scene` |
| `standingout` | Stood out | `standingout_scene` |

`WeeklyXPRequestForm.clean()` and `WeeklyXPRequest.clean()` both refuse a claimed
criterion without its scene. Two endpoints create a request:

- `accounts:weekly_xp_request` (`WeeklyXPRequestView`): the character's owner only.
- `game:weekly_xp_request:create` (`WeeklyXPRequestCreateView`): the character's owner
  or staff (`OwnerRequiredMixin`). The week page (`game:week:detail`) links it for each
  of the viewer's characters who played that week and have no request yet
  (`characters_to_file`).

Both file through `WeeklyXPRequestForm.submit()`, and both refuse a second request for
the same character and week with a flash message. The unique constraint
`unique_weekly_xp_request` on `(week, character)` (added to existing databases by
`tg_schema` 0010, which removed older duplicates) settles a double submit: the losing
save fails and is reported the same way. `accounts:weekly_xp_approval` loads the pair's
pending request, if any, before an approved one.

**Approval.** `WeeklyXPRequest.approve(xp_data=None)` runs in a transaction: it locks
the row, raises `ValueError` if the request is unsaved or already approved, applies any
criteria and scenes in `xp_data`, sets `approved=True`, then locks the character row
(`select_for_update`) and adds `total_xp()` (the count of true criteria, 1 to 5) to its
`xp`, so a concurrent award or spend is not overwritten. It returns the XP added. The
single-request endpoints report a request approved meanwhile by another storyteller
with a flash message.

| Endpoint | Caller check | Notes |
|----------|--------------|-------|
| `accounts:weekly_xp_approval` | `require_spending_approver(user, character)` | From the storyteller's Experience tab; the ST may change criteria before approving (`WeeklyXPRequestForm.st_save`) |
| `game:weekly_xp_request:approve` | `require_spending_approver` | From the request's detail page; same form, redirects to the week |
| `game:weekly_xp_request:batch_approve` | 1 to 100 decimal ids in `request_ids`; every id must be a pending request the caller can view in full (else a plain `404`), and `require_spending_approver` for each | Approves them as filed, in one transaction. The week page's per-row Approve button posts a single id here. |

The storyteller's queue is
`ProfileDashboard.get_unfulfilled_weekly_xp_requests_to_approve`: unapproved requests
of characters in the user's staffed chronicles.

### Story XP

`Story.award_xp({character: {"success", "danger", "growth", "drama", "duration"}})`
gives each character `duration` plus one point per true category
(`core.xp_utils.calculate_story_xp`) through `award_xp_atomically(Story, ...)`, and sets
`Story.xp_given`. The only caller is `accounts.forms.StoryXP`, which no view or template
uses, so story XP has no page in the running site.

`StoryXPRequest` rows record the same five values per character and story. The
`game:story_xp_request:*` pages list, show, create and edit them, but nothing reads them
to award XP; the admin shows their computed total.

### Backstory freebies

During character creation a storyteller can grant 0 to 15 extra freebie points once the
character reaches its class's freebie step
(`ProfileDashboard.freebies_to_approve`). `accounts:freebie_award` calls
`Human.award_backstory_freebies(n)`, which locks the character, refuses an
already-approved character with `ValidationError`, adds `n` to `freebies` and sets
`freebies_approved=True`. See [accounts views](../../accounts/docs/views-and-urls.md#profile-actions).

## XP spending

### The request

`XPSpendingRequest` records one spend: `trait_name`, `trait_type`, `trait_value` (the
new rating), `cost`, and the decision fields `approved` (`Pending`, `Approved`,
`Denied`), `approved_by` and `approved_at`. The XP is deducted when the request is
created, so a pending request already counts against `xp`. The spend page shows spent
(approved) and pending totals from these rows.

Requests are created only by the character XP services in
[`characters/services/xp_spending/`](../../characters/services/xp_spending/):
`XPSpendingServiceFactory.get_service(character)` picks the service for
`character.type` (falling back to `HumanXPSpendingService`), and its `spend(category,
example, value, note)` prices the trait, deducts the cost and files a pending request.

### The Spend XP page

`game:xp_spending_request:create` (`XPSpendingRequestCreateView`, template
`game/xp_spending_request/form.html`) is linked from the character sheet's XP history.

- **Access.** `Permission.SPEND_XP` on the character, then `OwnerRequiredMixin`
  (owner or staff). For an owner without a storyteller role, `SPEND_XP` holds only
  while the character's status is `App` (see
  [authorization](../../docs/architecture/authorization.md)).
- **Form.** `game.forms.xp_spend_form_class(character)` returns `MageXPSpendForm` for
  a `Mage` and `XPSpendForm` otherwise. Both wrap the character's own XP form
  (`characters.forms.core.xp.XPForm` or `characters.forms.mage.xp.MageXPForm`) with
  `XPSpendFormMixin`, which offers the trait types in `XP_SPEND_TRAIT_TYPES`
  (Attribute, Ability, Background, Willpower, MeritFlaw, Sphere, Arete, Practice) and
  builds only the chosen type's traits and, for a merit or flaw, its ratings. See
  [forms](forms.md#xp-spend-forms).
- **Chaining.** Each select carries htmx attributes (`enable_htmx`) that re-request
  the page by GET with the current selection; the view answers with the
  `game/xp_spending_request/_spend_fields.html` fragment marked `TG-Fragment: xp-spend`.
  Without JavaScript, the "Preview" button posts the selection back.
- **Preview.** `game.xp_spend.preview(character, cleaned_data)` runs the service's
  `spend()` inside a transaction that is always rolled back and reads the request it
  would have created. It returns a `SpendPreview` (trait, current and new rating, cost,
  unspent XP after, a pricing rule sentence and dot states) or a `SpendRefusal` with the
  service's error. Costs are never computed in `game`.
- **Spend.** `game.xp_spend.spend(character, cleaned_data)` runs `spend()` on a
  row-locked, freshly read character (`XPSpendingServiceFactory.locked`), so two
  concurrent spends see each other's deduction. On success the page redirects to
  itself with "Requested ... A Storyteller will review it."

### Deciding a request

Two endpoints decide XP spends, and both call
`game.spending_approval.decide_spending_request`:

| Endpoint | View | Input |
|----------|------|-------|
| `game:xp_spending_request:approve` | `XPSpendingRequestApproveView` | POST `approved=Approved` or `Denied`; anything else is `400` |
| `characters:xp_request_approve`, `characters:xp_request_reject` | `characters.views.core.actions.XPRequestApproveView` / `XPRequestRejectView` | From the character sheet |

`decide_spending_request(record_model, character, record_id, approver, decision)`:

1. Accepts only `XPSpendingRequest` or `FreebieSpendingRecord` and `"approve"` or
   `"deny"` (else `ValueError`).
2. Locks the record, which must belong to `character` (else `Http404`).
3. Resolves the concrete character (`get_real_instance()`); a caller without
   `VIEW_FULL` on it gets `Http404`, so outsiders learn nothing about the record.
4. Calls `require_spending_approver` (else `PermissionDenied`).
5. Raises `SpendingAlreadyDecided` if the record is no longer `Pending`. This check
   runs under the lock and after authorization, so a double submit is reported without
   revealing the record to outsiders.
6. Locks and re-reads the character, then calls the XP (or freebie) service's
   `apply(record, approver)` or `deny(record, approver)`. `apply` dispatches on
   `record.trait_type` to the service's applier, which writes the trait change and
   marks the request approved; `deny` refunds `cost` to `xp` and marks the request
   `Denied`.
7. Raises `SpendingDecisionError` when the service reports failure.

`XPSpendingRequestApproveView` flashes the service message or the error and redirects to
the request list.

### Who may approve

`can_approve_spending(user, character)` is the one rule for every spending and weekly XP
decision, and `core.permission_context` exposes it to templates as
`object_perms.can_approve_spending`:

- The user must hold `Permission.APPROVE` on the character: staff, the chronicle's
  head ST, or an ST with an `STRelationship` for the character's gameline.
- A user may not approve spending on a character they own, unless the character is an
  NPC and they hold the head ST or ST role for it. Staff get no exception for their own
  player characters.

`require_spending_approver` raises `PermissionDenied` when the rule fails.

### Correcting a request

`game:xp_spending_request:update` (`XPSpendingRequestUpdateView`) lets an approver
change `trait_name`, `trait_type` and `trait_value` of a pending request
(`XPSpendingRequestCorrectionForm`). The cost is not editable: it was deducted when the
request was filed and a denial refunds exactly that amount. Players cannot edit their
requests.

## Freebie spending records

`FreebieSpendingRecord` has the same shape as `XPSpendingRequest` and records freebie
points spent during character creation. The character freebie services in
[`characters/services/freebie_spending/`](../../characters/services/freebie_spending/)
create them as the player spends.

The `game:freebie_spending_record:*` pages list and show records the caller may read,
and create or edit a record for a character on which the caller holds
`Permission.SPEND_FREEBIES` (for an owner without an ST role, only while the character
is `Un` or `Rev`). Filing a record goes through
[`game.freebie_records.file_freebie_record`](../freebie_records.py): it locks the
character, refuses a negative cost or one above its `freebies`, deducts the cost and
creates the pending record, as a chargen spend does (a denial refunds `cost`). Editing is
limited to pending records and, like an XP request correction, cannot change the cost
(`FreebieSpendingRecordCorrectionForm`).

`decide_spending_request` accepts `FreebieSpendingRecord`, but no view calls it with
that model.

## Where the queues appear

The profile's NEEDS YOU and Experience tabs collect scene XP awards, weekly requests to
file and to approve, freebie awards and characters with pending XP spends; see
[accounts dashboard](../../accounts/docs/dashboard.md). The week page
(`game:week:detail`) lists the week's requests with batch approval for staff, and the
request list pages (`game:weekly_xp_request:list`, `game:xp_spending_request:list`) are
filtered by `game.security.filter_private_records`.

## See also

- [XP and approvals](../../docs/architecture/xp-and-approvals.md)
- [game models](models.md)
- [game views and URLs](views-and-urls.md)
- [accounts views and URLs](../../accounts/docs/views-and-urls.md)
- [`game/spending_approval.py`](../spending_approval.py), [`game/xp_spend.py`](../xp_spend.py)
- [`core/xp_utils.py`](../../core/xp_utils.py)
