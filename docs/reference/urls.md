# URL reference

This page maps the site's URLs: what the root URLconf includes, each app's namespaces and route
families, the naming conventions a new route must follow, and the model methods and helpers
that build URLs. It is for developers and agents who need to reverse a route, add one, or find
which view serves a path. For the access rules on each route see
[Authorization](../architecture/authorization.md); for adding a route see
[Adding a view](../guides/adding-a-view.md).

The project has about 1,850 URL patterns, most of them in the Django admin and in the per-type
character, item and location routes. This page describes their shape rather than listing every
one; [Listing every route](#listing-every-route) shows how to print the full table.

## Root URLconf

`ROOT_URLCONF` is `tg.urls` ([`tg/urls.py`](../../tg/urls.py)).

| Path prefix | Includes | Namespace |
|-------------|----------|-----------|
| `admin/` | `django.contrib.admin.site.urls` | `admin` |
| (empty) | [`core/urls.py`](../../core/urls.py) | `core` |
| `characters/` | [`characters/urls/__init__.py`](../../characters/urls/__init__.py) | `characters` |
| `locations/` | [`locations/urls/__init__.py`](../../locations/urls/__init__.py) | `locations` |
| `items/` | [`items/urls/__init__.py`](../../items/urls/__init__.py) | `items` |
| `game/` | [`game/urls.py`](../../game/urls.py) | `game` |
| `accounts/` | [`accounts/urls.py`](../../accounts/urls.py) | `accounts` |
| `accounts/password_reset/done/`, `accounts/reset/<uidb64>/<token>/`, `accounts/reset/done/` | Django's password-reset views with the site's templates (`accounts/auth/...`) | none (`password_reset_done`, `password_reset_confirm`, `password_reset_complete`) |
| `accounts/` | `django.contrib.auth.urls` | none (`login`, `logout`, `password_change`, `password_change_done`, `password_reset`, ...) |
| `MEDIA_URL` | `django.conf.urls.static.static(...)` (serves files only when `DEBUG` is on) | none |

Added at run time:

- `__chained_select__/` (name `__chained_select_ajax__`, view `widgets.views.auto_chained_ajax_view`)
  is inserted at the front of `tg.urls.urlpatterns` by `WidgetsConfig.ready()`
  ([`widgets/apps.py`](../../widgets/apps.py)). It answers the chained-select widgets' option
  requests.
- `__debug__/` (Django Debug Toolbar) is prepended when `DEBUG` is true and `debug_toolbar` is
  importable.

`accounts/login/` and `accounts/password_reset/` are matched by the `accounts` app's own views
(`accounts:login`, `accounts:password_reset`) because that include comes first; the
unnamespaced `login` and `password_reset` names from `django.contrib.auth.urls` reverse to the
same paths.

Error handlers: `handler403 = "core.views.errors.error_403"`, `handler404 = "core.views.errors.error_404"`,
`handler500 = "core.views.errors.error_500"`.

## `core`

Site-wide pages and staff-edited records ([`core/urls.py`](../../core/urls.py)).

| Path | Name | View |
|------|------|------|
| `/` | `core:home` | `core.views.home.HomeListView` |
| `/types/<kind>/<action>/` | `core:object_type_redirect` | `core.views.object_type_redirect.ObjectTypeRedirectView`: `GET` from the "new ..." pickers; `kind` is `character`, `group`, `item` or `location`, `action` is `create` or `list` |
| `/book/`, `/book/create/`, `/book/<pk>/`, `/book/update/<pk>/` | `core:index_book`, `core:create_book`, `core:book`, `core:update_book` | `core.views.book` |
| `/language/...` | `core:index_language`, `core:create_language`, `core:language`, `core:update_language` | `core.views.language` |
| `/newsitem/...` | `core:index_newsitem`, `core:create_newsitem`, `core:newsitem`, `core:update_newsitem` | `core.views.newsitem` |
| `/houserules/index/`, `/houserules/create/`, `/houserules/<pk>/`, `/houserules/update/<pk>/` | `core:houserules`, `core:create_houserule`, `core:houserule`, `core:update_houserule` | `core.views.houserules` |
| `/templates/`, `/templates/create/`, `/templates/import/` | `core:character_template_list`, `core:character_template_create`, `core:character_template_import` | `core.views.character_template` |
| `/templates/<int:pk>/`, `.../edit/`, `.../delete/`, `.../export/`, `.../create-npc/` | `core:character_template_detail`, `_update`, `_delete`, `_export`, `_create_npc` | `core.views.character_template` |

`core` names follow `<verb>_<noun>` (`create_book`, `update_book`, `index_book`) rather than the
`create:` / `update:` namespaces the object apps use.

## `accounts`

[`accounts/urls.py`](../../accounts/urls.py):

| Path (under `/accounts/`) | Name |
|---------------------------|------|
| `` | `accounts:user` (redirects to `core:home`) |
| `login/`, `signup/`, `password_reset/` | `accounts:login`, `accounts:signup`, `accounts:password_reset` |
| `profile/<pk>/`, `profile/update/<pk>/` | `accounts:profile`, `accounts:profile_update` |
| `scene/<int:scene_pk>/award-xp/`, `scene/<int:scene_pk>/mark-read/` | `accounts:scene_xp_award`, `accounts:mark_scene_read` |
| `approve/<str:object_type>/<int:pk>/`, `submit/...`, `revise/...`, `approve-image/...` | `accounts:object_approval`, `accounts:object_submission`, `accounts:object_revision`, `accounts:image_approval` |
| `character/<int:character_pk>/award-freebies/` | `accounts:freebie_award` |
| `weekly-xp/<int:week_pk>/<int:character_pk>/request/`, `.../approve/` | `accounts:weekly_xp_request`, `accounts:weekly_xp_approval` |

## `characters`

[`characters/urls/__init__.py`](../../characters/urls/__init__.py) builds the routes in two
parts.

**Gameline routes.** For each `(url_path, module_name, namespace)` in
`core.constants.GameLine.URL_PATTERNS` (vampire, werewolf, mage, wraith, changeling, demon,
mummy, hunter) it includes `characters/urls/<module_name>/__init__.py`'s `urls` list under
`characters/<url_path>/` with that namespace. Each gameline package has the same shape:

| Path (under `/characters/<gameline>/`) | Name | Module |
|----------------------------------------|------|--------|
| `create/<name>/` | `characters:<gameline>:create:<name>` | `create.py` |
| `update/<name>/<pk>/` | `characters:<gameline>:update:<name>` | `update.py` |
| `list/<name>/` | `characters:<gameline>:list:<name>` | `index.py` |
| `<name>/<pk>/` and other detail-level routes | `characters:<gameline>:<name>` | `detail.py` |

Examples: `characters:vampire:create:vampire`, `characters:vampire:update:discipline`,
`characters:demon:list:thrall`, `characters:vampire:clan`. Detail-level modules also hold:

- chargen entry points for some types: `<type>/<int:pk>/chargen/` (`vampire_chargen`,
  `ghoul_chargen`, `wraith_chargen`, `wto_human_chargen`, `demon_chargen`, `dtfhuman_chargen`,
  `thrall_chargen`), each routed to the type's creation router;
- template selection and creation for mortals: `<type>/<int:pk>/template/` and
  `<type>/<int:pk>/creation/` (`vtmhuman_template`, `vtmhuman_creation`, and the same for
  `wtahuman`, `mtahuman`, `wtohuman`, `ctdhuman`, `dtfhuman`);
- `characters:mage:spend_xp` (`mage/<int:pk>/xp/spend/`, `characters.views.mage.actions.MageXPSpendView`).

Some update and create routes have a `_full` variant with a `full/` path segment (for example
`characters:vampire:update:vtm_human_full`, `characters:mage:create:mage_full`);
`Human.get_full_update_url()` and `Human.get_full_creation_url()` reverse them.

**Core routes** (the `wod` gameline and cross-gameline pages), from
`characters/urls/core/{create,update,index,detail}.py` and the package itself:

| Path (under `/characters/`) | Name | View |
|-----------------------------|------|------|
| `create/character/`, `create/group/`, `create/human/`, `create/human/full/` | `characters:create:character`, `:create:group`, `:create:human`, `:create:human_full` | |
| `create/npc/`, `create/npc/<int:pk>/` | `characters:create:npc`, `characters:create:npc_for_character` | `characters.views.core.npc.NPCProfileCreateView` |
| `create/archetypes/`, `create/meritflaws/`, `create/specialties/`, `create/derangement/` | `characters:create:archetype`, `:meritflaw`, `:specialty`, `:derangement` | |
| `update/<name>/<pk>/` | `characters:update:character`, `:group`, `:human`, `:human_full`, `:archetype`, `:meritflaw`, `:specialty`, `:derangement` | |
| `list/archetypes/`, `list/meritflaws/`, `list/specialties/`, `list/derangement/` | `characters:list:archetype`, `:meritflaw`, `:specialty`, `:derangement` | |
| `index/`, `retired/`, `deceased/`, `npc/` | `characters:index`, `characters:retired`, `characters:deceased`, `characters:npc` | `characters.views.core.CharacterIndexView` and friends |
| `groups/<pk>/` | `characters:group` | `characters.views.core.GenericGroupDetailView` (router by group type) |
| `archetypes/<pk>/`, `meritflaws/<pk>/`, `specialties/<pk>/`, `derangement/<pk>/` | `characters:archetype`, `:meritflaw`, `:specialty`, `:derangement` | |
| `<int:pk>/chargen/back/` | `characters:chargen_back` | `characters.views.core.chargen_back.ChargenBackView` (`POST`) |
| `<int:pk>/xp-requests/<int:request_pk>/approve/`, `.../reject/` | `characters:xp_request_approve`, `characters:xp_request_reject` | `characters.views.core.actions` (`POST`) |
| `<int:pk>/retire/`, `<int:pk>/decease/`, `<int:pk>/specialties/` | `characters:retire`, `characters:decease`, `characters:add_specialties` | `characters.views.core.actions` (`POST`) |
| `<pk>/` | `characters:character` | `characters.views.core.GenericCharacterDetailView` |

`characters:character` is the type router: it loads the character, looks its `type` up in
`GenericCharacterDetailView.view_mapping` and hands off to that type's creation router (which
serves the current chargen step while the character is `Un` or `Rev`, else the detail view) or
detail view. It is listed last so the named paths above match first.

