# Mage: the Ascension models

This page is the reference for the Mage character types in
[`characters/models/mage/`](../models/mage/): `MtAHuman`, `Mage`, `Companion`,
`Sorcerer`, their rating through-models and the `Cabal` group. The Mage catalogues
(Spheres, factions, Effects, rotes, Resonance, the Focus models Practice / Instrument /
Paradigm / Tenet, sorcerer fellowships, Linear Magic paths and rituals, companion
Advantages) are described in [Reference data](reference-data.md#mage). Read
[Character models](models.md) first for the `Human` base. Terms such as Arete, Sphere,
Paradox and Focus are in the [glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Update URL that resolves |
|-------|--------|--------|------------------|--------------------------|
| `MtAHuman` | `Human` | `mta_human` | `mta_human` (14 steps) | `characters:mage:update:mta_human` |
| `Mage` | `MtAHuman` | `mage` | `mage` (21 steps) | `characters:mage:update:mage` |
| `Companion` | `MtAHuman` | `companion` | `companion` (14 steps) | only `characters:mage:update:companion_full` |
| `Sorcerer` | `MtAHuman` | `sorcerer` | `sorcerer` (18 steps) | only `characters:mage:update:sorcerer_full` |
| `Cabal` | `Group` | `cabal` | n/a | `characters:mage:update:cabal` |

All have `gameline = "mta"`. Every Mage character's detail page is the polymorphic
`characters:character` route. There is no `characters:mage:update:companion` or
`characters:mage:update:sorcerer` route, so `Companion.get_update_url()` and
`Sorcerer.get_update_url()` return `get_full_update_url()` (see
[Views and URLs](views-and-urls.md#mage)).

## MtAHuman

[`mtahuman.py`](../models/mage/mtahuman.py). The mortal base carries the whole Mage
ability list, about 80 extra `IntegerField` columns. The primary abilities are the 19 common
ones plus `awareness`, `art`, `leadership`, `larceny`, `meditation`, `research`,
`survival`, `technology`, `cosmology`, `enigmas`, `finance`, `law`, `occult`, `politics`.
Every other column (for example `acrobatics`, `blind_fighting`, `cryptography`,
`umbrood_protocols`) is a secondary ability, shown only when rated
(`AbilityBlock.secondary_ability_sections()`).

Other fields: `allied_characters` (`ManyToManyField(Character)`) and
`enhancement_devices` (`ManyToManyField(items.Wonder)`). `allowed_backgrounds` covers the
full Mage background list (`arcane`, `chantry`, `node`, `library`, `sanctum`, `wonder`,
`enhancement`, `requisitions`, `secret_weapons`, `totem` and others);
`background_points = 5`.

## Mage

[`mage.py`](../models/mage/mage.py).

### Fields

| Group | Fields |
|-------|--------|
| Affiliation | `affiliation`, `faction`, `subfaction` (`ForeignKey(MageFaction, SET_NULL)`, reverse `affiliations` / `factions` / `subfactions`) |
| Avatar | `essence` (`Dynamic`, `Pattern`, `Primordial`, `Questing`; default `Dynamic`), `age_of_awakening`, `avatar_description` |
| Spheres | `correspondence`, `time`, `spirit`, `mind`, `entropy`, `prime`, `forces`, `matter`, `life` (default `0`); `affinity_sphere` (`ForeignKey(Sphere)`); display-name choices `corr_name` (`correspondence` / `data`), `prime_name` (`prime` / `primal_utility`), `spirit_name` (`spirit` / `dimensional_science`) |
| Arete | `arete` (default `1`; constraint 1 to 10) |
| Focus | `metaphysical_tenet`, `personal_tenet`, `ascension_tenet` (`ForeignKey(Tenet)`), `other_tenets`, `practices` (through `PracticeRating`), `instruments` |
| Magick | `rote_points` (default `6`), `rotes` (`ManyToManyField(Rote)`), `resonance` (through `ResRating`), `quintessence`, `paradox` |
| Quiet | `quiet`, `quiet_type` (`none`, `denial`, `madness`, `morbidity`) |

`background_points = 7`; `allowed_backgrounds` adds `avatar` to the `MtAHuman` list.

### Rules in the model

- `clean()` requires Arete of at least 1 and no Sphere above Arete.
- `add_sphere(sphere)` caps at `min(arete, 5)` and refuses Entropy for the Ahl-i-Batin.
  `has_spheres()` requires a rated affinity Sphere and exactly 6 Sphere dots.
  `get_affinity_sphere_options()` unions the affiliation's, faction's and subfaction's
  `affinities` (all Spheres when none are set).
- `set_faction(affiliation, faction, subfaction=None)` checks each level's `parent` and,
  for Marauders, gives a random Quiet rating and type when unset.
- `add_background()` allows `requisitions` and `secret_weapons` only for the Technocratic
  Union. `is_technocrat` switches sheet labels.
- `add_arete(freebies=False)` caps at 3 when bought with freebies, else 10.
  `purchase_starting_arete(arete)` charges freebies for each dot above 1 on the Spheres
  step and logs it in `spent_freebies`.
- `has_focus()` requires all three tenets and practice dots equal to Arete.
  `PracticeRating.get_tenet_bonus()` returns +1 / -1 / 0 depending on whether the practice
  is only associated with, only limited by, or neither for the mage's tenets.
- `add_effect(effect)` creates a `Rote` for a learnable Effect (`Effect.is_learnable`)
  and deducts `effect.cost()` from `rote_points`; `has_effects()` is true at 0 rote points.
- `add_resonance()` / `subtract_resonance()` edit `ResRating` rows (0 to 5); zero rows are
  deleted.
- `has_specialties()` also requires a specialty for every Sphere at 4+, and
  `needed_specialties()` includes Spheres.
- `add_ability()` allows 5 dots instead of 4.

The `*_freebies(form)` methods (`sphere_freebies`, `rotes_freebies`, `resonance_freebies`,
`tenet_freebies`, `practice_freebies`, `arete_freebies`, `quintessence_freebies`) and the
legacy `spend_xp()` / `spend_freebies()` extend the `Human` hooks; the current spend flow
is in [Services](services.md).

### Through models

| Model | Fields | Constraint |
|-------|--------|------------|
| `ResRating` (`core.models.BaseResonanceRating`) | `mage`, `resonance`, `rating` | `characters_mage_resrating_rating_range` (0 to 10) |
| `PracticeRating` (`core.models.BasePracticeRating`) | `mage`, `practice`, `rating` | `characters_mage_practicerating_rating_range` (0 to 10) |

## Companion

[`companion.py`](../models/mage/companion.py). A mortal ally, Consor or Familiar.

| Field | Notes |
|-------|-------|
| `companion_type` | `companion` (default), `consor`, `familiar` |
| `companion_of` | `ForeignKey(Human, SET_NULL)` |
| `essence`, `rage` | Integers (spirit traits for familiars) |
| `advantages` | `ManyToManyField(Advantage)` through `AdvantageRating` (reverse `advantaged`) |
| `charms` | `ManyToManyField(SpiritCharm)` |

`prepare_starting_freebies()` sets the chargen freebie budget from `STARTING_FREEBIES`
(keys `acoylte`, `backup`, `consor`, `ally`; of these only `consor` is a `companion_type`
choice, so a plain companion keeps the field default of 15). A familiar gets 25 freebies
when it is not an NPC plus a fixed package: the Thaumivore flaw, the Bond-Sharing and
Paradox Nullification Advantages and the Airt Sense charm, logged in `spent_freebies`,
for a net cost of one freebie. The caller saves.

`add_advantage(advantage, rating)` accepts only a rating in `advantage.get_ratings()`.
`advantage_ratings` and `get_advantage_and_rating_list()` feed the sheet.
`AdvantageRating` has constraint `characters_mage_advantagerating_rating_range` (0 to 10).

## Sorcerer

[`sorcerer.py`](../models/mage/sorcerer.py). A Linear Magic user.

| Field | Notes |
|-------|-------|
| `fellowship` | `ForeignKey(SorcererFellowship, SET_NULL)`, reverse `sorcerer_affiliations` |
| `sorcerer_type` | `hedge_mage` (default) or `psychic`; the chargen `psychic` / `path` / `ritual` steps skip on it |
| `affinity_path` | `ForeignKey(LinearMagicPath)` |
| `casting_attribute` | `ForeignKey(Attribute)` |
| `quintessence` | Integer |
| `paths` | `ManyToManyField(LinearMagicPath)` through `PathRating` (reverse `known_to`) |
| `rituals` | `ManyToManyField(LinearMagicRitual)` |

`PathRating` stores `character`, `path`, `practice`, `ability` and `rating` (constraint 0
to 10). `add_path(path, practice, ability)` creates the rating at 1 or adds a dot;
`path_rating()`, `path_ratings` and `ritual_list` read them. `allowed_backgrounds` adds
`artifact` and drops `legend` and `wonder` compared with `MtAHuman`.

## Cabal

[`cabal.py`](../models/mage/cabal.py). A `Group` with no extra fields.
`get_display_type()` returns "Amalgam" when the leader is a Technocratic Union mage. The
detail page is `characters:group`; create, update and list routes are under
`characters:mage:`.

## See also

- [Character models](models.md)
- [Reference data: Mage](reference-data.md#mage)
- [Services](services.md) (Mage chargen, rotes and XP helpers)
- [Chargen](chargen.md)
- [Views and URLs](views-and-urls.md#mage)
