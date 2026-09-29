# Templates

This page is the reference for [`characters/templates/characters/`](../templates/characters/):
the character sheet shell and how each gameline's sheet extends it, the create and edit
form shells, the chargen templates, the reference-page shells, the shared `tl/` partials,
and the app's template tags and static scripts. It is for developers changing what a page
shows. The design system (Spread), the `tl` template tags and gameline theming are
project-wide: see [Front end](../../docs/architecture/frontend.md) and
[Template tags](../../docs/reference/template-tags.md).

All pages extend `core/tl_base.html` (directly or through a shell below) or
`core/form.html`, set `{% block gameline %}` for the accent and display font (usually
`{{ object|gameline_code }}`), and render ratings with the `tl` tags. Inline `style=""`
attributes are not allowed.

## Directory layout

| Path | Contents |
|------|----------|
| `index.html`, `charlist.html` | Character index (chronicle switch, status tabs, create pickers) and the Retired / Deceased / NPC lists |
| `core/character/` | The sheet shell `detail.html`, the base `form.html`, `display_includes/buttons.html` |
| `core/human/` | The `Human` sheet (`detail.html`), the human create/edit form (`form.html`), Basics (`humanbasics.html`), and `attributes.html`, `bio.html`, `chargen_form.html`, which Human step views name as `template_name` but `ChargenStepMixin` does not render (it uses `characters/core/chargen.html` for any name not ending in `/chargen.html`) |
| `core/attribute_block/`, `core/background_block/`, `core/ability_block/` | Attribute sheet section and chargen form, Backgrounds chargen formset, ability running status |
| `core/chargen.html`, `core/chargen/` | Chargen page shell and partials |
| `core/group/` | Group page and form, shared by every group type |
| `core/archetype/`, `core/derangement/`, `core/meritflaw/`, `core/specialty/`, `core/npc/`, `core/ally/` | Core reference pages, the NPC profile form, LinkedNPC fields |
| `shared/` | Partials shared across gamelines: `human/ability_block_display.html`, `human/basics_display_include.html`, `human/template_select.html`, `vampire/*` power and virtue displays, `group/list.html`, `reference/form.html` |
| `tl/` | Spread partials and shells (below) |
| `<gameline>/<type>/` | One directory per character type or catalogue: `detail.html`, `form.html`, `list.html`, `basics.html`, `chargen.html`, step partials |
| `werewolf/tl/`, `changeling/tl/`, `mage/form/` | Gameline form shells |

## The character sheet

`core/character/detail.html` is the sheet shell. It extends `core/tl_base.html`, draws the
line cover (type, chronicle, NPC flag, status, owner, XP, "Continue character creation"
when `chargen_url` is set, edit and XP buttons from `object_perms`) and defines the blocks
children fill:

| Block | Holds |
|-------|-------|
| `basics` | Cover facts |
| `cover_sub` | Line under the name (concept by default) |
| `statistics` | Numbered sheet sections |
| `flavor` | Appearance, history, journal |
| `experience` (`freebies`, `xp`) | The `?tab=experience` tab; `xp` defaults to `characters/tl/xp_history.html` |

`?tab=scenes` shows `characters/tl/scenes.html`. Viewers without full access get
`characters/tl/not_owner.html` (the public card and visible scenes).

`core/human/detail.html` extends the shell and fixes the section order for every
human-based type. Gamelines override blocks, never the order:

```text
statistics: attributes, abilities, powers, advantages, backgrounds, line, passions,
            fetters, health, mfs, languages, equipment, allies
flavor:     appearance, history, journal
```

Each gameline mortal sheet extends `core/human/detail.html`, and each supernatural sheet
extends its mortal: for example `vampire/vampire/detail.html` extends
`vampire/vtmhuman/detail.html` and fills `basics`, `powers` (Disciplines), `advantages`,
`line` (the active virtues, then Backgrounds), `health`, `mfs` and `freebies` (a freebie
form while the vampire is `Sub`), and empties `backgrounds`. `mage/mage/detail.html`, `werewolf/garou/detail.html`,
`hunter/hunter/detail.html` and the others follow the same pattern. The sheet sections
call model helpers such as `attribute_sections()`, `ability_sections()`,
`secondary_ability_sections()`, `get_health_table()`, `renown_tracks()`,
`gifts_by_rank()`, `art_rows()` and `lore_rows()` (see the model pages).

## Create and edit forms

| Shell | Used by |
|-------|---------|
| `core/form.html` (core app) | Most forms; blocks `creation_title`, `errors`, `contents`, `formdetails` |
| `core/human/form.html` | Human create and edit; the same template renders the create form, a storyteller's full form and an owner's limited form, with fields grouped into sections by `core/misc/field_sections.html` |
| `characters/tl/character_edit_fields.html` | Vampire, Demon and Hunter character forms: groups any form's fields into sections with `{% character_edit_sections form as sections %}` |
| `mage/form/base.html` | Mage-family and Mage reference forms; sections declared in `characters/views/mage/form_layout.py` |
| `werewolf/tl/form.html`, `changeling/tl/form.html` | Werewolf and Changeling character and reference forms |
| `shared/reference/form.html` | Plain reference entries (name, description, then any other field) |