## `items` and `locations`

Both apps take their routes from their registry ([`items/registry.py`](../../items/registry.py),
[`locations/registry.py`](../../locations/registry.py); see
[Adding an item or location type](../guides/adding-an-item-or-location-type.md)). The URL
packages mirror `characters/urls/`: one package per `GameLine.URL_PATTERNS` entry and a `core`
directory, each leaf module a single call such as `urls = registry.urls("demon", "create")`.

| Path | Name |
|------|------|
| `/items/<gameline>/create/<route>/`, `update/<route>/<int:pk>/`, `list/<route>/`, `<route>/<int:pk>/` | `items:<gameline>:create:<name>`, `items:<gameline>:update:<name>`, `items:<gameline>:list:<name>`, `items:<gameline>:<name>` |
| `/items/create/...`, `/items/update/...`, `/items/list/...`, `/items/<route>/<int:pk>/` | `items:create:<name>`, `items:update:<name>`, `items:list:<name>`, `items:<name>` (the `core` group: item, weapon, melee/ranged/thrown weapon, material, medium) |
| `/items/index/` | `items:index` (`items.views.core.ItemIndexView`) |
| `/items/<int:pk>/` | `items:item` (`items.views.core.GenericItemDetailView`, router by concrete type) |
| `/locations/<gameline>/...` | `locations:<gameline>:create:<name>`, `...:update:<name>`, `...:list:<name>`, `locations:<gameline>:<name>` |
| `/locations/create/...`, `/locations/update/...`, `/locations/list/...` | `locations:create:city`, `locations:create:location`, and the matching update and list names |
| `/locations/city/<int:pk>/` | `locations:city` |
| `/locations/index/` | `locations:index` |
| `/locations/<int:pk>/` | `locations:location` (router by concrete type) |

