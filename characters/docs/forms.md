# Forms

This page is the reference for [`characters/forms/`](../forms/): the reviewed field
allowlists that update views use, the limited forms owners get, the chargen forms
(allocation, backgrounds, gameline power steps, background-detail NPCs), the freebie and
XP forms, and the NPC and creation pickers. It is for developers changing what a form lets
a user submit. How forms plug into steps is in [Chargen](chargen.md); who may reach a form
is in [Authorization](../../docs/architecture/authorization.md).

## Layout

| Path | Contents |
|------|----------|
| [`forms/core/`](../forms/core/) | Gameline-independent forms (table below) |
| [`forms/constants.py`](../forms/constants.py) | `BASE_CATEGORY_CHOICES` (freebies: Attribute, Ability, Background, Willpower, MeritFlaw) and `XP_CATEGORY_CHOICES` (the same plus Image) |
| `forms/<gameline>/` | One module per character type or catalogue: creation (Basics) forms, power-step forms, freebie forms, catalogue forms |

## Update allowlists (`crud_fields`)

[`forms/core/crud_fields.py`](../forms/core/crud_fields.py) holds explicit tuples of
editable field names, in form order. Most full create and update views set `fields` to one
of them:

| Constant | Used by |
|----------|---------|
| `HUMAN_CREATE_FIELDS` / `HUMAN_UPDATE_FIELDS` | `HumanCreateView`, `HumanUpdateView` |
| `VAMPIRE_UPDATE_FIELDS`, `REVENANT_UPDATE_FIELDS` | `VampireUpdateView`, `RevenantUpdateView` |
| `WEREWOLF_UPDATE_FIELDS`, `KINFOLK_UPDATE_FIELDS`, `FERA_UPDATE_FIELDS`, `FOMOR_UPDATE_FIELDS`, `DRONE_UPDATE_FIELDS`, `WT_A_HUMAN_UPDATE_FIELDS` | The Werewolf update views |
| `MAGE_CREATE_FIELDS`, `MT_A_HUMAN_UPDATE_FIELDS` | `MageCreateView` / `MageUpdateView`, `MtAHumanUpdateView` |
| `WT_O_HUMAN_UPDATE_FIELDS` | `WtOHumanUpdateView` |
| `CHANGELING_UPDATE_FIELDS` | `ChangelingUpdateView` |
| `DEMON_UPDATE_FIELDS`, `DT_F_HUMAN_UPDATE_FIELDS`, `THRALL_UPDATE_FIELDS`, `EARTHBOUND_CREATE_FIELDS` / `EARTHBOUND_UPDATE_FIELDS` | The Demon views |
| `HT_R_HUMAN_CREATE_FIELDS` / `..._UPDATE_FIELDS`, `HUNTER_CREATE_FIELDS` / `..._UPDATE_FIELDS` | The Hunter views |
| `MUMMY_UPDATE_FIELDS` | `MummyUpdateView` |

Building blocks (`IDENTITY_FIELDS`, `ATTRIBUTE_FIELDS`, `COMMON_TALENT_FIELDS`,
`COMMON_SKILL_FIELDS`, `COMMON_KNOWLEDGE_FIELDS`, `BIOGRAPHY_FIELDS`) are shared by the
constants. The other character views declare an explicit list in their own module instead:
for example `VtMHumanUpdateView` (`VTMHUMAN_FORM_FIELDS`), `CtDHumanUpdateView`
(`CTDHUMAN_FORM_FIELDS`), `GhoulUpdateView`, `CompanionUpdateView` (`ST_EDIT_FIELDS`), the
Inanimae, Nunnehi and Autumn Person views, and `SpiritCreateView` / `SpiritUpdateView`.
`SorcererUpdateView` uses the `SorcererForm` model form.

The module rule is: new model fields require review, and editable fields are never derived
by introspecting the model. A field that is not in the tuple cannot be posted through the
full form. Two safeguards back this up:

- The route policy's field guard refuses non-staff changes to `owner`, `chronicle`,
  `gameline`, `status`, `npc`, `xp`, `freebies_approved`, `approved` and `approved_by`
  even when a form includes them (see
  [Authorization](../../docs/architecture/authorization.md)).
- [`tests/views/core/shared_character_crud_baseline.json`](../tests/views/core/shared_character_crud_baseline.json)
  records, per view path, the field count and a SHA-256 of the ordered field list, and
  [`test_shared_character_crud.py`](../tests/views/core/test_shared_character_crud.py)
  fails when a view's `fields` drift from it (see [Testing](testing.md)).

## Limited forms (owner edits)

