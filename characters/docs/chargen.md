# Chargen in the characters app

This page is the app-level reference for character creation ("chargen"): the exact
workflow of every character type, the modules that implement each one, the point values
per type, and the services that gameline steps call. The mechanism itself (workflow
registry, routers, `ChargenStepMixin`, allocation rules, the freebie stage, htmx and the
no-JavaScript fallback) is explained once in
[Character creation](../../docs/architecture/character-creation.md); read that first. To add
a step, follow [Adding a chargen step](../../docs/guides/adding-a-chargen-step.md).

## Files

| Path | Responsibility |
|------|----------------|
| [`chargen/__init__.py`](../chargen/__init__.py) | `get_workflow(character_type)` (lazy import, safe during model loading) |
| [`chargen/registry.py`](../chargen/registry.py) | `Step`, `Workflow`, `progress_rows()`, the `WorkflowViews` and `FreebiePosition` descriptors |
| [`chargen/definitions.py`](../chargen/definitions.py) | Shared `Step` constants, `bind()`, one `Workflow` per type in `WORKFLOWS`, `DETAIL_ONLY_FREEBIE_POSITIONS` |
| [`chargen/predicates.py`](../chargen/predicates.py) | Skip predicates |
| [`chargen/transitions.py`](../chargen/transitions.py) | `advance()`, `previous_position()` |
| [`views/core/chargen_mixins.py`](../views/core/chargen_mixins.py), [`allocations.py`](../views/core/allocations.py), [`spending.py`](../views/core/spending.py), [`generic_background.py`](../views/core/generic_background.py), [`chargen_back.py`](../views/core/chargen_back.py) | Shared step machinery (see [Views and URLs](views-and-urls.md#chargen-step-views)) |
| [`rules/`](../rules/) | Allocation rules and point pools (see [Costs and rules](costs-and-rules.md)) |
| [`templates/characters/core/chargen.html`](../templates/characters/core/chargen.html), [`templates/characters/core/chargen/`](../templates/characters/core/chargen/) | Page shell and step partials (see [Templates](templates.md#chargen-templates)) |

## Entry: Basics and templates

Every workflow starts before step 1 with the type's Basics view (`create:<type>`), which
creates the character with the owner, name, concept and type-specific identity fields
(clan, tribe, affiliation, ...). The default `creation_status` is `1`, so the character
lands on step 1.

Six mortal types also have a template picker (`<type>_template`):
`vtm_human`, `wta_human`, `mta_human`, `wto_human`, `ctd_human` and `dtf_human`.
`CharacterTemplateSelectView` renders only while `creation_status` is `0` (position zero
is "outside the numbered registry"); for any other value it redirects straight to the
`<type>_creation` router. Of these Basics views, `VtMHumanBasicsView` redirects to
`vtmhuman_creation` directly; the other five redirect to their template route.

## Workflows by type

Positions are 1-based `creation_status` values. An asterisk marks a step with a `skip_if`
predicate; bracketed steps are background-gated (skipped unless the character bought that
Background and its `BackgroundRating` is incomplete). The freebie column is the
`freebie_step` position.

| Type(s) | Views module (`characters.views.`) | Steps | Freebies |
|---------|-----------------------------------|-------|---------:|
| `human` | `core.human` | 1 attributes, 2 abilities, 3 backgrounds, 4 biography, 5 freebies*, 6 languages*, 7 specialties | 5 |
| `vtm_human` | `vampire.vtmhuman` | as `human`, then 7 [allies], 8 specialties | 5 |
| `vampire` (interactive) | `vampire.vampire_chargen` | 1-3, 4 disciplines, 5 virtues, 6 biography, 7 freebies*, 8 languages*, 9 [allies], 10 [mentor], 11 [contacts], 12 [retainers], 13 specialties | 7 |
| `ghoul` | `vampire.ghoul_chargen` | 1-3, 4 disciplines, 5 biography, 6 freebies*, 7 languages*, 8 [allies], 9 specialties | 6 |
| `wta_human`, `kinfolk` | `werewolf.wtahuman`, `werewolf.kinfolk` | as `vtm_human` | 5 |
| `werewolf` | `werewolf.garou` | 1-3, 4 gifts, 5 history, 6 biography, 7 freebies*, 8 languages*, 9 [allies], 10 [mentor], 11 [contacts], 12 specialties | 7 |
| `fomor` | `werewolf.fomor` | 1-3, 4 powers, 5 biography, 6 freebies*, 7 languages*, 8 [allies], 9 [contacts], 10 specialties | 6 |
| `drone` | `werewolf.drone` | as `human` | 5 |
| `fera` and all twelve breeds | `werewolf.fera` | 1 breed_faction, 2 attributes, 3 abilities, 4 backgrounds, 5 gifts, 6 history, 7 biography, 8 freebies*, 9 languages*, 10 [allies], 11 specialties | 8 |
| `mta_human`, `companion` | `mage.mtahuman`, `mage.companion` | as `human` to 6, then 7 [node], 8 [library], 9 [wonder], 10 [enhancement], 11 [sanctum], 12 [allies], 13 [chantry], 14 specialties | 5 |
| `mage` | `mage.mage` | 1-3, 4 spheres, 5 focus, 6 biography, 7 freebies*, 8 languages*, 9 rote*, 10 [node], 11 [library], 12 [familiar], 13 [wonder], 14 [enhancement], 15 [sanctum], 16 [allies], 17 [mentor], 18 [contacts], 19 [retainers], 20 [chantry], 21 specialties | 7 |
| `sorcerer` | `mage.sorcerer` | 1-3, 4 psychic*, 5 path*, 6 ritual*, 7 biography, 8 freebies*, 9 languages*, 10 [node], 11 [library], 12 [familiar], 13 [artifact], 14 [enhancement], 15 [sanctum], 16 [allies], 17 [chantry], 18 specialties | 8 |
| `ctd_human`, `wto_human`, `dtf_human` | `changeling.ctdhuman`, `wraith.wtohuman`, `demon.dtfhuman_chargen` | as `vtm_human` | 5 |
| `changeling` | `changeling.changeling` | 1-3, 4 arts_realms, 5 biography, 6 freebies*, 7 languages*, 8 [allies], 9 specialties | 6 |
| `wraith` | `wraith.wraith_chargen` | 1-3, 4 arcanos, 5 shadow, 6 passions*, 7 fetters*, 8 biography, 9 freebies*, 10 languages*, 11 [allies], 12 [mentor], 13 [contacts], 14 specialties | 9 |
| `demon` | `demon.demon_chargen` | 1-3, 4 lores, 5 apocalyptic_form, 6 virtues, 7 biography, 8 freebies*, 9 languages*, 10 [allies], 11 [mentor], 12 [contacts], 13 [retainers], 14 [followers], 15 specialties | 8 |
| `thrall` | `demon.thrall_chargen` | 1-3, 4 virtues, 5 biography, 6 freebies*, 7 languages*, 8 [allies], 9 specialties | 6 |

"1-3" is attributes, abilities, backgrounds. Only `vampire` is interactive (htmx).

Types without a workflow (`autumn_person`, `inanimae`, `nunnehi`, `earthbound`,
`htr_human`, `hunter`, `mtr_human`, `mummy`, `revenant`) are built with plain create and
update forms. `DETAIL_ONLY_FREEBIE_POSITIONS` still gives them a `freebie_step` (5, 6 or 7)
so `CharacterQuerySet.at_freebie_step()` and the storyteller's freebie queue work for them.
`spirit_character` and the base `character` have neither (`freebie_step == -1`).

## Point values

Attribute and Ability steps read `primary`, `secondary` and `tertiary` from the step view
class and pass them to `attribute_rule()` / `ability_rule()`
([`rules/limits.py`](../rules/limits.py)):

| Types | Attributes | Abilities |
|-------|-----------|-----------|
| `human` | 7 / 5 / 3 | 11 / 7 / 4 |
| `vampire`, `werewolf`, `fera`, `mage`, `changeling`, `wraith`, `demon`, `thrall`, `dtf_human` | 7 / 5 / 3 | 13 / 9 / 5 |
| `vtm_human`, `ghoul`, `wta_human`, `kinfolk`, `fomor`, `drone`, `mta_human`, `companion`, `sorcerer`, `ctd_human`, `wto_human` | 6 / 4 / 3 | 11 / 7 / 4 |

Attributes start at one dot (so a group of three totals `3 + points`); chargen Abilities
are capped at 3 (`CHARGEN_ABILITY_MAXIMUM`). Backgrounds must spend exactly
`background_points` (default 5; Mage and Wraith 7, Fomor 3, Drone 2), each dot costing the
Background's `multiplier`.

## Gameline steps

| Step | Views | What it enforces or writes |
|------|-------|-----------------------------|
| Vampire `disciplines` | `VampireDisciplinesView`, `GhoulDisciplinesView` | `VAMPIRE_DISCIPLINES` restricted to clan Disciplines (3 dots); `GHOUL_DISCIPLINES` (up to 2 more dots, Potence fixed) |
| Vampire `virtues` | `VampireVirtuesView` | `vampire_virtue_rule()` over the active virtues (7 dots); then `Vampire.apply_starting_virtues()` |
| Werewolf `gifts`, `history` | `WerewolfGiftsView`, `WerewolfHistoryView` | `WerewolfGiftsForm` (breed, auspice and tribe Gift); `WerewolfHistoryForm` |
| Fera `breed_faction`, `gifts`, `history` | `FeraBreedFactionView`, `FeraGiftsView`, `FeraHistoryView` | Breed class declarations (`chargen_choice_fields`, `gift_group_fields`; see [Werewolf models](models-werewolf.md#fera-changing-breeds)) |
| Fomor `powers` | `FomorPowersView` | Fomori powers |
| Mage `spheres` | `MageSpheresView` | `MageSpheresForm`; `Mage.purchase_starting_arete()` charges freebies for Arete above 1 |
| Mage `focus` | `MageFocusView` | `MageFocusForm` and the practice formset, saved by `services.mage_chargen.set_starting_practices()` |
| Mage `rote` | `MageRoteView` | `RoteCreationForm`, `services.rotes.learn_rote()`; skipped when `rote_points == 0` |
| Sorcerer `psychic` / `path` / `ritual` | `SorcererPsychicView`, `SorcererPathView`, `SorcererRitualView` | Numina formsets (paths total five levels), saved by `services.sorcerer_chargen.set_starting_numina()`, which also sets Willpower 5 and freebies 21; `NuminaRitualForm` for rituals |
| Changeling `arts_realms` | `ChangelingArtsRealmsView` | `CHANGELING_ARTS` (3) and `CHANGELING_REALMS` (5) |
| Wraith `arcanos`, `shadow`, `passions`, `fetters` | `WraithArcanosView`, `WraithShadowView`, `WraithPassionsView`, `WraithFettersView` | `WRAITH_ARCANOI` (5); Shadow archetype; Passions and Fetters until their totals reach 10 each |
| Demon `lores`, `apocalyptic_form`, `virtues` | `DemonLoresView`, `DemonApocalypticFormView`, `DemonVirtuesView` (Thrall: `ThrallVirtuesView`) | `DEMON_LORES` (3); `ApocalypticFormSelectionForm` and `services.demon_chargen.apply_apocalyptic_form()`; `FALLEN_VIRTUES` (6) |
| Background-detail steps | `...AlliesView`, `...MentorView`, `...NodeView`, ... | `GenericBackgroundView` with `LinkedNPCForm` or a location/item form |

The workflow binds each step to `<module>.<Prefix><Step>View` unless `definitions.py`
overrides it (only the `human` workflow does, to the `...ChargenView` classes).

## Templates per step

Each `Step` carries its body template. Defaults: `characters/core/chargen/form.html`;
Attributes `characters/core/attribute_block/form.html`; Abilities
`characters/core/chargen/abilities.html`; Backgrounds
`characters/core/background_block/form.html`; Freebies `characters/core/chargen/freebies.html`;
Languages `characters/core/human/human_language_block_form.html`; Specialties
`characters/core/chargen/specialties.html`. `bind(..., templates=...)` overrides them per
workflow, for example the gameline `ability_block_form.html` partials, the Vampire
`steps/disciplines.html` and `steps/virtues.html`, `chargen/freebies_chained.html` for the
Vampire freebies, and `locations/mage/node/form_include.html` for the Node step.

`ChargenStepMixin.get_template_names()` uses the view's `template_name` only when it ends
in `/chargen.html`; anything else falls back to `characters/core/chargen.html`. Gameline
step views point at their gameline shell (`characters/<gameline>/<type>/chargen.html`), and
every shell extends `characters/core/chargen.html` without changes, so the shells exist
only as override slots.

## Adding a character type to chargen

1. Write the step views in the type's views module, following an existing workflow.
2. Add a `bind(...)` workflow in `definitions.py` and register it in `WORKFLOWS` under
   the model's `type`.
3. Point the type's router (`<Type>CharacterCreationView` with
   `view_mapping = WorkflowViews()`) at it and add the type to
   `GenericCharacterDetailView.view_mapping`.
4. List every step view under `CHARGEN_STEP` in
   [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py).
5. Register freebie and XP services for the type (see [Services](services.md)).

The full recipe is in [Adding a character type](../../docs/guides/adding-a-character-type.md).
Reordering an existing workflow changes the meaning of saved `creation_status` values; it
needs a data migration for unfinished characters.

## See also

- [Character creation](../../docs/architecture/character-creation.md)
- [Adding a chargen step](../../docs/guides/adding-a-chargen-step.md)
- [Costs and rules](costs-and-rules.md)
- [Services](services.md)
- [Templates](templates.md)
