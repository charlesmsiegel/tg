# Glossary

Terms you meet in this codebase: the project's own vocabulary (storytellers, chronicles,
chargen, route policies, Spread) and the World of Darkness game terms its models are named
after. One line each, with the place in the code where the concept lives when that helps. It is
for developers and agents who know Django but not the games, or the games but not the code.

## Project terms

| Term | Meaning |
|------|---------|
| Action | One state change on one object with its own `POST` URL, built on `core.actions.ObjectActionView`; route policy `ACTION`. |
| Admin (role) | `Role.ADMIN`: a staff or superuser account; may do everything `PermissionManager` allows ([`core/permissions.py`](../../core/permissions.py)). |
| Approval | A storyteller moving a submitted object to `App`; see [XP, freebies and approvals](../architecture/xp-and-approvals.md). |
| Book, source | `core.models.Book` and `BookReference` (book plus page); every `core.models.Model` has `sources` and `add_source(title, page)`. |
| Character | `characters.models.core.character.Character`, the root of every playable character; `Human` adds the World of Darkness stat blocks. |
| Character template | `core.models.CharacterTemplate`: a stored set of starting traits applied to a new character; routes under `/templates/`. |
| Chargen | Character creation: the step-by-step wizard defined in [`characters/chargen/`](../../characters/chargen/); see [Character creation](../architecture/character-creation.md). |
| Chargen step | One `Step` of a `Workflow` (attributes, abilities, freebies, ...), served by a step view with the `CHARGEN_STEP` policy. |
| Chronicle | `game.models.Chronicle`: a campaign, with a head storyteller, storytellers, allowed object types and the characters, scenes and stories played in it. |
| `creation_status` | Integer field on `Character` (and `LocationModel`): the 1-based position of the current chargen step. |
| `display` | Boolean on `core.models.Model`; `False` leaves an object out of `ModelQuerySet.visible()` (the character index uses it) and out of the Known-by section. |
| Fixture seed | `core.tests.template_fixtures.seed()`: one approved instance of every concrete model, used by the render smoke test, the query budgets and `scripts/template_screenshots.py`. |
| Freebies | Freebie points spent at the end of chargen on extra traits; `Human.freebies` (default 15), spent through `FreebieSpendingServiceFactory` ([`characters/services/freebie_spending/`](../../characters/services/freebie_spending/)). |
| `freebies_approved` | Flag on `core.models.Model`: a storyteller has approved the freebie pool; the chargen Freebies step waits for it. |
| Gameline | One World of Darkness game line; a key of `settings.GAMELINES` (table below) and the `gameline` class attribute of every polymorphic model. |
| `game.models.Gameline` | A named game line row, used by `STRelationship` to scope a storyteller to one line in a chronicle. |
| Golden fixture | [`characters/tests/fixtures/chargen_order.json`](../../characters/tests/fixtures/chargen_order.json): the reviewed order of every workflow's step views. |
| Group | `characters.models.core.group.Group`: a set of characters with a leader; gameline groups are Coterie, Pack, Cabal, Motley, Circle, Conclave. |
| Head ST | The chronicle's head storyteller, `Chronicle.head_st`; `Role.CHRONICLE_HEAD_ST`. |
| Heading | The CSS class `<gameline>_heading` (`Model.get_heading()`); also `Profile.preferred_heading` and `Chronicle.headings`. |
| House rule | `core.models.HouseRule`: a table rule with an optional chronicle and a gameline (default `wod`); routes under `/houserules/`. |
| htmx fragment | A partial HTML response to an htmx request, labelled with the `TG-Fragment` header ([`core/htmx.py`](../../core/htmx.py)). |
| Interactive workflow | A chargen `Workflow(interactive=True)` that swaps step fragments with htmx and validates live; only Vampire today. |
| Journal | `game.models.Journal`: one per character, holding dated `JournalEntry` rows a storyteller can answer. |
| Known by | The section of a reference detail page listing characters that hold the trait ([`characters/views/core/known_by.py`](../../characters/views/core/known_by.py)). |
| Legacy database | A database created before a schema change; brought up to date by `tg_schema` migrations. |
| Limited form | The owner's edit form with descriptive fields only (`LimitedHumanEditForm`, `LimitedItemEditForm`), chosen by `ScopedEditFormMixin`. |
| Live model | A model looked up by label when a `tg_schema` migration runs (`tg_schema.schema.live_model`), never imported. |
| Local apps | `accounts`, `characters`, `core`, `game`, `items`, `locations`: they commit no migrations ([Schema migrations](../architecture/schema-migrations.md)). |
| NPC | `CharacterModel.npc`: a character run by the storyteller. The creation pages show the checkbox to storytellers only, and ignore it from anyone else (`ScopedCreationFormMixin`, `prepare_created_object`); the `OBJECT_WRITE` field guard refuses changes to it from non-staff users. |
| Object type | `game.models.ObjectType`: a seeded (`name`, `type`, `gameline`) row naming a creatable character type (`type` is `char`, `obj` or `loc`); feeds the new-character menu. |
| `object_perms` | The template context value holding the viewer's capabilities on the page's object (`core.permission_context.ObjectPermissions`). |
| Observer | `core.models.Observer`: a user granted access to one object; `Role.OBSERVER`, which carries `VIEW_PARTIAL` (the public card). |
| Owner | `core.models.Model.owner`: the player who owns an object; `Role.OWNER`. `None` for shared storyteller objects. |
| Player | `Role.PLAYER`: a user who owns a character in the object's chronicle; carries `VIEW_PARTIAL`. |
| Polymorphic model | A model built on `django-polymorphic`; `core.models.Model` is one, so a `Character` query can return `Vampire` rows ([Data model](../architecture/data-model.md)). |
| Post | `game.models.Post`: one message in a scene, optionally with a dice `roll`. |
| Public card | The minimal public view of an object a viewer cannot fully read (`core.views.public_object.PublicObjectDetailView`, `core/public_object_detail.html`). |
| Query budget | A ceiling on queries per page in [`core/tests/test_query_budgets.py`](../../core/tests/test_query_budgets.py) (`SHEET_CEILINGS`, `SCENE_CEILING`, `INDEX_CEILING`). |
| Reference data | Public game data (Clans, Disciplines, Gifts, Spheres, ...): `PUBLIC_READ` to read, `STAFF_WRITE` to write; see [Adding reference data](../guides/adding-reference-data.md). |
| Registry | `core.model_registry.ModelRegistry` in [`items/registry.py`](../../items/registry.py) and [`locations/registry.py`](../../locations/registry.py): one declaration per item or location model that builds its views, URLs and policies. |
| Route policy | The access rule for a view, declared in [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py) or a registry `ActionSpec` and enforced by `AuthorizationMiddleware`; see [Authorization](../architecture/authorization.md). |
| Router | A `core.views.generic.DictView` that hands a request to another view by the object's `type` or `creation_status`; route policy `ROUTER`. |
| Scene | `game.models.Scene`: one session of play in a chronicle, with characters, a location, posts and a `visibility`. |
| Scoped editor | A user who may fully edit an object: staff, the chronicle's head ST, or a storyteller of the chronicle and the object's gameline (`PermissionManager.user_has_scoped_editor_role`). |
| Service | A function or class that performs a state change and its rules (`characters/services/`, `core/services/`, `game/`); views call it. |
| Setting element | `game.models.SettingElement`: a named piece of setting lore; `Chronicle.common_knowledge_elements`. |
| Sheet | A character's detail page, built on [`characters/core/character/detail.html`](../../characters/templates/characters/core/character/detail.html). |
| Spread | The site's design system: [`core/static/core/tl/tl.css`](../../core/static/core/tl/tl.css), the `core/tl_base.html` page shell (cover and pages), `tl-` CSS classes and the `tl` template tags; see [Front end](../architecture/frontend.md). |
| ST, storyteller | The game master. `STRelationship` (user, chronicle, `Gameline`) makes a user a storyteller of one line in one chronicle; `Profile.is_st()` is true for anyone with such a row. |
| ST relationship | `game.models.STRelationship`, above. It gives `Role.CHRONICLE_ST` on the chronicle's objects of that gameline (matched by the `Gameline` name) and `Role.CHRONICLE_ST_VIEW` on the rest. |
| Game storyteller | A user in `Chronicle.game_storytellers`: a view-only storyteller; `Role.GAME_ST`. |
| Story | `game.models.Story`: a named story arc in a chronicle, the unit of story XP (`StoryXPRequest.story`). |
| `tg_schema` | The app whose committed, guarded migrations update legacy databases ([`tg_schema/`](../../tg_schema/)); see [Changing the schema](../guides/changing-the-schema.md). |
| `type` | The unique snake_case class attribute of every polymorphic model (`"vampire"`, `"wonder"`); keys workflows, routers and registries. |
| Visibility | `core.models.PermissionMixin.visibility`: `PUB` (public), `PRI` (private, default), `CHR` (chronicle only), `CUS` (custom). Scenes have their own: `CHRONICLE`, `PARTICIPANTS`, `PUBLIC`. |
| Visibility tier | `VisibilityTier.FULL`, `PARTIAL` or `NONE`: how much of an object a viewer sees. |
| Week | `game.models.Week`: a seven-day period ending on `end_date`, the unit of weekly XP. |
| Workflow | `characters.chargen.workflow.Workflow`: the ordered chargen steps of one character type, in `WORKFLOWS` ([`characters/chargen/definitions.py`](../../characters/chargen/definitions.py)). |
| XP | Experience points: `Character.xp`, earned from scenes, weeks and stories and spent through `XPSpendingRequest` rows a storyteller approves. |
| XP requests | `game.models.WeeklyXPRequest`, `StoryXPRequest` (earning) and `XPSpendingRequest` (spending); `FreebieSpendingRecord` records freebie spends. |

