"""Explicit own-session projection, never a session credential or private profile."""

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.middleware.csrf import get_token


def session_state(request):
    data = {"authenticated": request.user.is_authenticated, "csrf_token": get_token(request)}
    if not request.user.is_authenticated:
        return data
    data["user"] = {"id": request.user.pk, "username": request.user.username}
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        data["profile"] = None
    else:
        data["profile"] = {
            "theme": profile.theme,
            "preferred_heading": profile.preferred_heading,
            "is_st": profile.is_st(),
        }
    browser_close = request.session.get_expire_at_browser_close()
    data["session"] = {
        "browser_close": browser_close,
        # A configured policy, not a remaining TTL: Redis can revoke early, and
        # get_expiry_date() on default sessions would imply a sliding expiry.
        "cookie_age_seconds": settings.SESSION_COOKIE_AGE,
    }
    return data
