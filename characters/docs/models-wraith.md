# Wraith: the Oblivion models

This page is the reference for the Wraith character types in
[`characters/models/wraith/`](../models/wraith/): `WtOHuman`, `Wraith`, the per-wraith
`Passion`, `Fetter` and `ThornRating` rows, and the `Circle` group. The Wraith catalogues
(Arcanoi, Guilds, factions, Shadow archetypes, Thorns) are described in
[Reference data](reference-data.md#wraith). Read [Character models](models.md) first for
the `Human` base. Terms such as Corpus, Pathos, Angst, Shadow and Harrowing are in the
[glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `WtOHuman` | `Human` | `wto_human` | `wto_human` (8 steps) | `characters:character` |
| `Wraith` | `WtOHuman` | `wraith` | `wraith` (14 steps) | `characters:wraith:wraith` |
| `Circle` | `Group` | `circle` | n/a | `characters:group` |

`gameline = "wto"` (URL namespace `characters:wraith:`).

## WtOHuman

[`wtohuman.py`](../models/wraith/wtohuman.py). Extra ability columns (all primary):
talents `awareness`, `persuasion`; skills `larceny`, `leadership`, `meditation`,
`performance`; knowledges `bureaucracy`, `enigmas`, `occult`, `politics`, `technology`.
`allowed_backgrounds`: `contacts`, `mentor`, `allies`, `artifact`, `eidolon`, `haunt`,
`legacy`, `memoriam`, `notoriety`, `relic`, `status_background`.

## Wraith

[`wraith.py`](../models/wraith/wraith.py).

### Fields

| Group | Fields |
|-------|--------|
| Affiliation | `guild` (`ForeignKey(Guild)`, reverse `members`), `legion` (`ForeignKey(WraithFaction)`, reverse `legion_members`), `faction` (`ForeignKey(WraithFaction)`, reverse `faction_members`); all nullable, `SET_NULL` |
| Core traits | `corpus` (default `10`); `pathos` / `temporary_pathos` (default `5`) and `angst` / `temporary_angst` (default `1`, permanent minimum 1) from `core.linked_stat.linked_stat_fields` with `cap_temporary=False` (descriptors `pathos_stat`, `angst_stat`) |
| Arcanoi | Standard: `argos`, `castigate`, `embody`, `fatalism`, `flux`, `inhabit`, `keening`, `lifeweb`, `moliate`, `mnemosynis`, `outrage`, `pandemonium`, `phantasm`, `usury`, `intimation`. Dark: `blighted_insight`, `collogue`, `corruptor`, `false_life`, `tempestos`, `osseum`, `connaissance`. All default `0` |
| Shadow | `shadow_archetype` (`ForeignKey(ShadowArchetype)`, reverse `wraiths`), `thorns` (through `ThornRating`) |
| State | `character_type` (`wraith`, `spectre`, `doppelganger`, `chosen`, `dark_spirit`, `risen`), `in_catharsis`, `catharsis_count`, `harrowing_count`, `last_harrowing_result` (`none`, `success`, `failure`, `catharsis`), `is_shadow_dominant`, `spectrehood_date`, `redemption_attempts` |
| Story | `death_description`, `age_at_death` |

Class attributes: `background_points = 7`, `passion_points = 10`, `fetter_points = 10`.

### Behaviour

- `clean()` rejects permanent Angst below 1 ("All wraiths have a Shadow").
- `set_guild()` also sets Willpower from `Guild.willpower`.
- `get_arcanoi()` returns only the standard Arcanoi and `get_dark_arcanoi()` the dark ones;
  `has_arcanoi()` requires exactly 5 standard dots. `add_arcanos()` caps at 5.
  `get_arcanoi_ratings()` / `get_dark_arcanoi_ratings()` return `(label, rating)` pairs for
  the sheet.
- `add_passion()`, `add_fetter()` create rows; `has_passions()` and `has_fetters()`
  require their totals to equal `passion_points` / `fetter_points`. These two checks are
  also the skip predicates for the Passions and Fetters chargen steps
  (`completed_passions`, `completed_fetters` in
  [`chargen/predicates.py`](../chargen/predicates.py)).
- `add_thorn()` creates or raises a `ThornRating` to 1; `get_thorn_ratings()` lists rated
  Thorns.
- Shadow mechanics: `check_catharsis_trigger()` (temporary Angst above Willpower),
  `trigger_catharsis()`, `resolve_catharsis(shadow_won)`; `check_harrowing_trigger()`,
  `trigger_harrowing()`, `resolve_harrowing(result)` (`failure` calls `become_spectre()`,
  `catharsis` lowers Angst). `become_spectre()` sets `character_type = "spectre"`, stamps
  `spectrehood_date` and turns every Passion dark. `attempt_redemption()` and
  `complete_redemption(psyche_successes, shadow_successes)` reverse it; a successful
  redemption lowers permanent Angst by the margin, but never below 1.
  `get_catharsis_info()` and `get_harrowing_info()` summarise the state.
- Legacy spend hooks: `spend_freebies()`, `arcanos_freebies()`,
  `pathos_freebies()`, `passion_freebies()`, `fetter_freebies()`, `corpus_freebies()`.

### Per-wraith rows

| Model | Fields | Notes |
|-------|--------|-------|
| `Passion` ([`passion.py`](../models/wraith/passion.py)) | `wraith` (`ForeignKey(Wraith, CASCADE)`, reverse `passions`), `emotion`, `description`, `rating` (default `1`), `is_dark_passion` | Plain `models.Model` |
| `Fetter` ([`fetter.py`](../models/wraith/fetter.py)) | `wraith` (`CASCADE`, reverse `fetters`), `fetter_type` (`object`, `location`, `person`), `description`, `rating` (default `1`) | Plain `models.Model` |
| `ThornRating` | `wraith` (reverse `thorn_ratings`), `thorn` (reverse `wraith_ratings`), `rating` | Constraint `characters_wraith_thornrating_rating_range` |

`Passion` and `Fetter` rows are deleted with their wraith; everything else in the app uses
`SET_NULL`.

## Circle

[`circle.py`](../models/wraith/circle.py). A `Group` with no extra fields. It keeps
`Group.get_absolute_url()` (`characters:group`); a `CircleDetailView` route
`characters:wraith:circle` also exists, and create, update and list routes are under
`characters:wraith:`.

## See also

- [Character models](models.md)
- [Reference data: Wraith](reference-data.md#wraith)
- [Chargen](chargen.md)
- [Views and URLs](views-and-urls.md#wraith)