Update views of characters combine `core.mixins.ScopedEditFormMixin` with
`EditPermissionMixin` (see [core mixins](../../core/docs/mixins.md)). The mixin returns the
full form (built from the allowlist) only when the user has a scoped editor role for the
object (admin, chronicle head storyteller or chronicle storyteller); everyone else who may
edit gets the view's `limited_form_class`:

| Form | Model | Fields | Used by |
|------|-------|--------|---------|
| `LimitedHumanEditForm` ([`limited_edit.py`](../forms/core/limited_edit.py)) | `Human` | `notes`, `description`, `public_info`, `image`, `history`, `goals` | Every `Human` subclass update view |
| `OwnerUnapprovedCharacterEditForm` | `Character` | `name`, `concept`, `notes`, `description`, `public_info`, `image` | `CharacterUpdateView` |

So an owner never edits ratings directly: stats change through chargen, freebies or XP.

## Chargen forms

### Allocation

[`allocation.py`](../forms/core/allocation.py) provides `AllocationFormMixin`,
`AllocationModelForm`, the cached factory `allocation_modelform(model, fields)`, and the
template helpers `rating_values()` and `priority_columns()`. `clean()` runs the
`characters.rules` allocation rules passed as `allocation_rules=` plus an optional
`extra_clean` callable, reports the first violation only, and keeps flash text in
`flash_errors`. The PRI / SEC / TER ranks (`priority_<group>`) are read from the posted data
but are not form fields. Details: [Character creation](../../docs/architecture/character-creation.md#allocation-rules)
and [Costs and rules](costs-and-rules.md).

### Backgrounds

[`backgroundform.py`](../forms/core/backgroundform.py):

- `BackgroundRatingForm`: a `BackgroundRating` model form (`bg`, `rating` 0 to 5, `note`,
  `display_alt_name`, `pooled`); `save()` attaches the character.
- `BaseBackgroundRatingFormSet` and `BackgroundRatingFormSet` (an inline formset on
  `Human`, one extra row, no deletion). With `enforce_allocation` the formset requires
  exactly `character.background_points` dots, each costing the background's `multiplier`,
  and reports `character.background_violations()` (Kinfolk tribal limits) first.

### Background-detail NPCs

`LinkedNPCForm` ([`linked_npc.py`](../forms/core/linked_npc.py)) creates the NPC behind an
Allies, Mentor, Contacts, Retainers or Followers background. `npc_type` covers every
gameline's character types; `save()` creates the character with `npc=True`, status `Un`,
the name, concept, archetypes (not for Werewolf, Changeling and Fera) and a note recording
the rank, role and gameline basics to fill in later. `GenericBackgroundView` then sets the
NPC's owner and chronicle from the creating character, marks it `Sub`, and completes the
`BackgroundRating` (see [Views and URLs](views-and-urls.md#chargen-step-views)).

### Other shared steps

| Form | Module | Step |
|------|--------|------|
| `SpecialtiesForm` | [`specialty.py`](../forms/core/specialty.py) | Specialties (and the sheet's "add specialties" action): one text field with autocomplete suggestions per stat in `specialties_needed` |
| `CharacterTemplateSelectionForm` | [`template_selection.py`](../forms/core/template_selection.py) | Template picker before a mortal's chargen: public `CharacterTemplate`s for the subclass's `gameline` and `character_type` that are approved, or official (seeded) and not retired or deceased |
| `core.forms.language.HumanLanguageForm` | `core` app | Languages |

### Gameline forms

| Gameline | Creation (Basics) forms | Step and power forms |
|----------|-------------------------|----------------------|
| Vampire | `VtMHumanCreationForm`, `VampireCreationForm`, `GhoulCreationForm` | Disciplines and Virtues steps use allocation forms built in the views |
| Werewolf | `WtAHumanCreationForm`, `WerewolfCreationForm`, `KinfolkCreationForm`, `FomorCreationForm`, `DroneCreationForm`, `FeraCreationForm` | `WerewolfGiftsForm` (three Gifts: breed, auspice, tribe), `WerewolfHistoryForm`, `FeraStartingGiftsForm` (three rank-1 Gifts from the breed's groups), `FeraFirstChangeForm`, `SeptPositionForm` |
| Mage | `MtAHumanCreationForm`, `MageCreationForm` (chained affiliation / faction / subfaction), `SorcererBasicsForm` | `MageSpheresForm` (affinity Sphere, Arete at most 3), `MageFocusForm` and `PracticeRatingForm` / `BasePracticeRatingFormSet`, `RoteCreationForm`, `EffectForm` / `EffectCreateOrSelectForm`, `EnhancementForm`, `FamiliarForm`, the numina forms (`NuminaPathForm`, `PsychicPathForm`, their formsets, `NuminaRitualForm`), `SorcererForm` (full edit), `CabalForm` |
| Wraith | `WtOHumanCreationForm`, `WraithCreationForm` | `PassionForm`, `FetterForm` |
| Changeling | `CtDHumanCreationForm`, `ChangelingCreationForm` | `HouseFactionForm` |
| Demon | `DtFHumanCreationForm`, `DemonCreationForm`, `ThrallCreationForm` | `ApocalypticFormSelectionForm` (four low- and four high-Torment traits within budget, disjoint) |
| Mummy | `MtRHumanCreationForm`, `MummyCreationForm` | `DynastyForm`, `MummyTitleForm` |

Location and item forms used by Mage background steps (`NodeForm`, `LibraryForm`,
`SanctumForm`, `WonderForm`, `ArtifactCreateOrSelectForm`, `ChantrySelectOrCreateForm`)
belong to the `locations` and `items` apps.

## Freebie forms

Freebie forms have the fields `category`, `example`, `value`, `note` and `pooled`. They do
not save anything: `FreebieSpendingView` reads the cleaned data and calls the freebie
spending service (see [Services](services.md)).

| Form | Base | Used by |
|------|------|---------|
| `HumanFreebiesForm` ([`freebies.py`](../forms/core/freebies.py)) | `forms.Form` | Human and Werewolf (Garou) freebie steps; base of the Wraith, Demon, Companion and Sorcerer forms. Hides categories the character cannot afford (`validator()` checks `characters.costs.get_freebie_cost`) |
| `ChainedHumanFreebiesForm` ([`chained_freebies.py`](../forms/core/chained_freebies.py)) | `widgets.ChainedSelectMixin`, `ConditionalFieldsMixin` | Mortal freebie steps (`vtm_human`, `wta_human`, `mta_human`, `wto_human`, `ctd_human`, Kinfolk, Drone, Fera, Fomor). Cascading `example` and `value` choices computed at init; field visibility rules in `BASE_CONDITIONAL_FIELDS` |
| `ChainedVampireFreebiesForm`, `ChainedGhoulFreebiesForm` | `ChainedHumanFreebiesForm` | Vampire (Discipline, Virtue, Humanity, Path Rating) and Ghoul (Discipline) |
| `ChainedMageFreebiesForm` | `ChainedHumanFreebiesForm` | Mage |
| `ChainedChangelingFreebiesForm` | `ChainedHumanFreebiesForm` | Changeling |
| `WraithFreebiesForm`, `DemonFreebiesForm`, `DtFHumanFreebiesForm`, `ThrallFreebiesForm`, `CompanionFreebiesForm`, `SorcererFreebiesForm` | `HumanFreebiesForm` | The matching steps |

Merit and flaw choices in the chained forms are filtered by
`characters.utils.get_character_object_type()`, which treats every `*_human` type as
`human`.

## XP forms

`XPForm` ([`xp.py`](../forms/core/xp.py)) is a `ChainedSelectMixin` form with `category`
(from `XP_CATEGORY_CHOICES`, minus categories the character cannot use or afford),
`example`, `value`, `note`, `pooled` and `image_field`. `MageXPForm`
([`forms/mage/xp.py`](../forms/mage/xp.py)) adds Mage categories and cost helpers for
Spheres, practices and Arete. Both are bases for the XP spend forms in `game.forms`
(`XPSpendForm`, `MageXPSpendForm`); `MageXPForm` is also served directly by
`MageXPSpendView` (`characters:mage:spend_xp`). The request and approval flow is in
[XP, freebies and approvals](../../docs/architecture/xp-and-approvals.md).

## Creation pickers and NPC profiles

| Form | Purpose |
|------|---------|
| `CharacterCreationForm` ([`character_creation.py`](../forms/core/character_creation.py)) | The index page's "Begin a new character" picker: chained `gameline` and `char_type` from `game.ObjectType` rows (excluding `EXCLUDED_TYPES` and types without a create route, via `core.create_redirects.creatable_character_types`). Storytellers see every gameline; other users see Mage types only. It submits by `GET` to `core:object_type_redirect` |
| `GroupCreationForm` ([`group_creation.py`](../forms/core/group_creation.py)) | The "form a group" picker: storytellers choose any group type, other users only `cabal` |
| `NPCProfileForm` ([`npc_profile.py`](../forms/core/npc_profile.py)) | `NPCProfileCreateView` (`characters:create:npc`, optionally for a related character): any character type, with conditional sections for Mage, Sorcerer, Werewolf, Kinfolk, Wraith, Changeling, Thrall and Demon fields. `save()` creates an `npc=True`, `Un` character owned by the user, in a chronicle the user can read |

## See also

- [Chargen](chargen.md)
- [Views and URLs](views-and-urls.md)
- [Services](services.md)
- [Authorization](../../docs/architecture/authorization.md)
- [Adding a view](../../docs/guides/adding-a-view.md)