The path segment and the URL name come from each `ActionSpec.routes` pair and can differ (the
Demon relic's list path is `relics/` and its name `relic`; `items:create:melee_weapon` is at
`create/meleeweapon/`). Reverse by name.

## `game`

[`game/urls.py`](../../game/urls.py) is included with the `game` namespace; the module also sets
`app_name = "game"`. Sub-resources are nested namespaces.

| Path (under `/game/`) | Name |
|-----------------------|------|
| `chronicles/`, `chronicle/<int:pk>/` | `game:chronicles`, `game:chronicle` |
| `chronicle/<int:pk>/stories/`, `chronicle/<int:pk>/scenes/` (`POST`) | `game:chronicle_create_story`, `game:chronicle_create_scene` |
| `chronicle/<int:pk>/retired/`, `.../deceased/`, `.../npc/` | `game:retired`, `game:deceased`, `game:npc` (the character index views, filtered to the chronicle) |
| `scenes/`, `scene/<int:pk>/` | `game:scenes`, `game:scene` |
| `scene/<int:pk>/close/`, `.../characters/`, `.../posts/` (`POST`) | `game:scene_close`, `game:scene_add_character`, `game:scene_post` |
| `commands/` | `game:commands` |
| `journals/`, `journal/<int:pk>/` | `game:journals`, `game:journal` |
| `journal/<int:pk>/entries/`, `journal/<int:pk>/entries/<int:entry_pk>/response/` (`POST`) | `game:journal_add_entry`, `game:journal_respond` |
| `story/list/`, `story/create/`, `story/<int:pk>/`, `story/<int:pk>/update/` | `game:story:list`, `game:story:create`, `game:story:detail`, `game:story:update` |
| `week/...` | `game:week:list`, `:create`, `:detail`, `:update` |
| `weekly-xp-request/...` | `game:weekly_xp_request:list`, `:create` (`create/<int:week_pk>/<int:character_pk>/`), `:batch_approve`, `:detail`, `:approve` |
| `story-xp-request/...` | `game:story_xp_request:list`, `:create` (`create/<int:character_pk>/`), `:detail`, `:update` |
| `setting-element/...` | `game:setting_element:list`, `:create`, `:detail`, `:update` |
| `xp-spending-request/...` | `game:xp_spending_request:list`, `:create` (`create/<int:character_pk>/`), `:detail`, `:update`, `:approve` |
| `freebie-spending-record/...` | `game:freebie_spending_record:list`, `:create` (`create/<int:character_pk>/`), `:detail`, `:update` |
| `chronicle-manage/create/`, `chronicle-manage/<int:pk>/update/` | `game:chronicle_manage:create`, `game:chronicle_manage:update` |
| `scene-manage/create/`, `scene-manage/create/<int:chronicle_pk>/`, `scene-manage/<int:pk>/update/` | `game:scene_manage:create`, `game:scene_manage:create_for_chronicle`, `game:scene_manage:update` |

