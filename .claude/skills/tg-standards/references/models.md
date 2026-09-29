# Models

Rules and checklists for adding or changing a model, field, manager or relation. The
concepts (the three polymorphic trees, gamelines, the status lifecycle, reference data
versus player objects) are explained in
[docs/architecture/data-model.md](../../../../docs/architecture/data-model.md); field-level
reference is in [core/docs/models.md](../../../../core/docs/models.md) and
[characters/docs/models.md](../../../../characters/docs/models.md). Schema consequences are in
[schema-changes.md](schema-changes.md).

## Pick the base class

| You are adding | Subclass | Gets |
|----------------|----------|------|
| A character type | `characters.models.core.human.Human` (or a gameline human such as `VtMHuman`); `CharacterModel` only for non-human sheets such as `SpiritCharacter` | Stats blocks, chargen, sheet, `npc`, `xp`, status machine |
| A player group (coterie, pack, cabal) | `characters.models.core.group.Group` | Members, ownership, approval |
| An item | `items.models.core.item.ItemModel` | Registry URLs (`RegistryURLMixin`), `ItemQuerySet` |
| A location | `locations.models.core.location.LocationModel` | Registry URLs, `parent`, `LocationQuerySet.top_level()` |
| Reference data or another owned object (clan, tribe, gift, rote) | `core.models.Model` | `name`, `owner`, `chronicle`, `status`, `sources`, `description`, `public_info`, `image`, `visibility`, `observers` |
| A ratable trait (discipline, sphere, ability) | `characters.models.core.statistic.Statistic` | `name`, `property_name`, polymorphism |
| A plain record (rating row, request, log) | `core.base.ValidatedSaveMixin` first, then `models.Model` | `full_clean()` on save |

Never redefine a field inherited from `core.models.Model`
([`core/models.py`](../../../../core/models.py)). Add sources with `add_source(book_title,
page_number)`; do not create `BookReference` rows by hand.

## Class attributes

Every `core.models.Model` subclass sets two class attributes (not fields):

```python
class Revenant(VtMHuman):
    type = "revenant"   # snake_case, unique in its app
    gameline = "vtm"    # a key of settings.GAMELINES
```

- `type` keys `characters.views.core.GenericCharacterDetailView.view_mapping` and
  `characters.chargen.get_workflow(type)`. A new character type needs an entry in both;
  see [docs/guides/adding-a-character-type.md](../../../../docs/guides/adding-a-character-type.md).
- `gameline` drives `get_heading()`, `get_badge_class()`, the `gameline_code` template
  filter, and `PermissionManager`'s scoped ST roles (it matches
  `settings.GAMELINES[code]["name"]` against `game.Gameline.name`).
- `Model.SECONDARY_TYPES` lists the mortal types that get light badges; add a new
  `<gameline>_human` type there.
- Only `CharacterTemplate`, `Book`, `HouseRule` and some `game` models store `gameline` as a
  column. A new column uses `choices=settings.GAMELINE_CHOICES`.

## Fields and choices

- Gameline choices: `settings.GAMELINE_CHOICES`; names: `settings.GAMELINES[code]["name"]`
  (or `core.utils.get_gameline_name`). Code constants and URL modules:
  `core.constants.GameLine`.
- Status: `core.constants.CharacterStatus` (`Un`, `Rev`, `Sub`, `App`, `Dec`, `Ret`);
  image status: `ImageStatus` (`un`, `sub`, `app`); XP requests: `XPApprovalStatus`.
  Compare with the constants, not literals, in new code.
- Ratings: `IntegerField` with `MinValueValidator` / `MaxValueValidator` plus a named
  `CheckConstraint` (see [validation.md](validation.md)). Paired permanent/temporary stats
  use `core.linked_stat.linked_stat_fields` (`Human` willpower is the example).
- `JSONField(default=list)` / `default=dict` are safe (callables). Prefer a related model
  when rows are queried or approved individually, as `game.XPSpendingRequest` is.
- A new column on an existing model is `null=True` or has a default, and needs a
  `tg_schema` migration.

