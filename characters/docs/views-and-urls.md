# Views and URLs

This page is the reference for [`characters/views/`](../views/) and
[`characters/urls/`](../urls/): how the URLconf is assembled, the core routes, the
polymorphic routers, the view families every character type has, sheet actions, the
reference "Known by" section, and the routes of each gameline. It is for developers adding
a view or a route and for agents resolving a URL name. Route policies and permission
checks are explained in [Authorization](../../docs/architecture/authorization.md); the
chargen step views in [Character creation](../../docs/architecture/character-creation.md)
and [Chargen](chargen.md).

## URLconf layout

[`tg/urls.py`](../../tg/urls.py) includes [`characters/urls/__init__.py`](../urls/__init__.py)
at `characters/` with the namespace `characters`. That module builds, in order:

1. One include per entry of `core.constants.GameLine.URL_PATTERNS`: `vampire/`,
   `werewolf/`, `mage/`, `wraith/`, `changeling/`, `demon/`, `mummy/`, `hunter/`, each
   loading `characters/urls/<gameline>/__init__.py` (its `urls` list) under the namespace of
   the same name. Import errors are not caught: a broken gameline module stops startup
   rather than silently dropping its routes.
2. The core `create/`, `update/` and `list/` includes (namespaces `create`, `update`,
   `list`), from [`urls/core/`](../urls/core/).
3. `index/`, `retired/`, `deceased/`, `npc/`.
4. [`urls/core/detail.py`](../urls/core/detail.py), which ends with the catch-all
   `<pk>/` (`characters:character`). It must stay last.

Each gameline package has the same four modules: `create.py`, `update.py`, `index.py`
(list views, namespace `list`) and `detail.py`. So a gameline route name reads
`characters:<gameline>:<kind>:<name>` for create, update and list, and
`characters:<gameline>:<name>` for detail and special routes.

To list every resolved name, walk `django.urls.get_resolver().url_patterns` in
`python manage.py shell`. The project-wide URL table is in
[URLs](../../docs/reference/urls.md).

## Core routes

| Name | Path | View | Policy |
|------|------|------|--------|
| `characters:index` | `index/` | `CharacterIndexView` | `PUBLIC_INDEX` |
| `characters:retired`, `characters:deceased`, `characters:npc` | `retired/`, `deceased/`, `npc/` | `RetiredCharacterIndex`, `DeceasedCharacterIndex`, `NPCCharacterIndex` | `OBJECT_LIST` |
| `characters:character` | `<pk>/` | `GenericCharacterDetailView` (router) | `ROUTER` |
| `characters:group` | `groups/<pk>/` | `GenericGroupDetailView` (router) | `ROUTER` |
| `characters:chargen_back` | `<int:pk>/chargen/back/` | `ChargenBackView` | `LOGIN` |
| `characters:xp_request_approve`, `characters:xp_request_reject` | `<int:pk>/xp-requests/<int:request_pk>/approve/` (`reject/`) | `XPRequestApproveView`, `XPRequestRejectView` | `ACTION` |
| `characters:retire`, `characters:decease` | `<int:pk>/retire/`, `<int:pk>/decease/` | `CharacterRetireView`, `CharacterDeceaseView` | `ACTION` |
| `characters:add_specialties` | `<int:pk>/specialties/` | `CharacterSpecialtiesView` | `ACTION` |
| `characters:create:character` / `characters:update:character` | `create/character/`, `update/character/<pk>/` | `CharacterCreateView`, `CharacterUpdateView` | `OBJECT_CREATE` / `OBJECT_WRITE` |
| `characters:create:human`, `characters:create:human_full` | `create/human/`, `create/human/full/` | `HumanBasicsView`, `HumanCreateView` | `OBJECT_CREATE` |
| `characters:update:human`, `characters:update:human_full` | `update/human/<pk>/`, `update/human/full/<pk>/` | `HumanCharacterCreationView` (router), `HumanUpdateView` | `ROUTER`, `OBJECT_WRITE` |
| `characters:create:group`, `characters:update:group` | `create/group/`, `update/group/<pk>/` | `GroupCreateView`, `GroupUpdateView` | `OBJECT_CREATE` / `OBJECT_WRITE` |
| `characters:create:npc`, `characters:create:npc_for_character` | `create/npc/`, `create/npc/<int:pk>/` | `NPCProfileCreateView` | `LOGIN` |
| `archetype`, `meritflaw`, `specialty`, `derangement` | detail at `archetypes/<pk>/`, `meritflaws/<pk>/`, `specialties/<pk>/`, `derangement/<pk>/`, plus `create:`, `update:`, `list:` | `Archetype...View`, `MeritFlaw...View`, `Specialty...View`, `Derangement...View` | `PUBLIC_READ` / `STAFF_WRITE` |