## Naming conventions

- **Object apps** (`characters`, `items`, `locations`): `<app>:<gameline>:<action>:<name>` for
  `create`, `update` and `list`, and `<app>:<gameline>:<name>` for detail (no action segment).
  `<gameline>` is the gameline's `app_name` from `settings.GAMELINES` (`vampire`, `werewolf`,
  `mage`, `wraith`, `changeling`, `demon`, `mummy`, `hunter`). Models of the generic `wod`
  gameline drop that segment: `characters:create:human`, `items:weapon`.
- **Leaf URL modules** under `characters/urls/`, `items/urls/` and `locations/urls/` export a
  plain `urls` list and never define `app_name`; the namespaces come from the `include()`
  tuples. `test_list_included_url_modules_have_no_app_name` in
  [`core/tests/test_dead_code_removed.py`](../../core/tests/test_dead_code_removed.py) enforces
  it. The `*/urls/core/` directories have no `__init__.py`.
- **Primary keys**: new routes use `<int:pk>`. Many older routes use `<pk>`;
  `AuthorizationMiddleware` answers 404 to any `pk` that is not a positive ASCII integer, so
  both behave the same for bad input.
- **Actions** are their own paths under the object (`characters/<int:pk>/retire/`,
  `game/scene/<int:pk>/close/`), `POST` only.
