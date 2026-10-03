# Permissions and route policies

This page is the reference for how the project decides who may see or change what: the
roles and permissions in [`core/permissions.py`](../permissions.py), the per-route policy
evaluated by [`core/access_policy.py`](../access_policy.py) and
[`core/middleware/authorization.py`](../middleware/authorization.py), and the
capability snapshot that templates read. Read it before you add a view, change an access
rule or render an action button. For the concepts across apps, see
[Authorization](../../docs/architecture/authorization.md).

## Two layers

Access is checked twice, for different questions:

1. **Route policy** (before the view runs). Every project view has exactly one policy
   name in [`route_policy_manifest.py`](../route_policy_manifest.py). The middleware
   evaluates it: login required, staff only, POST only, "must be able to edit this
   object", and so on. A view with no policy is refused with `PermissionDenied`.
2. **Object permission** (inside the view, the mixin or the service).
   `PermissionManager` answers "does this user hold permission P on this object?" from
   the user's roles and the object's status.

The route layer lives in middleware so that a view which forgets a mixin is still
protected, and so that every route can be listed and tested in one place
([`core/tests/security/test_route_policies.py`](../tests/security/test_route_policies.py)).
The object layer is where the actual rules live; the route layer calls it.

## Roles

`PermissionManager.get_user_roles(user, obj, request=None)` returns a set of `Role`
values for one user and one object.

| Role | Granted when |
|------|--------------|
| `ANONYMOUS` | The user is not authenticated (the only role they get) |
| `AUTHENTICATED` | Every signed-in user |
| `ADMIN` | `user.is_staff` or `user.is_superuser` |
| `OWNER` | `obj.owner_id == user.pk` or `obj.user_id == user.pk` |
| `CHRONICLE_HEAD_ST` | The user is the head storyteller (`Chronicle.head_st`) of the object's chronicle |
| `GAME_ST` | The user is in the chronicle's `game_storytellers` |
| `CHRONICLE_ST_VIEW` | The user has any `game.STRelationship` in the object's chronicle |
| `CHRONICLE_ST` | The user has an `STRelationship` in that chronicle whose gameline name matches the object's gameline (via `settings.GAMELINES[code]["name"]`) |
| `PLAYER` | The user owns any character in the object's chronicle |
| `OBSERVER` | An `Observer` row links the user to this object (content type and pk) |

The object's gameline comes from its `gameline` attribute, or `get_gameline()`. For a
record that is not a `core.models.Model` but has a `character` attribute (XP requests,
journals), `PermissionManager.permission_subject()` uses that character instead, so the
record inherits the character's roles. Polymorphic base rows are resolved to their
concrete class once per request (`_real_subject`).

`get_scoped_roles(user, chronicle, gameline, request=None)` computes the same
storyteller roles for a chronicle and gameline pair without an object (used for creation
pages and chronicle-level actions).

## Permissions

`Permission` values and the roles that grant them (`ROLE_PERMISSIONS`):

| Permission | OWNER | ADMIN | HEAD_ST | CHRONICLE_ST | CHRONICLE_ST_VIEW | GAME_ST | PLAYER | OBSERVER |
|------------|:-----:|:-----:|:-------:|:------------:|:-----------------:|:-------:|:------:|:--------:|
| `VIEW_FULL` | yes | yes | yes | yes | yes | yes | | |
| `VIEW_PARTIAL` | yes | yes | yes | yes | yes | yes | yes | yes |
| `EDIT_FULL` | drafts only | yes | yes | yes | | | | |
| `EDIT_LIMITED` | yes | yes | yes | yes | | | | |
| `SPEND_XP` | yes | yes | yes | yes | | | | |
| `SPEND_FREEBIES` | yes | yes | yes | yes | | | | |
| `DELETE` | yes | yes | yes | yes | | | | |
| `APPROVE` | | yes | yes | yes | | | | |
| `MANAGE_OBSERVERS` | yes | yes | yes | yes | | | | |

