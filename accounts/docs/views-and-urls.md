# accounts views and URLs

This page lists every URL the `accounts` app serves, the view behind it, who may call
it and what it does. Read it before adding an endpoint or changing a permission check.
Sign-up, login and password pages are summarised here and described in full in
[authentication](authentication.md).

Source: [`accounts/urls.py`](../urls.py), [`accounts/views.py`](../views.py) and the
auth routes in [`tg/urls.py`](../../tg/urls.py).

## Access control layers

Each request passes through two layers before and inside the view:

1. **Route policy.** `core.middleware.authorization.AuthorizationMiddleware` looks up the
   view class in [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py).
   Sign-up, login and password reset are `PUBLIC_READ`. Every other `accounts` view is
   `ACCOUNT`, which returns a plain-text `401 Login required` to anonymous callers
   before the view runs. The middleware also answers `404` for a `pk` URL argument that
   is not a positive decimal integer.
2. **The view's own check.** Profile pages compare the profile's user with the caller;
   the action views call `verify_st_for_chronicle`, `ApprovalService`, or
   `game.spending_approval.require_spending_approver`.

`LoginRequiredMixin` is still on the views, so they stay safe if the route policy
changes. See [authorization](../../docs/architecture/authorization.md) for the roles and
permissions these checks use.

## URL table

All names are in the `accounts` namespace and mounted at `/accounts/`.

| Path | Name | View | Method |
|------|------|------|--------|
| `password_reset/` | `password_reset` | `CustomPasswordResetView` | GET, POST |
| `signup/` | `signup` | `SignUp` | GET, POST |
| `login/` | `login` | `CustomLoginView` | GET, POST |
| `profile/<pk>/` | `profile` | `ProfileView` | GET |
| `profile/update/<pk>/` | `profile_update` | `ProfileUpdateView` | GET, POST |
| `scene/<int:scene_pk>/award-xp/` | `scene_xp_award` | `SceneXPAwardView` | POST |
| `scene/<int:scene_pk>/mark-read/` | `mark_scene_read` | `MarkSceneReadView` | POST |
| `approve/<str:object_type>/<int:pk>/` | `object_approval` | `ObjectApprovalView` | POST |
| `submit/<str:object_type>/<int:pk>/` | `object_submission` | `ObjectSubmissionView` | POST |
| `revise/<str:object_type>/<int:pk>/` | `object_revision` | `ObjectRevisionView` | POST |
| `approve-image/<str:object_type>/<int:pk>/` | `image_approval` | `ImageApprovalView` | POST |
| `character/<int:character_pk>/award-freebies/` | `freebie_award` | `FreebieAwardView` | POST |
| `weekly-xp/<int:week_pk>/<int:character_pk>/request/` | `weekly_xp_request` | `WeeklyXPRequestView` | POST |
| `weekly-xp/<int:week_pk>/<int:character_pk>/approve/` | `weekly_xp_approval` | `WeeklyXPApprovalView` | POST |
| `` (empty) | `user` | `RedirectView` to `core:home` | any |

The POST-only views set `http_method_names = ["post"]`, so a GET returns 405.