## Status codes

| Field | Codes |
|-------|-------|
| `status` (`core.constants.CharacterStatus`, on every `core.models.Model`) | `Un` Unapproved (the draft state; default), `Rev` Returned for revisions, `Sub` Submitted, `App` Approved, `Ret` Retired, `Dec` Deceased. Character transitions are in `Character.STATUS_TRANSITIONS`. |
| `image_status` (`core.constants.ImageStatus`) | `un` Unapproved, `sub` Submitted (default), `app` Approved |
| `approved` on `XPSpendingRequest` and `FreebieSpendingRecord` (`core.constants.XPApprovalStatus`) | `Pending`, `Approved`, `Denied` (`WeeklyXPRequest.approved` is a boolean) |

## Roles and permissions

`PermissionManager` ([`core/permissions.py`](../../core/permissions.py)) derives a user's roles
on an object and grants permissions from them.

| Roles | `OWNER`, `ADMIN`, `CHRONICLE_HEAD_ST`, `CHRONICLE_ST`, `CHRONICLE_ST_VIEW`, `GAME_ST`, `PLAYER`, `OBSERVER`, `AUTHENTICATED`, `ANONYMOUS` |
|-------|------|
| Permissions | `VIEW_FULL`, `VIEW_PARTIAL`, `EDIT_FULL`, `EDIT_LIMITED`, `SPEND_XP`, `SPEND_FREEBIES`, `DELETE`, `APPROVE`, `MANAGE_OBSERVERS` |
| Route policies | `PUBLIC_READ`, `PUBLIC_INDEX`, `PUBLIC_CARD`, `ROUTER`, `LOGIN`, `ACCOUNT`, `GAME`, `OBJECT_CREATE`, `OBJECT_LIST`, `OBJECT_DETAIL`, `OBJECT_WRITE`, `OBJECT_ACTION`, `OBJECT_ST_WRITE`, `ACTION`, `CHARGEN_STEP`, `STAFF_WRITE`, `WIDGET` |

