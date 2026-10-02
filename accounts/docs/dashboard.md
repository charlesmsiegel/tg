# Dashboard and profile page

This page covers `accounts.dashboard.ProfileDashboard` (the per-user queue selectors),
the notification counts built from it, and how `ProfileView` turns those queues into the
tabbed profile page. Read it before adding a queue, a notification, or a profile tab.

Source: [`accounts/dashboard.py`](../dashboard.py) and `ProfileView` in
[`accounts/views.py`](../views.py).

## ProfileDashboard

`ProfileDashboard(profile)` wraps one `Profile`. Its methods only read; none of them
write. `Profile.dashboard` returns an instance, and `Profile` exposes each selector under
the same name (see [models](models.md#dashboard-wrappers)).

"Staffed chronicles" below means `game.security.staffed_chronicles(user)`: chronicles
where the user is head ST, a game storyteller, or has an `STRelationship`; staff and
superusers get every chronicle. Several `core` queryset helpers also include objects
with no chronicle when the user is staff or a superuser.

### Owned objects

| Method | Returns |
|--------|---------|
| `my_characters()` | `Character.objects.owned_by(user)` with `polymorphic_ctype` joined |
| `my_locations()` | `LocationModel` owned by the user, same shape |
| `my_items()` | `ItemModel` owned by the user, same shape |

### Storyteller queues

| Method | Returns |
|--------|---------|
| `st_relations()` | `dict` of `Chronicle` to the user's `STRelationship` rows for it (from `STRelationship.objects.for_user_optimized`) |
| `characters_to_approve()` | Characters with status `Sub` in staffed chronicles (`pending_approval_for_user`) |
| `items_to_approve()`, `locations_to_approve()` | The same for items and locations |
| `rotes_to_approve()` | `dict` of submitted `Rote` (status `Sub`, in the user's chronicles, ordered by name) to the list of mages that have it |
| `objects_to_approve()` | One list: characters, items, locations, then the rotes (the keys of `rotes_to_approve()`) |
| `freebies_to_approve()` | Characters in the user's chronicles with `freebies_approved=False` that are at their class's freebie step (`at_freebie_step()`) |
| `character_images_to_approve()`, `location_images_to_approve()`, `item_images_to_approve()` | Objects with `image_status="sub"` and a non-empty image, in the user's chronicles |
| `xp_requests()` | Finished scenes without XP awarded (`Scene.objects.awaiting_xp()`) in the user's chronicles |
| `xp_story()` | Stories with `xp_given=False` whose chronicle is staffed by the user, plus stories with no chronicle |
| `get_updated_journals()` | Journals that have at least one entry with an empty `st_message`, limited by `game.security.filter_private_records` to journals the user may read |
| `get_unfulfilled_weekly_xp_requests_to_approve()` | List of `(character, week)` pairs for characters in the user's chronicles that have an unapproved `WeeklyXPRequest` for a week they are enrolled in |
| `xp_spend_requests()` | Characters in staffed chronicles with at least one `XPSpendingRequest` whose `approved` is `"Pending"` |

### Player queues

| Method | Returns |
|--------|---------|
| `get_unfulfilled_weekly_xp_requests()` | List of `(character, week)` pairs: the user's non-NPC characters enrolled in a `Week` (`Week.characters`) with no `WeeklyXPRequest` yet for that week |
| `unread_scenes()` | Scenes where the user's `UserSceneReadStatus.read` is `False`, filtered by `game.security.filter_scenes` to scenes the user may read |

A character is enrolled in a week when a scene it played in is closed:
`Scene.close()` adds the scene's characters to the `Week` ending on the following Sunday
(see [game XP](../../game/docs/xp.md)).

## Notification counts

`ProfileDashboard.notification_context()` returns
`{"notification_count": int, "notification_breakdown": {label: count}}`. The
`notification_count` context processor caches it (see
[models](models.md#notification_count)). Only positive counts are added to the
breakdown.

Every user gets the player counts:

| Label | Source |
|-------|--------|
| Unread Scenes | `unread_scenes().count()` |
| Weekly XP Requests | `len(get_unfulfilled_weekly_xp_requests())` |

When `profile.is_st()` is true (the user heads a chronicle or has any `STRelationship`), these are added:

| Label | Source |
|-------|--------|
| Scene XP Requests | `xp_requests()` |
| Characters to Approve, Locations to Approve, Items to Approve | the approval selectors |
| Rotes to Approve | `rotes_to_approve()` |
| Freebies to Approve | `freebies_to_approve()` |
| XP Spend Requests | `xp_spend_requests()` |
| Character, Location and Item Images to Approve | the image selectors |
| Scenes Needing Attention | `Scene.objects.waiting_for_st()` in staffed chronicles, filtered by `filter_scenes` |
| Updated Journals | `get_updated_journals()` |
| Weekly XP to Approve | `len(get_unfulfilled_weekly_xp_requests_to_approve())` |

The storyteller counts are added when `Profile.is_st()` is true: the user is a chronicle's
`head_st` or holds an `STRelationship` row (see [models](models.md)). That is the same
rule the approval endpoints apply, so a head ST with no relationship row is counted. A
staff user without either gets only the player counts even though the selectors include
every chronicle for staff, and a game storyteller gets none of them: the endpoints reject
game storytellers too.

To add a notification, add a selector to `ProfileDashboard` and an `_add_count` line in
`_player_notification_count` or `_storyteller_notification_count`. Keep the calls
explicit: each one is a query per page render (cached for 60 seconds per user).

## Profile page

`ProfileView` (URL `accounts:profile`, template `accounts/detail.html`) shows one
profile. Only the profile's own user or a staff user may open it; anyone else gets 403
(`PermissionDenied`). Anonymous callers are stopped earlier by the `ACCOUNT` route policy.

### Tabs

The tab comes from `?tab=`. `ProfileView.get_tab` accepts `needs`, `characters` and
`experience` for everyone, plus `chronicles` and `journals` when the viewed profile
`is_st()`. Any other value falls back to `needs` when `needs_count` is non-zero, else
`characters`.

| Tab | Content | Template |
|-----|---------|----------|
| Needs you | Every queue collected by `get_needs_you` (below) | `accounts/includes/needs.html` |
| My characters | `my_characters`, `my_locations`, `my_items` as tiles | `includes/characters.html`, `locations.html`, `items.html` |
| Chronicles | `st_relations()`: each chronicle with the gamelines the user storytells | `includes/chronicles.html` |
| Experience | The player's weekly XP request cards; on a storyteller's own profile also weekly XP approvals and scene XP award cards | `includes/xp_weekly.html`, `xp_weekly_st.html`, `xp_scene_st.html` |
| Journals | `get_updated_journals()` | `includes/journals.html` |

### Context built by `get_context_data`

- `is_st`, `is_own`, `viewer_is_st`: `Profile.is_st()` for the viewed profile, whether
  the viewer is its user, and `is_st()` for the viewer. Each predicate is one query, so
  the view decides them once here and `get_needs_you` and the templates read the values
  (`includes/settings.html` uses `viewer_is_st`; the cover label and tabs use `is_st`).
- `scenes_waiting`: scenes with `waiting_for_st=True` in the profile user's staffed
  chronicles, filtered by `filter_scenes`; empty unless the profile `is_st()`.
- `st_queues`: true when the viewer is the profile's user and the profile `is_st()`. The
  storyteller forms are built only then:
  - `scenexp_forms`: one `accounts.forms.SceneXP` per scene in `xp_requests()`, prefixed
    `scene_<pk>`.
  - `freebie_forms`: one `FreebieAwardForm` per character in `freebies_to_approve()`.
  - `weekly_xp_request_forms_to_approve`: one `game.forms.WeeklyXPRequestForm` bound to
    the existing request for each pair in `get_unfulfilled_weekly_xp_requests_to_approve()`
    (fetched in one query).
- `weekly_xp_request_forms`: one unbound `WeeklyXPRequestForm` per pair in
  `get_unfulfilled_weekly_xp_requests()`.

### NEEDS YOU (`get_needs_you`)

`get_needs_you` evaluates each queue once so the tab count and the tab body agree. It
returns the queues plus these flags and summaries:

| Key | Meaning |
|-----|---------|
| `unread_scenes`, `scenes_waiting` | Always computed |
| `xp_spend_requests` | Computed when the profile `is_st()`; each character carries `pending_spendings` (its pending `XPSpendingRequest` rows) |
| `characters_to_approve`, `locations_to_approve`, `items_to_approve`, `rotes_to_approve`, `*_images_to_approve` | Only when `st_queues`; otherwise empty lists |
| `is_st`, `is_own`, `st_queues` | Role flags used by the templates |
| `other_queues` | `(label, count, anchor)` for Locations, Items, Rotes and Images; empty when all are zero |
| `weekly_xp_summary` | Counts of scene XP forms, weekly requests to approve and to file, and the latest `Week` among them |
| `needs_count` | Sum of every queue shown, used for the tab badge and the default tab |

The storyteller queues show only on a storyteller's own profile. Because `ProfileView`
admits only the owner and staff, the rows that are computed for "anyone viewing a
storyteller's profile" (`scenes_waiting`, `xp_spend_requests`) are seen in practice by
the owner and by staff.

### Acting from the profile

Every button on the page posts to a dedicated view in the `accounts` namespace and
redirects back to the profile (often to `?tab=experience`). See
[views and URLs](views-and-urls.md#profile-actions) for each endpoint.

## See also

- [accounts models](models.md)
- [accounts views and URLs](views-and-urls.md)
- [accounts templates](templates.md)
- [XP and approvals](../../docs/architecture/xp-and-approvals.md)
- [`game/security.py`](../../game/security.py)
