# Domain terms

World of Darkness and site terms mapped to the codes, models and fields that implement
them, so names in new code match the existing ones. Definitions for readers are in
[docs/reference/glossary.md](../../../../docs/reference/glossary.md); game rules belong to
the `wod-toolkit` skill.

## Gamelines

`settings.GAMELINES` ([`tg/settings/base.py`](../../../../tg/settings/base.py)) is the
registry. `core.constants.GameLine` has the same codes as constants (without `orp`) and
the URL module per gameline in `URL_PATTERNS`.

| Code | Name (`GAMELINES[code]["name"]`) | Short | URL namespace | Model folders |
|------|----------------------------------|-------|---------------|---------------|
| `wod` | World of Darkness | | (core) | `*/models/core/` |
| `vtm` | Vampire: the Masquerade | VtM | `vampire` | `*/models/vampire/` |
| `wta` | Werewolf: the Apocalypse | WtA | `werewolf` | `*/models/werewolf/` |
| `mta` | Mage: the Ascension | MtA | `mage` | `*/models/mage/` |
| `wto` | Wraith: the Oblivion | WtO | `wraith` | `*/models/wraith/` |
| `ctd` | Changeling: the Dreaming | CtD | `changeling` | `*/models/changeling/` |
| `dtf` | Demon: the Fallen | DtF | `demon` | `*/models/demon/` |
| `mtr` | Mummy: the Resurrection | MtR | `mummy` | `*/models/mummy/` |
| `htr` | Hunter: the Reckoning | HtR | `hunter` | `*/models/hunter/` |
| `orp` | Orpheus | Orp | | none yet |

`game.Gameline` rows (used by `STRelationship`) must carry exactly the `name` above.

## Statuses

| Constant | Code | Label | Meaning |
|----------|------|-------|---------|
| `CharacterStatus.UNAPPROVED` | `Un` | Unapproved | Draft; the owner edits it and runs chargen |
| `CharacterStatus.REVISION_REQUESTED` | `Rev` | Returned for revisions | Sent back by an ST; editable like a draft |
| `CharacterStatus.SUBMITTED` | `Sub` | Submitted | Waiting for ST approval |
| `CharacterStatus.APPROVED` | `App` | Approved | In play; the owner spends XP |
| `CharacterStatus.RETIRED` | `Ret` | Retired | Out of play |
| `CharacterStatus.DECEASED` | `Dec` | Deceased | Final |
| `ImageStatus.*` | `un`, `sub`, `app` | | Image approval (`Model.image_status`) |
| `XPApprovalStatus.*` | `Pending`, `Approved`, `Denied` | | `XPSpendingRequest.approved`, `FreebieSpendingRecord.approved` |

## Site terms

| Term | Implementation |
|------|----------------|
| ST (Storyteller) | A user with a role in a chronicle: `Chronicle.head_st` (head ST), an `STRelationship(user, chronicle, gameline)` (gameline ST), `Chronicle.game_storytellers` (game ST, read only). Roles in `core.permissions.Role` |
| Scoped ST / scoped editor | `CHRONICLE_HEAD_ST` or `CHRONICLE_ST` for the object's chronicle and gameline (editor adds `ADMIN`) |
| Chronicle | `game.Chronicle`: a campaign; scopes ST authority and object visibility |
| Story | `game.Story`: an arc of scenes within a chronicle |
| Scene | `game.Scene`: a play session with `Post`s; `visibility` `PUBLIC`, `CHRONICLE`, `PARTICIPANTS` |
| Week | `game.Week`: the XP period; `WeeklyXPRequest` per character and week |
| Journal | `game.Journal` (one per character) with `JournalEntry` rows |
| Player object | Characters, groups, items, locations, templates: owned, approvable, private |
| Reference data | Game data (clans, tribes, spheres, disciplines, books): public, staff-edited |
| NPC | `CharacterModel.npc = True` |
| Chargen | Character creation: `characters/chargen/` workflows, position in `Character.creation_status` |
| Freebies | Points spent at the end of chargen; `Human.freebies`, `FreebieSpendingRecord`, `freebies_approved` |
| XP | `Character.xp` (unspent), `XPSpendingRequest` per purchase, `WeeklyXPRequest` / `StoryXPRequest` for awards |
| Observer | `core.Observer`: a user granted partial read access to one object |
| Public card | The anonymous projection of a player object: `name`, `public_info`, approved image |

## Shared character traits

| Game term | Model or field |
|-----------|----------------|
| Attributes (Strength ... Wits) | `AttributeBlock` fields on `Human` (`strength`, `dexterity`, ...) |
| Abilities (Talents, Skills, Knowledges) | `AbilityBlock` fields; per-gameline lists `talents`, `skills`, `knowledges` on the class |
| Backgrounds | `Background` + `BackgroundRating` |
| Merits and Flaws | `MeritFlaw` + `MeritFlawRating` |
| Specialties | `Specialty` |
| Nature / Demeanor | `Human.nature`, `Human.demeanor` (`Archetype`) |
| Willpower | `Human.willpower` / `temporary_willpower` (`linked_stat_fields`) |
| Health | `HealthBlock` |

## Gameline traits

| Gameline | Power system | Key traits (model fields) |
|----------|--------------|---------------------------|
| Vampire | Disciplines (`Discipline`), clan (`VampireClan`), sect, Path (`Path`) | `generation_rating`, `blood_pool`, `max_blood_pool`, virtues (`conviction`, `courage`, ...) |
| Werewolf | Gifts (`Gift`), Rites (`Rite`), tribe (`Tribe`), totem | `rage`, `gnosis`, renown `glory` / `honor` / `wisdom` (linked stats) |
| Mage | Spheres (`Sphere`), rotes and effects (`Rote`, `Effect`), faction (`MageFaction`), practices | `arete`, `quintessence`, `paradox`, resonance (`ResRating`) |
| Wraith | Arcanoi (`Arcanos`), guild (`Guild`), faction, Shadow | `pathos`, `angst` (linked stats), fetters (`Fetter`), passions (`Passion`) |
| Changeling | Arts and Realms, kith (`Kith`), house, legacies, chimerae | `glamour`, `banality` (linked stats) |
| Demon | Lores (`Lore`, `LoreRating`), house (`DemonHouse`), faction, apocalyptic form | `faith`, `torment` (linked stats), `conviction`, `courage` |
| Hunter | Edges (`Edge`), creed (`Creed`) | `conviction`, `vision`, `zeal` (linked stats) |
| Mummy | Hekau, dynasty (`Dynasty`) | `sekhem`, `balance`, `ba` / `ka_rating` |

Use these names in new code: a Vampire field is `generation_rating`, not `generation`; a
paired stat is `<name>` / `temporary_<name>`.

## See also

- [docs/reference/glossary.md](../../../../docs/reference/glossary.md)
- [docs/architecture/data-model.md](../../../../docs/architecture/data-model.md)
- [model-inventory.md](model-inventory.md)