`CharacterIndexView` answers anonymous and non-staff users with the public card list
(`core.views.public_object.render_public_object_list`), adding the creation pickers for
signed-in users. Staff get the full index: visible characters grouped by chronicle and by
status tab (`?chronicle=<pk|none>&status=active|retired|deceased|npc`). The pickers submit
to `core:object_type_redirect` (see [Forms](forms.md#creation-pickers-and-npc-profiles)).

## Routers

[`characters/views/core/__init__.py`](../views/core/__init__.py) defines two
`core.views.generic.DictView` routers keyed on the object's `type`:

- `GenericCharacterDetailView` (`characters:character`): `protected_object = True`,
  `public_view_class = PublicObjectDetailView`, `default_redirect = "characters:index"`.
  Its `view_mapping` sends each type to either the type's chargen router (for types with a
  workflow: `human`, `vtm_human`, `vampire`, `ghoul`, `wta_human`, `werewolf`, `kinfolk`,
  `fomor`, `drone`, `fera` and every Fera breed, `mta_human`, `mage`, `companion`,
  `sorcerer`, `ctd_human`, `changeling`, `wto_human`, `wraith`, `dtf_human`, `demon`,
  `thrall`) or straight to a detail view (`revenant`, `spirit_character`,
  `autumn_person`, `inanimae`, `nunnehi`, `earthbound`, `htr_human`, `hunter`,
  `mtr_human`, `mummy`). The base `character` type has no entry and redirects to the index.
- `GenericGroupDetailView` (`characters:group`): `group`, `pack`, `cabal`, `motley`,
  `coterie`, `circle`, `conclave`.

A chargen router (`HumanCharacterCreationView` and each `...CharacterCreationView`) is a
second `DictView` keyed on `creation_status`. While the character is `Un` or `Rev` it
dispatches to the workflow step; otherwise to its `default_redirect`, the type's detail
view. Because every character's canonical URL is `characters:character`, the same URL
shows the wizard while a character is being built and the sheet afterwards.

Several types also expose their chargen router under extra names:
`characters:vampire:vampire_chargen`, `characters:vampire:ghoul_chargen`,
`characters:wraith:wraith_chargen`, `characters:wraith:wto_human_chargen`,
`characters:demon:demon_chargen`, `characters:demon:dtfhuman_chargen`,
`characters:demon:thrall_chargen`, and the `<type>_creation` routes for mortals
(`vtmhuman_creation`, `wtahuman_creation`, `mtahuman_creation`, `wtohuman_creation`,
`ctdhuman_creation`, `dtfhuman_creation`). For `human`, `werewolf`, `fera`, `fomor`,
`drone`, `mage` and `wraith` the `update:<type>` name itself points at the chargen router
and the full edit form is `update:<type>_full`.

## View families per character type

| Family | Typical class | Mixins | Policy |
|--------|---------------|--------|--------|
| Basics (first page of chargen) | `<Type>BasicsView` | `LoginRequiredMixin`, `CreateView` or `FormView`; the gameline basics views add `core.mixins.ScopedCreationFormMixin` (chronicle choices limited to readable chronicles) | `LOGIN` or `OBJECT_CREATE` |
| Template picker (mortals) | `<Type>TemplateSelectView` (`characters.views.core.template_selection.CharacterTemplateSelectView`) | `SharedTemplateMixin`, `LoginRequiredMixin` | `LOGIN` |
| Chargen steps | `<Type>AttributeView`, `...AbilityView`, `...BackgroundsView`, `...ExtrasView`, `...FreebiesView`, `...LanguagesView`, `...SpecialtiesView`, power and background-detail steps | `ChargenStepMixin` (+ `AllocationStepMixin`, `SpecialUserMixin`, `SpendFreebiesPermissionMixin`) | `CHARGEN_STEP` |
| Chargen router | `<Type>CharacterCreationView` | `DictView` with `chargen_router = True`, `view_mapping = WorkflowViews()` | `ROUTER` |
| Detail (sheet) | `<Type>DetailView` | `characters.views.core.character.CharacterDetailView` (`ViewPermissionMixin`, `DetailView`) | `OBJECT_DETAIL` |
| Full create / update | `<Type>CreateView`, `<Type>UpdateView` | `ScopedEditFormMixin`, `EditPermissionMixin`, `MessageMixin`; `fields` from an allowlist, `limited_form_class = LimitedHumanEditForm` | `OBJECT_CREATE`, `OBJECT_WRITE` |
| List | `<Type>ListView` | Player types: `OBJECT_LIST`; reference types: `CachedListView` or `ListView` | |

`CharacterDetailView` adds to the context: the character's `scenes` (cached per character
with `core.cache.cache_function`, then filtered by `game.security.filter_scenes` for the
current viewer), `chargen_url` while a workflow is in progress, `edit_url` (or `None` when
`get_update_url()` does not resolve), `can_retire` (owner or `EDIT_FULL`, when the status
machine allows `Ret`) and `can_decease` (scoped editor role, when `Dec` is allowed).

