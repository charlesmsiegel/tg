# game views and URLs

This page lists every URL under `/game/`, the view behind it, who may use it and what it
does. Read it before adding a page or action, or before changing a permission check in
the app. Scene and XP behaviour is summarised here and described in full in
[scenes](scenes.md) and [XP](xp.md).

Source: [`game/urls.py`](../urls.py), [`game/views.py`](../views.py) (pages) and
[`game/actions.py`](../actions.py) (POST actions). The app is mounted in
[`tg/urls.py`](../../tg/urls.py) as `path("game/", include(("game.urls", "game"),
namespace="game"))`; nested groups add a second namespace, for example
`game:story:detail`.

## Access control layers

A request passes up to three checks. The first two run in
`core.middleware.authorization.AuthorizationMiddleware` before the view:

1. **Route policy** from [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py),
   evaluated by `core.access_policy.authorize_route`:
   - `GAME` for every class in `game.views`: anonymous callers get a plain-text
     `401 Login required`, except GET and HEAD on `SceneListView` and
     `SceneDetailView`, which stay open so public scenes can be read without an
     account.
   - `ACTION` for every class in `game.actions`: non-POST methods get `405` and
     anonymous callers `401`.
2. **Private-record and audience check** (`AuthorizationMiddleware._check_game_detail`),
   for `game.views` classes with a `pk` URL argument whose model is `Chronicle`,
   `Scene`, `Journal`, `JournalEntry`, `WeeklyXPRequest`, `StoryXPRequest`,
   `XPSpendingRequest` or `FreebieSpendingRecord` (the two approve views count as
   their record's model). A missing object and one the caller may not read both get the
   same plain-text `404 Not found`:
   - chronicles: `game.security.readable_chronicles`;
   - scenes: `game.security.can_view_scene`;
   - private records: `game.security.can_read_private_record` (`VIEW_FULL` on the
     record's character).
3. **The view's own check**: a `core.mixins` mixin, a `dispatch` override or, for
   actions, `can_see` and `has_permission` on `core.actions.ObjectActionView`.

The middleware also answers `404` for a `pk` that is not a positive decimal integer.
See [authorization](../../docs/architecture/authorization.md) for roles and permissions,
and [access and selectors](access-and-selectors.md) for the `security.py` audiences.

## Chronicles

| Path | Name | View | Access | Notes |
|------|------|------|--------|-------|
| `chronicles/` | `chronicles` | `ChronicleListView` | Signed in | `readable_chronicles(user)` ordered by name |
| `chronicle/<pk>/` | `chronicle` | `ChronicleDetailView` | Readers of the chronicle | Tabbed page, see below |
| `chronicle/<pk>/stories/` | `chronicle_create_story` | `actions.ChronicleStoryCreateView` | `can_manage_chronicle` (head ST or staff) | `StoryForm`; the story gets this chronicle |
| `chronicle/<pk>/scenes/` | `chronicle_create_scene` | `actions.ChronicleSceneCreateView` | `can_create_scene`, then `can_manage_scope` for the chosen gameline (else `403`) | `SceneCreationForm`; `Chronicle.add_scene`; redirects to the scene |
| `chronicle/<pk>/retired/`, `deceased/`, `npc/` | `retired`, `deceased`, `npc` | `characters.views.core.RetiredCharacterIndex`, `DeceasedCharacterIndex`, `NPCCharacterIndex` | Route policy `OBJECT_LIST` | Character lists owned by the characters app |
| `chronicle-manage/create/` | `chronicle_manage:create` | `ChronicleCreateView` | Staff (`StorytellerRequiredMixin` with no chronicle) | `ChronicleForm` |
| `chronicle-manage/<pk>/update/` | `chronicle_manage:update` | `ChronicleUpdateView` | Head ST or staff | `ChronicleForm` |

`views.can_create_scene(user, chronicle)` is true for the head ST, staff, and any user
with an `STRelationship` in the chronicle. It decides who sees NEW SCENE; saving still
needs the matching gameline.

### ChronicleDetailView

Template `game/chronicle/detail.html`. The page is tabbed by query string:

| Parameter | Values | Default |
|-----------|--------|---------|
| `tab` | `overview`, `characters`, `scenes`, `locations`, `items`, `common-knowledge`, `stories` | `overview` |
| `status` | Characters: `active`, `retired`, `deceased`, `npc`. Scenes: `all`, `active`, `completed` | `active` / `all` |
| `line` | A gameline code with rows in the current tab | The first gameline with rows |
| `new` | `scene` or `story`: open that creation form | none |

The lists come from `game.selectors.chronicle_overview(chronicle, user)`, which limits
non-staff members to their own characters and items and hides the location tree. The
context also carries `can_manage_chronicle`, `can_create_scene`, the three
chronicle-aware creation forms (`char_form`, `loc_form`, `item_form`), `tab_counts`,
`live_scenes`, the chronicle's `stories`, `unassigned_stories` (stories without a
chronicle, shown to chronicle managers), `current_week` and `house_rule_count`.

When `ChronicleSceneCreateView` or `ChronicleStoryCreateView` receives an invalid form,
it re-renders this page with the bound form (`ObjectActionView.render_host`), and
`tab_context` opens the matching tab and form.

## Scenes

| Path | Name | View | Access | Notes |
|------|------|------|--------|-------|
| `scenes/` | `scenes` | `SceneListView` | Anyone; filtered by `filter_scenes` | Ordered by `-date_of_scene`, `-date_played` |
| `scene/<pk>/` | `scene` | `SceneDetailView` | `can_view_scene` (anonymous for `PUBLIC`) | Transcript and live chat; `?before=<post id>` for older posts |
| `scene/<pk>/posts/` | `scene_post` | `actions.ScenePostView` | `can_view_scene` and `scene_chat.can_post` | HTTP fallback for posting |
| `scene/<pk>/characters/` | `scene_add_character` | `actions.SceneAddCharacterView` | `can_view_scene` and the scene is open | `AddCharForm` |
| `scene/<pk>/close/` | `scene_close` | `actions.SceneCloseView` | `can_manage_scope(user, scene.chronicle, scene.gameline)` | Locks the scene, `Scene.close()`, broadcasts `scene.closed` |
| `scene-manage/create/` | `scene_manage:create` | `SceneCreateView` | Staff (no chronicle to scope to) | `SceneForm`; the scene has no chronicle |
| `scene-manage/create/<chronicle_pk>/` | `scene_manage:create_for_chronicle` | `SceneCreateView` | GET: head ST, staff or any ST of the chronicle. POST: `can_manage_scope` for the submitted gameline | `SceneForm` with locations of that chronicle |
| `scene-manage/<pk>/update/` | `scene_manage:update` | `SceneUpdateView` | `can_manage_scope` for the scene, and again for the submitted gameline | Edits `finished` and `xp_given` directly, without `close()` |
| `commands/` | `commands` | `CommandsView` | Signed in | The dice and point command reference |

Scene actions extend `actions.SceneActionView`: a caller who cannot read the scene gets
`404`, and every action except closing is refused (`403`) on a finished scene. The
scene page shows "Close scene" on an open scene only when its `can_close_scene` context
flag is set, from `game.views.can_close_scene`, the same rule `SceneCloseView` enforces.
Details of the scene page, posting, dice commands and read
markers are in [scenes](scenes.md).

## Stories

| Path | Name | View | Access |
|------|------|------|--------|
| `story/list/` | `story:list` | `StoryListView` | Signed in; every story, with its chronicle named only when the viewer can read it |
| `story/<pk>/` | `story:detail` | `StoryDetailView` | Signed in; same chronicle rule (`story_chronicle`) |
| `story/create/` | `story:create` | `StoryCreateView` | Staff (`StoryStaffRequiredMixin`) |
| `story/<pk>/update/` | `story:update` | `StoryUpdateView` | Staff |

The standalone forms use `StoryEditForm`, which lets staff assign a chronicle.
Chronicle managers create stories from the chronicle page instead
(`chronicle_create_story`).

## Journals

| Path | Name | View | Access |
|------|------|------|--------|
| `journals/` | `journals` | `JournalListView` | Signed in; `filter_private_records`; `?filter=mine` or `?filter=st`; 20 per page |
| `journal/<pk>/` | `journal` | `JournalDetailView` | `VIEW_FULL` on the journal (`ViewPermissionMixin`, `404` otherwise) |
| `journal/<pk>/entries/` | `journal_add_entry` | `actions.JournalEntryCreateView` | Readers of the journal who own the character |
| `journal/<pk>/entries/<entry_pk>/response/` | `journal_respond` | `actions.JournalResponseView` | `Permission.APPROVE` on the character |

`JournalEntryCreateView` saves through `JournalEntryForm.save()` (`Journal.add_post`,
which applies point tags and dice commands). `JournalResponseView` loads the entry with
`get_object_or_404(JournalEntry, pk=entry_pk, journal=journal)` and binds
`STResponseForm` with prefix `entry-<pk>`.

## Weeks and weekly XP

| Path | Name | View | Access |
|------|------|------|--------|
| `week/list/` | `week:list` | `WeekListView` | Signed in; 20 per page; `annotate_week_scene_counts` counts scenes the viewer can see |
| `week/<pk>/` | `week:detail` | `WeekDetailView` | Signed in; scenes by `filter_scenes`, requests by `filter_private_records`; previous and next week |
| `week/create/`, `week/<pk>/update/` | `week:create`, `week:update` | `WeekCreateView`, `WeekUpdateView` | Staff |
| `weekly-xp-request/list/` | `weekly_xp_request:list` | `WeeklyXPRequestListView` | Signed in; `filter_private_records`; 50 per page |
| `weekly-xp-request/<pk>/` | `weekly_xp_request:detail` | `WeeklyXPRequestDetailView` | Owner or anyone with `VIEW_FULL` on the character (`CharacterOwnerOrSTMixin`) |
| `weekly-xp-request/create/<week_pk>/<character_pk>/` | `weekly_xp_request:create` | `WeeklyXPRequestCreateView` | The character's owner or staff |
| `weekly-xp-request/<pk>/approve/` | `weekly_xp_request:approve` | `WeeklyXPRequestApproveView` | POST; `require_spending_approver` |
| `weekly-xp-request/batch-approve/` | `weekly_xp_request:batch_approve` | `WeeklyXPRequestBatchApproveView` | POST; see [XP](xp.md#weekly-xp) |

`can_manage_global_records` (staff or superuser) decides whether the week pages show
edit links and the pending-request table with batch approval. When
`WeeklyXPRequestBatchApproveView` receives no ids it redirects to the `Referer` header
when that URL is on this site (same host, and HTTPS when the request is), otherwise to the
week list.

## XP, story XP and freebie records

| Path | Name | View | Access |
|------|------|------|--------|
| `xp-spending-request/list/` | `xp_spending_request:list` | `XPSpendingRequestListView` | Signed in; `filter_private_records`; 50 per page |
| `xp-spending-request/<pk>/` | `xp_spending_request:detail` | `XPSpendingRequestDetailView` | `CharacterOwnerOrSTMixin`; decision form for approvers while pending |
| `xp-spending-request/create/<character_pk>/` | `xp_spending_request:create` | `XPSpendingRequestCreateView` | `SPEND_XP` on the character, then owner or staff |
| `xp-spending-request/<pk>/update/` | `xp_spending_request:update` | `XPSpendingRequestUpdateView` | `can_approve_spending`; pending requests only |
| `xp-spending-request/<pk>/approve/` | `xp_spending_request:approve` | `XPSpendingRequestApproveView` | POST `approved`; `decide_spending_request` |
| `story-xp-request/list/` | `story_xp_request:list` | `StoryXPRequestListView` | Signed in; `filter_private_records`; 50 per page |
| `story-xp-request/<pk>/` | `story_xp_request:detail` | `StoryXPRequestDetailView` | `CharacterOwnerOrSTMixin` |
| `story-xp-request/create/<character_pk>/` | `story_xp_request:create` | `StoryXPRequestCreateView` | `StorytellerRequiredMixin` scoped to the character's chronicle and gameline |
| `story-xp-request/<pk>/update/` | `story_xp_request:update` | `StoryXPRequestUpdateView` | Same, from the record's character |
| `freebie-spending-record/list/` | `freebie_spending_record:list` | `FreebieSpendingRecordListView` | Signed in; `filter_private_records`; 50 per page |
| `freebie-spending-record/<pk>/` | `freebie_spending_record:detail` | `FreebieSpendingRecordDetailView` | `CharacterOwnerOrSTMixin` |
| `freebie-spending-record/create/<character_pk>/` | `freebie_spending_record:create` | `FreebieSpendingRecordCreateView` | `SPEND_FREEBIES` on the character |
| `freebie-spending-record/<pk>/update/` | `freebie_spending_record:update` | `FreebieSpendingRecordUpdateView` | `CharacterOwnerOrSTMixin` and `SPEND_FREEBIES`; pending records only |

The list views set `show_owner_column` when the viewer is staff or a chronicle ST for any
row on the page (`_has_st_read_rows`); the weekly and XP lists then also show a
`pending_count`. `CharacterContextMixin` puts the record's concrete character in the
context as `character`, which the Spread cover uses for its gameline. The spending flow
is described in [XP](xp.md).

## Setting elements

| Path | Name | View | Access |
|------|------|------|--------|
| `setting-element/list/` | `setting_element:list` | `SettingElementListView` | Signed in; 50 per page |
| `setting-element/<pk>/` | `setting_element:detail` | `SettingElementDetailView` | Signed in; lists the chronicles that use it |
| `setting-element/create/`, `<pk>/update/` | `setting_element:create`, `setting_element:update` | `SettingElementCreateView`, `SettingElementUpdateView` | Staff: `StorytellerRequiredMixin` finds no chronicle for a setting element, and no storyteller role applies without one |

## Adding a page or action

1. Put a page (GET) in `views.py` and a state change in `actions.py` as an
   `ObjectActionView` subclass with `can_see`, `has_permission` and one `perform` call.
2. Add the dotted class path to the right set in
   [`core/route_policy_manifest.py`](../../core/route_policy_manifest.py) (`GAME` or
   `ACTION`); a view with no declared policy is refused with `403`.
3. If the page shows a private record or a scene by `pk`, give the view the record's
   `model` so the middleware hides it from non-readers.
4. Add the URL to `game/urls.py` and a test in `game/tests/views/` or
   `game/tests/urls/test_url_patterns.py`.

See [adding a view](../../docs/guides/adding-a-view.md) for the project-wide steps.

## See also

- [Scenes](scenes.md)
- [XP](xp.md)
- [Access and selectors](access-and-selectors.md)
- [game forms](forms.md)
- [Authorization](../../docs/architecture/authorization.md)
- [URL reference](../../docs/reference/urls.md)
