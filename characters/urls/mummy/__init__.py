from django.urls import include, path

from . import detail

urls = [
    path("", include(detail.urls)),
]
