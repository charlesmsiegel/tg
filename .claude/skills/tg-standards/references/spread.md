# Spread design system (migrated pages)

The site is moving from Bootstrap 4 + `tg-card` to **Spread**: every page is a two-page
spread, a fixed **cover** on the left (identity, key facts, primary actions) and the
scrolling **pages** on the right. Templates migrate one at a time; old and new pages
coexist. A migrated page loads no Bootstrap, jQuery, `style.css` or Font Awesome.

## Files

| File | Purpose |
|------|---------|
| `core/templates/core/tl_base.html` | Spread shell (all blocks below) |
| `core/templates/core/tl_auth.html` | Login shell: wide ink cover, centered 420px column |
| `core/templates/core/errors/error.html` | Shell for 401/403/404/500 |
| `core/static/core/tl/tl.css` | Tokens + every component class |
| `core/static/core/tl/tl.js` | Title fitting, popovers, message dismiss, `<details>` memory |
| `core/templates/core/tl/*.html` | `nav`, `messages`, `section`, `field`, `empty`, `trait_row`, `create_form`, `object_actions` |
| `core/templatetags/tl.py` | `{% dots %}`, `{% boxes %}`, `{% trait %}`, `{% track %}`, `{% qp_wheel %}`, `\|cover_title_class`, `\|gameline_code`, `{% tl_object_actions %}` |

Migrated so far: home, login / sign up / password reset, error pages, character index
(staff) and `core/public_object_list.html`.

## Migrating a template

1. `{% extends "core/tl_base.html" %}` instead of `core/base.html`.
2. Fill the blocks:

| Block | Use |
|-------|-----|
| `gameline` | `{{ object\|gameline_code }}` — sets `--acc` and `--display` |
| `cover_kind` | `ink` (neutral pages) or `line` (anything with a gameline) |
| `spread_mod` | `tl-spread--wide` for the 560px cover (home, login) |
| `cover_mod` | `tl-cover--low` pushes the title to the bottom of the cover |
| `cover_top`, `cover_title`, `cover_body`, `cover_actions` | Cover content |
| `nav` | `{% include "core/tl/nav.html" with nav_active="characters" %}`, or page tabs (`tl-nav tl-nav--tabs`) |
| `content`, `content_mod` | The pages |
| `actionbar` | Mobile fixed action bar (`<div class="tl-actionbar">`) |
| `extrascripts` | Page scripts; `{% page_media %}` still runs after it |

3. Replace Bootstrap behaviour: collapse → `<details>`; tabs → links with `?tab=`
   or `?status=`; dropdowns → `<details class="tl-pop">` + `.tl-pop__panel`.
4. Keep every `id` / `data-*` that JavaScript or htmx relies on; `#tg-messages` is
   in `core/tl/messages.html`.
5. No inline `style="…"` (the template policy test ratchets them down): add a class
   to `tl.css`.

## Rules

- Radius 0, no shadows. Rules carry hierarchy: `2px solid var(--ink)` above a
  section body, `1px solid var(--rule)` between rows.
- Colours only from tokens: `--paper --sheet --inset --ink --ink2 --rule --rubric --acc`.
  `--rubric` is for Storyteller voice, errors and counts, never decoration.
- Status is a mono uppercase word (`tl-status`), `--rubric` only for Deceased/problems.
- Cover titles: `class="tl-cover__name {{ name|cover_title_class:object }}" data-fit-title`.
- Forms: `{% include "core/tl/field.html" with field=form.x label="…" %}`.
- Empty states: `{% include "core/tl/empty.html" with text="…" %}` — no icons.
