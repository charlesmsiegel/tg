from importlib import import_module

from django.urls import include, path

from characters import views
from core.constants import GameLine

from .core import ajax, create, detail, index, update

# Generate gameline URL patterns programmatically
urlpatterns = []

for url_path, module_name, namespace in GameLine.URL_PATTERNS:
    try:
        gameline_module = import_module(f".{module_name}", package="characters.urls")
        urlpatterns.append(
            path(
                f"{url_path}/",
                include((gameline_module.urls, module_name), namespace=namespace),
            )
        )
    except (ImportError, AttributeError):
        # Skip if module doesn't exist or doesn't have urls attribute
        pass

# Add core URL patterns
urlpatterns.extend(
    [
        path("ajax/", include((ajax.urls, "characters_ajax"), namespace="ajax")),
        path("create/", include((create.urls, "characters_create"), namespace="create")),
        path("update/", include((update.urls, "characters_update"), namespace="update")),
        path("list/", include((index.urls, "characters_list"), namespace="list")),
        path("index/", views.core.CharacterIndexView.as_view(), name="index"),
        path("retired/", views.core.RetiredCharacterIndex.as_view(), name="retired"),
        path("deceased/", views.core.DeceasedCharacterIndex.as_view(), name="deceased"),
        path("npc/", views.core.NPCCharacterIndex.as_view(), name="npc"),
        path("", include(detail.urls)),
    ]
)
