# Core views

This page is the reference for the views, URL routes and view building blocks in the
`core` app: the pages under the `core:` namespace, the generic views and routers other
apps build on (`CachedDetailView`, `DictView`, the reference-view factory), the
item/location model registry, action endpoints and the error handlers. It is for anyone
adding or changing a view. Mixins have their own page ([mixins](mixins.md)); access rules
are in [permissions and policies](permissions-and-policies.md).

Every view listed here also has a route policy in
[`core/route_policy_manifest.py`](../route_policy_manifest.py). The policy runs in
middleware before the view, so the "Policy" column below is part of each view's contract.

## URL routes

[`core/urls.py`](../urls.py) is included at the site root under the `core` namespace
([`tg/urls.py`](../../tg/urls.py)). URL arguments named `pk` must be positive integers;
`AuthorizationMiddleware` answers anything else with a 404 before the view runs.

| Path | Name | View | Policy |
|------|------|------|--------|
| `/` | `core:home` | `HomeListView` | `PUBLIC_READ` |
| `/types/<kind>/<action>/` | `core:object_type_redirect` | `ObjectTypeRedirectView` | `PUBLIC_READ` |
| `/book/` | `core:index_book` | `BookListView` | `PUBLIC_READ` |
| `/book/<pk>/` | `core:book` | `BookDetailView` | `PUBLIC_READ` |
| `/book/create/` | `core:create_book` | `BookCreateView` | `STAFF_WRITE` |
| `/book/update/<pk>/` | `core:update_book` | `BookUpdateView` | `STAFF_WRITE` |
| `/language/` | `core:index_language` | `LanguageListView` | `PUBLIC_READ` |
| `/language/<pk>/` | `core:language` | `LanguageDetailView` | `PUBLIC_READ` |
| `/language/create/` | `core:create_language` | `LanguageCreateView` | `STAFF_WRITE` |
| `/language/update/<pk>/` | `core:update_language` | `LanguageUpdateView` | `STAFF_WRITE` |
| `/newsitem/` | `core:index_newsitem` | `NewsItemListView` | `PUBLIC_READ` |
| `/newsitem/<pk>/` | `core:newsitem` | `NewsItemDetailView` | `PUBLIC_READ` |
| `/newsitem/create/` | `core:create_newsitem` | `NewsItemCreateView` | `STAFF_WRITE` |
| `/newsitem/update/<pk>/` | `core:update_newsitem` | `NewsItemUpdateView` | `STAFF_WRITE` |
| `/houserules/index/` | `core:houserules` | `HouseRulesIndexView` | `PUBLIC_READ` |
| `/houserules/<pk>/` | `core:houserule` | `HouseRuleDetailView` | `PUBLIC_READ` |
| `/houserules/create/` | `core:create_houserule` | `HouseRuleCreateView` | `STAFF_WRITE` |
| `/houserules/update/<pk>/` | `core:update_houserule` | `HouseRuleUpdateView` | `STAFF_WRITE` |
| `/templates/` | `core:character_template_list` | `CharacterTemplateListView` | `OBJECT_LIST` |
| `/templates/create/` | `core:character_template_create` | `CharacterTemplateCreateView` | `OBJECT_CREATE` |
| `/templates/<pk>/` | `core:character_template_detail` | `CharacterTemplateDetailView` | `OBJECT_DETAIL` |
| `/templates/<pk>/edit/` | `core:character_template_update` | `CharacterTemplateUpdateView` | `OBJECT_WRITE` |
| `/templates/<pk>/delete/` | `core:character_template_delete` | `CharacterTemplateDeleteView` | `OBJECT_WRITE` |
| `/templates/<pk>/export/` | `core:character_template_export` | `CharacterTemplateExportView` | `OBJECT_DETAIL` |
| `/templates/import/` | `core:character_template_import` | `CharacterTemplateImportView` | `LOGIN` |
| `/templates/<pk>/create-npc/` | `core:character_template_create_npc` | `CharacterTemplateQuickNPCView` | `LOGIN` |