The template picker applies an approved public `CharacterTemplate` and sets
`creation_status = 1`. It only renders while `creation_status` is `0`; for any other value
it redirects to the type's creation route.

### Chargen step views

The step views live in the gameline modules (`vampire_chargen.py`, `garou.py`,
`mage.py`, ...) and follow the workflow's `view_path`s. Shared bases in
[`views/core/`](../views/core/):

| Module | Classes |
|--------|---------|
| [`chargen_mixins.py`](../views/core/chargen_mixins.py) | `ChargenStepMixin`, `ChargenProgressMixin` |
| [`allocations.py`](../views/core/allocations.py) | `AllocationStepMixin`, `PointAllocationView` |
| [`form_steps.py`](../views/core/form_steps.py) | `CharacterFormStepView` (a plain-form step) |
| [`backgrounds.py`](../views/core/backgrounds.py) | `HumanBackgroundsView` (the Backgrounds formset step) |
| [`extras.py`](../views/core/extras.py) | `CharacterExtrasView` (the Biography step) |
| [`spending.py`](../views/core/spending.py) | `FreebieSpendingView` |
| [`generic_background.py`](../views/core/generic_background.py) | `GenericBackgroundView` (Allies, Mentor, Contacts, Node, Library, ... detail steps) |
| [`chargen_back.py`](../views/core/chargen_back.py) | `ChargenBackView` |

`GenericBackgroundView` finds the first incomplete `BackgroundRating` for its
`background_name`, saves the step form (an NPC from `LinkedNPCForm` or a location/item
form), links the new object to the character (`owned_by`, owner, chronicle, status `Sub`),
stores its name and URL on the rating, marks it complete, and advances once no incomplete
rating of that background remains.

## Sheet actions

[`views/core/actions.py`](../views/core/actions.py) holds `core.actions.ObjectActionView`
subclasses: one `POST` URL, permission check and service call each.

| View | Permission | Service |
|------|------------|---------|
| `XPRequestApproveView`, `XPRequestRejectView` | `game.spending_approval.can_approve_spending` | `decide_spending_request()`; a double submit shows a warning instead of an error |
| `CharacterRetireView` | Owner or scoped editor role | `characters.services.status.change_character_status(..., "Ret")` under a row lock |
| `CharacterDeceaseView` | Scoped editor role | `change_character_status(..., "Dec")` |
| `CharacterSpecialtiesView` | `EDIT_FULL` | `characters.services.specialties.record_specialties()`; every field optional |
| `MageXPSpendView` ([`views/mage/actions.py`](../views/mage/actions.py)) | `SPEND_XP` | `characters.services.mage_xp.spend_mage_xp()`; errors re-render the Mage sheet |

## Known by

[`views/core/known_by.py`](../views/core/known_by.py) adds a "Known by" list to reference
detail pages: the characters that hold the power, with their rating, grouped by chronicle.
`KNOWN_BY_SOURCES` maps each reference model to where characters store it:

| Source | Reference models |
|--------|------------------|
| `RatingFields` (an integer field named by the reference row) | `Discipline` (Vampire, Ghoul, Revenant), `Sphere` (Mage), `Lore` (Demon, Earthbound), `Arcanos` (Wraith), `Edge` (Hunter) |
| `Members` (a many-to-many) | `Gift` (Werewolf, Fera, Kinfolk), `Rite` (Werewolf, Fera), `Rote` (Mage), Demon `Ritual` (Demon, Earthbound) |
| `Ratings` (a through model) | `MeritFlaw` (`MeritFlawRating`), `Thorn` (`ThornRating`), `LinearMagicPath` (`PathRating`), `Advantage` (`AdvantageRating`) |

