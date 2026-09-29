# Templates

Rules for writing a template, a partial or htmx markup. The visual system (shells, blocks,
tokens, components) is in [spread.md](spread.md); tags and filters are listed in
[docs/reference/template-tags.md](../../../../docs/reference/template-tags.md).

## Where templates live

- `<app>/templates/<app>/<gameline>/<model>/<page>.html`: `detail.html`, `form.html`,
  `list.html`, `chargen.html`, `template_select.html`
  (`characters/vampire/clan/detail.html`).
- Partials start with `_` when they are htmx fragments (`game/scene/_post.html`,
  `_post_window.html`) and otherwise live in a `tl/` folder of their area
  (`characters/tl/`, `game/tl/`, `core/tl/`).
- Shared fallbacks: `characters/shared/<kind>/...` and `core/registry/<action>.html`.
  A view declares its specific `template_name` and a `shared_template_name`
  (`core.mixins.SharedTemplateMixin`, `core.template_resolution.shared_template_names`);
  the specific file is an optional override. Do not copy a shared template to make a
  per-type one that says the same thing.

## Structure

- Extend a Spread shell (`core/tl_base.html`, `core/form.html`, `core/object.html`, an
  area shell). Set `{% block gameline %}{{ object|gameline_code }}{% endblock %}` on any
  page about a gameline object.
- Load what you use: `{% load tl sanitize_text %}`, plus `static`, `tl_forms`
  (`fields_only`, `fields_except`) as needed. The old `dots` library is unused; use the
  `tl` tags: `{% dots rating %}`, `{% boxes n %}`, `{% trait label value %}`,
  `{% track "Willpower" perm temp %}`, `{% fact "Owner" name url %}`.
- Fields: `{% include "core/tl/field.html" with field=form.x %}`. A template shared by
  several forms selects fields with `form|fields_only:"name concept"` so it never renders
  a field the form lacks.
- No Bootstrap grid or component classes, no jQuery, no `tg-card` markup, no Font
  Awesome.
- No inline `style="..."` and no `<style>` blocks
  (`core/tests/test_template_policy.py`: a budget of 3 inline styles, all in the password
  reset e-mail, and an allowlist of one `<style>` template). Add a class to
  `core/static/core/tl/tl.css`.
- No inline `<script>` code. Load `{% static %}` files through `extrascripts` or
  `form_scripts`; pass data with `{{ value|json_script:"id" }}` or `data-*` attributes
  (`characters/tests/test_static_page_assets.py`).
- `{# ... #}` only on a single line: Django prints a multi-line `{# #}` as page text.
  Longer notes use `{% comment %}`, which also documents a partial's parameters at its
  top.

## Data and escaping

- Autoescape stays on. User-entered rich text goes through `|sanitize_html` (bleach
  allowlist); scene posts through `|safe_post`; plain markdown-ish text through
  `|simple_markdown`. Never `|safe` or `{% autoescape off %}` on user data.
- Titles and names in `<title>` and headings: `{{ object.name|sanitize_html }}` as the
  shells do.
- Images: show `object.image` only when `object.image_status == "app"`; otherwise say it
  is pending.

## Permissions in templates

- Show or hide controls from `object_perms` (`object_perms.can_edit`,
  `.can_spend_xp`, `.can_approve`, `.is_owner`, `.can_chargen`, ...). It is a snapshot of
  `PermissionManager`, added by `PermissionContextMixin` and the middleware.
- Do not compute access from `user.is_staff`, `user.profile.is_st` or ownership
  comparisons; the view or `PermissionManager` decides, the template renders.
- Hiding a control is not authorization: the endpoint checks again.

## Queries

- Templates do not trigger queries per row: no related-manager `.all` inside loops over
  unprefetched data, no model methods that query. Prefetch in the view.
- `object.sources.all` on a cover is one query; loops over prefetched relations are free.
- Query ceilings in `core/tests/test_query_budgets.py` catch regressions on sheets, the
  scene page and the index.

## htmx markup

- Include `core/includes/interactive_scripts.html` on pages that use htmx or Alpine
  (`ws=True` adds the WebSocket extension, `alpine=False` leaves Alpine out). The meta
  config disables `eval` and restricts requests to the same origin.
- Alpine is the CSP build: no inline expressions that need `eval`; register components in
  a static script loaded before Alpine.
- Target stable ids; replace `#tg-messages` out of band (`core/tl/messages.html` with
  `oob=True`) to show messages after a swap.
- Every htmx interaction has a no-JavaScript path through the same URL (links and plain
  form posts).

## Tests that cover templates

| Test | Catches |
|------|---------|
| `core/tests/test_routed_templates.py` | A routed view whose template, parent or constant include is missing |
| `core/tests/test_template_render_smoke.py` | A fixture page that fails at render time |
| `core/tests/test_template_policy.py` | Inline styles, `<style>` blocks, extends depth |
| `core/tests/test_query_budgets.py` | Per-row queries on hot pages |
| `characters/tests/test_static_page_assets.py` | Inline scripts and leaked comments on chargen pages |

## Checklist

- [ ] Right location and name; shared template reused where one exists.
- [ ] Extends a Spread shell; `gameline` block set; `tl` tags and partials used.
- [ ] No inline styles, `<style>`, inline scripts, Bootstrap, jQuery, `tg-card`.
- [ ] User text sanitized; no `|safe` on user data.
- [ ] Controls gated on `object_perms`.
- [ ] No per-row queries; fragments have a no-JS path.

## See also

- [spread.md](spread.md), [views.md](views.md)
- [docs/architecture/frontend.md](../../../../docs/architecture/frontend.md)
- [docs/reference/template-tags.md](../../../../docs/reference/template-tags.md)
- [`core/templatetags/tl.py`](../../../../core/templatetags/tl.py), [`core/templatetags/sanitize_text.py`](../../../../core/templatetags/sanitize_text.py)
