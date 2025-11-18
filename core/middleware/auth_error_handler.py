"""
Middleware for handling authentication and authorization errors with proper HTTP status codes.

This middleware ensures that:
- Unauthenticated access to protected resources returns 401 (Unauthorized)
- Authenticated users without permission return 403 (Forbidden)
"""

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import resolve, reverse


class AuthErrorHandlerMiddleware:
    """
    Middleware to intercept authentication redirects and return proper error codes.

    When an unauthenticated user tries to access a protected view, Django's
    LoginRequiredMixin redirects to the login page. This middleware intercepts
    that redirect and returns a 401 error page instead.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if this is a redirect to the login page
        if isinstance(response, HttpResponseRedirect):
            login_url = settings.LOGIN_URL
            # Get the redirect location
            redirect_url = response.url

            # Check if redirecting to login and user is not authenticated
            if redirect_url.startswith(reverse(login_url)) and not request.user.is_authenticated:
                # Return 401 error instead of redirect
                return render(request, "core/errors/401.html", status=401)

        return response

    def process_exception(self, request, exception):
        """
        Handle PermissionDenied exceptions and return 403 error page.
        """
        if isinstance(exception, PermissionDenied):
            return render(request, "core/errors/403.html", status=403)
        return None
