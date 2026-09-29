# Template tags

This page lists every custom template tag and filter library in the project, grouped by
the name you pass to `{% load %}`. For each tag or filter it gives the signature, what the
arguments mean, what it outputs, and an example. It is for anyone writing templates; for
how the pieces fit into page design, see [Front end](../architecture/frontend.md).

Libraries live in `<app>/templatetags/` and are found through `APP_DIRS`; no library is a
builtin, so every template must `{% load %}` what it uses. Library names are
project-wide: two apps must not define a module with the same name.

| `{% load %}` name | Module | Purpose |
|-------------------|--------|---------|
| `tl` | [`core/templatetags/tl.py`](../../core/templatetags/tl.py) | Spread components: dots, boxes, tracks, facts, theming helpers, object actions |
| `tl_forms` | [`core/templatetags/tl_forms.py`](../../core/templatetags/tl_forms.py) | Pick form fields by name |
| `sanitize_text` | [`core/templatetags/sanitize_text.py`](../../core/templatetags/sanitize_text.py) | Clean user-written HTML and text |
| `permissions` | [`core/templatetags/permissions.py`](../../core/templatetags/permissions.py) | Permission checks for the current user |
| `object_actions` | [`core/templatetags/object_actions.py`](../../core/templatetags/object_actions.py) | Submit / approve actions (use `tl_object_actions` instead) |
| `field` | [`core/templatetags/field.py`](../../core/templatetags/field.py) | Look up a form field by name; add widget attributes |
| `dots` | [`core/templatetags/dots.py`](../../core/templatetags/dots.py) | Text dot and box strings |
| `get_specialty` | [`core/templatetags/get_specialty.py`](../../core/templatetags/get_specialty.py) | A character's specialty for a trait |
| `json_filters` | [`core/templatetags/json_filters.py`](../../core/templatetags/json_filters.py) | Pretty-print JSON |
| `model_meta` | [`core/templatetags/model_meta.py`](../../core/templatetags/model_meta.py) | A model's `verbose_name` |
| `character_edit` | [`characters/templatetags/character_edit.py`](../../characters/templatetags/character_edit.py) | Group a character form into sections |
| `startswith` | [`characters/templatetags/startswith.py`](../../characters/templatetags/startswith.py) | `str.startswith` as a filter |
| `widget_media` | [`widgets/templatetags/widget_media.py`](../../widgets/templatetags/widget_media.py) | Output the page's collected form and widget JavaScript |
| `filterable_list` | [`widgets/templatetags/filterable_list.py`](../../widgets/templatetags/filterable_list.py) | Declare the filterable-list script |
| `formset_tags` | [`widgets/templatetags/formset_tags.py`](../../widgets/templatetags/formset_tags.py) | Render dynamic add/remove formsets |

Django's own `static` and `humanize` libraries are also used.

## `tl`

The Spread design system's tags. Nearly every page loads it.

### `{% dots value total=5 variant="ink" size="" %}`

Filled and empty circles. `value` and `total` are converted with `int()` (anything
invalid counts as 0). `variant="acc"` colours filled dots with the gameline accent;
`size="lg"` draws larger dots.

Output: `<span class="tl-dots" role="img" aria-label="3 of 5">` containing `total`
`<span class="tl-dot">` elements, the first `value` with `is-on`.

```django
{% dots object.strength %}
{% dots object.arete 10 "acc" %}
```

### `{% boxes value total=10 %}`

Squares, for temporary pools. Output: `<span class="tl-boxes" role="img" aria-label="…">`
with `total` `<span class="tl-box">` elements, the first `value` with `is-on`.

```django
{% boxes object.temporary_willpower %}
```

### `{% trait label value specialty="" total=5 variant="ink" url="" %}`

Inclusion tag rendering `core/tl/trait_row.html`: the label (linked when `url` is given),
the specialty in small type, and `{% dots value total variant %}` on one row.

```django
{% trait "Strength" object.strength %}
```

### `{% track label perm=None temp=None total=10 variant="ink" mod="" %}`

A label on the left and, on the right, permanent dots (when `perm` is given) above
temporary boxes (when `temp` is neither `None` nor `""`). `mod` is a space-separated list
of `wide` (wider label) and `wrap` (let long rows of boxes wrap, for a large pool); other
words are ignored.

```django
{% track "Willpower" perm=object.willpower temp=object.temporary_willpower %}
{% track "Blood pool" temp=object.blood_pool total=object.max_blood_pool mod="wrap" %}
```

### `{% fact label value url=None %}`

