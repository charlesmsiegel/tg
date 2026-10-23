"""Throttle anonymous account POSTs with a shared, weighted two-bucket counter.

The estimate is current_count + previous_count * (1 - elapsed / window). Buckets
live for two windows; rejected attempts also count. This smooths the reset boundary
but assumes attempts were distributed uniformly in the previous bucket: the error
is bounded by that bucket's count, not an exact rolling timestamp log.

Every counter failure refuses the attempt and logs an error. Existing sessions use
the database in production, so a cache outage blocks new authentication attempts
without discarding established sessions. All workers must share the default cache.

Forwarded addresses are read only from AUTH_THROTTLE_TRUSTED_PROXIES, walking from
the socket peer toward the first untrusted hop. The ASGI listener must be private
and any server-level proxy-header handling must trust only the actual proxy.
"""

import hashlib
import logging
import time
from ipaddress import ip_address, ip_network

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache

logger = logging.getLogger(__name__)

THROTTLED_MESSAGE = "Too many attempts. Please wait a few minutes and try again."


def trusted_proxy_networks():
    """Explicit proxy IPs/CIDRs; None and an empty list both trust no headers."""
    return tuple(ip_network(proxy) for proxy in settings.AUTH_THROTTLE_TRUSTED_PROXIES or [])


def client_address(request):
    """Resolve the client from the trusted end of a forwarded chain."""
    remote = request.META.get("REMOTE_ADDR", "")
    try:
        peer = ip_address(remote)
    except ValueError:
        return remote
    networks = trusted_proxy_networks()
    address = peer
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if not forwarded:
        return str(peer)
    for hop in reversed(forwarded.split(",")):
        if not any(address in network for network in networks):
            break
        try:
            address = ip_address(hop.strip())
        except ValueError:
            return str(peer)
    return str(address)


def attempt_throttled(scope, request, identifier=""):
    """Count an attempt, refusing it when either limit or the cache cannot allow it."""
    client = client_address(request)
    account = hashlib.sha256(identifier.strip().lower().encode()).hexdigest()[:16]
    over_account = over_limit(f"{scope}:{client}:{account}", settings.AUTH_THROTTLE_LIMIT)
    if not identifier:
        return over_account
    over_client = over_limit(f"{scope}:{client}", settings.AUTH_THROTTLE_CLIENT_LIMIT)
    return over_account or over_client


def over_limit(name, limit):
    """Count atomically and compare a weighted estimate of the last window."""
    window = settings.AUTH_THROTTLE_WINDOW
    bucket, elapsed = divmod(time.time(), window)
    key = f"auth-throttle:{name}:{int(bucket)}"
    previous_key = f"auth-throttle:{name}:{int(bucket) - 1}"
    try:
        for _ in range(2):
            cache.add(key, 0, window * 2)
            try:
                count = cache.incr(key)
                break
            except ValueError:  # expired/evicted between add and incr: retry once
                continue
        else:
            raise ValueError("Counter unavailable after retry")
        # Initializing the previous bucket lets None mean a failed read, not a miss.
        cache.add(previous_key, 0, window * 2)
        previous = cache.get(previous_key)
        if not isinstance(count, int) or not isinstance(previous, int):
            raise ValueError("Counter unavailable")
    except Exception:
        # Cache backends raise different exceptions; this boundary must fail closed.
        logger.exception("Authentication throttle cache unavailable; refusing attempt")
        return True
    return count + previous * (1 - elapsed / window) > limit


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
