# Scripts by gameline

This page is the inventory of `populate_db/`: every script in load order, the models
it imports, and the other scripts it imports (and therefore runs first). It is for
developers looking for where a kind of data is loaded and for agents deciding which
script to edit. How the order is decided is explained in [loading](loading.md) and
[conventions](conventions.md).

## Folders

| Folder | Scripts | Contents |
|--------|---------|----------|
| top level | 18 | Books, Mage Resonance, `game.Gameline` rows, attributes, abilities, backgrounds, archetypes, derangements, specialties, merits and flaws, languages, nouns (used for random names), materials, weapons, `game.ObjectType` rows, companion advantages, house rules and news items |
| `changeling/` | 4 | Cantrips, chimera, kiths, treasures |
| `character_templates/` | 8 (including `__init__.py`) | `CharacterTemplate` rows per gameline and `faction_templates.py` |
| `demon/` | 25 | Houses, factions, lores, rituals, relics (including the `_hotf_` files from *Houses of the Fallen* and the `demon_earthbound_` files from *Demon: Earthbound*), visages and apocalyptic forms, Demon merits and flaws |
| `mage/` | 21 | Spheres, instruments, practices (including corrupted and specialized), tenets, paradigms, factions, effects, rotes, Wonders and example items, Sorcerer artifacts and fellowships, mediums, Digital Web sectors, spirits and example companions |
| `mummy/` | 3 (including `__init__.py`) | Dynasties and titles |
| `vampire/` | 8 | Disciplines, clans, bloodlines, paths, sects, titles, and Sorcerer linear magic paths and rituals |
| `werewolf/` | 13 | Tribes, camps, Gifts (including Fera Gifts), rites, renown incidents, totems, fetishes, talens, spirits and charms, battle scars, Fomori powers |
| `wraith/` | 4 | Factions, guilds, Shadow archetypes, Thorns |

There is no Hunter folder; Hunter data comes only from the shared top-level scripts.

### Files whose folder differs from their models

A few scripts sit in a gameline folder but load another gameline's models. The loader
does not care, but it matters when you look for data or filter with `--gameline`:

| Script | Loads |
|--------|-------|
| `mage/houses_INC.py` | Changeling `House` and `HouseFaction` |
| `mage/legacies.py` | Changeling `Legacy` |
| `mage/mage_spirits.py` | Werewolf `SpiritCharacter` and `SpiritCharm` |
| `vampire/linear_magic_path.py`, `vampire/linear_magic_rituals.py` | Mage Sorcerer `LinearMagicPath` and `LinearMagicRitual` |
| `mage/fellowships.py` | Mage Sorcerer `SorcererFellowship`, importing `vampire/linear_magic_path.py` |

## Inventory

The table below was produced from the scripts' `from ... import` statements. "Models
imported" lists the model classes a script imports; most scripts create rows of those
models, and a few only look rows up. Two `__init__.py` files hold only a docstring.

### Top level

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `00_books.py` | `Book` | — |
| `01_resonance.py` | `Resonance` | — |
| `aa_gamelines.py` | `Gameline` | — |
| `abilities.py` | `Ability` | — |
| `advantages.py` | `Advantage` | — |
| `archetypes.py` | `Archetype` | — |
| `attributes.py` | `Attribute` | — |
| `backgrounds.py` | `Background` | — |
| `derangements.py` | `Derangement` | — |
| `house_rules.py` | `HouseRule` | — |
| `languages.py` | `Language` | — |
| `materials.py` | `Material` | — |
| `merits_and_flaws_INC.py` | `MeritFlaw`, `Sphere` | `objects` |
| `news_items.py` | `NewsItem` | — |
| `nouns.py` | `Noun` | — |
| `objects.py` | `ObjectType` | — |
| `specialties.py` | `Specialty` | — |
| `weapons.py` | `MeleeWeapon`, `RangedWeapon`, `ThrownWeapon` | — |

### `changeling/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `changeling/cantrips.py` | `Cantrip` | — |
| `changeling/chimera.py` | `Chimera` | — |
| `changeling/kiths.py` | `Kith` | — |
| `changeling/treasures.py` | `Treasure` | — |

### `character_templates/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `character_templates/__init__.py` | — | — |
| `character_templates/changeling_templates.py` | `CharacterTemplate` | — |
| `character_templates/demon_templates.py` | `CharacterTemplate` | — |
| `character_templates/faction_templates.py` | `CharacterTemplate` | — |
| `character_templates/mage_templates.py` | `CharacterTemplate` | — |
| `character_templates/vampire_templates.py` | `CharacterTemplate` | — |
| `character_templates/werewolf_templates.py` | `CharacterTemplate` | — |
| `character_templates/wraith_templates.py` | `CharacterTemplate` | — |

### `demon/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `demon/demon_earthbound_abilities.py` | `Ability` | — |
| `demon/demon_earthbound_archetypes.py` | `Archetype` | — |
| `demon/demon_earthbound_backgrounds.py` | `Background` | — |
| `demon/demon_earthbound_lores.py` | `Lore` | — |
| `demon/demon_earthbound_relics.py` | `Relic` | — |
| `demon/demon_earthbound_rituals.py` | `Ritual` | `demon.demon_earthbound_lores`, `demon.demon_lores` |
| `demon/demon_factions.py` | `DemonFaction` | — |
| `demon/demon_houses.py` | `DemonHouse` | — |
| `demon/demon_lores.py` | `Lore` | `demon.demon_houses` |
| `demon/demon_merits_and_flaws.py` | `MeritFlaw` | `objects` |
| `demon/demon_relics.py` | `Relic` | `demon.demon_houses` |
| `demon/demon_relics_hotf_defilers.py` | `Relic` | `demon.demon_houses` |
| `demon/demon_relics_hotf_devils.py` | `Relic` | `demon.demon_houses` |
| `demon/demon_relics_hotf_devourers.py` | `Relic` | `demon.demon_houses` |
| `demon/demon_relics_hotf_fiends.py` | `Relic` | `demon.demon_houses` |
| `demon/demon_relics_hotf_slayers.py` | `Relic` | `demon.demon_houses` |
| `demon/demon_rituals.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_defilers.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_devils.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_devourers.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_fiends.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_malefactors.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_scourges.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_rituals_hotf_slayers.py` | `Ritual` | `demon.demon_houses`, `demon.demon_lores` |
| `demon/demon_visages.py` | `ApocalypticForm`, `ApocalypticFormTrait`, `Visage` | `demon.demon_houses` |

