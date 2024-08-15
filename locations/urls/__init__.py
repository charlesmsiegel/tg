from django.urls import include, path
from locations import views

from . import mage
from .core import create, detail, update

# Create your URLs here
urlpatterns = [
    path("mage/", include((mage.urls, "mage"), namespace="mage")),
    path("create/", include((create.urls, "locations_create"), namespace="create")),
    path("update/", include((update.urls, "locations_update"), namespace="update")),
    path("index/<gameline>/", views.core.LocationIndexView.as_view(), name="index"),
    path("", include(detail.urls)),
]