## Gamelines

From `settings.GAMELINES` ([`tg/settings/base.py`](../../tg/settings/base.py)) and
`core.constants.GameLine`.

| Code | Name | Short | `app_name` (URL namespace) | Human model |
|------|------|-------|----------------------------|-------------|
| `wod` | World of Darkness | | `wod` (no URL segment) | `Human` |
| `vtm` | Vampire: the Masquerade | VtM | `vampire` | `VtMHuman` |
| `wta` | Werewolf: the Apocalypse | WtA | `werewolf` | `WtAHuman` |
| `mta` | Mage: the Ascension | MtA | `mage` | `MtAHuman` |
| `wto` | Wraith: the Oblivion | WtO | `wraith` | `WtOHuman` |
| `ctd` | Changeling: the Dreaming | CtD | `changeling` | `CtDHuman` |
| `dtf` | Demon: the Fallen | DtF | `demon` | `DtFHuman` |
| `htr` | Hunter: the Reckoning | HtR | `hunter` | `HtRHuman` |
| `mtr` | Mummy: the Resurrection | MtR | `mummy` | `MtRHuman` |
| `orp` | Orpheus | Orp | `orpheus` | none (in `settings.GAMELINES` only; books are tagged with it) |

The eight line codes other than `wod` and `orp` also name a Spread accent colour and display font: `core/tl_base.html` writes the page's `gameline` block into `data-gameline`, and `core/static/core/tl/tl.css` maps `[data-gameline="vtm"]` and the others to `--acc` and `--display`.

