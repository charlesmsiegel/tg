# Character models: core tree and shared blocks

This page is the reference for the gameline-independent part of the character model tree in
[`characters/models/core/`](../models/core/): the `Character` and `Human` base classes, the
abstract blocks that give every sheet its attributes, abilities and health, the managers that
handle backgrounds and merits/flaws, groups, and the core reference models (archetypes,
merits and flaws, specialties, derangements, statistics). Read it before adding a field to
every character, changing the status machine, or writing code that reads traits generically.
Each gameline's subclasses are on their own page (see the [index](#gameline-pages) below).

The project-wide picture of the polymorphic trees is in
[Data model](../../docs/architecture/data-model.md). Terms such as ST, Nature and Demeanor
are defined in the [glossary](../../docs/reference/glossary.md).

## The inheritance tree

Every character row is a `django-polymorphic` multi-table child of `core.models.Model` (an
abstract base that already carries `name`, `owner`, `chronicle`, `status`, `visibility`,
`description`, `public_info`, `image`, `image_status`, `freebies_approved`, `st_notes`,
`display` and `sources`; see [`core/models.py`](../../core/models.py)).

```text
core.models.Model (abstract, polymorphic)
└── CharacterModel                    characters/models/core/character.py
    └── Character                     concept, creation_status, notes, xp
        ├── Human                     + AbilityBlock, HealthBlock, AttributeBlock
        │   ├── VtMHuman ─ Vampire, Ghoul, Revenant
        │   ├── WtAHuman ─ Werewolf, Kinfolk, Fomor, Drone, Fera ─ 12 Changing Breeds
        │   ├── MtAHuman ─ Mage, Companion, Sorcerer
        │   ├── WtOHuman ─ Wraith
        │   ├── CtDHuman ─ Changeling, AutumnPerson, Inanimae, Nunnehi
        │   ├── DtFHuman ─ Demon, Earthbound, Thrall
        │   ├── HtRHuman ─ Hunter
        │   └── MtRHuman ─ Mummy
        └── SpiritCharacter           (werewolf; no Human traits)
```

Groups (`Group` and its gameline subclasses) and the core reference models also extend
`core.models.Model` but sit outside the character tree.

### Class attributes every character type sets

| Attribute | Meaning | Used by |
|-----------|---------|---------|
| `type` | Stable string key (`"vampire"`, `"wta_human"`, ...). Not a database column. | Chargen workflow lookup ([`characters/chargen/`](../chargen/)), `GenericCharacterDetailView.view_mapping`, the spending service factories, `ObjectType` matching for merits/flaws |
| `gameline` | Gameline code (`"wod"`, `"vtm"`, `"wta"`, `"mta"`, `"wto"`, `"ctd"`, `"dtf"`, `"htr"`, `"mtr"`) | URL namespaces in `Human.get_update_url()` / `get_creation_url()`, templates' gameline theming |
| `freebie_step` | Descriptor (`characters.chargen.registry.FreebiePosition`): the 1-based position of the `freebies` step in the type's workflow, else the value in `DETAIL_ONLY_FREEBIE_POSITIONS`, else `-1` | `CharacterQuerySet.at_freebie_step()` |
| `allowed_backgrounds` | Property names of the backgrounds this type may buy | Background formset querysets, `Human.__init__` dynamic properties, XP/freebie forms |
| `background_points` | Dots available on the Backgrounds chargen step (default `5`) | `BaseBackgroundRatingFormSet` allocation check |
| `talents`, `skills`, `knowledges`, `primary_abilities` | Ability field names by group; `primary_abilities` are the ones rated on the Abilities chargen step and shown in the sheet's main columns | `AbilityBlock` helpers, `ability_rule()`, sheet templates |

## CharacterModel and Character

Source: [`characters/models/core/character.py`](../models/core/character.py).

`CharacterModel` adds only `npc` (`BooleanField`, default `False`) and installs
`CharacterManager` (`ModelManager.from_queryset(CharacterQuerySet)`).

