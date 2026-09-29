# Spread design system

The site's only front end. Every page is a two-page **spread**: a fixed **cover** on the
left (identity, key facts, primary actions) and the scrolling **pages** on the right. The
site loads no Bootstrap, jQuery, Font Awesome or legacy `style.css`; `tl.css` and `tl.js`
are the whole shell, with htmx and Alpine (CSP build) on interactive pages only. The
explanation is in [docs/architecture/frontend.md](../../../../docs/architecture/frontend.md);
template rules are in [templates.md](templates.md).

## Files

| File | Purpose |
|------|---------|
| `core/templates/core/tl_base.html` | Spread shell; every page extends it directly or through a shell below |
| `core/templates/core/tl_auth.html` | Login and sign-up shell: wide ink cover, one 420px column |
| `core/templates/core/errors/error.html` | Shell for the 401, 403, 404 and 500 pages |
| `core/templates/core/form.html` | Create and edit shell: cover, error summary, `contents`, Save / Back / Cancel, approval actions |
| `core/templates/core/object.html` | Detail shell for items, locations and reference objects (cover facts, sources, description) |
| `core/templates/core/tl/*.html` | Partials: `nav`, `messages`, `section`, `field`, `empty`, `trait_row`, `create_form`, `object_actions`, `source_facts` |
| `core/static/core/tl/tl.css` | Tokens and every component class (`core/tests/test_tl_css.py` checks brace balance) |
| `core/static/core/tl/tl.js` | Cover title fitting, message dismiss, one-open `<details>` popovers, remembered `<details>` state |
| `core/templatetags/tl.py` | `{% dots %}`, `{% boxes %}`, `{% trait %}`, `{% track %}`, `{% fact %}`, `{% qp_wheel %}`, `{% tl_object_actions %}`; filters `gameline_code`, `gameline_name`, `cover_title_class`, `type_label`, `update_url` |
| `core/templates/core/includes/interactive_scripts.html` | Vendored htmx (+ WebSocket extension) and Alpine CSP with SRI hashes |

Area shells build on these: the character sheet (`characters/core/character/detail.html`
and `characters/tl/*`), chargen (`characters/core/chargen.html`), reference pages
(`characters/tl/reference_detail.html`, `reference_list.html`), the registry pages
(`core/registry/*`), and the game pages (`game/tl/*`).

## Writing a page

1. `{% extends "core/tl_base.html" %}`, `core/form.html`, `core/object.html` or an area
   shell. Keep the extends chain at most five deep (`test_template_policy.test_extends_depth`).
2. Fill the blocks:

| Block | Use |
|-------|-----|
| `title` | `<title>` text |
| `gameline` | `{{ object\|gameline_code }}`; sets `data-gameline` on `<html>`, which sets `--acc` and `--display` |
| `cover_kind` | `ink` (neutral pages) or `line` (anything with a gameline) |
| `spread_mod` | `tl-spread--wide` for the 560px cover (home, login) |
| `cover_mod` | `tl-cover--low` pushes the title to the bottom of the cover |
| `cover_label` | `aria-label` of the cover |
| `cover_top`, `cover_title`, `cover_body`, `cover_actions` | Cover content |
| `nav` | `{% include "core/tl/nav.html" with nav_active="characters" %}` (values: `chronicles`, `characters`, `locations`, `items`, `houserules`, `profile`) or page tabs (`tl-nav tl-nav--tabs`) |
| `content`, `content_mod`, `after_content` | The pages |
| `actionbar` | Mobile fixed action bar (`<div class="tl-actionbar">`) |
| `styling`, `extrascripts` | Extra `<link>` / `<script src>` tags; `{% page_media %}` runs after `extrascripts` |

3. Interactive patterns without JavaScript: collapse is `<details>`; tabs are links with
   `?tab=` or `?status=`; dropdowns are `<details class="tl-pop">` with `.tl-pop__panel`.
4. Keep every `id` and `data-*` that scripts or htmx rely on; `#tg-messages` lives in
   `core/tl/messages.html` and may be replaced out of band.

## Visual rules

- Square corners (`border-radius: 0`) except dots and radio circles; no drop shadows
  (inset underlines mark the current tab). Rules carry hierarchy: `2px solid var(--ink)`
  above a section body, `1px solid var(--rule)` between rows.
- Colours only from tokens: `--paper`, `--sheet`, `--inset`, `--ink`, `--ink2`, `--rule`,
  `--rubric`, `--acc` (per gameline). `--rubric` is for Storyteller voice, errors and
  counts, never decoration. Dark mode redefines the tokens under `data-theme`.
- Status is a mono uppercase word (`tl-status`); `--rubric` only for Deceased and
  problems.
- Cover titles: `class="tl-cover__name {{ name|cover_title_class:object }}" data-fit-title`.
- Sections: `{% include "core/tl/section.html" with num="01" title="..." body_template="..." %}`.
- Form fields: `{% include "core/tl/field.html" with field=form.x %}` (`label=`, `help=`,
  `help_template=` optional).
- Empty states: `{% include "core/tl/empty.html" with text="..." %}`; no icons.
- A new look is a new class in `tl.css`, never an inline `style=""` or a `<style>` block.

## See also

- [docs/architecture/frontend.md](../../../../docs/architecture/frontend.md)
- [docs/reference/template-tags.md](../../../../docs/reference/template-tags.md)
- [templates.md](templates.md)
- [`core/static/core/tl/tl.css`](../../../../core/static/core/tl/tl.css)
