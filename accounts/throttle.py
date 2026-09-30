"""Throttle for the anonymous account forms: log in, sign up and password reset.

Each POST counts against a fixed window of ``AUTH_THROTTLE_WINDOW`` seconds, keyed on
the view's scope, the client address and, where the form names an account, that
username or email. Past ``AUTH_THROTTLE_LIMIT`` posts the view answers 429 with the
empty form and a message, without running the form: no password check, no account
created, no email sent. GET requests are never counted.

A form that names an account also counts every post from the client address, whatever
account it names, against ``AUTH_THROTTLE_CLIENT_LIMIT``: rotating usernames or emails
gives each a fresh per-account counter, but not a fresh per-client one.

The windows are fixed, so a client can make up to twice the limit in a burst that spans
a window boundary. The counters live in the default cache, which must be shared by all
workers (Redis in production) or each worker counts on its own.

The client address is ``REMOTE_ADDR``. Behind a reverse proxy, run Daphne with
``--proxy-headers`` so it is the visitor's address rather than the proxy's.
"""

import hashlib
import time

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache

THROTTLED_MESSAGE = "Too many attempts. Please wait a few minutes and try again."


def attempt_throttled(scope, request, identifier=""):
    """Count one attempt; return True when this client is over the limit for ``scope``.

    Fails open: when the cache cannot count (an expired key, or a Redis outage that
    ``IGNORE_EXCEPTIONS`` turns into ``None``), the attempt is allowed.
    """
    client = request.META.get("REMOTE_ADDR", "")
    account = hashlib.sha256(identifier.strip().lower().encode()).hexdigest()[:16]
    over_account = over_limit(f"{scope}:{client}:{account}", settings.AUTH_THROTTLE_LIMIT)
    if not identifier:
        return over_account
    over_client = over_limit(f"{scope}:{client}", settings.AUTH_THROTTLE_CLIENT_LIMIT)
    return over_account or over_client


def over_limit(name, limit):
    """Count one post against the counter ``name``; True once it passes ``limit``."""
    window = settings.AUTH_THROTTLE_WINDOW
    key = f"auth-throttle:{name}:{int(time.time() // window)}"
    cache.add(key, 0, window * 2)
    try:
        count = cache.incr(key)
    except ValueError:  # expired between add and incr
        return False
    return count is not None and count > limit


class AuthThrottleMixin:
    """Throttle POSTs to a form view; list it before the Django view class.

    ``throttle_scope`` names the counter; ``throttle_field`` is the posted field that
    names the account (``None`` counts per client address only).
    """

    throttle_scope = None
    throttle_field = None

    def post(self, request, *args, **kwargs):
        identifier = request.POST.get(self.throttle_field, "") if self.throttle_field else ""
        if attempt_throttled(self.throttle_scope, request, identifier):
            return self.throttled_response()
        return super().post(request, *args, **kwargs)

    def throttled_response(self):
        messages.error(self.request, THROTTLED_MESSAGE)
        self.object = None  # CreateView's form kwargs and context read it
        form_kwargs = self.get_form_kwargs()
        form_kwargs.pop("data", None)
        form_kwargs.pop("files", None)
        context = self.get_context_data(form=self.get_form_class()(**form_kwargs))
        return self.render_to_response(context, status=429)
