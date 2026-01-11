from django.urls import include, path

from items import views

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "mummy_create"), namespace="create")),
    path("update/", include((update.urls, "mummy_update"), namespace="update")),
    path("list/", include((index.urls, "mummy_list"), namespace="list")),
    path("", include(detail.urls)),
]