`AUTHENTICATED` and `ANONYMOUS` grant nothing. A user's permissions are the union over
all their roles.

"Drafts only": `OWNER` does not hold `EDIT_FULL` in the matrix, but
`user_has_permission` grants it when the object's status is `Un` or `Rev`. This is how a
player edits their own character during creation and after it is returned for revisions.

### Status restrictions

When `status_aware=True` (the default) and the object has a `status`,
`_check_status_restrictions` narrows the result. Roles `ADMIN`, `CHRONICLE_HEAD_ST` and
`CHRONICLE_ST` ("scoped editors") are exempt from the owner rules. For an owner who is not
a scoped editor the effective result is:

| Status | `EDIT_FULL` | `EDIT_LIMITED` | `SPEND_FREEBIES` | `SPEND_XP` | `DELETE` |
|--------|:-----------:|:--------------:|:----------------:|:----------:|:--------:|
| `Un` Unapproved | yes | yes | yes | no | yes |
| `Rev` Returned for revisions | yes | yes | yes | no | yes |
| `Sub` Submitted | no | no | no | no | no |
| `App` Approved | no | no | no | yes | no |
| `Ret` Retired | no | no | no | no | no |
| `Dec` Deceased | no | no | no | no | no |

Viewing is never restricted by status. For a deceased object, `EDIT_FULL`,
`EDIT_LIMITED`, `DELETE` and `SPEND_XP` require a scoped editor whatever other roles the
user has.

### Checking permissions

All methods are static and accept an optional `request`. Pass it: with a request, the
user's memberships are read once per request (five queries: head-ST chronicles,
game-ST chronicles, ST relationships, chronicles played in, observer rows) and every
later check on that request is answered from memory. Without it, each call queries the
database.

| Method | Question |
|--------|----------|
| `user_has_permission(user, obj, permission, status_aware=True, request=None)` | The general check |
| `user_can_view(user, obj)` | `VIEW_FULL` or `VIEW_PARTIAL` |
| `user_can_edit(user, obj)` | `EDIT_FULL` |
| `user_can_spend_xp(user, obj)` / `user_can_spend_freebies(user, obj)` | `SPEND_XP` / `SPEND_FREEBIES` |
| `get_visibility_tier(user, obj)` | `VisibilityTier.FULL`, `PARTIAL` or `NONE` |
| `user_has_scoped_editor_role(user, obj)` | Has `ADMIN`, `CHRONICLE_HEAD_ST` or `CHRONICLE_ST` on the object; used to choose between full and limited forms |
| `can_manage_scope(user, chronicle, gameline)` | Staff, or head ST / matching-gameline ST of that chronicle |
| `can_manage_chronicle(user, chronicle)` | Staff, or the chronicle's head ST (chronicle-wide actions have no gameline) |
| `user_can_manage_creation(user, form, request)` | `can_manage_scope` for the chronicle chosen in a creation form (bound data, then `?chronicle=`, then initial) and the form model's gameline |
| `check_permission(user, obj, "view_full")` | Instance method; accepts the permission as a string |

After a write that changes memberships, observers or ST relationships, call
`PermissionManager.invalidate_request_cache(request)` before checking again on the same
request. Owner and status are read live from the object and need no invalidation.

```python
from core.permissions import Permission, PermissionManager

if not PermissionManager.user_has_permission(
    request.user, character, Permission.SPEND_XP, request=request
):
    raise PermissionDenied
```

### Filtering querysets

`PermissionManager.filter_queryset_for_user(user, queryset)` returns the rows the user
can view at full or partial level:

- anonymous users get `queryset.none()`;
- staff and superusers get the queryset unchanged;
- everyone else gets rows they own (`owner` or `user` field), rows in chronicles where
  they are head ST, game ST or have any ST relationship, rows in chronicles where they
  own a character, and rows they observe (matched on content type as well as pk).

The result is `.distinct()`. List views use it through `VisibilityFilterMixin`. It does
not read the `visibility` field; public cards are a separate projection (below).

## Route policies

