from django.urls import include, path

from characters import views

from . import ajax, create, detail, index, update

urls = [
    path("ajax/", include((ajax.urls, "wraith_ajax"), namespace="ajax")),
    path("create/", include((create.urls, "wraith_create"), namespace="create")),
    path("update/", include((update.urls, "wraith_update"), namespace="update")),
    path("list/", include((index.urls, "wraith_list"), namespace="list")),
    path("", include(detail.urls)),
]
