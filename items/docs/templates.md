# Item templates

This page describes how the `items` templates are organised, which shared shells and
blocks each item page builds on, how a view picks its template, and which templates
other apps include. It is for developers styling or adding item pages. The design
system itself (Spread, the `tl` tags, gameline theming) is covered in
[frontend](../../docs/architecture/frontend.md).

## Layout

Templates live in [`items/templates/items/`](../templates/items/):

```text
items/
├── index.html                     staff index (ItemIndexView)
├── tl/                            shared item partials and shells
├── core/item/                     item detail shell and the plain item form
├── core/<type>/                   weapon, material, medium pages
└── <gameline>/<type>/             detail.html, form.html, list.html,
                                   display_includes/, form_include.html
```

A type folder usually holds `detail.html` and `form.html`; a few also have
`list.html` and `display_includes/` partials.

## How a view picks its template

Each registry spec names a template per action in its `templates` dict (see
[`items/registry.py`](../registry.py)). `RegistryViewMixin.get_template_names()`
appends a shared fallback after the view's own names, using
`core.template_resolution.shared_template_names()`:

| Action | Fallback |
|--------|----------|
| detail | `core/registry/detail.html` |
| list | `core/registry/list.html` |
| create, update | `core/registry/form.html` |

Django renders the first template that exists, so a type without its own template
still gets a working page. These item types have their own list template:
`MummyRelic`, `Vessel`, `Ushabti`, `Dross`, `Material`, `Medium`, `HunterGear` and
`HunterRelic`. `ItemModel` uses `core/registry/object_list.html` (plain names). The
remaining types use `core/registry/list.html`. List pages are rendered only for staff;
everyone else gets `core/public_object_list.html` (see
[views and URLs](views-and-urls.md#access-policies)).

Several types share a template: `MeleeWeapon`, `ThrownWeapon` and `Weapon` use
`items/core/weapon/detail.html`; `Talen`'s form extends `Fetish`'s.

## Shared shells

### Detail: `items/core/item/detail.html`

Extends `core/tl_base.html`. Every item detail page extends it, directly or through
`items/mage/wonder/detail.html` or `items/core/weapon/detail.html`. It sets the
gameline theme from the object (`{{ object|gameline_code }}`), links back to
`items:index`, and exposes these blocks:

| Area | Blocks |
|------|--------|
| Cover | `cover_stamp` (beside the eyebrow), `cover_sub` (under the name), `cover_facts` with the rows `owned_by`, `owner`, `chronicle`, `status`/`status_fact`, `sources`; `cover_stats` (numbers above the edit button) |
| Pages | Sections filled in this order: `status_row`, `model_specific`, `contents` (containing `additional_stats`), `description`, `post_content` |

Each section is a `<section class="tl-section">` with an empty
`.tl-section__num`; CSS counters number them. A section spans the full width unless
it carries a `tl-span-N` class.

### Wonder detail: `items/mage/wonder/detail.html`

Extends the item shell for every Wonder and for Fetish and Talen. `status_row` shows
the Wonder basics; `contents` holds `creation`, `resonance` (the shared
`characters/tl/resonance.html`) and `powers`. Artifact, Charm and Talisman override
`powers`; Fetish replaces `status_row` with the background cost only and empties
`resonance`. `items/mage/grimoire/detail.html` adds the bibliographic cover facts, the
contents strip and the teachings sections.

### Form: `items/tl/form.html`

Extends `core/form.html`. Every item form extends it. Children fill `contents` with
Spread fields: `{% include "core/tl/field.html" with field=form.x %}` inside a
`.tl-formgrid`, `core/misc/check.html` for checkboxes, `.tl-section` for groups. When
creating, the cover takes the gameline from `view.registry_spec.gameline`; when
editing, from the object. Errors use `core/misc/form_errors.html`. Set the page
heading with the `creation_title` block.

`items/core/item/form.html` checks each field before rendering it, because owners
editing without a scoped editor role receive `LimitedItemEditForm` (description,
public info, image) instead of the full form.

### List: `items/tl/list.html`

Extends `core/tl_base.html`. Children set `title`, `gameline`, `eyebrow`, `heading`,
`columns` (`<th>` cells after Name), `row` (`<td>` cells for each `obj`),
`create_action` and `empty`.

## Partials in `items/tl/`

| Template | Use |
|----------|-----|
| `stat.html` | One numeric stat: `{% include "items/tl/stat.html" with label="Background cost" value=object.background_cost %}`; `text=True` for word values, `note=` for a subscript |
| `effects.html` | Mage power section: `effect=` (one Effect) or `effects=` (a list), optional `arete=`; renders nothing when all are empty |
| `effect_card.html` | One Effect card (cost, name, description, Spheres above zero) |
| `wonder_fields.html` | The fields Wonder-like forms share (name, rank, background cost, maximum Quintessence, Arete, description); skips fields the form lacks |

## Wonder form

`items/mage/wonder/form_include.html` renders `WonderForm` (see
[forms](forms.md#wonderform)): type, rank, Arete, the Resonance rows
(`resonance_row.html`) and the power subforms (`effect_subform.html`). It loads
[`static/items/js/wonder-form.js`](../static/items/js/wonder-form.js), which
switches each power between "select an Effect" and "create an Effect".

Keep these hooks when editing it:

- `#resonance_formset`, `#empty_resonance_form`, `#effects_formset` and
  `#empty_effects_form` for the formset manager;
- `#id_wonder_type`, `#add-power`, and the `.effect-select-row` /
  `.effect-create-fields` classes inside each `[data-prefix]` subform for
  `wonder-form.js`.

The Wonder create and edit pages include it from `items/mage/wonder/form.html`. Mage,
MtA human and Companion character creation include it for their Wonder background
step (mapped in `characters/chargen/definitions.py`); there the context carries
`current_background`, and the lede shows the point budget (three times its rating).

## Templates used by other apps

| Template | Included by |
|----------|-------------|
| `items/mage/wonder/form_include.html` | Mage-family character creation, Wonder step |
| `items/mage/artifact/form_include.html` | Sorcerer character creation, Artifact step (`ArtifactCreateOrSelectForm`) |

## Conventions

- Load `{% load tl %}` (and `sanitize_text` when you print user text); use the `tl`
  tags such as `{% dots %}` and `{% trait %}` for ratings.
- Do not add inline `style=""` attributes or Bootstrap classes.
  `core/tests/test_template_policy.py` fails when the number of inline styles grows,
  and [`tests/views/test_spread_forms.py`](../tests/views/test_spread_forms.py) fails
  on legacy classes in item forms.
- When you add a form field, render it in the type's `form.html`; the Spread forms
  test fails on a field that is not rendered.

## See also

- [Frontend](../../docs/architecture/frontend.md)
- [Template tags reference](../../docs/reference/template-tags.md)
- [Item forms](forms.md)
- [Views and URLs](views-and-urls.md)
- [locations templates](../../locations/docs/templates.md)
