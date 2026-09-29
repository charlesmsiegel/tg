# Front end

This page describes the site's front end, the "Spread" design system: the base template
and its blocks, the page shells built on it, gameline theming, the one stylesheet and the
small set of scripts, how forms and messages render, the rules the template policy test
enforces, and how pages behave for keyboard users and without JavaScript. It is for anyone
writing or reviewing a template, stylesheet rule or front-end script. Template tag
signatures are listed in [Template tags](../reference/template-tags.md).

## Principles

- Every page is a two-part **spread**: a **cover** on the left (identity, key facts,
  primary actions) and the scrolling **pages** on the right. At 1100px and below the cover
  stacks above the pages.
- One stylesheet ([`core/static/core/tl/tl.css`](../../core/static/core/tl/tl.css)) and
  one base script ([`core/static/core/tl/tl.js`](../../core/static/core/tl/tl.js)) serve
  every page. There is no Bootstrap, jQuery, icon font, npm, bundler or build step.
- The server renders HTML; scripts add behaviour on top. Every form posts as a normal
  form, and every interactive feature has a plain-HTML path (see
  [Without JavaScript](#without-javascript)).
- Radius is 0 everywhere and there are no shadows; rules (lines) carry hierarchy. Colours
  come only from the CSS custom properties (tokens) described below.

## The base template

[`core/templates/core/tl_base.html`](../../core/templates/core/tl_base.html) is the root of
every page. It sets `data-theme` and `data-gameline` on `<html>`, loads the Google Fonts
Spectral and IBM Plex Mono and `tl.css`, renders a "Skip to content" link, the cover, the
navigation, the flash messages and `<main id="main">`, then loads `tl.js` (deferred), the
`extrascripts` block, and finally `{% page_media %}` (from `widget_media`), which outputs
the JavaScript that the page's forms, widgets and formsets declare.

| Block | Purpose |
|-------|---------|
| `title` | The `<title>` text (default "Tellurium Games") |
| `gameline` | Gameline code for `data-gameline`; default `wod`. Fill it with `{{ object\|gameline_code }}` |
| `styling` | Extra `<head>` content |
| `spread_mod` | Modifier class on `.tl-spread` (for example `tl-spread--wide`, `tl-spread--scene`) |
| `cover_kind` | `ink` (default, neutral) or `line` (coloured by the gameline accent) |
| `cover_mod` | Modifier class on the cover (for example `tl-cover--low`, `tl-cover--chargen`) |
| `cover_label` | `aria-label` of the cover `<aside>` |
| `cover_top` | Top of the cover; default is the wordmark linking home |
| `cover_title`, `cover_body`, `cover_actions` | Cover content |
| `nav` | Defaults to `{% include "core/tl/nav.html" %}`; pages pass `nav_active`, or replace it with page tabs (`tl-nav tl-nav--tabs`) |
| `content_mod` | Modifier class on `<main>` |
| `content`, `after_content` | The pages |
| `actionbar` | Rendered after the spread, for a fixed action bar |
| `extrascripts` | Page scripts, before `{% page_media %}` |

`core/tl/nav.html` renders the global navigation: a Chronicles popover (chronicles and open
scenes from the `core.context_processors.all_chronicles` context processor), Characters,
Locations, Items and House Rules, and an account popover showing the notification count
and breakdown (from `accounts.context_processors.notification_count`), profile, admin
(staff only) and log-out links; anonymous visitors get "Log in" and "Sign up". `nav_active` takes `chronicles`,
`characters`, `locations`, `items`, `houserules` or `profile`. At narrow widths the links
collapse into a menu sheet.

## Shells

Most pages extend a shell rather than `tl_base.html` directly:

| Shell | Used for | Blocks children fill |
|-------|----------|----------------------|
| [`core/form.html`](../../core/templates/core/form.html) | Create and edit forms | `creation_title`, `formdetails` (form attributes), `heading`, `progress`, `errors`, `image`, `contents`, `buttons`, `form_scripts` |
| [`core/object.html`](../../core/templates/core/object.html) | Item, location and generic detail pages | `cover_facts`, `image`, `objectname`, `references`, `status_row`, `contents`, `description`, `post_content`, `buttons` |
| `core/tl_auth.html` | Login, sign-up, password reset, logged out | `auth_title`, `auth_note`, `auth_body` |
| `core/errors/error.html` | 401, 403, 404 and 500 pages | |
| `characters/core/character/detail.html` | Character sheets (every type, through `characters/core/human/detail.html`) | cover facts, sheet sections, experience and scenes tabs |
| `characters/core/chargen.html` | Character creation steps | See [Character creation](character-creation.md#templates) |
| `characters/tl/reference_list.html`, `reference_detail.html`, `ref2_*.html` | Game reference data (Gifts, Rotes, Clans, ...) | filters, facts, sections |
| `locations/core/tl_list.html`, `tl_form.html`; `items/tl/form.html`, `items/tl/list.html` | Location and item lists and forms | |
| `game/tl/base.html`, `game/tl/form.html` | Chronicles, scenes, stories, weeks, journals, XP records | |

`core/form.html` renders one `<form class="tl-form">` with a CSRF token, the non-field
errors, the object's image (or "Image pending approval."), the `contents` block, and the
action row: **Save** first, so it stays the implicit submitter when the user presses
Enter, then **Back** (only mid-chargen, for the owner, carrying `formaction` and
`formnovalidate`) and **Cancel**. Both `core/form.html` and `core/object.html` render
`{% tl_object_actions %}` for the submit / approve buttons (see
[XP, freebies and approvals](xp-and-approvals.md#approvalservice)).

Shared partials live in [`core/templates/core/tl/`](../../core/templates/core/tl/):
`field.html`, `messages.html`, `nav.html`, `section.html` (a numbered section),
`empty.html` (an empty state: a sentence and an optional link), `trait_row.html`,
`create_form.html`, `object_actions.html` and `source_facts.html`.

## Gameline theming

Set the `gameline` block to a gameline code and the whole page takes that line's accent
colour and display font:

```django
{% extends "core/tl_base.html" %}
{% load tl %}
{% block gameline %}{{ object|gameline_code }}{% endblock gameline %}
{% block cover_kind %}line{% endblock cover_kind %}
```

`gameline_code` (in `core/templatetags/tl.py`) accepts a model with `get_gameline()` or
`gameline`, a chronicle (its `headings` value such as `mta_heading`) or a string, and
returns the code if it is a key of `settings.GAMELINES`, otherwise `wod`.

`tl.css` maps `[data-gameline="<code>"]` to two custom properties, and any element can
carry the attribute (a tile in a mixed list, for example):

| Code | `--acc` token | `--display` font |
|------|---------------|------------------|
| `mta` | `--mta` | Abbess |
| `vtm` | `--vtm` | Delavan |
| `wta` | `--wta` | Balthazar |
| `ctd` | `--ctd` | Kells |
| `wto` | `--wto` | MatrixTall |
| `dtf` | `--dtf` | EnvisionRoman |
| `htr` | `--htr` | Futura PT |
| `mtr` | `--mtr` | Papyrus |
| `wod` | `--ink` | OPTIProtea |

The display fonts are served from `source_static/fonts/` and declared with `@font-face`
at the top of `tl.css`. Cover titles use `class="tl-cover__name {{ name|cover_title_class:object }}"`
with `data-fit-title`: `cover_title_class` picks a size step from the longest word (scaled
by the display font's width), and `tl.js` shrinks a title further if it still overflows.

## Colour themes

`<html data-theme>` is the signed-in user's `Profile.theme` (`light` or `dark`,
`core.constants.ThemeChoices`), or `system` for anonymous visitors. The tokens
(`--paper`, `--sheet`, `--inset`, `--ink`, `--ink2`, `--rule`, `--rubric` and the eight
gameline colours) are defined on `:root`, redefined for `[data-theme="dark"]`, and
redefined again for `[data-theme="system"]` inside
`@media (prefers-color-scheme: dark)`. Use the tokens and `--acc` in new rules, never raw
colours; `--rubric` is reserved for storyteller voice, errors and counts.

## CSS

`tl.css` is the only stylesheet. It holds the font faces, tokens, gameline mappings, the
spread layout and every component class (`tl-cover`, `tl-nav`, `tl-section`, `tl-field`,
`tl-btn`, `tl-dots`, `tl-steps`, `tl-turn`, `tl-roll`, ...). Components are named
`tl-<block>`, with `__element` and `--modifier` suffixes and `is-<state>` classes. Layout
breakpoints are at 1100px and 720px, and `prefers-reduced-motion: reduce` turns off
transitions.

`core.tests.test_tl_css.TlCssBalanceTest` checks that every `{` in the file is closed,
because a lost brace would swallow every later rule into the preceding `@media` block.

## JavaScript

| Script | Loaded by | Does |
|--------|-----------|------|
| [`core/static/core/tl/tl.js`](../../core/static/core/tl/tl.js) | Every page (`tl_base.html`) | Fits oversized `data-fit-title` titles; dismisses messages (`data-tl-dismiss`); keeps one `details.tl-pop` / `details.tl-menu` open at a time and closes it on outside click or Escape; remembers `<details data-tl-remember="key">` state in `localStorage`; scrolls the current chargen step into view. Exposes `window.TL.fitTitles` |
| Widget and form media (`widgets/static/widgets/*.js`: `dot_rating.js`, `chained.js`, `conditional.js`, `formset_manager.js`, `filterable.js`, ...) | `{% page_media %}` from the forms and formsets in the context, or registered by `formset_tags` / `filterable_list` tags | The behaviour of each widget |
| Component scripts (`characters/js/chargen*.js`, `game/js/scene-chat.js`, `game/js/xp-spend.js`) | A view puts their static paths in `component_scripts`; `core/includes/interactive_scripts.html` loads them | Page-specific behaviour |
| [`core/static/core/js/validation.js`](../../core/static/core/js/validation.js) | `core/form.html` and the non-interactive chargen form | `TG.validation` helpers used by the older per-step validation scripts |
| Other page scripts under `characters/static/`, `items/static/`, `locations/static/`, `game/static/` | The templates that need them | Running totals and form helpers for specific pages |

### htmx and Alpine.js

htmx, its WebSocket extension and the Alpine.js CSP build are vendored under
[`source_static/vendor/`](../../source_static/vendor/) (a `STATICFILES_DIRS` entry), with
the version in each path. [`source_static/vendor/VENDOR.md`](../../source_static/vendor/VENDOR.md)
records each file's source, npm integrity, SRI hash and licence. To upgrade a library,
vendor the new version beside the old one, update that table and the include below, and
delete the old directory.

Pages opt in with
[`core/includes/interactive_scripts.html`](../../core/templates/core/includes/interactive_scripts.html):

```django
{% block extrascripts %}
    {% include "core/includes/interactive_scripts.html" %}
{% endblock extrascripts %}
```

It emits an `htmx-config` meta tag (`allowEval: false`, `includeIndicatorStyles: false`,
`selfRequestsOnly: true`, `historyCacheSize: 0`), then htmx 2.0.11, the `ws` extension
2.0.4 when `ws=True`, each script in the context's `component_scripts`, and Alpine.js
3.17.4 unless `alpine=False`. Every script is `defer`, so they run in document order and
components register before Alpine starts; the vendored files also carry `integrity`
(SRI) attributes.
`core.tests.test_htmx` recomputes each vendored file's SRI hash and fails if the include,
`VENDOR.md` or the bytes on disk disagree.

The Alpine **CSP build** evaluates directive expressions with its own parser instead of
`new Function`, so it needs no `'unsafe-eval'`; all components are registered with
`Alpine.data()` in static files. Current users: interactive chargen (htmx and Alpine), the
scene page (htmx and the `ws` extension, `alpine=False`) and the Spend XP page (htmx,
`alpine=False`).

### htmx conventions

[`core/htmx.py`](../../core/htmx.py) defines the server side of the contract:

- `is_fragment_request(request)`: an `HX-Request` that is not a history restore or boosted
  request. Only fragment requests get partial responses.
- `mark_fragment(response, kind)` sets the `TG-Fragment` header. Client scripts compare it
  with the requesting element's expectation (`data-tg-expect` in chargen) and load the URL
  as a full page when they differ, so a login page or error never gets swapped into the
  middle of a page.
- `vary_on_htmx(response)` adds `Vary` on every header `is_fragment_request` reads, so a
  cache never serves a fragment for a full-page request.
- `hx_redirect(url)` answers with `HX-Redirect` (a 200) to make htmx navigate the whole
  page.
- `trigger(response, event, detail, header="HX-Trigger")` adds a client event.

Fragments that update more than one region use out-of-band swaps (`hx-swap-oob`), and
`core/tl/messages.html` accepts `oob=True` for that purpose.

## Template tags

Load `{% load tl sanitize_text %}` in most templates. The main tags:

| Tag or filter | Output |
|---------------|--------|
| `{% dots value total=5 variant="ink" size="" %}` | Filled and empty circles |
| `{% boxes value total=10 %}` | Squares (temporary pools) |
| `{% track "Willpower" perm temp %}` | Label with permanent dots over temporary boxes |
| `{% trait "Strength" 3 "Wiry" %}` | Label, specialty and dots on one row |
| `{% fact "Nature" object.nature %}` | A cover fact row, linked when the value has a URL |
| `{{ object\|gameline_code }}`, `{{ name\|cover_title_class:object }}` | Theming helpers |
| `{% tl_object_actions %}` | Submit / return / approve buttons for the current `object` |
| `{{ text\|sanitize_html }}`, `{{ post.message\|safe_post }}` | User text cleaned by bleach |

Every library, with signatures and examples, is in
[Template tags](../reference/template-tags.md).

## Forms

Render each field with the shared partial:

```django
{% include "core/tl/field.html" with field=form.name %}
{% include "core/tl/field.html" with field=form.concept label="Concept" help="" %}
```

`field.html` renders the label, the widget (selects inside `.tl-field__control`), the
errors (`<ul class="tl-field__error" id="<id>_error">`) and help text. `label=` overrides
the label; `help=` replaces the field's help text and `help=""` hides it;
`help_template=` renders an include as help. A field with errors gets `is-invalid`.

When one template serves several forms (a create form, a storyteller's full edit form and
an owner's limited form), pick fields by name with `tl_forms`, so the template never
renders a field the form lacks or drops one it has:

```django
{% load tl_forms %}
{% for field in form|fields_only:"name concept" %}
    {% include "core/tl/field.html" with field=field %}
{% endfor %}
```

Character edit forms group their fields into sections with
`{% character_edit_sections form as sections %}` (`character_edit` library).

## Messages

`core/tl/messages.html` is included by `tl_base.html` under the navigation. It always
renders `<div id="tg-messages" aria-live="polite">`, even when empty, so htmx fragments can
replace it out of band and screen readers announce new notices. Each message gets
`role="alert"` for errors and `role="status"` otherwise, a mono tag ("Error",
"† Warning", "Saved", "† Notice"), its text through `sanitize_html`, and a dismiss button
handled by `tl.js`. Views add messages with `django.contrib.messages` or `MessageMixin`.

## Template policy

[`core/tests/test_template_policy.py`](../../core/tests/test_template_policy.py) scans every
template under `accounts`, `characters`, `core`, `game`, `items` and `locations` and fails
when:

- the count of inline `style="` attributes exceeds `INLINE_STYLE_BUDGET` (3, all in the
  password-reset e-mail, because e-mail clients need inline styles). Put new styles in
  `tl.css`;
- a `<style>` block appears outside `STYLE_BLOCK_TEMPLATES` (only the password-reset
  e-mail);
- a template sits more than `MAX_EXTENDS_DEPTH` (5) `{% extends %}` hops below its root.

The `qp_wheel` tag is the one deliberate inline style in rendered pages: it positions each
box of the Mage Quintessence / Paradox wheel with computed `left` / `top` values. It is
produced by Python, not written in a template, so the policy test does not count it.

## Accessibility

- A "Skip to content" link targets `<main id="main" tabindex="-1">`.
- Focus is always visible (`:focus-visible` outline in the accent colour; paper-coloured
  on the ink cover).
- Navigation marks the current section with `aria-current="page"`, and the chargen step
  list marks the current step with `aria-current="step"`.
- Dot and box ratings render with `role="img"` and an `aria-label` such as "3 of 5".
- Messages, the chargen live feedback and the scene connection status are `aria-live`
  regions; errors use `role="alert"`.
- After an htmx step swap, chargen moves focus to the error summary or the new step
  heading.
- Popovers are `<details>` elements, so they work with the keyboard; `tl.js` adds Escape
  to close and returns focus to the summary.
- Transitions are disabled for users who prefer reduced motion.

## Without JavaScript

Every page works with scripts disabled, with less convenience:

- Forms are real `<form method="post">` elements; htmx attributes are added alongside
  `action`, never instead of it.
- Dot ratings keep the `<input type="number">` as the control; the dots are hidden without
  JavaScript.
- Popovers and menus are `<details>` elements, which open natively.
- Chargen steps, the Spend XP page's preview (a "Preview" submit button) and the scene's
  "Show earlier posts" link (an `href` to `?before=`) all have full-page equivalents, and
  scene posts go through the HTTP form.
- `<details data-tl-remember>` and title fitting are enhancements only; the server already
  picks a title size step.

## See also

- [Template tags](../reference/template-tags.md)
- [Character creation](character-creation.md)
- [Scenes and real-time updates](scenes-and-realtime.md)
- [`core` app](../../core/README.md)
- [`widgets` app](../../widgets/README.md)