`Character` fields:

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `concept` | `CharField(100)`, indexed | `""` | One-line character concept |
| `creation_status` | `IntegerField` | `1` | Current chargen position (see [Chargen](chargen.md)) |
| `notes` | `TextField`, nullable | `""` | Player notes |
| `xp` | `IntegerField`, indexed | `0` | Unspent XP. A `CheckConstraint` (`characters_character_xp_non_negative`) keeps it `>= 0` |

### Status machine

`Character.STATUS_TRANSITIONS` defines which status changes `Character.clean()` accepts
(status codes come from `core.constants.CharacterStatus`):

| From | Allowed targets |
|------|-----------------|
| `Un` (Unapproved) | `Sub`, `Ret` |
| `Sub` (Submitted) | `Rev`, `App`, `Ret` |
| `Rev` (Returned for revisions) | `Sub`, `Ret` |
| `App` (Approved) | `Ret`, `Dec` |
| `Ret` (Retired) | `App` |
| `Dec` (Deceased) | none |

`clean()` loads the stored row and raises `ValidationError` on `status` for any other
change. `save()` detects a change into `Ret` or `Dec` and then calls
`remove_from_organizations()`, which runs every cleanup registered with
`core.utils.CharacterOrganizationRegistry` (`Group.cleanup_character_organizations` removes
memberships and leaderships; `locations.models.mage.chantry` registers its own).

### Queryset helpers

`Character.objects` (and every subclass manager) exposes these chainable methods in addition
to the `core.models.ModelQuerySet` ones (`visible()`, `for_chronicle()`, `owned_by()`, ...):

| Method | Returns |
|--------|---------|
| `npcs()` / `player_characters()` | Filter on `npc` |
| `active()` | `status` in `ACTIVE_STATUSES`: `Un`, `Rev`, `Sub`, `App` |
| `retired()` / `deceased()` | `status` `Ret` / `Dec` |
| `with_group_ordering()` | Annotates `first_group_id` (lowest group id the character belongs to), selects `chronicle`, orders by chronicle, `-first_group_id`, name. Pair it with the module function `attach_first_groups(characters)`, which sets `character.first_group` for every row with one query |
| `pending_approval_for_user(user)` | `Sub` characters in chronicles the user staffs (`game.security.staffed_chronicles`); staff and superusers also see chronicle-less ones |
| `at_freebie_step()` | Characters whose `creation_status` equals their class's `freebie_step`, filtered in SQL per polymorphic content type |

### XP methods

XP is held as an integer balance; each spend creates a `game.models.XPSpendingRequest`
(reverse accessor `xp_spendings`). The spending rules themselves live in
[services](services.md); these model methods are the primitives the services call.

| Method | Behaviour |
|--------|-----------|
| `add_xp(amount)` | Atomic; locks the row with `select_for_update()` and adds `amount` |
| `spend_xp(trait_name, trait_display, cost, category, trait_value=0)` | Atomic; raises `ValidationError(code="insufficient_xp")` when `xp < cost`, deducts `cost` and creates a `Pending` `XPSpendingRequest` |
| `approve_xp_spend(request_id, trait_property_name, new_value, approver)` | Atomic; marks the request `Approved` and sets the trait |
| `create_xp_spending_request(...)`, `get_pending_xp_requests()`, `get_xp_spending_history()`, `approve_xp_request()`, `deny_xp_request()` | Thin wrappers around `XPSpendingRequest` rows |
| `waiting_for_xp_spend()` | Whether any request is `Pending` |
| `total_spent_xp()` | Sum of `cost` over `Approved` requests |
| `total_xp()` / `available_xp()` | Both return `xp` (the balance is already net of spends) |

### Navigation helpers

- `get_absolute_url()` returns `characters:character` (the polymorphic router, see
  [Views and URLs](views-and-urls.md)); several subclasses override it with their own detail
  route.
