from django.urls import include, path

from . import ajax, create, detail, index, update

urls = [
    path("create/", include((create.urls, "mage_create"), namespace="create")),
    path("update/", include((update.urls, "mage_update"), namespace="update")),
    path("list/", include((index.urls, "mage_list"), namespace="list")),
    path("ajax/", include((ajax.urls, "mage_ajax"), namespace="ajax")),
    # Include list views directly (without /list/ prefix) for backwards compatibility
    path("", include(index.urls)),
    path("", include(detail.urls)),
]
