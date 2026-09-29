# Adding reference data

This guide covers adding a reference model: game data such as a Discipline, Gift, Sphere,
Lore, Clan or House that every visitor may read and only staff may write. It walks through the
model, the public detail and list pages, the staff create and update forms, the "Known by"
section, templates, URLs, route policies, admin, the `populate_db` data file and the tests. It
is for developers and agents adding a new kind of game data. Why reference data is public is
explained in [Authorization](../architecture/authorization.md#reference-data-is-public) and
[Data model](../architecture/data-model.md#reference-data-and-player-objects).

The running example adds a Demon: the Fallen `Covenant`. It is illustrative; nothing named
`Covenant` exists in `characters/`. The closest real examples are `DemonHouse` and `Lore`
([`characters/models/demon/house.py`](../../characters/models/demon/house.py),
[`characters/models/demon/lore.py`](../../characters/models/demon/lore.py)) and `Discipline`
([`characters/models/vampire/discipline.py`](../../characters/models/vampire/discipline.py)).

## Prerequisites

- The gameline exists (a `settings.GAMELINES` key and a `characters/urls/<app_name>/` package).
- You know how characters will record the data: an integer rating field named after it
  (Disciplines, Spheres), a many-to-many field (Gifts, Rites), a through model with a rating
  (Merits and Flaws), or not at all.

## Choose the base class

| Base | Gives you | Use for | Examples |
|------|-----------|---------|----------|
| `core.models.Model` ([`core/models.py`](../../core/models.py)) | `name`, `description`, `public_info`, `sources` (book references, `add_source()`), `image`, `owner`, `chronicle`, `status`, `display`, `visibility`, `get_gameline()`, `get_type()` | Most reference data | `VampireClan`, `Gift`, `Lore`, `DemonHouse`, `Guild`, `Arcanos` |
| `characters.models.core.statistic.Statistic` | a polymorphic model with `name` and `property_name` only | A trait rated by an integer field of the same name on characters | `Discipline`, `Sphere`, `Background` |
| `django.db.models.Model` | nothing | Rare; you write `__str__` and URL methods yourself | `Edge` |

`core.models.Model.save()` runs `full_clean()`; override `clean()` for cross-field rules,
collecting errors into one dict and raising one `ValidationError`.

## Files you will touch

| Area | File |
|------|------|
| Model | `characters/models/demon/covenant.py`, `characters/models/demon/__init__.py` |
| Schema | `tg_schema/migrations/NNNN_covenant.py`, `tg_schema/tests/test_covenant.py` |
| Views | `characters/views/demon/covenant.py`, `characters/views/demon/__init__.py` |
| Known by | [`characters/views/core/known_by.py`](../../characters/views/core/known_by.py) (optional) |
| URLs | `characters/urls/demon/create.py`, `update.py`, `index.py`, `detail.py` |
| Templates | `characters/templates/characters/demon/covenant/{detail,list,form}.html` |
| Policies | [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py) |
| Admin | [`characters/admin.py`](../../characters/admin.py) |
| Data | `populate_db/demon/demon_covenants.py` |
| Tests | `characters/tests/models/demon/test_covenant.py`, `characters/tests/views/demon/test_covenant.py` |

## Steps

### 1. Model

```python
from django.db import models
from django.urls import reverse

from core.models import Model


class Covenant(Model):
    """A pact tradition shared by several Houses of the Fallen."""

    type = "covenant"
    gameline = "dtf"

    oath = models.TextField(default="", blank=True)
    houses = models.ManyToManyField("DemonHouse", blank=True, related_name="covenants")

    class Meta:
        verbose_name = "Covenant"
        verbose_name_plural = "Covenants"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:demon:covenant", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:demon:update:covenant", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:demon:create:covenant")
```

- `type` is unique snake_case; `gameline` is a `settings.GAMELINES` key and drives theming.
- Do not redeclare fields `core.models.Model` already has (`name`, `description`, `sources`,
  ...).
- Instead of the three URL methods you can mix in `core.models.URLMethodsMixin` and set
  `url_namespace = "characters:demon"` and `url_name = "covenant"`; it reverses
  `<namespace>:<name>`, `<namespace>:update:<name>` and `<namespace>:create:<name>`.
- Export the model from [`characters/models/demon/__init__.py`](../../characters/models/demon/__init__.py).

A new model is a new table: add a `tg_schema` migration that creates it on existing databases
([Changing the schema](changing-the-schema.md#a-new-table)).

### 2. Views

`characters/views/demon/covenant.py`, in the shape of
[`characters/views/vampire/discipline.py`](../../characters/views/vampire/discipline.py):

```python
from django.views.generic import CreateView, UpdateView

from characters.models.demon.covenant import Covenant
from characters.views.core.known_by import KnownByMixin
from core.mixins import MessageMixin
from core.views import CachedDetailView, CachedListView


class CovenantDetailView(KnownByMixin, CachedDetailView):
    model = Covenant
    template_name = "characters/demon/covenant/detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("houses", "sources__book")


class CovenantListView(CachedListView):
    model = Covenant
    ordering = ["name"]
    template_name = "characters/demon/covenant/list.html"


class CovenantCreateView(MessageMixin, CreateView):
    model = Covenant
    fields = ["name", "description", "oath", "houses"]
    template_name = "characters/demon/covenant/form.html"
    success_message = "Covenant created successfully."
    error_message = "There was an error creating the Covenant."


class CovenantUpdateView(MessageMixin, UpdateView):
    model = Covenant
    fields = ["name", "description", "oath", "houses"]
    template_name = "characters/demon/covenant/form.html"
    success_message = "Covenant updated successfully."
    error_message = "There was an error updating the Covenant."
```

- **No login mixin on the read views.** Reference detail and list pages are public; the route
  policy (step 5) is what protects the write views.
- **Caching.** `CachedDetailView` and `CachedListView`
  ([`core/views/generic.py`](../../core/views/generic.py)) apply
  `core.cache.cache_page_per_visitor(CACHE_TIMEOUT_LONG)` (15 minutes) to `dispatch`. Use them,
  or that decorator, and never Django's `cache_page`: pages carry per-user markup (the nav,
  Edit links, messages), and `cache_page` would serve one visitor's page to the next. Cached
  views read no query parameters; a request with a query string bypasses the cache. See
  [Caching](../architecture/caching.md).
- **Read views define no `post()`, `put()`, `patch()` or `delete()`.**
  `test_public_reference_views_do_not_accept_mutating_methods` fails on a `PUBLIC_READ` view
  that does.
- **Explicit field lists** on the create and update views; never `"__all__"`.
- `MessageMixin` flashes the messages and, for `CreateView`, runs `prepare_created_object`
  (owner and starting status) when the model is a `core.models.Model`.
- Export the four views from
  [`characters/views/demon/__init__.py`](../../characters/views/demon/__init__.py).

`core/views/reference.py` holds a factory (`create_reference_views`, `ReferenceViewSet`) that
builds these four classes, but no routed view uses it. Route policies are keyed by the view's
module and class name, so write the classes out in the gameline module as above.

### 3. The "Known by" section (optional)

A reference detail page can list the characters that hold the trait, grouped by chronicle,
showing only characters whose full sheet the viewer may read and nothing to anonymous visitors.
It comes from `known_by()` in
[`characters/views/core/known_by.py`](../../characters/views/core/known_by.py) through
`KnownByMixin`, and needs an entry in `KNOWN_BY_SOURCES` describing where characters record the
trait:

| Source | Characters record it as | Example entry |
|--------|--------------------------|---------------|
| `RatingFields(holders, field=..., minimum=...)` | an integer field on each holder model; `field(obj)` names it (default `property_name`) | `Discipline: RatingFields((Vampire, Ghoul, Revenant))` |
| `Members(holders, "<m2m field>")` | a many-to-many field on each holder model; no rating | `Gift: Members((Werewolf, Fera, Kinfolk), "gifts")` |
| `Ratings(through, "<reference fk>", "<character fk>")` | a through model with a non-zero `rating` | `MeritFlaw: Ratings(MeritFlawRating, "mf", "character", style="number")` |

For the example, if `Demon` gained a `covenants` many-to-many field (a schema change of its
own), the entry would be `Covenant: Members((Demon, Earthbound), "covenants")`. Each source
costs one query per holder model, and the list is capped at `KNOWN_BY_LIMIT` (100) rows.

`KnownByMixin.render_to_response` adds `Vary: Cookie` and, for a signed-in viewer,
`Cache-Control: private`, so the per-viewer list is never stored in or served from the page
cache. Keep the mixin first in the bases, before `CachedDetailView`.

### 4. URLs

Add the four routes to `characters/urls/demon/` (leaf modules export `urls` and define no
`app_name`):

```python
# detail.py
path("covenant/<int:pk>/", CovenantDetailView.as_view(), name="covenant"),
# index.py
path("covenant/", CovenantListView.as_view(), name="covenant"),
# create.py
path("covenant/", CovenantCreateView.as_view(), name="covenant"),
# update.py
path("covenant/<int:pk>/", CovenantUpdateView.as_view(), name="covenant"),
```

These give `characters:demon:covenant`, `characters:demon:list:covenant`,
`characters:demon:create:covenant` and `characters:demon:update:covenant`, the names the model
reverses. Use `<int:pk>` in new routes. See [URL reference](../reference/urls.md).

### 5. Route policies

In [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py), sorted into place:

| Group | Views |
|-------|-------|
| `PUBLIC_READ` | `characters.views.demon.covenant.CovenantDetailView`, `characters.views.demon.covenant.CovenantListView` |
| `STAFF_WRITE` | `characters.views.demon.covenant.CovenantCreateView`, `characters.views.demon.covenant.CovenantUpdateView` |

`STAFF_WRITE` answers 401 to anonymous users and raises `PermissionDenied` (403) for signed-in
users who are not `is_staff` or `is_superuser`.

### 6. Templates

Create `characters/templates/characters/demon/covenant/`. Reference pages use one of two shell
pairs in [`characters/templates/characters/tl/`](../../characters/templates/characters/tl/):

| Gamelines | Detail shell | List shell |
|-----------|--------------|------------|
| Vampire, Wraith, Demon, Hunter, Mummy | `ref2_detail.html` (blocks `ref_back`, `ref_eyebrow`, `ref_facts`, `ref_actions`, `ref_sections`) | `ref2_list.html` (blocks `ref_eyebrow`, `ref_title`, `ref_list`, `ref_empty`, `ref_actions`) |
| Mage, Werewolf, Changeling, core | `reference_detail.html` (blocks `back`, `facts`, `sections`, `description`, `after_description`; shows Edit when `object_perms` allows it) | `reference_list.html` (blocks `cover_title`, `filters`, `ref_create`, shown to staff only, and `content`) |

Both detail shells include `characters/tl/known_by.html` after their sections; it renders
nothing unless the view supplied `known_by`. Copy the Demon House files for the example:

```django
{# detail.html #}
{% extends "characters/tl/ref2_detail.html" %}
{% load tl %}
{% block gameline %}dtf{% endblock gameline %}
{% block ref_back %}<a href="{% url 'characters:demon:list:covenant' %}">← Covenants</a>{% endblock ref_back %}
{% block ref_eyebrow %}Covenant · Demon{% endblock ref_eyebrow %}
{% block ref_facts %}
    {% for house in object.houses.all %}{% fact "House" house %}{% endfor %}
{% endblock ref_facts %}
{% block ref_sections %}
    {% include "characters/tl/ref2_prose.html" with title="Description" text=object.description %}
    {% include "characters/tl/ref2_prose.html" with title="Oath" text=object.oath %}
{% endblock ref_sections %}
```

- List items carry `data-filterable-item` and `data-name="{{ obj.name|lower }}"` so the name
  filter (`widgets/static/widgets/filterable.js`) works.
- The form extends `core/form.html` and renders fields with
  `{% include "core/tl/field.html" with field=form.name %}`, as
  `characters/vampire/discipline/form.html` does.
- Show Edit and "+ New" controls only to staff (`object_perms.can_edit`, or
  `user.is_staff`); the write views refuse everyone else.
- On a cached page, do not render per-user content beyond the nav and do not render
  `{% csrf_token %}`: either makes the page per-visitor (see
  [Caching](../architecture/caching.md#page_media-and-the-csrf-token)).

### 7. Admin

Register the model in [`characters/admin.py`](../../characters/admin.py), with
`list_display` where it helps staff, as `DemonHouseAdmin` does:

```python
@admin.register(Covenant)
class CovenantAdmin(admin.ModelAdmin):
    list_display = ("name",)
```

### 8. Seed data

Put the canonical rows in a `populate_db` script. `python manage.py populate_gamedata`
([`core/management/commands/populate_gamedata.py`](../../core/management/commands/populate_gamedata.py))
finds every `.py` file under `populate_db/` recursively and `exec`s each one in its own
transaction: files directly in `populate_db/` first, then a `core/` subdirectory, then other
subdirectories alphabetically (each sorted by path), then `chronicles/`. A file that fails is
reported and the others still load.

```python
# populate_db/demon/demon_covenants.py
from characters.models.demon.covenant import Covenant
from populate_db.demon.demon_houses import devils, fiends

oathbound = Covenant.objects.get_or_create(
    name="The Oathbound",
    oath="Keep the word given at the Fall.",
)[0]
oathbound.houses.add(devils, fiends)
oathbound.add_source("Demon: The Fallen", 150)
```

- Use `get_or_create` so a second run changes nothing.
- A script may import names from another script (`populate_db.demon.demon_lores` imports the
  House objects from `populate_db.demon.demon_houses`).
- Load only this file with `python manage.py populate_gamedata --only covenants`; `--only`,
  `--skip` and `--gameline` match against the file name, and `--dry-run` lists what would load.

Reference types need no `game.models.ObjectType` row. `populate_db/objects.py` has rows for
many existing reference types; if you add one, also add its name to `EXCLUDED_TYPES` in
[`characters/forms/core/character_creation.py`](../../characters/forms/core/character_creation.py)
and in `ChronicleCharacterCreationForm` in [`game/forms.py`](../../game/forms.py), or it appears
in the storyteller's new-character menus. See [Seed data](../getting-started/seed-data.md).

## Tests

| What | Where and how |
|------|---------------|
| Model: `__str__`, `clean()`, URL methods reverse | `characters/tests/models/demon/test_covenant.py` |
| Detail and list are public: anonymous `GET` returns 200 | `characters/tests/views/demon/test_covenant.py`; see `test_discipline_detail_is_public` in [`characters/tests/views/test_auth_required.py`](../../characters/tests/views/test_auth_required.py) |
| Writes are staff-only: anonymous 401, player 403, staff succeeds | same module; pattern in [`core/tests/security/test_reference_writes.py`](../../core/tests/security/test_reference_writes.py) |
| Known by: owner, storyteller, staff and anonymous see the right rows; the query count stays flat | [`characters/tests/views/test_known_by.py`](../../characters/tests/views/test_known_by.py) |
| One viewer's page is not served to the next | `test_a_viewers_page_is_not_served_to_the_next_viewer` in `test_known_by.py`; `core/tests/test_cache_per_visitor.py` |

Clear the cache in `setUp()` (`django.core.cache.cache.clear()`) in tests of cached pages, as
[`characters/tests/views/test_reference_pages.py`](../../characters/tests/views/test_reference_pages.py)
does, or a page cached by an earlier test is served. The route-policy test,
[`core/tests/test_routed_templates.py`](../../core/tests/test_routed_templates.py) and the
template render smoke test cover the new views and templates without further setup.

## Checklist

- [ ] Model on the right base; unique `type`; `gameline`; `Meta` ordering; URL methods; exported.
- [ ] `tg_schema` migration and test for the new table.
- [ ] Detail and list views cached with `CachedDetailView` / `CachedListView`, no write methods,
  `prefetch_related` for what the template shows.
- [ ] Create and update views with `MessageMixin` and explicit `fields`.
- [ ] `KNOWN_BY_SOURCES` entry and `KnownByMixin` if characters hold the trait.
- [ ] Four routes named after the model's URL methods.
- [ ] `PUBLIC_READ` for reads, `STAFF_WRITE` for writes.
- [ ] Templates on the `ref2_*` or `reference_*` shells; staff-only controls; no per-user
  content on cached pages.
- [ ] Admin registration; idempotent `populate_db` script.
- [ ] Public-read, staff-write and Known-by tests.

## See also

- [Caching](../architecture/caching.md)
- [Authorization](../architecture/authorization.md)
- [Adding a view](adding-a-view.md)
- [Changing the schema](changing-the-schema.md)
- [Seed data](../getting-started/seed-data.md)
- [`characters/README.md`](../../characters/README.md)
