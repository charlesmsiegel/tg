"""Custom error views for handling HTTP errors with proper status codes."""

from django.shortcuts import render


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

    This view is called when an unhandled exception occurs.
    """
    return render(request, "core/errors/500.html", status=500)