`known_by(obj, user)` returns `None` for anonymous viewers. Otherwise it lists only
characters with `display=True` whose full sheet the viewer can read: all of them for
staff, else the viewer's own and those in chronicles the viewer staffs. At most
`KNOWN_BY_LIMIT` (100) rows are shown. `KnownByMixin` puts the result in the context and
marks the response `Vary: Cookie` and, for signed-in viewers, `Cache-Control: private`,
because several of these views are cached per URL (`CachedDetailView`). The template is
`characters/tl/known_by.html`.

## Reference views

Reference detail and list views are `PUBLIC_READ`; many extend
`core.views.CachedDetailView` / `CachedListView` (15-minute `cache_page_per_visitor`).
Their create and update views are plain `CreateView` / `UpdateView` with `MessageMixin`
and an explicit `fields` list; the `STAFF_WRITE` policy restricts them to staff. See
[Reference data](reference-data.md) and [Caching](../../docs/architecture/caching.md).

## Gameline routes

The tables list the character and group routes of each gameline; reference catalogues
follow the pattern `create:<name>`, `update:<name>`, `list:<name>` and a detail route
`<name>` (names in [Reference data](reference-data.md)).

### Vampire

| Type | Create | Update | Detail / router |
|------|--------|--------|-----------------|
| `vtm_human` | `create:vtm_human` (`VtMHumanBasicsView`) | `update:vtm_human`, `update:vtm_human_full` (`VtMHumanUpdateView`) | `vtmhuman_template`, `vtmhuman_creation` |
| `vampire` | `create:vampire` (`VampireBasicsView`) | `update:vampire` (`VampireUpdateView`) | `vampire`, `vampire_chargen` |
| `ghoul` | `create:ghoul` (`GhoulBasicsView`) | `update:ghoul` (`GhoulUpdateView`) | `ghoul`, `ghoul_chargen` |
| `revenant` | `create:revenant` (`RevenantCreateView`) | `update:revenant` | `revenant` |
| `coterie` | `create:coterie` | `update:coterie` | `coterie`, `list:coterie` |

### Werewolf

| Type | Create | Update | Detail / router |
|------|--------|--------|-----------------|
| `wta_human` | `create:wta_human` | `update:wta_human`, `update:wta_human_full` (`WtAHumanUpdateView`) | `wtahuman_template`, `wtahuman_creation` |
| `werewolf` | `create:werewolf` (`WerewolfBasicsView`) | `update:werewolf` (router), `update:werewolf_full` | through `characters:character` |
| `kinfolk` | `create:kinfolk` | `update:kinfolk`, `update:kinfolk_full` (`KinfolkUpdateView`) | through `characters:character` |
| `fomor`, `drone` | `create:fomor`, `create:drone` | `update:<type>` (router), `update:<type>_full` | `drone`; Fomor through `characters:character` |
| `fera` and breeds | `create:fera` (`FeraBasicsView`) | `update:fera` (router), `update:fera_full` | `fera`, and `ajaba` ... `rokea` (all `FeraDetailView`) |
| `spirit_character` | `create:spirit` | `update:spirit` | `spirit` |
| `pack` | `create:pack` | `update:pack` | `list:pack`; detail through `characters:group` |

### Mage

| Type | Create | Update | Detail / router |
|------|--------|--------|-----------------|
| `mta_human` | `create:mta_human` | `update:mta_human`, `update:mta_human_full` (`MtAHumanUpdateView`) | `mtahuman_template`, `mtahuman_creation` |
| `mage` | `create:mage` (`MageBasicsView`), `create:mage_full` | `update:mage` (router), `update:mage_full` | `spend_xp` (`MageXPSpendView`) |
| `companion` | `create:companion` (`CompanionBasicsView`), `create:companion_full` | `update:companion_full` only | through `characters:character` |
| `sorcerer` | `create:sorcerer` (`SorcererBasicsView`) | `update:sorcerer_full` only | through `characters:character` |
| `cabal` | `create:cabal` | `update:cabal` | `list:cabal`; detail through `characters:group` |

`characters:mage:practice` is itself a router (`GenericPracticeDetailView`) that picks the
Practice, Specialized Practice or Corrupted Practice detail view. `characters:mage:path` and
`characters:mage:ritual` are the Linear Magic path and ritual pages
([`hedge_magic.py`](../views/mage/hedge_magic.py)). Mage-family edit forms lay their fields
out in sections declared in [`form_layout.py`](../views/mage/form_layout.py).

### Wraith

