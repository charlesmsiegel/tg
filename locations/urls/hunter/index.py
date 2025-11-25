from django.urls import path
from locations import views

app_name = "hunter:list"
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
