# Dedicated action endpoints (Step 5)

## Intent and compatibility

This implements the Step 5 brief (`docs/code-fixing/05-action-endpoints.md`). As
with Steps 0, 2, 3, 4, 6, 7 and 9, it supersedes the brief's historical
"design only" restriction. After this step, each state-changing action on a
detail page has its own URL, form, permission, transaction and response. A
detail view renders the page and never handles POST.

This design builds on the following upstream designs, all implemented on `main`:

* **Step 0 (authorization):** `core/access_policy.authorize_route` evaluates the
  reviewed `core/route_policy_manifest.py` before dispatch, and
  `PermissionManager` holds the role rules. This step adds one policy family,
  `ACTION`, and does not change who may do what, except where the table of
  defects says so.
* **Step 4 (game rules out of views):** the services and form rules that
  actions call already exist: `decide_spending_request`,
  `XPSpendingServiceFactory.locked`, `learn_rote`, `RoteCreationForm.clean`,
  `SpecialtiesForm`, `Scene.close`/`add_character`/`add_post` and
  `Chronicle.add_scene`. This step adds three small services and changes none
  of the rules.

Out of scope: htmx (Step 10; this step only provides the hook), chargen step
views (routed by the Step 2 registry), scene chat over WebSockets (Step 11),
and schema changes. There are **no migrations**.

## Audit: confirmed and refuted findings (HEAD `cb4f3eb`)

The audit was taken at `c1c509a`. Steps 0 and 4 have since hardened most
branches, so several "Reported" items are gone. Line numbers are current.

| Brief finding | Status now | Evidence |
|---|---|---|
| `MageDetailView.post` binds `MageXPForm` + `RoteCreationForm`, branches on `spend_xp` | **Confirmed** (85 lines now; the Rote ladder moved into `RoteCreationForm.clean` in Step 4) | `characters/views/mage/mage.py:93-177` |
| Spend-XP category sub-branches (Image, Rote, others) | **Confirmed** | `mage.py:140-163` |
| Approve located by searching for the `"Approve"` value | **Confirmed**, now with strict key parsing | `mage.py:95-117` |
| Mage handles Reject, specialties, retire, decease | **Confirmed** | `mage.py:95-166` |
| Mage re-implements approval instead of `XPApprovalMixin` | **Confirmed**. Both now call `decide_spending_request`, but each parses its own button | `mage.py:95`, `core/mixins.py:547` |
| Mage retire/decease skips the owner/`EDIT_FULL` check | **Refuted**: Step 0 added the checks (`mage.py:124-131`) before delegating to `CharacterDetailView.post` | |
| `ApprovalMixin.post` finds the request from a button value | **Confirmed** | `core/mixins.py:530-545` |
| Approve has no `select_for_update`; reject does | **Refuted**: both go through `decide_spending_request`, which locks the pending row | `game/spending_approval.py:47-53` |
| `ApprovalMixin` falls through to a redirect when the parent has no `post` | **Confirmed but unreachable**: every user of the mixin inherits `CharacterDetailView.post` | `core/mixins.py:575-577` |
| Drone, Fomor and Spirit detail views have no `post` | **Refuted**: all three inherit `CharacterDetailView.post`, so retire/decease work. They lack `XPApprovalMixin`, but no template outside Mage renders approve buttons | resolver walk of `GenericCharacterDetailView.view_mapping` |
| `ChronicleDetailView.post` branches on `create_character`/`location`/`item`, then `create_story`/`create_scene` | **Confirmed** | `game/views.py:124-189` |
| Chronicle POST reads raw `name`/`location`/`date_of_scene` | **Refuted**: Step 0 switched to `SceneCreationForm` | `game/views.py:171` |
| `Story.objects.create` not linked to the chronicle | **Confirmed, and preserved**: `Story` has no chronicle field, so linking it needs a schema change | `game/models.py:306` |
| `SceneDetailView.post` branches on `close_scene`, `character_to_add`, `message` | **Confirmed**. `character_to_add` is parsed from raw POST although `AddCharForm` encodes the same rule | `game/views.py:222-280`, `game/forms.py:371` |
| `JournalDetailView.post` finds the entry with a substring match on POST keys | **Refuted**: Step 0 parses `submit_response` as a positive integer scoped to this journal | `game/views.py:318-327` |
| Index "create or list" POSTs use an incomplete map with `get_or_create` | **Refuted** for the security side: all three call `resolve_object_type_url`. The endpoints are still POSTs used as navigation | `characters/views/core/__init__.py:388`, `items/…:70`, `locations/…:43` |

