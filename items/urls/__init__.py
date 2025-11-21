from django.urls import include, path
from importlib import import_module
from items import views

from core.constants import GameLine
from .core import create, detail, index, update

# Generate gameline URL patterns programmatically
urlpatterns = []

# Available gameline modules in items app
AVAILABLE_GAMELINES = ["vampire", "werewolf", "mage"]

for url_path, module_name, namespace in GameLine.URL_PATTERNS:
    # Only include gamelines that exist in this app
    if module_name in AVAILABLE_GAMELINES:
        try:
            gameline_module = import_module(f".{module_name}", package="items.urls")
            urlpatterns.append(
                path(f"{url_path}/", include((gameline_module.urls, module_name), namespace=namespace))
            )
        except (ImportError, AttributeError):
            # Skip if module doesn't exist or doesn't have urls attribute
            pass

# Add core URL patterns
urlpatterns.extend([
    path("create/", include((create.urls, "items_create"), namespace="create")),
    path("update/", include((update.urls, "items_update"), namespace="update")),
    path("list/", include((index.urls, "items_list"), namespace="list")),
    path("index/", views.core.ItemIndexView.as_view(), name="index"),
    path("", include(detail.urls)),
])
