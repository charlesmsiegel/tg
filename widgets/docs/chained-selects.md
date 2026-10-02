# Chained selects

This page explains the cascading dropdowns in the `widgets` app: a child `<select>`
whose options depend on the value of its parent (affiliation, then faction, then
subfaction; category, then example, then value). It covers the fields, the form mixin,
the three ways a child gets its options, server-side validation and the JSON endpoint.
It is for developers writing forms with dependent choices.

## The pieces

| Piece | Where | Role |
|-------|-------|------|
| `ChainedChoiceField` | [`fields/chained.py`](../fields/chained.py) | A `ChoiceField` with `parent_field` and either `choices_map` or `choices_callback` |
| `ChainedModelChoiceField` | same | A `ModelChoiceField` with `parent_field` and `parent_fk`; `get_queryset_for_parent(value)` filters `queryset` on `{parent_fk: value}` |
| `ChainedSelect` | [`widgets/chained.py`](../widgets/chained.py) | The `<select>` for the classic (embedded tree or endpoint) modes; declares `widgets/chained.js` |
| `HtmxChainedSelect` | same | The `<select>` for htmx mode; declares no script |
| `ChainedSelectMixin` | [`mixins/chained.py`](../mixins/chained.py) | Links the fields of a form into chains, configures the widgets, populates children and validates |
| `auto_chained_ajax_view` | [`views.py`](../views.py) | JSON options for registered forms |

## Declaring a chain

```python
from widgets import ChainedChoiceField, ChainedSelectMixin


class OriginForm(ChainedSelectMixin, forms.Form):
    affiliation = ChainedChoiceField(
        choices=[("traditions", "Traditions"), ("technocracy", "Technocracy")]
    )
    faction = ChainedChoiceField(
        parent_field="affiliation",
        choices_map={
            "traditions": [("hermetic", "Order of Hermes")],
            "technocracy": [("iteration_x", "Iteration X")],
        },
    )
```

`ChainedChoiceField(*, parent_field=None, choices_map=None, choices_callback=None,
empty_label="---------", choices=(), **kwargs)`:

- A root field (no `parent_field`) uses `choices`; an empty choice with `empty_label` is
  prepended when missing.
- A child field starts with only the empty choice. `get_choices_for_parent(value)`
  returns the empty choice plus `choices_map[value]` (a non-string value such as a pk
  is looked up by its string form when that is a key) or, failing that, the result of
  `choices_callback(value)`.
