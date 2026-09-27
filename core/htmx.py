"""Small helpers for the htmx request/response contract (no django-htmx dependency).

A *fragment request* is an htmx request that expects a partial response. History
restoration and boosted navigation are htmx requests too, but they swap the whole
page, so they receive a full page.
"""

import json

from django.http import HttpResponse
from django.utils.cache import patch_vary_headers

FRAGMENT_HEADER = "TG-Fragment"


def is_htmx(request):
    return request.headers.get("HX-Request") == "true"


def is_fragment_request(request):
    return (
        is_htmx(request)
        and request.headers.get("HX-History-Restore-Request") != "true"
        and request.headers.get("HX-Boosted") != "true"
    )


def hx_redirect(url):
    """Ask htmx to navigate the whole page (a 3xx would be followed inside the XHR)."""
    response = HttpResponse(status=200)
    response["HX-Redirect"] = url
    return response


def mark_fragment(response, kind):
    """Label a partial so the client swap guard knows what it received."""
    response[FRAGMENT_HEADER] = kind
    return response


# Every request header is_fragment_request() reads: a cache must key on all of
# them, or a cached fragment could answer a history restore or boosted request.
FRAGMENT_REQUEST_HEADERS = ["HX-Request", "HX-History-Restore-Request", "HX-Boosted"]


def vary_on_htmx(response):
    patch_vary_headers(response, FRAGMENT_REQUEST_HEADERS)
    return response


def trigger(response, event, detail, *, header="HX-Trigger"):
    """Add a client event carrying JSON detail, keeping existing ones.

    ``HX-Trigger`` fires as soon as the response arrives, even if the client
    then cancels the swap; pass ``header="HX-Trigger-After-Swap"`` for events
    that must only follow content that was actually swapped in.
    """
    events = json.loads(response.get(header) or "{}")
    events[event] = detail
    response[header] = json.dumps(events)
    return response
