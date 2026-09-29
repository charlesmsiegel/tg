# Location templates

This page describes how the `locations` templates are organised, the shared shells and
blocks every location page builds on, the partials, the wizard templates, and the form
includes that the character wizards reuse. It is for developers styling or adding
location pages. The design system (Spread, the `tl` tags, gameline theming) is covered
in [frontend](../../docs/architecture/frontend.md).

## Layout

Templates live in [`locations/templates/locations/`](../templates/locations/):

```text
locations/
├── index.html                   staff index (LocationIndexView)
├── core/
│   ├── tl_form.html             form shell (extends core/form.html)
│   ├── tl_list.html             list shell (extends core/tl_base.html)
│   ├── location/                detail and form shells, generic location pages
│   └── city/                    City pages
├── tl/                          shared partials
├── mage/tl/zone_formset.html    reality zone rows
├── mage/chantry/                chantry detail, forms and wizard templates
├── changeling/freehold/chargen/ freehold wizard steps
└── <gameline>/<type>/           detail.html, form.html, list.html,
                                 display_includes/, form_include.html
```

Every registered location type names its own `detail`, `list`, `create` and `update`
templates in [`locations/registry.py`](../registry.py); create and update share the
type's `form.html`. The registry views still append the shared fallbacks
(`core/registry/<action>.html`), which apply only if a named template is missing.
List templates render only for staff (see
[views and URLs](views-and-urls.md#access-policies)).

## Shells

### Detail: `locations/core/location/detail.html`

Extends `core/tl_base.html`; every location detail page extends it. The cover shows
the type and gameline, "Located in" chains from `LocationModel.containment_chains()`,
the owner and status. Blocks:

| Area | Blocks |
|------|--------|
| Cover | `cover_rank` (dots under the name), `cover_sub` (line under the name), `type_facts` (rows between "Located in" and "Owner"), `cover_facts` (the whole fact list) |
| Pages | Numbered sections in this order: `barriers`, `model_specific`, `reality_zone`, `additional_content`, `description`, `post_content` (scenes at this place) |

Each block renders zero or more `<section class="tl-section [tl-span-N]">` with an
empty `.tl-section__num`; CSS counters number them. The barriers and scenes sections
come from `core/location/display_includes/barriers.html` and `scenes.html`.

### Form: `locations/core/tl_form.html` and `locations/core/location/form.html`

`tl_form.html` extends `core/form.html` and is the shell for every location form and
wizard step: cover, Save and Cancel, the error summary and the submit or approval
actions. Set the `form_line` block (for example `mta`) so the cover takes the
gameline colour before the object exists.

`location/form.html` extends it with a standard layout. Override these blocks:
`name` and `contained_within` (the first row), `gauntlets` (the Barriers group, shown
only when the form has a barrier field), `reality_zone`, `other`, `description` and
`post_description`. Set the heading with `creation_title`.

### List: `locations/core/tl_list.html`

Extends `core/tl_base.html`. The cover uses the registry's `list_title` and
`list_heading`. Blocks: `create` (cover button), `list_head` (`<th>` after Name),
`list_cells` (`<td>` for each `obj`), `name_note` (lines under the name) and `empty`.

## Partials in `locations/tl/`

| Template | Use |
|----------|-----|
| `field.html` | One form field, or nothing when the form lacks it; checkboxes become check rows, textareas and multiple selects take a full row; `label=`, `help=`, `full=True` |
| `fields.html` | Every field of `fields_form` in order, as a two-column grid |
| `kv.html` | Key/value row: `label=`, `value=` |
| `stat.html` | Numeric stat: `label=`, `value=`, optional `of=` (maximum), `note=`, `text=True` |
| `faction_fact.html` | Cover row for a Mage faction chain, from `object.faction` |
| `person_row.html` | One character row (`person`) |
| `step_row.html` | One row of a wizard's step list: `at=`, `step=`, `label=`, optional `tag=` |
| `tree_node.html`, `tree_row.html` | The staff index tree: one node and its children, recursively |
| `containers_cell.html` | The containers of a place, for list cells |

## Mage templates

| Template | Purpose |
|----------|---------|
| `mage/node/form_include.html` | `NodeForm` fields and its three formsets (merits and flaws, Resonance, reality zone). Formset rows carry their hidden id and parent inputs so an edit updates existing ratings. |
| `mage/library/form_include.html` | `LibraryForm` fields; `books` only on the edit form |
| `mage/sanctum/form_include.html` | `SanctumForm` fields and reality zone |
| `mage/demesne/form_include.html` | `DemesneForm` fields and reality zone |
| `mage/paradox_realm/form_include.html` | `ParadoxRealmForm` fields and the obstacle and atmosphere formsets |
| `mage/tl/zone_formset.html` | The reality zone practice rows (`formset=form.reality_zone_formset`); renders nothing when the form has no zone formset |
| `mage/chantry/basics.html` | Wizard entry (`ChantryCreateForm`); links storytellers to the direct form |
| `mage/chantry/locgen.html` | Wizard steps 1–6: step heading ("Step NN of 07"), points left, backgrounds and effects so far, then the step's form |
| `mage/chantry/point_spend_form.html` | Step 1 form (`ChantryPointForm`); keep the `example_wrap`, `note_wrap` and `display_alt_name_wrap` ids and their initial `d-none` for the conditional-fields script |
| `mage/chantry/effects_form.html` | Step 2 form (`ChantryEffectsForm`), with [`chantry-effects.js`](../static/locations/js/chantry-effects.js) |
| `mage/chantry/tl/steps.html` | The step list on the wizard cover |
| `mage/chantry/form.html` | Direct storyteller form; must render every field in `DIRECT_FORM_FIELDS`, since an omitted field is blanked on save |
| `mage/chantry/detail.html`, `tl/members.html`, `tl/integrated_effects.html`, `tl/effect_rows.html` | Chantry page: personnel, effects |
| `mage/chantry/select_or_create_form.html` | Chantry step of the Mage-family character wizards (`ChantrySelectOrCreateForm`); keep the `data-create-or-select-container` blocks and their initial `d-none` |

The wizard and form includes read `object_perms.can_chargen` (added to template
contexts by the authorization middleware) to decide whether to show the form.

## Changeling freehold templates

| Template | Purpose |
|----------|---------|
| `changeling/freehold/chargen/base.html` | Wizard step shell: the draft's name and the four steps on the cover, "Step 0N of 04"; children set `step_at`, `step_label`, `submit_label` and `contents` |
| `chargen/basics.html`, `features.html`, `powers.html`, `details.html` | The four steps; Features loads [`freehold-features.js`](../static/locations/js/freehold-features.js), Powers loads [`freehold-powers.js`](../static/locations/js/freehold-powers.js) |
| `changeling/freehold/form.html` | Direct form, with [`freehold-form.js`](../static/locations/js/freehold-form.js) |
| `changeling/freehold/tl/guide.html` | Collapsible rules reminders; pass `archetypes=True`, `powers=True`, `features=True`, `about=True` or `quirks=True` |
| `changeling/freehold/display_includes/` | Detail sections: basics, features, powers |

## Templates used by other apps

The Mage-family character wizards map background steps to these includes in
`characters/chargen/definitions.py`:

| Background | Template |
|------------|----------|
| Node | `locations/mage/node/form_include.html` |
| Library | `locations/mage/library/form_include.html` |
| Sanctum | `locations/mage/sanctum/form_include.html` |
| Chantry | `locations/mage/chantry/select_or_create_form.html` |

In that context `current_background` is the background rating being detailed, and the
includes show its rating in their instructions.

## Conventions

- Load `{% load tl %}` (and `sanitize_text` for user text); use the `tl` tags for dots
  and traits.
- Do not add inline `style=""` attributes or Bootstrap classes;
  `core/tests/test_template_policy.py` fails when the number of inline styles grows.
- Keep the element ids and data attributes the JavaScript files and formset manager
  depend on (listed above) when editing a form include.

## See also

- [Frontend](../../docs/architecture/frontend.md)
- [Template tags reference](../../docs/reference/template-tags.md)
- [Location forms](forms.md)
- [Chantries](chantries.md) and [freeholds](freeholds.md)
- [items templates](../../items/docs/templates.md)
