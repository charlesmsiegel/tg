from django.urls import path
from items import views

app_name = "hunter:detail"
urls = [
    path(
        "gear/<pk>/",
        views.hunter.HunterGearDetailView.as_view(),
        name="gear",
    ),
    path(
        "relic/<pk>/",
        views.hunter.HunterRelicDetailView.as_view(),
        name="relic",
    ),
]