Because the owner's `LimitedHumanEditForm` and the full allowlist form share one template,
section helpers render whatever fields the bound form has and skip the rest.

## Chargen templates

| Template | Role |
|----------|------|
| `core/chargen.html` | Page shell: draft cover with the step list, then one step (`chargen/step_body.html`) inside the htmx root (`chargen/interactive.html`) or a plain multipart form |
| `<gameline>/<type>/chargen.html` | One-line `{% extends "characters/core/chargen.html" %}` override slots, selected by `ChargenStepMixin.get_template_names()` |
| `core/chargen/step_body.html`, `step.html`, `step_fragment.html` | Step body, the swappable form, the htmx fragment response |
| `core/chargen/progress_region.html`, `steps.html`, `step_list.html` | Step list (desktop list and mobile sheet) |
| `core/chargen/form.html`, `fields.html` | Default step body |
| `core/chargen/abilities.html`, `alloc_row.html`, `priority_head.html`, `pool.html` | Ranked allocation columns and the PRI / SEC / TER picker |
| `core/chargen/freebies.html`, `freebies_chained.html` | Freebie step bodies |
| `core/chargen/specialties.html`, `skip.html` | Final step; "nothing to allocate" body |
| `core/chargen/feedback.html`, `options.html` | Validation and chained-options partials |

Step body overrides per workflow (gameline `ability_block_form.html`, Vampire
`steps/*.html`, Wraith `steps/*.html`, Mage `mage_*_form.html`, location and item
`form_include.html` partials) are listed in [Chargen](chargen.md#templates-per-step). The
mechanics are in [Character creation](../../docs/architecture/character-creation.md#templates).

## Reference pages

Two generations of reference shells exist side by side:

| Shells | Blocks | Used by |
|--------|--------|---------|
| `tl/reference_detail.html`, `tl/reference_list.html` | `back`, `facts`, `cover_extra`, `ref_actions`, `sections`, `description`, `after_description` | Core, Werewolf, Mage and Changeling catalogues |
| `tl/ref2_detail.html`, `tl/ref2_list.html` (with `ref2_prose.html`, `ref2_pager.html`) | `gameline`, `ref_back`, `ref_eyebrow`, `ref_name`, `ref_after_name`, `ref_facts`, `ref_list`, ... | Vampire, Wraith, Demon, Hunter and Mummy catalogues |
| `tl/ref2_chars.html` (tiles from `ref2_char_tile.html`) | `chars_eyebrow`, `chars_title`, `chars_actions` | Hunter, Demon and Mummy character lists |

Both detail shells include `characters/tl/known_by.html` when the view supplies
`known_by` (see [Views and URLs](views-and-urls.md#known-by)).

## `tl/` partials

| Partial | Purpose |
|---------|---------|
| `character_tile.html` | Character tile for the index and lists |
| `create_forms.html` | "Begin a new character" and "Or form a group" pickers on the index cover |
| `xp_history.html` | Experience tab: unspent XP and spend history with approve / reject buttons |
| `scenes.html` | Scene rows for the sheet |
| `not_owner.html` | Public view of a sheet |
| `backgrounds.html`, `background_row.html`, `merits.html`, `appearance.html`, `history.html`, `prose_block.html`, `journal_link.html`, `specialties_form.html` | Sheet sections |
| `power_cell.html`, `rotes.html`, `rote_card.html`, `resonance.html` | Power and Mage sections |
| `known_by.html` | Known-by list on reference pages |
| `reference_cover_title.html`, `reference_no_results.html` | Pieces of the reference shells |

## Template tags

| Library | Tag or filter | Purpose |
|---------|---------------|---------|
| [`character_edit`](../templatetags/character_edit.py) | `{% character_edit_sections form as sections %}` | Groups a character form's fields into sections (identity grid, Attribute columns, Ability columns, long text); every field appears once |
| [`startswith`](../templatetags/startswith.py) | `startswith` filter | `value\|startswith:"prefix"` |

The `tl`, `sanitize_text`, `tl_forms` and `model_meta` libraries come from the `core` app.

## Static files

[`static/characters/js/`](../static/characters/js/):

| Script | Loaded for |
|--------|------------|
| `chargen.js`, `chargen-components.js`, `chargen-priority.js` | Chargen (htmx fragment handling, Alpine components, PRI / SEC / TER picker) |
| `attribute-validation.js`, `ability-validation.js`, `background-validation.js` | Running hints on non-interactive chargen steps (included by the attribute, ability-status and Backgrounds step templates) |
| `mage-xp.js`, `mage-xp-rote.js`, `mage-enhancements.js`, `sorcerer-freebies.js` | Mage sheet XP form, rote form, Enhancement step, Sorcerer freebies |
| `thorn-list.js` | Wraith Thorn list |

Templates pass configuration to these scripts as data (attributes or JSON), not as inline
code; [`tests/test_static_page_assets.py`](../tests/test_static_page_assets.py) checks that
such values render as inert, escaped data.

## See also

- [Front end](../../docs/architecture/frontend.md)
- [Template tags](../../docs/reference/template-tags.md)
- [Character creation](../../docs/architecture/character-creation.md#templates)
- [Views and URLs](views-and-urls.md)
- [Chargen](chargen.md)