- `next_stage(user=...)` and `prev_stage()` delegate to `characters.chargen.transitions`.
- `can_navigate_back()` is the single gate for chargen back-navigation: status `Un` or `Rev`,
  `creation_status > 1`, within the workflow, and `freebies_approved` false.
  `chargen_back_url` returns the `characters:chargen_back` URL when it is true, else `""`.
- `get_type()` returns `"Human"` for any type containing `human`, `"Spirit"` for
  `spirit_character`, and the title-cased `type` otherwise.

## Human

Source: [`characters/models/core/human.py`](../models/core/human.py).
`Human(AbilityBlock, HealthBlock, AttributeBlock, Character)` is the base of every
playable sheet.

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `nature`, `demeanor` | `ForeignKey(Archetype, SET_NULL)`, nullable | `None` | Reverse names `nature_of`, `demeanor_of` |
| `specialties` | `ManyToManyField(Specialty)` | | |
| `languages` | `ManyToManyField(core.Language)` | | |
| `merits_and_flaws` | `ManyToManyField(MeritFlaw, through="MeritFlawRating")` | | Reverse name `flawed` |
| `derangements` | `ManyToManyField(Derangement)` | | |
| `willpower`, `temporary_willpower` | `IntegerField` pair from `core.linked_stat.linked_stat_fields("willpower", default=3, min_permanent=1)` | `3` / `3` | `willpower_stat` is the linked-stat descriptor; the pair's `CheckConstraint`s are added with the prefix `characters_human_` |
| `age` | `IntegerField`, nullable | | Validators and constraint: 0 to 5000 |
| `apparent_age` | `IntegerField`, nullable | | Validators and constraint: 0 to 200 |
| `date_of_birth` | `DateField`, nullable | | |
| `history`, `goals` | `TextField`, nullable | `""` | |
| `freebies` | `IntegerField` | `15` | Unspent freebie points |
| `spent_freebies` | `JSONField(list)` | `[]` | Legacy list of spend records; current code records spends as `game.models.FreebieSpendingRecord` rows (reverse accessor `freebie_spendings`) |

Class defaults: `allowed_backgrounds = ["contacts", "mentor"]`, `background_points = 5`, and
the 19 common abilities as `talents`, `skills`, `knowledges` and `primary_abilities` (listed
inline; `AbilityBlock` itself reads the same lists from `core.constants.AbilityFields`).

### Key methods

