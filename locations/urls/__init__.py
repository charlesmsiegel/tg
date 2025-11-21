from django.urls import include, path
from importlib import import_module
from locations import views

from core.constants import GameLine
from .core import create, detail, index, update

# Generate gameline URL patterns programmatically
urlpatterns = []

# Available gameline modules in locations app
AVAILABLE_GAMELINES = ["vampire", "werewolf", "mage", "wraith"]

for url_path, module_name, namespace in GameLine.URL_PATTERNS:
    # Only include gamelines that exist in this app
    if module_name in AVAILABLE_GAMELINES:
        try:
            gameline_module = import_module(f".{module_name}", package="locations.urls")
            urlpatterns.append(
                path(f"{url_path}/", include((gameline_module.urls, module_name), namespace=namespace))
            )
        except (ImportError, AttributeError):
            # Skip if module doesn't exist or doesn't have urls attribute
            pass

# Add core URL patterns
urlpatterns.extend([
    path("create/", include((create.urls, "locations_create"), namespace="create")),
    path("update/", include((update.urls, "locations_update"), namespace="update")),
    path("list/", include((index.urls, "locations_list"), namespace="list")),
    path("index/", views.core.LocationIndexView.as_view(), name="index"),
    path("", include(detail.urls)),
])
