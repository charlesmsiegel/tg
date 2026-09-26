from django.urls import path

from locations import views

urls = [
    path(
        "safehouse/",
        views.hunter.SafehouseCreateView.as_view(),
        name="safehouse",
    ),
    path(
        "hunting-ground/",
        views.hunter.HuntingGroundCreateView.as_view(),
        name="hunting_ground",
    ),
]