- **Every routed view needs a route policy**; see
  [Authorization](../architecture/authorization.md#route-policies).

## Building URLs in code

| Helper | Returns |
|--------|---------|
| `Character.get_absolute_url()` ([`characters/models/core/character.py`](../../characters/models/core/character.py)) | `characters:character` (the type router). Some types override it with their own detail route: `Vampire` (`characters:vampire:vampire`), `Thrall` (`characters:demon:thrall`), `DtFHuman`, `Demon`, `Earthbound`, and others. |
| `Character.get_update_url()`, `Character.get_creation_url()` | `characters:update:character`, `characters:create:character` |
| `Human.get_update_url()`, `Human.get_creation_url()` ([`characters/models/core/human.py`](../../characters/models/core/human.py)) | `characters:<app_name>:update:<type>` and `characters:<app_name>:create:<type>`, where `Human.get_gameline_for_url(gameline)` gives `"<app_name>:"` or `""` for `wod`. Subclasses whose route names differ from `type` override them (`DtFHuman` uses `dtfhuman`). |
| `Human.get_full_update_url()`, `Human.get_full_creation_url()` | The same names with `_full` |
| `Character.chargen_back_url` | `characters:chargen_back` while back-navigation is allowed, else `""` |
| `core.models.URLMethodsMixin` ([`core/models.py`](../../core/models.py)) | From `url_namespace` and `url_name` (default: the lowercased class name): `<ns>:<name>`, `<ns>:update:<name>`, `<ns>:create:<name>` |
| `core.registry_urls.RegistryURLMixin` ([`core/registry_urls.py`](../../core/registry_urls.py)) | For `ItemModel` and `LocationModel` subclasses: the names in the model's `ModelSpec.model_urls` |
| Reference models (`Discipline`, `DemonHouse`, ...) | Their own `get_absolute_url` / `get_update_url` / `get_creation_url` with `reverse(...)` |
| `{{ obj|update_url }}` (`tl` template library, [`core/templatetags/tl.py`](../../core/templatetags/tl.py)) | `obj.get_update_url()`, or `""` when the model has no update route |
| `core.create_redirects.resolve_object_type_url(category, type_name, action, gameline)` | The create or list URL for a type chosen in a picker: items and locations through the registry, characters through `game.models.ObjectType` and the name `characters:<app_name>:<action>:<type_name>` (`dtf_human`, `htr_human`, `mtr_human` drop the underscore) |

## Listing every route

There is no `show_urls` command. Two read-only scripts print route tables:

```bash
python scripts/inventory_authorization_routes.py > route-inventory.md   # every route and router branch, with its guard
python scripts/inventory_model_routes.py                                # item and location routes as JSON
```

or walk the resolver in a shell:

```bash
python manage.py shell -c "
from django.urls import URLPattern, URLResolver, get_resolver
def walk(patterns, prefix='', ns=()):
    for p in patterns:
        if isinstance(p, URLResolver):
            walk(p.url_patterns, prefix + str(p.pattern), ns + ((p.namespace,) if p.namespace else ()))
        elif p.name:
            print(prefix + str(p.pattern), ':'.join(ns + (p.name,)))
walk(get_resolver().url_patterns)
"
```

## See also

- [Authorization](../architecture/authorization.md)
- [Adding a view](../guides/adding-a-view.md)
- [Adding a character type](../guides/adding-a-character-type.md)
- [Adding an item or location type](../guides/adding-an-item-or-location-type.md)
- [`tg/urls.py`](../../tg/urls.py)
