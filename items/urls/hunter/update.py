from django.urls import path

from items import views

app_name = "hunter:update"
urls = [
    path(
        "gear/<pk>/",
        views.hunter.HunterGearUpdateView.as_view(),
        name="gear",
    ),
    path(
        "relic/<pk>/",
        views.hunter.HunterRelicUpdateView.as_view(),
        name="relic",
    ),
]
