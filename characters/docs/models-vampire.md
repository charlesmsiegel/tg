# Vampire: the Masquerade models

This page is the reference for the Vampire character types in
[`characters/models/vampire/`](../models/vampire/): `VtMHuman`, `Vampire`, `Ghoul`,
`Revenant` and the `Coterie` group. The Vampire reference catalogues (clans, Disciplines,
Paths, sects, titles, Revenant families) are described in
[Reference data](reference-data.md#vampire). Read [Character models](models.md) first for the
`Human` base these types extend. Terms such as Discipline, generation and Path of
Enlightenment are in the [glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `VtMHuman` | `Human` | `vtm_human` | `vtm_human` (8 steps) | `characters:character` |
| `Vampire` | `VtMHuman` | `vampire` | `vampire` (13 steps, interactive) | `characters:vampire:vampire` |
| `Ghoul` | `VtMHuman` | `ghoul` | `ghoul` (9 steps) | `characters:vampire:ghoul` |
| `Revenant` | `VtMHuman` | `revenant` | none (freebie position 6 from `DETAIL_ONLY_FREEBIE_POSITIONS`) | `characters:vampire:revenant` |
| `Coterie` | `Group` | `coterie` | n/a | `characters:vampire:coterie` |

All have `gameline = "vtm"`, so their URLs live in the `characters:vampire:` namespace
(see [Views and URLs](views-and-urls.md#vampire)). Workflows are listed step by step in
[Chargen](chargen.md#workflows-by-type).

## VtMHuman

[`vtmhuman.py`](../models/vampire/vtmhuman.py). The mortal base of the gameline.

- Extra ability columns (`IntegerField`, default `0`): talents `awareness`, `leadership`;
  skills `animal_ken`, `larceny`, `performance`, `survival`; knowledges `finance`, `law`,
  `occult`, `politics`, `technology`. All are in `primary_abilities`.
- `allowed_backgrounds`: `contacts`, `mentor`, `allies`, `alternate_identity`,
  `black_hand_membership`, `domain`, `fame`, `generation`, `herd`, `influence`,
  `resources`, `retainers`, `rituals`, `status_background`.
- Background columns: `allies`, `alternate_identity`, `black_hand_membership`, `domain`,
  `fame`, `generation`, `herd`, `influence`, `resources`, `retainers`, `rituals`,
  `status_background` are real `IntegerField`s. Attribute access on these names reads the
  column, not the `BackgroundRating` rows (see
  [Dynamic background properties](models.md#dynamic-background-properties)).

## Vampire

[`vampire.py`](../models/vampire/vampire.py).

### Fields

| Group | Fields |
|-------|--------|
| Affiliation | `clan` (`ForeignKey(VampireClan)`, reverse `vampires`), `sect` (`ForeignKey(VampireSect)`, reverse `vampires`), `sire` (`ForeignKey("self")`, reverse `childer`), `titles` (`ManyToManyField(VampireTitle)`, reverse `holders`). All foreign keys are nullable with `SET_NULL` |
| Generation and blood | `generation_rating` (default `13`), `blood_pool` / `max_blood_pool` (default `10`), `blood_per_turn` (default `1`); `blood` is a `core.linked_stat.LinkedStat` over the pool pair with `cap_temporary=False` |
| Disciplines | 25 `IntegerField`s, default `0`: `celerity`, `fortitude`, `potence`, `auspex`, `dominate`, `dementation`, `presence`, `animalism`, `protean`, `obfuscate`, `chimerstry`, `necromancy`, `obtenebration`, `quietus`, `serpentis`, `thaumaturgy`, `vicissitude`, `daimoinon`, `melpominee`, `mytherceria`, `obeah`, `temporis`, `thanatosis`, `valeren`, `visceratika` |
| Virtues | `has_conviction`, `has_instinct` (booleans selecting the Sabbat virtues), `conscience`, `self_control`, `courage`, `conviction`, `instinct` (default `1`) |
| Morality | `humanity` (default `7`), `path` (`ForeignKey(Path)`, reverse `followers`), `path_rating` (default `0`) |

Database constraints: `conscience`, `self_control`, `conviction`, `instinct` 0 to 5;
`courage` 1 to 5; `humanity` and `path_rating` 0 to 10.

### Generation

`GENERATION_TABLE` maps generations 3 to 15 to `(max_trait, max_blood_pool,
blood_per_turn)`. `save()` calls `update_generation_values()`, which copies the pool size
and per-turn rate from the table, so edit `generation_rating` rather than the pool fields.
`get_trait_max()` returns the table's trait maximum (5 for unknown generations);
`get_attribute_max()` and `get_discipline_max()` both return it.
`get_attribute_min("appearance")` returns `0` for clan Nosferatu.

`spend_blood(amount)` raises `ValueError` above `blood_per_turn`, returns `False` when the
pool is short, else deducts and saves. `restore_blood(amount)` caps at `max_blood_pool` and
returns the amount restored. `validate_blood_pool()` returns an error dict.

### Virtues and Path

A vampire rates either Conscience or Conviction and either Self-Control or Instinct, plus
Courage. The `has_conviction` / `has_instinct` flags choose, and helpers read the active
pair: `active_virtue_1`, `active_virtue_2` (and `*_name`), `active_virtue_fields()`,
`get_active_virtues()`, `set_virtue_by_name()`.

- `save()` calls `path.update_character_virtues(self)` when a Path is set, which flips the
  flags to the Path's `requires_conviction` / `requires_instinct` and zeroes the virtue
  being switched away from.
- `apply_starting_virtues()` sets Willpower to Courage and sets either `humanity` or
  `path_rating` (with Path) to the sum of the two active virtues, zeroing the other.
- `clean()` requires the active virtues and Courage to be at least 1. While the status is
  `Un` or `Sub`, it also requires starting Humanity (no Path) or Path rating (with Path)
  of at least 4 (`MIN_STARTING_HUMANITY`, `MIN_STARTING_PATH_RATING`) and at most 10.

### Disciplines

`get_disciplines()` returns `{name: rating}` for Disciplines above zero.
`get_clan_disciplines()` lists the clan's `Discipline` rows; `is_clan_discipline()` accepts
a property name or a `Discipline`. In-clan and out-of-clan costs differ; see
[Costs and rules](costs-and-rules.md).

### Legacy spending hooks

`spend_xp(trait)` and `spend_freebies(trait)` extend the `Human` versions with Disciplines
(capped by `get_discipline_max()`), virtues (cap 5), `humanity` and `path_rating`
(cap 10). `discipline_freebies()`, `virtue_freebies()`, `humanity_freebies()` and
`path_rating_freebies()` are the per-category form hooks. `xp_frequencies()` and
`freebie_frequencies()` return category weightings; application code does not call them.
The request-and-approval flow uses the [spending services](services.md) instead.

## Ghoul

[`ghoul.py`](../models/vampire/ghoul.py).

| Field | Notes |
|-------|-------|
| `domitor` | `ForeignKey(Vampire, SET_NULL)`, nullable, reverse `ghouls` |
| `is_independent` | Boolean |
| `blood_pool` / `max_blood_pool` | Defaults `0` / `2`; `blood` linked stat |
| `potence` (default `1`), `celerity`, `fortitude`, `auspex`, `dominate`, `obfuscate`, `presence` | Discipline ratings |
| `years_as_ghoul` | Integer |
| `conscience`, `self_control`, `courage` | Default `1` |

`allowed_backgrounds`: `contacts`, `mentor`, `allies`, `alternate_identity`, `resources`,
`retainers`, `status_background`. `get_available_disciplines()` returns the domitor's clan
Disciplines, or Potence, Celerity and Fortitude when there is no domitor clan.
`discipline_freebies()` charges a flat 7.

## Revenant

[`revenant.py`](../models/vampire/revenant.py).

| Field | Notes |
|-------|-------|
| `family` | `ForeignKey(RevenantFamily, SET_NULL)`, nullable, reverse `revenants` |
| `blood_pool` / `max_blood_pool` | Default `10`; `blood` linked stat |
| `pseudo_generation` | Default `10` |
| `potence`, `celerity`, `fortitude`, `auspex`, `dominate`, `obfuscate`, `presence`, `animalism`, `necromancy`, `vicissitude` | Discipline ratings, default `0` |
| `family_flaw` | Text |
| `actual_age` | Integer |

`allowed_backgrounds` adds `generation` to the Ghoul list. `get_family_disciplines()` and
`get_available_disciplines()` read the family's Disciplines (physical Disciplines without
a family). Revenants have no chargen workflow; they are created and edited through
`RevenantCreateView` / `RevenantUpdateView`.

## Coterie

[`coterie.py`](../models/vampire/coterie.py). A `Group` with no extra fields
(`gameline = "vtm"`). URL names `characters:vampire:coterie`,
`characters:vampire:create:coterie`, `characters:vampire:update:coterie`,
`characters:vampire:list:coterie`.

## See also

- [Character models](models.md)
- [Reference data: Vampire](reference-data.md#vampire)
- [Costs and rules](costs-and-rules.md)
- [Services](services.md)
- [Views and URLs](views-and-urls.md#vampire)
