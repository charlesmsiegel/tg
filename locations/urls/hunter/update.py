from django.urls import path
from locations import views

app_name = "hunter:update"
urls = [
    path(
        "safehouse/<pk>/",
        views.hunter.SafehouseUpdateView.as_view(),
        name="safehouse",
    ),
    path(
        "hunting-ground/<pk>/",
        views.hunter.HuntingGroundUpdateView.as_view(),
        name="hunting_ground",
    ),
]
