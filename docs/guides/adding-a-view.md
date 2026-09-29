# Adding a view

This guide is the procedure for adding a page or endpoint: choosing its route policy, the
mixins from `core.mixins`, fetching objects without extra queries, rendering a Spread template,
flashing messages, answering htmx fragment requests, caching (rarely), and the tests. It is for
developers and agents adding any routed view in `accounts`, `characters`, `core`, `game`,
`items` or `locations`. The authorization model behind it is in
[Authorization](../architecture/authorization.md); item and location CRUD views are declared in
their registries instead (see [Adding an item or location type](adding-an-item-or-location-type.md)).

## How a request is authorized

Two layers check every project view, in this order:

1. **The route policy.** `core.middleware.authorization.AuthorizationMiddleware.process_view`
   calls `core.access_policy.authorize_route` before the view runs. The policy comes from the
   view's own `access_policy` attribute (set by the item and location registries) or from its
   entry in [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py), keyed by
   `"<module>.<ClassName>"`. A view with no policy is denied (`PermissionDenied`), so a
   forgotten declaration fails closed instead of exposing a page. The middleware also answers
   404 to a `pk` URL argument that is not a positive integer.
2. **The view's mixins and code** check what the policy cannot: which form an editor gets,
   which rows a list shows, object rules of `game` and `accounts` views, and action
   permissions.

The policy lives in middleware so that one evaluator sees every URL and the manifest is the
single reviewed list of what each route allows.

## Prerequisites

