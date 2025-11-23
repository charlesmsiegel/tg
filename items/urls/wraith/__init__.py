from django.urls import include, path

from . import create, detail, index, update

app_name = "wraith"
urlpatterns = [
    path("", include((index.urls, index.app_name))),
    path("detail/", include((detail.urls, detail.app_name))),
    path("create/", include((create.urls, create.app_name))),
    path("update/", include((update.urls, update.app_name))),
]
