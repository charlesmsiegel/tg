from django.urls import path
from locations import views

app_name = "hunter:detail"
urls = [
    path(
        "safehouse/<pk>/",
        views.hunter.SafehouseDetailView.as_view(),
        name="safehouse",
    ),
    path(
        "hunting-ground/<pk>/",
        views.hunter.HuntingGroundDetailView.as_view(),
        name="hunting_ground",
    ),
]
