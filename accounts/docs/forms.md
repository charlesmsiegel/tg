# accounts forms

This page documents every form in [`accounts/forms.py`](../forms.py): what it binds to,
its fields, the validation it adds and the method that persists it. Read it before
changing an auth page, the profile settings form, or an XP award form.

The auth and profile forms still add legacy CSS classes (`tg-form-control`,
`tg-form-check-input`) to their widgets. The Spread templates render fields through
`core/tl/field.html` and `accounts/includes/check_field.html`, which supply their own
markup (see [frontend](../../docs/architecture/frontend.md)).

## CustomAuthenticationForm

Subclass of Django's `AuthenticationForm` used by `CustomLoginView`. It only adds a
class and a placeholder to the `username` and `password` widgets; authentication is
unchanged.

## CustomUserCreationForm

Subclass of `UserCreationForm` used by `SignUp`.

| Field | Notes |
|-------|-------|
| `username` | Django's username field |
| `email` | `EmailField(required=False)` |
| `password1`, `password2` | Checked against `AUTH_PASSWORD_VALIDATORS` |

- `clean()` raises "Username and Email must be distinct" when both are given and equal.
- `save(commit=True)` copies `email` onto the user before saving.

## ProfileUpdateForm

`ModelForm` on `Profile` used by `ProfileUpdateView`. Fields: `preferred_heading`,
`theme`, `highlight_text`, `discord_id`, `lines`, `veils`, `discord_toggle`,
`lines_toggle`, `veils_toggle`. `discord_id` is optional. Validation beyond the field
choices comes from `Profile.clean()` (see [models](models.md#validation)).

## SceneXP

Plain `Form` for awarding scene XP; used by `ProfileView` (to render) and
`SceneXPAwardView` (to save).

- Constructor: `SceneXP(data=None, *, scene, prefix=...)`. The views use the prefix
  `scene_<scene pk>` so several scene forms can share one page.
- Fields: one optional `BooleanField` per player character in the scene
  (`scene.characters.player_characters()`), named after the character's `name`.
- `clean()` returns a `dict` mapping each `Character` (looked up by name among the
  scene's characters) to its boolean.
- `save()` calls `scene.award_xp(cleaned_data)`: 1 XP to each ticked character, then the
  scene is marked `xp_given`. It raises `ValidationError` if XP was already awarded.

Because fields are keyed by character name, two characters with the same name in one
scene share a field.

## StoryXP

Plain `Form` for awarding story XP. It is tested but not used by any view or template:
the profile page does not build story XP forms.

- Constructor: `StoryXP(data=None, *, story)`.
- For every `Human` with status `App` (across all chronicles) it adds
  `<name>-success`, `<name>-danger`, `<name>-growth`, `<name>-drama` (booleans) and
  `<name>-duration` (integer, default 0).
- `rows()` yields `(character, [bound fields in TOPICS order])` for a table layout.
- `clean()` returns `{character: {"success", "danger", "growth", "drama", "duration"}}`.
- `save()` calls `story.award_xp(cleaned_data)`, which awards
  `duration + one point per ticked category` to each character through
  `core.xp_utils.calculate_story_xp` and `award_xp_atomically`.

## FreebieAwardForm

Plain `Form` used by `ProfileView` (one per character awaiting freebie approval) and
`FreebieAwardView`.

- Constructor: `FreebieAwardForm(data=None, *, character)`.
- Field: `backstory_freebies`, `IntegerField(min_value=0, max_value=15, initial=0)`.
- `save()` calls `character.award_backstory_freebies(n)`, defined on
  `characters.models.core.human.Human`: it adds `n` to `freebies` and sets
  `freebies_approved=True` under a row lock, raising `ValidationError` if freebies were
  already approved.

## Forms from other apps used here

`WeeklyXPRequestForm` from [`game/forms.py`](../../game/forms.py) backs the weekly XP
request and approval cards on the profile. It is documented in
[game forms](../../game/docs/forms.md#weeklyxprequestform).

## See also

- [accounts views and URLs](views-and-urls.md)
- [authentication](authentication.md)
- [accounts templates](templates.md)
- [game XP](../../game/docs/xp.md)
