# Core models

This page describes the models, managers and model mixins defined in
[`core/models.py`](../models.py) and [`core/base.py`](../base.py), and the choice
constants in [`core/constants.py`](../constants.py). It is for anyone adding a model that
inherits from them or reading data through them.

## Validation on save

Every core model validates itself when saved.

- `core.base.ValidatedSaveMixin` is for ordinary (non-polymorphic) models. Its `save()`
  calls `full_clean()` first. It lives in `core/base.py` so that model modules in other
  apps can import it without importing `core.models` (which imports `game.models`).
- `core.models.Model.save()` does the same for the polymorphic tree.

Both accept `skip_validation=True` to bypass the check:

```python
obj.save(skip_validation=True)   # no full_clean(); use only for bulk or repair code
```

`full_clean()` runs field validation plus each model's `clean()`, so a `ValidationError`
from `save()` is the normal signal that data is invalid.

## The polymorphic base: `core.models.Model`

`Model` is an abstract model that combines `PermissionMixin` with django-polymorphic's
`PolymorphicModel`. `characters.CharacterModel`, `items.ItemModel`,
`locations.LocationModel` and `core.CharacterTemplate` derive from it, so every
player-facing object has the same fields and permission behaviour.

| Field | Type | Notes |
|-------|------|-------|
| `name` | `CharField(200)` | Required (`clean()` rejects blank) |
| `owner` | FK `User`, nullable | `SET_NULL`; indexed. `None` means a shared (storyteller-owned) object |
| `chronicle` | FK `game.Chronicle`, nullable | `SET_NULL`; indexed. Scopes storyteller roles |
| `status` | `CharField(3)` | `CharacterStatus.CHOICES`, default `"Un"`; indexed |
| `display` | `BooleanField` | Default `True`; `ModelQuerySet.visible()` filters on it |
| `sources` | M2M `BookReference` | Sourcebook citations |
| `description`, `public_info`, `st_notes` | `TextField` | `public_info` is what anonymous public cards show |
| `image` | `ImageField` | Upload path from `core.utils.filepath` |
| `image_status` | `CharField(3)` | `ImageStatus.CHOICES`, default `"sub"` |
| `freebies_approved` | `BooleanField` | Set by storytellers |
| `visibility` | `CharField(3)` | From `PermissionMixin`, see below |

Class attributes, not fields:

- `type`: a short identifier (`"model"` here; subclasses set e.g. `"vtm_human"`).
  `get_type()` title-cases it for display.
- `gameline`: the gameline code (`"wod"` by default). `get_gameline()` reads it and
  `get_full_gameline()` maps it to the name in `settings.GAMELINES`.
- `SECONDARY_TYPES`: mortal and spirit types; `is_primary_type()` and
  `get_badge_class()` use it.

`clean()` checks that `name` is not blank and that `status` and `image_status` are valid
choices. Other helpers: `has_name()`, `set_name()`, `update_status()`, `has_source()`,
`add_source(book_title, page_number)` (creates the `Book` and `BookReference` if needed),
`get_heading()` (returns `"<gameline>_heading"`).

### `PermissionMixin`

An abstract mixin that adds:

- `visibility`: `"PUB"` (Public), `"PRI"` (Private, the default), `"CHR"` (Chronicle
  Only) or `"CUS"` (Custom). Only the public-card list
  (`core.views.public_object.render_public_object_list`) reads it: `PUB` rows are listed
  for everyone and `CHR` rows for users who can read the object's chronicle. `CUS` has no
  behaviour of its own. Full access is always decided by `PermissionManager`, never by
  this field.
- `observers`: a `GenericRelation` to `Observer`.
- `add_observer(user, granted_by)` and `remove_observer(user)`.

### `ModelQuerySet` and `ModelManager`

`Model.objects` is a `ModelManager`, a `PolymorphicManager` built from `ModelQuerySet`.

| Method | Returns |
|--------|---------|
| `with_polymorphic_ctype()` | `select_related("polymorphic_ctype")`. Call it before iterating rows whose subclass methods you use (`get_absolute_url()`, `get_type()`...). Not needed for `count()`, `exists()`, `values()` or a query already restricted to one subclass |
| `pending_approval_for_user(user)` | Submitted (`status="Sub"`) rows in chronicles the user staffs (plus chronicle-less rows for staff), with owner, profile, chronicle and ctype joined, ordered by name |
| `visible()` | `display=True` |
| `for_chronicle(chronicle)` | Rows in that chronicle |
| `owned_by(user)` | Rows the user owns |
| `with_pending_images()` | `image_status="sub"` with a non-empty image |
| `for_user_chronicles(user)` | Rows in chronicles the user staffs (plus chronicle-less rows for staff) |

"Staffs" comes from `game.security.staffed_chronicles`.

The manager does not add `select_related("polymorphic_ctype")` automatically: most
queries do not need it and it adds a join to each.

## `URLMethodsMixin`

A mixin for models whose URLs follow the `<namespace>:<name>`,
`<namespace>:update:<name>`, `<namespace>:create:<name>` pattern. Set `url_namespace`
(required) and optionally `url_name` (defaults to the lowercased class name); it provides
`get_absolute_url()`, `get_update_url()` and the class method `get_creation_url()`. Each
raises `NotImplementedError` when `url_namespace` is unset.

```python
class Archetype(URLMethodsMixin, models.Model):
    url_namespace = "characters"
    url_name = "archetype"
# get_absolute_url() -> reverse("characters:archetype", kwargs={"pk": self.pk})
```

Item and location types use `core.registry_urls.RegistryURLMixin` instead, which asks the
app's model registry for the URL (see [views](views.md#registry-views)).

## Concrete core models

