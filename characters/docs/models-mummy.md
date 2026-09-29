# Mummy: the Resurrection models

This page is the reference for the Mummy character types in
[`characters/models/mummy/`](../models/mummy/): `MtRHuman` and `Mummy` (one of the Amenti).
The Mummy catalogues (dynasties, mummy titles) are described in
[Reference data](reference-data.md#mummy). Read [Character models](models.md) first for
the `Human` base. Terms such as Sekhem, Ba, Ka and Hekau are in the
[glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `MtRHuman` | `Human` | `mtr_human` | none (freebie position 5) | `characters:mummy:mtrhuman` |
| `Mummy` | `MtRHuman` | `mummy` | none (freebie position 7) | `characters:mummy:mummy` |

`gameline = "mtr"` (URL namespace `characters:mummy:`). Both types override their URL
methods to use the route names `mtrhuman` and `mummy`, and both are created and edited with
plain form views (`MtRHumanCreateView` / `MtRHumanUpdateView`, `MummyCreateView` /
`MummyUpdateView`). Mummy has no group model.

## MtRHuman

[`mtr_human.py`](../models/mummy/mtr_human.py).

- Extra ability columns (all primary): talents `awareness`, `leadership`; skills
  `animal_ken`, `larceny`, `meditation`, `performance`, `survival`; knowledges `enigmas`,
  `law`, `occult`, `politics`, `technology`, `theology`.
- `allowed_backgrounds`: `contacts`, `mentor`, `allies`, `resources`, `retainers`, `cult`,
  `tomb`, `rank`, `remembrance`, `vessel`, `artifact`, `ka`, `amenti_companion`.
- Background columns: `allies`, `resources`, `retainers`, `tomb`, `rank`, `remembrance`,
  `vessel`, `artifact`, `ka`, `amenti_companion` are real `IntegerField`s; attribute access
  reads the column, not the `BackgroundRating` rows (see
  [Dynamic background properties](models.md#dynamic-background-properties)).

## Mummy

[`mummy.py`](../models/mummy/mummy.py).

| Group | Fields |
|-------|--------|
| Core traits | `balance` (default `5`, 0 to 10), `sekhem` (default `1`, 0 to 10), `ba` (current pool, default `10`), `ka_rating` (capacity, default `10`); `ba_stat` is a `core.linked_stat.LinkedStat` over `ka_rating` / `ba` with `cap_temporary=False` |
| Virtues | `conviction`, `restraint` (default `1`, 0 to 5) |
| Web | `web` (`isis`, `osiris`, `horus`, `maat`, `thoth`) |
| Hekau | Universal `alchemy`, `celestial`, `effigy`, `necromancy`, `nomenclature`; web-specific `ushabti`, `judge`, `phoenix`, `vision`, `divination` (0 to 5) |
| Lineage | `dynasty` (`ForeignKey(Dynasty, SET_NULL)`), `titles` (`ManyToManyField(MummyTitle)`), `mentor_mummy` (`ForeignKey("self")`, reverse `students`) |
| Rebirth | `incarnation` (default `1`), `years_since_rebirth`, `death_in_first_life`, `past_lives_memory`, `ancient_name` |
| Appearance | `mummified_appearance` (`preserved`, `desiccated`, `skeletal`, `varies`), `can_pass_as_mortal` |

The ranges above are field validators; `Mummy` declares no database constraints.

Behaviour:

- `save()` calls `update_ka_from_sekhem()`, which sets `ka_rating = sekhem * 10`, so edit
  Sekhem rather than `ka_rating`.
- `get_hekau()` returns rated Hekau by display name; `total_hekau()`, `has_hekau()`.
- `is_web_hekau(name)` is true for the Hekau tied to the mummy's web (Isis: Ushabti,
  Osiris: Judge, Horus: Phoenix, Ma'at: Vision, Thoth: Divination).
- `spend_ba(amount)` deducts and saves when the pool is large enough;
  `regain_ba(amount)` caps at `ka_rating`.

## See also

- [Character models](models.md)
- [Reference data: Mummy](reference-data.md#mummy)
- [Views and URLs](views-and-urls.md#mummy)
- [Services](services.md)
