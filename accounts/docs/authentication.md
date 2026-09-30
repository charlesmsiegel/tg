# Authentication flows

This page describes how people sign up, log in, log out and reset or change their
password, which views and templates serve each step, and the settings they depend on.
Read it before changing an auth page, the reset email, or the auth URL routing.

The project uses Django's built-in `User` and auth views. The `accounts` app replaces
the forms and templates of the steps it customises; the rest come from
`django.contrib.auth.urls`.

## URL routing

[`tg/urls.py`](../../tg/urls.py) registers, in order:

1. `accounts/` → `accounts.urls` in the `accounts` namespace. This provides
   `accounts:signup`, `accounts:login` and `accounts:password_reset`.
2. `accounts/password_reset/done/`, `accounts/reset/<uidb64>/<token>/` and
   `accounts/reset/done/` → Django's `PasswordResetDoneView`,
   `PasswordResetConfirmView` and `PasswordResetCompleteView` with templates from
   `accounts/templates/accounts/auth/`. They keep Django's un-namespaced names
   (`password_reset_done`, `password_reset_confirm`, `password_reset_complete`).
3. `accounts/` → `django.contrib.auth.urls` (un-namespaced `login`, `logout`,
   `password_change`, `password_change_done`, `password_reset`, and the three above).

Django resolves a path to the first matching pattern, so `/accounts/login/` and
`/accounts/password_reset/` are served by this app's `CustomLoginView` and
`CustomPasswordResetView` even when reached through the un-namespaced names `login` and
`password_reset`. Step 2 exists because `django.contrib.admin` is earlier in
`INSTALLED_APPS` than `accounts` and ships templates named `registration/password_reset_*.html`;
without explicit template names the admin's versions would render.

Related settings in [`tg/settings/base.py`](../../tg/settings/base.py):

