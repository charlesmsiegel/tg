# game templates and scripts

This page lists the templates in [`game/templates/game/`](../templates/game/) and the
scripts in [`game/static/game/js/`](../static/game/js/): which view renders each
template, the shared shells and partials, and the ids the scripts depend on. Read it
before changing a game page or adding one.

All pages use the Spread design system. Most extend `game/tl/base.html`, which extends
`core/tl_base.html`; the scene page extends `core/tl_base.html` directly. See
[frontend](../../docs/architecture/frontend.md) for the shell's blocks and components
and [template tags](../../docs/reference/template-tags.md) for the `tl` tags and filters
(`gameline_code`, `cover_title_class`, `fact`).

## Shared shells and includes (`game/tl/`)

| Template | Role |
|----------|------|
| `game/tl/base.html` | Parent of the game pages. Fills `nav` with `core/tl/nav.html` and `nav_active="chronicles"`. Pages tied to a gameline set `{% block gameline %}` and `{% block cover_kind %}line{% endblock %}`. |
| `game/tl/form.html` | Create and edit shell: a cover titled from `form_eyebrow` / `form_title`, one POST form with the non-field error summary, the `fields` block (default `game/tl/fields.html`), Save and Cancel. Blocks: `form_eyebrow`, `form_title`, `form_intro`, `form_attrs`, `fields`, `submit_label`, `cancel_url`, `form_wrap`, `form_aside`. |
| `game/tl/fields.html` | Renders every visible field of `form`: checkboxes through `game/tl/check.html`, others through `core/tl/field.html`. `skip` leaves one field out (the weekly XP forms pass `skip="finishing"`). |
| `game/tl/check.html` | One checkbox with its label, errors and help text |
| `game/tl/pager.html` | Pagination links for the paginated lists; `qs` is a query-string prefix kept on each link |

Record pages about one character (journal, weekly XP, story XP, XP and freebie records)
take their gameline from the `character` context variable, which `CharacterContextMixin`
or the view sets to the concrete character.

## Pages

| Template | Rendered by | Notes |
|----------|-------------|-------|
| `chronicle/list.html` | `ChronicleListView` | Readable chronicles |
| `chronicle/detail.html` | `ChronicleDetailView` (and the chronicle actions on an invalid form) | Tabbed page; one include per tab from `chronicle/display_includes/` |
| `chronicle/form.html` | `ChronicleCreateView`, `ChronicleUpdateView` | |
| `scene/list.html` | `SceneListView` | |
| `scene/detail.html` | `SceneDetailView` | Transcript, cover with cast and actions, composer; live chat when `live` (see [websockets](websockets.md)) |
| `scene/form.html` | `SceneCreateView`, `SceneUpdateView` | Line cover in the scene's or chronicle's gameline when there is one |
| `scene/commands.html` | `CommandsView` | The `/roll`, `/stat`, `#` tag and `@storyteller` reference |
| `story/list.html`, `story/detail.html`, `story/form.html` | The story views | The chronicle is named only when `visible_chronicle` / `story_chronicle` is set; Edit shows for staff only |
| `week/list.html` | `WeekListView` | Uses `week.cached_scene_count` |
| `week/detail.html` | `WeekDetailView` | Staff see the pending-request table with batch approval (`week-detail.js`) and the approved table; players see their own requests; then finished scenes and characters |
| `week/form.html` | `WeekCreateView`, `WeekUpdateView` | |
| `journal/list.html` | `JournalListView` | Filter (all, mine, my chronicles) and one tile per journal |
| `journal/detail.html` | `JournalDetailView` | New entry form for the owner; ST response form under each unanswered entry for approvers |
| `weekly_xp_request/list.html`, `detail.html`, `form.html` | The weekly XP request views | The detail page shows the review form to an approver while pending |
| `story_xp_request/list.html`, `detail.html`, `form.html` | The story XP request views | |
| `xp_spending_request/list.html` | `XPSpendingRequestListView` | |
| `xp_spending_request/detail.html` | `XPSpendingRequestDetailView` | "Correct" and the decision form for an approver while pending |
| `xp_spending_request/form.html` | `XPSpendingRequestCreateView`, `XPSpendingRequestUpdateView` | Spend XP page with the character's request history; plain fields when correcting |
| `freebie_spending_record/list.html`, `detail.html`, `form.html` | The freebie record views | Edit shows for the owner |
| `setting_element/list.html`, `detail.html`, `form.html` | The setting element views | Edit shows when `can_manage_global_records` |

### Chronicle tab includes

`chronicle/display_includes/`:

