from django.urls import path

from locations import views

app_name = "hunter:create"
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
