from django.urls import path

from locations import views

urls = [
    path(
        "safehouses/",
        views.hunter.SafehouseListView.as_view(),
        name="safehouse",
    ),
    path(
        "hunting-grounds/",
        views.hunter.HuntingGroundListView.as_view(),
        name="hunting_ground",
    ),
]
