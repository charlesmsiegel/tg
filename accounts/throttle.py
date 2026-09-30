"""Throttle for the anonymous account forms: log in, sign up and password reset.

Each POST counts against a fixed window of ``AUTH_THROTTLE_WINDOW`` seconds, keyed on
the view's scope, the client address and, where the form names an account, that
username or email. Past ``AUTH_THROTTLE_LIMIT`` posts the view answers 429 with the
empty form and a message, without running the form: no password check, no account
created, no email sent. GET requests are never counted.

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
    window = settings.AUTH_THROTTLE_WINDOW
    account = hashlib.sha256(identifier.strip().lower().encode()).hexdigest()[:16]
    client = request.META.get("REMOTE_ADDR", "")
    key = f"auth-throttle:{scope}:{client}:{account}:{int(time.time() // window)}"
    cache.add(key, 0, window * 2)
    try:
        count = cache.incr(key)
    except ValueError:  # expired between add and incr
        return False
    return count is not None and count > settings.AUTH_THROTTLE_LIMIT


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