| Group | Methods |
|-------|---------|
| URLs | `get_update_url()` → `characters:<gameline short name>:update:<type>`; `get_full_update_url()` → `..._full`; class methods `get_creation_url()` and `get_full_creation_url()`. The gameline prefix comes from `core.utils.get_short_gameline_name()` and is empty for `wod`. Types whose update route has another name override these (and some do not resolve; see [Views and URLs](views-and-urls.md)) |
| Freebies | `total_freebies()`, `create_freebie_spending_record()`, `get_freebie_spending_history()`, `total_freebies_from_model()`, `award_backstory_freebies(amount)` (atomic; `0 <= amount <= 15`; adds to `freebies` and sets `freebies_approved`; raises `ValidationError` if already approved) |
| Willpower | `add_willpower()`, `set_willpower(value)` (lowers `temporary_willpower` when needed, then saves) |
| Specialties | `specialties_by_stat()` (one query, uses the prefetch cache), `get_specialty(stat)`, `filter_specialties(stat=None)`, `add_specialty(specialty)`, `has_specialties()`, `needed_specialties()` (stats rated 4+ plus a fixed list of broad abilities rated 1+, minus those already specialised) |
| Chargen checks | `has_finishing_touches()`, `has_history()`, `has_archetypes()`, `set_archetypes()`, `add_derangement()`, `is_group_member()`, `get_group()` |
| Backgrounds | `background_manager` property (see [Managers](#managers)); delegates `add_background()`, `total_background_rating()`, `get_backgrounds()`, `total_backgrounds()`, `filter_backgrounds()`, `has_backgrounds()`, `new_background_freebies()`, `existing_background_freebies()`; `background_violations(ratings)` returns `[]` here and is overridden by `Kinfolk` |
| Merits and flaws | `merit_flaw_manager` property; delegates `num_languages()`, `get_mf_and_rating_list()`, `add_mf()`, `filter_mfs()`, `mf_rating()`, `has_max_flaws()`, `total_flaws()`, `total_merits()`, `meritflaw_freebies()`; `mf_based_corrections()` zeroes the lowest ability group when the character has the "Ability Deficit" flaw |
| Legacy spending | `spend_xp(trait)` and `spend_freebies(trait)` apply a spend directly to the model and return `True`/`False`, or the trait name when the method does not handle it (gameline subclasses extend `spend_freebies`; only `Mage` overrides `spend_xp`, keeping its keyword form). Called with keyword arguments, `spend_xp(trait_name=..., cost=..., ...)` delegates to `Character.spend_xp`. The request and approval flow uses the [spending services](services.md) instead |

### Dynamic background properties

`Human.__init__` walks `allowed_backgrounds` and, for each name the class does not already
define, installs a property on the class whose getter returns
`background_manager.get_background_property(name)` (the sum of the character's
`BackgroundRating` rows for that background) and whose setter creates or deletes
`BackgroundRating` rows. So `mage.avatar` or `garou.pure_breed` read the rating rows.

`VtMHuman`, `HtRHuman` and `MtRHuman` also declare integer columns named after some of their
backgrounds (for example `allies`, `resources`). Because the property is only installed when
the class has no attribute of that name, attribute access on those types reads the column,
while `total_background_rating()` still reads `BackgroundRating` rows.

## Blocks

The blocks are abstract models mixed into `Human`
([`characters/models/core/`](../models/core/)).

### AttributeBlock

[`attribute_block.py`](../models/core/attribute_block.py). Nine `IntegerField`s
(`strength` ... `appearance`), default `1`, validators 0 to 10, one range
`CheckConstraint` each (named `%(app_label)s_%(class)s_<field>_range`).

| Method | Behaviour |
|--------|-----------|
| `add_attribute(name, maximum=None)` | Adds a dot up to `get_attribute_max()` |
| `get_attribute_max()` | `5`; `Vampire` returns its generation's trait maximum |
| `get_attribute_min(name=None)` | `1`; `Vampire` returns `0` for Appearance when the clan is Nosferatu |
| `validate_attributes()` | Dict of attributes below their minimum |
| `get_attributes()`, `get_physical_attributes()`, `get_social_attributes()`, `get_mental_attributes()`, `total_*()`, `filter_attributes()` | Readers |
| `has_attributes(primary=7, secondary=5, tertiary=3)` | Group totals, sorted, equal `3 + tertiary`, `3 + secondary`, `3 + primary` |
| `attribute_sections()` | `[(heading, [(label, rating, specialty), ...]), ...]` for the sheet, in `ATTRIBUTE_GROUPS` order |

`Attribute` (a `Statistic` subclass) is the reference row for each attribute; forms use its
`property_name` to address the field.

### AbilityBlock

[`ability_block.py`](../models/core/ability_block.py). The 19 common abilities (8 talents,
6 skills, 5 knowledges) as `IntegerField`s, default `0`, validators and constraints 0 to 10.
Gameline human classes add their own ability columns and override the four ability lists.

| Method | Behaviour |
|--------|-----------|
| `add_ability(name, maximum=4)` | Adds a dot (`Mage.add_ability` raises the maximum to 5) |
| `get_talents()`, `get_skills()`, `get_knowledges()`, `get_abilities()`, `filter_abilities()`, `total_*()` | Readers over the class's lists |
| `has_abilities(primary=13, secondary=9, tertiary=5)` | Group totals, sorted, equal the three targets |
| `ability_label(stat)` | Title case, with `ABILITY_LABELS` overrides (`primal_urge` → `Primal-Urge`) |
| `ability_sections()` | Primary abilities by group for the sheet |
| `secondary_ability_sections()` / `get_secondaries_for_display()` | Non-zero abilities outside `primary_abilities`, padded into three columns |

`Ability` is the matching `Statistic` subclass.

### HealthBlock

[`health_block.py`](../models/core/health_block.py). `current_health_levels` is a string
of damage marks (`"B"`, `"L"`, `"A"`), `max_health_levels` defaults to `7`.
`add_bashing()`, `add_lethal()` and `add_aggravated()` append a mark (bashing on a full track
upgrades one `B` to `L`) and keep the string sorted with aggravated first.
`get_health_table()` zips level names, wound penalties and marks for the sheet;
`get_wound_penalty()` returns `0`, `-1`, `-2`, `-5` or `-1000` (incapacitated).

### Background storage

[`background_block.py`](../models/core/background_block.py).

| Model | Purpose | Key fields |
|-------|---------|------------|
| `Background` (`Statistic`) | Reference row per background | `property_name`, `multiplier` (default `1`, freebie/XP cost multiplier), `alternate_name`, `poolable` (default `True`) |
| `BackgroundRating` | One rated background on one character; a character can hold several rows for the same background (for example two Allies with different notes) | `char` (`ForeignKey(Human)`, reverse `backgrounds`), `bg`, `rating` (constraint 0 to 10), `note`, `url`, `complete`, `pooled`, `display_alt_name`; `display_name()` |
| `PooledBackgroundRating` | A background pooled by a group | `group` (reverse `pooled_backgrounds`), `bg`, `rating`, `note`, `url`, `complete` |

`complete=False` marks a background that still needs its linked object (a mentor NPC, a
node, a library...); the conditional chargen steps look for such rows (see
[Chargen](chargen.md)). `BackgroundBlock` is an abstract mixin with the same API as
`BackgroundManager`; characters use the manager, and `locations.models.mage.chantry.Chantry`
uses the mixin.

### Merits and flaws

[`merit_flaw_block.py`](../models/core/merit_flaw_block.py).

| Model | Key fields and methods |
|-------|------------------------|
| `MeritFlaw` (`core.models.Model`, `type="merit_flaw"`) | `ratings` (`ManyToManyField(core.Number)`), `max_rating`, `min_rating`, `allowed_types` (`ManyToManyField(game.ObjectType)`: which character or location types may take it). `add_rating()` / `add_ratings()` keep `max_rating` and `min_rating` in step; `get_ratings()` returns the sorted values; `__str__` shows them |
| `MeritFlawRating` | `character` (`ForeignKey(Human)`, reverse `merit_flaw_ratings`), `mf` (reverse `character_ratings`), `rating` (constraint -10 to 10) |
| `MeritFlawBlock` (abstract) | Generic merit/flaw API over any `merits_and_flaws` through model; used by `locations` (`Node`, `HorizonRealm`) |

Flaws are negative ratings. `has_max_flaws()` is true when the flaw total is `-7` or lower;
`filter_mfs()` then offers only merits. Choices are always restricted to merits whose
`allowed_types` include the character's `game.models.ObjectType`, but two lookups exist:

- `MeritFlawManager.filter_mfs()` (behind `Human.filter_mfs()`) uses `character.type`
  unchanged, except that `fomor` is mapped to `human`. A `vtm_human` therefore looks for an
  `ObjectType` named `vtm_human`.
- The XP and freebie forms ([forms](forms.md)) call
  `characters.utils.get_character_object_type()`, which maps every `*_human` type to
  `human`.

## Managers

[`characters/managers/`](../managers/) holds plain classes (not Django managers) that
`Human` builds lazily and caches per instance.

| Class | Owns |
|-------|------|
| `BackgroundManager` | Rating sums (`total_background_rating`), `get_backgrounds()` (`{name: total_background_rating(name)}` over `allowed_backgrounds`, so it always reads `BackgroundRating` rows), `add_background(background, maximum=5)` (takes a property name or a `Background`; adds a dot to the character's first row for that background rated under 5, creating a row when there is none; the cap is a fixed 5), `has_backgrounds()`, the legacy freebie hooks, and the dynamic-property getter/setter |
| `MeritFlawManager` | `add_mf()` (rating must be one of the merit's `ratings`), `filter_mfs()`, `mf_rating()`, totals, `num_languages()` (the "Language" merit's rating, doubled with "Natural Linguist") |

## Groups

[`group.py`](../models/core/group.py). `Group(core.models.Model)` with `members`
(`ManyToManyField(Character)`) and `leader` (`ForeignKey(Character, SET_NULL)`, reverse
`leads_group`).

- `roster` (cached property): the leader first, then members by name, as concrete types.
- `update_pooled_backgrounds()`: recomputes `PooledBackgroundRating` rows from members'
  `pooled=True` background ratings, keyed by background and note.
- `get_absolute_url()` → `characters:group` (the polymorphic group router).

| Subclass | Gameline | `type` | Extra fields |
|----------|----------|--------|--------------|
| `Coterie` | vtm | `coterie` | none |
| `Pack` | wta | `pack` | `totem` (`ForeignKey(Totem)`); `set_totem()`, `has_totem()`, `total_totem()` |
| `Cabal` | mta | `cabal` | none |
| `Circle` | wto | `circle` | none |
| `Motley` | ctd | `motley` | none |
| `Conclave` | dtf | `conclave` | none |

## Core reference models

| Model | Base | Fields beyond `core.models.Model` | URL names |
|-------|------|-----------------------------------|-----------|
| `Archetype` | `URLMethodsMixin`, `Model` | none | `characters:archetype`, `characters:update:archetype`, `characters:create:archetype`, `characters:list:archetype` |
| `Derangement` | `URLMethodsMixin`, `Model` | none | `characters:derangement` (+ `update:`, `create:`, `list:`) |
| `Specialty` | `Model` | `stat` (the trait's property name); `display_stat()`, `__str__` shows `name (Stat)` | `characters:specialty` (+ `update:`, `create:`, `list:`) |
| `MeritFlaw` | `Model` | see above | `characters:meritflaw` (+ `update:`, `create:`, `list:`) |
| `Statistic` | `PolymorphicModel` | `name`, `property_name` | none |
| `Attribute`, `Ability`, `Background` | `Statistic` | see above | none |

`Statistic` subclasses in gameline packages: `Discipline` (vampire) and `Sphere` (mage).

## Gameline pages

| Gameline | Page |
|----------|------|
| Vampire: the Masquerade | [models-vampire.md](models-vampire.md) |
| Werewolf: the Apocalypse (Garou, Kinfolk, Fomori, Drones, Fera, spirits) | [models-werewolf.md](models-werewolf.md) |
| Mage: the Ascension (Mage, Companion, Sorcerer) | [models-mage.md](models-mage.md) |
| Wraith: the Oblivion | [models-wraith.md](models-wraith.md) |
| Changeling: the Dreaming (Kithain, Inanimae, Nunnehi, Autumn People) | [models-changeling.md](models-changeling.md) |
| Demon: the Fallen (Demon, Earthbound, Thrall) | [models-demon.md](models-demon.md) |
| Hunter: the Reckoning | [models-hunter.md](models-hunter.md) |
| Mummy: the Resurrection | [models-mummy.md](models-mummy.md) |

## Schema changes

The `characters` app has no migration files; its tables are created from the current models
and older databases are brought up to date by the `tg_schema` app. See
[Schema migrations](../../docs/architecture/schema-migrations.md) before adding or renaming a
field.

## See also

- [Data model](../../docs/architecture/data-model.md)
- [Reference data](reference-data.md)
- [Chargen](chargen.md) and [Services](services.md)
- [Adding a character type](../../docs/guides/adding-a-character-type.md)
- [`core/models.py`](../../core/models.py)