| Type | Create | Update | Detail / router |
|------|--------|--------|-----------------|
| `wto_human` | `create:wto_human` | `update:wto_human`, `update:wto_human_full` | `wtohuman_template`, `wtohuman_creation`, `wto_human_chargen` |
| `wraith` | `create:wraith` (`WraithBasicsView`) | `update:wraith` (router), `update:wraith_full` | `wraith`, `wraith_chargen` |
| `circle` | `create:circle` | `update:circle` | `circle`, `list:circle` |

### Changeling

| Type | Create | Update | Detail / router |
|------|--------|--------|-----------------|
| `ctd_human` | `create:ctd_human` | `update:ctd_human`, `update:ctd_human_full` | `ctdhuman_template`, `ctdhuman_creation` |
| `changeling` | `create:changeling` (`ChangelingBasicsView`) | `update:changeling`, `update:changeling_full` (`ChangelingUpdateView`) | `changeling` |
| `inanimae`, `nunnehi`, `autumn_person` | `create:<type>` | `update:<type>` | `<type>` |
| `motley` | `create:motley` | `update:motley` | `motley`, `list:motley` |
| `chimera` | `create:chimera` | `update:chimera` | `chimera`, `list:chimera` |

### Demon

| Type | Create | Update | Detail / router |
|------|--------|--------|-----------------|
| `dtf_human` | `create:dtfhuman` | `update:dtfhuman` | `dtfhuman`, `list:dtfhuman`, `dtfhuman_template`, `dtfhuman_creation`, `dtfhuman_chargen` |
| `demon` | `create:demon` (`DemonBasicsView`) | `update:demon` | `demon`, `list:demon`, `demon_chargen` |
| `thrall` | `create:thrall` (`ThrallBasicsView`) | `update:thrall` | `thrall`, `list:thrall`, `thrall_chargen` |
| `earthbound` | `create:earthbound` | `update:earthbound` | `earthbound`, `list:earthbound` |
| `conclave` | `create:conclave` | `update:conclave` | `conclave`, `list:conclave` |

Demon and Hunter detail routes use `<int:pk>`; the other gamelines' detail routes use `<pk>` (their chargen, template and creation routes use `<int:pk>`).

### Hunter

| Type | Create | Update | Detail |
|------|--------|--------|--------|
| `htr_human` | `create:htrhuman` | `update:htrhuman` | `htrhuman`, `list:htrhuman` |
| `hunter` | `create:hunter` | `update:hunter` | `hunter`, `list:hunter` |

### Mummy

| Type | Create | Update | Detail |
|------|--------|--------|--------|
| `mtr_human` | `create:mtrhuman` | `update:mtrhuman` | `mtrhuman`, `list:mtrhuman` |
| `mummy` | `create:mummy` | `update:mummy` | `mummy`, `list:mummy` |

## URL methods

`Human.get_update_url()`, `get_full_update_url()`, `get_creation_url()` and
`get_full_creation_url()` build names from `gameline` and `type`. Types whose routes are
named differently override them:

| Type | Override |
|------|----------|
| `companion`, `sorcerer` | `get_update_url()` returns `get_full_update_url()` (`update:<type>_full`) |
| `htr_human`, `hunter` | `update:htrhuman` / `create:htrhuman`, `update:hunter` / `create:hunter` |
| `fera` and every breed | `update:fera`, `update:fera_full`, `create:fera` (the breeds have only detail routes) |
| `earthbound` | `update:earthbound`, `create:earthbound` |

`ApocalypticForm` has no routes and no URL methods; the demon `Ritual` has no creation
route or `get_creation_url()`.
[`tests/models/test_url_methods.py`](../tests/models/test_url_methods.py) reverses
`get_absolute_url()`, `get_update_url()` and `get_creation_url()` on every concrete model.
The `_full` variants still only resolve for types with a `<type>_full` route (creation:
`human`, `mage` and `companion`); nothing calls them for other types.
`CharacterDetailView` still catches `NoReverseMatch` for the edit link.
[`tests/models/core/test_human_urls.py`](../tests/models/core/test_human_urls.py) tests
the gameline prefix used to build these names, and
[`tests/urls/test_url_patterns.py`](../tests/urls/test_url_patterns.py) tests that core
routes resolve.

## See also

- [Authorization](../../docs/architecture/authorization.md)
- [Character creation](../../docs/architecture/character-creation.md)
- [Forms](forms.md)
- [Templates](templates.md)
- [Adding a view](../../docs/guides/adding-a-view.md)
- [core mixins](../../core/docs/mixins.md)
