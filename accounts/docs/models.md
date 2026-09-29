# accounts models, signals and context processors

This page is the reference for the `Profile` model in
[`accounts/models.py`](../models.py) and the code that creates it and exposes it to
templates: the signal, the admin registration and the two context processors. Read it
before adding a preference, changing how storyteller status is detected, or adding a
value to every template's context.

## Profile

`Profile` extends `django.contrib.auth.models.User` with a one-to-one row rather than a
custom user model. It inherits `core.base.ValidatedSaveMixin`, so every `save()` runs
`full_clean()` first (pass `skip_validation=True` to bypass it).

### Fields

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `user` | `OneToOneField(User, on_delete=CASCADE)` | required | The account this profile belongs to; reverse accessor `user.profile` |
| `preferred_heading` | `CharField`, choices `core.constants.HeadingChoices.CHOICES` | `"wod_heading"` | The gameline display font used for the user's name on the profile cover |
| `theme` | `CharField`, choices `ThemeChoices.CHOICES` (`light`, `dark`) | `"light"` | Colour scheme; `core/tl_base.html` writes it into `<html data-theme>` |
| `highlight_text` | `BooleanField` | `True` | Highlights quoted and special text in scenes (the scene page adds `tl-scene--highlight`) |
| `discord_id` | `CharField(100)` | `""` | Discord username |
| `lines` | `TextField`, nullable | `""` | Topics the player does not want in play at all |
| `veils` | `TextField`, nullable | `""` | Content the player wants kept off screen |
| `discord_toggle`, `lines_toggle`, `veils_toggle` | `BooleanField` | `False` | Whether the matching value is shown to other viewers of the profile |

### Validation

`Profile.clean()` adds these checks on top of field validation:

- `theme` must be one of the keys in `ThemeChoices.CHOICES` (also available as the
  `theme_list` property).
- `preferred_heading` must be one of a fixed list in `clean()`: `wod_heading`,
  `vtm_heading`, `wta_heading`, `mta_heading`, `ctd_heading`, `wto_heading`. This list is
  narrower than `HeadingChoices.CHOICES`, which also offers `dtf_heading`; a profile saved
  with `dtf_heading` fails validation.
- `user` must be set.

### Storyteller helpers

| Method | Returns | Rule |
|--------|---------|------|
| `is_st()` | `bool` | The user has at least one `game.models.STRelationship` row, for any chronicle and gameline. Being a chronicle's `head_st`, a game storyteller or staff does not count on its own. |
| `is_st_for(chronicle)` | `bool` | The user is `chronicle.head_st`, or has an `STRelationship` for that chronicle. `False` for `None`. Game storytellers (`Chronicle.game_storytellers`) do not qualify. |

`is_st()` drives what the profile page and the notification badge treat as storyteller
work (see [dashboard](dashboard.md)). Authorization for an actual action does not use
either method: the views call `core.permissions.PermissionManager` (see
[authorization](../../docs/architecture/authorization.md)).

### Dashboard wrappers

`Profile.dashboard` is a property returning `accounts.dashboard.ProfileDashboard(self)`.
Each of the following methods delegates to the dashboard method of the same name and is
documented in [dashboard.md](dashboard.md):

`st_relations`, `my_characters`, `my_locations`, `my_items`, `xp_requests`, `xp_story`,
`xp_weekly`, `characters_to_approve`, `items_to_approve`, `locations_to_approve`,
`rotes_to_approve`, `objects_to_approve`, `freebies_to_approve`,
`character_images_to_approve`, `location_images_to_approve`, `item_images_to_approve`,
`get_updated_journals`, `get_unfulfilled_weekly_xp_requests`,
`get_unfulfilled_weekly_xp_requests_to_approve`, `xp_spend_requests`, `unread_scenes`.

Templates call these wrappers directly, for example `object.my_characters` in
`accounts/detail.html`. New selectors belong on `ProfileDashboard`; add a wrapper only
when a template or another app needs it on the profile.

### Other methods

- `__str__()` returns the username.
- `get_absolute_url()` reverses `accounts:profile` with the profile's own `pk`. The
  profile `pk` is not guaranteed to equal the user `pk`; link with
  `user.profile.get_absolute_url()` rather than building the URL from a user id.

## Profile creation signal

[`accounts/signals.py`](../signals.py) registers `create_user_profile` on `post_save`
for `User`. When a user is created it runs `Profile.objects.create(user=instance)` in the
same transaction as the user insert, so every user has a profile from the start and code
may read `user.profile` without a guard. `AccountsConfig.ready()` in
[`accounts/apps.py`](../apps.py) imports the module so the receiver is connected.

## Admin

[`accounts/admin.py`](../admin.py) registers `Profile` with `ProfileAdmin`, which lists
the `user` column only. Edit preferences through the default change form.

## Context processors

Both are listed in `TEMPLATES[0]["OPTIONS"]["context_processors"]` in
[`tg/settings/base.py`](../../tg/settings/base.py) and run on every template render
with a request.

### `theme_context`

For an authenticated user adds `user_theme` (`profile.theme`) and
`user_highlight_text` (`profile.highlight_text`). Anonymous requests get an empty dict.
The Spread base template reads `user.profile.theme` directly, so these two variables are
available but not required by the current templates.

### `notification_count`

Adds `notification_count` (an `int`) and `notification_breakdown` (a `dict` of label to
count, only positive counts) for authenticated users; anonymous users get `0` and `{}`.

- The values come from `ProfileDashboard(profile).notification_context()`.
- The result is cached with Django's cache under the key `notification_count_<user id>`
  for 60 seconds. Nothing invalidates the key early, so the badge can lag a change by up
  to a minute.
- Any exception while computing is logged at `WARNING` and the page renders with zero
  notifications, so a broken selector never takes a page down.

The navigation (`core/templates/core/tl/nav.html`) renders the badge and the breakdown.

## See also

- [Dashboard and profile page](dashboard.md)
- [accounts views and URLs](views-and-urls.md)
- [Authorization](../../docs/architecture/authorization.md)
- [Caching](../../docs/architecture/caching.md)
- [`game` models](../../game/docs/models.md) (`STRelationship`, `Chronicle`)
