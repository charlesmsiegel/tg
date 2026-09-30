# Demon: the Fallen models

This page is the reference for the Demon character types in
[`characters/models/demon/`](../models/demon/): `DtFHuman`, `Demon`, `Earthbound`,
`Thrall`, the `LoreBlock` mixin, the per-character `ApocalypticForm`, `Pact` and
`LoreRating` rows, and the `Conclave` group. The Demon catalogues (houses, factions,
Lores, visages, apocalyptic form traits, rituals) are described in
[Reference data](reference-data.md#demon). Read [Character models](models.md) first for
the `Human` base. Terms such as Faith, Torment, Lore and Thrall are in the
[glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `DtFHuman` | `Human` | `dtf_human` | `dtf_human` (8 steps) | `characters:demon:dtfhuman` |
| `Demon` | `LoreBlock`, `DtFHuman` | `demon` | `demon` (15 steps) | `characters:demon:demon` |
| `Thrall` | `DtFHuman` | `thrall` | `thrall` (9 steps) | `characters:demon:thrall` |
| `Earthbound` | `LoreBlock`, `DtFHuman` | `earthbound` | none (freebie position 7) | `characters:demon:earthbound` |
| `Conclave` | `Group` | `conclave` | n/a | `characters:group` (a `characters:demon:conclave` route also exists) |

`gameline = "dtf"` (URL namespace `characters:demon:`). `DtFHuman` defines its own URL
methods with the route names `dtfhuman` (no underscore). `Earthbound` overrides
them with its own routes, `characters:demon:update:earthbound` and
`characters:demon:create:earthbound` (see [Views and URLs](views-and-urls.md#demon)).

## DtFHuman

[`dtf_human.py`](../models/demon/dtf_human.py). Extra ability columns (all primary):
talents `awareness`, `intuition`, `leadership`, `seduction`; skills `performance`,
`security`, `survival`, `technology`, `animal_ken`, `demolitions`; knowledges `finance`,
`law`, `enigmas`, `occult`, `politics`, `religion`, `research`. `allowed_backgrounds`:
`contacts`, `mentor`, `allies`, `eminence`, `fame`, `followers`, `influence`, `legacy`,
`pacts`, `paragon`, `resources`. `Thrall` uses the same list.

## LoreBlock

[`lore_block.py`](../models/demon/lore_block.py). An abstract mixin with the 23 Lores as
`IntegerField`s named `lore_of_<name>` (`lore_of_awakening`, `lore_of_the_beast`, ...,
`lore_of_the_winds`), default `0`. Methods: `get_lores()`, `total_lores()`,
`add_lore(name, maximum=5)`, `filter_lores()`, `lore_label(field)` and `lore_rows()`
(sheet rows, linked to the matching `Lore` records by `property_name`).

## Demon

[`demon.py`](../models/demon/demon.py).

| Group | Fields |
|-------|--------|
| Affiliation | `house` (`ForeignKey(DemonHouse)`, reverse `demons`), `faction` (`ForeignKey(DemonFaction)`, reverse `members`), `visage` (`ForeignKey(Visage)`, reverse `demons`), `apocalyptic_form` (`ForeignKey(ApocalypticForm)`, reverse `demons`); all nullable, `SET_NULL` |
| Faith and Torment | `faith` / `temporary_faith` (default `3`), `torment` / `temporary_torment` (defaults `3` / `0`) from `core.linked_stat.linked_stat_fields` |
| Virtues | `conviction`, `courage`, `conscience` (default `1`) |
| Story | `celestial_name`, `age_of_fall`, `abyss_duration`, `days_until_consumption` (default `30`) |
| Relations | `thralls` (`ManyToManyField(Thrall)` through `Pact`, reverse `masters`), `rituals` (`ManyToManyField(Ritual)`, reverse `demons_who_know`) |

`allowed_backgrounds` adds `alternate_identity`, `cult`, `retainers`, `ritual_knowledge`
and `status_background` to the `DtFHuman` list.

Behaviour:

- `has_lores()` needs at least 3 Lore dots. `set_house()` sets Torment to the house's
  `starting_torment`. `add_torment()` / `reduce_torment()` stay within 0 to 10.
- `has_virtues()` requires each virtue at least 1 and a total of 6.
- `has_apocalyptic_form()` requires a linked form that passes `ApocalypticForm.is_valid()`;
  `get_low_torment_traits()`, `get_high_torment_traits()` and the
  `apocalyptic_form_*` counters delegate to it.
- `ritual_knowledge_xp_cost()` returns 6 per dot of the `ritual_knowledge` background.
  `get_rituals()`, `knows_ritual()`, `add_ritual()`, `remove_ritual()`,
  `get_available_rituals()` manage known rituals.
- `add_pact(thrall, terms="", faith_payment=0, enhancements=None)` creates a `Pact`;
  `get_pacts()` and `total_pacts()` read them.
- Legacy spend hooks: `lore_freebies()`, `faith_freebies()`, `virtue_freebies()`,
  `temporary_faith_freebies()`, `spend_freebies()`.

`LoreRating` (`demon`, `lore`, `rating`; constraint
`characters_demon_lorerating_rating_range`, 0 to 10) is defined in the same module and
registered in the admin, but the Lore ratings a Demon uses are the `LoreBlock` columns.

## ApocalypticForm

[`apocalyptic_form.py`](../models/demon/apocalyptic_form.py). A `core.models.Model` that
holds one configured form: `low_torment_traits` and `high_torment_traits`
(`ManyToManyField(ApocalypticFormTrait)`). A form is valid with exactly four low-Torment
and four high-Torment traits costing at most 16 points in total
(`is_valid()`, `is_complete()`, `points_remaining()`). `can_add_low_torment_trait()`
rejects `high_torment_only` traits; neither list may repeat a trait or share one with the
other list. `add_*`, `remove_*` and `copy_from()` edit it. It has no routes and no URL methods;
forms are edited through the Demon chargen step and the Demon forms.

## Thrall

[`thrall.py`](../models/demon/thrall.py). Fields: `faith_potential` and
`daily_faith_offered` (default `1`), `master` (`ForeignKey(Demon, SET_NULL)`, reverse
`primary_thralls`), `enhancements` (`JSONField(list)`), `conviction`, `courage`,
`conscience`. `calculate_daily_faith()` sets and returns half the Faith Potential rounded
up; `has_virtues()` matches the Demon rule; `get_pacts()`, `get_active_pacts()`,
`total_pacts()`, `add_enhancement()`, `remove_enhancement()`.

## Pact

[`pact.py`](../models/demon/pact.py). The through model between `Demon` and `Thrall`:
`demon` and `thrall` (`CASCADE`), `terms`, `faith_payment`, `enhancements`
(`JSONField(list)`), `active` (default `True`). A pact is visible only to users who may
fully view its demon or its thrall (`characters.views.demon.pact.user_can_view_pact`).

## Earthbound

[`earthbound.py`](../models/demon/earthbound.py). An ancient demon bound to a reliquary.

| Group | Fields |
|-------|--------|
| Affiliation | `house` (reverse `earthbound`), `visage`, `apocalyptic_form` |
| Urges | `urge_flesh`, `urge_thought`, `urge_emotion` (default `1`) |
| Faith and Torment | `faith` / `temporary_faith` (defaults `3` / `10`), `torment` / `temporary_torment` (defaults `6` / `0`) |
| Virtues | `conviction`, `courage`, `conscience` |
| Reliquary | `reliquary_type` (`perfect`, `improvised`, `location`), `reliquary_description`, `reliquary_materials`, `reliquary_max_health` / `reliquary_current_health` (default `10`), `reliquary_soak`, `can_manifest`, `manifestation_range` |
| Cult and lore | `cult_size`, `worship_ritual_frequency`, `known_celestial_names`, `known_true_names` (JSON lists), `mastery_rating`, `indoctrination`, `recall`, `tactics`, `torture`, `rituals` (reverse `earthbound_who_know`) |
| Story | `celestial_name`, `date_summoned`, `time_in_stasis` |

`allowed_backgrounds`: `contacts`, `mentor`, `allies`, `influence`, `resources`,
`codex`, `cult`, `hoard`, `mastery`, `thralls`, `worship`. Methods:
`is_final_damnation()` (Torment 10), `get_faith_per_manifestation_turn()`,
`get_max_faith_from_hoard()` (10 + 5 per Hoard dot), `calculate_reliquary_health()`,
`can_regenerate_reliquary()`, and the same apocalyptic-form helpers as `Demon`.

## Conclave

[`conclave.py`](../models/demon/conclave.py). A `Group` with no extra fields; it keeps
`Group.get_absolute_url()`.

## See also

- [Character models](models.md)
- [Reference data: Demon](reference-data.md#demon)
- [Services](services.md) (`demon_chargen`)
- [Chargen](chargen.md)
- [Views and URLs](views-and-urls.md#demon)