One cover fact row: `<div class="tl-facts__row">` with a mono key and the value. Renders
nothing when `value` is `None` or `""`. The value links to `url`, or to
`value.get_absolute_url()` when it has one and it resolves.

```django
{% fact "Nature" object.nature %}
{% url 'accounts:profile' object.owner.id as owner_url %}{% fact "Owner" object.owner.username owner_url %}
```

### `{% qp_wheel quintessence paradox=None label="Quintessence" total=20 %}`

The Mage Quintessence / Paradox wheel: `total` boxes on a circle, Quintessence filled
from the start, Paradox filled from the end (Paradox wins where they overlap), and both
numbers in the centre. `paradox=None` draws a Quintessence-only wheel (Sorcerers). Each
box carries a computed inline `left`/`top` style.

```django
{% qp_wheel object.quintessence object.paradox %}
```

### `{{ name|cover_title_class:gameline }}`

A size-step class for a large cover title, chosen from the length of the longest word
times a width factor for the gameline's display font: `""`, `tl-cover__name--l`,
`tl-cover__name--m` or `tl-cover__name--s`. The argument is anything `gameline_code`
accepts, or a number used as the factor directly (default `"wod"`).

```django
<h1 class="tl-cover__name {{ object.name|cover_title_class:object }}" data-fit-title>{{ object.name }}</h1>
```

### `{{ value|gameline_code }}`

The gameline code for `data-gameline` and the `gameline` block. Accepts a model with
`get_gameline()` or a `gameline` attribute, a chronicle (its `headings`, such as
`mta_heading`), or a string (`"mta"`, `"mta_heading"`). Returns the code if it is a key
of `settings.GAMELINES`, else `"wod"`.

```django
{% block gameline %}{{ object|gameline_code }}{% endblock gameline %}
```

### `{{ value|gameline_name }}`

The short gameline name for eyebrows ("Mage", "Vampire", ...): the part of the full name
before the colon. Returns `""` for `wod`.

### `{{ obj|update_url }}`

`obj.get_update_url()`, or `""` when the object has no such method or no update route
(`NoReverseMatch`, `NotImplementedError`).

```django
{% with edit_url=object|update_url %}{% if edit_url %}<a href="{{ edit_url }}">Edit</a>{% endif %}{% endwith %}
```

### `{{ obj|type_label }}`

`obj.get_type()` when the object has it, else its model's `verbose_name` in title case.

### `{% tl_object_actions %}`