`core.access_policy.route_policy(view)` returns the view's policy: the class attribute
`access_policy` when the class itself defines it (registry-built views do), otherwise
`VIEW_POLICIES["<module>.<ClassName>"]`. `authorize_route(request, view, args, kwargs,
subject=None)` then returns `None` (continue), returns a response, or raises.

| Policy | What `authorize_route` does |
|--------|-----------------------------|
| `PUBLIC_READ`, `PUBLIC_INDEX` | Nothing: anyone may call the view |
| `PUBLIC_CARD` | Passes to the projection, which checks detail-card visibility itself |
| `ROUTER` | Nothing here; the view is a `DictView` that authorizes the object and each target itself |
| `ACTION` | Non-POST gets 405; anonymous gets a plain 401. The action class checks the object |
| `WIDGET` | Anonymous gets JSON `{"error": "Authentication required"}` with 401 |
| `LOGIN`, `ACCOUNT`, `GAME`, `OBJECT_CREATE` | Anonymous gets a plain 401. Exception: `GET`/`HEAD` of `game.views.SceneDetailView` and `SceneListView` pass through (those views apply scene visibility themselves) |
| `STAFF_WRITE` | Anonymous gets 401; a signed-in non-staff user gets `PermissionDenied` |
| `OBJECT_LIST` | For anyone but staff, `GET`/`HEAD` is answered by `render_public_object_list()` (the public-card list) instead of the view |
| `CHARGEN_STEP` | Loads the object (a `LocationModel` for `locations.*` views, else a `CharacterModel`) and requires `EDIT_FULL` and status `Un` or `Rev`; otherwise 404 |
| `OBJECT_DETAIL` | Loads the object. With `VIEW_FULL` the view runs. Otherwise `GET`/`HEAD` gets `PublicObjectDetailView` (name, `public_info`, approved image) only for `PUB` or `CHR` in a readable chronicle; hidden objects and other methods get 404 |
| `OBJECT_WRITE`, `OBJECT_ACTION`, `OBJECT_ST_WRITE` | See below |

For the three write policies the object is loaded and:

1. `OBJECT_ST_WRITE` additionally requires a scoped editor role.
2. An official `CharacterTemplate` (`is_official=True`) requires a scoped editor role.
3. `EDIT_FULL` is required, else `PermissionDenied`.
4. For non-staff `POST`, `PUT` and `PATCH` requests, the fields `owner`, `chronicle`,
   `gameline`, `status`, `npc`, `xp`, `freebies_approved`, `approved` and `approved_by`
   may appear in the POST only with their current value. For `OBJECT_WRITE` and
   `OBJECT_ST_WRITE`, a checkbox (`npc`, `freebies_approved`) that the view's form
   declares, that is currently true and that is missing from the POST counts as a change.
   Any change raises `PermissionDenied("Approval and ownership fields require a dedicated
   action")`. Status, ownership and approval changes go through action endpoints and
   `ApprovalService` instead.

Objects are loaded by `pk`; a missing or malformed pk is a 404.

### `AuthorizationMiddleware`

[`AuthorizationMiddleware`](../middleware/authorization.py) runs after
`AuthenticationMiddleware`. In `process_view` it:

1. Ignores views whose module does not start with a project prefix (`accounts.`,
   `characters.`, `core.`, `game.`, `items.`, `locations.`, `widgets.`), so Django admin
   and `django.contrib.auth` views are not affected.
2. Returns a plain-text 404 when a `pk` URL argument is not a positive ASCII integer.
3. Skips views derived from `core.model_registry.RegistryViewMixin`; they call
   `authorize_route` in their own `dispatch()` so the loaded object is reused.
4. For classes in `game.views`, looks up private records (`Journal`, `JournalEntry`,
   `XPSpendingRequest`, `FreebieSpendingRecord`, `WeeklyXPRequest`, `StoryXPRequest`),
   `Scene` and `Chronicle` by pk and returns the same plain-text 404 when the object is
   missing or the user may not read it (`game.security.can_read_private_record`,
   `can_view_scene`, `readable_chronicles`). A fixed response keeps hidden ids
   indistinguishable from missing ones.