| Include | Tab |
|---------|-----|
| `overview_section.html` | Overview: live scenes, stories, player characters, common knowledge |
| `characters_section.html`, `character_table.html` | Characters: status and gameline sub-tabs, a table grouped by group, and the "New character" GET form |
| `scenes_section.html` | Scenes: All / Active / Completed, gameline sub-tabs, a table per month, and the NEW SCENE form (`game:chronicle_create_scene`) |
| `locations_section.html`, `location_row.html` | Locations: the containment tree, rows recursing into children |
| `items_section.html` | Items and the "New item" GET form |
| `common_knowledge_section.html` | Setting elements by gameline |
| `stories_section.html` | Stories, the NEW STORY form (`game:chronicle_create_story`) and unassigned stories for managers |

The "New character / location / item" forms submit by GET to
`core:object_type_redirect`; see [forms](forms.md#chronicle-object-creation-forms).

## Scene partials

The scene page is assembled from partials that the WebSocket consumer also renders, so a
live update and a reload produce the same markup. Partials that take `oob` add
`hx-swap-oob="true"` for out-of-band swaps.

| Partial | Content | Also rendered by |
|---------|---------|------------------|
| `scene/_post_window.html` | A window of posts with the unread divider (`#unread-divider`) and the "Show earlier posts" link | `SceneDetailView` as the `scene-posts` fragment |
| `scene/_post.html` | One post (`data-post-id`, `data-speaker`); `tl-turn--st` for storyteller authors, `tl-turn--mine` for the viewer's own; the roll strip when `post.roll_strip` is set, else the message | `ws/_posts.html` |
| `scene/_roll_dice.html` | One roll's dice as tiles | |
| `scene/_cast.html` | The cast list on the cover (`#scene-cast`) | `scene.characters` event |
| `scene/_post_character_field.html` | The "Posting as" choice (`#post-character-field`) | `scene.characters` event, for the character's owner |
| `scene/_add_character_field.html` | The add-character select (`#add-char-field`) | `scene.characters` event |
| `scene/_post_message_fields.html` | Display name and message inputs (`#post-message-fields`) | Reply to a successful socket post |
| `scene/ws/_posts.html` | New posts appended to `#posts-container` | Socket only |
| `scene/ws/_notice.html` | The `#scene-chat-notice` live region | Socket only |
| `scene/ws/_closed.html` | Closed-state replacements for `#scene-actions`, `#scene-cover-actions`, `#scene-live-badge` | Socket only |

The comment at the top of `scene/detail.html` lists every id `scene-chat.js` and the
`ws` extension rely on. Keep it in step with the script.

## Other partials

| Partial | Used by |
|---------|---------|
| `week/_request_marks.html` | `week/detail.html`: the five criteria of a request as ✓ or — cells |
| `xp_spending_request/_spend_fields.html` | `xp_spending_request/form.html`; also returned alone as the `xp-spend` fragment |
| `xp_spending_request/_status.html` | The status word (`Pending`, `Approved`, `Denied`) on the XP pages |

## Scripts

| Script | Loaded by | Purpose |
|--------|-----------|---------|
| `game/js/scene-chat.js` | `SceneDetailView` (`component_scripts`, through `core/includes/interactive_scripts.html`) | Live chat behaviour; see [websockets](websockets.md#the-client-script) |
| `game/js/xp-spend.js` | `XPSpendingRequestCreateView` (`component_scripts`) | Accepts an htmx swap into the spend form only when the response carries `TG-Fragment: xp-spend`; otherwise loads the response URL as a page |
| `game/js/week-detail.js` | `week/detail.html` (`<script>` tag, only for staff with pending requests) | Select-all and the selected count for batch approval; needs `#batch-approve-form`, `#select-all-checkbox`, `#select-all-btn`, `#batch-approve-btn`, `#selected-count` and `.request-checkbox` |

The `interactive_scripts.html` include loads htmx (and the `ws` extension when
`ws=True`) from `static/vendor/` before the component scripts.

## Conventions

- Extend `game/tl/base.html` for a new page and `game/tl/form.html` for a create or
  edit page; render fields with `game/tl/fields.html` or `core/tl/field.html`.
- Do not add inline `style=""` attributes or `<style>` blocks; the template policy test
  (`core/tests/test_template_policy.py`) fails when the total count of inline styles
  grows or a `<style>` block appears outside its allow-list.
- A partial that the socket also sends must render correctly from its own inputs
  (listed in its header comment), without the page context.

## See also

- [Frontend](../../docs/architecture/frontend.md)
- [WebSockets](websockets.md)
- [game views and URLs](views-and-urls.md)
- [Scenes](scenes.md)
- [Template tags](../../docs/reference/template-tags.md)
