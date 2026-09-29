# Permissions and route policies

Rules for access control: which route policy a view gets, where object checks live, how
owners are limited to safe fields, and what must be tested. The full explanation (roles,
permission matrix, status rules, public cards, scene visibility, approvals) is in
[docs/architecture/authorization.md](../../../../docs/architecture/authorization.md) and
[core/docs/permissions-and-policies.md](../../../../core/docs/permissions-and-policies.md);
the mixins are in [core/docs/mixins.md](../../../../core/docs/mixins.md).

## The two layers

1. **Route policy, per URL.** `core.middleware.authorization.AuthorizationMiddleware` calls
   `core.access_policy.authorize_route` in `process_view`, before the view runs. The policy
   comes from the view class's own `access_policy` attribute (registry views, set from
   `ActionSpec.policy`) or from `core/route_policy_manifest.py`. No policy: denied.
2. **Object permission, per object.** `core.permissions.PermissionManager` answers
   `user_has_permission(user, obj, Permission.X, request=request)` from the user's roles
   for that object and the object's `status`.

The route layer lives in middleware so a view that forgets a mixin is still covered, and
every route can be enumerated and tested in one place.

## Choosing a policy

| The view | Policy | Add in the view |
|----------|--------|-----------------|
| Reads reference data | `PUBLIC_READ` (no write methods allowed) | Nothing; may be cached |
| Creates or edits reference data | `STAFF_WRITE` | `MessageMixin` |
| Lists player objects | `OBJECT_LIST` | `VisibilityFilterMixin` |
| Shows one player object | `OBJECT_DETAIL` | Nothing; non-full viewers get the public card |
| Creates a player object | `OBJECT_CREATE` | `MessageMixin` (runs `prepare_created_object`), `ScopedCreationFormMixin` if the form has `chronicle` |
| Edits or deletes a player object | `OBJECT_WRITE` | `EditPermissionMixin`; owner-editable characters add `ScopedEditFormMixin` + `limited_form_class` |
| A form only storytellers may use | `OBJECT_ST_WRITE` | As `OBJECT_WRITE` |
| One POST state change on one object | `ACTION` | Subclass `core.actions.ObjectActionView` |
| A chargen step | `CHARGEN_STEP` | `ChargenStepMixin` (see [docs/architecture/character-creation.md](../../../../docs/architecture/character-creation.md)) |
| Dispatches to other views by type or step (`DictView`) | `ROUTER` | `protected_object = True` or `chargen_router = True`; every target also has a policy |
| `game` / `accounts` pages | `GAME` / `ACCOUNT` | Object checks in the view (`StorytellerRequiredMixin`, `CharacterOwnerOrSTMixin`, `game.security` filters) |
| Needs a user, no object | `LOGIN` | |
| Item or location CRUD from the registry | Its `ActionSpec.policy`, never the manifest | See [registry.md](registry.md) |

Add manifest entries to the matching `frozenset` in sorted order, as the dotted
`module.ClassName` of the class that URL routing resolves. Remove the entry when you remove
the view: `test_every_project_route_and_router_target_has_one_policy` fails on stale
entries too. `scripts/build_route_policy_manifest.py` overwrites the manifest; use its
output only as a suggestion.

## Object checks

- Ask `PermissionManager`, and pass `request=`: memberships are loaded once per request
  and cached on it. After changing memberships, observers or `STRelationship`s mid-request,
  call `PermissionManager.invalidate_request_cache(request)`.
- Never test roles by hand in views (`user.profile.is_st()`, `obj.owner == user`,
  `chronicle.head_st == user`) to decide access. Use `user_has_permission`,
  `user_has_scoped_editor_role`, `can_manage_scope` or `can_manage_chronicle`.
- New capability: extend `Permission` and `ROLE_PERMISSIONS` (and
  `ObjectPermissions` in `core/permission_context.py` if templates need it) instead of a
  one-off check.
- Scope storytellers by chronicle **and gameline**: `CHRONICLE_ST` needs an
  `STRelationship` whose `Gameline.name` equals `settings.GAMELINES[obj.gameline]["name"]`.
- Filter lists with `PermissionManager.filter_queryset_for_user` (via
  `VisibilityFilterMixin`) or the `game.security` helpers (`readable_chronicles`,
  `staffed_chronicles`, `filter_private_records`, `filter_scenes`).

## Hiding what a user may not see

