from django.urls import include, path

from characters import views

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "mage_create"), namespace="create")),
    path("update/", include((update.urls, "mage_update"), namespace="update")),
    path("list/", include((index.urls, "mage_list"), namespace="list")),
    path("", include(detail.urls)),
]