POST handlers the brief did not list, found by `grep "def post("` and a search
for `request.POST` key tests:

| Handler | Kind | Disposition |
|---|---|---|
| `CharacterDetailView.post` (`characters/views/core/character.py:74`) | retire + decease in one handler, reached by every character detail view | **Split** (A3, A4) |
| `accounts.views` × 9 (submission, revision, approval, image, freebies, weekly XP, scene XP, mark read) | Already one URL per action | Unchanged: the model this step follows |
| `game.views.XPSpendingRequestApproveView` | One URL; the decision is a form value (`Approved`/`Denied`) | Unchanged; it gains the "already decided" message (D1) |
| `game.views.WeeklyXPRequestApproveView`, `…BatchApproveView` | One URL each | Unchanged |
| `ChargenBackView`, `NPCProfileCreateView`, `CharacterTemplateQuickNPCView` | One URL each | Unchanged |
| `ChantryPointsView.post`, `ChantryIntegratedEffectsView.post`, `_ChantryCreateView.post` | Chargen steps / create form | Out of scope (Step 2) |
| `DictView.post` | Router | Unchanged; the targets it reaches lose their `post` |
| Vampire, Ghoul and Revenant detail templates | A "specialties" form whose handler ignores it | **Removed** (D4) |

### Defects found

| # | Defect | Action |
|---|---|---|
| D1 | A second Approve on a decided XP request raises `Http404` from `decide_spending_request`, so a double-click shows a 404 page. | **Fixed**: after the permission checks, the service raises `SpendingAlreadyDecided` (a `SpendingDecisionError`), and callers show "already approved/denied". Callers without authority still get the same 404 as before |
| D2 | `mage_xp_form.html` shows Approve/Reject for **Denied** requests (`!= "Approved"`). Clicking them returns a 404. | **Fixed**: buttons show only for `Pending` |
| D3 | The approve/reject buttons sit inside the spend-XP `<form>`, so they submit every spend field too. | **Fixed**: each pending request has its own two small forms |
| D4 | Vampire, Ghoul and Revenant detail templates render a "Choose Specialties" form guarded by `object.needs_specialties`, which only `Mage` defines. It never renders, and its handler would have ignored it. | **Removed** the dead blocks. No behaviour changes |
| D5 | `JournalDetailView.post` allowed an ST response with `EDIT_FULL`, which a player owner has on a draft (`Un`/`Rev`) character. So a player could write their own "ST response". The template already showed the form only for `can_approve`. | **Fixed**: the response endpoint requires `APPROVE` on the journal's character (the scoped ST rule the template uses) |
| D6 | `JournalDetailView.post` rendered the page from the POST, so a refresh re-submitted the entry. | **Fixed**: post/redirect/get |
| D7 | `CharacterDetailView.post` handles `retire` and `decease` in one request. A crafted POST with both runs App→Ret and then Ret→Dec, which fails model validation with a 500. An invalid transition is otherwise ignored silently. | **Fixed**: one action per request; an invalid transition shows an error message |
| D8 | `ApprovalMixin` and Mage redirect to `characters:character`, the generic router. For an approved Vampire, Ghoul, Demon, Thrall or DtF Human, that router's `default_redirect` is `django.views.generic.DetailView`, which has no route policy, so it returns **403**, even to staff. | **Fixed** at the action boundary: actions redirect to `object.get_absolute_url()`, the type's own detail route. `ActionRedirectTargetTests` pins both facts: the generic URL still returns 403, and retiring lands on a 200 page. The router defect is reported, but not fixed here, because Step 2 owns the routers |
| D9 | Chronicle creation (`create_character`/`create_location`/`create_item`) and the index pages use POST, with a CSRF token, for pure navigation. | **Fixed**: GET forms to one typed redirect endpoint |
| D10 | `ChronicleDetailView.post` re-rendered the page with a fresh, unbound form when story or scene input was invalid, so the errors were lost. | **Fixed**: the action re-renders the chronicle page with the bound form |

