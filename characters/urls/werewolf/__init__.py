from django.urls import include, path

from characters import views

from . import ajax, create, detail, index, update

urls = [
    path("ajax/", include((ajax.urls, "werewolf_ajax"), namespace="ajax")),
    path("create/", include((create.urls, "werewolf_create"), namespace="create")),
    path("update/", include((update.urls, "werewolf_update"), namespace="update")),
    path("list/", include((index.urls, "werewolf_list"), namespace="list")),
    path("", include(detail.urls)),
]
