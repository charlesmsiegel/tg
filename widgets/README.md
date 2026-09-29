# widgets

The `widgets` app holds the project's reusable form components: cascading ("chained")
selects, declarative show/hide rules for form fields, a create-or-select toggle,
clickable dot ratings, selects whose options carry metadata, dynamic formsets and a
client-side list filter. Each component is a Django widget, field, form mixin or
template tag on the server plus a small plain-JavaScript manager in
[`static/widgets/`](static/widgets/). It has no models.

Read this before you build a form with dependent fields or repeating rows; the pages
under [`docs/`](docs/) are the detailed reference.

## Main concepts

- **Media, not inline scripts.** Widgets declare their JavaScript through Django `Media`.
  The Spread base template renders the combined media of every form and formset on the
  page once, through the `{% page_media %}` tag. Configuration travels as inert JSON in
  `<script type="application/json">` tags, never as executable inline script. See
  [widgets](docs/widgets.md#page-media).
- **Progressive enhancement.** The real form controls (a `<select>`, a number input, a
  checkbox) always post the value. JavaScript only changes what is shown.
- **Two ways to fill a chained child select.** An embedded choice tree or the JSON
  endpoint for classic pages, or htmx requests to the page's own URL on interactive
  chargen pages. See [chained selects](docs/chained-selects.md).
- **Same rules on both sides.** `ConditionalFieldsMixin` evaluates visibility rules in the
  browser (`conditional.js`) and on the server (`field_visibility()`) with the same
  semantics.

## Key modules

| Path | Responsibility |
|------|----------------|
| [`__init__.py`](__init__.py) | Public exports: `ChainedSelect`, `CreateOrSelectWidget`, `OptionMetadataSelect`, `ChainedChoiceField`, `ChainedModelChoiceField`, `CreateOrSelectField`, `ChainedSelectMixin`, `ConditionalFieldsMixin`, `CreateOrSelectMixin`, `auto_chained_ajax_view`, `render_filterable_list_script` |
| [`fields/`](fields/) | `ChainedChoiceField`, `ChainedModelChoiceField`, `CreateOrSelectField` |
| [`mixins/`](mixins/) | `ChainedSelectMixin`, `ConditionalFieldsMixin`, `CreateOrSelectMixin` (form mixins) |
| [`widgets/`](widgets/) | `ChainedSelect`, `HtmxChainedSelect`, `CreateOrSelectWidget`, `DotRatingInput`, `OptionMetadataSelect`, script helpers for the formset manager and filterable list |
| [`templatetags/`](templatetags/) | `widget_media` (`{% page_media %}`), `formset_tags` (`{% formset %}`), `filterable_list` |
| [`views.py`](views.py) | `auto_chained_ajax_view`: the chained-select JSON endpoint |
| [`apps.py`](apps.py) | `WidgetsConfig.ready()` adds the endpoint's URL to the root URLconf |
| [`utils.py`](utils.py) | `config_script()` (inert JSON script tag), `normalize_choices()` |
| [`templates/widgets/dot_rating.html`](templates/widgets/dot_rating.html) | Markup of `DotRatingInput` |
| [`static/widgets/`](static/widgets/) | `chained.js`, `conditional.js`, `create_or_select.js`, `dot_rating.js`, `filterable.js`, `formset_manager.js`, `metadata_select.js` |
| [`tests/`](tests/) | Python tests per component, endpoint authorization, static-asset contracts and optional real-browser tests |

## How it connects to other apps

- `core/templates/core/tl_base.html` ends with `{% load widget_media %}{% page_media %}`,
  so every Spread page loads the media its forms need.
- `core.views.generic.MultipleFormsetsMixin` exposes formsets in the shape
  `{% page_media %}` recognises and uses the formset manager conventions.
- `characters` uses the chained, conditional and dot-rating components for character
  creation (`characters/forms/core/chained_freebies.py`,
  `characters/views/core/chargen_mixins.py`, the Mage forms); `locations` and `items`
  use chained selects, conditional fields, create-or-select and `{% formset %}` in their
  creation and Mage forms and templates.
- The endpoint's route policy is `WIDGET` in
  [`core/route_policy_manifest.py`](../core/route_policy_manifest.py).

## Documentation

| Page | Covers |
|------|--------|
| [widgets.md](docs/widgets.md) | Every widget, field, mixin and template tag; `{% page_media %}` |
| [chained-selects.md](docs/chained-selects.md) | Chained selects in depth: embedded tree, JSON endpoint, htmx mode, validation |
| [javascript.md](docs/javascript.md) | The browser managers: data attributes, events and global APIs |

## See also

- [Frontend architecture](../docs/architecture/frontend.md)
- [Character creation](../docs/architecture/character-creation.md)
- [Core templates and static files](../core/docs/templates-and-static.md)
- [core app](../core/README.md)