`core.views.public_object.PublicObjectDetailView` (`PUBLIC_CARD`) has no URL of its own;
the access policy renders it in place of a private detail page (see
[public projections](#public-projections)).

## Home page

`core.views.home.HomeListView` renders `core/index.html` with the news items
(`NewsItem`, newest first, as `news`) and `continue_scenes`: up to six
(`CONTINUE_SCENE_LIMIT`) unfinished scenes the user has a character in or staffs,
filtered through `game.security.filter_scenes`, annotated with `post_count` and
`last_post` and ordered by latest post. Anonymous users get no scenes. The view is
cached for five minutes with `cache_page_per_visitor` (see
[utilities](utilities.md#caching)).

## Reference pages: books, languages, news, house rules

These are plain Django generic views over the core models in
[models](models.md#concrete-core-models). Reads are public; writes are staff only
(`STAFF_WRITE` refuses anonymous callers with 401 and signed-in non-staff with 403).

| Module | Notes |
|--------|-------|
| [`views/book.py`](../views/book.py) | Detail and list cached for 15 minutes (`cache_page_per_visitor`). Form fields: `name`, `url`, `edition`, `gameline`, `storytellers_vault` |
| [`views/language.py`](../views/language.py) | Detail uses the generic `core/object.html`. Fields: `name`, `frequency` |
| [`views/newsitem.py`](../views/newsitem.py) | List ordered by `-date`. Fields: `title`, `content`, `date` |
| [`views/houserules.py`](../views/houserules.py) | `HouseRulesIndexView` groups rules with `group_rules_by_gameline()` (in `settings.GAMELINES` order, `wod` rules first under "All lines", empty groups dropped) and sets `header` from the user's `profile.preferred_heading`. Fields: `name`, `description`, `chronicle`, `gameline` |

All create and update views use `MessageMixin`, so they flash a message and, on create,
run `prepare_created_object` (a no-op for these non-polymorphic models).

## Character templates

[`views/character_template.py`](../views/character_template.py) manages
`CharacterTemplate` rows (see [models](models.md#charactertemplate)). Every view also
carries `LoginRequiredMixin`.

| View | Behaviour |
|------|-----------|
| `CharacterTemplateListView` | Paginated (20). Non-staff see templates they own or that belong to chronicles they staff. Filters: `?gameline=`, `?character_type=`, `?filter=mine|official|community`. Because the policy is `OBJECT_LIST`, a non-staff `GET` receives the public-card list instead of this view |
| `CharacterTemplateDetailView` | Context name `template` |
| `CharacterTemplateCreateView`, `CharacterTemplateUpdateView` | Use `core.forms.CharacterTemplateForm`, which receives `user`, limits `chronicle` to readable chronicles and, on create, sets `owner` to the user and `is_official=False` |
| `CharacterTemplateDeleteView` | Redirects to the list |
| `CharacterTemplateExportView` | Returns the template as a JSON attachment (`<name>_template.json`) |
| `CharacterTemplateImportView` | `CharacterTemplateImportForm`: a `.json` file up to 5 MB, `is_public`, optional `chronicle`. Requires `name`, `gameline` and `character_type` keys and creates an unofficial template owned by the user with status `Un` |
| `CharacterTemplateQuickNPCView` | POST only. Requires `can_manage_scope` for the template's chronicle and gameline, creates an approved NPC of the mapped model (`mage`, `vampire`, `werewolf`, `changeling`, `wraith`, `demon`) named `"<concept> (NPC)"`, applies the template and redirects to the character |

Official templates (`is_official=True`) can be changed only by a scoped editor; the
`OBJECT_WRITE` policy enforces that (see
[route policies](permissions-and-policies.md#route-policies)).

## Public projections

[`views/public_object.py`](../views/public_object.py) holds the only views that show a
permission-controlled object to someone without full access. They render an allowlisted
projection, never the object itself.

- `PublicObjectDetailView` renders `core/public_object_detail.html` with
  `public_object = {name, public_info, image_url}`. `image_url` is set only when the image
  is approved. The `OBJECT_DETAIL` policy and `DictView` routers render it for `GET`/`HEAD`
  from a user without `VIEW_FULL` only when `can_view_public_object(request, obj)` admits
  them: `PUB`, or `CHR` in a readable chronicle. `PRI`, legacy `CUS` and unknown values
  are hidden as `404` from non-full viewers. The projection rechecks admission itself.
- `render_public_object_list(request, model_class, extra_context=None)` renders
  `core/public_object_list.html` for the `OBJECT_LIST` policy. Staff see every row;
  everyone else sees rows with `visibility="PUB"` (templates must also be `is_public`),
  plus, when signed in, rows `PermissionManager.filter_queryset_for_user` returns and
  `visibility="CHR"` rows in readable chronicles. It reads only `pk`, `name`,
  `public_info`, `image` and `image_status`, caps the list at 250 rows and links each
  card to the model family's detail route (`characters:character`, `items:item`,
  `locations:location`, `characters:group`, and so on). An unsupported model raises
  `ValueError`.

## Object type selection

`ObjectTypeRedirectView` (GET and HEAD only) turns a "create a …" or "list …" selection
into a redirect. `kind` is `character`, `group`, `item` or `location`; `action` is
`create` or `list`. It reads the type from the form field for the kind (`char_type`,
`group_type`, `item_type`, `loc_type`) or `type`, plus an optional `gameline`, and calls
`core.create_redirects.resolve_object_type_url()`:

- items and locations are resolved through their model registry
  (`ModelRegistry.resolve()` then `selection_url()`);
- characters and groups are resolved through seeded `game.ObjectType` rows; exactly one
  match is required, and the route is `characters:<app_name>:<action>:<type>` (no
  gameline segment for `wod`). `dtf_human`, `htr_human` and `mtr_human` map to the route
  names `dtfhuman`, `htrhuman` and `mtrhuman` (`CHARACTER_ROUTE_NAMES`). The character
  pickers offer only types for which `character_type_has_route()` is true.

Unknown or ambiguous types are a 404. Anonymous users choosing `create` are redirected to
login. No route name is ever taken from the request. The Spread partial
`core/tl/create_form.html` submits to this view.

## Generic views

[`views/generic.py`](../views/generic.py):

### `CachedDetailView` and `CachedListView`

`DetailView` and `ListView` wrapped in `cache_page_per_visitor(CACHE_TIMEOUT_LONG)`
(15 minutes). Use them for read-only reference pages (clans, spheres, and so on) under
the `PUBLIC_READ` policy. Do not use them for pages that show per-object permissions.

### `DictView`

A router: it loads one object and hands the request to another view chosen by one of the
object's attributes. Character detail pages (`characters.views.core.GenericCharacterDetailView`,
keyed on `type`) and character-creation wizards (`HumanCharacterCreationView`, keyed on
`creation_status`) are `DictView`s. Its policy is `ROUTER`, which does nothing in
middleware, because the router authorizes the object and the chosen target itself.

| Attribute | Meaning |
|-----------|---------|
| `model_class` | Model to load by `pk` (`get_object_or_404`) |
| `key_property` | Attribute of the object used as the key |
| `view_mapping` | `{key: view class}`; may be a property |
| `default_redirect` | URL name (redirect) or view class (rendered) when the key is not mapped |
| `protected_object` | Require `VIEW_FULL` before routing |
| `public_view_class` | View rendered for a visibility-admitted `GET`/`HEAD` without `VIEW_FULL` (usually `PublicObjectDetailView`) |
| `chargen_router` | Creation wizard mode (below) |

`handle_request()` (used for both GET and POST):

1. Loads the object.
2. With `protected_object` and no `VIEW_FULL`: renders `public_view_class` for reads only
   when detail-card visibility admits the user, otherwise 404. It passes the resolved object
   and honors any target-policy denial response.
3. With `chargen_router`, when the key is a mapped step: a user without `EDIT_FULL` is
   sent to the default page if they can view the object (reads only), otherwise 404.
4. For a mapped key, calls `authorize_route()` for the target view with the loaded object
   as `subject` (so the target's policy checks the same row) and dispatches to it.
5. Otherwise returns `get_default_redirect()`, which also authorizes a view-class
   default.

Override `is_valid_key(obj, key)` to add conditions (the chargen routers also require
status `Un` or `Rev`). The route test
`core/tests/security/test_route_policies.py` requires every `ROUTER` over a
character, group, item, location or template model to set `protected_object` or
`chargen_router`.

### `MultipleFormsetsMixin`

For a create or update view that edits several formsets next to its form. Declare
`formsets = {prefix: FormsetClass}`. It adds `<prefix>_context` (the formset, its empty
form and the element ids the formset manager script expects: `<prefix>_formset`,
`empty_<prefix>_form`) and `<prefix>_js` to the context, binds the formsets on POST,
saves them in `form_valid` (or returns `form_invalid` if any is invalid) and keeps the
bound formsets on an invalid form. `get_form_data(prefix, blankable=None)` returns the
posted rows of one formset as dicts, dropping rows with an empty value outside
`blankable`. Override `get_formset_kwargs(prefix)` to pass extra kwargs; the default adds
`instance=self.object` when the view has one. See the
[formset widget](../../widgets/docs/widgets.md) for the client side.

## Registry views

Items and locations do not write a view class per model. Each app declares its models in
a registry (`items/registry.py`, `locations/registry.py`) built from
[`core/model_registry.py`](../model_registry.py):

- `ModelSpec`: one routable model: `model_label`, `slug`, `group` (URL group, such as
  `mage` or `core`), `gameline`, the four `actions`, and optionally `fields`,
  `form_class`, `templates`, `label`, `list_title`, `model_urls` (URL name per action)
  and `dispatch_view` (a custom detail router).
- `ActionSpec`: one of `detail`, `list`, `create`, `update`: `view_path` (the class
  name the view is published under), `policy` (a key of `POLICIES`), optional `custom`
  base class, `options` (class attributes), `routes` (`(url name, path)` pairs) and
  `form_updates` (widget attrs and help text per field).
- `ModelRegistry(app, entries)` validates the declarations at import time: all four
  actions present, a known policy on each, no duplicate model, slug or route. It builds
  each view class on first use with `RegistryViewMixin`, `MessageMixin` for writes,
  `VisibilityFilterMixin` for `OBJECT_LIST` lists and the matching Django generic view,
  and publishes it in the module named by `view_path` unless a class of that name already
  exists there.

`RegistryViewMixin` calls `authorize_route()` in its own `dispatch()` (the middleware
skips registry views), reusing the loaded object; falls back to
`core/registry/{detail,list,form}.html` after the declared template; sets `list_title` and
`list_heading` on lists; applies `form_updates`; and runs `prepare_created_object` on
create.

Other registry methods: `urls(group, action)` (URL patterns for an app's URL modules),
`url(model, action, pk=None)` (used by `core.registry_urls.RegistryURLMixin` to give
models `get_absolute_url()`, `get_update_url()` and `get_creation_url()`),
`resolve(type_name, gameline=None)`, `selection_url(entry, action)` and `menu(user)` (the
create menu: everything for staff and storytellers, Mage entries for other users,
`STAFF_WRITE` creates only for staff). `get_registry("items"|"locations")` returns an
app's registry.

[`views/registry.py`](../views/registry.py) provides `RegistryDetailView`, a `DictView`
that dispatches a base-model URL (`/items/<pk>/`) to the registered detail view of the
object's concrete class, authorizing it with the object as subject.

See [adding an item or location type](../../docs/guides/adding-an-item-or-location-type.md).

## Action endpoints

A state change (approve, retire, post to a scene, spend XP) gets its own POST URL and a
view built on [`core.actions.ObjectActionView`](../actions.py). Detail views render pages
and never handle POST; `core/tests/test_action_guard.py` enforces this and also forbids
views that pick an action from posted button names.

`ObjectActionView.post()` runs these steps in order:

1. `get_object()`: `get_object_or_404(get_queryset(), pk=kwargs[pk_url_kwarg])`.
2. `authorize()`: `can_see(subject)` (default `VIEW_FULL`) or 404, so a caller who may
   not see the object cannot tell it exists; then `has_permission(subject)` (default
   `permission`) or `PermissionDenied`. `get_permission_subject()` chooses the subject.
3. `get_form()`: binds `form_class` to `request.POST` and `request.FILES` if set; an
   invalid form goes to `form_invalid()`.
4. `perform(form)` inside `transaction.atomic()`, after re-reading the object with
   `select_for_update()` when `lock = True`. `perform` makes one service call and
   returns its result. A result with `success = False`, an `ActionFailed` or a
   `ValidationError` rolls back and goes to `action_failed()`.
5. `action_succeeded(result)`: flashes `result.message` or `success_message` (formatted
   with `object`) and redirects to `get_success_url(result)` (the object's URL by
   default).

On failure the error is flashed and the user is redirected to `get_failure_url()`, unless
`host_view_class` is set, in which case the originating page is re-rendered with the
bound form (`render_host()`, form under `host_form_context_name`). `fragment_response()`
is a hook for htmx partials; it is called first on every outcome, after authorization
and validation.

The route policy for action views is `ACTION`: the middleware answers non-POST requests
with 405 and anonymous ones with 401, and the action class does the object check.

```python
# characters/views/core/actions.py
class CharacterStatusView(ObjectActionView):
    model = Character
    lock = True
    target_status = None

    def perform(self, form):
        return change_character_status(self.object, self.target_status)


class CharacterDeceaseView(CharacterStatusView):
    target_status = "Dec"

    def has_permission(self, subject):
        return PermissionManager.user_has_scoped_editor_role(
            self.request.user, subject, request=self.request
        )
```

Action tests use `core.tests.action_audience.ActionAudienceMixin` (see
[testing](testing.md#helpers-for-other-apps)).

## Error views

[`views/errors.py`](../views/errors.py) is wired as `handler403`, `handler404` and
`handler500` in [`tg/urls.py`](../../tg/urls.py).

| Handler | Template | Notes |
|---------|----------|-------|
| `error_403` | `core/errors/403.html` | |
| `error_404` | `core/errors/404.html` | |
| `error_500` | `core/errors/500.html` | Rendered with `render_to_string` and no request, so no context processor or database query runs. `500.html` is a standalone page for the same reason |

401 pages come from `AuthErrorHandlerMiddleware` (see
[permissions and policies](permissions-and-policies.md#autherrorhandlermiddleware)).
The 401, 403 and 404 templates extend `core/errors/error.html`.

## See also

- [View mixins](mixins.md)
- [Permissions and policies](permissions-and-policies.md)
- [Adding a view](../../docs/guides/adding-a-view.md)
- [URL reference](../../docs/reference/urls.md)
- [`core/views/`](../views/)
