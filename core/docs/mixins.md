# View mixins

This page lists every class-based-view mixin in [`core/mixins.py`](../mixins.py): what it
does, what it checks and where it fits. It is for anyone writing or reviewing a view. Import
mixins from `core.mixins`; the route policy of the view (see
[permissions and policies](permissions-and-policies.md#route-policies)) still applies on
top of whatever a mixin checks.

## Summary

| Mixin | Kind | Denial |
|-------|------|--------|
| `PermissionRequiredMixin` | Object permission gate | 404 or 403 (configurable) |
| `ViewPermissionMixin` | Requires `VIEW_FULL` | 404 |
| `EditPermissionMixin` | Requires `EDIT_FULL` | 403 |
| `SpendFreebiesPermissionMixin` | Requires `SPEND_FREEBIES` | 403 |
| `ScopedEditFormMixin` | Chooses full or limited form | none (form choice) |
| `VisibilityFilterMixin` | Filters list querysets; adds tier and flags | none (filters) |
| `OwnerRequiredMixin` | Owner or staff only | 403 |
| `CharacterOwnerOrSTMixin` | `VIEW_FULL` on the record's character, or staff | 403 |
| `StorytellerRequiredMixin` | Staff or scoped storyteller for the target | 403 |
| `ScopedCreationFormMixin` | Limits the chronicle choice to readable chronicles | none |
| `PermissionContextMixin` | Adds `object_perms` to the context | none |
| `SpecialUserMixin` | `check_if_special_user()` helper | none |
| `ObjectCachingMixin` | Caches `get_object()` | none |
| `MessageMixin` | Success/error flash messages; creation ownership | none |
| `SuccessMessageMixin`, `ErrorMessageMixin` | The two halves of `MessageMixin` | none |
| `SharedTemplateMixin` | Specific template, then a shared fallback | none |
| `ListHeadingMixin` | `list_title` and `list_heading` for shared list pages | none |

## Permission gates

### `PermissionRequiredMixin`

Checks one permission on `self.get_object()` in `dispatch()`, before the handler runs.

- `required_permission`: a `core.permissions.Permission`; `has_permission()` raises
  `ValueError` if it is unset.
- `raise_404_on_deny` (default `True`): raise `Http404` rather than `PermissionDenied`,
  so a user who may not see an object cannot tell it exists.
- Override `has_permission()` for a custom rule.

It includes `ObjectCachingMixin` (the object fetched for the check is reused by the view)
and `PermissionContextMixin`.

### `ViewPermissionMixin`, `EditPermissionMixin`, `SpendFreebiesPermissionMixin`

Preset subclasses:

| Mixin | `required_permission` | On denial |
|-------|----------------------|-----------|
| `ViewPermissionMixin` | `VIEW_FULL` | 404 |
| `EditPermissionMixin` | `EDIT_FULL` | 403 |
| `SpendFreebiesPermissionMixin` | `SPEND_FREEBIES` | 403 |

`EDIT_FULL` includes an owner editing a draft (`Un` or `Rev`), so `EditPermissionMixin`
suits both storyteller edit pages and character-creation steps.

```python
# characters/views/changeling/autumn_person.py (abridged)
class AutumnPersonUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = AutumnPerson
    fields = [...]                            # full field list, for scoped editors
    limited_form_class = LimitedHumanEditForm  # what an owner may submit
```

### `ScopedEditFormMixin`

Picks the form class: the view's normal `form_class` when the user has a scoped editor role
on the object (`PermissionManager.user_has_scoped_editor_role`: admin, head ST or
matching-gameline ST), otherwise `limited_form_class` (required; `ValueError` if unset).
It does not grant access; pair it with `EditPermissionMixin`. The limited form is used as
given, even when the view edits a subclass, so its model and widgets stay as reviewed.

### `VisibilityFilterMixin`

For list and detail views of permission-controlled models.

- `get_queryset()` returns `PermissionManager.filter_queryset_for_user(user, qs)`
  (see [filtering querysets](permissions-and-policies.md#filtering-querysets)).
- On paginated pages it calls `prepare_permission_objects` for the page's rows.
- When the view has an `object`, the context gains `visibility_tier`, `user_can_edit`,
  `user_can_spend_xp`, `user_can_spend_freebies` and the `VisibilityTier` enum.

Registry list views with the `OBJECT_LIST` policy get this mixin automatically.

### `OwnerRequiredMixin`

Allows only the owner (`obj.owner` or `obj.user` equals the request user) and staff or
superusers; everyone else gets `PermissionDenied`.

- By default it checks `self.get_object()`.
- With `owner_check_model` set, it loads that model by the URL kwarg
  `owner_check_kwarg` (default `"character_pk"`), stores it on `self.<owner_check_attr>`
  (default `character`) and checks that object, with `owner_check_message` as the error.

It does not consult storyteller roles; use a permission mixin when STs should pass.

### `CharacterOwnerOrSTMixin`

For records that hang off a character (XP requests, journal entries). Staff pass; anyone
else needs `VIEW_FULL` on `obj.character`. Otherwise `PermissionDenied`.

### `StorytellerRequiredMixin`

Restricts a view to staff or a storyteller scoped to the target. In `dispatch()`:

1. Anonymous users get `PermissionDenied`; staff pass.
2. The target chronicle is found from the object (a `Chronicle` itself, `obj.chronicle`,
   or `obj.character.chronicle`), else the `chronicle_pk` URL kwarg, else the chronicle of
   the character in `character_pk`.
3. The gameline comes from the object, its character, or (for POST) the `gameline` form
   field.
4. With a gameline, `can_manage_scope(user, chronicle, gameline)` decides; for a
   `Chronicle` model or when no gameline is known, `can_manage_chronicle` (head ST only).
5. For a `Scene` view without an object on `GET`/`HEAD`, any storyteller with an
   `STRelationship` in the chronicle also passes.

## Forms and creation

### `ScopedCreationFormMixin`

In `get_form()`, if the form has a `chronicle` field, limits its queryset to
`game.security.readable_chronicles(user)`, so a user cannot create an object in a
chronicle they cannot see.

### `MessageMixin`, `SuccessMessageMixin`, `ErrorMessageMixin`

- `SuccessMessageMixin`: after a successful `form_valid`, flashes `success_message`
  formatted with `{name}`, `{id}`, `{pk}` (from the saved object, each cut to 100
  characters), `{model_name}` and `{model_name_plural}`. If formatting fails the raw
  string is used.
- `ErrorMessageMixin`: flashes `error_message` (default "Please correct the errors
  below.") on `form_invalid`.
- `MessageMixin` combines both. On a `CreateView` it also calls
  `prepare_created_object(form, request)` before saving.

`prepare_created_object(form, request)` applies to new `core.models.Model` instances only:

- anonymous users get `PermissionDenied`;
- a chosen chronicle must be one of `readable_chronicles(user)`;
- `owner` is set to the user, or to `None` when the user is a scoped editor for the
  chronicle and gameline and the POST contains `shared=1`;
- `status` is forced to `"Un"` unless the user is staff or a superuser (`Role.ADMIN`).

This is why creation views must use `MessageMixin` (or call the function): it stops a
player from creating an approved object or one owned by someone else.

## Context and template helpers

### `PermissionContextMixin`

Adds `object_perms` (an `ObjectPermissions` snapshot) to the context when the context
has a permission-controlled `object`. See
[capabilities for templates](permissions-and-policies.md#capabilities-for-templates).

### `SpecialUserMixin`

Adds `check_if_special_user(obj, user)`, which returns
`user_has_permission(user, obj, VIEW_FULL)`. Detail views use it to decide whether to
show the full sheet. It also includes `PermissionContextMixin`.

### `ObjectCachingMixin`

Caches the first `get_object()` result on the view as `_cached_object`, so a permission
check in `dispatch()` and the handler share one query.

### `SharedTemplateMixin`

Returns `template_name` (the specific override slot) followed by
`shared_template_name`. Django renders the first that exists, so the shared template is
used until someone writes the specific one. If no `template_name` is declared, the shared
template is the page. Built on `core.template_resolution.shared_template_names`.

### `ListHeadingMixin`

Adds `list_title` (defaults to the model's `verbose_name_plural`) and `list_heading`
(`"<model.gameline>_heading"`, or `"wod_heading"`) for shared list templates.

## Choosing mixins

| View | Typical mixins |
|------|----------------|
| Private object detail | `ViewPermissionMixin` or `SpecialUserMixin` (policy `OBJECT_DETAIL`) |
| Object edit | `EditPermissionMixin`, `ScopedEditFormMixin`, `MessageMixin` (policy `OBJECT_WRITE`) |
| Object create | `ScopedCreationFormMixin`, `MessageMixin` (policy `OBJECT_CREATE`) |
| Private object list | `VisibilityFilterMixin` (policy `OBJECT_LIST`) |
| Reference data detail/list | none, or `CachedDetailView` / `CachedListView` (policy `PUBLIC_READ`) |
| Storyteller-only form | `StorytellerRequiredMixin` |
| A single state change | Not a mixin: subclass `core.actions.ObjectActionView` (policy `ACTION`) |

## See also

- [Permissions and policies](permissions-and-policies.md)
- [Views](views.md)
- [Adding a view](../../docs/guides/adding-a-view.md)
- [`core/mixins.py`](../mixins.py)