## Relations

| Relation | `on_delete` | Example |
|----------|-------------|---------|
| Link to an independent row (owner, chronicle, archetype, parent clan) | `SET_NULL`, `null=True, blank=True` | `Model.owner`, `Human.nature` |
| Row that exists only for its parent (through row, request, application record) | `CASCADE` | `TemplateApplication.character`, `game.XPSpendingRequest.character`, `wraith.Fetter` |
| Self-reference (bloodline, sub-location) | `SET_NULL` with a `related_name` | `VampireClan.parent_clan` (`bloodlines`) |

Most existing rating rows (`BackgroundRating.char`, `BaseBackgroundRating.bg`) use
`SET_NULL` and survive their parent as orphans. Follow the table for new models; do not
copy that pattern.

- Give every FK and M2M a `related_name` that reads from the other side (`bloodlines`,
  `template_applications`). Two FKs to one model must have distinct names
  (`Human.nature` / `demeanor` → `nature_of` / `demeanor_of`).
- Index FKs and fields used in hot filters (`db_index=True`, or `Meta.indexes`), as
  `Model.owner`, `chronicle` and `status` do.
- Uniqueness: prefer a named `models.UniqueConstraint` with `violation_error_message`
  (`game.STRelationship`, `game.UserSceneReadStatus`) over `unique_together`.

## Meta

- `verbose_name` and `verbose_name_plural` always (registry menus, list titles and
  success messages use them).
- `ordering` when the model is listed (`["name"]` for reference data).
- Constraint names are globally unique: prefix them with the app and model
  (`characters_character_xp_non_negative`).

## URLs

| Model family | How it gets URLs |
|--------------|------------------|
| Items and locations | `RegistryURLMixin` ([`core/registry_urls.py`](../../../../core/registry_urls.py)) resolves `model_urls` from its `ModelSpec`; see [registry.md](registry.md) |
| Characters | `Character.get_absolute_url()` → `characters:character` (the type router); `get_update_url()` per type |
| Reference models | Explicit methods, or `core.models.URLMethodsMixin` with `url_namespace` / `url_name` (`Archetype`) |

`get_creation_url` is a `classmethod`. The URL names follow [urls.md](urls.md).

## Querying

- `Model.objects` does not join `polymorphic_ctype`. Call `.with_polymorphic_ctype()` when
  you iterate and call subclass methods (`get_absolute_url`, `get_type`, `get_heading`).
- `select_related` for FKs you read, `prefetch_related` for M2M and reverse FKs, in the
  view's `get_queryset()`, not in templates.
- Use the queryset helpers (`visible()`, `owned_by()`, `for_chronicle()`,
  `pending_approval_for_user()`; `CharacterQuerySet.active()`, `npcs()`, ...), and add new
  ones to the tree's queryset rather than filtering in views.
- Permission-scoped lists use `PermissionManager.filter_queryset_for_user`, never a
  hand-written owner filter. See [permissions.md](permissions.md).

## Checklist

- [ ] Base class from the table; no redefined inherited fields.
- [ ] `type` unique in the app, `gameline` in `settings.GAMELINES`; router and chargen
  entries for a character type.
- [ ] Choices from settings or `core.constants`.
- [ ] `on_delete`, `related_name`, indexes chosen deliberately.
- [ ] Named constraints with messages; `clean()` for cross-field rules
  ([validation.md](validation.md)).
- [ ] `verbose_name`, `verbose_name_plural`, `ordering`, `__str__`.
- [ ] URL methods resolve; registry entry for an item or location.
- [ ] `tg_schema` migration for any column, table or constraint an existing database lacks.
- [ ] Model tests under `<app>/tests/models/<gameline>/test_<module>.py`.

## See also

- [docs/architecture/data-model.md](../../../../docs/architecture/data-model.md)
- [schema-changes.md](schema-changes.md), [validation.md](validation.md)
- [model-inventory.md](model-inventory.md)
- [`core/models.py`](../../../../core/models.py), [`core/base.py`](../../../../core/base.py)