| Model | Purpose | Key fields and rules |
|-------|---------|----------------------|
| `Book` | A sourcebook | `name`, `url`, `edition` (1e, 2e, Rev, 20th, DA, VA, WW, SC, KotE), `gameline` (from `settings.GAMELINE_CHOICES`), `storytellers_vault`. `clean()` requires a name and a valid gameline. URL `core:book` |
| `BookReference` | A page in a book | `book` (FK, `SET_NULL`), `page` (must be ≥ 0). `str()` returns HTML (`<i>book</i> p. N`); templates build citations from `book` and `page` instead (`core/tl/source_facts.html`) |
| `Observer` | Grants one user observer access to one object | Generic FK (`content_type`, `object_id`), `user`, `granted_by`, `granted_at`, `notes`. Unique per (content type, object, user). `clean()` checks the target exists |
| `NewsItem` | Front-page news | `title`, `content` (both required), `date`. URLs `core:newsitem`, `core:update_newsitem`, `core:create_newsitem` |
| `Language` | A language a character can speak | `name` (required), `frequency` (≥ 0; orders the suggestions in `core.forms.HumanLanguageForm` and weights random language choice in `items` grimoire generation). URLs `core:language`, `core:update_language`, `core:create_language` |
| `HouseRule` | A table rule | `name`, `description`, `sources`, optional `chronicle`, `gameline`. `clean()` requires a name and valid gameline |
| `Noun` | A plain word list row | `name` (required) |
| `Number` | A single integer | `value`; no validation mixin |
| `CharacterTemplate` | A reusable character build | See below |
| `TemplateApplication` | Audit row: template applied to a character | `character` (FK `characters.Character`, cascade), `template` (`SET_NULL`), `applied_at` |

### `CharacterTemplate`

A concrete subclass of `Model` (so it has owner, chronicle, status and the permission
behaviour). Its `type` is `"character_template"`.

- Descriptive fields: `gameline` (from `GameLine.CHOICES`), `character_type` (free text,
  required), `concept`, `faction`.
- JSON data: `basic_info`, `attributes`, `abilities`, `backgrounds` (list of
  `{name, rating}`), `powers`, `merits_flaws` (list of `{name, rating}`), `specialties`
  (list of `"Ability (Specialty)"` strings), `languages`, `suggested_freebie_spending`;
  plus `equipment` text.
- Metadata: `is_official` (default `True`), `is_public` (default `True`), `times_used`,
  `created_at`, `updated_at`.
- Unique on (`gameline`, `character_type`, `name`).

`clean()` requires `character_type` and restricts `gameline` to `wod`, `vtm`, `wta`,
`mta`, `wto`, `ctd` and `dtf`.

Here `gameline` is a model field, not a class attribute. Read `template.gameline`:
the inherited `get_gameline()` reads the class attribute, so on a template it returns
the field descriptor rather than the stored code. As a result `get_heading()` returns a
string built from that descriptor and the `tl` filter `gameline_code` returns `"wod"` for
every template, so template pages always use the generic theme.

`apply_to_character(character)` copies the template onto a character: `basic_info`
values of the form `"FK:Archetype:<name>"` are resolved to `Archetype` rows; attributes,
abilities and powers are set when the character has a matching attribute; backgrounds,
merits and flaws, languages and specialties are looked up by name and created as rating
rows (unknown names are skipped). It then saves the character, records a
`TemplateApplication` and increments `times_used`.

Official templates can be edited only by a storyteller scoped to them (see
[permissions](permissions-and-policies.md#route-policies)).

## Abstract rating bases

Through-models in other apps share these abstract bases. Each subclass adds its own parent
foreign key, `Meta` constraints and extra fields.

| Base | Fields it provides |
|------|--------------------|
| `BaseMeritFlawRating` | `mf` (FK `characters.MeritFlaw`, cascade), `rating` (-10..10) |
| `BaseBackgroundRating` | `bg` (FK `characters.Background`, `SET_NULL`), `rating` (0..10), `note`, `url`, `complete` |
| `BasePracticeRating` | `practice` (FK `characters.Practice`, `SET_NULL`); the subclass defines `rating` |
| `BaseResonanceRating` | `rating` (0..10); the subclass defines the `resonance` FK |

## Constants

[`core/constants.py`](../constants.py) holds the choice sets used across apps:

| Class | Values |
|-------|--------|
| `GameLine` | Codes `wod`, `vtm`, `wta`, `mta`, `wto`, `ctd`, `dtf`, `htr`, `mtr` with `CHOICES`; `URL_PATTERNS` lists `(url_path, module_name, namespace)` for the eight gameline URL modules |
| `CharacterStatus` | `Un` (Unapproved), `Rev` (Returned for revisions), `Sub` (Submitted), `App` (Approved), `Dec` (Deceased), `Ret` (Retired) |
| `ImageStatus` | `un`, `sub`, `app` |
| `ObjectTypeChoices` | `char`, `loc`, `obj` |
| `HeadingChoices` | `<code>_heading` values for seven gamelines |
| `ThemeChoices` | `light`, `dark` |
| `AbilityFields` | `TALENTS`, `SKILLS`, `KNOWLEDGES`, `PRIMARY_ABILITIES` field-name lists |
| `XPApprovalStatus` | `Pending`, `Approved`, `Denied` |

Gameline display names and URL app names come from `settings.GAMELINES` (which also
includes `orp`), not from `GameLine`. Use `settings.GAMELINE_CHOICES` for model fields
that should accept every configured gameline.

## See also

- [Data model](../../docs/architecture/data-model.md)
- [Permissions and policies](permissions-and-policies.md)
- [Glossary](../../docs/reference/glossary.md)
- [`core/models.py`](../models.py)
- [characters app](../../characters/README.md)
