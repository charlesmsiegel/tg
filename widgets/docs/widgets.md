# Widgets, fields, mixins and tags

This page is the reference for every server-side component in the `widgets` app: what
it renders, which options it takes, what JavaScript it declares and how a form or
template uses it. It is for developers building forms. Chained selects have their own
page ([chained selects](chained-selects.md)); the browser side is in
[JavaScript](javascript.md).

## Page media

Widgets declare their scripts through Django `Media`. You do not add `<script>` tags for
them: [`core/tl_base.html`](../../core/templates/core/tl_base.html) ends with

```django
{% load widget_media %}
{% page_media %}
```

and `page_media` (in [`templatetags/widget_media.py`](../templatetags/widget_media.py))
renders one combined, de-duplicated `Media` for the page. It collects:

1. Media registered during the current render by other tags through
   `register_media(context, media)`: `{% formset %}`, `{% formset_script %}` and
   `{% filterable_list_script %}` use it.
2. The `media` of every form (`forms.BaseForm`) among the context's values.
3. For every formset (`BaseFormSet`) among the context's values, or under the key
   `"formset"` of a dict value (the shape `MultipleFormsetsMixin` produces), the
   formset's media, its empty form's media and `widgets/formset_manager.js`.

`page_media` looks only at those shapes. It skips context values that are Django
`LazyObject`s (such as `csrf_token` and `user`) without evaluating them: an `isinstance`
check on the lazy `csrf_token` would evaluate it and set a CSRF cookie on every page,
which would also stop anonymous pages from being shared by the page cache (see
[core utilities](../../core/docs/utilities.md#caching)).

Registered media is stored on the render context frame of the outermost template
render, so includes can register media and the base template still sees it, and a
reused `Context` does not leak media into another response.

A template rendered on its own (an htmx fragment, a standalone page that does not
extend `tl_base.html`) must render the media itself, with `{{ form.media }}` or by
ending with `{% load widget_media %}{% page_media %}`.

## Chained selects

`ChainedChoiceField`, `ChainedModelChoiceField`, `ChainedSelect`, `HtmxChainedSelect`
and `ChainedSelectMixin` build cascading dropdowns (affiliation, then faction, then
subfaction). See [chained selects](chained-selects.md).

## Conditional fields: `ConditionalFieldsMixin`

[`mixins/conditional.py`](../mixins/conditional.py). A form mixin that shows or hides
fields based on other fields' values, their selected option's metadata or context
variables, from one declarative rule set.

```python
# characters/forms/core/chained_freebies.py (abridged)
BASE_CONDITIONAL_FIELDS = {
    "example": {
        "hidden_when": {
            "category": {"value_in": ["-----", "Willpower", "Quintessence", "Rotes", "Resonance"]}
        },
    },
    "value": {"visible_when": {"category": {"value_is": "MeritFlaw"}}},
    "pooled": {
        "visible_when": {
            "category": {"value_is": "Background"},
            "example": {"metadata_truthy": "poolable"},
            "_context": {"is_group_member": True},
        },
    },
}


class ChainedHumanFreebiesForm(ConditionalFieldsMixin, ChainedSelectMixin, forms.Form):
    def get_conditional_context(self):
        context = super().get_conditional_context()
        if self.instance:
            context["is_group_member"] = getattr(self.instance, "is_group_member", False)
        return context

    def get_conditional_rules(self):
        return dict(BASE_CONDITIONAL_FIELDS)
```

Rule keys per target field:

| Key | Meaning |
|-----|---------|
| `visible_when` | `{source: checks}`; the field is visible only when **every** check holds |
| `hidden_when` | Same format; the field is hidden when **any** check holds (evaluated only if still visible) |
| `wrapper_id` | Element id to show or hide in the browser (default `<field>_wrap`) |
| `initially_hidden` | Used by `wrap_field()` (default `True`) |

Checks on a source field: `value_is`, `value_in`, `value_not_in`, `checked_is` (for a
checkbox; other checks on the same source are then ignored), `metadata_is` (`{key:
value}` compared as strings against the selected option's metadata) and
`metadata_truthy` (`"key"`, true when the value is `"true"`, `"True"` or `True`). The
special source `_context` compares `get_conditional_context()` values with `==`. A
source that is not a field of the form fails its check.

| Method or attribute | Purpose |
|---------------------|---------|
| `conditional_fields` / `get_conditional_rules()` | The rules; override the method for dynamic rules |
| `conditional_context` / `get_conditional_context()` | Values for `_context` checks; also settable with the `conditional_context=` form kwarg |
| `conditional_js()` | The rules and context as an inert JSON script tag (`data-conditional-rules`) for `conditional.js`. Render it in the template: `{{ form.conditional_js }}` |
| `media` | Adds `widgets/conditional.js`, except in htmx mode |
| `field_visibility(values)` | `{field: bool}` for a dict of submitted string values, with the same semantics as the browser |
| `current_values()` | The values the browser would read now (bound data, or initial values, with an unselected select counted as its first option) |
| `visibility`, `visibility_json()` | `field_visibility(current_values())`, as a dict or JSON |
| `wrap_field(name, label_prefix="")` | `<div id="<name>_wrap" class="col-sm[ d-none]">` around the field |

The browser manager shows and hides the wrapper by toggling the `d-none` class, which
`tl.css` keeps as `display: none` (`.tl .d-none`). Give each conditional field a wrapper with the right
id, starting with `d-none` when it should start hidden.

In htmx mode (after `ChainedSelectMixin.enable_htmx_chains()`), the form's media and
`conditional_js()` leave the browser manager out; the server computes visibility with
`field_visibility()` and the chargen views send it to the page as a `tg-visibility`
event (see [chained selects](chained-selects.md#htmx-mode)).

## Create or select

[`fields/create_or_select.py`](../fields/create_or_select.py),
[`mixins/create_or_select.py`](../mixins/create_or_select.py),
[`widgets/create_or_select.py`](../widgets/create_or_select.py). For a ModelForm that
either picks an existing object or creates a new one (an effect, an artifact, a chantry).

```python
# items/forms/mage/sorcerer_artifact.py (abridged)
class ArtifactCreateOrSelectForm(CreateOrSelectMixin, forms.ModelForm):
    create_or_select_config = {
        "toggle_field": "select_or_create",
        "select_field": "select",
        "error_message": "You must either select an existing Artifact or choose to create a new one.",
    }

    select_or_create = CreateOrSelectField(label="Create new Artifact?")
    select = forms.ModelChoiceField(queryset=SorcererArtifact.objects.all(), required=False)

    class Meta:
        model = SorcererArtifact
        fields = ["select_or_create", "select", "name", "rank", "description"]
```

- `CreateOrSelectField` is a non-required `BooleanField` (true means "create") whose
  widget is `CreateOrSelectWidget(group_name=...)`.
- `CreateOrSelectWidget` is a checkbox that adds `data-create-or-select-toggle` and
  `data-create-or-select-group` (the `group_name`, or the field's HTML name) and declares
  `widgets/create_or_select.js`.
- `CreateOrSelectMixin` reads `create_or_select_config` (`toggle_field`, default
  `select_or_create`; `select_field`, default `select`; `error_message`):
  - `clean()` adds `error_message` to the select field when neither mode is chosen;
  - `_post_clean()` skips model validation in select mode and sets `self.instance` to the
    selected object;
  - `save()` returns the selected object in select mode, otherwise saves a new instance;
  - `is_creating()` and `get_selected_object()` report the mode.

In the template, mark the two containers with the same group name:

```django
{% include "core/misc/check.html" with field=form.select_or_create %}
<div data-create-or-select-container="{{ form.select_or_create.html_name }}" data-create-or-select-mode="select">
    {% include "core/tl/field.html" with field=form.select %}
</div>
<div data-create-or-select-container="{{ form.select_or_create.html_name }}" data-create-or-select-mode="create" class="d-none">
    {% include "core/tl/field.html" with field=form.name %}
</div>
```

## Dot rating: `DotRatingInput`

[`widgets/dots.py`](../widgets/dots.py). A `NumberInput` rendered with clickable dots
(`widgets/dot_rating.html`). The number input stays the form control, so the form posts
the same value with or without JavaScript.

`DotRatingInput(*, minimum=0, maximum=5, label="", alpine=True, attrs=None)`:

- `alpine=True`: the markup is driven by the Alpine component `tgDots` (defined in
  `characters/static/characters/js/chargen-components.js`), and the widget declares no
  media. Use it only on pages that load Alpine (the interactive chargen pages).
- `alpine=False`: the markup carries `data-dot-rating` and the widget declares
  `widgets/dot_rating.js`, which works on any page.

`label` (default: the field name in title case) labels the button group; `minimum` and
`maximum` bound the rating. The chargen views swap bounded number fields to this widget
with `characters.views.core.chargen_mixins.use_dot_widgets()`.

## Option metadata: `OptionMetadataSelect`

[`widgets/metadata_select.py`](../widgets/metadata_select.py). A `Select` whose choices
may be 3-tuples `(value, label, {key: value})`. Each metadata item becomes a
`data-<key>` attribute on its `<option>`; the select gets `data-metadata-select` and the
widget declares `widgets/metadata_select.js`, which fires a `metadata:change` event and
offers `OptionMetadata.get()`. `metadata_fields` is accepted and stored but not applied
to model choices. No form in the project uses this widget at present; chained selects
carry option metadata themselves (see [chained selects](chained-selects.md)).

## Dynamic formsets: `{% formset %}`

[`templatetags/formset_tags.py`](../templatetags/formset_tags.py). A block tag that
renders a whole formset with add and remove buttons driven by
`widgets/formset_manager.js`.

```django
{% load formset_tags %}
{# characters/templates/characters/core/background_block/form.html (abridged) #}
{% formset form prefix="backgrounds" add_label="+ Add background" add_class="tl-btn tl-btn--ghost tl-btn--sm" remove_class="tl-btn tl-btn--quiet" wrapper_class="tl-bgrow" %}
    {% for hidden in subform.hidden_fields %}{{ hidden }}{% endfor %}
    {% include "core/tl/field.html" with field=subform.bg label="Background" help="" %}
    {% include "core/tl/field.html" with field=subform.rating label="Rating" help="" %}
{% endformset %}
```

It renders the management form, a container `<div id="<prefix>_formset"
data-formset-container data-formset-prefix="<prefix>">` with one row per form, a hidden
`<div id="empty_<prefix>_form" class="d-none">` holding the empty form's row, and an add
button (`data-formset-add`). Inside the block the current form is `subform` (also
`form`). Each row is `<div class="<wrapper_class>" data-formset-form>` followed by a
remove button (`data-formset-remove`) unless `show_remove=False`. It registers the
formset's media, the empty form's media and `formset_manager.js` for `{% page_media %}`.

| Argument | Default |
|----------|---------|
| first argument | The formset (required) |
| `prefix` | `formset.prefix` |
| `add_label` / `add_class` | `"Add"` / `""` |
| `remove_label` / `remove_class` | `"Remove"` / `"tg-btn btn-danger btn-sm"` |
| `wrapper_class` | `"form-row"` |
| `show_remove` | `True` |
| `animate` | `False` (adds `data-formset-animate`) |

Arguments must be `key=value`; quoted values are strings, `True`/`False` are booleans,
anything else is a template variable. Label and class values are inserted into the HTML
without escaping, so pass only literals from templates.

For hand-built markup, the library also has `{% formset_script %}` (register the
manager's media), `{% formset_container prefix empty_form_id=None animate=False %}`
(container data attributes), `{% formset_add_btn prefix label="Add" **attrs %}` and
`{% formset_form_wrapper %}` (the `data-formset-form` attribute). The Mage wonder form
templates in `items` use these. `widgets.widgets.render_formset_manager_script()` returns
the manager's `<script>` tag for code that needs it outside a template.

## Filterable lists

[`widgets/filterable.py`](../widgets/filterable.py) and
[`templatetags/filterable_list.py`](../templatetags/filterable_list.py). A client-side
filter for a server-rendered list, configured entirely with data attributes (listed in
[JavaScript](javascript.md#filterable-lists)). Load the script with:

```django
{% load filterable_list %}
{% filterable_list_script %}
```

The tag registers `widgets/filterable.js` for `{% page_media %}` and outputs nothing.
`render_filterable_list_script()` returns the `<script>` tag directly. The characters
reference list shells (`characters/tl/reference_list.html`, `characters/tl/ref2_list.html`)
use it.

## Helpers

[`utils.py`](../utils.py):

- `config_script(value, **attrs)` returns `json_script(value)` with extra attributes on
  the `<script>` tag (for example `data-chain-tree="chain_0"`). The JSON is escaped for
  HTML and has type `application/json`, so it never runs.
- `normalize_choices(choices)` turns 2-tuples, 3-tuples with metadata or model instances
  into `[{"value", "label"[, "metadata"]}]` with string values; the JSON endpoint uses it.

## See also

- [Chained selects](chained-selects.md)
- [JavaScript](javascript.md)
- [Core templates and static files](../../core/docs/templates-and-static.md)
- [`core.views.generic.MultipleFormsetsMixin`](../../core/docs/views.md#multipleformsetsmixin)
- [Frontend architecture](../../docs/architecture/frontend.md)