| Setting | Value |
|---------|-------|
| `LOGIN_URL` | `"login"` |
| `LOGIN_REDIRECT_URL` | `"core:home"` |
| `LOGOUT_REDIRECT_URL` | `"core:home"` |
| `PASSWORD_RESET_TIMEOUT` | env `PASSWORD_RESET_TIMEOUT`, default `3600` seconds |
| `DEFAULT_FROM_EMAIL` | env `DEFAULT_FROM_EMAIL`, default `noreply@tellurian-games.com` |
| `EMAIL_BACKEND` | env `EMAIL_BACKEND`, default the console backend |
| `AUTH_PASSWORD_VALIDATORS` | Django's four default validators |
| `AUTH_THROTTLE_LIMIT`, `AUTH_THROTTLE_CLIENT_LIMIT`, `AUTH_THROTTLE_WINDOW` | env, default `10` posts per account and `50` per address per `300` seconds (see [Throttling](#throttling)) |

See [settings](../../docs/reference/settings.md) for the email settings in full.

## Throttling

`SignUp`, `CustomLoginView` and `CustomPasswordResetView` use
`accounts.throttle.AuthThrottleMixin`. Every POST counts against a fixed window in the
cache, keyed on the view (`signup`, `login`, `password_reset`), the client address
(`REMOTE_ADDR`) and, for log in and password reset, the posted username or email
(trimmed, case-insensitive). Sign-up counts per address only. Once a key passes
`AUTH_THROTTLE_LIMIT` posts (default 10) in the current `AUTH_THROTTLE_WINDOW` (default
300 seconds) the view answers `429` with an empty form and the message "Too many
attempts. Please wait a few minutes and try again." The form is not run, so no password
is checked, no account is created and no email is sent. GET requests are not counted.
Log in and password reset also count every post from the address, whatever username or
email it names, against `AUTH_THROTTLE_CLIENT_LIMIT` (default 50), so rotating accounts
from one address does not escape the throttle. The windows are fixed, so a burst that
spans a window boundary can reach twice a limit.

- The counters live in the default cache (Redis in production). If the cache cannot
  count, the attempt is allowed.
- Behind a reverse proxy, `REMOTE_ADDR` is the proxy's address unless Daphne runs with
  `--proxy-headers`. Without it every visitor shares one address, so the sign-up limit
  and the per-address log-in and reset limits become site-wide.
- `client.login()` and `force_login()` in tests bypass the views and are never counted.
- The admin login (`/admin/login/`) and password change are not throttled.

## Sign up

`accounts.views.SignUp` (`/accounts/signup/`, route policy `PUBLIC_READ`) is a
`CreateView` with `accounts.forms.CustomUserCreationForm` and template
`accounts/signup.html`.

- Fields: username, email (optional), password, password confirmation.
- The form rejects a username equal to the email.
- On success the user is created (the signal creates the `Profile`), the view flashes
  "Account created successfully! Welcome to Tellurium Games." and redirects to
  `core:home`. The new user is not logged in automatically.

Because email is optional, a user who signs up without one cannot use the password
reset flow.

## Log in

`accounts.views.CustomLoginView` (`/accounts/login/`, `PUBLIC_READ`) is Django's
`LoginView` with `CustomAuthenticationForm`. It sets no `template_name`, so it renders
Django's default `registration/login.html`, which this app provides in
[`accounts/templates/registration/login.html`](../templates/registration/login.html).

- On success it flashes "Welcome back, <username>!" and redirects to the user's profile
  (`profile.get_absolute_url()`). `get_success_url` is overridden, so a `next` parameter
  is posted by the template but not followed.
- On failure it flashes "Invalid username or password." and re-renders the form.

When an anonymous user reaches a view guarded by `LoginRequiredMixin`,
`core.middleware.auth_error_handler.AuthErrorHandlerMiddleware` turns the redirect to
`LOGIN_URL` into a `401` page (`core/errors/401.html`) that links to login and sign-up.
Views under a login-requiring route policy answer `401` before the view runs.

## Log out

Logout is Django's `LogoutView` from `django.contrib.auth.urls` at `/accounts/logout/`.
It accepts POST only; the profile page's "Log out" button posts to `{% url 'logout' %}`.
After logout it redirects to `LOGOUT_REDIRECT_URL` (`core:home`).

## Password reset

| Step | URL | View | Template |
|------|-----|------|----------|
| Request | `/accounts/password_reset/` | `accounts.views.CustomPasswordResetView` | `accounts/auth/password_reset_form.html` |
| Email sent | `/accounts/password_reset/done/` | `PasswordResetDoneView` | `accounts/auth/password_reset_done.html` |
| Set new password | `/accounts/reset/<uidb64>/<token>/` | `PasswordResetConfirmView` | `accounts/auth/password_reset_confirm.html` |
| Done | `/accounts/reset/done/` | `PasswordResetCompleteView` | `accounts/auth/password_reset_complete.html` |

`CustomPasswordResetView` sends a multipart email:

- plain text from `accounts/registration/password_reset_email.txt`
  (`email_template_name`);
- HTML from `accounts/registration/password_reset_email.html`
  (`html_email_template_name`).

Both render the username, the site name, and the absolute link
`{{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}`.
The HTML version is autoescaped, so a username containing markup is shown as text
(`accounts/tests/views/test_password_reset.py` checks this).

The subject comes from `registration/password_reset_subject.txt`.
`CustomPasswordResetView` does not set `subject_template_name`, and
`django.contrib.auth` (earlier in `INSTALLED_APPS`) ships a template with that name, so
Django's own subject template is the one used, not the copy in
`accounts/templates/registration/`.

As with Django's default, the "email sent" page is shown whether or not an account
matches the address, so the form does not reveal which addresses are registered. The
confirm link expires after `PASSWORD_RESET_TIMEOUT` seconds or once used.

## Password change

`/accounts/password_change/` and `/accounts/password_change/done/` come from
`django.contrib.auth.urls` with no project override. They render the
`registration/password_change_*.html` templates shipped by `django.contrib.admin`, so
they use the admin's look rather than the site's.

## See also

- [accounts views and URLs](views-and-urls.md)
- [accounts templates](templates.md)
- [accounts forms](forms.md)
- [Settings reference](../../docs/reference/settings.md)
- [Security operations](../../docs/operations/security.md)