## The action base class

`core/actions.py`:

```python
class ActionFailed(Exception):
    """A service refused the action. The message is shown to the user."""

class ObjectActionView(View):
    http_method_names = ["post"]
    model = None                # subject model; polymorphic managers return the real class
    pk_url_kwarg = "pk"
    permission = None           # Permission checked on the subject (or override has_permission)
    form_class = None           # optional; bound to request.POST / request.FILES
    lock = False                # re-read the subject with select_for_update inside the transaction
    success_message = ""        # formatted with object=
    host_view_class = None      # detail view that re-renders on invalid input (optional)
    host_form_context_name = "form"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()          # 404: missing
        self.authorize()                         # 404: hidden, 403: visible but not allowed
        form = self.get_form()
        if form is not None and not self.is_valid(form):
            return self.form_invalid(form)       # nothing written
        try:
            with transaction.atomic():
                if self.lock:
                    self.object = self.lock_object(self.object)
                result = self.perform(form)
        except (ActionFailed, ValidationError) as exc:
            return self.action_failed(exc, form)
        return self.action_succeeded(result)
```

| Hook | Default | Overridden by |
|---|---|---|
| `get_queryset()` | `model._default_manager.all()` | scene/journal (`select_related`) |
| `get_permission_subject()` | `self.object` | journal actions (the character), XP decision (the character) |
| `can_see(subject)` | `VIEW_FULL` on the subject | scenes (`can_view_scene`), journals (`can_read_private_record`), chronicles (`readable_chronicles`) |
| `has_permission(subject)` | `user_has_permission(user, subject, self.permission)` | retire (owner or scoped editor), decease (scoped editor), approve (`can_approve_spending`), scene actions |
| `is_valid(form)` | `form.is_valid()` | Mage spend (also validates the rote form) |
| `perform(form)` | abstract | every action: exactly one service or model call |
| `lock_object(obj)` | `type(obj)._default_manager.select_for_update().get(pk=obj.pk)` | |
| `get_success_url(result)` | `self.object.get_absolute_url()` | scene creation (the new scene) |
| `get_failure_url()` | `get_success_url(None)` | |
| `fragment_response(result=None, form=None, error=None)` | `None` | **Step 10's hook** (see below) |

**Order of checks.** Visibility comes first, then permission, then form
validation, then the service. Step 0 requires that a caller without read
access gets the same 404 for an existing ID as for a missing one, before any
form validation or side effect.

**Transactions and locking.** `perform()` always runs inside
`transaction.atomic()`. Actions whose service already locks (spending
decisions, XP spending, rote learning) leave `lock = False`, so the row is not
locked twice. Status transitions and scene closing set `lock = True`: they
re-read the row with `select_for_update()` and re-check their state rule
under the lock. On SQLite `select_for_update` is a no-op; on PostgreSQL it is
a row lock.

**Result mapping.** `perform()` returns a result object with `success`,
`message` and `error` (`ServiceResult`, `XPSpendResult`), a model instance, or
`None`. A result with `success=False` is turned into `ActionFailed(error)`.
Success flashes `result.message`, or else `success_message`, and redirects.
`ActionFailed` and `ValidationError` roll back the transaction, flash the error
and redirect to the failure URL. When a host view is configured, they instead
re-render the host with the bound form and the error attached. Other
exceptions propagate.

