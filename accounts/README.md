# accounts

The `accounts` app owns everything tied to a signed-in person rather than to a game
object: the `Profile` that extends Django's `User`, sign-up and the login and
password-reset pages, the profile page with its approval and experience queues, and the
POST endpoints storytellers use to approve objects and award experience. This page is the
entry point for developers and agents working in the app; the pages under
[`docs/`](docs/) are the detailed reference.

## Main concepts

- **Profile**: a one-to-one extension of `django.contrib.auth.models.User` holding display
  preferences (theme, heading font, text highlighting) and the player's safety settings
  (Discord ID, lines and veils, each with a visibility toggle). A `post_save` signal
  creates one for every new user.
- **Dashboard**: `accounts.dashboard.ProfileDashboard` computes the per-user queues
  (objects to approve, scenes awaiting XP, unread scenes, weekly XP requests) that the
  profile page and the navigation's notification badge show.
- **Profile page**: a tabbed page (`?tab=needs|characters|chronicles|experience|journals`)
  that opens on NEEDS YOU when something waits on the user.
- **Profile actions**: one POST-only view per action (approve, submit, return for
  revision, approve an image, award scene XP, award backstory freebies, file or approve a
  weekly XP request, mark a scene read). Each authorizes the caller, performs one service
  or model call and redirects with a flash message.

Terms such as ST (Storyteller), freebies and chronicle are defined in the
[glossary](../docs/reference/glossary.md).

## Key modules

| Path | Responsibility |
|------|----------------|
| [`models.py`](models.py) | `Profile` model: preferences, `is_st` / `is_st_for`, and thin wrappers around the dashboard selectors |
| [`dashboard.py`](dashboard.py) | `ProfileDashboard`: queue selectors and notification counts for one profile |
| [`views.py`](views.py) | Sign-up, login, password reset, the profile page and its update form, and the profile action endpoints |
| [`throttle.py`](throttle.py) | `AuthThrottleMixin`: cache-based throttle on POSTs to sign-up, login and password reset |
| [`forms.py`](forms.py) | Login and sign-up forms, `ProfileUpdateForm`, `SceneXP`, `StoryXP`, `FreebieAwardForm` |
| [`urls.py`](urls.py) | URL patterns under `/accounts/` in the `accounts` namespace |
| [`context_processors.py`](context_processors.py) | `theme_context` and `notification_count` (cached per user for 60 seconds) |
| [`signals.py`](signals.py) | Creates a `Profile` when a `User` is created |
| [`admin.py`](admin.py) | Registers `Profile` in the Django admin |
| [`apps.py`](apps.py) | `AccountsConfig`; imports `signals` in `ready()` |
| [`templates/accounts/`](templates/accounts/) | Profile page, profile form, sign-up and password-reset pages, the reset email |
| [`templates/registration/`](templates/registration/) | The login page and a password-reset subject template |
| [`tests/`](tests/) | Model, dashboard, form, view, context-processor and integration tests |

`accounts/migrations/` contains no migration files: a fresh database gets the tables from
the current models, and changes for older databases are applied by the `tg_schema` app
(see [schema migrations](../docs/architecture/schema-migrations.md)).

## How it connects to other apps

- **game**: `Profile.is_st` and `is_st_for` read `game.models.STRelationship` and
  `Chronicle.head_st`. The dashboard reads `Scene`, `Story`, `Week`, `WeeklyXPRequest`,
  `Journal` and `XPSpendingRequest`, and filters them with the read audiences in
  [`game/security.py`](../game/security.py). The weekly XP endpoints use
  `game.forms.WeeklyXPRequestForm` and `game.spending_approval.require_spending_approver`.
- **core**: approval, submission and revision go through
  `core.services.ApprovalService` ([`core/services/approval.py`](../core/services/approval.py));
  storyteller checks use `core.permissions.PermissionManager`. Route-level access for
  every view is declared in [`core/route_policy_manifest.py`](../core/route_policy_manifest.py)
  (`ACCOUNT` for the profile views and actions, `PUBLIC_READ` for sign-up, login and
  password reset). Pages extend `core/tl_base.html` or `core/tl_auth.html`.
- **characters, items, locations**: the dashboard lists owned and pending objects
  through the shared queryset helpers `owned_by`, `pending_approval_for_user`,
  `with_pending_images` and `for_user_chronicles` defined in
  [`core/models.py`](../core/models.py) and
  [`characters/models/core/character.py`](../characters/models/core/character.py).
- **tg**: [`tg/urls.py`](../tg/urls.py) mounts this app at `/accounts/`, adds the
  password-reset done/confirm/complete views with this app's templates, and includes
  `django.contrib.auth.urls` after them.

## Documentation

| Page | Contents |
|------|----------|
| [docs/models.md](docs/models.md) | `Profile` fields, validation, methods; the signal, admin and context processors |
| [docs/dashboard.md](docs/dashboard.md) | `ProfileDashboard` selectors, notification counts, the profile page tabs and NEEDS YOU |
| [docs/views-and-urls.md](docs/views-and-urls.md) | Every URL, view, permission check and redirect |
| [docs/authentication.md](docs/authentication.md) | Sign-up, login, logout, password reset and change |
| [docs/forms.md](docs/forms.md) | Every form in `forms.py` |
| [docs/templates.md](docs/templates.md) | Template inventory, includes and the password-reset email |

## Tests

Tests live in [`tests/`](tests/) and run with `python manage.py test accounts`. See
[testing](../docs/development/testing.md) for the runner and conventions.

| Path | Covers |
|------|--------|
| `tests/models/test_models.py` | Profile creation, ST helpers, queues, preferences, `__str__` |
| `tests/test_dashboard.py` | `ProfileDashboard` notifications and selectors, head-ST and staff scope, story XP queue |
| `tests/forms/test_forms.py` | Sign-up, login, profile, `SceneXP`, `StoryXP`, `FreebieAwardForm` |
| `tests/views/test_views.py` | Profile page, update view, IDOR protection, approval and XP workflows, login |
| `tests/views/test_profile_actions.py` | Each profile action endpoint |
| `tests/views/test_auth_redirects.py` | Login and logout redirect settings |
| `tests/views/test_password_reset.py` | Plain-text and HTML reset email |
| `tests/test_throttle.py` | Throttling of login, sign-up and password reset |
| `tests/context_processors/test_context_processors.py` | `theme_context`, `notification_count` |
| `tests/integration/test_integration.py` | The profile-creation signal |

## See also

- [Authorization](../docs/architecture/authorization.md)
- [XP and approvals](../docs/architecture/xp-and-approvals.md)
- [game app](../game/README.md)
- [core app](../core/README.md)
