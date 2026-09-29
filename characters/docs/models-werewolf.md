# Werewolf: the Apocalypse models

This page is the reference for the Werewolf character types in
[`characters/models/werewolf/`](../models/werewolf/): `WtAHuman`, `Werewolf` (Garou),
`Kinfolk`, `Fomor`, `Drone`, the Changing Breeds (`Fera` and its twelve subclasses),
`SpiritCharacter` and the `Pack` group. The Werewolf catalogues (tribes, camps, Gifts,
rites, totems, spirit charms, Fomori powers, battle scars, renown incidents, sept
positions) are described in [Reference data](reference-data.md#werewolf). Read
[Character models](models.md) first for the `Human` base. Terms such as Auspice, Gnosis and
Kinfolk are in the [glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `WtAHuman` | `Human` | `wta_human` | `wta_human` (8 steps) | `characters:character` |
| `Werewolf` | `WtAHuman` | `werewolf` | `werewolf` (12 steps) | `characters:character` |
| `Kinfolk` | `WtAHuman` | `kinfolk` | `kinfolk` (8 steps) | `characters:character` |
| `Fomor` | `WtAHuman` | `fomor` | `fomor` (10 steps) | `characters:character` |
| `Drone` | `WtAHuman` | `drone` | `drone` (7 steps) | `characters:werewolf:drone` |
| `Fera` | `WtAHuman` | `fera` | `fera` (11 steps) | `characters:character` |
| `Ajaba`, `Ananasi`, `Bastet`, `Corax`, `Grondr`, `Gurahl`, `Kitsune`, `Mokole`, `Nagah`, `Nuwisha`, `Ratkin`, `Rokea` | `Fera` | lower-case class name | the same `fera` workflow | `characters:werewolf:<type>` (all served by `FeraDetailView`) |
| `SpiritCharacter` | `Character` | `spirit_character` | none | `characters:character` |
| `Pack` | `Group` | `pack` | n/a | `characters:group` |

All have `gameline = "wta"` (URL namespace `characters:werewolf:`). The Fera subclasses
have no `create:` or `update:` routes of their own, so `get_update_url()` and
`get_creation_url()` inherited from `Human` do not resolve for them; they are created and
edited through the `fera` routes (see [Views and URLs](views-and-urls.md#werewolf)).

## WtAHuman

[`wtahuman.py`](../models/werewolf/wtahuman.py). Adds ability columns (all primary):
talents `leadership`, `primal_urge`; skills `animal_ken`, `larceny`, `performance`,
`survival`; knowledges `enigmas`, `law`, `occult`, `rituals`, `technology`.
`allowed_backgrounds`: `contacts`, `mentor`, `allies`, `ancestors`, `fate`, `fetish`,
`kinfolk_rating`, `pure_breed`, `resources`, `rites`, `spirit_heritage`, `totem` (all
stored as `BackgroundRating` rows).

## Gift permissions

Gifts are filtered through `GiftPermission` rows ([`gift.py`](../models/werewolf/gift.py)),
plain `(shifter, condition)` pairs such as `("werewolf", "theurge")` or
`("bastet", "simba")`. A `Gift` lists the permissions that may learn it in `allowed`, and a
shapeshifter collects permissions in its `gift_permissions` many-to-many as its breed,
auspice, tribe and camp are set. `filter_gifts()` then returns the Gifts whose `allowed`
intersects the character's permissions.

The module function `gifts_by_rank(gifts, sources, shifter)` groups a character's Gifts by
rank for the sheet and labels each with the first source in `sources` that one of its
permissions grants. `Werewolf`, `Kinfolk` and `Fera` wrap it in their own `gifts_by_rank()`.

## Werewolf (Garou)

[`garou.py`](../models/werewolf/garou.py).

| Group | Fields |
|-------|--------|
| Identity | `rank` (default `1`; names in `rank_names`: Cliath to Elder), `deed_name`, `auspice` (choices `ragabash`, `theurge`, `philodox`, `galliard`, `ahroun`), `breed` (`homid`, `metis`, `lupus`), `tribe` (`ForeignKey(Tribe, SET_NULL)`), `camps` (`ManyToManyField(Camp)`) |
| Power | `gnosis`, `rage` (default `1`; validators and constraints 1 to 10) |
| Renown | `glory`, `wisdom`, `honor` and `temporary_*` pairs from `core.linked_stat.linked_stat_fields` (descriptors `glory_renown`, `wisdom_renown`, `honor_renown`); `renown_incidents` (`JSONField`, list of `RenownIncident` names) |
| Story | `first_change`, `age_of_first_change` |
| Possessions | `gifts`, `rites_known`, `fetishes_owned` (`items.Fetish`), `battle_scars`, `gift_permissions` |

Behaviour:

- `set_breed()` swaps the breed permission and sets starting Gnosis (homid 1, metis 3,
  lupus 5). `set_auspice()` swaps the auspice permission and sets starting Renown and Rage
  (Ragabash takes a `ragabash_renown` triple). `set_tribe()` returns `False` for a homid Red
  Talon, else sets Willpower from `Tribe.willpower` and raises Pure Breed to 3 for Silver
  Fangs. `add_camp()` adds the camp's permission when one exists. Each setter saves.
- `has_gifts()` requires at least three Gifts including one each from breed, auspice and
  tribe. `filter_gifts()` limits to `rank <= self.rank`.
- `total_rites()` counts rite levels, with level-0 rites as half a point; `has_rites()`
  compares it with the `rites` background.
- `add_renown_incident(r, rite=None)` checks the incident's breed, required rite,
  `only_once` and whether the last incident was posthumous, then adds its Renown to the
  temporary tracks. `update_renown()` converts every 10 temporary points into a permanent
  dot. `add_battle_scar()` adds the scar's Glory and calls `update_renown()`.
- `increase_rank()` checks the class-level `requirements[auspice][rank + 1]` table
  (per-track minimums or a `total`) and raises rank up to 5.
- `renown_tracks()` and `renown_incident_list()` feed the sheet.
- `clean()` rejects Gnosis or Rage below 1. `spend_xp()` / `spend_freebies()` extend the
  legacy hooks (see [Services](services.md) for the current flow).

## Kinfolk

[`kinfolk.py`](../models/werewolf/kinfolk.py). Fields: `breed` (`homid`, `lupus`),
`tribe`, `relation`, `gnosis` (default `0`), the three Renown pairs, `gifts`,
`gift_permissions`, `fetishes_owned`. `allowed_backgrounds`: `allies`, `contacts`,
`mentor`, `pure_breed`, `resources`.

Tribal restrictions come from `characters.rules.limits.KINFOLK_TRIBE_BACKGROUND_LIMITS`
(`forbidden`, `max` and `required` backgrounds per tribe):

- `background_violations(ratings)` overrides the `Human` hook used by the Backgrounds
  chargen step and returns the first broken restriction as `(index, RuleViolation)`.
- `add_background()` refuses a forbidden background or one already at its cap.
- `set_tribe()` also raises Pure Breed to 1 for Silver Fangs and adds the first
  `Derangement` for Black Spiral Dancers.

The "Gnosis" merit sets `gnosis = rating - 4` (in `add_mf()` and `mf_based_corrections()`);
the "Fetish" merit adds the first `Fetish` in `mf_based_corrections()`. `filter_gifts()`
offers rank-1 Gifts only.

## Fomor and Drone

| Class | Fields | Notes |
|-------|--------|-------|
| `Fomor` ([`fomor.py`](../models/werewolf/fomor.py)) | `rage`, `gnosis`, `powers` (`ManyToManyField(FomoriPower)`) | `allowed_backgrounds = ["allies", "contacts", "resources"]`, `background_points = 3`; `add_power()`, `filter_powers()`. `MeritFlawManager.filter_mfs()` treats a Fomor as `human` when filtering merits |
| `Drone` ([`drone.py`](../models/werewolf/drone.py)) | `bane_name`, `bane_type`, `rage`, `gnosis`, `willpower_per_turn` (default `1`) | `allowed_backgrounds = ["contacts", "resources"]`, `background_points = 2`; `has_bane()`, `set_bane()` |

## Fera (Changing Breeds)

[`fera.py`](../models/werewolf/fera.py). `Fera` is concrete (its own table) and is also
the base of the twelve breeds. Common fields: `breed`, `faction`, `gnosis`, `rage`,
`renown` / `temporary_renown`, `first_change`, `age_of_first_change`, `gifts`,
`rites_known`, `fetishes_owned`, `gift_permissions`.

Each breed class declares its chargen choices as class attributes, and the shared
[`fera` workflow](chargen.md#workflows-by-type) reads them:

| Attribute | Meaning |
|-----------|---------|
| `chargen_choice_fields` | Fields chosen on the Breed Faction step, in the order their `set_<field>()` side effects run |
| `optional_choice_fields` | Choice fields that may be left blank |
| `chargen_help_text` | Help text per choice field |
| `gift_group_fields` | `(context key, field)`: rank-1 Gifts permitted by that field's value |
| `fixed_gift_groups` | `(context key, condition)`: rank-1 Gift lists every member may use |

`apply_chargen_choices(changed_fields)` runs the setters for changed choices;
`starting_gift_groups()` builds the Gifts step's lists; `choice_display()`,
`sheet_choices()`, `gifts_by_rank()` and `renown_tracks()` (the breed's own Renown fields
from `RENOWN_TRAITS`, plus the generic pool when used) feed the sheet.

| Breed | Choice fields | Extra fields |
|-------|---------------|--------------|
| `Ajaba` | `breed`, `auspice` | `auspice`, `ferocity`, `obligation`, `wisdom` |
| `Ananasi` | `breed`, `aspect` | `aspect`, `cunning`, `obedience`, `wisdom` |
| `Bastet` | `breed`, `tribe`, `pryio` | `tribe` (nine tribes), `pryio`, `ferocity`, `honor`, `cunning` |
| `Corax` | `breed` (fixed group `corax`) | `curiosity` |
| `Grondr` | `breed`, `auspice` | `auspice`, `glory`, `honor`, `wisdom` |
| `Gurahl` | `breed`, `auspice` | `auspice`, `honor`, `succor`, `vision` |
| `Kitsune` | `breed`, `path` | `path`, `chie`, `toku`, `kagayaki` |
| `Mokole` | `breed`, `stream`, `auspice` | `stream`, `auspice`, `valor`, `harmony`, `wisdom`, `mnesis` (default `1`) |
| `Nagah` | `breed`, `auspice` | `auspice`, `obligation`, `wisdom`, `subtlety` |
| `Nuwisha` | `breed`, `role` (optional; fixed group `nuwisha`) | `role`, `glory`, `humor`, `cunning` |
| `Ratkin` | `breed`, `aspect` | `aspect`, `infamy`, `obligation`, `cunning` |
| `Rokea` | `breed`, `auspice` | `auspice`, `valor`, `harmony`, `innovation` |

Each breed also defines `BREEDS`, choice lists for its faction-like fields, and
`set_breed()` / `set_<field>()` methods that add the matching `GiftPermission` (with the
breed's `type` as `shifter`); `set_breed()` also sets starting Gnosis by breed (and, for
some breeds such as `Corax`, Rage).

## SpiritCharacter

[`spirit_character.py`](../models/werewolf/spirit_character.py). Extends `Character`
directly, so it has no Attributes, Abilities or Backgrounds. Fields: `willpower`, `rage`,
`gnosis`, `essence` (integers, default `0`) and `charms`
(`ManyToManyField(SpiritCharm)`). URLs: `characters:werewolf:create:spirit`,
`characters:werewolf:update:spirit`; the detail page goes through `characters:character`.
`Character.get_type()` returns `"Spirit"`.

## Pack

[`pack.py`](../models/werewolf/pack.py). A `Group` with `totem`
(`ForeignKey(Totem, SET_NULL)`); `set_totem()`, `has_totem()`, `total_totem()` (sums a
`totem` attribute of each member). It keeps `Group.get_absolute_url()`
(`characters:group`).

## See also

- [Character models](models.md)
- [Reference data: Werewolf](reference-data.md#werewolf)
- [Chargen](chargen.md)
- [Views and URLs](views-and-urls.md#werewolf)
- [`characters/rules/limits.py`](../rules/limits.py)