**Invalid input.** With `host_view_class` set, `form_invalid` re-renders
that detail page with the bound form as `TemplateResponse(status=200)`. That
keeps the old Mage behaviour of showing field errors in place, and lets
`AuthorizationMiddleware.process_template_response` add `object_perms` as it
does for the page itself. Without a host view, it flashes each error and
redirects (post/redirect/get). A forged foreign key, such as a character from
another chronicle, is a form error. It writes nothing and returns 302 with
the error message, where the old handlers returned 403. The authorization of
the **actor** stays a 403.

**htmx hook (Step 10).** The success, failure and invalid paths each call
`fragment_response(...)` first and use its return value when it is not `None`.
The base returns `None`. Step 10 overrides it on the actions it converts,
typically `if request.headers.get("HX-Request"): return
TemplateResponse(request, fragment_template, ctx)`. The authorization, form
and service path does not change, so a fragment can never bypass a check.

### Route policy `ACTION`

`core/access_policy.py` gains one family, and every action class is listed
under it in `core/route_policy_manifest.py`:

```python
if policy == "ACTION":
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])                   # 405, before any lookup
    if not request.user.is_authenticated:
        return HttpResponse("Login required", status=401, ...)    # same as LOGIN
    return None                                                   # the class authorizes the object
```

The route policy is the method and login gate that applies to every action.
The object rule stays next to the action, as `permission` or
`has_permission`, where a reviewer reads it together with the service call.
This matches how the `ACCOUNT` endpoints work today. The route-manifest test
still fails on any action class without a declaration.

## Action inventory

"Visible" means the `can_see` rule; failing it returns 404. "Scoped editor"
means `PermissionManager.user_has_scoped_editor_role` (staff, head ST, or an
ST with the matching chronicle and gameline).

### Characters (`characters/views/core/actions.py`, `characters/views/mage/actions.py`)

| # | Old handler / branch | New endpoint (name) | Form | Permission | Service | Response |
|---|---|---|---|---|---|---|
| A1 | `ApprovalMixin.post` "Approve"; `MageDetailView.post` "Approve" | `POST /characters/<pk>/xp-requests/<request_pk>/approve/` (`characters:xp_request_approve`) | none | visible = `VIEW_FULL` on the character; `can_approve_spending` (scoped ST; NPC-only self-approval) | `decide_spending_request(XPSpendingRequest, character, request_pk, user, "approve")` (locks the request row) | 302 to `character.get_absolute_url()` + message; already decided → warning (D1); unknown request → 404 |
| A2 | same, "Reject" | `…/xp-requests/<request_pk>/reject/` (`characters:xp_request_reject`) | none | as A1 | same with `"deny"` | as A1 |
| A3 | `CharacterDetailView.post` `retire`; Mage delegate | `POST /characters/<pk>/retire/` (`characters:retire`) | none | visible; owner **or** scoped editor | `change_character_status(character, "Ret")` (`lock = True`; transition re-checked under the lock) | 302 + message; invalid transition → error (D7) |
| A4 | same, `decease` | `POST /characters/<pk>/decease/` (`characters:decease`) | none | visible; scoped editor | `change_character_status(character, "Dec")` | as A3 |
| A5 | `MageDetailView.post` `specialties` | `POST /characters/<pk>/specialties/` (`characters:add_specialties`) | `SpecialtiesForm` (fields optional, as before) | visible; `EDIT_FULL` (unchanged) | `record_specialties(character, cleaned_data)` | 302 + message |
| A6 | `MageDetailView.post` `spend_xp` (Image / Rote / other categories) | `POST /characters/mage/mage/<pk>/xp/spend/` (`characters:mage:spend_xp`); `model = Mage`, so other types get a 404 | `MageXPForm`, plus `RoteCreationForm` when category is `Rote` | visible; `SPEND_XP` (unchanged) | `spend_mage_xp(mage, cleaned_data, rote_data)`, which calls exactly one of: set image, `learn_rote`, `XPSpendingServiceFactory.locked(...).spend(...)` | 302 + message; invalid or refused → re-render `MageDetailView` with the bound forms (as before) |

