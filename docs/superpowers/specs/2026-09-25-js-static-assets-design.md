# JavaScript static assets design

The current user request authorizes both planning and implementation, superseding
the source summary's design-only restriction. This work relocates existing
JavaScript without changing validation rules, introducing dependencies or build
tools, or rewriting behavior with htmx/Alpine. Scene chat stays with Step 11.

## Loading and configuration

Use ordinary scripts, preserving existing globals and initialization order.
Widget classes declare `forms.Media`; the conditional form mixin adds its media
to the parent form's media. Widgets render controls and inert configuration only.
The base template aggregates form and formset media from context once at the end
of the body; standalone fragments must include `{{ form.media }}` themselves.
List/formset tags register Django Media in the current template render; the base
template outputs the combined dependencies once. Standalone templates using these
tags end with `{% load widget_media %}{% page_media %}`. Python compatibility
helpers return external script references without process-wide flags. Managers
retain their browser guards.

Each manager remains responsible for its existing data attributes, DOM events,
and public methods. Move algorithm bodies verbatim. Keep DOMContentLoaded,
htmx/Turbo hooks and formset reinitialization. Any added lifecycle hook is limited
to replacing the deleted inline initialization calls, not rewriting algorithms.

Scalar configuration uses HTML-escaped data attributes. Complex configuration
uses Django `json_script` (also from Python), preserving existing data markers
used by managers. It escapes `<`, `>` and `&`, so values containing `</script>`
cannot terminate the data element. Page scripts read data at their original
script position; do not interpolate Django expressions into executable JS.

## Inventory and audit corrections

The complete page inventory is [js-page-inventory.md](js-page-inventory.md).
It records 23 executable blocks in 22 app templates. `core/form.html` adds the
shared validation helper, and `game/scene/detail.html` is explicitly excluded.
The reported 25-template/1,640-line total is stale; count actual script bodies,
not whole templates. Fourteen conditional placeholders are confirmed (including
the NPC creation page). The chained mixin embeds choice trees and also supports
AJAX; preserve the form path, field, parent value and choices response protocol
used by Step 0's allowlisted endpoint.

| Python source / constant | Static destination | Inputs | Step 10 |
| --- | --- | --- | --- |
| widgets/widgets/point_pool.py / POINT_POOL_JS | widgets/static/widgets/point_pool.js | pool name/group, JSON pool config | Yes, verbatim |
| widgets/widgets/chained.py / CHAINED_SELECT_JS | widgets/static/widgets/chained.js | chain/parent/position, JSON tree, AJAX URL/form path | Yes, verbatim |
| widgets/mixins/conditional.py / CONDITIONAL_FIELDS_JS | widgets/static/widgets/conditional.js | JSON rules/context, wrapper/control IDs | Yes, verbatim |
| widgets/widgets/create_or_select.py / CREATE_OR_SELECT_JS | widgets/static/widgets/create_or_select.js | toggle group and container mode | No |
| widgets/widgets/metadata_select.py / OPTION_METADATA_JS | widgets/static/widgets/metadata_select.js | option data attributes | No |
| widgets/widgets/formset_manager.py / FORMSET_MANAGER_JS | widgets/static/widgets/formset_manager.js | prefix, management form, empty template, animation | No |
| widgets/widgets/filterable.py / FILTERABLE_LIST_JS | widgets/static/widgets/filterable.js | filter/list/item attributes | No |
| core/templates/core/form.html / inline helper | core/static/core/js/validation.js | DOM elements passed through existing TG.validation API | Possible |

All seven constants are confirmed. Shared emission flags also exist in metadata,
point pools and conditional fields, beyond the two named by the summary. Delete
all of these and their request_finished signal registrations. Delete the
formset render-once helper and update its callers. No request mutates global
Python script-loading state after this change.

## Caching and CSP readiness

Source paths are stable. Development uses normal staticfiles; production uses
Django ManifestStaticFilesStorage through STORAGES, creating content-hashed URLs
during collectstatic. Run collectstatic as part of deployment before serving the
new release; retain previous hashed files for open pages during rollout. Configure
immutable long-lived caching for hashed static files at the static server.
The existing stylesheet's `../static/fonts/` URLs escape the collection root;
they are corrected to `fonts/` so manifest collection succeeds while retaining
the same font resources.

No CSP is added. Remaining blockers for script-src 'self' include scene chat,
remote jQuery/Popper/jQuery UI and Patreon scripts, and any inline event handlers
or javascript URLs elsewhere (confirmed in the core character-template detail/
list pages and the HTTP 500 page). Audit these separately rather than silently
vendoring/upgrading third-party dependencies in this relocation. JSON data
scripts are inert and explicitly permitted by the regression guard.

## Verification and review model

Characterization tests run in real local Chrome before and after relocation:
point totals, chained choices, conditional visibility, add/remove formset rows,
filtering, create/select mode and attribute validation. Python tests cover Media
deduplication, independent/repeated renders, safe JSON and static discovery.
A template inventory test permits executable inline scripts only in scene chat.
Run the existing widget suite, relevant core/template tests and collectstatic.

Theory: Python supplies markup/data; static files own the same browser managers.
Reused: Django Media, staticfiles and json_script instead of a custom loader.
Assumes: existing manager naming/scoping rules remain application contracts.
Watch: scripts must load after their markup but before DOMContentLoaded callbacks;
empty formsets must include media needed by newly added rows.

## Known existing limits retained

Characterization exposed an existing formset reindexing problem: the evaluated
Python JS string loses a backslash in its dynamic regular expression, so removing
a middle unsaved row does not reliably renumber later rows. This relocation
preserves that evaluated body; browser coverage verifies adding rows, removing
the last unsaved row and marking a persisted row DELETE. Fix middle-row
reindexing separately with its own failing test. Conditional-field manager
initialization and unprefixed ID scoping likewise retain their existing rules.
