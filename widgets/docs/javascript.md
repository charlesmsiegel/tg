# Widget JavaScript

This page describes the browser side of the `widgets` app: the seven scripts in
[`static/widgets/`](../static/widgets/), the markup each one looks for, the events they
fire and the global objects they expose. It is for developers writing templates that use
these components or scripts that talk to them. The server side is in
[widgets](widgets.md) and [chained selects](chained-selects.md).

## Common behaviour

- Each script is plain JavaScript with no dependencies, wrapped in an IIFE, and safe to
  load more than once: it returns early if its global already exists.
- Each initialises on `DOMContentLoaded` (or at once if the document has loaded) and
  again after `htmx:afterSwap`, so content swapped in by htmx is enhanced. Most also
  re-initialise on `turbo:render` and `turbo:frame-load`.
- Each marks the elements it has set up (a `WeakSet` or a `data-*` flag), so calling
  `init()` again only picks up new elements.
- Configuration is read from `data-*` attributes and from inert
  `<script type="application/json">` tags; none of the scripts evaluates code from the
  page.
- Scripts are loaded through Django `Media` and `{% page_media %}` (see
  [widgets](widgets.md#page-media)); do not add `<script>` tags for them by hand.

| Script | Global | Loaded by |
|--------|--------|-----------|
| `chained.js` | `window.ChainedSelect` | `ChainedSelect` widget media |
| `conditional.js` | `window.ConditionalFields` | `ConditionalFieldsMixin.media` (not in htmx mode) |
| `create_or_select.js` | `window.CreateOrSelect` | `CreateOrSelectWidget` media |
| `dot_rating.js` | `window.TGDots` | `DotRatingInput(alpine=False)` media |
| `metadata_select.js` | `window.OptionMetadata` | `OptionMetadataSelect` media |
| `formset_manager.js` | `window.FormsetManager` | `{% formset %}`, `{% formset_script %}`, any formset in the context |
| `filterable.js` | `window.FilterableList` | `{% filterable_list_script %}` |

## Chained selects

`chained.js` handles selects with `data-chained-select`:

| Attribute | Meaning |
|-----------|---------|
| `data-chain-name` | The chain the select belongs to |
| `data-chain-position` | Its position (0 = root) |
| `data-parent-field` | The parent field name |
| `data-ajax-url`, `data-form-path` | Fetch options from the endpoint instead of the tree |
| `data-empty-label` | Label of the empty option |

Trees come from `<script type="application/json" data-chain-tree="<chain name>">`,
keyed `"<parent field>:<parent value>"`. A field's name is taken from the select's
`name` (or `id`) after the last `-`, so formset prefixes do not matter.

When a select changes, the next select in the chain is filled (from the tree, or by
`fetch` from the endpoint with `field`, `parent_value` and `form` parameters, showing
"Loading..." and disabling the select meanwhile) and every select further down is reset
to its empty option. Options get `data-*` attributes from each choice's `metadata`. The
filled select fires `change` so the chain continues and conditional rules re-run. A
failed request shows "Error loading".

API: `ChainedSelect.init()`, `ChainedSelect.setValue(chainName, fieldName, value)`,
`ChainedSelect.getValues(chainName)`.

On interactive chargen pages chained selects use htmx attributes instead (see
[chained selects](chained-selects.md#htmx-mode)) and `chained.js` is not loaded.

## Conditional fields

`conditional.js` reads every `<script type="application/json" data-conditional-rules>`
(`{"rules": ..., "context": ...}`, from `form.conditional_js`), merges them, and
re-applies all rules when a source field fires `change` or `metadata:change`. Source
fields are found by id `id_<field>`, so the scheme only works for unprefixed forms.
For each rule it adds or removes the `d-none` class on the element with id
`wrapper_id` or `<field>_wrap`. The semantics match
`ConditionalFieldsMixin.field_visibility()` (see
[widgets](widgets.md#conditional-fields-conditionalfieldsmixin)).

Metadata for `metadata_is` and `metadata_truthy` comes from `OptionMetadata.get()` when
that script is present, else from the selected option's `dataset`.

`ConditionalFields.init()` does its work only on the first call; rules that arrive later
in a swapped fragment are not picked up.

## Create or select

`create_or_select.js` finds checkboxes with `data-create-or-select-toggle` and, for each
`data-create-or-select-group` value, the two containers
`[data-create-or-select-container="<group>"][data-create-or-select-mode="select"]` and
`[...][data-create-or-select-mode="create"]`. Checked shows the create container and
hides the select container (with `d-none`); unchecked does the reverse. A toggle without
both containers logs a warning and is left alone. It also re-initialises on
`formset:widgetsInit`.

API: `CreateOrSelect.setMode(group, createMode)`, `CreateOrSelect.getMode(group)`.

## Dot ratings

`dot_rating.js` enhances `[data-dot-rating][data-min][data-max]` containers holding a
number `<input>` and a hidden `.tg-dot-buttons` group of `button.tg-dot[data-value]`:

- enhancing hides the input and shows the dots;
- clicking dot *n* sets the rating to *n*, or to *n* − 1 when *n* is already the value
  (so a dot can be cleared), clamped to `data-min`..`data-max`, then fires `input` and
  `change` on the input so totals and validators update;
- typing in the input, or a script changing it and firing `input`/`change`, repaints the
  dots (`is-filled`, `aria-pressed`).

Click, input and change listeners are delegated to `document`. API:
`TGDots.enhance(root)`, `TGDots.paint(control)`.

With `DotRatingInput(alpine=True)` the same markup is driven by the Alpine component
`tgDots` in `characters/static/characters/js/chargen-components.js` instead.

## Option metadata

`metadata_select.js` watches selects with `data-metadata-select` and, on change (and on
load when a value is selected), dispatches a bubbling `metadata:change` event with
`detail = {value, metadata, select}`, where `metadata` is the selected option's
`dataset`. `chained.js` also fires it through this script after refilling a select.

API: `OptionMetadata.get(selectOrSelector)`, `OptionMetadata.isTrue(select, key)`
(`"true"`, `"True"` or `true`), `OptionMetadata.getField(select, key, default)`,
`OptionMetadata.fireMetadataChange(select)`.

## Formsets

`formset_manager.js` manages `[data-formset-container][data-formset-prefix]` containers.

| Markup | Meaning |
|--------|---------|
| `data-formset-container`, `data-formset-prefix="<prefix>"` | The container rows are appended to |
| `data-formset-empty-form="<id>"` | Id of the empty-form template (default `empty_<prefix>_form`) |
| `data-formset-animate="true"` | Fade rows in and out |
| `data-formset-add="<prefix>"` | Add button |
| `data-formset-remove="<prefix>"` | Remove button inside a row |
| `data-formset-form` | A row |

**Add** copies the empty form's inner HTML, replaces `__prefix__` with the current
`TOTAL_FORMS` value, appends the row, increments `id_<prefix>-TOTAL_FORMS`, re-runs
`ChainedSelect.init()` and `ConditionalFields.init()`, and dispatches `formset:widgetsInit`
on the row and `formset:added` (`detail = {prefix, index, form}`) on the container.

**Remove** finds the row (`[data-formset-form]`, or a few fallbacks). If the row has a
`-DELETE` checkbox (a saved record), it ticks it and hides the row, so Django deletes the
record on save. Otherwise it removes the row, renumbers every remaining row (hidden
deleted rows included, since they are still submitted) to `0..n-1` in their `name`,
`id`, `label[for]` and `data-prefix` values, and sets `TOTAL_FORMS` to `n`. It
dispatches `formset:removed` (`detail = {prefix, form, deleted}`) on `document`.

API: `FormsetManager.init()`, `FormsetManager.addForm(prefix)`,
`FormsetManager.addForms(prefix, count)`, `FormsetManager.getFormCount(prefix)`.

The empty form, container and button ids follow the conventions of
`core.views.generic.MultipleFormsetsMixin` (`<prefix>_formset`, `empty_<prefix>_form`).

## Filterable lists

`filterable.js` filters `[data-filterable-list="<name>"]` containers holding
`[data-filterable-item]` elements. Controls can be anywhere on the page:

| Attribute | On | Filter |
|-----------|----|--------|
| `data-filter-input="field"` | text input | Item's `data-field` contains the text (case-insensitive) |
| `data-filter-select="field"` | select | Item's `data-field` equals the value; with `data-filter-match="token"`, one of its space-separated words equals it |
| `data-filter-checkbox="field"` | checkbox (`value`) | Item has `data-field="<value>"` or a `data-field-<value>="true"`-style flag; the mode comes from the nearest `data-filter-mode` (`all`, default; `any`; `none`) |
| `data-filter-max="field"` | number input | Item's `data-field` is at most the value |
| `data-filter-clear` | button | Clears every control |
| `data-filter-count` | element | Shows "X of Y shown" |
| `data-filter-no-results` | element | Shown when nothing matches; start it with `hidden` |

Hidden items get `display: none`. Controls may add `data-filter-list="<name>"`, but every
control on the page applies to every list, so use one filterable list per page.

## See also

- [Widgets](widgets.md)
- [Chained selects](chained-selects.md)
- [Frontend architecture](../../docs/architecture/frontend.md)
- [Core `tl.js`](../../core/docs/templates-and-static.md#tljs)