## Traits shared by every line

| Term | Meaning and code |
|------|------------------|
| Traits | The rated qualities on a character sheet, usually 0 to 5 dots. |
| Attributes | Nine innate ratings in three groups (Physical: Strength, Dexterity, Stamina; Social: Charisma, Manipulation, Appearance; Mental: Perception, Intelligence, Wits); `AttributeBlock`. |
| Abilities | Learned ratings in three groups: Talents, Skills, Knowledges; `AbilityBlock`, `core.constants.AbilityFields`, and each model's `talents`, `skills`, `knowledges` lists. |
| PRI / SEC / TER | Primary, secondary and tertiary priority: how many dots each Attribute or Ability group gets at chargen (`characters.rules.allocation.PriorityRule`). |
| Backgrounds | Rated advantages such as Allies, Contacts, Mentor, Resources; `Background` and `BackgroundRating` (with a `complete` flag for chargen detail steps). |
| Merits and Flaws | Point-costed advantages and drawbacks; `MeritFlaw` and `MeritFlawRating` (`rating` from -10 to 10; negative for Flaws). |
| Specialty | A focus within a trait: needed at 4 dots, and at 1 dot for broad Abilities such as Crafts or Firearms (`Human.needed_specialties`); `Specialty` (`name`, `stat`). |
| Nature, Demeanor | A character's true and shown personality archetypes; `Human.nature` and `Human.demeanor`, foreign keys to `Archetype`. |
| Willpower | Permanent and temporary Willpower; `Human.willpower` / `temporary_willpower` from `core.linked_stat.linked_stat_fields`. |
| Derangement | A mental illness; `Derangement`. |
| Health | The damage track; `HealthBlock`. |
| Virtues | Moral traits (Conscience, Self-Control, Courage for Vampire; Conviction, Courage, Conscience for Demon). |
| Freebie points, XP | See Project terms. |
| Splat | Informal: a character type within a gameline (a Vampire clan, a Werewolf tribe, a Changeling kith). |
| Mortal, Kinfolk, Ghoul... | Humans tied to a line: each line's Human model plus lesser supernaturals (Ghoul, Revenant, Kinfolk, Fomor, Drone, Companion, Sorcerer, Thrall, Autumn Person). |

## Gameline terms

