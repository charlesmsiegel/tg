from django.urls import path

from locations import views
from locations.registry import registry

urls = registry.urls("hunter", "detail") + [
    path(
        "safehouse/",
        views.hunter.SafehouseListView.as_view(),
        name="safehouse-list",
    ),
    path(
        "hunting-ground/",
        views.hunter.HuntingGroundListView.as_view(),
        name="hunting-ground-list",
    ),
]
