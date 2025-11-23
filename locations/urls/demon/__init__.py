from django.urls import include, path

from . import create, detail, index, update

app_name = "demon"

urls = [
    path("create/", include((create.urls, "demon_create"), namespace="create")),
    path("update/", include((update.urls, "demon_update"), namespace="update")),
    path("list/", include((index.urls, "demon_list"), namespace="list")),
    path("", include(detail.urls)),
]
