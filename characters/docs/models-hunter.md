# Hunter: the Reckoning models

This page is the reference for the Hunter character types in
[`characters/models/hunter/`](../models/hunter/): `HtRHuman` and `Hunter` (one of the
Imbued). The Hunter catalogues (creeds, Edges, hunter organizations) are described in
[Reference data](reference-data.md#hunter). Read [Character models](models.md) first for
the `Human` base. Terms such as Creed, Edge and Imbued are in the
[glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `HtRHuman` | `Human` | `htr_human` | none (freebie position 5) | `characters:hunter:htrhuman` |
| `Hunter` | `HtRHuman` | `hunter` | none (freebie position 7) | `characters:hunter:hunter` |

`gameline = "htr"` (URL namespace `characters:hunter:`). Neither type has a chargen
workflow: both are created and edited with plain form views
(`characters:hunter:create:hunter`, `characters:hunter:create:htrhuman`,
`characters:hunter:update:hunter`, `characters:hunter:update:htrhuman`). `HtRHuman`
and `Hunter` override `get_update_url()` and `get_creation_url()` to name these routes
(the `Human` defaults would look for `...:htr_human`). Hunter has no group model.

## HtRHuman

[`htrhuman.py`](../models/hunter/htrhuman.py).

- Extra ability columns (all primary): talents `awareness`, `leadership`; skills
  `animal_ken`, `larceny`, `performance`, `repair`, `survival`; knowledges `finance`,
  `law`, `occult`, `politics`, `technology`. Like the other lines' 20th-anniversary lists
  it has no `dodge` (there is no such field).
- `allowed_backgrounds`: `allies`, `contacts`, `influence`, `mentor`, `resources`,
  `status_background`. `allies`, `influence`, `resources` and `status_background` are
  also real `IntegerField` columns, which attribute access reads instead of the
  `BackgroundRating` rows (see
  [Dynamic background properties](models.md#dynamic-background-properties)).

## Hunter

[`hunter.py`](../models/hunter/hunter.py).

| Group | Fields |
|-------|--------|
| Creed | `creed` (`ForeignKey(Creed, SET_NULL)`, reverse `hunters`), `primary_virtue` (`conviction`, `vision`, `zeal`; default `conviction`) |
| Virtues | `conviction`, `vision`, `zeal` and their `temporary_*` pairs from `core.linked_stat.linked_stat_fields` (default `1`, permanent 1 to 5, `cap_temporary=False`) |
| Conviction Edges | `discern`, `burden`, `balance`, `expose`, `investigate`, `witness`, `prosecute` |
| Vision Edges | `illuminate`, `ward`, `cleave`, `hide`, `blaze`, `radiate`, `vengeance` |
| Zeal Edges | `demand`, `confront`, `donate`, `becalm`, `respire`, `rejuvenate`, `redeem` |
| Other | `imbuing_date`, `safehouse` (`ForeignKey("locations.Safehouse", SET_NULL)`, reverse `members`), `cell_members` (symmetrical `ManyToManyField("self")`) |

All Edge fields are `IntegerField`s with default `0`.

- `get_edges()` returns `{"conviction": {...}, "vision": {...}, "zeal": {...}}` with the
  rated Edges under each virtue.
- `primary_edges()` returns the creed's `primary_virtue` when a creed is set, else the
  character's own `primary_virtue`.
- Hunter has no spending hooks of its own; the XP and freebie
  [spending services](services.md) handle Hunter spends.

## See also

- [Character models](models.md)
- [Reference data: Hunter](reference-data.md#hunter)
- [Services](services.md)
- [Views and URLs](views-and-urls.md#hunter)
