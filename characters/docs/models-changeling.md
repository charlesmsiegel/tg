# Changeling: the Dreaming models

This page is the reference for the Changeling character types in
[`characters/models/changeling/`](../models/changeling/): `CtDHuman`, `Changeling`
(Kithain), `Inanimae`, `Nunnehi`, `AutumnPerson` and the `Motley` group. The Changeling
catalogues (kiths, houses, house factions, Legacies, cantrips, chimera) are described in
[Reference data](reference-data.md#changeling). Read [Character models](models.md) first
for the `Human` base. Terms such as Kith, Seeming, Glamour and Banality are in the
[glossary](../../docs/reference/glossary.md).

## Types at a glance

| Class | Parent | `type` | Chargen workflow | Detail URL name |
|-------|--------|--------|------------------|-----------------|
| `CtDHuman` | `Human` | `ctd_human` | `ctd_human` (8 steps) | `characters:character` |
| `Changeling` | `CtDHuman` | `changeling` | `changeling` (9 steps) | `characters:character` (a `characters:changeling:changeling` route also exists) |
| `Inanimae` | `CtDHuman` | `inanimae` | none (freebie position 5) | `characters:changeling:inanimae` |
| `Nunnehi` | `CtDHuman` | `nunnehi` | none (freebie position 5) | `characters:changeling:nunnehi` |
| `AutumnPerson` | `CtDHuman` | `autumn_person` | none (freebie position 5) | `characters:changeling:autumn_person` |
| `Motley` | `Group` | `motley` | n/a | `characters:group` (a `characters:changeling:motley` route also exists) |

`gameline = "ctd"` (URL namespace `characters:changeling:`). Types without a workflow are
created and edited with plain create/update views; their freebie positions come from
`DETAIL_ONLY_FREEBIE_POSITIONS` (see [Chargen](chargen.md)).

## CtDHuman

[`ctdhuman.py`](../models/changeling/ctdhuman.py). Extra ability columns (all primary):
talents `kenning`, `leadership`; skills `animal_ken`, `larceny`, `performance`,
`survival`; knowledges `enigmas`, `gremayre`, `law`, `politics`, `technology`.
`allowed_backgrounds`: `contacts`, `mentor`, `chimera`, `dreamers`, `holdings`,
`remembrance`, `resources`, `retinue`, `title`, `treasure`. Every subclass inherits these
lists.

## Changeling

[`changeling.py`](../models/changeling/changeling.py).

### Fields

| Group | Fields |
|-------|--------|
| Identity | `court` (`seelie`, `unseelie`), `kith` (`ForeignKey(Kith)`), `seeming` (`childling`, `wilder`, `grump`), `house` (`ForeignKey(House)`), `seelie_legacy` / `unseelie_legacy` (`ForeignKey(Legacy)`, reverse `seelie_legacy_of` / `unseelie_legacy_of`); all nullable, `SET_NULL` |
| Arts | `autumn`, `chicanery`, `chronos`, `contract`, `dragons_ire`, `legerdemain`, `metamorphosis`, `naming`, `oneiromancy`, `primal`, `pyretics`, `skycraft`, `soothsay`, `sovereign`, `spring`, `summer`, `wayfare`, `winter` |
| Realms | `actor`, `fae`, `nature_realm`, `prop`, `scene`, `time` |
| Glamour and Banality | `banality` / `temporary_banality` (defaults `3` / `0`) and `glamour` / `temporary_glamour` (default `4`), from `core.linked_stat.linked_stat_fields` with `cap_temporary=False` |
| Thresholds | `musing_threshold`, `ravaging_threshold` (choice lists), `antithesis` |
| Story | `true_name`, `date_ennobled`, `crysalis`, `date_of_crysalis`, `fae_mien` |

### Behaviour

- `set_seeming()` sets Willpower to 4, then adds a Glamour dot for childlings and wilders or
  a Willpower dot for grumps.
- `eligible_for_house()` is true when the `title` background is above 0 or the kith name
  contains "Sidhe". `set_house()` requires eligibility and a house of the same court;
  `has_house()` is true when an eligible character has a house or an ineligible one has
  none.
- `set_seelie_legacy()` / `set_unseelie_legacy()` accept only a Legacy of the matching
  court.
- `has_arts()` requires exactly 3 Art dots and `has_realms()` exactly 5 Realm dots;
  `add_art()` and `add_realm()` cap at 5.
- `birthright_correction()` applies kith birthrights: Troll +1 Strength and one health
  level, Satyr +1 Stamina, Piskey +1 Dexterity, Sidhe +2 Appearance (Attributes may exceed
  5 here).
- `art_rows()` and `realm_rows()` feed the sheet.
- Legacy spend hooks: `art_freebies()`, `realm_freebies()`, `glamour_freebies()`,
  `spend_xp()`, `spend_freebies()`.

## Inanimae

[`inanimae.py`](../models/changeling/inanimae.py). Elemental fae.

| Field | Values |
|-------|--------|
| `kingdom` | `kubera`, `ondine`, `paroseme`, `sylph`, `salamander`, `solimond`, `mannikin` |
| `inanimae_seeming` | `glimmer`, `naturae`, `ancient` |
| `season` | `spring`, `summer`, `autumn`, `winter` |
| `mana` | Integer, default `4` |
| `anchor_description`, `elemental_strength`, `elemental_weakness` | Text |

Setters and checks: `set_kingdom()`, `set_season()`, `set_inanimae_seeming()`,
`add_mana()`, `set_anchor()`, and the matching `has_*()`.

## Nunnehi

[`nunnehi.py`](../models/changeling/nunnehi.py). Native American fae.

| Field | Values |
|-------|--------|
| `tribe` | `may_may_gway_shi`, `yunwi_tsundi`, `canotina`, `kachina`, `nanehi`, `nunnehi_proper`, `other` |
| `nunnehi_seeming` | `katchina`, `kohedan`, `kurganegh` |
| `path` | `warrior`, `healer`, `sage`, `trickster` |
| `spirit_medicine` | Integer, default `4` |
| `sacred_place`, `spirit_guide`, `tribal_duty` | Text / char |

## AutumnPerson

[`autumn_person.py`](../models/changeling/autumn_person.py). A Banality-soaked mortal
antagonist.

| Field | Values |
|-------|--------|
| `archetype` | `authority`, `bureaucrat`, `cynic`, `fundamentalist`, `corporate`, `scientist`, `debunker`, `other` |
| `banality_rating` | Integer, default `8` |
| `awareness` | `unaware`, `suspicious`, `aware`, `hunter` (a `CharField`, not an ability) |
| `organization`, `motivation`, `sphere_of_influence` | Text |
| `anti_fae_abilities` | `JSONField(list)` |
| `is_dauntain`, `former_kith` | A changeling turned Autumn Person (`make_dauntain()`) |

`add_anti_fae_ability()` appends to the JSON list.

## Motley

[`motley.py`](../models/changeling/motley.py). A `Group` with no extra fields; it keeps
`Group.get_absolute_url()`.

## See also

- [Character models](models.md)
- [Reference data: Changeling](reference-data.md#changeling)
- [Chargen](chargen.md)
- [Views and URLs](views-and-urls.md#changeling)