### `mage/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `mage/artifacts.py` | `SorcererArtifact` | — |
| `mage/corruptedpractices.py` | `CorruptedPractice` | `mage.practices_INC` |
| `mage/effects_INC.py` | `Effect` | — |
| `mage/fellowships.py` | `Attribute`, `SorcererFellowship`, `LinearMagicPath` | `attributes`, `vampire.linear_magic_path` |
| `mage/houses_INC.py` | `House`, `HouseFaction` | — |
| `mage/instruments_INC.py` | `Instrument` | — |
| `mage/legacies.py` | `Legacy` | — |
| `mage/mage_example_companions.py` | `Companion`, `SpiritCharm` | `advantages`, `archetypes` |
| `mage/mage_example_items.py` | `Resonance`, `Artifact`, `Charm`, `Grimoire`, `Talisman`, `Wonder` | `mage.effects_INC` |
| `mage/mage_example_rotes.py` | `Rote` | `abilities`, `attributes`, `mage.effects_INC`, `mage.practices_INC` |
| `mage/mage_spirits.py` | `SpiritCharm`, `SpiritCharacter` | — |
| `mage/magefactions.py` | `MageFaction`, `Paradigm`, `Practice`, `Sphere` | `languages`, `mage.mediums`, `mage.paradigms_INC`, `mage.practices_INC`, `mage.spheres`, `materials` |
| `mage/mediums.py` | `Medium` | — |
| `mage/paradigms_INC.py` | `Paradigm` | `mage.tenets` |
| `mage/practices_INC.py` | `Instrument`, `Practice`, `Resonance` | `abilities`, `mage.instruments_INC` |
| `mage/rotes.py` | `Ability`, `Attribute`, `Effect`, `Practice`, `Rote` | `mage.effects_INC`, `abilities`, `attributes`, `mage.practices_INC` |
| `mage/sectors.py` | `Sector` | — |
| `mage/specializedpractices.py` | `SpecializedPractice` | `mage.magefactions`, `mage.practices_INC` |
| `mage/spheres.py` | `Sphere` | — |
| `mage/tenets.py` | `Tenet` | `mage.practices_INC` |
| `mage/wonders_INC.py` | `Effect`, `Artifact`, `Grimoire`, `Talisman`, `Resonance`, `Charm`, `Wonder` | `mage.effects_INC` |

### `mummy/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `mummy/__init__.py` | — | — |
| `mummy/dynasties.py` | `Dynasty` | — |
| `mummy/titles.py` | `MummyTitle` | — |

### `vampire/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `vampire/linear_magic_path.py` | `Statistic`, `LinearMagicPath` | — |
| `vampire/linear_magic_rituals.py` | `LinearMagicPath`, `LinearMagicRitual` | `vampire.linear_magic_path` |
| `vampire/vampire_bloodlines.py` | `VampireClan` | `vampire.vampire_clans`, `vampire.vampire_disciplines` |
| `vampire/vampire_clans.py` | `VampireClan` | `vampire.vampire_disciplines` |
| `vampire/vampire_disciplines.py` | `Discipline` | — |
| `vampire/vampire_paths.py` | `Path` | — |
| `vampire/vampire_sects.py` | `VampireSect` | — |
| `vampire/vampire_titles.py` | `VampireTitle` | `vampire.vampire_sects` |

### `werewolf/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `werewolf/battle_scars.py` | `BattleScar` | — |
| `werewolf/camps.py` | `Camp` | `werewolf.tribes` |
| `werewolf/fera_gifts.py` | `Gift`, `GiftPermission` | — |
| `werewolf/fetishes.py` | `Fetish` | — |
| `werewolf/fomor_powers_INC.py` | `FomoriPower` | — |
| `werewolf/gifts_INC.py` | `Gift`, `GiftPermission` | — |
| `werewolf/renown_incidents.py` | `RenownIncident` | `werewolf.rites` |
| `werewolf/rites.py` | `Rite` | — |
| `werewolf/spirit_charms.py` | `SpiritCharm`, `Gift` | — |
| `werewolf/spirits.py` | `SpiritCharm`, `SpiritCharacter` | — |
| `werewolf/talens.py` | `Talen` | — |
| `werewolf/totems.py` | `Totem` | — |
| `werewolf/tribes.py` | `Tribe` | — |

### `wraith/`

| Script | Models imported | Scripts imported (`populate_db.` omitted) |
|---|---|---|
| `wraith/wraith_factions.py` | `WraithFaction` | — |
| `wraith/wraith_guilds.py` | `Guild` | — |
| `wraith/wraith_shadow_archetypes.py` | `ShadowArchetype` | — |
| `wraith/wraith_thorns.py` | `Thorn` | — |

## See also

- [Loading](loading.md)
- [Conventions](conventions.md)
- [Adding data](adding-data.md)
- [Glossary](../../docs/reference/glossary.md)
- [populate_db overview](../README.md)