### Game (`game/actions.py`)

| # | Old handler / branch | New endpoint (name) | Form | Permission | Service | Response |
|---|---|---|---|---|---|---|
| G1 | `SceneDetailView.post` `close_scene` | `POST /game/scene/<pk>/close/` (`game:scene_close`) | none | visible = `can_view_scene`; `can_manage_scope(scene.chronicle, scene.gameline)` | `scene.close()` (`lock = True`; already finished → "already closed" message) | 302 to the scene |
| G2 | `SceneDetailView.post` `character_to_add` | `POST /game/scene/<pk>/characters/` (`game:scene_add_character`) | `AddCharForm` (same chronicle; own characters unless scope ST; not already present) | visible; scene not finished (403) | `scene.add_character(character)` | 302 + message; invalid choice → error message, nothing written |
| G3 | `SceneDetailView.post` `message` (and the chat's no-socket fallback) | `POST /game/scene/<pk>/posts/` (`game:scene_post`) | `PostForm` (the user's characters in this scene and chronicle) | visible; not finished; the user owns a character in the scene (403) | `scene.add_post(character, display_name, straighten_quotes(message))`; `ValueError` → `ActionFailed` | 302 + message |
| G4 | `JournalDetailView.post` `submit_entry` | `POST /game/journal/<pk>/entries/` (`game:journal_add_entry`) | `JournalEntryForm` | visible = `can_read_private_record`; owner of the journal's character (403) | `journal.add_post(date, message)` via `form.save()` | 302 to the journal (D6) |
| G5 | `JournalDetailView.post` `submit_response` | `POST /game/journal/<pk>/entries/<entry_pk>/response/` (`game:journal_respond`) | `STResponseForm(prefix="entry-<pk>")` | visible; `APPROVE` on the character (D5); entry must belong to this journal (404) | `form.save()` (sets `entry.st_message`) | 302 to the journal |
| G6 | `ChronicleDetailView.post` `create_story` | `POST /game/chronicle/<pk>/stories/` (`game:chronicle_create_story`) | `StoryForm` | visible = `readable_chronicles`; `can_manage_chronicle` | `form.save()` | 302 to the chronicle; invalid → re-render the chronicle page with the bound `story_form` |
| G7 | `ChronicleDetailView.post` `create_scene` | `POST /game/chronicle/<pk>/scenes/` (`game:chronicle_create_scene`) | `SceneCreationForm(chronicle, user)` | visible; `can_manage_chronicle` or any `STRelationship` in the chronicle; then `can_manage_scope(chronicle, gameline)` for the chosen gameline (403) | `chronicle.add_scene(name, location, date_of_scene=…, gameline=…)` | 302 to the new scene; invalid → re-render with the bound `form` (D10) |

### Navigation (`core/views/object_type_redirect.py`)

| # | Old handler | New endpoint | Decision |
|---|---|---|---|
| N1 | `CharacterIndexView.post` (`create`, `create_group`) | `GET /types/character/create/?char_type=&gameline=` and `GET /types/group/create/?group_type=&gameline=` (`core:object_type_redirect`) | **A single typed GET endpoint.** Choosing a type to create is navigation: it writes nothing, so it needs no CSRF token or POST. The endpoint validates `kind` and `action` against fixed sets and resolves the type only through `resolve_object_type_url`, which is Step 0's seeded-`ObjectType`/registry lookup, so it never trusts a route name from input. An unknown type returns 404. `create` requires login: the view redirects to login, which `AuthErrorHandlerMiddleware` turns into the project's 401. `list` is public |
| N2 | `ItemIndexView.post` | `GET /types/item/create/?item_type=&gameline=` | as N1 |
| N3 | `LocationIndexView.post` | `GET /types/location/create/?loc_type=&gameline=` | as N1 |
| N4 | `ChronicleDetailView.post` `create_character` / `create_location` / `create_item` | the same endpoint, from the chronicle page's three forms | as N1. The character form now also sends its gameline, as the index form already did |

