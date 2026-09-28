"""Custom error views for handling HTTP errors with proper status codes."""

from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import loader


def error_403(request, exception=None):
    """
    Handle 403 Forbidden errors.

    This view is called when an authenticated user doesn't have permission
    to access a resource.
    """
    return render(request, "core/errors/403.html", status=403)


def error_404(request, exception=None):
    """
    Handle 404 Not Found errors.

    This view is called when a requested page doesn't exist.
    """
    return render(request, "core/errors/404.html", status=404)


def error_500(request):
    """
    Handle 500 Internal Server Error.

    This view is called when an unhandled exception occurs. Like Django's own
    ``server_error`` it renders without the request: context processors query the
    database (navigation, notifications) and may be what failed, so the page must
    not depend on them.
    """
    return HttpResponseServerError(loader.render_to_string("core/errors/500.html"))