5. Calls `authorize_route`.

In `process_template_response` it adds `object_perms` (below) to any
`TemplateResponse` whose context has an `object`.

### `AuthErrorHandlerMiddleware`

[`AuthErrorHandlerMiddleware`](../middleware/auth_error_handler.py) is the last
middleware. It turns a redirect to `settings.LOGIN_URL` for an anonymous user (what
`LoginRequiredMixin` produces) into a 401 page (`core/errors/401.html`), and renders
`core/errors/403.html` with status 403 for a `PermissionDenied` raised by a view.

### Declaring a policy for a new view

1. Add `"<module>.<ClassName>"` (the module where the class is defined) to the right set
   in `POLICIES`. Item and location types declared in a model registry set
   `ActionSpec.policy` instead; a view must not have both.
2. Pick the narrowest policy. Public views must not define `post`, `put`, `patch` or
   `delete` (the route test checks `PUBLIC_READ` views for this).
3. Run the route policy tests in
   [`core/tests/security/`](../tests/security/).

[`scripts/build_route_policy_manifest.py`](../../scripts/build_route_policy_manifest.py)
can generate a starting manifest for review; the runtime never generates policies.

## Capabilities for templates

Templates do not ask `PermissionManager` questions one by one. They read
`object_perms`, a frozen `core.permission_context.ObjectPermissions` built from it:

| Attribute | Meaning |
|-----------|---------|
| `can_view_full`, `can_view_partial` | `VIEW_FULL`, `VIEW_PARTIAL` |
| `can_edit`, `can_edit_limited` | `EDIT_FULL`, `EDIT_LIMITED` |
| `can_spend_xp`, `can_spend_freebies` | `SPEND_XP`, `SPEND_FREEBIES` |
| `can_approve`, `can_delete`, `can_manage_observers` | `APPROVE`, `DELETE`, `MANAGE_OBSERVERS` |
| `can_approve_spending` | `game.spending_approval.can_approve_spending` (no self-approval of a player character) |
| `is_owner` | Has `OWNER` |
| `is_chronicle_st` | Any of `CHRONICLE_HEAD_ST`, `CHRONICLE_ST_VIEW`, `CHRONICLE_ST`, `GAME_ST` |
| `is_scoped_st` | `CHRONICLE_HEAD_ST` or `CHRONICLE_ST` |
| `can_manage_character` | `is_scoped_st` or `ADMIN` |
| `can_chargen` | `EDIT_FULL` and status `Un` or `Rev` |
| `visibility_tier` | `VisibilityTier` value |

`add_object_permissions(request, context)` sets `context["object_perms"]` when
`context["object"]` is a `core.models.Model` (or a record whose permission subject is
one). `PermissionContextMixin` calls it from `get_context_data`, and the middleware calls
it for any `TemplateResponse`. Snapshots are cached on the request per user, object,
roles, status and `npc`.

For lists, call `prepare_permission_objects(request, rows)` on the materialized page; it
resolves polymorphic rows in one query per concrete type and warms the snapshot cache, so
`{% object_permissions row as row_perms %}` (from the `permissions` tag library) costs no
further queries per row.

The `permissions` library also has single-question tags (`user_can_view`,
`user_can_edit`, `user_has_permission`, `visibility_tier`, `user_roles`, `is_owner`,
`is_st`, `is_game_st`) and tier filters (`is_full`, `is_partial`, `is_none`). No project
template uses them; prefer `object_perms` or `object_permissions`. The approval buttons
come from `{% tl_object_actions %}` (see
[templates and static files](templates-and-static.md#object-actions)).

## See also

- [Authorization architecture](../../docs/architecture/authorization.md)
- [View mixins](mixins.md)
- [Views](views.md)
- [Security tests](testing.md#security-tests)
- [`core/permissions.py`](../permissions.py)
- [game app](../../game/README.md) (`game/security.py`)