Plain links would not work: the type is chosen in a `<select>`, and a
link-per-type list would duplicate the registry menus. The query-parameter
names stay the existing form field names (`char_type`, `group_type`,
`item_type`, `loc_type`). The chained-select JavaScript keeps working
unchanged.

After this step, `POST` to any character, scene, journal or chronicle detail
URL, or to an index page, returns **405**. The views have no `post`, and
`DictView.post` forwards to a target without one.

## Services added

| Service | Signature | Notes |
|---|---|---|
| `characters/services/status.py` | `change_character_status(character, target) -> ServiceResult` | Caller holds the lock. It checks `STATUS_TRANSITIONS`, then `save(update_fields=["status"])`. Returns `success=False` with "Cannot mark …" for an invalid transition |
| `characters/services/specialties.py` | `record_specialties(character, cleaned_data) -> ServiceResult` | The body of `MageDetailView.add_specialties`: `get_or_create` each named `Specialty` for the stat keys the form allowed, then add it. Unchanged rule |
| `characters/services/mage_xp.py` | `spend_mage_xp(mage, cleaned_data, rote_data=None) -> result` | The category dispatch that was in the view. Each branch is exactly one existing call |
| `game/spending_approval.py` | `SpendingAlreadyDecided(SpendingDecisionError)` | Raised after the visibility and approver checks when the record is not `Pending` (D1) |

## Templates

| Template | Change |
|---|---|
| `characters/core/character/display_includes/buttons.html` | Two forms, `action="{% url 'characters:retire' object.pk %}"` and `…decease…`, still shown by `can_retire`/`can_decease`. **Every character detail page** includes this through `characters/core/character/detail.html`, so every type (including Drone, Fomor, Spirit, Autumn Person, Earthbound, Hunter, Mummy) offers exactly the actions its generic endpoints accept |
| `characters/mage/mage/mage_xp_form.html` | Request history moves out of the spend form. Each `Pending` row has two one-button forms pointing at A1/A2, shown when `object_perms.can_approve_spending` (D2, D3). The spend form posts to `characters:mage:spend_xp` |
| `characters/mage/mage/detail.html` | The specialties form posts to `characters:add_specialties` |
| `characters/vampire/{vampire,ghoul,revenant}/detail.html` | Dead specialties blocks removed (D4) |
| `game/scene/detail.html` | Post, add-character and close forms get their own `action`. The WebSocket fallback's `postForm.submit()` follows the form's action |
| `game/journal/detail.html` | The entry form posts to G4. Each response form posts to G5 for its entry; the field name `entry-<pk>-st_message` is unchanged |
| `game/chronicle/display_includes/{scenes,characters,locations,items}_section.html` | Scene and story forms post to G7/G6. The character, location and item forms become `method="get"` to N4 (no CSRF token) |
| `characters/index.html`, `characters/charlist.html`, `items/index.html`, `locations/index.html`, `core/public_object_list.html` | Creation forms become `method="get"` to the typed endpoint; the hidden or button `action` field is removed |

**Forms that submitted several intents at once.** Only one did: the Mage XP
form, where Approve/Reject rode along with every spend field. It is split
into one spend form and one small form per pending request. Every other page
already had one `<form>` per intent that shared a URL. Those forms keep their
fields and only change `action`.

## Retire, decease and approval on every character type

* **Retire/decease:** one pair of generic endpoints on `Character`. The
  buttons are in the base character detail template, and the flags come from
  `CharacterDetailView.get_context_data`. Both are therefore uniform across
  all 44 mapped character types, and the endpoints enforce the same rule the
  flags show. A test iterates `GenericCharacterDetailView.view_mapping`,
  creates each type, and asserts that staff can retire and decease it
  (App→Ret, App→Dec) and that the owner can retire it. Three types (Autumn
  Person, Inanimae, Nunnehi) cannot be saved at all without their chargen
  choices. For those, the test asserts that the action reports the model
  error instead of failing with a 500.
