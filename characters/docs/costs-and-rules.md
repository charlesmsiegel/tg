# Costs and rules

This page is the reference for the game-rule data in the `characters` app: the freebie and
XP cost tables in [`characters/costs.py`](../costs.py), and the chargen allocation rules and
point pools in [`characters/rules/`](../rules/). It is for developers changing a price or a
starting pool. How the rules run inside a chargen step (phases, PRI / SEC / TER ranking,
client hints) is explained in
[Character creation](../../docs/architecture/character-creation.md#allocation-rules).

## Costs (`characters/costs.py`)

Two dictionaries and four lookup functions. Keys are lower-case trait types; the lookups
lower-case their argument and replace spaces with underscores, so `"Path Rating"` finds
`path_rating`.

| Function | Returns |
|----------|---------|
| `get_freebie_cost(trait_type)` | The flat `FREEBIE_COSTS` value, `"rating"` for `meritflaw`, or `10000` for an unknown key |
| `get_xp_cost(trait_type)` | The `XP_COSTS` multiplier (or flat cost for `new_*` keys), or `10000` for an unknown key |
| `get_meritflaw_freebie_cost(rating)` | `abs(rating)` |
| `get_meritflaw_xp_cost(current_rating, new_rating)` | `3 * abs(new_rating - current_rating)` |

`10000` is a sentinel: callers treat it as "not priced here". `HumanFreebiesForm.validator()`
keeps a category it cannot price so gameline forms can handle it, and
`forms.core.xp._calculate_xp_cost()` uses it to detect that no `new_<trait>` cost exists.
A misspelt key therefore shows up as an unaffordable spend rather than an error.

### Freebie costs (flat per dot)

| Group | Costs |
|-------|-------|
| Universal | attribute 5, ability 2, background 1 (times the Background's `multiplier`), willpower 1, meritflaw = rating |
| Mage | sphere 7, arete 4, quintessence 0.25, resonance 3, tenet 0, practice 1, rotes 1 |
| Sorcerer | path 7, ritual 3 |
| Vampire | discipline 7, virtue 2, humanity 2, path_rating 2 |
| Werewolf | gift 7, rite 1, rage 1, gnosis 2, glory 1, honor 1, wisdom 1 |
| Wraith | arcanos 5, pathos 0.5, passion 2, fetter 1, wraith_willpower 2 (Corpus has no freebie cost) |
| Changeling | art 5, realm 2, glamour 3, banality 2 |
| Demon | lore 7, faith 6, temporary_faith 1; Thrall faith_potential 7 |
| Hunter | edge 7, conviction 1 |
| Mummy | hekau 5, sekhem 1, balance 4, ba 1, mummy_ritual 1, mummy_spell 1 |

### XP costs

Most values are multipliers of the current rating; `new_*` keys are flat costs for the
first dot.

| Group | Costs |
|-------|-------|
| Universal | attribute ×4, ability ×2 (new 3), background ×3 (new 5), willpower ×1, meritflaw 3 per point of change |
| Mage | sphere ×8, affinity_sphere ×7, new_sphere 10, arete ×8, resonance ×3 (new 5), practice ×1 (new 3), rotes 1, tenet 0 |
| Sorcerer | path ×7 (new 10), ritual 2 per level |
| Vampire | discipline ×5 (in clan), out_of_clan_discipline ×7, caitiff_discipline ×6, new_discipline 10, secondary_path ×4 (new 7), virtue ×2, humanity ×2, path_rating ×2 |
| Werewolf | gift ×3 per level (other_gift ×5), rite ×1, rage ×1, gnosis ×2, glory / honor / wisdom ×1 |
| Wraith | arcanos ×3 (new 7), pathos ×2, corpus ×1, angst ×1 |
| Changeling | art ×4 (new 7), realm ×3 (new 5), glamour ×3, banality 2 per point, changeling_willpower ×2 |
| Demon | lore ×5 (other_lore ×7; new 7, new_other_lore 10), faith ×7, reduce_torment 10 per point; Thrall faith_potential ×10 |
| Mummy | hekau ×5, favored_hekau ×4, other_hekau ×6, udjasen_hekau ×5, new_hekau 7, sekhem ×10, balance ×7, mummy_new_spell / mummy_new_ritual 1 per level |
| Companion | advantage 3 per point of change, charm 5 |

The spending services apply the modifiers (new trait, affinity Sphere, in-clan
Discipline, Background multiplier); see [Services](services.md). The "Sphere Natural" and
"Sphere Inept" merit adjustments exist only in the legacy `Mage.spend_xp()` hook.
Some code prices without these tables: the legacy model hooks (for example
`Vampire.discipline_freebies()` charges 7 or 10, `Ghoul.discipline_freebies()` 7,
`Hunter.spend_freebies()` 7 per Edge) and the Mage Arete purchase on the Spheres step,
which uses `Human.freebie_spend_record()` and so `get_freebie_cost("arete")`.

## Allocation rules (`characters/rules/allocation.py`)

Pure, frozen dataclasses that never touch the database, so forms, views and the browser
share them:

| Type | Purpose | Key attributes |
|------|---------|----------------|
| `RuleViolation` | One broken rule | `message`, `field`, `flash` |
| `AllocationRule` | Named fields that sum to exactly (`comparison="exact"`) or at most (`"at_most"`) `total` | `name`, `fields`, `total`, `message`, `flash`, `maximum` (per trait), `allowed` (traits that may be above zero) and their messages |
| `PriorityRule` | Three groups ranked primary / secondary / tertiary | `groups`, `points`, `base` (free dots per field), `minimum`, `maximum`, `range_fields`, messages; `priority_field(group)` names the posted rank (`priority_<group>`) |

Each rule implements `violations(values, phase)` for the phases `totals`, `bounds` and
`choices`, plus `satisfied()`, `status()` (running totals for display) and
`client_data()` (JSON-safe limits). `first_violation(rules, values)` returns the earliest
violation by phase, then rule order; that is the single error a step shows.

## Pools and limits (`characters/rules/limits.py`)

| Name | Rule |
|------|------|
| `attribute_rule(primary, secondary, tertiary)` | `PriorityRule` over `ATTRIBUTE_GROUPS` (physical, social, mental), `base=1`, range 1 to 5 |
| `ability_rule(model, form_fields, primary, secondary, tertiary, range_flash=None, flash=None)` | `PriorityRule` over talents, skills, knowledges, counting only the fields the form offers (so Mage secondary abilities are ignored), range 0 to `CHARGEN_ABILITY_MAXIMUM` (3) over `model.primary_abilities` |
| `VAMPIRE_DISCIPLINES` | 25 Discipline fields, exactly 3 dots; views restrict `allowed` to the clan's Disciplines with `dataclasses.replace` |
| `GHOUL_DISCIPLINES`, `GHOUL_FIXED_DISCIPLINES` | Up to 2 dots among Celerity, Fortitude, Auspex, Dominate, Obfuscate, Presence; Potence is the fixed first dot and not in the pool |
| `VAMPIRE_VIRTUES`, `vampire_virtue_rule(vampire)` | Exactly 7 dots over the vampire's active virtues (`active_virtue_fields()`) |
| `CHANGELING_ARTS`, `CHANGELING_REALMS` | Exactly 3 Art dots and 5 Realm dots, each at most 5 |
| `WRAITH_ARCANOI` | Exactly 5 dots over the standard Arcanoi, each at most 5 |
| `DEMON_LORES` | Exactly 3 dots over the 23 Lores |
| `FALLEN_VIRTUES` | Conviction, Courage and Conscience total exactly 6 (Demon and Thrall) |
| `KINFOLK_TRIBE_BACKGROUND_LIMITS` | Per tribe: `forbidden`, `max` and `required` backgrounds, used by `Kinfolk.background_violations()` and `Kinfolk.add_background()` |
| `APOCALYPTIC_FORM_TRAITS_PER_STATE`, `APOCALYPTIC_FORM_POINT_BUDGET` | 4 traits per Torment state, 16 points |

Per-type Attribute and Ability points are not in this module: they are the `primary`,
`secondary` and `tertiary` attributes of each step view (table in
[Chargen](chargen.md#point-values)).

## Rules that live on models

Some limits are enforced by model methods rather than the rule objects: trait maximums in
`add_*` helpers (`Human.add_ability` caps at 4, `Mage.add_ability` at 5,
`Vampire.get_trait_max()` by generation), `Mage.clean()` (Spheres at most Arete),
`Vampire.clean()` (starting Humanity or Path at least 4), `Werewolf.clean()` (Gnosis and
Rage at least 1), `Wraith.clean()` (Angst at least 1), and the database `CheckConstraint`s
listed on the model pages. See [Character models](models.md).

## See also

- [Character creation](../../docs/architecture/character-creation.md)
- [Chargen](chargen.md)
- [Services](services.md)
- [Forms](forms.md)
