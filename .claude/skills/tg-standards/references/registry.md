# Item and location registry

Rules for adding or changing an item or location type. Items and locations do not have
hand-written CRUD views, URL lists or manifest entries: each routable model has one
`ModelSpec` in [`items/registry.py`](../../../../items/registry.py) or
[`locations/registry.py`](../../../../locations/registry.py), and
[`core/model_registry.py`](../../../../core/model_registry.py) builds the views and routes
from it. The walkthrough is
[docs/guides/adding-an-item-or-location-type.md](../../../../docs/guides/adding-an-item-or-location-type.md);
app detail is in [items/README.md](../../../../items/README.md) and
[locations/README.md](../../../../locations/README.md).

## What a `ModelSpec` declares

| Field | Meaning |
|-------|---------|
| `model_label` | `"items.Vessel"`; one spec per model (duplicates raise `ImproperlyConfigured`) |
| `slug` | URL and type-selection name (`"vessel"`); unique per `gameline` |
| `group` | URL group: the gameline URL module (`"mummy"`) or `"core"` |
| `gameline` | Gameline code (`"mtr"`), matching the model's `gameline` |
| `actions` | Exactly `detail`, `list`, `create`, `update`, each an `ActionSpec` |
| `fields` | Default form fields for create and update (explicit tuple) |
| `form_class` | Dotted path of a `ModelForm` used instead of `fields` |
| `templates` | Per action template; missing ones fall back to `core/registry/<action>.html` (`form` for create and update) |
| `model_urls` | URL name per action; `RegistryURLMixin` reverses these for `get_absolute_url`, `get_update_url`, `get_creation_url` |
| `label`, `list_title` | Menu label and list page title (default from `verbose_name`) |
| `dispatch_view` | Dotted path of a router used as the detail view (Chantry creation workflow) |

Each `ActionSpec`:

| Field | Meaning |
|-------|---------|
| `view_path` | Dotted name the built view is exported as (`items.views.mummy.VesselDetailView`) and the name route policy tests use |
| `policy` | Its route policy (a key of `POLICIES`); required, validated at import |
| `routes` | `(url name, path)` pairs inside the group's action namespace; `<pk>` is rewritten to `<int:pk>` |
| `options` | Class attributes for the built view (`fields`, `ordering`, `success_message`, `error_message`, `form_class`) |
| `custom` | Dotted path of a hand-written base class for behaviour the generic view lacks (`items.views.core.item._ItemCreateView`) |
| `form_updates` | Widget `attrs` and `help_text` changes applied to named form fields |

## Rules

- **Register every concrete `ItemModel` and `LocationModel` subclass**
  (`core/tests/test_model_registry.py::test_every_concrete_model_is_registered`).
- **Declare the policy on the `ActionSpec`, never in `core/route_policy_manifest.py`**:
  `OBJECT_DETAIL`, `OBJECT_LIST`, `OBJECT_CREATE`, `OBJECT_WRITE` for player objects;
  `PUBLIC_READ` / `STAFF_WRITE` for reference data. A view with both fails
  `test_route_policies`.
- **Field lists stay explicit** (`fields`, `options["fields"]` or a `form_class` with
  `Meta.fields`).
- **Keep route names and paths stable**; `core/tests/fixtures/model_routes.json` pins the
  existing ones.
- **Put custom behaviour in a `custom` base or a `form_class`**, in the app's `views/` or
  `forms/`, not in a parallel hand-written view and URL. The built view still runs
  `authorize_route` first: `RegistryViewMixin.dispatch()` authorizes with the loaded
  object before any custom `dispatch()`, so the middleware skips it.
- **Export built views** from the gameline view module
  (`VesselDetailView = registry.view("items.Vessel", "detail")`) so `view_path` imports.
- The model inherits `RegistryURLMixin` through `ItemModel` / `LocationModel`; do not
  define URL methods on it.

## What the registry adds for you

- `MessageMixin` on create and update (success and error messages, and
  `prepare_created_object` on create).
- `VisibilityFilterMixin` on `OBJECT_LIST` lists; `ordering = ["name"]` by default.
- `PermissionContextMixin` (`object_perms`) and the shared templates.
- Polymorphic detail dispatch: `GenericItemDetailView` / `GenericLocationDetailView`
  (`core.views.registry.RegistryDetailView`) resolve `/items/<pk>/` to the concrete
  type's detail view, authorizing it with the resolved object.
- The create menu (`ModelRegistry.menu(user)`) and `core:object_type_redirect` selection.

## Checklist

- [ ] One `ModelSpec`, four actions, a policy on each.
- [ ] Explicit fields or a form class; templates exist or fall back on purpose.
- [ ] `model_urls` names match `routes`; existing routes unchanged.
- [ ] Views exported under their `view_path`.
- [ ] Model has `type`, `gameline`, `verbose_name`; `tg_schema` migration for its table
  on existing databases ([schema-changes.md](schema-changes.md)).
- [ ] Tests: create assigns the owner, update denies another user, detail shows the
  public card to others (`core/tests/test_model_registry.py` covers the generic
  contract; add type-specific behaviour tests under `<app>/tests/`).

## See also

- [docs/guides/adding-an-item-or-location-type.md](../../../../docs/guides/adding-an-item-or-location-type.md)
- [`core/model_registry.py`](../../../../core/model_registry.py), [`core/registry_urls.py`](../../../../core/registry_urls.py)
- [items/README.md](../../../../items/README.md), [locations/README.md](../../../../locations/README.md)
- [permissions.md](permissions.md), [urls.md](urls.md)