| Gameline | Terms and their models |
|----------|------------------------|
| Vampire | Kindred `Vampire`; `VampireClan` (Clans and bloodlines), `VampireSect`, `VampireTitle`, `Path` (Paths of Enlightenment, an alternative to Humanity), `Discipline` (supernatural powers, rated fields such as `Vampire.potence`), `Ghoul`, `Revenant` / `RevenantFamily`, `Coterie` (group); items `VampireArtifact`, `Bloodstone`; locations `Domain`, `Elysium`, `Haven`, `Rack`, `Barrens`, `TremereChantry`. |
| Werewolf | Garou `Werewolf`; `Tribe`, `Camp`, `Gift` (powers, a many-to-many on the character), `Rite`, `Totem`, `RenownIncident`, `BattleScar`, `SeptPosition`, `Pack` (group), `Kinfolk`, `Fera` and the Changing Breeds (`Ajaba`, `Ananasi`, `Bastet`, `Corax`, `Grondr`, `Gurahl`, `Kitsune`, `Mokole`, `Nagah`, `Nuwisha`, `Ratkin`, `Rokea`), `Fomor` / `FomoriPower`, `Drone`, `SpiritCharacter`, `SpiritCharm`; items `Fetish`, `Talen`; location `Caern`. The Gauntlet is `LocationModel.gauntlet`. |
| Mage | `Mage` with Arete, Quintessence and Paradox; `Sphere` (the nine Spheres, rated fields), `Rote`, `Effect`, `Resonance`, focus (`Paradigm`, `Practice`, `SpecializedPractice`, `CorruptedPractice`, `Instrument`, `Tenet`), `MageFaction` (Traditions, Conventions and other factions, nested through `parent`), `Cabal` (group), `Companion` / `Advantage`, `Sorcerer` with `LinearMagicPath` and `LinearMagicRitual`, `SorcererFellowship`; items `Wonder`, `Talisman`, `Charm`, `Periapt`, `Artifact`, `Grimoire`, `SorcererArtifact`; locations `Node`, `Sanctum`, `Chantry`, `Library`, `RealityZone`, `HorizonRealm`, `Demesne`, `ParadoxRealm`, `Sector`. |
| Wraith | `Wraith`; `Arcanos` (Arcanoi, the powers), `Guild`, `WraithFaction`, `Passion`, `Fetter`, `ShadowArchetype` and `Thorn` (the Shadow), Pathos and Angst, `Circle` (group); items `WraithArtifact`, `WraithRelic`; locations `Haunt`, `Necropolis`, `Citadel`, `Byway`, `Nihil`, `WraithFreehold`. The Shroud is `LocationModel.shroud`. |
| Changeling | Kithain `Changeling`; `Kith`, `House`, `HouseFaction`, `Legacy`, `Cantrip`, `Chimera`, Arts and Realms (rated fields), Glamour and Banality, `Motley` (group), `Inanimae`, `Nunnehi`, `AutumnPerson`; items `Treasure`, `Dross`; locations `Freehold`, `Holding`, `Trod`, `DreamRealm`. |
| Demon | The Fallen `Demon`; `DemonHouse` (the seven Houses), `DemonFaction`, `Lore` (powers, rated fields such as `lore_of_...`), `ApocalypticForm` / `ApocalypticFormTrait`, `Visage`, Faith and Torment, `Pact`, `Thrall` (a mortal bound by a pact), `Earthbound`, `Ritual`, `Conclave` (group); item `Relic`; locations `Bastion`, `Reliquary`. |
| Hunter | `Hunter`; `Creed`, `Edge` (powers), `HunterOrganization`; items `HunterGear`, `HunterRelic`; locations `HuntingGround`, `Safehouse`. |
| Mummy | `Mummy` with Sekhem and Hekau; `Dynasty`, `MummyTitle`; items `MummyRelic`, `Vessel`, `Ushabti`; locations `Tomb`, `CultTemple`, `UndergroundSanctuary`. |

## See also

- [Data model](../architecture/data-model.md)
- [Authorization](../architecture/authorization.md)
- [Character creation](../architecture/character-creation.md)
- [XP, freebies and approvals](../architecture/xp-and-approvals.md)
- [URL reference](urls.md)
