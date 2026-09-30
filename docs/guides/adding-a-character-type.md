# Adding a character type

This guide walks through adding a new playable character model to an existing gameline:
the model, its forms and views, its URLs and templates, its chargen (character creation)
workflow, its route policies, admin, seed data, the schema migration existing databases need,
and the tests and guard files that must be updated. It is for developers and agents adding a
splat such as a new Demon-line mortal. The model tree and the chargen machinery are explained
in [Data model](../architecture/data-model.md) and
[Character creation](../architecture/character-creation.md); this page is the procedure.

The running example adds a `Cultist` to Demon: the Fallen (`gameline = "dtf"`). Every name
containing `Cultist` or `cultist` is illustrative; everything else is real code. The closest
real type to copy is `Thrall`
([`characters/models/demon/thrall.py`](../../characters/models/demon/thrall.py)).

## Prerequisites

- The gameline exists: a key in `settings.GAMELINES` ([`tg/settings/base.py`](../../tg/settings/base.py)),
  a row in `core.constants.GameLine.URL_PATTERNS` and a package in `characters/urls/<app_name>/`.
  Here `dtf` maps to `app_name` `demon`.
- You know which existing model the type extends: `Human`
  ([`characters/models/core/human.py`](../../characters/models/core/human.py)) or the
  gameline's human base (`VtMHuman`, `WtAHuman`, `MtAHuman`, `WtOHuman`, `CtDHuman`,
  `DtFHuman`, `HtRHuman`, `MtRHuman`).
- You have read [Adding a chargen step](adding-a-chargen-step.md) if the type needs a step no
  workflow has yet.

## Files you will touch

| Area | File |
|------|------|
| Model | `characters/models/demon/cultist.py`, `characters/models/demon/__init__.py` |
| Schema | `tg_schema/migrations/NNNN_cultist.py`, `tg_schema/tests/test_cultist.py` |
| Forms | `characters/forms/demon/cultist.py`, [`characters/forms/core/crud_fields.py`](../../characters/forms/core/crud_fields.py), `characters/forms/demon/freebies.py` |
| Views | `characters/views/demon/cultist.py`, `characters/views/demon/cultist_chargen.py`, `characters/views/demon/__init__.py` |
| Router | [`characters/views/core/__init__.py`](../../characters/views/core/__init__.py) (`GenericCharacterDetailView.view_mapping`) |
| Workflow | [`characters/chargen/definitions.py`](../../characters/chargen/definitions.py) |
| Services | `characters/services/freebie_spending/demon.py`, `characters/services/xp_spending/demon.py` (optional) |
| URLs | `characters/urls/demon/create.py`, `update.py`, `index.py`, `detail.py` |
| Templates | `characters/templates/characters/demon/cultist/{basics,chargen,detail,form,list}.html` |
| Policies | [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py) |
| Admin | [`characters/admin.py`](../../characters/admin.py) |
| Seed data | [`populate_db/objects.py`](../../populate_db/objects.py) |
| Guard files | [`core/tests/test_query_budgets.py`](../../core/tests/test_query_budgets.py), [`characters/tests/views/core/shared_character_crud_baseline.json`](../../characters/tests/views/core/shared_character_crud_baseline.json), [`characters/tests/fixtures/chargen_order.json`](../../characters/tests/fixtures/chargen_order.json) |
| Tests | `characters/tests/models/demon/test_cultist.py`, `characters/tests/views/demon/test_cultist.py`, `characters/tests/views/demon/test_cultist_chargen.py` |

## Steps

### 1. Model

Create `characters/models/demon/cultist.py`:

```python
from django.db import models
from django.urls import reverse

from characters.models.demon.dtf_human import DtFHuman


class Cultist(DtFHuman):
    """A mortal follower of an Earthbound cult."""

    type = "cultist"
    gameline = "dtf"

    devotion = models.IntegerField(default=1)
    cult = models.ForeignKey(
        "Earthbound",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cultists",
    )

    background_points = 5

    class Meta:
        verbose_name = "Cultist"
        verbose_name_plural = "Cultists"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:demon:cultist", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:cultist", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:cultist")
```

