# Forms

Rules for writing a form, a formset or a character CRUD field list. Rendering is in
[templates.md](templates.md); who gets which form is in [permissions.md](permissions.md).

## Field lists are allowlists

- Every `ModelForm` names its fields: `Meta.fields = [...]`, or `fields = [...]` on the
  generic view. Never `"__all__"`, `Meta.exclude` or a list built by introspecting the
  model. *Why:* a new model field must be reviewed before users can post it.
- Character create and update field lists live in
  [`characters/forms/core/crud_fields.py`](../../../../characters/forms/core/crud_fields.py)
  as tuples composed from shared groups (`IDENTITY_FIELDS`, `ATTRIBUTE_FIELDS`,
  `COMMON_TALENT_FIELDS`, ...) and are imported by the views
  (`fields = HT_R_HUMAN_UPDATE_FIELDS`). Field order in the tuple is the form order.
- `characters/tests/views/core/shared_character_crud_baseline.json` pins, per view, the
  field count and a SHA-256 of the ordered field list, and which views select a limited
  form; `characters/tests/views/core/test_shared_character_crud.py` compares them. Changing
  a list means updating the baseline in the same diff, on purpose.
- Registry item and location forms take `ModelSpec.fields` or an explicit
  `ActionSpec.options["fields"]` / `form_class` ([registry.md](registry.md)).
- Never include `owner`, `status`, `xp`, `freebies_approved`, `approved`, `approved_by`
  in a player-facing form. `chronicle` and `npc` may appear on create and ST forms; the
  route guard still rejects changes by non-staff on write routes
  ([permissions.md](permissions.md)).

## Full and limited forms

- Storytellers (scoped editors) get the full form; owners get a limited form of
  descriptive fields. The view picks with `ScopedEditFormMixin` and `limited_form_class`.
- Limited forms live in
  [`characters/forms/core/limited_edit.py`](../../../../characters/forms/core/limited_edit.py):
  `LimitedHumanEditForm` (`notes`, `description`, `public_info`, `image`, `history`,
  `goals`) works for every `Human` subclass; `OwnerUnapprovedCharacterEditForm` covers
  `Character` drafts. Reuse them rather than writing a per-gameline copy.
- Do not choose a form class with `user.profile.is_st()` or `user.is_staff`; that ignores
  chronicle and gameline scope.

## Scoping choices to the user

- A `chronicle` field lists only `game.security.readable_chronicles(user)`.
  `ScopedCreationFormMixin` does this for create views; forms built outside a view take a
  `user` keyword and filter in `__init__`.
- Other user-dependent querysets (the user's characters, a scene's participants) are
  filtered in the form's `__init__` from explicit keyword arguments (`user=`, `scene=`,
  `character=`) passed by `get_form_kwargs()`. Start from `Model.objects.none()` in the
  field declaration when the queryset depends on those arguments.
- `PermissionManager.user_can_manage_creation(user, form, request)` tells a creation page
  whether to show ST-only controls for the chronicle selected in the form.

## Validation

- Field rules in `clean_<field>()`, cross-field rules in `clean()`; model rules stay in the
  model's `clean()` (a `ModelForm` runs it). See [validation.md](validation.md).
- Game-rule totals (priority dots, freebie costs) belong in the chargen step form or a
  service, not the view. Services return a `ServiceResult`; the view adds `error` to the
  form with `form.add_error(None, ...)`.
- Formset-level rules go in a `BaseInlineFormSet.clean()`.

## Widgets and styling

- Do not set Bootstrap classes (`form-control`, `form-select`, `form-check`) or inline
  styles in widget `attrs`. Spread styles inputs by position inside `.tl-field`
  (`core/static/core/tl/tl.css`). Older forms still carry such classes; they are inert,
  do not add more.
- `attrs` may carry `placeholder`, `rows`, `aria-*` and `data-*` hooks for page scripts.
- Reusable widgets are in the `widgets` app (`widgets/widgets/`): `DotRatingInput`,
  `ChainedSelect` / `HtmxChainedSelect`, `CreateOrSelectWidget`,
  `OptionMetadataSelect`, plus the filterable-list and formset-manager scripts. Their
  JavaScript ships as widget `Media`; `{% page_media %}` at the end of
  `core/tl_base.html` collects the media of every form and formset in the context.
- Multiple formsets on one page: `core.views.generic.MultipleFormsetsMixin` with the
  `FormsetManager` id conventions (`{prefix}_formset`, `empty_{prefix}_form`).

## Checklist

- [ ] Explicit field list; no `__all__`, `exclude` or introspection.
- [ ] Character CRUD lists come from `crud_fields.py`; baseline updated on purpose.
- [ ] Protected fields absent from player forms; owners get a limited form.
- [ ] Chronicle and other choices scoped to the user.
- [ ] No Bootstrap classes or inline styles in `attrs`.
- [ ] Form tests: valid data saves, each rule rejects, scoped querysets exclude other
  users' rows (`<app>/tests/forms/<gameline>/test_<module>.py`).

## See also

- [docs/architecture/character-creation.md](../../../../docs/architecture/character-creation.md)
- [core/docs/mixins.md](../../../../core/docs/mixins.md)
- [`widgets/`](../../../../widgets/) and its docs
- [permissions.md](permissions.md), [templates.md](templates.md)
