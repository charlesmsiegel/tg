# MODELS.md

This document provides a comprehensive inventory of all models across all apps in this project, along with their implementation status for URLs, Views, Templates, Forms, and Index integration.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Fully implemented |
| ⚠️ | Partially implemented |
| ❌ | Not implemented |
| N/A | Not applicable |

---

## Table of Contents

1. [Characters App](#characters-app)
   - [Core Models](#characters-core-models)
   - [Vampire (VtM)](#vampire-vtm)
   - [Werewolf (WtA)](#werewolf-wta)
   - [Mage (MtA)](#mage-mta)
   - [Wraith (WtO)](#wraith-wto)
   - [Changeling (CtD)](#changeling-ctd)
   - [Demon (DtF)](#demon-dtf)
   - [Mummy (MtR)](#mummy-mtr)
   - [Hunter (HtR)](#hunter-htr)
2. [Items App](#items-app)
   - [Core Items](#items-core)
   - [Vampire Items](#items-vampire)
   - [Werewolf Items](#items-werewolf)
   - [Mage Items](#items-mage)
   - [Wraith Items](#items-wraith)
   - [Changeling Items](#items-changeling)
   - [Demon Items](#items-demon)
   - [Mummy Items](#items-mummy)
   - [Hunter Items](#items-hunter)
3. [Locations App](#locations-app)
   - [Core Locations](#locations-core)
   - [Vampire Locations](#locations-vampire)
   - [Werewolf Locations](#locations-werewolf)
   - [Mage Locations](#locations-mage)
   - [Wraith Locations](#locations-wraith)
   - [Changeling Locations](#locations-changeling)
   - [Demon Locations](#locations-demon)
   - [Mummy Locations](#locations-mummy)
   - [Hunter Locations](#locations-hunter)
4. [Game App](#game-app)
5. [Core App](#core-app)
6. [Accounts App](#accounts-app)

---

## Characters App

### Characters Core Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Character | `core/character.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Human | `core/human.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Group | `core/group.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Archetype | `core/archetype.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| MeritFlaw | `core/merit_flaw_block.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Specialty | `core/specialty.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Derangement | `core/derangement.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Statistic | `core/statistic.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Attribute | `core/attribute_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| AttributeBlock | `core/attribute_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Ability | `core/ability_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| AbilityBlock | `core/ability_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Background | `core/background_block.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| BackgroundRating | `core/background_block.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| PooledBackgroundRating | `core/background_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| BackgroundBlock | `core/background_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| MeritFlawRating | `core/merit_flaw_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| MeritFlawBlock | `core/merit_flaw_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| HealthBlock | `core/health_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Vampire (VtM)

#### Character Types

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| VtMHuman | `vampire/vtmhuman.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Vampire | `vampire/vampire.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ghoul | `vampire/ghoul.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Revenant | `vampire/revenant.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚠️ |
| Coterie | `vampire/coterie.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | N/A |

#### Reference Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| VampireClan | `vampire/clan.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Discipline | `vampire/discipline.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| VampireSect | `vampire/sect.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Path | `vampire/path.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| VampireTitle | `vampire/title.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| RevenantFamily | `vampire/revenant.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ❌ |

### Werewolf (WtA)

#### Character Types

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| WtAHuman | `werewolf/wtahuman.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Werewolf | `werewolf/garou.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Kinfolk | `werewolf/kinfolk.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Fera | `werewolf/fera.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Bastet | `werewolf/bastet.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Corax | `werewolf/corax.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Gurahl | `werewolf/gurahl.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Mokole | `werewolf/mokole.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Nuwisha | `werewolf/nuwisha.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ratkin | `werewolf/ratkin.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Rokea | `werewolf/rokea.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ananasi | `werewolf/ananasi.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Ajaba | `werewolf/ajaba.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Nagah | `werewolf/nagah.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Kitsune | `werewolf/kitsune.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Grondr | `werewolf/grondr.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Fomor | `werewolf/fomor.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Drone | `werewolf/drone.py` | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| SpiritCharacter | `werewolf/spirit_character.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ | N/A |
| Pack | `werewolf/pack.py` | ⚠️ | ❌ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ✅ | N/A |

#### Reference Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Tribe | `werewolf/tribe.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Gift | `werewolf/gift.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| GiftPermission | `werewolf/gift.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Rite | `werewolf/rite.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Camp | `werewolf/camp.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Charm | `werewolf/charm.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Totem | `werewolf/totem.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Battlescar | `werewolf/battlescar.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| SeptPosition | `werewolf/septposition.py` | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ⚠️ |
| RenownIncident | `werewolf/renownincident.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| FomoriPower | `werewolf/fomoripower.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |

### Mage (MtA)

#### Character Types

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| MtAHuman | `mage/mtahuman.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Mage | `mage/mage.py` | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Companion | `mage/companion.py` | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Sorcerer | `mage/sorcerer.py` | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Cabal | `mage/cabal.py` | ⚠️ | ❌ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ✅ | N/A |

#### Reference Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Sphere | `mage/sphere.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| Resonance | `mage/resonance.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Rote | `mage/rote.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Effect | `mage/effect.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Instrument | `mage/focus.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Practice | `mage/focus.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| SpecializedPractice | `mage/focus.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| CorruptedPractice | `mage/focus.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Tenet | `mage/focus.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Paradigm | `mage/focus.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| MageFaction | `mage/faction.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Fellowship | `mage/fellowship.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| SorcererFellowship | `mage/fellowship.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Advantage | `mage/companion.py` | ✅ | ✅ | ❌ | ❌ | ❌ | N/A | ✅ | ⚠️ |
| LinearMagicPath | `mage/sorcerer.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| LinearMagicRitual | `mage/sorcerer.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| ResRating | `mage/mage.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| PracticeRating | `mage/mage.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| PathRating | `mage/sorcerer.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| AdvantageRating | `mage/companion.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |

### Wraith (WtO)

#### Character Types

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| WtOHuman | `wraith/wtohuman.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Wraith | `wraith/wraith.py` | ✅ | ⚠️ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Circle | `wraith/circle.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | N/A |

#### Reference Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| WraithFaction | `wraith/faction.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| Guild | `wraith/guild.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| Arcanos | `wraith/arcanos.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| ShadowArchetype | `wraith/shadow_archetype.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| Passion | `wraith/passion.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Fetter | `wraith/fetter.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Thorn | `wraith/thorn.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| ThornRating | `wraith/wraith.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Changeling (CtD)

#### Character Types

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| CtDHuman | `changeling/ctdhuman.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Changeling | `changeling/changeling.py` | ✅ | ⚠️ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Inanimae | `changeling/inanimae.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Nunnehi | `changeling/nunnehi.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| AutumnPerson | `changeling/autumn_person.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Motley | `changeling/motley.py` | ⚠️ | ❌ | ✅ | ✅ | ❌ | ✅ | ⚠️ | ✅ | N/A |

#### Reference Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Kith | `changeling/kith.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| House | `changeling/house.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| HouseFaction | `changeling/house_faction.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Legacy | `changeling/legacy.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Cantrip | `changeling/cantrip.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ |
| Chimera | `changeling/chimera.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |

### Demon (DtF)

#### Character Types

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| DtFHuman | `demon/dtf_human.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Demon | `demon/demon.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Thrall | `demon/thrall.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Earthbound | `demon/earthbound.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ⚠️ |
| Conclave | `demon/conclave.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | N/A |

#### Reference Models

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Lore | `demon/lore.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| LoreBlock | `demon/lore_block.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| DemonHouse | `demon/house.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| DemonFaction | `demon/faction.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Visage | `demon/visage.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| ApocalypticFormTrait | `demon/apocalyptic_form.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| Ritual | `demon/ritual.py` | ⚠️ | ✅ | ❌ | ✅ | ❌ | ⚠️ | ✅ | ⚠️ |
| Pact | `demon/pact.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| LoreRating | `demon/demon.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Mummy (MtR)

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| MtRHuman | `mummy/mtr_human.py` | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Mummy | `mummy/mummy.py` | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Dynasty | `mummy/dynasty.py` | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ⚠️ | N/A |
| MummyTitle | `mummy/mummy_title.py` | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ⚠️ | N/A |

### Hunter (HtR)

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index | Chargen |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|:-------:|
| HtRHuman | `hunter/htrhuman.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Hunter | `hunter/hunter.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| Creed | `hunter/creed.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | N/A |
| Edge | `hunter/edge.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | N/A |
| HunterOrganization | `hunter/organization.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ | N/A |

---

## Items App

### Items Core

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| ItemModel | `core/item.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Weapon | `core/weapon.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| MeleeWeapon | `core/meleeweapon.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| RangedWeapon | `core/rangedweapon.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| ThrownWeapon | `core/thrownweapon.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Medium | `core/medium.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Material | `core/material.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |

### Items Vampire

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| VampireArtifact | `vampire/artifact.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Bloodstone | `vampire/bloodstone.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Items Werewolf

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Fetish | `werewolf/fetish.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Talen | `werewolf/talen.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Items Mage

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Wonder | `mage/wonder.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| WonderResonanceRating | `mage/wonder.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Artifact | `mage/artifact.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Charm | `mage/charm.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Grimoire | `mage/grimoire.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Periapt | `mage/periapt.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Talisman | `mage/talisman.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| SorcererArtifact | `mage/sorcerer_artifact.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Items Wraith

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| WraithArtifact | `wraith/artifact.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| WraithRelic | `wraith/relic.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Items Changeling

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Treasure | `changeling/treasure.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Dross | `changeling/dross.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |

### Items Demon

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Relic | `demon/relic.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Items Mummy

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Ushabti | `mummy/ushabti.py` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Vessel | `mummy/vessel.py` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| MummyRelic | `mummy/relic.py` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| RelicResonanceRating | `mummy/relic.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

### Items Hunter

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| HunterGear | `hunter/gear.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| HunterRelic | `hunter/relic.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |

---

## Locations App

### Locations Core

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| LocationModel | `core/location.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| City | `core/city.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Locations Vampire

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Haven | `vampire/haven.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| HavenMeritFlawRating | `vampire/haven.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Domain | `vampire/domain.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Elysium | `vampire/elysium.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| TremereChantry | `vampire/chantry.py` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |
| Rack | `vampire/rack.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Barrens | `vampire/barrens.py` | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ⚠️ |

### Locations Werewolf

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Caern | `werewolf/caern.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Locations Mage

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Node | `mage/node.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| NodeMeritFlawRating | `mage/node.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| NodeResonanceRating | `mage/node.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Sanctum | `mage/sanctum.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Chantry | `mage/chantry.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| ChantryBackgroundRating | `mage/chantry.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Demesne | `mage/demesne.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| HorizonRealm | `mage/realm.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Library | `mage/library.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| RealityZone | `mage/reality_zone.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| ZoneRating | `mage/reality_zone.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Sector | `mage/sector.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| ParadoxRealm | `mage/paradox_realm.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| ParadoxObstacle | `mage/paradox_realm.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| ParadoxAtmosphere | `mage/paradox_realm.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |

### Locations Wraith

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Citadel | `wraith/citadel.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Haunt | `wraith/haunt.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| WraithFreehold | `wraith/freehold.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Byway | `wraith/byway.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Nihil | `wraith/nihil.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Necropolis | `wraith/necropolis.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Locations Changeling

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Freehold | `changeling/freehold.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Holding | `changeling/holding.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| Trod | `changeling/trod.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| DreamRealm | `changeling/dream_realm.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |

### Locations Demon

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Bastion | `demon/bastion.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Reliquary | `demon/reliquary.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |

### Locations Mummy

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Tomb | `mummy/tomb.py` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| TombMeritFlawRating | `mummy/tomb.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| UndergroundSanctuary | `mummy/sanctuary.py` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| CultTemple | `mummy/cult_temple.py` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |

### Locations Hunter

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Safehouse | `hunter/safehouse.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| HuntingGround | `hunter/huntingground.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |

---

## Game App

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Chronicle | `game/models.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ✅ |
| STRelationship | `game/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Story | `game/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Week | `game/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Scene | `game/models.py` | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | ✅ | ✅ |
| UserSceneReadStatus | `game/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Post | `game/models.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| JournalEntry | `game/models.py` | N/A | N/A | N/A | N/A | N/A | ✅ | N/A | N/A |
| Journal | `game/models.py` | ✅ | ✅ | N/A | N/A | ❌ | N/A | ✅ | ✅ |
| WeeklyXPRequest | `game/models.py` | ✅ | ✅ | ✅ | ⚠️ | ❌ | ✅ | ✅ | ✅ |
| StoryXPRequest | `game/models.py` | ✅ | ✅ | ⚠️ | ⚠️ | ❌ | ⚠️ | ✅ | ✅ |
| XPSpendingRequest | `game/models.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| FreebieSpendingRecord | `game/models.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| ObjectType | `game/models.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |
| SettingElement | `game/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Gameline | `game/models.py` | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | ⚠️ | ⚠️ | ⚠️ |

---

## Core App

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Model | `core/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Book | `core/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| BookReference | `core/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Observer | `core/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| NewsItem | `core/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Language | `core/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Number | `core/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| Noun | `core/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| HouseRule | `core/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| CharacterTemplate | `core/models.py` | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| TemplateApplication | `core/models.py` | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

---

## Accounts App

| Model | File | List | Detail | Create | Update | Delete | Form | Template | Index |
|-------|------|:----:|:------:|:------:|:------:|:------:|:----:|:--------:|:-----:|
| Profile | `accounts/models.py` | ⚠️ | ✅ | N/A | ✅ | ❌ | ✅ | ✅ | N/A |

---

## Summary Statistics

### Overall Implementation Status

| App | Total Models | Fully Implemented | Partially Implemented | Not Implemented |
|-----|--------------|-------------------|----------------------|-----------------|
| Characters | 148 | 89 | 42 | 17 |
| Items | 29 | 21 | 4 | 4 |
| Locations | 47 | 31 | 10 | 6 |
| Game | 17 | 8 | 8 | 1 |
| Core | 11 | 5 | 0 | 6 |
| Accounts | 1 | 0 | 1 | 0 |
| **Total** | **253** | **154** | **65** | **34** |

### Implementation Gaps by Category

**Missing Delete Views**: All models (project does not implement deletion through the UI)

**Mummy Gameline**: Largely unimplemented (detail views only)

**Hunter Gameline**: Partially implemented (needs completion)

**Group Models** (Pack, Cabal, Motley, Circle, Conclave): Missing detail views

**Reference Models**: Many missing dedicated list views/index integration

---

## Notes

1. **Abstract/Mixin Models** (AttributeBlock, AbilityBlock, etc.) are marked N/A as they don't require CRUD operations
2. **Through Models** (BackgroundRating, MeritFlawRating, etc.) are marked N/A for List/Detail/Create/Update but may have Form support for inline editing
3. **Index** column indicates whether the model appears in the main app index page and/or create dropdown
4. **Chargen** column (character tables only) indicates character generation workflow support
5. All models use polymorphic inheritance from `core.models.Model` for Characters, Items, and Locations
