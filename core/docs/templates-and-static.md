# Templates and static files

This page describes the page shells, partials, template tag libraries and static assets
that live in `core`: the Spread design system every page is built on. It is for anyone
writing or changing a template. For the design rules across the project see
[Frontend](../../docs/architecture/frontend.md); for every tag's arguments see the
[template tag reference](../../docs/reference/template-tags.md).

## Spread in one paragraph

Spread is the site's design system. A page is a two-part spread: a **cover** on the left
(an `<aside>` with the page's eyebrow, title, facts and main actions) and **pages** on the
right (the global nav, flash messages and the content). One stylesheet
([`static/core/tl/tl.css`](../static/core/tl/tl.css)) and one small script
([`static/core/tl/tl.js`](../static/core/tl/tl.js)) serve every page. There is no
Bootstrap, jQuery or icon font. Colours and the display font follow the page's gameline
through a `data-gameline` attribute.

## Page shells

Every page extends [`core/tl_base.html`](../templates/core/tl_base.html) or a shell built
on it.

| Template | Use for | Child blocks |
|----------|---------|--------------|
| `core/tl_base.html` | Everything (the root) | See below |
| `core/object.html` | A generic object detail page (cover built from the object's type, owner, chronicle, status and sources); `LanguageDetailView` renders it | `cover_facts`, `image`, `objectname`, `references`, `status_row`, `contents`, `description`, `post_content`, `buttons` |
| `core/form.html` | Create and edit pages of characters, items and locations, including chargen steps | `creation_title`, `formdetails`, `heading`, `progress`, `errors`, `image`, `contents`, `buttons`, `form_scripts` |
| `core/misc/form.html` | Create and edit pages of the core reference models, registry objects and groups | `creation_title`, `form_eyebrow`, `form_lede`, `formdetails`, `errors`, `contents`, `buttons`, `submit_label` |
| `core/tl_auth.html` | Login, sign-up, password reset, logged out | `auth_title`, `auth_note`, `auth_body` |
| `core/errors/error.html` | 401, 403 and 404 pages | `error_code`, `error_headline`, `error_text` |
| `core/registry/{detail,list,form,object_list}.html` | Fallbacks for registry item and location types without their own template | |
| `core/public_object_detail.html`, `core/public_object_list.html` | The public projections (see [views](views.md#public-projections)) | |

`core/errors/500.html` does not extend anything: it is rendered without a request or
context processors (see [views](views.md#error-views)).

Apps add their own area shells on top of these, for example
`characters/tl/reference_detail.html`, `game/tl/base.html` and
`items/core/item/detail.html` (on `tl_base.html`), or `items/tl/form.html` and
`locations/core/tl_form.html` (on `core/form.html`). Look for an area shell before
extending `tl_base.html` directly.

### `tl_base.html` blocks

| Block | Default | Purpose |
|-------|---------|---------|
| `title` | `Tellurium Games` | `<title>` |
| `gameline` | `wod` | Value of `<html data-gameline>`; sets the accent colour and display font |
| `styling` | empty | Extra `<head>` content |
| `spread_mod`, `cover_mod`, `content_mod` | empty | Modifier classes (`tl-spread--wide`, `tl-cover--low`, `tl-content--narrow`...) |
| `cover_kind` | `ink` | `tl-cover--ink` (dark cover) or `line` (ruled cover in the gameline accent) |
| `cover_label` | `Page summary` | `aria-label` of the cover |
| `cover_top` | Wordmark link home | Top of the cover |
| `cover_title`, `cover_body`, `cover_actions` | empty | Cover title, facts and buttons |
| `nav` | `core/tl/nav.html` | Global nav; override to pass `nav_active` |
| `content`, `after_content` | empty | The page content inside `<main id="main">` |
| `actionbar` | empty | Fixed action bar after the spread |
| `extrascripts` | empty | Page scripts, after `tl.js` |

The base also sets `<html data-theme>` to the user's profile theme (`light` or `dark`)
or `system` for anonymous visitors, includes `core/tl/messages.html` under the nav,
loads the Spread fonts (Spectral and IBM Plex Mono from Google Fonts), `tl.css` and
`tl.js` (deferred), and ends with `{% page_media %}` from the `widgets` app's
`widget_media` library, which writes the `<script>`/`<link>` tags of every form and
formset in the context once (see [widgets](../../widgets/docs/widgets.md#page-media)).

A numbered section on a detail page:

```django
{% include "core/tl/section.html" with num="01" title="Attributes" body_template="characters/core/attribute_block/detail.html" %}
```

A typical form page:

```django
{% extends "core/misc/form.html" %}
{% block contents %}
    {% include "core/tl/field.html" with field=form.name %}
    {% include "core/tl/field.html" with field=form.description %}
{% endblock contents %}
```

`core/form.html` renders Save first (so Enter submits it), then a chargen Back button
(when `object.chargen_back_url` is set and the user owns the object) and Cancel. It loads
`core/js/validation.js` inside the form and renders `{% tl_object_actions %}` after it.

## Partials

| Template | Include with | Renders |
|----------|--------------|---------|
| `core/tl/field.html` | `field=form.x`, optional `label`, `help`, `help_template` | One form field: label, input (selects wrapped for the arrow), errors, help text |
| `core/misc/check.html` | `field=form.flag` | A checkbox with its label on one line |
| `core/misc/field_sections.html` | `fields=form\|fields_except:"name owner"`, optional `numbers_title`, `others_title` | Number inputs as compact rows, then the other fields in a grid |
| `core/misc/form_errors.html` | uses `form` (or `form=other_form`) | Error summary with a count and links to fields |
| `core/misc/image.html` | `obj=object` | Approved image, or a pending box |
| `core/tl/section.html` | `num`, `title`, `body_template`, optional `power`, `aside`, `anchor` | A numbered section |
| `core/tl/empty.html` | `text`, optional `action_url`, `action_label` | An empty state |
| `core/tl/messages.html` | `oob=True` for an htmx out-of-band swap | Flash messages in `#tg-messages` |
| `core/tl/nav.html` | `nav_active` (`chronicles`, `characters`, `locations`, `items`, `houserules`, `profile`) | Global nav, including the chronicles menu fed by the `all_chronicles` context processor |
| `core/tl/create_form.html` | `create_form`, `kind`, `label` | A GET form to `core:object_type_redirect` |
| `core/tl/source_facts.html` | uses `object` | One cover fact row per `BookReference` |
| `core/tl/trait_row.html` | used by `{% trait %}` | Label, specialty and dots |
| `core/tl/object_actions.html` | used by `{% tl_object_actions %}` | Submit, return and approve forms |
| `core/includes/interactive_scripts.html` | optional `ws=True`, `alpine=False`, `component_scripts` | Vendored htmx, the htmx WebSocket extension and Alpine (CSP build) with SRI hashes, plus the htmx config (`allowEval: false`, `selfRequestsOnly: true`, no history cache) |

`interactive_scripts.html` is used by the pages that need htmx: the chargen shell
(`characters/core/chargen.html`), the scene page and the XP spending form. The vendored
files live in `source_static/vendor/`; `core/tests/test_htmx.py` checks each SRI hash
against the file.

### Object actions

`{% tl_object_actions %}` (in `tl`) and `{% object_actions %}` (in `object_actions`)
render `core/tl/object_actions.html` for the page's `object` when it is a character,
group, chimera, effect, rote, item, location or character template:

- **Submit for approval** when the user has `EDIT_FULL`, the status is `Un` or `Rev` and
  the model's optional `submission_errors()` returns nothing; otherwise the errors are
  listed under "Finish creation first".
- **Return for revisions** and **Approve** when the user has `APPROVE` and the status is
  `Sub`.

The forms post to `accounts:object_submission`, `accounts:object_revision` and
`accounts:object_approval`, which call `ApprovalService` (see
[services](services.md#approvalservice)).

## Template tag libraries

The `core` libraries and what they are for. The full tag and filter reference is in
[template tags](../../docs/reference/template-tags.md).

| Library | Role | Main tags and filters |
|---------|------|-----------------------|
| `tl` ([`tl.py`](../templatetags/tl.py)) | Spread markup | `{% dots %}`, `{% boxes %}`, `{% trait %}`, `{% track %}`, `{% fact %}`, `{% qp_wheel %}`, `{% tl_object_actions %}`; filters `gameline_code`, `gameline_name`, `cover_title_class`, `update_url`, `type_label` |
| `tl_forms` | Pick fields from whatever form the view supplied | `fields_only`, `fields_except`, `numeric_fields`, `other_fields` |
| `sanitize_text` | Render user text safely | `sanitize_html` (bleach allowlist), `safe_post` (sanitized HTML with quoted dialogue wrapped in `<span class="quote">`), `quote_tag`, `simple_markdown` |
| `permissions` | Permission snapshots in templates | `{% object_permissions obj as perms %}`; see [permissions](permissions-and-policies.md#capabilities-for-templates) |
| `object_actions` | Approval buttons | `{% object_actions %}` |
| `dots` | Text dots for plain contexts | filters `dots` (`●○`), `boxes` (`■□`), `abs`, `lore_name`, `linked_dots` |
| `field` | Form field access | filters `field`, `add_class`, `add_attr` |
| `get_specialty` | Specialty lookup | filter `get_specialty` (calls `character.get_specialty(stat)`) |
| `json_filters` | JSON display | filter `pprint` |
| `model_meta` | Model metadata | filter `verbose_name` |

The `tl` library's `{% dots %}` tag and the `dots` library's `dots` filter share a name.
Spread pages use the `tl` tag; do not load both libraries in one template.

`gameline_code` accepts a model (through `get_gameline()` or a `gameline` attribute), a
`Chronicle` (its `headings`), or a string such as `"mta"` or `"mta_heading"`, and falls
back to `"wod"` for anything not in `settings.GAMELINES`. Use it for the `gameline`
block:

```django
{% block gameline %}{{ object|gameline_code }}{% endblock gameline %}
```

## Template rules

These are enforced by tests in [`core/tests/`](../tests/) (see [testing](testing.md)):

- No new inline `style="..."` attributes and no `<style>` blocks in app templates
  (`test_template_policy.py`). Put styles in `tl.css`. The only exceptions are in the
  password-reset e-mail template, because e-mail clients need inline styles.
- No template more than five `{% extends %}` hops below its root.
- Every template a routed view renders, extends or includes must exist and compile
  (`test_routed_templates.py`), and every fixture page must render
  (`test_template_render_smoke.py`).
- `tl.css` must have balanced braces (`test_tl_css.py`).

### Specific-then-shared templates

A view can name its own template and fall back to a shared one:
`core.template_resolution.shared_template_names(names, *shared)` returns the view's names
followed by the fallbacks, without duplicates. Django renders the first that exists.
`SharedTemplateMixin` (`shared_template_name`) and the registry views use it (see
[mixins](mixins.md#sharedtemplatemixin)).

## Static files

| File | Purpose |
|------|---------|
| [`static/core/tl/tl.css`](../static/core/tl/tl.css) | The whole Spread stylesheet: tokens, shell, nav, sections, traits, tiles, buttons, fields, messages, scene transcript, character sheet, responsive rules, then per-area additions (werewolf sheet, items...) |
| [`static/core/tl/tl.js`](../static/core/tl/tl.js) | Spread behaviour, no dependencies |
| [`static/core/js/validation.js`](../static/core/js/validation.js) | `TG.validation` helpers for chargen step scripts |

Fonts, images and vendored libraries are not in `core/static/`: they are in
`source_static/` at the repository root (`STATICFILES_DIRS`). `tl.css` loads the
per-gameline display fonts from `source_static/fonts/` by relative URL.

### `tl.css`

Design tokens are CSS custom properties on `:root`: `--paper`, `--sheet`, `--inset`,
`--ink`, `--ink2`, `--rule`, `--rubric`, one colour per gameline (`--mta`, `--vtm`,
`--wta`, `--ctd`, `--wto`, `--dtf`, `--htr`, `--mtr`), `--serif`, `--mono`, `--acc`
(accent) and `--display` (display font).

- **Theme**: `:root[data-theme="dark"]` swaps the palette; `data-theme="system"` follows
  `prefers-color-scheme`.
- **Gameline**: `[data-gameline="<code>"]` sets `--acc` to the gameline colour and
  `--display` to its font (Abbess for Mage, Delavan for Vampire, and so on; `wod` uses
  ink and OPTIProtea). The attribute works on any element, so a tile in a mixed list can
  carry its own gameline.
- **Breakpoints**: 1100px and 720px. At 720px and below the nav collapses into a menu
  sheet.
- Components use `tl-` class names in BEM style (`tl-cover__title`,
  `tl-btn--ghost`). Radius is 0 and there are no shadows; dots are the only circles.

Add new rules to `tl.css` in the section for their area; do not add stylesheets per page.

### `tl.js`

Loaded with `defer` on every page. It:

1. Shrinks oversized cover titles marked `data-fit-title` until they fit, then allows
   wrapping; re-fits on resize, after fonts load and after `htmx:afterSwap`.
2. Removes a flash message when its `[data-tl-dismiss]` button is clicked.
3. Keeps one `<details class="tl-pop">` or `tl-menu` open at a time and closes it on an
   outside click, on Escape or on a `[data-tl-close]` click.
4. Remembers the open state of `<details data-tl-remember="key">` in `localStorage`.
5. Scrolls the current chargen step (`.tl-steps [aria-current="step"]`) into view inside
   the cover.

It exposes `window.TL.fitTitles`.

### `validation.js`

Defines `window.TG.validation` with `setStatus(el, valid, message)`,
`setSubmitEnabled(form, enabled)` (the main submit buttons only, not Back or Cancel),
`sumFields(form, selector)` and `countChecked(form, selector)`. `core/form.html` loads it
inside the form so that step scripts can use it from `DOMContentLoaded` handlers.

## See also

- [Frontend architecture](../../docs/architecture/frontend.md)
- [Template tag reference](../../docs/reference/template-tags.md)
- [widgets app](../../widgets/README.md)
- [Testing](testing.md#template-and-frontend-guards)
- [`core/templates/core/`](../templates/core/)
