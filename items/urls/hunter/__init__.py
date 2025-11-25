from django.urls import include, path

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "hunter_create"), namespace="create")),
    path("update/", include((update.urls, "hunter_update"), namespace="update")),
    path("list/", include((index.urls, "hunter_list"), namespace="list")),
    path("", include(detail.urls)),
]