- Choices may be 3-tuples `(value, label, {metadata})`. The metadata reaches the browser
  as `data-*` attributes on the options, where conditional rules can test it
  (`metadata_is`, `metadata_truthy`, see
  [widgets](widgets.md#conditional-fields-conditionalfieldsmixin)).
- `valid_value()` accepts any value for a child field; the mixin validates it against
  the parent in `clean()`.

## What `ChainedSelectMixin` does

On `__init__`, `_setup_chains()`:

1. Finds the chained fields and builds one chain per root: a chained field with no
   `parent_field`, followed by the child whose `parent_field` names it, and so on. Chains
   are named `chain_0`, `chain_1`, ... in field order.
2. Replaces each chain field's widget with a `ChainedSelect` if it is not one, and sets
   `chain_name`, `chain_position`, `parent_field` and `empty_label` on it.
3. Builds the choice tree for the chain: the root's choices under `_root`, and each
   child's `choices_map` under `"<parent field>:<parent value>"`. The tree is attached to
   the root widget, which renders it after itself as
   `<script type="application/json" data-chain-tree="chain_0">`.
4. If any field in the chain has a `choices_callback` and no `choices_map`, sets
   `ajax_url` (the form's `chained_ajax_url`, default `/__chained_select__/`) and
   `form_path` (`"<module>.<ClassName>"`) on the widgets of the callback fields.
5. Fills each child's choices from the bound value (or initial value; a model instance
   is reduced to its `pk`) of its parent, so a re-rendered form shows the right options.

`clean()` checks each chained child with a value: the value must be among
`get_choices_for_parent(<cleaned parent value>)`, else the field gets "Invalid
selection for the chosen `<parent>`." (code `invalid_choice`). Only
`ChainedChoiceField` children are checked this way; a `ChainedModelChoiceField` child is
validated only against its own `queryset`, so narrow that queryset yourself.

Because chains start at a chained field with no parent, a chain whose root is a plain
`ChoiceField` (as `category` is in the freebie forms) is not configured for the classic
modes. `chain_for(name)` follows `parent_field` links from any field and is what htmx
mode uses.

## Three ways to fill a child

### Embedded tree (default)

When every child has a `choices_map`, all options are in the page. `chained.js` reads
the tree and, when a parent changes, fills the next child from
`tree["<parent>:<value>"]` and resets the ones below it. No request is made.

### JSON endpoint

When a child has only a `choices_callback`, `chained.js` asks the server:

```text
GET /__chained_select__/?form=<form_path>&field=<child field>&parent_value=<id>
```

`WidgetsConfig.ready()` ([`apps.py`](../apps.py)) inserts this route at the start of the
root URLconf with the name `__chained_select_ajax__`, so no URL module lists it. Its
route policy is `WIDGET`: anonymous callers get `{"error": "Authentication required"}`
with status 401 from the middleware (and from the view itself).

`auto_chained_ajax_view` accepts GET only and answers only for forms and fields listed
in `widgets.views.REGISTERED_FORMS` (dotted form path to its chained fields). It never
imports a class named in the request: the registered path is resolved with `import_string`,
the form is built with the requesting user, and the form's own
`allowed_chained_parent(field_name, parent_id)` decides which parents it would offer that
user. The widgets app itself imports nothing from the other apps.

| Check | Failure |
|-------|---------|
| Signed in | 401 `{"error": "Authentication required"}` |
| `form` is registered and `field` is one of its allowed fields | 400 `{"error": "Unknown form or field"}` |
| `parent_value` is an ASCII decimal string of at most 20 digits and at least 1 | 400 `{"error": "Invalid parent"}` |
| The parent is one the form would offer this user | 400 `{"error": "Invalid parent"}` |

On success it builds the form through its registered factory (which receives the
request, so a form that needs `user` gets it), calls the field's `choices_callback` with
the parent id and returns `{"choices": [{"value", "label"[, "metadata"]}]}` (through
`normalize_choices`).

The only registered form is `characters.forms.mage.mage.MageCreationForm`, for the
fields `faction` and `subfaction`; its parent check requires the faction to hang off an
affiliation in the form's `affiliation` queryset. To register another form, add an
entry `"<module>.<Class>": (factory, frozenset({fields}))` and extend the parent check
for it; `widgets/tests/test_ajax_authorization.py` covers the contract.

### htmx mode

The interactive character-creation pages do not use `chained.js`. The chargen views
(`characters/views/core/chargen_mixins.py`) call
`form.enable_htmx_chains(self.request.path)` on interactive pages, which:

- finds every chain through `chain_for()` (so a plain `ChoiceField` can be the root);
- fills each child from the current value of its parent (`_chain_value`: bound data, or
  the initial value, or the first option of an unselected select), keeping only
  `(value, label)` in the rendered choices;
- replaces each widget with `HtmxChainedSelect`, which on a parent adds
  `hx-get="<page URL>"`, `hx-trigger="change"`, `hx-target="#<child id>"`,
  `hx-swap="innerHTML"`, `hx-sync="this:replace"`, `hx-include` with the chain's own
  selects only (never the CSRF token), `hx-vals` naming the child in `_options`, and
  `data-tg-expect="chargen-options"`;
- sets `form.htmx_chains = True`, which also turns off `ConditionalFieldsMixin`'s
  browser script.

The step view answers the `_options` request with the child's `<option>` elements (a
fragment marked `TG-Fragment: chargen-options`), a `TG-Chain` header naming the parent
values the answer is for, and the fields' new visibility from `field_visibility()` as an
`HX-Trigger-After-Swap` event `tg-visibility`. Without JavaScript the form still posts,
and the bound re-render fills the children from the submitted parents.

See [character creation](../../docs/architecture/character-creation.md).

## Rendering

Render chained fields like any other field; the media is collected by
`{% page_media %}` in the base template:

```django
{% include "core/tl/field.html" with field=form.affiliation %}
{% include "core/tl/field.html" with field=form.faction %}
```

In a fragment that does not extend `core/tl_base.html`, add `{{ form.media }}`.

## See also

- [Widgets](widgets.md)
- [JavaScript](javascript.md#chained-selects)
- [Character creation](../../docs/architecture/character-creation.md)
- [Route policies](../../core/docs/permissions-and-policies.md#route-policies)
- [`widgets/mixins/chained.py`](../mixins/chained.py)
