# Admin

This page describes the Django admin registrations in
[`characters/admin.py`](../admin.py). It is for staff who use `/admin/` to inspect or fix
character data, and for developers adding a model. The admin is a maintenance tool: the
site's own views, route policies and spending services are the supported way to change
characters (see [Authorization](../../docs/architecture/authorization.md)).

## What is registered

102 of the app's 127 models are registered. Most use a plain `ModelAdmin` or a default
registration; a few add list columns, filters and search.

| Area | Registered with custom `ModelAdmin` | Plain `admin.site.register` |
|------|--------------------------------------|-----------------------------|
| Core | `Character`, `Human` (name, owner, chronicle), `Archetype`, `MeritFlaw`, `Derangement`, `Group` (name, leader, chronicle), `Specialty` (name, stat), `BackgroundRating` (char, bg, rating, note) | `CharacterModel`, `MeritFlawRating`, `Statistic`, `Ability`, `Attribute`, `Background`, `PooledBackgroundRating` |
| Vampire | none | `VtMHuman`, `Vampire`, `Ghoul`, `Revenant`, `RevenantFamily`, `VampireClan`, `VampireSect`, `VampireTitle`, `Path`, `Discipline` |
| Werewolf | `Rite`, `Tribe`, `Gift`, `RenownIncident`, `BattleScar`, `Camp`, `Werewolf`, `Kinfolk`, `Pack` (name, leader, totem), `Fomor`, `FomoriPower`, `Totem`, `SpiritCharm`, `SpiritCharacter`, `Drone`, `SeptPosition`, and the breeds `Ajaba`, `Ananasi`, `Grondr`, `Kitsune`, `Nagah`, `Rokea` (breed and renown columns) | `WtAHuman`, `GiftPermission` |
| Mage | `Resonance`, `Effect` (Sphere columns), `Paradigm`, `Practice`, `SpecializedPractice`, `CorruptedPractice`, `Instrument`, `Tenet`, `MageFaction` (name, parent), `Rote` (Sphere columns computed from the Effect), `Mage` (filters: owner, arete, essence, affinity Sphere, chronicle), `ResRating`, `Cabal`, `Companion`, `Sorcerer`, `LinearMagicRitual` | `MtAHuman`, `PracticeRating`, `LinearMagicPath`, `PathRating`, `Sphere`, `SorcererFellowship`, `Advantage`, `AdvantageRating` |
| Wraith | `Wraith` (filters: owner, guild, legion, faction, chronicle, status), `Guild`, `WraithFaction`, `Arcanos`, `ShadowArchetype`, `Thorn` | `WtOHuman`, `ThornRating`, `Fetter`, `Passion` |
| Changeling | `Changeling` | `CtDHuman`, `HouseFaction`, `Legacy`, `House`, `Kith`, `Motley` |
| Demon | `Demon` (filters: owner, house, faction, chronicle, status; search: name, celestial name), `DemonFaction`, `DemonHouse`, `Visage`, `Lore`, `Thrall`, `Earthbound`, `ApocalypticFormTrait`, `Ritual` (search: name, description) | `DtFHuman`, `LoreRating`, `Pact` |

## Not registered

`AutumnPerson`, `Inanimae`, `Nunnehi`, `Cantrip`, `Chimera`, `Coterie`, `Circle`,
`Conclave`, `ApocalypticForm`, `Fera` and the breeds `Bastet`, `Corax`, `Gurahl`, `Mokole`,
`Nuwisha`, `Ratkin`, and every Hunter and Mummy model (`HtRHuman`, `Hunter`, `Creed`,
`Edge`, `HunterOrganization`, `MtRHuman`, `Mummy`, `Dynasty`, `MummyTitle`). Edit these
through the site's views or `python manage.py shell`.

## Cautions

- Admin saves call `Model.save()`, so model rules still run: `Character.clean()` checks
  status transitions when the form is validated, and moving a character to `Ret` or `Dec`
  removes it from its groups and chantries.
- Editing `xp`, `freebies` or ratings directly bypasses the XP and freebie records (see
  [Services](services.md)); prefer the approval pages and actions.
- The `Character`, `Human` and `Group` admins are plain `ModelAdmin`s on polymorphic
  parents: their forms contain only the fields declared up to that class, not a
  subclass's gameline fields.

## See also

- [Character models](models.md)
- [Services](services.md)
- [Maintenance](../../docs/operations/maintenance.md)
- [`characters/admin.py`](../admin.py)
