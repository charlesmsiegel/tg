# Adding an item or location type

This guide covers adding a new item model (a subclass of `ItemModel`) or location model (a
subclass of `LocationModel`): the model, its declaration in the app's registry (which builds the
views, URLs and route policies), optional custom views and forms, templates, admin, schema and
tests. It is for developers and agents working in [`items/`](../../items/) or
[`locations/`](../../locations/). The item and location trees are described in
[Data model](../architecture/data-model.md).

The running example adds a Demon: the Fallen item `Sigil`. It is illustrative; nothing named
`Sigil` exists. The closest real examples are `items.Relic`
([`items/models/demon/relic.py`](../../items/models/demon/relic.py)) and, for locations,
`locations.Bastion` ([`locations/models/demon/bastion.py`](../../locations/models/demon/bastion.py)).
A location type follows the same steps with `locations/` paths and `LocationModel`.

## How the registry works

Items and locations do not declare views, URLs or route policies one by one. Each app has one
registry, [`items/registry.py`](../../items/registry.py) and
[`locations/registry.py`](../../locations/registry.py), a `core.model_registry.ModelRegistry`
holding one `ModelSpec` per routable model ([`core/model_registry.py`](../../core/model_registry.py)):

| `ModelSpec` field | Meaning |
|-------------------|---------|
| `model_label` | `"items.Sigil"` |
| `slug` | The type's name in the create menus and `core.create_redirects`; unique per gameline (`items.Relic` uses `demon_relic`) |
| `group` | The URL group: the gameline's `app_name` (`demon`) or `core` |
| `gameline` | A `settings.GAMELINES` key; the create menu groups by it |
| `actions` | Exactly `detail`, `list`, `create` and `update`, each an `ActionSpec` |
| `fields` | Form fields for create and update when there is no `form_class` or per-action `fields` |
| `form_class` | Dotted path of a `ModelForm` used for create and update |
| `templates` | Per action: `detail`, `list`, `create`, `update` |
| `label`, `list_title` | Menu label and list-page title (default: the model's verbose names) |
| `model_urls` | Per action, the URL name `RegistryURLMixin` reverses |
| `dispatch_view` | Dotted path of a view that replaces the detail view in the generic `items:item` / `locations:location` router (a workflow router such as `ChantryCreationView`) |

| `ActionSpec` field | Meaning |
|--------------------|---------|
| `view_path` | Dotted path the view is exported under (`items.views.demon.sigil.SigilDetailView`); route policies are keyed by it |
| `policy` | The route policy; must be a key of `core.route_policy_manifest.POLICIES` |
| `routes` | `(url name, path)` pairs, relative to the group's `create/`, `update/`, `list/` or detail include |
| `options` | Class attributes for the generated view (`fields`, `ordering`, `success_message`, `error_message`, `form_class`, ...) |
| `custom` | Dotted path of a hand-written base class for this action (see [step 4](#4-custom-behaviour-optional)) |
| `form_updates` | Per field, widget `attrs` and `help_text` applied in `get_form()` |

`registry.view(model, action)` builds the class
`type(<name from view_path>, (RegistryViewMixin, [MessageMixin], [VisibilityFilterMixin], base), attrs)`:

- `RegistryViewMixin.dispatch()` loads the object for detail and update and runs
  `authorize_route` itself, with the policy set as the class's `access_policy` (the middleware
  skips these views so the object is loaded once).
- The base is `custom` if given, else Django's `DetailView`, `ListView`, `CreateView` or
  `UpdateView`. Create and update views get `MessageMixin` (and `prepare_created_object` on
  create); `OBJECT_LIST` lists get `VisibilityFilterMixin`.
- Templates resolve through `core.template_resolution.shared_template_names`: the declared
  template if it exists, else [`core/templates/core/registry/`](../../core/templates/core/registry/)
  `detail.html`, `list.html` or `form.html`.
- The class is also placed in its `view_path` module if that module does not define the name.

The gameline URL modules (`items/urls/<group>/create.py` and so on) are one line each,
`urls = registry.urls("<group>", "<action>")`, so a new entry is routed without editing them.
`RegistryURLMixin` ([`core/registry_urls.py`](../../core/registry_urls.py)), a base of
`ItemModel` and `LocationModel`, gives every model `get_absolute_url`, `get_update_url` and
`get_creation_url` from `model_urls`.

## Prerequisites

- The gameline has a URL group under `items/urls/<app_name>/` (every gameline in
  `core.constants.GameLine.URL_PATTERNS` has one) and a views package `items/views/<app_name>/`.
- You know whether the type is a player object (owned, approved: `OBJECT_*` policies) or
  shared reference data (`PUBLIC_READ` reads, `STAFF_WRITE` writes, as `items.Material` and
  `items.Medium`).

## Steps

### 1. Model

`items/models/demon/sigil.py`:

```python
from django.db import models

from items.models.core import ItemModel


class Sigil(ItemModel):
    """A mark of power carved by one of the Fallen."""

    type = "sigil"
    gameline = "dtf"

    house = models.ForeignKey(
        "characters.DemonHouse",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sigils",
    )
    potency = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Sigil"
        verbose_name_plural = "Sigils"
        ordering = ["name"]
```

- `ItemModel` ([`items/models/core/item.py`](../../items/models/core/item.py)) adds
  `owned_by` (characters) and `located_at` (locations) to the `core.models.Model` fields.
  `LocationModel` ([`locations/models/core/location.py`](../../locations/models/core/location.py))
  adds `parent`, `contained_within`, `owned_by`, `gauntlet`, `shroud`, `dimension_barrier` and
  `creation_status`.
- Set a unique `type` and a `gameline`. Give new fields defaults or `null=True`.
- Do not write URL methods; `RegistryURLMixin` supplies them.
- Export the model from `items/models/demon/__init__.py`.

A new model is a new table: add a `tg_schema` migration for existing databases
([Changing the schema](changing-the-schema.md#a-new-table)).

### 2. Registry entry

Add a `ModelSpec` to the list in [`items/registry.py`](../../items/registry.py), next to its
gameline's other entries:

```python
ModelSpec(
    model_label="items.Sigil",
    slug="sigil",
    group="demon",
    gameline="dtf",
    label="Sigil",
    actions={
        "detail": ActionSpec(
            view_path="items.views.demon.sigil.SigilDetailView",
            policy="OBJECT_DETAIL",
            routes=[("sigil", "sigil/<int:pk>/")],
        ),
        "list": ActionSpec(
            view_path="items.views.demon.sigil.SigilListView",
            policy="OBJECT_LIST",
            options={"ordering": ["name"]},
            routes=[("sigil", "sigils/")],
        ),
        "create": ActionSpec(
            view_path="items.views.demon.sigil.SigilCreateView",
            policy="OBJECT_CREATE",
            options={
                "success_message": "Sigil '{name}' created successfully!",
                "error_message": "Failed to create sigil. Please correct the errors below.",
            },
            routes=[("sigil", "sigil/")],
        ),
        "update": ActionSpec(
            view_path="items.views.demon.sigil.SigilUpdateView",
            policy="OBJECT_WRITE",
            options={
                "success_message": "Sigil '{name}' updated successfully!",
                "error_message": "Failed to update sigil. Please correct the errors below.",
            },
            routes=[("sigil", "sigil/<int:pk>/")],
        ),
    },
    model_urls={
        "detail": "items:demon:sigil",
        "update": "items:demon:update:sigil",
        "create": "items:demon:create:sigil",
        "list": "items:demon:list:sigil",
    },
    fields=("name", "description", "house", "potency"),
    templates={
        "detail": "items/demon/sigil/detail.html",
        "list": "items/demon/sigil/list.html",
        "create": "items/demon/sigil/form.html",
        "update": "items/demon/sigil/form.html",
    },
),
```

- The policy goes here and only here: never add a registry view to
  `core/route_policy_manifest.py` (`test_every_project_route_and_router_target_has_one_policy`
  fails on "Policy has two sources").
- Player objects: `OBJECT_DETAIL`, `OBJECT_LIST`, `OBJECT_CREATE`, `OBJECT_WRITE`
  (`OBJECT_ST_WRITE` for a storyteller-only form). Reference data: `PUBLIC_READ` for detail
  and list, `STAFF_WRITE` for create and update.
- List fields explicitly; never list `owner`, `chronicle`, `status` or the other fields the
  write policies refuse from non-staff users (see
  [Authorization](../architecture/authorization.md#the-policies)).
- `ModelRegistry.__init__` raises `ImproperlyConfigured` for a missing action, an unknown or
  missing policy, a duplicate model, a duplicate `(gameline, slug)`, or a duplicate route name
  or path within a group and action.

### 3. Export the views

Create `items/views/demon/sigil.py` so the dotted paths resolve, the same way
[`items/views/demon/relic.py`](../../items/views/demon/relic.py) does:

```python
from items.registry import registry

SigilDetailView = registry.view("items.Sigil", "detail")
SigilListView = registry.view("items.Sigil", "list")
SigilCreateView = registry.view("items.Sigil", "create")
SigilUpdateView = registry.view("items.Sigil", "update")
```

and re-export them from `items/views/demon/__init__.py`.

### 4. Custom behaviour (optional)

When the generated view is not enough, write a base class in the same module and name it in
`ActionSpec.custom`. The registry still adds `RegistryViewMixin` (and `MessageMixin`) and still
enforces the policy. Existing uses:

| Need | Example |
|------|---------|
| Owners edit a limited form, scoped editors the full one | `items.views.vampire._VampireArtifactUpdateView` (`get_form_class()` with `PermissionManager.user_has_scoped_editor_role`), `items.views.core.item._ItemUpdateView` with `LimitedItemEditForm` |
| Extra detail context | `items.views.mage.wonder._WonderDetailView` |
| A creation wizard for a location | `locations.views.mage.chantry.ChantryCreationView` as `dispatch_view` |

A form with custom widgets or validation goes in `items/forms/<app_name>/` and is named in
`ModelSpec.form_class` (whole model) or `options["form_class"]` (one action), as
`items.forms.vampire.artifact.VampireArtifactForm` is. Use Spread-compatible widgets (no
Bootstrap classes); `form_updates` covers placeholders and help texts without a form class.

### 5. Templates

Create `items/templates/items/demon/sigil/`. Any template you do not write falls back to the
shared registry template, so you can start with none and add them as the page needs.

| File | Extends | Blocks to fill |
|------|---------|----------------|
| `detail.html` | `items/core/item/detail.html` | `cover_sub`, `cover_facts`, `cover_stats`, `model_specific`, `additional_stats`, `post_content` |
| `form.html` | `items/tl/form.html` | `creation_title`, `contents` (fields in `.tl-formgrid` via `core/tl/field.html`, checkboxes via `core/misc/check.html`) |
| `list.html` | `items/tl/list.html` | `title`, `gameline`, `eyebrow`, `heading`, `columns`, `row`, `create_action`, `empty` |

For a location: `locations/core/location/detail.html` (`type_facts`, `model_specific`,
`additional_content`, ...), `locations/core/location/form.html` (`creation_title`,
`form_line`, `other`) and `locations/core/tl_list.html` (`list_head`, `list_cells`, `empty`),
as [`locations/templates/locations/demon/bastion/`](../../locations/templates/locations/demon/bastion/)
does. Section markup and helpers (`{% trait %}`, `locations/tl/stat.html`, `.tl-kv`) are
described in each shell's header comment. Follow the Spread rules: no inline styles or
Bootstrap, `object_perms` for controls; see [Front end](../architecture/frontend.md).

### 6. Admin

Register the model in [`items/admin.py`](../../items/admin.py) (or
[`locations/admin.py`](../../locations/admin.py)):

```python
@admin.register(Sigil)
class SigilAdmin(admin.ModelAdmin):
    list_display = ("name", "house", "potency")
    list_filter = ("house",)
```

### 7. Menus and seed data

The "new item" and "new location" pickers (`items.forms.core.item_creation.ItemCreationForm`,
`locations.forms.core.location_creation.LocationCreationForm`) list `registry.menu(user)`: every entry with a create
action, all gamelines for staff and storytellers and Mage only for other users, and entries
whose create policy is `STAFF_WRITE` only for staff. The chosen slug resolves through
`registry.resolve()` and `registry.selection_url()`, so no `game.models.ObjectType` row is
needed. Canonical rows of a reference-style type go in a `populate_db` script (see
[Adding reference data](adding-reference-data.md#8-seed-data)).

## Tests

| What | Where |
|------|-------|
| Every concrete `ItemModel` / `LocationModel` is registered; every action has a policy; create and update views have success and error messages | [`core/tests/test_model_registry.py`](../../core/tests/test_model_registry.py) (automatic) |
| Existing route names and paths are unchanged | `test_existing_routes_keep_names_and_paths` against [`core/tests/fixtures/model_routes.json`](../../core/tests/fixtures/model_routes.json) (automatic; new routes are allowed) |
| Every route has one policy | [`core/tests/security/test_route_policies.py`](../../core/tests/security/test_route_policies.py) (automatic) |
| Detail and edit pages render for the fixture storyteller | [`core/tests/test_template_render_smoke.py`](../../core/tests/test_template_render_smoke.py) with `core.tests.template_fixtures.seed()` (automatic; the model must be creatable with generic values) |
| Owner creates and becomes owner; another user cannot update (403); a hidden object shows the public card; a player cannot change `status` | `items/tests/views/demon/test_sigil.py`; patterns in `test_create_assigns_owner_and_update_denies_other_user` and [`locations/tests/views/test_authorization.py`](../../locations/tests/views/test_authorization.py) |
| Model defaults and `clean()` rules | `items/tests/models/demon/test_sigil.py` |
| A custom view's extra behaviour | next to the view's tests |
| The `tg_schema` migration | `tg_schema/tests/test_<name>.py` |

## Checklist

- [ ] Model subclasses `ItemModel` or `LocationModel`; unique `type`; `gameline`; `Meta`;
  defaults on new fields; exported.
- [ ] `tg_schema` migration and test for the new table.
- [ ] `ModelSpec` with all four actions, policies, routes, `model_urls` and an explicit field
  list; no manifest entry.
- [ ] View module exporting the four `registry.view(...)` classes; re-exported.
- [ ] Custom base or form only where the generated view is not enough; owners get a limited
  form where they should.
- [ ] Templates on the item or location shells, or the registry fallbacks.
- [ ] Admin registration.
- [ ] Security, model and view tests.

## See also

- [Data model](../architecture/data-model.md)
- [Authorization](../architecture/authorization.md)
- [Adding a view](adding-a-view.md)
- [Changing the schema](changing-the-schema.md)
- [`items/README.md`](../../items/README.md)
- [`locations/README.md`](../../locations/README.md)