- You know what the view shows or changes, for whom, and which object it acts on.
- You have read the policy table in
  [Authorization](../architecture/authorization.md#the-policies).

## Steps

### 1. Choose the kind of view and its policy

| The view... | Base and mixins | Policy |
|-------------|-----------------|--------|
| shows one player object (character, group, item, location, template) | `DetailView` (+ `ViewPermissionMixin`) | `OBJECT_DETAIL` |
| lists player objects | `VisibilityFilterMixin`, `ListView` | `OBJECT_LIST` |
| creates a player object | `MessageMixin`, `CreateView` (+ `ScopedCreationFormMixin` when the form has `chronicle`) | `OBJECT_CREATE` |
| edits a player object | `EditPermissionMixin`, `MessageMixin`, `UpdateView` (+ `ScopedEditFormMixin` for owner edits) | `OBJECT_WRITE` |
| edits a player object, storytellers only | as above | `OBJECT_ST_WRITE` |
| changes one object's state with a `POST` (approve, retire, post to a scene) | `core.actions.ObjectActionView` | `ACTION` |
| is a chargen step | see [Adding a chargen step](adding-a-chargen-step.md) | `CHARGEN_STEP` |
| dispatches to other views by object type or state | `core.views.generic.DictView` | `ROUTER` |
| reads reference data | `CachedDetailView` / `CachedListView` | `PUBLIC_READ` |
| writes reference data | `MessageMixin`, `CreateView` / `UpdateView` | `STAFF_WRITE` |
| is a `game` page (chronicles, scenes, stories, weeks, XP requests) | `StorytellerRequiredMixin`, `CharacterOwnerOrSTMixin` or `game.security` filters | `GAME` |
| is an `accounts` page | its own object checks | `ACCOUNT` |
| needs only a signed-in user | `LoginRequiredMixin` | `LOGIN` |

Answer 404 rather than 403 when the user may not learn that the object exists.
`ViewPermissionMixin` raises 404; `EditPermissionMixin` raises 403 (set
`raise_404_on_deny = True` on a subclass to hide the object instead); `ObjectActionView.authorize()` gives 404 when the
user cannot see the object and 403 when they can see it but may not act.

### 2. Pick the mixins

All live in [`core/mixins.py`](../../core/mixins.py). Import them from `core.mixins`.

| Mixin or function | Does |
|-------------------|------|
| `ViewPermissionMixin` | Requires `Permission.VIEW_FULL` on `get_object()`; 404 otherwise |
| `EditPermissionMixin` | Requires `Permission.EDIT_FULL`; 403 otherwise |
| `SpendFreebiesPermissionMixin` | Requires `Permission.SPEND_FREEBIES`; 403 otherwise |
| `PermissionRequiredMixin` | Base of the three above: set `required_permission` and `raise_404_on_deny` |
| `ScopedEditFormMixin` | `get_form_class()` returns the full form for a scoped editor (staff, the chronicle's head ST, or a storyteller for the chronicle and gameline) and `limited_form_class` for anyone else |
| `ScopedCreationFormMixin` | Limits a form's `chronicle` choices to `game.security.readable_chronicles(user)` |
| `VisibilityFilterMixin` | Filters the list queryset with `PermissionManager.filter_queryset_for_user`; warms `object_perms` for a paginated page |
| `MessageMixin` | `SuccessMessageMixin` + `ErrorMessageMixin`; for a `CreateView`, also runs `prepare_created_object` |
| `prepare_created_object(form, request)` | Sets the owner (or none when a storyteller posts `shared=1`), status `Un` for non-admins, and refuses a chronicle the user cannot read |
| `PermissionContextMixin` | Adds `object_perms` to the context |
| `ObjectCachingMixin` | Caches `get_object()` for the request |
| `StorytellerRequiredMixin` | Staff, or a storyteller for the target's chronicle and gameline (head ST for chronicle-wide targets) |
| `CharacterOwnerOrSTMixin` | Staff, or `VIEW_FULL` on the object's `character` |
| `OwnerRequiredMixin` | The object's owner (or `user`), or staff |
| `SpecialUserMixin` | `check_if_special_user(obj, user)`: `VIEW_FULL` |
| `SharedTemplateMixin` | Renders `template_name` if it exists, else `shared_template_name` |
| `ListHeadingMixin` | `list_title` and `list_heading` for the shared list pages |

Put mixins to the left of the Django base class. Decide object access in `PermissionManager`
([`core/permissions.py`](../../core/permissions.py)) through these mixins, an action's
`permission` or `has_permission`, or `game.security`; not in view bodies or templates.

### 3. Write the view

Fetch with `get_object_or_404` (or the generic view's `get_object`, which raises 404), and
load what the template uses in the same query:

```python
from django.views.generic import DetailView, ListView

from characters.models.vampire.coterie import Coterie
from core.mixins import ViewPermissionMixin, VisibilityFilterMixin


class CoterieRosterView(ViewPermissionMixin, DetailView):
    model = Coterie
    template_name = "characters/vampire/coterie/roster.html"

    def get_queryset(self):
        return super().get_queryset().select_related("leader", "chronicle")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = self.object.members.select_related("owner").order_by("name")
        return context


class CoterieRosterListView(VisibilityFilterMixin, ListView):
    model = Coterie
    template_name = "characters/vampire/coterie/roster_list.html"
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related("leader").prefetch_related("members")
```

(`CoterieRosterView` and `CoterieRosterListView` are illustrative.)

- `select_related` for foreign keys, `prefetch_related` for many-to-many and reverse relations.
- On a polymorphic queryset whose rows call subclass methods (`get_absolute_url`, `get_type`),
  call `.with_polymorphic_ctype()`; hydration then costs one query per concrete type.
- Keep queries out of templates: a per-row query in a loop is the N+1 pattern that
  [`core/tests/test_query_budgets.py`](../../core/tests/test_query_budgets.py) guards on sheets,
  the scene page and the indexes.
- List editable fields explicitly (`fields = [...]` or the form's `Meta.fields`); never
  `"__all__"`.
- Put rules in services (`characters/services/`, `core/services/`, `game/`) or models; the
  view authorizes, binds the form and renders.
- Never call `form_valid()` from `form_invalid()`
  ([`characters/tests/test_view_rules_guard.py`](../../characters/tests/test_view_rules_guard.py)).

### 4. State changes: one action, one endpoint

A detail view never handles `POST`, and no view picks an action from a posted button name.
[`core/tests/test_action_guard.py`](../../core/tests/test_action_guard.py) fails on
`"approve" in request.POST`-style checks and on routed `DetailView`s that define `post()`.
Each state change is an `ObjectActionView` ([`core/actions.py`](../../core/actions.py)):

```python
from characters.models.core import Character
from characters.services.willpower import restore_willpower  # illustrative service
from core.actions import ObjectActionView
from core.permissions import Permission


class CharacterRestoreWillpowerView(ObjectActionView):
    """A storyteller restores the character's temporary Willpower."""

    model = Character
    lock = True
    permission = Permission.EDIT_FULL

    def perform(self, form):
        return restore_willpower(self.object)
```

`ObjectActionView.post()` loads the object (404 if missing), checks `VIEW_FULL` (404) and then
`permission` or `has_permission(subject)` (403), validates `form_class` if set, runs
`perform()` inside `transaction.atomic()` (after `select_for_update()` when `lock = True`),
flashes `result.message` or `success_message`, and redirects to the object's
`get_absolute_url()`. A result with `success=False` (such as
`characters.services.result.ServiceResult.fail(...)`) or a raised `ActionFailed` /
`ValidationError` flashes the error and redirects to `get_failure_url()` (by default the same
object page); set `host_view_class` to re-render the originating page with the bound form
instead. Real examples:
`characters.views.core.actions.CharacterRetireView`, `game.actions.SceneCloseView`.

Declare it `ACTION` and route it under the object:

```python
path("<int:pk>/restore-willpower/", CharacterRestoreWillpowerView.as_view(), name="restore_willpower"),
```

```django
<form method="post" action="{% url 'characters:restore_willpower' object.pk %}">
    {% csrf_token %}
    <button type="submit" class="tl-btn">Restore Willpower</button>
</form>
```

Show the form only when `object_perms` says the user may act (`object_perms.can_edit` here).

### 5. Route and declare the policy

- Add the URL to the app's URL module. Use `<int:pk>` and a name inside the app's namespaces
  (`characters:vampire:update:clan`, `game:story:detail`); see
  [URL reference](../reference/urls.md).
- Add the dotted view path to its group in
  [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py), keeping the group
  sorted. Every view a `DictView` can hand off to needs a policy too, including its
  `default_redirect` class.
- [`core/tests/security/test_route_policies.py`](../../core/tests/security/test_route_policies.py)
  fails when a routed view, or a router branch, has no policy or has two.

### 6. Template

- Extend a Spread shell: `core/tl_base.html` for pages, `core/form.html` for forms,
  `core/object.html` or an app shell (the character sheet, `characters/tl/ref2_detail.html`,
  `locations/core/location/detail.html`, ...). No Bootstrap, jQuery or `tg-card` markup.
- Set `{% block gameline %}{{ object|gameline_code }}{% endblock %}` for gameline theming.
- `{% load tl sanitize_text %}`; render fields with
  `{% include "core/tl/field.html" with field=form.x %}`, ratings with `{% dots %}`, tracks
  with `{% track %}`, cover facts with `{% fact %}`.
- Escape user text: `|sanitize_html` for rich text, never `|safe`.
- No inline `style="..."`, `<style>` block or inline script; CSS goes in
  `core/static/core/tl/tl.css`, JavaScript in `<app>/static/<app>/js/`
  ([`core/tests/test_template_policy.py`](../../core/tests/test_template_policy.py) ratchets
  inline styles and style blocks).
- Read permissions from `object_perms` (`can_view_full`, `can_edit`, `can_edit_limited`,
  `can_spend_xp`, `can_approve`, `is_owner`, `is_scoped_st`, `can_chargen`, ...; see
  [`core/permission_context.py`](../../core/permission_context.py)), not from role checks.
  `PermissionContextMixin` adds it, and `AuthorizationMiddleware.process_template_response`
  adds it to any `TemplateResponse` whose context has a permission-controlled `object`.

See [Front end](../architecture/frontend.md) and [Template tags](../reference/template-tags.md).

### 7. Messages

Use Django's messages framework. `core/tl_base.html` includes `core/tl/messages.html` on every
page. `MessageMixin` flashes `success_message` (formatted with the saved object's `name`, `id`,
`pk`, `model_name`, `model_name_plural`) and `error_message`; `ObjectActionView` flashes the
service result.

### 8. htmx fragments

A view that answers htmx with a partial uses the helpers in [`core/htmx.py`](../../core/htmx.py):

| Helper | Use |
|--------|-----|
| `is_fragment_request(request)` | True for an `HX-Request` that is neither a history restore nor boosted; those swap the whole page and must get a full page |
| `mark_fragment(response, kind)` | Sets `TG-Fragment: <kind>` so the client's swap guard knows what it received |
| `vary_on_htmx(response)` | Adds `Vary` on `HX-Request`, `HX-History-Restore-Request` and `HX-Boosted`, so no cache serves a fragment for a page or the reverse |
| `hx_redirect(url)` | A 200 with `HX-Redirect`, making htmx navigate the whole page (a 3xx would be followed inside the request) |
| `trigger(response, event, detail, header=...)` | Adds a client event with JSON detail to `HX-Trigger` (or `HX-Trigger-After-Swap`) |

Vary every response of the view, full page or fragment, as
`game.views.SceneDetailView.render_to_response` does:

```python
def render_to_response(self, context, **response_kwargs):
    response = vary_on_htmx(super().render_to_response(context, **response_kwargs))
    if self.is_posts_fragment():
        response.template_name = self.fragment_template_name
        mark_fragment(response, "scene-posts")
    return response
```

The fragment is served by the same URL and the same authorization as the page. Keep a no-script
path: the same URL must work as a plain form post or link.

### 9. Caching

Cache a full page only if it is public (`PUBLIC_READ` or `PUBLIC_INDEX`) and the same for every
viewer apart from the nav. Use `CachedDetailView` / `CachedListView` or
`@method_decorator(cache_page_per_visitor(timeout), name="dispatch")` from
[`core/cache.py`](../../core/cache.py); never Django's `cache_page`, which would serve one
visitor's page (nav, messages, Edit links) to the next. Mark any per-viewer section of a cached
page `Cache-Control: private`, as `KnownByMixin` does. Never cache an `OBJECT_*`, `GAME`,
`ACCOUNT` or `LOGIN` view. Details: [Caching](../architecture/caching.md).

## Tests

- **Security, for every new route**: each audience gets the right status. For object views and
  actions, `core.tests.action_audience.ActionAudienceMixin` creates the owner, another player,
  a storyteller of the chronicle and gameline, one of another gameline, one of another
  chronicle, staff and anonymous; see the status tables in
  [`characters/tests/views/test_character_actions.py`](../../characters/tests/views/test_character_actions.py).
  Test that hidden objects give 404, `GET` on an action gives 405, and the object is unchanged
  after a denied request.
- **Behaviour**: the page renders the right context; the action's service result reaches the
  user; invalid input changes nothing.
- **Queries**: for a page that lists rows, assert the query count does not grow with the rows
  (`django.test.utils.CaptureQueriesContext`), as `test_query_budgets.py` does.
- **htmx**: a fragment request gets `TG-Fragment` and `Vary`; a history-restore request gets
  the full page (see `test_history_restore_and_boosted_requests_get_full_pages` in
  [`characters/tests/views/test_chargen_htmx.py`](../../characters/tests/views/test_chargen_htmx.py)).
- The route-policy test, the routed-templates test (every template a routed view names, and its
  extends and includes, exists) and the action and view-rule guards cover the new view
  automatically.

Put tests in `<app>/tests/`, mirroring the source path. See [Testing](../development/testing.md).

## Checklist

- [ ] One policy for the view, the narrowest that fits, in the manifest (or the registry).
- [ ] Mixins from `core.mixins`; object rules in `PermissionManager`, not the view body.
- [ ] 404 for objects the user may not see.
- [ ] `get_object_or_404` / `get_object`, `select_related` / `prefetch_related`, no per-row
  queries in the template.
- [ ] Explicit field lists; limited form for owner edits.
- [ ] No `post()` on detail views; each state change is an `ObjectActionView` with `ACTION`.
- [ ] Spread template: shell, `gameline` block, `tl` tags, no inline styles, `object_perms`.
- [ ] htmx responses varied and marked; a no-script path exists.
- [ ] Caching only on public pages, only with `cache_page_per_visitor`.
- [ ] Security and behaviour tests.

## See also

- [Authorization](../architecture/authorization.md)
- [Caching](../architecture/caching.md)
- [Front end](../architecture/frontend.md)
- [URL reference](../reference/urls.md)
- [`core/mixins.py`](../../core/mixins.py)
- [`core/actions.py`](../../core/actions.py)
