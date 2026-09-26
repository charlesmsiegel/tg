from django.urls import include, path

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "vampire_create"), namespace="create")),
    path("update/", include((update.urls, "vampire_update"), namespace="update")),
    path("list/", include((index.urls, "vampire_list"), namespace="list")),
    path("", include(detail.urls)),
]