- A missing object and a hidden one get the same response. `ViewPermissionMixin` and
  `PermissionRequiredMixin` raise 404 on denial by default; `ObjectActionView.authorize()`
  raises 404 when the user lacks `VIEW_FULL`, before checking `permission`.
- `OBJECT_DETAIL` shows a non-full viewer the public card (`name`, `public_info`, approved
  image) on GET and 404 on other methods. Never render private fields for them.
- The middleware answers a plain-text 404 for private `game` records, scenes and chronicles
  the user cannot read, and for a `pk` that is not a positive integer.
- A 403 (`EditPermissionMixin`, `SpendFreebiesPermissionMixin`, `STAFF_WRITE`) is fine only
  when the user can already see the object or the page.

## Protected fields and limited forms

- For non-staff POST/PUT/PATCH on `OBJECT_WRITE`, `OBJECT_ACTION` and `OBJECT_ST_WRITE`,
  `authorize_route` refuses any change to `owner`, `chronicle`, `gameline`, `status`,
  `npc`, `xp`, `freebies_approved`, `approved`, `approved_by` (an unchecked `npc` or
  `freebies_approved` box counts as a change). Storytellers change them through actions
  and services (`ApprovalService`, `game.spending_approval`, `characters.services.status`).
- Owners may edit their own draft (`EDIT_FULL` while `Un` or `Rev`), but only descriptive
  fields. Character update views combine:

```python
class HtRHumanUpdateView(ScopedEditFormMixin, EditPermissionMixin, UpdateView):
    model = HtRHuman
    fields = HT_R_HUMAN_UPDATE_FIELDS          # full form, scoped editors only
    limited_form_class = LimitedHumanEditForm  # characters/forms/core/limited_edit.py
```

- `ScopedEditFormMixin` gives the full form only to `ADMIN`, `CHRONICLE_HEAD_ST` or
  `CHRONICLE_ST` and raises `ValueError` if `limited_form_class` is missing.
- `LimitedHumanEditForm` allows `notes`, `description`, `public_info`, `image`, `history`,
  `goals`. Owners change stats only through chargen, freebies and XP requests.

## Templates

Templates read `object_perms` (a frozen `core.permission_context.ObjectPermissions`:
`can_edit`, `can_edit_limited`, `can_spend_xp`, `can_approve`, `is_owner`,
`is_scoped_st`, `can_chargen`, ...), added by `PermissionContextMixin` and by the
middleware's `process_template_response`. Do not compute roles in templates; the
`permissions` tag library exists for older pages.

## Reference data versus player data

- Reference models (clans, disciplines, tribes, guilds, arcanoi, factions, books,
  languages) are public: `PUBLIC_READ` detail and list, no login, `STAFF_WRITE` writes.
- Player data (characters, groups such as coteries, packs, cabals and motleys, items,
  locations, character templates, chimerae, effects, rotes) always goes through an
  `OBJECT_*`, `ACTION` or `CHARGEN_STEP` policy.

## Tests

| Change | Test |
|--------|------|
| Any new route | `core/tests/security/test_route_policies.py` passes (policy declared) |
| New player-object view | Anonymous, other player, ST of another chronicle, ST of another gameline, owner, scoped ST, staff: each gets the expected status and content |
| New action | Use `core.tests.action_audience.ActionAudienceMixin` (owner, player, st, other_line_st, other_chronicle_st, staff, anonymous) |
| New write route | A non-staff POST changing a protected field gets 403 and changes nothing |
| Hidden object | Same status and body as a missing pk |

Security tests live in `core/tests/security/` for cross-cutting rules and next to the view
tests (`items/tests/views/test_authorization.py`, `characters/tests/views/test_auth_required.py`)
for app routes.

## Checklist

- [ ] One policy per routed view (manifest or registry), narrowest fit, sorted entry.
- [ ] Object access via `PermissionManager` with `request=`; no hand-rolled role checks.
- [ ] Hidden equals missing; partial viewers see the public card only.
- [ ] Protected fields untouched by forms; owner edits use a limited form.
- [ ] Templates use `object_perms`.
- [ ] Denial tests for every audience that must be refused.

## See also

- [docs/architecture/authorization.md](../../../../docs/architecture/authorization.md)
- [core/docs/permissions-and-policies.md](../../../../core/docs/permissions-and-policies.md)
- [core/docs/mixins.md](../../../../core/docs/mixins.md)
- [`core/access_policy.py`](../../../../core/access_policy.py), [`core/permissions.py`](../../../../core/permissions.py)
- [views.md](views.md), [forms.md](forms.md)