- **`type`** is a unique snake_case string. It keys the chargen workflow
  (`characters.chargen.get_workflow`), the type router, the spending-service maps and the URL
  names that `Human.get_update_url` and `Human.get_creation_url` build:
  `characters:<app_name>:update:<type>` and `characters:<app_name>:create:<type>`.
- **`gameline`** is a key of `settings.GAMELINES`; `get_gameline()`, theming
  (`gameline_code`) and the URL helpers read it.
- Give every new field a default or `null=True`. The fixture seeder in
  [`core/tests/template_fixtures.py`](../../core/tests/template_fixtures.py) fills required
  fields generically, and existing rows need a value.
- `on_delete=SET_NULL` with `null=True` for links to rows that live on their own.
- URL methods: check what the base class returns. `Character.get_absolute_url` returns
  `characters:character` (the type router, which also serves the wizard), and `Human` builds
  the update and create names from `type`. Several bases override them with their own route
  names: `DtFHuman` returns `characters:demon:dtfhuman`, `characters:demon:update:dtfhuman` and
  `characters:demon:create:dtfhuman`, so a `DtFHuman` subclass overrides all three again, as `Thrall`, `Demon` and the example
  do. On a base that keeps the
  inherited methods (`WtAHuman`, `MtAHuman`), the type's routes only have to be named after
  `type`.
- Game rules (XP costs, `spend_xp`, `xp_frequencies`) go on the model or in a service; see
  `Thrall.spend_xp` for the locked (`select_for_update()` inside `transaction.atomic()`)
  pattern.

Export it from [`characters/models/demon/__init__.py`](../../characters/models/demon/__init__.py)
(`from .cultist import Cultist` and the `__all__` entry). `characters/models/__init__.py`
imports each gameline package, which is how Django finds the model.

### 2. Schema for existing databases

