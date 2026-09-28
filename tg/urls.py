"""
URL configuration for tg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("core.urls", "core"), namespace="core")),
    path(
        "characters/",
        include(("characters.urls", "characters"), namespace="characters"),
    ),
    path("locations/", include(("locations.urls", "locations"), namespace="locations")),
    path("items/", include(("items.urls", "items"), namespace="items")),
    path("game/", include(("game.urls", "game"), namespace="game")),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    # Same paths and names as django.contrib.auth.urls, pointed at the site's own
    # templates: the default "registration/..." names resolve to django.contrib.admin's.
    path(
        "accounts/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Django Debug Toolbar (development only)
if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

# Custom error handlers
handler403 = "core.views.errors.error_403"
handler404 = "core.views.errors.error_404"
handler500 = "core.views.errors.error_500"
