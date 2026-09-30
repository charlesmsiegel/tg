# Character templates

Rules for working on `core.models.CharacterTemplate`: pre-built character concepts that
can be applied to a new character or turned into an NPC. The model is documented in
[core/docs/models.md](../../../../core/docs/models.md); chargen in
[docs/architecture/character-creation.md](../../../../docs/architecture/character-creation.md).

## The model

`CharacterTemplate(Model)` ([`core/models.py`](../../../../core/models.py)) is a player
object: it has `owner`, `chronicle`, `status`, `visibility` and the approval workflow.
Unlike other `Model` subclasses it stores `gameline` as a **column**
(`choices=settings.GAMELINE_CHOICES`, default `"wod"`) next to `character_type` (the character
`type`, such as `"vampire"`).

| Field | Content |
|-------|---------|
| `basic_info` | `{field: value}` set on the character; `"FK:Archetype:<name>"` resolves an archetype |
| `attributes`, `abilities`, `powers` | `{property_name: rating}` set with `setattr` when the character has the attribute |
| `backgrounds`, `merits_flaws` | `[{"name": ..., "rating": ...}]`, matched by `name` |
| `specialties` | `["Ability (Specialty)", ...]` |
| `languages` | Language names |
| `equipment`, `suggested_freebie_spending` | Guidance text and data; not applied |
| `is_official`, `is_public`, `times_used` | Metadata |

`Meta.unique_together = [["gameline", "character_type", "name"]]`.

`apply_to_character(character)` sets the fields, creates `BackgroundRating`,
`MeritFlawRating` and `Specialty` rows with `get_or_create`, adds languages, saves the
character, records a `TemplateApplication` and increments `times_used`. Names that match
no row are skipped silently.

## Rules

- **Keys are property names.** `attributes`, `abilities` and `powers` keys must be field
  names on the target character class (`"alertness"`, `"potence"`); unknown keys are
  ignored, so a typo loses data without an error. Test a new template against its
  character type.
- **Only `Archetype` is supported in `"FK:Model:Name"`.** Add a resolver in
  `apply_to_character` (with a test) before using another model name.
- **Call it inside a transaction.** `CharacterTemplateSelectView.form_valid` is
  `@transaction.atomic`; `CharacterTemplateQuickNPCView` wraps creation and application in
  `transaction.atomic()`.
- **Access follows the player-object policies**: list `OBJECT_LIST`, detail and export
  `OBJECT_DETAIL`, create `OBJECT_CREATE`, update and delete `OBJECT_WRITE`, import and
  quick NPC `LOGIN` (the quick NPC view requires `can_manage_scope` for the template's
  chronicle and gameline). An **official** template (`is_official=True`) needs a scoped
  editor for every `OBJECT_*` write (`core/access_policy.py`).
- **Selection offers approved public templates only.**
  `characters.forms.core.template_selection.CharacterTemplateSelectionForm` filters
  `gameline`, `character_type`, `is_public=True`, `status="App"`; subclasses set the
  `gameline` and `character_type` class attributes.
- **The selection step is position 0**, outside the numbered chargen workflow:
  `characters.views.core.template_selection.CharacterTemplateSelectView` serves only the
  owner's `Un`/`Rev` character with `creation_status == 0`, applies the template, sets
  `creation_status = 1` and redirects to `creation_route`. Gameline subclasses set
  `model`, `form_class`, `template_name` and `creation_route`, and are routed in the
  gameline's `detail.py` (`characters:vampire:vtmhuman_template`).
- **Seed data** lives in `populate_db/character_templates/<gameline>_templates.py` and uses
  `CharacterTemplate.objects.get_or_create(name=..., gameline=..., defaults={...})`;
  `populate_gamedata` loads it.
- `CharacterTemplate.clean()` lists valid gamelines in code (`wod`, `vtm`, `wta`, `mta`,
  `wto`, `ctd`, `dtf`); a template for `htr` or `mtr` fails validation until that list
  follows `settings.GAMELINES`.

## Views and URLs

[`core/views/character_template.py`](../../../../core/views/character_template.py), routed
in `core/urls.py` as `core:character_template_list`, `_create`, `_detail`, `_update`,
`_delete`, `_export` (JSON download), `_import` (JSON upload through
`core.forms.character_template.CharacterTemplateImportForm`, always `is_official=False`)
and `_create_npc` (POST; creates an approved NPC of the mapped model and applies the
template).

## Checklist

- [ ] Keys match the target class's field names; `FK:` only for `Archetype`.
- [ ] Application runs in a transaction; tests assert the character's values and the
  `TemplateApplication` row.
- [ ] Official templates still require a scoped editor to change.
- [ ] Selection shows only approved, public templates of the right gameline and type.
- [ ] Seed scripts use `get_or_create` and a valid gameline.

## See also

- [core/docs/models.md](../../../../core/docs/models.md)
- [docs/architecture/character-creation.md](../../../../docs/architecture/character-creation.md)
- [`characters/views/core/template_selection.py`](../../../../characters/views/core/template_selection.py)
- [`core/tests/views/test_character_template.py`](../../../../core/tests/views/test_character_template.py)
- [permissions.md](permissions.md), [commands.md](commands.md)