* **Approval:** one pair of generic endpoints on `Character`. `XPApprovalMixin`
  and `ApprovalMixin` are deleted, and so are the 25 base-class mentions.
  Only Mage renders per-request buttons on the sheet. Every other type is
  approved from the XP spending request pages (`game:xp_spending_request:*`),
  which already call the same service. The new endpoints accept any
  character type, so no page offers an action that does not work.

## Tests

1. **Base class** (`core/tests/test_actions.py`): GET, PUT and HEAD return 405
   before any lookup. Anonymous POST returns 401. A missing or hidden object
   returns 404, and a visible one without permission returns 403. An invalid
   form writes nothing. `ActionFailed` rolls back a partial write. A
   non-`None` `fragment_response` short-circuits all three paths.
2. **Per-action permission matrix**, for every action A1–A6 and G1–G7:
   owner, other player, ST of this chronicle (matching gameline), ST of
   another chronicle, and anonymous. Each case asserts the status and that
   the database is unchanged after a denial. Staff and a wrong-gameline ST
   are added where the rule distinguishes them.
3. **GET rejected:** each action URL returns 405 on GET, for both anonymous
   and logged-in users.
4. **Approve idempotency and double submit:** approving the same request
   twice applies the spend once. The second response is 302 with an "already"
   message, the XP balance and the `XPSpendingRequest` state are unchanged,
   and there is one `approved_by`. Reject after approve does not un-apply the
   spend. A request of another character returns 404. PC self-approval
   returns 403, and NPC self-approval by a scoped ST succeeds.
5. **Old URLs:** POST to each old detail URL with the old button name returns
   405 and changes nothing.
6. **Every character type:** the retire/decease walk described above.
7. **Navigation:** every configured kind resolves; an unknown type returns
   404; anonymous `create` returns 401; a POST returns 405.
8. **Guard** (`core/tests/test_action_guard.py`): an AST scan fails if a view
   module under the six apps tests a POST key, or compares a POST value,
   to choose a branch (`"x" in request.POST`, `request.POST.values()`,
   `request.POST.keys()`, `"x" in form.data`). A resolver walk fails if a
   `DetailView` reachable from the URLconf defines `post`. Both fail at
   `cb4f3eb`, and both pass after this step.

Existing tests that posted to the old URLs are moved to the new endpoints.
They keep their assertions except where a defect above changes the outcome
(D1, D5, D7, and forged foreign keys becoming form errors).

## PR slicing (implemented here as ordered commits in one PR)

1. **Approval (security-adjacent first):** `ObjectActionView`, the `ACTION`
   policy, A1/A2, `SpendingAlreadyDecided`, the Mage history template (D1–D3).
   Delete `ApprovalMixin`/`XPApprovalMixin` and Mage's inline approval.
2. **Retire/decease:** A3/A4, the status service, `buttons.html`; delete
   `CharacterDetailView.post`.
3. **Mage sheet:** A5/A6, the specialties and Mage-XP services; delete
   `MageDetailView.post`; remove the dead Vampire-family blocks (D4).
4. **Scene:** G1–G3; delete `SceneDetailView.post`.
5. **Journal:** G4/G5 (D5, D6); delete `JournalDetailView.post`.
6. **Chronicle:** G6/G7 and the chronicle's navigation forms (D10); delete
   `ChronicleDetailView.post`.
7. **Index navigation:** the typed GET endpoint; delete the three index `post`
   methods (D9).
8. **Guard test and implementation record.**

Each slice removes one old handler, adds its endpoints and moves its
template, so reverting any one slice restores that handler alone. Slice 1's
base class is the only shared code.

