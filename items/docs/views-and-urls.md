# Item views and URLs

This page explains how the `items` app turns its registry into views and URL patterns,
which access policy guards each action, which views carry custom behaviour, and the
full list of item URLs. It is for developers adding or changing an item page and for
agents that need to link to or call one.

## The registry

Source: [`items/registry.py`](../registry.py), built on
[`core/model_registry.py`](../../core/model_registry.py).

`items.registry.registry` is a `ModelRegistry("items", [...])` holding one `ModelSpec`
per routable model. A spec declares:

| `ModelSpec` field | Meaning |
|-------------------|---------|
| `model_label` | `"items.<Model>"` |
| `slug` | Unique type key within its gameline, used by the create menu (`ItemCreationForm`) and `ModelRegistry.resolve()` |
| `group` | URL group: `core` or a gameline folder (`mage`, `vampire`, ...) |
| `gameline` | Gameline code shown on covers and used by the create menu |
| `label`, `list_title` | Menu label and list-page title (defaults: the model's verbose names) |
| `actions` | Exactly `detail`, `list`, `create` and `update`, each an `ActionSpec` |
| `fields` | Model fields for the generated create/update form when no form class is set |
| `form_class` | Dotted path of a form class used for create and update |
| `templates` | Template per action; missing actions fall back to `core/registry/<action>.html` |
| `model_urls` | URL name per action, used by `get_absolute_url()`, `get_update_url()`, `get_creation_url()` and the list link |

Each `ActionSpec` declares:

| `ActionSpec` field | Meaning |
|--------------------|---------|
| `view_path` | Public dotted path of the view class, for example `items.views.mage.wonder.WonderCreateView` |
| `policy` | Access policy name from `core.route_policy_manifest.POLICIES` |
| `custom` | Optional dotted path of a hand-written base view (by convention an underscore class next to the public name) |
| `options` | Class attributes for the generated view (`fields`, `form_class`, `ordering`, `success_message`, `error_message`, ...) |
| `routes` | `(url_name, path)` pairs, relative to the action's URL include |
| `form_updates` | Per-field widget `attrs` and `help_text` applied in `get_form()` |

`ModelRegistry.__init__` validates the declarations at import time and raises
`ImproperlyConfigured` when an entry lacks one of the four actions, repeats a model or
a `(gameline, slug)` pair, names an unknown policy, or repeats a route name or path
within a group and action.

### How views are built

`registry.view(model, action)` returns the view class for an action, building it on
first use. The view modules under [`items/views/`](../views/) do nothing but bind
these classes to their public names, for example:

```python
# items/views/mage/charm.py
CharmDetailView = registry.view("items.Charm", "detail")
```

The generated class is `RegistryViewMixin` + (`MessageMixin` for create/update) +
(`VisibilityFilterMixin` for lists with the `OBJECT_LIST` policy) + the base view:
the `custom` class when one is declared, otherwise Django's `DetailView`, `ListView`,
`CreateView` or `UpdateView`. The builder also:

- sets `model`, `access_policy`, and the spec's `options` as class attributes;
- uses `form_class` when the action or the spec names one, otherwise `fields` from
  the action options or the spec;
- defaults the success and error messages to "<Verbose name> '{name}' created/updated
  successfully!" and "Failed to create/update <verbose name>. ...";
- orders lists by `name` unless the action sets `ordering`.

`RegistryViewMixin.dispatch()` evaluates the declared policy with
`core.access_policy.authorize_route()` before any custom logic runs, resolving the
object once for `detail` and `update`. The authorization middleware skips registry
views for that reason, so the check happens exactly once. On create,
`RegistryViewMixin.form_valid()` calls `core.mixins.prepare_created_object()`, which
requires a logged-in user, checks the chosen chronicle is readable, sets `owner` to
the user (or leaves it empty when a storyteller or admin posts `shared=1`) and sets
`status` to `Un` for everyone except admins.

## Access policies

Every item action names one of these policies. The evaluator is
`core.access_policy.authorize_route()`; see
[authorization](../../docs/architecture/authorization.md) for the full model.

| Policy | Used by | Effect |
|--------|---------|--------|
| `OBJECT_DETAIL` | Detail of every item type | Users with `VIEW_FULL` on the object see the page. Others get the public projection (`core/public_object_detail.html`: name, public info and an approved image) on GET, and a 404 on other methods. |
| `OBJECT_LIST` | List of every item type | Staff and superusers see the per-type list, filtered by `VisibilityFilterMixin`. Everyone else gets the shared public list (`core/public_object_list.html`) on GET. |
| `OBJECT_CREATE` | Create of every item type | Login required; anonymous users get a 401 response. |
| `OBJECT_WRITE` | Update of every item type | Requires `EDIT_FULL` (403 otherwise). For non-staff POSTs, changing `owner`, `chronicle`, `gameline`, `status`, `npc`, `xp`, `freebies_approved`, `approved` or `approved_by` is refused. |
| `PUBLIC_READ` | `Material` and `Medium` detail and list | Anyone, logged in or not. |
| `STAFF_WRITE` | `Material` and `Medium` create and update | Login and staff (or superuser) required. |
| `PUBLIC_INDEX` | `ItemIndexView` (declared in the route manifest) | Anyone; the view itself decides what to show. |
| `ROUTER` | `GenericItemDetailView` (declared in the route manifest) | Anyone; the router authorizes the resolved object itself. |

Because non-staff users always receive the public list, the per-type list templates
(for example `items/mummy/relic/list.html`) are only ever rendered for staff.

## Polymorphic detail routing

`/items/<pk>/` (URL name `items:item`) is `GenericItemDetailView`
([`items/views/core/__init__.py`](../views/core/__init__.py)), a
`core.views.registry.RegistryDetailView`. It:

1. loads the `ItemModel` row (polymorphic, so it is the concrete subclass);
2. looks up that class in `registry.detail_views` (every registered `ItemModel`
   subclass; `Material` and `Medium` are excluded because they are not items) and
   returns 404 for an unregistered type;
3. authorizes the type's registry detail view against the object (so a user without
   `VIEW_FULL` gets the public projection);