A new model is a new table. Fresh and test databases get it from the model; databases created
before it need a `tg_schema` migration that creates the table when it is missing. Follow
[Changing the schema](changing-the-schema.md#a-new-table). Do not commit anything from
`characters/migrations/` except `__init__.py`.

### 3. Forms

**Creation (basics) form**, `characters/forms/demon/cultist.py`. The first page of creation
collects identity fields, like `ThrallCreationForm`
([`characters/forms/demon/thrall.py`](../../characters/forms/demon/thrall.py)):

```python
from django import forms

from characters.models.demon.cultist import Cultist
from characters.models.demon.earthbound import Earthbound


class CultistCreationForm(forms.ModelForm):
    class Meta:
        model = Cultist
        fields = ["name", "nature", "demeanor", "concept", "cult", "chronicle", "image", "npc"]

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["cult"].queryset = Earthbound.objects.all()
        self.fields["cult"].required = False
        self.fields["image"].required = False
```

**Storyteller edit field list.** Character update views take their full field list from
[`characters/forms/core/crud_fields.py`](../../characters/forms/core/crud_fields.py), an
explicit, reviewed allowlist ("never derive editable fields by introspection"). Add a tuple
built from the shared groups and lists there. The ability fields must be the ones the model
has: a Demon-line mortal has the DtF abilities that `DT_F_HUMAN_UPDATE_FIELDS` lists.

```python
CULTIST_UPDATE_FIELDS = (
    *DT_F_HUMAN_UPDATE_FIELDS,
    "devotion",
    "cult",
)
```

Never list `owner`, `chronicle`, `gameline`, `status`, `npc`, `xp`, `freebies_approved`,
`approved` or `approved_by`: the `OBJECT_WRITE` policy refuses a non-staff `POST` that changes
them (see [Authorization](../architecture/authorization.md#the-policies)).

**Owner edit form.** Owners get a limited form. `LimitedHumanEditForm`
([`characters/forms/core/limited_edit.py`](../../characters/forms/core/limited_edit.py))
works for every `Human` subclass: `notes`, `description`, `public_info`, `image`, `history`,
`goals`.

**Pin the field list in the baseline.**
[`characters/tests/views/core/test_shared_character_crud.py`](../../characters/tests/views/core/test_shared_character_crud.py)
compares each update view's `fields` with
[`shared_character_crud_baseline.json`](../../characters/tests/views/core/shared_character_crud_baseline.json):
a field count and the SHA-256 of the field names joined by newlines (duplicates removed, order
kept), plus the limited form's class name. Compute the entry:

```bash
python manage.py shell -c "import hashlib; from characters.forms.core.crud_fields import CULTIST_UPDATE_FIELDS as F; f = list(dict.fromkeys(F)); print(len(f), hashlib.sha256('\n'.join(f).encode()).hexdigest())"
```

and add, keyed by the view's dotted path:

```json
"characters.views.demon.cultist.CultistUpdateView": {
  "fields_sha256": "<hash>",
  "field_count": <count>,
  "limited_form": "LimitedHumanEditForm"
}
```

**Freebies form.** The freebies step uses a subclass of
`characters.forms.core.freebies.HumanFreebiesForm` that sets the category choices, as
`ThrallFreebiesForm` in
[`characters/forms/demon/freebies.py`](../../characters/forms/demon/freebies.py) does.

### 4. Views

**Detail, update and list**, `characters/views/demon/cultist.py`, following
[`characters/views/demon/thrall.py`](../../characters/views/demon/thrall.py) and
`HumanUpdateView`:

```python
from django.views.generic import ListView, UpdateView

from characters.forms.core.crud_fields import CULTIST_UPDATE_FIELDS
from characters.forms.core.limited_edit import LimitedHumanEditForm
from characters.models.demon.cultist import Cultist
from characters.views.core.human import HumanDetailView
from core.mixins import (
    EditPermissionMixin,
    MessageMixin,
    ScopedEditFormMixin,
    VisibilityFilterMixin,
)


class CultistDetailView(HumanDetailView):
    model = Cultist
    template_name = "characters/demon/cultist/detail.html"


class CultistUpdateView(ScopedEditFormMixin, EditPermissionMixin, MessageMixin, UpdateView):
    model = Cultist
    fields = CULTIST_UPDATE_FIELDS
    limited_form_class = LimitedHumanEditForm
    template_name = "characters/demon/cultist/form.html"
    success_message = "Cultist updated successfully."
    error_message = "Error updating cultist."


class CultistListView(VisibilityFilterMixin, ListView):
    model = Cultist
    template_name = "characters/demon/cultist/list.html"
    context_object_name = "cultists"
    paginate_by = 25

    def get_queryset(self):
        return super().get_queryset().select_related("owner", "cult", "chronicle").order_by("name")
```

- `HumanDetailView` extends `CharacterDetailView` (`ViewPermissionMixin`), which adds scenes,
  `chargen_url`, `edit_url` and the retire and decease flags to the context.
- `ScopedEditFormMixin.get_form_class()` returns the full form built from `fields` for a
  scoped editor (`PermissionManager.user_has_scoped_editor_role`: staff, the chronicle's head
  ST, or a storyteller for the chronicle and gameline) and `limited_form_class` for anyone else
  `EditPermissionMixin` lets in, such as the owner of a draft.
- Detail views never define `post()`; state changes are separate `ObjectActionView` endpoints
  ([`core/tests/test_action_guard.py`](../../core/tests/test_action_guard.py) fails otherwise).

**Chargen views**, `characters/views/demon/cultist_chargen.py`. Each workflow step is a view
class; reuse the shared ones by subclassing and setting `model` and `template_name`, as
[`characters/views/demon/thrall_chargen.py`](../../characters/views/demon/thrall_chargen.py)
does:

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import FormView

from characters.chargen.registry import WorkflowViews
from characters.forms.core.linked_npc import LinkedNPCForm
from characters.forms.demon.cultist import CultistCreationForm
from characters.forms.demon.freebies import CultistFreebiesForm
from characters.models.demon.cultist import Cultist
from characters.views.core.backgrounds import HumanBackgroundsView
from characters.views.core.extras import CharacterExtrasView
from characters.views.core.generic_background import GenericBackgroundView
from characters.views.core.human import (
    HumanAbilityView,
    HumanAttributeView,
    HumanCharacterCreationView,
    HumanFreebiesView,
    HumanLanguagesView,
    HumanSpecialtiesView,
)
from characters.views.demon.cultist import CultistDetailView
from core.mixins import ScopedCreationFormMixin, prepare_created_object
from core.permissions import PermissionManager

TEMPLATE = "characters/demon/cultist/chargen.html"


class CultistBasicsView(ScopedCreationFormMixin, LoginRequiredMixin, FormView):
    form_class = CultistCreationForm
    template_name = "characters/demon/cultist/basics.html"

    def get_form_kwargs(self):
        return {**super().get_form_kwargs(), "user": self.request.user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["storyteller"] = PermissionManager.user_can_manage_creation(
            self.request.user, context["form"], request=self.request
        )
        return context

    def form_valid(self, form):
        prepare_created_object(form, self.request)  # owner, starting status, chronicle check
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("characters:character", kwargs={"pk": self.object.pk})


class CultistAttributeView(HumanAttributeView):
    model = Cultist
    template_name = TEMPLATE


class CultistAbilityView(HumanAbilityView):
    model = Cultist
    fields = Cultist.primary_abilities
    template_name = TEMPLATE
    primary, secondary, tertiary = 13, 9, 5


class CultistBackgroundsView(HumanBackgroundsView):
    model = Cultist
    template_name = TEMPLATE


class CultistExtrasView(CharacterExtrasView):
    model = Cultist
    fields = ["age", "apparent_age", "date_of_birth", "history", "goals", "notes"]
    template_name = TEMPLATE
    optional_fields = ("notes", "history", "goals")


class CultistFreebiesView(HumanFreebiesView):
    model = Cultist
    form_class = CultistFreebiesForm
    template_name = TEMPLATE


class CultistLanguagesView(HumanLanguagesView):
    model = Cultist
    template_name = TEMPLATE


class CultistAlliesView(GenericBackgroundView):
    background_name = "allies"
    primary_object_class = Cultist
    model = Cultist
    template_name = TEMPLATE
    form_class = LinkedNPCForm


class CultistSpecialtiesView(HumanSpecialtiesView):
    model = Cultist
    template_name = TEMPLATE


class CultistCharacterCreationView(HumanCharacterCreationView):
    view_mapping = WorkflowViews()
    model_class = Cultist
    key_property = "creation_status"
    default_redirect = CultistDetailView
```

- `prepare_created_object` ([`core/mixins.py`](../../core/mixins.py)) sets the owner (or no
  owner when a storyteller posts `shared=1`), sets status `Un` for non-admins and refuses a
  chronicle the user cannot read. Several existing basics views (`ThrallBasicsView`,
  `VampireBasicsView`) set only the owner, in their form's `save()`; `MessageMixin` calls
  `prepare_created_object` automatically only for `CreateView` subclasses.
- The basics templates show the `npc` checkbox only when `storyteller` is true.
  `ScopedCreationFormMixin.get_form()` enforces the same rule on the server: it removes the
  `npc` field when `PermissionManager.user_can_manage_creation(...)` is false, so a player's
  posted `npc=on` is ignored.
- `CultistCharacterCreationView` is the chargen router: `WorkflowViews()` resolves
  `get_workflow(Cultist.type).view_mapping` (position to step view), and the router
  dispatches by `creation_status` while the status is `Un` or `Rev`.
- **Set `default_redirect` to your own detail view.** `DictView.get_default_redirect`
  authorizes it with `authorize_route`, which denies a view that has no route policy. Django's
  generic `DetailView` has none.
- The last step (`HumanSpecialtiesView.form_valid`) sets the status to `Sub`.
- Keep every `ChargenStepMixin` subclass in the module in the workflow:
  `test_no_orphan_step_views` in
  [`characters/tests/test_chargen_registry.py`](../../characters/tests/test_chargen_registry.py)
  fails on an unused one.

Export the views from
[`characters/views/demon/__init__.py`](../../characters/views/demon/__init__.py): the URL
modules import `CultistBasicsView`, `CultistDetailView`, `CultistListView`,
`CultistUpdateView` and `CultistCharacterCreationView` from `characters.views.demon`.

### 5. Register the type with the router

Add the type to `GenericCharacterDetailView.view_mapping` in
[`characters/views/core/__init__.py`](../../characters/views/core/__init__.py):

```python
# Demon
"thrall": demon.ThrallCharacterCreationView,
"cultist": demon.CultistCharacterCreationView,
```

`characters:character` (`/characters/<pk>/`) resolves the object, looks up its `type` here
and hands off to your router (a type with no wizard maps straight to its detail view, as
`"earthbound": demon.EarthboundDetailView` does).
`test_router_coverage` in `characters/tests/test_chargen_registry.py` checks that every
mapped router with `chargen_router = True` has a workflow with the same view mapping, and that
every other mapped type has none.

### 6. Chargen workflow

Declare the ordered steps in
[`characters/chargen/definitions.py`](../../characters/chargen/definitions.py) with `bind()`,
which turns shared `Step` definitions into steps bound to your view module. A step's view is
`<module>.<prefix><Step.view_path>View` unless you name it in `views={...}`, and its step-body
template is the `Step`'s unless you override it in `templates={...}`:

```python
CULTIST = bind(
    STATS  # attributes, abilities, backgrounds
    + (
        EXTRAS,
        FREEBIES,
        LANGUAGES,
        ALLIES,
        SPECIALTIES,
    ),
    "characters.views.demon.cultist_chargen",
    "Cultist",
)

WORKFLOWS = {
    ...
    "cultist": CULTIST,
}
```

`Workflow` requires unique step keys and exactly one `freebies` step. Positions are stored in
`Character.creation_status` (1-based), so once characters exist, reordering steps needs a
migration; see [Adding a chargen step](adding-a-chargen-step.md#reordering-steps).

Record the workflow in the golden fixture
[`characters/tests/fixtures/chargen_order.json`](../../characters/tests/fixtures/chargen_order.json)
(type to ordered list of dotted step-view paths). `test_all_persisted_positions_are_preserved`
checks every workflow listed there against the registry, and that each step's template loads.

A type without a creation wizard gets no workflow. Its freebie position then comes from
`DETAIL_ONLY_FREEBIE_POSITIONS` in the same module (`Character.freebie_step` is `-1` for a type
in neither place); that dictionary is pinned by
`test_detail_only_types_preserve_freebie_metadata_without_a_wizard`.

### 7. Spending services (optional)

Freebie and XP spending pick a service by `character.type` and fall back to the Human
services. To give the type its own rules, subclass the Human service and register it at the
bottom of the gameline module, as Thrall does:

```python
# characters/services/freebie_spending/demon.py
FreebieSpendingServiceFactory.register("cultist", CultistFreebieSpendingService)
# characters/services/xp_spending/demon.py
XPSpendingServiceFactory.register("cultist", CultistXPSpendingService)
```

### 8. URLs

Add one route per module in `characters/urls/demon/`. Leaf modules export a plain `urls`
list and must not define `app_name`
(`test_list_included_url_modules_have_no_app_name` in
[`core/tests/test_dead_code_removed.py`](../../core/tests/test_dead_code_removed.py)). The
names must match what the model's URL methods reverse (`type` for `Human` subclasses):

```python
# create.py
path("cultist/", CultistBasicsView.as_view(), name="cultist"),
# update.py
path("cultist/<int:pk>/", CultistUpdateView.as_view(), name="cultist"),
# index.py
path("cultist/", CultistListView.as_view(), name="cultist"),
# detail.py
path("cultist/<int:pk>/", CultistDetailView.as_view(), name="cultist"),
```

This gives `characters:demon:create:cultist`, `characters:demon:update:cultist`,
`characters:demon:list:cultist` and `characters:demon:cultist`. Some gamelines also route
`<type>/<int:pk>/chargen/` to the creation router (`characters:demon:thrall_chargen`); no
application code reverses those names (only tests do), and the wizard's URL is
`characters:character`. See
[URL reference](../reference/urls.md).

### 9. Templates

Create `characters/templates/characters/demon/cultist/`, copying the Thrall files:

| File | Extends | Content |
|------|---------|---------|
| `basics.html` | `core/form.html` | `creation_title`, `formdetails` (multipart), fields through `{% include "core/tl/field.html" with field=form.x %}`, the NPC checkbox inside `{% if storyteller %}` |
| `chargen.html` | `characters/core/chargen.html` | nothing else; `ChargenStepMixin.get_template_names()` renders a `template_name` ending in `/chargen.html`, otherwise the shared `characters/core/chargen.html` |
| `detail.html` | `characters/demon/dtfhuman/detail.html` | override the sheet blocks (`basics`, `powers`, `advantages`, `line`, ...) of [`characters/core/human/detail.html`](../../characters/templates/characters/core/human/detail.html); never their order |
| `form.html` | `core/form.html` | `{% include "characters/tl/character_edit_fields.html" %}` in `contents` |
| `list.html` | `characters/tl/ref2_chars.html` | `gameline` block `dtf`, titles, a loop over `cultists` with `characters/tl/ref2_char_tile.html` |

Rules (see [Front end](../architecture/frontend.md)):

- Sheet cover facts use `{% fact "Label" value %}`, ratings `{% dots %}`, tracks
  `{% track "Willpower" perm=... temp=... %}` from `{% load tl %}`.
- No inline `style=""` or `<style>` block, no Bootstrap, jQuery or `tg-card` markup;
  [`core/tests/test_template_policy.py`](../../core/tests/test_template_policy.py) ratchets
  inline styles and style blocks.
- At most 5 `{% extends %}` hops below the root (`test_extends_depth`): the chain here is
  `tl_base` → `character/detail` → `human/detail` → `dtfhuman/detail` → `cultist/detail`.
- Permission-dependent controls read `object_perms` (added by `PermissionContextMixin` and by
  `AuthorizationMiddleware.process_template_response`).

### 10. Route policies

Every routed view, and every view a router can hand off to, needs exactly one entry in
[`core/route_policy_manifest.py`](../../core/route_policy_manifest.py). Add each dotted path to
its group, keeping the lists sorted:

| Group | Views |
|-------|-------|
| `LOGIN` | `characters.views.demon.cultist_chargen.CultistBasicsView` (the gameline basics views are listed here) |
| `OBJECT_DETAIL` | `characters.views.demon.cultist.CultistDetailView` |
| `OBJECT_WRITE` | `characters.views.demon.cultist.CultistUpdateView` |
| `OBJECT_LIST` | `characters.views.demon.cultist.CultistListView` |
| `ROUTER` | `characters.views.demon.cultist_chargen.CultistCharacterCreationView` |
| `CHARGEN_STEP` | every step view: `CultistAttributeView`, `CultistAbilityView`, ... `CultistSpecialtiesView` |

[`core/tests/security/test_route_policies.py`](../../core/tests/security/test_route_policies.py)
walks every URL and every router branch and fails on a missing or duplicate declaration. See
[Authorization](../architecture/authorization.md#choosing-the-policy-for-a-new-route).

### 11. Admin

Register the model in [`characters/admin.py`](../../characters/admin.py):

```python
@admin.register(Cultist)
class CultistAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "cult", "devotion")
    list_filter = ("owner",)
```

### 12. Seed the type menu

The "new character" menu (`characters.forms.core.character_creation.CharacterCreationForm`)
lists `game.models.ObjectType` rows with `type="char"`, and choosing one redirects through
`core.create_redirects.resolve_object_type_url` to
`characters:<app_name>:create:<ObjectType.name>`. Add the row to
[`populate_db/objects.py`](../../populate_db/objects.py), with the name equal to the create
route's name:

```python
ObjectType.objects.get_or_create(name="cultist", type="char", gameline="dtf")
```

Storytellers see every gameline in the menu; other users see only Mage types. Existing
databases pick up the row with `python manage.py populate_gamedata --only objects`. See
[Seed data](../getting-started/seed-data.md).

### 13. Tests

Add tests under `characters/tests/`, mirroring the source path:

- **Model** (`characters/tests/models/demon/test_cultist.py`): defaults, `clean()` rules, XP
  and freebie costs, `get_update_url()` and `get_creation_url()` resolve.
- **Views** (`characters/tests/views/demon/test_cultist.py`), following
  `characters/tests/views/demon/test_thrall.py`: the owner and a chronicle storyteller get the
  full sheet; another user gets the public card (`core/public_object_detail.html`, status 200)
  on `GET`; the owner gets `LimitedHumanEditForm` and a scoped storyteller the full form; a
  player cannot change `status` or `npc` through the update form (403).
- **Chargen** (`characters/tests/views/demon/test_cultist_chargen.py`): walk
  `reverse("characters:character", kwargs={"pk": ...})` step by step, as
  [`characters/tests/views/test_chargen_nojs_walkthrough.py`](../../characters/tests/views/test_chargen_nojs_walkthrough.py)
  does, and check the last step sets `Sub`.
- **Query ceiling.** Add `"characters.Cultist": <n>` to `SHEET_CEILINGS` in
  [`core/tests/test_query_budgets.py`](../../core/tests/test_query_budgets.py).
  `test_every_character_model_has_a_ceiling` fails until the label is there; measure the
  sheet's query count for the fixture storyteller and use that number.
- **Template fixtures.** `core.tests.template_fixtures.seed()` creates one approved instance of
  every concrete character model; [`core/tests/test_template_render_smoke.py`](../../core/tests/test_template_render_smoke.py)
  then renders its detail and edit pages and every list page. The model must be creatable
  with generic values, or `test_fixture_set_covers_the_models` reports it as skipped.
- The route-policy, routed-template, CRUD-baseline and chargen-registry tests cover the new
  files automatically once steps 3 to 10 are done.

Run them with `python manage.py test characters core tg_schema`. See
[Testing](../development/testing.md).

## Checklist

- [ ] Model subclasses the gameline human base; unique `type`, valid `gameline`, `Meta`
  names and ordering; new fields defaulted or nullable; exported from the gameline package.
- [ ] `tg_schema` migration and test for the new table.
- [ ] Creation form; `*_UPDATE_FIELDS` in `crud_fields.py`; baseline JSON entry; freebies form.
- [ ] Detail, update (`ScopedEditFormMixin` + `limited_form_class`), list
  (`VisibilityFilterMixin`, `select_related`) and basics views.
- [ ] Step views and a `...CharacterCreationView` whose `default_redirect` is the type's
  detail view; all exported.
- [ ] `GenericCharacterDetailView.view_mapping` entry.
- [ ] Workflow in `definitions.py` and `WORKFLOWS`; golden fixture updated.
- [ ] URL routes named after the model's URL methods; no `app_name` in leaf modules.
- [ ] Templates extend the Spread shells; no inline styles; extends depth at most 5.
- [ ] Every view in exactly one manifest group.
- [ ] Admin registration; `ObjectType` row in `populate_db/objects.py`.
- [ ] Model, view and chargen tests; `SHEET_CEILINGS` entry.

## See also

- [Character creation](../architecture/character-creation.md)
- [Adding a chargen step](adding-a-chargen-step.md)
- [Adding a view](adding-a-view.md)
- [Authorization](../architecture/authorization.md)
- [Changing the schema](changing-the-schema.md)
- [`characters/README.md`](../../characters/README.md)
