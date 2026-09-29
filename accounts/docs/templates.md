# accounts templates

This page lists the templates in [`accounts/templates/`](../templates/), which view
renders each one, the context it expects and the includes it pulls in. Read it before
changing the profile page, an auth page or the password-reset email.

All pages use the Spread design system: full pages extend `core/tl_base.html` and auth
pages extend `core/tl_auth.html`. Fields render through `core/tl/field.html`. See
[frontend](../../docs/architecture/frontend.md) for the shared components, and
[template tags](../../docs/reference/template-tags.md) for `tl` filters such as
`gameline_code`, `cover_title_class`, `type_label` and the `{% fact %}` tag.

## Pages

| Template | Rendered by | Notes |
|----------|-------------|-------|
| `accounts/detail.html` | `ProfileView` | Profile cover and tabbed pages; see below |
| `accounts/form.html` | `ProfileUpdateView` | Profile settings in two sections, "Display preferences" and "Privacy & safety" |
| `accounts/signup.html` | `SignUp` | Extends `core/tl_auth.html`; shows `non_field_errors` in the note area |
| `registration/login.html` | `CustomLoginView` (Django's default template name) | Posts to `{% url 'login' %}`, links to password reset and sign-up |
| `accounts/auth/password_reset_form.html` | `CustomPasswordResetView` | Email field only |
| `accounts/auth/password_reset_done.html` | `PasswordResetDoneView` (set in `tg/urls.py`) | |
| `accounts/auth/password_reset_confirm.html` | `PasswordResetConfirmView` | Shows the form when `validlink`, else an error and a link to request a new one |
| `accounts/auth/password_reset_complete.html` | `PasswordResetCompleteView` | Link to login |
| `accounts/auth/password_rules.html` | Included as `help_template` by the sign-up and confirm pages | Static list mirroring `AUTH_PASSWORD_VALIDATORS` |

## Emails

| Template | Used as |
|----------|---------|
| `accounts/registration/password_reset_email.txt` | `CustomPasswordResetView.email_template_name` (plain text body, `autoescape off`) |
| `accounts/registration/password_reset_email.html` | `CustomPasswordResetView.html_email_template_name` (HTML alternative, autoescaped, inline CSS) |
| `registration/password_reset_subject.txt` | Not used: Django resolves this name to `django.contrib.auth`'s own copy, which comes first in `INSTALLED_APPS` |

The email templates receive Django's password-reset context: `user`, `site_name`,
`domain`, `protocol`, `uid`, `token`. See
[authentication](authentication.md#password-reset).

The HTML email carries a `<style>` block and inline `style` attributes, which email
clients need; it is not a page and does not extend the Spread base.
[`core/tests/test_template_policy.py`](../../core/tests/test_template_policy.py) allows
the email's styles and fails if the site-wide count of inline styles grows.

## The profile page

`accounts/detail.html` fills these blocks of `core/tl_base.html`:

- `cover_title`: "Storyteller" or "Player", the join month, and the username in the
  profile's `preferred_heading` font (via `gameline_code`).
- `cover_body`: `accounts/includes/settings.html`, the rule list of preferences and
  safety settings. Theme, highlighting and heading show only to the owner. Discord,
  veils and lines show to the owner, to any viewer whose profile `is_st`, or to anyone
  when the matching toggle is on; the owner also sees whether each is public.
- `cover_actions`: "Edit profile" and a POST "Log out" button, for the owner only.
- `nav`: the tab bar. Chronicles and Journals appear only when `is_st`. The NEEDS YOU
  tab shows `needs_count`.
- `content`: one include per tab (context from `ProfileView`; see
  [dashboard](dashboard.md#profile-page)).

### Includes

All in `accounts/templates/accounts/includes/`. Each hides itself when its queue is
empty.

| Include | Used by | Shows |
|---------|---------|-------|
| `needs.html` | `detail.html` (tab `needs`) | The NEEDS YOU tab: the includes below, and an "Other queues" counter row |
| `character_approval.html` | `needs.html` | `characters_to_approve` as `approval_row.html` rows |
| `approval_row.html` | character, location and item approval includes | One object: name, chronicle, type and status, owner, Review and Approve (`accounts:object_approval`) |
| `location_approval.html`, `item_approval.html` | `needs.html` | Locations and items to approve |
| `rote_approval.html` | `needs.html` | `rotes_to_approve` with the mages that know each rote |
| `image_approval.html`, `image_row.html` | `needs.html` | Pending character, location and item images with Approve (`accounts:image_approval`) |
| `freebies.html` | `needs.html` | `freebie_forms` (storyteller's own profile only), posting to `accounts:freebie_award` |
| `xp_spend_requests.html` | `needs.html` | Characters with pending XP spends and their `pending_spendings`; Review opens the character's experience tab |
| `xp_summary.html` | `needs.html` | Counts from `weekly_xp_summary` and a button to the Experience tab |
| `attention.html` | `needs.html` | `scenes_waiting` with each scene's `st_message` |
| `active_scenes.html` | `needs.html` | `unread_scenes` with a "Mark read" button (`accounts:mark_scene_read`) |
| `characters.html`, `locations.html`, `items.html` | `detail.html` (tab `characters`) | Owned objects as tiles |
| `owned_tile.html` | the three above | One tile: type, status, name, concept, gameline |
| `chronicles.html` | `detail.html` (tab `chronicles`) | `object.st_relations` |
| `journals.html` | `detail.html` (tab `journals`) | `object.get_updated_journals` |
| `xp_weekly.html` | `detail.html` (tab `experience`) | `weekly_xp_request_forms`, posting to `accounts:weekly_xp_request` |
| `xp_weekly_st.html` | `detail.html` (tab `experience`, `st_queues`) | `weekly_xp_request_forms_to_approve`, posting to `accounts:weekly_xp_approval` |
| `xp_weekly_rows.html` | `xp_weekly.html`, `xp_weekly_st.html` | The four criterion checkboxes with their scene selects, and non-field errors |
| `xp_scene_st.html` | `detail.html` (tab `experience`, `st_queues`) | `scenexp_forms`, one card per scene, posting to `accounts:scene_xp_award` |
| `settings.html` | `detail.html` (cover) | Preferences and safety settings |
| `check_field.html` | `form.html` | A checkbox with its label, errors and help text |
| `xp_story.html`, `xp_story_st.html` | nothing | Story XP sections; no view supplies `story_xp_forms`, so they are not included anywhere |

## Conventions

- Keep every include self-hiding (`{% if queue %}...{% endif %}`) so `needs.html` can
  include them unconditionally.
- Do not add inline `style=""` or `<style>` blocks to page templates; the template policy
  test fails when either appears in a new place.
- Profile links elsewhere in the site should use `owner.profile.get_absolute_url`, since
  `accounts:profile` takes a profile primary key.

## See also

- [Dashboard and profile page](dashboard.md)
- [Authentication flows](authentication.md)
- [Frontend](../../docs/architecture/frontend.md)
- [Template tags](../../docs/reference/template-tags.md)