4. renders the type's detail view with the object already resolved.

Most item types use `items:item` as their `get_absolute_url()` target, so links to an
item go through this router. The per-type detail routes (for example
`/items/mage/charm/<pk>/`) render the same view directly.

## Creating an item from a menu

Creation starts from a type chooser rather than a per-type link:

1. `items.forms.core.ItemCreationForm` lists the gameline and item type choices from
   `registry.menu(user)` (see [forms](forms.md#itemcreationform)).
2. The form submits with GET to `core:object_type_redirect` with `kind="item"` and
   `action="create"` (`/types/item/create/`), implemented by
   `core.views.object_type_redirect.ObjectTypeRedirectView`.
3. That view calls `core.create_redirects.resolve_object_type_url("obj", item_type,
   "create", gameline)`, which resolves the slug through `registry.resolve()` and
   redirects to `registry.selection_url()`: the create route whose URL name equals the
   slug when there is one, otherwise the model's `model_urls["create"]`.

`registry.menu(user)` returns nothing for anonymous users. Staff, superusers and
storytellers (`user.profile.is_st()`) see every type; other players see only Mage
(`mta`) types. Types whose create policy is `STAFF_WRITE` (`Material`, `Medium`) are
listed only for staff and superusers.

## The staff index

`/items/index/` (URL name `items:index`) is `ItemIndexView`
([`items/views/core/__init__.py`](../views/core/__init__.py)).

- Staff and superusers get `items/index.html`: one chronicle at a time (`?chronicle=<pk>`
  or `?chronicle=none`; default: the first chronicle that has items), optionally
  narrowed to one gameline (`?line=<code>`). Items come from
  `ItemModel.objects.visible()` and are grouped into tables in this order: Wonders
  (every Mage item except grimoires), Grimoires, Fetishes & Talens (all Werewolf
  items), each other gameline, then Weapons and Other items (generic items whose `type`
  does or does not contain "weapon"). The helpers are `item_group()` and
  `group_items()`.
- Everyone else gets the shared public list of items (`render_public_object_list`),
  with the creation form in the context when logged in.

## Custom views

These view classes carry behaviour beyond the generated CRUD. Each is wrapped by the
registry, so the declared policy still applies first.

| Class | Module | Behaviour |
|-------|--------|-----------|
| `_ItemCreateView` | [`views/core/item.py`](../views/core/item.py) | Login required; adds placeholders. The owner is set only by `prepare_created_object()` (the creator, or none for a storyteller's shared item) |
| `_ItemUpdateView` | [`views/core/item.py`](../views/core/item.py) | `EditPermissionMixin`. Users with a scoped editor role (`PermissionManager.user_has_scoped_editor_role`: roles `ADMIN`, `CHRONICLE_HEAD_ST` or `CHRONICLE_ST` for the item) get the full form (`name`, `description`); other editors, such as the owner, get `LimitedItemEditForm` |
| `_VampireArtifactCreateView` | [`views/vampire/__init__.py`](../views/vampire/__init__.py) | Form is `VampireArtifactForm`; the owner comes from `prepare_created_object()` as for other items |
| `_VampireArtifactUpdateView` | [`views/vampire/__init__.py`](../views/vampire/__init__.py) | Scoped editors get `VampireArtifactForm`; other editors get `LimitedVampireArtifactEditForm` (`description`, `history`) |
| `_WonderCreateView` | [`views/mage/wonder.py`](../views/mage/wonder.py) | `WonderForm` chooses the concrete class (Charm, Artifact or Talisman) only after validation, so the view builds `form.instance` with `form.save(commit=False)` before calling `prepare_created_object()` |
| `_WonderDetailView`, `_ArtifactDetailView`, `_CharmDetailView`, `_PeriaptDetailView`, `_TalismanDetailView` | [`views/mage/`](../views/mage/) | Add `resonance`: the item's `WonderResonanceRating` rows ordered by Resonance name |
| `_GrimoireDetailView` | [`views/mage/grimoire.py`](../views/mage/grimoire.py) | Adds the practices, instruments, abilities, spheres and rotes lists, the faction's paradigms, `faction_chain` (the faction and its parents, outermost first), `year` (`abs(date_written)`) and `contents` |

`grimoire_contents(rank, is_primer, practices, spheres, abilities, rotes)` in
[`views/mage/grimoire.py`](../views/mage/grimoire.py) turns the `Grimoire.has_rotes()`
rule into the header numbers, a state (`complete`, `under` or `over`) and one cell per
slot in `CONTENTS_ORDER` (Primer, Practices, Spheres, Abilities, Rotes). Cells past
`rank + 3` are marked `over`.

## URL patterns

[`items/urls/__init__.py`](../urls/__init__.py) is included at `/items/` under the
`items` namespace ([`tg/urls.py`](../../tg/urls.py)). It adds, in order:

1. one include per gameline from `core.constants.GameLine.URL_PATTERNS`
   (`vampire/`, `werewolf/`, `mage/`, `wraith/`, `changeling/`, `demon/`, `mummy/`,
   `hunter/`), each under the namespace of the same name;
2. `create/`, `update/` and `list/` includes for the `core` group (namespaces
   `create`, `update`, `list`);
3. `index/` (`items:index`);
4. the `core` detail routes and the router `<int:pk>/` (`items:item`).

Each gameline package ([`items/urls/mage/__init__.py`](../urls/mage/__init__.py) and
siblings) nests `create/`, `update/` and `list/` includes and its detail routes. Every
leaf module asks the registry for its routes, for example
`registry.urls("mage", "create")`.

URL names follow one pattern. For a route named `<name>` in group `<group>`:

| Action | URL name | Path prefix |
|--------|----------|-------------|
| detail | `items:<group>:<name>` | `/items/<group>/` |
| list | `items:<group>:list:<name>` | `/items/<group>/list/` |
| create | `items:<group>:create:<name>` | `/items/<group>/create/` |
| update | `items:<group>:update:<name>` | `/items/<group>/update/` |

For the `core` group, drop `<group>:` from the name and `<group>/` from the path (for
example `items:create:weapon` at `/items/create/weapon/`).

### Every item route

Paths are relative to `/items/`. All non-reference types use `OBJECT_DETAIL`,
`OBJECT_LIST`, `OBJECT_CREATE` and `OBJECT_WRITE`; `Material` and `Medium` use
`PUBLIC_READ` and `STAFF_WRITE`. `ItemModel` itself has no per-type detail route; its
detail is reached through `items:item`.

### `core`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `ItemModel` | `item` | `item` | — | `list/item/` | `create/item/` | `update/item/<pk>/` | `items:item` |
| `Material` | `material` | `material` | `material/<pk>/` | `list/material/` | `create/material/` | `update/material/<pk>/` | `items:material` |
| `Medium` | `medium` | `medium` | `medium/<pk>/` | `list/medium/` | `create/medium/` | `update/medium/<pk>/` | `items:medium` |
| `MeleeWeapon` | `melee_weapon` | `melee_weapon` | `melee_weapon/<pk>/` | `list/melee_weapon/` | `create/meleeweapon/` | `update/meleeweapon/<pk>/` | `items:item` |
| `RangedWeapon` | `ranged_weapon` | `ranged_weapon` | `ranged_weapon/<pk>/` | `list/ranged_weapon/` | `create/rangedweapon/` | `update/rangedweapon/<pk>/` | `items:item` |
| `ThrownWeapon` | `thrown_weapon` | `thrown_weapon` | `thrown_weapon/<pk>/` | `list/thrown_weapon/` | `create/thrownweapon/` | `update/thrownweapon/<pk>/` | `items:item` |
| `Weapon` | `weapon` | `weapon` | `weapon/<pk>/` | `list/weapon/` | `create/weapon/` | `update/weapon/<pk>/` | `items:item` |

### `vampire`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `VampireArtifact` | `vampire_artifact` | `artifact` | `vampire/artifact/<pk>/` | `vampire/list/artifacts/` | `vampire/create/artifact/` | `vampire/update/artifact/<pk>/` | `items:vampire:artifact` |
| `Bloodstone` | `bloodstone` | `bloodstone` | `vampire/bloodstone/<pk>/` | `vampire/list/bloodstones/` | `vampire/create/bloodstone/` | `vampire/update/bloodstone/<pk>/` | `items:item` |

### `werewolf`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Fetish` | `fetish` | `fetish` | `werewolf/fetish/<pk>/` | `werewolf/list/fetish/` | `werewolf/create/fetish/` | `werewolf/update/fetish/<pk>/` | `items:item` |
| `Talen` | `talen` | `talen` | `werewolf/talen/<pk>/` | `werewolf/list/talen/` | `werewolf/create/talen/` | `werewolf/update/talen/<pk>/` | `items:item` |

### `mage`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Artifact` | `artifact` | `artifact` | `mage/artifact/<pk>/` | `mage/list/artifact/` | `mage/create/artifact/` | `mage/update/artifact/<pk>/` | `items:item` |
| `Charm` | `charm` | `charm` | `mage/charm/<pk>/` | `mage/list/charm/` | `mage/create/charm/` | `mage/update/charm/<pk>/` | `items:item` |
| `Grimoire` | `grimoire` | `grimoire` | `mage/grimoire/<pk>/` | `mage/list/grimoire/` | `mage/create/grimoire/` | `mage/update/grimoire/<pk>/` | `items:item` |
| `Periapt` | `periapt` | `periapt` | `mage/periapt/<pk>/` | `mage/list/periapt/` | `mage/create/periapt/` | `mage/update/periapt/<pk>/` | `items:item` |
| `SorcererArtifact` | `sorcerer_artifact` | `sorcerer_artifact` | `mage/sorcerer_artifact/<pk>/` | `mage/list/sorcerer_artifact/` | `mage/create/sorcerer_artifact/` | `mage/update/sorcerer_artifact/<pk>/` | `items:item` |
| `Talisman` | `talisman` | `talisman` | `mage/talisman/<pk>/` | `mage/list/talisman/` | `mage/create/talisman/` | `mage/update/talisman/<pk>/` | `items:item` |
| `Wonder` | `wonder` | `wonder` | `mage/wonder/<pk>/` | `mage/list/wonder/` | `mage/create/wonder/` | `mage/update/wonder/<pk>/` | `items:item` |

### `wraith`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `WraithRelic` | `wraith_relic` | `relic` | `wraith/relic/<pk>/` | `wraith/list/relics/` | `wraith/create/relic/` | `wraith/update/relic/<pk>/` | `items:wraith:relic` |
| `WraithArtifact` | `wraith_artifact` | `artifact` | `wraith/artifact/<pk>/` | `wraith/list/artifacts/` | `wraith/create/artifact/` | `wraith/update/artifact/<pk>/` | `items:wraith:artifact` |

### `changeling`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Treasure` | `treasure` | `treasure` | `changeling/treasure/<pk>/` | `changeling/list/treasures/` | `changeling/create/treasure/` | `changeling/update/treasure/<pk>/` | `items:item` |
| `Dross` | `dross` | `dross` | `changeling/dross/<pk>/` | `changeling/list/dross/` | `changeling/create/dross/` | `changeling/update/dross/<pk>/` | `items:changeling:dross` |

### `demon`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `Relic` | `demon_relic` | `relic` | `demon/relic/<pk>/` | `demon/list/relics/` | `demon/create/relic/` | `demon/update/relic/<pk>/` | `items:demon:relic` |

### `hunter`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `HunterGear` | `hunter_gear` | `gear` | `hunter/gear/<pk>/` | `hunter/list/gear/` | `hunter/create/gear/` | `hunter/update/gear/<pk>/` | `items:item` |
| `HunterRelic` | `hunter_relic` | `relic` | `hunter/relic/<pk>/` | `hunter/list/relics/` | `hunter/create/relic/` | `hunter/update/relic/<pk>/` | `items:item` |

### `mummy`

| Model | Slug | Route name | Detail | List | Create | Update | `get_absolute_url()` |
|---|---|---|---|---|---|---|---|
| `MummyRelic` | `mummy_relic` | `relic` | `mummy/relic/<pk>/` | `mummy/list/relic/` | `mummy/create/relic/` | `mummy/update/relic/<pk>/` | `items:mummy:relic` |
| `Vessel` | `vessel` | `vessel` | `mummy/vessel/<pk>/` | `mummy/list/vessel/` | `mummy/create/vessel/` | `mummy/update/vessel/<pk>/` | `items:mummy:vessel` |
| `Ushabti` | `ushabti` | `ushabti` | `mummy/ushabti/<pk>/` | `mummy/list/ushabti/` | `mummy/create/ushabti/` | `mummy/update/ushabti/<pk>/` | `items:mummy:ushabti` |

### Other item routes

| Path | URL name | View |
|------|----------|------|
| `/items/index/` | `items:index` | `ItemIndexView` |
| `/items/<pk>/` | `items:item` | `GenericItemDetailView` |

## See also

- [Item models](models.md)
- [Item forms](forms.md)
- [Item templates](templates.md)
- [Authorization](../../docs/architecture/authorization.md)
- [URL reference](../../docs/reference/urls.md)
- [Adding an item or location type](../../docs/guides/adding-an-item-or-location-type.md)
