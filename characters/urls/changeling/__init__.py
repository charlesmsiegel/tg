from characters import views
from django.urls import include, path

from . import create, detail, index, update

urls = [
    path("create/", include((create.urls, "changeling_create"), namespace="create")),
    path("update/", include((update.urls, "changeling_update"), namespace="update")),
    path("list/", include((index.urls, "changeling_list"), namespace="list")),
    path("", include(detail.urls)),
]