Inclusion tag rendering `core/tl/object_actions.html` for the context's `object`. It shows
"Submit for approval" to a user with `EDIT_FULL` while the status is `Un` or `Rev` (or the
object's `submission_errors()` list instead, when it has any), and "Return for revisions"
and "Approve" to a user with `APPROVE` while the status is `Sub`. It renders nothing for
object types the approval endpoints do not handle. Needs `request` in the context. See
[XP, freebies and approvals](../architecture/xp-and-approvals.md).

## `tl_forms`

Filters that pick fields by name, so one template can serve forms with different field
sets. `names` is a string of field names separated by spaces or commas.

| Filter | Returns |
|--------|---------|
| `{{ form\|fields_only:"a b c" }}` | The bound fields named, in that order; names the form lacks are skipped |
| `{{ form\|fields_except:"a b c" }}` | The form's visible bound fields not named, in form order |
| `{{ fields\|numeric_fields }}` | The fields whose widget is a number input |
| `{{ fields\|other_fields }}` | The fields whose widget is not a number input |

Each returns `[]` for a missing form.

```django
{% load tl_forms %}
{% for field in form|fields_only:"name concept" %}
    {% include "core/tl/field.html" with field=field %}
{% endfor %}
```

## `sanitize_text`

Filters for text that users wrote. HTML cleaning uses `bleach` with this allow-list:
`a` (`href` only, `http`/`https`/`mailto` links), `b`, `i`, `em`, `strong`, `u`, `p`,
`br`, `strike`, `ul`, `li`, and `span` with `class="quote"` only. Other tags are stripped.

| Filter | Output |
|--------|--------|
| `{{ value\|sanitize_html }}` | The cleaned HTML, marked safe; `""` for `None` or `""`. Non-strings are converted with `str()` |
| `{{ value\|safe_post }}` | Cleaned HTML with every `"quoted"` run in text (not inside tags) wrapped in `<span class="quote">`. Used for scene posts |
| `{{ value\|quote_tag }}` | Escapes all HTML, then wraps `"quoted"` runs in `<span class="quote">`. Non-strings pass through unchanged |
| `{{ value\|simple_markdown }}` | Escapes HTML, converts `**bold**` and `*italic*`, turns blank lines into paragraphs and single newlines into `<br>`, wrapped in `<p>` |

```django
{% load sanitize_text %}
<div class="tl-prose">{{ object.description|sanitize_html|linebreaks }}</div>
<div class="tl-turn__text">{{ post.message|safe_post }}</div>
```

## `permissions`

Permission checks for `request.user` (the context must contain `request`). Prefer the
`object_perms` snapshot that `AuthorizationMiddleware` adds to every template response
whose context has an `object`; these tags are for other objects.

| Tag or filter | Returns |
|---------------|---------|
| `{% object_permissions obj as perms %}` | An `ObjectPermissions` snapshot (`core.permission_context`): `can_view_full`, `can_view_partial`, `can_edit`, `can_edit_limited`, `can_spend_xp`, `can_spend_freebies`, `can_approve`, `can_approve_spending`, `can_delete`, `can_manage_observers`, `is_owner`, `is_chronicle_st`, `is_scoped_st`, `can_manage_character`, `can_chargen`, `visibility_tier` |
| `{% user_can_view obj %}` | `VIEW_FULL` |
| `{% user_can_edit obj %}` | `EDIT_FULL` |
| `{% user_can_spend_xp obj %}` | `SPEND_XP` |
| `{% user_can_spend_freebies obj %}` | `SPEND_FREEBIES` |
| `{% user_has_permission obj "EDIT_LIMITED" %}` | The named `core.permissions.Permission` member; `False` for an unknown name |
| `{% visibility_tier obj %}` | A `VisibilityTier` (`FULL`, `PARTIAL`, `NONE`) |
| `{{ tier\|is_full }}`, `{{ tier\|is_partial }}`, `{{ tier\|is_none }}` | Compare a tier |
| `{% user_roles obj %}` | The user's set of `Role` values for the object |
| `{% is_owner obj %}` | `obj.owner == user` (or `obj.user == user`) |
| `{% is_st obj %}` | With an object: `can_manage_character` from the snapshot (admin, head ST or chronicle ST). Without: staff, superuser, or `profile.is_st()`; presentation only |
| `{% is_game_st obj %}` | The user is one of the object's chronicle's `game_storytellers` |

```django
{% load permissions %}
{% object_permissions row as row_perms %}
{% if row_perms.can_edit %}<a href="{{ row|update_url }}">Edit</a>{% endif %}
```

## `object_actions`

`{% object_actions %}` is the inclusion tag behind `{% tl_object_actions %}` and renders
the same template with the same logic. Load `tl` and use `tl_object_actions` instead.

## `field`

| Filter | Output |
|--------|--------|
| `{{ form\|field:"name" }}` | `form["name"]`, or `""` when the form is missing or has no such field |
| `{{ bound_field\|add_class:"css" }}` | The widget rendered with `class="css"` (replacing the widget's own `class`) |
| `{{ bound_field\|add_attr:"name:value" }}` | The widget rendered with the widget's attributes plus `name="value"` |

`add_class` and `add_attr` return the rendered widget HTML, so they must come last in a
filter chain; `add_attr` returns its input unchanged when the argument has no `:`.

```django
{% load field %}
{{ form|field:field_name }}
```

## `dots`

Text versions of ratings, returning plain strings of symbols. No current template loads
this library; `tl`'s `{% dots %}` and `{% boxes %}` tags draw the Spread markup instead.

| Filter | Output |
|--------|--------|
| `{{ value\|dots }}` / `{{ value\|dots:10 }}` | `●` for each point and `○` up to the maximum (default 5, widened to 10 when the value exceeds 5 and no maximum was given); `None` counts as 0, negative values as 0 |
| `{{ value\|boxes }}` | `■` and `□`; the maximum becomes 10 when the value exceeds it |
| `{{ value\|abs }}` | Absolute value; 0 for `None`; unchanged if not a number |
| `{{ value\|lore_name }}` | `"lore_of_the_beast"` -> `"Lore Of The Beast"` |
| `{{ stat\|linked_dots }}` / `{{ stat\|linked_dots:10 }}` | Two `<span class="dots">` lines: permanent dots over temporary boxes. Accepts an object with `permanent` / `temporary`, a `(permanent, temporary)` pair or a dict |

## `get_specialty`

`{{ character|get_specialty:"firearms" }}` returns `character.get_specialty(stat)`, or
`None` for anything without that method (on a create page `object` is `None`).

```django
{% load get_specialty %}
{% trait "Firearms" object.firearms object|get_specialty:"firearms" %}
```

## `json_filters`

`{{ value|pprint }}` returns JSON indented by two spaces (`ensure_ascii=False`). A string
is parsed first; anything that cannot be serialized is returned as `str(value)`.

## `model_meta`

`{{ obj|verbose_name }}` returns `obj._meta.verbose_name` for a model instance or class,
which templates cannot read directly.

## `character_edit`

`{% character_edit_sections form as sections %}` groups a character create or edit form's
fields for `characters/tl/character_edit_fields.html`. It returns
`{"hidden": [...], "sections": [...]}`; each section is a dict with `title`, `num`
(`"01"`, `"02"`, ...), `kind` (`grid`, `columns` or `long`) and either `fields` or
`columns` (a list of `(title, fields)`). Sections appear in this order when they have
fields: Identity (plain fields, then checkboxes and file uploads), Attributes (Physical,
Social, Mental columns), Abilities (Talents, Skills, Knowledges, from the instance's
ability lists), Traits (other number inputs split over up to three columns) and Details
(textareas and multi-selects). Every field the form carries appears exactly once.

```django
{% load character_edit %}
{% character_edit_sections form as sections %}
{% for field in sections.hidden %}{{ field }}{% endfor %}
```

## `startswith`

`{{ s|startswith:"prefix" }}` returns `s.startswith(prefix)`. `s` must be a string.

## `widget_media`

`{% page_media %}` outputs the combined `forms.Media` (script tags) for the page: the media
of every form in the context, of every formset (found directly or under a `formset` key in
a `*_context` dict) plus its empty form and `widgets/formset_manager.js`, and anything
registered during the render by `formset_tags` or `filterable_list`. It skips lazy context
values such as `csrf_token` so it never evaluates them.

`core/tl_base.html` calls it at the end of `<body>`, so pages extending it need nothing
more. A template that does not extend the base (a standalone page) must end with:

```django
{% load widget_media %}{% page_media %}
```

## `filterable_list`

`{% filterable_list_script %}` registers `widgets/filterable.js` with the page media and
outputs nothing. The script then filters any element marked `data-filterable-list`
through its `data-filterable-item` children and the page's `data-filter-input`,
`data-filter-select`, `data-filter-checkbox`, `data-filter-max`, `data-filter-clear`,
`data-filter-count` and `data-filter-no-results` controls (a control may name its list
with `data-filter-list`).

```django
{% load filterable_list %}
{% filterable_list_script %}
<input type="text" data-filter-input="name" placeholder="Search...">
<div data-filterable-list="my-list">
    <div data-filterable-item data-name="item one" data-type="a">Item 1</div>
</div>
```

## `formset_tags`

### `{% formset formset_var key=value ... %} ... {% endformset %}`

Renders a complete add/remove formset: the management form, a container
`<div id="<prefix>_formset" data-formset-container data-formset-prefix="<prefix>">`, one
row per form, a hidden empty-form template (`<div id="empty_<prefix>_form" class="d-none">`)
and an add button, and registers the formset's media plus `widgets/formset_manager.js`.
Inside the block, `subform` (also `form`) is the current form. Arguments must be
`key=value`:

| Argument | Default |
|----------|---------|
| `prefix` | `formset.prefix` |
| `add_label` | `"Add"` |
| `add_class` | `""` |
| `remove_label` | `"Remove"` |
| `remove_class` | `"tg-btn btn-danger btn-sm"` |
| `wrapper_class` | `"form-row"` |
| `show_remove` | `True` |
| `animate` | `False` |

```django
{% load formset_tags %}
{% formset formset prefix="reality_zone" add_label="Add practice" add_class="tl-btn tl-btn--ghost tl-btn--sm" wrapper_class="tl-locrow" show_remove=False %}
    {% include "core/tl/field.html" with field=subform.practice %}
{% endformset %}
```

### Lower-level tags

| Tag | Output |
|-----|--------|
| `{% formset_script %}` | Registers `widgets/formset_manager.js`; outputs nothing |
| `{% formset_container prefix empty_form_id=None animate=False %}` | The container's data attributes |
| `{% formset_add_btn prefix label="Add" **attrs %}` | An add button; keyword arguments become attributes (`_` -> `-`) |
| `{% formset_form_wrapper %}` | `data-formset-form=""` for a row element |

## See also

- [Front end](../architecture/frontend.md)
- [Authorization](../architecture/authorization.md)
- [`core` app](../../core/README.md)
- [`widgets` app](../../widgets/README.md)
