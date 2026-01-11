from django.urls import include, path

from characters import views

from . import ajax, create, detail, index, update

urls = [
    path("ajax/", include((ajax.urls, "changeling_ajax"), namespace="ajax")),
    path("create/", include((create.urls, "changeling_create"), namespace="create")),
    path("update/", include((update.urls, "changeling_update"), namespace="update")),
    path("list/", include((index.urls, "changeling_list"), namespace="list")),
    path("", include(detail.urls)),
]