[`tg/urls.py`](../../tg/urls.py) adds un-namespaced routes under `/accounts/` for the
rest of the password-reset flow and then includes `django.contrib.auth.urls`; see
[authentication](authentication.md#url-routing). Because `accounts.urls` is included
first, the un-namespaced names `login` and `password_reset` resolve to the same paths and
are served by this app's views.

## Pages

### `ProfileView`

`LoginRequiredMixin`, `DetailView` on `Profile`, template `accounts/detail.html`.
`get_object` raises `PermissionDenied` unless the caller is the profile's user or staff.
The context, the tabs and NEEDS YOU are described in
[dashboard](dashboard.md#profile-page).

### `ProfileUpdateView`

`MessageMixin`, `LoginRequiredMixin`, `UpdateView` on `Profile` with
`accounts.forms.ProfileUpdateForm`, template `accounts/form.html`. Same owner-or-staff
rule as `ProfileView`. On success it flashes "Profile updated successfully!" and
redirects to `Profile.get_absolute_url()`; on invalid input it flashes the error message
and re-renders.

## Profile actions

These views share three helpers in `accounts/views.py`:

- `verify_st_for_chronicle(request, chronicle, action_description, gameline=None)`
  raises `PermissionDenied` unless the caller may manage the scope:
  `PermissionManager.can_manage_scope(user, chronicle, gameline, request)` when a
  gameline is given (head ST, a matching `STRelationship`, or staff), otherwise
  `PermissionManager.can_manage_chronicle` (head ST or staff). A `None` chronicle is
  refused for everyone but staff.
- `object_error_redirect(request, object_type, pk, exc)` flashes each message of a
  `ValidationError` and redirects to the object's page.
- `profile_tab_redirect(request, tab)` redirects to the caller's own profile with
  `?tab=<tab>`.

`object_type` must be a key of `core.services.ApprovalService.OBJECT_MODEL_MAP`
(`character`, `group`, `chimera`, `effect`, `location`, `item`, `rote`, `template`) or,
for images, of `IMAGE_MODEL_MAP` (`character`, `location`, `item`). Any other value is a
404.

| View | Who may call it | What it does | Redirect |
|------|-----------------|--------------|----------|
| `ObjectApprovalView` | A scoped ST for the object's chronicle and gameline (`verify_st_for_chronicle`), and `Permission.APPROVE` on the object inside `ApprovalService.approve_object` | Locks the object, requires status `Sub`, sets `App`. For a character, recomputes pooled backgrounds of its groups. A `ValidationError` (not submitted) returns to the object with messages. | Caller's profile |
| `ObjectSubmissionView` | Anyone who can view the object in full and edit it (`VIEW_FULL` and `EDIT_FULL`) | `ApprovalService.transition_object(..., "Sub")`: requires status `Un` or `Rev`, and runs the model's optional `submission_errors()` hook | The object's page |
| `ObjectRevisionView` | `APPROVE` on the object (checked in `transition_object`) | `transition_object(..., "Rev")`: requires status `Sub`, runs the model's optional `on_returned_for_revision()` hook | The object's page |
| `ImageApprovalView` | A scoped ST (`verify_st_for_chronicle`) | `ApprovalService.approve_image`: sets `image_status="app"` | Caller's profile |
| `SceneXPAwardView` | A scoped ST for the scene's chronicle and `Scene.gameline` | Binds `accounts.forms.SceneXP` (prefix `scene_<pk>`) and calls `Scene.award_xp`: 1 XP to each ticked player character, then `xp_given=True`. A second award raises `ValidationError`, reported as "XP was already awarded". | `?tab=experience` |
| `FreebieAwardView` | A scoped ST for the character | `FreebieAwardForm.save()`: `award_backstory_freebies(n)` with 0 to 15 points, which also marks freebies approved. A repeated award (freebies already approved) raises `ValidationError`, reported as a flash message. | Caller's profile |
| `WeeklyXPRequestView` | The character's owner (`char.owner == request.user`, else 403) | `WeeklyXPRequestForm.submit()` creates the request with `finishing=True`. A second request for the same week (a repeated or concurrent POST) is refused with a flash message; the `(week, character)` unique constraint backs the check. | `?tab=experience` |
| `WeeklyXPApprovalView` | `require_spending_approver(user, character)`: `APPROVE` on the character, and no self-approval of an owned player character | Loads the request for `(character, week)` (a pending one first; 404 if none) and calls `WeeklyXPRequestForm.st_save()`, which runs `WeeklyXPRequest.approve()` and adds its XP. An already approved request is reported, not re-applied. | `?tab=experience` |
| `MarkSceneReadView` | Any logged-in user who can read the scene (`game.security.can_view_scene`, else 404) | Creates the user's `UserSceneReadStatus` row if missing and marks the scene read through its latest post | Caller's profile |

`ObjectApprovalView` checks scope at two points on purpose: the view checks the
chronicle and gameline before calling the service, and `ApprovalService.approve_object`
checks `Permission.APPROVE` and the `Sub` status again under a row lock, so a request
that races a status change cannot approve the wrong state. `ImageApprovalView` has only
the view-level check; `ApprovalService.approve_image` does not lock or re-check.

`game` has its own weekly XP pages and approval endpoints that write the same records;
see [game XP](../../game/docs/xp.md).

## Auth views

| View | Base | Notes |
|------|------|-------|
| `SignUp` | `AuthThrottleMixin`, `MessageMixin`, `CreateView` | `CustomUserCreationForm`, template `accounts/signup.html`, redirects to `core:home` |
| `CustomLoginView` | `AuthThrottleMixin`, `LoginView` | `CustomAuthenticationForm`, default template `registration/login.html`; always redirects to the user's profile |
| `CustomPasswordResetView` | `AuthThrottleMixin`, `PasswordResetView` | Page `accounts/auth/password_reset_form.html`, email `accounts/registration/password_reset_email.txt` and `.html` |

All three answer `429` to POSTs past the throttle limit. Details, including the throttle
and why the templates are not under `registration/`, are in
[authentication](authentication.md).

## Adding a profile action

1. Add a `View` subclass with `LoginRequiredMixin` and `http_method_names = ["post"]`.
2. Authorize first: load the object with `get_object_or_404`, then call
   `verify_st_for_chronicle` or a `PermissionManager` check.
3. Do the work in one service or model call; catch its expected exceptions and turn
   them into `messages.error`.
4. Redirect with `profile_tab_redirect` or to the object.
5. Add the dotted view path to the `ACCOUNT` set in
   [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py); an
   unlisted view is denied.
6. Add a test to `accounts/tests/views/test_profile_actions.py`.

## See also

- [Dashboard and profile page](dashboard.md)
- [accounts forms](forms.md)
- [Authorization](../../docs/architecture/authorization.md)
- [XP and approvals](../../docs/architecture/xp-and-approvals.md)
- [URL reference](../../docs/reference/urls.md)
- [`core/services/approval.py`](../../core/services/approval.py)
